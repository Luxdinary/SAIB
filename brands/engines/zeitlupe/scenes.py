"""Revlore format "Zeitlupe" (02.11.2026): scene types zl_*, see OneDrive\\Business\\02 Marke\\Revlore\\Format-Bibel.md.

The picture explains what the voice alone cannot: the engine first runs in real time as a long exposure (nothing
recognisable), drops into slow motion with the factor on screen, equal-time strobe ticks show where the piston is
fast, a pen draws the measured curve in step with the crank, and at the end the engine speeds back up to real time.

All motion comes from the slider-crank model of brands/engines/scenes.py. The brand module injects its namespace as
`RV` before this file runs (see the block at the end of brands/engines/scenes.py), so kinematics, the engine drawing
and its animation exist exactly once.

Scene types:
- zl_hook     real time (long exposure) -> slow motion, question on screen, optional still frame and mid-stroke line
- zl_strobe   model, velocity arrow next to the bore, stroke ruler with a tick every `step` crank degrees (equal time)
- zl_cause    same layout; rod highlight, rod angle beta, a ghost piston on the pure sine path, gap on the ruler
- zl_trace    small model and a measuring panel: crank angle and ms axes, pen draws the curve with the crank
- zl_realtime result rows, the engine speeds up until real time, brand line

Persistent elements (every scene): slow-motion band at the top (factor computed from the crank speed against the
reference speed `ref_rpm`, default 3000/min, an example value), source line at the bottom (`source`), optional dial
with crank angle and ms after TDC at the reference speed.
"""
from __future__ import annotations

import math

from fn.render.templates import SceneCtx, SceneOut

AMBER = "#F5B342"
REF_RPM = 3000.0
LEFT, RIGHT = 108, 920          # x >= 930 stays free for platform icons
BAND_Y = 262                    # baseline of the slow-motion band (logo above at 120-160)
SRC_Y = 1290                    # source line above the captions (prüfrunde 03.11.: below them it is hidden by platform UI)
STEP = 15.0                     # strobe step in crank degrees
MOVING = ("piston", "rod", "rodhi", "crank", "crankpin", "vin", "vex", "camin", "camex", "gas", "flowin", "flowex", "spark")

R, L = RV.R, RV.L  # noqa: F821  (RV is injected by the brand module)
CX, CY = RV.CX, RV.CY  # noqa: F821


def frac(a: float) -> float:
    """Piston travel from TDC as a fraction of the stroke (real slider-crank)."""
    return (RV.pin_y(a) - RV.PIN_TDC) / (2 * R)  # noqa: F821


def frac_sine(a: float) -> float:
    """Same for a pure sine motion (infinitely long rod)."""
    return (1 - math.cos(math.radians(a))) / 2


def vel(a: float) -> float:
    """Piston velocity in units of R*omega, positive = downwards."""
    return RV.piston_velocity(a) / R  # noqa: F821


def vel_sine(a: float) -> float:
    return math.sin(math.radians(a))


A_VMAX = max((i / 10 for i in range(0, 1800)), key=vel)       # 74.0 deg for lambda = 0.3125
VMAX = vel(A_VMAX)


def _e(s) -> str:
    return RV._e(s)  # noqa: F821


def _k(c: SceneCtx) -> dict:
    k = RV._pal(c)  # noqa: F821
    k["amber"] = AMBER
    return k


def _num(x: float, nd: int = 1, de: bool = True) -> str:
    out = f"{x:.{nd}f}"
    return out.replace(".", ",") if de else out


# --- ground and wrapper ------------------------------------------------------------------------------

def _ground(s: str, k: dict) -> str:
    """Measuring room: graphite gradient, one static 40 px grid, vignette. No drifting drawings (that backdrop belongs
    to the old template); the only motion in the picture comes from the mechanism."""
    return (f'<defs><pattern id="{s}-zg" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0 L0,0 L0,40" fill="none" '
            f'stroke="{k["steel"]}" stroke-opacity="0.05" stroke-width="1"/></pattern>'
            f'<linearGradient id="{s}-zexp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{k["steel"]}" stop-opacity="0.9"/>'
            f'<stop offset="0.14" stop-color="{k["steel"]}" stop-opacity="0.5"/><stop offset="0.5" stop-color="{k["steel"]}" stop-opacity="0.26"/>'
            f'<stop offset="0.86" stop-color="{k["steel"]}" stop-opacity="0.5"/><stop offset="1" stop-color="{k["steel"]}" stop-opacity="0.9"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-bgv)"/>'
            f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-zg)"/>'
            f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-vig)"/>')


def _out(c: SceneCtx, k: dict, inner: str, tl: list[str], ev: list[float], problems: list[str]) -> SceneOut:
    html_ = (f'<div class="scene-inner rv zl"><svg class="rv-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
             f'{RV._defs(c.sid, k)}{_ground(c.sid, k)}{inner}</svg></div>')  # noqa: F821
    evs = sorted(set(round(e, 3) for e in ev if c.start - 1e-3 <= e <= c.end + 1e-3))
    return SceneOut(html=html_, tl=tl, events=evs, problems=problems)


def _show(sel: str, t: float, dur: float = 0.3, y: float = 0) -> str:
    return RV._show(sel, t, dur, y)  # noqa: F821


def _check(problems: list[str], field: str, text: str, lim: int) -> None:
    if len(text) > lim:
        problems.append(f"revlore.zeitlupe.{field}: {len(text)} chars > {lim}")


# --- slow-motion band ---------------------------------------------------------------------------------

def _factor(w: float, ref: float) -> tuple[str, str]:
    """(mode, factor) for a crank speed w in deg/s against the reference speed in 1/min."""
    if w < 1.0:
        return "stand", ""
    f = ref / (w / 6.0)
    if f < 1.5:
        return "real", "1:1"
    n = round(f / 10) * 10 if f >= 100 else (round(f / 5) * 5 if f >= 20 else round(f))
    return "slow", f"1:{int(n)}"


def _band(c: SceneCtx, d: dict, k: dict, track, real: list[tuple[float, float]]) -> tuple[str, list[str], list[float]]:
    """Top band: ECHTZEIT / ZEITLUPE 1:n / STANDBILD, computed per knot segment of the crank track; `real` lists
    intervals shown as real time (long exposure). Segments shorter than 0.3 s keep the previous label."""
    s = c.sid
    ref = float(d.get("ref_rpm", REF_RPM))
    de = c.lang == "de"
    names = {"real": "ECHTZEIT" if de else "REAL TIME", "slow": "ZEITLUPE" if de else "SLOW MOTION",
             "stand": "STANDBILD" if de else "FREEZE"}
    segs: list[tuple[float, float, tuple[str, str]]] = []
    knots = [(c.start, track.k[0][1])] + [kn for kn in track.k if c.start < kn[0] < c.end] + [(c.end, track.angle(c.end))]
    for (ta, _), (tb, _) in zip(knots, knots[1:]):
        if tb - ta < 1e-3:
            continue
        w = (track.angle(tb) - track.angle(ta)) / (tb - ta)
        lab = _factor(w, ref)
        for r0, r1 in real:
            if r0 - 1e-3 <= ta and tb <= r1 + 1e-3:
                lab = ("real", "1:1")
        if segs and (segs[-1][2] == lab or tb - ta < 0.3):
            segs[-1] = (segs[-1][0], tb, segs[-1][2])
        else:
            segs.append((ta, tb, lab))
    labels = sorted({sg[2] for sg in segs})
    svg = [f'<line x1="{LEFT}" y1="292" x2="{RIGHT}" y2="292" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="2"/>',
           f'<text class="zl-ref" x="{RIGHT}" y="{BAND_Y}" text-anchor="end">{_e(("Beispiel: %d/min" if de else "example: %d rpm") % ref)}</text>']
    for i, (mode, fac) in enumerate(labels):
        fac_html = f'<tspan class="zl-fac" dx="16">{_e(fac)}</tspan>' if fac and mode != "real" else ""
        svg.append(f'<text id="{s}-zb{i}" class="zl-mode{" real" if mode == "real" else ""}" x="{LEFT}" y="{BAND_Y}" opacity="0">'
                   f'{_e(names[mode])}{fac_html}</text>')
    tl, ev = [], []
    for j, (ta, tb, lab) in enumerate(segs):
        i = labels.index(lab)
        tl.append(f'tl.set("#{s}-zb{i}",{{opacity:1}},{ta:.3f});')
        if j + 1 < len(segs):
            tl.append(f'tl.set("#{s}-zb{i}",{{opacity:0}},{tb:.3f});')
            ev.append(tb)
    return "".join(svg), tl, ev


def _source(c: SceneCtx, d: dict, problems: list[str], y: float = SRC_Y) -> str:
    src = d.get("source", "")
    if not src:
        return ""
    _check(problems, "source", src, 64)
    return f'<text class="zl-src" x="{LEFT}" y="{y}">{_e(("Quelle: " if c.lang == "de" else "Source: ") + src)}</text>'


# --- dial: crank angle and time after TDC at the reference speed ---------------------------------------

def _dial(c: SceneCtx, d: dict, k: dict, track, cx: float, cy: float, r: float = 70) -> tuple[str, list[str]]:
    s = c.sid
    ref = float(d.get("ref_rpm", REF_RPM))
    ms_rev = 60000.0 / ref
    de = c.lang == "de"
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{k["surface"]}" fill-opacity="0.9" stroke="{k["steel"]}" stroke-opacity="0.5" stroke-width="2"/>',
           f'<path id="{s}-dsec" d="M{cx},{cy} L{cx},{cy - r + 6} Z" fill="{k["accent"]}" fill-opacity="0.22"/>']
    for a in range(0, 360, 30):
        ln = 14 if a % 90 == 0 else 7
        x1, y1 = cx + (r - ln) * math.sin(math.radians(a)), cy - (r - ln) * math.cos(math.radians(a))
        x2, y2 = cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a))
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{k["steel"]}" stroke-width="2"/>')
    for a in (0, 90, 180, 270):
        v = ms_rev * a / 360.0
        txt = _num(v, 0) if abs(v - round(v)) < 1e-6 else _num(v, 1)
        if a == 180:
            txt += " ms"
        x = cx + (r + 24) * math.sin(math.radians(a))
        y = cy - (r + 24) * math.cos(math.radians(a)) + 9
        anchor = "middle" if a in (0, 180) else ("start" if a == 90 else "end")
        if a == 0:
            y -= 4
        if a == 180:
            y += 10
        out.append(f'<text class="zl-dial" x="{x - (8 if a == 90 else (-8 if a == 270 else 0)) + (0 if a in (0, 180) else 0):.1f}" y="{y:.1f}" text-anchor="{anchor}">{txt}</text>')
    out.append(f'<g id="{s}-dptr" transform="rotate(0 {cx} {cy})"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 6}" stroke="{k["accent"]}" stroke-width="5" stroke-linecap="round"/>'
               f'<circle cx="{cx}" cy="{cy}" r="7" fill="{k["accent"]}"/></g>')
    out.append(f'<text class="zl-dial-s" x="{cx - r - 24}" y="{cy + r + 40}" text-anchor="end">{_e("nach OT" if de else "after TDC")}</text>')

    def sector(a: float) -> str:
        # fixed number of points: GSAP interpolates the path number by number, so the structure must never change
        m = a % 360.0
        rr = r - 6
        pts = " L".join(f"{cx + rr * math.sin(math.radians(m * i / 36)):.1f},{cy - rr * math.cos(math.radians(m * i / 36)):.1f}" for i in range(37))
        return f"M{cx},{cy} L{pts} Z"
    smp = track.samples(4.0, extra=[0.0, 359.9, 360.0, 719.9])
    tl = RV._kf(f"#{s}-dptr", smp, lambda a: f"rotate({a:.2f} {cx} {cy})", "transform")  # noqa: F821
    tl += RV._kf(f"#{s}-dsec", smp, sector, "d")  # noqa: F821
    return "".join(out), tl


# --- model helpers ------------------------------------------------------------------------------------

def _crown_screen(view, a: float) -> float:
    return RV._T(view, 0, RV.pin_y(a) - RV.PIN2CROWN)[1]  # noqa: F821


def _long_exposure(s: str, k: dict) -> str:
    """Real-time look: the moving parts as a long exposure. The piston band is densest at the dead centres, where the
    piston spends the most time (schematic)."""
    top = RV.CROWN_TDC  # noqa: F821
    h = RV.CROWN_BDC + RV.PISTON_H - top  # noqa: F821
    return (f'<g id="{s}-lex" opacity="0">'
            f'<rect x="{RV.BORE_L + 3}" y="{top:.1f}" width="{RV.BORE_R - RV.BORE_L - 6}" height="{h:.1f}" rx="6" fill="url(#{s}-zexp)"/>'  # noqa: F821
            f'<path d="M{CX - R - 14},{CY} L{CX - 18},{RV.PIN_TDC:.0f} L{CX + 18},{RV.PIN_TDC:.0f} L{CX + R + 14},{CY} Q{CX},{CY + R + 60} {CX - R - 14},{CY} Z" '  # noqa: F821
            f'fill="{k["steel"]}" fill-opacity="0.2"/>'
            f'<circle cx="{CX}" cy="{CY}" r="{R + 36}" fill="url(#{s}-gweb)" fill-opacity="0.55"/>'
            f'<circle cx="{CX}" cy="{CY}" r="{R + 36}" fill="none" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="10"/>'
            f'<circle cx="{CX}" cy="{CY}" r="30" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-width="4"/></g>')


def _realtime(s: str, intervals: list[tuple[float, float]]) -> list[str]:
    """Hide the sharp moving parts and show the long exposure during the given intervals."""
    parts = ",".join(f"#{s}-{p}" for p in MOVING)
    tl = []
    for t0, t1 in intervals:
        tl.append(f'tl.set("{parts}",{{attr:{{visibility:"hidden"}}}},{t0:.3f});')
        tl.append(f'tl.set("#{s}-lex",{{opacity:1}},{t0:.3f});')
        if t1 is not None:
            tl.append(f'tl.set("{parts}",{{attr:{{visibility:"visible"}}}},{t1:.3f});')
            tl.append(f'tl.to("#{s}-lex",{{opacity:0,duration:0.12}},{t1:.3f});')
    return tl


def _arrow(c: SceneCtx, k: dict, view, track, x: float, length: float) -> tuple[str, list[str]]:
    """Velocity arrow beside the bore, anchored at the crown height; length proportional to the piston speed."""
    s = c.sid
    svg = (f'<line id="{s}-zar" x1="{x}" y1="600" x2="{x}" y2="600" stroke="{k["accent"]}" stroke-width="10" '
           f'stroke-linecap="round" marker-end="url(#{s}-arr)" opacity="0"/>')
    smp = track.samples(3.0, extra=[0.0, 180.0, 360.0, 540.0])
    tl = RV._kf(f"#{s}-zar", smp, lambda a: f"{_crown_screen(view, a):.1f}", "y1")  # noqa: F821
    tl += RV._kf(f"#{s}-zar", smp, lambda a: f"{_crown_screen(view, a) + length * vel(a) / VMAX:.1f}", "y2")  # noqa: F821
    return svg, tl


# --- stroke ruler with strobe ticks --------------------------------------------------------------------

def _ruler(c: SceneCtx, d: dict, k: dict, view, track, problems: list[str], *, x: float = 812, y0: float = 470,
           y1: float = 1010, sine: bool = False) -> tuple[str, list[str], list[float]]:
    """Magnified stroke ruler (TDC top, BDC bottom). A tick appears each time the crank passes another `step` degrees
    of the down stroke for the first time in the scene (equal crank steps = equal time at constant speed), so the gaps
    between ticks show where the piston is fast. Pointer follows the crown, a projection line connects both."""
    s = c.sid
    de = c.lang == "de"
    W = 40
    step = float(d.get("step", STEP))
    ref = float(d.get("ref_rpm", REF_RPM))
    Y = lambda f: y0 + (y1 - y0) * f
    angs = [i * step for i in range(int(180 / step) + 1)]
    out = [f'<text class="zl-lab" x="{RIGHT}" y="{min(y0 - 52, 338)}" text-anchor="end">{_e("Kolbenweg" if de else "Piston travel")}</text>',
           f'<text class="zl-lab" x="{RIGHT}" y="{min(y0 - 20, 376)}" text-anchor="end">{_e(("1 Strich = %s ms" if de else "1 tick = %s ms") % _num(60000.0 / ref * step / 360.0, 2, de))}</text>',
           f'<rect x="{x}" y="{y0}" width="{W}" height="{y1 - y0}" rx="6" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-opacity="0.45" stroke-width="2"/>',
           f'<line x1="{x - 26}" y1="{Y(0.5):.1f}" x2="{x + W + 6}" y2="{Y(0.5):.1f}" stroke="{k["steel"]}" stroke-width="2" stroke-dasharray="6 6"/>',
           f'<text class="zl-lab" x="{x - 32}" y="{Y(0.5) + 9:.1f}" text-anchor="end">{_e("Mitte" if de else "Mid")}</text>']
    # widest gap (the fastest stretch)
    gaps = [(frac(b) - frac(a), a, b) for a, b in zip(angs, angs[1:])]
    _, ga, gb = max(gaps)
    out.append(f'<rect id="{s}-zgap" x="{x + 2}" y="{Y(frac(ga)):.1f}" width="{W - 4}" height="{Y(frac(gb)) - Y(frac(ga)):.1f}" fill="{k["accent"]}" fill-opacity="0.45" opacity="0"/>')
    tl, ev = [], []
    pre = bool(d.get("ticks_shown"))
    for i, a in enumerate(angs):
        y = Y(frac(a))
        major = a in (0.0, 90.0, 180.0)
        out.append(f'<line id="{s}-zt{i}" x1="{x - (10 if major else 4)}" y1="{y:.1f}" x2="{x + W + (10 if major else 4)}" y2="{y:.1f}" '
                   f'stroke="{k["text"]}" stroke-width="{4 if major else 3}" opacity="{1 if pre else 0}"/>')
        if a in (0.0, 180.0, 90.0):
            lab = {0.0: "OT" if de else "TDC", 90.0: "90°", 180.0: "UT" if de else "BDC"}[a]
            out.append(f'<text id="{s}-ztl{i}" class="zl-lab" x="{x - 32}" y="{y + 9 + (14 if a == 0 else (-6 if a == 180 else 0)):.1f}" text-anchor="end" opacity="{1 if pre else 0}">{lab}</text>')
        if pre:
            continue
        hits = [t for t in track.times_at(a % 360.0, 360.0) if c.start - 1e-3 <= t <= c.end]
        t = hits[0] if hits else c.start + 0.2
        tl.append(f'tl.set("#{s}-zt{i}",{{opacity:1}},{t:.3f});')
        if a in (0.0, 180.0, 90.0):
            tl.append(f'tl.set("#{s}-ztl{i}",{{opacity:1}},{t:.3f});')
            ev.append(t)                 # the small ticks are mechanism, not picture events
    # pointer, projection line
    bore_x = RV._T(view, RV.BORE_R, 0)[0]  # noqa: F821
    out.append(f'<line id="{s}-zpl" x1="{bore_x + 4:.1f}" y1="600" x2="{x - 4}" y2="600" stroke="{k["accent"]}" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="4 6"/>')
    out.append(f'<path id="{s}-zptr" d="M{x + W + 4},0 L{x + W + 26},-13 L{x + W + 26},13 Z" fill="{k["accent"]}" transform="translate(0,{y0})"/>')
    smp = track.samples(3.0, extra=angs)
    tl += RV._kf(f"#{s}-zpl", smp, lambda a: f"{_crown_screen(view, a):.1f}", "y1")  # noqa: F821
    tl += RV._kf(f"#{s}-zpl", smp, lambda a: f"{Y(frac(a)):.1f}", "y2")  # noqa: F821
    tl += RV._kf(f"#{s}-zptr", smp, lambda a: f"translate(0,{Y(frac(a)):.1f})", "transform")  # noqa: F821
    if "gap_at" in d:
        t = RV.at_time(c, d, d["gap_at"])  # noqa: F821
        tl.append(f'tl.fromTo("#{s}-zgap",{{opacity:0}},{{opacity:1,duration:0.3}},{t:.3f});')
        ev.append(t)
    for j, (key, f) in enumerate((("zero_top_at", 0.0), ("zero_bottom_at", 1.0))):
        if key in d:
            yy = Y(f) + (23 if f == 0 else -9)
            out.append(f'<text id="{s}-zz{j}" class="zl-lab acc" x="{x - 92}" y="{yy:.1f}" text-anchor="end" opacity="0">v = 0</text>')
            t = RV.at_time(c, d, d[key])  # noqa: F821
            tl.append(_show(f"#{s}-zz{j}", t, 0.25))
            ev.append(t)
    if sine:
        out.append(f'<rect id="{s}-zsg" x="{x + 2}" y="{y0}" width="{W - 4}" height="0" fill="{k["accent"]}" fill-opacity="0.5" opacity="0"/>')
        out.append(f'<path id="{s}-zsp" d="M{x - 4},0 L{x - 26},-13 L{x - 26},13 Z" fill="none" stroke="{k["steel"]}" stroke-width="3" transform="translate(0,{y0})" opacity="0"/>')
        tl += RV._kf(f"#{s}-zsp", smp, lambda a: f"translate(0,{Y(frac_sine(a)):.1f})", "transform")  # noqa: F821
        tl += RV._kf(f"#{s}-zsg", smp, lambda a: f"{Y(frac_sine(a)):.1f}", "y")  # noqa: F821
        tl += RV._kf(f"#{s}-zsg", smp, lambda a: f"{max(0.0, Y(frac(a)) - Y(frac_sine(a))):.1f}", "height")  # noqa: F821
    return "".join(out), tl, ev


def _notes(c: SceneCtx, d: dict, k: dict, problems: list[str]) -> tuple[str, list[str], list[float]]:
    """Free notes in screen coordinates: [{text, at, x, y, anchor, color}] (mono 28)."""
    s = c.sid
    svg, tl, ev = [], [], []
    cols = {"accent": k["accent"], "text": k["text"], "steel": k["steel"], "amber": AMBER, "fire": k["fire"]}
    for i, n in enumerate(d.get("notes", [])):
        _check(problems, f"note {i}", n.get("text", ""), 36)
        svg.append(f'<text id="{s}-zn{i}" class="zl-note" x="{n.get("x", LEFT)}" y="{n.get("y", 1120)}" text-anchor="{n.get("anchor", "start")}" '
                   f'fill="{cols.get(n.get("color", "text"), k["text"])}" opacity="0">{_e(n.get("text", ""))}</text>')
        t = RV.at_time(c, d, n.get("at", 0.5))  # noqa: F821
        tl.append(_show(f"#{s}-zn{i}", t, 0.3, 8))
        ev.append(t)
    return "".join(svg), tl, ev


def _engine(c: SceneCtx, d: dict, k: dict, view, track) -> tuple[str, list[str], list[float]]:
    s = c.sid
    opts = {"fuel": d.get("fuel", "petrol"), "injector": d.get("injector"), "knock": bool(d.get("knock"))}
    svg = RV._place(view, RV.engine_svg(s, k, **opts) + _long_exposure(s, k))  # noqa: F821
    tl, ev = RV.engine_anim(s, k, track, **opts)  # noqa: F821
    return svg, tl, ev


# 1. hook: real time -> slow motion ------------------------------------------------------------------------

def zl_hook(c: SceneCtx, d: dict) -> SceneOut:
    """data: claim, claim_lines, claim_highlight, claim_at; slow_at (end of the real-time long exposure); theta;
    mid_at (dashed mid-stroke line with label); strike_at (claim struck through); view; dial; source."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    claim = d.get("claim", "")
    _check(problems, "claim", claim, 64)
    track = RV.Track.from_data(c, d, (0.0, 720.0))  # noqa: F821
    view = RV._view(d, (0.72, 500.0))  # noqa: F821
    t_slow = RV.at_time(c, d, d.get("slow_at", 0.1))  # noqa: F821
    eng, tl, ev = _engine(c, d, k, view, track)
    tl += _realtime(s, [(c.start, t_slow)])
    ev.append(t_slow)
    band, btl, bev = _band(c, d, k, track, [(c.start, t_slow)])
    tl += btl
    ev += bev
    lines = d.get("claim_lines") or [claim]
    hl = d.get("claim_highlight", "")
    cl = []
    for i, ln in enumerate(lines):
        txt = _e(ln)
        if hl and hl in ln:
            txt = txt.replace(_e(hl), f'<tspan class="hl">{_e(hl)}</tspan>')
        cl.append(f'<text class="zl-claim" x="540" y="{372 + i * 88}" text-anchor="middle">{txt}</text>')
    inner = [eng, f'<g id="{s}-zcl" opacity="0">{"".join(cl)}</g>', band]
    q_at = RV.at_time(c, d, d.get("claim_at", 0.05))  # noqa: F821
    tl.append(_show(f"#{s}-zcl", q_at, 0.35, 12))
    ev.append(q_at)
    if "strike_at" in d:
        y = 372 + (len(lines) - 1) * 88 - 26
        w = max(len(x) for x in lines) * 19
        inner.append(f'<line id="{s}-zstr" x1="{540 - w:.0f}" y1="{y}" x2="{540 + w:.0f}" y2="{y}" stroke="{AMBER}" stroke-width="8" stroke-linecap="round" '
                     f'stroke-dasharray="{2 * w:.0f}" stroke-dashoffset="{2 * w:.0f}"/>')
        t = RV.at_time(c, d, d["strike_at"])  # noqa: F821
        tl.append(f'tl.to("#{s}-zstr",{{attr:{{"stroke-dashoffset":0}},duration:0.35,ease:"power2.out"}},{t:.3f});')
        ev.append(t)
    if "mid_at" in d:
        ym = RV._T(view, 0, RV.CROWN_TDC + R)[1]  # noqa: F821
        xa = RV._T(view, 330, 0)[0]  # noqa: F821
        xb = RV._T(view, RV.BORE_R + 30, 0)[0]  # noqa: F821
        inner.append(f'<g id="{s}-zmid" opacity="0"><line x1="{xa:.1f}" y1="{ym:.1f}" x2="{xb:.1f}" y2="{ym:.1f}" stroke="{AMBER}" stroke-width="4" stroke-dasharray="12 9"/>'
                     f'<text class="zl-note" x="{xa - 14:.1f}" y="{ym + 10:.1f}" text-anchor="end" fill="{AMBER}">{_e("Hubmitte" if c.lang == "de" else "Mid-stroke")}</text></g>')
        t = RV.at_time(c, d, d["mid_at"])  # noqa: F821
        tl.append(_show(f"#{s}-zmid", t, 0.25))
        ev.append(t)
    if d.get("dial", True):
        dsv, dtl = _dial(c, d, k, track, 800, 1130)
        inner.append(dsv)
        tl += dtl
    inner.append(_source(c, d, problems))
    return _out(c, k, "".join(inner), tl, ev, problems)


# 2. strobe: velocity arrow and stroke ruler -------------------------------------------------------------

STROBE_VIEW = (0.8, 330.0)


def _view_x(d: dict, default: tuple[float, float], x: float):
    v = dict(d.get("view") or {})
    v.setdefault("x", x)
    return RV._view({"view": v}, default)  # noqa: F821


def zl_strobe(c: SceneCtx, d: dict) -> SceneOut:
    """data: theta; arrow_at (velocity arrow appears); gap_at (fastest stretch on the ruler); zero_top_at,
    zero_bottom_at ("v = 0" at TDC and BDC); step; ticks_shown; notes; dial; source; view."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    track = RV.Track.from_data(c, d, (0.0, 720.0))  # noqa: F821
    view = _view_x(d, STROBE_VIEW, 420)
    eng, tl, ev = _engine(c, d, k, view, track)
    band, btl, bev = _band(c, d, k, track, [])
    inner = [eng]
    tl += btl
    ev += bev
    if d.get("arrow", True):
        asv, atl = _arrow(c, k, view, track, 618, 150)
        inner.append(asv)
        tl += atl
        t = RV.at_time(c, d, d.get("arrow_at", 0.0))  # noqa: F821
        tl.append(f'tl.fromTo("#{s}-zar",{{opacity:0}},{{opacity:1,duration:0.25}},{t:.3f});')
        ev.append(t)
    rsv, rtl, rev = _ruler(c, d, k, view, track, problems)
    inner.append(rsv)
    tl += rtl
    ev += rev
    nsv, ntl, nev = _notes(c, d, k, problems)
    inner.append(nsv)
    tl += ntl
    ev += nev
    if d.get("dial", True):
        dsv, dtl = _dial(c, d, k, track, 800, 1130)
        inner.append(dsv)
        tl += dtl
    inner += [band, _source(c, d, problems)]
    return _out(c, k, "".join(inner), tl, ev, problems)


# 3. cause: rod angle and the pure sine for comparison ----------------------------------------------------

def zl_cause(c: SceneCtx, d: dict) -> SceneOut:
    """data: theta; rod_at (rod highlighted); beta_at (rod angle beta at the piston pin); pins_at (piston pin and crank
    pin marked); sine_at (ghost piston on the pure sine path, second pointer and gap on the ruler); notes; ticks_shown;
    dial; source; view."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    track = RV.Track.from_data(c, d, (0.0, 360.0))  # noqa: F821
    view = _view_x(d, STROBE_VIEW, 420)
    eng, tl, ev = _engine(c, d, k, view, track)
    band, btl, bev = _band(c, d, k, track, [])
    tl += btl
    ev += bev
    smp = track.samples(3.0, extra=[0.0, 90.0, 180.0, 270.0])
    pin = lambda a: RV.pin_y(a)  # noqa: E731,F821
    cp = lambda a: RV.crank_pin(a)  # noqa: E731,F821
    # overlays in native coordinates (placed with the same view as the engine)
    nat = [f'<line id="{s}-zrod" x1="{CX}" y1="{RV.PIN_TDC:.1f}" x2="{CX}" y2="{CY - R}" stroke="{k["accent"]}" stroke-width="12" stroke-linecap="round" opacity="0"/>',  # noqa: F821
           f'<g id="{s}-zbeta" opacity="0"><line id="{s}-zax" x1="{CX}" y1="{RV.PIN_TDC:.1f}" x2="{CX}" y2="{RV.PIN_TDC + 170:.1f}" stroke="{AMBER}" stroke-width="4" stroke-dasharray="10 8"/>'  # noqa: F821
           f'<path id="{s}-zarc" d="" fill="none" stroke="{AMBER}" stroke-width="5"/>'
           f'<text id="{s}-zbl" class="zl-beta" x="0" y="0" text-anchor="middle">β</text></g>',
           f'<g id="{s}-zpins" opacity="0"><circle id="{s}-zpp" cx="{CX}" cy="{RV.PIN_TDC:.1f}" r="22" fill="none" stroke="{k["accent"]}" stroke-width="5"/>'  # noqa: F821
           f'<circle id="{s}-zcp" cx="{CX}" cy="{CY - R}" r="30" fill="none" stroke="{k["accent"]}" stroke-width="5"/></g>',
           f'<line id="{s}-zghost" x1="{RV.BORE_L + 8}" y1="{RV.CROWN_TDC:.1f}" x2="{RV.BORE_R - 8}" y2="{RV.CROWN_TDC:.1f}" stroke="{k["text"]}" stroke-width="4" stroke-dasharray="12 8" opacity="0"/>']  # noqa: F821
    tl += RV._kf(f"#{s}-zrod", smp, lambda a: f"{pin(a):.2f}", "y1")  # noqa: F821
    tl += RV._kf(f"#{s}-zrod", smp, lambda a: f"{cp(a)[0]:.2f}", "x2")  # noqa: F821
    tl += RV._kf(f"#{s}-zrod", smp, lambda a: f"{cp(a)[1]:.2f}", "y2")  # noqa: F821
    tl += RV._kf(f"#{s}-zax", smp, lambda a: f"{pin(a):.2f}", "y1")  # noqa: F821
    tl += RV._kf(f"#{s}-zax", smp, lambda a: f"{pin(a) + 170:.2f}", "y2")  # noqa: F821
    tl += RV._kf(f"#{s}-zpp", smp, lambda a: f"{pin(a):.2f}", "cy")  # noqa: F821
    tl += RV._kf(f"#{s}-zcp", smp, lambda a: f"{cp(a)[0]:.2f}", "cx")  # noqa: F821
    tl += RV._kf(f"#{s}-zcp", smp, lambda a: f"{cp(a)[1]:.2f}", "cy")  # noqa: F821

    def arc(a: float) -> str:
        py = pin(a)
        x2, y2 = cp(a)
        phi = math.atan2(x2 - CX, y2 - py)            # rod direction from the cylinder axis (downwards)
        rr = 110                                      # polyline with a fixed point count (see _dial.sector)
        return "M" + " L".join(f"{CX + rr * math.sin(phi * i / 12):.2f},{py + rr * math.cos(phi * i / 12):.2f}" for i in range(13))

    def beta_label(a: float) -> str:
        py = pin(a)
        x2, y2 = cp(a)
        phi = math.atan2(x2 - CX, y2 - py) / 2
        return f"translate({CX + 150 * math.sin(phi) + (26 if phi >= 0 else -26):.2f},{py + 150 * math.cos(phi) + 14:.2f})"
    tl += RV._kf(f"#{s}-zarc", smp, arc, "d")  # noqa: F821
    tl += RV._kf(f"#{s}-zbl", smp, beta_label, "transform")  # noqa: F821
    tl += RV._kf(f"#{s}-zghost", smp, lambda a: f"{RV.CROWN_TDC + 2 * R * frac_sine(a):.2f}", "y1")  # noqa: F821
    tl += RV._kf(f"#{s}-zghost", smp, lambda a: f"{RV.CROWN_TDC + 2 * R * frac_sine(a):.2f}", "y2")  # noqa: F821
    for key, sel in (("rod_at", "zrod"), ("beta_at", "zbeta"), ("pins_at", "zpins"), ("sine_at", "zghost")):
        if key in d:
            t = RV.at_time(c, d, d[key])  # noqa: F821
            target = 0.6 if sel == "zrod" else 1
            tl.append(f'tl.fromTo("#{s}-{sel}",{{opacity:0}},{{opacity:{target},duration:0.3}},{t:.3f});')
            ev.append(t)
    if "rod_off_at" in d:
        tl.append(f'tl.to("#{s}-zrod",{{opacity:0,duration:0.3}},{RV.at_time(c, d, d["rod_off_at"]):.3f});')  # noqa: F821
    inner = [eng, RV._place(view, "".join(nat))]  # noqa: F821
    rsv, rtl, rev = _ruler(c, d, k, view, track, problems, sine=True)
    inner.append(rsv)
    tl += rtl
    ev += rev
    if "sine_at" in d:
        t = RV.at_time(c, d, d["sine_at"])  # noqa: F821
        tl.append(f'tl.fromTo("#{s}-zsp,#{s}-zsg",{{opacity:0}},{{opacity:1,duration:0.3}},{t:.3f});')
    nsv, ntl, nev = _notes(c, d, k, problems)
    inner.append(nsv)
    tl += ntl
    ev += nev
    if d.get("dial", True):
        dsv, dtl = _dial(c, d, k, track, 800, 1130)
        inner.append(dsv)
        tl += dtl
    inner += [band, _source(c, d, problems)]
    return _out(c, k, "".join(inner), tl, ev, problems)


# 4. trace: the pen draws the curve with the crank ----------------------------------------------------------

PX0, PX1, PY0, PY1 = 196, 890, 890, 1170       # plot area of the measuring panel
YLIM = 1.2


def _px(a: float) -> float:
    return PX0 + (a % 360.0) / 360.0 * (PX1 - PX0)


def _pxa(a: float) -> float:
    """Same without wrapping (0..360 inclusive), for curves inside one revolution."""
    return PX0 + a / 360.0 * (PX1 - PX0)


def _py(v: float) -> float:
    return PY1 - (v + YLIM) / (2 * YLIM) * (PY1 - PY0)


def _series_path(fn, a0: float, a1: float, step: float = 2.0) -> tuple[str, list[float]]:
    """Path over crank angles a0..a1 (inside one revolution) and the cumulative length at every point."""
    n = max(1, int(math.ceil((a1 - a0) / step)))
    pts = [(_pxa(a0 + (a1 - a0) * i / n), _py(fn(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    cum = [0.0]
    for p, q in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), cum


def zl_trace(c: SceneCtx, d: dict) -> SceneOut:
    """data: theta; series [{kind: sine|real, mode: live|draw|show, at}]; marks [{x, label, at, color, row, side}];
    notes; arrow_at; source; view. `live` couples the pen to the crank: the curve grows with the crank angle over one
    revolution from the beat's first angle (wrapping at 360)."""
    k = _k(c)
    s = c.sid
    de = c.lang == "de"
    problems: list[str] = []
    track = RV.Track.from_data(c, d, (0.0, 360.0))  # noqa: F821
    view = _view_x(d, (0.5, 312.0), 330)
    eng, tl, ev = _engine(c, d, k, view, track)
    band, btl, bev = _band(c, d, k, track, [])
    tl += btl
    ev += bev
    ref = float(d.get("ref_rpm", REF_RPM))
    ms_rev = 60000.0 / ref
    g = [f'<rect x="{LEFT}" y="806" width="{RIGHT - LEFT}" height="486" rx="18" fill="{k["surface"]}" fill-opacity="0.9" stroke="{k["steel"]}" stroke-opacity="0.3" stroke-width="2"/>',
         f'<text class="zl-lab" x="{PX0 - 60}" y="852">{_e("Kolbentempo, abwärts +" if de else "Piston speed, down +")}</text>']
    for a in range(0, 361, 45):
        g.append(f'<line x1="{_px(a) if a < 360 else PX1:.1f}" y1="{PY0}" x2="{_px(a) if a < 360 else PX1:.1f}" y2="{PY1}" stroke="{k["hairline"]}" stroke-width="{2 if a % 90 == 0 else 1}"/>')
    for v in (-1.0, -0.5, 0.5, 1.0):
        g.append(f'<line x1="{PX0}" y1="{_py(v):.1f}" x2="{PX1}" y2="{_py(v):.1f}" stroke="{k["hairline"]}" stroke-width="1"/>')
    g.append(f'<line x1="{PX0}" y1="{_py(0):.1f}" x2="{PX1}" y2="{_py(0):.1f}" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="2"/>')
    g.append(f'<path d="M{PX0},{PY0 - 8} L{PX0},{PY1} L{PX1 + 6},{PY1}" fill="none" stroke="{k["steel"]}" stroke-width="3"/>')
    for a, lab in ((0, "OT" if de else "TDC"), (90, "90°"), (180, "UT" if de else "BDC"), (270, "270°"), (360, "OT" if de else "TDC")):
        x = _px(a) if a < 360 else PX1
        g.append(f'<text class="zl-tick" x="{x:.1f}" y="{PY1 + 38}" text-anchor="middle">{lab}</text>')
        v = ms_rev * a / 360.0
        g.append(f'<text class="zl-tick ms" x="{x:.1f}" y="{PY1 + 72}" text-anchor="middle">{_num(v, 0) if abs(v - round(v)) < 1e-6 else _num(v, 1)}{" ms" if a == 360 else ""}</text>')
    g.append(f'<text class="zl-tick ms" x="{PX0 - 60}" y="{PY1 + 72}" text-anchor="start">t</text>')
    fns = {"sine": vel_sine, "real": vel}
    colors = {"sine": k["steel"], "real": k["accent"]}
    legend = {"sine": "Sinus (90°)" if de else "Sine (90°)", "real": "Modell" if de else "Model"}
    a_start = track.angle(c.start)
    pen_fn = None
    for i, sr in enumerate(d.get("series", [])):
        kind = sr.get("kind", "real")
        fn = fns[kind]
        col = colors[kind]
        dash = kind == "sine"
        mode = sr.get("mode", "draw")
        width = 4 if dash else 7
        if mode == "live":
            pen_fn = fn
            m0 = a_start % 360.0
            pieces = [(m0, 360.0, a_start)] + ([(0.0, m0, a_start + (360.0 - m0))] if m0 > 0.5 else [])
            for j, (p, q, a_begin) in enumerate(pieces):
                path, cum = _series_path(fn, p, q)
                ln = cum[-1] + 1
                g.append(f'<path id="{s}-zs{i}_{j}" d="{path}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linejoin="round" '
                         f'stroke-linecap="round" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>')
                n = len(cum) - 1

                def off(a, a_begin=a_begin, p=p, q=q, cum=cum, ln=ln, n=n):
                    u = min(max((a - a_begin) / (q - p), 0.0), 1.0) * n
                    i0 = min(int(u), n - 1)
                    lv = cum[i0] + (cum[i0 + 1] - cum[i0]) * (u - i0)
                    return f"{ln - lv:.1f}"
                tl += RV._kf(f"#{s}-zs{i}_{j}", track.samples(2.0), off, "stroke-dashoffset")  # noqa: F821
            if dash:
                problems.append("revlore.zeitlupe: live mode draws a solid line; use draw/show for the dashed sine")
            t = c.start
        else:
            path, cum = _series_path(fn, 0.0, 360.0)
            ln = cum[-1] + 1
            if dash:
                g.append(f'<path id="{s}-zs{i}" d="{path}" fill="none" stroke="{col}" stroke-width="{width}" stroke-dasharray="14 10" opacity="0"/>')
            else:
                g.append(f'<path id="{s}-zs{i}" d="{path}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" '
                         f'stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>')
            t = RV.at_time(c, d, sr.get("at", 0.0)) if mode == "draw" else c.start  # noqa: F821
            if dash:
                if mode == "show":
                    tl.append(f'tl.set("#{s}-zs{i}",{{opacity:1}},{t:.3f});')
                else:      # dashed line drawn left to right with a moving clip
                    g.append(f'<clipPath id="{s}-zc{i}"><rect id="{s}-zcr{i}" x="{PX0 - 10}" y="{PY0 - 20}" width="0" height="{PY1 - PY0 + 40}"/></clipPath>')
                    g[-2] = g[-2].replace('opacity="0"/>', f'opacity="0" clip-path="url(#{s}-zc{i})"/>')
                    tl.append(f'tl.set("#{s}-zs{i}",{{opacity:1}},{t:.3f});')
                    tl.append(f'tl.to("#{s}-zcr{i}",{{attr:{{width:{PX1 - PX0 + 20}}},duration:1.4,ease:"power1.inOut"}},{t:.3f});')
            else:
                dur = 0.01 if mode == "show" else 1.4
                tl.append(f'tl.to("#{s}-zs{i}",{{attr:{{"stroke-dashoffset":0}},duration:{dur},ease:"power1.inOut"}},{t:.3f});')
        ev.append(t)
        ly = 420 + 56 * i
        dash_attr = ' stroke-dasharray="12 8"' if dash else ""
        g.append(f'<g id="{s}-zlg{i}" opacity="0"><line x1="600" y1="{ly}" x2="650" y2="{ly}" stroke="{col}" stroke-width="{width}"{dash_attr}/>'
                 f'<text class="zl-leg" x="666" y="{ly + 10}">{_e(legend[kind])}</text></g>')
        tl.append(_show(f"#{s}-zlg{i}", t, 0.3))
    cols = {"accent": k["accent"], "steel": k["steel"], "amber": AMBER, "text": k["text"]}
    for i, m in enumerate(d.get("marks", [])):
        x = _px(m["x"])
        col = cols.get(m.get("color", "accent"), k["accent"])
        _check(problems, f"mark {i}", m.get("label", ""), 18)
        side = m.get("side", "r")
        g.append(f'<g id="{s}-zm{i}" opacity="0"><line x1="{x:.1f}" y1="{PY0 - 4}" x2="{x:.1f}" y2="{PY1}" stroke="{col}" stroke-width="3" stroke-dasharray="8 6"/>'
                 f'<text class="zl-mark" x="{x + (10 if side == "r" else -10):.1f}" y="{(_py(m["y"]) + 10) if "y" in m else PY0 + 30 + 38 * m.get("row", 0):.1f}" text-anchor="{"start" if side == "r" else "end"}" fill="{col}">{_e(m.get("label", ""))}</text></g>')
        t = RV.at_time(c, d, m.get("at", 0.5))  # noqa: F821
        tl.append(_show(f"#{s}-zm{i}", t, 0.3))
        ev.append(t)
    for i, n in enumerate(d.get("curve_notes", [])):
        _check(problems, f"curve note {i}", n.get("text", ""), 22)
        x, y = _px(n["x"]), _py(n["y"])
        g.append(f'<text id="{s}-zq{i}" class="zl-note" x="{x:.1f}" y="{y:.1f}" text-anchor="{n.get("anchor", "start")}" fill="{cols.get(n.get("color", "text"), k["text"])}" opacity="0">{_e(n["text"])}</text>')
        t = RV.at_time(c, d, n.get("at", 0.5))  # noqa: F821
        tl.append(_show(f"#{s}-zq{i}", t, 0.3, 8))
        ev.append(t)
    # cursor and pen
    smp = track.samples(2.0, extra=[0.0, 359.9, 360.0, 719.9])
    g.append(f'<line id="{s}-zcur" x1="{_px(a_start):.1f}" y1="{PY0}" x2="{_px(a_start):.1f}" y2="{PY1}" stroke="{k["text"]}" stroke-opacity="0.55" stroke-width="2"/>')
    tl += RV._kf(f"#{s}-zcur", smp, lambda a: f"{_px(a):.1f}", "x1")  # noqa: F821
    tl += RV._kf(f"#{s}-zcur", smp, lambda a: f"{_px(a):.1f}", "x2")  # noqa: F821
    if pen_fn is not None:
        g.append(f'<circle id="{s}-zpen" cx="{_px(a_start):.1f}" cy="{_py(pen_fn(a_start)):.1f}" r="12" fill="{k["text"]}" stroke="{k["accent"]}" stroke-width="5"/>')
        tl += RV._kf(f"#{s}-zpen", smp, lambda a: f"{_px(a):.1f}", "cx")  # noqa: F821
        tl += RV._kf(f"#{s}-zpen", smp, lambda a: f"{_py(pen_fn(a)):.1f}", "cy")  # noqa: F821
    inner = [eng]
    if d.get("arrow", True):
        asv, atl = _arrow(c, k, view, track, 470, 110)
        inner.append(asv)
        tl += atl
        t = RV.at_time(c, d, d.get("arrow_at", 0.0))  # noqa: F821
        tl.append(f'tl.fromTo("#{s}-zar",{{opacity:0}},{{opacity:1,duration:0.25}},{t:.3f});')
    inner.append("".join(g))
    nsv, ntl, nev = _notes(c, d, k, problems)
    inner.append(nsv)
    tl += ntl
    ev += nev
    if d.get("dial", True):
        dsv, dtl = _dial(c, d, k, track, 800, 640, 62)
        inner.append(dsv)
        tl += dtl
    inner += [band, _source(c, d, problems, 790)]
    return _out(c, k, "".join(inner), tl, ev, problems)


# 5. back to real time ---------------------------------------------------------------------------------

def zl_realtime(c: SceneCtx, d: dict) -> SceneOut:
    """data: theta (speeding up); real_at (from here the long exposure, band ECHTZEIT); rows [{text, hl, at}];
    brand {text, hl, at}; dial; source; view."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    track = RV.Track.from_data(c, d, (0.0, 720.0))  # noqa: F821
    view = RV._view(d, (0.62, 612.0))  # noqa: F821
    eng, tl, ev = _engine(c, d, k, view, track)
    t_real = RV.at_time(c, d, d["real_at"]) if "real_at" in d else None  # noqa: F821
    real = [(t_real, c.end)] if t_real is not None else []
    if t_real is not None:
        tl += _realtime(s, [(t_real, None)])
        ev.append(t_real)
    band, btl, bev = _band(c, d, k, track, real)
    tl += btl
    ev += bev
    inner = [eng]
    for i, r in enumerate(d.get("rows", [])):
        txt = r.get("text", "")
        _check(problems, f"row {i}", txt, 36)
        hl = r.get("hl", "")
        body = _e(txt).replace(_e(hl), f'<tspan class="hl">{_e(hl)}</tspan>') if hl and hl in txt else _e(txt)
        inner.append(f'<text id="{s}-zr{i}" class="zl-row" x="{LEFT}" y="{372 + 66 * i}" opacity="0">{body}</text>')
        t = RV.at_time(c, d, r.get("at", 0.2 + 0.15 * i))  # noqa: F821
        tl.append(_show(f"#{s}-zr{i}", t, 0.3, 10))
        ev.append(t)
    if d.get("brand"):
        b = d["brand"]
        _check(problems, "brand", b.get("text", ""), 40)
        hl = b.get("hl", "")
        body = _e(b["text"]).replace(_e(hl), f'<tspan class="acc">{_e(hl)}</tspan>') if hl else _e(b["text"])
        inner.append(f'<text id="{s}-zbr" class="zl-brand" x="540" y="1225" text-anchor="middle" opacity="0">{body}</text>')
        t = RV.at_time(c, d, b.get("at", 0.8))  # noqa: F821
        tl.append(_show(f"#{s}-zbr", t, 0.35, 10))
        ev.append(t)
    if d.get("dial", False):
        dsv, dtl = _dial(c, d, k, track, 800, 1130)
        inner.append(dsv)
        tl += dtl
    inner += [band, _source(c, d, problems)]
    return _out(c, k, "".join(inner), tl, ev, problems)


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:
    k = {"text": pal.get("text", "#E7ECF1"), "muted": pal.get("muted", "#8D99A6"), "accent": pal.get("accent", "#2F9BFF"),
         "steel": pal.get("steel", "#AEB9C5")}
    return f"""
.zl .zl-mode{{font-family:'FN {display}';font-weight:600;font-size:48px;fill:{k['text']};letter-spacing:0.08em;}}
.zl .zl-mode.real{{fill:{AMBER};}}
.zl .zl-fac{{fill:{k['accent']};letter-spacing:0.02em;}}
.zl .zl-ref{{font-family:'FN {mono}';font-size:26px;fill:{k['muted']};}}
.zl .zl-claim{{font-family:'FN {display}';font-weight:600;font-size:80px;fill:{k['text']};}}
.zl .zl-claim .hl{{fill:{k['accent']};}}
.zl .zl-lab{{font-family:'FN {mono}';font-size:30px;fill:{k['steel']};}}
.zl .zl-lab.acc{{fill:{k['accent']};}}
.zl .zl-note{{font-family:'FN {mono}';font-size:30px;}}
.zl .zl-src{{font-family:'FN {mono}';font-size:26px;fill:{k['muted']};}}
.zl .zl-dial{{font-family:'FN {mono}';font-size:28px;fill:{k['steel']};}}
.zl .zl-dial-s{{font-family:'FN {mono}';font-size:28px;fill:{k['muted']};}}
.zl .zl-beta{{font-family:'FN {display}';font-weight:600;font-size:56px;fill:{AMBER};}}
.zl .zl-tick{{font-family:'FN {mono}';font-size:30px;fill:{k['steel']};}}
.zl .zl-tick.ms{{fill:{k['muted']};}}
.zl .zl-leg{{font-family:'FN {mono}';font-size:30px;fill:{k['text']};}}
.zl .zl-mark{{font-family:'FN {display}';font-weight:600;font-size:34px;}}
.zl .zl-row{{font-family:'FN {display}';font-weight:500;font-size:48px;fill:{k['text']};}}
.zl .zl-row .hl{{fill:{k['accent']};}}
.zl .zl-brand{{font-family:'FN {display}';font-weight:600;font-size:46px;fill:{k['text']};letter-spacing:0.03em;}}
.zl .zl-brand .acc{{fill:{k['accent']};}}
.scene-inner.rv.zlp{{background-color:transparent;}}
.zl .zt-lab{{font-family:'FN {mono}';font-size:30px;fill:{k['text']};}}
.zl .zt-ax{{font-family:'FN {mono}';font-size:26px;fill:{k['muted']};}}
.zl .zt-pt{{font-family:'FN {display}';font-weight:600;font-size:30px;fill:{k['text']};}}
.zl .zt-cur{{font-family:'FN {display}';font-weight:600;font-size:64px;fill:{k['text']};}}
.zl .zt-cur .hl{{fill:{AMBER};}}
.zl .zt-row{{font-family:'FN {display}';font-weight:500;font-size:36px;fill:{k['text']};}}
.zl .zt-row .hl{{fill:{k['accent']};}}
.zl .zt-lim{{font-family:'FN {display}';font-weight:600;font-size:40px;fill:{k['accent']};}}
.zl .zt-note{{font-family:'FN {mono}';font-size:28px;fill:{k['steel']};}}
"""


# 6. adapted Q1 scenes (zlx_*): week-1 plans keep their paid voices --------------------------------------------
# Their spoken text was written for the Q1 scenes (cutaway, chart, readout, board, plug). The adapter runs the Q1
# template inside the Zeitlupe frame: measuring-room ground instead of the drafting room, no push-in, no scene title,
# no cycle strip (unless the beat sets `zl_strip`, e.g. when the voice mentions the strip), labels as plain mono text
# with a leader line instead of cards, plus the slow-motion band and the source line.

def _zl_backdrop(c: SceneCtx, k: dict) -> tuple[str, list[str]]:
    return _ground(c.sid, k), []


def _zl_card(gid: str, k: dict, text: str, side: str, y: float, ax: float | None = None, ay: float | None = None,
             color: str | None = None) -> str:
    """Label as plain text with a leader line (no card): mono 30 at the left (x 120) or right (x 918) edge."""
    color = color or k["accent"]
    w = len(text) * 18
    x0 = RV.LEFT if side == "l" else RV.RIGHT - w  # noqa: F821
    ex = x0 + w + 10 if side == "l" else x0 - 10
    lead = ""
    if ax is not None:
        stub = ex + (22 if side == "l" else -22)
        lead = (f'<polyline points="{ex:.0f},{y:.0f} {stub:.0f},{y:.0f} {ax:.0f},{ay:.0f}" fill="none" stroke="{color}" stroke-opacity="0.8" stroke-width="2.5"/>'
                f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="8" fill="{color}" stroke="{k["bg"]}" stroke-width="3"/>')
    return (f'<g id="{gid}" opacity="0">{lead}<line x1="{x0:.0f}" y1="{y + 20:.0f}" x2="{x0 + w:.0f}" y2="{y + 20:.0f}" stroke="{color}" stroke-width="3"/>'
            f'<text class="lbl" x="{x0:.0f}" y="{y + 10:.0f}">{_e(text)}</text></g>')


_PATCH = {"_backdrop": _zl_backdrop, "_push": lambda c: "", "_card": _zl_card,
          "strip_svg": lambda *a, **kw: "", "strip_anim": lambda *a, **kw: ([], []), "strip_count": lambda *a, **kw: []}
_STRIP_KEYS = ("strip_svg", "strip_anim", "strip_count")


def _adapt(name: str):
    orig = RV.TEMPLATES[name]  # noqa: F821

    def scene(c: SceneCtx, d: dict) -> SceneOut:
        d2 = {kk: v for kk, v in d.items() if kk not in ("title", "source", "zl_strip")}
        G = orig.__globals__
        patch = {kk: v for kk, v in _PATCH.items() if not (d.get("zl_strip") and kk in _STRIP_KEYS)}
        if d.get("zl_strip"):
            d2["strip"] = True
            patch["STRIP_Y"] = 1180     # above the source line and the AI label (renderer change 03.11.: label >= 430 px from the bottom)
        saved = {kk: G[kk] for kk in patch}
        G.update(patch)
        try:
            out = orig(c, d2)
        finally:
            G.update(saved)
        k = _k(c)
        problems: list[str] = []
        track = RV.Track.from_data(c, d2, (0.0, 360.0))  # noqa: F821
        moving = name in ("rv_cutaway", "rv_exploded", "rv_drive") or (name == "rv_chart" and d.get("engine"))
        band, btl, bev = _band(c, d, k, track, []) if moving else ("", [], [])   # no band where nothing turns
        extra = band + _source(c, d, problems)
        i = out.html.rfind("</svg>")
        html_ = out.html[:i].replace('class="scene-inner rv"', 'class="scene-inner rv zl"', 1) + extra + out.html[i:]
        evs = sorted(set(list(out.events) + [round(e, 3) for e in bev]))
        return SceneOut(html=html_, tl=list(out.tl) + btl, events=evs, problems=list(out.problems) + problems)
    scene.__name__ = f"zlx_{name[3:]}"
    return scene


_ADAPTED = {f"zlx_{n[3:]}": _adapt(n) for n in ("rv_cutaway", "rv_chart", "rv_readout", "rv_board", "rv_plug", "rv_exploded", "rv_drive")}


# 7. Technik-Kanal (Neustart 03.11.2026): photo scenes and the miniature circuit breaker ---------------------------
# Testvideo "Zwei Auslöser in einem Sicherungsautomaten". Photos and clips come from the plan's asset layer (one hero
# clip per beat, brands/engines/assets/higgsfield/library); a scene with `photo` leaves the ground transparent so the
# clip shows, `ground_at` covers it later with the measuring room. The breaker is a simplified model after
# DE3625425A1 (BBC 1986): thermobimetal, electromagnetic release with plunger, latch, contacts, arc into the stack of
# extinguishing plates. Times on screen are norm limits (Siemens SENTRON table: 1.45 x In < 1 h; B from 5 x In
# < 0.1 s), never invented event times; the band therefore reads "bis n:1" (time-lapse) and "mind. 1:n" (slow motion).

COPPER = "#C58B4E"
BRASS = "#C9A44C"


def _tout(c: SceneCtx, k: dict, inner: str, tl: list[str], ev: list[float], problems: list[str], *,
          photo: bool = False, ground_at: float | None = None) -> SceneOut:
    s = c.sid
    shade = (f'<defs><linearGradient id="{s}-ztop" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#06080B" stop-opacity="0.78"/><stop offset="0.22" stop-color="#06080B" stop-opacity="0"/>'
             f'<stop offset="0.55" stop-color="#06080B" stop-opacity="0"/><stop offset="0.8" stop-color="#06080B" stop-opacity="0.82"/>'
             f'<stop offset="1" stop-color="#06080B" stop-opacity="0.82"/></linearGradient></defs>'
             f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-ztop)"/>')
    if not photo:
        ground = _ground(s, k)
    elif ground_at is None:
        ground = shade
    else:
        ground = shade + f'<g id="{s}-zgr" opacity="0">{_ground(s, k)}</g>'
        tl = [f'tl.to("#{s}-zgr",{{opacity:1,duration:0.45,ease:"power1.inOut"}},{ground_at:.3f});'] + tl
        ev = ev + [ground_at]
    cls = "scene-inner rv zl zlp" if photo else "scene-inner rv zl"
    html_ = (f'<div class="{cls}"><svg class="rv-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
             f'{RV._defs(s, k)}{ground}{inner}</svg></div>')  # noqa: F821
    evs = sorted(set(round(e, 3) for e in ev if c.start - 1e-3 <= e <= c.end + 1e-3))
    return SceneOut(html=html_, tl=tl, events=evs, problems=problems)


def _t(c: SceneCtx, d: dict, at, default: float = 0.5) -> float:
    return RV.at_time(c, d, at if at is not None else default)  # noqa: F821


def _tband(c: SceneCtx, k: dict, items: list[tuple[float, str, str]], ref: str = "") -> tuple[str, list[str], list[float]]:
    """Time band for the technology scenes: items [(t0, mode, factor text)], mode real | slow | fast | stand;
    each label holds until the next item."""
    s = c.sid
    de = c.lang == "de"
    names = {"real": "ECHTZEIT" if de else "REAL TIME", "slow": "ZEITLUPE" if de else "SLOW MOTION",
             "fast": "ZEITRAFFER" if de else "TIME-LAPSE", "stand": "STANDBILD" if de else "FREEZE"}
    svg = [f'<line x1="{LEFT}" y1="292" x2="{RIGHT}" y2="292" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="2"/>']
    if ref:
        svg.append(f'<text class="zl-ref" x="{RIGHT}" y="{BAND_Y}" text-anchor="end">{_e(ref)}</text>')
    tl, ev = [], []
    items = sorted(items)
    for i, (t0, mode, fac) in enumerate(items):
        fac_html = f'<tspan class="zl-fac" dx="16">{_e(fac)}</tspan>' if fac else ""
        svg.append(f'<text id="{s}-tb{i}" class="zl-mode{" real" if mode == "real" else ""}" x="{LEFT}" y="{BAND_Y}" opacity="0">'
                   f'{_e(names[mode])}{fac_html}</text>')
        tl.append(f'tl.set("#{s}-tb{i}",{{opacity:1}},{max(t0, c.start):.3f});')
        if i + 1 < len(items):
            tl.append(f'tl.set("#{s}-tb{i}",{{opacity:0}},{items[i + 1][0]:.3f});')
            ev.append(items[i + 1][0])
    return "".join(svg), tl, ev


def _fac(model_s: float, video_s: float, fast: bool, de: bool) -> str:
    """Factor text from a norm limit: time-lapse "bis n:1" (the real process takes at most model_s), slow motion
    "mind. 1:n" (the real process is over within model_s). n is rounded down."""
    n = (model_s / video_s) if fast else (video_s / model_s)
    n = int(n // 10 * 10) if n >= 100 else int(n)
    if fast:
        return ("bis %d:1" if de else "up to %d:1") % n
    return ("mind. 1:%d" if de else "at least 1:%d") % n


def _tlabel(gid: str, k: dict, text: str, x: float, y: float, anchor: str = "start",
            ax: float | None = None, ay: float | None = None, cls: str = "zt-lab") -> str:
    """Label on a dark plate (mono 30), optional leader line with a dot at (ax, ay)."""
    w = len(text) * 18 + 20
    x0 = x if anchor == "start" else x - w
    lead = ""
    if ax is not None:
        sx = x0 if ax < x0 else x0 + w
        lead = (f'<line x1="{sx:.0f}" y1="{y - 10:.0f}" x2="{ax:.0f}" y2="{ay:.0f}" stroke="{k["accent"]}" stroke-width="2.5"/>'
                f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="7" fill="{k["accent"]}" stroke="{k["bg"]}" stroke-width="3"/>')
    return (f'<g id="{gid}" opacity="0">{lead}<rect x="{x0:.0f}" y="{y - 32:.0f}" width="{w:.0f}" height="44" rx="6" '
            f'fill="{k["bg"]}" fill-opacity="0.88"/><text class="{cls}" x="{x0 + 10:.0f}" y="{y:.0f}">{_e(text)}</text></g>')


def _hltext(text: str, hl: str, cls: str = "hl") -> str:
    return _e(text).replace(_e(hl), f'<tspan class="{cls}">{_e(hl)}</tspan>') if hl and hl in text else _e(text)


# --- the breaker model (local coordinates 0..500 x 0..700, lever on the front at the right) ---------------------

MCB_PARTS = {   # part: (anchor in local coords, label position in local coords, anchor side, DE, EN)
    "bimetal": ((404, 320), (390, 190), "end", "Bimetall", "bimetal"),
    "coil": ((232, 300), (252, 302), "start", "Spule", "coil"),
    "latch": ((340, 452), (250, 606), "start", "Schaltschloss", "latch"),
    "contact": ((126, 452), (20, 404), "start", "Kontakt", "contact"),
    "chute": ((70, 650), (20, 742), "start", "Löschbleche", "arc plates"),
}
BM_REST = ("M400,220 Q400,320 400,420", "M407,220 Q407,320 407,420")
BM_BENT = ("M400,220 Q396,322 362,412", "M407,220 Q403,322 369,413")


def _mcb_svg(s: str, k: dict) -> str:
    st, mu = k["steel"], k["muted"]
    o = [f'<rect x="-18" y="300" width="20" height="80" fill="{k["steel_dark"]}"/>',
         f'<rect x="0" y="0" width="500" height="700" rx="24" fill="{k["surface"]}" fill-opacity="0.96" stroke="{st}" stroke-width="3"/>']
    for y0 in (20, 620):   # terminals with screws
        o.append(f'<rect x="170" y="{y0}" width="120" height="60" rx="6" fill="#2A323C" stroke="{st}" stroke-width="2"/>'
                 f'<circle cx="230" cy="{y0 + 30}" r="18" fill="url(#{s}-gsteel)"/><line x1="218" y1="{y0 + 30}" x2="242" y2="{y0 + 30}" stroke="#2A323C" stroke-width="4"/>')
    wires = ["M230,80 L230,150 L200,150 L200,230", "M170,360 L120,360 L120,440", "M400,220 L440,220 L440,560 L230,560 L230,620"]
    for w in wires:
        o.append(f'<path d="{w}" fill="none" stroke="{COPPER}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<g id="{s}-wh" opacity="0">' + "".join(f'<path d="{w}" fill="none" stroke="{AMBER}" stroke-width="11" stroke-linejoin="round"/>' for w in wires) + '</g>')
    o.append(f'<path d="M260,500 C330,545 395,480 402,424" fill="none" stroke="{COPPER}" stroke-width="5" stroke-dasharray="3 5"/>')
    # coil with plunger, field lines
    o.append(f'<g id="{s}-fld" opacity="0"><ellipse cx="200" cy="300" rx="70" ry="104" fill="none" stroke="{k["accent"]}" stroke-width="2.5" stroke-dasharray="8 8"/>'
             f'<ellipse cx="200" cy="300" rx="100" ry="140" fill="none" stroke="{k["accent"]}" stroke-width="2" stroke-dasharray="8 10" stroke-opacity="0.6"/></g>')
    o.append(f'<rect x="168" y="230" width="64" height="140" rx="6" fill="#2A323C" stroke="{st}" stroke-width="2"/>')
    turns = "".join(f'<path d="M168,{y} Q200,{y + 7} 232,{y}" fill="none" stroke="{COPPER}" stroke-width="4"/>' for y in range(240, 366, 11))
    turns_hot = "".join(f'<path d="M168,{y} Q200,{y + 7} 232,{y}" fill="none" stroke="{AMBER}" stroke-width="5"/>' for y in range(240, 366, 11))
    o.append(turns + f'<g id="{s}-coh" opacity="0">{turns_hot}</g>')
    o.append(f'<g id="{s}-plg" transform="translate(0 0)"><rect x="194" y="250" width="12" height="180" rx="3" fill="url(#{s}-gsteel)"/></g>')
    # fixed contact, runner, plate stack
    o.append(f'<rect x="14" y="512" width="112" height="138" rx="6" fill="none" stroke="{mu}" stroke-width="2"/>')
    o.append("".join(f'<line x1="22" y1="{520 + 15 * i}" x2="118" y2="{520 + 15 * i}" stroke="{st}" stroke-width="4"/>' for i in range(9)))
    o.append(f'<path d="M120,458 L112,516" stroke="{st}" stroke-width="5"/><rect x="110" y="440" width="20" height="18" fill="{st}"/>')
    # moving contact arm (pivot 260,500)
    o.append(f'<g id="{s}-arm" transform="rotate(0 260 500)"><line x1="260" y1="500" x2="134" y2="452" stroke="{st}" stroke-width="10" stroke-linecap="round"/>'
             f'<rect x="124" y="444" width="14" height="16" fill="{COPPER}"/><circle cx="260" cy="500" r="10" fill="{st}"/></g>')
    # arcs: at the contact gap, then inside the plate stack
    o.append(f'<path id="{s}-arc1" d="M126,452 L118,470 L132,486 L120,500 L134,514" fill="none" stroke="{AMBER}" stroke-width="5" opacity="0"/>')
    o.append(f'<g id="{s}-arc2" opacity="0">' + "".join(
        f'<path d="M{40 + 9 * (i % 3)},{522 + 15 * i} L{58 + 6 * (i % 2)},{528 + 15 * i} L{48},{535 + 15 * i}" fill="none" stroke="{AMBER}" stroke-width="4"/>'
        for i in range(8)) + '</g>')
    # bimetal (two layers), hot overlay, trip bar, latch, link to the lever
    o.append(f'<path id="{s}-bm1" d="{BM_REST[0]}" fill="none" stroke="{BRASS}" stroke-width="7"/>'
             f'<path id="{s}-bm2" d="{BM_REST[1]}" fill="none" stroke="{st}" stroke-width="7"/>'
             f'<path id="{s}-bmh" d="{BM_REST[0]}" fill="none" stroke="{AMBER}" stroke-width="9" opacity="0"/>')
    o.append(f'<g id="{s}-trp" transform="translate(0 0)"><rect x="300" y="432" width="92" height="14" rx="4" fill="{k["steel_dark"]}" stroke="{st}" stroke-width="2"/></g>')
    o.append(f'<line x1="480" y1="252" x2="352" y2="444" stroke="{mu}" stroke-width="4" stroke-dasharray="10 8"/>')
    o.append(f'<g id="{s}-lat" transform="rotate(0 330 452)"><rect x="330" y="446" width="44" height="14" rx="4" fill="{st}"/></g><circle cx="330" cy="452" r="8" fill="{st}"/>')
    # lever on the front (pivot 500,240), ON = up
    o.append(f'<g id="{s}-lev" transform="rotate(-28 500 240)"><rect x="496" y="226" width="78" height="28" rx="8" fill="{k["steel_dark"]}" stroke="{st}" stroke-width="2"/></g>'
             f'<circle cx="500" cy="240" r="12" fill="{st}"/>')
    return "".join(o)


def _mcb(s: str, k: dict, tx: float, ty: float, sc: float) -> str:
    return f'<g transform="translate({tx} {ty}) scale({sc})">{_mcb_svg(s, k)}</g>'


def _trip_tl(s: str, t: float, arm: float = -22.0) -> list[str]:
    """Latch releases, lever drops to OFF, contacts open (local rotations, so the group transform stays valid)."""
    return [f'tl.to("#{s}-trp",{{attr:{{transform:"translate(-24 0)"}},duration:0.12,ease:"power2.in"}},{t:.3f});',
            f'tl.to("#{s}-lat",{{attr:{{transform:"rotate(-35 330 452)"}},duration:0.15,ease:"power2.in"}},{t + 0.08:.3f});',
            f'tl.to("#{s}-arm",{{attr:{{transform:"rotate({arm} 260 500)"}},duration:0.25,ease:"power3.out"}},{t + 0.1:.3f});',
            f'tl.to("#{s}-lev",{{attr:{{transform:"rotate(28 500 240)"}},duration:0.25,ease:"back.out(2)"}},{t + 0.15:.3f});']


def _labels(c: SceneCtx, d: dict, k: dict, tx: float, ty: float, sc: float) -> tuple[str, list[str], list[float]]:
    out, tl, ev = [], [], []
    for i, lb in enumerate(d.get("labels", [])):
        (ax, ay), (lx, ly), side, de_t, en_t = MCB_PARTS[lb["part"]]
        text = lb.get("text") or (de_t if c.lang == "de" else en_t)
        out.append(_tlabel(f"{c.sid}-tl{i}", k, text, tx + sc * lx, ty + sc * ly, side, tx + sc * ax, ty + sc * ay))
        t = _t(c, d, lb.get("at"), 0.3 + 0.1 * i)
        tl.append(_show(f"#{c.sid}-tl{i}", t, 0.3, 8))
        ev.append(t)
    return "".join(out), tl, ev


def _rows(c: SceneCtx, d: dict, k: dict, problems: list[str], y0: float = 1180, dy: float = 56) -> tuple[str, list[str], list[float]]:
    out, tl, ev = [], [], []
    for i, r in enumerate(d.get("rows", [])):
        txt = r.get("text", "")
        _check(problems, f"row {i}", txt, 40)
        out.append(f'<text id="{c.sid}-tr{i}" class="zt-row" x="{LEFT}" y="{y0 + dy * i}" opacity="0">{_hltext(txt, r.get("hl", ""))}</text>')
        t = _t(c, d, r.get("at"), 0.5 + 0.15 * i)
        tl.append(_show(f"#{c.sid}-tr{i}", t, 0.3, 8))
        ev.append(t)
    return "".join(out), tl, ev


def _current(c: SceneCtx, d: dict, problems: list[str]) -> tuple[str, list[str], list[float]]:
    cur = d.get("current")
    if not cur:
        return "", [], []
    _check(problems, "current", cur["text"], 24)
    t = _t(c, d, cur.get("at"), 0.1)
    return (f'<text id="{c.sid}-cur" class="zt-cur" x="{LEFT}" y="392" opacity="0">{_hltext(cur["text"], cur.get("hl", ""))}</text>',
            [_show(f"#{c.sid}-cur", t, 0.3, 10)], [t])


def zt_photo(c: SceneCtx, d: dict) -> SceneOut:
    """Photo or clip (plan asset, hero of this beat) with band ECHTZEIT. data: claim_lines, claim_highlight, claim_at;
    brand {text, hl, at}; note {text, at} (safety line); source."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    inner, tl, ev = [], [], []
    for i, line in enumerate(d.get("claim_lines", [])):
        _check(problems, f"claim line {i}", line, 22)
        inner.append(f'<text id="{s}-pc{i}" class="zl-claim" x="{LEFT}" y="{410 + 92 * i}" opacity="0">{_hltext(line, d.get("claim_highlight", ""))}</text>')
        t = _t(c, d, d.get("claim_at"), 0.05) + 0.25 * i
        tl.append(_show(f"#{s}-pc{i}", t, 0.35, 12))
        ev.append(t)
    if d.get("brand"):
        b = d["brand"]
        _check(problems, "brand", b.get("text", ""), 40)
        inner.append(f'<text id="{s}-pbr" class="zl-brand" x="540" y="1170" text-anchor="middle" opacity="0">{_hltext(b["text"], b.get("hl", ""), "acc")}</text>')
        t = _t(c, d, b.get("at"), 0.6)
        tl.append(_show(f"#{s}-pbr", t, 0.35, 10))
        ev.append(t)
    if d.get("note"):
        n = d["note"]
        _check(problems, "note", n.get("text", ""), 52)
        inner.append(f'<text id="{s}-pnt" class="zt-note" x="540" y="1226" text-anchor="middle" opacity="0">{_e(n["text"])}</text>')
        t = _t(c, d, n.get("at"), 0.7)
        tl.append(_show(f"#{s}-pnt", t, 0.35, 6))
        ev.append(t)
    band, btl, bev = _tband(c, k, [(c.start, "real", "")])
    inner += [band, _source(c, d, problems)]
    return _tout(c, k, "".join(inner), tl + btl, ev + bev, problems, photo=True)


XRAY = (230.0, 420.0, 1.12)      # model placement in the x-ray scene: translate x, y, scale
SIDE = (120.0, 440.0, 0.98)      # in the time-lapse and slow-motion scenes (right column stays free)


def zt_mcb(c: SceneCtx, d: dict) -> SceneOut:
    """The breaker model. data.mode:
    - "xray": over the photo of the breaker a scan line runs down (scan_at, scan_s) and uncovers the model; labels
      [{part, at}] name the parts (bimetal, coil, latch, contact, chute).
    - "thermal": optional photo insert until ground_at; the bimetal warms and bends between heat_from and trip_at
      (time-lapse up to the norm limit `model_s`, default 3600 s), clock and bend meter in the right column, then the
      latch releases. current {text, hl, at}; rows [{text, hl, at}].
    - "magnetic": current jumps at jump_at (wires and coil glow, field), the plunger strikes at strike_at, contacts
      open, the arc runs into the plates and is gone at quench_at (slow motion against the norm limit `model_s`,
      default 0.1 s); `limit` {text, at} in the right column.
    source on all."""
    k = _k(c)
    s = c.sid
    de = c.lang == "de"
    mode = d.get("mode", "xray")
    problems: list[str] = []
    tl: list[str] = []
    ev: list[float] = []
    inner: list[str] = []
    photo, ground_at = False, None
    if mode == "xray":
        tx, ty, sc = XRAY
        t0 = _t(c, d, d.get("scan_at"), 0.12)
        dur = float(d.get("scan_s", 2.2))
        photo = True
        inner.append(f'<defs><clipPath id="{s}-xc"><rect id="{s}-xr" x="0" y="380" width="1080" height="0"/></clipPath></defs>'
                     f'<g clip-path="url(#{s}-xc)"><rect x="0" y="380" width="1080" height="880" fill="{k["bg"]}" fill-opacity="0.84"/>'
                     f'{_mcb(s, k, tx, ty, sc)}</g>'
                     f'<g id="{s}-xl" opacity="0"><rect x="0" y="372" width="1080" height="16" fill="{k["accent"]}" fill-opacity="0.25"/>'
                     f'<line x1="0" y1="380" x2="1080" y2="380" stroke="{k["accent"]}" stroke-width="4"/></g>')
        tl += [f'tl.set("#{s}-xl",{{opacity:1}},{t0:.3f});',
               f'tl.to("#{s}-xr",{{attr:{{height:880}},duration:{dur:.2f},ease:"none"}},{t0:.3f});',
               f'tl.to("#{s}-xl",{{y:880,duration:{dur:.2f},ease:"none"}},{t0:.3f});',
               f'tl.to("#{s}-xl",{{opacity:0,duration:0.3}},{t0 + dur:.3f});']
        ev += [t0, t0 + dur]
        lab, ltl, lev = _labels(c, d, k, tx, ty, sc)
        inner.append(lab)
        tl += ltl
        ev += lev
        band, btl, bev = _tband(c, k, [(c.start, "real", ""), (t0 + dur, "stand", "")])
    else:
        tx, ty, sc = SIDE
        if d.get("photo"):
            photo, ground_at = True, _t(c, d, d.get("ground_at"), 0.15)
        inner.append(_mcb(s, k, tx, ty, sc))
        cur, ctl, cev = _current(c, d, problems)
        rows, rtl, rev = _rows(c, d, k, problems)
        inner += [cur, rows]
        tl += ctl + rtl
        ev += cev + rev
        cx, cy = 820.0, 600.0
        if mode == "thermal":
            h0 = _t(c, d, d.get("heat_from"), 0.2)
            h1 = _t(c, d, d.get("trip_at"), 0.85)
            model_s = float(d.get("model_s", 3600))
            for pid, bent in ((f"{s}-bm1", BM_BENT[0]), (f"{s}-bm2", BM_BENT[1]), (f"{s}-bmh", BM_BENT[0])):
                tl.append(f'tl.to("#{pid}",{{attr:{{d:"{bent}"}},duration:{h1 - h0:.3f},ease:"power1.in"}},{h0:.3f});')
            tl.append(f'tl.to("#{s}-bmh",{{opacity:0.85,duration:{h1 - h0:.3f},ease:"power1.in"}},{h0:.3f});')
            # clock (one turn = the norm limit) and bend meter
            inner.append(f'<circle cx="{cx}" cy="{cy}" r="76" fill="{k["surface"]}" fill-opacity="0.9" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="2"/>'
                         + "".join(f'<line x1="{cx + 62 * math.sin(math.radians(a)):.1f}" y1="{cy - 62 * math.cos(math.radians(a)):.1f}" '
                                   f'x2="{cx + 76 * math.sin(math.radians(a)):.1f}" y2="{cy - 76 * math.cos(math.radians(a)):.1f}" stroke="{k["steel"]}" stroke-width="2"/>'
                                   for a in range(0, 360, 30))
                         + f'<g id="{s}-clk" transform="rotate(0 {cx} {cy})"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 64}" stroke="{AMBER}" stroke-width="5" stroke-linecap="round"/></g>'
                         f'<circle cx="{cx}" cy="{cy}" r="7" fill="{AMBER}"/>'
                         f'<text class="zt-ax" x="{cx}" y="{cy - 92}" text-anchor="middle">{_e(d.get("clock_label", "1 h" if de else "1 h"))}</text>'
                         f'<rect x="800" y="740" width="40" height="280" rx="6" fill="none" stroke="{k["steel"]}" stroke-width="2"/>'
                         f'<rect id="{s}-mtr" x="804" y="1016" width="32" height="0" fill="{AMBER}"/>'
                         f'<line x1="784" y1="744" x2="856" y2="744" stroke="{k["accent"]}" stroke-width="4"/>'
                         f'<text class="zt-ax" x="{cx}" y="1066" text-anchor="middle">{_e("Biegung" if de else "bend")}</text>')
            tl += [f'tl.to("#{s}-clk",{{attr:{{transform:"rotate(359 {cx} {cy})"}},duration:{h1 - h0:.3f},ease:"none"}},{h0:.3f});',
                   f'tl.to("#{s}-mtr",{{attr:{{height:272,y:744}},duration:{h1 - h0:.3f},ease:"power1.in"}},{h0:.3f});']
            tl += _trip_tl(s, h1, -10.0)
            tl += [f'tl.to("#{s}-arc1",{{opacity:1,duration:0.05}},{h1 + 0.15:.3f});', f'tl.to("#{s}-arc1",{{opacity:0,duration:0.2}},{h1 + 0.4:.3f});']
            ev += [h0, h1]
            band, btl, bev = _tband(c, k, [(c.start, "real", ""), (h0, "fast", _fac(model_s, h1 - h0, True, de)), (h1 + 0.2, "real", "")],
                                    d.get("band_ref", ""))
        else:
            j = _t(c, d, d.get("jump_at"), 0.15)
            st_ = _t(c, d, d.get("strike_at"), 0.45)
            q = _t(c, d, d.get("quench_at"), 0.85)
            model_s = float(d.get("model_s", 0.1))
            tl += [f'tl.to("#{s}-wh",{{opacity:0.9,duration:0.15}},{j:.3f});',
                   f'tl.to("#{s}-coh",{{opacity:1,duration:0.4}},{j:.3f});',
                   f'tl.to("#{s}-fld",{{opacity:1,duration:0.6}},{j + 0.2:.3f});',
                   f'tl.to("#{s}-plg",{{attr:{{transform:"translate(0 40)"}},duration:0.35,ease:"power3.in"}},{st_ - 0.35:.3f});']
            tl += _trip_tl(s, st_, -22.0)
            mid = st_ + 0.45 * (q - st_)
            tl += [f'tl.to("#{s}-arc1",{{opacity:1,duration:0.1}},{st_ + 0.1:.3f});',
                   f'tl.to("#{s}-arc1",{{opacity:0,duration:0.5}},{mid:.3f});',
                   f'tl.to("#{s}-arc2",{{opacity:1,duration:0.4}},{mid - 0.2:.3f});',
                   f'tl.to("#{s}-arc2",{{opacity:0,duration:0.3}},{q:.3f});',
                   f'tl.to("#{s}-wh",{{opacity:0,duration:0.3}},{q:.3f});',
                   f'tl.to("#{s}-coh",{{opacity:0,duration:0.3}},{q:.3f});',
                   f'tl.to("#{s}-fld",{{opacity:0,duration:0.3}},{q:.3f});']
            # stopwatch without numbers: one turn from the jump to the quench, the norm limit as text
            inner.append(f'<circle cx="{cx}" cy="{cy}" r="76" fill="{k["surface"]}" fill-opacity="0.9" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="2"/>'
                         f'<rect x="{cx - 14}" y="{cy - 100}" width="28" height="18" rx="4" fill="{k["steel"]}"/>'
                         f'<g id="{s}-sw" transform="rotate(0 {cx} {cy})"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 64}" stroke="{k["accent"]}" stroke-width="5" stroke-linecap="round"/></g>'
                         f'<circle cx="{cx}" cy="{cy}" r="7" fill="{k["accent"]}"/>')
            tl.append(f'tl.to("#{s}-sw",{{attr:{{transform:"rotate(359 {cx} {cy})"}},duration:{q - j:.3f},ease:"none"}},{j:.3f});')
            lim = d.get("limit")
            if lim:
                _check(problems, "limit", lim["text"], 12)
                inner.append(f'<text id="{s}-lim" class="zt-lim" x="{cx}" y="{cy + 130}" text-anchor="middle" opacity="0">{_e(lim["text"])}</text>'
                             f'<text id="{s}-lim2" class="zt-ax" x="{cx}" y="{cy + 176}" text-anchor="middle" opacity="0">{_e("Norm" if de else "standard")}</text>')
                t = _t(c, d, lim.get("at"), 0.9)
                tl += [_show(f"#{s}-lim", t, 0.3, 8), _show(f"#{s}-lim2", t + 0.1, 0.3, 8)]
                ev.append(t)
            ev += [j, st_, mid, q]
            band, btl, bev = _tband(c, k, [(c.start, "real", ""), (j, "slow", _fac(model_s, q - j, False, de)), (q + 0.2, "stand", "")],
                                    d.get("band_ref", ""))
    inner += [band, _source(c, d, problems)]
    return _tout(c, k, "".join(inner), tl + btl, ev + bev, problems, photo=photo, ground_at=ground_at)


# trip curve: x = multiple of the rated current (log, 1..20), y = time to trip (log, 0.01 s .. 10000 s)
CX0, CX1, CY0, CY1 = 230.0, 900.0, 1150.0, 430.0


def _cx(m: float) -> float:
    return CX0 + (CX1 - CX0) * math.log10(m) / math.log10(20)


def _cy(t: float) -> float:
    return CY0 - (CY0 - CY1) * (math.log10(t) + 2) / 6


def zt_curve(c: SceneCtx, d: dict) -> SceneOut:
    """Trip curve with log axes. data: zones [{m0, m1, text, at}] (instant-trip band, e.g. B 3..5, C 5..10, drawn
    below 0.1 s); points [{m, t, text, side, at}] (norm values); curve {knots [[m, t], ...], from, to, text}: a pen
    draws the schematic course (labelled as such); source."""
    k = _k(c)
    s = c.sid
    de = c.lang == "de"
    problems: list[str] = []
    tl: list[str] = []
    ev: list[float] = []
    st, mu = k["steel"], k["muted"]
    o = [f'<rect x="{CX0}" y="{CY1}" width="{CX1 - CX0}" height="{CY0 - CY1}" fill="{k["surface"]}" fill-opacity="0.55"/>']
    labels_t = {-2: "0,01 s", -1: "0,1 s", 0: "1 s", 1: "10 s", 2: "100 s", 3: "1000 s"} if de else \
        {-2: "0.01 s", -1: "0.1 s", 0: "1 s", 1: "10 s", 2: "100 s", 3: "1000 s"}
    for e in range(-2, 5):
        y = _cy(10.0 ** e)
        o.append(f'<line x1="{CX0}" y1="{y:.1f}" x2="{CX1}" y2="{y:.1f}" stroke="{st}" stroke-opacity="0.18" stroke-width="1.5"/>')
        if e in labels_t:
            o.append(f'<text class="zt-ax" x="{CX0 - 12}" y="{y + 9:.1f}" text-anchor="end">{labels_t[e]}</text>')
    y1h = _cy(3600)
    o.append(f'<line x1="{CX0}" y1="{y1h:.1f}" x2="{CX1}" y2="{y1h:.1f}" stroke="{AMBER}" stroke-opacity="0.7" stroke-width="2.5" stroke-dasharray="10 8"/>'
             f'<text class="zt-ax" x="{CX0 - 12}" y="{y1h + 9:.1f}" text-anchor="end" style="fill:{AMBER}">1 h</text>')
    y01 = _cy(0.1)
    o.append(f'<line x1="{CX0}" y1="{y01:.1f}" x2="{CX1}" y2="{y01:.1f}" stroke="{k["accent"]}" stroke-opacity="0.8" stroke-width="2.5" stroke-dasharray="10 8"/>')
    for m in (1, 2, 5, 10, 20):
        x = _cx(m)
        o.append(f'<line x1="{x:.1f}" y1="{CY1}" x2="{x:.1f}" y2="{CY0}" stroke="{st}" stroke-opacity="0.18" stroke-width="1.5"/>'
                 f'<text class="zt-ax" x="{x:.1f}" y="{CY0 + 40}" text-anchor="middle">{m}</text>')
    o.append(f'<rect x="{CX0}" y="{CY1}" width="{CX1 - CX0}" height="{CY0 - CY1}" fill="none" stroke="{st}" stroke-opacity="0.6" stroke-width="2"/>'
             f'<text class="zt-ax" x="{CX1}" y="{CY0 + 84}" text-anchor="end">{_e("Vielfaches des Nennstroms In" if de else "multiple of rated current In")}</text>'
             f'<text class="zt-ax" x="{CX0}" y="{CY1 - 22}">{_e("Zeit bis zur Auslösung" if de else "time to trip")}</text>')
    for i, z in enumerate(d.get("zones", [])):
        x0, x1 = _cx(float(z["m0"])), _cx(float(z["m1"]))
        o.append(f'<g id="{s}-cz{i}" opacity="0"><rect x="{x0:.1f}" y="{y01:.1f}" width="{x1 - x0:.1f}" height="{CY0 - y01:.1f}" '
                 f'fill="{k["accent"]}" fill-opacity="{0.32 if i == 0 else 0.16}"/>'
                 f'<text class="zt-pt" x="{x1 - 12:.1f}" y="{CY0 - 16:.1f}" text-anchor="end">{_e(z.get("text", ""))}</text></g>')
        t = _t(c, d, z.get("at"), 0.4 + 0.2 * i)
        tl.append(_show(f"#{s}-cz{i}", t, 0.35))
        ev.append(t)
    cv = d.get("curve")
    if cv:
        pts = [(_cx(float(m)), _cy(float(t))) for m, t in cv["knots"]]
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        o.append(f'<polyline id="{s}-cv" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{k["text"]}" '
                 f'stroke-width="5" stroke-linejoin="round" stroke-dasharray="{length:.1f}" stroke-dashoffset="{length:.1f}"/>')
        if cv.get("text"):
            o.append(f'<text id="{s}-cvt" class="zt-ax" x="{CX1 - 8}" y="{_cy(40):.1f}" text-anchor="end" opacity="0">{_e(cv["text"])}</text>')
        t0, t1 = _t(c, d, cv.get("from"), 0.1), _t(c, d, cv.get("to"), 0.5)
        tl += [f'tl.to("#{s}-cv",{{attr:{{"stroke-dashoffset":0}},duration:{max(0.3, t1 - t0):.3f},ease:"none"}},{t0:.3f});']
        if cv.get("text"):
            tl.append(_show(f"#{s}-cvt", t0, 0.3))
        ev += [t0, t1]
    for i, p in enumerate(d.get("points", [])):
        x, y = _cx(float(p["m"])), _cy(float(p["t"]))
        txt = p.get("text", "")
        _check(problems, f"point {i}", txt, 22)
        side = p.get("side", "r")
        w = len(txt) * 17 + 20
        lx = x + 18 if side == "r" else x - 18 - w
        ly = y - 18 if p.get("up", True) else y + 46
        o.append(f'<g id="{s}-cp{i}" opacity="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{AMBER if p.get("hot") else k["accent"]}" stroke="{k["bg"]}" stroke-width="3"/>'
                 f'<rect x="{lx:.1f}" y="{ly - 32:.1f}" width="{w}" height="44" rx="6" fill="{k["bg"]}" fill-opacity="0.88"/>'
                 f'<text class="zt-pt" x="{lx + 10:.1f}" y="{ly:.1f}">{_e(txt)}</text></g>')
        t = _t(c, d, p.get("at"), 0.2 + 0.12 * i)
        tl.append(_show(f"#{s}-cp{i}", t, 0.3, 6))
        ev.append(t)
    band, btl, bev = _tband(c, k, [(c.start, "stand", "")])
    o += [band, _source(c, d, problems)]
    return _tout(c, k, "".join(o), tl + btl, ev + bev, problems)


# --- zt_chart: general measuring-station chart driven by data only (04.11.2026) ----------------------------------
# For topics without a model of their own: a curve from a formula or from points, axes (linear or log), marks, bands and
# rules, optionally over a photo. A plan written by a model API names the formula and its parameters; the numbers come
# from the code, never from the text model. Same plot area as zt_curve.

import re as _re

_SAFE_FN = {k: getattr(math, k) for k in ("sin", "cos", "tan", "exp", "log", "log10", "sqrt", "pi", "radians", "degrees")}


def _formula(expr: str, params: dict, x: float) -> float:
    if len(expr) > 120 or "__" in expr or not _re.fullmatch(r"[0-9A-Za-z_+\-*/().,\s]+", expr):
        raise ValueError(f"formula not allowed: {expr!r}")
    return float(eval(expr, {"__builtins__": {}}, {**_SAFE_FN, **{k: float(v) for k, v in params.items()}, "x": x}))  # noqa: S307


def _ax(a: dict):
    lo, hi, log = float(a["min"]), float(a["max"]), bool(a.get("log"))
    return lo, hi, (math.log10 if log else (lambda v: v))


def _m(v: float, ax, p0: float, p1: float) -> float:
    lo, hi, f = ax
    return p0 + (p1 - p0) * (f(v) - f(lo)) / (f(hi) - f(lo))


def zt_chart(c: SceneCtx, d: dict) -> SceneOut:
    """data: x, y {min, max, log, label, ticks [[value, text], ...]}; series [{formula, params, x0, x1, knots, text, from, to}];
    points [{x, y, text, at, hot, side, up}]; bands [{x0, x1, text, at}] (full-height columns); rules [{y|x, text, hot}];
    photo (bool, with ground_at: the measuring ground covers the photo later); mode: stand | real; source."""
    k = _k(c)
    s = c.sid
    problems: list[str] = []
    tl: list[str] = []
    ev: list[float] = []
    st = k["steel"]
    X, Y = _ax(d["x"]), _ax(d["y"])
    px = lambda v: _m(v, X, CX0, CX1)  # noqa: E731
    py = lambda v: _m(v, Y, CY0, CY1)  # noqa: E731
    o = [f'<rect x="{CX0}" y="{CY1}" width="{CX1 - CX0}" height="{CY0 - CY1}" fill="{k["surface"]}" fill-opacity="0.55"/>']
    for val, txt in d["y"].get("ticks", []):
        yy = py(float(val))
        o.append(f'<line x1="{CX0}" y1="{yy:.1f}" x2="{CX1}" y2="{yy:.1f}" stroke="{st}" stroke-opacity="0.18" stroke-width="1.5"/>'
                 f'<text class="zt-ax" x="{CX0 - 12}" y="{yy + 9:.1f}" text-anchor="end">{_e(txt)}</text>')
    for val, txt in d["x"].get("ticks", []):
        xx = px(float(val))
        o.append(f'<line x1="{xx:.1f}" y1="{CY1}" x2="{xx:.1f}" y2="{CY0}" stroke="{st}" stroke-opacity="0.18" stroke-width="1.5"/>'
                 f'<text class="zt-ax" x="{xx:.1f}" y="{CY0 + 40}" text-anchor="middle">{_e(txt)}</text>')
    o.append(f'<rect x="{CX0}" y="{CY1}" width="{CX1 - CX0}" height="{CY0 - CY1}" fill="none" stroke="{st}" stroke-opacity="0.6" stroke-width="2"/>'
             f'<text class="zt-ax" x="{CX1}" y="{CY0 + 84}" text-anchor="end">{_e(d["x"].get("label", ""))}</text>'
             f'<text class="zt-ax" x="{CX0}" y="{CY1 - 22}">{_e(d["y"].get("label", ""))}</text>')
    for i, b in enumerate(d.get("bands", [])):
        x0, x1 = px(float(b["x0"])), px(float(b["x1"]))
        o.append(f'<g id="{s}-ba{i}" opacity="0"><rect x="{x0:.1f}" y="{CY1}" width="{x1 - x0:.1f}" height="{CY0 - CY1}" fill="{k["accent"]}" fill-opacity="0.2"/>'
                 f'<text class="zt-pt" x="{x1 - 12:.1f}" y="{CY0 - 16:.1f}" text-anchor="end">{_e(b.get("text", ""))}</text></g>')
        t = _t(c, d, b.get("at"), 0.4 + 0.2 * i)
        tl.append(_show(f"#{s}-ba{i}", t, 0.35))
        ev.append(t)
    for i, r in enumerate(d.get("rules", [])):
        col = AMBER if r.get("hot") else k["accent"]
        if "y" in r:
            yy = py(float(r["y"]))
            line = f'<line x1="{CX0}" y1="{yy:.1f}" x2="{CX1}" y2="{yy:.1f}" stroke="{col}" stroke-width="2.5" stroke-dasharray="10 8"/>'
            lab = f'<text class="zt-ax" x="{CX1 - 8}" y="{yy - 10:.1f}" text-anchor="end" style="fill:{col}">{_e(r.get("text", ""))}</text>'
        else:
            xx = px(float(r["x"]))
            line = f'<line x1="{xx:.1f}" y1="{CY1}" x2="{xx:.1f}" y2="{CY0}" stroke="{col}" stroke-width="2.5" stroke-dasharray="10 8"/>'
            lab = f'<text class="zt-ax" x="{xx + 8:.1f}" y="{CY1 + 30}" style="fill:{col}">{_e(r.get("text", ""))}</text>'
        o.append(f'<g id="{s}-ru{i}" opacity="0">{line}{lab}</g>')
        t = _t(c, d, r.get("at"), 0.3)
        tl.append(_show(f"#{s}-ru{i}", t, 0.3))
        ev.append(t)
    for i, sr in enumerate(d.get("series", [])):
        if "formula" in sr:
            x0, x1 = float(sr.get("x0", d["x"]["min"])), float(sr.get("x1", d["x"]["max"]))
            n = 120
            xs = [x0 + (x1 - x0) * j / n for j in range(n + 1)]
            if d["x"].get("log"):
                xs = [10 ** (math.log10(x0) + (math.log10(x1) - math.log10(x0)) * j / n) for j in range(n + 1)]
            pts = [(px(x), py(_formula(sr["formula"], sr.get("params", {}), x))) for x in xs]
        else:
            pts = [(px(float(a)), py(float(b))) for a, b in sr["knots"]]
        pts = [(x, min(max(y, CY1), CY0)) for x, y in pts]
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        o.append(f'<polyline id="{s}-sr{i}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" '
                 f'stroke="{AMBER if sr.get("hot") else k["text"]}" stroke-width="5" stroke-linejoin="round" '
                 f'stroke-dasharray="{length:.1f}" stroke-dashoffset="{length:.1f}"/>')
        t0, t1 = _t(c, d, sr.get("from"), 0.1), _t(c, d, sr.get("to"), 0.5)
        tl.append(f'tl.to("#{s}-sr{i}",{{attr:{{"stroke-dashoffset":0}},duration:{max(0.3, t1 - t0):.3f},ease:"none"}},{t0:.3f});')
        ev += [t0, t1]
        if sr.get("text"):
            o.append(f'<text id="{s}-st{i}" class="zt-ax" x="{CX1 - 8}" y="{CY1 + 40 + 34 * i}" text-anchor="end" opacity="0">{_e(sr["text"])}</text>')
            tl.append(_show(f"#{s}-st{i}", t0, 0.3))
    for i, p in enumerate(d.get("points", [])):
        x, y = px(float(p["x"])), py(float(p["y"]))
        txt = p.get("text", "")
        _check(problems, f"point {i}", txt, 26)
        w = len(txt) * 17 + 20
        lx = x + 18 if p.get("side", "r") == "r" else x - 18 - w
        if lx + w > CX1:
            lx = x - 18 - w
        ly = y - 18 if p.get("up", True) else y + 46
        o.append(f'<g id="{s}-pt{i}" opacity="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{AMBER if p.get("hot") else k["accent"]}" stroke="{k["bg"]}" stroke-width="3"/>'
                 f'<rect x="{lx:.1f}" y="{ly - 32:.1f}" width="{w}" height="44" rx="6" fill="{k["bg"]}" fill-opacity="0.88"/>'
                 f'<text class="zt-pt" x="{lx + 10:.1f}" y="{ly:.1f}">{_e(txt)}</text></g>')
        t = _t(c, d, p.get("at"), 0.2 + 0.12 * i)
        tl.append(_show(f"#{s}-pt{i}", t, 0.3, 6))
        ev.append(t)
    band, btl, bev = _tband(c, k, [(c.start, "real" if d.get("mode") == "real" else "stand", "")])
    o += [band, _source(c, d, problems)]
    photo = bool(d.get("photo"))
    return _tout(c, k, "".join(o), tl + btl, ev + bev, problems, photo=photo,
                 ground_at=_t(c, d, d.get("ground_at"), 0.15) if photo else None)


TEMPLATES = {"zl_hook": zl_hook, "zl_strobe": zl_strobe, "zl_cause": zl_cause, "zl_trace": zl_trace, "zl_realtime": zl_realtime,
             "zt_photo": zt_photo, "zt_mcb": zt_mcb, "zt_curve": zt_curve, "zt_chart": zt_chart, **_ADAPTED}
HOOK_SCENE_TYPES = ["zl_hook", "zt_photo"]
LIMITS = {"zl_hook": {"claim": 64}, **{f"zlx_{n[3:]}": v for n, v in RV.LIMITS.items() if n != "rv_hook"}}  # noqa: F821
