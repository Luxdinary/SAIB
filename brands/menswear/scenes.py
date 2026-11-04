"""Suitwerk scene types (brand scene module brands/menswear/scenes.py, see fn.render.brand_scenes).

Five brand types with the Suitwerk prefix, one per shared direction scene type; the shared types stay untouched.
One jacket (line illustration from `tools/garment.py`) is the running object of every scene; text sits beside
or above it, never on a slide.

| scene type        | Suitwerk layout (shared counterpart)                                             |
|-------------------|----------------------------------------------------------------------------------|
| suitwerk_hook     | big question, jacket draws itself, detail loupe on the button + "?"              |
| suitwerk_fitting  | fitting: a pin travels to the detail, zoom, the state changes (e.g. button closes) |
| suitwerk_ladder   | rule ladder: jacket left, one tag per button on the right, optional second stage  |
| suitwerk_compare  | two jackets side by side with title, tag and shape arrows (waist, hips)           |
| suitwerk_takeaway | cards with a mini jacket each; `mode: closing` = the jacket is put right, statement |

Text limits are reported as "<type>.<field>: N chars > L" (the report treats them as readability failures).

Explainer layer (Schnitt- und Layout-Vorlage, 30.10.2026): every time field (`*_at`, `at`) takes seconds from the
beat start or a word anchor "w:Wort[#n]" (start of that spoken word in the beat, like fn.render.explainer).
Scene content stays above y 1100 (marker and source bar from `explainer.source_y`) and left of x 930.
`hold_end: true` keeps the scene up to its end (the next beat comes in with an iris or a blende);
`backdrop: true` puts the atelier ground under a scene that comes in with a transition, faded out afterwards.
Colours with a fixed meaning come from `explainer.colors` in brand.yaml (amber = open, red = risk, green = reached).

Qualitaetsrunde Q1 (31.10.2026, Briefing OneDrive `02 Marke\\Qualitaetsrunde 2026-10-31.md`): LAYER draws the atelier
ground under all scenes (light pool, woven texture, tailor's pattern pieces and a tape measure in slow parallax,
vignette; code only), jackets are larger and lit from the top left, a detail loupe magnifies the button, and every
scene has a slow push-in plus several events on spoken words. The status bar gets the tone `green` (reached state).
"""
from __future__ import annotations

import html
import math
import re
import sys
from pathlib import Path

import yaml

from fn.render.templates import SceneCtx, SceneOut

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import garment as G  # noqa: E402
import objects as O  # noqa: E402

W = 1080
X_RIGHT = 930                         # platform icons from here
_XC = ((yaml.safe_load((Path(__file__).resolve().parent / "brand.yaml").read_text(encoding="utf-8")) or {})
       .get("explainer") or {}).get("colors") or {}
AMBER, GREEN = _XC.get("unsicher", "#E8A33D"), _XC.get("erreicht", "#8DBE96")
LIMITS = {
    "cinematic_hook": {"question": 56, "badge": 14},
    "ui_demo": {"headline": 44, "label": 30},
    "data_flow": {"headline": 44, "tag": 18, "stage_title": 18},
    "comparison": {"headline": 44, "title": 18, "tag": 26, "tag2": 34},
    "key_takeaway": {"headline": 44, "item_title": 26, "item_sub": 40, "statement": 40, "chip": 40},
}
_TOTAL = {"t": 80.0}                  # video length, set by LAYER (called before the scenes) for the backdrops


def _e(s) -> str:
    return html.escape(str(s))


def _limit(kind: str, key: str, val: str, where: str, out: list[str]) -> None:
    lim = LIMITS[kind].get(key)
    if lim and len(str(val)) > lim:
        out.append(f"{kind}.{where}: {len(str(val))} chars > {lim}")


def _rel(c: SceneCtx, value, default: float) -> float:
    """Seconds from the beat start: a number, or "w:Wort[#n]" = start of that spoken word in this beat."""
    if value is None or value == "":
        return float(default)
    if isinstance(value, (int, float)):
        return float(value)
    m = re.fullmatch(r"w:(.+?)(?:#(\d+))?", str(value).strip())
    if not m:
        raise ValueError(f"{c.sid}: time {value!r} is neither seconds nor 'w:Wort'")
    stem, nth = m.group(1).lower(), int(m.group(2) or 1)
    hits = [w for w in c.words if re.sub(r"[^\wäöüß]", "", w.text.lower()).startswith(stem)]
    if len(hits) < nth:
        raise ValueError(f"{c.sid}: anchor word {value!r} not spoken in this beat")
    return hits[nth - 1].start - c.start


def _spec(d: dict, fastened_key: str = "fastened", default_fast=None, **over) -> dict:
    """Object spec of a scene, a side, a stage or a card: `object` (see tools/objects.py) or the jacket from
    `variant` / `fastened` (Q1 plans)."""
    if d.get("object"):
        base = dict(d["object"])
    else:
        base = {"kind": "jacket", "variant": d.get("variant", "sb2")}
    if fastened_key in d:
        base["fastened"] = d[fastened_key]
    elif "fastened" not in base and default_fast is not None:
        base["fastened"] = default_fast
    if "strain" in d and "strain" not in over:
        base["strain"] = bool(d["strain"])
    base.update(over)
    return base


# --- atelier ground (LAYER and backdrops) -----------------------------------------------------------

_NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
          "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/>"
          "<feColorMatrix values='0 0 0 0 0.85 0 0 0 0 0.75 0 0 0 0 0.6 0 0 0 0.07 0'/></filter>"
          "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")


def _drift(t: float | None) -> dict:
    """Position of the slow layers at video time t (None = tweened by the timeline, start values)."""
    p = 0.0 if t is None else max(0.0, min(1.0, t / _TOTAL["t"]))
    q = -(math.cos(math.pi * p) - 1) / 2          # GSAP sine.inOut
    return {"draft": (-24 + 48 * p, -36 + 72 * p), "light": (-70 + 140 * q, -20 + 50 * q), "weave": (-14 * p, -28 * p)}


def _draft_svg(acc: str) -> str:
    """Tailor's pattern paper: grid, a front panel and a sleeve as pattern pieces, grain lines, chalk marks, tape."""
    body = G._left_body("sb2", [0])
    sleeve = "M116,96 C96,120 88,160 86,220 C82,350 76,480 72,612 L150,624 C154,500 156,380 160,280 C150,200 132,140 116,96 Z"
    ticks = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{22 if x % 60 == 0 else 11}"/>' for x in range(0, 1500, 12))
    chalk = "".join(f'<path d="M{x - 9},{y - 9} L{x + 9},{y + 9} M{x + 9},{y - 9} L{x - 9},{y + 9}"/>'
                    for x, y in ((220, 1180), (980, 520), (1080, 1300), (300, 1720), (760, 260)))
    return f"""<svg viewBox="0 0 1240 2080" width="1240" height="2080" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;overflow:visible">
<defs><pattern id="swa-grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0 L0 0 0 80" fill="none" stroke="{acc}" stroke-opacity="0.045" stroke-width="1"/>
<path d="M-4 0 L4 0 M0 -4 L0 4" stroke="{acc}" stroke-opacity="0.12" stroke-width="1"/></pattern></defs>
<rect width="1240" height="2080" fill="url(#swa-grid)"/>
<g fill="none" stroke="{acc}" stroke-linejoin="round" stroke-linecap="round">
 <g transform="translate(-150,330) rotate(-8 300 400) scale(2.05)" stroke-opacity="0.15">
  <path d="{body}" stroke-width="0.9"/>
  <path d="{body}" stroke-width="0.6" stroke-dasharray="5 6" transform="translate(-14,-12) scale(1.045)"/>
  <path d="M206,250 L206,610 M200,262 L206,250 L212,262 M200,598 L206,610 L212,598" stroke-width="0.8"/>
  <path d="M120,470 L300,470" stroke-width="0.6" stroke-dasharray="2 5"/>
 </g>
 <g transform="translate(860,1160) rotate(14 120 360) scale(2.3)" stroke-opacity="0.13">
  <path d="{sleeve}" stroke-width="0.9"/>
  <path d="{sleeve}" stroke-width="0.6" stroke-dasharray="5 6" transform="translate(-6,-8) scale(1.06)"/>
  <path d="M118,200 L112,520 M112,212 L118,200 L124,212 M106,508 L112,520 L118,508" stroke-width="0.8"/>
 </g>
 <g stroke-opacity="0.14" stroke-width="2">{chalk}</g>
 <path d="M60,940 C300,900 620,980 1200,880" stroke-opacity="0.10" stroke-width="1.4" stroke-dasharray="3 9"/>
 <g transform="translate(-60,1850) rotate(-7)">
  <rect x="0" y="0" width="1500" height="56" fill="{acc}" fill-opacity="0.07" stroke-opacity="0.22" stroke-width="1.5"/>
  <g stroke-opacity="0.30" stroke-width="1.6">{ticks}</g>
 </g>
</g></svg>"""


def _atelier_html(pal: dict, t: float | None, cls: str) -> str:
    """The ground. t=None: the LAYER under all scenes (moved by the timeline); t=seconds: a static copy at that
    time for a scene that comes in with a transition (so the backdrop matches the layer when it fades)."""
    acc = pal["accent"]
    d = _drift(t)

    def tr(k: str) -> str:
        return "" if t is None else f"transform:translate({d[k][0]:.1f}px,{d[k][1]:.1f}px);"
    return (f'<div class="{cls}" style="position:absolute;inset:0;overflow:hidden;pointer-events:none;">'
            f'<div class="swa swa-base"></div>'
            f'<div class="swa swa-draft" style="{tr("draft")}">{_draft_svg(acc)}</div>'
            f'<div class="swa swa-weave" style="{tr("weave")}"></div>'
            f'<div class="swa swa-beamwrap"><div class="swa swa-beam"></div></div>'
            f'<div class="swa swa-light" style="{tr("light")}"></div>'
            f'<div class="swa swa-vig"></div></div>')


def _atelier_css(pal: dict) -> str:
    acc, bg = pal["accent"], pal["bg"]
    return f"""
#sw-atelier{{position:absolute;inset:0;z-index:0;}}
.swa{{position:absolute;pointer-events:none;}}
.swa-base{{inset:0;background:radial-gradient(ellipse 90% 58% at 50% 40%,#2c3d5c 0%,#1d2b44 36%,{bg} 62%,#0c1322 100%);}}
.swa-draft{{left:-80px;top:-80px;width:1240px;height:2080px;}}
.swa-weave{{inset:-60px;background-image:repeating-linear-gradient(45deg,color-mix(in srgb,{acc} 5%,transparent) 0 1px,transparent 1px 7px),repeating-linear-gradient(-45deg,rgba(0,0,0,0.10) 0 1px,transparent 1px 9px),{_NOISE};}}
.swa-beamwrap{{inset:0;filter:blur(22px);}}
.swa-beam{{left:0;top:0;width:{W}px;height:1500px;clip-path:polygon(41% 0,59% 0,92% 100%,8% 100%);background:linear-gradient(to bottom,rgba(242,232,210,0.10) 0%,rgba(242,232,210,0.035) 55%,transparent 92%);}}
.swa-light{{left:-200px;top:-260px;width:1480px;height:1700px;background:radial-gradient(ellipse 46% 40% at 50% 50%,rgba(240,222,186,0.15) 0%,rgba(212,180,131,0.06) 42%,transparent 72%);}}
.swa-vig{{inset:0;background:radial-gradient(ellipse 78% 62% at 50% 42%,transparent 52%,rgba(4,8,15,0.62) 100%);}}
.st-green{{color:{GREEN};}}
"""


def LAYER(plan, brand, project_dir, captions):  # noqa: N802 (contract name)
    """Atelier ground under all scenes, slow parallax (pattern paper, light, weave) over the whole video."""
    last = max((g.end for g in captions), default=60.0)
    tail = float((plan.layout or {}).get("tail_seconds", 2.6))
    _TOTAL["t"] = round(last + tail + 0.4, 2)
    tot = _TOTAL["t"]
    pal = brand.palette
    script = f"""<script>(function(){{var T=(window.__timelines||{{}}).main;if(!T)return;
T.fromTo("#sw-atelier .swa-draft",{{x:-24,y:-36}},{{x:24,y:36,duration:{tot},ease:"none"}},0);
T.fromTo("#sw-atelier .swa-light",{{x:-70,y:-20}},{{x:70,y:30,duration:{tot},ease:"sine.inOut"}},0);
T.fromTo("#sw-atelier .swa-weave",{{x:0,y:0}},{{x:-14,y:-28,duration:{tot},ease:"none"}},0);
T.seek(0);}})();</script>"""
    return {"head_html": f"<style>{_atelier_css(pal)}</style>",
            "under_scenes_html": _atelier_html(pal, None, "").replace('<div class=""', '<div id="sw-atelier"', 1),
            "body_end_html": script}


def _backdrop(c: SceneCtx, d: dict) -> str:
    if not d.get("backdrop"):
        return ""
    return _atelier_html(c.pal, c.start, "sw-bd")


# --- shared pieces ---------------------------------------------------------------------------------

def _css(c: SceneCtx) -> str:
    p = c.pal
    acc, text, surf, muted = p["accent"], p["text"], p["surface"], p["muted"]
    red = p.get("signal_red", "#C9776B")
    s = c.sid
    disp, body = c.display_font, c.body_font
    return f"""<style>
#{s} .sw{{position:absolute;inset:0;}}
#{s} .sw-st{{position:absolute;inset:0;transform-origin:520px 700px;}}
#{s} .sw-h{{position:absolute;left:108px;width:822px;top:{c.zone_top + 2}px;text-align:center;font-family:'FN {disp}';font-weight:600;font-size:68px;line-height:1.08;color:{text};letter-spacing:-0.01em;}}
#{s} .sw-q{{position:absolute;left:108px;width:822px;top:{c.zone_top}px;text-align:center;font-family:'FN {disp}';font-weight:600;font-size:72px;line-height:1.06;color:{text};}}
#{s} .sw-jk{{position:absolute;transform-origin:50% 50%;filter:drop-shadow(0 28px 34px rgba(3,7,14,0.55));}}
#{s} .sw-jk .jacket{{width:100%;height:100%;display:block;overflow:visible;}}
#{s} .ln,#{s} .lnm{{fill:none;stroke:{acc};stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .lnm{{stroke-width:4;}}
#{s} .seam{{stroke-opacity:0.45;stroke-width:1.6;}}
#{s} .thin{{stroke-width:1.6;}}
#{s} .fold{{stroke-width:3.6;stroke-linecap:round;}} #{s} .vent{{stroke-width:2.2;}} #{s} .measure{{stroke-opacity:0.7;}}
#{s} .btn{{fill:{p['bg']};stroke:{acc};stroke-width:2.6;}}
#{s} .hole{{stroke:{acc};stroke-width:2.6;}}
#{s} .strain{{fill:none;stroke:{red};stroke-width:3.4;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .ring{{fill:none;stroke:{text};stroke-width:2.6;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .sw-over{{position:absolute;left:0;top:0;width:{W}px;height:1920px;overflow:visible;}}
#{s} .sw-jo{{position:absolute;overflow:visible;}}
#{s} .sw-lead{{fill:none;stroke:{acc};stroke-width:2;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .sw-dot{{fill:{acc};}}
#{s} .cut{{fill:none;stroke:{acc};stroke-width:6;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .ghost{{fill:none;stroke:{acc};stroke-width:4;stroke-linecap:round;stroke-dasharray:0.025 0.02;opacity:0;}}
#{s} .arw{{fill:none;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 1;stroke-dashoffset:0;}}
#{s} .arw.gold{{stroke:{acc};}} #{s} .arw.red{{stroke:{red};}}
#{s} .pulse{{fill:none;stroke:{acc};stroke-width:3;opacity:0;}}
#{s} .pulse.red{{stroke:{red};}} #{s} .pulse.amber{{stroke:{AMBER};}}
#{s} .sw-tag{{position:absolute;font-family:'FN {body}';font-weight:600;font-size:38px;line-height:1.1;color:{text};white-space:nowrap;transform-origin:0 50%;}}
#{s} .sw-tag small{{display:block;font-weight:400;font-size:28px;color:{muted};margin-top:6px;letter-spacing:0.02em;}}
#{s} .sw-tag small i{{font-family:'FN {disp}';font-style:italic;font-weight:600;font-size:30px;}}
#{s} .tone-always{{color:{acc};}} #{s} .tone-never{{color:{red};}} #{s} .tone-sometimes{{color:{AMBER};}}
#{s} .sw-stage{{position:absolute;left:600px;font-family:'FN {disp}';font-weight:600;font-size:46px;color:{text};white-space:nowrap;}}
#{s} .sw-stage::after{{content:"";display:block;width:70px;height:2px;background:{acc};margin-top:12px;}}
#{s} .ok .ring{{stroke:{GREEN};stroke-width:3.4;}}
#{s} .sw-card{{position:absolute;background:color-mix(in srgb,{surf} 94%,transparent);border:1.5px solid color-mix(in srgb,{acc} 50%,transparent);border-radius:16px;padding:20px 30px;font-family:'FN {body}';font-size:38px;font-weight:500;color:{text};text-align:center;box-shadow:0 1px 2px rgba(0,0,0,0.3),0 22px 46px rgba(0,0,0,0.45);}}
#{s} .sw-badge{{position:absolute;width:84px;height:84px;border-radius:50%;border:2.5px solid {acc};background:{p['bg']};color:{acc};font-family:'FN {disp}';font-weight:600;font-size:58px;line-height:78px;text-align:center;box-shadow:0 10px 26px rgba(0,0,0,0.45);}}
#{s} .sw-loupe{{position:absolute;border-radius:50%;overflow:hidden;background:{p['bg']};border:3px solid {acc};box-shadow:0 0 0 10px color-mix(in srgb,{acc} 10%,transparent),0 26px 60px rgba(0,0,0,0.6);}}
#{s} .sw-loupe .ln{{stroke-width:1.3;}} #{s} .sw-loupe .btn,#{s} .sw-loupe .hole{{stroke-width:1.4;}} #{s} .sw-loupe .ring{{stroke-width:1.4;}}
#{s} .sw-loupe .strain{{stroke-width:1.8;}}
#{s} .sw-loupe .glass{{position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 34% 28%,rgba(255,255,255,0.16) 0%,transparent 42%),radial-gradient(circle at 50% 50%,transparent 62%,rgba(0,0,0,0.38) 100%);}}
#{s} .sw-ctitle{{position:absolute;text-align:center;font-family:'FN {disp}';font-weight:600;font-size:50px;color:{text};}}
#{s} .sw-ctag{{position:absolute;text-align:center;font-family:'FN {body}';font-size:31px;font-weight:500;line-height:1.2;color:{muted};}}
#{s} .sw-ctag.amber{{color:{AMBER};font-size:29px;}}
#{s} .sw-ctag b{{color:{acc};font-weight:600;}}
#{s} .sw-pin{{position:absolute;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;border:3px solid {text};box-shadow:0 6px 16px rgba(0,0,0,0.5);}}
#{s} .sw-pin::after{{content:"";position:absolute;left:16px;top:16px;width:6px;height:6px;border-radius:50%;background:{text};}}
#{s} .sw-kc{{position:absolute;left:108px;width:822px;box-sizing:border-box;height:218px;display:flex;align-items:center;gap:30px;background:color-mix(in srgb,{surf} 82%,transparent);border:1.5px solid color-mix(in srgb,{acc} 22%,transparent);border-radius:18px;padding:0 30px 0 22px;box-shadow:0 18px 40px rgba(0,0,0,0.38);}}
#{s} .kc-on{{position:absolute;inset:-1.5px;border-radius:18px;border:2.5px solid color-mix(in srgb,{acc} 80%,transparent);opacity:0;pointer-events:none;}}
#{s} .sw-kc .sw-mini{{position:relative;width:160px;height:208px;flex:0 0 160px;}}
#{s} .sw-kc .sw-mini .jacket{{position:absolute;left:0;top:0;width:160px;height:208px;overflow:visible;}}
#{s} .sw-kn{{position:absolute;right:26px;top:20px;font-family:'FN {disp}';font-weight:600;font-size:34px;color:{acc};opacity:0.8;}}
#{s} .sw-kt{{font-family:'FN {disp}';font-weight:600;font-size:48px;line-height:1.1;color:{text};text-align:left;}}
#{s} .sw-ks{{font-family:'FN {body}';font-size:32px;line-height:1.25;color:{muted};margin-top:10px;text-align:left;}}
#{s} .sw-stmt{{position:absolute;left:108px;width:822px;text-align:center;font-family:'FN {disp}';font-weight:600;font-size:74px;line-height:1.08;color:{text};}}
#{s} .sw-chip{{position:absolute;left:108px;width:822px;text-align:center;font-family:'FN {body}';font-size:34px;letter-spacing:0.08em;color:{acc};}}
</style>"""


def _place(cx: float, top: float, width: float) -> dict:
    s = width / G.VW
    return {"left": cx - width / 2, "top": top, "w": width, "h": G.VH * s, "s": s, "cx": cx}


def _place_collar(cx: float, collar_y: float, width: float) -> dict:
    """Box whose drawn collar (viewBox y 44) sits at collar_y."""
    s = width / G.VW
    return _place(cx, collar_y - 44 * s, width)


def _px(box: dict, pt: tuple[float, float]) -> tuple[float, float]:
    return box["left"] + pt[0] * box["s"], box["top"] + pt[1] * box["s"]


def _jk(sid: str, cls: str, box: dict, svg: str, extra_style: str = "") -> str:
    return (f'<div class="sw-jk {cls}" style="left:{box["left"]:.1f}px;top:{box["top"]:.1f}px;width:{box["w"]:.1f}px;'
            f'height:{box["h"]:.1f}px;{extra_style}">{svg}</div>')


def _jo(cls: str, box: dict, inner: str) -> str:
    """Overlay in the jacket's own coordinates (viewBox 600 x 780) on top of a jacket box."""
    return (f'<svg class="sw-jo {cls}" style="left:{box["left"]:.1f}px;top:{box["top"]:.1f}px;width:{box["w"]:.1f}px;'
            f'height:{box["h"]:.1f}px" viewBox="0 0 {G.VW} {G.VH}">{inner}</svg>')


def _arrow(cls: str, x: float, y: float, dx: float) -> str:
    """Short arrow from (x, y) by dx (jacket coordinates), head at the end."""
    e = x + dx
    h = 13 if dx > 0 else -13
    return f'<path class="arw {cls}" pathLength="1" d="M{x:.0f},{y:.0f} L{e:.0f},{y:.0f} M{e - h:.0f},{y - 12:.0f} L{e:.0f},{y:.0f} L{e - h:.0f},{y + 12:.0f}"/>'


def _pulse(cls: str, x: float, y: float, r: float = 30) -> str:
    return f'<circle class="pulse {cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.0f}"/>'


def _tl_pulse(sel: str, at: float) -> list[str]:
    return [f'tl.fromTo("{sel}",{{opacity:0,scale:0.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{at:.3f});']


def _loupe(uid: str, spec: dict, target: str, cx: float, cy: float, r: float, mag: float, accent: str, *, cls: str = "") -> str:
    """A round magnifier: the same object drawn `mag` px per unit, the target detail in the middle of the glass."""
    tx, ty = O.spot(spec, target)
    left, top = r - tx * mag, r - ty * mag
    svg = O.draw(uid, spec, accent, ring=[target])
    return (f'<div class="sw-loupe {cls}" style="left:{cx - r:.0f}px;top:{cy - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px">'
            f'<div class="sw-li" style="position:absolute;left:{left:.1f}px;top:{top:.1f}px;width:{G.VW * mag:.1f}px;height:{G.VH * mag:.1f}px">{svg}</div>'
            f'<div class="glass"></div></div>')


def _draw_in(sel: str, at: float, dur: float = 1.6) -> list[str]:
    return [f'tl.fromTo("{sel} .ln",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur:.2f},ease:"power1.inOut",stagger:0.025}},{at:.3f});',
            f'tl.fromTo("{sel} .fill",{{opacity:0}},{{opacity:1,duration:0.7,ease:"power1.out"}},{at + dur * 0.55:.3f});',
            f'tl.fromTo("{sel} .btns",{{opacity:0}},{{opacity:1,duration:0.4}},{at + dur * 0.8:.3f});']


def _enter_exit(c: SceneCtx, d: dict | None = None) -> list[str]:
    s, d = c.sid, d or {}
    out = []
    if d.get("backdrop"):      # the transition (iris/blende) brings the scene in; the ground goes once it is complete
        out.append(f'tl.to("#{s} .sw-bd",{{opacity:0,duration:0.3}},{c.start + float(d.get("backdrop_seconds", 0.7)):.3f});')
    else:
        out.append(f'tl.fromTo("#{s} .sw",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power1.out"}},{c.start:.3f});')
    if not d.get("hold_end"):
        out.append(f'tl.to("#{s} .sw",{{opacity:0,duration:0.2,ease:"power1.in"}},{max(c.start + c.enter + 0.05, c.end - 0.2):.3f});')
    # slow push-in over the whole scene (camera), calm: at most 4 %
    out.append(f'tl.fromTo("#{s} .sw-st",{{scale:1}},{{scale:{float(d.get("push", 1.035)):.3f},duration:{c.duration:.2f},ease:"none"}},{c.start:.3f});')
    return out


def _mask(top: int, bottom: int) -> str:
    g = f"linear-gradient(to bottom,transparent {top}px,#000 {top + 40}px,#000 {bottom - 50}px,transparent {bottom}px)"
    return f"-webkit-mask-image:{g};mask-image:{g};"


def _lead_path(a: tuple[float, float], b: tuple[float, float]) -> str:
    mx = (a[0] + b[0]) / 2
    return f"M{a[0]:.1f},{a[1]:.1f} L{mx:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"


# --- 1. hook --------------------------------------------------------------------------------------

def hook(c: SceneCtx, d: dict) -> SceneOut:
    """Question on top, the jacket draws itself, a loupe opens on the detail, the cut line answers "kein Versehen"."""
    s, t = c.sid, c.t
    spec = _spec(d, default_fast=[0])
    target = d.get("target", "button:1")
    box = _place_collar(float(d.get("jacket_x", 380)), c.zone_top + 168, 590)
    tp = _px(box, O.spot(spec, target))
    lx, ly, lr = float(d.get("loupe_x", 742)), float(d.get("loupe_y", 872)), float(d.get("loupe_r", 172))
    svg = O.draw(f"{s}j", spec, c.pal["accent"], ring=[target])
    edge = O.front_edge(spec)
    q_at, b_at = _rel(c, d.get("question_at"), 0.4), _rel(c, d.get("badge_at"), 1.9)
    l_at, n_at, cut_at = (_rel(c, d.get(k), v) for k, v in (("loupe_at", b_at), ("nie_at", b_at + 1.0), ("cut_at", 4.5)))
    badge = d.get("badge", "?")
    # connector: from the ring on the button to the near edge of the loupe
    ang = math.atan2(ly - tp[1], lx - tp[0])
    a = (tp[0] + 30 * box["s"] * math.cos(ang), tp[1] + 30 * box["s"] * math.sin(ang))
    b = (lx - lr * math.cos(ang), ly - lr * math.sin(ang))
    bx, by = lx + lr * 0.62, ly - lr * 0.95
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st">
<div class="sw-q">{_e(d.get('question', ''))}</div>
{_jk(s, 'cam', box, svg)}
{_jo('cutl', box, f'<path class="cut" pathLength="1" d="{edge}"/>') if edge else ''}
<svg class="sw-over" viewBox="0 0 {W} 1920"><path class="sw-lead" pathLength="1" d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"/></svg>
{_loupe(f"{s}l", spec, target, lx, ly, lr, float(d.get("loupe_mag", 2.4)), c.pal["accent"])}
<div class="sw-badge" style="left:{bx - 42:.0f}px;top:{by - 42:.0f}px">{_e(badge)}</div>
</div></div>""")
    out.tl += _enter_exit(c, {**d, "push": 1.04})
    out.tl += _draw_in(f"#{s} .cam", t(0.05), 1.5)
    out.tl.append(f'tl.fromTo("#{s} .sw-q",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{t(q_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .cam .ring",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power1.inOut"}},{t(b_at - 0.2):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-lead",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.35}},{t(l_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-loupe",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.4)"}},{t(l_at + 0.15):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-li",{{scale:0.8,transformOrigin:"{lr:.0f}px {lr:.0f}px"}},{{scale:1.08,duration:{max(1.0, c.duration - l_at):.2f},ease:"none"}},{t(l_at + 0.15):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-badge",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{t(n_at):.3f});')
    if edge:
        out.tl.append(f'tl.fromTo("#{s} .cut",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.7,ease:"power1.inOut"}},{t(cut_at):.3f});')
    out.events = [c.start, t(q_at), t(1.5), t(b_at), t(l_at + 0.15), t(n_at)] + ([t(cut_at)] if edge else [])
    _limit("cinematic_hook", "question", d.get("question", ""), "question", out.problems)
    _limit("cinematic_hook", "badge", badge, "badge", out.problems)
    return out


# --- 2. fitting (ui_demo) -------------------------------------------------------------------------

def fitting(c: SceneCtx, d: dict) -> SceneOut:
    """Close-up: a pin travels to the detail, zoom, the state changes (`from` -> `to` object, or from_fastened ->
    to_fastened on the jacket). Optional events only when their anchor is set: all_at (button pulses), error_at
    (red ring), pull_at (red arrows at the hips), tense_at (strain pulses), ghost_at (gold target line)."""
    s, t = c.sid, c.t
    spec_a = _spec(d, "from_fastened", default_fast=[0], **(d.get("from") or {}))
    spec_b = _spec(d, "to_fastened", default_fast=[0, 1], **{"strain": bool(d.get("strain", True)), **(d.get("to") or {})})
    target = d.get("target", "button:1")
    box = _place_collar(520, c.zone_top + 112, 640)
    tp = _px(box, O.spot(spec_a, target))
    zoom = float(d.get("zoom", 1.6))
    svg_a = O.draw(f"{s}a", spec_a, c.pal["accent"])
    svg_b = O.draw(f"{s}b", spec_b, c.pal["accent"])
    keys = (("pointer_at", 1.6), ("zoom_at", 3.6), ("flip_at", 5.0), ("label_at", 6.0))
    p_at, z_at, f_at, l_at = (_rel(c, d.get(k), v) for k, v in keys)
    opt = {k: _rel(c, d[k], 0.0) for k in ("all_at", "error_at", "pull_at", "tense_at", "ghost_at") if d.get(k) is not None}
    win_top, win_bot = 236, c.zone_top + c.zone_h          # the close-up stays in a window above the marker row
    label = d.get("label", "")
    btn = O.button_spots(spec_a) if "all_at" in opt else []
    pulses = "".join(_pulse(f"p{i}", x, y, 30) for i, (x, y) in enumerate(btn))
    hips = (_arrow("red pull", 92, 640, 46) + _arrow("red pull", 508, 640, -46)) if "pull_at" in opt else ""
    edge = O.front_edge(spec_a) if "ghost_at" in opt else ""
    ghost = f'<path class="ghost" pathLength="1" d="{edge}"/>' if edge else ""
    ex, ey = O.spot(spec_a, target)
    err = f'<circle class="pulse red err" cx="{ex}" cy="{ey}" r="34"/>' if "error_at" in opt else ""
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st">
<div class="sw-h">{_e(d.get('headline', ''))}</div>
<div class="sw-win" style="position:absolute;inset:0;{_mask(win_top, win_bot)}">
<div class="sw-zoomwrap" style="position:absolute;inset:0;transform-origin:{tp[0]:.1f}px {tp[1]:.1f}px;">
{_jk(s, 'sa', box, svg_a)}{_jk(s, 'sb', box, svg_b, 'opacity:0;')}
{_jo('fo', box, pulses + hips + ghost + err)}
<div class="sw-pin" style="left:{tp[0]:.1f}px;top:{tp[1]:.1f}px"></div>
</div></div>
<div class="sw-card" style="left:150px;width:740px;box-sizing:border-box;top:{c.zone_top - 40}px">{_e(label)}</div>
</div></div>""")
    out.tl += _enter_exit(c, {**d, "push": 1.0})
    out.tl.append(f'tl.fromTo("#{s} .sw-h",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{c.start:.3f});')
    events = [c.start, t(p_at), t(z_at), t(f_at), t(l_at)]
    for i in range(len(btn)):       # "Alle Knöpfe": every button shows itself
        out.tl += _tl_pulse(f"#{s} .p{i}", t(opt["all_at"] + 0.12 * i))
        out.tl.append(f'tl.to("#{s} .p{i}",{{opacity:0,duration:0.4}},{t(opt["all_at"] + 1.4):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-pin",{{x:320,y:260,opacity:0}},{{x:0,y:0,opacity:1,duration:0.9,ease:"power2.inOut"}},{t(p_at):.3f});')
    if err:
        out.tl += _tl_pulse(f"#{s} .err", t(opt["error_at"]))      # "Fehler": the detail gets a red ring
        out.tl.append(f'tl.to("#{s} .err",{{opacity:0,duration:0.3}},{t(f_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-zoomwrap",{{scale:1}},{{scale:{zoom},duration:1.1,ease:"power2.inOut"}},{t(z_at):.3f});')
    out.tl.append(f'tl.to("#{s} .sw-h",{{opacity:0,duration:0.35}},{t(z_at):.3f});')   # the zoomed object covers the headline zone
    out.tl.append(f'tl.to("#{s} .sw-pin",{{opacity:0,duration:0.3}},{t(f_at - 0.2):.3f});')
    out.tl.append(f'tl.to("#{s} .sb",{{opacity:1,duration:0.5}},{t(f_at):.3f});')
    out.tl.append(f'tl.to("#{s} .sa",{{opacity:0,duration:0.5}},{t(f_at):.3f});')
    if spec_b.get("strain"):
        out.tl.append(f'tl.fromTo("#{s} .sb .strain",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power1.out"}},{t(f_at + 0.3):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-card",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t(l_at):.3f});')
    if hips:
        out.tl.append(f'tl.fromTo("#{s} .pull",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{t(opt["pull_at"]):.3f});')
    if "tense_at" in opt and spec_b.get("strain"):
        out.tl.append(f'tl.fromTo("#{s} .sb .strain",{{strokeWidth:3.4}},{{strokeWidth:5.2,duration:0.3,yoyo:true,repeat:1}},{t(opt["tense_at"]):.3f});')
    if ghost:
        out.tl.append(f'tl.to("#{s} .ghost",{{opacity:0.9,duration:0.6}},{t(opt["ghost_at"]):.3f});')
    out.tl.append(f'tl.to("#{s} .sw-zoomwrap",{{scale:{max(1.0, zoom - 0.2):.2f},duration:{max(0.5, c.duration - l_at - 0.6):.2f},ease:"none"}},{t(l_at + 0.4):.3f});')
    events += [t(v) for v in opt.values()]
    out.events = sorted(set(events))
    _limit("ui_demo", "headline", d.get("headline", ""), "headline", out.problems)
    _limit("ui_demo", "label", label, "label", out.problems)
    return out


# --- 3. rule ladder (data_flow) -------------------------------------------------------------------

def ladder(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    stages = d.get("stages", [])
    box = _place_collar(330, c.zone_top + 126, 590)
    parts, tl, events, probs = [], [], [c.start], []
    tl.append(f'tl.fromTo("#{s} .sw-h",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{c.start:.3f});')
    for k, st in enumerate(stages):
        spec = _spec(st, default_fast=[0])
        at = _rel(c, st.get("at"), 0.0)
        svg = O.draw(f"{s}s{k}", spec, c.pal["accent"])
        leads, tags, pul = [], [], []
        # tag rows follow the buttons but keep at least 104 px apart (text + small line)
        names = [tg.get("spot") or f"button:{tg['button']}" for tg in st.get("tags", [])]
        bps = [_px(box, O.spot(spec, nm)) for nm in names]
        rows: dict[int, float] = {}
        last = -1e9
        for j in sorted(range(len(bps)), key=lambda j: bps[j][1]):
            rows[j] = max(bps[j][1], last + 104)
            last = rows[j]
        for j, tg in enumerate(st.get("tags", [])):
            bp = bps[j]
            ty = rows[j]
            leads.append(f'<path class="sw-lead l{k}_{j}" pathLength="1" d="{_lead_path((bp[0] + 18, bp[1]), (596, ty))}"/><circle class="sw-dot d{k}_{j}" cx="596" cy="{ty:.1f}" r="5"/>')
            tone = tg.get("tone", "sometimes")
            pcls = {"always": "", "never": "red", "sometimes": "amber"}.get(tone, "")
            pul.append(_pulse(f"{pcls} q{k}_{j}", *O.spot(spec, names[j]), 32))
            en = f' <i class="en e{k}_{j} tone-{tone}">· {_e(tg["en"])}</i>' if tg.get("en") else ""
            sub = f"<small>{_e(tg.get('sub', ''))}{en}</small>" if (tg.get("sub") or en) else ""
            tags.append(f'<div class="sw-tag t{k}_{j} tone-{tone}" style="left:616px;top:{ty - 24:.1f}px">{_e(tg["text"])}{sub}</div>')
            _limit("data_flow", "tag", tg["text"], f"stage{k}.tag{j}", probs)
        title = f'<div class="sw-stage" style="top:{c.zone_top + 118}px">{_e(st["title"])}</div>' if st.get("title") else ""
        if st.get("title"):
            _limit("data_flow", "stage_title", st["title"], f"stage{k}.title", probs)
        parts.append(f'<div class="stage{k}" style="position:absolute;inset:0;opacity:0">{_jk(s, f"j{k}", box, svg)}{_jo(f"jo{k}", box, "".join(pul))}'
                     f'<svg class="sw-over" viewBox="0 0 {W} 1920">{"".join(leads)}</svg>{title}{"".join(tags)}</div>')
        nxt = _rel(c, stages[k + 1].get("at"), 0.0) if k + 1 < len(stages) else None
        tl.append(f'tl.to("#{s} .stage{k}",{{opacity:1,duration:0.45}},{t(at):.3f});')
        if k == 0:
            tl += _draw_in(f"#{s} .j0", t(at), 1.2)
        else:
            tl.append(f'tl.fromTo("#{s} .j{k}",{{x:-30}},{{x:0,duration:0.6,ease:"power2.out"}},{t(at):.3f});')
        if nxt is not None:
            tl.append(f'tl.to("#{s} .stage{k}",{{opacity:0,duration:0.4}},{t(nxt - 0.1):.3f});')
        step = float(st.get("tag_step", 1.2))
        first = _rel(c, st.get("tags_at"), at + (1.2 if k == 0 else 0.5))
        for j, tg in enumerate(st.get("tags", [])):
            ta = _rel(c, tg.get("at"), first + j * step)
            tl.append(f'tl.fromTo("#{s} .l{k}_{j}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.4}},{t(ta):.3f});')
            tl.append(f'tl.fromTo("#{s} .d{k}_{j}",{{opacity:0}},{{opacity:1,duration:0.2}},{t(ta + 0.3):.3f});')
            tl.append(f'tl.fromTo("#{s} .t{k}_{j}",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.35,ease:"power2.out"}},{t(ta + 0.3):.3f});')
            tl += _tl_pulse(f"#{s} .q{k}_{j}", t(ta))
            tl.append(f'tl.to("#{s} .q{k}_{j}",{{opacity:0,duration:0.4}},{t(ta + 1.1):.3f});')
            events.append(t(ta))
            if tg.get("en"):        # the English mnemonic word lights up on its spoken word
                ea = _rel(c, tg.get("en_at"), ta + 2.0)
                tl.append(f'tl.fromTo("#{s} .e{k}_{j}",{{opacity:0}},{{opacity:1,duration:0.3}},{t(ea):.3f});')
                tl.append(f'tl.fromTo("#{s} .t{k}_{j}",{{scale:1}},{{scale:1.08,duration:0.25,yoyo:true,repeat:1,ease:"power1.inOut"}},{t(ea):.3f});')
                events.append(t(ea))
        if st.get("focus_at") is not None:   # the jacket steps back so the rules carry the scene
            fa = _rel(c, st.get("focus_at"), 0.0)
            tl.append(f'tl.to("#{s} .j{k}",{{opacity:0.5,duration:0.5}},{t(fa):.3f});')
            events.append(t(fa))
        events.append(t(at))
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st"><div class="sw-h">{_e(d.get('headline', ''))}</div>{''.join(parts)}</div></div>""")
    out.tl = _enter_exit(c, d) + tl
    out.events = sorted(set(events))
    _limit("data_flow", "headline", d.get("headline", ""), "headline", out.problems)
    out.problems += probs
    return out


# --- 4. comparison --------------------------------------------------------------------------------

def compare(c: SceneCtx, d: dict) -> SceneOut:
    """Two jackets; optional shape arrows (`shape: waist|hips|pull` per side), a second tag in amber, pulses."""
    s, t = c.sid, c.t
    sides, extra_tl, events = [], [], []
    centers = (300, 738)
    width = float(d.get("jacket_w", 470))
    for k, side in enumerate(("left", "right")):
        cx = centers[k]
        sd = d.get(side) or {}
        spec = _spec(sd, default_fast=[0])
        box = _place_collar(cx, c.zone_top + 190, width)
        rings = [sd["target"]] if sd.get("target") else []
        svg = O.draw(f"{s}{side[0]}", spec, c.pal["accent"], ring=rings)
        title_top = c.zone_top + 104
        tag_top = box["top"] + 728 * box["s"]
        tw = 380 if k else 360
        tag2 = (f'<div class="sw-ctag amber tg2" style="left:{cx - tw / 2:.0f}px;width:{tw}px;top:{tag_top + 42:.0f}px">{_e(sd["tag2"])}</div>'
                if sd.get("tag2") else "")
        ov = []
        for sh in sd.get("shapes", []):     # arrows that show the cut: waist in, hips out, pull in (red)
            kind = sh.get("kind")
            if kind == "waist":
                ov.append(f'<g class="sh{k}_{kind}">{_arrow("gold", 100, 440, 46)}{_arrow("gold", 500, 440, -46)}</g>')
            elif kind == "hips":
                ov.append(f'<g class="sh{k}_{kind}">{_arrow("gold", 140, 640, -52)}{_arrow("gold", 460, 640, 52)}</g>')
            elif kind == "pull":
                ov.append(f'<g class="sh{k}_{kind}">{_arrow("red", 84, 640, 50)}{_arrow("red", 516, 640, -50)}</g>')
            elif kind == "cut":
                ov.append(f'<g class="sh{k}_{kind}"><path class="cut" pathLength="1" d="{O.front_edge(spec)}"/></g>')
            ta = t(_rel(c, sh.get("at"), 1.0))
            sel = f"#{s} .sh{k}_{kind} .arw" if kind != "cut" else f"#{s} .sh{k}_{kind} .cut"
            extra_tl.append(f'tl.fromTo("{sel}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{ta:.3f});')
            events.append(ta)
        for pi, pu in enumerate(sd.get("pulses", [])):   # a ring pulse on a named detail
            x, y = O.spot(spec, pu["target"])
            ov.append(_pulse(f'{pu.get("tone", "")} pu{k}_{pi}', x, y, 34))
            ta = t(_rel(c, pu.get("at"), 1.0))
            extra_tl += _tl_pulse(f"#{s} .pu{k}_{pi}", ta)
            events.append(ta)
        if sd.get("tag2"):
            ta = t(_rel(c, sd.get("tag2_at"), 6.0))
            extra_tl.append(f'tl.fromTo("#{s} .side{k} .tg2",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.35}},{ta:.3f});')
            events.append(ta)
        sides.append(f'<div class="sw-side side{k}" style="position:absolute;inset:0">'
                     f'<div class="sw-ctitle" style="left:{cx - 200}px;width:400px;top:{title_top}px">{_e(sd.get("title", ""))}</div>'
                     f'{_jk(s, f"jj{k}", box, svg)}{_jo(f"o{k}", box, "".join(ov))}'
                     f'<div class="sw-ctag" style="left:{cx - tw / 2:.0f}px;width:{tw}px;top:{tag_top:.0f}px">{sd.get("tag_html") or _e(sd.get("tag", ""))}</div>{tag2}</div>')
    l_at, r_at = _rel(c, d.get("left_at"), 0.3), _rel(c, d.get("right_at"), 3.0)
    tag_at = (_rel(c, d.get("left_tag_at"), l_at + 1.4), _rel(c, d.get("right_tag_at"), r_at + 1.4))
    mid = (centers[0] + centers[1]) / 2
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st"><div class="sw-h">{_e(d.get('headline', ''))}</div>
<svg class="sw-over" viewBox="0 0 {W} 1920"><path class="sw-lead mid" pathLength="1" d="M{mid:.0f},{c.zone_top + 120} L{mid:.0f},{c.zone_top + 760}"/></svg>{''.join(sides)}</div></div>""")
    out.tl = _enter_exit(c, d)
    out.tl.append(f'tl.fromTo("#{s} .sw-h",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .mid",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8}},{t(0.2):.3f});')
    for k, at in enumerate((l_at, r_at)):
        out.tl.append(f'tl.fromTo("#{s} .side{k}",{{opacity:0.0}},{{opacity:1,duration:0.4}},{t(at):.3f});')
        out.tl += _draw_in(f"#{s} .jj{k}", t(at), 1.1)
        out.tl.append(f'tl.fromTo("#{s} .side{k} .ring",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.5}},{t(tag_at[k] - 0.2):.3f});')
        if (d.get(("left", "right")[k]) or {}).get("strain"):
            out.tl.append(f'tl.fromTo("#{s} .side{k} .strain",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.7}},{t(tag_at[k] - 0.3):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .side{k} .sw-ctag:not(.tg2)",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35}},{t(tag_at[k]):.3f});')
    out.tl += extra_tl
    out.events = sorted(set([c.start, t(l_at), t(tag_at[0]), t(r_at), t(tag_at[1])] + events))
    _limit("comparison", "headline", d.get("headline", ""), "headline", out.problems)
    for side in ("left", "right"):
        sd = d.get(side) or {}
        _limit("comparison", "title", sd.get("title", ""), f"{side}.title", out.problems)
        _limit("comparison", "tag", sd.get("tag", ""), f"{side}.tag", out.problems)
        _limit("comparison", "tag2", sd.get("tag2", ""), f"{side}.tag2", out.problems)
    return out


# --- 5. take-away and closing ---------------------------------------------------------------------

def takeaway(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    if d.get("mode") == "closing":
        return closing(c, d)
    items = d.get("items", [])[:3]
    cards = []
    top0 = c.zone_top + 112
    for i, it in enumerate(items):
        spec = _spec(it, default_fast=[0])
        mini = O.draw(f"{s}m{i}", spec, c.pal["accent"], lines_class="lnm")
        then = None
        if it.get("then_fastened") is not None or it.get("then"):   # state change on a word (e.g. "Aufstehen": closed again)
            then = {**spec, **({"fastened": it["then_fastened"]} if it.get("then_fastened") is not None else {}), **(it.get("then") or {})}
            mini = (f'<div class="mA" style="position:absolute;inset:0">{mini}</div>'
                    f'<div class="mB" style="position:absolute;inset:0;opacity:0">{O.draw(f"{s}n{i}", then, c.pal["accent"], lines_class="lnm")}</div>')
        ring = ""
        if it.get("ring"):
            x, y = O.spot(then or spec, it["ring"])
            ring = (f'<svg class="mr" viewBox="0 0 {G.VW} {G.VH}" style="position:absolute;inset:0;width:160px;height:208px;overflow:visible">'
                    f'{_pulse(it.get("ring_tone", ""), x, y, 46)}</svg>')
        cards.append(f'<div class="sw-kc k{i}" style="top:{top0 + i * 236}px"><div class="sw-mini">{mini}{ring}</div>'
                     f'<div><div class="sw-kt">{_e(it.get("title", ""))}</div><div class="sw-ks">{_e(it.get("sub", ""))}</div></div>'
                     f'<div class="sw-kn">{i + 1}</div><div class="kc-on"></div></div>')
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st"><div class="sw-h">{_e(d.get('headline', ''))}</div>{''.join(cards)}</div></div>""")
    out.tl = _enter_exit(c, d)
    out.tl.append(f'tl.fromTo("#{s} .sw-h",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{c.start:.3f});')
    events = [c.start]
    ats = [_rel(c, it.get("at"), 0.5 + i * 2.0) for i, it in enumerate(items)]
    for i, it in enumerate(items):
        at = ats[i]
        out.tl.append(f'tl.fromTo("#{s} .k{i}",{{opacity:0.25,x:0}},{{opacity:1,x:0,duration:0.4,ease:"power2.out"}},{t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .k{i} .lnm",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power1.inOut"}},{t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .k{i} .kc-on",{{opacity:0}},{{opacity:1,duration:0.35}},{t(at):.3f});')
        if i + 1 < len(items):
            out.tl.append(f'tl.to("#{s} .k{i} .kc-on",{{opacity:0,duration:0.3}},{t(ats[i + 1]):.3f});')
            out.tl.append(f'tl.to("#{s} .k{i}",{{opacity:0.6,duration:0.3}},{t(ats[i + 1]):.3f});')
        events.append(t(at))
        if it.get("then_fastened") is not None or it.get("then"):
            ta = t(_rel(c, it.get("then_at"), at + 2.0))
            out.tl.append(f'tl.to("#{s} .k{i} .mB",{{opacity:1,duration:0.4}},{ta:.3f});')
            out.tl.append(f'tl.to("#{s} .k{i} .mA",{{opacity:0,duration:0.4}},{ta:.3f});')
            events.append(ta)
        if it.get("ring"):
            ta = t(_rel(c, it.get("ring_at"), at + 0.8))
            out.tl += _tl_pulse(f"#{s} .k{i} .pulse", ta)
            events.append(ta)
    out.events = sorted(set(events))
    _limit("key_takeaway", "headline", d.get("headline", ""), "headline", out.problems)
    for i, it in enumerate(items):
        _limit("key_takeaway", "item_title", it.get("title", ""), f"item{i}.title", out.problems)
        _limit("key_takeaway", "item_sub", it.get("sub", ""), f"item{i}.sub", out.problems)
    return out


def closing(c: SceneCtx, d: dict) -> SceneOut:
    """The story ends in the action: the wrong state is put right on the jacket, then the statement."""
    s, t = c.sid, c.t
    spec_a = _spec(d, "from_fastened", default_fast=[0, 1], **{"strain": bool(d.get("from_strain", True)), **(d.get("from") or {})})
    spec_b = _spec(d, "to_fastened", default_fast=[0], **{"strain": False, **(d.get("to") or {})})
    target = d.get("target", "button:1")
    box = _place_collar(520, c.zone_top + 46, 600)
    svg_a = O.draw(f"{s}a", spec_a, c.pal["accent"])
    svg_b = O.draw(f"{s}b", spec_b, c.pal["accent"], ring=[target])
    edge = O.front_edge(spec_b)
    fix_at, ring_at, st_at, chip_at = (_rel(c, d.get(k), v) for k, v in (("fix_at", 0.4), ("ring_at", 0.8), ("statement_at", 1.6), ("chip_at", 2.9)))
    st_top = box["top"] + 724 * box["s"]
    chip = d.get("chip", "")
    out = SceneOut(html=f"""{_css(c)}<div class="sw">{_backdrop(c, d)}<div class="sw-st">
{_jk(s, 'ca', box, svg_a)}{_jk(s, 'cb ok', box, svg_b, 'opacity:0;')}
{_jo('co', box, f'<path class="cut" pathLength="1" d="{edge}"/>') if edge else ''}
<div class="sw-stmt" style="top:{st_top:.0f}px">{_e(d.get('statement', ''))}</div>
<div class="sw-chip" style="top:{st_top + 98:.0f}px">{_e(chip)}</div>
</div></div>""")
    out.tl = _enter_exit(c, {**d, "push": 1.03})
    out.tl.append(f'tl.to("#{s} .ca .strain",{{opacity:0,duration:0.4}},{t(fix_at):.3f});')
    out.tl.append(f'tl.to("#{s} .cb",{{opacity:1,duration:0.6}},{t(fix_at + 0.2):.3f});')
    out.tl.append(f'tl.to("#{s} .ca",{{opacity:0,duration:0.6}},{t(fix_at + 0.2):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .cb .ring",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.7}},{t(ring_at):.3f});')
    if edge:
        out.tl.append(f'tl.fromTo("#{s} .co .cut",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power1.inOut"}},{t(ring_at + 0.3):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-stmt",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{t(st_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sw-chip",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.5}},{t(chip_at):.3f});')
    out.events = [c.start, t(fix_at), t(ring_at), t(st_at), t(chip_at)]
    _limit("key_takeaway", "statement", d.get("statement", ""), "statement", out.problems)
    _limit("key_takeaway", "chip", chip, "chip", out.problems)
    return out


TEMPLATES = {"suitwerk_hook": hook, "suitwerk_fitting": fitting, "suitwerk_ladder": ladder,
             "suitwerk_compare": compare, "suitwerk_takeaway": takeaway}
HOOK_SCENE_TYPES = ["suitwerk_hook"]


# --- Format "Kreidestrich" (02.11.2026): scene types kw_*, see kreidestrich/scenes.py ------------------------------
# A plan with layout.format == "kreidestrich" gets the cloth layer (tape measure band, chalk filter) instead of the
# atelier; plans with suitwerk_* scenes render unchanged.
import importlib.util as _ilu  # noqa: E402

_kw_spec = _ilu.spec_from_file_location("sw_kreidestrich_scenes", Path(__file__).resolve().with_name("kreidestrich") / "scenes.py")
_kw = _ilu.module_from_spec(_kw_spec)
_kw_spec.loader.exec_module(_kw)
TEMPLATES.update(_kw.TEMPLATES)
LIMITS.update(_kw.LIMITS)
HOOK_SCENE_TYPES += _kw.HOOK_SCENE_TYPES
CSS = _kw.CSS
MANIFEST_EXTRA = _kw.MANIFEST_EXTRA
_sw_layer = LAYER


def LAYER(plan, brand, project_dir, captions):  # noqa: F811,N802 (contract name)
    if (getattr(plan, "layout", None) or {}).get("format") == "kreidestrich":
        return _kw.LAYER(plan, brand, project_dir, captions)
    return _sw_layer(plan, brand, project_dir, captions)
