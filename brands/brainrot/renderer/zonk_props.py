"""Zonkfruit props: plain objects, plants and animals drawn in code (viewBox 0 0 220 240), never with faces.

Only Plümo has a face (character rule). Animals are shown as faceless silhouettes or from behind. Every prop is a
function uid -> SVG body; gradient ids are prefixed with the uid so several copies can live on one page.
Used by zonk_templates.fruit_svg (scan items, zoom fruit, diagram inner, compare bars, lens content).
"""
from __future__ import annotations

import math


def _rg(uid: str, name: str, stops: list[tuple[float, str]], cx: float = 0.35, cy: float = 0.3, r: float = 0.8) -> str:
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{uid}-{name}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def _lg(uid: str, name: str, stops: list[tuple[float, str]], x2: float = 0, y2: float = 1) -> str:
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{uid}-{name}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def sun(u):
    rays = "".join(f'<path d="M110,120 L{110 + 104 * math.cos(math.radians(a - 7)):.1f},{120 + 104 * math.sin(math.radians(a - 7)):.1f} '
                   f'L{110 + 104 * math.cos(math.radians(a + 7)):.1f},{120 + 104 * math.sin(math.radians(a + 7)):.1f} Z" fill="#FFB800"/>'
                   for a in range(0, 360, 30))
    return f'<defs>{_rg(u, "s", [(0, "#FFF7C2"), (0.55, "#FFD84D"), (1, "#F08A00")])}</defs>{rays}<circle cx="110" cy="120" r="62" fill="url(#{u}-s)"/>'


def pineapple(u):
    cells = "".join(f'<path d="M{x},{y} l14,-12 l14,12 l-14,12 Z" fill="none" stroke="#9A5B00" stroke-width="3"/>'
                    for y in range(104, 222, 22) for x in range(52 + (11 if (y // 22) % 2 else 0), 156, 28))
    return (f'<defs>{_rg(u, "p", [(0, "#FFE58A"), (0.5, "#F2B21C"), (1, "#B86E00")])}</defs>'
            f'<path d="M110,92 L84,20 L104,60 L110,8 L116,60 L136,20 Z" fill="#3FAF3A"/><path d="M110,92 L62,40 L100,72 Z M110,92 L158,40 L120,72 Z" fill="#2E8A2A"/>'
            f'<ellipse cx="110" cy="164" rx="64" ry="76" fill="url(#{u}-p)"/>{cells}')


def fruitlet(u):
    return (f'<defs>{_rg(u, "f", [(0, "#FFF0A8"), (0.6, "#F2B21C"), (1, "#B86E00")])}</defs>'
            + "".join(f'<path d="M{x},{y} l40,-34 l40,34 l-40,34 Z" fill="url(#{u}-f)" stroke="#8A4D00" stroke-width="5"/>'
                      for x, y in [(30, 70), (110, 70), (70, 120), (-10, 120), (150, 120), (30, 170), (110, 170), (70, 220)])
            + '<circle cx="110" cy="120" r="6" fill="#8A4D00"/>')


def apple(u):
    return (f'<defs>{_rg(u, "a", [(0, "#FF9A8A"), (0.5, "#E8283A"), (1, "#8A0B1C")])}</defs>'
            f'<path d="M110,64 C150,40 196,70 190,130 C186,190 150,226 126,222 C118,220 114,216 110,216 C106,216 102,220 94,222 C70,226 34,190 30,130 C24,70 70,40 110,64 Z" fill="url(#{u}-a)"/>'
            '<path d="M110,64 C108,46 112,30 122,18" stroke="#5A3A1A" stroke-width="7" fill="none" stroke-linecap="round"/>'
            '<path d="M118,40 C138,20 166,24 172,34 C150,46 132,46 118,40 Z" fill="#3FAF3A"/>')


def apple_slice(u, brown: bool = False):
    flesh = "#C98A4A" if brown else "#FFF6D6"
    return (f'<path d="M20,150 C20,80 70,40 110,40 C150,40 200,80 200,150 Z" fill="#E8283A"/>'
            f'<path d="M30,150 C30,90 74,54 110,54 C146,54 190,90 190,150 Z" fill="{flesh}" class="zflesh"/>'
            '<path d="M100,118 C100,104 106,96 110,96 C114,96 120,104 120,118 C120,128 114,134 110,134 C106,134 100,128 100,118 Z" fill="#6B4220"/>')


def apple_brown(u):
    return apple_slice(u, brown=True)


def starfish(u):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        r = 100 if k % 2 == 0 else 40
        pts.append(f"{110 + r * math.cos(a):.1f},{124 + r * math.sin(a):.1f}")
    dots = "".join(f'<circle cx="{110 + rr * math.cos(math.radians(-90 + k * 72)):.1f}" cy="{124 + rr * math.sin(math.radians(-90 + k * 72)):.1f}" r="5" fill="#FFD0A0"/>'
                   for k in range(5) for rr in (30, 52, 72))
    return f'<defs>{_rg(u, "s", [(0, "#FFB38A"), (0.6, "#F0643A"), (1, "#A8301A")], 0.5, 0.5)}</defs><polygon points="{" ".join(pts)}" fill="url(#{u}-s)" stroke="#8A2A10" stroke-width="4" stroke-linejoin="round"/>{dots}'


def fish(u):
    return (f'<defs>{_lg(u, "f", [(0, "#8AD8FF"), (1, "#2A7FC0")])}</defs>'
            f'<path d="M30,120 C60,70 140,70 170,120 C140,170 60,170 30,120 Z" fill="url(#{u}-f)"/><path d="M168,120 L212,86 L204,120 L212,154 Z" fill="#2A7FC0"/>'
            '<path d="M80,80 L100,52 L118,82 Z" fill="#2A7FC0"/><path d="M60,120 C70,108 70,132 60,120" stroke="#1A5A90" stroke-width="4" fill="none"/>')


def helmet(u):
    return (f'<defs>{_rg(u, "v", [(0, "#BFE8FF"), (0.6, "#3A6FA8"), (1, "#14243A")])}</defs>'
            '<circle cx="110" cy="118" r="96" fill="#E8ECF2" stroke="#9AA3B2" stroke-width="6"/>'
            f'<ellipse cx="110" cy="112" rx="70" ry="60" fill="url(#{u}-v)"/><path d="M70,84 C84,70 104,66 116,68" stroke="#ffffff" stroke-opacity="0.7" stroke-width="8" fill="none" stroke-linecap="round"/>'
            '<rect x="56" y="200" width="108" height="30" rx="12" fill="#C9CFD9"/>')


def speaker(u):
    return ('<rect x="40" y="40" width="140" height="180" rx="22" fill="#2A2230" stroke="#FF43C0" stroke-width="6"/>'
            '<circle cx="110" cy="92" r="26" fill="#120d16" stroke="#B04A92" stroke-width="5"/><circle cx="110" cy="164" r="40" fill="#120d16" stroke="#B04A92" stroke-width="6"/>'
            '<circle cx="110" cy="164" r="12" fill="#B04A92"/>')


def soundwave(u):
    return "".join(f'<path d="M{60 + 34 * k},{120 - 60 + 12 * k} C{80 + 34 * k},{120 - 30} {80 + 34 * k},{120 + 30} {60 + 34 * k},{120 + 60 - 12 * k}" '
                   f'stroke="#B7FF00" stroke-width="10" fill="none" stroke-linecap="round" opacity="{1 - k * 0.22:.2f}"/>' for k in range(4)) \
        + '<circle cx="40" cy="120" r="16" fill="#FF43C0"/>'


def flytrap(u):
    teeth = "".join(f'<path d="M{48 + 14 * k},{96} l6,-18 l6,18 Z" fill="#B7FF00"/>' for k in range(9))
    teeth2 = "".join(f'<path d="M{48 + 14 * k},{124} l6,18 l6,-18 Z" fill="#B7FF00"/>' for k in range(9))
    return (f'<defs>{_rg(u, "t", [(0, "#FF8A9C"), (1, "#B0122E")], 0.5, 0.5)}</defs>'
            '<path d="M110,230 C110,190 100,170 110,140" stroke="#3FAF3A" stroke-width="12" fill="none"/>'
            f'<path d="M40,98 C60,40 160,40 180,98 Z" fill="url(#{u}-t)" stroke="#3FAF3A" stroke-width="8" class="zjaw-top"/>'
            f'<path d="M40,122 C60,180 160,180 180,122 Z" fill="url(#{u}-t)" stroke="#3FAF3A" stroke-width="8"/>{teeth}{teeth2}'
            '<line x1="90" y1="78" x2="96" y2="92" stroke="#FFF2C7" stroke-width="4"/><line x1="124" y1="78" x2="118" y2="92" stroke="#FFF2C7" stroke-width="4"/>')


def fly(u):
    return ('<ellipse cx="110" cy="130" rx="40" ry="28" fill="#2A2A30"/><ellipse cx="80" cy="96" rx="34" ry="20" fill="#CFE9FF" opacity="0.8" transform="rotate(-25,80,96)"/>'
            '<ellipse cx="140" cy="96" rx="34" ry="20" fill="#CFE9FF" opacity="0.8" transform="rotate(25,140,96)"/><circle cx="66" cy="132" r="18" fill="#2A2A30"/>')


def icecube(u):
    return (f'<defs>{_lg(u, "i", [(0, "#F2FBFF"), (1, "#8FD3F2")], 1, 1)}</defs>'
            '<path d="M50,90 L120,60 L190,90 L190,180 L120,214 L50,180 Z" fill="#BFE9FF" stroke="#6FB8E0" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M50,90 L120,60 L190,90 L120,120 Z" fill="url(#{u}-i)"/><path d="M120,120 L120,214" stroke="#6FB8E0" stroke-width="4"/>'
            '<path d="M70,104 L96,94" stroke="#ffffff" stroke-width="7" stroke-linecap="round"/>')


def glass(u):
    return ('<path d="M44,40 L176,40 L160,226 L60,226 Z" fill="#CFEFFF" fill-opacity="0.25" stroke="#E8F7FF" stroke-width="6"/>'
            '<path d="M52,110 L168,110 L160,222 L60,222 Z" fill="#3AA0E0" fill-opacity="0.65"/><path d="M52,110 L168,110" stroke="#BFE9FF" stroke-width="5"/>'
            '<path d="M88,84 L132,74 L148,104 L104,116 Z" fill="#E8F7FF" stroke="#8FD3F2" stroke-width="4"/>')


def sloth(u):     # hanging from a branch, seen as a faceless furry silhouette
    return (f'<defs>{_rg(u, "f", [(0, "#C9B08A"), (0.6, "#8A7350"), (1, "#5A4A30")])}</defs>'
            '<rect x="0" y="22" width="220" height="16" rx="8" fill="#6B4220"/>'
            '<path d="M60,30 C56,60 62,80 70,96 M160,30 C164,60 158,80 150,96" stroke="#8A7350" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="110" cy="140" rx="66" ry="76" fill="url(#{u}-f)"/>'
            '<path d="M70,120 C90,110 100,140 120,128 C140,118 150,150 160,140" stroke="#7FB04A" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.85"/>'
            '<path d="M60,170 C84,162 100,186 126,176 C146,168 156,186 166,180" stroke="#7FB04A" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.7"/>')


def hair_algae(u):
    return ('<rect x="70" y="0" width="80" height="240" rx="30" fill="#A8906A"/>'
            + "".join(f'<path d="M{86 + 16 * k},10 L{86 + 16 * k},230" stroke="#7A6448" stroke-width="5"/>' for k in range(4))
            + "".join(f'<circle cx="{92 + 16 * (k % 4)}" cy="{30 + 22 * k}" r="7" fill="#5FC23A"/>' for k in range(9)))


def jackfruit(u):
    bumps = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#9AB82A"/>' for y in range(40, 220, 16) for x in range(56 + (8 if (y // 16) % 2 else 0), 170, 16)
                    if ((x - 110) / 60) ** 2 + ((y - 128) / 96) ** 2 < 0.9)
    return (f'<defs>{_rg(u, "j", [(0, "#E8F28A"), (0.6, "#B8C832"), (1, "#6A7A10")])}</defs>'
            f'<ellipse cx="110" cy="128" rx="66" ry="104" fill="url(#{u}-j)"/>{bumps}<rect x="104" y="6" width="12" height="28" rx="6" fill="#5A3A1A"/>')


def raindrop_tear(u):
    return (f'<defs>{_rg(u, "r", [(0, "#E8F7FF"), (0.6, "#5FB8F0"), (1, "#1A6FB0")])}</defs>'
            f'<path d="M110,20 C150,90 176,130 176,160 C176,200 146,226 110,226 C74,226 44,200 44,160 C44,130 70,90 110,20 Z" fill="url(#{u}-r)"/>')


def raindrop_bun(u):
    return (f'<defs>{_rg(u, "r", [(0, "#E8F7FF"), (0.6, "#5FB8F0"), (1, "#1A6FB0")])}</defs>'
            f'<path d="M20,160 C20,90 70,64 110,64 C150,64 200,90 200,160 C170,150 50,150 20,160 Z" fill="url(#{u}-r)"/>')


def fig(u):
    return (f'<defs>{_rg(u, "f", [(0, "#B98AD8"), (0.6, "#6B2F8A"), (1, "#2E0F40")])}</defs>'
            f'<path d="M110,30 C130,30 136,60 150,80 C190,120 196,170 170,204 C150,228 70,228 50,204 C24,170 30,120 70,80 C84,60 90,30 110,30 Z" fill="url(#{u}-f)"/>'
            '<rect x="104" y="10" width="12" height="26" rx="6" fill="#5A7A2A"/>')


def fig_cut(u):
    flowers = "".join(f'<path d="M{110 + 70 * math.cos(math.radians(a)):.1f},{140 + 70 * math.sin(math.radians(a)):.1f} L{110 + 36 * math.cos(math.radians(a)):.1f},{140 + 36 * math.sin(math.radians(a)):.1f}" '
                      f'stroke="#FF6FA8" stroke-width="7" stroke-linecap="round"/>' for a in range(0, 360, 18))
    return ('<path d="M110,30 C130,30 136,60 150,80 C190,120 196,170 170,204 C150,228 70,228 50,204 C24,170 30,120 70,80 C84,60 90,30 110,30 Z" fill="#6B2F8A"/>'
            '<ellipse cx="110" cy="140" rx="86" ry="88" fill="#F2E2C2"/>' + flowers + '<ellipse cx="110" cy="140" rx="30" ry="34" fill="#F7EEDC"/>'
            '<circle cx="110" cy="52" r="6" fill="#2E0F40"/>')


def bee(u):      # faceless: body stripes and wings only
    return ('<ellipse cx="70" cy="80" rx="44" ry="26" fill="#E8F4FF" opacity="0.8" transform="rotate(-20,70,80)"/>'
            '<ellipse cx="140" cy="76" rx="44" ry="26" fill="#E8F4FF" opacity="0.8" transform="rotate(20,140,76)"/>'
            '<ellipse cx="110" cy="138" rx="76" ry="56" fill="#FFC21A"/>'
            '<path d="M78,92 C70,120 70,156 78,184 M110,84 C102,120 102,156 110,192 M142,92 C134,120 134,156 142,184" stroke="#2A2030" stroke-width="16" fill="none"/>'
            '<path d="M186,138 L210,138" stroke="#2A2030" stroke-width="8" stroke-linecap="round"/>')


def honeycomb(u):
    hexes = "".join(f'<path d="M{x},{y} l20,-12 l20,12 l0,24 l-20,12 l-20,-12 Z" fill="#FFC21A" stroke="#B87A00" stroke-width="4"/>'
                    for y in range(40, 220, 36) for x in range(20 + (20 if (y // 36) % 2 else 0), 190, 40))
    return hexes


def cashew_apple(u):
    return (f'<defs>{_rg(u, "c", [(0, "#FFE08A"), (0.5, "#FF8A2A"), (1, "#C0301A")])}</defs>'
            '<rect x="104" y="6" width="12" height="30" rx="6" fill="#5A7A2A"/>'
            f'<path d="M70,34 C110,24 150,34 156,70 C164,120 150,160 128,168 C116,172 104,172 92,168 C70,160 56,120 64,70 C66,50 66,40 70,34 Z" fill="url(#{u}-c)"/>'
            '<path d="M86,170 C70,186 74,222 104,226 C132,230 146,204 132,188 C124,180 116,186 110,180 C104,174 98,166 86,170 Z" fill="#8A9A5A" stroke="#5A6A2A" stroke-width="4"/>')


def onion(u):
    return (f'<defs>{_rg(u, "o", [(0, "#F2C8E8"), (0.6, "#B04A92"), (1, "#5A1A46")])}</defs>'
            f'<path d="M110,30 C120,60 190,100 190,160 C190,206 154,228 110,228 C66,228 30,206 30,160 C30,100 100,60 110,30 Z" fill="url(#{u}-o)"/>'
            '<path d="M110,30 C108,20 112,10 110,4" stroke="#7FB04A" stroke-width="6" fill="none"/>'
            '<path d="M110,60 C90,100 76,150 90,220 M110,60 C130,100 144,150 130,220" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="4" fill="none"/>')


def onion_half(u):
    rings = "".join(f'<path d="M{110 - r},{150} C{110 - r},{150 - r * 1.2:.0f} {110 + r},{150 - r * 1.2:.0f} {110 + r},{150}" stroke="#E8B8DA" stroke-width="7" fill="none"/>'
                    for r in (24, 44, 64, 84))
    return f'<path d="M20,150 C20,70 200,70 200,150 Z" fill="#FBEFF7" stroke="#B04A92" stroke-width="6"/>{rings}'


def tearcloud(u):
    return ('<circle cx="70" cy="120" r="40" fill="#E8F7FF" opacity="0.8"/><circle cx="120" cy="96" r="48" fill="#E8F7FF" opacity="0.8"/>'
            '<circle cx="160" cy="130" r="36" fill="#E8F7FF" opacity="0.8"/><path d="M110,150 C120,170 126,184 110,196 C94,184 100,170 110,150 Z" fill="#5FB8F0"/>')


def rafflesia(u):
    petals = "".join(f'<ellipse cx="{110 + 62 * math.cos(math.radians(a)):.1f}" cy="{124 + 62 * math.sin(math.radians(a)):.1f}" rx="50" ry="40" '
                     f'transform="rotate({a},{110 + 62 * math.cos(math.radians(a)):.1f},{124 + 62 * math.sin(math.radians(a)):.1f})" fill="#C0301A" stroke="#7A1508" stroke-width="4"/>'
                     for a in range(-90, 270, 72))
    spots = "".join(f'<circle cx="{110 + d * math.cos(math.radians(a)):.1f}" cy="{124 + d * math.sin(math.radians(a)):.1f}" r="6" fill="#FFE2C8"/>'
                    for a in range(-90, 270, 24) for d in (60, 84))
    return f'{petals}{spots}<circle cx="110" cy="124" r="40" fill="#7A1508"/><circle cx="110" cy="124" r="28" fill="#2A0A06"/>'


def panda(u):     # seen from behind: round black-and-white body, no face
    return ('<ellipse cx="110" cy="160" rx="78" ry="70" fill="#F7F7F2"/><circle cx="110" cy="80" r="52" fill="#F7F7F2"/>'
            '<circle cx="70" cy="40" r="20" fill="#1A1A1E"/><circle cx="150" cy="40" r="20" fill="#1A1A1E"/>'
            '<path d="M36,130 C40,110 70,104 90,112 C70,130 60,150 56,176 C44,170 34,150 36,130 Z" fill="#1A1A1E"/>'
            '<path d="M184,130 C180,110 150,104 130,112 C150,130 160,150 164,176 C176,170 186,150 184,130 Z" fill="#1A1A1E"/>'
            '<ellipse cx="72" cy="222" rx="30" ry="16" fill="#1A1A1E"/><ellipse cx="148" cy="222" rx="30" ry="16" fill="#1A1A1E"/>')


def bamboo(u):
    stalk = "".join(f'<rect x="{x}" y="20" width="26" height="210" rx="10" fill="#7FB04A" stroke="#4E8A2A" stroke-width="4"/>'
                    + "".join(f'<rect x="{x - 2}" y="{y}" width="30" height="8" rx="4" fill="#4E8A2A"/>' for y in (70, 130, 190)) for x in (60, 100, 140))
    return stalk + '<path d="M126,70 C150,50 176,52 190,60 C170,72 146,76 126,70 Z" fill="#3FAF3A"/><path d="M86,130 C60,110 36,114 26,122 C46,134 70,136 86,130 Z" fill="#3FAF3A"/>'


def pot(u):
    return ('<path d="M30,96 L190,96 L176,214 C174,224 166,230 156,230 L64,230 C54,230 46,224 44,214 Z" fill="#9AA3B2" stroke="#5A6272" stroke-width="5"/>'
            '<rect x="20" y="84" width="180" height="18" rx="9" fill="#C9CFD9" stroke="#5A6272" stroke-width="4"/>'
            '<rect x="2" y="110" width="30" height="12" rx="6" fill="#5A6272"/><rect x="188" y="110" width="30" height="12" rx="6" fill="#5A6272"/>'
            + "".join(f'<path d="M{70 + 40 * k},70 C{60 + 40 * k},50 {84 + 40 * k},40 {74 + 40 * k},16" stroke="#E8F7FF" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.7"/>' for k in range(3)))


def mountain(u):
    return (f'<defs>{_lg(u, "m", [(0, "#B9A2D8"), (1, "#4B2A70")])}</defs>'
            f'<path d="M0,230 L110,24 L220,230 Z" fill="url(#{u}-m)"/><path d="M110,24 L84,74 L100,66 L110,84 L122,64 L136,74 Z" fill="#FFFFFF"/>'
            '<path d="M0,230 L60,130 L120,230 Z" fill="#3A1F5A"/>')


def thermometer(u):
    return ('<rect x="92" y="20" width="36" height="170" rx="18" fill="#F2F2F2" stroke="#9AA3B2" stroke-width="5"/>'
            '<rect x="102" y="80" width="16" height="120" rx="8" fill="#FF4D4D" class="zmerc"/><circle cx="110" cy="200" r="28" fill="#FF4D4D" stroke="#9AA3B2" stroke-width="5"/>'
            + "".join(f'<rect x="132" y="{40 + 20 * k}" width="18" height="5" fill="#9AA3B2"/>' for k in range(7)))


def choco_white(u, dark: bool = False):
    base, edge = ("#6B3A1E", "#3E1E0C") if dark else ("#FFF4DC", "#D9C49A")
    cells = "".join(f'<rect x="{40 + 48 * (k % 3)}" y="{40 + 48 * (k // 3)}" width="40" height="40" rx="6" fill="{base}" stroke="{edge}" stroke-width="4"/>' for k in range(12))
    return f'<rect x="30" y="30" width="160" height="208" rx="12" fill="{edge}"/>{cells}'


def choco_dark(u):
    return choco_white(u, dark=True)


def cocoa_butter(u):
    return ('<path d="M40,120 L180,120 L170,200 C168,214 156,222 142,222 L78,222 C64,222 52,214 50,200 Z" fill="#FFF0C8" stroke="#D9B66A" stroke-width="5"/>'
            '<ellipse cx="110" cy="120" rx="70" ry="18" fill="#FFF7DE" stroke="#D9B66A" stroke-width="5"/>'
            '<path d="M150,40 C176,40 190,70 176,92 C166,108 134,108 124,92 C110,70 124,40 150,40 Z" fill="#8A4A22"/>')


def redwood(u):
    return (f'<defs>{_lg(u, "t", [(0, "#B0502A"), (1, "#6A2A10")], 1, 0)}</defs>'
            f'<path d="M100,240 L104,40 L116,40 L120,240 Z" fill="url(#{u}-t)"/>'
            + "".join(f'<path d="M110,{y} L{110 - w},{y + 40} L{110 + w},{y + 40} Z" fill="#2E7D3A"/>' for y, w in [(6, 22), (40, 34), (80, 44), (124, 52)]))


def sunflower(u):     # flower head only, no face
    petals = "".join(f'<ellipse cx="{110 + 66 * math.cos(math.radians(a)):.1f}" cy="{100 + 66 * math.sin(math.radians(a)):.1f}" rx="28" ry="12" '
                     f'transform="rotate({a},{110 + 66 * math.cos(math.radians(a)):.1f},{100 + 66 * math.sin(math.radians(a)):.1f})" fill="#FFC21A" stroke="#E08A00" stroke-width="3"/>'
                     for a in range(0, 360, 24))
    seeds = "".join(f'<circle cx="{110 + d * math.cos(math.radians(a)):.1f}" cy="{100 + d * math.sin(math.radians(a)):.1f}" r="3.5" fill="#2A1A0A"/>'
                    for a in range(0, 360, 30) for d in (14, 28))
    return ('<path d="M110,150 C112,190 108,220 110,240" stroke="#3FAF3A" stroke-width="12" fill="none"/>'
            '<path d="M110,200 C80,180 60,190 54,200 C74,214 96,212 110,200 Z" fill="#3FAF3A"/>'
            f'{petals}<circle cx="110" cy="100" r="44" fill="#5A3A1A"/>{seeds}')


def cloud_bolt(u):
    return ('<circle cx="70" cy="90" r="44" fill="#5A5470"/><circle cx="124" cy="70" r="54" fill="#6A6480"/><circle cx="168" cy="98" r="40" fill="#5A5470"/>'
            '<rect x="40" y="90" width="150" height="46" rx="23" fill="#5A5470"/>'
            '<path d="M120,130 L92,190 L116,190 L100,238 L150,168 L124,168 L142,130 Z" fill="#FFE04D" stroke="#FFB800" stroke-width="4" stroke-linejoin="round"/>')


def house(u):
    return ('<path d="M30,110 L110,40 L190,110 Z" fill="#B04A92"/><rect x="46" y="108" width="128" height="122" fill="#FFF2C7"/>'
            '<rect x="94" y="160" width="34" height="70" rx="4" fill="#6B4220"/><rect x="60" y="130" width="28" height="28" fill="#5FB8F0" stroke="#6B4220" stroke-width="4"/>'
            '<rect x="134" y="130" width="28" height="28" fill="#5FB8F0" stroke="#6B4220" stroke-width="4"/>')


def stopwatch(u):
    return ('<circle cx="110" cy="134" r="88" fill="#FFF4FA" stroke="#2A2230" stroke-width="10"/><rect x="96" y="18" width="28" height="30" rx="6" fill="#2A2230"/>'
            '<path d="M110,134 L110,72" stroke="#FF43C0" stroke-width="9" stroke-linecap="round" class="zhand"/><circle cx="110" cy="134" r="10" fill="#2A2230"/>'
            + "".join(f'<rect x="107" y="52" width="6" height="14" fill="#2A2230" transform="rotate({a},110,134)"/>' for a in range(0, 360, 30)))


def lightwave(u, color: str = "#4D7CFF", n: int = 6):
    pts = " ".join(f"{10 + x * 2},{120 + 70 * math.sin(x * 2 * math.pi * n / 100):.1f}" for x in range(101))
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'


def wave_blue(u):
    return lightwave(u, "#4D7CFF", 7)


def wave_red(u):
    return lightwave(u, "#FF4D4D", 2)


def sky_blue(u):
    return (f'<defs>{_lg(u, "k", [(0, "#1F5FD8"), (1, "#8FD3FF")])}</defs><rect x="10" y="10" width="200" height="220" rx="30" fill="url(#{u}-k)"/>'
            '<circle cx="160" cy="62" r="24" fill="#FFE04D"/>'
            + "".join(f'<circle cx="{40 + 30 * k}" cy="{150 + (k % 2) * 30}" r="5" fill="#ffffff" opacity="0.7"/>' for k in range(6)))


def paint_roller(u):
    return ('<rect x="30" y="40" width="160" height="56" rx="20" fill="#FFD84D" stroke="#B88A00" stroke-width="5"/>'
            '<path d="M110,96 L110,130 L60,130 L60,150" stroke="#9AA3B2" stroke-width="10" fill="none"/>'
            '<rect x="48" y="150" width="24" height="84" rx="10" fill="#B04A92"/>')


def ruler(u):
    return ('<rect x="80" y="4" width="60" height="232" rx="8" fill="#FFD84D" stroke="#B88A00" stroke-width="4"/>'
            + "".join(f'<rect x="80" y="{14 + 18 * k}" width="{26 if k % 5 == 0 else 14}" height="4" fill="#5A3A00"/>' for k in range(12)))


PROPS = {
    "sun": sun, "pineapple": pineapple, "fruitlet": fruitlet, "apple": apple, "apple_slice": apple_slice, "apple_brown": apple_brown,
    "starfish": starfish, "fish": fish, "helmet": helmet, "speaker": speaker, "soundwave": soundwave, "flytrap": flytrap, "fly": fly,
    "icecube": icecube, "glass": glass, "sloth": sloth, "hair_algae": hair_algae, "jackfruit": jackfruit, "raindrop_tear": raindrop_tear,
    "raindrop_bun": raindrop_bun, "fig": fig, "fig_cut": fig_cut, "bee": bee, "honeycomb": honeycomb, "cashew_apple": cashew_apple,
    "onion": onion, "onion_half": onion_half, "tearcloud": tearcloud, "rafflesia": rafflesia, "panda": panda, "bamboo": bamboo,
    "pot": pot, "mountain": mountain, "thermometer": thermometer, "choco_white": choco_white, "choco_dark": choco_dark,
    "cocoa_butter": cocoa_butter, "redwood": redwood, "sunflower": sunflower, "cloud_bolt": cloud_bolt, "house": house,
    "stopwatch": stopwatch, "wave_blue": wave_blue, "wave_red": wave_red, "sky_blue": sky_blue, "paint_roller": paint_roller,
    "ruler": ruler,
}
