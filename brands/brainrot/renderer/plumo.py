"""Plümo, the recurring character of Zonkfruit (brand_id brainrot): SVG generator, code only (no AI image).

One function builds the character in three views (front, side, back) and six poses. Every variable part
(lids, pupils, mouths, stem, leaf, body) is its own element with a stable id `<uid>-<part>` so scene
templates can animate expressions with GSAP (scaleY on lids, opacity on mouths, rotation on the leaf,
squash/stretch on the body). Static poses set the same parts through SVG attributes.

Style lock (see assets/character/character.md): colours below are fixed; silhouette, spring stem,
magenta leaf as the only "hand", heavy deadpan lids, three freckles on the right cheek and the "?" sticker
on the back never change. Draft until Stefan approves the character.
"""
from __future__ import annotations

# fixed colours (hex) -------------------------------------------------------------------------------
C = {
    "body": "#B7FF00",        # lime (brand accent)
    "body_hi": "#ECFFA6",     # highlight
    "body_mid": "#8FD600",    # mid shade
    "body_lo": "#4E8C00",     # core shadow
    "lid": "#9BE000",         # eyelid skin
    "line": "#2C4F00",        # lid edge, outline accents
    "rim": "#FF43C0",         # magenta rim light (surreal 3D look)
    "leaf": "#FF43C0",        # leaf = his only hand
    "leaf_lo": "#C21F8C",
    "vein": "#7A1F5E",
    "stem": "#B04A92",        # spring stem, light plum (readable on #101010)
    "eye": "#FFF7FB",
    "pupil": "#101010",
    "mouth": "#3B0F31",
    "freckle": "#FF43C0",
    "sticker": "#FFF2C7",
    "sticker_ink": "#101010",
    "shadow": "#000000",
}

VIEWBOX = "-60 -110 520 600"        # body sits on y=440, stem/leaf need head room, leaf can point sideways
BODY = "M200,92 C292,92 346,176 356,276 C366,378 318,442 200,442 C82,442 34,378 44,276 C54,176 108,92 200,92 Z"
SPRING = "M200,96 c-22,-5 -22,-19 0,-23 c22,-4 22,-18 0,-22 c-22,-5 -22,-19 0,-23 c18,-3 20,-12 6,-18"
LEAF = "M206,10 C226,-28 286,-38 322,-12 C292,18 244,30 206,10 Z"
LEAF_VEIN = "M210,9 C240,-6 276,-14 312,-12"

POSES = {
    # name: lids (0 open .. 1 shut), pupil dx, dy, r, mouth, leaf rotation (deg, around stem tip), body tilt, squash
    "neutral":   dict(lid_l=0.46, lid_r=0.46, pdx=0, pdy=4, pr=11, mouth="flat", leaf=28, tilt=0, sy=1.0, stem=1.0),
    "staunen":   dict(lid_l=0.0, lid_r=0.0, pdx=0, pdy=0, pr=7, mouth="o", leaf=-34, tilt=0, sy=1.08, stem=1.22),
    "stolz":     dict(lid_l=0.62, lid_r=0.62, pdx=-6, pdy=-4, pr=11, mouth="smug", leaf=118, tilt=-7, sy=1.02, stem=1.0),
    "zeigen":    dict(lid_l=0.35, lid_r=0.35, pdx=12, pdy=2, pr=11, mouth="talk", leaf=-4, tilt=4, sy=1.0, stem=1.05),
    "verwirrt":  dict(lid_l=0.05, lid_r=0.6, pdx=-4, pdy=0, pr=10, mouth="wavy", leaf=70, tilt=-4, sy=0.98, stem=0.9),
    "umgekippt": dict(lid_l=1.0, lid_r=1.0, pdx=0, pdy=0, pr=11, mouth="flat", leaf=150, tilt=90, sy=0.94, stem=0.8),
}

MOUTHS = {
    "flat": f'<path d="M180,318 Q200,322 220,318" fill="none" stroke="{C["mouth"]}" stroke-width="7" stroke-linecap="round"/>',
    "o": f'<ellipse cx="200" cy="322" rx="15" ry="19" fill="{C["mouth"]}"/><ellipse cx="200" cy="330" rx="8" ry="6" fill="#B23A86"/>',
    "smug": f'<path d="M178,320 Q202,326 224,310" fill="none" stroke="{C["mouth"]}" stroke-width="7" stroke-linecap="round"/>',
    "talk": f'<ellipse cx="200" cy="320" rx="17" ry="10" fill="{C["mouth"]}"/>',
    "wavy": f'<path d="M176,320 q8,-7 16,0 t16,0 t16,0" fill="none" stroke="{C["mouth"]}" stroke-width="6" stroke-linecap="round"/>',
}


def _defs(u: str) -> str:
    return f"""<defs>
<radialGradient id="{u}-g" cx="0.36" cy="0.30" r="0.78">
 <stop offset="0" stop-color="{C['body_hi']}"/><stop offset="0.32" stop-color="{C['body']}"/>
 <stop offset="0.78" stop-color="{C['body_mid']}"/><stop offset="1" stop-color="{C['body_lo']}"/></radialGradient>
<linearGradient id="{u}-rim" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0.72" stop-color="{C['rim']}" stop-opacity="0"/><stop offset="1" stop-color="{C['rim']}" stop-opacity="0.55"/></linearGradient>
<linearGradient id="{u}-leafg" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="{C['leaf']}"/><stop offset="1" stop-color="{C['leaf_lo']}"/></linearGradient>
<radialGradient id="{u}-sh" cx="0.5" cy="0.5" r="0.5">
 <stop offset="0" stop-color="{C['shadow']}" stop-opacity="0.55"/><stop offset="1" stop-color="{C['shadow']}" stop-opacity="0"/></radialGradient>
<clipPath id="{u}-clipL"><ellipse cx="158" cy="236" rx="31" ry="35"/></clipPath>
<clipPath id="{u}-clipR"><ellipse cx="244" cy="236" rx="31" ry="35"/></clipPath>
<clipPath id="{u}-clipB"><path d="{BODY}"/></clipPath>
<clipPath id="{u}-clipS"><ellipse cx="96" cy="236" rx="22" ry="34"/></clipPath>
</defs>"""


def _eye(u: str, side: str, cx: int, lid: float, p: dict) -> str:
    # lid: rect from the top of the eye; templates animate attr height / line y1,y2 (see lid_attrs) to blink
    h, ly = lid_attrs(lid)
    return (f'<g id="{u}-eye{side}"><ellipse cx="{cx}" cy="236" rx="31" ry="35" fill="{C["eye"]}"/>'
            f'<g id="{u}-pup{side}" transform="translate({p["pdx"]},{p["pdy"]})">'
            f'<circle id="{u}-pc{side}" cx="{cx}" cy="240" r="{p["pr"]}" fill="{C["pupil"]}"/><circle cx="{cx + 4}" cy="235" r="3.5" fill="#FFFFFF"/></g>'
            f'<g clip-path="url(#{u}-clip{side})"><rect id="{u}-lid{side}" x="{cx - 34}" y="{EYE_TOP}" width="68" height="{h}" fill="{C["lid"]}"/>'
            f'<line id="{u}-lin{side}" x1="{cx - 34}" y1="{ly}" x2="{cx + 34}" y2="{ly}" stroke="{C["line"]}" stroke-width="6"/></g>'
            f'<ellipse cx="{cx}" cy="236" rx="31" ry="35" fill="none" stroke="{C["line"]}" stroke-width="3" opacity="0.55"/></g>')


EYE_TOP = 236 - 35


def lid_attrs(lid: float) -> tuple[float, float]:
    """(rect height, edge line y) for a lid closure 0..1; a fully open lid parks its edge line above the eye."""
    h = round(72 * lid, 2)
    return h, round(EYE_TOP + h - 1 if lid > 0.04 else EYE_TOP - 8, 2)


def _stem_and_leaf(u: str, p: dict, back: bool = False) -> str:
    leaf_fill = f"url(#{u}-leafg)" if not back else C["leaf_lo"]
    return (f'<g id="{u}-stem" transform="translate(200,96) scale(1,{p["stem"]:.3f}) translate(-200,-96)">'
            f'<path d="{SPRING}" fill="none" stroke="{C["stem"]}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<g id="{u}-leaf" transform="rotate({p["leaf"]},206,10)"><path d="{LEAF}" fill="{leaf_fill}"/>'
            f'<path d="{LEAF_VEIN}" fill="none" stroke="{C["vein"]}" stroke-width="4" stroke-linecap="round" opacity="0.8"/></g></g>')


def _body(u: str) -> str:
    return (f'<path d="{BODY}" fill="url(#{u}-g)"/>'
            f'<path d="{BODY}" fill="url(#{u}-rim)"/>'
            f'<ellipse cx="146" cy="168" rx="38" ry="22" fill="#FFFFFF" opacity="0.28" transform="rotate(-24,146,168)"/>')


def _freckles(dx: int = 0) -> str:
    # three magenta freckles in a triangle on his right cheek (viewer's left); never moved, never mirrored
    pts = [(116, 290, 7), (138, 302, 6), (112, 312, 5)]
    return "".join(f'<circle cx="{x + dx}" cy="{y}" r="{r}" fill="{C["freckle"]}"/>' for x, y, r in pts)


def _sticker(cx: int = 200, cy: int = 300, scale: float = 1.0, u: str = "") -> str:
    rx, ry = 46 * scale, 34 * scale
    return (f'<g id="{u}-sticker"><ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{C["sticker"]}" stroke="{C["sticker_ink"]}" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy + 15 * scale:.1f}" text-anchor="middle" font-family="FN Fredoka, Fredoka, sans-serif" font-weight="700" '
            f'font-size="{44 * scale:.0f}" fill="{C["sticker_ink"]}">?</text></g>')


def plumo_svg(pose: str = "neutral", view: str = "front", uid: str = "p", *, width: int | None = None,
              css_class: str = "plumo", shadow: bool = True, all_mouths: bool = False) -> str:
    """Return an inline <svg> of Plümo. `all_mouths=True` emits every mouth (non-active ones at opacity 0)
    with ids `<uid>-m-<name>` so templates can switch expressions over time."""
    p = POSES[pose]
    u = uid
    w = f' width="{width}"' if width else ""
    sh = f'<ellipse id="{u}-shadow" cx="200" cy="446" rx="150" ry="22" fill="url(#{u}-sh)"/>' if shadow else ""
    if view == "front":
        if all_mouths:
            mouths = "".join(f'<g id="{u}-m-{n}" opacity="{1 if n == p["mouth"] else 0}">{m}</g>' for n, m in MOUTHS.items())
        else:
            mouths = f'<g id="{u}-m-{p["mouth"]}">{MOUTHS[p["mouth"]]}</g>'
        face = _eye(u, "L", 158, p["lid_l"], p) + _eye(u, "R", 244, p["lid_r"], p) + _freckles() + f'<g id="{u}-mouth">{mouths}</g>'
        inner = _body(u) + f'<g id="{u}-face">{face}</g>'
        stem = _stem_and_leaf(u, p)
    elif view == "side":     # profile facing left: freckled right cheek, one eye, sticker edge at the back
        eye = (f'<ellipse cx="96" cy="236" rx="22" ry="34" fill="{C["eye"]}"/>'
               f'<circle cx="{86 + min(p["pdx"], 0)}" cy="242" r="{max(p["pr"] - 2, 5)}" fill="{C["pupil"]}"/>'
               f'<g clip-path="url(#{u}-clipS)"><rect x="70" y="201" width="52" height="{max(p["lid_l"], 0.001) * 70:.1f}" fill="{C["lid"]}"/>'
               f'<line x1="70" y1="{201 + p["lid_l"] * 70:.1f}" x2="122" y2="{201 + p["lid_l"] * 70:.1f}" stroke="{C["line"]}" stroke-width="6"/></g>')
        mouth = f'<path d="M46,318 Q60,322 74,316" fill="none" stroke="{C["mouth"]}" stroke-width="7" stroke-linecap="round"/>'
        freck = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C["freckle"]}"/>' for x, y, r in [(150, 292, 7), (170, 304, 6), (146, 314, 5)])
        inner = _body(u) + f'<g id="{u}-face">{eye}{mouth}{freck}</g>'
        stem = _stem_and_leaf(u, {**p, "leaf": p["leaf"] + 150})
    elif view == "back":
        inner = _body(u).replace(f"url(#{u}-rim)", "none") + f'<path d="M200,120 C214,200 214,380 200,430" fill="none" stroke="{C["body_mid"]}" stroke-width="5" opacity="0.7"/>' + _sticker(u=u)
        stem = _stem_and_leaf(u, {**p, "leaf": 180 - p["leaf"]}, back=True)
    else:
        raise ValueError(view)
    tilt = p["tilt"]
    # pivot for tilting: bottom-right corner of the body when falling to the right (the "Zonk"), bottom centre otherwise
    pivot = "330,430" if tilt >= 60 else "200,440"
    lift = ' translate(-14,293)' if tilt >= 60 else ""   # lying on the right side, moved back over the footprint
    body_g = (f'<g id="{u}-all" transform="rotate({tilt},{pivot}){lift}">'
              f'<g id="{u}-squash" transform="translate(200,442) scale({2 - p["sy"]:.3f},{p["sy"]:.3f}) translate(-200,-442)">'
              f'{stem}<g id="{u}-body">{inner}</g></g></g>')
    return (f'<svg class="{css_class}" id="{u}" viewBox="{VIEWBOX}"{w} xmlns="http://www.w3.org/2000/svg" overflow="visible">'
            f'{_defs(u)}{sh}{body_g}</svg>')


def logo_svg() -> str:
    """Small brand mark: Plümo's head (lime circle, deadpan lids, magenta leaf), for the logo slot."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
<circle cx="60" cy="68" r="48" fill="{C['body']}"/>
<path d="M60,22 c-8,-2 -8,-8 0,-10 c8,-2 8,-7 0,-9" fill="none" stroke="{C['stem']}" stroke-width="5" stroke-linecap="round"/>
<path d="M62,6 C70,-6 92,-8 104,2 C94,12 76,16 62,6 Z" fill="{C['leaf']}"/>
<ellipse cx="44" cy="62" rx="11" ry="12" fill="{C['eye']}"/><ellipse cx="76" cy="62" rx="11" ry="12" fill="{C['eye']}"/>
<rect x="32" y="49" width="24" height="12" fill="{C['lid']}"/><rect x="64" y="49" width="24" height="12" fill="{C['lid']}"/>
<line x1="32" y1="61" x2="56" y2="61" stroke="{C['line']}" stroke-width="3"/><line x1="64" y1="61" x2="88" y2="61" stroke="{C['line']}" stroke-width="3"/>
<circle cx="44" cy="66" r="4" fill="{C['pupil']}"/><circle cx="76" cy="66" r="4" fill="{C['pupil']}"/>
<path d="M52,88 Q60,90 68,88" fill="none" stroke="{C['mouth']}" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="30" cy="80" r="3" fill="{C['freckle']}"/><circle cx="37" cy="86" r="2.6" fill="{C['freckle']}"/><circle cx="29" cy="90" r="2.2" fill="{C['freckle']}"/>
</svg>
"""
