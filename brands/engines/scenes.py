"""Revlore (engines) scene templates: mechanism hook, cutaway, exploded view, timing drive, readout.

Loaded by fn.render.brand_scenes for brand `engines` only (TEMPLATES, LIMITS, HOOK_SCENE_TYPES, CSS);
see docs/direction-system.md section 6d. Everything is programmatic SVG animated with GSAP attribute tweens, so the
motion is computed, not drawn:

- slider-crank kinematics: piston pin y = CY - (R cos t + sqrt(L^2 - R^2 sin^2 t)), crank turns clockwise
  as seen in the drawing, rod follows piston pin and crank pin;
- four-stroke cycle over 720 deg crank angle, camshafts at half crank speed, same direction (belt or chain);
- valve events from MIT 2.61 lecture 8 "typical valve timing": IVO 10 deg btdc, IVC 40 deg abdc,
  EVO 40 deg bbdc, EVC 10 deg atdc (inside the published ranges); lift from the cam profile;
- spark at 30 deg btdc (MBT example, MIT 2.61 lecture 9, Fig. 9-3).

Crank angle 0 = TDC at the start of the intake stroke. A beat's `data.theta` lists knots
[[at, deg], ...]; `at` is a fraction of the beat (0..1) or "w:<word>" (the start of that spoken word,
taken from SceneCtx.words). Angles are unwrapped (keep increasing); positions use mod 720.

Quality round Q1 (31.10.2026, Qualitätsrunde): every scene draws the same drafting-room backdrop (gradient, top
light, vignette, drifting grid and ghost drawings as a function of absolute time, so cuts stay continuous); the engine
carries intake plenum and exhaust header and fills about 90 % of the content width; titles are centred under the
explainer kicker; labels are cards with leader lines; each scene pushes in by 2.5 %; the cycle strip with the
"Zyl. 1" tile runs in every scene. The engine drawing is in native coordinates (crank at 540/1010) and placed with a
view (scale, top): the default cutaway view keeps the crank at 540/1010, so circle transitions meet the crank.
"""
from __future__ import annotations

import html
import math
import re

from fn.render.templates import SceneCtx, SceneOut


# --- geometry (native SVG coordinates of the engine drawing, 1080 x 1920 frame) -------------------------
CX, CY = 540, 1010        # crank centre
R, L = 100, 320           # crank radius, rod length (lambda = 0.31)
PIN2CROWN = 46            # piston pin to crown
PISTON_H = 118
BORE_L, BORE_R = 430, 650
BLOCK_L, BLOCK_R = 350, 730          # block walls with water jackets
HEAD_L, HEAD_R = 330, 750            # cylinder head (overhangs the block)
ROOF_EDGE_Y, ROOF_TOP_Y = 522, 482   # pent roof: edges at the liner, ridge at the centre
TILT = math.radians(20)   # valve axis inclination (= roof slope)
STEM = 140
LIFT_MAX = 22
CAM_BASE = 26
SEAT_X = 488              # intake seat centre x (exhaust mirrored)

IVO, IVC, EVO, EVC = -10.0, 220.0, 500.0, 730.0
SPARK = 330.0
PHASES = [(-10.0, "fresh"), (220.0, "comp"), (330.0, "burn"), (500.0, "exh")]

# --- screen layout (explainer layout 2026-10-30, quality round 2026-10-31) ----------------------------
TITLE_X, TITLE_Y = 540, 318          # centred scene title, Oswald 64 px: glyph box ~242-335, below the kicker (186-218)
STRIP_X, STRIP_Y, STRIP_W, STRIP_H = 108, 1468, 814, 66    # cycle strip below the captions, right edge 922
STRIP_TILE = 142                     # "Zyl. 1" tile at the left of the strip
LEFT, RIGHT = 120, 918               # card edges; x >= 930 stays free for platform icons
VIEW_CUT = (0.9, 371.0)              # cutaway view: scale, screen y of native y 300 -> crank stays at 540/1010
PUSH = 1.025                         # camera push-in per scene, around (540, 760)
STROKES_DE = ["Ansaugen", "Verdichten", "Arbeiten", "Ausstoßen"]
STROKES_EN = ["Intake", "Compression", "Power", "Exhaust"]

_TEXT = {"title": 30, "claim": 64, "label": 18, "chip": 18, "line": 36, "big": 12}   # characters per field kind


def _e(s) -> str:
    return html.escape(str(s))


def pin_y(th: float) -> float:
    t = math.radians(th)
    return CY - (R * math.cos(t) + math.sqrt(L * L - (R * math.sin(t)) ** 2))


def crank_pin(th: float) -> tuple[float, float]:
    t = math.radians(th)
    return CX + R * math.sin(t), CY - R * math.cos(t)


PIN_TDC = pin_y(0.0)
CROWN_TDC = PIN_TDC - PIN2CROWN
CROWN_BDC = pin_y(180.0) - PIN2CROWN


def _valve_axes(side: int):
    """side -1 intake (left), +1 exhaust (right). Returns seat centre, unit vector up the stem, cam centre."""
    sx = SEAT_X if side < 0 else 1080 - SEAT_X
    sy = ROOF_EDGE_Y - (abs(sx - (BORE_L if side < 0 else BORE_R))) * math.tan(TILT)
    ux, uy = (-math.sin(TILT) if side < 0 else math.sin(TILT)), -math.cos(TILT)
    top = (sx + ux * STEM, sy + uy * STEM)
    cam = (top[0] + ux * (CAM_BASE + 12), top[1] + uy * (CAM_BASE + 12))
    return (sx, sy), (ux, uy), top, cam


def _event_lift(th: float, open_deg: float, close_deg: float) -> float:
    """Valve lift from a cos^2 cam flank; window in crank degrees, periodic over 720."""
    peak = (open_deg + close_deg) / 2.0
    half = (close_deg - open_deg) / 2.0
    d = ((th - peak + 360.0) % 720.0) - 360.0
    if abs(d) >= half:
        return 0.0
    return LIFT_MAX * math.cos(math.pi * d / (2 * half)) ** 2


def lift_in(th: float) -> float:
    return _event_lift(th, IVO, IVC)


def lift_ex(th: float) -> float:
    return _event_lift(th, EVO, EVC)


def phase(th: float) -> str:
    m = (th + 10.0) % 720.0 - 10.0
    cur = "fresh"
    for start, name in PHASES:
        if m >= start:
            cur = name
    return cur


def gas_opacity(th: float) -> float:
    m = (th + 10.0) % 720.0 - 10.0
    if m < 220:
        return 0.20
    if m < 330:
        return 0.20 + 0.25 * (m - 220) / 110
    if m < 500:
        return 0.85 - 0.5 * (m - 330) / 170
    return 0.35 - 0.23 * (m - 500) / 210


# --- time <-> angle ----------------------------------------------------------------------------------

def _norm(w: str) -> str:
    return re.sub(r"[^\wäöüß]", "", w.lower())


def word_time(c: SceneCtx, d: dict, word: str) -> float:
    """Start of the n-th spoken word in this beat that begins with `word` ("Wort" or "Wort#2", SceneCtx.words);
    middle of the beat if the word is not found."""
    m = re.fullmatch(r"(.+?)(?:#(\d+))?", word)
    key, nth = _norm(m.group(1)), int(m.group(2) or 1)
    hits = [w for w in getattr(c, "words", None) or [] if _norm(w.text).startswith(key)]
    if len(hits) >= nth:
        return float(hits[nth - 1].start)
    return c.start + c.duration * 0.5


def at_time(c: SceneCtx, d: dict, at) -> float:
    if isinstance(at, str) and at.startswith("w:"):
        return word_time(c, d, at[2:])
    return c.start + c.duration * float(at)


class Track:
    """Piecewise-linear crank angle over absolute time."""

    def __init__(self, knots: list[tuple[float, float]]):
        k = sorted(knots)
        out = [k[0]]
        for t, a in k[1:]:
            if t <= out[-1][0] + 1e-3:
                t = out[-1][0] + 1e-3
            out.append((t, a))
        self.k = out

    @classmethod
    def from_data(cls, c: SceneCtx, d: dict, default: tuple[float, float] = (0.0, 0.0)):
        spec = d.get("theta") or [[0, default[0]], [1, default[1]]]
        return cls([(at_time(c, d, at), float(deg)) for at, deg in spec])

    @property
    def t0(self) -> float:
        return self.k[0][0]

    @property
    def t1(self) -> float:
        return self.k[-1][0]

    def angle(self, t: float) -> float:
        if t <= self.k[0][0]:
            return self.k[0][1]
        for (ta, aa), (tb, ab) in zip(self.k, self.k[1:]):
            if t <= tb:
                return aa + (ab - aa) * (t - ta) / (tb - ta)
        return self.k[-1][1]

    def times_at(self, deg: float, period: float = 720.0) -> list[float]:
        """All times where the unwrapped angle passes deg (mod period), increasing segments only."""
        ts = []
        for (ta, aa), (tb, ab) in zip(self.k, self.k[1:]):
            if ab <= aa:
                continue
            n0 = math.ceil((aa - deg) / period - 1e-9)
            n1 = math.floor((ab - deg) / period + 1e-9)
            for n in range(n0, n1 + 1):
                a = deg + n * period
                if aa < a <= ab:
                    ts.append(round(ta + (tb - ta) * (a - aa) / (ab - aa), 3))
        return ts

    def samples(self, step: float = 6.0, extra: list[float] | None = None) -> list[tuple[float, float]]:
        """(t, angle) samples: knots, every `step` degrees, and the given extra angles (mod 720)."""
        pts: list[tuple[float, float]] = []
        for (ta, aa), (tb, ab) in zip(self.k, self.k[1:]):
            n = max(1, int(math.ceil(abs(ab - aa) / step)))
            dt = (tb - ta) / n
            if dt < 1 / 30 and n > 1:                  # never finer than one frame
                n = max(1, int((tb - ta) * 30))
            for i in range(n):
                pts.append((ta + (tb - ta) * i / n, aa + (ab - aa) * i / n))
        pts.append(self.k[-1])
        for a in extra or []:
            for t in self.times_at(a):
                pts.append((t, self.angle(t)))
        pts.sort()
        clean = [pts[0]]
        for p in pts[1:]:
            if p[0] - clean[-1][0] > 1e-3:
                clean.append(p)
        return clean


def _kf(sel: str, samples: list[tuple[float, float]], fn, attr: str) -> list[str]:
    """GSAP keyframes for one attribute (value = fn(angle)), piecewise linear between samples."""
    t0 = samples[0][0]
    v0 = fn(samples[0][1])
    lines = [f'tl.set("{sel}",{{attr:{{"{attr}":"{v0}"}}}},{t0:.3f});']
    frames = []
    prev = t0
    for t, a in samples[1:]:
        frames.append(f'{{attr:{{"{attr}":"{fn(a)}"}},duration:{t - prev:.3f},ease:"none"}}')
        prev = t
    if frames:
        lines.append(f'tl.to("{sel}",{{keyframes:[{",".join(frames)}]}},{t0:.3f});')
    return lines


def _kf_num(sel: str, samples, fn, prop: str) -> list[str]:
    """Same for a plain numeric property (opacity)."""
    t0 = samples[0][0]
    lines = [f'tl.set("{sel}",{{{prop}:{fn(samples[0][1]):.3f}}},{t0:.3f});']
    frames, prev = [], t0
    for t, a in samples[1:]:
        frames.append(f'{{{prop}:{fn(a):.3f},duration:{t - prev:.3f},ease:"none"}}')
        prev = t
    if frames:
        lines.append(f'tl.to("{sel}",{{keyframes:[{",".join(frames)}]}},{t0:.3f});')
    return lines


def _f(x: float) -> str:
    return f"{x:.1f}"


# --- palette helpers -------------------------------------------------------------------------------

def _pal(c: SceneCtx) -> dict:
    p = c.pal
    return {
        "bg": p.get("bg", "#171C22"), "surface": p.get("surface", "#222932"), "text": p.get("text", "#E7ECF1"),
        "muted": p.get("muted", "#8D99A6"), "accent": p.get("accent", "#2F9BFF"), "steel": p.get("steel", "#AEB9C5"),
        "steel_dark": p.get("steel_dark", "#5E6A76"), "hairline": p.get("hairline_solid", "#3A4450"),
        "fire": p.get("combustion", "#FF7A2F"), "exhaust": p.get("exhaust", "#7D8794"), "hatch": p.get("hatch", "#4A5562"),
    }


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:
    """Revlore scene CSS, appended by the director after the shared CSS."""
    k = {"text": pal.get("text", "#E7ECF1"), "muted": pal.get("muted", "#8D99A6"), "accent": pal.get("accent", "#2F9BFF"),
         "steel": pal.get("steel", "#AEB9C5"), "bg": pal.get("bg", "#171C22")}
    # opaque ground: an incoming scene covers the outgoing one during a circle or cross-fade transition (explainer
    # layer) instead of showing both drawings at once; the backdrop itself is SVG inside every scene (_backdrop)
    return f"""
.scene-inner.rv{{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;gap:0;background-color:{k['bg']};}}
.rv svg.rv-svg{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;}}
.rv .lbl{{font-family:'FN {mono}';font-size:30px;fill:{k['text']};}}
.rv .dim{{font-family:'FN {mono}';font-size:30px;fill:{k['steel']};}}
.rv .dim.hi{{fill:{k['accent']};}}
.rv .ttl{{font-family:'FN {display}';font-weight:600;font-size:64px;fill:{k['text']};letter-spacing:0.01em;}}
.rv .ttl .num{{fill:{k['accent']};}}
.rv .claim{{font-family:'FN {display}';font-weight:600;font-size:80px;fill:{k['text']};}}
.rv .claim .hl{{fill:{k['accent']};}}
.rv .cnt-l{{font-family:'FN {mono}';font-size:26px;fill:{k['muted']};letter-spacing:0.04em;}}
.rv .cnt-n{{font-family:'FN {display}';font-weight:600;font-size:120px;fill:{k['text']};}}
.rv .cnt-n.acc{{fill:{k['accent']};}}
.rv .cnt-m{{font-family:'FN {display}';font-weight:600;font-size:100px;fill:{k['text']};}}
.rv .cnt-m.acc{{fill:{k['accent']};}}
.rv .seg-t{{font-family:'FN {display}';font-weight:500;font-size:28px;fill:{k['muted']};}}
.rv .seg-t.on{{fill:{k['text']};}}
.rv .tile-t{{font-family:'FN {display}';font-weight:600;font-size:30px;fill:{k['text']};letter-spacing:0.02em;}}
.rv .chip-t{{font-family:'FN {display}';font-weight:600;font-size:42px;fill:{k['text']};}}
.rv .big{{font-family:'FN {display}';font-weight:600;font-size:150px;fill:{k['text']};}}
.rv .line{{font-family:'FN {mono}';font-size:36px;fill:{k['steel']};}}
.rv .line .acc{{fill:{k['accent']};}}
.rv .tick{{font-family:'FN {mono}';font-size:36px;fill:{k['steel']};}}
.rv .note{{font-family:'FN {mono}';font-size:30px;fill:{k['muted']};}}
.rv .tick-s{{font-family:'FN {mono}';font-size:28px;fill:{k['steel']};}}
.rv .axis-t{{font-family:'FN {mono}';font-size:26px;fill:{k['muted']};letter-spacing:0.04em;}}
.rv .band-t,.rv .mark-t{{font-family:'FN {display}';font-weight:600;font-size:34px;fill:{k['text']};}}
.rv .leg-t{{font-family:'FN {mono}';font-size:26px;fill:{k['text']};}}
.rv .leg-b{{font-family:'FN {display}';font-weight:500;font-size:40px;fill:{k['text']};}}
.rv .year{{font-family:'FN {display}';font-weight:600;font-size:190px;fill:{k['accent']};letter-spacing:0.02em;}}
.rv .doc-h{{font-family:'FN {mono}';font-size:28px;fill:#3A4450;letter-spacing:0.06em;}}
.rv .doc-t{{font-family:'FN {display}';font-weight:600;font-size:42px;fill:#171C22;}}
.rv .doc-s{{font-family:'FN {display}';font-weight:600;font-size:30px;fill:{k['accent']};}}
.rv .row-t{{font-family:'FN {display}';font-weight:500;font-size:38px;fill:{k['text']};}}
.rv .col-h{{font-family:'FN {display}';font-weight:600;font-size:52px;fill:{k['text']};}}
.rv .cell-t{{font-family:'FN {display}';font-weight:500;font-size:36px;fill:{k['text']};}}
.rv .vclaim{{font-family:'FN {display}';font-weight:600;font-size:60px;fill:{k['text']};}}
.rv .vstamp{{font-family:'FN {display}';font-weight:600;font-size:42px;fill:{k['text']};letter-spacing:0.04em;}}
.rv .bar-v{{font-family:'FN {display}';font-weight:600;font-size:46px;fill:{k['text']};}}
"""


def _defs(sid: str, k: dict) -> str:
    s = sid
    return (f'<defs><pattern id="{s}-hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="14" height="14" fill="{k["surface"]}"/><line x1="0" y1="0" x2="0" y2="14" stroke="{k["hatch"]}" stroke-width="3"/></pattern>'
            f'<marker id="{s}-arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{k["accent"]}"/></marker>'
            f'<marker id="{s}-arrx" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{k["exhaust"]}"/></marker>'
            # backdrop: graphite gradient, top light, vignette, two drafting grids
            f'<linearGradient id="{s}-bgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#202832"/>'
            f'<stop offset="0.55" stop-color="{k["bg"]}"/><stop offset="1" stop-color="#101418"/></linearGradient>'
            f'<linearGradient id="{s}-lit" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#DCE8F5" stop-opacity="0.07"/>'
            f'<stop offset="0.5" stop-color="#DCE8F5" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="{s}-vig" cx="0.5" cy="0.42" r="0.75"><stop offset="0.45" stop-color="#06080B" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#06080B" stop-opacity="0.62"/></radialGradient>'
            f'<pattern id="{s}-gmin" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24,0 L0,0 L0,24" fill="none" stroke="{k["steel"]}" stroke-opacity="0.035" stroke-width="1"/></pattern>'
            f'<pattern id="{s}-gmaj" width="96" height="96" patternUnits="userSpaceOnUse"><path d="M96,0 L0,0 L0,96" fill="none" stroke="{k["steel"]}" stroke-opacity="0.085" stroke-width="1.5"/></pattern>'
            # materials: turned steel (piston, valves), forged web, soft shadows
            f'<linearGradient id="{s}-gsteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E6A76"/>'
            f'<stop offset="0.2" stop-color="{k["steel"]}"/><stop offset="0.46" stop-color="#E2E8EE"/>'
            f'<stop offset="0.72" stop-color="{k["steel"]}"/><stop offset="1" stop-color="#66727E"/></linearGradient>'
            f'<linearGradient id="{s}-gweb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7C8894"/>'
            f'<stop offset="1" stop-color="#46505B"/></linearGradient>'
            f'<radialGradient id="{s}-gface" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#26303A"/>'
            f'<stop offset="1" stop-color="{k["surface"]}"/></radialGradient>'
            f'<filter id="{s}-sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity="0.5"/></filter>'
            f'<filter id="{s}-blur" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="16"/></filter>'
            '</defs>')


# --- backdrop: same drafting room in every scene, driven by absolute time ------------------------------

GRID_SPEED = 5.0            # px/s upward drift of the drafting grid
GHOST_RATE = 2.4            # deg/s of the ghost sprocket


def _ghost_xy(t: float) -> tuple[float, float]:
    return 14 * math.sin(2 * math.pi * t / 29.0), 22 * math.sin(2 * math.pi * t / 37.0)


def _backdrop(c: SceneCtx, k: dict) -> tuple[str, list[str]]:
    """Depth without glow: graphite gradient, light falling from the top left, vignette, a drafting grid that drifts
    and ghost technical drawings (sprocket, crank throw, concentric circles) that float slower than the grid
    (parallax). Positions are functions of absolute time, so the backdrop runs on through hard cuts."""
    s = c.sid
    st = k["steel"]
    teeth = "".join(f'<rect x="-7" y="-268" width="14" height="22" rx="3" transform="rotate({360 * i / 32:.2f})"/>' for i in range(32))
    ghost = (f'<g id="{s}-bgd" transform="translate(0,0)" fill="none" stroke="{st}" stroke-opacity="0.13" stroke-width="2">'
             f'<g transform="translate(925,330)"><g id="{s}-bgs" transform="rotate(0)">'
             f'<circle r="250"/><circle r="196" stroke-dasharray="6 10"/><circle r="64"/><circle r="22"/>'
             f'<g fill="{st}" fill-opacity="0.05" stroke="none">{teeth}</g>'
             + "".join(f'<line x1="0" y1="-70" x2="0" y2="-190" transform="rotate({a})"/>' for a in range(0, 360, 60))
             + '</g><line x1="-300" y1="0" x2="300" y2="0" stroke-dasharray="24 8 4 8"/><line x1="0" y1="-300" x2="0" y2="300" stroke-dasharray="24 8 4 8"/></g>'
             f'<g transform="translate(150,1520)"><circle r="110"/><circle r="205" stroke-dasharray="4 10"/><circle r="300"/>'
             f'<line x1="-340" y1="0" x2="340" y2="0" stroke-dasharray="24 8 4 8"/><line x1="0" y1="-340" x2="0" y2="340" stroke-dasharray="24 8 4 8"/></g>'
             f'<g transform="translate(70,760) rotate(-24) scale(1.5)"><path d="M-125,0 A125,125 0 0,0 125,0 Z"/>'
             f'<rect x="-36" y="-134" width="72" height="160" rx="34"/><circle r="30"/><circle cy="-100" r="24"/></g>'
             f'<path d="M760,1180 L1020,1180 M760,1166 L760,1194 M1020,1166 L1020,1194" stroke-opacity="0.09"/>'
             f'<path d="M60,240 L60,560 M46,240 L74,240 M46,560 L74,560" stroke-opacity="0.09"/></g>')
    frame = "".join(f'<path d="{p}" fill="none" stroke="{st}" stroke-opacity="0.22" stroke-width="2"/>' for p in
                    ("M44,84 L44,44 L84,44", "M996,44 L1036,44 L1036,84", "M44,1836 L44,1876 L84,1876", "M996,1876 L1036,1876 L1036,1836"))
    svg = (f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-bgv)"/>'
           f'<g id="{s}-bgg" transform="translate(0,0)"><rect x="0" y="-220" width="1080" height="2380" fill="url(#{s}-gmin)"/>'
           f'<rect x="0" y="-220" width="1080" height="2380" fill="url(#{s}-gmaj)"/></g>'
           f'{ghost}<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-lit)"/>'
           f'<rect x="0" y="0" width="1080" height="1920" fill="url(#{s}-vig)"/>{frame}')
    t0, t1 = c.start, c.end
    g0 = -((t0 * GRID_SPEED) % 96.0)
    tl = [f'tl.fromTo("#{s}-bgg",{{attr:{{transform:"translate(0,{g0:.2f})"}}}},'
          f'{{attr:{{transform:"translate(0,{g0 - (t1 - t0) * GRID_SPEED:.2f})"}},duration:{t1 - t0:.3f},ease:"none"}},{t0:.3f});']
    n = max(2, int((t1 - t0) / 0.5) + 1)
    smp = [(t0 + (t1 - t0) * i / (n - 1),) * 2 for i in range(n)]
    tl += _kf(f"#{s}-bgd", smp, lambda t: "translate({:.2f},{:.2f})".format(*_ghost_xy(t)), "transform")
    tl += [f'tl.fromTo("#{s}-bgs",{{attr:{{transform:"rotate({t0 * GHOST_RATE:.2f})"}}}},'
           f'{{attr:{{transform:"rotate({t1 * GHOST_RATE:.2f})"}},duration:{t1 - t0:.3f},ease:"none"}},{t0:.3f});']
    return svg, tl


def _push(c: SceneCtx) -> str:
    """Slow camera push-in on the scene's motif group (#<sid>-cam) over the whole beat."""
    p = PUSH
    return (f'tl.fromTo("#{c.sid}-cam",{{attr:{{transform:"matrix(1,0,0,1,0,0)"}}}},'
            f'{{attr:{{transform:"matrix({p},0,0,{p},{(1 - p) * 540:.2f},{(1 - p) * 760:.2f})"}},duration:{c.duration:.3f},ease:"sine.inOut"}},{c.start:.3f});')


# --- view: native engine drawing -> screen ------------------------------------------------------------

def _view(d: dict, default: tuple[float, float] = VIEW_CUT) -> tuple[float, float, float]:
    v = d.get("view") or {}
    s = float(v.get("s", default[0]))
    top = float(v.get("top", default[1]))
    return s, float(v.get("x", 540)) - s * 540, top - s * 300


def _T(view, x: float, y: float) -> tuple[float, float]:
    s, dx, dy = view
    return dx + s * x, dy + s * y


def _place(view, inner: str) -> str:
    s, dx, dy = view
    return f'<g transform="translate({dx:.2f},{dy:.2f}) scale({s})">{inner}</g>'


# --- the engine drawing --------------------------------------------------------------------------

def _cam_path(cx: float, cy: float, nose_dir: float) -> str:
    """Cam outline: base circle plus the cos^2 flank used for the lift (nose pointing to nose_dir rad)."""
    half_cam = math.radians((IVC - IVO) / 4.0)            # half opening window in cam degrees
    pts = []
    for i in range(0, 360, 6):
        a = math.radians(i)
        d = (a - nose_dir + math.pi) % (2 * math.pi) - math.pi
        r = CAM_BASE + (LIFT_MAX * math.cos(math.pi * d / (2 * half_cam)) ** 2 if abs(d) < half_cam else 0)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def _crank_web(sid: str, k: dict, *, pin: bool = False) -> str:
    """Crank web (counterweight half disc and throw), drawn at angle 0; id {sid}-crank."""
    return (f'<g id="{sid}-crank" transform="rotate(0 {CX} {CY})">'
            f'<path d="M{CX - 125},{CY} A125,125 0 0,0 {CX + 125},{CY} Z" fill="url(#{sid}-gweb)" stroke="#2B333C" stroke-width="2"/>'
            f'<rect x="{CX - 36}" y="{CY - R - 34}" width="72" height="{R + 60}" rx="34" fill="url(#{sid}-gweb)" stroke="#2B333C" stroke-width="2"/>'
            f'<circle cx="{CX}" cy="{CY}" r="30" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-width="4"/>'
            f'<line x1="{CX}" y1="{CY + 60}" x2="{CX}" y2="{CY + 112}" stroke="{k["bg"]}" stroke-width="6"/>'
            + (f'<circle cx="{CX}" cy="{CY - R}" r="24" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-width="4"/>' if pin else "")
            + '</g>')


def _piston(sid: str, k: dict) -> str:
    pt = CROWN_TDC
    return (f'<g id="{sid}-piston" transform="translate(0,0)">'
            f'<rect x="{BORE_L + 3}" y="{pt:.1f}" width="{BORE_R - BORE_L - 6}" height="{PISTON_H}" rx="6" fill="url(#{sid}-gsteel)"/>'
            + "".join(f'<line x1="{BORE_L + 3}" y1="{pt + y:.1f}" x2="{BORE_R - 3}" y2="{pt + y:.1f}" stroke="{k["steel_dark"]}" stroke-width="4"/>' for y in (14, 26, 38))
            + f'<rect x="{BORE_L + 3}" y="{pt:.1f}" width="{BORE_R - BORE_L - 6}" height="6" rx="3" fill="#EEF2F6" fill-opacity="0.55"/>'
            + f'<circle cx="{CX}" cy="{PIN_TDC:.1f}" r="16" fill="{k["surface"]}" stroke="{k["steel_dark"]}" stroke-width="4"/></g>')


def _rod(sid: str, k: dict, y1: float, x2: float, y2: float) -> str:
    return (f'<line id="{sid}-rod" x1="{CX}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{k["steel"]}" stroke-width="30" stroke-linecap="round"/>'
            f'<line id="{sid}-rodhi" x1="{CX}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#E2E8EE" stroke-opacity="0.5" stroke-width="7" stroke-linecap="round"/>')


def engine_svg(sid: str, k: dict, *, fuel: str = "petrol", injector: str | None = None, knock: bool = False,
               speed: bool = False) -> str:
    """Cutaway of one cylinder (DOHC, two valves, pent roof) with intake plenum and exhaust header, in native
    coordinates. Ids: {sid}-piston, -rod, -rodhi, -crank, -crankpin, -vin, -vex, -camin, -camex, -gas, -spark,
    -flowin, -fin, -flowex, -fex."""
    s = sid
    hatch = f"url(#{s}-hatch)"
    out = [f'<ellipse cx="540" cy="1196" rx="360" ry="24" fill="#04060A" fill-opacity="0.55" filter="url(#{s}-blur)"/>',
           f'<g filter="url(#{s}-sh)">']
    # intake plenum and runner, exhaust header (outer walls, cut = hatched)
    out.append(f'<rect x="120" y="300" width="124" height="262" rx="22" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<rect x="236" y="378" width="100" height="94" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<rect x="744" y="378" width="206" height="94" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>')
    # crankcase (hatched wall, open inside)
    out.append(f'<path d="M352,880 L352,1124 Q352,1186 414,1186 L666,1186 Q728,1186 728,1124 L728,880 Z" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<path d="M384,880 L384,1116 Q384,1156 424,1156 L656,1156 Q696,1156 696,1116 L696,880 Z" fill="{k["bg"]}"/>')
    # block walls with water jackets
    out.append(f'<rect x="{BLOCK_L}" y="{ROOF_EDGE_Y}" width="{BORE_L - BLOCK_L}" height="{890 - ROOF_EDGE_Y}" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<rect x="{BORE_R}" y="{ROOF_EDGE_Y}" width="{BLOCK_R - BORE_R}" height="{890 - ROOF_EDGE_Y}" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<rect x="366" y="552" width="34" height="306" rx="14" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<rect x="680" y="552" width="34" height="306" rx="14" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>')
    # cylinder head
    out.append(f'<path d="M{HEAD_L},322 Q{HEAD_L},300 {HEAD_L + 22},300 L{HEAD_R - 22},300 Q{HEAD_R},300 {HEAD_R},322 L{HEAD_R},{ROOF_EDGE_Y} '
               f'L{BORE_R},{ROOF_EDGE_Y} L540,{ROOF_TOP_Y} L{BORE_L},{ROOF_EDGE_Y} L{HEAD_L},{ROOF_EDGE_Y} Z" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
               f'<line x1="{HEAD_L}" y1="{ROOF_EDGE_Y}" x2="{BORE_L}" y2="{ROOF_EDGE_Y}" stroke="{k["steel_dark"]}" stroke-width="4"/>'
               f'<line x1="{BORE_R}" y1="{ROOF_EDGE_Y}" x2="{HEAD_R}" y2="{ROOF_EDGE_Y}" stroke="{k["steel_dark"]}" stroke-width="4"/>')
    # ports (cut free) and cam pockets
    for side in (-1, 1):
        (sx, sy), (ux, uy), top, cam = _valve_axes(side)
        tx, ty = math.cos(TILT), (-math.sin(TILT) if side < 0 else math.sin(TILT))   # along the roof slope
        a = (sx - tx * 27, sy - ty * 27)
        b = (sx + tx * 27, sy + ty * 27)
        outer_x = HEAD_L if side < 0 else HEAD_R
        p = (f"M{outer_x},392 L{(sx + outer_x) / 2:.1f},{404:.1f} L{max(a[0], b[0]) if side < 0 else min(a[0], b[0]):.1f},{min(a[1], b[1]):.1f} "
             f"L{min(a[0], b[0]) if side < 0 else max(a[0], b[0]):.1f},{max(a[1], b[1]):.1f} L{(sx + outer_x) / 2 - side * 10:.1f},{462:.1f} L{outer_x},458 Z")
        out.append(f'<path d="{p}" fill="{k["bg"]}"/>')
        out.append(f'<circle cx="{cam[0]:.1f}" cy="{cam[1]:.1f}" r="{CAM_BASE + LIFT_MAX + 6}" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>')
        out.append(f'<line x1="{sx + ux * 30:.1f}" y1="{sy + uy * 30:.1f}" x2="{top[0]:.1f}" y2="{top[1]:.1f}" stroke="{k["bg"]}" stroke-width="16"/>')
    # channels of plenum, runner and header; flanges
    out.append(f'<rect x="134" y="314" width="96" height="234" rx="12" fill="{k["bg"]}"/>'
               f'<rect x="224" y="392" width="112" height="66" fill="{k["bg"]}"/>'
               f'<rect x="744" y="392" width="206" height="66" fill="{k["bg"]}"/>'
               f'<ellipse cx="950" cy="425" rx="9" ry="47" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="2"/>'
               f'<ellipse cx="950" cy="425" rx="5" ry="33" fill="{k["bg"]}"/>')
    for fx in (HEAD_L - 12, HEAD_R - 12):
        out.append(f'<rect x="{fx}" y="366" width="24" height="26" rx="3" fill="{k["steel_dark"]}"/>'
                   f'<rect x="{fx}" y="458" width="24" height="26" rx="3" fill="{k["steel_dark"]}"/>')
    # bore
    out.append(f'<rect x="{BORE_L}" y="{ROOF_EDGE_Y}" width="{BORE_R - BORE_L}" height="{890 - ROOF_EDGE_Y}" fill="{k["bg"]}"/>')
    out.append(f'<line x1="{BORE_L}" y1="{ROOF_EDGE_Y}" x2="{BORE_L}" y2="890" stroke="{k["steel_dark"]}" stroke-width="3"/>'
               f'<line x1="{BORE_R}" y1="{ROOF_EDGE_Y}" x2="{BORE_R}" y2="890" stroke="{k["steel_dark"]}" stroke-width="3"/>')
    # gas
    out.append(f'<path id="{s}-gas" d="M{BORE_L + 2},{ROOF_EDGE_Y} L540,{ROOF_TOP_Y} L{BORE_R - 2},{ROOF_EDGE_Y} L{BORE_R - 2},{CROWN_TDC:.1f} L{BORE_L + 2},{CROWN_TDC:.1f} Z" fill="{k["accent"]}" fill-opacity="0.2"/>')
    # flow through plenum, runner and port (dashes move with the crank while the valve is open)
    out.append(f'<g id="{s}-flowin" opacity="0"><path id="{s}-fin" d="M182,520 L182,428 L330,425 L452,438 L474,470" fill="none" stroke="{k["accent"]}" '
               f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14 18" stroke-dashoffset="0" marker-end="url(#{s}-arr)"/></g>')
    out.append(f'<g id="{s}-flowex" opacity="0"><path id="{s}-fex" d="M606,470 L628,438 L750,425 L938,425" fill="none" stroke="{k["exhaust"]}" '
               f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14 18" stroke-dashoffset="0" marker-end="url(#{s}-arrx)"/></g>')
    # crank web (behind the rod), rod, crank pin, piston
    out.append(_crank_web(s, k))
    px, py = crank_pin(0.0)
    out.append(_rod(s, k, PIN_TDC, px, py))
    out.append(f'<g id="{s}-crankpin" transform="rotate(0 {CX} {CY})"><circle cx="{CX}" cy="{CY - R}" r="24" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-width="4"/></g>')
    out.append(_piston(s, k))
    # valves and cams
    for side, name in ((-1, "in"), (1, "ex")):
        (sx, sy), (ux, uy), top, cam = _valve_axes(side)
        tx, ty = math.cos(TILT), (-math.sin(TILT) if side < 0 else math.sin(TILT))
        d1 = (sx - tx * 26, sy - ty * 26)
        d2 = (sx + tx * 26, sy + ty * 26)
        d3 = (d2[0] - ux * 8, d2[1] - uy * 8)
        d4 = (d1[0] - ux * 8, d1[1] - uy * 8)
        color = k["accent"] if side < 0 else k["exhaust"]
        out.append(f'<g id="{s}-v{name}" transform="translate(0,0)">'
                   f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{top[0]:.1f}" y2="{top[1]:.1f}" stroke="{k["steel"]}" stroke-width="9"/>'
                   f'<path d="M{d1[0]:.1f},{d1[1]:.1f} L{d2[0]:.1f},{d2[1]:.1f} L{d3[0]:.1f},{d3[1]:.1f} L{d4[0]:.1f},{d4[1]:.1f} Z" fill="url(#{s}-gsteel)" stroke="{color}" stroke-width="3"/>'
                   f'<rect x="{top[0] - 17:.1f}" y="{top[1] - 11:.1f}" width="34" height="22" rx="4" fill="{k["steel_dark"]}" stroke="{color}" stroke-width="3" transform="rotate({math.degrees(-side * TILT * -1):.1f} {top[0]:.1f} {top[1]:.1f})"/></g>')
        follower = math.atan2(top[1] - cam[1], top[0] - cam[0])
        out.append(f'<g id="{s}-cam{name}" transform="rotate(0 {cam[0]:.1f} {cam[1]:.1f})">'
                   f'<path d="{_cam_path(cam[0], cam[1], follower)}" fill="url(#{s}-gweb)" stroke="{color}" stroke-width="3"/>'
                   f'<circle cx="{cam[0]:.1f}" cy="{cam[1]:.1f}" r="8" fill="{k["bg"]}"/></g>')
    spray = "#CFE3F5"
    if fuel == "diesel":
        # diesel injector in the centre instead of a spark plug; fuel spray, then flames at the spray tips
        out.append(f'<rect x="{CX - 13}" y="300" width="26" height="{ROOF_TOP_Y - 306}" rx="6" fill="url(#{s}-gsteel)"/>'
                   f'<rect x="{CX - 20}" y="330" width="40" height="40" rx="5" fill="{k["steel_dark"]}"/>'
                   f'<path d="M{CX - 6},{ROOF_TOP_Y - 8} L{CX + 6},{ROOF_TOP_Y - 8} L{CX},{ROOF_TOP_Y + 6} Z" fill="{k["steel"]}"/>')
        tips = [(462, 560), (500, 590), (580, 590), (618, 560)]
        out.append(f'<g id="{s}-dspray" opacity="0">' + "".join(
            f'<line x1="{CX}" y1="{ROOF_TOP_Y + 6}" x2="{x}" y2="{y}" stroke="{spray}" stroke-width="6" stroke-linecap="round" stroke-dasharray="10 8"/>' for x, y in tips) + '</g>')
        out.append(f'<g id="{s}-spark" opacity="0">' + "".join(
            f'<circle cx="{x}" cy="{y}" r="24" fill="{k["fire"]}" fill-opacity="0.85"/><circle cx="{(x + CX) / 2:.0f}" cy="{(y + ROOF_TOP_Y) / 2:.0f}" r="15" fill="{k["fire"]}" fill-opacity="0.7"/>'
            for x, y in tips) + '</g>')
    else:
        # spark plug (ceramic insulator, steel body)
        out.append(f'<rect x="{CX - 13}" y="318" width="26" height="{ROOF_TOP_Y - 330}" rx="6" fill="url(#{s}-gsteel)"/>'
                   f'<rect x="{CX - 11}" y="304" width="22" height="58" rx="8" fill="#E7ECF1"/>'
                   f'<rect x="{CX - 20}" y="362" width="40" height="22" rx="4" fill="{k["steel_dark"]}"/>'
                   f'<line x1="{CX}" y1="{ROOF_TOP_Y - 14}" x2="{CX}" y2="{ROOF_TOP_Y + 6}" stroke="{k["steel"]}" stroke-width="5"/>')
        out.append(f'<g id="{s}-spark" opacity="0">'
                   f'<circle cx="{CX}" cy="{ROOF_TOP_Y + 14}" r="26" fill="{k["fire"]}" fill-opacity="0.9"/>'
                   + "".join(f'<line x1="{CX + 30 * math.cos(math.radians(a)):.1f}" y1="{ROOF_TOP_Y + 14 + 30 * math.sin(math.radians(a)):.1f}" '
                             f'x2="{CX + 56 * math.cos(math.radians(a)):.1f}" y2="{ROOF_TOP_Y + 14 + 56 * math.sin(math.radians(a)):.1f}" stroke="{k["fire"]}" stroke-width="5" stroke-linecap="round"/>'
                             for a in range(0, 360, 45)) + '</g>')
    if injector == "port":     # injector above the intake runner, sprays towards the back of the intake valve
        out.append(f'<line x1="290" y1="318" x2="318" y2="392" stroke="{k["steel_dark"]}" stroke-width="18" stroke-linecap="round"/>'
                   f'<line x1="290" y1="318" x2="318" y2="392" stroke="{k["steel"]}" stroke-width="6"/>')
        out.append(f'<g id="{s}-ispray" opacity="0">' + "".join(
            f'<line x1="322" y1="398" x2="{x}" y2="{y}" stroke="{spray}" stroke-width="5" stroke-linecap="round" stroke-dasharray="8 7"/>' for x, y in ((420, 420), (430, 440), (410, 452))) + '</g>')
    elif injector == "direct":  # injector in the head on the intake side, sprays into the cylinder
        out.append(f'<line x1="372" y1="474" x2="440" y2="506" stroke="{k["steel_dark"]}" stroke-width="18" stroke-linecap="round"/>'
                   f'<line x1="372" y1="474" x2="440" y2="506" stroke="{k["steel"]}" stroke-width="6"/>')
        out.append(f'<g id="{s}-ispray" opacity="0">' + "".join(
            f'<line x1="446" y1="512" x2="{x}" y2="{y}" stroke="{spray}" stroke-width="6" stroke-linecap="round" stroke-dasharray="10 8"/>' for x, y in ((560, 560), (540, 600), (575, 520))) + '</g>')
    if knock:                  # self-ignition spots in the end gas at the edges of the chamber
        out.append(f'<g id="{s}-knock" opacity="0">' + "".join(
            f'<g transform="translate({x},{y})"><circle r="16" fill="#FFD7B0"/>' + "".join(
                f'<line x1="{20 * math.cos(math.radians(a)):.1f}" y1="{20 * math.sin(math.radians(a)):.1f}" x2="{34 * math.cos(math.radians(a)):.1f}" y2="{34 * math.sin(math.radians(a)):.1f}" stroke="{k["fire"]}" stroke-width="4" stroke-linecap="round"/>'
                for a in range(0, 360, 60)) + '</g>' for x, y in ((452, 536), (628, 536))) + '</g>')
    if speed:                  # arrow beside the bore: piston velocity, length proportional to dy/dtheta
        out.append(f'<line id="{s}-vel" x1="{BLOCK_R + 34}" y1="700" x2="{BLOCK_R + 34}" y2="700" stroke="{k["accent"]}" stroke-width="10" stroke-linecap="round" marker-end="url(#{s}-arr)"/>')
    out.append("</g>")
    return "".join(out)


def piston_velocity(th: float) -> float:
    """d(pin_y)/d(theta) in px per radian (positive = piston moving down)."""
    h = 0.25
    return (pin_y(th + h) - pin_y(th - h)) / math.radians(2 * h)


def engine_anim(sid: str, k: dict, track: Track, *, spark: bool = True, fuel: str = "petrol", injector: str | None = None,
                knock: bool = False, speed: bool = False) -> tuple[list[str], list[float]]:
    """GSAP lines for the whole mechanism over the track; returns (lines, event times)."""
    s = f"#{sid}"
    smp = track.samples(6.0, extra=[IVO, IVC, EVO, EVC % 720, SPARK, 0.0, 180.0, 360.0, 540.0])
    tl: list[str] = []
    ev: list[float] = []
    rods = f"{s}-rod,{s}-rodhi"
    tl += _kf(f"{s}-piston", smp, lambda a: f"translate(0,{pin_y(a) - PIN_TDC:.2f})", "transform")
    tl += _kf(f"{s}-crank", smp, lambda a: f"rotate({a:.2f} {CX} {CY})", "transform")
    tl += _kf(f"{s}-crankpin", smp, lambda a: f"rotate({a:.2f} {CX} {CY})", "transform")
    tl += _kf(rods, smp, lambda a: f"{pin_y(a):.2f}", "y1")
    tl += _kf(rods, smp, lambda a: f"{crank_pin(a)[0]:.2f}", "x2")
    tl += _kf(rods, smp, lambda a: f"{crank_pin(a)[1]:.2f}", "y2")
    for side, name, liftf, (o, cl) in ((-1, "in", lift_in, (IVO, IVC)), (1, "ex", lift_ex, (EVO, EVC))):
        (sx, sy), (ux, uy), top, cam = _valve_axes(side)
        peak = (o + cl) / 2.0
        tl += _kf(f"{s}-v{name}", smp, lambda a, ux=ux, uy=uy, lf=liftf: f"translate({-ux * lf(a):.2f},{-uy * lf(a):.2f})", "transform")
        # cam turns clockwise at half crank speed; nose meets the follower at the peak of the event
        tl += _kf(f"{s}-cam{name}", smp, lambda a, cx=cam[0], cy=cam[1], pk=peak: f"rotate({(a - pk) / 2.0:.2f} {cx:.1f} {cy:.1f})", "transform")
        tl += _kf_num(f"{s}-flow{name}", smp, lambda a, lf=liftf: min(1.0, lf(a) / (LIFT_MAX * 0.4)), "opacity")
        tl += _kf(f"{s}-f{name}", smp, lambda a: f"{-a * 1.4:.1f}", "stroke-dashoffset")
    tl += _kf(f"{s}-gas", smp, lambda a: (f"M{BORE_L + 2},{ROOF_EDGE_Y} L540,{ROOF_TOP_Y} L{BORE_R - 2},{ROOF_EDGE_Y} "
                                          f"L{BORE_R - 2},{pin_y(a) - PIN2CROWN:.2f} L{BORE_L + 2},{pin_y(a) - PIN2CROWN:.2f} Z"), "d")
    tl += _kf_num(f"{s}-gas", smp, gas_opacity, "opacity")
    colors = {"fresh": k["accent"], "comp": k["accent"], "burn": k["fire"], "exh": k["exhaust"]}
    tl.append(f'tl.set("{s}-gas",{{attr:{{fill:"{colors[phase(track.angle(track.t0))]}","fill-opacity":1}}}},{track.t0:.3f});')
    for start, name in PHASES:
        if fuel == "diesel" and name == "burn":
            start = 355.0
        for t in track.times_at(start % 720):
            tl.append(f'tl.set("{s}-gas",{{attr:{{fill:"{colors[name]}"}}}},{t:.3f});')
    if spark and fuel == "diesel":     # injection from 345 deg, ignition after the ignition delay at 355 deg
        for t in track.times_at(345.0):
            tl.append(f'tl.fromTo("{s}-dspray",{{opacity:0}},{{opacity:1,duration:0.05}},{t:.3f});')
        for t in track.times_at(380.0):
            tl.append(f'tl.to("{s}-dspray",{{opacity:0,duration:0.15}},{t:.3f});')
        for t in track.times_at(355.0):
            tl.append(f'tl.fromTo("{s}-spark",{{opacity:0}},{{opacity:1,duration:0.08}},{t:.3f});')
            tl.append(f'tl.to("{s}-spark",{{opacity:0,duration:0.5,ease:"power2.in"}},{t + 0.35:.3f});')
            ev.append(t)
    elif spark:
        for t in track.times_at(SPARK):
            tl.append(f'tl.fromTo("{s}-spark",{{opacity:0}},{{opacity:1,duration:0.05}},{t:.3f});')
            tl.append(f'tl.to("{s}-spark",{{opacity:0,duration:0.35,ease:"power2.in"}},{t + 0.12:.3f});')
            ev.append(t)
    if injector:
        a_on, a_off = (20.0, 150.0) if injector == "port" else (60.0, 150.0)
        for t in track.times_at(a_on):
            tl.append(f'tl.fromTo("{s}-ispray",{{opacity:0}},{{opacity:1,duration:0.05}},{t:.3f});')
        for t in track.times_at(a_off):
            tl.append(f'tl.to("{s}-ispray",{{opacity:0,duration:0.2}},{t:.3f});')
    if knock:
        for t in track.times_at(368.0):
            for j in range(3):
                tl.append(f'tl.fromTo("{s}-knock",{{opacity:0}},{{opacity:1,duration:0.03}},{t + 0.12 * j:.3f});')
                tl.append(f'tl.to("{s}-knock",{{opacity:0,duration:0.07}},{t + 0.12 * j + 0.05:.3f});')
            ev.append(t)
    if speed:
        tl += _kf(f"{s}-vel", smp, lambda a: f"{700 + 1.3 * piston_velocity(a):.1f}", "y2")
    return tl, ev


# --- labels as cards with leader lines ----------------------------------------------------------------

LABELS = {
    # key: (anchor x, y in native coordinates, side, card y on screen, de, en)
    "camin": (427, 334, "l", 640, "Nockenwelle", "Camshaft"),
    "vin": (452, 432, "l", 760, "Einlassventil", "Intake valve"),
    "piston": (440, 620, "l", 880, "Kolben", "Piston"),
    "rod": (556, 780, "r", 900, "Pleuel", "Con rod"),
    "crank": (640, 1010, "r", 1060, "Kurbelwelle", "Crankshaft"),
    "vex": (628, 432, "r", 640, "Auslassventil", "Exhaust valve"),
    "plug": (540, 330, "l", 640, "Zündkerze", "Spark plug"),
    "chamber": (580, 505, "r", 640, "Brennraum", "Chamber"),
}


def _card(gid: str, k: dict, text: str, side: str, y: float, ax: float | None = None, ay: float | None = None,
          color: str | None = None) -> str:
    """Label card (mono 30 px) at the left (x 120) or right (x 918) edge, leader line to the anchor (screen)."""
    color = color or k["accent"]
    w, h = len(text) * 18 + 44, 58
    x0 = LEFT if side == "l" else RIGHT - w
    ex = x0 + w if side == "l" else x0
    lead = ""
    if ax is not None:
        stub = ex + (26 if side == "l" else -26)
        lead = (f'<polyline points="{ex:.0f},{y:.0f} {stub:.0f},{y:.0f} {ax:.0f},{ay:.0f}" fill="none" stroke="{k["text"]}" stroke-opacity="0.75" stroke-width="2.5"/>'
                f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="8" fill="{color}" stroke="{k["bg"]}" stroke-width="3"/>')
    return (f'<g id="{gid}" opacity="0">{lead}'
            f'<rect x="{x0:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="12" fill="{k["surface"]}" fill-opacity="0.96" stroke="{color}" stroke-opacity="0.85" stroke-width="2"/>'
            f'<rect x="{x0:.0f}" y="{y - h / 2 + 12:.0f}" width="5" height="{h - 24}" rx="2" fill="{color}"/>'
            f'<text class="lbl" x="{x0 + 24:.0f}" y="{y + 10:.0f}">{_e(text)}</text></g>')


def _callouts(c: SceneCtx, d: dict, k: dict, view, problems: list[str]) -> tuple[str, list[str], list[float]]:
    """Labels (`labels`, keys of LABELS or {key, side, y}) at `labels_at`, and free notes
    (`notes`: [{text, at, side, y, to: [native x, y], color: accent|fire|exhaust|amber}])."""
    s = c.sid
    svg, tl, ev = [], [], []
    labels = d.get("labels", [])
    ats = d.get("labels_at", [0.25 + 0.15 * i for i in range(len(labels))])
    for i, item in enumerate(labels):
        item = {"key": item} if isinstance(item, str) else dict(item)
        ax, ay, side, y, de, en = LABELS[item["key"]]
        text = de if c.lang == "de" else en
        _check(problems, "label", f"label {i}", text)
        sx, sy = _T(view, ax, ay)
        svg.append(_card(f"{s}-lb{i}", k, text, item.get("side", side), item.get("y", y), sx, sy))
        t = at_time(c, d, ats[i] if i < len(ats) else 0.3)
        tl.append(_show(f"#{s}-lb{i}", t, 0.3, 10))
        ev.append(t)
    cols = {"accent": k["accent"], "fire": k["fire"], "exhaust": k["exhaust"], "amber": "#F5B342"}
    for i, n in enumerate(d.get("notes", [])):
        _check(problems, "label", f"note {i}", n.get("text", ""))
        to = n.get("to")
        sx, sy = _T(view, *to) if to else (None, None)
        svg.append(_card(f"{s}-nt{i}", k, n.get("text", ""), n.get("side", "l"), n.get("y", 1000), sx, sy, cols.get(n.get("color", "accent"))))
        t = at_time(c, d, n.get("at", 0.6))
        tl.append(_show(f"#{s}-nt{i}", t, 0.3, 10))
        ev.append(t)
    return "".join(svg), tl, ev


# --- persistent cycle strip (the "Arbeitsspiel" bar, the brand's status bar) ---------------------------

def _seg_x(i: int) -> tuple[float, float]:
    x0 = STRIP_X + STRIP_TILE + 8
    w = (STRIP_X + STRIP_W - x0) / 4
    return x0 + i * w, w


def strip_svg(sid: str, k: dict, lang: str) -> str:
    names = STROKES_DE if lang == "de" else STROKES_EN
    tile = "Zyl. 1" if lang == "de" else "Cyl. 1"
    out = [f'<g id="{sid}-strip">',
           f'<rect x="{STRIP_X}" y="{STRIP_Y}" width="{STRIP_TILE}" height="{STRIP_H}" rx="12" fill="{k["surface"]}" stroke="{k["steel"]}" stroke-opacity="0.45" stroke-width="2"/>',
           # tile icon: bore with piston
           f'<path d="M{STRIP_X + 18},{STRIP_Y + 14} L{STRIP_X + 18},{STRIP_Y + 52} M{STRIP_X + 46},{STRIP_Y + 14} L{STRIP_X + 46},{STRIP_Y + 52}" stroke="{k["steel"]}" stroke-width="3"/>',
           f'<rect id="{sid}-tpis" x="{STRIP_X + 21}" y="{STRIP_Y + 22}" width="22" height="16" rx="3" fill="{k["accent"]}"/>',
           f'<text class="tile-t" x="{STRIP_X + 58}" y="{STRIP_Y + 44}">{_e(tile)}</text>']
    for i, n in enumerate(names):
        x, w = _seg_x(i)
        out.append(f'<rect id="{sid}-seg{i}" x="{x + 3:.1f}" y="{STRIP_Y}" width="{w - 6:.1f}" height="{STRIP_H}" rx="10" fill="{k["surface"]}" stroke="{k["hairline"]}" stroke-width="2"/>')
        out.append(f'<text id="{sid}-segt{i}" class="seg-t" x="{x + w / 2:.1f}" y="{STRIP_Y + 43}" text-anchor="middle">{i + 1} {_e(n)}</text>')
    x0, _ = _seg_x(0)
    out.append(f'<rect id="{sid}-mark" x="{x0 - 3:.1f}" y="{STRIP_Y - 10}" width="6" height="{STRIP_H + 20}" rx="3" fill="{k["accent"]}"/>')
    out.append("</g>")
    return "".join(out)


def strip_anim(sid: str, k: dict, track: Track) -> tuple[list[str], list[float]]:
    s = f"#{sid}"
    tl, ev = [], []
    smp = track.samples(6.0, extra=[0.0, 180.0, 360.0, 540.0])
    x_start, _ = _seg_x(0)
    span = STRIP_X + STRIP_W - x_start
    t0 = smp[0][0]
    x = lambda a: x_start - 3 + ((a % 720) / 720) * span
    tl.append(f'tl.set("{s}-mark",{{attr:{{x:{x(smp[0][1]):.1f}}}}},{t0:.3f});')
    frames, prev, prev_a = [], t0, smp[0][1]
    for t, a in smp[1:]:
        if math.floor(a / 720 + 1e-9) > math.floor(prev_a / 720 + 1e-9) and a % 720 < 1e-6:
            frames.append(f'{{attr:{{x:{x_start - 3 + span:.1f}}},duration:{t - prev:.3f},ease:"none"}}')
            frames.append(f'{{attr:{{x:{x_start - 3:.1f}}},duration:0}}')
        else:
            frames.append(f'{{attr:{{x:{x(a):.1f}}},duration:{t - prev:.3f},ease:"none"}}')
        prev, prev_a = t, a
    tl.append(f'tl.to("{s}-mark",{{keyframes:[{",".join(frames)}]}},{t0:.3f});')
    # tile icon: the piston moves with the crank (same kinematics, scaled to the icon)
    tl += _kf(f"{s}-tpis", smp, lambda a: f"{STRIP_Y + 14 + (pin_y(a) - PIN_TDC) / (2 * R) * 22:.1f}", "y")

    def seg(a: float) -> int:
        return int((a % 720) // 180)
    cur = seg(track.angle(track.t0))
    for i in range(4):
        on = i == cur
        tl.append(f'tl.set("{s}-seg{i}",{{attr:{{fill:"{k["accent"] if on else k["surface"]}","fill-opacity":{0.28 if on else 1}}}}},{track.t0:.3f});')
        tl.append(f'tl.set("{s}-segt{i}",{{attr:{{class:"seg-t{" on" if on else ""}"}}}},{track.t0:.3f});')
    for b in (0.0, 180.0, 360.0, 540.0):
        i = int(b // 180)
        for t in track.times_at(b):
            if abs(t - track.t0) < 1e-3:
                continue
            j = (i - 1) % 4
            tl.append(f'tl.set("{s}-seg{j}",{{attr:{{fill:"{k["surface"]}","fill-opacity":1}}}},{t:.3f});')
            tl.append(f'tl.set("{s}-segt{j}",{{attr:{{class:"seg-t"}}}},{t:.3f});')
            tl.append(f'tl.set("{s}-seg{i}",{{attr:{{fill:"{k["accent"]}","fill-opacity":0.28}}}},{t:.3f});')
            tl.append(f'tl.set("{s}-segt{i}",{{attr:{{class:"seg-t on"}}}},{t:.3f});')
    return tl, ev


def strip_count(sid: str, k: dict, t: float, cur: int = 0) -> list[str]:
    """All four fields light up one after another (the spoken "vier Hübe"), then the active one stays."""
    s = f"#{sid}"
    tl = []
    for i in range(4):
        ti = t + 0.16 * i
        tl.append(f'tl.set("{s}-seg{i}",{{attr:{{fill:"{k["accent"]}","fill-opacity":0.28}}}},{ti:.3f});')
        tl.append(f'tl.set("{s}-segt{i}",{{attr:{{class:"seg-t on"}}}},{ti:.3f});')
    t_end = t + 0.16 * 4 + 0.5
    for i in range(4):
        if i != cur:
            tl.append(f'tl.set("{s}-seg{i}",{{attr:{{fill:"{k["surface"]}","fill-opacity":1}}}},{t_end:.3f});')
            tl.append(f'tl.set("{s}-segt{i}",{{attr:{{class:"seg-t"}}}},{t_end:.3f});')
    return tl


# --- scene wrappers --------------------------------------------------------------------------------

def _wrap(c: SceneCtx, inner_svg: str, k: dict) -> tuple[str, list[str]]:
    bg, bg_tl = _backdrop(c, k)
    return (f'<div class="scene-inner rv"><svg class="rv-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            f'{_defs(c.sid, k)}{bg}{inner_svg}</svg></div>'), bg_tl


def _fade(c: SceneCtx, *, fade_in: bool = True, fade_out: bool = True) -> list[str]:
    out = []
    if fade_in:
        out.append(f'tl.fromTo("#{c.sid} .scene-inner",{{opacity:0}},{{opacity:1,duration:0.2,ease:"power2.out"}},{c.start:.3f});')
    if fade_out:
        out.append(f'tl.to("#{c.sid} .scene-inner",{{opacity:0,duration:0.15,ease:"power2.in"}},{max(c.start + 0.3, c.end - 0.15):.3f});')
    return out


def _check(problems: list[str], kind: str, field: str, text: str) -> None:
    lim = _TEXT[kind]
    if len(text) > lim:
        problems.append(f"revlore.{field}: {len(text)} chars > {lim}")


def _show(sel: str, t: float, dur: float = 0.3, y: float = 0) -> str:
    return f'tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.3f});'


def _title(c: SceneCtx, d: dict, k: dict, problems: list[str]) -> str:
    t = d.get("title", "")
    if not t:
        return ""
    _check(problems, "title", "title", t)
    num = d.get("num", "")
    num_html = f'<tspan class="num">{_e(num)} </tspan>' if num else ""
    return f'<text id="{c.sid}-ttl" class="ttl" x="{TITLE_X}" y="{TITLE_Y}" text-anchor="middle" opacity="0">{num_html}{_e(t)}</text>'


def _out(c: SceneCtx, inner: str, k: dict, tl: list[str], ev: list[float], problems: list[str]) -> SceneOut:
    html_, bg_tl = _wrap(c, inner, k)
    return SceneOut(html=html_, tl=bg_tl + tl + [_push(c)], events=sorted(set(round(e, 3) for e in ev)), problems=problems)


# 1. mechanism hook (scene type rv_hook, the brand's hook type) -------------------------------------

def mechanism_hook(c: SceneCtx, d: dict) -> SceneOut:
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    claim = d.get("claim", "")
    _check(problems, "claim", "claim", claim)
    lines = d.get("claim_lines") or [claim]
    hl = d.get("claim_highlight", "")
    claim_svg = []
    for i, ln in enumerate(lines):
        txt = _e(ln)
        if hl and hl in ln:
            txt = _e(ln).replace(_e(hl), f'<tspan class="hl">{_e(hl)}</tspan>')
        claim_svg.append(f'<text class="claim" x="540" y="{300 + i * 92}" text-anchor="middle">{txt}</text>')
    track = Track.from_data(c, d, (0.0, 1440.0))
    view = _view(d, (0.74, 470.0))
    revs = int(track.angle(track.t1) // 360)
    sparks = track.times_at(SPARK)
    lab_rev, lab_ign = ("Umdrehungen", "Zündungen") if c.lang == "de" else ("Revolutions", "Ignitions")
    cnt = []
    for (x0, lab, pre, n_max, acc) in ((108, lab_rev, "rv", revs, ""), (708, lab_ign, "ig", len(sparks), " acc")):
        cnt.append(f'<rect x="{x0}" y="664" width="210" height="236" rx="16" fill="{k["surface"]}" fill-opacity="0.92" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="2"/>'
                   f'<text class="cnt-l" x="{x0 + 105}" y="714" text-anchor="middle">{lab}</text>'
                   f'<line x1="{x0 + 24}" y1="736" x2="{x0 + 186}" y2="736" stroke="{k["hairline"]}" stroke-width="2"/>')
        for n in range(n_max + 1):
            cnt.append(f'<text id="{s}-{pre}{n}" class="cnt-n{acc}" x="{x0 + 105}" y="866" text-anchor="middle" opacity="{1 if n == 0 else 0}">{n}</text>')
    opts = {"fuel": d.get("fuel", "petrol"), "injector": d.get("injector"), "knock": bool(d.get("knock")), "speed": bool(d.get("speed"))}
    inner = (f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{_place(view, engine_svg(s, k, **opts))}'
             f'<g id="{s}-cnt" opacity="0" display="{"inline" if d.get("counters", True) else "none"}">{"".join(cnt)}</g></g>'
             f'<g id="{s}-claim" opacity="0">{"".join(claim_svg)}</g>' + strip_svg(s, k, c.lang))
    tl, ev = engine_anim(s, k, track, **opts)
    a, b = strip_anim(s, k, track)
    tl += a
    tl += _fade(c, fade_in=False)
    tl.append(_show(f"#{s}-cnt", c.start + 0.05, 0.25))
    q_at = at_time(c, d, d.get("claim_at", 0.0))
    tl.append(_show(f"#{s}-claim", q_at, 0.35, 14))
    ev.append(q_at)
    for n, t in enumerate(track.times_at(0.0, 360.0)[: revs], start=1):
        tl.append(f'tl.set("#{s}-rv{n - 1}",{{opacity:0}},{t:.3f});')
        tl.append(f'tl.set("#{s}-rv{n}",{{opacity:1}},{t:.3f});')
        ev.append(t)
    for n, t in enumerate(sparks, start=1):
        tl.append(f'tl.set("#{s}-ig{n - 1}",{{opacity:0}},{t:.3f});')
        tl.append(f'tl.set("#{s}-ig{n}",{{opacity:1}},{t:.3f});')
    return _out(c, inner, k, tl, ev, problems)


# 2. cutaway (Schnittansicht) -------------------------------------------------------------------------

def cutaway(c: SceneCtx, d: dict) -> SceneOut:
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    track = Track.from_data(c, d, (0.0, 180.0))
    close = bool(d.get("cta") or d.get("chips"))
    view = _view(d, (0.85, 400.0) if close else VIEW_CUT)
    opts = {"fuel": d.get("fuel", "petrol"), "injector": d.get("injector"), "knock": bool(d.get("knock")), "speed": bool(d.get("speed"))}
    eng = engine_svg(s, k, **opts) + (_stroke_dims(s, k, c.lang) if d.get("stroke_dims") else "")
    cards, ctl, cev = _callouts(c, d, k, view, problems)
    inner = f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{_place(view, eng)}{cards}</g>' + _title(c, d, k, problems)
    if d.get("strip", True):
        inner += strip_svg(s, k, c.lang)
    chips = d.get("chips", [])
    widths = [len(ch.get("text", "")) * 18 + 48 for ch in chips]
    x = 540 - (sum(widths) + 14 * max(0, len(chips) - 1)) / 2
    for i, ch in enumerate(chips):
        _check(problems, "chip", f"chip {i}", ch.get("text", ""))
        inner += (f'<g id="{s}-ch{i}" opacity="0"><rect x="{x:.0f}" y="300" width="{widths[i]}" height="76" rx="14" fill="{k["surface"]}" stroke="{k["accent"]}" stroke-width="2"/>'
                  f'<text class="chip-t" x="{x + widths[i] / 2:.0f}" y="354" text-anchor="middle">{_e(ch.get("text", ""))}</text></g>')
        x += widths[i] + 14
    if d.get("cta"):
        cta = d["cta"]
        _check(problems, "title", "cta", cta.get("title", ""))
        inner += (f'<g id="{s}-cta" opacity="0"><text class="ttl" x="540" y="256" text-anchor="middle">'
                  f'<tspan class="num">{_e(cta.get("brand", ""))}</tspan> {_e(cta.get("title", ""))}</text></g>')
    tl, ev = engine_anim(s, k, track, **opts)
    if d.get("strip", True):
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    tl += _fade(c, fade_in=d.get("fade_in", False), fade_out=d.get("fade_out", True))
    if d.get("title"):
        t = at_time(c, d, d.get("title_at", 0.0))
        tl.append(_show(f"#{s}-ttl", t + 0.05, 0.3, 10))
        ev.append(t)
    tl += ctl
    ev += cev
    for i, ch in enumerate(chips):
        t = at_time(c, d, ch.get("at", 0.5))
        tl.append(_show(f"#{s}-ch{i}", t, 0.3, 10))
        ev.append(t)
    if d.get("stroke_dims"):
        t = at_time(c, d, d.get("dims_at", 0.3))
        tl.append(_show(f"#{s}-dims", t, 0.3))
        ev.append(t)
    if d.get("cta"):
        t = at_time(c, d, d["cta"].get("at", 0.7))
        if d.get("title"):
            tl.append(f'tl.to("#{s}-ttl",{{opacity:0,duration:0.2}},{t - 0.2:.3f});')
        tl.append(_show(f"#{s}-cta", t, 0.35, 10))
        ev.append(t)
    return _out(c, inner, k, tl, ev, problems)


def _stroke_dims(sid: str, k: dict, lang: str, x: float = 765) -> str:
    """OT, UT and stroke at the right of the bore (native coordinates)."""
    ot, ut, hub = ("OT", "UT", "Hub") if lang == "de" else ("TDC", "BDC", "Stroke")
    return (f'<g id="{sid}-dims" opacity="0">'
            f'<line x1="{BORE_R + 8}" y1="{CROWN_TDC:.1f}" x2="{x + 30}" y2="{CROWN_TDC:.1f}" stroke="{k["text"]}" stroke-opacity="0.7" stroke-width="2.5" stroke-dasharray="6 6"/>'
            f'<line x1="{BORE_R + 8}" y1="{CROWN_BDC:.1f}" x2="{x + 30}" y2="{CROWN_BDC:.1f}" stroke="{k["text"]}" stroke-opacity="0.7" stroke-width="2.5" stroke-dasharray="6 6"/>'
            f'<line x1="{x}" y1="{CROWN_TDC + 6:.1f}" x2="{x}" y2="{CROWN_BDC - 6:.1f}" stroke="{k["accent"]}" stroke-width="5" marker-start="url(#{sid}-arr)" marker-end="url(#{sid}-arr)"/>'
            f'<text class="dim" x="{x + 44}" y="{CROWN_TDC + 11:.1f}">{ot}</text>'
            f'<text class="dim" x="{x + 44}" y="{CROWN_BDC + 11:.1f}">{ut}</text>'
            f'<text class="dim hi" x="{x + 44}" y="{(CROWN_TDC + CROWN_BDC) / 2 + 11:.1f}">{hub}</text></g>')


# 3. exploded view (Explosionsansicht) -------------------------------------------------------------

def exploded(c: SceneCtx, d: dict) -> SceneOut:
    """Piston, pin, rod and crankshaft apart with label cards, assemble, then turn: one stroke = half a turn.
    Native = screen coordinates (crank at 540/1010, the same point as the cutaway view: circle transition)."""
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    off = {"piston": -170, "rod": -85, "crank": 0}     # exploded piston top y 374, below the title
    px, py = crank_pin(0.0)
    hatch = f"url(#{s}-hatch)"
    liner = (f'<g id="{s}-liner" opacity="0">'      # block and crankcase in section fade in when the parts assemble
             f'<path d="M352,880 L352,1124 Q352,1186 414,1186 L666,1186 Q728,1186 728,1124 L728,880 Z" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<path d="M384,880 L384,1116 Q384,1156 424,1156 L656,1156 Q696,1156 696,1116 L696,880 Z" fill="{k["bg"]}"/>'
             f'<rect x="{BLOCK_L}" y="{ROOF_EDGE_Y}" width="{BORE_L - BLOCK_L}" height="{890 - ROOF_EDGE_Y}" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="{BORE_R}" y="{ROOF_EDGE_Y}" width="{BLOCK_R - BORE_R}" height="{890 - ROOF_EDGE_Y}" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="366" y="552" width="34" height="306" rx="14" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="680" y="552" width="34" height="306" rx="14" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="{BORE_L}" y="{ROOF_EDGE_Y}" width="{BORE_R - BORE_L}" height="{890 - ROOF_EDGE_Y}" fill="{k["bg"]}"/></g>')
    parts = (f'<ellipse cx="540" cy="1196" rx="300" ry="22" fill="#04060A" fill-opacity="0.55" filter="url(#{s}-blur)"/>{liner}'
             f'<g filter="url(#{s}-sh)">'
             f'<g id="{s}-xcrank" transform="translate(0,{off["crank"]})">{_crank_web(s, k, pin=True)}</g>'
             f'<g id="{s}-xrod" transform="translate(0,{off["rod"]})">{_rod(s, k, PIN_TDC, px, py)}</g>'
             f'<g id="{s}-xpiston" transform="translate(0,{off["piston"]})">{_piston(s, k)}</g></g>')
    names = {"de": ["Kolben", "Kolbenbolzen", "Pleuel", "Kurbelwelle"], "en": ["Piston", "Piston pin", "Con rod", "Crankshaft"]}[c.lang]
    anchors = [(BORE_L + 3, CROWN_TDC + 60 + off["piston"]), (CX + 16, PIN_TDC + off["piston"]),
               (CX + 14, (PIN_TDC + py) / 2 + off["rod"]), (CX - 125, CY + 30 + off["crank"])]
    sides = ["l", "r", "r", "l"]
    ys = [CROWN_TDC + 60 + off["piston"], PIN_TDC + off["piston"] - 10, (PIN_TDC + py) / 2 + off["rod"], CY + 30]
    lab = "".join(_card(f"{s}-xl{i}", k, n, sides[i], ys[i], ax, ay) for i, (n, (ax, ay)) in enumerate(zip(names, anchors)))
    ghost = (f'<g id="{s}-ghost" opacity="0"><rect x="{BORE_L + 3}" y="{CROWN_BDC:.1f}" width="{BORE_R - BORE_L - 6}" height="{PISTON_H}" rx="6" fill="none" '
             f'stroke="{k["accent"]}" stroke-width="3" stroke-dasharray="10 8"/></g>')
    arc_r = 160
    arc = (f'<path id="{s}-arc" d="M{CX},{CY - arc_r} A{arc_r},{arc_r} 0 0,1 {CX},{CY + arc_r}" fill="none" stroke="{k["accent"]}" stroke-width="6" '
           f'marker-end="url(#{s}-arr)" stroke-dasharray="{math.pi * arc_r:.0f}" stroke-dashoffset="{math.pi * arc_r:.0f}" opacity="0"/>'
           f'<g id="{s}-arct" opacity="0">{_card(f"{s}-arcc", k, "½ Umdrehung" if c.lang == "de" else "½ turn", "l", CY + 20)}</g>')
    inner = (f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{parts}{lab}{ghost}{arc}{_stroke_dims(s, k, c.lang)}</g>'
             + _title(c, d, k, problems) + strip_svg(s, k, c.lang))
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    tl.append(f'tl.set("#{s}-arcc",{{opacity:1}},{c.start:.3f});')
    ev = [c.start]
    for i in range(4):
        t = c.start + 0.25 + 0.2 * i
        tl.append(_show(f"#{s}-xl{i}", t, 0.25))
        ev.append(t)
    t_as = at_time(c, d, d.get("assemble_at", 0.3))
    for i in range(4):
        tl.append(f'tl.to("#{s}-xl{i}",{{opacity:0,duration:0.25}},{t_as - 0.1:.3f});')
    for part in ("piston", "rod", "crank"):
        tl.append(f'tl.to("#{s}-x{part}",{{attr:{{transform:"translate(0,0)"}},duration:0.9,ease:"power2.inOut"}},{t_as:.3f});')
    tl.append(f'tl.to("#{s}-liner",{{opacity:0.75,duration:0.6,ease:"power2.out"}},{t_as + 0.4:.3f});')
    ev += [t_as, t_as + 0.9]
    if d.get("title"):
        tl.append(_show(f"#{s}-ttl", c.start + 0.1, 0.3, 10))
    track = Track.from_data(c, d, (0.0, 360.0))
    smp = track.samples(6.0, extra=[180.0])
    rods = f"#{s}-rod,#{s}-rodhi"
    tl += _kf(f"#{s}-piston", smp, lambda a: f"translate(0,{pin_y(a) - PIN_TDC:.2f})", "transform")
    tl += _kf(f"#{s}-crank", smp, lambda a: f"rotate({a:.2f} {CX} {CY})", "transform")
    tl += _kf(rods, smp, lambda a: f"{pin_y(a):.2f}", "y1")
    tl += _kf(rods, smp, lambda a: f"{crank_pin(a)[0]:.2f}", "x2")
    tl += _kf(rods, smp, lambda a: f"{crank_pin(a)[1]:.2f}", "y2")
    t_dims = at_time(c, d, d.get("dims_at", 0.6))
    tl.append(_show(f"#{s}-dims", t_dims, 0.3))
    tl.append(_show(f"#{s}-ghost", t_dims, 0.3))
    ev.append(t_dims)
    half = track.times_at(180.0)
    t_turn = max([t for t, a in track.k if a <= track.k[0][1]] or [track.t0])     # rotation starts after the last rest knot
    if half:
        tl.append(f'tl.set("#{s}-arc",{{opacity:1}},{t_turn:.3f});')
        tl.append(f'tl.to("#{s}-arc",{{attr:{{"stroke-dashoffset":0}},duration:{max(0.2, half[0] - t_turn):.3f},ease:"none"}},{t_turn:.3f});')
        tl.append(_show(f"#{s}-arct", half[0], 0.25))
        ev += [t_turn, half[0]]
    a, b = strip_anim(s, k, track)
    tl += a
    if d.get("count_at"):
        t_c = at_time(c, d, d["count_at"])
        tl += strip_count(s, k, t_c)
        ev.append(t_c)
    return _out(c, inner, k, tl, ev, problems)


# 4. timing drive (Steuertrieb) -----------------------------------------------------------------------

def _belt_path(c1, r1, c2, r2) -> tuple[str, float]:
    """Open belt around two pulleys on a vertical line (c1 above c2). Returns path and its length."""
    (x1, y1), (x2, y2) = c1, c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    vx, vy = dx / d, dy / d
    k = (r1 - r2) / d
    h = math.sqrt(1 - k * k)
    nr = (k * vx - h * vy, k * vy + h * vx)      # right-hand tangent normal (screen)
    nl = (k * vx + h * vy, k * vy - h * vx)
    if nr[0] < 0:
        nr, nl = nl, nr
    p1r = (x1 + r1 * nr[0], y1 + r1 * nr[1])
    p2r = (x2 + r2 * nr[0], y2 + r2 * nr[1])
    p2l = (x2 + r2 * nl[0], y2 + r2 * nl[1])
    p1l = (x1 + r1 * nl[0], y1 + r1 * nl[1])
    path = (f"M{p1r[0]:.1f},{p1r[1]:.1f} L{p2r[0]:.1f},{p2r[1]:.1f} A{r2},{r2} 0 0,1 {p2l[0]:.1f},{p2l[1]:.1f} "
            f"L{p1l[0]:.1f},{p1l[1]:.1f} A{r1},{r1} 0 1,1 {p1r[0]:.1f},{p1r[1]:.1f} Z")
    return path, 0.0


def _sprocket(sid: str, gid: str, cx: float, cy: float, r: float, teeth: int, k: dict, color: str, cam: bool = False) -> str:
    out = [f'<g id="{gid}" transform="rotate(0 {cx} {cy})">',
           f'<circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="url(#{sid}-gface)" stroke="{k["steel"]}" stroke-width="4"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="{k["hairline"]}" stroke-width="3"/>']
    for i in range(teeth):
        a = 360 * i / teeth
        out.append(f'<rect x="{cx - 5:.1f}" y="{cy - r - 4:.1f}" width="10" height="14" fill="{k["steel"]}" transform="rotate({a:.2f} {cx} {cy})"/>')
    for i in range(5 if cam else 3):     # lightening holes
        a = math.radians(90 + 360 * i / (5 if cam else 3))
        out.append(f'<circle cx="{cx + r * 0.4 * math.cos(a):.1f}" cy="{cy + r * 0.4 * math.sin(a):.1f}" r="{r * 0.1:.1f}" fill="{k["bg"]}" stroke="{k["hairline"]}" stroke-width="2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy - r + 26}" r="11" fill="{color}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="{k["bg"]}" stroke="{k["steel"]}" stroke-width="3"/></g>')
    return "".join(out)


def timing_drive(c: SceneCtx, d: dict) -> SceneOut:
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    cam_c, cam_r = (540, 600), 170.0
    cr_c, cr_r = (540, 1010), 85.0
    belt, _ = _belt_path(cam_c, cam_r, cr_c, cr_r)
    zc, zk = int(d.get("teeth_crank", 20)), int(d.get("teeth_cam", 40))
    lang = c.lang
    t_crank, t_cam = ("Kurbelwelle", "Nockenwelle") if lang == "de" else ("Crankshaft", "Camshaft")
    teeth_w = "Zähne" if lang == "de" else "teeth"
    note = d.get("note", "Zähnezahlen: Beispiel" if lang == "de" else "Tooth counts: example")
    _check(problems, "line", "note", note)
    pitch = 2 * math.pi * cr_r / zc
    track = Track.from_data(c, d, (0.0, 720.0))
    total = track.angle(track.t1) - track.angle(track.t0)
    crank_revs = int(round(total / 360))
    cam_vals = ["0", "½", "1", "1½", "2"]
    cards = []
    for (x0, y0, lab, pre, tid, z, acc) in ((108, 448, t_cam, "cc", "tc", zk, " acc"), (690, 862, t_crank, "kc", "tk", zc, "")):
        cards.append(f'<rect x="{x0}" y="{y0}" width="228" height="290" rx="16" fill="{k["surface"]}" fill-opacity="0.94" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="2"/>'
                     f'<text class="cnt-l" x="{x0 + 114}" y="{y0 + 48}" text-anchor="middle">{lab}</text>'
                     f'<line x1="{x0 + 24}" y1="{y0 + 70}" x2="{x0 + 204}" y2="{y0 + 70}" stroke="{k["hairline"]}" stroke-width="2"/>'
                     f'<text id="{s}-{tid}" class="note" x="{x0 + 114}" y="{y0 + 262}" text-anchor="middle">{z} {teeth_w}</text>')
        for n in range(crank_revs + 1):
            val = cam_vals[min(n, 4)] if pre == "cc" else str(n)
            cards.append(f'<text id="{s}-{pre}{n}" class="cnt-m{acc}" x="{x0 + 114}" y="{y0 + 196}" text-anchor="middle" opacity="{1 if n == 0 else 0}">{val} U</text>')
    cards.append(f'<rect id="{s}-halfr" x="108" y="448" width="228" height="290" rx="16" fill="none" stroke="{k["accent"]}" stroke-width="4" opacity="0"/>')
    inner = [f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">',
             f'<ellipse cx="540" cy="1150" rx="220" ry="18" fill="#04060A" fill-opacity="0.5" filter="url(#{s}-blur)"/>',
             f'<g filter="url(#{s}-sh)">',
             f'<path d="{belt}" fill="none" stroke="#262E37" stroke-width="18"/>',
             f'<path id="{s}-belt" d="{belt}" fill="none" stroke="{k["steel"]}" stroke-width="7" stroke-dasharray="{pitch * 0.42:.1f} {pitch * 0.58:.1f}" stroke-dashoffset="0"/>',
             _sprocket(s, f"{s}-spc", cam_c[0], cam_c[1], cam_r, zk, k, k["accent"], cam=True),
             _sprocket(s, f"{s}-spk", cr_c[0], cr_c[1], cr_r, zc, k, k["accent"]),
             '</g>',
             f'<polygon points="{cam_c[0] - 14},{cam_c[1] - cam_r - 38} {cam_c[0] + 14},{cam_c[1] - cam_r - 38} {cam_c[0]},{cam_c[1] - cam_r - 16}" fill="{k["text"]}"/>',
             f'<polygon points="{cr_c[0] - 14},{cr_c[1] - cr_r - 38} {cr_c[0] + 14},{cr_c[1] - cr_r - 38} {cr_c[0]},{cr_c[1] - cr_r - 16}" fill="{k["text"]}"/>',
             "".join(cards), '</g>',
             f'<text id="{s}-note" class="note" x="540" y="1150" text-anchor="middle" opacity="0">{_e(note)}</text>' if note else ""]
    if d.get("title"):
        inner.append(_title(c, d, k, problems))
    if d.get("strip", True):
        inner.append(strip_svg(s, k, lang))
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    ev = [c.start]
    a0 = track.angle(track.t0)
    smp = track.samples(6.0)
    tl += _kf(f"#{s}-spk", smp, lambda a: f"rotate({a - a0:.2f} {cr_c[0]} {cr_c[1]})", "transform")
    tl += _kf(f"#{s}-spc", smp, lambda a: f"rotate({(a - a0) / 2:.2f} {cam_c[0]} {cam_c[1]})", "transform")
    # belt moves along the path with the crank sprocket's pitch speed
    tl += _kf(f"#{s}-belt", smp, lambda a: f"{-math.radians(a - a0) * cr_r:.2f}", "stroke-dashoffset")
    rev_times = [tt for tt in track.times_at(a0 % 360, 360.0) if tt > track.t0 + 1e-3][:crank_revs]
    for n, t in enumerate(rev_times, start=1):
        for p in ("kc", "cc"):
            tl.append(f'tl.set("#{s}-{p}{n - 1}",{{opacity:0}},{t:.3f});')
            tl.append(f'tl.set("#{s}-{p}{n}",{{opacity:1}},{t:.3f});')
        ev.append(t)
    t_note = at_time(c, d, d.get("note_at", 0.6))
    if note:
        tl.append(_show(f"#{s}-note", t_note, 0.3))
    else:   # no own example note (explainer chip "Beispielwert"): the tooth counts light up at the spoken word
        tl.append(f'tl.to(["#{s}-tc","#{s}-tk"],{{fill:"{k["accent"]}",duration:0.3}},{t_note:.3f});')
    ev.append(t_note)
    if d.get("half_at"):      # "halber Drehzahl": the cam card frame lights up
        t_h = at_time(c, d, d["half_at"])
        tl.append(f'tl.fromTo("#{s}-halfr",{{opacity:0}},{{opacity:1,duration:0.3}},{t_h:.3f});')
        ev.append(t_h)
    if d.get("title"):
        t = at_time(c, d, d.get("title_at", 0.0))
        tl.append(_show(f"#{s}-ttl", t + 0.05, 0.3, 10))
    if d.get("strip", True):
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    return _out(c, "".join(inner), k, tl, ev, problems)


# 5. readout (Messwert und Rechnung) ------------------------------------------------------------------

def readout(c: SceneCtx, d: dict) -> SceneOut:
    """Rev counter with needle, then computed lines appear at their spoken words."""
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    gx, gy, gr = 540, 690, 300
    vmax = float(d.get("gauge_max", 7))
    val = float(d.get("gauge_value", 3))
    unit = d.get("gauge_unit", "× 1000/min")

    def pt(v, r):
        a = math.radians(225 - 270 * v / vmax)
        return gx + r * math.cos(a), gy - r * math.sin(a)

    g = [f'<ellipse cx="{gx}" cy="{gy + gr + 40}" rx="280" ry="20" fill="#04060A" fill-opacity="0.5" filter="url(#{s}-blur)"/>',
         f'<g filter="url(#{s}-sh)"><circle cx="{gx}" cy="{gy}" r="{gr + 22}" fill="url(#{s}-gface)" stroke="{k["steel"]}" stroke-opacity="0.5" stroke-width="3"/></g>',
         f'<path d="M{pt(0, gr)[0]:.1f},{pt(0, gr)[1]:.1f} A{gr},{gr} 0 1,1 {pt(vmax, gr)[0]:.1f},{pt(vmax, gr)[1]:.1f}" fill="none" stroke="{k["hairline"]}" stroke-width="12"/>',
         f'<path id="{s}-garc" d="M{pt(0, gr)[0]:.1f},{pt(0, gr)[1]:.1f} A{gr},{gr} 0 0,1 {pt(val, gr)[0]:.1f},{pt(val, gr)[1]:.1f}" fill="none" stroke="{k["accent"]}" stroke-width="12" '
         f'stroke-dasharray="{math.radians(270 * val / vmax) * gr:.1f}" stroke-dashoffset="{math.radians(270 * val / vmax) * gr:.1f}"/>']
    for i in range(int(vmax) + 1):
        a1, a2 = pt(i, gr - 10), pt(i, gr - 48)
        lx, ly = pt(i, gr - 90)
        g.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}" stroke="{k["steel"]}" stroke-width="6"/>')
        g.append(f'<text class="tick" x="{lx:.1f}" y="{ly + 13:.1f}" text-anchor="middle">{i}</text>')
        if i < vmax:
            m1, m2 = pt(i + 0.5, gr - 10), pt(i + 0.5, gr - 30)
            g.append(f'<line x1="{m1[0]:.1f}" y1="{m1[1]:.1f}" x2="{m2[0]:.1f}" y2="{m2[1]:.1f}" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="3"/>')
    g.append(f'<text class="note" x="{gx}" y="{gy + 210}" text-anchor="middle">{_e(unit)}</text>')
    g.append(f'<g id="{s}-needle" transform="rotate({-135} {gx} {gy})"><line x1="{gx}" y1="{gy + 34}" x2="{gx}" y2="{gy - gr + 52}" stroke="{k["accent"]}" stroke-width="9" stroke-linecap="round"/>'
             f'<circle cx="{gx}" cy="{gy}" r="24" fill="{k["accent"]}"/><circle cx="{gx}" cy="{gy}" r="9" fill="{k["bg"]}"/></g>')
    fig = d.get("figure", "gauge")
    fig_tl: list[str] = []
    if fig == "bars":
        bars = d.get("bars", [])
        bmax = float(d.get("bar_max") or max(abs(float(b["value"])) for b in bars))
        g = []
        for i, b in enumerate(bars):
            y = 500 + i * 125
            w = 640 * abs(float(b["value"])) / bmax
            col = {"accent": k["accent"], "fire": k["fire"], "exhaust": k["exhaust"], "steel": k["steel"]}.get(b.get("color", "accent"), k["accent"])
            _check(problems, "line", f"bar {i}", b.get("label", ""))
            g.append(f'<text class="lbl" x="120" y="{y}">{_e(b.get("label", ""))}</text>'
                     f'<rect x="120" y="{y + 18}" width="800" height="52" rx="10" fill="{k["surface"]}" fill-opacity="0.8"/>'
                     f'<rect id="{s}-bar{i}" x="120" y="{y + 18}" width="0" height="52" rx="10" fill="{col}"/>'
                     + (f'<text id="{s}-bv{i}" class="bar-v" x="{120 + w + 18:.0f}" y="{y + 60}" opacity="0">{_e(b.get("text", b["value"]))}</text>' if w < 470 else
                        f'<text id="{s}-bv{i}" class="bar-v" x="{120 + w - 18:.0f}" y="{y + 60}" text-anchor="end" fill="{k["bg"]}" opacity="0">{_e(b.get("text", b["value"]))}</text>'))
            t = at_time(c, d, b.get("at", 0.2 + 0.15 * i))
            fig_tl.append(f'tl.to("#{s}-bar{i}",{{attr:{{width:{w:.1f}}},duration:0.8,ease:"power2.out"}},{t:.3f});')
            fig_tl.append(_show(f"#{s}-bv{i}", t + 0.5, 0.3))
            ev_fig = t
        figure_events = [at_time(c, d, b.get("at", 0.2 + 0.15 * i)) for i, b in enumerate(bars)]
    elif fig == "cylinder":
        top, h, x0c, x1c = 470, 300, 400, 680
        trk = Track.from_data(c, d, (0.0, 360.0))
        py = lambda a: top + 10 + (pin_y(a) - PIN_TDC) / (2 * R) * h
        bl, sl = d.get("bore_label", "Bohrung B" if c.lang == "de" else "Bore B"), d.get("stroke_label", "Hub S" if c.lang == "de" else "Stroke S")
        g = [f'<rect x="{x0c - 26}" y="{top - 20}" width="26" height="{h + 150}" fill="url(#{s}-hatch)" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="{x1c}" y="{top - 20}" width="26" height="{h + 150}" fill="url(#{s}-hatch)" stroke="{k["hairline"]}" stroke-width="2"/>'
             f'<rect x="{x0c - 40}" y="{top - 46}" width="{x1c - x0c + 80}" height="26" fill="url(#{s}-hatch)" stroke="{k["hairline"]}" stroke-width="2"/>',
             f'<rect id="{s}-swept" x="{x0c}" y="{top + 10}" width="{x1c - x0c}" height="{h}" fill="{k["accent"]}" fill-opacity="0.22" opacity="0"/>',
             f'<g id="{s}-cpis" transform="translate(0,0)"><rect x="{x0c + 2}" y="{top + 10}" width="{x1c - x0c - 4}" height="96" rx="6" fill="url(#{s}-gsteel)"/></g>',
             f'<g id="{s}-dimb" opacity="0"><line x1="{x0c + 6}" y1="{top - 80}" x2="{x1c - 6}" y2="{top - 80}" stroke="{k["accent"]}" stroke-width="5" marker-start="url(#{s}-arr)" marker-end="url(#{s}-arr)"/>'
             f'<text class="lbl" x="{(x0c + x1c) / 2}" y="{top - 100}" text-anchor="middle">{_e(bl)}</text></g>',
             f'<g id="{s}-dims2" opacity="0"><line x1="{x1c + 70}" y1="{top + 16}" x2="{x1c + 70}" y2="{top + h + 4}" stroke="{k["accent"]}" stroke-width="5" marker-start="url(#{s}-arr)" marker-end="url(#{s}-arr)"/>'
             f'<text class="lbl" x="{x1c + 92}" y="{top + h / 2 + 10}">{_e(sl)}</text></g>']
        smp = trk.samples(6.0)
        fig_tl += _kf(f"#{s}-cpis", smp, lambda a: f"translate(0,{py(a) - top - 10:.1f})", "transform")
        figure_events = []
        for key, sel in (("bore_at", f"#{s}-dimb"), ("stroke_at", f"#{s}-dims2"), ("fill_at", f"#{s}-swept")):
            if d.get(key) is not None:
                t = at_time(c, d, d[key])
                fig_tl.append(_show(sel, t, 0.3))
                figure_events.append(t)
    else:
        figure_events = []
    lines = d.get("lines", [])
    out_lines = []
    for i, ln in enumerate(lines):
        _check(problems, "line", f"line {i}", ln.get("text", ""))
        y = int(d.get("lines_y", 1060)) + i * 78
        txt = _e(ln.get("text", ""))
        if ln.get("hl"):
            txt = txt.replace(_e(ln["hl"]), f'<tspan class="acc">{_e(ln["hl"])}</tspan>')
        out_lines.append(f'<g id="{s}-ln{i}" opacity="0"><rect x="120" y="{y - 50}" width="798" height="68" rx="12" fill="{k["surface"]}" fill-opacity="0.9" stroke="{k["hairline"]}" stroke-width="2"/>'
                         f'<text class="line" x="540" y="{y}" text-anchor="middle">{txt}</text></g>')
    big = d.get("big", {})
    if big:
        _check(problems, "big", "big", big.get("text", ""))
        out_lines.append(f'<text id="{s}-big" class="big" x="540" y="{gy + 40}" text-anchor="middle" opacity="0">{_e(big.get("text", ""))}</text>')
    inner = f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{"".join(g)}{"".join(out_lines)}</g>' + _title(c, d, k, problems)
    if d.get("strip", True):
        inner += strip_svg(s, k, c.lang)
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    ev = [c.start]
    if fig == "gauge":
        t_v = at_time(c, d, d.get("gauge_at", 0.1))
        tl.append(f'tl.to("#{s}-needle",{{attr:{{transform:"rotate({-135 + 270 * val / vmax:.1f} {gx} {gy})"}},duration:0.9,ease:"power2.out"}},{t_v:.3f});')
        tl.append(f'tl.to("#{s}-garc",{{attr:{{"stroke-dashoffset":0}},duration:0.9,ease:"power2.out"}},{t_v:.3f});')
        ev += [t_v, t_v + 0.9]
    else:
        tl += fig_tl
        ev += figure_events
    for i, ln in enumerate(lines):
        t = at_time(c, d, ln.get("at", 0.3 + 0.2 * i))
        tl.append(_show(f"#{s}-ln{i}", t, 0.3, 10))
        ev.append(t)
    if big:
        t = at_time(c, d, big.get("at", 0.8))
        tl.append(f'tl.to("#{s}-needle",{{opacity:0.15,duration:0.3}},{t:.3f});')
        tl.append(f'tl.fromTo("#{s}-big",{{opacity:0,scale:0.9,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{t:.3f});')
        ev.append(t)
    if d.get("title"):
        tl.append(_show(f"#{s}-ttl", c.start + 0.1, 0.3, 10))
    if d.get("strip", True):
        track = Track.from_data(c, d, (0.0, 360.0))
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    return _out(c, inner, k, tl, ev, problems)

# 6. chart (Diagramm über dem Kurbelwinkel oder dem Volumen) -----------------------------------------------

def _pv_points(r: float = 10.0, rise: float = 3.0, n: int = 90) -> dict:
    """Ideal constant-volume cycle (schematic): volume from the real slider-crank, pressure polytropic (gamma 1.4)."""
    vc = 1.0 / (r - 1.0)
    vol = lambda a: vc + (pin_y(a) - PIN_TDC) / (2 * R)
    comp = [(vol(180 + 180 * i / n), (vol(180) / vol(180 + 180 * i / n)) ** 1.4) for i in range(n + 1)]
    p2 = comp[-1][1]
    p3 = p2 * rise
    exp_ = [(vol(180 * i / n), p3 * (vc / vol(180 * i / n)) ** 1.4) for i in range(n + 1)]
    return {"comp": comp, "burn": [(vc, p2), (vc, p3)], "exp": exp_, "blow": [exp_[-1], (vol(180), 1.0)],
            "pmax": p3, "vmax": vol(180)}


def _motored(a: float, r: float = 10.0) -> float:
    vc = 1.0 / (r - 1.0)
    return ((vc + 1.0) / (vc + (pin_y(a) - PIN_TDC) / (2 * R))) ** 1.35


def _fired(a: float, spark: float, q: float = 2.2, dur: float = 60.0) -> float:
    xb = 0.0 if a <= spark else 1.0 - math.exp(-5.0 * ((a - spark) / dur) ** 3)
    return _motored(a) * (1.0 + q * xb)


def _chart_data(c: SceneCtx, d: dict, k: dict) -> dict:
    kind = d.get("kind", "custom")
    de = c.lang == "de"
    out = {"series": [], "xticks": [], "xlabel": "", "ylabel": "", "scheme": True}
    if kind == "piston_speed":
        xs = [i * 3.0 for i in range(121)]
        out.update(xlim=(0, 360), ylim=(-1.25, 1.25), xlabel="Kurbelwinkel" if de else "Crank angle",
                   ylabel="Kolbengeschwindigkeit" if de else "Piston speed", scheme=False,
                   xticks=[(0, "OT" if de else "TDC"), (90, "90°"), (180, "UT" if de else "BDC"), (270, "270°"), (360, "OT" if de else "TDC")])
        out["series"] = [{"label": "Sinus" if de else "Sine", "pts": [(x, math.sin(math.radians(x))) for x in xs], "color": k["steel"], "dash": "10 9"},
                         {"label": "Kurbeltrieb" if de else "Slider-crank", "pts": [(x, piston_velocity(x) / R) for x in xs], "color": k["accent"]}]
    elif kind == "valve_lift":
        xs = [-180 + i * 4.0 for i in range(181)]
        out.update(xlim=(-180, 540), ylim=(0, LIFT_MAX * 1.35), xlabel="Kurbelwinkel" if de else "Crank angle",
                   ylabel="Ventilhub" if de else "Valve lift", scheme=False,
                   xticks=[(-180, "UT" if de else "BDC"), (0, "OT" if de else "TDC"), (180, "UT" if de else "BDC"), (360, "OT" if de else "TDC"), (540, "UT" if de else "BDC")])
        out["series"] = [{"label": "Auslass" if de else "Exhaust", "pts": [(x, lift_ex(x)) for x in xs], "color": k["exhaust"]},
                         {"label": "Einlass" if de else "Intake", "pts": [(x, lift_in(x)) for x in xs], "color": k["accent"]}]
    elif kind == "pv":
        pv = _pv_points(float(d.get("r", 10)))
        out.update(xlim=(0, pv["vmax"] * 1.08), ylim=(0, pv["pmax"] * 1.08), xlabel="Volumen" if de else "Volume", ylabel="Druck" if de else "Pressure",
                   xticks=[(1.0 / (float(d.get("r", 10)) - 1.0), "OT" if de else "TDC"), (pv["vmax"], "UT" if de else "BDC")])
        out["series"] = [{"label": "Verdichten" if de else "Compression", "pts": pv["comp"], "color": k["accent"]},
                         {"label": "Verbrennen" if de else "Combustion", "pts": pv["burn"], "color": k["fire"]},
                         {"label": "Arbeiten" if de else "Expansion", "pts": pv["exp"], "color": k["fire"]},
                         {"label": "Ausstoßen" if de else "Exhaust", "pts": pv["blow"], "color": k["exhaust"]}]
        out["area"] = pv["comp"] + pv["exp"]
    elif kind == "pressure":
        xs = [-60 + i * 1.5 for i in range(101)]
        cases = d.get("cases") or [{"spark": -30}]
        pmax = max(_fired(x, cc["spark"]) for cc in cases for x in xs)
        out.update(xlim=(-60, 90), ylim=(0, pmax * 1.1), xlabel="Kurbelwinkel" if de else "Crank angle", ylabel="Zylinderdruck" if de else "Cylinder pressure",
                   xticks=[(-60, "-60°"), (-30, "-30°"), (0, "OT" if de else "TDC"), (30, "30°"), (60, "60°"), (90, "90°")])
        out["series"] = [{"label": "ohne Zündung" if de else "no ignition", "pts": [(x, _motored(x)) for x in xs], "color": k["muted"], "dash": "8 8"}]
        cols = {"accent": k["accent"], "steel": k["steel"], "muted": k["muted"], "fire": k["fire"]}
        for cc in cases:
            out["series"].append({"label": cc.get("label", ""), "pts": [(x, _fired(x, cc["spark"])) for x in xs],
                                  "color": cols.get(cc.get("color", "accent"), k["accent"]), "dash": cc.get("dash")})
    elif kind == "hrr":      # diesel heat release, schematic: ignition delay, premixed peak, mixing-controlled, late
        xs = [-10 + i * 0.5 for i in range(121)]
        f = lambda x: 0.0 if x < 0 else (1.0 * math.exp(-((x - 3.0) / 2.2) ** 2) + 0.42 * math.exp(-((x - 14.0) / 8.0) ** 2)
                                         + (0.08 * math.exp(-(x - 24.0) / 10.0) if x > 24 else 0.0))
        out.update(xlim=(-10, 50), ylim=(0, 1.15), xlabel="Kurbelwinkel" if de else "Crank angle", ylabel="Wärmefreisetzung" if de else "Heat release",
                   xticks=[(-10, "-10°"), (0, "OT" if de else "TDC"), (10, "10°"), (20, "20°"), (30, "30°"), (40, "40°"), (50, "50°")])
        out["series"] = [{"label": "", "pts": [(x, f(x)) for x in xs], "color": k["fire"]}]
    else:
        out.update(xlim=tuple(d["xlim"]), ylim=tuple(d["ylim"]), xlabel=d.get("xlabel", ""), ylabel=d.get("ylabel", ""),
                   xticks=[tuple(t) for t in d.get("xticks", [])], scheme=d.get("scheme", True))
        out["series"] = [{"label": sr.get("label", ""), "pts": [tuple(p) for p in sr["pts"]], "color": k.get(sr.get("color", "accent"), k["accent"]),
                          "dash": sr.get("dash")} for sr in d.get("series", [])]
    return out


def chart(c: SceneCtx, d: dict) -> SceneOut:
    """Animated line chart: series draw at their spoken words, vertical marks and shaded bands appear at words, an
    optional dot follows the crank angle, an optional small engine above runs in sync (`engine: true`)."""
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    cd = _chart_data(c, d, k)
    small = bool(d.get("engine"))
    x0, x1 = 190, 900
    y0, y1 = (800, 1110) if small else (470, 1060)
    (ax0, ax1), (ay0, ay1) = cd["xlim"], cd["ylim"]
    X = lambda x: x0 + (x - ax0) / (ax1 - ax0) * (x1 - x0)
    Y = lambda y: y1 - (y - ay0) / (ay1 - ay0) * (y1 - y0)
    g = [f'<rect x="{x0 - 30}" y="{y0 - 60}" width="{x1 - x0 + 50}" height="{y1 - y0 + 120}" rx="18" fill="{k["surface"]}" fill-opacity="0.82" stroke="{k["steel"]}" stroke-opacity="0.3" stroke-width="2"/>']
    for gy in (0.25, 0.5, 0.75):
        g.append(f'<line x1="{x0}" y1="{y0 + gy * (y1 - y0):.0f}" x2="{x1}" y2="{y0 + gy * (y1 - y0):.0f}" stroke="{k["hairline"]}" stroke-width="1.5"/>')
    if ay0 < 0 < ay1:
        g.append(f'<line x1="{x0}" y1="{Y(0):.1f}" x2="{x1}" y2="{Y(0):.1f}" stroke="{k["steel"]}" stroke-opacity="0.6" stroke-width="2"/>')
    g.append(f'<path d="M{x0},{y0 - 10} L{x0},{y1} L{x1 + 6},{y1}" fill="none" stroke="{k["steel"]}" stroke-width="3"/>')
    for xv, lab in cd["xticks"]:
        g.append(f'<line x1="{X(xv):.1f}" y1="{y1}" x2="{X(xv):.1f}" y2="{y1 + 12}" stroke="{k["steel"]}" stroke-width="3"/>'
                 f'<text class="tick-s" x="{X(xv):.1f}" y="{y1 + 46}" text-anchor="middle">{_e(lab)}</text>')
    g.append(f'<text class="axis-t" x="{x0}" y="{y0 - 24}">{_e(cd["ylabel"])}</text>')
    g.append(f'<text class="axis-t" x="{x1}" y="{y0 - 24}" text-anchor="end">{_e(cd["xlabel"])}</text>')
    if cd.get("scheme"):
        g.append(f'<text class="axis-t" x="{x1}" y="{y1 - 16}" text-anchor="end">Schema</text>' if c.lang == "de" else
                 f'<text class="axis-t" x="{x1}" y="{y1 - 16}" text-anchor="end">Schematic</text>')
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    ev = [c.start]
    # bands (behind the curves)
    cols = {"accent": k["accent"], "fire": k["fire"], "exhaust": k["exhaust"], "steel": k["steel"], "amber": "#F5B342"}
    for i, b in enumerate(d.get("bands", [])):
        bx0, bx1 = X(b["x0"]), X(b["x1"])
        col = cols.get(b.get("color", "accent"), k["accent"])
        g.append(f'<g id="{s}-bd{i}" opacity="0"><rect x="{bx0:.1f}" y="{y0}" width="{bx1 - bx0:.1f}" height="{y1 - y0}" fill="{col}" fill-opacity="0.16"/>'
                 f'<line x1="{bx0:.1f}" y1="{y0}" x2="{bx0:.1f}" y2="{y1}" stroke="{col}" stroke-width="2" stroke-dasharray="6 6"/>'
                 f'<line x1="{bx1:.1f}" y1="{y0}" x2="{bx1:.1f}" y2="{y1}" stroke="{col}" stroke-width="2" stroke-dasharray="6 6"/>'
                 + (f'<text class="band-t" x="{(bx0 + bx1) / 2:.1f}" y="{y0 + 38 + 40 * b.get("row", 0)}" text-anchor="middle">{_e(b["label"])}</text>' if b.get("label") else "")
                 + '</g>')
        t = at_time(c, d, b.get("at", 0.4))
        tl.append(_show(f"#{s}-bd{i}", t, 0.3))
        ev.append(t)
    if cd.get("area"):
        pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in cd["area"])
        g.append(f'<polygon id="{s}-area" points="{pts}" fill="{k["accent"]}" fill-opacity="0.22" opacity="0"/>')
        t = at_time(c, d, d.get("area_at", 0.8))
        tl.append(_show(f"#{s}-area", t, 0.4))
        ev.append(t)
    # series
    ats = d.get("series_at", [])
    legend_y = y0 + 6
    only = d.get("series_only")      # indices of the series to show (e.g. only the compression line)
    for i, sr in enumerate(cd["series"]):
        if only is not None and i not in only:
            continue
        pts = [(X(x), Y(y)) for x, y in sr["pts"]]
        ln = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])) + 1
        path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        g.append(f'<path id="{s}-sr{i}" d="{path}" fill="none" stroke="{sr["color"]}" stroke-width="{6 if not sr.get("dash") else 4}" stroke-linejoin="round" '
                 f'stroke-linecap="round" stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>')
        if sr.get("dash"):
            g.append(f'<path id="{s}-srd{i}" d="{path}" fill="none" stroke="{k["surface"]}" stroke-width="5" stroke-dasharray="{sr["dash"]}" opacity="0"/>')
        t = at_time(c, d, ats[i] if i < len(ats) else 0.1 + 0.12 * i)
        dur = float(d.get("draw_seconds", 1.2))
        tl.append(f'tl.to("#{s}-sr{i}",{{attr:{{"stroke-dashoffset":0}},duration:{dur:.2f},ease:"power1.inOut"}},{t:.3f});')
        if sr.get("dash"):
            tl.append(f'tl.set("#{s}-srd{i}",{{opacity:1}},{t:.3f});')
        ev.append(t)
        if sr.get("label") and d.get("legend", True):
            lx, ly = (560, 430 + 56 * i) if small else (x1 - 250, legend_y + 40 * i)
            g.append(f'<g id="{s}-lg{i}" opacity="0"><rect x="{lx}" y="{ly}" width="34" height="10" rx="4" fill="{sr["color"]}"/>'
                     f'<text class="{"leg-b" if small else "leg-t"}" x="{lx + 48}" y="{ly + 14}">{_e(sr["label"])}</text></g>')
            tl.append(_show(f"#{s}-lg{i}", t, 0.3))
    # vertical marks
    for i, m in enumerate(d.get("marks", [])):
        mx = X(m["x"])
        col = cols.get(m.get("color", "accent"), k["accent"])
        g.append(f'<g id="{s}-mk{i}" opacity="0"><line x1="{mx:.1f}" y1="{y0 - 6}" x2="{mx:.1f}" y2="{y1}" stroke="{col}" stroke-width="3" stroke-dasharray="8 6"/>'
                 + (f'<text class="mark-t" x="{mx + (10 if m.get("side", "r") == "r" else -10):.1f}" y="{y0 + 30 + 40 * m.get("row", 0)}" text-anchor="{"start" if m.get("side", "r") == "r" else "end"}" fill="{col}">{_e(m["label"])}</text>' if m.get("label") else "")
                 + '</g>')
        t = at_time(c, d, m.get("at", 0.5))
        tl.append(_show(f"#{s}-mk{i}", t, 0.3))
        ev.append(t)
    track = Track.from_data(c, d, (0.0, 360.0))
    # dot following the crank angle along the last series (crank-angle charts only)
    if d.get("dot") and d.get("kind") in ("piston_speed", "valve_lift"):
        sr = cd["series"][-1]
        fn = (lambda a: piston_velocity(a % 360) / R) if d["kind"] == "piston_speed" else lift_in
        xm = (lambda a: a % 360) if d["kind"] == "piston_speed" else (lambda a: ((a + 180) % 720) - 180)
        g.append(f'<circle id="{s}-dot" cx="{X(xm(track.angle(track.t0))):.1f}" cy="{Y(fn(track.angle(track.t0))):.1f}" r="13" fill="{k["text"]}" stroke="{sr["color"]}" stroke-width="5"/>')
        smp = track.samples(4.0)
        tl += _kf(f"#{s}-dot", smp, lambda a: f"{X(xm(a)):.1f}", "cx")
        tl += _kf(f"#{s}-dot", smp, lambda a: f"{Y(fn(a)):.1f}", "cy")
    inner = ""
    if small:
        view = _view(d, (0.46, 352.0))
        v = d.get("view") or {}
        if "x" in v:
            view = (view[0], float(v["x"]) - view[0] * 540, view[2])
        opts = {"fuel": d.get("fuel", "petrol"), "injector": d.get("injector"), "knock": bool(d.get("knock")), "speed": bool(d.get("speed"))}
        inner += _place(view, engine_svg(s, k, **opts))
        a, b = engine_anim(s, k, track, **opts)
        tl += a
        ev += b
        cards, ctl, cev = _callouts(c, d, k, view, problems)
        inner += cards
        tl += ctl
        ev += cev
    inner = f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{inner}{"".join(g)}</g>' + _title(c, d, k, problems)
    if d.get("title"):
        tl.append(_show(f"#{s}-ttl", c.start + 0.1, 0.3, 10))
    if d.get("strip", True):
        inner += strip_svg(s, k, c.lang)
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    return _out(c, inner, k, tl, ev, problems)


# 7. board (Tafel: Geschichte, Gegenüberstellung, Mythos-Urteil) -----------------------------------------

def _rows(s: str, k: dict, rows: list, y0: float, step: float, x: float = 120, w: float = 798, problems=None) -> str:
    out = []
    for i, r in enumerate(rows):
        y = y0 + i * step
        if problems is not None:
            _check(problems, "line", f"row {i}", r.get("text", ""))
        out.append(f'<g id="{s}-rw{i}" opacity="0"><rect x="{x}" y="{y - 46}" width="{w}" height="66" rx="12" fill="{k["surface"]}" fill-opacity="0.92" stroke="{k["hairline"]}" stroke-width="2"/>'
                   f'<rect x="{x + 22}" y="{y - 21}" width="16" height="16" fill="{k["accent"]}"/>'
                   f'<text class="row-t" x="{x + 58}" y="{y}">{_e(r.get("text", ""))}</text></g>')
    return "".join(out)


def board(c: SceneCtx, d: dict) -> SceneOut:
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    mode = d.get("mode", "history")
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    ev = [c.start]
    parts = []
    track = Track.from_data(c, d, (0.0, 360.0))
    rows = d.get("rows", [])
    if mode == "history":
        years = d.get("years") or ([{"year": d["year"], "at": 0.0}] if d.get("year") else [])
        for i, yv in enumerate(years):
            parts.append(f'<text id="{s}-yr{i}" class="year" x="540" y="560" text-anchor="middle" opacity="0">{_e(yv["year"])}</text>')
            t = at_time(c, d, yv.get("at", 0.0))
            if i:
                tl.append(f'tl.to("#{s}-yr{i - 1}",{{opacity:0,duration:0.2}},{t - 0.05:.3f});')
            tl.append(f'tl.fromTo("#{s}-yr{i}",{{opacity:0,scale:0.92,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{t + 0.05:.3f});')
            ev.append(t)
        doc = d.get("doc")
        if doc:
            parts.append(f'<g id="{s}-doc" opacity="0"><rect x="160" y="610" width="760" height="230" rx="10" fill="#E9EDF1"/>'
                         f'<rect x="160" y="610" width="760" height="54" rx="10" fill="#D4DAE1"/>'
                         f'<text class="doc-h" x="190" y="646">{_e(doc.get("head", ""))}</text>'
                         + "".join(f'<text class="doc-t" x="190" y="{716 + 56 * j}">{_e(ln)}</text>' for j, ln in enumerate(doc.get("lines", [])[:2]))
                         + f'<g transform="translate(820,760) rotate(-12)"><circle r="56" fill="none" stroke="{k["accent"]}" stroke-width="5"/>'
                         f'<circle r="44" fill="none" stroke="{k["accent"]}" stroke-width="2"/><text class="doc-s" x="0" y="10" text-anchor="middle">{_e(doc.get("stamp", ""))}</text></g></g>')
            for ln in doc.get("lines", []):
                _check(problems, "line", "doc line", ln)
            t = at_time(c, d, doc.get("at", 0.25))
            tl.append(f'tl.fromTo("#{s}-doc",{{opacity:0,y:30,rotation:-2,transformOrigin:"50% 50%"}},{{opacity:1,y:0,rotation:0,duration:0.5,ease:"power3.out"}},{t:.3f});')
            ev.append(t)
        parts.append(_rows(s, k, rows, 940 if doc else 720, 84, problems=problems))
    elif mode == "compare":
        L, Rr = d.get("left", {}), d.get("right", {})
        for side, col, xc in (("L", L, 300), ("R", Rr, 760)):
            if col.get("engine"):
                e = col["engine"]
                es = f"{s}{side}"
                view = (0.4, xc - 0.4 * 540, 380 - 0.4 * 300)
                opts = {"fuel": e.get("fuel", "petrol"), "injector": e.get("injector"), "knock": bool(e.get("knock")), "speed": False}
                parts.append(_defs(es, k) + _place(view, engine_svg(es, k, **opts)))
                a, b = engine_anim(es, k, track, **opts)
                tl += a
                ev += b
            parts.append(f'<g id="{s}-h{side}" opacity="0"><text class="col-h" x="{xc}" y="{760 if col.get("engine") else 520}" text-anchor="middle">{_e(col.get("title", ""))}</text></g>')
            _check(problems, "chip", f"column {side}", col.get("title", ""))
            t = at_time(c, d, col.get("at", 0.1 if side == "L" else 0.2))
            tl.append(_show(f"#{s}-h{side}", t, 0.3, 10))
            ev.append(t)
            ry0 = 840 if col.get("engine") else 610
            for j, txt in enumerate(col.get("rows", [])):
                _check(problems, "chip", f"cell {side}{j}", txt)
                parts.append(f'<g id="{s}-c{side}{j}" opacity="0"><rect x="{xc - 220}" y="{ry0 + 86 * j - 44}" width="440" height="66" rx="12" fill="{k["surface"]}" fill-opacity="0.92" stroke="{k["hairline"]}" stroke-width="2"/>'
                             f'<text class="cell-t" x="{xc}" y="{ry0 + 86 * j + 2}" text-anchor="middle">{_e(txt)}</text></g>')
        parts.append(f'<line x1="540" y1="{480 if not (L.get("engine") or Rr.get("engine")) else 360}" x2="540" y2="1150" stroke="{k["steel"]}" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="6 10"/>')
        for j, at in enumerate(d.get("rows_at", [])):
            t = at_time(c, d, at)
            tl.append(_show(f"#{s}-cL{j}", t, 0.3, 10))
            tl.append(_show(f"#{s}-cR{j}", t + 0.15, 0.3, 10))
            ev.append(t)
    elif mode == "verdict":
        claim = d.get("claim_lines", [])
        parts.append(f'<g id="{s}-cl" opacity="0">' + "".join(f'<text class="vclaim" x="540" y="{540 + 74 * j}" text-anchor="middle">{_e(ln)}</text>' for j, ln in enumerate(claim))
                     + '</g>' + "".join(f'<line class="{s}-st" x1="170" y1="{520 + 74 * j}" x2="910" y2="{520 + 74 * j}" stroke="{k["text"]}" stroke-width="7" stroke-dasharray="740" stroke-dashoffset="740"/>' for j in range(len(claim)))
                     + ''
                     + f'<g id="{s}-vd" opacity="0" transform="rotate(-5 540 {600 + 74 * len(claim)})"><rect x="330" y="{555 + 74 * len(claim)}" width="420" height="78" rx="12" fill="none" stroke="{k["text"]}" stroke-width="4"/>'
                     f'<text class="vstamp" x="540" y="{608 + 74 * len(claim)}" text-anchor="middle">{_e(d.get("verdict", "Stimmt so nicht" if c.lang == "de" else "Not quite"))}</text></g>')
        for ln in claim:
            _check(problems, "claim", "claim line", ln)
        t = at_time(c, d, d.get("claim_at", 0.05))
        tl.append(_show(f"#{s}-cl", t, 0.35, 12))
        ev.append(t)
        t = at_time(c, d, d.get("verdict_at", 0.4))
        tl.append(f'tl.to(".{s}-st",{{attr:{{"stroke-dashoffset":0}},duration:0.45,ease:"power2.inOut",stagger:0.15}},{t:.3f});')
        tl.append(f'tl.fromTo("#{s}-vd",{{opacity:0,scale:1.25,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t + 0.35:.3f});')
        ev.append(t)
        parts.append(_rows(s, k, rows, 840 + 74 * max(0, len(claim) - 2), 84, problems=problems))
    for i, r in enumerate(rows):
        t = at_time(c, d, r.get("at", 0.5 + 0.12 * i))
        tl.append(_show(f"#{s}-rw{i}", t, 0.3, 12))
        ev.append(t)
    inner = f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{"".join(parts)}</g>' + _title(c, d, k, problems)
    if d.get("title"):
        tl.append(_show(f"#{s}-ttl", c.start + 0.1, 0.3, 10))
    if d.get("strip", True):
        inner += strip_svg(s, k, c.lang)
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    return _out(c, inner, k, tl, ev, problems)


# 8. spark plug (Zündkerze im Schnitt) -----------------------------------------------------------------

PLUG_PARTS = {
    # key: (anchor x, y native, side, card y screen, de, en)
    "terminal": (540, 400, "l", 430, "Anschluss", "Terminal"),
    "insulator": (580, 560, "r", 560, "Isolator", "Insulator"),
    "resistor": (540, 560, "l", 600, "Widerstand", "Resistor"),
    "hex": (612, 680, "r", 720, "Gehäuse", "Shell"),
    "gasket": (606, 766, "r", 820, "Dichtring", "Gasket"),
    "thread": (592, 840, "r", 920, "Gewinde", "Thread"),
    "nose": (530, 860, "l", 880, "Isolatorfuß", "Insulator nose"),
    "center": (540, 900, "l", 1000, "Mittelelektrode", "Centre electrode"),
    "ground": (586, 924, "r", 1040, "Masseelektrode", "Ground electrode"),
}


def plug_svg(sid: str, k: dict, nose: float = 868.0) -> str:
    """Spark plug in section in native coordinates (centre x 540, top 380, tip 935), in a hatched cylinder head."""
    s = sid
    hatch = f"url(#{s}-hatch)"
    ceramic = "#E7ECF1"
    out = [f'<rect x="380" y="772" width="110" height="128" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
           f'<rect x="590" y="772" width="110" height="128" fill="{hatch}" stroke="{k["hairline"]}" stroke-width="2"/>'
           f'<rect x="380" y="900" width="320" height="70" fill="{k["fire"]}" fill-opacity="0.08"/>',
           f'<g filter="url(#{s}-sh)">',
           f'<rect x="522" y="380" width="36" height="52" rx="8" fill="url(#{s}-gsteel)"/>',
           f'<path d="M496,432 L584,432 L584,640 L496,640 Z" fill="{ceramic}"/>']
    for y in range(452, 630, 26):
        out.append(f'<line x1="496" y1="{y}" x2="584" y2="{y}" stroke="#B9C2CC" stroke-width="3"/>')
    out.append(f'<rect x="470" y="640" width="140" height="80" rx="6" fill="url(#{s}-gsteel)"/>'
               f'<line x1="516" y1="640" x2="516" y2="720" stroke="{k["steel_dark"]}" stroke-width="3"/><line x1="564" y1="640" x2="564" y2="720" stroke="{k["steel_dark"]}" stroke-width="3"/>'
               f'<rect x="484" y="720" width="112" height="44" fill="url(#{s}-gsteel)"/>'
               f'<rect id="{s}-gk" x="474" y="760" width="132" height="12" rx="3" fill="#C8875A"/>')
    # threaded shell in section: two walls with thread teeth, insulator nose and centre electrode inside
    for xw, sign in ((490, 1), (590, -1)):
        out.append(f'<rect x="{min(xw, xw - 14 * sign) if sign < 0 else xw}" y="772" width="14" height="128" fill="{k["steel"]}"/>')
        for y in range(780, 896, 14):
            out.append(f'<path d="M{xw},{y} L{xw - 10 * sign},{y + 7} L{xw},{y + 14}" fill="{k["steel"]}"/>')
    out.append(f'<path d="M506,772 L574,772 L556,{nose:.0f} L524,{nose:.0f} Z" fill="{ceramic}"/>'
               f'<rect x="534" y="432" width="12" height="474" fill="{k["steel_dark"]}"/>'
               f'<rect id="{s}-res" x="531" y="520" width="18" height="80" rx="4" fill="#3A2F2A"/>'
               f'<rect x="533" y="896" width="14" height="12" fill="{k["steel"]}"/>'
               f'<path d="M590,900 L598,900 L598,940 L536,940 L536,926 L584,926 L584,900 Z" fill="{k["steel"]}"/>')
    out.append('</g>')
    out.append(f'<g id="{s}-pspk" opacity="0"><polyline points="540,909 534,914 546,918 538,923" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
               f'<circle cx="540" cy="916" r="14" fill="{k["fire"]}" fill-opacity="0.55"/></g>')
    out.append(f'<path id="{s}-heat" d="M540,{nose - 6:.0f} L552,800 L586,776 L640,800 L660,860" fill="none" stroke="{k["fire"]}" stroke-width="7" '
               f'stroke-linecap="round" stroke-dasharray="14 12" marker-end="url(#{s}-arrf)" opacity="0"/>')
    return "".join(out)


def plug(c: SceneCtx, d: dict) -> SceneOut:
    k = _pal(c)
    s = c.sid
    problems: list[str] = []
    tl = _fade(c, fade_in=d.get("fade_in", True), fade_out=d.get("fade_out", True))
    ev = [c.start]
    parts = [f'<defs><marker id="{s}-arrf" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{k["fire"]}"/></marker></defs>']
    if d.get("mode") == "compare":     # hot plug (long nose) beside a cold plug (short nose)
        for side, xc, nose, lab in (("H", 320, 880.0, d.get("left_label", "heiß" if c.lang == "de" else "hot")),
                                    ("C", 760, 828.0, d.get("right_label", "kalt" if c.lang == "de" else "cold"))):
            ps = f"{s}{side}"
            view = (0.95, xc - 0.95 * 540, 380 - 0.95 * 380)
            parts.append(_defs(ps, k) + f'<defs><marker id="{ps}-arrf" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{k["fire"]}"/></marker></defs>'
                         + _place(view, plug_svg(ps, k, nose)))
            parts.append(f'<g id="{s}-cap{side}" opacity="0"><text class="col-h" x="{xc}" y="1150" text-anchor="middle">{_e(lab)}</text></g>')
            t = at_time(c, d, d.get("labels_at", [0.2, 0.35])[0 if side == "H" else 1])
            tl.append(_show(f"#{s}-cap{side}", t, 0.3, 10))
            ev.append(t)
            for t in [at_time(c, d, a) for a in d.get("heat_at", [])]:
                tl.append(f'tl.set("#{ps}-heat",{{opacity:1}},{t:.3f});')
                tl.append(f'tl.fromTo("#{ps}-heat",{{attr:{{"stroke-dashoffset":0}}}},{{attr:{{"stroke-dashoffset":-130}},duration:{max(0.5, c.end - t):.2f},ease:"none"}},{t:.3f});')
                ev.append(t)
        sparks_sel = [f"#{s}H-pspk", f"#{s}C-pspk"]
    else:
        view = _view(d, (1.25, 380.0))
        parts.append(_place(view, plug_svg(s, k, float(d.get("nose", 868)))))
        for i, item in enumerate(d.get("labels", [])):
            item = {"key": item} if isinstance(item, str) else dict(item)
            ax, ay, side, y, de, en = PLUG_PARTS[item["key"]]
            sx, sy = _T(view, ax, ay)
            parts.append(_card(f"{s}-lb{i}", k, de if c.lang == "de" else en, item.get("side", side), item.get("y", y), sx, sy))
            t = at_time(c, d, (d.get("labels_at") or [])[i] if i < len(d.get("labels_at") or []) else 0.2 + 0.1 * i)
            tl.append(_show(f"#{s}-lb{i}", t, 0.3, 10))
            ev.append(t)
        for t in [at_time(c, d, a) for a in d.get("heat_at", [])]:
            tl.append(f'tl.set("#{s}-heat",{{opacity:1}},{t:.3f});')
            tl.append(f'tl.fromTo("#{s}-heat",{{attr:{{"stroke-dashoffset":0}}}},{{attr:{{"stroke-dashoffset":-130}},duration:{max(0.5, c.end - t):.2f},ease:"none"}},{t:.3f});')
            ev.append(t)
        sparks_sel = [f"#{s}-pspk"]
    for t in [at_time(c, d, a) for a in d.get("sparks_at", [])]:
        for j in range(4):
            for sel in sparks_sel:
                tl.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.03}},{t + 0.22 * j:.3f});')
                tl.append(f'tl.to("{sel}",{{opacity:0,duration:0.08}},{t + 0.22 * j + 0.06:.3f});')
        ev.append(t)
    inner = f'<g id="{s}-cam" transform="matrix(1,0,0,1,0,0)">{"".join(parts)}</g>' + _title(c, d, k, problems)
    if d.get("title"):
        tl.append(_show(f"#{s}-ttl", c.start + 0.1, 0.3, 10))
    track = Track.from_data(c, d, (0.0, 360.0))
    if d.get("strip", True):
        inner += strip_svg(s, k, c.lang)
        a, b = strip_anim(s, k, track)
        tl += a
        ev += b
    return _out(c, inner, k, tl, ev, problems)


TEMPLATES = {"rv_hook": mechanism_hook, "rv_cutaway": cutaway, "rv_exploded": exploded, "rv_drive": timing_drive,
             "rv_readout": readout, "rv_chart": chart, "rv_board": board, "rv_plug": plug}
HOOK_SCENE_TYPES = ["rv_hook"]
LIMITS = {"rv_hook": {"claim": 64}, "rv_cutaway": {"title": 30}, "rv_exploded": {"title": 30},
          "rv_drive": {"title": 30, "note": 36}, "rv_readout": {"title": 30}, "rv_chart": {"title": 30},
          "rv_board": {"title": 30}, "rv_plug": {"title": 30}}


# --- Format "Zeitlupe" (02.11.2026): scene types zl_*, see zeitlupe/scenes.py ----------------------------------------
# The module reuses the kinematics, the engine drawing and its animation from this file: its namespace is handed over
# as RV before the module runs. Plans with rv_* scenes render unchanged.
import importlib.util as _ilu
from pathlib import Path as _Path
from types import SimpleNamespace as _NS

_zl_spec = _ilu.spec_from_file_location("rv_zeitlupe_scenes", _Path(__file__).resolve().with_name("zeitlupe") / "scenes.py")
_zl = _ilu.module_from_spec(_zl_spec)
_zl.RV = _NS(**{_k: _v for _k, _v in globals().items() if not _k.startswith("__")})
_zl_spec.loader.exec_module(_zl)
TEMPLATES.update(_zl.TEMPLATES)
LIMITS.update(_zl.LIMITS)
HOOK_SCENE_TYPES += _zl.HOOK_SCENE_TYPES
_rv_css = CSS


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:  # noqa: F811
    return _rv_css(pal, display, display_w, body, mono) + _zl.CSS(pal, display, display_w, body, mono)
