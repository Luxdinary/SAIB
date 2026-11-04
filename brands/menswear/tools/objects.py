"""Suitwerk objects: every drawing a Suitwerk scene can show, in the jacket's style and its 600 x 780 viewBox.

The jacket (`garment.py`) stays the running object; for topics that are not about the jacket itself (Woche 1,
01.11.2026) the scenes take an object spec instead:

    {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "shawl", "dinner": true, "neck": "bow", ...}
    {"kind": "jacket_back", "vents": "none|centre|side"}
    {"kind": "waistcoat", "fastened": [0, 1, 2, 3, 4], "strain": false}
    {"kind": "tailcoat"}                                     white tie: tailcoat, white waistcoat, wing collar, bow
    {"kind": "torso", "tie_tip": 585, "hold": "belt|braces|none", "neck": "tie|none"}
    {"kind": "legs", "break": "none|slight|full", "turnup": false, "seated": false, "sock": "long|short", "shoe": "oxford|derby"}
    {"kind": "knot", "knot": "four_in_hand|half_windsor|windsor"}
    {"kind": "swatch", "weave": "plain|twill|herringbone|flannel|tweed|fresco|worsted|woollen|pinstripe|chalkstripe",
     "colour": "#2A3550", "layers": 1}
    {"kind": "fibres", "microns": [18.75, 16.25]}
    {"kind": "yarn", "spin": "worsted|woollen"}

`draw(uid, spec, accent, ring=[names])` returns the SVG; `spot(spec, name)` gives a named point (rings, pins, zoom,
tags); `button_spots(spec)` the button points (pulses); `front_edge(spec)` the cut line (jacket only, else "").
Line paths carry class `ln` (or `lnm` for minis) and `pathLength=1` so scenes draw them in; fills carry `fill`,
buttons sit in `g.btns`, strain lines in `g.strains` (class `strain`), rings in `g.rings`.
"""
from __future__ import annotations

import random

import garment as G

VW, VH, CX = G.VW, G.VH, G.CX
NAVY, NAVY_L, SHIRT, TIE, INK = "#26344D", "#2B3A55", "#E9E3D7", "#8A6E4B", "#8C7650"
SHIRT_BLUE = "#BCC6D6"           # light blue shirt, muted so the gold line still reads


def _wrap(uid: str, body: str, accent: str, rings: str = "", btns: str = "", strains: str = "", defs: str = "") -> str:
    sh = f"{uid}-sh"
    tw = f"{uid}-tw"
    return f"""<svg class="jacket" viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="{tw}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{accent}" stroke-opacity="0.09" stroke-width="2"/></pattern>
<linearGradient id="{sh}" gradientUnits="userSpaceOnUse" x1="110" y1="40" x2="500" y2="760"><stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/><stop offset="0.42" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.34"/></linearGradient>{defs}</defs>
<g class="cloth">{body}</g><g class="btns">{btns}</g><g class="strains">{strains}</g><g class="rings">{rings}</g>
</svg>"""


class _Pen:
    """Small helper: cloth shapes and lines in the jacket style."""

    def __init__(self, uid: str, lc: str):
        self.uid, self.lc, self.parts = uid, lc, []

    def cloth(self, d: str, fill: str = NAVY, tex: bool = True, shade: bool = True) -> None:
        s = f'<path class="fill" d="{d}" fill="{fill}"/>'
        if tex:
            s += f'<path class="fill" d="{d}" fill="url(#{self.uid}-tw)"/>'
        if shade:
            s += f'<path class="fill shade" d="{d}" fill="url(#{self.uid}-sh)"/>'
        self.parts.append(s + f'<path class="{self.lc}" pathLength="1" d="{d}"/>')

    def flat(self, d: str, fill: str, line: bool = True, cls: str = "") -> None:
        self.parts.append(f'<path class="fill {cls}" d="{d}" fill="{fill}"/>' + (f'<path class="{self.lc} thin" pathLength="1" d="{d}"/>' if line else ""))

    def line(self, d: str, cls: str = "") -> None:
        self.parts.append(f'<path class="{self.lc} {cls}" pathLength="1" d="{d}"/>')

    def raw(self, s: str) -> None:
        self.parts.append(s)

    def html(self) -> str:
        return "".join(self.parts)


def _rings(spec: dict, ring: list[str] | None) -> str:
    out = ""
    for name in ring or []:
        x, y = spot(spec, name)
        out += f'<circle class="ring" pathLength="1" cx="{x}" cy="{y}" r="30"/>'
    return out


# --- jacket back (vents) ---------------------------------------------------------------------------

_BACK_L = ("M300,52 C280,52 262,54 256,58 C210,70 160,80 116,96 C122,160 128,210 134,262 C150,330 162,380 160,430 "
           "C156,520 150,600 148,700 C190,712 240,716 300,716 Z")


def _jacket_back(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    vents = spec.get("vents", "centre")
    p.cloth(G._mirror(_BACK_L))
    p.cloth(_BACK_L)
    sleeve = "M116,96 C96,120 88,160 86,220 C82,350 76,480 72,612 L150,624 C154,500 156,380 160,280 C150,200 132,140 116,96 Z"
    p.cloth(sleeve)
    p.cloth(G._mirror(sleeve))
    p.cloth("M300,40 C276,40 258,46 252,58 C270,66 286,70 300,70 C314,70 330,66 348,58 C342,46 324,40 300,40 Z", NAVY_L)
    p.line("M300,70 C304,260 296,440 300,716", "seam")
    p.line("M190,120 C206,300 200,520 196,712", "seam")
    p.line(G._mirror("M190,120 C206,300 200,520 196,712"), "seam")
    if vents == "centre":
        p.flat("M300,560 L310,716 L292,716 Z", "#0E1524", line=False)
        p.line("M300,560 L300,716 M306,566 L306,716", "vent")
    elif vents == "side":
        p.flat("M199,580 L208,713 L190,712 Z", "#0E1524", line=False)
        p.flat(G._mirror("M199,580 L208,713 L190,712 Z"), "#0E1524", line=False)
        p.line("M196,580 L196,712 M202,586 L202,713", "vent")
        p.line(G._mirror("M196,580 L196,712 M202,586 L202,713"), "vent")
    return _wrap(uid, p.html(), accent, _rings(spec, ring))


# --- waistcoat -------------------------------------------------------------------------------------

_WC_L = "M270,64 L214,72 C212,150 196,220 168,256 C170,360 172,470 176,566 L286,618 L300,626 L300,292 C290,210 280,140 270,64 Z"
WC_BUTTONS = [330, 382, 434, 486, 538, 590]


def _waistcoat(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    fast = spec.get("fastened", [0, 1, 2, 3, 4])
    p.flat("M232,40 L300,300 L368,40 Z", SHIRT, line=False)
    p.flat("M288,74 L312,74 L307,96 L314,282 L300,300 L286,282 L293,96 Z", TIE, line=False)
    p.line("M232,40 L286,86 L298,66 M368,40 L314,86 L302,66", "thin")
    p.cloth("M150,590 L450,590 L456,712 L144,712 Z")
    p.line("M150,618 L450,618", "seam")
    p.cloth("M214,64 L130,104 C114,230 120,430 140,604 L460,604 C480,430 486,230 470,104 L386,64 Z", SHIRT_BLUE, tex=False)
    p.line("M150,112 C126,250 120,430 114,540 M450,112 C474,250 480,430 486,540", "thin")
    p.cloth(G._mirror(_WC_L))
    p.cloth(_WC_L)
    for y in (470,):
        p.cloth(f"M200,{y} L262,{y + 4} L262,{y + 12} L200,{y + 8} Z")
        p.cloth(G._mirror(f"M200,{y} L262,{y + 4} L262,{y + 12} L200,{y + 8} Z"))
    btns = ""
    for i, y in enumerate(WC_BUTTONS):
        closed = i in fast
        x = CX if closed else CX + 12
        hole = f'<line class="hole" x1="{CX - 24}" y1="{y}" x2="{CX - 10}" y2="{y}"/>'
        btns += f'{hole}<circle class="btn{"" if closed else " open"}" cx="{x}" cy="{y}" r="9"/>'
    strains = ""
    if spec.get("strain"):
        y = WC_BUTTONS[-1]
        for d in (f"M294,{y - 4} C270,{y - 20} 248,{y - 34} 226,{y - 52}", f"M294,{y + 4} C268,{y + 14} 240,{y + 18} 214,{y + 18}"):
            strains += f'<path class="strain" pathLength="1" d="{d}"/><path class="strain" pathLength="1" d="{G._mirror(d)}"/>'
    return _wrap(uid, p.html(), accent, _rings(spec, ring), btns, strains)


# --- tailcoat (white tie) -------------------------------------------------------------------------

def _tailcoat(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    black, satin = "#15171C", "#24272F"
    # trousers between the tails
    p.cloth("M214,560 L386,560 L382,720 L304,720 L300,640 L296,720 L218,720 Z", black)
    p.line("M222,600 L222,720 M378,600 L378,720", "thin")
    # tails behind the legs
    tail_l = "M150,430 C152,560 150,640 156,720 L214,720 C214,640 212,560 206,470 Z"
    p.cloth(tail_l, black)
    p.cloth(G._mirror(tail_l), black)
    # shirt, white waistcoat (low V, cut straight at the waist), wing collar, bow
    p.flat("M246,50 L300,470 L354,50 Z", "#F4F1EA", line=False)
    p.raw("".join(f'<circle class="fill" cx="300" cy="{y}" r="4" fill="#C9C2B4"/>' for y in (150, 210, 270)))
    wc = "M232,250 L300,478 L368,250 L384,470 L340,548 L300,532 L260,548 L216,470 Z"
    p.flat(wc, "#F2EEE6")
    p.line("M246,50 L262,66 L276,60 M354,50 L338,66 L324,60", "thin")
    bow = "M300,82 L270,70 L274,82 L270,96 Z M300,82 L330,70 L326,82 L330,96 Z"
    p.flat(bow, "#FBF9F4")
    # coat fronts end at the waist; peak lapels with satin facing
    front_l = ("M256,58 C210,70 160,80 116,96 C122,160 128,210 134,262 C150,330 158,380 156,430 L214,440 L232,250 "
               "L262,92 L262,58 Z")
    p.cloth(G._mirror(front_l), black)
    p.cloth(front_l, black)
    sleeve = "M116,96 C96,120 88,160 86,220 C82,350 76,480 72,612 L150,624 C154,500 156,380 160,280 C150,200 132,140 116,96 Z"
    p.cloth(sleeve, black)
    p.cloth(G._mirror(sleeve), black)
    lap = "M232,250 L262,92 L232,142 L168,118 C178,200 214,236 232,250 Z"
    p.cloth(lap, satin)
    p.cloth(G._mirror(lap), satin)
    btns = "".join(f'<circle class="btn" cx="{x}" cy="{y}" r="8" style="fill:{satin}"/>' for x in (196, 404) for y in (330, 400))
    return _wrap(uid, p.html(), accent, _rings(spec, ring), btns)


# --- torso (shirt, tie, waistband; belt or braces) -------------------------------------------------

def _torso(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    tip = float(spec.get("tie_tip", 585))
    hold = spec.get("hold", "belt")
    shirt = "M232,46 L140,96 C120,200 128,420 150,580 L450,580 C472,420 480,200 460,96 L368,46 Z"
    p.cloth(shirt, SHIRT_BLUE, tex=False)
    p.line("M150,104 C126,240 118,420 112,530 M450,104 C474,240 482,420 488,530", "thin")
    p.line("M300,100 L300,580", "thin")
    p.raw("".join(f'<circle class="fill" cx="300" cy="{y}" r="5" fill="#B9C2D0"/>' for y in (160, 240, 320, 400, 480)))
    p.cloth("M232,46 L282,108 L300,74 L318,108 L368,46 L300,40 Z", "#CDD5E2", tex=False)
    # trousers and waistband
    p.cloth("M146,572 L454,572 L460,720 L310,720 L300,680 L290,720 L140,720 Z")
    p.line("M150,606 L450,606", "seam")
    if hold == "belt":
        p.flat("M146,578 L454,578 L454,606 L146,606 Z", "#3A2A1E")
        p.flat("M282,574 L318,574 L318,610 L282,610 Z", "none")
        p.raw(f'<path class="fill" d="M286,578 L314,578 L314,606 L286,606 Z" fill="none" stroke="{accent}" stroke-width="3"/>')
        p.line("M180,572 L180,612 M420,572 L420,612 M250,572 L250,612 M350,572 L350,612", "seam")
    elif hold == "braces":
        for x in (226, 374):
            p.flat(f"M{x - 10},56 L{x + 10},56 L{x + 12},560 L{x - 12},560 Z", "#5A2E2E")
            p.flat(f"M{x - 14},556 L{x + 14},556 L{x + 10},592 L{x - 10},592 Z", "#3A2A1E")
        p.raw("".join(f'<circle class="fill" cx="{x}" cy="586" r="6" fill="{accent}"/>' for x in (218, 234, 366, 382)))
    if spec.get("neck", "tie") == "tie":
        tie = f"M288,104 L312,104 L307,128 L318,{tip - 26:g} L300,{tip:g} L282,{tip - 26:g} L293,128 Z"
        p.flat(tie, TIE)
        p.flat("M286,84 L314,84 L310,110 L290,110 Z", "#7A5F3E")
    return _wrap(uid, p.html(), accent, _rings(spec, ring))


# --- legs (break, turn-up, sock, shoe) -------------------------------------------------------------

LEGS_DY = -50


def _legs(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    brk, seated = spec.get("break", "slight"), bool(spec.get("seated"))
    hem = {"none": 668, "slight": 684, "full": 700}.get(brk, 684)
    if seated:
        hem = 560
    # shoe in profile (toe to the right)
    lace = spec.get("shoe", "oxford")
    shoe = "M150,698 C150,664 182,650 226,650 L330,654 C392,660 446,680 500,696 C536,706 556,722 556,742 L556,756 L150,756 Z"
    p.cloth(shoe, "#2A1C14", tex=False)
    p.line("M150,742 L556,742", "thin")
    if lace == "derby":
        p.line("M296,654 C318,684 360,696 396,700", "thin")
    else:
        p.line("M318,656 C332,676 362,688 392,692", "thin")
    p.line("M336,664 L362,672 M346,658 L372,668", "thin")
    # sock between hem and shoe
    if seated or spec.get("sock_show"):
        sock = spec.get("sock", "long")
        top = hem
        if sock == "short":
            p.flat(f"M206,{top} L352,{top} L356,626 L202,626 Z", "#C8A68A", line=False)
            p.flat("M202,626 L356,626 L356,656 L202,656 Z", "#1E2638")
        else:
            p.flat(f"M206,{top} L352,{top} L356,656 L202,656 Z", "#1E2638")
    # trouser leg (front crease) with the break fold
    leg = f"M180,0 L380,0 L370,{hem - 14} C360,{hem} 320,{hem + 8} 270,{hem + 4} L196,{hem - 6} Z"
    p.cloth(leg)
    p.line(f"M282,0 L286,{hem - 30}", "seam")
    if brk == "slight" and not seated:
        p.line(f"M374,{hem - 80} C352,{hem - 64} 338,{hem - 52} 330,{hem - 38}", "fold")
    elif brk == "full" and not seated:
        p.line(f"M376,{hem - 120} C350,{hem - 100} 334,{hem - 80} 326,{hem - 64} M372,{hem - 62} C352,{hem - 48} 340,{hem - 34} 334,{hem - 22}", "fold")
    if spec.get("turnup"):
        p.line(f"M198,{hem - 46} L370,{hem - 58}", "")
    # the leg fades in from the top so it never runs into a title above the object
    mask = (f'<linearGradient id="{uid}-lg" gradientUnits="userSpaceOnUse" x1="0" y1="110" x2="0" y2="250"><stop offset="0" stop-color="#000"/>'
            f'<stop offset="1" stop-color="#fff"/></linearGradient><mask id="{uid}-lm" maskUnits="userSpaceOnUse" x="-100" y="-100" width="800" height="1000">'
            f'<rect x="-100" y="-100" width="800" height="1000" fill="url(#{uid}-lg)"/></mask>')
    # lifted by LEGS_DY so the shoe ends where a jacket hem ends (tags and statements sit below that line)
    return _wrap(uid, f'<g transform="translate(0,{LEGS_DY})"><g mask="url(#{uid}-lm)">{p.html()}</g></g>', accent,
                 _rings(spec, ring), defs=mask)


# --- tie knot ---------------------------------------------------------------------------------------

def _knot(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    k = spec.get("knot", "four_in_hand")
    w = {"four_in_hand": 70, "half_windsor": 96, "windsor": 128}.get(k, 80)
    spread = {"four_in_hand": 60, "half_windsor": 90, "windsor": 130}.get(k, 80)
    p.cloth("M90,80 L510,80 L530,720 L70,720 Z", SHIRT_BLUE, tex=False)
    p.line("M300,330 L300,720", "thin")
    blade = "M262,330 L338,330 L356,640 L300,700 L244,640 Z"
    p.flat(blade, TIE)
    tilt = 10 if k == "four_in_hand" else 0
    knot = f"M{300 - w / 2:g},{220 + tilt:g} L{300 + w / 2:g},220 L{300 + w * 0.18:g},336 L{300 - w * 0.18:g},336 Z"
    p.flat(knot, "#7A5F3E")
    p.line("M300,300 L300,336", "thin dimple")
    # collar wings: wider spread for bigger knots
    p.flat(f"M300,140 L{300 - w / 2 - 6:g},216 L{300 - w / 2 - spread:g},360 L170,170 Z", "#CDD5E2")
    p.flat(f"M300,140 L{300 + w / 2 + 6:g},216 L{300 + w / 2 + spread:g},360 L430,170 Z", "#CDD5E2")
    p.line("M170,170 C220,120 380,120 430,170", "thin")
    return _wrap(uid, p.html(), accent, _rings(spec, ring))


# --- fabric swatch -----------------------------------------------------------------------------------

def _swatch_defs(uid: str, weave: str, colour: str, accent: str) -> tuple[str, str]:
    """(defs, fill url) for a woven surface."""
    pid = f"{uid}-wv"
    hi, lo = "rgba(255,255,255,0.16)", "rgba(0,0,0,0.28)"
    if weave == "plain" or weave == "fresco":
        gap = 3 if weave == "fresco" else 0
        t = 10
        tile = (f'<rect width="{t}" height="{t}" fill="{"#0F1626" if gap else colour}"/>'
                f'<rect x="0" y="{gap / 2}" width="{t / 2}" height="{t - gap}" fill="{colour}"/><rect x="0" y="{gap / 2}" width="{t / 2}" height="{t - gap}" fill="{hi}"/>'
                f'<rect x="{t / 2}" y="{gap / 2}" width="{t / 2}" height="{t - gap}" fill="{colour}"/><rect x="{t / 2 + gap / 2}" y="0" width="{t / 2 - gap}" height="{t}" fill="{lo}"/>')
        return f'<pattern id="{pid}" width="{t}" height="{t}" patternUnits="userSpaceOnUse">{tile}</pattern>', f"url(#{pid})"
    if weave in ("twill", "worsted"):
        sw = 1.2 if weave == "worsted" else 2.2
        return (f'<pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
                f'<rect width="8" height="8" fill="{colour}"/><line x1="0" y1="0" x2="0" y2="8" stroke="{hi}" stroke-width="{sw}"/>'
                f'<line x1="4" y1="0" x2="4" y2="8" stroke="{lo}" stroke-width="{sw}"/></pattern>', f"url(#{pid})")
    if weave == "herringbone":
        return (f'<pattern id="{pid}" width="36" height="16" patternUnits="userSpaceOnUse"><rect width="36" height="16" fill="{colour}"/>'
                f'<path d="M0,16 L18,0 M0,8 L9,0 M9,16 L18,8 M18,0 L36,16 M18,8 L27,16 M27,0 L36,8" stroke="{hi}" stroke-width="2.4"/>'
                f'<line x1="18" y1="0" x2="18" y2="16" stroke="{lo}" stroke-width="1.5"/></pattern>', f"url(#{pid})")
    if weave in ("flannel", "woollen", "tweed"):
        seed = random.Random(7)
        dots = ""
        if weave == "tweed":
            cols = ["#8A6E4B", "#5E7A5A", "#B9A27A", "#3D4A63", "#9C5A4A"]
            dots = "".join(f'<rect x="{seed.uniform(0, 60):.1f}" y="{seed.uniform(0, 60):.1f}" width="{seed.uniform(2, 6):.1f}" height="1.6" fill="{seed.choice(cols)}"/>' for _ in range(70))
        filt = (f'<filter id="{pid}-f" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>'
                f'<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.22 0"/><feGaussianBlur stdDeviation="{0.9 if weave == "flannel" else 0.4}"/></filter>')
        return (f'{filt}<pattern id="{pid}" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="{colour}"/>'
                f'<rect width="60" height="60" filter="url(#{pid}-f)"/>{dots}</pattern>', f"url(#{pid})")
    if weave in ("pinstripe", "chalkstripe"):
        line = (f'<line x1="20" y1="0" x2="20" y2="40" stroke="#E9E3D7" stroke-width="1.4"/>' if weave == "pinstripe" else
                f'<line x1="20" y1="0" x2="20" y2="40" stroke="#E9E3D7" stroke-opacity="0.95" stroke-width="5" filter="url(#{pid}-b)"/>')
        blur = f'<filter id="{pid}-b" x="-1" y="0" width="3" height="1"><feGaussianBlur stdDeviation="1.4"/></filter>' if weave == "chalkstripe" else ""
        return (f'{blur}<pattern id="{pid}" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="{colour}"/>'
                f'<path d="M0,0 L40,40" stroke="{hi}" stroke-width="1"/>{line}</pattern>', f"url(#{pid})")
    return f'<pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{colour}"/></pattern>', f"url(#{pid})"


def _swatch(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    weave, colour = spec.get("weave", "twill"), spec.get("colour", "#2A3550")
    defs, url = _swatch_defs(uid, weave, colour, accent)
    layers = int(spec.get("layers", 1))
    body = "M70,140 L530,140 L530,560 L430,660 L70,660 Z"
    for k in range(layers - 1, 0, -1):            # cloth thickness: stacked edges under the swatch
        p.raw(f'<path class="fill" d="M{70 + k * 6},{140 + k * 9} L{530 + k * 6},{140 + k * 9} L{530 + k * 6},{560 + k * 9} '
              f'L{430 + k * 6},{660 + k * 9} L{70 + k * 6},{660 + k * 9} Z" fill="{colour}" opacity="{0.9 - k * 0.12:.2f}"/>')
    p.raw(f'<path class="fill" d="{body}" fill="{url}"/><path class="fill shade" d="{body}" fill="url(#{uid}-sh)"/>')
    p.line(body)
    p.flat("M530,560 L430,660 L452,566 Z", colour)
    p.line("M430,660 L452,566 L530,560", "thin")
    p.line("M90,700 L510,700 M90,690 L90,710 M510,690 L510,710", "seam measure")
    return _wrap(uid, p.html(), accent, _rings(spec, ring), defs=defs)


# --- fibres (cross-sections) and yarn ----------------------------------------------------------------

def _fibres(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    mic = spec.get("microns", [18.75, 16.25])
    n = len(mic)
    xs = [300] if n == 1 else [170 + i * (260 / (n - 1)) for i in range(n)]
    for i, (x, m) in enumerate(zip(xs, mic)):
        r = float(m) * 7.0
        p.flat(f"M{x - r:.1f},360 A{r:.1f},{r:.1f} 0 1,0 {x + r:.1f},360 A{r:.1f},{r:.1f} 0 1,0 {x - r:.1f},360 Z", "#C9B48E")
        p.raw(f'<circle class="fill" cx="{x:.1f}" cy="360" r="{r * 0.72:.1f}" fill="#D9C7A4"/>')
        p.line(f"M{x - r:.1f},{360 + r + 40:.1f} L{x + r:.1f},{360 + r + 40:.1f} M{x - r:.1f},{360 + r + 30:.1f} L{x - r:.1f},{360 + r + 50:.1f} "
               f"M{x + r:.1f},{360 + r + 30:.1f} L{x + r:.1f},{360 + r + 50:.1f}", "measure")
    return _wrap(uid, p.html(), accent, _rings(spec, ring))


def _yarn(uid, spec, accent, ring, lc):
    p = _Pen(uid, lc)
    rnd = random.Random(11)
    worsted = spec.get("spin", "worsted") == "worsted"
    strands = ""
    for k in range(14):
        off = (k - 7) * 9
        if worsted:
            strands += f'<path d="M{300 + off},60 C{330 + off},220 {270 + off},380 {300 + off},540 C{330 + off},640 {290 + off},700 {300 + off},740" stroke="#D9C7A4" stroke-width="3" fill="none"/>'
        else:
            pts = " ".join(f"{300 + off + rnd.uniform(-26, 26):.0f},{y}" for y in range(60, 760, 40))
            strands += f'<polyline points="{pts}" stroke="#D9C7A4" stroke-width="3" fill="none" stroke-linejoin="round"/>'
    if not worsted:
        for _ in range(60):
            x, y = 300 + rnd.uniform(-80, 80), rnd.uniform(70, 740)
            strands += f'<path d="M{x:.0f},{y:.0f} q{rnd.uniform(-30, 30):.0f},{rnd.uniform(-20, 20):.0f} {rnd.uniform(-46, 46):.0f},{rnd.uniform(-12, 12):.0f}" stroke="#C9B48E" stroke-width="2" fill="none"/>'
    p.raw(f'<g class="fill">{strands}</g>')
    p.line("M236,60 L236,740 M364,60 L364,740" if worsted else "M206,60 L206,740 M394,60 L394,740", "seam")
    return _wrap(uid, p.html(), accent, _rings(spec, ring))


# --- dispatcher ---------------------------------------------------------------------------------------

_SPOTS = {
    "jacket_back": {"vent": (300, 650), "vent_l": (199, 650), "vent_r": (401, 650), "seam": (300, 400), "collar": (300, 56),
                    "hem": (300, 706), "shoulder": (116, 96)},
    "waistcoat": {**{f"button:{i}": (300, y) for i, y in enumerate(WC_BUTTONS)}, "button:open": (312, WC_BUTTONS[-1]), "hem": (300, 620), "waistband": (360, 604), "point": (190, 590),
                  "pocket": (231, 476), "v": (300, 296), "neck": (300, 80), "shoulder": (214, 72)},
    "tailcoat": {"bow": (300, 82), "waistcoat": (300, 470), "tails": (180, 660), "lapel": (210, 190), "collar": (262, 62),
                 "front": (214, 440), "trousers": (222, 700), "shirt": (300, 210), "button": (196, 330)},
    "torso": {"knot": (300, 96), "collar": (300, 70), "belt": (300, 592), "buckle": (300, 592), "waistband": (300, 592),
              "brace": (226, 576), "brace_r": (374, 300), "placket": (300, 320)},
    "legs": {"hem": (284, 684), "break": (350, 620), "shoe": (450, 708), "sock": (280, 610), "heel": (168, 720), "crease": (283, 300),
             "lacing": (356, 670)},
    "knot": {"knot": (300, 270), "dimple": (300, 318), "collar": (210, 260), "collar_r": (390, 260), "blade": (300, 560)},
    "swatch": {"center": (300, 400), "corner": (470, 600), "edge": (300, 140), "weave": (220, 300), "measure": (300, 700)},
    "fibres": {"fibre:0": None, "fibre:1": None, "fibre:2": None, "scale": (300, 560)},
    "yarn": {"center": (300, 400), "fibre": (330, 260), "end": (300, 720)},
}


def spot(spec: dict, name: str) -> tuple[float, float]:
    kind = spec.get("kind", "jacket")
    if kind == "jacket":
        return G.point(spec.get("variant", "sb2"), name, spec.get("fastened", [0]))
    if kind == "torso" and name == "tie_tip":
        return 300, float(spec.get("tie_tip", 585))
    if kind == "legs":
        if spec.get("seated") and name == "hem":
            return 284, 560 + LEGS_DY
        x, y = _SPOTS["legs"].get(name) or (300, 450)
        return x, y + LEGS_DY
    if kind == "fibres" and name.startswith("fibre:"):
        mic = spec.get("microns", [18.75, 16.25])
        n, i = len(mic), int(name.split(":")[1])
        return (300 if n == 1 else 170 + i * (260 / (n - 1))), 360
    pts = _SPOTS.get(kind, {})
    if name in pts and pts[name] is not None:
        return pts[name]
    return 300, 400


def draw(uid: str, spec: dict, accent: str = "#D4B483", ring: list[str] | None = None, lines_class: str = "ln") -> str:
    kind = spec.get("kind", "jacket")
    if kind == "jacket":
        opts = {k: spec[k] for k in ("lapel", "dinner", "neck", "pockets", "ticket", "flower", "lapel_hole", "cuff", "chest_pocket") if k in spec}
        return G.jacket_svg(uid, spec.get("variant", "sb2"), spec.get("fastened", [0]), strain=bool(spec.get("strain")),
                            accent=accent, ring=ring, lines_class=lines_class, **opts)
    fn = {"jacket_back": _jacket_back, "waistcoat": _waistcoat, "tailcoat": _tailcoat, "torso": _torso, "legs": _legs,
          "knot": _knot, "swatch": _swatch, "fibres": _fibres, "yarn": _yarn}[kind]
    return fn(uid, spec, accent, ring, lines_class)


def button_spots(spec: dict) -> list[tuple[float, float]]:
    kind = spec.get("kind", "jacket")
    if kind == "jacket":
        var = spec.get("variant", "sb2")
        return [G.point(var, f"button:{i}", spec.get("fastened", [0])) for i in range(len(G.VARIANTS[var]["buttons"]))]
    if kind == "waistcoat":
        return [(300, y) for y in WC_BUTTONS]
    return []


def front_edge(spec: dict) -> str:
    if spec.get("kind", "jacket") != "jacket":
        return ""
    return G.front_edge(spec.get("variant", "sb2"), spec.get("fastened", [0]))
