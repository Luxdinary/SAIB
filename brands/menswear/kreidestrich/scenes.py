"""Suitwerk format "Kreidestrich" (02.11.2026): scene types kw_* (brand module part, loaded from brands/menswear/scenes.py).

Format bible: OneDrive\\Business\\02 Marke\\Suitwerk\\Format-Bibel.md. Everything happens on the tailor's table, seen from
above: a dark worsted cloth as the ground, tailor's chalk for every mark, a tape measure as the band on top and a
linen tester (Fadenzaehler) for the close-up. Fabric is drawn thread by thread from the weave (warp up or down at every
crossing), never as a texture picture; the weave draft (Bindungspatrone) is the same function written on squared paper.
Right and wrong stand side by side and are judged in chalk. A plan with layout.format == "kreidestrich" gets the
cloth layer (LAYER) instead of the atelier; the old suitwerk_* scenes stay unchanged.

| scene type | role                               | data |
|------------|------------------------------------|------|
| kw_hook    | two swatches on the table, chalk   | question, question_at, chalk_at, swatches[{label, kind}], labels_at, neq_at, lens_at, lens2_at, source |
|            | stroke, linen tester on a swatch   |      |
| kw_weave   | the weave built thread by thread   | kind (plain|twill), title, title_at, rows_at, row_step, rows, warp_at, weft_at, formula{text, at}, |
|            | in the linen tester (zoomed)       | shift_at, diag_at, note{text, at}, colors_note, source |
| kw_draft   | weave draft on squared paper       | left/right{kind, title, word, word_at}, start_at, row_step, legend{text, at}, source |
| kw_flip    | both swatches turned over          | left/right{kind, title, front, back}, flip_at, left_at, right_at, arrow_at, source |
| kw_close   | verdict in chalk, the tilt test,   | lines[{text, at}], chip{text, at}, tilt_at, rule{text, at}, sign_at, claim, source |
|            | sign-off                           |      |

Times: seconds from the beat start or "w:Wort[#n][+0.3]" (start of that spoken word in the beat). An anchor that is not
spoken is reported as a problem and the default time is used. Scene content stays inside x 108-930 and y 290-1100;
the source line sits at y 1112 (below the scenes, above the captions).
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

X0, X1 = 108, 930
SRC_Y = 1112
CHALK = "#EEE7D7"
CHALK_DIM = "rgba(238,231,215,0.62)"
RED_CHALK = "#E59A8C"              # chalk for "wrong", only where something is wrong
GREEN_CHALK = "#A9D3B0"            # chalk for "right"
WARP = ("#3E5C8E", "#8FB0DE")      # zoomed panel: warp (Kette) dark edge, light centre
WEFT = ("#A8925F", "#F1E3BC")      # zoomed panel: weft (Schuss)
NAVY_WARP = ("#1F3050", "#5675A8")  # swatches: navy worsted; warp a little lighter than weft so the weave reads
NAVY_WEFT = ("#0F1828", "#2A3B5C")
LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo" / "suitwerk-mark.svg"

LIMITS: dict[str, dict[str, int]] = {
    "kw_hook": {"question": 34, "label": 16, "source": 70},
    "kw_weave": {"title": 18, "formula": 24, "note": 34, "source": 70},
    "kw_draft": {"title": 16, "word": 16, "legend": 30, "source": 70},
    "kw_flip": {"title": 16, "front": 22, "back": 28, "source": 70},
    "kw_close": {"line": 30, "chip": 44, "rule": 30, "claim": 40, "sign_note": 30, "source": 70},
}
HOOK_SCENE_TYPES = ["kw_hook"]
SERIES = {"stoff": {"de": "Unter dem Fadenzähler", "en": "Under the linen tester"},
          "anprobe": {"de": "Anprobe", "en": "Fitting"},
          "mass": {"de": "Nachgemessen", "en": "Measured"},
          "anlass": {"de": "Die Kleiderordnung", "en": "The dress code"}}


def _e(s) -> str:
    return html.escape(str(s))


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", str(s).lower())


def _rel(c: SceneCtx, v, default: float, out: SceneOut) -> float:
    """Beat-relative seconds from a number or a "w:Wort[#n][+0.4]" string."""
    if v is None or v == "":
        return float(default)
    if isinstance(v, (int, float)):
        return float(v)
    m = re.fullmatch(r"w:(.+?)(?:#(\d+))?([+\-]\d+(?:\.\d+)?)?", str(v).strip())
    if m:
        stem, nth = _norm(m.group(1)), int(m.group(2) or 1)
        hits = [w for w in (c.words or []) if _norm(w.text).startswith(stem)]
        if len(hits) >= nth:
            return max(0.0, hits[nth - 1].start - c.start + float(m.group(3) or 0))
    out.problems.append(f"{c.sid}: word anchor {v!r} not spoken in this beat; default time used")
    return float(default)


def _chk(scene: str, key: str, val, where: str, out: SceneOut) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _frame(c: SceneCtx) -> list[str]:
    s = c.sid
    return [f'tl.fromTo("#{s} .kw-in",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power1.out"}},{c.start:.3f});',
            f'tl.to("#{s} .kw-in",{{opacity:0,duration:0.22,ease:"power1.in"}},{max(c.start + c.enter + 0.05, c.end - 0.22):.3f});']


def _in(c: SceneCtx, sel: str, at: float, *, dy: int = 16, dur: float = 0.4) -> str:
    return (f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur:.2f},ease:"power2.out"}},'
            f'{c.t(at):.3f});')


def _draw(c: SceneCtx, sel: str, at: float, dur: float = 0.6) -> str:
    """Chalk stroke drawn on (paths carry pathLength="1" and the class kw-st)."""
    return (f'tl.fromTo("#{c.sid} {sel}",{{strokeDashoffset:1,opacity:1}},{{strokeDashoffset:0,duration:{dur:.2f},'
            f'ease:"power1.inOut"}},{c.t(at):.3f});')


def _deep(c: SceneCtx) -> bool:
    """The plan uses the deeper stage (zone down to about y 1240, layout.zone_lower_right_px <= 940)."""
    return c.zone_top + c.zone_h > 1150


def _src_y(c: SceneCtx) -> int:
    return c.zone_top + c.zone_h - 70 if _deep(c) else SRC_Y


def _source(c: SceneCtx, d: dict, out: SceneOut, scene: str) -> str:
    src = d.get("source", "")
    if not src:
        return ""
    _chk(scene, "source", src, "source", out)
    word = "Quelle" if c.lang == "de" else "Source"
    return f'<div class="kw-src" style="top:{_src_y(c)}px"><b>{word}</b> {_e(src)}</div>'


# --- weave geometry ------------------------------------------------------------------------------------------------

def warp_up(kind: str, i: int, j: int) -> bool:
    """True where warp thread i lies over weft thread j. plain: over one, under one, the next weft the other way round.
    twill (2/2): over two, under two, every weft shifted by one thread; the line runs from top right to bottom left."""
    if kind == "plain":
        return (i + j) % 2 == 0
    if kind == "twill":
        return (i + j) % 4 in (0, 1)
    raise ValueError(f"unknown weave {kind!r}")


def _grads(uid: str, warp: tuple[str, str], weft: tuple[str, str]) -> str:
    a, b = warp
    p, q = weft
    return (f'<linearGradient id="{uid}gw" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="0.45" stop-color="{b}"/><stop offset="1" stop-color="{a}"/></linearGradient>'
            f'<linearGradient id="{uid}gf" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{p}"/>'
            f'<stop offset="0.45" stop-color="{q}"/><stop offset="1" stop-color="{p}"/></linearGradient>')


def weave_svg(uid: str, kind: str, n: int, cell: float, *, warp=WARP, weft=WEFT, ratio: float = 0.76,
              rows: int | None = None, shuttle: bool = True) -> tuple[str, float]:
    """Zoomed weave, n warps x rows wefts, drawn in three layers: warps, then the weft rows (each grows from the left,
    class {uid}-wf{j}), then the warp pieces that lie on top. Returns (svg inner, panel size)."""
    rows = rows or n
    w = cell * ratio
    size = n * cell
    hgt = rows * cell
    warps = "".join(f'<rect x="{(i + 0.5) * cell - w / 2:.1f}" y="-6" width="{w:.1f}" height="{hgt + 12:.1f}" rx="{w / 2:.1f}" fill="url(#{uid}gw)"/>'
                    for i in range(n))
    wefts = "".join(f'<rect class="{uid}-wf {uid}-wf{j}" x="-6" y="{(j + 0.5) * cell - w / 2:.1f}" width="{size + 12:.1f}" height="{w:.1f}" '
                    f'rx="{w / 2:.1f}" fill="url(#{uid}gf)"/>' for j in range(rows))
    tops = []
    for j in range(rows):
        for i in range(n):
            if warp_up(kind, i, j):
                tops.append(f'<rect x="{(i + 0.5) * cell - w / 2:.1f}" y="{j * cell - 0.5:.1f}" width="{w:.1f}" height="{cell + 1:.1f}" fill="url(#{uid}gw)"/>')
    shut = ""
    if shuttle:
        shut = (f'<g class="{uid}-sh" opacity="0"><path d="M0,{-w * 0.62:.1f} L{cell * 0.9:.1f},0 L0,{w * 0.62:.1f} Z" fill="{CHALK}"/>'
                f'<rect x="-14" y="{-w * 0.26:.1f}" width="16" height="{w * 0.52:.1f}" fill="{CHALK}"/></g>')
    svg = (f'<defs>{_grads(uid, warp, weft)}<filter id="{uid}sd" x="-20%" y="-20%" width="140%" height="140%">'
           f'<feDropShadow dx="0" dy="0" stdDeviation="{cell * 0.06:.1f}" flood-color="#000" flood-opacity="0.55"/></filter></defs>'
           f'<g>{warps}</g><g filter="url(#{uid}sd)">{wefts}</g><g filter="url(#{uid}sd)">{"".join(tops)}</g>{shut}')
    return svg, size


def weave_pattern(pid: str, kind: str, cell: float, *, warp=NAVY_WARP, weft=NAVY_WEFT, mirror: bool = False) -> str:
    """SVG <pattern> of one repeat (plain 2x2, twill 4x4) for a swatch seen at normal size; mirror = back side."""
    rep = 2 if kind == "plain" else 4
    w = cell * 0.8
    size = rep * cell
    body = [_grads(pid, warp, weft)]
    for i in range(rep):
        body.append(f'<rect x="{(i + 0.5) * cell - w / 2:.2f}" y="0" width="{w:.2f}" height="{size:.2f}" fill="url(#{pid}gw)"/>')
    for j in range(rep):
        body.append(f'<rect x="0" y="{(j + 0.5) * cell - w / 2:.2f}" width="{size:.2f}" height="{w:.2f}" fill="url(#{pid}gf)"/>')
    for j in range(rep):
        for i in range(rep):
            if warp_up(kind, i, j):
                body.append(f'<rect x="{(i + 0.5) * cell - w / 2:.2f}" y="{j * cell:.2f}" width="{w:.2f}" height="{cell:.2f}" fill="url(#{pid}gw)"/>')
    tr = f' patternTransform="scale(-1,1)"' if mirror else ""
    return (f'<pattern id="{pid}" width="{size:.2f}" height="{size:.2f}" patternUnits="userSpaceOnUse"{tr}>'
            f'<rect width="{size:.2f}" height="{size:.2f}" fill="{warp[0]}"/>{"".join(body)}</pattern>')


def _pinked(w: float, h: float, tooth: float = 12.0) -> str:
    """Outline of a swatch cut with pinking shears (zigzag on all four edges)."""
    pts = []
    nx, ny = max(2, round(w / tooth)), max(2, round(h / tooth))
    sx, sy = w / nx, h / ny
    d = tooth * 0.45
    for k in range(nx):
        pts += [(k * sx, 0), ((k + 0.5) * sx, d)]
    for k in range(ny):
        pts += [(w, k * sy), (w - d, (k + 0.5) * sy)]
    for k in range(nx):
        pts += [(w - k * sx, h), (w - (k + 0.5) * sx, h - d)]
    for k in range(ny):
        pts += [(0, h - k * sy), (d, h - (k + 0.5) * sy)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def fuzz_svg(cls: str, w: float, h: float, n: int, length: float, seed: int, color: str = "#B9C8E2", opacity: float = 0.72) -> str:
    """Loose fibre ends on a cloth surface (woollen yarn, milled cloth): short random strokes, deterministic."""
    import random
    rnd = random.Random(seed)
    strokes = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        a = rnd.uniform(0, 6.283)
        ln = length * rnd.uniform(0.5, 1.2)
        import math as _m
        cx, cy = x + _m.cos(a + 0.6) * ln * 0.5, y + _m.sin(a + 0.6) * ln * 0.5
        strokes.append(f'M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {x + _m.cos(a) * ln:.1f},{y + _m.sin(a) * ln:.1f}')
    return (f'<path class="{cls}" d="{" ".join(strokes)}" fill="none" stroke="{color}" stroke-opacity="{opacity}" '
            f'stroke-width="1.7" stroke-linecap="round"/>')


def swatch_svg(uid: str, kind: str, w: float, h: float, cell: float = 9.0, *, mirror: bool = False, fuzz: bool = False) -> str:
    """A navy worsted swatch with pinked edges, lit from the top left; fuzz = woollen surface with fibre ends."""
    pid = f"{uid}p"
    outline = _pinked(w, h)
    hair = ""
    if fuzz:
        hair = (f'<clipPath id="{uid}c"><path d="{outline}"/></clipPath>'
                f'<g clip-path="url(#{uid}c)">{fuzz_svg("kw-fz", w, h, int(w * h / 230), 16, len(uid) * 7 + 3, opacity=0.6)}</g>')
    return (f'<svg class="kw-sw" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" style="overflow:visible">'
            f'<defs>{weave_pattern(pid, kind, cell, mirror=mirror)}'
            f'<radialGradient id="{uid}l" cx="0.28" cy="0.2" r="0.95"><stop offset="0" stop-color="#FFF6E0" stop-opacity="0.16"/>'
            f'<stop offset="0.6" stop-color="#FFF6E0" stop-opacity="0.02"/><stop offset="1" stop-color="#000" stop-opacity="0.32"/></radialGradient></defs>'
            f'<path d="{outline}" fill="url(#{pid})"/>{hair}<path d="{outline}" fill="url(#{uid}l)"/></svg>')


def linen_tester(uid: str, win: float, inner: str) -> str:
    """Folding linen tester from above: metal frame, a scale on two inner edges, the magnified view in the window."""
    fr = 22
    o = win + 2 * fr
    ticks = []
    for k in range(0, 21):
        x = fr + k * win / 20
        ln = 14 if k % 5 == 0 else 7
        ticks.append(f'<line x1="{x:.1f}" y1="{fr}" x2="{x:.1f}" y2="{fr + ln}"/>')
        ticks.append(f'<line x1="{fr}" y1="{x:.1f}" x2="{fr + ln}" y2="{x:.1f}"/>')
    return (f'<div class="kw-lt" id="{uid}" style="width:{o:.0f}px;height:{o:.0f}px">'
            f'<div class="kw-lt-win" style="left:{fr}px;top:{fr}px;width:{win:.0f}px;height:{win:.0f}px">{inner}'
            f'<div class="kw-lt-glass"></div></div>'
            f'<svg class="kw-lt-fr" viewBox="0 0 {o:.0f} {o:.0f}" width="{o:.0f}" height="{o:.0f}" style="overflow:visible">'
            f'<defs><linearGradient id="{uid}m" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#E9E4D8"/>'
            f'<stop offset="0.5" stop-color="#9C978C"/><stop offset="1" stop-color="#D2CCBE"/></linearGradient></defs>'
            f'<path fill-rule="evenodd" fill="url(#{uid}m)" d="M0,0 H{o:.0f} V{o:.0f} H0 Z M{fr},{fr} V{fr + win:.0f} H{fr + win:.0f} V{fr} Z"/>'
            f'<rect x="-66" y="{o / 2 - 46:.0f}" width="68" height="92" rx="10" fill="url(#{uid}m)" opacity="0.92"/>'
            f'<g stroke="#2A2A2A" stroke-width="2">{"".join(ticks)}</g></svg></div>')


# --- kw_hook: two swatches, a chalk stroke, the linen tester ------------------------------------------------------

def kw_hook(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    q = d.get("question", "")
    _chk("kw_hook", "question", q, "question", out)
    sws = (d.get("swatches") or [{"kind": "plain"}, {"kind": "twill"}])[:2]
    sw_w, sw_h, sw_top = 330, (520 if _deep(c) else 420), zt + 250
    xs = (X0 + 30, X1 - 30 - sw_w)
    parts = []
    for k, sw in enumerate(sws):
        _chk("kw_hook", "label", sw.get("label", ""), f"swatches{k}.label", out)
        parts.append(f'<div class="kw-swbox sw{k}" style="left:{xs[k]}px;top:{sw_top}px">{swatch_svg(f"{s}s{k}", sw["kind"], sw_w, sw_h, fuzz=bool(sw.get("fuzz")))}</div>')
        if sw.get("label"):
            parts.append(f'<div class="kw-chalk kw-lab lab{k}" style="left:{xs[k]}px;width:{sw_w}px;top:{sw_top + sw_h + 22}px">{_e(sw["label"])}</div>')
    win = 250
    views = []
    for k, sw in enumerate(sws):
        inner, size = weave_svg(f"{s}z{k}", sw["kind"], 8, 34, warp=NAVY_WARP, weft=NAVY_WEFT, shuttle=False)
        if sw.get("fuzz"):
            inner += fuzz_svg("kw-fz", size, size, 140, 30, 11 + k, "#9FB3D6", 0.7)
        views.append(f'<svg class="kw-zv zv{k}" viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" '
                     f'style="position:absolute;inset:0;opacity:{1 if k == 0 else 0}">{inner}</svg>')
    lt_left = [xs[0] + sw_w / 2 - (win + 44) / 2, xs[1] + sw_w / 2 - (win + 44) / 2]
    lt_top = sw_top + (110 if _deep(c) else 60)
    midx = (xs[0] + sw_w + xs[1]) / 2
    out.html = f"""<div class="kw-in">
  <div class="kw-q" style="top:{zt + 10}px">{_e(q)}</div>
  <svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-stroke" pathLength="1" d="M{X0 + 40},{zt + 196} C{X0 + 260},{zt + 180} {X1 - 300},{zt + 214} {X1 - 40},{zt + 192}"/>
   <path class="kw-st kw-neq" pathLength="1" d="M{midx - 30:.0f},{sw_top + 180} L{midx + 30:.0f},{sw_top + 180} M{midx - 30:.0f},{sw_top + 214} L{midx + 30:.0f},{sw_top + 214} M{midx + 22:.0f},{sw_top + 156} L{midx - 22:.0f},{sw_top + 238}"/></svg>
  {"".join(parts)}
  <div class="kw-ltbox" style="left:{lt_left[0]:.0f}px;top:{lt_top}px">{linen_tester(f"{s}lt", win, "".join(views))}</div>
</div>"""
    out.tl += _frame(c)
    q_at = _rel(c, d.get("question_at"), 0.3, out)
    chalk_at = _rel(c, d.get("chalk_at"), q_at + 0.5, out)
    lab_at = _rel(c, d.get("labels_at"), 2.0, out)
    neq_at = _rel(c, d.get("neq_at"), 3.0, out)
    lens_at = _rel(c, d.get("lens_at"), 5.0, out)
    lens2_at = _rel(c, d.get("lens2_at"), lens_at + 2.2, out)
    out.tl.append(_in(c, ".kw-q", q_at, dy=20, dur=0.5))
    out.tl.append(_draw(c, ".kw-stroke", chalk_at, 0.7))
    for k in range(len(sws)):
        out.tl.append(f'tl.fromTo("#{s} .sw{k}",{{opacity:0,y:-40,rotation:{-4 if k == 0 else 5}}},{{opacity:1,y:0,rotation:{-2 if k == 0 else 2},duration:0.6,ease:"power2.out"}},{c.t(0.1 + 0.3 * k):.3f});')
        out.tl.append(_in(c, f".lab{k}", lab_at + 0.25 * k, dy=8))
    out.tl.append(_draw(c, ".kw-neq", neq_at, 0.6))
    out.tl.append(f'tl.to("#{s} .kw-neq",{{opacity:0,duration:0.25}},{c.t(max(neq_at + 0.8, lens_at - 0.1)):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .kw-ltbox",{{opacity:0,x:{lt_left[1] - lt_left[0] + 160:.0f},y:180}},{{opacity:1,x:0,y:0,duration:0.8,ease:"power2.out"}},{c.t(lens_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .zv0",{{scale:0.7,transformOrigin:"50% 50%"}},{{scale:1,duration:{max(0.8, lens2_at - lens_at):.2f},ease:"none"}},{c.t(lens_at):.3f});')
    out.tl.append(f'tl.to("#{s} .kw-ltbox",{{x:{lt_left[1] - lt_left[0]:.0f},duration:0.8,ease:"power2.inOut"}},{c.t(lens2_at):.3f});')
    out.tl.append(f'tl.to("#{s} .zv0",{{opacity:0,duration:0.4}},{c.t(lens2_at + 0.2):.3f});')
    out.tl.append(f'tl.to("#{s} .zv1",{{opacity:1,duration:0.4}},{c.t(lens2_at + 0.2):.3f});')
    out.html += _source(c, d, out, "kw_hook")
    out.events = sorted({c.start, c.t(q_at), c.t(chalk_at), c.t(lab_at), c.t(neq_at), c.t(lens_at), c.t(lens2_at)})
    return out


# --- kw_weave: the weave built thread by thread -------------------------------------------------------------------

def kw_weave(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    kind = d.get("kind", "plain")
    n = int(d.get("n", 8))
    rows = int(d.get("rows", n))
    for k in ("title",):
        _chk("kw_weave", k, d.get(k, ""), k, out)
    f = d.get("formula") or {}
    note = d.get("note") or {}
    _chk("kw_weave", "formula", f.get("text", ""), "formula.text", out)
    _chk("kw_weave", "note", note.get("text", ""), "note.text", out)
    win = 540 if _deep(c) else 460
    cell = win / n
    inner, size = weave_svg(f"{s}w", kind, n, cell, rows=rows)
    lt_left, lt_top = 540 - (win + 44) / 2 + 40, zt + 190
    wx, wy = lt_left + 22, lt_top + 22
    # chalk marks on the zoomed weave (in window coordinates)
    marks = []
    if kind == "twill":
        # the twill line through the warp floats: cells with i + j = 4m + 0.5 (top right to bottom left)
        k0 = 4 * (n // 4)
        a = (k0 + 1.5) * cell
        x1, y1 = min(size, a), max(0.0, a - size)
        x2, y2 = max(0.0, a - size), min(size, a)
        marks.append(f'<path class="kw-st kw-diag" pathLength="1" d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}"/>')
        # one thread step: the float over warps 4-5 in row 0 lies over warps 3-4 in row 1 (one thread to the left)
        hx, hy = 4.15 * cell, 1.35 * cell
        marks.append(f'<path class="kw-st kw-shift" pathLength="1" d="M{5.0 * cell:.0f},{0.55 * cell:.0f} L{hx:.0f},{hy:.0f} '
                     f'M{hx + 4:.0f},{hy - 30:.0f} L{hx:.0f},{hy:.0f} L{hx + 30:.0f},{hy - 2:.0f}"/>')
    over = (f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" '
            f'style="position:absolute;inset:0;overflow:visible">{"".join(marks)}</svg>')
    view = f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" style="position:absolute;inset:0">{inner}</svg>'
    # labels: warp arrow on the left (vertical), weft arrow on top (horizontal)
    lab_warp = "Kette" if c.lang == "de" else "Warp"
    lab_weft = "Schuss" if c.lang == "de" else "Weft"
    out.html = f"""<div class="kw-in">
  <div class="kw-title" style="top:{zt + 4}px"><span class="kw-ttl">{_e(d.get("title", ""))}</span></div>
  <div class="kw-formula" style="top:{zt + 86}px">{_e(f.get("text", ""))}</div>
  <div class="kw-ltbox" style="left:{lt_left:.0f}px;top:{lt_top}px">{linen_tester(f"{s}lt", win, view + over)}</div>
  <svg class="kw-over" viewBox="0 0 1080 1920">
   <path class="kw-st kw-arw kw-wa" pathLength="1" d="M{X0 + 12},{wy + 40:.0f} L{X0 + 12},{wy + 300:.0f} M{X0},{wy + 284:.0f} L{X0 + 12},{wy + 302:.0f} L{X0 + 24},{wy + 284:.0f}"/>
   <path class="kw-st kw-arw kw-fa" pathLength="1" d="M{wx + 60:.0f},{lt_top - 20} L{wx + 330:.0f},{lt_top - 20} M{wx + 312:.0f},{lt_top - 32} L{wx + 332:.0f},{lt_top - 20} L{wx + 312:.0f},{lt_top - 8}"/>
  </svg>
  <div class="kw-chalk kw-side kw-wl" style="left:{X0 - 4}px;top:{wy + 316:.0f}px">{lab_warp}</div>
  <div class="kw-chalk kw-side kw-fl" style="left:{wx + 350:.0f}px;top:{lt_top - 44}px">{lab_weft}</div>
  <div class="kw-note" style="top:{zt + 80}px">{_e(note.get("text", ""))}</div>
  <div class="kw-cnote" style="top:{lt_top + win + 64:.0f}px">{_e(d.get("colors_note", ""))}</div>
</div>"""
    out.tl += _frame(c)
    t_at = _rel(c, d.get("title_at"), 0.1, out)
    out.tl.append(_in(c, ".kw-title", t_at, dy=14))
    out.tl.append(f'tl.fromTo("#{s} .kw-ltbox",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{c.t(0.15):.3f});')
    out.tl.append(f'tl.set("#{s} .{s}w-wf",{{attr:{{width:0}}}},{c.start:.3f});')
    warp_at = _rel(c, d.get("warp_at"), 0.6, out)
    weft_at = _rel(c, d.get("weft_at"), 1.6, out)
    out.tl.append(_draw(c, ".kw-wa", warp_at, 0.5))
    out.tl.append(_in(c, ".kw-wl", warp_at + 0.2, dy=8))
    out.tl.append(_draw(c, ".kw-fa", weft_at, 0.5))
    out.tl.append(_in(c, ".kw-fl", weft_at + 0.2, dy=8))
    r_at = _rel(c, d.get("rows_at"), weft_at, out)
    step = float(d.get("row_step", 0.55))
    first = float(d.get("first_row", 1.2))      # the first weft goes slowly (over, under is spoken on it)
    events = [c.start, c.t(t_at), c.t(warp_at), c.t(weft_at)]
    t_row = r_at
    for j in range(rows):
        dur = first if j == 0 else min(step * 0.9, 0.5)
        out.tl.append(f'tl.fromTo("#{s} .{s}w-wf{j}",{{attr:{{width:0}}}},{{attr:{{width:{size + 12:.1f}}},duration:{dur:.2f},ease:"none"}},{c.t(t_row):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .{s}w-sh",{{opacity:1,x:-6,y:{(j + 0.5) * cell:.1f}}},{{x:{size + 6:.1f},duration:{dur:.2f},ease:"none"}},{c.t(t_row):.3f});')
        events.append(c.t(t_row))
        t_row += first + 0.25 if j == 0 else step
    out.tl.append(f'tl.to("#{s} .{s}w-sh",{{opacity:0,duration:0.2}},{c.t(t_row):.3f});')
    if f.get("text"):
        fa = _rel(c, f.get("at"), r_at + 0.4, out)
        out.tl.append(_in(c, ".kw-formula", fa, dy=10))
        events.append(c.t(fa))
    if kind == "twill":
        if d.get("shift_at") is not None:
            sa = _rel(c, d.get("shift_at"), 0.0, out)
            out.tl.append(_draw(c, ".kw-shift", sa, 0.4))
            events.append(c.t(sa))
        if d.get("diag_at") is not None:
            da = _rel(c, d.get("diag_at"), 0.0, out)
            out.tl.append(_draw(c, ".kw-diag", da, 0.9))
            events.append(c.t(da))
    if note.get("text"):
        na = _rel(c, note.get("at"), c.duration - 2.0, out)
        out.tl.append(f'tl.to("#{s} .kw-formula",{{opacity:0,duration:0.2}},{c.t(na - 0.25):.3f});')   # the note takes the formula line
        out.tl.append(_in(c, ".kw-note", na, dy=10))
        events.append(c.t(na))
    if d.get("colors_note"):
        out.tl.append(_in(c, ".kw-cnote", weft_at + 0.6, dy=6))
    out.html += _source(c, d, out, "kw_weave")
    out.events = sorted(set(events))
    return out


# --- kw_draft: the weave draft on squared paper ------------------------------------------------------------------

def kw_draft(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    n, cs = 8, 44
    gw = n * cs
    tops = zt + 230
    xs = (X0 + 14, X1 - 14 - gw)
    sides, tl, events = [], [], [c.start]
    start = _rel(c, d.get("start_at"), 1.0, out)
    step = float(d.get("row_step", 0.28))
    for k, key in enumerate(("left", "right")):
        sd = d.get(key) or {}
        kind = sd.get("kind", "plain" if k == 0 else "twill")
        _chk("kw_draft", "title", sd.get("title", ""), f"{key}.title", out)
        _chk("kw_draft", "word", sd.get("word", ""), f"{key}.word", out)
        cells = []
        for j in range(n):
            for i in range(n):
                if warp_up(kind, i, j):
                    cells.append(f'<rect class="r{j}" x="{i * cs + 3}" y="{j * cs + 3}" width="{cs - 6}" height="{cs - 6}" fill="#1E2A44"/>')
        grid = "".join(f'<line x1="{i * cs}" y1="0" x2="{i * cs}" y2="{gw}"/><line x1="0" y1="{i * cs}" x2="{gw}" y2="{i * cs}"/>' for i in range(n + 1))
        stair = ""
        if kind == "twill":
            stair = f'<path class="kw-st kw-stair" pathLength="1" d="M{gw - 0.5 * cs:.0f},{0.5 * cs:.0f} L{0.5 * cs:.0f},{gw - 0.5 * cs:.0f}"/>'
        sides.append(f'<div class="kw-paper p{k}" style="left:{xs[k] - 24}px;top:{tops - 24}px;width:{gw + 48}px;height:{gw + 48}px"></div>'
                     f'<div class="kw-ptitle pt{k}" style="left:{xs[k]}px;width:{gw}px;top:{tops - 96}px">{_e(sd.get("title", ""))}</div>'
                     f'<svg class="kw-grid g{k}" viewBox="0 0 {gw} {gw}" width="{gw}" height="{gw}" style="left:{xs[k]}px;top:{tops}px">'
                     f'<g stroke="#B2584A" stroke-opacity="0.55" stroke-width="1.5">{grid}</g>{"".join(cells)}'
                     f'<g class="kw-redst">{stair}</g></svg>'
                     f'<div class="kw-chalk kw-word w{k}" style="left:{xs[k]}px;width:{gw}px;top:{tops + gw + 44}px">{_e(sd.get("word", ""))}</div>')
        tl.append(f'tl.fromTo("#{s} .p{k},#{s} .g{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.45,ease:"power2.out"}},{c.t(0.1 + 0.2 * k):.3f});')
        tl.append(_in(c, f".pt{k}", 0.3 + 0.2 * k, dy=10))
        tl.append(f'tl.set("#{s} .g{k} rect",{{opacity:0}},{c.start:.3f});')
        for j in range(n):
            tl.append(f'tl.to("#{s} .g{k} .r{j}",{{opacity:1,duration:0.12}},{c.t(start + j * step):.3f});')
        wa = _rel(c, sd.get("word_at"), start + n * step + 0.5 * k, out)
        tl.append(_in(c, f".w{k}", wa, dy=8))
        events += [c.t(wa)]
        if kind == "twill":
            tl.append(_draw(c, f".g{k} .kw-stair", wa, 0.8))
    events += [c.t(start), c.t(start + n * step)]
    lg = d.get("legend") or {}
    _chk("kw_draft", "legend", lg.get("text", ""), "legend.text", out)
    out.html = f"""<div class="kw-in">
  <div class="kw-legend" style="top:{zt + 14}px"><i></i><span>{_e(lg.get("text", ""))}</span></div>
  {"".join(sides)}
</div>"""
    out.tl += _frame(c) + tl
    if lg.get("text"):
        la = _rel(c, lg.get("at"), start - 0.3, out)
        out.tl.append(_in(c, ".kw-legend", la, dy=10))
        events.append(c.t(la))
    out.html += _source(c, d, out, "kw_draft")
    out.events = sorted(set(events))
    return out


# --- kw_flip: both swatches turned over ---------------------------------------------------------------------------

def kw_flip(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    sw_w, sw_h = 360, (540 if _deep(c) else 470)
    top = zt + 150
    xs = (X0 + 30, X1 - 30 - sw_w)
    parts, events = [], [c.start]
    flip_at = _rel(c, d.get("flip_at"), 0.6, out)
    out.tl += _frame(c)

    def turn(sel_out: str, sel_in: str, at: float) -> None:
        # turn over around the vertical axis: one side shrinks to an edge, the other opens from it
        out.tl.append(f'tl.to("#{s} {sel_out}",{{scaleX:0,duration:0.32,ease:"power2.in",transformOrigin:"50% 50%"}},{c.t(at):.3f});')
        out.tl.append(f'tl.set("#{s} {sel_out}",{{opacity:0}},{c.t(at + 0.32):.3f});')
        out.tl.append(f'tl.fromTo("#{s} {sel_in}",{{opacity:1,scaleX:0,transformOrigin:"50% 50%"}},{{scaleX:1,duration:0.32,ease:"power2.out",immediateRender:false}},{c.t(at + 0.32):.3f});')

    for k, key in enumerate(("left", "right")):
        sd = d.get(key) or {}
        kind = sd.get("kind", "plain" if k == 0 else "twill")
        for fld in ("title", "front", "back"):
            _chk("kw_flip", fld, sd.get(fld, ""), f"{key}.{fld}", out)
        _chk("kw_flip", "back", sd.get("verdict", ""), f"{key}.verdict", out)
        parts.append(f'<div class="kw-ptitle ft{k}" style="left:{xs[k]}px;width:{sw_w}px;top:{zt + 60}px">{_e(sd.get("title", ""))}</div>'
                     f'<div class="kw-swbox fa{k}" style="left:{xs[k]}px;top:{top}px">{swatch_svg(f"{s}f{k}", kind, sw_w, sw_h, 16, fuzz=bool(sd.get("fuzz")))}</div>'
                     f'<div class="kw-swbox fb{k}" style="left:{xs[k]}px;top:{top}px;opacity:0">{swatch_svg(f"{s}b{k}", kind, sw_w, sw_h, 16, mirror=True, fuzz=bool(sd.get("fuzz")))}</div>'
                     f'<div class="kw-side kw-chalk fl{k}" style="left:{xs[k]}px;width:{sw_w}px;top:{top + sw_h + 30}px;text-align:center">{_e(sd.get("front", ""))}</div>'
                     f'<div class="kw-side kw-chalk fk{k}" style="left:{xs[k]}px;width:{sw_w}px;top:{top + sw_h + 30}px;text-align:center;opacity:0">{_e(sd.get("back", ""))}</div>'
                     f'<div class="kw-chalk kw-verdict fv{k}" style="left:{xs[k] - 20}px;width:{sw_w + 40}px;top:{top + sw_h + 96}px">{_e(sd.get("verdict", ""))}</div>')
        out.tl.append(f'tl.fromTo("#{s} .fa{k}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{c.t(0.1 + 0.2 * k):.3f});')
        out.tl.append(_in(c, f".ft{k}", 0.2 + 0.2 * k, dy=10))
        out.tl.append(_in(c, f".fl{k}", min(0.4 + 0.2 * k, max(flip_at, 1.2) - 0.6), dy=8))
        fk = max(flip_at, 1.2) + 0.3 * k
        if d.get("flip", True):
            turn(f".fa{k}", f".fb{k}", fk)
            out.tl.append(f'tl.to("#{s} .fl{k}",{{opacity:0,duration:0.2}},{c.t(fk):.3f});')
            out.tl.append(f'tl.to("#{s} .fk{k}",{{opacity:1,duration:0.25}},{c.t(fk + 0.5):.3f});')
            events.append(c.t(fk))
        if sd.get("return_at") is not None:          # back to the face (to show what only the face has)
            ra = _rel(c, sd.get("return_at"), fk + 2.0, out)
            out.tl.append(f'tl.set("#{s} .fa{k}",{{opacity:1}},{c.t(ra + 0.32):.3f});')
            turn(f".fb{k}", f".fa{k}", ra)
            out.tl.append(f'tl.to("#{s} .fk{k}",{{opacity:0,duration:0.2}},{c.t(ra):.3f});')
            out.tl.append(f'tl.to("#{s} .fl{k}",{{opacity:1,duration:0.25}},{c.t(ra + 0.5):.3f});')
            events.append(c.t(ra))
        va = _rel(c, sd.get("at"), flip_at + 1.2 + 2.0 * k, out)
        out.tl.append(_in(c, f".fv{k}", va, dy=10))
        out.tl.append(_draw(c, f".fu{k}", va + 0.35, 0.5))
        events.append(c.t(va))
    # the twill line on the front of the right swatch: chalk arrow from top right to bottom left
    ax, ay = xs[1], top
    out.html = f"""<div class="kw-in">
  {"".join(parts)}
  <svg class="kw-over" viewBox="0 0 1080 1920">{''.join(f'<path class="kw-st kw-arw fu{k}" pathLength="1" d="M{xs[k] + 40},{top + sw_h + 152} C{xs[k] + 140},{top + sw_h + 146} {xs[k] + 220},{top + sw_h + 158} {xs[k] + sw_w - 40},{top + sw_h + 150}"/>' for k in range(2))}<path class="kw-st kw-arw kw-dg" pathLength="1" d="M{ax + 310},{ay + 80} L{ax + 60},{ay + 330} M{ax + 62},{ay + 296} L{ax + 60},{ay + 330} L{ax + 94},{ay + 328}"/></svg>
</div>"""
    if d.get("arrow_at") is not None:
        aa = _rel(c, d.get("arrow_at"), 0.0, out)
        out.tl.append(_draw(c, ".kw-dg", aa, 0.8))
        events.append(c.t(aa))
    out.html += _source(c, d, out, "kw_flip")
    out.events = sorted(set(events))
    return out


# --- kw_close: verdict, the tilt test, sign-off ------------------------------------------------------------------

def kw_close(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    lines = d.get("lines", [])[:2]
    for k, ln in enumerate(lines):
        _chk("kw_close", "line", ln.get("text", ""), f"lines{k}.text", out)
    ch = d.get("chip") or {}
    rule = d.get("rule") or {}
    _chk("kw_close", "chip", ch.get("text", ""), "chip.text", out)
    _chk("kw_close", "rule", rule.get("text", ""), "rule.text", out)
    _chk("kw_close", "claim", d.get("claim", ""), "claim", out)
    _chk("kw_close", "sign_note", d.get("sign_note", ""), "sign_note", out)
    sw_w, sw_h = (350, 370) if _deep(c) else (340, 340)
    top = zt + 120
    xs = (X0 + 40, X1 - 40 - sw_w)
    kinds = d.get("kinds", ["plain", "twill"])
    sw = "".join(f'<div class="kw-swbox cs{k}" style="left:{xs[k]}px;top:{top}px">{swatch_svg(f"{s}c{k}", kinds[k], sw_w, sw_h, 14, fuzz=k in d.get("fuzz", []))}'
                 f'<div class="kw-sheen sh{k}"></div></div>' for k in range(2))
    lns = "".join(f'<div class="kw-chalk kw-verdict cl{k}" style="left:{xs[k] - 30}px;width:{sw_w + 60}px;top:{top + sw_h + 26}px">{_e(ln.get("text", ""))}</div>'
                  for k, ln in enumerate(lines))
    mark = LOGO.read_text(encoding="utf-8") if LOGO.exists() else ""
    mark = re.sub(r"<\?xml.*?\?>", "", mark)
    out.html = f"""<div class="kw-in">
  <div class="kw-cchip" style="top:{zt + 6}px"><span>{_e(ch.get("text", ""))}</span></div>
  <div class="kw-tilt">{sw}</div>
  {lns}
  <div class="kw-rule" style="top:{top + sw_h + 150}px">{_e(rule.get("text", ""))}</div>
  <svg class="kw-over" viewBox="0 0 1080 1920">{''.join(f'<path class="kw-st kw-arw cu{k}" pathLength="1" d="M{xs[k] + 50},{top + sw_h + 86} C{xs[k] + 140},{top + sw_h + 80} {xs[k] + 220},{top + sw_h + 92} {xs[k] + sw_w - 50},{top + sw_h + 84}"/>' for k in range(len(lines)))}<path class="kw-st kw-ul" pathLength="1" d="M{X0 + 120},{top + sw_h + 244} C{X0 + 300},{top + sw_h + 234} {X1 - 300},{top + sw_h + 254} {X1 - 120},{top + sw_h + 240}"/></svg>
  <div class="kw-sign" style="top:{zt + 150}px"><div class="kw-sign-mark">{mark}</div><div class="kw-sign-word">SUITWERK</div>
    <div class="kw-claim">{_e(d.get("claim", ""))}</div><div class="kw-chalk kw-signnote">{_e(d.get("sign_note", ""))}</div></div>
  <svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-sgl" pathLength="1" d="M{X0 + 230},{zt + 382} C{X0 + 360},{zt + 372} {X1 - 360},{zt + 390} {X1 - 230},{zt + 378}"/></svg>
</div>"""
    out.tl += _frame(c)
    events = [c.start]
    for k in range(2):
        out.tl.append(f'tl.fromTo("#{s} .cs{k}",{{opacity:0,y:-24}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{c.t(0.1 + 0.2 * k):.3f});')
    for k, ln in enumerate(lines):
        la = _rel(c, ln.get("at"), 0.6 + 1.2 * k, out)
        out.tl.append(_in(c, f".cl{k}", la, dy=10))
        out.tl.append(_draw(c, f".cu{k}", la + 0.3, 0.5))
        events.append(c.t(la))
    if ch.get("text"):
        ca = _rel(c, ch.get("at"), 0.3, out)
        out.tl.append(_in(c, ".kw-cchip", ca, dy=8))
        events.append(c.t(ca))
    if d.get("tilt_at") is not None:
        ta = _rel(c, d.get("tilt_at"), 0.0, out)
        # the light runs over both swatches: on the twill the diagonal catches it, the plain weave stays even
        for k in range(2):
            out.tl.append(f'tl.fromTo("#{s} .sh{k}",{{opacity:0,x:-260}},{{opacity:1,x:260,duration:1.6,ease:"sine.inOut"}},{c.t(ta + 0.1 * k):.3f});')
            out.tl.append(f'tl.to("#{s} .sh{k}",{{opacity:0,duration:0.3}},{c.t(ta + 1.6):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .cs1",{{rotation:0}},{{rotation:-6,duration:0.8,ease:"power2.inOut"}},{c.t(ta):.3f});')
        events.append(c.t(ta))
    if rule.get("text"):
        ra = _rel(c, rule.get("at"), 3.0, out)
        out.tl.append(_in(c, ".kw-rule", ra, dy=14, dur=0.5))
        out.tl.append(_draw(c, ".kw-ul", ra + 0.4, 0.7))
        events.append(c.t(ra))
    sign = _rel(c, d.get("sign_at"), c.duration - 3.0, out)
    out.tl.append(f'tl.to("#{s} .kw-tilt,#{s} .kw-verdict,#{s} .kw-cchip,#{s} .kw-rule,#{s} .kw-ul,#{s} .cu0,#{s} .cu1",{{opacity:0,y:-16,duration:0.35,ease:"power2.in"}},{c.t(sign - 0.35):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .kw-sign",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{c.t(sign):.3f});')
    out.tl.append(_draw(c, ".kw-sgl", sign + 0.5, 0.8))
    if d.get("sign_note"):
        out.tl.append(_in(c, ".kw-signnote", sign + 1.4, dy=8))
        events.append(c.t(sign + 1.4))
    events.append(c.t(sign))
    out.html += _source(c, d, out, "kw_close")
    out.tl.append(f'tl.to("#{s} .kw-src",{{opacity:0,duration:0.3}},{c.t(sign - 0.35):.3f});')
    out.events = sorted(set(events))
    return out


TEMPLATES = {"kw_hook": kw_hook, "kw_weave": kw_weave, "kw_draft": kw_draft, "kw_flip": kw_flip, "kw_close": kw_close}


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: N802 (contract name)
    txt, mut = pal.get("text", "#F2EEE6"), pal.get("muted", "#9AA0A8")
    D, B = f"'FN {display}'", f"'FN {body}'"
    return f"""
.kw-in{{position:absolute;inset:0;}}
.kw-over{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;pointer-events:none;}}
.kw-st{{fill:none;stroke:{CHALK};stroke-width:8;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 1;stroke-dashoffset:1;filter:url(#kw-chalk);}}
.kw-arw{{stroke-width:5;}}
.kw-diag{{stroke-width:9;}}
.kw-redst .kw-st{{stroke:#B2584A;filter:none;stroke-width:5;}}
.kw-chalk{{position:absolute;font-family:{B};font-weight:600;color:{CHALK};filter:url(#kw-chalk);}}
.kw-q{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{D};font-weight:600;font-size:70px;line-height:1.08;color:{txt};}}
.kw-lab{{text-align:center;font-size:40px;}}
.kw-swbox{{position:absolute;filter:drop-shadow(0 22px 26px rgba(2,6,14,0.6));}}
.kw-sw{{display:block;}}
.kw-ltbox{{position:absolute;filter:drop-shadow(0 26px 34px rgba(2,6,14,0.65));}}
.kw-lt{{position:relative;}}
.kw-lt-win{{position:absolute;overflow:hidden;background:#0E1626;}}
.kw-lt-glass{{position:absolute;inset:0;background:radial-gradient(circle at 30% 24%,rgba(255,255,255,0.18) 0%,transparent 40%),radial-gradient(circle at 50% 50%,transparent 64%,rgba(0,0,0,0.42) 100%);}}
.kw-lt-fr{{position:absolute;left:0;top:0;}}
.kw-title{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;}}
.kw-ttl{{font-family:{D};font-weight:600;font-size:72px;color:{txt};}}
.kw-formula{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{B};font-weight:600;font-size:40px;letter-spacing:0.02em;color:{CHALK};filter:url(#kw-chalk);}}
.kw-side{{font-size:40px;}}
.kw-note{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{D};font-weight:600;font-size:46px;color:{txt};}}
.kw-cnote{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{B};font-size:30px;letter-spacing:0.03em;color:{mut};}}
.kw-paper{{position:absolute;background:#EFE8D6;border-radius:4px;box-shadow:0 18px 30px rgba(2,6,14,0.55);}}
.kw-grid{{position:absolute;overflow:visible;}}
.kw-ptitle{{position:absolute;text-align:center;font-family:{D};font-weight:600;font-size:52px;color:{txt};}}
.kw-word{{text-align:center;font-size:50px;}}
.kw-legend{{position:absolute;left:{X0}px;width:{X1 - X0}px;display:flex;justify-content:center;align-items:center;gap:16px;font-family:{B};font-weight:500;font-size:34px;color:{txt};}}
.kw-legend i{{display:inline-block;width:26px;height:26px;background:#1E2A44;border:7px solid #EFE8D6;border-radius:3px;}}
.kw-verdict{{text-align:center;font-size:42px;line-height:1.2;}}
.kw-cchip{{position:absolute;left:{X0}px;width:{X1 - X0}px;display:flex;justify-content:center;}}
.kw-cchip span{{font-family:{B};font-weight:500;font-size:32px;color:{txt};border:2px solid rgba(238,231,215,0.5);border-radius:999px;padding:10px 28px;background:rgba(10,16,28,0.55);}}
.kw-sheen{{position:absolute;left:0;top:0;width:340px;height:340px;background:linear-gradient(115deg,transparent 30%,rgba(255,244,214,0.30) 48%,transparent 66%);mix-blend-mode:screen;opacity:0;}}
.kw-rule{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{D};font-weight:600;font-size:62px;line-height:1.1;color:{txt};}}
.kw-sign{{position:absolute;left:{X0}px;width:{X1 - X0}px;display:flex;flex-direction:column;align-items:center;opacity:0;}}
.kw-sign-mark svg{{width:120px;height:120px;display:block;}}
.kw-sign-word{{margin-top:20px;font-family:{D};font-weight:600;font-size:62px;letter-spacing:0.16em;color:{txt};}}
.kw-claim{{margin-top:40px;font-family:{B};font-size:36px;color:{CHALK_DIM};}}
.kw-signnote{{position:relative;margin-top:60px;font-size:42px;opacity:0;}}
.kw-src{{position:absolute;left:{X0}px;width:{X1 - X0}px;font-family:{B};font-size:24px;line-height:1.2;letter-spacing:0;color:{mut};}}
.kw-src b{{font-weight:600;color:{CHALK_DIM};margin-right:6px;}}
"""


# --- the layer: dark worsted cloth on the cutting table, tape measure band, chalk filter ----------------------------

def _tape(x: int, y: int, w: int) -> str:
    cm = 12                                   # px per drawn centimetre (scale of the band, not a measurement)
    ticks, nums = [], []
    for k in range(0, w // cm + 1):
        xx = x + k * cm
        h = 16 if k % 5 == 0 else 9
        ticks.append(f'<line x1="{xx}" y1="{y}" x2="{xx}" y2="{y + h}"/>')
        if k % 10 == 0 and k:
            nums.append(f'<text x="{xx}" y="{y + 40}" text-anchor="middle">{k}</text>')
    return (f'<rect x="{x - 8}" y="{y - 2}" width="{w + 16}" height="48" rx="3" fill="#E8DCBC"/>'
            f'<g stroke="#2B2B2B" stroke-width="1.6">{"".join(ticks)}</g>'
            f'<g font-family="\'FN Inter\'" font-weight="600" font-size="24" fill="#2B2B2B">{"".join(nums)}</g>')


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: N802 (contract name)
    lay = getattr(plan, "layout", None) or {}
    lang = getattr(plan, "language", "de")
    series = SERIES.get(lay.get("series", "stoff"), SERIES["stoff"]).get(lang, "")
    topic = lay.get("series_topic", "")
    label = series + (f" · {topic}" if topic else "")
    noise = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>"
             "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>"
             "<feColorMatrix values='0 0 0 0 0.8 0 0 0 0 0.82 0 0 0 0 0.9 0 0 0 0.06 0'/></filter>"
             "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")
    # the ground is a worsted twill itself: fine diagonal ribs (top right to bottom left), seen from above
    html_ = f"""<div id="kwx" style="position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:#141E33">
<div class="kwx-twill"></div><div class="kwx-noise"></div><div id="kwx-lamp"></div><div class="kwx-vig"></div>
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="kw-chalk" x="-8%" y="-30%" width="116%" height="160%">
 <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="7" result="n"/>
 <feDisplacementMap in="SourceGraphic" in2="n" scale="4.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
 <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="2" result="g"/>
 <feColorMatrix in="g" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  -2.4 0 0 0 1.85" result="m"/>
 <feComposite in="d" in2="m" operator="in"/>
</filter></defs></svg>
<style>
.kwx-twill{{position:absolute;inset:-40px;background:repeating-linear-gradient(135deg,rgba(150,170,210,0.12) 0 2px,transparent 2px 7px),
 repeating-linear-gradient(135deg,rgba(0,0,0,0.26) 0 1px,transparent 1px 7px),radial-gradient(ellipse 95% 70% at 50% 40%,#22314F 0%,#18243C 52%,#0D1424 100%);}}
.kwx-noise{{position:absolute;inset:0;background-image:{noise};}}
#kwx-lamp{{position:absolute;left:-260px;top:-160px;width:1500px;height:1500px;background:radial-gradient(circle,rgba(246,226,186,0.16) 0%,rgba(246,226,186,0.05) 40%,transparent 66%);}}
.kwx-vig{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 64% at 50% 42%,transparent 55%,rgba(3,6,12,0.66) 100%);}}
</style></div>
<div id="kwx-band" style="position:absolute;left:0;top:0;width:1080px;height:300px;z-index:21;pointer-events:none">
<div style="position:absolute;left:{X0}px;top:190px;width:{X1 - X0}px;font-family:'FN Inter';font-weight:600;font-size:24px;letter-spacing:0.12em;text-transform:uppercase;color:{CHALK};filter:url(#kw-chalk)">{html.escape(label)}</div>
<svg viewBox="0 0 1080 300" width="1080" height="300" style="position:absolute;inset:0">{_tape(X0, 232, X1 - X0)}</svg></div>"""
    script = """<script>
(function(){var t=window.__timelines&&window.__timelines.main;if(!t)return;var T=Number(document.getElementById("root").dataset.duration)||60;
t.fromTo("#kwx-lamp",{x:-40,y:-20},{x:80,y:40,duration:T,ease:"sine.inOut"},0);
t.fromTo(".kwx-twill",{x:0,y:0},{x:18,y:-18,duration:T,ease:"none"},0);
t.seek(0);})();
</script>"""
    return {"under_scenes_html": html_, "body_end_html": script, "events": []}


def MANIFEST_EXTRA(plan) -> dict:  # noqa: N802 (contract name)
    used = sorted({b.scene_type for b in plan.beats if b.scene_type.startswith("kw_")})
    if not used:
        return {}
    return {"format": {"name": "Suitwerk Format \"Kreidestrich\"", "version": "0.1 (Pilot)",
                       "bible": "OneDrive\\Business\\02 Marke\\Suitwerk\\Format-Bibel.md", "scene_types": used,
                       "visuals": "Illustration aus HTML/SVG/CSS: Gewebe Faden fuer Faden aus der Bindung gerechnet, "
                                  "Bindungspatrone aus derselben Funktion; Farben im vergroesserten Gewebe nur zur Unterscheidung",
                       "ai_images": "keine (nur Code-Grafik)"}}


# =========================================================================================================
# Week 1 building blocks (02.11.2026): weight on the scale, a ruler with marks, fibre cross-sections, the way to the
# yarn, and the finishing of a woollen cloth. Same rules as above: everything drawn and computed, chalk for marks.
#
# | scene type | role                                | data |
# |------------|-------------------------------------|------|
# | kw_weigh   | a strip of cloth on a scale,         | question{text, at}, title{text, at}, kind, fuzz, value, unit, weigh_at, readout_label, |
# |            | length and width chalked             | len_at, len_label, width_at, width_label, source |
# | kw_range   | ruler with marks (weights, microns)  | title{text, at}, unit, min, max, step, label_every, decimals, marks[{value, label, sub, at, up}], |
# |            |                                      | band{from, to, label, at}, drift{from, to, label, at}, note{text, at}, source |
# | kw_fibre   | fibre cross-sections to scale        | title{text, at}, px_per_um, items[{label, um, sub, at}], bar_um, stack_at, note{text, at}, source |
# | kw_yarn    | fibres on the way to the yarn        | title{text, at}, mode (woollen|worsted), steps[{key, label, at}], noil_label, source |
# | kw_finish  | a woollen cloth after the loom       | title{text, at}, stages[{kind, label, at}], colors_note, source |
# =========================================================================================================

LIMITS.update({
    "kw_weigh": {"question": 34, "title": 26, "readout_label": 30, "len_label": 18, "width_label": 22, "source": 70},
    "kw_range": {"title": 30, "label": 22, "sub": 22, "band": 30, "drift": 30, "note": 40, "source": 70},
    "kw_fibre": {"title": 30, "label": 16, "sub": 18, "note": 40, "source": 70},
    "kw_yarn": {"title": 26, "label": 30, "noil_label": 16, "source": 70},
    "kw_finish": {"title": 26, "label": 30, "source": 70},
})
HOOK_SCENE_TYPES.append("kw_weigh")


def _num(v: float, lang: str, dec: int = 0) -> str:
    s = f"{v:.{dec}f}"
    return s.replace(".", ",") if lang == "de" else s


def _txt(c: SceneCtx, d: dict, key: str, scene: str, out: SceneOut, default_at: float) -> tuple[str, float]:
    t = d.get(key) or {}
    _chk(scene, key, t.get("text", ""), f"{key}.text", out)
    return t.get("text", ""), _rel(c, t.get("at"), default_at, out)


# --- kw_weigh -----------------------------------------------------------------------------------------------------

def kw_weigh(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    q, q_at = _txt(c, d, "question", "kw_weigh", out, 0.2)
    ti, ti_at = _txt(c, d, "title", "kw_weigh", out, 0.1)
    head = q or ti
    sx0, sx1, sy0, sy1 = 330, 650, zt + 170, zt + 560          # the strip: width across, one metre down
    value, unit = float(d.get("value", 350)), d.get("unit", "g")
    _chk("kw_weigh", "readout_label", d.get("readout_label", ""), "readout_label", out)
    _chk("kw_weigh", "len_label", d.get("len_label", ""), "len_label", out)
    _chk("kw_weigh", "width_label", d.get("width_label", ""), "width_label", out)
    steps = [round(value * f / 10) * 10 for f in (0, 0.25, 0.5, 0.72, 0.88, 0.96)] + [value]
    digits = "".join(f'<span class="kw-dg{i}">{_num(v, c.lang)}</span>' for i, v in enumerate(steps))
    strip = swatch_svg(f"{s}st", d.get("kind", "twill"), sx1 - sx0, sy1 - sy0, 9, fuzz=bool(d.get("fuzz")))
    out.html = f"""<div class="kw-in">
  <div class="{'kw-q' if q else 'kw-title'} kw-head" style="top:{zt + (4 if q else 44)}px">{('<span class="kw-ttl kw-ttl-s">' + _e(head) + '</span>') if not q else _e(head)}</div>
  <div class="kw-scale" style="left:{sx0 - 50}px;top:{sy0 - 30}px;width:{sx1 - sx0 + 100}px;height:{sy1 - sy0 + 60}px"></div>
  <div class="kw-swbox kw-strip" style="left:{sx0}px;top:{sy0}px">{strip}</div>
  <div class="kw-display" style="left:{(sx0 + sx1) / 2 - 150:.0f}px;top:{sy1 + 50}px"><b>{digits}</b><i>{_e(unit)}</i></div>
  <div class="kw-readlab" style="top:{sy1 + 160}px">{_e(d.get("readout_label", ""))}</div>
  <svg class="kw-over" viewBox="0 0 1080 1920">
   <path class="kw-st kw-arw kw-len" pathLength="1" d="M{sx1 + 80},{sy0} L{sx1 + 80},{sy1} M{sx1 + 64},{sy0} L{sx1 + 96},{sy0} M{sx1 + 64},{sy1} L{sx1 + 96},{sy1}"/>
   <path class="kw-st kw-arw kw-wid" pathLength="1" d="M{sx0},{sy0 - 60} L{sx1},{sy0 - 60} M{sx0},{sy0 - 76} L{sx0},{sy0 - 44} M{sx1},{sy0 - 76} L{sx1},{sy0 - 44}"/>
  </svg>
  <div class="kw-chalk kw-side kw-lenl" style="left:{sx1 + 104}px;top:{(sy0 + sy1) / 2 - 50:.0f}px;width:{X1 - sx1 - 104}px">{_e(d.get("len_label", ""))}</div>
  <div class="kw-chalk kw-side kw-widl" style="left:{sx0 - 40}px;width:{sx1 - sx0 + 80}px;top:{sy0 - 120}px;text-align:center">{_e(d.get("width_label", ""))}</div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".kw-head", q_at if q else ti_at, dy=18, dur=0.5))
    out.tl.append(f'tl.fromTo("#{s} .kw-scale",{{opacity:0}},{{opacity:1,duration:0.4}},{c.t(0.1):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .kw-strip",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.6,ease:"power2.out"}},{c.t(0.25):.3f});')
    events = [c.start, c.t(q_at if q else ti_at)]
    w_at = _rel(c, d.get("weigh_at"), 1.2, out)
    out.tl.append(f'tl.set("#{s} .kw-display b span",{{opacity:0}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .kw-display",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.3}},{c.t(max(0.3, w_at - 0.3)):.3f});')
    for i in range(len(steps)):
        out.tl.append(f'tl.set("#{s} .kw-dg{i}",{{opacity:1}},{c.t(w_at + 0.14 * i):.3f});')
        if i + 1 < len(steps):
            out.tl.append(f'tl.set("#{s} .kw-dg{i}",{{opacity:0}},{c.t(w_at + 0.14 * (i + 1)):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .kw-strip",{{y:-6}},{{y:0,duration:0.5,ease:"bounce.out"}},{c.t(w_at):.3f});')
    events.append(c.t(w_at))
    if d.get("readout_label"):
        ra = _rel(c, d.get("readout_at"), w_at + 1.2, out)
        out.tl.append(_in(c, ".kw-readlab", ra, dy=8))
        events.append(c.t(ra))
    if d.get("len_at") is not None:
        la = _rel(c, d.get("len_at"), 0.0, out)
        out.tl.append(_draw(c, ".kw-len", la, 0.6))
        out.tl.append(_in(c, ".kw-lenl", la + 0.3, dy=8))
        events.append(c.t(la))
    if d.get("width_at") is not None:
        wa = _rel(c, d.get("width_at"), 0.0, out)
        out.tl.append(f'tl.to("#{s} .kw-head",{{opacity:0,duration:0.25}},{c.t(max(0.2, wa - 0.3)):.3f});')
        out.tl.append(_draw(c, ".kw-wid", wa, 0.6))
        out.tl.append(_in(c, ".kw-widl", wa + 0.3, dy=8))
        events.append(c.t(wa))
    out.html += _source(c, d, out, "kw_weigh")
    out.events = sorted(set(events))
    return out


# --- kw_range -----------------------------------------------------------------------------------------------------

def kw_range(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    ti, ti_at = _txt(c, d, "title", "kw_range", out, 0.1)
    lo, hi = float(d.get("min", 0)), float(d.get("max", 100))
    step, every = float(d.get("step", 10)), int(d.get("label_every", 5))
    dec = int(d.get("decimals", 0))
    rx0, rx1, ry = 150, 890, zt + 330

    def X(v: float) -> float:
        return rx0 + (v - lo) / (hi - lo) * (rx1 - rx0)
    ticks, nums = [], []
    k, v = 0, lo
    while v <= hi + 1e-9:
        x = X(v)
        big = k % every == 0
        ticks.append(f'<line x1="{x:.1f}" y1="{ry}" x2="{x:.1f}" y2="{ry + (26 if big else 13)}"/>')
        if big:
            nums.append(f'<text x="{x:.1f}" y="{ry + 52}" text-anchor="middle">{_num(v, c.lang, dec)}</text>')
        k += 1
        v = lo + k * step
    marks, tl, events = [], [], [c.start, c.t(ti_at)]
    for i, m in enumerate(d.get("marks", [])):
        _chk("kw_range", "label", m.get("label", ""), f"marks{i}.label", out)
        _chk("kw_range", "sub", m.get("sub", ""), f"marks{i}.sub", out)
        x = X(float(m["value"]))
        up = m.get("up", i % 2 == 0)
        y_line = (ry - 96, ry - 8) if up else (ry + 70, ry + 160)
        ly = ry - 196 if up else ry + 170
        tone = {"green": GREEN_CHALK, "red": RED_CHALK}.get(m.get("tone", ""), CHALK)
        lx = min(max(x - 150, X0), X1 - 300)
        marks.append(f'<path class="kw-st kw-arw mk{i}" pathLength="1" style="stroke:{tone}" d="M{x:.1f},{y_line[0]} L{x:.1f},{y_line[1]}"/>')
        out.html += (f'<div class="kw-chalk kw-mark ml{i}" style="left:{lx:.0f}px;width:300px;top:{ly}px;color:{tone}">'
                     f'{_e(m.get("label", ""))}<small>{_e(m.get("sub", ""))}</small></div>')
        at = _rel(c, m.get("at"), 0.8 + 1.2 * i, out)
        tl.append(_draw(c, f".mk{i}", at, 0.4))
        tl.append(_in(c, f".ml{i}", at + 0.15, dy=8))
        events.append(c.t(at))
    band = d.get("band") or {}
    bhtml = ""
    if band:
        _chk("kw_range", "band", band.get("label", ""), "band.label", out)
        bx0, bx1 = X(float(band["from"])), X(float(band["to"]))
        bhtml = (f'<div class="kw-band" style="left:{min(bx0, bx1):.0f}px;width:{abs(bx1 - bx0):.0f}px;top:{ry - 6}px"></div>'
                 f'<div class="kw-chalk kw-bandl" style="left:{X0}px;width:{X1 - X0}px;top:{ry + 270}px">{_e(band.get("label", ""))}</div>')
        ba = _rel(c, band.get("at"), 2.0, out)
        tl.append(f'tl.fromTo("#{s} .kw-band",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},{{opacity:1,scaleX:1,duration:0.6,ease:"power2.out"}},{c.t(ba):.3f});')
        tl.append(_in(c, ".kw-bandl", ba + 0.3, dy=8))
        events.append(c.t(ba))
    drift = d.get("drift") or {}
    dhtml = ""
    if drift:
        _chk("kw_range", "drift", drift.get("label", ""), "drift.label", out)
        dx0, dx1 = X(float(drift["from"])), X(float(drift["to"]))
        hd = 22 if dx1 < dx0 else -22
        dhtml = (f'<path class="kw-st kw-arw kw-drift" pathLength="1" d="M{dx0:.0f},{ry + 110} C{(dx0 + dx1) / 2:.0f},{ry + 150} {(dx0 + dx1) / 2:.0f},{ry + 150} {dx1:.0f},{ry + 110} '
                 f'M{dx1 + hd:.0f},{ry + 100} L{dx1:.0f},{ry + 110} L{dx1 + hd * 0.4:.0f},{ry + 130}"/>')
        out.html += f'<div class="kw-chalk kw-driftl" style="left:{X0}px;width:{X1 - X0}px;top:{ry + 330}px">{_e(drift.get("label", ""))}</div>'
        da = _rel(c, drift.get("at"), 2.0, out)
        tl.append(_draw(c, ".kw-drift", da, 0.9))
        tl.append(_in(c, ".kw-driftl", da + 0.4, dy=8))
        events.append(c.t(da))
    note, na = _txt(c, d, "note", "kw_range", out, c.duration - 2.0)
    unit = d.get("unit", "")
    out.html = f"""<div class="kw-in">
  <div class="kw-title" style="top:{zt + 4}px"><span class="kw-ttl kw-ttl-s">{_e(ti)}</span></div>
  <svg class="kw-over kw-ruler" viewBox="0 0 1080 1920"><rect x="{rx0 - 30}" y="{ry - 6}" width="{rx1 - rx0 + 60}" height="70" rx="4" fill="#E8DCBC"/>
   <g stroke="#2B2B2B" stroke-width="2">{"".join(ticks)}</g><g font-family="'FN Inter'" font-weight="600" font-size="24" fill="#2B2B2B">{"".join(nums)}</g>
   <text x="{rx1 + 30}" y="{ry - 16}" font-family="'FN Inter'" font-weight="600" font-size="24" fill="#EEE7D7" text-anchor="end">{_e(unit)}</text></svg>
  {bhtml}
  <svg class="kw-over" viewBox="0 0 1080 1920">{"".join(marks)}{dhtml}</svg>
  {out.html}
  <div class="kw-note" style="top:{ry + 390}px">{_e(note)}</div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".kw-title", ti_at, dy=14))
    out.tl.append(f'tl.fromTo("#{s} .kw-ruler",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.6,ease:"power2.out"}},{c.t(0.2):.3f});')
    out.tl += tl
    if note:
        out.tl.append(_in(c, ".kw-note", na, dy=10))
        events.append(c.t(na))
    out.html += _source(c, d, out, "kw_range")
    out.events = sorted(set(events))
    return out


# --- kw_fibre -----------------------------------------------------------------------------------------------------

def kw_fibre(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    ti, ti_at = _txt(c, d, "title", "kw_fibre", out, 0.1)
    items = d.get("items", [])[:3]
    ppu = float(d.get("px_per_um", 13))
    cy = zt + 380
    widths = [float(it["um"]) * ppu for it in items]
    gap = (X1 - X0 - sum(widths)) / (len(items) + 1)
    x = X0 + gap
    centers = []
    for w_ in widths:
        centers.append(x + w_ / 2)
        x += w_ + gap
    parts, tl, events = [], [], [c.start, c.t(ti_at)]
    for i, it in enumerate(items):
        _chk("kw_fibre", "label", it.get("label", ""), f"items{i}.label", out)
        _chk("kw_fibre", "sub", it.get("sub", ""), f"items{i}.sub", out)
        r = widths[i] / 2
        cx = centers[i]
        parts.append(f'<div class="kw-fib fb{i}" style="left:{cx - r:.1f}px;top:{cy - r:.1f}px;width:{2 * r:.1f}px;height:{2 * r:.1f}px"></div>'
                     f'<div class="kw-chalk kw-fibl fl{i}" style="left:{cx - 150:.0f}px;top:{cy + 175}px">{_e(it.get("label", ""))}'
                     f'<small>{_e(it.get("sub", ""))}</small></div>')
        at = _rel(c, it.get("at"), 0.8 + 1.4 * i, out)
        tl.append(f'tl.fromTo("#{s} .fb{i}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.5)"}},{c.t(at):.3f});')
        tl.append(_in(c, f".fl{i}", at + 0.2, dy=8))
        events.append(c.t(at))
    bar = float(d.get("bar_um", 10))
    bw = bar * ppu
    parts.append(f'<svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-arw kw-bar" pathLength="1" '
                 f'd="M{X0 + 20},{zt + 150} L{X0 + 20 + bw:.0f},{zt + 150} M{X0 + 20},{zt + 136} L{X0 + 20},{zt + 164} M{X0 + 20 + bw:.0f},{zt + 136} L{X0 + 20 + bw:.0f},{zt + 164}"/></svg>'
                 f'<div class="kw-chalk kw-side kw-barl" style="left:{X0 + 40 + bw:.0f}px;top:{zt + 124}px">{_num(bar, c.lang)} µm</div>')
    tl.append(_draw(c, ".kw-bar", 0.4, 0.5))
    tl.append(_in(c, ".kw-barl", 0.6, dy=6))
    if d.get("stack_at") is not None and items:
        sa = _rel(c, d.get("stack_at"), c.duration - 3.0, out)
        mid = 540
        for i in range(len(items)):
            tl.append(f'tl.to("#{s} .fb{i}",{{x:{mid - centers[i]:.1f},duration:0.8,ease:"power2.inOut"}},{c.t(sa):.3f});')
            tl.append(f'tl.to("#{s} .fl{i}",{{opacity:0,duration:0.3}},{c.t(sa):.3f});')
        events.append(c.t(sa))
    note, na = _txt(c, d, "note", "kw_fibre", out, c.duration - 2.0)
    out.html = f"""<div class="kw-in">
  <div class="kw-title" style="top:{zt + 4}px"><span class="kw-ttl kw-ttl-s">{_e(ti)}</span></div>
  {"".join(parts)}
  <div class="kw-note" style="top:{zt + 690}px">{_e(note)}</div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".kw-title", ti_at, dy=14))
    out.tl += tl
    if note:
        out.tl.append(_in(c, ".kw-note", na, dy=10))
        events.append(c.t(na))
    out.html += _source(c, d, out, "kw_fibre")
    out.events = sorted(set(events))
    return out


# --- kw_yarn ------------------------------------------------------------------------------------------------------

def _fibre_states(mode: str, zt: int, n: int = 34) -> tuple[list[float], dict[str, list[str]]]:
    """Fibre paths (M x0,y0 Q cx,cy x1,y1) for every step; the same structure in every state so GSAP can tween them."""
    import math as _m
    import random
    rnd = random.Random(7 if mode == "worsted" else 3)
    lens = [rnd.uniform(70, 150) if (mode == "worsted" and i % 3 == 0) else rnd.uniform(150 if mode == "worsted" else 90, 240 if mode == "worsted" else 170)
            for i in range(n)]
    cy = zt + 400

    def p(x0, y0, ang, ln, bend):
        x1, y1 = x0 + _m.cos(ang) * ln, y0 + _m.sin(ang) * ln
        mx, my = (x0 + x1) / 2 - _m.sin(ang) * bend, (y0 + y1) / 2 + _m.cos(ang) * bend
        return f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}"
    st: dict[str, list[str]] = {k: [] for k in ("raw", "card", "slub", "comb", "top", "draw", "spin")}
    for i, ln in enumerate(lens):
        a = rnd.uniform(0, 6.283)
        st["raw"].append(p(540 + rnd.gauss(0, 70) - _m.cos(a) * ln / 2, cy + rnd.gauss(0, 70) - _m.sin(a) * ln / 2, a, ln, rnd.uniform(-30, 30)))
        a2 = rnd.uniform(-0.9, 0.9) + (0 if rnd.random() < 0.5 else 3.1416)
        st["card"].append(p(rnd.uniform(160, 900 - ln * 0.6), cy + rnd.uniform(-130, 110), a2, ln, rnd.uniform(-18, 18)))
        a3 = rnd.uniform(-0.6, 0.6)
        st["slub"].append(p(rnd.uniform(170, 900 - ln), cy + rnd.uniform(-30, 30), a3, ln * 0.9, rnd.uniform(-10, 10)))
        short = mode == "worsted" and i % 3 == 0
        if short:   # combing removes the short fibres: they drop below the band (noil)
            x0 = rnd.uniform(200, 760)
            st["comb"].append(p(x0, zt + 640 + rnd.uniform(-20, 20), rnd.uniform(-0.3, 0.3), ln, 4))
            for k in ("top", "draw", "spin"):
                st[k].append(st["comb"][-1])
        else:
            x0 = rnd.uniform(170, 900 - ln)
            y0 = cy + rnd.uniform(-40, 40)
            st["comb"].append(p(x0, y0, 0.0, ln, rnd.uniform(-3, 3)))
            st["top"].append(p(x0, cy + (y0 - cy) * 0.55, 0.0, ln, 0))
            st["draw"].append(p(170 + (x0 - 170) * 1.0, cy + (y0 - cy) * 0.2, 0.0, ln * 1.05, 0))
            st["spin"].append(st["draw"][-1])
    if mode == "woollen":
        st["spin"] = list(st["slub"])
    return lens, st


def kw_yarn(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    ti, ti_at = _txt(c, d, "title", "kw_yarn", out, 0.1)
    mode = d.get("mode", "worsted")
    lens, st = _fibre_states(mode, zt)
    paths = "".join(f'<path class="kw-fb f{i}" d="{st["raw"][i]}"/>' for i in range(len(lens)))
    cy = zt + 400
    twist_w = 10 if mode == "worsted" else 34
    twist = "".join(f'<path d="M{x},{cy - twist_w} L{x + 26},{cy + twist_w}"/>' for x in range(170, 900, 22))
    labels = []
    tl, events = [], [c.start, c.t(ti_at)]
    out.tl += _frame(c)
    out.tl.append(_in(c, ".kw-title", ti_at, dy=14))
    out.tl.append(f'tl.fromTo("#{s} .kw-fbs",{{opacity:0}},{{opacity:1,duration:0.5}},{c.t(0.2):.3f});')
    prev_at = None
    for j, stp in enumerate(d.get("steps", [])):
        key = stp.get("key", "card")
        _chk("kw_yarn", "label", stp.get("label", ""), f"steps{j}.label", out)
        at = _rel(c, stp.get("at"), 0.8 + 2.0 * j, out)
        labels.append(f'<div class="kw-formula kw-stl sl{j}" style="top:{zt + 86}px">{_e(stp.get("label", ""))}</div>')
        if prev_at is not None:
            tl.append(f'tl.to("#{s} .sl{j - 1}",{{opacity:0,duration:0.2}},{c.t(at - 0.2):.3f});')
        tl.append(_in(c, f".sl{j}", at, dy=10))
        prev_at = at
        if key in st and key != "raw":
            for i in range(len(lens)):
                tl.append(f'tl.to("#{s} .f{i}",{{attr:{{d:"{st[key][i]}"}},duration:1.1,ease:"power2.inOut"}},{c.t(at + 0.004 * i):.3f});')
        if key == "comb":
            tl.append(_in(c, ".kw-noil", at + 1.0, dy=8))
        if key == "spin":
            tl.append(f'tl.fromTo("#{s} .kw-twist",{{opacity:0}},{{opacity:1,duration:0.6}},{c.t(at + 0.4):.3f});')
        events.append(c.t(at))
    out.tl += tl
    _chk("kw_yarn", "noil_label", d.get("noil_label", ""), "noil_label", out)
    out.html = f"""<div class="kw-in">
  <div class="kw-title" style="top:{zt + 4}px"><span class="kw-ttl kw-ttl-s">{_e(ti)}</span></div>
  {"".join(labels)}
  <svg class="kw-over kw-fbs" viewBox="0 0 1080 1920">{paths}<g class="kw-twist">{twist}</g></svg>
  <div class="kw-chalk kw-side kw-noil" style="left:{X0}px;top:{zt + 690}px;width:{X1 - X0}px;text-align:center">{_e(d.get("noil_label", ""))}</div>
</div>"""
    out.html += _source(c, d, out, "kw_yarn")
    out.events = sorted(set(events))
    return out


# --- kw_finish ----------------------------------------------------------------------------------------------------

def kw_finish(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    ti, ti_at = _txt(c, d, "title", "kw_finish", out, 0.1)
    win = 540 if _deep(c) else 460
    inner, size = weave_svg(f"{s}w", d.get("kind", "twill"), 8, win / 8, warp=NAVY_WARP, weft=NAVY_WEFT, ratio=0.66, shuttle=False)
    long_ = fuzz_svg("kw-fzl", size, size, 220, 44, 5, "#A9BBDB", 0.75)
    short = fuzz_svg("kw-fzs", size, size, 260, 12, 9, "#A9BBDB", 0.6)
    view = (f'<svg class="kw-wv" viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" style="position:absolute;inset:0">{inner}</svg>'
            f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" style="position:absolute;inset:0">'
            f'<g class="kw-fzlg" opacity="0">{long_}</g><g class="kw-fzsg" opacity="0">{short}</g></svg>')
    lt_left, lt_top = 540 - (win + 44) / 2, zt + 170
    labels, tl, events = [], [], [c.start, c.t(ti_at)]
    prev = None
    for j, stg in enumerate(d.get("stages", [])):
        _chk("kw_finish", "label", stg.get("label", ""), f"stages{j}.label", out)
        at = _rel(c, stg.get("at"), 0.6 + 2.0 * j, out)
        labels.append(f'<div class="kw-formula sl{j}" style="top:{zt + 86}px">{_e(stg.get("label", ""))}</div>')
        if prev is not None:
            tl.append(f'tl.to("#{s} .sl{j - 1}",{{opacity:0,duration:0.2}},{c.t(at - 0.2):.3f});')
        tl.append(_in(c, f".sl{j}", at, dy=10))
        prev = at
        kind = stg.get("kind")
        if kind == "milled":     # washed and milled: the cloth closes up, fibres lock together, the weave blurs
            tl.append(f'tl.to("#{s} .kw-wv",{{scale:0.9,transformOrigin:"50% 50%",filter:"blur(2.2px)",duration:1.4,ease:"power2.inOut"}},{c.t(at + 0.2):.3f});')
            tl.append(f'tl.to("#{s} .kw-fzlg",{{opacity:1,duration:1.2}},{c.t(at + 0.4):.3f});')
        elif kind == "cropped":  # cropped: the long loose hairs are cut, a short even surface stays
            tl.append(f'tl.to("#{s} .kw-fzlg",{{opacity:0,duration:0.8}},{c.t(at + 0.2):.3f});')
            tl.append(f'tl.to("#{s} .kw-fzsg",{{opacity:1,duration:0.8}},{c.t(at + 0.2):.3f});')
            tl.append(f'tl.to("#{s} .kw-wv",{{filter:"blur(1.2px)",duration:0.8}},{c.t(at + 0.2):.3f});')
            tl.append(f'tl.fromTo("#{s} .kw-blade",{{opacity:1,x:-40}},{{x:{win + 40},duration:1.0,ease:"none"}},{c.t(at + 0.1):.3f});')
            tl.append(f'tl.to("#{s} .kw-blade",{{opacity:0,duration:0.2}},{c.t(at + 1.1):.3f});')
        elif kind == "checked":
            tl.append(_draw(c, ".kw-ring", at + 0.2, 0.7))
        events.append(c.t(at))
    out.html = f"""<div class="kw-in">
  <div class="kw-title" style="top:{zt + 4}px"><span class="kw-ttl kw-ttl-s">{_e(ti)}</span></div>
  {"".join(labels)}
  <div class="kw-ltbox" style="left:{lt_left:.0f}px;top:{lt_top}px">{linen_tester(f"{s}lt", win, view + f'<div class="kw-blade" style="position:absolute;top:0;bottom:0;width:6px;background:linear-gradient(90deg,transparent,{CHALK},transparent);opacity:0"></div>')}</div>
  <svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-ring" pathLength="1" d="M{540 + 280},{lt_top + 260} C{540 + 300},{lt_top + 60} {540 - 300},{lt_top + 40} {540 - 290},{lt_top + 250} C{540 - 300},{lt_top + 470} {540 + 290},{lt_top + 480} {540 + 284},{lt_top + 280}"/></svg>
  <div class="kw-cnote" style="top:{lt_top + win + 64:.0f}px">{_e(d.get("colors_note", ""))}</div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".kw-title", ti_at, dy=14))
    out.tl.append(f'tl.fromTo("#{s} .kw-ltbox",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{c.t(0.15):.3f});')
    if d.get("start_state") == "milled":
        out.tl.insert(0, f'tl.set("#{s} .kw-wv",{{scale:0.9,transformOrigin:"50% 50%",filter:"blur(2.2px)"}},{c.start:.3f});')
        out.tl.insert(0, f'tl.set("#{s} .kw-fzlg",{{opacity:1}},{c.start:.3f});')
    if d.get("colors_note"):
        out.tl.append(_in(c, ".kw-cnote", 0.8, dy=6))
    out.tl += tl
    out.html += _source(c, d, out, "kw_finish")
    out.events = sorted(set(events))
    return out


TEMPLATES.update({"kw_weigh": kw_weigh, "kw_range": kw_range, "kw_fibre": kw_fibre, "kw_yarn": kw_yarn, "kw_finish": kw_finish})
_kw_css_base = CSS


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: F811,N802 (contract name)
    txt, mut = pal.get("text", "#F2EEE6"), pal.get("muted", "#9AA0A8")
    D, B = f"'FN {display}'", f"'FN {body}'"
    return _kw_css_base(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
.kw-ttl-s{{font-size:62px;}}
.kw-scale{{position:absolute;border-radius:18px;background:linear-gradient(160deg,#4A505A,#2B3038);box-shadow:0 22px 34px rgba(2,6,14,0.6),inset 0 2px 0 rgba(255,255,255,0.12);}}
.kw-display{{position:absolute;width:300px;height:96px;border-radius:12px;background:#0B1018;border:3px solid #5A606B;display:flex;align-items:center;justify-content:center;gap:14px;box-shadow:0 12px 24px rgba(0,0,0,0.5);}}
.kw-display b{{position:relative;width:170px;height:70px;}}
.kw-display b span{{position:absolute;right:0;top:0;font-family:{B};font-weight:600;font-size:64px;line-height:70px;color:#CFE6C4;letter-spacing:0.02em;}}
.kw-display i{{font-style:normal;font-family:{B};font-weight:600;font-size:40px;color:#CFE6C4;}}
.kw-readlab{{position:absolute;left:{X0}px;width:{X1 - X0}px;text-align:center;font-family:{B};font-weight:500;font-size:38px;color:{txt};}}
.kw-mark{{text-align:center;font-size:36px;line-height:1.15;}}
.kw-mark small,.kw-fibl small{{display:block;font-size:28px;font-weight:500;margin-top:4px;opacity:0.85;}}
.kw-band{{position:absolute;height:82px;background:rgba(169,211,176,0.28);border:2px solid rgba(169,211,176,0.7);border-radius:4px;}}
.kw-bandl,.kw-driftl{{text-align:center;font-size:38px;}}
.kw-fib{{position:absolute;border-radius:50%;background:radial-gradient(circle at 35% 30%,#F4ECD8 0%,#D9CBA8 55%,#A8977A 100%);box-shadow:0 0 0 3px rgba(238,231,215,0.0),0 16px 26px rgba(2,6,14,0.55);}}
.kw-fibl{{width:300px;text-align:center;font-size:36px;line-height:1.15;}}
.kw-fb{{fill:none;stroke:#E8DCC0;stroke-width:4;stroke-linecap:round;stroke-opacity:0.92;}}
.kw-twist{{opacity:0;}} .kw-twist path{{stroke:{CHALK};stroke-width:2.5;stroke-opacity:0.55;}}
.kw-noil{{opacity:0;}}
"""


# =========================================================================================================
# Photo layer (Neustart 03.11.2026, Testvideo-Konzept 2026-11): photorealistic Higgsfield stills ("so sieht es aus")
# under or beside the chalk drawing ("so ist es gebaut"). Files are named relative to brands/menswear/assets/higgsfield
# (e.g. "testvideo/sw_tv_pair_light.jpg"); LAYER copies every referenced file to <project>/assets/kw/. Every scene
# that shows a photo carries the stamp "KI-Bild". Photos never prove a weave: the structure stays in warp_up().
#
# | scene type | role | data |
# |------------|------|------|
# | kw_photo   | full-bleed photo sequence with a slow camera move, chalk question, chalk marks, | shots[{src, at, zoom, pan}], dim, question{text, at}, chalk_at, |
# |            | linen tester landing on the cloth                                              | neq{x, y, at}, notes[{text, x, y, w, at}], lens{at, kind, swap_at, swap_kind}, source |
# Options on other scenes: kw_weave / kw_draft `backdrop` {src, dim, zoom}; kw_flip sides `photo` {front, back};
# kw_close `shots` [{src, at, zoom, dim}] (the swatches give way to the photo, the sign-off sits on the last one).
# =========================================================================================================

PHOTO_ROOT = Path(__file__).resolve().parent.parent / "assets" / "higgsfield"
STAMP_PHOTO = {"de": "KI-Bild", "en": "AI image"}
LIMITS.update({"kw_photo": {"question": 34, "note": 30, "source": 70}})
HOOK_SCENE_TYPES.append("kw_photo")


def _href(src: str) -> str:
    return "assets/kw/" + Path(str(src)).name


def _photo_files(obj) -> list[str]:
    """Every photo path in a beat's data (keys src, front, back)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("src", "front", "back", "clip") and isinstance(v, str) and v.lower().endswith((".jpg", ".jpeg", ".png", ".mp4")):
                out.append(v)
            else:
                out += _photo_files(v)
    elif isinstance(obj, list):
        for v in obj:
            out += _photo_files(v)
    return out


def _stamp(c: SceneCtx, cls: str = "") -> str:
    return f'<div class="kw-aistamp {cls}">{_e(STAMP_PHOTO.get(c.lang, STAMP_PHOTO["de"]))}</div>'


def _shots(c: SceneCtx, shots: list[dict], out: SceneOut, *, dim: float = 0.35, cls: str = "kw-shot") -> tuple[str, list[str], list[float]]:
    """Full-bleed photos, cross-faded at their `at`, each with a slow zoom and pan over the rest of the beat."""
    html_, tl, ev = [], [], []
    for i, sh in enumerate(shots):
        at = _rel(c, sh.get("at"), 0.0, out) if i else 0.0
        z0, z1 = (sh.get("zoom") or [1.0, 1.08])[:2]
        px = sh.get("pan") or [0, 0, 0, -30]
        d_ = float(sh.get("dim", dim))
        html_.append(f'<div class="{cls} {cls}{i}" style="position:absolute;inset:0;overflow:hidden;opacity:{1 if i == 0 else 0}">'
                     f'<img class="kw-shimg" data-shot="{c.sid}:{cls}:{i}" src="{_href(sh["src"])}" style="position:absolute;left:-2%;top:-2%;width:104%;height:104%;object-fit:cover"/>'
                     f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,12,22,{min(0.9, d_ + 0.35):.2f}) 0%,'
                     f'rgba(8,12,22,{d_:.2f}) 22%,rgba(8,12,22,{d_:.2f}) 58%,rgba(8,12,22,{min(0.92, d_ + 0.45):.2f}) 100%)"></div></div>')
        sel = f"#{c.sid} .{cls}{i} .kw-shimg"
        tl.append(f'tl.fromTo("{sel}",{{scale:{z0},x:{px[0]},y:{px[1]}}},{{scale:{z1},x:{px[2]},y:{px[3]},duration:{max(1.0, c.duration - at):.2f},ease:"none"}},{c.t(at):.3f});')
        if i:
            tl.append(f'tl.to("#{c.sid} .{cls}{i}",{{opacity:1,duration:0.6,ease:"power1.inOut"}},{c.t(at):.3f});')
            tl.append(f'tl.to("#{c.sid} .{cls}{i - 1}",{{opacity:0,duration:0.6,ease:"power1.inOut"}},{c.t(at + 0.1):.3f});')
            ev.append(c.t(at))
    return "".join(html_), tl, ev


def _inject(out: SceneOut, html_: str) -> None:
    """Put html_ as the first child of the scene's .kw-in (under all scene content)."""
    out.html = out.html.replace('<div class="kw-in">', '<div class="kw-in">' + html_, 1)


def kw_photo(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    q = d.get("question") or {}
    _chk("kw_photo", "question", q.get("text", ""), "question", out)
    shots_html, tl, events = _shots(c, d.get("shots", []), out, dim=float(d.get("dim", 0.3)))
    parts = []
    if q.get("text"):
        parts.append(f'<div class="kw-q" style="top:{zt + 10}px">{_e(q["text"])}</div>')
        parts.append(f'<svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-stroke" pathLength="1" d="M{X0 + 60},{zt + 110} C{X0 + 260},{zt + 96} {X1 - 300},{zt + 126} {X1 - 60},{zt + 104}"/></svg>')
    neq = d.get("neq") or {}
    if neq:
        x, y = float(neq.get("x", 540)), float(neq.get("y", 900))
        parts.append(f'<svg class="kw-over" viewBox="0 0 1080 1920"><path class="kw-st kw-neq" pathLength="1" d="M{x - 34:.0f},{y - 18:.0f} L{x + 34:.0f},{y - 18:.0f} M{x - 34:.0f},{y + 18:.0f} L{x + 34:.0f},{y + 18:.0f} M{x + 24:.0f},{y - 46:.0f} L{x - 24:.0f},{y + 46:.0f}"/></svg>')
    for i, n in enumerate(d.get("notes", [])):
        _chk("kw_photo", "note", n.get("text", ""), f"notes{i}.text", out)
        parts.append(f'<div class="kw-chalk kw-pnote pn{i}" style="left:{n.get("x", X0)}px;top:{n.get("y", 900)}px;width:{n.get("w", 400)}px">{_e(n.get("text", ""))}</div>')
    lens = d.get("lens") or {}
    win = 420
    if lens:
        views = []
        for k, kind in enumerate([lens.get("kind", "plain")] + ([lens["swap_kind"]] if lens.get("swap_kind") else [])):
            inner, size = weave_svg(f"{s}z{k}", kind, 8, 34, warp=NAVY_WARP, weft=NAVY_WEFT, shuttle=False)
            views.append(f'<svg class="kw-zv zv{k}" viewBox="0 0 {size:.0f} {size:.0f}" width="{win}" height="{win}" '
                         f'style="position:absolute;inset:0;opacity:{1 if k == 0 else 0}">{inner}</svg>')
        parts.append(f'<div class="kw-ltbox kw-plens" style="left:{540 - (win + 44) / 2 + 30:.0f}px;top:{zt + 300}px">{linen_tester(f"{s}lt", win, "".join(views))}</div>')
    out.html = f'<div class="kw-in">{shots_html}{_stamp(c)}{"".join(parts)}</div>'
    out.tl += _frame(c)
    out.tl += tl
    events += [c.start]
    if q.get("text"):
        qa = _rel(c, q.get("at"), 0.2, out)
        out.tl.append(_in(c, ".kw-q", qa, dy=20, dur=0.5))
        ca = _rel(c, d.get("chalk_at"), qa + 0.6, out)
        out.tl.append(_draw(c, ".kw-stroke", ca, 0.7))
        events += [c.t(qa), c.t(ca)]
    if neq:
        na = _rel(c, neq.get("at"), 2.0, out)
        out.tl.append(_draw(c, ".kw-neq", na, 0.6))
        events.append(c.t(na))
    for i, n in enumerate(d.get("notes", [])):
        na = _rel(c, n.get("at"), 1.0 + i, out)
        out.tl.append(_in(c, f".pn{i}", na, dy=8))
        events.append(c.t(na))
    if lens:
        la = _rel(c, lens.get("at"), c.duration - 3.0, out)
        if neq:
            out.tl.append(f'tl.to("#{s} .kw-neq",{{opacity:0,duration:0.25}},{c.t(la - 0.1):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .kw-plens",{{opacity:0,y:220,scale:1.25}},{{opacity:1,y:0,scale:1,duration:0.7,ease:"power3.out"}},{c.t(la):.3f});')
        events.append(c.t(la))
        if lens.get("swap_kind"):
            sa = _rel(c, lens.get("swap_at"), la + 2.0, out)
            out.tl.append(f'tl.to("#{s} .zv0",{{opacity:0,duration:0.4}},{c.t(sa):.3f});')
            out.tl.append(f'tl.to("#{s} .zv1",{{opacity:1,duration:0.4}},{c.t(sa):.3f});')
            events.append(c.t(sa))
    out.html += _source(c, d, out, "kw_photo")
    out.events = sorted(set(events))
    return out


def swatch_photo_svg(uid: str, src: str, w: float, h: float) -> str:
    """A photo of real cloth, cut with pinking shears (same outline as the drawn swatches)."""
    outline = _pinked(w, h)
    return (f'<svg class="kw-sw" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" style="overflow:visible">'
            f'<defs><clipPath id="{uid}c"><path d="{outline}"/></clipPath></defs>'
            f'<image href="{_href(src)}" x="0" y="0" width="{w:.0f}" height="{h:.0f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{uid}c)"/></svg>')


# --- wrap the existing scenes with the photo options ------------------------------------------------------------

def _with_backdrop(fn):
    def wrapped(c: SceneCtx, d: dict) -> SceneOut:
        out = fn(c, d)
        bd = d.get("backdrop")
        if bd:
            html_, tl, _ = _shots(c, [dict(bd, at=0)], out, dim=float(bd.get("dim", 0.62)), cls="kw-bd")
            _inject(out, html_ + _stamp(c))
            out.tl = tl + out.tl
        return out
    wrapped.__name__ = fn.__name__
    return wrapped


_kw_flip_drawn = kw_flip


def kw_flip(c: SceneCtx, d: dict) -> SceneOut:  # noqa: F811
    out = _kw_flip_drawn(c, d)
    photo = False
    for k, key in enumerate(("left", "right")):
        ph = (d.get(key) or {}).get("photo")
        if not ph:
            continue
        photo = True
        sw_w, sw_h = 360, (540 if _deep(c) else 470)
        for side, part in (("front", "fa"), ("back", "fb")):
            if ph.get(side):
                # replace the drawn swatch of this side with the photo, keep the box (position, flip animation)
                out.html = re.sub(rf'(<div class="kw-swbox {part}{k}"[^>]*>)<svg class="kw-sw".*?</svg>(</div>)',
                                  lambda m: m.group(1) + swatch_photo_svg(f"{c.sid}{part}{k}p", ph[side], sw_w, sw_h) + m.group(2),
                                  out.html, count=1, flags=re.S)
    if photo:
        _inject(out, _stamp(c))
    return out


_kw_close_drawn = kw_close


def kw_close(c: SceneCtx, d: dict) -> SceneOut:  # noqa: F811
    out = _kw_close_drawn(c, d)
    shots = d.get("shots") or []
    for k, ph in enumerate(d.get("swatch_photos") or []):
        if ph:   # real cloth instead of the drawn swatch, same box and light sweep
            out.html = re.sub(rf'(<div class="kw-swbox cs{k}"[^>]*>)<svg class="kw-sw".*?</svg>',
                              lambda m: m.group(1) + swatch_photo_svg(f"{c.sid}cs{k}p", ph, 350, 370), out.html, count=1, flags=re.S)
    if not shots:
        return out
    s = c.sid
    html_, tl, ev = [], [], []
    for i, sh in enumerate(shots):
        at = _rel(c, sh.get("at"), 0.0, out)
        h, t2, _ = _shots(c, [dict(sh, at=0)], out, dim=float(sh.get("dim", 0.4)), cls=f"kw-cs{i}x")
        html_.append(f'<div class="kw-csh csh{i}" style="position:absolute;inset:0;opacity:0">{h}</div>')
        # the camera move of each shot starts when it appears
        tl += [x.replace(f"{c.start:.3f});", f"{c.t(at):.3f});") if x.endswith(f"{c.start:.3f});") else x for x in t2]
        tl.append(f'tl.to("#{s} .csh{i}",{{opacity:1,duration:0.6,ease:"power1.inOut"}},{c.t(at):.3f});')
        if i == 0:
            tl.append(f'tl.to("#{s} .kw-tilt,#{s} .kw-verdict,#{s} .kw-cchip,#{s} .cu0,#{s} .cu1",{{opacity:0,duration:0.4}},{c.t(at):.3f});')
        else:
            tl.append(f'tl.to("#{s} .csh{i - 1}",{{opacity:0,duration:0.6}},{c.t(at + 0.1):.3f});')
        ev.append(c.t(at))
    if d.get("rays_at") is not None:   # chalk follows the twill ribs on the photo (top right to bottom left)
        ra = _rel(c, d.get("rays_at"), 0.0, out)
        rays = "".join(f'<path class="kw-st kw-arw kw-ray r{j}" pathLength="1" d="M{700 + 60 * j},{520 + 40 * j} L{420 + 60 * j},{800 + 40 * j}"/>' for j in range(3))
        html_.append(f'<svg class="kw-over kw-rays" viewBox="0 0 1080 1920">{rays}</svg>')
        for j in range(3):
            tl.append(_draw(c, f".r{j}", ra + 0.25 * j, 0.6))
        sign = _rel(c, d.get("sign_at"), c.duration - 3.0, out)
        tl.append(f'tl.to("#{s} .kw-rays",{{opacity:0,duration:0.3}},{c.t(sign - 0.35):.3f});')
        ev.append(c.t(ra))
    _inject(out, "".join(html_) + _stamp(c, "kw-aistamp-close"))
    out.tl = out.tl[:2] + tl + out.tl[2:]
    out.events = sorted(set(out.events + ev))
    return out


kw_weave = _with_backdrop(kw_weave)
kw_draft = _with_backdrop(kw_draft)
kw_weigh = _with_backdrop(kw_weigh)
kw_range = _with_backdrop(kw_range)
kw_fibre = _with_backdrop(kw_fibre)
kw_yarn = _with_backdrop(kw_yarn)
kw_finish = _with_backdrop(kw_finish)
TEMPLATES.update({"kw_weigh": kw_weigh, "kw_range": kw_range, "kw_fibre": kw_fibre, "kw_yarn": kw_yarn, "kw_finish": kw_finish, "kw_photo": kw_photo, "kw_weave": kw_weave, "kw_draft": kw_draft, "kw_flip": kw_flip, "kw_close": kw_close})
_kw_css_photo = CSS


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: F811,N802 (contract name)
    mut = pal.get("muted", "#9AA0A8")
    B = f"'FN {body}'"
    return _kw_css_photo(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
.kw-aistamp{{position:absolute;right:{1080 - X1}px;top:{zone_top + 4}px;z-index:5;font-family:{B};font-weight:600;font-size:24px;letter-spacing:0.08em;
 color:#EEE7D7;background:rgba(8,12,22,0.55);border:1.5px solid rgba(238,231,215,0.45);border-radius:6px;padding:2px 10px;}}
.kw-aistamp-close{{top:{zone_top + 70}px;}}
.kw-pnote{{font-size:40px;line-height:1.15;text-shadow:0 2px 12px rgba(0,0,0,0.6);}}
.kw-q{{text-shadow:0 3px 18px rgba(0,0,0,0.55);}}
"""


_kw_layer_drawn = LAYER


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: F811,N802 (contract name)
    """The cloth layer plus: copy every photo the plan uses to <project>/assets/kw/."""
    res = _kw_layer_drawn(plan, brand, project_dir, captions)
    import shutil
    dst = Path(project_dir) / "assets" / "kw"
    problems = list(res.get("problems", []))
    for b in getattr(plan, "beats", []):
        for src in _photo_files(getattr(b, "data", {}) or {}):
            p = PHOTO_ROOT / src
            if not p.exists():
                problems.append(f"{b.id}: photo {src} not found under {PHOTO_ROOT}")
                continue
            dst.mkdir(parents=True, exist_ok=True)
            if not (dst / p.name).exists():
                shutil.copy2(p, dst / p.name)
    res["problems"] = problems
    return res


# --- Kling clips (03.11.2026) ------------------------------------------------------------------------------------
# A shot may carry `clip` (an .mp4 whose first frame is the still in `src`, e.g. a Kling clip started from that still)
# and `mirror: true`. The renderer plays clips as top-level clips, so LAYER puts each one under the scenes (track 0,
# above the cloth ground) and hides the still in the scene when the clip starts. The clip is placed at the END of its
# segment (start = max(segment start, segment end - clip length)): the still shows first, then the clip takes over
# on the same frame, so there is no jump. The dim gradient of the shot stays in the scene above the clip.
CLIP_SECONDS = 8.0


def _clip_segments(beat, words) -> list[dict]:
    """Clips of one beat with absolute times: [{clip, mirror, start, end, still}]; `still` is the data-shot key."""
    d = getattr(beat, "data", {}) or {}
    st, du = getattr(beat, "start", None), getattr(beat, "duration", None)
    if st is None or du is None:
        return []
    bw = [w for w in words if st <= w.start < st + du]

    def at(v, default):
        if v is None or v == "":
            return default
        if isinstance(v, (int, float)):
            return float(v)
        m = re.fullmatch(r"w:(.+?)(?:#(\d+))?([+\-]\d+(?:\.\d+)?)?", str(v).strip())
        if m:
            hits = [w for w in bw if _norm(w.text).startswith(_norm(m.group(1)))]
            n = int(m.group(2) or 1)
            if len(hits) >= n:
                return max(0.0, hits[n - 1].start - st + float(m.group(3) or 0))
        return default
    segs = []
    groups = []
    if getattr(beat, "scene_type", "") == "kw_photo":
        groups.append(("kw-shot", d.get("shots") or [], False))
    if d.get("backdrop"):
        groups.append(("kw-bd", [dict(d["backdrop"], at=0)], False))
    if getattr(beat, "scene_type", "") == "kw_close" and d.get("shots"):
        groups.append(("kw-cs", d["shots"], True))
    for cls, shots, per_shot_cls in groups:
        times = [at(s.get("at"), 0.0) if (i or per_shot_cls) else 0.0 for i, s in enumerate(shots)]
        for i, s in enumerate(shots):
            if not s.get("clip"):
                continue
            a = times[i]
            b = times[i + 1] if i + 1 < len(shots) else du
            length = float(s.get("clip_seconds", CLIP_SECONDS))
            cs = max(a, b + 0.6 - length)     # runs 0.6 s into the next shot's cross-fade
            key = f"{beat.id}:{cls}{i}x:0" if per_shot_cls else f"{beat.id}:{cls}:{i}"
            segs.append({"clip": s["clip"], "mirror": bool(s.get("mirror")), "start": st + cs, "end": st + min(du, b + 0.6), "still": key,
                         "fade_in": cs <= a + 0.01})
    return segs


_kw_layer_photo = LAYER


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: F811,N802 (contract name)
    res = _kw_layer_photo(plan, brand, project_dir, captions)
    words = [w for g in captions for w in getattr(g, "words", [])]
    html_, js = [], []
    for b in getattr(plan, "beats", []):
        for k, seg in enumerate(_clip_segments(b, words)):
            vid = f"kwclip-{b.id}-{k}"
            dur = max(0.1, seg["end"] - seg["start"])
            flip = "transform:scaleX(-1);" if seg["mirror"] else ""
            html_.append(f'<video id="{vid}" class="clip kw-clip" src="{_href(seg["clip"])}" data-start="{seg["start"]:.3f}" '
                         f'data-duration="{dur:.3f}" data-track-index="0" data-volume="0" muted playsinline '
                         f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:1;{flip}"></video>')
            # the still in the scene gives way when the clip starts (same frame, so no visible jump)
            js.append(f'T.set(\'[data-shot="{seg["still"]}"]\',{{opacity:0}},{seg["start"] + 0.04:.3f});')
            if seg["fade_in"]:
                js.append(f'T.fromTo("#{vid}",{{opacity:0}},{{opacity:1,duration:0.5}},{seg["start"]:.3f});')
    if html_:
        res["under_scenes_html"] = res.get("under_scenes_html", "") + "".join(html_)
        res["body_end_html"] = res.get("body_end_html", "") + (
            "<script>(function(){var T=window.__timelines&&window.__timelines.main;if(!T)return;" + "".join(js) + "T.seek(0);})();</script>")
    return res
