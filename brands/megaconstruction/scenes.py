"""Gigastruct scene types (brand module, loaded by fn.render.brand_scenes): five direction scene types for megaconstructions.

The 3D model (gigastruct3d.js, one persistent WebGL canvas) is the dominant motif of every scene and the
red thread of the video; these templates only draw the 2D layer above it: engineering-drawing labels,
dimension chips, a phase rail, computed comparison bars and number tiles. No cards over the whole frame,
no slide look. Loaded for this brand only by fn.render.brand_scenes (docs/direction-system.md, 6d); the
signature and return type are those of fn.render.templates (SceneCtx -> SceneOut). Times: "at" (seconds from the
beat start), "at_word" (+ "at_offset") or "@Wort+0.5" strings, resolved from SceneCtx.words; a word that is not
found is reported as a problem and the default time is used.

| scene type     | Gigastruct meaning      | data |
|----------------|-------------------------|------|
| gs_hook        | Monument-Hook           | kicker, question, number{value, unit, at}, badge{text, at}, question_at |
| gs_phases      | Bauphasen in Schritten  | kicker, headline, steps[{label, sub, at}] |
| gs_section     | Schnittmodell           | kicker, headline, callouts[{anchor, text, at}], dims[{anchor, text, at}], note |
| gs_compare     | Größenvergleich, gerechnet | kicker, headline, a{label, value, unit}, b{label, value, unit}, decimals, glyph, a_at, b_at, result_at |
| gs_numbers     | Kennzahlen / Abschluss  | kicker, headline, items[{value, unit, label, at}] or mode "closing": statement, counter{done, total, label, at}, chip{text, at} |

Every number in a comparison is computed here from the two source values (ratio, bar widths, glyph count),
never typed into the plan; the calculation string is returned in the scene for the manifest.
"""
from __future__ import annotations

import html
import math
import re

from fn.render.templates import SceneCtx, SceneOut

X0 = 108                     # title-safe left edge (compose.TITLE_SAFE_X)
WIDTH = 1080 - 2 * X0

_FIELD_LIMITS = {
    "gs_hook": {"kicker": 34, "question": 64, "badge": 30, "number": 10},
    "gs_phases": {"kicker": 34, "headline": 48, "step_label": 30, "step_sub": 40},
    "gs_section": {"kicker": 34, "headline": 48, "callout": 26, "dim": 12, "note": 40},
    "gs_compare": {"kicker": 34, "headline": 48, "label": 26},
    "gs_numbers": {"kicker": 34, "headline": 48, "value": 8, "item_label": 22, "statement": 70, "counter_label": 34, "chip": 30},
}

COMPUTED: list[dict] = []    # calculations of the last build (render_gigastruct writes them to the manifest)


def _word_start(ctx: SceneCtx, word: str) -> float | None:
    target = re.sub(r"[^\wäöüßøæå]", "", word.lower())
    for w in getattr(ctx, "words", None) or []:
        if re.sub(r"[^\wäöüßøæå]", "", w.text.lower()).startswith(target):
            return w.start
    return None


def _rel(ctx: SceneCtx, d: dict, default: float, out: SceneOut, key: str = "at") -> float:
    """Beat-relative seconds from a number, an "@Wort+0.5" string or (for key "at") at_word/at_offset."""
    v = d.get(key)
    if isinstance(v, (int, float)):
        return float(v)
    spec = v[1:] if isinstance(v, str) and v.startswith("@") else None
    if spec is None and key == "at" and d.get("at_word"):
        off = float(d.get("at_offset", 0))
        spec = f"{d['at_word']}{off:+}" if off else str(d["at_word"])
    if spec:
        m = re.match(r"^(.+?)([+\-]\d+(?:\.\d+)?)?$", spec)
        t = _word_start(ctx, m.group(1)) if m else None
        if t is not None:
            return max(0.0, t - ctx.start + float(m.group(2) or 0))
        out.problems.append(f"word anchor '{spec}' not found in the beat; default time used")
    return default


def _e(s) -> str:
    return html.escape(str(s))


def de_num(x: float, decimals: int = 0) -> str:
    """German number format: 73.500 / 7,3."""
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def _limit(scene: str, key: str, val, where: str, out: list[str]) -> None:
    lim = _FIELD_LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _head(ctx: SceneCtx, data: dict, scene: str, out: SceneOut, tl_at: float = 0.05) -> str:
    """Kicker (mono, accent) + headline at the top of the zone; returns html."""
    k, h = data.get("kicker", ""), data.get("headline", "")
    _limit(scene, "kicker", k, "kicker", out.problems)
    _limit(scene, "headline", h, "headline", out.problems)
    sid = ctx.sid
    parts = []
    if k:
        parts.append(f'<div class="gs-kicker" id="{sid}k"><span class="gs-tick"></span>{_e(k)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}k",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:{ctx.enter:.2f},ease:"power3.out"}},{ctx.t(tl_at):.3f});')
    if h:
        parts.append(f'<div class="gs-headline" id="{sid}h">{_e(h)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}h",{{opacity:0,y:18}},{{opacity:1,y:0,duration:{ctx.enter:.2f},ease:"power3.out"}},{ctx.t(tl_at + 0.12):.3f});')
        out.events.append(ctx.t(tl_at + 0.12))
    return f'<div class="gs-head" style="top:{ctx.zone_top}px">{"".join(parts)}</div>'


def hook(ctx: SceneCtx, data: dict) -> SceneOut:
    out = SceneOut(html="")
    sid = ctx.sid
    q, k = data.get("question", ""), data.get("kicker", "")
    _limit("gs_hook", "question", q, "question", out.problems)
    _limit("gs_hook", "kicker", k, "kicker", out.problems)
    q_at = _rel(ctx, data, 0.1, out, "question_at")
    parts = [f'<div class="gs-head" style="top:{ctx.zone_top}px">']
    if k:
        parts.append(f'<div class="gs-kicker" id="{sid}k"><span class="gs-tick"></span>{_e(k)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}k",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{ctx.t(0.05):.3f});')
    parts.append(f'<div class="gs-question" id="{sid}q">{_e(q)}</div></div>')
    out.tl.append(f'tl.fromTo("#{sid}q",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{ctx.t(q_at):.3f});')
    out.events.append(ctx.t(q_at))
    num = data.get("number") or {}
    if num:
        _limit("gs_hook", "number", num.get("value", ""), "number", out.problems)
        at = ctx.t(_rel(ctx, num, 1.4, out))
        parts.append(f'<div class="gs-plate" id="{sid}n" style="top:{int(num.get("y", 1010))}px"><span class="gs-plate-in"><span class="gs-bracket"></span>'
                     f'<span class="gs-bignum">{_e(num.get("value", ""))}</span><span class="gs-unit">{_e(num.get("unit", ""))}</span></span></div>')
        out.tl.append(f'tl.fromTo("#{sid}n",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}n .gs-bracket",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{at:.3f});')
        out.events.append(at)
    badge = data.get("badge") or {}
    if badge:
        _limit("gs_hook", "badge", badge.get("text", ""), "badge", out.problems)
        at = ctx.t(_rel(ctx, badge, 2.4, out))
        parts.append(f'<div class="gs-chiprow" style="top:{int(badge.get("y", 1150))}px"><div class="gs-chip gs-chip-accent" id="{sid}b">{_e(badge.get("text", ""))}</div></div>')
        out.tl.append(f'tl.fromTo("#{sid}b",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{at:.3f});')
        out.events.append(at)
    out.html = "".join(parts)
    return out


def phases(ctx: SceneCtx, data: dict) -> SceneOut:
    """Bauphasen: a phase rail under the headline; each step lights up at its time, label below."""
    out = SceneOut(html="")
    sid = ctx.sid
    head = _head(ctx, data, "gs_phases", out)
    steps = data.get("steps", [])[:5]
    n = max(1, len(steps))
    rail_y = ctx.zone_top + int(data.get("rail_dy", 190))
    gapx = WIDTH / max(1, n - 1) if n > 1 else 0
    dots, labels = [], []
    for i, s in enumerate(steps):
        _limit("gs_phases", "step_label", s.get("label", ""), f"step {i + 1}", out.problems)
        _limit("gs_phases", "step_sub", s.get("sub", ""), f"step {i + 1} sub", out.problems)
        x = X0 + i * gapx if n > 1 else X0 + WIDTH / 2
        at = ctx.t(_rel(ctx, s, 0.4 + i * 2.0, out))
        dots.append(f'<div class="gs-dot" id="{sid}d{i}" style="left:{x - 17:.0f}px;top:{rail_y - 17}px"><span>{i + 1}</span></div>')
        labels.append(f'<div class="gs-step" id="{sid}s{i}" style="top:{rail_y + 52}px"><div class="gs-step-l">{_e(s.get("label", ""))}</div>'
                      f'<div class="gs-step-s">{_e(s.get("sub", ""))}</div></div>')
        out.tl.append(f'tl.to("#{sid}d{i}",{{backgroundColor:"{ctx.pal["accent"]}",borderColor:"{ctx.pal["accent"]}",color:"{ctx.pal["bg"]}",scale:1.12,duration:0.25}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}s{i}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{at:.3f});')
        if i + 1 < n:
            nxt = ctx.t(_rel(ctx, steps[i + 1], 0.4 + (i + 1) * 2.0, SceneOut(html="")))
            out.tl.append(f'tl.to("#{sid}s{i}",{{opacity:0,duration:0.2}},{max(at + 0.35, nxt - 0.2):.3f});')
            out.tl.append(f'tl.to("#{sid}d{i}",{{scale:1,duration:0.2}},{max(at + 0.35, nxt - 0.2):.3f});')
            out.tl.append(f'tl.fromTo("#{sid}r{i}",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power1.inOut"}},{max(at + 0.3, nxt - 0.45):.3f});')
        out.events.append(at)
    rails = "".join(f'<div class="gs-rail" style="left:{X0 + i * gapx:.0f}px;top:{rail_y - 2}px;width:{gapx:.0f}px"><div class="gs-rail-fill" id="{sid}r{i}"></div></div>'
                    for i in range(n - 1))
    out.html = head + rails + "".join(dots) + "".join(labels)
    return out


def section(ctx: SceneCtx, data: dict) -> SceneOut:
    """Schnittmodell: callouts and dimension chips pinned to 3D anchors (positioned each frame by the 3D layer)."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_head(ctx, data, "gs_section", out)]
    for i, c in enumerate(data.get("callouts", [])):
        _limit("gs_section", "callout", c.get("text", ""), f"callout {i + 1}", out.problems)
        at = ctx.t(_rel(ctx, c, 0.6 + i * 0.8, out))
        side = c.get("side", "up")
        parts.append(f'<div class="gs-pin gs-pin-{side}" id="{sid}c{i}" data-anchor="{_e(c["anchor"])}"><span class="gs-pin-dot"></span>'
                     f'<span class="gs-pin-line"></span><span class="gs-pin-text">{_e(c.get("text", ""))}</span></div>')
        out.tl.append(f'tl.fromTo("#{sid}c{i} .gs-pin-text",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}c{i} .gs-pin-line",{{scaleY:0}},{{scaleY:1,duration:0.25}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}c{i} .gs-pin-dot",{{scale:0}},{{scale:1,duration:0.2}},{at:.3f});')
        out.events.append(at)
    callouts = data.get("callouts", [])
    first_callout = min((ctx.t(_rel(ctx, c, 0.6 + i * 0.8, SceneOut(html=""))) for i, c in enumerate(callouts)), default=None)
    for i, d in enumerate(data.get("dims", [])):
        _limit("gs_section", "dim", d.get("text", ""), f"dim {i + 1}", out.problems)
        at = ctx.t(_rel(ctx, d, 0.4 + i * 0.6, out))
        parts.append(f'<div class="gs-dim" id="{sid}m{i}" data-anchor="{_e(d["anchor"])}"><span>{_e(d.get("text", ""))}</span></div>')
        out.tl.append(f'tl.fromTo("#{sid}m{i} span",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{at:.3f});')
        if data.get("dims_out") and first_callout is not None and first_callout > at + 0.6:
            # the dimension chips make room before the callouts arrive (they share the end face)
            out.tl.append(f'tl.to("#{sid}m{i} span",{{opacity:0,duration:0.25}},{first_callout - 0.3:.3f});')
        out.events.append(at)
    note = data.get("note", "")
    if note:
        _limit("gs_section", "note", note, "note", out.problems)
        parts.append(f'<div class="gs-note" id="{sid}x" style="top:{ctx.zone_top + int(data.get("note_dy", 170))}px">{_e(note)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}x",{{opacity:0}},{{opacity:0.9,duration:0.3}},{ctx.t(0.8):.3f});')
    out.html = "".join(parts)
    return out


TOWER_SVG = ('<svg viewBox="0 0 40 80" class="gs-glyph-svg"><path d="M20 2 L22 18 L28 46 L36 78 L28 78 L20 58 L12 78 L4 78 L12 46 L18 18 Z" '
             'fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/><path d="M11 46 H29 M15 30 H25" stroke="currentColor" stroke-width="3"/></svg>')


def compare(ctx: SceneCtx, data: dict) -> SceneOut:
    """Größenvergleich: two bars with computed widths, the computed ratio, glyph count = floor(ratio)."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_head(ctx, data, "gs_compare", out)]
    a, b = data["a"], data["b"]
    for side, d in (("a", a), ("b", b)):
        _limit("gs_compare", "label", d.get("label", ""), f"{side}.label", out.problems)
    va, vb = float(a["value"]), float(b["value"])
    ratio = va / vb
    dec = int(data.get("decimals", 1))
    unit = a.get("unit", "")

    def num(x: float, d: int | None = None) -> str:
        """number in the video's language; values keep their own decimals (50.5 stays 50,5 / 50.5)"""
        if d is None:
            d = 0 if float(x).is_integer() else len(repr(float(x)).split(".")[1])
        return de_num(x, d) if getattr(ctx, "lang", "de") != "en" else f"{x:,.{d}f}"

    de_num_v = num
    calc = f"{num(va)} {unit} ÷ {num(vb)} {b.get('unit', unit)} = {num(ratio, 2)}"
    COMPUTED.append({"beat_scene": sid, "a": a, "b": b, "ratio": round(ratio, 4), "calculation": calc})
    top = ctx.zone_top + int(data.get("bars_dy", 560))
    row_h = int(data.get("row_h", 118))
    big, small = (va, vb) if va >= vb else (vb, va)
    # the reference (b) is spoken first in most scripts; rows keep the order of the plan unless "order": "ba"
    rows = [("a", a, va), ("b", b, vb)] if data.get("order", "ab") == "ab" else [("b", b, vb), ("a", a, va)]
    a_at, b_at, r_at = ctx.t(_rel(ctx, data, 0.4, out, "a_at")), ctx.t(_rel(ctx, data, 2.0, out, "b_at")), ctx.t(_rel(ctx, data, 3.6, out, "result_at"))
    bar_w = WIDTH - 40
    for j, (side, d, v) in enumerate(rows):
        w = bar_w * v / big
        at = a_at if side == "a" else b_at
        cls = "gs-bar-accent" if v == big else "gs-bar-ref"
        parts.append(f'<div class="gs-barrow" id="{sid}{side}" style="top:{top + j * row_h}px"><div class="gs-barlab">{_e(d.get("label", ""))}'
                     f'<b>{_e(de_num_v(v))} {_e(d.get("unit", ""))}</b></div><div class="gs-bar {cls}" id="{sid}{side}bar" style="width:{w:.1f}px"></div></div>')
        out.tl.append(f'tl.fromTo("#{sid}{side}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}{side}bar",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out"}},{at + 0.1:.3f});')
        out.events.append(at)
    ratio_txt = f"{num(ratio, dec)}×" if data.get("ratio_style", "times") == "times" else num(ratio, dec)
    parts.append(f'<div class="gs-ratio" id="{sid}r" style="top:{top + 2 * row_h + 8}px"><span class="gs-ratio-n">{_e(ratio_txt)}</span>'
                 f'<span class="gs-calc">{_e(calc)}</span></div>')
    out.tl.append(f'tl.fromTo("#{sid}r",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{r_at:.3f});')
    out.events.append(r_at)
    if data.get("glyph") == "tower":
        n = int(math.floor(ratio))
        COMPUTED[-1]["glyphs"] = n
        gl = "".join(f'<span class="gs-glyph" id="{sid}g{i}">{TOWER_SVG}</span>' for i in range(n))
        parts.append(f'<div class="gs-glyphs" style="top:{top - 150}px">{gl}</div>')
        for i in range(n):
            out.tl.append(f'tl.fromTo("#{sid}g{i}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.18}},{b_at + 0.5 + i * 0.12:.3f});')
        out.events.append(b_at + 0.5)
    out.html = "".join(parts)
    return out


def numbers(ctx: SceneCtx, data: dict) -> SceneOut:
    """Kennzahlen: up to three number tiles low in the zone; mode 'closing': statement + counter + chip."""
    if data.get("mode") == "closing":
        return closing(ctx, data)
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_head(ctx, data, "gs_numbers", out)]
    items = data.get("items", [])[:3]
    n = max(1, len(items))
    tw = (WIDTH - (n - 1) * 24) / n
    top = ctx.zone_top + int(data.get("tiles_dy", 600))
    for i, it in enumerate(items):
        _limit("gs_numbers", "value", it.get("value", ""), f"item {i + 1} value", out.problems)
        _limit("gs_numbers", "item_label", it.get("label", ""), f"item {i + 1} label", out.problems)
        at = ctx.t(_rel(ctx, it, 0.5 + i * 1.2, out))
        cls = " gs-tile-ref" if it.get("ref") else ""
        # long values (e.g. 200.000 t in a row of three) shrink to fit the tile: digits ~0.5 em, unit 46 px
        unit_w = len(str(it.get("unit", ""))) * 22 + 10
        fs = int(min(124, (tw - 52 - unit_w) / max(1, len(str(it.get("value", ""))) * 0.5)))
        parts.append(f'<div class="gs-tile{cls}" id="{sid}t{i}" style="left:{X0 + i * (tw + 24):.0f}px;width:{tw:.0f}px;top:{top}px">'
                     f'<div class="gs-tile-v" style="font-size:{fs}px">{_e(it.get("value", ""))}<small>{_e(it.get("unit", ""))}</small></div>'
                     f'<div class="gs-tile-l">{_e(it.get("label", ""))}</div></div>')
        out.tl.append(f'tl.fromTo("#{sid}t{i}",{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}t{i} .gs-tile-v",{{scale:0.86}},{{scale:1,duration:0.5,ease:"back.out(2)"}},{at:.3f});')
        out.events.append(at)
    note = data.get("note", "")
    if note:
        _limit("gs_section", "note", note, "note", out.problems)
        at = ctx.t(_rel(ctx, data, 0.8, out, "note_at"))
        parts.append(f'<div class="gs-note" id="{sid}x" style="top:{ctx.zone_top + int(data.get("note_dy", 170))}px">{_e(note)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}x",{{opacity:0}},{{opacity:0.9,duration:0.3}},{at:.3f});')
    out.html = "".join(parts)
    return out


def closing(ctx: SceneCtx, data: dict) -> SceneOut:
    """Abschluss in der Handlung: the model stays; statement, a computed progress counter (done/total blocks), follow chip."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_head(ctx, data, "gs_numbers", out)]
    st = data.get("statement", "")
    _limit("gs_numbers", "statement", st, "statement", out.problems)
    if st:
        parts.append(f'<div class="gs-statement" id="{sid}st" style="top:{ctx.zone_top + int(data.get("statement_dy", 0))}px">{_e(st)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}st",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{ctx.t(0.3):.3f});')
        out.events.append(ctx.t(0.3))
    cnt = data.get("counter") or {}
    if cnt:
        done, total = int(cnt["done"]), int(cnt["total"])
        _limit("gs_numbers", "counter_label", cnt.get("label", ""), "counter.label", out.problems)
        COMPUTED.append({"beat_scene": sid, "counter": f"{total} - {done} = {total - done} remaining"})
        at = ctx.t(_rel(ctx, cnt, 1.2, out))
        top = ctx.zone_top + int(cnt.get("dy", 560))
        blocks = "".join(f'<i class="{"on" if i < done else ""}" id="{sid}q{i}"></i>' for i in range(total))
        parts.append(f'<div class="gs-counter" id="{sid}cn" style="top:{top}px"><div class="gs-counter-n"><b>{done}</b> / {total}'
                     f'<span>{_e(cnt.get("label", ""))}</span></div><div class="gs-blocks">{blocks}</div></div>')
        out.tl.append(f'tl.fromTo("#{sid}cn",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{at:.3f});')
        for i in range(done):
            out.tl.append(f'tl.fromTo("#{sid}q{i}",{{scale:0.2}},{{scale:1,duration:0.25,ease:"back.out(3)"}},{at + 0.4 + i * 0.15:.3f});')
        out.events.append(at)
    chip = data.get("chip") or {}
    if chip:
        _limit("gs_numbers", "chip", chip.get("text", ""), "chip", out.problems)
        at = ctx.t(_rel(ctx, chip, 2.6, out))
        parts.append(f'<div class="gs-chiprow" style="top:{ctx.zone_top + int(chip.get("dy", 760))}px"><div class="gs-chip gs-chip-accent" id="{sid}ch">{_e(chip.get("text", ""))}</div></div>')
        out.tl.append(f'tl.fromTo("#{sid}ch",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{at:.3f});')
        out.events.append(at)
    out.html = "".join(parts)
    return out


TEMPLATES = {"gs_hook": hook, "gs_phases": phases, "gs_section": section, "gs_compare": compare, "gs_numbers": numbers}
HOOK_SCENE_TYPES = ["gs_hook"]
# flat limits of top-level text fields for fn.render.brand_scenes.text_limits (nested fields are checked in the templates)
LIMITS = {t: {k: v for k, v in lim.items() if k in ("kicker", "headline", "question", "statement", "note")} for t, lim in _FIELD_LIMITS.items()}


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):  # noqa: N802 (contract name)
    return css(pal, display, body, mono)


def css(pal: dict, display: str, body: str, mono: str) -> str:
    acc, bg, text, muted, surf = pal["accent"], pal["bg"], pal["text"], pal.get("muted", "#8F9CA8"), pal.get("surface", "#30465B")
    green = pal.get("signal_green", "#5CD08A")   # reached state only (elements on the seabed)
    shadow = "0 14px 34px rgba(6,14,24,0.48)"
    return f"""
#gs3d,#gs3dprev{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:0;}}
#gs3dprev{{visibility:hidden;}}
#bg{{display:none;}}
#gsshade{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1;pointer-events:none;
  background:
    linear-gradient(180deg,color-mix(in srgb,{bg} 86%,transparent) 0px,color-mix(in srgb,{bg} 55%,transparent) 300px,transparent 560px,transparent 1060px,color-mix(in srgb,{bg} 62%,transparent) 1250px,color-mix(in srgb,{bg} 90%,transparent) 1520px,{bg} 1920px),
    radial-gradient(ellipse 820px 1100px at 540px 820px,transparent 55%,rgba(6,14,24,0.42) 100%);}}
.scene{{z-index:5;}}
.gs-head{{position:absolute;left:{X0}px;width:{WIDTH}px;text-align:center;}}
.gs-kicker{{font-family:'FN {mono}';font-size:30px;letter-spacing:0.08em;text-transform:uppercase;color:{acc};display:flex;align-items:center;justify-content:center;gap:14px;margin-bottom:18px;}}
.gs-tick{{display:inline-block;width:34px;height:4px;background:{acc};}}
.gs-headline{{font-family:'FN {display}';font-weight:700;font-size:78px;line-height:1.04;color:{text};text-shadow:0 4px 22px rgba(6,14,24,0.65);}}
.gs-question{{font-family:'FN {display}';font-weight:700;font-size:88px;line-height:1.0;color:{text};text-shadow:0 4px 26px rgba(6,14,24,0.7);}}
.gs-plate{{position:absolute;left:{X0}px;width:{WIDTH}px;display:flex;justify-content:center;}}
.gs-plate-in{{position:relative;display:flex;align-items:baseline;gap:14px;padding:22px 34px 10px;background:color-mix(in srgb,{bg} 84%,transparent);border-radius:16px;box-shadow:{shadow};}}
.gs-bracket{{position:absolute;left:18px;right:18px;top:10px;height:14px;border:4px solid {acc};border-bottom:none;transform-origin:left center;}}
.gs-bignum{{font-family:'FN {display}';font-weight:700;font-size:168px;line-height:1;color:{acc};}}
.gs-unit{{font-family:'FN {display}';font-weight:600;font-size:76px;color:{text};}}
.gs-chiprow{{position:absolute;left:{X0}px;width:{WIDTH}px;display:flex;justify-content:center;}}
.gs-chip{{font-family:'FN {mono}';font-size:36px;font-weight:700;padding:14px 28px;border-radius:14px;background:color-mix(in srgb,{bg} 84%,transparent);border:3px solid {acc};color:{text};box-shadow:{shadow};}}
.gs-chip-accent{{background:{acc};color:{bg};border-color:{acc};}}
.gs-rail{{position:absolute;height:6px;background:color-mix(in srgb,{text} 26%,transparent);border-radius:3px;}}
.gs-rail-fill{{width:100%;height:100%;background:{acc};transform-origin:left center;transform:scaleX(0);border-radius:3px;}}
.gs-dot{{position:absolute;width:34px;height:34px;border-radius:50%;border:4px solid color-mix(in srgb,{text} 60%,transparent);background:{bg};color:{text};font-family:'FN {mono}';font-size:18px;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(6,14,24,0.5);}}
.gs-step{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:16px 26px 18px;background:color-mix(in srgb,{bg} 92%,transparent);border-left:8px solid {acc};border-radius:14px;box-shadow:{shadow};text-align:left;}}
.gs-step-l{{font-family:'FN {display}';font-weight:700;font-size:60px;line-height:1.05;color:{text};}}
.gs-step-s{{font-family:'FN {mono}';font-size:32px;color:{acc};margin-top:8px;}}
.gs-pin{{position:absolute;width:0;height:0;}}
.gs-pin-dot{{position:absolute;left:-10px;top:-10px;width:20px;height:20px;border-radius:50%;background:{acc};box-shadow:0 0 0 6px color-mix(in srgb,{bg} 70%,transparent);}}
.gs-pin-line{{position:absolute;left:-2px;width:4px;height:120px;background:{acc};transform-origin:50% 100%;}}
.gs-pin-up .gs-pin-line{{bottom:0;}}
.gs-pin-down .gs-pin-line{{top:0;transform-origin:50% 0%;}}
.gs-pin-text{{position:absolute;white-space:nowrap;transform:translateX(-50%);font-family:'FN {display}';font-weight:700;font-size:44px;color:{text};background:color-mix(in srgb,{bg} 90%,transparent);border-left:6px solid {acc};padding:8px 18px;border-radius:12px;box-shadow:{shadow};}}
.gs-pin-up .gs-pin-text{{bottom:120px;}}
.gs-pin-down .gs-pin-text{{top:120px;}}
.gs-dim{{position:absolute;width:0;height:0;}}
.gs-dim span{{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;font-family:'FN {mono}';font-size:40px;font-weight:700;color:{bg};background:{acc};padding:8px 16px;border-radius:12px;box-shadow:{shadow};}}
.gs-note{{position:absolute;left:{X0}px;width:{WIDTH}px;text-align:center;font-family:'FN {mono}';font-size:28px;color:{text};}}
.gs-barrow{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:12px 20px 16px;background:color-mix(in srgb,{bg} 90%,transparent);border-radius:14px;box-shadow:{shadow};}}
.gs-barlab{{display:flex;justify-content:space-between;font-family:'FN {display}';font-weight:600;font-size:40px;color:{text};margin-bottom:10px;}}
.gs-barlab b{{font-family:'FN {mono}';font-weight:700;font-size:38px;}}
.gs-bar{{height:30px;border-radius:6px;transform-origin:left center;}}
.gs-bar-accent{{background:{acc};}}
.gs-bar-ref{{background:color-mix(in srgb,{text} 70%,transparent);}}
.gs-ratio{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:10px 24px 14px;display:flex;align-items:center;gap:26px;background:color-mix(in srgb,{bg} 90%,transparent);border-radius:14px;border-top:6px solid {acc};box-shadow:{shadow};}}
.gs-ratio-n{{font-family:'FN {display}';font-weight:700;font-size:118px;line-height:1;color:{acc};}}
.gs-calc{{font-family:'FN {mono}';font-size:30px;line-height:1.3;color:{text};}}
.gs-glyphs{{position:absolute;left:{X0}px;width:{WIDTH}px;display:flex;gap:10px;color:{text};}}
.gs-glyph{{display:block;width:56px;height:112px;}}
.gs-glyph-svg{{width:100%;height:100%;}}
.gs-tile{{position:absolute;box-sizing:border-box;padding:22px 24px;border-top:8px solid {acc};background:color-mix(in srgb,{bg} 90%,transparent);border-radius:14px;box-shadow:{shadow};text-align:center;}}
.gs-tile-ref{{border-top-color:color-mix(in srgb,{text} 55%,transparent);}}
.gs-tile-v{{font-family:'FN {display}';font-weight:700;font-size:124px;line-height:1;color:{text};}}
.gs-tile-v small{{font-size:46px;margin-left:8px;color:{acc};}}
.gs-tile-ref .gs-tile-v small{{color:{muted};}}
.gs-tile-l{{font-family:'FN {mono}';font-size:30px;color:{text};margin-top:10px;}}
.gs-statement{{position:absolute;left:{X0}px;width:{WIDTH}px;text-align:center;font-family:'FN {display}';font-weight:700;font-size:78px;line-height:1.04;color:{text};text-shadow:0 4px 22px rgba(6,14,24,0.65);}}
.gs-counter{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;background:color-mix(in srgb,{bg} 90%,transparent);padding:20px 24px;border-radius:14px;box-shadow:{shadow};}}
.gs-counter-n{{font-family:'FN {display}';font-weight:600;font-size:56px;color:{text};display:flex;align-items:baseline;gap:14px;}}
.gs-counter-n b{{font-size:110px;color:{green};line-height:1;}}
.gs-counter-n span{{font-family:'FN {mono}';font-size:28px;color:{muted};margin-left:auto;}}
.gs-blocks{{display:grid;grid-template-columns:repeat(30,1fr);gap:5px;margin-top:16px;}}
.gs-blocks i{{display:block;height:20px;border-radius:3px;background:color-mix(in srgb,{text} 18%,transparent);}}
.gs-blocks i.on{{background:{green};}}
.st-accent{{color:{acc};}}
.st-green{{color:{green};}}
#root .xsrc-inner{{background:color-mix(in srgb,{bg} 86%,transparent);padding:4px 12px;margin-left:-12px;width:auto;max-width:832px;border-radius:10px;}}
"""


# Format "Bauaufgabe" (02.11.2026): scene types gb_* in the same namespace; see scenes_bauaufgabe.py
from pathlib import Path as _P  # noqa: E402
_gb_file = _P(__file__).with_name("scenes_bauaufgabe.py")
exec(compile(_gb_file.read_text(encoding="utf-8"), str(_gb_file), "exec"))
