"""Suitwerk garment drawing: a single jacket as clean line illustration (SVG), the brand's running object.

Pure geometry, no rendering engine: `jacket_svg()` returns SVG markup for one jacket in a 600 x 780 viewBox,
`point()` gives the coordinates of named details (buttons, lapel, pocket, hem) so scenes can place rings,
callouts and zoom targets. Front view, no person; the V shows shirt and tie.

Variants: sb1 / sb2 / sb3 (single-breasted, 1-3 buttons, notch lapel), db6 (double-breasted 6x2, peak lapel).
State: `fastened` = indices of closed buttons (top = 0). The front edges stay together down to the lowest
fastened button and open below it; fastening the bottom button of a single-breasted jacket adds strain lines.
"""
from __future__ import annotations

import re

VW, VH = 600, 780
CX = 300
HEM_Y = 716
DB_EDGE = 384      # front edge of the overlapping panel (double-breasted)

# button y positions (top first) and break point per variant
VARIANTS = {
    "sb1": {"buttons": [500], "break": 478, "lapel": "notch", "db": False},
    "sb2": {"buttons": [452, 548], "break": 430, "lapel": "notch", "db": False},
    "sb3": {"buttons": [404, 476, 548], "break": 384, "lapel": "notch", "db": False},
    "db6": {"buttons": [470, 556], "break": 448, "lapel": "peak", "db": True},
}

COLORS = {
    "fill": "#26344D",       # jacket cloth (navy, a step lighter than the ground)
    "lapel": "#2B3A55",
    "shirt": "#E9E3D7",
    "tie": "#8A6E4B",
    "inside": "#121B2B",
    "strain": "#C9776B",
}


def _mirror(path: str) -> str:
    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", lambda m: f"{VW - float(m.group(1)):g},{m.group(2)}", path)


def _edge_left(variant: str, fastened: list[int]) -> tuple[str, float]:
    """Front edge of the left panel from the break point to the hem; returns (path segment, join y)."""
    v = VARIANTS[variant]
    if v["db"]:
        return "", v["break"]
    ys = v["buttons"]
    join = max([ys[i] for i in fastened if i < len(ys)], default=v["break"])
    join_y = join + 8
    bottom_closed = (len(ys) - 1) in fastened and len(ys) > 1
    if bottom_closed:   # quarters pulled together: straight longer, then a tight turn to the hem
        seg = f"L{CX},{join_y} C{CX},{join_y + 70} {CX - 18},{HEM_Y - 20} {CX - 26},{HEM_Y}"
    elif not fastened:  # open jacket (seated): edges part right from the break
        seg = f"C{CX - 8},{join_y + 120} {CX - 40},{HEM_Y - 90} {CX - 58},{HEM_Y}"
    else:
        seg = f"L{CX},{join_y} C{CX - 2},{join_y + 80} {CX - 22},{HEM_Y - 60} {CX - 44},{HEM_Y}"
    return seg, join_y


def _left_body(variant: str, fastened: list[int]) -> str:
    v = VARIANTS[variant]
    brk = v["break"]
    head = ("M256,58 C210,70 160,80 116,96 C122,160 128,210 134,262 C150,330 162,380 160,430 "
            "C156,520 150,600 148,700 ")
    if v["db"]:
        # double-breasted: the top panel reaches over the centre; straight front edge, square hem
        return head + f"C190,710 260,716 {DB_EDGE},716 L{DB_EDGE},{brk} L{CX - 38},64 Z"
    seg, _ = _edge_left(variant, fastened)
    hem_x = re.findall(r"(-?\d+(?:\.\d+)?),%d" % HEM_Y, seg)
    hx = float(hem_x[-1]) if hem_x else CX - 44
    # hem from the side to the front edge, then up the edge (reverse of seg) to the break and the roll line
    return head + f"C190,712 226,716 {hx:g},{HEM_Y} " + _reverse_edge(seg, brk) + f" L{CX - 38},64 Z"


def _reverse_edge(seg: str, brk: float) -> str:
    """The front-edge segment runs break -> hem; the body outline needs hem -> break."""
    nums = [tuple(map(float, p)) for p in re.findall(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", seg)]
    pts = [(CX, brk)] + nums
    out: list[str] = []
    cmds = re.findall(r"[LC]", seg)
    # walk commands backwards
    groups: list[tuple[str, list]] = []
    k = 1
    for c in cmds:
        n = 1 if c == "L" else 3
        groups.append((c, pts[k:k + n]))
        k += n
    prev_end = [(CX, brk)] + [g[1][-1] for g in groups]
    for gi in range(len(groups) - 1, -1, -1):
        c, ps = groups[gi]
        start = prev_end[gi]
        if c == "L":
            out.append(f"L{start[0]:g},{start[1]:g}")
        else:
            c1, c2, _ = ps
            out.append(f"C{c2[0]:g},{c2[1]:g} {c1[0]:g},{c1[1]:g} {start[0]:g},{start[1]:g}")
    return " ".join(out)


def _lapel_left(variant: str, lapel: str | None = None) -> tuple[str, str]:
    """(lapel path, collar path) for the left side; `lapel` overrides the variant's lapel (notch, peak, shawl)."""
    v = VARIANTS[variant]
    brk = v["break"]
    bx = DB_EDGE if v["db"] else CX
    kind = lapel or v["lapel"]
    if kind == "shawl":      # one rolled piece from the neck to the break, no notch
        lapel_p = f"M{bx},{brk} L268,84 C236,104 200,140 190,196 C206,268 262,{brk - 70} {bx},{brk} Z"
        collar = "M300,44 C280,46 262,50 252,58 L268,84 Z"
        return lapel_p, collar
    if kind == "peak":
        lapel = f"M{bx},{brk} L262,92 L232,142 L168,118 C178,210 268,{brk - 90} {bx},{brk} Z"
        collar = "M300,44 C280,46 262,50 252,58 L232,124 L238,132 L262,92 Z"
    else:
        lapel = f"M{bx},{brk} L262,92 L226,152 L188,166 C204,252 262,{brk - 70} {bx},{brk} Z"
        collar = "M300,44 C280,46 262,50 252,58 L210,136 L226,152 L262,92 Z"
    return lapel, collar


def buttons(variant: str, fastened: list[int]) -> list[dict]:
    """Button positions (viewBox coordinates) with state."""
    v = VARIANTS[variant]
    out = []
    if v["db"]:
        rows = [(386, None)] + [(y, i) for i, y in enumerate(v["buttons"])]
        for y, idx in rows:
            for x in (CX - 62, CX + 62):
                closed = idx is not None and idx in fastened and x == CX + 62
                out.append({"x": x, "y": y, "idx": idx, "fastened": closed, "decor": idx is None or x == CX - 62})
        return out
    _, join = _edge_left(variant, fastened)
    for i, y in enumerate(v["buttons"]):
        closed = i in fastened
        # an open button below the join sits on the right panel, a little off the centre line
        x = CX if (closed or y <= join) else CX + 16
        out.append({"x": x, "y": y, "idx": i, "fastened": closed, "decor": False})
    return out


def point(variant: str, name: str, fastened: list[int] | None = None) -> tuple[float, float]:
    """Named detail -> (x, y) in the viewBox: button:N, lapel, notch, collar, pocket, chest, hem, shoulder, quarters."""
    fastened = fastened or []
    v = VARIANTS[variant]
    if name.startswith("button:"):
        i = int(name.split(":")[1])
        b = [b for b in buttons(variant, fastened) if b["idx"] == i and not (v["db"] and b["x"] == CX - 62)]
        return (b[0]["x"], b[0]["y"]) if b else (CX, v["buttons"][-1])
    return {
        "lapel": (214, 240), "notch": (222, 150) if v["lapel"] == "notch" else (214, 132), "collar": (262, 70),
        "pocket": (216, 574), "chest": (403, 252), "hem": (CX, HEM_Y - 10), "shoulder": (116, 96),
        "quarters": (CX, 640), "break": (CX, v["break"]), "sleeve": (90, 560), "waist": (CX, 470),
        "lapel_hole": (385, 194), "cuff": (111, 628), "ticket": (217, 530), "neck": (CX, 92), "lapel_r": (386, 240),
    }[name]


def jacket_svg(uid: str, variant: str = "sb2", fastened: list[int] | None = None, *, strain: bool = False,
               lines_class: str = "ln", accent: str = "#D4B483", colors: dict | None = None, ring: list[str] | None = None,
               lapel: str | None = None, dinner: bool = False, neck: str = "tie", pockets: str = "flap",
               ticket: bool = False, flower: bool = False, lapel_hole: bool = False, cuff: float = 0.0,
               chest_pocket: bool = True) -> str:
    """SVG for one jacket. Line paths carry `pathLength=1` and the class `lines_class` so a scene can draw them in.

    Layers: fill (cloth with twill texture), shirt and tie in the V, lines (outline, lapels, seams, pockets),
    buttons, optional strain lines (class `strain`). `uid` keeps pattern ids unique within the page.
    Options (Woche 1, 01.11.2026): `lapel` notch|peak|shawl, `dinner` (black cloth, satin facings, covered buttons),
    `neck` tie|bow|none|open, `pockets` flap|jetted|patch, `ticket`, `flower` / `lapel_hole` (left lapel, viewer right),
    `cuff` = visible shirt cuff below the sleeve in viewBox units (0 = none)."""
    fastened = list(fastened if fastened is not None else [0])
    col = {**COLORS, **(colors or {})}
    if dinner:
        col.update({"fill": "#15171C", "lapel": "#24272F", "shirt": "#F4F1EA"})
        pockets = "jetted"
    v = VARIANTS[variant]
    body_l = _left_body(variant, fastened)
    if v["db"]:
        body_r = _mirror(_left_body("sb2", [0]))  # under panel, hidden below the top panel
    else:
        body_r = _mirror(body_l)
    lap_l, col_l = _lapel_left(variant, lapel)
    lap_r = _mirror(lap_l)
    col_r = _mirror(col_l)
    if v["db"] and (lapel or v["lapel"]) == "peak":
        # right lapel rolls to the same break on the overlapping edge
        lap_r = f"M{DB_EDGE},{v['break']} L338,92 L368,142 L432,118 C428,220 {DB_EDGE + 10},{v['break'] - 120} {DB_EDGE},{v['break']} Z"
    sleeve_l = "M116,96 C96,120 88,160 86,220 C82,350 76,480 72,612 L150,624 C154,500 156,380 160,280 C150,200 132,140 116,96 Z"
    sleeve_r = _mirror(sleeve_l)
    vb = v["break"]
    vx = DB_EDGE if v["db"] else CX
    shirt = f"M{CX - 40},58 L{vx},{vb} L{CX + 40},58 Z"
    tie = (f"M{CX - 12},80 L{CX + 12},80 L{CX + 7},104 L{CX + 14},{min(vb - 10, 360)} L{CX},{min(vb + 6, 378)} "
           f"L{CX - 14},{min(vb - 10, 360)} L{CX - 7},104 Z")
    bow = (f"M{CX},92 L{CX - 34},78 L{CX - 30},92 L{CX - 34},106 Z M{CX},92 L{CX + 34},78 L{CX + 30},92 L{CX + 34},106 Z "
           f"M{CX - 7},85 L{CX + 7},85 L{CX + 7},99 L{CX - 7},99 Z")
    shirt_collar = f"M{CX - 40},58 L{CX - 14},96 L{CX - 2},76 M{CX + 40},58 L{CX + 14},96 L{CX + 2},76"
    if neck == "open":
        shirt_collar = f"M{CX - 40},58 L{CX - 30},110 L{CX - 4},84 M{CX + 40},58 L{CX + 30},110 L{CX + 4},84"
    if pockets == "jetted":
        pocket_l = "M168,566 L262,573 L262,580 L168,573 Z"
    elif pockets == "patch":
        pocket_l = "M162,544 L266,552 L262,652 C261,660 256,664 248,663 L178,657 C170,656 166,651 166,643 Z"
    else:
        pocket_l = "M168,560 L262,567 L262,592 L168,585 Z"
    pocket_r = _mirror(pocket_l)
    ticket_p = "M182,518 L252,523 L252,541 L182,536 Z"
    chest = "M372,258 L434,248 L436,262 L374,272 Z"
    dart_l = "M214,300 C218,400 218,480 216,556"
    dart_r = _mirror(dart_l)
    tw = f"{uid}-tw"
    lc = lines_class
    sh = f"{uid}-sh"
    sat = f"{uid}-sat"

    def cloth(p: str, fill: str, satin: bool = False) -> str:
        # cloth, twill (or satin sheen), one light from the top left (volume, Q1) and the line on top
        tex = f'<path class="fill" d="{p}" fill="url(#{sat})"/>' if satin else f'<path class="fill" d="{p}" fill="url(#{tw})"/>'
        return (f'<path class="fill" d="{p}" fill="{fill}"/>{tex}'
                f'<path class="fill shade" d="{p}" fill="url(#{sh})"/><path class="{lc}" pathLength="1" d="{p}"/>')

    extra = (chest,) if chest_pocket else ()
    extra += (ticket_p,) if ticket else ()
    parts = [cloth(body_r, col["fill"]), cloth(body_l, col["fill"])]
    parts += [f'<path class="{lc} seam" pathLength="1" d="{p}"/>' for p in (dart_l, dart_r)]
    parts += [cloth(p, col["fill"]) for p in (pocket_l, pocket_r) + extra]
    if cuff:
        c = float(cuff)
        band = f"M73,610 L151,622 L150,{622 + c:g} L72,{610 + c:g} Z"
        parts.append(f'<path class="fill" d="{band}" fill="{col["shirt"]}"/><path class="fill" d="{_mirror(band)}" fill="{col["shirt"]}"/>'
                     f'<path class="{lc} thin cuffl" pathLength="1" d="M72,{610 + c:g} L150,{622 + c:g} {_mirror(f"M72,{610 + c:g} L150,{622 + c:g}")}"/>')
    parts += [cloth(p, col["fill"]) for p in (sleeve_l, sleeve_r)]
    parts.append(f'<path class="fill" d="{shirt}" fill="{col["shirt"]}"/>')
    if neck == "tie":
        parts.append(f'<path class="fill" d="{tie}" fill="{col["tie"]}"/>')
    elif neck == "bow":
        parts.append(f'<path class="fill" d="{bow}" fill="#0E0F12"/><path class="{lc} thin" pathLength="1" d="{bow}"/>')
        parts += [f'<circle class="fill" cx="{CX}" cy="{y}" r="3.2" fill="#0E0F12"/>' for y in (140, 200, 260) if y < vb - 20]
    elif neck in ("none", "open"):
        parts.append(f'<path class="{lc} thin" pathLength="1" d="M{CX},100 L{CX},{vb - 6}"/>')
    parts.append(f'<path class="{lc} thin" pathLength="1" d="{shirt_collar}"/>')
    parts += [cloth(p, col["lapel"], satin=dinner) for p in (lap_r, lap_l, col_r, col_l)]
    if lapel_hole or flower:
        parts.append(f'<path class="{lc} thin hole2" pathLength="1" d="M374,200 L396,190"/>')
    if flower:
        fl = "".join(f'<circle class="fill" cx="{385 + 12 * dx:g}" cy="{190 + 12 * dy:g}" r="9" fill="#E9E3D7"/>'
                     for dx, dy in ((0, -1), (0.95, -0.3), (0.6, 0.8), (-0.6, 0.8), (-0.95, -0.3)))
        parts.append(f'<g class="flower">{fl}<circle class="fill" cx="385" cy="190" r="6" fill="{accent}"/>'
                     f'<path class="{lc} thin" pathLength="1" d="M385,198 C383,220 380,236 376,252"/></g>')
    line_html = "".join(parts)
    btn_html = ""
    bst = ' style="fill:#24272F"' if dinner else ""
    for b in buttons(variant, fastened):
        hole = "" if b["decor"] else f'<line class="hole" x1="{b["x"] - 30}" y1="{b["y"]}" x2="{b["x"] - 14}" y2="{b["y"]}"/>' if b["fastened"] else \
            (f'<line class="hole" x1="{CX - 30}" y1="{b["y"]}" x2="{CX - 14}" y2="{b["y"]}"/>' if b["x"] != CX else "")
        btn_html += f'{hole}<circle class="btn{" open" if not b["fastened"] else ""}" cx="{b["x"]}" cy="{b["y"]}" r="11"{bst}/>'
    strain_html = ""
    if strain:
        y = v["buttons"][-1]
        for d in (f"M{CX - 6},{y - 4} C{CX - 40},{y - 26} {CX - 70},{y - 46} {CX - 96},{y - 70}",
                  f"M{CX - 6},{y + 4} C{CX - 44},{y + 22} {CX - 80},{y + 30} {CX - 112},{y + 34}",
                  f"M{CX - 8},{y - 14} C{CX - 30},{y - 50} {CX - 44},{y - 80} {CX - 52},{y - 112}"):
            strain_html += f'<path class="strain" pathLength="1" d="{d}"/><path class="strain" pathLength="1" d="{_mirror(d)}"/>'
    rings = ""
    for name in ring or []:
        x, y = point(variant, name, fastened)
        rings += f'<circle class="ring" pathLength="1" cx="{x}" cy="{y}" r="30"/>'
    return f"""<svg class="jacket" viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="{tw}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{accent}" stroke-opacity="0.09" stroke-width="2"/></pattern>
<linearGradient id="{sat}" gradientUnits="userSpaceOnUse" x1="180" y1="60" x2="420" y2="420"><stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.04"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.16"/></linearGradient>
<linearGradient id="{sh}" gradientUnits="userSpaceOnUse" x1="110" y1="40" x2="500" y2="760"><stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/><stop offset="0.42" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.34"/></linearGradient></defs>
<g class="cloth">{line_html}</g><g class="btns">{btn_html}</g><g class="strains">{strain_html}</g><g class="rings">{rings}</g>
</svg>"""


def front_edge(variant: str, fastened: list[int] | None = None) -> str:
    """Both front edges from the lowest fastened button (or the break) down to the hem, as one path (viewBox
    coordinates): the line that shows how the jacket opens over the hips (cut line, ghost outline)."""
    fastened = list(fastened if fastened is not None else [0])
    if VARIANTS[variant]["db"]:
        return f"M{DB_EDGE},{VARIANTS[variant]['break']} L{DB_EDGE},{HEM_Y}"
    seg, _ = _edge_left(variant, fastened)
    left = f"M{CX},{VARIANTS[variant]['break']} {seg}"
    return f"{left} {_mirror(left)}"


def mini_jacket(uid: str, variant: str, fastened: list[int], *, strain: bool = False) -> str:
    """Small pictogram version (same drawing, used in take-away cards)."""
    return jacket_svg(uid, variant, fastened, strain=strain, lines_class="lnm")
