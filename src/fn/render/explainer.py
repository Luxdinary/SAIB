"""Explainer layer ("Erklärschicht"): the cut and layout rules of Stefan's long-form template (VORLAGE.md,
30.10.2026), adapted to 9:16 shorts of 65-95 s. Brand-neutral; a brand switches it on in brands/<id>/brand.yaml:

    explainer:
      enabled: true
      voice_tag: {de: "SYNTHETISCHE STIMME", en: "SYNTHETIC VOICE"}       # top right, whole video
      opening: {de: "Synthetische Stimme · Quellen am Bildschirm", en: "..."}  # source row from 0 s
      opening_seconds: 3.5
      head_on_hook: false          # head (kicker + title) on the hook beat
      colors: {fakt: "#4f8cff", auslegung: "#9b6bff", unsicher: "#ffb347", luecke: "#ff5a5a", beispiel: "#8a93a6"}
      kicker_labels: {de: {problem: "DAS PROBLEM", ...}}                 # optional, per beat function
      source_y: 1396               # top of the marker row (source bar below it); right edge stays left of x 930
      source_layout: inline        # optional: source text to the right of the chips, one row (for tight layouts)
      ai_label_in_tag: true        # optional: no bottom AI label; voice_tag carries the AI notice instead

Per beat (plan JSON, beat["overlay"], all optional):
    kicker: "2 · DAS PROBLEM"      # default "<n> · <label of the beat function>"
    title: "Vier Hübe"             # only for scenes WITHOUT their own title (9:16: the scene title is the head title)
    head_at / head_until: "w:Wort" or seconds from beat start; dim_at: same (head drops to 35 %)
    marker: fakt | auslegung | unsicher | luecke | none   # default: fakt when the beat has sources and a claim function
    marker_at / marker_until: anchors (marker_until frees the row for scene content that appears late); source: false (hide bar) or a text replacing the automatic label
    example: true                  # "Beispielwert" chip: values in the scene are invented
    transition: {type: iris, x: 540, y: 760, seconds: 0.7} | {type: blende, seconds: 0.7}   # into this beat
    vignette: true                 # darker edges for a close-up

Anchors "w:Wort" resolve to the first spoken word of the beat that starts with "Wort" (case-insensitive),
"w:Wort#2" to the second such word. Head and marker count as visual events only when anchored mid-beat (head_at / marker_at).
Sources: plan.sources[i].label (short, preferred) or the title shortened at " (" / ":"; checked_at as the
retrieval date. A label longer than two lines is reported as a problem, never silently cut.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

from ..direction.story import CLAIM_FUNCTIONS

KICKER = {
    "de": {"hook": "EINSTIEG", "problem": "DAS PROBLEM", "explanation": "DIE ERKLÄRUNG", "demonstration": "SO SIEHT ES AUS",
           "insight": "DER KERN", "benefit": "DAS BRINGT DIR", "close": "ZUM SCHLUSS"},
    "en": {"hook": "OPENING", "problem": "THE PROBLEM", "explanation": "HOW IT WORKS", "demonstration": "WHAT IT LOOKS LIKE",
           "insight": "THE POINT", "benefit": "WHAT YOU GET", "close": "TO SUM UP"},
}
MARKER_WORD = {
    "de": {"fakt": "Fakt", "auslegung": "Auslegung", "unsicher": "Unsicher", "luecke": "Lücke", "beispiel": "Beispielwert"},
    "en": {"fakt": "Fact", "auslegung": "Interpretation", "unsicher": "Uncertain", "luecke": "Gap", "beispiel": "Example value"},
}
DEFAULT_COLORS = {"fakt": "#4f8cff", "auslegung": "#9b6bff", "unsicher": "#ffb347", "luecke": "#ff5a5a", "beispiel": "#8a93a6"}
SOURCE_WORD = {"de": ("Quelle", "Quellen", "abgerufen"), "en": ("Source", "Sources", "retrieved")}
MAX_TITLE = 26
MAX_SOURCE_CHARS = 100            # two lines of mono at 24 px in 822 px, with word wrap


@dataclass
class ExplainerOut:
    html: list[str] = field(default_factory=list)
    tl: list[str] = field(default_factory=list)
    css: str = ""
    events: list[float] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    transitions: dict[int, dict] = field(default_factory=dict)   # beat index -> transition (director extends the previous scene)


def config(brand) -> dict:
    return dict((brand.design or {}).get("explainer") or {})


def enabled(brand, plan) -> bool:
    lay = plan.layout or {}
    if "explainer" in lay:
        return bool(lay["explainer"])
    return bool(config(brand).get("enabled"))


def _anchor(value, beat, words, default: float) -> float:
    """Absolute time of an anchor: seconds from beat start, or 'w:Wort[#n]' = start of that spoken word in the beat."""
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return beat.start + float(value)
    m = re.fullmatch(r"w:(.+?)(?:#(\d+))?", str(value).strip())
    if not m:
        raise ValueError(f"beat {beat.id}: anchor {value!r} is neither seconds nor 'w:Wort'")
    stem, nth = m.group(1).lower(), int(m.group(2) or 1)
    hits = [w for w in words if re.sub(r"[^\wäöüß]", "", w.text.lower()).startswith(stem.lower())]
    if len(hits) < nth:
        raise ValueError(f"beat {beat.id}: anchor word {value!r} not spoken in this beat")
    return hits[nth - 1].start


def _source_label(src: dict) -> str:
    if src.get("label"):
        return str(src["label"]).strip()
    t = str(src.get("title", "")).strip()
    cut = [i for i in (t.find(" ("), t.find(": ")) if i >= 8]
    return t[:min(cut)] if cut else t


def _date(s: str) -> str:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(s or ""))
    return f"{m.group(3)}.{m.group(2)}.{m.group(1)}" if m else str(s or "")


def source_text(plan, beat, lang: str) -> str:
    by_id = {s.get("id"): s for s in plan.sources}
    srcs = [by_id[i] for i in beat.source_ids if i in by_id]
    if not srcs:
        return ""
    one, many, got = SOURCE_WORD.get(lang, SOURCE_WORD["de"])
    labels = "; ".join(dict.fromkeys(_source_label(s) for s in srcs))
    dates = sorted({_date(s.get("checked_at", "")) for s in srcs if s.get("checked_at")})
    tail = f" · {got} {dates[-1]}" if dates else ""
    return f"{many if len(srcs) > 1 else one}: {labels}{tail}"


def _marker_shape(kind: str, color: str) -> str:
    if kind == "fakt":
        return f'<span class="xm-shape" style="width:22px;height:22px;background:{color}"></span>'
    if kind == "auslegung":
        return f'<span class="xm-shape" style="width:20px;height:20px;background:{color};transform:rotate(45deg)"></span>'
    if kind == "unsicher":
        return f'<span class="xm-shape" style="width:26px;height:13px;background:{color};border-radius:13px 13px 0 0"></span>'
    if kind == "luecke":
        return f'<span class="xm-shape" style="width:22px;height:22px;border:3px dashed {color};border-radius:50%"></span>'
    return f'<span class="xm-shape" style="width:18px;height:18px;border:3px solid {color};border-radius:4px"></span>'


def build(plan, brand, captions, *, total: float, outro_start: float, pal: dict, display: str, display_w: int,
          mono: str, zone_top: int, lang: str) -> ExplainerOut:
    cfg = config(brand)
    out = ExplainerOut()
    colors = {**DEFAULT_COLORS, **(cfg.get("colors") or {})}
    labels = {**KICKER.get(lang, KICKER["de"]), **((cfg.get("kicker_labels") or {}).get(lang) or {})}
    words_all = [w for g in captions for w in g.words]
    src_y = int((plan.layout or {}).get("source_y", cfg.get("source_y", 1396)))
    head_top = int((plan.layout or {}).get("head_top", cfg.get("head_top", 186)))
    x0, right = 108, 930
    inline = cfg.get("source_layout") == "inline"

    # voice tag (top right, whole video)
    tag = (cfg.get("voice_tag") or {}).get(lang) or ("SYNTHETISCHE STIMME" if lang == "de" else "SYNTHETIC VOICE")
    out.html.append(f'<div id="xtag" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="13">'
                    f'<div class="xtag-inner">{html.escape(tag)}</div></div>')
    out.tl.append('tl.fromTo("#xtag .xtag-inner",{opacity:0},{opacity:1,duration:0.3},0.05);')

    # opening line in the source row
    first_end = plan.beats[0].end if plan.beats and plan.beats[0].end else 3.0
    op_text = (cfg.get("opening") or {}).get(lang)
    if op_text:
        op_s = min(float(cfg.get("opening_seconds", 3.5)), max(1.5, first_end - 0.2))
        out.html.append(f'<div id="xopen" class="clip xlayer" data-start="0" data-duration="{op_s:.3f}" data-track-index="14">'
                        f'<div class="xsrc-inner">{html.escape(op_text)}</div></div>')
        out.tl.append('tl.fromTo("#xopen .xsrc-inner",{opacity:0},{opacity:1,duration:0.3},0.1);')
        out.tl.append(f'tl.to("#xopen .xsrc-inner",{{opacity:0,duration:0.25}},{op_s - 0.3:.3f});')

    n = 0
    for i, beat in enumerate(plan.beats):
        ov = dict(getattr(beat, "overlay", {}) or {})
        bw = [w for w in words_all if beat.start <= w.start < beat.end]
        end = min(beat.end, outro_start)
        if end - beat.start < 0.6:
            continue
        sid = f"x{i + 1}"
        n += 1

        # head: kicker + title (top left, under the logo row)
        show_head = ov.get("head", True) and (beat.function != "hook" or cfg.get("head_on_hook") or ov.get("title"))
        if show_head:
            kicker = ov.get("kicker") or f"{n} · {labels.get(beat.function, beat.function.upper())}"
            title = ov.get("title", "")
            if len(title) > MAX_TITLE:
                out.problems.append(f"{beat.id}: head title {len(title)} chars > {MAX_TITLE}")
            h0 = max(beat.start + 0.1, _anchor(ov.get("head_at"), beat, bw, beat.start + 0.25))
            h1 = min(end - 0.1, _anchor(ov.get("head_until"), beat, bw, end - 0.15))
            if h1 - h0 > 0.5:
                out.html.append(f'<div id="{sid}h" class="clip xlayer" data-start="{h0:.3f}" data-duration="{h1 - h0:.3f}" data-track-index="15">'
                                f'<div class="xhead"><div class="xkicker">{html.escape(kicker)}</div>'
                                + (f'<div class="xtitle">{html.escape(title)}</div>' if title else "") + "</div></div>")
                out.tl.append(f'tl.fromTo("#{sid}h .xhead",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{h0:.3f});')
                if ov.get("dim_at") is not None:
                    d = _anchor(ov["dim_at"], beat, bw, h0)
                    out.tl.append(f'tl.to("#{sid}h .xhead",{{opacity:0.35,duration:0.3}},{max(h0 + 0.3, d):.3f});')
                out.tl.append(f'tl.to("#{sid}h .xhead",{{opacity:0,duration:0.15}},{h1 - 0.15:.3f});')
                if ov.get("head_at") is not None:      # only a mid-beat change is a new visual event
                    out.events.append(h0)

        # marker capsule + source bar (bottom left, above the platform caption block)
        kind = ov.get("marker")
        if kind is None:
            kind = "fakt" if beat.source_ids and beat.function in CLAIM_FUNCTIONS else "none"
        if kind not in ("fakt", "auslegung", "unsicher", "luecke", "none"):
            out.problems.append(f"{beat.id}: unknown marker {kind!r}")
            kind = "none"
        chips = []
        if kind != "none":
            chips.append(f'<span class="xm">{_marker_shape(kind, colors[kind])}<span>{html.escape(MARKER_WORD[lang if lang in MARKER_WORD else "de"][kind])}</span></span>')
        if ov.get("example"):
            chips.append(f'<span class="xm">{_marker_shape("beispiel", colors["beispiel"])}<span>{html.escape(MARKER_WORD[lang if lang in MARKER_WORD else "de"]["beispiel"])}</span></span>')
        src = ""
        if kind in ("fakt", "unsicher", "luecke") and ov.get("source", True) is not False:
            src = ov["source"] if isinstance(ov.get("source"), str) else source_text(plan, beat, lang)
            if kind == "fakt" and not src:
                out.problems.append(f"{beat.id}: marker 'fakt' without a source")
            if len(src) > MAX_SOURCE_CHARS:
                out.problems.append(f"{beat.id}: source bar {len(src)} chars > {MAX_SOURCE_CHARS} (two lines); add sources[].label")
        if chips or src:
            m0 = max(beat.start + 0.15, _anchor(ov.get("marker_at"), beat, bw, beat.start + 0.35))
            if i == 0 and op_text:
                m0 = max(m0, op_s + 0.05)
            m1 = min(end - 0.1, _anchor(ov.get("marker_until"), beat, bw, end - 0.1))
            if m1 - m0 > 0.5:
                if inline:      # chips and source in one row (source wraps to the right of the chips)
                    out.html.append(f'<div id="{sid}m" class="clip xlayer" data-start="{m0:.3f}" data-duration="{m1 - m0:.3f}" data-track-index="16">'
                                    f'<div class="xmark inline">{"".join(chips)}'
                                    + (f'<span class="xsrc-inner">{html.escape(src)}</span>' if src else "") + "</div></div>")
                else:
                    out.html.append(f'<div id="{sid}m" class="clip xlayer" data-start="{m0:.3f}" data-duration="{m1 - m0:.3f}" data-track-index="16">'
                                    f'<div class="xmark">{"".join(chips)}</div>'
                                    + (f'<div class="xsrc-inner">{html.escape(src)}</div>' if src else "") + "</div>")
                out.tl.append(f'tl.fromTo("#{sid}m .xmark",{{opacity:0,x:-12}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{m0:.3f});')
                if src:
                    out.tl.append(f'tl.fromTo("#{sid}m .xsrc-inner",{{opacity:0}},{{opacity:1,duration:0.3}},{m0 + 0.1:.3f});')
                if ov.get("marker_at") is not None:
                    out.events.append(m0)

        if ov.get("vignette"):
            out.html.append(f'<div id="{sid}v" class="clip xvig" data-start="{beat.start:.3f}" data-duration="{end - beat.start:.3f}" data-track-index="17"></div>')
            out.tl.append(f'tl.fromTo("#{sid}v",{{opacity:0}},{{opacity:1,duration:0.6}},{beat.start:.3f});')

        tr = ov.get("transition")
        if tr and i > 0:
            if tr.get("type") not in ("iris", "blende"):
                out.problems.append(f"{beat.id}: unknown transition {tr.get('type')!r}")
            else:
                out.transitions[i] = {"type": tr["type"], "seconds": float(tr.get("seconds", 0.7)),
                                      "x": int(tr.get("x", 540)), "y": int(tr.get("y", zone_top + 450))}

    # vignette darkens the edges; on a light scheme var(--bg) would lighten them, so use a dark tint there
    vig = cfg.get("vignette_color") or ("rgba(20,12,14,0.32)" if pal.get("scheme") == "light"
                                        else "color-mix(in srgb,var(--bg) 78%,transparent)")
    out.css = f"""
#xtag{{z-index:22;}}
.xlayer{{z-index:26;}}
.xtag-inner{{position:absolute;right:108px;top:130px;font-family:'FN {mono}';font-size:20px;letter-spacing:0.14em;color:var(--muted);}}
.xhead{{position:absolute;left:{x0}px;top:{head_top}px;width:{right - x0}px;z-index:22;}}
.xkicker{{font-family:'FN {mono}';font-size:24px;letter-spacing:0.16em;color:{colors['fakt']};text-transform:uppercase;white-space:nowrap;}}
.xtitle{{font-family:'FN {display}';font-weight:{display_w};font-size:52px;line-height:1.05;color:var(--text);margin-top:6px;white-space:nowrap;}}
.xmark{{position:absolute;left:{x0}px;top:{src_y}px;display:flex;gap:14px;z-index:26;}}
.xm{{display:inline-flex;align-items:center;gap:12px;height:44px;padding:0 18px 0 14px;border-radius:22px;background:color-mix(in srgb,var(--surface) 90%,transparent);border:2px solid color-mix(in srgb,var(--text) 18%,transparent);font-family:'FN {mono}';font-size:24px;color:var(--text);}}
.xm-shape{{display:inline-block;flex:none;}}
.xsrc-inner{{position:absolute;left:{x0}px;width:{right - x0}px;top:{src_y + 56}px;font-family:'FN {mono}';font-size:24px;line-height:1.3;color:var(--text);opacity:0.9;z-index:26;text-shadow:0 2px 10px color-mix(in srgb,var(--bg) 80%,transparent);}}
#xopen .xsrc-inner{{top:{src_y}px;}}
.xmark.inline{{width:{right - x0}px;align-items:flex-start;}}
.xmark.inline .xm{{flex:none;}}
.xmark.inline .xsrc-inner{{position:static;width:auto;flex:1;font-size:22px;padding-top:2px;}}
.xvig{{z-index:12;pointer-events:none;background:radial-gradient(ellipse at 50% 42%,transparent 38%,{vig} 100%);}}
"""
    return out
