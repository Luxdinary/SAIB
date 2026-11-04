"""Build one HyperFrames project (a chapter of the long video, or a reel) from timed scenes.

Layers (z order): hairline grid, background clip or still (track 0), scrim, scene (track 1), marker and source bar
(track 3), head with kicker and chapter title (track 4), captions in 9:16 (track 5), chapter card (track 6),
voice (track 7), opening line or reel end card (track 8). Positions come from fmt.FORMATS.
"""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from . import blocks
from .blocks import Ctx, e

BRAND_DIR = Path(__file__).resolve().parents[1]
ROOT = BRAND_DIR.parents[1]
LIB = BRAND_DIR / "assets" / "higgsfield"
GSAP = ROOT / "assets" / "vendor" / "gsap.min.js"
FONTS = {
    "Display": BRAND_DIR / "assets" / "fonts" / "manrope" / "manrope-latin-wght-normal.woff2",
    "DisplayExt": BRAND_DIR / "assets" / "fonts" / "manrope" / "manrope-latin-ext-wght-normal.woff2",
    "Mono": BRAND_DIR / "assets" / "fonts" / "ibmplexmono" / "IBMPlexMono-Medium.ttf",
}
FONT_LICENSES = [BRAND_DIR / "assets" / "fonts" / "manrope" / "LICENSE-manrope.txt", BRAND_DIR / "assets" / "fonts" / "ibmplexmono" / "OFL.txt"]
LOGO = BRAND_DIR / "assets" / "logo" / "scutum-mark.svg"

PAL = {"bg": "#0b1120", "surface": "#121b2f", "text": "#e9eef8", "muted": "#a1adc4", "accent": "#4f8cff",
       "amber": "#ffd166", "red": "#ff6b6b", "green": "#2ec4b6", "violet": "#b07cff", "paper": "#fbfbfd",
       "paper_ink": "#141a24", "hairline": "rgba(226,232,246,0.12)"}
TAG = {"de": {"16x9": "KI-GENERIERT · SYNTHETISCHE STIMME", "9x16": "KI-GENERIERT · SYNTHETISCHE STIMME"},
       "en": {"16x9": "AI-GENERATED · SYNTHETIC VOICE", "9x16": "AI-GENERATED · SYNTHETIC VOICE"}}
SRC_WORD = {"de": "Quelle", "en": "Source"}
SCRIM = 0.62


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)


def _bg_html(sc: dict, project: Path, f: dict, tl: list, problems: list) -> list[str]:
    """Background media for one scene: a looping clip (repeated in segments) or a still with a slow push."""
    bg = sc.get("bg")
    if not bg:
        return []
    name = bg if isinstance(bg, str) else bg.get("file", "")
    src = (LIB / name) if not Path(name).is_absolute() else Path(name)
    if not src.exists() and src.suffix.lower() == ".mp4" and src.with_name(src.stem + ".start.png").exists():
        src = src.with_name(src.stem + ".start.png")         # clip not made yet: its start frame with a slow push (Bild vor Video)
    if not src.exists():
        problems.append(f"{sc['sid']}: background {name} missing; grid only")
        return []
    rel = f"assets/lib/{src.name}"
    _copy(src, project / rel)
    start, end = sc["start"], sc["end"]
    out = []
    if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        out.append(f'<img id="{sc["sid"]}-bg" class="clip bgm" src="{rel}" alt="" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="0">')
        tl.append(f'tl.fromTo("#{sc["sid"]}-bg",{{scale:1.0}},{{scale:1.06,duration:{end - start:.3f},ease:"none"}},{start:.3f});')
        return out
    seg = float(bg.get("loop_seconds", 8.0)) if isinstance(bg, dict) else 8.0
    t, k = start, 0
    while t < end - 0.05:
        d = min(seg, end - t)
        out.append(f'<video id="{sc["sid"]}-bg{k}" class="clip bgm" src="{rel}" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="0" data-media-start="0" data-volume="0" muted playsinline></video>')
        t += d
        k += 1
    return out


def _source_text(sc: dict, f: dict, lang: str) -> str:
    s = sc.get("source_short") if f["name"] == "9x16" and sc.get("source_short") else sc.get("source", "")
    return f"{SRC_WORD[lang]}: {s}" if s else ""


def build(seg: dict, fmt: dict, project: Path) -> dict:
    """seg: lang, total, scenes[], heads[], cards[], opening, endcard, captions[], voice, voice_start, title.
    Returns {"events": [...], "problems": [...]}."""
    f, lang = fmt, seg["lang"]
    W, H, X0 = f["W"], f["H"], f["X0"]
    if project.exists():
        shutil.rmtree(project)
    (project / "assets").mkdir(parents=True)
    for k, p in FONTS.items():
        _copy(p, project / "assets" / "fonts" / p.name)
    for p in FONT_LICENSES:
        _copy(p, project / "assets" / "fonts" / p.name)
    _copy(GSAP, project / "assets" / "vendor" / "gsap.min.js")
    _copy(LOGO, project / "assets" / "logo.svg")

    parts: list[str] = ['<div id="grid"></div>', '<div id="scrim"></div>']
    welt = seg.get("welt")                      # world of the week before (welt_scene.build_layer): stage, boot, drive
    _copy(BRAND_DIR / "assets" / "fonts" / "ibmplexmono" / "IBMPlexMono-Regular.ttf", project / "assets" / "fonts" / "IBMPlexMono-Regular.ttf")
    if welt:
        parts.append(welt["stage_html"])
    tl: list[str] = []
    events: list[float] = []
    problems: list[str] = []
    total = float(seg["total"])

    # scenes and their backgrounds
    for sc in seg["scenes"]:
        ctx = Ctx(sid=sc["sid"], start=sc["start"], end=sc["end"], f=f, lang=lang, words=sc.get("words", []))
        builder = blocks.BUILDERS.get(sc["type"])
        if builder is None:
            problems.append(f"{sc['sid']}: unknown scene type {sc['type']}")
            continue
        out = builder(ctx, sc.get("data") or {}, "assets/logo.svg") if sc["type"] == "close" else builder(ctx, sc.get("data") or {})
        problems += ctx.problems
        dur = sc["end"] - sc["start"]
        parts += _bg_html(sc, project, f, tl, problems)
        scrim = float(sc.get("scrim") if sc.get("scrim") is not None else (0.30 if sc["type"] == "broll" else SCRIM)) if sc.get("bg") else 0.0
        tl.append(f'tl.set("#scrim",{{opacity:{scrim:.2f}}},{sc["start"]:.3f});')
        parts.append(f'<div id="{sc["sid"]}" class="clip scene" data-start="{sc["start"]:.3f}" data-duration="{dur:.3f}" data-track-index="1"><div class="sc-in">{out.html}</div></div>')
        tl.append(f'tl.fromTo("#{sc["sid"]} .sc-in",{{opacity:0}},{{opacity:1,duration:0.45,ease:"power2.out"}},{sc["start"]:.3f});')
        tl.append(f'tl.to("#{sc["sid"]} .sc-in",{{opacity:0,duration:0.3,ease:"power2.in"}},{max(sc["start"] + 0.5, sc["end"] - 0.3):.3f});')
        tl += out.tl
        events += [sc["start"]] + out.events

        # marker capsule and source bar for the spoken passage of this scene
        for j, ms in enumerate(sc.get("marks", [])):
            mk, src_t = ms.get("marker"), _source_text(ms, f, lang)
            if not mk and not src_t:
                continue
            a, b = max(sc["start"], ms["start"]), min(sc["end"], ms["end"])
            if b - a < 0.8:
                continue
            inner = (f'<div class="mkcap">{blocks.mark_html(mk, lang)}</div>' if mk else "") + \
                    (f'<div class="srcbar">{html.escape(src_t)}</div>' if src_t else "")
            mid = f'{sc["sid"]}-m{j}'
            parts.append(f'<div id="{mid}" class="clip mlay" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">{inner}</div>')
            tl.append(f'tl.fromTo("#{mid} > *",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.35}},{a:.3f});')
            tl.append(f'tl.to("#{mid} > *",{{opacity:0,duration:0.25}},{max(a + 0.4, b - 0.25):.3f});')
            events.append(a)
            limit = 300 if f["name"] == "16x9" else 140
            if len(src_t) > limit:
                problems.append(f"{mid}: source line {len(src_t)} chars > {limit} for {f['name']}")

    # head: kicker (and title in 16:9) per chapter
    for i, hd in enumerate(seg.get("heads", [])):
        hid = f"head{i}"
        title = ""
        if f["title_px"] and hd.get("title"):
            title = f'<div class="hd-t">{e(hd["title"])}</div>'
        parts.append(f'<div id="{hid}" class="clip" data-start="{hd["start"]:.3f}" data-duration="{hd["end"] - hd["start"]:.3f}" data-track-index="4">'
                     f'<div class="hd"><div class="hd-k">{e(hd.get("kicker"))}</div>{title}</div></div>')
        tl.append(f'tl.fromTo("#{hid} .hd",{{opacity:0}},{{opacity:1,duration:0.4}},{hd["start"]:.3f});')
        if title:
            until = min(hd["end"] - 0.3, hd["start"] + float(hd.get("title_seconds", 8.0)))
            tl.append(f'tl.to("#{hid} .hd-t",{{opacity:0,duration:0.5}},{until:.3f});')

    if not welt:                                # the world draws its own voice tag in its HUD
        parts.append(f'<div id="tag">{html.escape(TAG[lang][f["name"]])}</div>')

    # realistic inserts (Higgsfield clip or still) over the scene, each labelled as AI depiction
    ins_label = {"de": "KI-GENERIERTE DARSTELLUNG · SYNTHETISCHE STIMME", "en": "AI-GENERATED DEPICTION · SYNTHETIC VOICE"}[lang]
    for i, ins in enumerate(seg.get("inserts", [])):
        name = ins["file"]
        src = (LIB / name) if not Path(name).is_absolute() else Path(name)
        if not src.exists():
            problems.append(f"insert {name} missing")
            continue
        rel = f"assets/lib/{src.name}"
        _copy(src, project / rel)
        iid, a, d = f"ins{i}", float(ins["start"]), float(ins["dur"])
        if src.suffix.lower() == ".mp4":
            media = (f'<video id="{iid}-v" class="clip insm" src="{rel}" data-start="{a:.3f}" data-duration="{d:.3f}" '
                     f'data-track-index="2" data-media-start="0" data-volume="0" muted playsinline></video>')
        else:
            media = f'<img id="{iid}-v" class="clip insm" src="{rel}" alt="" data-start="{a:.3f}" data-duration="{d:.3f}" data-track-index="2">'
            tl.append(f'tl.fromTo("#{iid}-v",{{scale:1.0}},{{scale:1.07,duration:{d:.3f},ease:"none"}},{a:.3f});')
        parts.append(media)
        parts.append(f'<div id="{iid}" class="clip insl" data-start="{a:.3f}" data-duration="{d:.3f}" data-track-index="9">'
                     f'<div class="ins-l">{html.escape(ins_label)}</div></div>')
        tl.append(f'tl.fromTo(["#{iid}-v","#{iid}"],{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.out"}},{a:.3f});')
        tl.append(f'tl.to(["#{iid}-v","#{iid}"],{{opacity:0,duration:0.35,ease:"power2.in"}},{a + d - 0.35:.3f});')
        events += [a, a + d]

    # chapter cards
    for i, cd in enumerate(seg.get("cards", [])):
        cid = f"card{i}"
        parts.append(f'<div id="{cid}" class="clip ccard" data-start="{cd["start"]:.3f}" data-duration="{cd["dur"]:.3f}" data-track-index="6">'
                     f'<div class="cc-in"><div class="cc-n">{e(cd.get("num"))}</div><div class="cc-t">{e(cd.get("title"))}</div></div></div>')
        tl.append(f'tl.fromTo("#{cid} .cc-in",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{cd["start"]:.3f});')
        tl.append(f'tl.to("#{cid}",{{opacity:0,duration:0.35}},{cd["start"] + cd["dur"] - 0.35:.3f});')
        events.append(cd["start"])

    # opening line (long video, chapter 0)
    op = seg.get("opening")
    if op:
        parts.append(f'<div id="opening" class="clip" data-start="{op["start"]:.3f}" data-duration="{op["end"] - op["start"]:.3f}" data-track-index="8">'
                     f'<div class="op">{html.escape(op["text"])}</div></div>')
        tl.append(f'tl.fromTo("#opening .op",{{opacity:0}},{{opacity:1,duration:0.4}},{op["start"]:.3f});')
        tl.append(f'tl.to("#opening .op",{{opacity:0,duration:0.4}},{op["end"] - 0.4:.3f});')

    # reel end card
    ec = seg.get("endcard")
    if ec:
        lines = "".join(f'<div class="ec-l ec{i}">{e(t)}</div>' for i, t in enumerate(ec["lines"]))
        parts.append(f'<div id="endcard" class="clip" data-start="{ec["start"]:.3f}" data-duration="{ec["dur"]:.3f}" data-track-index="8">'
                     f'<div class="ec-in"><img src="assets/logo.svg" alt="" class="ec-logo">{lines}</div></div>')
        tl.append(f'tl.fromTo("#endcard .ec-in",{{opacity:0}},{{opacity:1,duration:0.4}},{ec["start"]:.3f});')
        events.append(ec["start"])

    # captions (9:16 only)
    if f["captions"]:
        for i, g in enumerate(seg.get("captions", [])):
            words = "".join(f'<span class="w{" hl" if k == g.highlight else ""}">{html.escape(w.text)}</span> ' for k, w in enumerate(g.words))
            parts.append(f'<div id="cap{i}" class="clip cap" data-start="{g.start:.3f}" data-duration="{max(0.1, g.end - g.start):.3f}" data-track-index="5">'
                         f'<div class="cap-in">{words}</div></div>')

    # voice
    if seg.get("voice"):
        _copy(Path(seg["voice"]), project / "assets" / "voice.wav")
        vd = float(seg["voice_seconds"])
        parts.append(f'<audio id="voice" class="clip" src="assets/voice.wav" data-start="{seg["voice_start"]:.3f}" data-duration="{vd:.3f}" data-track-index="7" data-volume="1"></audio>')

    css = _css(f, seg)
    index = f"""<!doctype html>
<html lang="{lang}" data-resolution="{'landscape' if W > H else 'portrait'}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>{html.escape(seg.get('title', 'Scutoria'))}</title>
<script src="assets/vendor/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}" data-fps="30">
{chr(10).join(parts)}
</div>
{welt["boot_html"] if welt else ""}
<script>
const tl = gsap.timeline({{ paused: true }});
{welt["drive_js"] if welt else ""}
{chr(10).join(tl)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
    (project / "index.html").write_text(index, encoding="utf-8", newline="\n")
    (project / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": False}}, indent=2) + "\n", encoding="utf-8")
    (project / "meta.json").write_text(json.dumps({"id": project.name, "name": seg.get("title", "Scutoria")}) + "\n", encoding="utf-8")
    return {"events": sorted(set(round(x, 3) for x in events)), "problems": problems}


def _css(f: dict, seg: dict) -> str:
    W, H, X0 = f["W"], f["H"], f["X0"]
    p = PAL
    col = f["name"] == "9x16"
    return f"""
@font-face{{font-family:'FN Display';src:url('assets/fonts/{FONTS['Display'].name}') format('woff2');font-weight:100 900;font-display:block;}}
@font-face{{font-family:'FN Display';src:url('assets/fonts/{FONTS['DisplayExt'].name}') format('woff2');font-weight:100 900;font-display:block;unicode-range:U+0100-024F,U+1E00-1EFF,U+20A0-20CF,U+2C60-2C7F,U+A720-A7FF;}}
@font-face{{font-family:'FN Mono';src:url('assets/fonts/{FONTS['Mono'].name}') format('truetype');font-weight:400 600;font-display:block;}}
@font-face{{font-family:'Manrope';src:url('assets/fonts/{FONTS['Display'].name}') format('woff2');font-weight:200 800;font-display:block;}}
@font-face{{font-family:'Manrope';src:url('assets/fonts/{FONTS['DisplayExt'].name}') format('woff2');font-weight:200 800;font-display:block;unicode-range:U+0100-024F,U+1E00-1EFF;}}
@font-face{{font-family:'IBM Plex Mono';src:url('assets/fonts/IBMPlexMono-Regular.ttf') format('truetype');font-weight:400;font-display:block;}}
#welt{{z-index:4;}} #welt svg{{display:block;}}
.insm{{z-index:7;width:{W}px;height:{H}px;object-fit:cover;}}
.insl{{z-index:8;}}
.ins-l{{position:absolute;right:{X0}px;bottom:{f['tag_y']}px;font-family:'FN Mono';font-size:{f['tag_px']}px;letter-spacing:0.12em;color:#e9eef8;background:rgba(11,17,32,0.72);padding:6px 12px;border-radius:6px;}}
:root{{--bg:{p['bg']};--surface:{p['surface']};--text:{p['text']};--muted:{p['muted']};--accent:{p['accent']};--amber:{p['amber']};--red:{p['red']};
--green:{p['green']};--violet:{p['violet']};--paper:{p['paper']};--paper-ink:{p['paper_ink']};--hairline:{p['hairline']};}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);font-family:'FN Display',sans-serif;font-weight:400;color:var(--text);}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);}}
#grid{{position:absolute;inset:0;z-index:0;background-image:linear-gradient(var(--hairline) 1px,transparent 1px),linear-gradient(90deg,var(--hairline) 1px,transparent 1px);background-size:96px 96px;opacity:0.5;}}
.clip{{position:absolute;inset:0;}}
.bgm{{z-index:1;width:{W}px;height:{H}px;object-fit:cover;}}
#scrim{{position:absolute;inset:0;z-index:2;background:var(--bg);opacity:0;}}
.scene{{z-index:5;}}
.mlay,.ccard,#tag{{z-index:20;}}
.mkcap{{position:absolute;left:{X0}px;top:{f['marker_y']}px;display:inline-flex;align-items:center;padding:8px 18px;border-radius:999px;background:color-mix(in srgb,var(--surface) 92%,transparent);border:1px solid var(--hairline);font-size:{f['source_px']}px;}}
.srcbar{{position:absolute;left:{X0}px;width:{f['source_w']}px;top:{f['source_y']}px;font-family:'FN Mono';font-size:{f['source_px']}px;line-height:1.4;color:var(--muted);}}
.hd{{position:absolute;left:{X0}px;top:{f['kicker_y']}px;z-index:20;}}
.hd-k{{font-family:'FN Mono';font-size:{f['kicker_px']}px;letter-spacing:0.14em;text-transform:uppercase;color:var(--accent);}}
.hd-t{{font-family:'FN Display';font-weight:800;font-size:{f['title_px'] or 1}px;line-height:1.1;letter-spacing:-0.02em;margin-top:10px;}}
#tag{{position:absolute;right:{X0}px;top:{f['tag_y']}px;font-family:'FN Mono';font-size:{f['tag_px']}px;letter-spacing:0.12em;color:var(--muted);}}
.ccard{{z-index:40;background:var(--bg);}}
.cc-in{{position:absolute;left:{X0}px;right:{X0}px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;align-items:{'center' if col else 'flex-start'};text-align:{'center' if col else 'left'};gap:18px;}}
.cc-n{{font-family:'FN Mono';font-size:{40 if not col else 48}px;color:var(--accent);letter-spacing:0.1em;}}
.cc-t{{font-family:'FN Display';font-weight:800;font-size:{84 if not col else 76}px;line-height:1.08;letter-spacing:-0.02em;max-width:{W - 2 * X0}px;}}
#opening{{z-index:21;}}
.op{{position:absolute;left:{X0}px;top:{f['opening_y']}px;font-family:'FN Mono';font-size:{f['source_px']}px;color:var(--muted);}}
#endcard{{z-index:45;background:var(--bg);}}
.ec-in{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;text-align:center;padding:0 {X0}px;}}
.ec-logo{{width:96px;height:96px;margin-bottom:10px;}}
.ec-l{{font-size:44px;line-height:1.25;}}
.ec-l.ec0{{font-family:'FN Display';font-weight:800;font-size:56px;}}
.ec-l.ec2{{font-family:'FN Mono';font-size:28px;color:var(--muted);}}
.cap{{z-index:30;}}
.cap-in{{position:absolute;left:{(W - (f['cap_w'] or 800)) // 2}px;width:{f['cap_w'] or 800}px;bottom:{f['cap_bottom']}px;text-align:center;font-family:'FN Display';font-weight:800;font-size:{f['cap_px'] or 56}px;line-height:1.15;text-shadow:0 4px 24px rgba(0,0,0,0.55);}}
.cap-in .w.hl{{color:var(--accent);}}
{blocks.css(f)}
"""
