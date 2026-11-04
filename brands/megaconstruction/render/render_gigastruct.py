"""Gigastruct render: the shared direction pipeline (scripts/render_direction.py) plus the brand's 3D layer.

Nothing in src/fn or scripts/ is changed. The five Gigastruct scene types (gs_hook, gs_phases, gs_section,
gs_compare, gs_numbers) live in brands/megaconstruction/scenes.py and are loaded by the shared renderer itself
(fn.render.brand_scenes); this wrapper only
1. resolves word anchors ("@Wort+0.5") in the 3D keyframes of plan.layout.model3d from the word timings,
2. adds one persistent WebGL canvas (gigastruct3d.js, Three.js r170, MIT) under all scenes, driven by
   plan.layout.model3d and the HyperFrames seek protocol (the shared renderer has no hook for a brand layer yet),
3. writes the computed comparisons and the 3D/licence notes into manifest.json (storage and mirror).

Run (same arguments as render_direction.py):
  .venv\\Scripts\\python.exe brands\\megaconstruction\\render\\render_gigastruct.py data\\direction\\<id>.json --version V1 --tts gemini --mirror gigastruct/<name>
Dry run without video:  ... --version dry --tts mock --no-render
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from fn.render import assets as asset_layer  # noqa: E402
from fn.render import brand_scenes  # noqa: E402

_spec = importlib.util.spec_from_file_location("render_direction", ROOT / "scripts" / "render_direction.py")
rd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rd)

BRAND_DIR = HERE.parent
THREE_JS = BRAND_DIR / "assets" / "vendor" / "three.module.min.js"
THREE_LICENSE = BRAND_DIR / "assets" / "vendor" / "LICENSE-three.txt"
LAYER_JS = HERE / "gigastruct3d.js"
_STATE: dict = {}


def _norm(w: str) -> str:
    return re.sub(r"[^\wäöüßøæå]", "", w.lower())


def _word_time(captions, word: str, after: float) -> float | None:
    target = _norm(word)
    for g in captions:
        for w in g.words:
            if w.start >= after - 0.05 and _norm(w.text).startswith(target):
                return w.start
    return None


def _rel(spec, beat, captions, missing: list[str]) -> float | None:
    """Beat-relative seconds of a time spec: number (seconds), "%0.4" (share of the beat) or "@Wort+0.5" (spoken word)."""
    if isinstance(spec, (int, float)):
        return float(spec)
    word_spec = str(spec).strip()
    if word_spec.startswith("%"):   # share of the beat duration (language-independent 3D keyframes)
        return round(float(word_spec[1:]) * (beat.duration or 0), 3)
    m = re.match(r"^@?([^+\-]+)([+\-][\d.]+)?$", word_spec)
    if not m:
        return None
    t = _word_time(captions, m.group(1), beat.start)
    if t is None:
        missing.append(f"{beat.id}: word '{m.group(1)}' not found")
        return None
    return round(t - beat.start + float(m.group(2) or 0), 3)


def _resolve_words(plan, captions) -> list[str]:
    """Replace word anchors in the 3D keyframes by beat-relative seconds. Unresolved anchors are reported, never guessed."""
    missing: list[str] = []

    def rel(word_spec: str, beat) -> float | None:
        return _rel(word_spec, beat, captions, missing)

    m3 = (plan.layout or {}).get("model3d") or {}
    beats = {b.id: b for b in plan.beats}
    for bid, shot in (m3.get("shots") or {}).items():
        b = beats.get(bid)
        if b is None:
            continue
        for key, val in (shot.get("props") or {}).items():
            if isinstance(val, list):
                for kf in val:
                    if isinstance(kf, list) and isinstance(kf[0], str):
                        r = rel(kf[0], b)
                        kf[0] = r if r is not None else 0.0
        cam = shot.get("cam") or {}
        if isinstance(cam.get("seconds"), str):
            r = rel(cam["seconds"], b)
            cam["seconds"] = r if r is not None else None
    # status bar states may hang on a spoken word ("at": "@Wort+0.2"); the shared renderer only knows "offset" seconds
    for st in ((plan.layout or {}).get("status_bar") or {}).get("states", []):
        b = beats.get(st.get("beat"))
        if b is not None and isinstance(st.get("at"), str):
            r = rel(st["at"], b)
            st["offset"] = r if r is not None else st.get("offset", 0.3)
    return missing


def _shot_events(plan) -> list[float]:
    """Absolute times of 3D state changes (keyframes) for the visual-cuts check."""
    m3 = (plan.layout or {}).get("model3d") or {}
    out: list[float] = []
    for b in plan.beats:
        shot = (m3.get("shots") or {}).get(b.id) or {}
        for val in (shot.get("props") or {}).values():
            if isinstance(val, list):
                for kf in val[1:]:
                    if isinstance(kf, list) and isinstance(kf[0], (int, float)) and 0 < kf[0] < (b.duration or 0):
                        out.append(round(b.start + float(kf[0]), 3))
    return out


def _transitions(plan) -> dict:
    """Explainer transitions (beats[].overlay.transition) for the 3D layer, same defaults as fn.render.explainer."""
    zone_top = int((plan.layout or {}).get("zone_top", 290))
    out = {}
    for i, b in enumerate(plan.beats):
        tr = (getattr(b, "overlay", None) or {}).get("transition")
        if i > 0 and tr and tr.get("type") in ("iris", "blende"):
            out[b.id] = {"type": tr["type"], "seconds": float(tr.get("seconds", 0.7)),
                         "x": int(tr.get("x", 540)), "y": int(tr.get("y", zone_top + 450))}
    return out


def _drawing_layer(plan) -> str:
    """Format Bauaufgabe: drawing frame with tick marks and the chapter rail (state set per frame by gigastruct3d.js)."""
    ticks = "".join(f'<i style="left:{x}px"></i>' for x in range(100, 1000, 100)) + "".join(f'<b style="top:{y}px"></b>' for y in range(100, 1840, 100))
    chapters = ((plan.layout or {}).get("chapters") or {}).get("labels", [])
    rail = "".join(f"<div><b>{i + 1:02d}</b>{html.escape(c)}</div>" for i, c in enumerate(chapters))
    return f'\n<div id="gbframe">{ticks}</div>\n<div id="gbrail">{rail}</div>'


MEDIA_LABEL = {"de": "KI-Darstellung · kein Foto", "en": "AI depiction · not a photo"}


def _media_seconds(p: Path) -> float | None:
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def _media_layer(plan, captions, project_dir: Path, accent: str) -> dict:
    """Realistic Higgsfield stills and clips (Neustart 2026-11) between the 3D canvas and the scenes.

    plan.layout.media: [{beat, kind: video|image|strip, file | files[], from, to, box[l,t,w,h], move{scale,x,y},
    enter: cut|fade|swipe, exit: cut|fade|wipe, shade, label, label_y, marks[{x0,y0,x1,y1,text,at,out,tpos}]}] (tpos: label position along the line, 0..1).
    Files relative to brands/megaconstruction/<layout.media_folder>; each needs a licence line in LICENSE.md next to it.
    Times: seconds, "%share" or "@Wort+0.3" relative to the beat. Marks (dimension lines) move with the picture.
    """
    lay = plan.layout or {}
    items = lay.get("media") or []
    res = {"html": [], "tl": [], "events": [], "problems": [], "licenses": []}
    if not items:
        return res
    folder = BRAND_DIR / lay.get("media_folder", "assets/higgsfield")
    dst = project_dir / "assets" / "media"
    dst.mkdir(parents=True, exist_ok=True)
    beats = {b.id: b for b in plan.beats}
    missing: list[str] = []
    label_txt = MEDIA_LABEL.get(plan.language, MEDIA_LABEL["de"])

    def src(name: str) -> str | None:
        p = folder / name
        if not p.exists():
            res["problems"].append(f"media missing: {p}")
            return None
        lic = asset_layer._licenses(p.parent).get(p.name, "")
        if not lic:
            res["problems"].append(f"media without licence line in {p.parent / 'LICENSE.md'}: {p.name}")
        res["licenses"].append({"asset": f"media:{p.name}", "license": lic, "proof": str(p.parent / "LICENSE.md")})
        shutil.copy2(p, dst / p.name)
        return f"assets/media/{p.name}"

    for k, it in enumerate(items):
        b = beats.get(it.get("beat"))
        if b is None:
            res["problems"].append(f"media {k}: unknown beat {it.get('beat')}")
            continue
        r0 = _rel(it.get("from", 0), b, captions, missing)
        r1 = _rel(it.get("to", "%1"), b, captions, missing)
        if r0 is None or r1 is None or r1 <= r0:
            res["problems"].append(f"media {k} ({b.id}): bad interval {it.get('from')} .. {it.get('to')}")
            continue
        t0, t1 = round(b.start + r0, 3), round(b.start + r1, 3)
        dur = round(t1 - t0, 3)
        left, top, w, h = it.get("box", [0, 0, 1080, 1920])
        box = f"left:{left}px;top:{top}px;width:{w}px;height:{h}px"
        win = " gbm-win" if [left, top, w, h] != [0, 0, 1080, 1920] else ""
        kind = it.get("kind", "image")
        mid = f"gm{k}"
        attrs = f'data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="0"'
        if kind == "video":
            s = src(it["file"])
            if s is None:
                continue
            secs = _media_seconds(folder / it["file"])
            if secs is not None and dur > secs + 0.05:
                res["problems"].append(f"media {k} ({b.id}): {dur:.2f} s on screen but the clip has {secs:.2f} s")
            res["html"].append(f'<video id="{mid}" class="clip gbm{win}" src="{s}" {attrs} data-volume="0" muted playsinline style="{box}"></video>')
        elif kind == "strip":
            files = [src(f) for f in it.get("files", [])]
            if not files or None in files:
                continue
            tw = int(it.get("tile_w", round(h * 0.75)))
            gap = 16
            span = len(files) * tw + (len(files) - 1) * gap
            tiles = "".join(f'<img src="{f}" alt="" style="width:{tw}px;height:{h}px">' for f in files)
            res["html"].append(f'<div id="{mid}" class="clip gbm{win}" {attrs} style="{box}"><div class="gbm-strip" id="{mid}s" style="gap:{gap}px">{tiles}</div></div>')
            res["tl"].append(f'tl.fromTo("#{mid}s",{{x:0}},{{x:{-(span - w)},duration:{dur:.3f},ease:"none"}},{t0:.3f});')
        else:
            s = src(it["file"])
            if s is None:
                continue
            res["html"].append(f'<div id="{mid}" class="clip gbm{win}" {attrs} style="{box}"><img src="{s}" alt=""></div>')
        # overlay: shade for legibility, marks (move with the picture), label
        shade = float(it.get("shade", 0.0))
        marks_html = []
        for j, mk in enumerate(it.get("marks", [])):
            x0, y0, x1, y1 = (float(mk[c]) for c in ("x0", "y0", "x1", "y1"))
            import math
            ln, ang = math.hypot(x1 - x0, y1 - y0), math.degrees(math.atan2(y1 - y0, x1 - x0))
            mkid = f"{mid}m{j}"
            marks_html.append(f'<div class="gbm-mark" id="{mkid}" style="left:{x0 - left:.0f}px;top:{y0 - top:.0f}px;width:{ln:.0f}px;transform:rotate({ang:.2f}deg)">'
                              f'<i class="gbm-ml" id="{mkid}l"></i><b class="gbm-mt" id="{mkid}t" style="left:{float(mk.get("tpos", 0.5)) * 100:.0f}%">'
                              f'{html.escape(mk.get("text", ""))}</b></div>')
            ra = _rel(mk.get("at", 0.5), b, captions, missing)
            at = b.start + (ra if ra is not None else 0.5)
            res["tl"].append(f'tl.fromTo("#{mkid}l",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{at:.3f});')
            res["tl"].append(f'tl.fromTo("#{mkid}t",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{at + 0.35:.3f});')
            res["events"].append(round(at, 3))
            if mk.get("out") is not None:
                ro = _rel(mk["out"], b, captions, missing)
                if ro is not None:
                    res["tl"].append(f'tl.to("#{mkid}",{{opacity:0,duration:0.3}},{b.start + ro:.3f});')
        res["html"].append(f'<div id="{mid}m" class="clip gbm-marks{win}" {attrs} style="{box}">{"".join(marks_html)}</div>')
        lab = it.get("label", label_txt)
        shade_css = (f"background:linear-gradient(180deg,rgba(8,16,26,{shade:.2f}) 0%,rgba(8,16,26,{shade * 0.35:.2f}) 30%,"
                     f"rgba(8,16,26,{shade * 0.35:.2f}) 62%,rgba(8,16,26,{min(1.0, shade * 1.15):.2f}) 100%);") if shade else ""
        lab_html = f'<div class="gbm-label" style="top:{int(it.get("label_y", 1190))}px">{html.escape(lab)}</div>' if lab else ""
        res["html"].append(f'<div id="{mid}o" class="clip gbm-over" {attrs}><div class="gbm-shade" style="{box};{shade_css}"></div>{lab_html}</div>')
        mv = it.get("move") or {}
        if mv:
            frm = {key: mv[key][0] for key in ("scale", "x", "y") if key in mv}
            to = {key: mv[key][1] for key in ("scale", "x", "y") if key in mv}
            f_js = ",".join(f"{a}:{v}" for a, v in frm.items())
            t_js = ",".join(f"{a}:{v}" for a, v in to.items())
            res["tl"].append(f'tl.fromTo(["#{mid}","#{mid}m"],{{{f_js}}},{{{t_js},duration:{dur:.3f},ease:"sine.inOut"}},{t0:.3f});')
        sel = f'["#{mid}","#{mid}m","#{mid}o"]'
        enter, ex = it.get("enter", "fade"), it.get("exit", "fade")
        if enter == "fade":
            res["tl"].append(f'tl.fromTo({sel},{{opacity:0}},{{opacity:1,duration:0.5,ease:"power1.inOut"}},{t0:.3f});')
        elif enter == "swipe":
            res["tl"].append(f'tl.fromTo({sel},{{xPercent:100}},{{xPercent:0,duration:0.45,ease:"power3.out"}},{t0:.3f});')
        if ex == "fade":
            res["tl"].append(f'tl.to({sel},{{opacity:0,duration:0.5,ease:"power1.inOut"}},{t1 - 0.5:.3f});')
        elif ex == "wipe":   # the picture turns into the drawing: an orange scan line clears it from left to right
            wd = float(it.get("wipe_seconds", 0.9))
            res["html"].append(f'<div id="{mid}w" class="clip gbm-scan" {attrs} style="left:{left}px;top:{top}px;height:{h}px"></div>')
            res["tl"].append(f'tl.fromTo({sel},{{clipPath:"inset(0px 0px 0px 0px)"}},{{clipPath:"inset(0px 0px 0px {w}px)",duration:{wd:.2f},ease:"power1.inOut"}},{t1 - wd:.3f});')
            res["tl"].append(f'tl.fromTo("#{mid}w",{{x:0,opacity:1}},{{x:{w},opacity:1,duration:{wd:.2f},ease:"power1.inOut"}},{t1 - wd:.3f});')
            res["tl"].append(f'tl.set("#{mid}w",{{opacity:0}},0);')
            res["tl"].append(f'tl.set("#{mid}w",{{opacity:1}},{t1 - wd:.3f});')
            res["events"].append(round(t1 - wd, 3))
        res["events"] += [t0, round(t1 - 0.5, 3)]
    res["problems"] += [f"media anchor: {m}" for m in missing]
    res["css"] = f"""
.gbm{{position:absolute;z-index:2;overflow:hidden;object-fit:cover;transform-origin:50% 50%;}}
.gbm img{{width:100%;height:100%;object-fit:cover;display:block;}}
.gbm-win{{box-shadow:0 0 0 3px color-mix(in srgb,#E9EDF0 70%,transparent);}}
.gbm-strip{{position:absolute;left:0;top:0;display:flex;height:100%;}}
.gbm-strip img{{object-fit:cover;flex:none;}}
.gbm-marks{{position:absolute;z-index:2;pointer-events:none;transform-origin:50% 50%;}}
.gbm-mark{{position:absolute;height:0;transform-origin:0 0;}}
.gbm-ml{{position:absolute;left:0;top:-3px;width:100%;height:6px;background:{accent};transform-origin:0 50%;}}
.gbm-ml::before,.gbm-ml::after{{content:"";position:absolute;top:-17px;width:6px;height:40px;background:{accent};}}
.gbm-ml::before{{left:0;}}
.gbm-ml::after{{right:0;}}
.gbm-mt{{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);white-space:nowrap;font-family:'FN JetBrains Mono',monospace;font-weight:700;font-size:44px;color:#0f1d2b;background:{accent};padding:4px 14px;}}
.gbm-over{{position:absolute;inset:0;z-index:2;pointer-events:none;}}
.gbm-shade{{position:absolute;}}
.gbm-label{{position:absolute;left:84px;font-family:'FN JetBrains Mono',monospace;font-weight:700;font-size:24px;letter-spacing:0.08em;text-transform:uppercase;color:#E9EDF0;border:2px dashed color-mix(in srgb,#E9EDF0 75%,transparent);padding:5px 12px;background:rgba(8,16,26,0.72);}}
.gbm-scan{{position:absolute;z-index:2;width:8px;margin-left:-4px;background:{accent};box-shadow:0 0 0 2px rgba(8,16,26,0.4);}}
"""
    return res


_orig_build = rd.build_direction_project


def build_with_3d(plan, brand, captions, *, total, project_dir, voice_file=None, voice_start=0.0, outro=True, fps=30, title="", assets=None, **more):
    missing = _resolve_words(plan, captions)
    computed = brand_scenes.load(plan.brand_id).templates["gs_compare"].__globals__["COMPUTED"]
    computed.clear()
    bauaufgabe = (plan.layout or {}).get("format") == "bauaufgabe"
    if bauaufgabe:   # source line of every gb_* scene from its source_ids (labels), unless the plan sets data.src
        labels = {s.get("id"): s.get("label") or s.get("title", "") for s in plan.sources}
        for b in plan.beats:
            if b.scene_type.startswith("gb_") and b.source_ids and "_src" not in b.data:
                own = b.data.get("src")
                pre = ("Source: ", "Sources: ") if plan.language == "en" else ("Quelle: ", "Quellen: ")
                b.data["_src"] = own or pre[len(b.source_ids) > 1] + "; ".join(labels.get(i, i) for i in b.source_ids)
    build = _orig_build(plan, brand, captions, total=total, project_dir=project_dir, voice_file=voice_file, voice_start=voice_start,
                        outro=outro, fps=fps, title=title, assets=assets, **more)
    build.problems += [f"word anchor: {m}" for m in missing]
    m3 = (plan.layout or {}).get("model3d")
    if not m3:
        return build
    pal = brand.palette
    spec = {
        "palette": {**{"bg": pal["bg"], "accent": pal["accent"], "green": pal.get("signal_green", "#5CD08A")}, **(brand.design.get("model_palette") or {}), **(m3.get("palette") or {})},
        "beats": [{"id": b.id, "start": b.start, "end": round(b.start + b.duration, 3)} for b in plan.beats],
        "objects": m3.get("objects", []), "anchors": m3.get("anchors", {}), "shots": m3.get("shots", {}),
        "fov": m3.get("fov", 38), "fog": m3.get("fog"), "default_cam": m3.get("default_cam"),
        "transitions": _transitions(plan),
        "chapters": (plan.layout or {}).get("chapters"),
    }
    (project_dir / "assets" / "vendor").mkdir(parents=True, exist_ok=True)
    (project_dir / "assets" / "gs").mkdir(parents=True, exist_ok=True)
    shutil.copy2(THREE_JS, project_dir / "assets" / "vendor" / THREE_JS.name)
    shutil.copy2(THREE_LICENSE, project_dir / "assets" / "vendor" / THREE_LICENSE.name)
    shutil.copy2(LAYER_JS, project_dir / "assets" / "gs" / LAYER_JS.name)
    head = (f"<script>\nwindow.GS_SPEC = {json.dumps(spec, ensure_ascii=False)};\n"
            "window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};\n"
            "window.__hf.buildReady['gs3d'] = new Promise(function (r) { window.__gsReady = r; });\n"
            "window.addEventListener('hf-seek', function (e) { if (window.__gsRender) window.__gsRender(e.detail.time); else window.__gsPending = e.detail.time; });\n"
            "</script>\n</head>")
    idx = build.index
    page = idx.read_text(encoding="utf-8")
    page = page.replace("</head>", head, 1)
    page = page.replace('<div id="bg"></div>', '<div id="bg"></div>\n<canvas id="gs3dprev" width="1080" height="1920"></canvas>'
                        '\n<canvas id="gs3d" width="1080" height="1920"></canvas>\n<div id="gsshade"></div>' + (_drawing_layer(plan) if bauaufgabe else ""), 1)
    page = page.replace("</body>", '<script type="module" src="assets/gs/gigastruct3d.js"></script>\n</body>', 1)
    media = _media_layer(plan, captions, project_dir, pal["accent"])
    if media["html"]:
        anchor = '\n<div id="gbframe">' if bauaufgabe else '\n<div id="gsshade"></div>'
        page = page.replace(anchor, "\n" + "\n".join(media["html"]) + anchor, 1)
        page = page.replace("</head>", f"<style>{media['css']}</style>\n</head>", 1)
        marker = "window.__timelines = window.__timelines || {};"
        if marker not in page:
            build.problems.append("media: timeline marker not found, picture motion missing")
        page = page.replace(marker, "\n".join(media["tl"]) + "\n" + marker, 1)
    build.problems += media["problems"]
    idx.write_text(page, encoding="utf-8", newline="\n")
    build.events = sorted(set(build.events + _shot_events(plan) + media["events"]))
    _STATE["media_licenses"] = media["licenses"]
    _STATE["computed"] = list(computed)
    _STATE["word_anchor_problems"] = missing
    return build


def _overview(folder: Path, version: str, manifest: dict, report, sub: str) -> None:
    idx = folder / "index.html"
    if not idx.exists():
        idx.parent.mkdir(parents=True, exist_ok=True)
        idx.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Gigastruct Regie</title></head>'
                       '<body style="font-family:sans-serif;background:#0f1d2b;color:#e9edf0;padding:24px"><h1>Gigastruct · Vorlage und Testvideos</h1></body></html>',
                       encoding="utf-8")
    _orig_overview(folder, version, manifest, report, sub)


_orig_overview = rd._update_overview
rd.build_direction_project = build_with_3d
rd._update_overview = _overview


def _amend_manifest(plan_path: str, version: str, mirror: str) -> None:
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    vid = f"{plan['video_id']}-{version}"
    extra = {
        "computations": _STATE.get("computed", []) + list((plan.get("layout") or {}).get("computations", [])),
        "renderer_extension": {"wrapper": "brands/megaconstruction/render/render_gigastruct.py", "scenes": "brands/megaconstruction/scenes.py",
                               "layer_3d": "brands/megaconstruction/render/gigastruct3d.js",
                               "library": "three.js r170 (npm three@0.170.0), MIT, brands/megaconstruction/assets/vendor/LICENSE-three.txt"},
        "imagery": "Stilisierte 3D-Modelle aus Grundkörpern (Architekturmodell-Optik), keine fotorealistischen Abbildungen realer Bauwerke, "
                   "keine Fotos oder KI-Bilder; Querschnitt schematisch. Keine Offenlegung nach Art. 50 Abs. 4 AI Act über das KI-Label hinaus erforderlich "
                   "(Leitlinien C(2026) 5054: stilisierte Darstellungen sind keine Deepfakes).",
    }
    if (plan.get("layout") or {}).get("media"):   # Neustart 2026-11: realistic Higgsfield pictures, Format-Bibel rule 9 lifted by Stefan
        extra["imagery"] = ("Stilisierte 3D-Modelle aus Grundkörpern und realistische KI-Bilder/-Clips (Higgsfield). Darstellungen des realen "
                            "Bauwerks tragen im Bild die Plakette 'KI-Darstellung · kein Foto' und werden nie als Foto ausgegeben; "
                            "KI-Label dauerhaft. Regel 9 der Format-Bibel durch Stefans Vorgabe vom 02.11.2026 aufgehoben.")
    for folder in (rd.STORAGE_DIR / "direction" / vid, rd.mirror_dir() / "_Demos" / Path(mirror)):
        mf = folder / "manifest.json"
        if not mf.exists():
            continue
        m = json.loads(mf.read_text(encoding="utf-8"))
        m.update(extra)
        m.setdefault("licenses", []).append({"asset": "lib:three.js r170", "license": "MIT", "proof": "brands/megaconstruction/assets/vendor/LICENSE-three.txt"})
        m["licenses"] += _STATE.get("media_licenses", [])
        mf.write_text(json.dumps(m, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    version = args[args.index("--version") + 1] if "--version" in args else "A"
    mirror = args[args.index("--mirror") + 1] if "--mirror" in args else "scutoria-regie/fassung-a"
    sys.argv = [str(ROOT / "scripts" / "render_direction.py"), *args]
    code = rd.main()
    if code == 0 and "--no-render" not in args:
        _amend_manifest(args[0], version, mirror)
    sys.exit(code)
