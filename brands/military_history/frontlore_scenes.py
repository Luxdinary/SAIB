"""Frontlore (military_history) variants of the five direction scene types: documentary tech, archive look.

Loaded by `fn.render.brand_scenes` through `scenes:` in brands/military_history/brand.yaml (docs/direction-system.md 6d):
`TEMPLATES` holds Frontlore variants of the shared scene types; they apply to Frontlore plans only. The scene type
names stay the same, so story validation and the direction checks apply unchanged.

| scene type      | Frontlore layout                                                                             |
|-----------------|----------------------------------------------------------------------------------------------|
| cinematic_hook  | archive card slides in, the drawing draws itself, date stamp, route strip, the dispatch slip   |
| data_flow       | mode `map`: schematic sheet (point, region, road, chain of masts); default: route with stations, dispatch and counters |
| ui_demo         | technical drawing on a drafting sheet, callouts with leader lines, arms turn, detail zoom, counter |
| comparison      | mode `relay`: neighbour station, own station, sight line, two role cards, arms copy the signal; else shared |
| key_takeaway    | mode `timeline` (dated points on a drawn line), mode `closing` (the card returns, stamp, call), else shared |

Q1 (31.10.2026, Qualitätsrunde): every time in `data` may be a word anchor "w:Wort" / "w:Wort#2" (first / second
spoken word of the beat starting with "Wort"), resolved on `SceneCtx.words`; plain numbers stay seconds from the beat
start. `LAYER` puts the survey-map background (make_background.py) under all scenes and pans it per beat.

Drawings are SVG files in brands/military_history/assets/drawings/ (own work, `class="ln"` + `pathLength="1"`
for drawn strokes). Masts in the scenes are generated (`_mast`), stylized, not to scale, no real signal code.
No photos, no realistic scenes of real events (Art. 50 AI Act), no weapons as subject.
"""
from __future__ import annotations

import html
import math
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAWINGS = HERE / "assets" / "drawings"
BG_DIR = HERE / "assets" / "bg"

FL_LIMITS = {
    "cinematic_hook": {"question": 64, "card_title": 30, "card_meta": 28, "stamp": 12, "card_no": 14},
    "data_flow": {"headline": 60, "node_label": 22, "node_code": 14, "edge_label": 28, "chip": 30},
    "ui_demo": {"headline": 60, "callout": 30, "note": 30, "sheet_title": 30},
    "comparison": {"headline": 60},
    "key_takeaway": {"headline": 60, "year": 6, "item_title": 30, "item_sub": 40, "statement": 64, "stamp": 12, "chip": 34, "card_title": 30},
}

# stylized arm positions (rotation in degrees per arm: left/right of pair 1, 2, 3); no historical code table
STATES = {"rest": [0, 0, 0, 0, 0, 0], "A": [38, 0, -36, 34, 0, -34], "B": [-34, 38, 0, -36, 36, 0], "C": [0, -36, 36, 0, -38, 36]}
ARM = 64


def _e(s) -> str:
    return html.escape(str(s))


def _norm(s: str) -> str:
    return re.sub(r"[^\w]", "", str(s).lower())


def _at(c, v, default: float, probs: list[str]) -> float:
    """Seconds from the beat start: a number, or a word anchor "w:Wort" / "w:Wort#2" on the spoken words of the beat."""
    if v is None:
        return float(default)
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v)
    if not s.startswith("w:"):
        return float(s)
    tok, n = s[2:], 1
    if "#" in tok:
        tok, k = tok.rsplit("#", 1)
        n = int(k)
    key = _norm(tok)
    hits = [w for w in (getattr(c, "words", None) or []) if _norm(w.text).startswith(key)]
    if len(hits) >= n:
        return round(hits[n - 1].start - c.start, 3)
    probs.append(f"word anchor {s!r} not found in the beat")
    return float(default)


def _limits(scene_type: str, d: dict) -> list[str]:
    lim = FL_LIMITS.get(scene_type, {})
    p: list[str] = []

    def chk(key, val, where):
        if lim.get(key) and len(str(val)) > lim[key]:
            p.append(f"{scene_type}.{where}: {len(str(val))} chars > {lim[key]}")

    if scene_type == "cinematic_hook":
        for k in ("question", "card_title", "card_meta", "stamp", "card_no"):
            chk(k, d.get(k, ""), k)
    elif scene_type == "data_flow":
        chk("headline", d.get("headline", ""), "headline")
        for n in d.get("nodes", []) + d.get("places", []):
            chk("node_label", n.get("label", ""), f"node {n.get('label', '')}")
            chk("node_code", n.get("code", ""), "node code")
        for e in d.get("edges", []):
            chk("edge_label", e.get("label", ""), "edge")
        for k in ("route_label", "line_label", "chip"):
            chk("edge_label" if k != "chip" else "chip", d.get(k, ""), k)
        chk("chip", (d.get("highlight") or {}).get("label", ""), "highlight.label")
    elif scene_type == "ui_demo":
        chk("headline", d.get("headline", ""), "headline")
        chk("note", d.get("note", ""), "note")
        chk("sheet_title", d.get("sheet_title", ""), "sheet_title")
        for c in d.get("callouts", []):
            chk("callout", c.get("label", ""), "callout")
    elif scene_type == "comparison":
        chk("headline", d.get("headline", ""), "headline")
    elif scene_type == "key_takeaway":
        chk("headline", d.get("headline", ""), "headline")
        for it in d.get("items", []):
            chk("year", it.get("year", ""), "item.year")
            chk("item_title", it.get("title", ""), "item.title")
            chk("item_sub", it.get("sub", ""), "item.sub")
        for k in ("statement", "stamp", "chip", "card_title"):
            chk(k, d.get(k, ""), k)
    return p


def drawing(name: str, cls: str = "") -> str:
    """Inline SVG from assets/drawings (comments stripped); arms get classes arm0..arm5 so a scene can turn them."""
    f = DRAWINGS / name
    if not name or not f.exists():
        return ""
    svg = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8"), flags=re.S).strip()
    k = iter(range(99))
    svg = re.sub(r'class="ln arm"', lambda m: f'class="ln arm arm{next(k)}"', svg)
    return svg.replace("<svg ", f'<svg class="fl-svg {cls}" ', 1)


def _arm_origins(name: str) -> list[tuple[float, float]]:
    f = DRAWINGS / name
    if not f.exists():
        return []
    return [(float(a), float(b)) for a, b in re.findall(r'class="ln arm"[^>]*?x1="([\d.]+)" y1="([\d.]+)"', f.read_text(encoding="utf-8"))]


def _draw_tl(sel: str, at: float, dur: float = 1.4) -> list[str]:
    return [f'tl.fromTo("{sel} .ln",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur:.2f},ease:"power1.inOut",stagger:{{amount:{dur * 0.6:.2f}}}}},{at:.3f});',
            f'tl.fromTo("{sel} .sight,{sel} .pivot",{{opacity:0}},{{opacity:1,duration:0.4}},{at + dur * 0.8:.3f});']


def _mast(pid: str, x: float, y: float, s: float = 1.0, house: bool = True, scope: bool = False) -> tuple[str, list[tuple[float, float]]]:
    """Stylized telegraph mast standing on (x, y) in absolute SVG units; arms are lines with ids pid-a0..a5."""
    p: list[str] = []
    sw = lambda w: f' style="stroke-width:{max(2.0, w * s):.1f}"'                                   # noqa: E731
    if house:
        p.append(f'<rect class="ln" pathLength="1" x="{x - 70 * s:.1f}" y="{y - 110 * s:.1f}" width="{140 * s:.1f}" height="{110 * s:.1f}"{sw(5)}/>')
        p.append(f'<rect class="ln" pathLength="1" x="{x - 30 * s:.1f}" y="{y - 230 * s:.1f}" width="{60 * s:.1f}" height="{120 * s:.1f}"{sw(5)}/>')
        top, mtop = y - 230 * s, y - 430 * s
    else:
        p.append(f'<line class="ln" pathLength="1" x1="{x - 22 * s:.1f}" y1="{y:.1f}" x2="{x + 22 * s:.1f}" y2="{y:.1f}"{sw(5)}/>')
        top, mtop = y, y - 210 * s
    if scope:
        p.append(f'<line class="ln" pathLength="1" x1="{x - 30 * s:.1f}" y1="{y - 190 * s:.1f}" x2="{x - 110 * s:.1f}" y2="{y - 206 * s:.1f}"{sw(9)}/>')
    p.append(f'<line class="ln" pathLength="1" x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{mtop:.1f}"{sw(8)}/>')
    origins = []
    span = top - mtop
    for k in range(3):
        py = mtop + span * (0.12 + 0.3 * k)
        for i, side in ((2 * k, -1), (2 * k + 1, 1)):
            p.append(f'<line class="ln" id="{pid}-a{i}" pathLength="1" x1="{x:.1f}" y1="{py:.1f}" x2="{x + side * ARM * s:.1f}" y2="{py:.1f}"{sw(11)}/>')
            origins.append((round(x, 1), round(py, 1)))
        p.append(f'<circle class="pivot" cx="{x:.1f}" cy="{py:.1f}" r="{max(3.0, 7 * s):.1f}"/>')
    return "".join(p), origins


def _arms_tl(sel_of, origins, state: str, at: float, dur: float = 0.35, set_only: bool = False) -> list[str]:
    out = []
    for i, (ox, oy) in enumerate(origins):
        rot = STATES[state][i]
        if set_only:
            out.append(f'tl.set("{sel_of(i)}",{{rotation:{rot},svgOrigin:"{ox} {oy}"}},{at:.3f});')
        else:
            out.append(f'tl.to("{sel_of(i)}",{{rotation:{rot},svgOrigin:"{ox} {oy}",duration:{dur:.2f},ease:"power2.inOut"}},{at:.3f});')
    return out


def _dep(sid: str, label: str, sub: str = "", glyphs: int = 4, cls: str = "") -> str:
    """The dispatch slip (thread object of the video): paper, header, a row of signal boxes. No message content."""
    boxes = "".join(f'<i class="fl-dg" id="{sid}-dg{k}"></i>' for k in range(glyphs))
    subl = f'<div class="fl-dep-sub">{_e(sub)}</div>' if sub else ""
    return (f'<div class="fl-dep {cls}" id="{sid}-dep"><div class="fl-dep-h"><i class="fl-dep-ic"></i>{_e(label)}</div>'
            f'{subl}<div class="fl-dep-g">{boxes}</div></div>')


def _count_tl(sel: str, to: int, at: float, dur: float = 0.9) -> str:
    return (f'(function(){{const o={{v:0}};const el=document.querySelector("{sel}");'
            f'tl.to(o,{{v:{to},duration:{dur:.2f},ease:"power1.out",onUpdate:function(){{if(el)el.textContent=Math.round(o.v);}}}},{at:.3f});}})();')


def _thin(events: list[float], gap: float = 0.8) -> list[float]:
    """Actions closer than `gap` seconds read as one picture change; report them as one visual event."""
    out: list[float] = []
    for e in sorted(set(round(x, 3) for x in events)):
        if not out or e - out[-1] >= gap:
            out.append(e)
    return out


def _stage_h(c, d: dict) -> int:
    """Stage height under the scene title: zone minus gap minus 80 px per title line (`headline_lines`, default 1)."""
    return int(c.zone_h - 26 - 80 * int(d.get("headline_lines", 1)))


def _base():
    from fn.render import templates as T
    return T


# --- cinematic_hook: archive card ------------------------------------------------------------------

def cinematic_hook(c, d: dict):
    T = _base()
    P: list[str] = []
    out = T.SceneOut(html="")
    at = lambda k, df: _at(c, d.get(k), df, P)                                                        # noqa: E731
    svg = drawing(d.get("drawing", ""), "card-draw")
    card_at, draw_at, stamp_at = at("card_at", 0.05), at("draw_at", 0.4), at("stamp_at", 1.3)
    q_at, dep_at = at("question_at", 0.15), at("packet_at", 3.3)
    a_at, b_at, em_at = at("from_at", 4.0), at("to_at", 4.7), at("em_at", 6.1)
    q, em = d.get("question", ""), d.get("question_em", "")
    qh = _e(q)
    if em and em in q:
        qh = qh.replace(_e(em), f'<span class="fl-em">{_e(em)}<i class="fl-em-line"></i></span>', 1)
    route = d.get("route") or []
    strip = ""
    if len(route) == 2:
        strip = (f'<div class="fl-rs"><span class="fl-rs-a">{_e(route[0])}</span><i class="fl-rs-line"></i>'
                 f'<span class="fl-rs-b">{_e(route[1])}</span></div>')
    dep = _dep(c.sid, d.get("packet_label", ""), d.get("packet_sub", ""), cls="dv-hook") if d.get("packet_label") else ""
    out.html = f"""
<div class="scene-inner fl-hook">
  <div class="question fl-question">{qh}</div>
  <div class="stage">
    <div class="fl-card">
      <div class="fl-card-head"><span>{_e(d.get('card_meta', ''))}</span><span>{_e(d.get('card_no', ''))}</span></div>
      <div class="fl-card-title">{_e(d.get('card_title', ''))}</div>
      {strip}
      <div class="fl-card-draw">{svg}</div>
      <div class="fl-stamp" data-layout-ignore>{_e(d.get('stamp', ''))}</div>
    </div>
    {dep}
  </div>
</div>"""
    s, t = c.sid, c.t
    out.tl += T._enter_exit(c)
    out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .fl-question",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(q_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fl-card",{{y:260,rotation:-3,opacity:0}},{{y:0,rotation:-1,opacity:1,duration:0.6,ease:"power3.out"}},{t(card_at):.3f});')
    out.tl += _draw_tl(f"#{s} .fl-card-draw", t(draw_at), 1.3)
    out.tl.append(f'tl.fromTo("#{s} .fl-stamp",{{opacity:0,scale:2.2,rotation:-16}},{{opacity:0.92,scale:1,rotation:-8,duration:0.26,ease:"power4.in"}},{t(stamp_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fl-card",{{x:0}},{{x:5,duration:0.05,yoyo:true,repeat:3}},{t(stamp_at + 0.25):.3f});')
    events = [c.start, t(card_at), t(draw_at), t(stamp_at)]
    if dep:
        out.tl.append(f'tl.fromTo("#{s}-dep",{{opacity:0,x:120,y:-140,rotation:6}},{{opacity:1,x:0,y:0,rotation:-5,duration:0.55,ease:"power3.out"}},{t(dep_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-dg0",{{backgroundColor:"rgba(31,38,32,0)"}},{{backgroundColor:"var(--fl-stamp)",duration:0.2}},{t(dep_at + 0.5):.3f});')
        events.append(t(dep_at))
    if strip:
        out.tl.append(f'tl.fromTo("#{s} .fl-rs-a",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3}},{t(a_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .fl-rs-line",{{scaleX:0}},{{scaleX:1,duration:{max(0.3, b_at - a_at - 0.1):.2f},ease:"power1.inOut"}},{t(a_at + 0.1):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .fl-rs-b",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.3}},{t(b_at):.3f});')
        events += [t(a_at), t(b_at)]
    if em and em in q:
        out.tl.append(f'tl.fromTo("#{s} .fl-em-line",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power2.out"}},{t(em_at):.3f});')
        events.append(t(em_at))
    out.events = _thin(events)
    out.problems = _limits("cinematic_hook", d) + P + ([] if svg else [f"cinematic_hook: drawing {d.get('drawing')!r} missing chars > 0"] if d.get("drawing") else [])
    return out


# --- data_flow: schematic map / route with stations ------------------------------------------------

def data_flow(c, d: dict):
    return _map(c, d) if d.get("mode") == "map" else _route(c, d)


def _map(c, d: dict):
    """A point (seat of government), a region, the long road between them, then a chain of masts on the same line."""
    T = _base()
    P: list[str] = []
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    H = _stage_h(c, d)
    pa, pb = d["places"][0], d["places"][1]
    ax, ay = float(pa["x"]), float(pa["y"])
    bx, by, rx, ry = float(pb["x"]), float(pb["y"]), float(pb.get("rx", 165)), float(pb.get("ry", 105))
    vx, vy = ax - bx, ay - by
    ln = math.hypot(vx, vy)
    ux, uy = vx / ln, vy / ln
    k = 1 / math.sqrt((ux / rx) ** 2 + (uy / ry) ** 2)
    ex, ey = bx + ux * (k + 16), by + uy * (k + 16)
    sx, sy = ax - ux * 46, ay - uy * 46
    n = int(d.get("masts", 6))
    masts, origins = [], []
    for i in range(n):
        f = 0.12 + 0.76 * i / max(1, n - 1)
        mx, my = sx + (ex - sx) * f, sy + (ey - sy) * f
        m, o = _mast(f"{s}-m{i}", mx, my, 0.34, house=False)
        masts.append(f'<g class="fl-mg" id="{s}-mg{i}">{m}</g>')
        origins.append(o)
    rlx, rly = d.get("route_label_xy", [450, 400])
    cx, cy = d.get("chip_xy", [470, 575])
    dx, dy = d.get("packet_xy", [600, 215])
    hx, hy = rlx - 44, rly + 26
    hourglass = (f'<g id="{s}-hg"><path class="fl-hgp" d="M{hx - 18} {hy - 24} H{hx + 18} L{hx} {hy} L{hx + 18} {hy + 24} H{hx - 18} L{hx} {hy} Z"/>'
                 f'<line class="fl-hgl" x1="{hx - 22}" y1="{hy - 26}" x2="{hx + 22}" y2="{hy - 26}"/><line class="fl-hgl" x1="{hx - 22}" y1="{hy + 26}" x2="{hx + 22}" y2="{hy + 26}"/></g>')
    svg = (f'<svg class="fl-svg fl-mapsvg" viewBox="0 0 864 {H}" style="width:864px;height:{H}px">'
           f'<ellipse class="fl-region" id="{s}-reg" cx="{bx}" cy="{by}" rx="{rx}" ry="{ry}"/>'
           f'<line class="fl-road" id="{s}-road" pathLength="1" x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"/>'
           f'<line class="fl-tline" id="{s}-tline" x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"/>'
           f'{"".join(masts)}{hourglass}</svg>')
    dep = _dep(s, d.get("packet_label", ""), d.get("packet_sub", ""), cls="dv-map") if d.get("packet_label") else ""
    html_ = f"""
<div class="scene-inner fl-mapscene">
  {T._headline(d.get('headline', ''))}
  <div class="stage">
    <div class="fl-mapwrap" style="height:{H}px">
      {svg}
      <div class="fl-pt" id="{s}-pa" style="left:{ax - 27:.0f}px;top:{ay - 27:.0f}px"></div>
      <div class="fl-pl" id="{s}-pal" style="left:{ax + 46:.0f}px;top:{ay - 40:.0f}px"><b>{_e(pa.get('label', ''))}</b><span>{_e(pa.get('code', ''))}</span></div>
      <div class="fl-pl center" id="{s}-pbl" style="left:{bx - 160:.0f}px;width:320px;top:{by - 44:.0f}px"><b>{_e(pb.get('label', ''))}</b><span>{_e(pb.get('code', ''))}</span></div>
      <div class="fl-rl" id="{s}-rl" style="left:{rlx}px;top:{rly}px">{_e(d.get('route_label', ''))}</div>
      <div class="fl-rl acc" id="{s}-ll" style="left:{rlx}px;top:{rly}px">{_e(d.get('line_label', ''))}</div>
      {f'<div class="fl-chip" id="{s}-chip" style="left:{cx}px;top:{cy}px">{_e(d["chip"])}</div>' if d.get("chip") else ""}
      <div class="fl-depwrap" style="left:{dx}px;top:{dy}px">{dep}</div>
    </div>
  </div>
</div>"""
    out = T.SceneOut(html=html_)
    out.tl += T._enter_exit(c)
    out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    b_at, a_at = at(pb.get("at"), 0.4), at(pa.get("at"), 1.8)
    road_at, rl_at, wait_at = at(d.get("route_at"), 2.2), at(d.get("route_label_at"), 3.0), at(d.get("wait_at"), 4.0)
    chip_at, dep_at = at(d.get("chip_at"), 5.2), at(d.get("packet_at"), 7.2)
    ll_at = at(d.get("line_label_at"), 9.0)
    m_at = at(d.get("masts_at"), 8.4 if n else ll_at)       # without masts the road label gives way to the line label
    out.tl.append(f'tl.fromTo("#{s}-reg",{{opacity:0,scale:0.85,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.45,ease:"power3.out"}},{t(b_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-pbl",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.3}},{t(b_at + 0.1):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-pa",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t(a_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-pal",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:0.3}},{t(a_at + 0.08):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-road",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.8,ease:"power1.inOut"}},{t(road_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-rl",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(rl_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-hg",{{opacity:0}},{{opacity:1,duration:0.3}},{t(rl_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-hg",{{rotation:0}},{{rotation:180,svgOrigin:"{hx} {hy}",duration:0.6,ease:"power2.inOut"}},{t(wait_at):.3f});')
    out.tl.append(f'tl.to("#{s}-hg",{{rotation:360,svgOrigin:"{hx} {hy}",duration:0.6,ease:"power2.inOut"}},{t(wait_at + 1.1):.3f});')
    events = [c.start, t(b_at), t(a_at), t(road_at), t(rl_at), t(wait_at)]
    if d.get("chip"):
        out.tl.append(f'tl.fromTo("#{s}-chip",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t(chip_at):.3f});')
        events.append(t(chip_at))
    if dep:
        out.tl.append(f'tl.fromTo("#{s}-dep",{{opacity:0,y:-30,rotation:4}},{{opacity:1,y:0,rotation:-3,duration:0.45,ease:"power3.out"}},{t(dep_at):.3f});')
        events.append(t(dep_at))
    out.tl.append(f'tl.to("#{s}-road",{{opacity:0.25,duration:0.4}},{t(m_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-tline",{{opacity:0}},{{opacity:1,duration:0.4}},{t(m_at):.3f});')
    out.tl.append(f'tl.to("#{s}-rl,#{s}-hg",{{opacity:0,duration:0.25}},{t(m_at):.3f});')
    out.tl.append(f'tl.to("#{s}-pa",{{backgroundColor:"{c.pal["accent"]}",duration:0.25}},{t(m_at):.3f});')
    span = max(0.6, ll_at - m_at + 0.5)
    for i in range(n):
        mt = m_at + span * i / max(1, n - 1)
        out.tl.append(f'tl.fromTo("#{s}-mg{i} .ln",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.35,ease:"power1.out"}},{t(mt):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-mg{i} .pivot",{{opacity:0}},{{opacity:1,duration:0.2}},{t(mt + 0.2):.3f});')
        out.tl += _arms_tl(lambda j, i=i: f"#{s}-m{i}-a{j}", origins[i], "A" if i % 2 == 0 else "B", t(mt + 0.3), 0.3)
    out.tl.append(f'tl.fromTo("#{s}-ll",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(ll_at):.3f});')
    events += [t(m_at), t(ll_at)]
    out.events = _thin(events)
    out.problems = _limits("data_flow", d) + P
    return out


def _route(c, d: dict):
    """Vertical route: stations, the dispatch travels row by row on the spoken place names, counters on the right."""
    T = _base()
    P: list[str] = []
    nodes = d.get("nodes", [])[:5]
    edges = d.get("edges", [])
    n = len(nodes)
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    stage_h = _stage_h(c, d)
    pad = 44
    step = min(440, (stage_h - 2 * pad) / max(1, n - 1))
    top = max(pad, (stage_h - step * (n - 1)) / 2)
    ys = [round(top + i * step) for i in range(n)]
    rows, elabels, ticks = [], [], []
    for i, nd in enumerate(nodes):
        rows.append(f'<div class="fl-stop" id="{s}-n{i}" style="top:{ys[i] - 30}px"><i class="fl-mk"></i>'
                    f'<span class="fl-stop-label">{_e(nd.get("label", ""))}</span><span class="fl-stop-code">{_e(nd.get("code", ""))}</span></div>')
    for i in range(n - 1):
        lab = edges[i].get("label", "") if i < len(edges) else ""
        if lab:
            mid = round((ys[i] + ys[i + 1]) / 2)
            elabels.append(f'<div class="fl-edge" id="{s}-e{i}" style="top:{mid - 18}px">{_e(lab)}</div>')
            for k in range(5):
                ty = ys[i] + 40 + (ys[i + 1] - ys[i] - 80) * k / 4
                ticks.append(f'<i class="fl-tick" style="top:{ty:.0f}px"></i>')
    cnt = d.get("count") or {}
    tot = d.get("total") or {}
    right = ""
    if cnt:
        right += (f'<div class="fl-count" id="{s}-cnt"><b id="{s}-cntn">{int(cnt.get("to", 0))}</b>'
                  f'<span>{_e(cnt.get("label", ""))}</span></div>')
    if tot:
        right += (f'<div class="fl-count" id="{s}-tot"><b><small>{_e(tot.get("pre", ""))}</small><em id="{s}-totn">{int(tot.get("to", 0))}</em></b>'
                  f'<span>{_e(tot.get("label", ""))}</span></div>')
    dep = _dep(s, d.get("packet_label", ""), cls="dv-route", glyphs=3) if d.get("packet_label") else ""
    out = T.SceneOut(html=f"""
<div class="scene-inner fl-route">
  {T._headline(d.get('headline', ''))}
  <div class="stage">
    <div class="fl-map" style="height:{stage_h}px">
      <div class="fl-line" style="top:{ys[0] if ys else 0}px;height:{(ys[-1] - ys[0]) if n > 1 else 0}px"></div>
      {''.join(ticks)}{''.join(rows)}{''.join(elabels)}
      {right}
      <div class="fl-depwrap fl-dw-route" style="top:{(ys[0] if ys else 0) - 52}px">{dep}</div>
    </div>
  </div>
</div>""")
    out.tl += T._enter_exit(c)
    out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fl-line",{{scaleY:0}},{{scaleY:1,duration:{min(1.4, max(0.6, c.duration * 0.25)):.2f},ease:"power1.inOut"}},{t(0.2):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fl-tick",{{opacity:0}},{{opacity:1,duration:0.2,stagger:0.05}},{t(0.9):.3f});')
    for i in range(n):
        out.tl.append(f'tl.fromTo("#{s}-n{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t(0.3 + i * 0.22):.3f});')
    for i in range(n - 1):
        out.tl.append(f'tl.fromTo("#{s}-e{i}",{{opacity:0}},{{opacity:1,duration:0.3}},{t(0.6 + i * 0.22):.3f});')
    events = [c.start]
    if cnt:
        ca = at(cnt.get("at"), 0.1)
        out.tl.append(f'tl.fromTo("#{s}-cnt",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{t(ca):.3f});')
        out.tl.append(_count_tl(f"#{s}-cntn", int(cnt.get("to", 0)), t(ca), 0.8))
        out.tl.append(f'tl.to("#{s}-cnt",{{autoAlpha:0,y:-20,duration:0.3}},{t(at(cnt.get("until"), 3.0)):.3f});')
        events.append(t(ca))
    arr = [at(nd.get("at"), 1.2 + i * 1.1) for i, nd in enumerate(nodes)]
    if n >= 2:
        if dep:
            out.tl.append(f'tl.fromTo("#{s}-dep",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(arr[0] - 0.1):.3f});')
        for i in range(n):
            if i and dep:
                mv = max(0.25, min(0.6, arr[i] - arr[i - 1] - 0.05))
                out.tl.append(f'tl.to("#{s}-dep",{{y:{ys[i] - ys[0]},duration:{mv:.2f},ease:"power2.inOut"}},{t(arr[i] - mv):.3f});')
            out.tl.append(f'tl.to("#{s}-n{i} .fl-mk",{{backgroundColor:"{c.pal["accent"]}",duration:0.2}},{t(arr[i]):.3f});')
            out.tl.append(f'tl.fromTo("#{s}-n{i} .fl-stop-label",{{color:"{c.pal["text"]}"}},{{color:"{c.pal["accent"]}",duration:0.15,yoyo:true,repeat:1}},{t(arr[i]):.3f});')
            events.append(t(arr[i]))
        for k in range(3 if dep else 0):
            out.tl.append(f'tl.fromTo("#{s}-dg{k}",{{backgroundColor:"rgba(31,38,32,0)"}},{{backgroundColor:"var(--fl-stamp)",duration:0.15}},{t(arr[min(n - 1, 1 + k)]):.3f});')
    if tot:
        ta = at(tot.get("at"), c.duration - 3.0)
        out.tl.append(f'tl.fromTo("#{s}-tot",{{autoAlpha:0,y:20}},{{autoAlpha:1,y:0,duration:0.3}},{t(ta):.3f});')
        out.tl.append(_count_tl(f"#{s}-totn", int(tot.get("to", 0)), t(ta), 0.9))
        events.append(t(ta))
    out.events = _thin(events)
    out.problems = _limits("data_flow", d) + P
    return out


# --- ui_demo: technical drawing with callouts ------------------------------------------------------

def ui_demo(c, d: dict):
    T = _base()
    P: list[str] = []
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    svg = drawing(d.get("drawing", ""), "sheet-draw")
    callouts = d.get("callouts", [])[:5]
    sheet_w, sheet_h = 864, int(d.get("sheet_h", 680))
    k = float(d.get("draw_scale", 1.0))                     # drawing scale inside the sheet (viewBox 760 x 620)
    ox, oy = round((sheet_w - 760 * k) / 2), int(d.get("draw_top", 56))
    leaders, labels = [], []
    for i, co in enumerate(callouts):
        ax, ay = round(ox + k * int(co["x"])), round(oy + k * int(co["y"]))
        lx, ly = int(co["lx"]), int(co["ly"])
        leaders.append(f'<line class="fl-leader" id="{s}-l{i}" pathLength="1" x1="{ax}" y1="{ay}" x2="{lx}" y2="{ly + 22}"/>'
                       f'<circle class="fl-dot" id="{s}-d{i}" cx="{ax}" cy="{ay}" r="9"/>')
        align = "right" if co.get("align") == "right" else "left"
        style = f"top:{ly}px;" + (f"right:{sheet_w - lx}px;" if align == "right" else f"left:{lx}px;")
        label = _e(co.get("label", ""))
        cn = co.get("count") or {}
        if cn and "{n}" in co.get("label", ""):
            label = label.replace("{n}", f'<b class="fl-cn" id="{s}-cn{i}">{int(cn.get("to", 0))}</b>')
        labels.append(f'<div class="fl-callout {align}" id="{s}-c{i}" style="{style}">{label}</div>')
    note = d.get("note", "Stilisierte Darstellung" if c.lang == "de" else "Stylized drawing")
    out = T.SceneOut(html=f"""
<div class="scene-inner fl-cut">
  {T._headline(d.get('headline', ''))}
  <div class="stage">
    <div class="fl-sheet" style="width:{sheet_w}px;height:{sheet_h}px">
      <div class="fl-sheet-title">{_e(d.get('sheet_title', ''))}</div>
      <div class="fl-sheet-draw" style="left:{ox}px;top:{oy}px;width:{760 * k:.0f}px;height:{620 * k:.0f}px">{svg}</div>
      <svg class="fl-leaders" viewBox="0 0 {sheet_w} {sheet_h}" style="width:{sheet_w}px;height:{sheet_h}px">{''.join(leaders)}</svg>
      {''.join(labels)}
      <div class="fl-note">{_e(note)}</div>
    </div>
  </div>
</div>""")
    out.tl += T._enter_exit(c)
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fl-sheet",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{t(0.1):.3f});')
    draw_at = at(d.get("draw_at"), 0.3)
    out.tl += _draw_tl(f"#{s} .fl-sheet-draw", t(draw_at), float(d.get("draw_seconds", 1.6)))
    events = [c.start, t(draw_at)]
    for i, co in enumerate(callouts):
        ca = at(co.get("at"), 1.6 + i * 1.6)
        out.tl.append(f'tl.fromTo("#{s}-d{i}",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{t(ca):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-l{i}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.35,ease:"power1.out"}},{t(ca + 0.1):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-c{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(ca + 0.35):.3f});')
        events.append(t(ca))
        cn = co.get("count") or {}
        if cn and "{n}" in co.get("label", ""):
            cat = at(cn.get("at"), ca + 1.0)
            out.tl.append(_count_tl(f"#{s}-cn{i}", int(cn.get("to", 0)), t(cat), float(cn.get("seconds", 1.2))))
            out.tl.append(f'tl.fromTo("#{s}-c{i}",{{scale:1}},{{scale:1.06,duration:0.2,yoyo:true,repeat:1,transformOrigin:"0% 50%"}},{t(cat):.3f});')
            events.append(t(cat))
    # arms turn into stylized positions on spoken words (svgOrigin = pivot in drawing units)
    origins = _arm_origins(d.get("drawing", ""))
    for sig in d.get("signals", []):
        st = sig.get("state", "A")
        if st in STATES and origins:
            sa = at(sig.get("at"), 6.0)
            out.tl += _arms_tl(lambda j: f"#{s} .sheet-draw .arm{j}", origins, st, t(sa), 0.4)
            events.append(t(sa))
    z = d.get("zoom") or {}
    if z.get("at") is not None:
        fx = (ox + k * int(z.get("x", 380))) / sheet_w * 100
        fy = 100.0 if z.get("grow") == "up" else (oy + k * int(z.get("y", 310))) / sheet_h * 100
        za = at(z["at"], 5.0)
        out.tl.append(f'tl.set("#{s} .fl-sheet",{{transformOrigin:"{fx:.1f}% {fy:.1f}%"}},{c.start:.3f});')
        out.tl.append(f'tl.fromTo("#{s} .fl-sheet",{{scale:1}},{{scale:{min(1.3, float(z.get("scale", 1.15))):.2f},duration:0.9,ease:"power2.inOut"}},{t(za):.3f});')
        if z.get("grow") == "up":
            out.tl.append(f'tl.to("#{s} .h2",{{opacity:0.15,duration:0.4}},{t(za):.3f});')
        if z.get("back_at") is not None:
            zb = at(z["back_at"], za + 3.0)
            out.tl.append(f'tl.to("#{s} .fl-sheet",{{scale:1,duration:0.8,ease:"power2.inOut"}},{t(zb):.3f});')
            if z.get("grow") == "up":
                out.tl.append(f'tl.to("#{s} .h2",{{opacity:1,duration:0.4}},{t(zb):.3f});')
            events.append(t(zb))
        events.append(t(za))
    out.events = _thin(events)
    out.problems = _limits("ui_demo", d) + P + ([] if svg else [f"ui_demo: drawing {d.get('drawing')!r} missing chars > 0"])
    return out


# --- comparison: relay between two stations --------------------------------------------------------

def _versus(c, d: dict):
    """Two archive cards side by side (claim / finding, before / after), rows on spoken words, verdict chip."""
    T = _base()
    P: list[str] = []
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    H = _stage_h(c, d)
    cards = []
    for i, side in enumerate(("left", "right")):
        cd = d.get(side) or {}
        rows = "".join(f'<div class="fl-rrow" id="{s}-{side}-r{k}"><i class="mk mk-fact"></i><span>{_e(r["text"] if isinstance(r, dict) else r)}</span></div>'
                       for k, r in enumerate(cd.get("rows", [])))
        tag = f'<div class="fl-vtag">{_e(cd["tag"])}</div>' if cd.get("tag") else ""
        cards.append(f'<div class="fl-vcard {side}" id="{s}-{side}" style="left:{0 if i == 0 else 444}px;min-height:{H - 110}px">'
                     f'{tag}<div class="fl-vtitle">{_e(cd.get("title", ""))}</div>{rows}</div>')
    verdict = f'<div class="fl-verdict" id="{s}-verdict">{_e(d["verdict"])}</div>' if d.get("verdict") else ""
    out = T.SceneOut(html=f"""
<div class="scene-inner fl-vs">
  {T._headline(d.get('headline', ''))}
  <div class="stage"><div class="fl-vswrap" style="height:{H}px">{''.join(cards)}{verdict}</div></div>
</div>""")
    out.tl += T._enter_exit(c)
    out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    for i, side in enumerate(("left", "right")):
        cd = d.get(side) or {}
        ca = at(cd.get("at"), 0.4 + 3.0 * i)
        out.tl.append(f'tl.fromTo("#{s}-{side}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(ca):.3f});')
        events.append(t(ca))
        for k, r in enumerate(cd.get("rows", [])):
            ra = at(r.get("at") if isinstance(r, dict) else None, ca + 0.4 + 0.5 * k)
            out.tl.append(f'tl.fromTo("#{s}-{side}-r{k}",{{opacity:0,x:-12}},{{opacity:1,x:0,duration:0.3}},{t(ra):.3f});')
            events.append(t(ra))
        if i == 1 and d.get("dim_left_at") is not None:
            out.tl.append(f'tl.to("#{s}-left",{{opacity:0.5,duration:0.3}},{t(at(d["dim_left_at"], ca)):.3f});')
    if verdict:
        va = at(d.get("verdict_at"), c.duration - 2.0)
        out.tl.append(f'tl.fromTo("#{s}-verdict",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.6)"}},{t(va):.3f});')
        events.append(t(va))
    out.events = _thin(events)
    out.problems = _limits("comparison", d) + P
    return out


def comparison(c, d: dict):
    if d.get("mode") == "versus_fl":
        return _versus(c, d)
    if d.get("mode") != "relay":
        return _base().comparison(c, d)
    T = _base()
    P: list[str] = []
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    H = _stage_h(c, d)
    (ax_, ay_, as_), (bx_, by_, bs_) = (170, 266, 0.5), (640, 270, 0.62)
    ma, oa = _mast(f"{s}-ma", ax_, ay_, as_)
    mb, ob = _mast(f"{s}-mb", bx_, by_, bs_, scope=True)
    tip = (bx_ - 110 * bs_, by_ - 206 * bs_)
    sight = f'<line class="sight fl-sight" id="{s}-sight" x1="{tip[0]:.1f}" y1="{tip[1]:.1f}" x2="{ax_ + 16}" y2="{ay_ - 330 * as_:.1f}"/>'
    svg = (f'<svg class="fl-svg fl-relaysvg" viewBox="0 0 864 300" style="width:864px;height:300px">'
           f'<g id="{s}-sa">{ma}</g><g id="{s}-sb">{mb}</g>{sight}</svg>')
    cards = []
    for i, cd in enumerate((d.get("cards") or [])[:2]):
        rows = "".join(f'<div class="fl-rrow"><i class="mk mk-fact"></i><span>{_e(r)}</span></div>' for r in cd.get("rows", []))
        icon = ('<svg class="fl-ric" viewBox="0 0 60 40"><path d="M4 24 L44 12 L48 26 L8 36 Z"/><circle cx="52" cy="18" r="6"/></svg>' if cd.get("icon") == "scope"
                else '<svg class="fl-ric" viewBox="0 0 60 40"><path d="M10 34 H50"/><path d="M30 34 V6"/><path d="M30 10 L50 2"/><path d="M30 10 L12 20"/></svg>')
        cards.append(f'<div class="fl-rcard" id="{s}-k{i}" style="left:{0 if i == 0 else 444}px"><div class="fl-rtitle">{icon}{_e(cd.get("title", ""))}</div>{rows}</div>')
    dep = _dep(s, d.get("packet_label", ""), glyphs=4, cls="dv-relay") if d.get("packet_label") else ""
    html_ = f"""
<div class="scene-inner fl-relay">
  {T._headline(d.get('headline', ''))}
  <div class="stage">
    <div class="fl-relaywrap" style="height:{H}px">
      {svg}
      <div class="fl-slabel" id="{s}-la" style="left:{ax_ - 200}px">{_e(d.get('left_station', ''))}</div>
      <div class="fl-slabel" id="{s}-lb" style="left:{bx_ - 200}px">{_e(d.get('right_station', ''))}</div>
      {''.join(cards)}
      <div class="fl-dict" id="{s}-dict">{_e(d.get('dictate_label', ''))}</div>
      <div class="fl-depwrap fl-dw-relay">{dep}</div>
    </div>
  </div>
</div>"""
    out = T.SceneOut(html=html_)
    out.tl += T._enter_exit(c)
    out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    st_at = at(d.get("stations_at"), 0.1)
    out.tl += _draw_tl(f"#{s}-sa", t(st_at), 0.9)
    out.tl += _draw_tl(f"#{s}-sb", t(st_at + 0.3), 0.9)
    out.tl.append(f'tl.fromTo("#{s}-la,#{s}-lb",{{opacity:0}},{{opacity:1,duration:0.3}},{t(st_at + 0.6):.3f});')
    out.tl += _arms_tl(lambda j: f"#{s}-ma-a{j}", oa, "A", c.start, set_only=True)
    out.tl += _arms_tl(lambda j: f"#{s}-mb-a{j}", ob, "rest", c.start, set_only=True)
    events = [c.start, t(st_at)]
    for i, cd in enumerate((d.get("cards") or [])[:2]):
        ka = at(cd.get("at"), 2.0)
        out.tl.append(f'tl.fromTo("#{s}-k{i}",{{opacity:0,y:30}},{{opacity:0.55,y:0,duration:0.35,ease:"power3.out"}},{t(ka + 0.12 * i):.3f});')
        ha = at(cd.get("hi_at"), 3.5 + 4 * i)
        out.tl.append(f'tl.to("#{s}-k{i}",{{opacity:1,borderColor:"{c.pal["accent"]}",duration:0.3}},{t(ha):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-k{i} .fl-rrow",{{opacity:0.35}},{{opacity:1,duration:0.3,stagger:0.5}},{t(ha + 0.1):.3f});')
        if i == 0:
            out.tl.append(f'tl.to("#{s}-k0",{{borderColor:"rgba(230,233,229,0.18)",duration:0.3}},{t(at(d.get("set_at"), 8.0)):.3f});')
        events += [t(ka), t(ha)]
    sa = at(d.get("sight_at"), 6.0)
    out.tl.append(f'tl.fromTo("#{s}-sight",{{opacity:0}},{{opacity:1,duration:0.35}},{t(sa):.3f});')
    da = at(d.get("dictate_at"), 6.7)
    out.tl.append(f'tl.fromTo("#{s}-dict",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t(da):.3f});')
    events += [t(sa), t(da)]
    ma_at = at(d.get("match_at"), 8.9)
    out.tl += _arms_tl(lambda j: f"#{s}-mb-a{j}", ob, "A", t(ma_at), 0.45)
    events.append(t(ma_at))
    if dep:
        pa = at(d.get("packet_at"), 10.8)
        out.tl.append(f'tl.fromTo("#{s}-dep",{{opacity:0}},{{opacity:1,duration:0.25}},{t(pa - 0.45):.3f});')
        out.tl.append(f'tl.to("#{s}-dep",{{x:{d.get("packet_dx", 400)},duration:1.0,ease:"power2.inOut"}},{t(pa):.3f});')
        events.append(t(pa))
    for k, fl in enumerate(d.get("flip_at", [])):
        fa = at(fl, 11.7 + k)
        stn = "B" if k % 2 == 0 else "C"
        out.tl += _arms_tl(lambda j: f"#{s}-ma-a{j}", oa, stn, t(fa), 0.3)
        out.tl += _arms_tl(lambda j: f"#{s}-mb-a{j}", ob, stn, t(fa + 0.35), 0.3)
        if dep:
            out.tl.append(f'tl.fromTo("#{s}-dg{min(3, k + 1)}",{{backgroundColor:"rgba(31,38,32,0)"}},{{backgroundColor:"var(--fl-stamp)",duration:0.15}},{t(fa + 0.35):.3f});')
        events.append(t(fa))
    if dep:
        out.tl.append(f'tl.fromTo("#{s}-dg0",{{backgroundColor:"rgba(31,38,32,0)"}},{{backgroundColor:"var(--fl-stamp)",duration:0.15}},{t(ma_at + 0.45):.3f});')
    out.events = _thin(events)
    out.problems = _limits("comparison", d) + P
    return out


# --- key_takeaway: timeline / closing card ---------------------------------------------------------

def key_takeaway(c, d: dict):
    T = _base()
    P: list[str] = []
    s, t = c.sid, c.t
    at = lambda v, df: _at(c, v, df, P)                                                               # noqa: E731
    mode = d.get("mode")
    if mode == "timeline":
        items = d.get("items", [])[:4]
        pts = "".join(f'<div class="fl-tp" id="{s}-p{i}"><div class="fl-year">{_e(it.get("year", ""))}</div><i class="fl-tmk"></i>'
                      f'<div class="fl-ttext"><div class="fl-ttitle">{_e(it.get("title", ""))}</div><div class="fl-tsub">{_e(it.get("sub", ""))}</div></div></div>'
                      for i, it in enumerate(items))
        out = T.SceneOut(html=f"""
<div class="scene-inner fl-time">
  {T._headline(d.get('headline', ''))}
  <div class="stage"><div class="fl-tl"><div class="fl-tline"></div><div class="fl-tfill" id="{s}-fill"></div>{pts}</div></div>
</div>""")
        out.tl += T._enter_exit(c)
        out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
        out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
        out.tl.append(f'tl.fromTo("#{s} .fl-tline",{{scaleY:0}},{{scaleY:1,duration:1.0,ease:"power1.inOut"}},{t(0.2):.3f});')
        fill_h = lambda i: f'() => document.querySelector("#{s}-p{i}").offsetTop + document.querySelector("#{s}-p{i} .fl-tmk").offsetTop + 22'  # noqa: E731
        if items:
            out.tl.append(f'tl.set("#{s}-fill",{{height:{fill_h(0)}}},{c.start:.3f});')
        events = [c.start]
        ats = [at(it.get("at"), 0.5 + i * max(1.2, (c.duration - 1.5) / max(1, len(items)))) for i, it in enumerate(items)]
        for i, it in enumerate(items):
            a = ats[i]
            out.tl.append(f'tl.fromTo("#{s}-p{i}",{{opacity:0.18,x:-20}},{{opacity:1,x:0,duration:0.35}},{t(a):.3f});')
            out.tl.append(f'tl.fromTo("#{s}-p{i} .fl-tmk",{{scale:0.4,backgroundColor:"{c.pal["surface"]}"}},{{scale:1,backgroundColor:"{c.pal["accent"]}",duration:0.3,ease:"back.out(2)"}},{t(a):.3f});')
            out.tl.append(f'tl.fromTo("#{s}-p{i} .fl-year",{{scale:1}},{{scale:1.08,duration:0.18,yoyo:true,repeat:1,transformOrigin:"100% 50%"}},{t(a):.3f});')
            if i:
                out.tl.append(f'tl.to("#{s}-fill",{{height:{fill_h(i)},duration:0.6,ease:"power2.inOut"}},{t(a - 0.3):.3f});')
            sub_at = it.get("sub_at")
            if sub_at is not None:
                sa = at(sub_at, a + 1.0)
                out.tl.append(f'tl.fromTo("#{s}-p{i} .fl-tsub",{{color:"{c.pal["muted"]}"}},{{color:"{c.pal["accent"]}",duration:0.25}},{t(sa):.3f});')
                events.append(t(sa))
            events.append(t(a))
        end_at = d.get("end_at")
        if end_at is not None:
            ea = at(end_at, c.duration - 1.0)
            out.tl.append(f'tl.to("#{s} .fl-tp:not(:last-child) .fl-ttitle",{{opacity:0.45,duration:0.35}},{t(ea):.3f});')
            events.append(t(ea))
        out.events = _thin(events)
        out.problems = _limits("key_takeaway", d) + P
        return out
    if mode == "closing":
        svg = drawing(d.get("drawing", ""), "card-draw")
        stamp_at, st_at = at(d.get("stamp_at"), 1.0), at(d.get("statement_at"), 0.5)
        chip_at = at(d.get("chip_at"), max(st_at + 1.5, c.duration - 3.2))
        sign_at, ghost_at, note_at = at(d.get("sign_at"), st_at), at(d.get("ghost_at"), stamp_at - 0.6), at(d.get("note_at"), stamp_at + 1.2)
        chip = f'<div class="fl-close-chip">{_e(d["chip"])}</div>' if d.get("chip") else ""
        sign = f'<div class="fl-sign" id="{s}-sign">{_e(d["sign"])}</div>' if d.get("sign") else ""
        note = f'<div class="fl-cnote" id="{s}-note">{_e(d["note"])}</div>' if d.get("note") else ""
        out = T.SceneOut(html=f"""
<div class="scene-inner fl-close">
  <div class="stage">
    <div class="fl-card small">
      <div class="fl-card-head"><span>{_e(d.get('card_meta', ''))}</span><span>{_e(d.get('card_no', ''))}</span></div>
      <div class="fl-card-title">{_e(d.get('card_title', ''))}</div>
      <div class="fl-card-draw">{svg}</div>
      {sign}{note}
      <div class="fl-stamp" data-layout-ignore>{_e(d.get('stamp', ''))}</div>
    </div>
    <div class="fl-close-statement">{_e(d.get('statement', ''))}</div>{chip}
  </div>
</div>""")
        out.tl += T._enter_exit(c)
        out.tl.append(T._camera(c, scale_to=1.02, y_to=-6))
        out.tl.append(f'tl.fromTo("#{s} .fl-card",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power3.out"}},{t(0.05):.3f});')
        out.tl += _draw_tl(f"#{s} .fl-card-draw", t(0.1), 0.8)
        out.tl.append(f'tl.fromTo("#{s} .fl-close-statement",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(st_at):.3f});')
        events = [c.start, t(st_at), t(stamp_at)]
        if sign:
            out.tl.append(f'tl.fromTo("#{s}-sign",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t(sign_at):.3f});')
            events.append(t(sign_at))
        if d.get("ghost_at") is not None:
            out.tl.append(f'tl.to("#{s} .fl-card-draw .ln",{{opacity:0.3,duration:0.5}},{t(ghost_at):.3f});')
            events.append(t(ghost_at))
        out.tl.append(f'tl.fromTo("#{s} .fl-stamp",{{opacity:0,scale:2.2,rotation:-16}},{{opacity:0.92,scale:1,rotation:-8,duration:0.26,ease:"power4.in"}},{t(stamp_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .fl-card",{{x:0}},{{x:5,duration:0.05,yoyo:true,repeat:3}},{t(stamp_at + 0.25):.3f});')
        if note:
            out.tl.append(f'tl.fromTo("#{s}-note",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(note_at):.3f});')
            events.append(t(note_at))
        if chip:
            out.tl.append(f'tl.fromTo("#{s} .fl-close-chip",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.35}},{t(chip_at):.3f});')
            events.append(t(chip_at))
        out.events = _thin(events)
        out.problems = _limits("key_takeaway", d) + P
        return out
    return T.key_takeaway(c, d)            # shared list/statement layout


# --- brand-wide layer: survey map background with parallax -----------------------------------------

def LAYER(plan, brand, project_dir, captions):  # noqa: N802
    """Background under all scenes: base (light, paper, grid) drifts slowly, contours pan to a new spot per beat."""
    dst = Path(project_dir) / "assets" / "bg"
    dst.mkdir(parents=True, exist_ok=True)
    probs = []
    for f in ("base.jpg", "contours.png", "LICENSE.md"):
        if (BG_DIR / f).exists():
            shutil.copy2(BG_DIR / f, dst / f)
        else:
            probs.append(f"background file {f} missing (run brands/military_history/make_background.py)")
    beats = [b for b in plan.beats if b.start is not None]
    total = max([b.start + b.duration for b in beats] + [1.0]) + float((plan.layout or {}).get("tail_seconds", 2.6))
    pans = [(-60, -40), (50, -90), (-90, 30), (70, 60), (-30, 100), (90, -20), (-70, -90), (40, 80)]
    tl = [f'tl.fromTo("#flw-base",{{x:-34,y:-24,scale:1}},{{x:34,y:24,scale:1.035,duration:{total:.2f},ease:"none"}},0);',
          f'tl.set("#flw-cont",{{x:{pans[0][0]},y:{pans[0][1]}}},0);']
    events = []
    for i, b in enumerate(beats[1:], 1):
        px, py = pans[i % len(pans)]
        tl.append(f'tl.to("#flw-cont",{{x:{px},y:{py},duration:1.8,ease:"power2.inOut"}},{b.start:.3f});')
        events.append(round(b.start, 3))
    under = ('<div id="flw"><img id="flw-base" src="assets/bg/base.jpg" alt=""><img id="flw-cont" src="assets/bg/contours.png" alt="">'
             '<div id="flw-vig"></div></div>')
    head = ("<style>#flw{position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none;}"
            "#flw img{position:absolute;left:-120px;top:-120px;width:1320px;height:2280px;}"
            "#flw-vig{position:absolute;inset:0;background:radial-gradient(ellipse 85% 70% at 40% 38%,rgba(0,0,0,0) 50%,rgba(12,16,13,0.55) 100%);}</style>")
    body_end = "<script>(function(){const tl=window.__timelines&&window.__timelines.main;if(!tl)return;" + "".join(tl) + "tl.seek(0);})();</script>"
    return {"head_html": head, "under_scenes_html": under, "body_end_html": body_end, "events": events, "problems": probs}


def scene_css(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:
    acc, text, surf, muted, bg = pal["accent"], pal["text"], pal["surface"], pal["muted"], pal["bg"]
    paper, ink = pal.get("paper", "#E9E4D4"), pal.get("paper_ink", "#1F2620")
    stamp = pal.get("stamp", "#2B4257")
    hair = pal.get("hairline", "rgba(230,233,229,0.12)")
    return f"""
/* Frontlore: documentary tech */
:root{{--fl-stamp:{stamp};}}
.h2{{font-family:'FN {display}';font-weight:{display_w};text-transform:uppercase;letter-spacing:0.02em;font-size:74px;line-height:1.04;text-shadow:0 2px 18px rgba(0,0,0,0.35);}}
.question.fl-question{{font-family:'FN {display}';font-weight:{display_w};font-size:84px;line-height:1.04;letter-spacing:0;text-transform:none;text-shadow:0 2px 18px rgba(0,0,0,0.35);}}
.fl-em{{position:relative;display:inline-block;}}
.fl-em-line{{position:absolute;left:0;right:0;bottom:-4px;height:8px;background:{acc};transform-origin:0 50%;}}
.fl-hook .stage{{display:flex;align-items:center;justify-content:center;}}
.fl-card{{position:relative;width:800px;background:{paper};color:{ink};border-radius:3px;padding:24px 34px 28px;text-align:left;
  box-shadow:0 1px 2px rgba(0,0,0,0.3),0 30px 70px rgba(0,0,0,0.45);background-image:repeating-linear-gradient(0deg,transparent 0 46px,rgba(31,38,32,0.07) 46px 48px);}}
.fl-card::before{{content:"";position:absolute;left:0;right:0;top:0;height:10px;background:{acc};opacity:0.55;}}
.fl-card-head{{display:flex;justify-content:space-between;font-family:'FN {mono}';font-size:28px;letter-spacing:0.06em;color:{ink};opacity:0.75;margin-top:6px;}}
.fl-card-title{{font-family:'FN {display}';font-weight:{display_w};font-size:54px;line-height:1.1;margin:8px 0 6px;color:{ink};}}
.fl-rs{{display:flex;align-items:center;gap:16px;font-family:'FN {mono}';font-size:30px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:{ink};margin:4px 0 6px;}}
.fl-rs-line{{flex:1 1 auto;height:0;border-top:5px dashed {stamp};transform-origin:0 50%;}}
.fl-card-draw{{height:340px;display:flex;justify-content:center;color:{ink};}}
.fl-card-draw .fl-svg{{height:340px;width:auto;}}
.fl-card.small{{width:740px;padding:20px 30px 22px;}}
.fl-card.small .fl-card-draw,.fl-card.small .fl-card-draw .fl-svg{{height:330px;}}
.fl-card.small .fl-card-title{{font-size:46px;}}
.fl-svg .ln{{fill:none;stroke:currentColor;stroke-width:5;stroke-dasharray:1;stroke-dashoffset:1;}}
.fl-svg .ln.thin{{stroke-width:3;}}
.fl-svg .ln.mast{{stroke-width:8;}}
.fl-svg .ln.arm{{stroke-width:11;}}
.fl-svg .ln.scope{{stroke-width:9;}}
.fl-svg .sight{{stroke:currentColor;stroke-width:3;stroke-dasharray:10 12;opacity:0.7;}}
.fl-svg .pivot{{fill:currentColor;}}
.fl-stamp{{position:absolute;right:36px;bottom:40px;font-family:'FN {display}';font-weight:700;font-size:64px;line-height:1;color:{stamp};border:7px solid {stamp};border-radius:8px;padding:8px 22px;letter-spacing:0.06em;text-transform:uppercase;opacity:0;}}
/* dispatch slip: the thread object */
.fl-dep{{position:relative;width:270px;background:{paper};color:{ink};border-radius:3px;padding:12px 16px 14px;text-align:left;
  box-shadow:0 2px 3px rgba(0,0,0,0.3),0 18px 40px rgba(0,0,0,0.45);border-top:8px solid {stamp};}}
.fl-dep-h{{display:flex;align-items:center;gap:10px;font-family:'FN {mono}';font-size:28px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;}}
.fl-dep-ic{{display:inline-block;width:22px;height:16px;border:3px solid {ink};position:relative;}}
.fl-dep-sub{{font-family:'FN {mono}';font-size:26px;margin-top:4px;opacity:0.8;}}
.fl-dep-g{{display:flex;gap:10px;margin-top:10px;}}
.fl-dg{{display:block;width:40px;height:26px;border:3px solid {ink};border-radius:2px;opacity:0.85;}}
.fl-dep.dv-hook{{position:absolute;left:0;bottom:6px;z-index:3;transform:rotate(-5deg);}}
.fl-depwrap{{position:absolute;z-index:3;}}
.fl-dw-route{{left:634px;}}
.fl-dw-route .fl-dep{{width:230px;}}
.fl-dw-relay{{left:222px;top:140px;z-index:1;}}
.fl-relaysvg{{z-index:2;}}
.fl-dw-relay .fl-dep{{width:230px;padding:10px 14px 12px;}}
/* schematic map */
.fl-mapwrap{{position:absolute;left:0;top:0;width:864px;}}
.fl-mapsvg{{position:absolute;left:0;top:0;color:{acc};overflow:visible;}}
.fl-region{{fill:color-mix(in srgb,{acc} 12%,transparent);stroke:{acc};stroke-width:4;stroke-dasharray:14 10;}}
.fl-road{{stroke:{muted};stroke-width:5;stroke-dasharray:1;stroke-dashoffset:1;}}
.fl-tline{{stroke:{acc};stroke-width:6;stroke-dasharray:16 12;}}
.fl-hgp{{fill:color-mix(in srgb,{acc} 22%,transparent);stroke:{acc};stroke-width:4;stroke-linejoin:round;}}
.fl-hgl{{stroke:{acc};stroke-width:5;stroke-linecap:round;}}
.fl-pt{{position:absolute;width:54px;height:54px;border:6px solid {acc};background:{bg};border-radius:2px;}}
.fl-pl{{position:absolute;display:flex;flex-direction:column;text-align:left;line-height:1.1;}}
.fl-pl b{{font-size:50px;font-weight:700;color:{text};}}
.fl-pl span{{font-family:'FN {mono}';font-size:30px;color:{muted};margin-top:4px;}}
.fl-pl.center{{text-align:center;align-items:center;}}
.fl-rl{{position:absolute;max-width:380px;font-family:'FN {mono}';font-size:32px;line-height:1.2;font-weight:600;color:{text};background:color-mix(in srgb,{bg} 80%,transparent);padding:6px 12px;border-left:6px solid {muted};}}
.fl-rl.acc{{border-left-color:{acc};color:{acc};}}
/* route map */
.fl-map{{position:absolute;left:0;top:0;width:864px;}}
.fl-line{{position:absolute;left:120px;width:0;border-left:6px dashed {acc};transform-origin:50% 0;}}
.fl-tick{{position:absolute;left:108px;width:30px;height:4px;background:{acc};opacity:0.8;}}
.fl-stop{{position:absolute;left:96px;height:60px;display:flex;align-items:center;gap:28px;text-align:left;}}
.fl-mk{{display:inline-block;width:54px;height:54px;border:5px solid {acc};background:{bg};border-radius:2px;}}
.fl-stop-label{{font-size:44px;font-weight:700;color:{text};}}
.fl-stop-code{{font-family:'FN {mono}';font-size:30px;color:{muted};}}
.fl-edge{{position:absolute;left:180px;font-family:'FN {mono}';font-size:30px;color:{muted};}}
.fl-count{{position:absolute;right:0;top:0;width:250px;text-align:right;display:flex;flex-direction:column;align-items:flex-end;}}
.fl-count b{{font-family:'FN {display}';font-weight:{display_w};font-size:150px;line-height:0.95;color:{text};}}
.fl-count b small{{font-size:48px;color:{muted};margin-right:8px;}}
.fl-count b em{{font-style:normal;}}
.fl-count span{{font-family:'FN {mono}';font-size:28px;letter-spacing:0.08em;color:{acc};margin-top:6px;}}
.fl-packet{{display:none;}}
.fl-chip{{position:absolute;background:{acc};color:{bg};border-radius:4px;padding:10px 22px;font-family:'FN {mono}';font-size:30px;font-weight:600;white-space:nowrap;}}
/* technical drawing */
.fl-cut .stage{{display:flex;align-items:center;justify-content:center;}}
.fl-sheet{{position:relative;z-index:2;background:{surf};border:2px solid {hair};border-radius:4px;transform-origin:50% 50%;box-shadow:0 30px 70px rgba(0,0,0,0.4);
  background-image:linear-gradient({hair} 1px,transparent 1px),linear-gradient(90deg,{hair} 1px,transparent 1px);background-size:48px 48px;color:{text};}}
.fl-sheet-title{{position:absolute;left:24px;top:16px;font-family:'FN {mono}';font-size:26px;color:{muted};letter-spacing:0.05em;}}
.fl-sheet-draw{{position:absolute;width:760px;height:620px;color:{text};}}
.fl-sheet-draw .fl-svg{{width:100%;height:100%;}}
.fl-leaders{{position:absolute;left:0;top:0;overflow:visible;}}
.fl-leader{{stroke:{acc};stroke-width:3;stroke-dasharray:1;stroke-dashoffset:1;}}
.fl-dot{{fill:{acc};}}
.fl-callout{{position:absolute;max-width:400px;background:color-mix(in srgb,{bg} 88%,transparent);border-left:6px solid {acc};padding:8px 16px;font-size:34px;font-weight:600;line-height:1.2;color:{text};text-align:left;}}
.fl-callout.right{{border-left:none;border-right:6px solid {acc};text-align:right;}}
.fl-cn{{color:{acc};font-family:'FN {display}';font-weight:{display_w};font-size:46px;}}
.fl-note{{position:absolute;right:20px;bottom:14px;font-family:'FN {mono}';font-size:26px;color:{muted};}}
/* relay */
.fl-relaywrap{{position:absolute;left:0;top:0;width:864px;}}
.fl-relaysvg{{position:absolute;left:0;top:0;color:{text};overflow:visible;}}
.fl-sight{{stroke:{acc} !important;stroke-width:4 !important;}}
.fl-slabel{{position:absolute;top:276px;width:400px;text-align:center;font-family:'FN {mono}';font-size:26px;letter-spacing:0.08em;text-transform:uppercase;color:{muted};}}
.fl-rcard{{position:absolute;top:364px;width:420px;min-height:262px;background:color-mix(in srgb,{surf} 92%,transparent);border:3px solid {hair};border-top:10px solid {acc};border-radius:4px;padding:18px 22px;text-align:left;box-shadow:0 24px 50px rgba(0,0,0,0.35);}}
.fl-rtitle{{display:flex;align-items:center;gap:14px;font-family:'FN {mono}';font-size:30px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:{acc};margin-bottom:14px;}}
.fl-ric{{width:54px;height:36px;fill:none;stroke:{acc};stroke-width:4;stroke-linecap:round;stroke-linejoin:round;}}
.fl-rrow{{display:flex;align-items:flex-start;gap:14px;font-size:36px;font-weight:600;line-height:1.18;color:{text};margin-top:12px;}}
.fl-rrow .mk{{flex:0 0 18px;width:18px;height:18px;margin-top:12px;background:{acc};}}
.fl-dict{{position:absolute;left:300px;top:316px;width:264px;text-align:center;background:{acc};color:{bg};font-family:'FN {mono}';font-size:28px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:6px 0;border-radius:4px;z-index:2;}}
/* versus: two archive cards */
.fl-vswrap{{position:absolute;left:0;top:0;width:864px;}}
.fl-vcard{{position:absolute;top:0;width:420px;background:color-mix(in srgb,{surf} 94%,transparent);border:3px solid {hair};border-top:10px solid {muted};border-radius:4px;padding:20px 24px;text-align:left;box-shadow:0 24px 50px rgba(0,0,0,0.35);}}
.fl-vcard.right{{border-top-color:{acc};}}
.fl-vtag{{font-family:'FN {mono}';font-size:28px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:{muted};margin-bottom:8px;}}
.fl-vcard.right .fl-vtag{{color:{acc};}}
.fl-vtitle{{font-family:'FN {display}';font-weight:{display_w};font-size:46px;line-height:1.08;color:{text};margin-bottom:10px;}}
.fl-verdict{{position:absolute;left:0;right:0;bottom:0;margin:0 auto;width:max-content;max-width:840px;background:{acc};color:{bg};font-family:'FN {mono}';font-size:32px;font-weight:700;padding:12px 26px;border-radius:4px;text-align:center;}}
/* comparison (shared) as archive cards */
.cmp .card{{border-radius:4px;border-top:10px solid color-mix(in srgb,{acc} 55%,transparent);}}
.cmp .card.right{{border-color:{hair};border-top:10px solid {acc};}}
.cmp .ctitle{{font-family:'FN {mono}';font-weight:600;font-size:32px;letter-spacing:0.06em;text-transform:uppercase;color:{acc};}}
.cmp .crow{{font-size:42px;}}
.mk-fact{{border-radius:0;}}
/* timeline */
.fl-time .stage{{display:flex;align-items:center;justify-content:center;}}
.fl-tl{{position:relative;width:864px;display:flex;flex-direction:column;gap:64px;padding:20px 0;}}
.fl-tline{{position:absolute;left:256px;top:0;bottom:0;width:6px;background:color-mix(in srgb,{acc} 35%,transparent);transform-origin:50% 0;}}
.fl-tfill{{position:absolute;left:256px;top:0;width:6px;height:60px;background:{acc};}}
.fl-tp{{position:relative;display:flex;align-items:center;gap:0;text-align:left;min-height:140px;}}
.fl-year{{width:220px;font-family:'FN {display}';font-weight:{display_w};font-size:96px;line-height:1;color:{text};text-align:right;padding-right:22px;}}
.fl-tmk{{flex:0 0 44px;width:44px;height:44px;margin-left:12px;border:6px solid {acc};background:{surf};}}
.fl-ttext{{margin-left:34px;}}
.fl-ttitle{{font-size:48px;font-weight:700;color:{text};line-height:1.12;}}
.fl-tsub{{font-family:'FN {mono}';font-size:30px;color:{muted};margin-top:8px;}}
/* closing */
.fl-close .stage{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;}}
.fl-sign{{position:absolute;right:30px;top:62px;background:{stamp};color:{paper};font-family:'FN {display}';font-weight:{display_w};font-size:38px;letter-spacing:0.08em;text-transform:uppercase;padding:8px 20px;border-radius:4px;box-shadow:0 6px 16px rgba(0,0,0,0.25);}}
.fl-cnote{{position:absolute;left:30px;bottom:26px;font-family:'FN {mono}';font-size:26px;color:{ink};border-left:5px solid {stamp};padding-left:12px;max-width:340px;line-height:1.25;}}
.fl-close-statement{{font-family:'FN {display}';font-weight:{display_w};font-size:66px;line-height:1.1;color:{text};max-width:880px;text-shadow:0 2px 18px rgba(0,0,0,0.35);}}
.fl-close-chip{{font-family:'FN {mono}';font-size:32px;font-weight:600;color:{bg};background:{acc};border-radius:4px;padding:12px 28px;}}
"""


# Loaded by fn.render.brand_scenes (brand.yaml `scenes:`); variants apply to Frontlore plans only.
TEMPLATES = {"cinematic_hook": cinematic_hook, "data_flow": data_flow, "ui_demo": ui_demo, "comparison": comparison, "key_takeaway": key_takeaway}
LIMITS = FL_LIMITS
HOOK_SCENE_TYPES = ["cinematic_hook"]


# --- Format "Rekonstruktion" (02.11.2026): scene types fr_*, see rekonstruktion.py ----------------------------------
# The module reuses the word anchors and helpers of this file: its namespace is handed over as FL before it runs.
# Plans with the old scene types (and without layout.format "rekonstruktion") render unchanged.
import importlib.util as _ilu
from types import SimpleNamespace as _NS

_fr_spec = _ilu.spec_from_file_location("fl_rekonstruktion", HERE / "rekonstruktion.py")
_fr = _ilu.module_from_spec(_fr_spec)
_fr.FL = _NS(**{_k: _v for _k, _v in globals().items() if not _k.startswith("__")})
_fr_spec.loader.exec_module(_fr)
TEMPLATES.update(_fr.TEMPLATES)
LIMITS = {**FL_LIMITS, **_fr.LIMITS}
HOOK_SCENE_TYPES += _fr.HOOK_SCENE_TYPES
_fl_css, _fl_layer = scene_css, LAYER


def scene_css(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:  # noqa: F811
    return _fl_css(pal, display, display_w, body, mono) + _fr.CSS(pal, display, display_w, body, mono)


def LAYER(plan, brand, project_dir, captions):  # noqa: F811,N802
    """Format "Rekonstruktion": static map table with time ruler; otherwise the survey map of the old template."""
    if ((plan.layout or {}).get("format")) == "rekonstruktion":
        return _fr.LAYER(plan, brand, project_dir, captions)
    return _fl_layer(plan, brand, project_dir, captions)

MANIFEST_EXTRA = _fr.MANIFEST_EXTRA
