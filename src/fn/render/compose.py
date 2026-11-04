"""Build a HyperFrames project (index.html + assets) from brand, scenes, captions and audio.

Layout follows docs/design-system.md. One root composition "main"; every timed element is a
root-level `.clip` with data-start/data-duration; one paused GSAP timeline drives all motion.
"""
from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from ..brands import Brand
from ..config import ASSETS_DIR
from .ffmpeg import audio_duration as ffmpeg_audio_duration

W, H = 1080, 1920
TITLE_SAFE_X = 108
TITLE_SAFE_W = W - 2 * TITLE_SAFE_X
SCENE_TOP, SCENE_BOTTOM = 300, 1150
PROGRESS_Y = 1168
CAPTION_BOTTOM = 640
AI_LABEL_BOTTOM = 150

FONT_FILES = {
    "Inter": ("inter", "Inter[opsz,wght].ttf"),
    "Montserrat": ("montserrat", "Montserrat[wght].ttf"),
    "JetBrains Mono": ("jetbrainsmono", "JetBrainsMono[wght].ttf"),
    "Playfair Display": ("playfairdisplay", "PlayfairDisplay[wght].ttf"),
    "Oswald": ("oswald", "Oswald[wght].ttf"),
}
GSAP_FILE = ASSETS_DIR / "vendor" / "gsap.min.js"


@dataclass
class Scene:
    id: str
    start: float
    duration: float
    headline: str
    body: str = ""
    kind: str = "card"          # hook | card | fact | code | payoff
    source_label: str = ""      # e.g. "[S1] bsi.bund.de, 2026-10-29"
    code_lines: list[str] = field(default_factory=list)
    number: str = ""            # big numeral for fact scenes

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class CaptionGroup:
    start: float
    end: float
    words: list[Word]
    highlight: int = -1          # index of the emphasised word, -1 = none

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words)


@dataclass
class Composition:
    brand: Brand
    language: str
    duration: float
    scenes: list[Scene]
    captions: list[CaptionGroup]
    voice_file: Path | None = None
    voice_start: float = 0.0
    music_file: Path | None = None
    music_gain: float = 0.12
    title: str = ""
    fps: int = 30

    @property
    def intro_seconds(self) -> float:
        return float(self.brand.intro.get("seconds", 1.6))

    @property
    def outro_seconds(self) -> float:
        return float(self.brand.outro.get("seconds", 4.0))


# ----------------------------------------------------------------------------- captions

def group_words(words: list[Word], per_group: int, *, pause_gap: float = 0.15) -> list[CaptionGroup]:
    """2-6 words per group; break at sentence end, at a pause >= pause_gap, or at the word limit."""
    groups: list[CaptionGroup] = []
    cur: list[Word] = []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        sentence_end = w.text.rstrip().endswith((".", "!", "?", ":"))
        pause = nxt is not None and (nxt.start - w.end) >= pause_gap
        if len(cur) >= per_group or sentence_end or pause or nxt is None:
            start = cur[0].start
            end = cur[-1].end
            if nxt is not None:
                end = max(end, min(nxt.start, end + 0.25))
            hl = max(range(len(cur)), key=lambda k: len(cur[k].text.strip(".,!?:;")))
            groups.append(CaptionGroup(start=start, end=end, words=list(cur), highlight=hl))
            cur = []
    # no overlap between consecutive groups
    for a, b in zip(groups, groups[1:]):
        if a.end > b.start:
            a.end = b.start
    return [g for g in groups if g.end > g.start]


def fit_font_size(text: str, base: int, min_size: int, max_width: int, *, uppercase: bool) -> int:
    factor = 0.62 if uppercase else 0.55
    width = len(text) * factor * base
    if width <= max_width:
        return base
    # allow two lines before shrinking below 0.8 * base
    two_line_ok = width <= 2 * max_width * 0.95
    if two_line_ok:
        return max(min_size, int(base * 0.9))
    size = int(max_width * 2 / (len(text) * factor))
    return max(min_size, min(base, size))


# ----------------------------------------------------------------------------- styling

def _font_face_css(families: set[str]) -> str:
    css = []
    for fam in sorted(families):
        folder, fname = FONT_FILES[fam]
        css.append(
            f"@font-face{{font-family:'FN {fam}';src:url('assets/fonts/{folder}/{fname}') format('truetype');"
            f"font-weight:100 900;font-style:normal;font-display:block;}}"
        )
    return "\n".join(css)


def _bg_pattern_css(pattern: str, pal: dict) -> str:
    acc, bg, surf = pal["accent"], pal["bg"], pal["surface"]
    line = f"color-mix(in srgb, {acc} 12%, transparent)"
    faint = f"color-mix(in srgb, {acc} 7%, transparent)"
    if pattern == "dot-grid":
        return f"background-color:{bg};background-image:radial-gradient({line} 2px, transparent 2.5px);background-size:48px 48px;"
    if pattern == "hex-grid":
        return (f"background-color:{bg};background-image:repeating-linear-gradient(60deg,{faint} 0 1px,transparent 1px 70px),"
                f"repeating-linear-gradient(-60deg,{faint} 0 1px,transparent 1px 70px),repeating-linear-gradient(0deg,{faint} 0 1px,transparent 1px 70px);")
    if pattern == "blueprint-grid":
        return (f"background-color:{bg};background-image:linear-gradient({line} 1px,transparent 1px),linear-gradient(90deg,{line} 1px,transparent 1px),"
                f"linear-gradient({faint} 1px,transparent 1px),linear-gradient(90deg,{faint} 1px,transparent 1px);background-size:300px 300px,300px 300px,60px 60px,60px 60px;")
    if pattern == "isometric-blocks":
        return (f"background-color:{bg};background-image:repeating-linear-gradient(30deg,{faint} 0 1px,transparent 1px 90px),"
                f"repeating-linear-gradient(-30deg,{faint} 0 1px,transparent 1px 90px);")
    if pattern == "fabric-gradient":
        return (f"background:linear-gradient(160deg,{bg} 0%,{surf} 55%,{bg} 100%);"
                f"background-image:repeating-linear-gradient(45deg,{faint} 0 1px,transparent 1px 6px),linear-gradient(160deg,{bg} 0%,{surf} 55%,{bg} 100%);")
    if pattern == "vignette":
        return f"background:radial-gradient(ellipse at 50% 40%,{surf} 0%,{bg} 60%,#000 100%);"
    if pattern == "map-contours":
        rings = ",".join(f"radial-gradient(circle at 30% 35%,transparent {r}px,{faint} {r + 1}px,transparent {r + 2}px)" for r in range(120, 1400, 110))
        return f"background-color:{bg};background-image:{rings};"
    if pattern == "petal-gradient":
        return (f"background-color:{bg};background-image:radial-gradient(circle at 20% 15%,color-mix(in srgb,{acc} 22%,transparent) 0,transparent 38%),"
                f"radial-gradient(circle at 85% 70%,color-mix(in srgb,{acc} 18%,transparent) 0,transparent 42%);")
    if pattern == "checkerboard":
        return (f"background-color:{bg};background-image:repeating-conic-gradient({surf} 0 25%,transparent 0 50%);"
                f"background-size:140px 140px;background-position:0 1200px;")
    return f"background-color:{bg};"


def _visual_html(motif: str, scene: Scene, pal: dict, idx: int) -> str:
    """Placeholder visual for a scene by brand motif (Phase 1: shapes only)."""
    acc, text, surf, muted = pal["accent"], pal["text"], pal["surface"], pal["muted"]
    if scene.kind == "code" or (motif == "code-window" and scene.code_lines):
        lines = scene.code_lines or ["$ claude", "> /init", "> ..."]
        rows = "".join(f'<div class="code-line">{html.escape(l)}</div>' for l in lines[:6])
        return (f'<div class="vis code-win"><div class="code-bar"><i></i><i></i><i></i></div>{rows}</div>')
    if scene.number:
        return f'<div class="vis big-number">{html.escape(scene.number)}</div>'
    if motif == "code-window":
        return (f'<svg class="vis" viewBox="0 0 480 420" fill="none"><rect x="40" y="60" width="400" height="300" rx="26" fill="{surf}" stroke="{acc}" stroke-width="3"/>'
                f'<text x="90" y="230" fill="{acc}" font-size="110" font-family="FN JetBrains Mono">&gt;_</text>'
                f'<rect x="300" y="150" width="90" height="12" rx="6" fill="{muted}" opacity="0.5"/><rect x="300" y="190" width="60" height="12" rx="6" fill="{muted}" opacity="0.35"/></svg>')
    if motif == "shield-lines":
        return ('<svg class="vis" viewBox="0 0 400 440" fill="none"><path d="M200 20 L360 80 V220 C360 320 290 390 200 420 C110 390 40 320 40 220 V80 Z" '
                f'stroke="{acc}" stroke-width="6"/><path d="M130 220 L185 275 L280 170" stroke="{acc}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    if motif == "blueprint":
        return (f'<svg class="vis" viewBox="0 0 480 400" fill="none" stroke="{acc}" stroke-width="3"><circle cx="240" cy="200" r="150"/><circle cx="240" cy="200" r="90"/>'
                f'<circle cx="240" cy="200" r="30"/><line x1="40" y1="200" x2="440" y2="200" stroke-dasharray="8 10"/><line x1="240" y1="20" x2="240" y2="380" stroke-dasharray="8 10"/>'
                f'<line x1="90" y1="365" x2="390" y2="365"/><line x1="90" y1="352" x2="90" y2="378"/><line x1="390" y1="352" x2="390" y2="378"/>'
                f'<text x="240" y="395" fill="{text}" font-size="22" text-anchor="middle" stroke="none" font-family="FN JetBrains Mono">300 mm</text></svg>')
    if motif == "scale-bars":
        hs = [120, 220, 360, 300, 180]
        bars = "".join(f'<rect x="{30 + i * 90}" y="{400 - h}" width="60" height="{h}" fill="{acc if i == 2 else surf}" stroke="{acc}" stroke-width="2"/>' for i, h in enumerate(hs))
        return f'<svg class="vis" viewBox="0 0 480 420" fill="none">{bars}<line x1="20" y1="400" x2="470" y2="400" stroke="{text}" stroke-width="3"/></svg>'
    if motif == "gold-hairlines":
        return (f'<svg class="vis" viewBox="0 0 480 420" fill="none" stroke="{acc}" stroke-width="1.5"><rect x="60" y="40" width="360" height="340"/>'
                f'<rect x="80" y="60" width="320" height="300"/><path d="M160 360 L240 120 L320 360" /><line x1="140" y1="200" x2="340" y2="200"/></svg>')
    if motif == "film-grain":
        return (f'<svg class="vis" viewBox="0 0 480 420" fill="none"><circle cx="240" cy="210" r="150" fill="{surf}"/>'
                f'<circle cx="240" cy="210" r="150" stroke="{acc}" stroke-width="2"/><path d="M60 330 Q240 150 420 330" stroke="{acc}" stroke-width="4"/></svg>')
    if motif == "archive-stamp":
        return (f'<div class="vis stamp"><div class="stamp-top">ARCHIVE</div><div class="stamp-mid">{html.escape(scene.source_label or "1943 · DOC 17")}</div>'
                f'<div class="stamp-bot">STYLIZED · NO REAL FOOTAGE</div></div>')
    if motif == "soft-bloom":
        return (f'<svg class="vis" viewBox="0 0 480 420" fill="none"><circle cx="200" cy="200" r="120" fill="{acc}" opacity="0.35"/>'
                f'<circle cx="290" cy="230" r="110" fill="{acc}" opacity="0.28"/><circle cx="240" cy="150" r="90" fill="{text}" opacity="0.12"/></svg>')
    if motif == "neon-wobble":
        return (f'<svg class="vis" viewBox="0 0 480 420" fill="none"><path d="M120 100 C 220 20, 380 60, 400 180 C 420 300, 300 400, 180 370 C 60 340, 40 200, 120 100 Z" '
                f'stroke="{acc}" stroke-width="8" fill="{surf}"/><circle cx="200" cy="190" r="18" fill="{text}"/><circle cx="290" cy="190" r="18" fill="{text}"/>'
                f'<path d="M190 280 Q245 330 300 280" stroke="{text}" stroke-width="8" stroke-linecap="round"/></svg>')
    return f'<svg class="vis" viewBox="0 0 480 420" fill="none"><rect x="40" y="40" width="400" height="340" rx="28" stroke="{acc}" stroke-width="4"/></svg>'


# ----------------------------------------------------------------------------- build

def build_project(comp: Composition, project_dir: Path) -> Path:
    """Write index.html, copy fonts, GSAP and audio into project_dir. Returns the index.html path."""
    b = comp.brand
    pal = b.palette
    fonts = b.fonts
    display = fonts.get("display", {}).get("family", "Inter")
    display_w = fonts.get("display", {}).get("weight", 800)
    body = fonts.get("body", {}).get("family", "Inter")
    mono = (fonts.get("mono") or {}).get("family") or "JetBrains Mono"
    sub = b.subtitle_style or {}
    cap_font = sub.get("font_family", body)
    cap_weight = sub.get("font_weight", 700)
    cap_size = int(sub.get("font_size_px", 60))
    cap_min = int(sub.get("min_font_size_px", 42))
    cap_upper = sub.get("text_transform", "none") == "uppercase"
    cap_style = sub.get("style", "highlight-word")
    scrim = sub.get("scrim", {})
    tempo = b.design.get("tempo", "medium")
    enter = {"snappy": 0.18, "chaotic": 0.15, "punchy": 0.2, "slow": 0.4, "gentle": 0.4, "epic": 0.35}.get(tempo, 0.25)

    project_dir.mkdir(parents=True, exist_ok=True)
    assets = project_dir / "assets"
    (assets / "fonts").mkdir(parents=True, exist_ok=True)
    (assets / "vendor").mkdir(parents=True, exist_ok=True)
    used_fonts = {display, body, mono, cap_font}
    for fam in used_fonts:
        folder, fname = FONT_FILES[fam]
        src = ASSETS_DIR / "fonts" / folder
        dst = assets / "fonts" / folder
        dst.mkdir(exist_ok=True)
        for f in (fname, "OFL.txt"):
            if (src / f).exists() and not (dst / f).exists():
                shutil.copy2(src / f, dst / f)
    if GSAP_FILE.exists():
        shutil.copy2(GSAP_FILE, assets / "vendor" / "gsap.min.js")
        gsap_src = "assets/vendor/gsap.min.js"
    else:
        gsap_src = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
    voice_rel = None
    if comp.voice_file and comp.voice_file.exists():
        voice_rel = f"assets/{comp.voice_file.name}"
        if comp.voice_file.resolve() != (assets / comp.voice_file.name).resolve():
            shutil.copy2(comp.voice_file, assets / comp.voice_file.name)
    music_rel = None
    if comp.music_file and comp.music_file.exists():
        music_rel = f"assets/{comp.music_file.name}"
        shutil.copy2(comp.music_file, assets / comp.music_file.name)

    total = comp.duration
    intro_s = comp.intro_seconds
    outro_s = comp.outro_seconds
    outro_start = max(intro_s, total - outro_s)
    lang = comp.language
    ai_label = b.ai_label(lang)
    cta = b.cta(lang)
    motif = b.design.get("motif", "card")
    pattern = b.design.get("bg_pattern", "")
    art50 = b.intro.get("art50_disclosure", {})
    art50_on = bool(art50.get("enabled"))

    parts: list[str] = []
    tl: list[str] = []

    # background
    parts.append('<div id="bg"></div>')

    # intro
    parts.append(
        f'<div id="intro" class="clip" data-start="0" data-duration="{intro_s:.2f}" data-track-index="5">'
        f'<div class="intro-inner"><span class="mark"></span><span id="intro-word" class="wordmark">{html.escape(b.name)}</span></div></div>'
    )
    kind = b.intro.get("kind", "scale-in")
    if kind in ("typing-cursor",):
        tl.append(f'tl.fromTo("#intro .intro-inner",{{opacity:0}},{{opacity:1,duration:0.2}},0);')
        tl.append(f'tl.fromTo("#intro-word",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{max(0.4, intro_s - 0.6):.2f},ease:"steps(12)"}},0.2);')
    elif kind in ("flash-cut", "character-bounce"):
        tl.append(f'tl.fromTo("#intro .intro-inner",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:0.25,ease:"power4.out"}},0);')
        tl.append(f'tl.to("#intro .intro-inner",{{scale:1.06,duration:{max(0.3, intro_s - 0.45):.2f},ease:"sine.inOut"}},0.25);')
    else:
        tl.append(f'tl.fromTo("#intro .intro-inner",{{opacity:0,scale:0.92,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{min(0.6, intro_s * 0.45):.2f},ease:"power3.out"}},0);')
    tl.append(f'tl.to("#intro .intro-inner",{{opacity:0,duration:0.2}},{max(0.0, intro_s - 0.2):.2f});')

    if art50_on:
        a_s = float(art50.get("seconds", 2.5))
        a_text = art50.get("text", {}).get(lang, "AI-generated scenes.")
        parts.append(f'<div id="art50" class="clip" data-start="0" data-duration="{a_s:.2f}" data-track-index="6">'
                     f'<div class="art50-inner">{html.escape(a_text)}</div></div>')
        tl.append('tl.fromTo("#art50 .art50-inner",{opacity:0},{opacity:1,duration:0.2},0);')
        tl.append(f'tl.to("#art50 .art50-inner",{{opacity:0,duration:0.2}},{a_s - 0.2:.2f});')

    # logo top-left + AI label + progress (persistent)
    parts.append(f'<div id="logo" class="clip" data-start="{intro_s:.2f}" data-duration="{total - intro_s:.2f}" data-track-index="4">'
                 f'<div class="logo-inner"><span class="mark small"></span><span class="wordmark small">{html.escape(b.name)}</span></div></div>')
    tl.append(f'tl.fromTo("#logo .logo-inner",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},{intro_s:.2f});')
    parts.append(f'<div id="ailabel">{html.escape(ai_label)}</div>')
    parts.append('<div id="progress"><div id="progress-fill"></div></div>')
    tl.append(f'tl.fromTo("#progress-fill",{{scaleX:0}},{{scaleX:1,duration:{total - intro_s:.2f},ease:"none"}},{intro_s:.2f});')

    # scenes + counters
    n = len(comp.scenes)
    for i, sc in enumerate(comp.scenes):
        sid = f"s{i + 1}"
        headline_cls = "headline hook" if sc.kind == "hook" else "headline"
        if len(sc.headline) > 52:
            headline_cls += " xlong"
        elif len(sc.headline) > 34:
            headline_cls += " long"
        vis = _visual_html(motif, sc, pal, i)
        body_html = f'<div class="body">{html.escape(sc.body)}</div>' if sc.body else ""
        src_html = f'<div class="source">{html.escape(sc.source_label)}</div>' if sc.source_label else ""
        parts.append(
            f'<div id="{sid}" class="clip scene" data-start="{sc.start:.2f}" data-duration="{sc.duration:.2f}" data-track-index="1">'
            f'<div class="scene-inner"><div class="{headline_cls}">{html.escape(sc.headline)}</div>{vis}{body_html}{src_html}</div></div>'
        )
        parts.append(f'<div id="{sid}-counter" class="clip counter" data-start="{sc.start:.2f}" data-duration="{sc.duration:.2f}" data-track-index="4">'
                     f'<div class="counter-inner">{i + 1}/{n}</div></div>')
        s0 = sc.start
        tl.append(f'tl.fromTo("#{sid} .headline",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{enter:.2f},ease:"power3.out"}},{s0:.2f});')
        tl.append(f'tl.fromTo("#{sid} .vis",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:{enter + 0.1:.2f},ease:"power3.out"}},{s0 + 0.08:.2f});')
        if sc.body:
            tl.append(f'tl.fromTo("#{sid} .body",{{opacity:0,y:20}},{{opacity:1,y:0,duration:{enter:.2f}}},{s0 + 0.25:.2f});')
        if sc.source_label:
            tl.append(f'tl.fromTo("#{sid} .source",{{opacity:0}},{{opacity:1,duration:0.3}},{s0 + 0.5:.2f});')
        tl.append(f'tl.fromTo("#{sid}-counter .counter-inner",{{opacity:0}},{{opacity:1,duration:0.2}},{s0:.2f});')
        # slow drift on the visual over the scene for life
        tl.append(f'tl.to("#{sid} .vis",{{y:-14,duration:{max(0.5, sc.duration - enter - 0.3):.2f},ease:"sine.inOut"}},{s0 + enter + 0.1:.2f});')
        tl.append(f'tl.to("#{sid} .scene-inner",{{opacity:0,duration:0.15}},{max(s0, sc.end - 0.15):.2f});')

    # captions
    cap_parts = []
    for j, g in enumerate(comp.captions):
        cid = f"c{j + 1}"
        text = g.text.upper() if cap_upper else g.text
        size = fit_font_size(text, cap_size, cap_min, int(sub.get("position", {}).get("max_width_px", 900)), uppercase=cap_upper)
        words_html = []
        for k, w in enumerate(g.words):
            t = w.text.upper() if cap_upper else w.text
            cls = "w hl" if (k == g.highlight and cap_style != "word-by-word") else "w"
            words_html.append(f'<span class="{cls}" id="{cid}w{k}">{html.escape(t)}</span>')
        dur = max(0.1, g.end - g.start)
        cap_parts.append(f'<div id="{cid}" class="clip cap" data-start="{g.start:.3f}" data-duration="{dur:.3f}" data-track-index="{2 + (j % 2)}">'
                         f'<div class="cap-inner" style="font-size:{size}px">{" ".join(words_html)}</div></div>')
        tl.append(f'tl.fromTo("#{cid} .cap-inner",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{g.start:.3f});')
        if cap_style == "word-by-word":
            for k, w in enumerate(g.words):
                tl.append(f'tl.fromTo("#{cid}w{k}",{{opacity:0.35}},{{opacity:1,duration:0.08}},{max(g.start, w.start):.3f});')
        elif cap_style == "pop-rotate" and g.highlight >= 0:
            tl.append(f'tl.fromTo("#{cid}w{g.highlight}",{{scale:0.6,rotation:-6}},{{scale:1.12,rotation:3,duration:0.18,ease:"back.out(2)"}},{max(g.start, g.words[g.highlight].start):.3f});')
        elif g.highlight >= 0:
            tl.append(f'tl.fromTo("#{cid}w{g.highlight}",{{scale:0.92}},{{scale:1.06,duration:0.15,ease:"back.out(1.6)"}},{max(g.start, g.words[g.highlight].start):.3f});')
        fade_out_at = max(g.start + 0.13, g.end - 0.1)
        if fade_out_at + 0.1 <= g.end + 0.001:
            tl.append(f'tl.to("#{cid} .cap-inner",{{opacity:0,duration:0.1,ease:"power2.in"}},{fade_out_at:.3f});')
    parts.append('<div id="captions" data-track-kind="captions">' + "".join(cap_parts) + "</div>")

    # outro
    parts.append(
        f'<div id="outro" class="clip" data-start="{outro_start:.2f}" data-duration="{total - outro_start:.2f}" data-track-index="3">'
        f'<div class="outro-inner"><span class="mark"></span><div class="wordmark">{html.escape(b.name)}</div>'
        f'<div class="cta">{html.escape(cta)}</div></div></div>'
    )
    tl.append(f'tl.fromTo("#outro .outro-inner",{{opacity:0,scale:0.96}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{outro_start:.2f});')
    tl.append(f'tl.fromTo("#outro .cta",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{outro_start + 0.35:.2f});')

    # audio
    if voice_rel:
        v_dur = max(0.0, min(total - comp.voice_start, ffmpeg_audio_duration(comp.voice_file) or (total - comp.voice_start)))
        parts.append(f'<audio id="voice" class="clip" src="{voice_rel}" data-start="{comp.voice_start:.3f}" data-duration="{v_dur:.3f}" data-track-index="7" data-volume="1"></audio>')
    if music_rel:
        parts.append(f'<audio id="music" class="clip" src="{music_rel}" data-start="0" data-duration="{total:.3f}" data-track-index="8" data-volume="{comp.music_gain}" data-fade-in="0.5" data-fade-out="1.5"></audio>')

    scrim_css = ""
    if scrim and float(scrim.get("opacity", 0)) > 0:
        scrim_css = (f"background:color-mix(in srgb,{scrim.get('color', pal['surface'])} {int(float(scrim['opacity']) * 100)}%,transparent);"
                     f"padding:{scrim.get('padding_px', 18)}px 28px;border-radius:{scrim.get('radius_px', 16)}px;")

    css = f"""
{_font_face_css(used_fonts)}
:root{{--bg:{pal['bg']};--accent:{pal['accent']};--text:{pal['text']};--surface:{pal['surface']};--muted:{pal['muted']};}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);font-family:'FN {body}',sans-serif;color:var(--text);}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;}}
#bg{{position:absolute;inset:0;z-index:0;{_bg_pattern_css(pattern, pal)}}}
.clip{{position:absolute;inset:0;}}
.wordmark{{font-family:'FN {display}';font-weight:{display_w};letter-spacing:-0.02em;}}
.mark{{display:inline-block;width:40px;height:40px;border-radius:12px;background:var(--accent);margin-right:22px;vertical-align:middle;}}
.mark.small{{width:26px;height:26px;border-radius:8px;margin-right:14px;}}
#intro{{z-index:50;}}
.intro-inner{{position:absolute;left:0;right:0;top:860px;text-align:center;font-size:104px;color:var(--text);}}
.intro-inner .wordmark{{display:inline-block;vertical-align:middle;}}
#art50{{z-index:60;}}
.art50-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:1180px;text-align:center;font-size:40px;line-height:1.3;color:var(--text);background:color-mix(in srgb,var(--surface) 85%,transparent);padding:28px 36px;border-radius:20px;border:2px solid var(--accent);}}
#logo{{z-index:20;}}
.logo-inner{{position:absolute;left:72px;top:112px;font-size:56px;line-height:72px;}}
.logo-inner .wordmark{{vertical-align:middle;}}
.counter{{z-index:20;}}
.counter-inner{{position:absolute;right:72px;top:124px;font-size:30px;font-weight:500;color:var(--muted);font-family:'FN {mono}';}}
#ailabel{{position:absolute;left:0;right:0;bottom:{AI_LABEL_BOTTOM}px;text-align:center;font-size:30px;font-weight:500;color:var(--muted);z-index:30;letter-spacing:0.04em;}}
#progress{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:{PROGRESS_Y}px;height:6px;background:color-mix(in srgb,var(--text) 14%,transparent);border-radius:3px;z-index:20;overflow:hidden;}}
#progress-fill{{width:100%;height:100%;background:var(--accent);transform-origin:left center;}}
.scene{{z-index:10;}}
.scene-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:{SCENE_TOP}px;height:{SCENE_BOTTOM - SCENE_TOP}px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:28px;text-align:center;}}
.headline{{font-family:'FN {display}';font-weight:{display_w};font-size:72px;max-width:860px;line-height:1.08;color:var(--text);letter-spacing:-0.015em;}}
.headline.hook{{font-size:92px;line-height:1.04;}}
.headline.long{{font-size:60px;}}
.headline.hook.long{{font-size:72px;}}
.headline.xlong{{font-size:52px;}}
.headline.hook.xlong{{font-size:62px;}}
.vis{{width:560px;height:380px;flex:0 0 auto;}}
.body{{font-size:40px;line-height:1.3;color:var(--text);opacity:0.92;max-width:820px;}}
.source{{font-size:30px;color:var(--muted);font-family:'FN {mono}';}}
.big-number{{display:flex;align-items:center;justify-content:center;font-family:'FN {display}';font-weight:{display_w};font-size:170px;line-height:1;color:var(--accent);height:230px;}}
.code-win{{background:var(--surface);border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);border-radius:22px;padding:26px 30px;text-align:left;font-family:'FN {mono}';font-size:32px;line-height:1.5;color:var(--text);box-shadow:0 30px 80px rgba(0,0,0,0.35);width:760px;height:auto;min-height:320px;}}
.code-bar{{margin-bottom:18px;}}
.code-bar i{{display:inline-block;width:16px;height:16px;border-radius:50%;background:var(--muted);margin-right:10px;opacity:0.6;}}
.code-line{{white-space:pre;overflow:hidden;text-overflow:ellipsis;}}
.code-line:first-of-type{{color:var(--accent);}}
.stamp{{border:3px solid var(--accent);border-radius:8px;padding:30px;width:620px;height:auto;font-family:'FN {mono}';color:var(--text);text-align:left;}}
.stamp-top{{font-size:28px;letter-spacing:0.3em;color:var(--muted);}}
.stamp-mid{{font-size:64px;margin:16px 0;color:var(--accent);}}
.stamp-bot{{font-size:24px;letter-spacing:0.12em;color:var(--muted);}}
#captions{{position:absolute;inset:0;z-index:30;}}
.cap{{overflow:visible;}}
.cap-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;bottom:{CAPTION_BOTTOM}px;text-align:center;font-family:'FN {cap_font}';font-weight:{cap_weight};line-height:{sub.get('line_height', 1.15)};color:{sub.get('color', pal['text'])};text-transform:{'uppercase' if cap_upper else 'none'};letter-spacing:{sub.get('letter_spacing_em', 0)}em;text-shadow:{sub.get('shadow', 'none')};overflow:visible;}}
.cap-inner .w{{display:inline-block;}}
.cap-inner .w.hl{{color:{sub.get('highlight_color', pal['accent'])};}}
.cap-inner .w.hl{{{"font-style:italic;" if cap_style == "italic-emphasis" else ""}}}
.cap-inner{{{scrim_css}}}
#outro{{z-index:40;}}
.outro-inner{{position:absolute;left:{TITLE_SAFE_X}px;width:{TITLE_SAFE_W}px;top:700px;text-align:center;background:color-mix(in srgb,var(--bg) 92%,transparent);padding:40px 0;}}
.outro-inner .wordmark{{font-size:112px;display:inline-block;vertical-align:middle;}}
.outro-inner .mark{{width:52px;height:52px;border-radius:16px;}}
.cta{{margin-top:48px;font-size:52px;line-height:1.2;color:var(--text);}}
.outro-label{{margin-top:36px;font-size:30px;color:var(--muted);letter-spacing:0.04em;}}
"""

    index = f"""<!doctype html>
<html lang="{lang}" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>{html.escape(comp.title or b.name)}</title>
<script src="{gsap_src}"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}" data-fps="{comp.fps}">
{chr(10).join(parts)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
    (project_dir / "index.html").write_text(index, encoding="utf-8", newline="\n")
    (project_dir / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": False},
    }, indent=2) + "\n", encoding="utf-8")
    (project_dir / "meta.json").write_text(json.dumps({"id": project_dir.name, "name": comp.title or b.name}) + "\n", encoding="utf-8")
    return project_dir / "index.html"
