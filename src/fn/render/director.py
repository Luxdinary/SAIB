"""Director composer: renders a `DirectionPlan` into a HyperFrames project using the five scene templates.

Sits next to `compose.build_project` (Phase-1 single-template layout) and reuses its font, background
and caption helpers. Nothing in the Phase-1 pipeline imports this module; the direction pipeline
(`scripts/render_prototype.py`, later `fn.cli direct`) does.

Layout differences to the Phase-1 layout (all per docs/direction-system.md):
- scene zone y 320..1200 (focus in the upper middle of the frame, one dominant motif per scene)
- captions anchored 560 px from the bottom (y 1360) so they never cover the scene zone
- logo small (wordmark 40 px), no scene counter, progress bar at the very bottom above the AI label
"""
from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from ..brands import Brand
from ..config import ASSETS_DIR
from ..direction.story import Beat, DirectionPlan
from .compose import (CaptionGroup, FONT_FILES, GSAP_FILE, W, H, TITLE_SAFE_X, TITLE_SAFE_W, AI_LABEL_BOTTOM,
                      _bg_pattern_css, _font_face_css, fit_font_size)
from .ffmpeg import audio_duration as ffmpeg_audio_duration
from .templates import SceneCtx, scene_css
from .templates_file import file_css, AMBER, RED
from ..config import ROOT
from . import assets as asset_layer
from . import brand_scenes
from . import explainer

DEFAULT_LAYOUT = {"zone_top": 290, "zone_h": 910, "caption_bottom_px": 560, "progress_y": 1724, "logo_px": 40}
# The AI label must stay above the TikTok/Reels description block (Prüfrunde 03.11.2026, R1): at least 430 px from the
# bottom (y <= ~1460), between the captions (y ~1360) and the platform UI; plans with a lower value are lifted.
AI_LABEL_MIN_BOTTOM = 430


@dataclass
class DirectionBuild:
    index: Path
    events: list[float]
    problems: list[str] = field(default_factory=list)   # template-level findings (text limits, schematic UI)
    scene_types: list[str] = field(default_factory=list)
    art50_seconds: float = 0.0                          # EU AI Act Art. 50 disclosure card shown at the start
    named_events: dict = field(default_factory=dict)    # {beat id: {event name: absolute time}} from SceneOut.named_events (sound cues)


def assign_timing(plan: DirectionPlan, words: list, *, first_start: float, outro_start: float, lead: float = 0.15) -> None:
    """Fill beat.start/duration from word timings (absolute video time); beats are consecutive and gap-free."""
    counts = [len(b.spoken.split()) for b in plan.beats]
    starts: list[float] = []
    idx = 0
    for n in counts:
        starts.append(words[idx].start if idx < len(words) else (starts[-1] + 1.0 if starts else first_start))
        idx += n
    for i, b in enumerate(plan.beats):
        start = first_start if i == 0 else max(first_start, starts[i] - lead)
        end = outro_start if i == len(plan.beats) - 1 else max(start + 1.0, starts[i + 1] - lead)
        b.start, b.duration = round(start, 3), round(end - start, 3)


def build_direction_project(plan: DirectionPlan, brand: Brand, captions: list[CaptionGroup], *, total: float,
                            project_dir: Path, voice_file: Path | None = None, voice_start: float = 0.0,
                            outro: bool = True, fps: int = 30, title: str = "",
                            assets: "asset_layer.AssetSet | None" = None, sfx_in_project: bool = True) -> DirectionBuild:
    """`assets` (Fassung B): background clip per scene type and hero clip per beat, placeholders allowed.
    `sfx_in_project=False` keeps the plan's `assets.sfx` files out of the HyperFrames audio: the sound layer
    (fn.render.sound) mixes them itself and replaces the rendered audio track."""
    aset = assets          # the local name `assets` below is the project's asset folder
    b = brand
    pal = b.palette
    fonts = b.fonts
    display = fonts.get("display", {}).get("family", "Inter")
    display_w = int(fonts.get("display", {}).get("weight", 800))
    body = fonts.get("body", {}).get("family", "Inter")
    mono = (fonts.get("mono") or {}).get("family") or "JetBrains Mono"
    sub = b.subtitle_style or {}
    cap_font = sub.get("font_family", body)
    cap_weight = sub.get("font_weight", 700)
    cap_size = int(sub.get("font_size_px", 58))
    cap_min = int(sub.get("min_font_size_px", 42))
    layout = {**DEFAULT_LAYOUT, **(plan.layout or {})}
    cap_transform = layout.get("caption_transform", sub.get("text_transform", "none"))
    cap_upper = cap_transform == "uppercase"
    cap_width = int(layout.get("caption_width_px", sub.get("position", {}).get("max_width_px", 900)))
    zone_top, zone_h = int(layout["zone_top"]), int(layout["zone_h"])
    cap_bottom = int(layout["caption_bottom_px"])
    tempo = b.design.get("tempo", "medium")
    enter = {"snappy": 0.18, "chaotic": 0.15, "punchy": 0.2, "slow": 0.4, "gentle": 0.4, "epic": 0.35}.get(tempo, 0.25)
    lang = plan.language
    outro_s = float(b.outro.get("seconds", 4.0)) if outro else 0.0
    outro_start = total - outro_s

    project_dir.mkdir(parents=True, exist_ok=True)
    assets = project_dir / "assets"
    (assets / "fonts").mkdir(parents=True, exist_ok=True)
    (assets / "vendor").mkdir(parents=True, exist_ok=True)
    used_fonts = {display, body, mono, cap_font}
    font_css = _brand_font_css(b, used_fonts, assets)
    flat = bool(b.design.get("flat"))
    logo_cfg = b.design.get("logo") or {}
    logo_src = ""
    if logo_cfg.get("file") and (ROOT / logo_cfg["file"]).exists():
        (assets / "logo").mkdir(exist_ok=True)
        shutil.copy2(ROOT / logo_cfg["file"], assets / "logo" / Path(logo_cfg["file"]).name)
        logo_src = f"assets/logo/{Path(logo_cfg['file']).name}"
    if GSAP_FILE.exists():
        shutil.copy2(GSAP_FILE, assets / "vendor" / "gsap.min.js")
        gsap_src = "assets/vendor/gsap.min.js"
    else:
        gsap_src = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
    voice_rel = None
    if voice_file and Path(voice_file).exists():
        voice_file = Path(voice_file)
        voice_rel = f"assets/{voice_file.name}"
        if voice_file.resolve() != (assets / voice_file.name).resolve():
            shutil.copy2(voice_file, assets / voice_file.name)

    parts: list[str] = ['<div id="bg"></div>'] + ([] if bool(b.design.get("flat")) else ['<div id="light"></div>'])
    tl: list[str] = []
    events: list[float] = []
    problems: list[str] = []
    # calm background motion over the whole video: grid parallax + a soft light gradient crossing the frame
    tl.append(f'tl.fromTo("#bg",{{x:-40,y:-30}},{{x:40,y:30,duration:{total:.3f},ease:"none"}},0);')
    if not flat:
        tl.append(f'tl.fromTo("#light",{{x:-300,y:-500,opacity:0.5}},{{x:300,y:500,opacity:0.5,duration:{total:.3f},ease:"sine.inOut"}},0);')

    # brand-wide layer (brands/<id>/scenes.py LAYER): e.g. one canvas under all scenes
    layer = brand_scenes.layer_for(b.id, plan, b, project_dir, captions)
    if layer.get("under_scenes_html"):
        parts.append(layer["under_scenes_html"])
    events += [float(e) for e in layer.get("events", [])]
    problems += [f"layer: {p}" for p in layer.get("problems", [])]

    # asset layer (Fassung B): clips or placeholders on track 0, scrim above them
    clip_src: dict[str, str] = {}
    if aset and aset.enabled:
        clip_src = asset_layer.copy_assets(aset, project_dir / "assets")
        parts.append('<div id="scrim"></div>')
    if aset and (aset.enabled or aset.sfx or aset.problems):
        problems += [f"assets: {p}" for p in aset.problems]

    # persistent layer: small logo, AI label, progress bar
    wordmark = logo_cfg.get("wordmark_text", b.name) if logo_src else b.name
    mark_html = f'<img class="logo-img" src="{logo_src}" alt="">' if logo_src else '<span class="mark"></span>'
    parts.append(f'<div id="logo" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="4">'
                 f'<div class="logo-inner{" brandmark" if logo_src else ""}">{mark_html}<span class="wordmark">{html.escape(wordmark)}</span></div></div>')
    tl.append('tl.fromTo("#logo .logo-inner",{opacity:0,y:-8},{opacity:1,y:0,duration:0.3},0.05);')
    if not ((b.design.get("explainer") or {}).get("ai_label_in_tag") and explainer.enabled(b, plan)):
        parts.append(f'<div id="ailabel">{html.escape(b.ai_label(lang))}</div>')
    # Art. 50 disclosure (brands/<id>/intro_config.json art50_disclosure.enabled): a card in the first seconds
    art50 = b.intro.get("art50_disclosure", {}) or {}
    art50_s = float(art50.get("seconds", 2.5)) if art50.get("enabled") else 0.0
    if art50_s:
        a_text = (art50.get("text", {}) or {}).get(lang, "KI-generierte Darstellung." if lang == "de" else "AI-generated depiction.")
        parts.append(f'<div id="art50" class="clip" data-start="0" data-duration="{art50_s:.2f}" data-track-index="6">'
                     f'<div class="art50-inner">{html.escape(a_text)}</div></div>')
        tl.append('tl.fromTo("#art50 .art50-inner",{opacity:0},{opacity:1,duration:0.2},0);')
        tl.append(f'tl.to("#art50 .art50-inner",{{opacity:0,duration:0.2}},{max(0.2, art50_s - 0.2):.2f});')
    parts.append('<div id="progress"><div id="progress-fill"></div></div>')
    tl.append(f'tl.fromTo("#progress-fill",{{scaleX:0}},{{scaleX:1,duration:{total:.3f},ease:"none"}},0);')

    # status bar (A2): the file and its upload state, changing per beat (amber = open question, red = block)
    sbar = layout.get("status_bar") or {}
    if sbar.get("states"):
        beat_start = {bt.id: bt.start for bt in plan.beats if bt.start is not None}
        states = [st for st in sbar["states"] if st.get("beat") in beat_start]
        spans = "".join(f'<span class="st st-{st.get("tone", "muted")}" id="st{k}">{html.escape(st.get("text", ""))}</span>' for k, st in enumerate(states))
        parts.append(f'<div id="status"><span class="st-file"><span class="st-icon">&#9638;</span>{html.escape(sbar.get("file", ""))}</span><span class="st-states">{spans}</span></div>')
        tl.append('tl.fromTo("#status",{opacity:0,y:10},{opacity:1,y:0,duration:0.3},0.1);')
        for k, st in enumerate(states):
            at = float(beat_start[st["beat"]]) + float(st.get("offset", 0.3))
            tl.append(f'tl.set("#st{k}",{{opacity:0}},0);')
            tl.append(f'tl.to("#st{k}",{{opacity:1,duration:0.25}},{at:.3f});')
            if k + 1 < len(states):
                nxt = float(beat_start[states[k + 1]["beat"]]) + float(states[k + 1].get("offset", 0.3))
                tl.append(f'tl.to("#st{k}",{{opacity:0,duration:0.2}},{max(at + 0.3, nxt - 0.2):.3f});')

    # explainer layer (head, voice tag, marker, source bar, transitions): brand.yaml explainer.enabled or plan.layout.explainer
    xpl = None
    if explainer.enabled(b, plan):
        xpl = explainer.build(plan, b, captions, total=total, outro_start=outro_start if outro else total, pal=pal,
                              display=display, display_w=display_w, mono=mono, zone_top=zone_top, lang=lang)
        parts += xpl.html
        tl += xpl.tl
        events += xpl.events
        problems += [f"explainer: {p}" for p in xpl.problems]

    # beats -> scenes
    scene_types: list[str] = []
    named_events: dict[str, dict[str, float]] = {}
    all_words = [w for g in captions for w in g.words]
    for i, beat in enumerate(plan.beats):
        if beat.start is None or beat.duration is None:
            raise ValueError(f"beat {beat.id} has no timing; call assign_timing first")
        template = brand_scenes.template_for(b.id, beat.scene_type)
        if template is None:
            raise ValueError(f"beat {beat.id}: unknown scene type {beat.scene_type}")
        sid = f"b{i + 1}"
        beat_words = [w for w in all_words if beat.start <= w.start < beat.start + beat.duration]
        ctx = SceneCtx(sid=sid, start=beat.start, duration=beat.duration, pal=pal, display_font=display, body_font=body,
                       mono_font=mono, zone_top=zone_top, zone_h=zone_h, enter=enter, lang=lang, flat=flat, words=beat_words)
        out = template(ctx, beat.data)
        named = getattr(out, "named_events", None) or {}
        if named:
            named_events[beat.id] = {str(k): float(v) for k, v in named.items()}
        if aset and aset.enabled:
            bgc = aset.background_for(beat.scene_type)
            if bgc is not None:
                if bgc.placeholder:
                    parts.append(asset_layer.placeholder_html(sid, beat.scene_type, beat.start, beat.duration, pal["accent"]))
                else:
                    parts.append(asset_layer.background_clip_html(sid, clip_src[bgc.name], beat.start, beat.duration))
            hero = aset.hero_for(beat.id)
            if hero is not None:
                if hero.placeholder:
                    parts.append(asset_layer.placeholder_html(f"{sid}-hero", "hero", beat.start, beat.duration, pal["accent"]))
                else:
                    parts.append(asset_layer.hero_clip_html(sid, clip_src[hero.name], beat.start, beat.duration))
        s_start, s_dur, track = beat.start, beat.duration, 1
        if xpl is not None:
            track = 1 if i % 2 == 0 else 5          # alternate tracks so a transition can overlap two scenes
            nxt = xpl.transitions.get(i + 1)
            if nxt:
                s_dur += nxt["seconds"]             # keep this scene under the incoming one during the transition
            cur = xpl.transitions.get(i)
            if cur:
                if cur["type"] == "iris":
                    c0 = f"circle(0px at {cur['x']}px {cur['y']}px)"
                    c1 = f"circle(2300px at {cur['x']}px {cur['y']}px)"
                    tl.append(f'tl.fromTo("#{sid}",{{clipPath:"{c0}"}},{{clipPath:"{c1}",duration:{cur["seconds"]:.2f},ease:"power2.inOut"}},{beat.start:.3f});')
                else:
                    tl.append(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{cur["seconds"]:.2f},ease:"power1.inOut"}},{beat.start:.3f});')
                events.append(beat.start)
        parts.append(f'<div id="{sid}" class="clip scene {beat.scene_type}" data-start="{s_start:.3f}" data-duration="{s_dur:.3f}" data-track-index="{track}">{out.html}</div>')
        tl += out.tl
        events += out.events
        problems += [f"{beat.id}: {p}" for p in out.problems]
        scene_types.append(beat.scene_type)

    # captions (same grouping/format as Phase 1, lower anchor)
    cap_parts = []
    for j, g in enumerate(captions):
        cid = f"c{j + 1}"
        text = g.text.upper() if cap_upper else g.text
        size = fit_font_size(text, cap_size, cap_min, cap_width, uppercase=cap_upper)
        words_html = []
        for k, w in enumerate(g.words):
            t = w.text.upper() if cap_upper else w.text
            cls = "w hl" if k == g.highlight else "w"
            words_html.append(f'<span class="{cls}" id="{cid}w{k}">{html.escape(t)}</span>')
        dur = max(0.1, g.end - g.start)
        cap_parts.append(f'<div id="{cid}" class="clip cap" data-start="{g.start:.3f}" data-duration="{dur:.3f}" data-track-index="{2 + (j % 2)}">'
                         f'<div class="cap-inner" style="font-size:{size}px">{" ".join(words_html)}</div></div>')
        tl.append(f'tl.fromTo("#{cid} .cap-inner",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{g.start:.3f});')
        if g.highlight >= 0:
            tl.append(f'tl.fromTo("#{cid}w{g.highlight}",{{scale:0.94}},{{scale:{1.03 if flat else 1.06},duration:0.15,ease:"power2.out"}},{max(g.start, g.words[g.highlight].start):.3f});')
        fade_out_at = max(g.start + 0.13, g.end - 0.1)
        if fade_out_at + 0.1 <= g.end + 0.001:
            tl.append(f'tl.to("#{cid} .cap-inner",{{opacity:0,duration:0.1,ease:"power2.in"}},{fade_out_at:.3f});')
    parts.append('<div id="captions" data-track-kind="captions">' + "".join(cap_parts) + "</div>")

    if outro:
        parts.append(f'<div id="outro" class="clip" data-start="{outro_start:.3f}" data-duration="{outro_s:.3f}" data-track-index="3">'
                     f'<div class="outro-inner"><span class="mark big"></span><div class="wordmark big">{html.escape(b.name)}</div>'
                     f'<div class="cta">{html.escape(b.cta(lang))}</div></div></div>')
        tl.append(f'tl.fromTo("#outro .outro-inner",{{opacity:0,scale:0.96}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{outro_start:.3f});')
        tl.append(f'tl.fromTo("#outro .cta",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{outro_start + 0.35:.3f});')
        events.append(outro_start)

    if voice_rel:
        v_dur = max(0.0, min(total - voice_start, ffmpeg_audio_duration(voice_file) or (total - voice_start)))
        parts.append(f'<audio id="voice" class="clip" src="{voice_rel}" data-start="{voice_start:.3f}" data-duration="{v_dur:.3f}" data-track-index="7" data-volume="1"></audio>')
    if aset and aset.sfx and sfx_in_project:
        parts += asset_layer.sfx_html(aset, project_dir / "assets", total)

    css = f"""
{font_css}
:root{{--bg:{pal['bg']};--accent:{pal['accent']};--text:{pal['text']};--surface:{pal['surface']};--muted:{pal['muted']};}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);font-family:'FN {body}',sans-serif;color:var(--text);}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;}}
#bg{{position:absolute;inset:-60px;z-index:0;{_bg_css(b.design.get('bg_pattern', ''), pal)}}}
#light{{position:absolute;left:-200px;top:-200px;width:1480px;height:2320px;z-index:0;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,color-mix(in srgb,{pal['accent']} 14%,transparent) 0%,transparent 55%);}}
.clip{{position:absolute;inset:0;}}
{asset_layer.assets_css(pal['bg'], aset.scrim) if aset and aset.enabled else ''}
.wordmark{{font-family:'FN {display}';font-weight:{display_w};letter-spacing:-0.02em;}}
#logo{{z-index:20;}}
.logo-inner{{position:absolute;left:72px;top:116px;font-size:{int(layout['logo_px'])}px;line-height:56px;display:flex;align-items:center;gap:12px;color:var(--text);opacity:0.92;}}
.logo-inner.brandmark{{gap:{int(logo_cfg.get('logo_height_px', 44))}px;}}
.logo-img{{width:{int(logo_cfg.get('logo_height_px', 44))}px;height:{int(logo_cfg.get('logo_height_px', 44))}px;display:block;}}
.logo-inner.brandmark .wordmark{{font-weight:700;font-size:28px;letter-spacing:0.18em;text-transform:uppercase;}}
.mark{{display:inline-block;width:22px;height:22px;border-radius:7px;background:var(--accent);}}
.mark.big{{width:52px;height:52px;border-radius:16px;margin-right:22px;vertical-align:middle;}}
#ailabel{{position:absolute;left:0;right:0;bottom:{max(int(layout.get('ai_label_bottom_px', AI_LABEL_BOTTOM)), AI_LABEL_MIN_BOTTOM)}px;text-align:center;font-size:30px;font-weight:600;color:var(--text);opacity:0.85;z-index:30;letter-spacing:0.04em;}}
#progress{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:{int(layout['progress_y'])}px;height:6px;background:color-mix(in srgb,var(--text) 14%,transparent);border-radius:3px;z-index:20;overflow:hidden;}}
#progress-fill{{width:100%;height:100%;background:var(--accent);transform-origin:left center;}}
{scene_css(pal, display, display_w, body, mono, zone_top, zone_h, flat)}
{file_css(pal, display, display_w, mono, flat)}
{brand_scenes.css_for(b.id, pal, display, display_w, body, mono, zone_top, zone_h, flat)}
{xpl.css if xpl is not None else ''}
#status{{position:absolute;left:{TITLE_SAFE_X}px;width:{min(TITLE_SAFE_W, 940 - TITLE_SAFE_X)}px;top:{int(layout.get('status_y', 1480))}px;height:84px;z-index:25;display:flex;align-items:center;justify-content:space-between;background:color-mix(in srgb,var(--surface) 85%,transparent);border:2px solid color-mix(in srgb,var(--accent) 25%,transparent);border-radius:20px;padding:0 26px;font-size:30px;color:var(--text);}}
.st-file{{font-family:'FN {mono}';display:flex;align-items:center;gap:12px;}}
.st-icon{{color:var(--accent);font-size:30px;}}
.st-states{{position:relative;display:block;min-width:460px;height:84px;}}
.st{{position:absolute;right:0;top:0;height:84px;display:flex;align-items:center;font-weight:600;white-space:nowrap;}}
.st-amber{{color:{pal.get('signal_amber', AMBER)};}}
.st-red{{color:{pal.get('signal_red', RED)};}}
.st-muted{{color:var(--muted);}}
#captions{{position:absolute;inset:0;z-index:30;}}
.cap{{overflow:visible;}}
.cap-inner{{position:absolute;left:{(W - cap_width) // 2}px;width:{cap_width}px;bottom:{cap_bottom}px;text-align:center;font-family:'FN {cap_font}';font-weight:{cap_weight};line-height:{sub.get('line_height', 1.15)};color:{sub.get('color', pal['text'])};text-transform:{'uppercase' if cap_upper else 'none'};letter-spacing:{sub.get('letter_spacing_em', 0)}em;text-shadow:{sub.get('shadow', '0 4px 24px rgba(0,0,0,0.45)')};}}
.cap-inner .w{{display:inline-block;margin:0 0.09em;transform-origin:50% 100%;}}
.cap-inner .w.hl{{color:{sub.get('highlight_color', pal['accent'])};}}
#art50{{z-index:60;}}
.art50-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:{zone_top + 40}px;text-align:center;font-size:40px;line-height:1.3;color:var(--text);background:color-mix(in srgb,var(--surface) 92%,transparent);padding:28px 36px;border-radius:20px;border:2px solid var(--accent);}}
#outro{{z-index:40;}}
.outro-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:700px;text-align:center;background:color-mix(in srgb,var(--bg) 92%,transparent);padding:40px 0;}}
.outro-inner .wordmark.big{{font-size:112px;display:inline-block;vertical-align:middle;}}
.cta{{margin-top:48px;font-size:52px;line-height:1.2;color:var(--text);}}
"""
    index = f"""<!doctype html>
<html lang="{lang}" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>{html.escape(title or plan.title or b.name)}</title>
<script src="{gsap_src}"></script>
<style>{css}</style>
{layer.get('head_html', '')}
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}" data-fps="{fps}">
{chr(10).join(parts)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
{layer.get('body_end_html', '')}
</body>
</html>
"""
    (project_dir / "index.html").write_text(index, encoding="utf-8", newline="\n")
    (project_dir / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": False},
    }, indent=2) + "\n", encoding="utf-8")
    (project_dir / "meta.json").write_text(json.dumps({"id": project_dir.name, "name": title or plan.title or b.name}) + "\n", encoding="utf-8")
    return DirectionBuild(index=project_dir / "index.html", events=sorted(set(round(e, 3) for e in events)),
                          problems=problems, scene_types=scene_types, art50_seconds=art50_s, named_events=named_events)


def _font_face(family: str, rel: str, weight: str = "100 900") -> str:
    fmt = "woff2" if rel.endswith(".woff2") else "truetype"
    return (f"@font-face{{font-family:'FN {family}';src:url('{rel}') format('{fmt}');"
            f"font-weight:{weight};font-style:normal;font-display:block;}}")


def _brand_font_css(brand: Brand, families: set[str], assets: Path) -> str:
    """@font-face for every used family: brand-specific files (brand.yaml fonts.*.file) first, shared fonts otherwise."""
    css: list[str] = []
    done: set[str] = set()
    for role in ("display", "body", "mono", "caption"):
        f = (brand.fonts.get(role) or {})
        fam, file = f.get("family"), f.get("file")
        if not fam or fam in done or fam not in families or not file:
            continue
        files = [file] + list(f.get("extra_files") or [])
        slug = fam.lower().replace(" ", "")
        (assets / "fonts" / slug).mkdir(parents=True, exist_ok=True)
        for fp in files:
            src = ROOT / fp
            if src.exists():
                dst = assets / "fonts" / slug / src.name
                if not dst.exists():
                    shutil.copy2(src, dst)
                weight = "100 900" if ("wght" in src.name or src.suffix == ".woff2") else str(f.get("weight", 400))
                css.append(_font_face(fam, f"assets/fonts/{slug}/{src.name}", weight))
        lic = f.get("license_file")
        if lic and (ROOT / lic).exists():
            dst = assets / "fonts" / slug / Path(lic).name
            if not dst.exists():
                shutil.copy2(ROOT / lic, dst)
        done.add(fam)
    for fam in sorted(families - done):
        if fam in FONT_FILES:
            folder, fname = FONT_FILES[fam]
            src, dst = ASSETS_DIR / "fonts" / folder, assets / "fonts" / folder
            dst.mkdir(parents=True, exist_ok=True)
            for fn in (fname, "OFL.txt"):
                if (src / fn).exists() and not (dst / fn).exists():
                    shutil.copy2(src / fn, dst / fn)
            css.append(_font_face(fam, f"assets/fonts/{folder}/{fname}"))
    return "\n".join(css)


def _bg_css(pattern: str, pal: dict) -> str:
    if pattern == "hairline-grid":          # brand: flat ground, grid at most as hairlines
        hair = pal.get("hairline", "rgba(226,232,246,0.12)")
        return (f"background-color:{pal['bg']};background-image:linear-gradient({hair} 1px,transparent 1px),"
                f"linear-gradient(90deg,{hair} 1px,transparent 1px);background-size:96px 96px;")
    return _bg_pattern_css(pattern, pal)


def group_phrases(words, *, min_words: int = 2, max_words: int = 4, pause_gap: float = 0.35):
    """Caption groups of 2-4 words at sense boundaries: break at sentence punctuation, at a clear pause or at
    max_words; single-word groups are merged with their neighbour. Returns compose.CaptionGroup objects."""
    LEAD = {"und", "oder", "ob", "wie", "über", "von", "vor", "bei", "in", "im", "mit", "zum", "zur", "der", "die", "das", "den",
            "dem", "des", "ein", "eine", "einen", "nicht", "also", "aber", "dass", "wenn", "welchen", "welche", "euer", "dieser",
            "diese", "dieses", "für", "nach", "aus", "außer", "sondern", "etwa", "and", "or", "if", "how", "of", "with", "the", "a", "an", "not"}
    groups: list[list] = []
    cur: list = []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        strong = w.text.rstrip().endswith((".", "!", "?", ":", ";"))
        soft = w.text.rstrip().endswith(",")
        pause = nxt is not None and (nxt.start - w.end) >= pause_gap
        if nxt is None or strong or (soft and len(cur) >= min_words) or (pause and len(cur) >= min_words):
            groups.append(cur)
            cur = []
        elif len(cur) >= max_words:
            # no sense boundary yet: split before the last function word so the phrase stays whole
            cut = next((j for j in range(len(cur) - 1, min_words - 1, -1) if cur[j].text.lower().strip(".,!?:;") in LEAD), len(cur))
            groups.append(cur[:cut])
            cur = cur[cut:]
    if cur:
        groups.append(cur)
    merged: list[list] = []
    for g in groups:
        if len(g) < min_words and merged and len(merged[-1]) + len(g) <= max_words + 1:
            merged[-1] = merged[-1] + g
        else:
            merged.append(g)
    out = []
    for k, g in enumerate(merged):
        start, end = g[0].start, g[-1].end
        if k + 1 < len(merged):
            end = max(end, min(merged[k + 1][0].start, end + 0.25))
        hl = max(range(len(g)), key=lambda j: len(g[j].text.strip(".,!?:;")))
        out.append(CaptionGroup(start=start, end=end, words=list(g), highlight=hl))
    for a, b in zip(out, out[1:]):
        if a.end > b.start:
            a.end = b.start
    return [g for g in out if g.end > g.start]
