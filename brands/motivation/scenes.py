"""Gritwerk scene types (brands/motivation/scenes.py, contract: fn.render.brand_scenes).

Qualitätsrunde 31.10.2026 (Ziel Scutoria-Niveau): a brand layer with depth under all scenes (LAYER: lamp light,
a calendar of day boxes as a desk in perspective, defocused paper cards, dust in the light, slow camera per beat),
the habit card as the leading object in every scene, big motifs (card 864 px = the full content width) and at
least three image events per scene, each on a spoken word ("w:Wort").

Recurring object (red thread): the habit card, a paper card with a cue ("Nach dem Frühstück"), an action
("ein Glas Wasser") and a grid of day boxes that fill in gold. The status bar carries its name.

Scene types (hook type: gritwerk_tracker):
- gritwerk_tracker  (Cinematic Hook)  habit card, boxes fill to `fill_to`, a stamp lands, the goal ("66 im Schnitt") appears
- gritwerk_study    (Explanation)     the study as a habit card: participants chip, 12 weeks x 7 days fill week by week,
                                      the cue becomes concrete, a daily "how automatic?" scale
- gritwerk_curve    (Data)            schematic learning curve (asymptotic) drawn by a pen dot, paper tags at the
                                      day markers, plateau band, range bar (measured part solid, extrapolated part dashed)
- gritwerk_streaks  (Comparison)      two strips of day boxes, one with a missed day, both keep going, "tomorrow" box
- gritwerk_plan     (Benefit)         the habit card assembles itself: action, cue, then the grid grows from 3 to 10 weeks
- gritwerk_close    (Close)           the plan card again, today's box gets its tick, brand name, claim
"""
from __future__ import annotations

import math
import random
import re

from fn.render.templates import SceneCtx, SceneOut, _e, _enter_exit, _headline

_LIM = {
    "tracker": {"question": 64, "cue": 40, "action": 26, "stamp": 16, "counter_label": 12, "goal": 22},
    "study": {"headline": 30, "cue": 30, "cue_to": 30, "action": 26, "people": 20, "scale_label": 22, "scale_lo": 10, "scale_hi": 10},
    "curve": {"headline": 30, "marker_label": 18, "range_label": 40, "range_note": 34, "y_label": 26, "x_label": 12, "band": 16},
    "streaks": {"headline": 30, "row_title": 24, "note": 52, "chip": 26, "chip_to": 26},
    "plan": {"headline": 30, "cue": 40, "action": 26, "cue_ph": 14, "action_ph": 14, "step": 26, "short_label": 14, "long_label": 14},
    "tracker_close": {"headline": 30, "cue": 40, "action": 26, "chip": 28, "name": 20, "claim": 40, "disclaimer": 60},
    "paper": {"headline": 30, "tag": 22, "cite": 34, "claim": 74, "row_k": 12, "row_v": 38, "stat_value": 12, "stat_label": 36},
    "versus": {"headline": 30, "verdict": 56, "link": 24, "tag": 22, "cite": 30, "line": 50, "value": 12},
    "bars": {"headline": 30, "caption": 44, "note": 56, "label": 18, "text": 10},
}
CARD_W, PAD_X = 864, 40
SCALE_W = 380            # width of the daily "how automatic?" scale in gritwerk_study
INNER_W = CARD_W - 2 * PAD_X


def _rel(c: SceneCtx, v, default) -> float:
    """Offset from the scene start: seconds, or "w:Wort[#n]" = start of that spoken word in the beat
    (Schnitt- und Layout-Vorlage: every image action hangs on a spoken word)."""
    if v is None or v == "":
        return float(default)
    if isinstance(v, (int, float)):
        return float(v)
    m = re.fullmatch(r"w:(.+?)(?:#(\d+))?", str(v).strip())
    if not m:
        raise ValueError(f"{c.sid}: time {v!r} is neither seconds nor 'w:Wort'")
    stem, nth = m.group(1).lower(), int(m.group(2) or 1)
    hits = [w for w in c.words if re.sub(r"[^\wäöüß]", "", w.text.lower()).startswith(stem)]
    if len(hits) < nth:
        raise ValueError(f"{c.sid}: anchor word {v!r} not spoken in this beat")
    return round(hits[nth - 1].start - c.start, 3)


def _limits(mode: str, pairs: list[tuple[str, str]]) -> list[str]:
    lim = _LIM[mode]
    return [f"{mode}.{k}: {len(str(v))} chars > {lim[k]}" for k, v in pairs if lim.get(k) and len(str(v)) > lim[k]]


def _push(c: SceneCtx, scale_to: float = 1.04, y_to: int = -10) -> str:
    """Push-in of the whole stage over the scene (stronger than the flat shared camera, still calm)."""
    return (f'tl.fromTo("#{c.sid} .stage",{{scale:1,y:0}},{{scale:{scale_to},y:{y_to},duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});')


def _enter(c: SceneCtx) -> list[str]:
    """Fade in; the fade out starts only at the end of the beat, i.e. inside the transition into the next beat
    (the director extends the clip by the transition), so an iris or a cross-fade opens over the old picture."""
    return [_enter_exit(c)[0],
            f'tl.to("#{c.sid} .scene-inner",{{opacity:0,duration:0.45,ease:"power1.in"}},{c.end:.3f});']


def _h2_in(c: SceneCtx) -> str:
    return f'tl.fromTo("#{c.sid} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});'


# --- habit card -----------------------------------------------------------------------------------

def _grid(sid: str, total: int, *, box: int, gx: int, gy: int, cols: int | None = None, rows: int | None = None,
          prefix: str = "x", cls: str = "") -> str:
    """Day boxes. With `rows` the grid flows column by column (one column = one week)."""
    cells = "".join(f'<div class="gw-box" id="{sid}-{prefix}{i}" style="width:{box}px;height:{box}px"><div class="gw-fill"></div></div>'
                    for i in range(total))
    if rows:
        style = f"grid-template-rows:repeat({rows},{box}px);grid-auto-flow:column;grid-auto-columns:{box}px;column-gap:{gx}px;row-gap:{gy}px"
    else:
        style = f"grid-template-columns:repeat({cols},{box}px);column-gap:{gx}px;row-gap:{gy}px"
    return f'<div class="gw-grid {cls}" id="{sid}-grid" style="{style}">{cells}</div>'


def _weeks(sid: str, n: int, box: int, gx: int) -> str:
    nums = "".join(f'<span id="{sid}-wk{k}">{k + 1}</span>' for k in range(n))
    return f'<div class="gw-weeks" style="grid-template-columns:repeat({n},{box}px);column-gap:{gx}px">{nums}</div>'


def _card(sid: str, *, cue: str, action: str, body: str, foot: str = "", head_right: str = "", cls: str = "",
          cue_html: str | None = None, action_html: str | None = None) -> str:
    cue_html = cue_html if cue_html is not None else f'<div class="gw-cue" id="{sid}-cue">{_e(cue)}</div>'
    action_html = action_html if action_html is not None else f'<div class="gw-act" id="{sid}-act">{_e(action)}</div>'
    return f"""
    <div class="gw-card {cls}" id="{sid}-card">
      <div class="gw-head"><div class="gw-headl">{cue_html}{action_html}</div>{head_right}</div>
      {body}
      {foot}
    </div>"""


def _foot(sid: str, label: str, right: str = "") -> str:
    return (f'<div class="gw-foot"><div class="gw-footl"><span class="gw-clabel">{_e(label)}</span>'
            f'<span class="gw-count" id="{sid}-cnt"></span></div>{right}</div>')


def _fill_boxes(c: SceneCtx, idxs: list[int], start: float, dur: float, prefix: str = "x") -> tuple[list[str], list[float]]:
    """Gold fill per box, evenly over `dur`; returns timeline lines and the absolute fill times."""
    tl, times = [], []
    n = max(1, len(idxs))
    for k, i in enumerate(idxs):
        at = c.t(start + dur * k / n)
        tl.append(f'tl.fromTo("#{c.sid}-{prefix}{i} .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.16,ease:"back.out(2)"}},{at:.3f});')
        times.append(at)
    return tl, times


def _counter(c: SceneCtx, values: list, times: list[float], key: str = "n") -> tuple[str, list[str]]:
    """Counter as stacked spans switched with tl.set (deterministic under seeking, no onUpdate callbacks)."""
    spans = "".join(f'<span class="gw-n" id="{c.sid}-{key}{k}">{_e(v)}</span>' for k, v in enumerate(values))
    tl = [f'tl.set("#{c.sid}-{key}{k}",{{opacity:0}},{c.start:.3f});' for k in range(len(values))]
    for k, at in enumerate(times):
        tl.append(f'tl.set("#{c.sid}-{key}{k}",{{opacity:1}},{at:.3f});')
        if k:
            tl.append(f'tl.set("#{c.sid}-{key}{k - 1}",{{opacity:0}},{at:.3f});')
    return spans, tl


def _put_counter(out: SceneOut, sid: str, spans: str) -> None:
    out.html = out.html.replace(f'<span class="gw-count" id="{sid}-cnt"></span>', f'<span class="gw-count" id="{sid}-cnt">{spans}</span>')


def _swap_text(c: SceneCtx, sel_a: str, sel_b: str, at: float) -> list[str]:
    """Text A slides out, text B slides in (cue or action that becomes concrete)."""
    return [f'tl.set("{sel_b}",{{opacity:0,y:18}},{c.start:.3f});',
            f'tl.to("{sel_a}",{{opacity:0,y:-18,duration:0.22,ease:"power2.in"}},{c.t(at):.3f});',
            f'tl.to("{sel_b}",{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{c.t(at + 0.18):.3f});']


# --- 1. hook: tracker -------------------------------------------------------------------------------

def hook_tracker(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    total, cols = int(d.get("boxes", 66)), int(d.get("cols", 11))
    fill_to = min(total, int(d.get("fill_to", 21)))
    fill_at, fill_dur = _rel(c, d.get("fill_at"), 0.4), float(d.get("fill_dur", 2.2))
    stamp_at = _rel(c, d.get("stamp_at"), fill_at + fill_dur + 0.2)
    q_at = _rel(c, d.get("question_at"), 0.2)
    rest_at = _rel(c, d.get("rest_at"), stamp_at + 1.0)
    gap = 9 if cols > 8 else 14
    rows = -(-total // cols)
    box = min(84, (INNER_W - (cols - 1) * gap) // cols, (384 - (rows - 1) * gap) // rows)   # 66/11 -> 56 (Q1), 28/7 -> 84
    grid = _grid(s, total, box=box, gx=gap, gy=gap, cols=cols)
    goal = d.get("goal", "")
    right = f'<div class="gw-goal" id="{s}-goal">{_e(goal)}</div>' if goal else ""
    html = f"""
<div class="scene-inner gw-scene gw-hook">
  <div class="question">{_e(d.get('question', ''))}</div>
  <div class="stage">
    {_card(s, cue=d.get('cue', ''), action=d.get('action', ''), body=grid, foot=_foot(s, d.get('counter_label', 'Tag'), right))}
    {f'<div class="gw-stamp" id="{s}-stamp">{_e(d["stamp"])}</div>' if d.get('stamp') else ''}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.035, -8))
    out.tl.append(f'tl.fromTo("#{s}-card",{{y:90,opacity:0,rotationX:18,transformPerspective:1400,transformOrigin:"50% 100%"}},{{y:0,opacity:1,rotationX:0,duration:0.6,ease:"power3.out"}},{t(0.05):.3f});')
    fl, times = _fill_boxes(c, list(range(fill_to)), fill_at, fill_dur)
    out.tl += fl
    spans, ctl = _counter(c, list(range(1, fill_to + 1)), times)
    _put_counter(out, s, spans)
    out.tl += ctl
    if d.get("stamp"):
        out.tl.append(f'tl.fromTo("#{s}-stamp",{{opacity:0,scale:1.6,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.32,ease:"power4.in"}},{t(stamp_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-card",{{x:0}},{{x:5,duration:0.05,yoyo:true,repeat:3}},{t(stamp_at + 0.3):.3f});')
    # the empty rest of the grid lights up as a wave towards the last box: the calendar is longer than the stamp says
    if fill_to < total:
        rest = ",".join(f"#{s}-x{i}" for i in range(fill_to, total))
        out.tl.append(f'tl.fromTo("{rest}",{{borderColor:"rgba(27,23,18,0.16)"}},{{borderColor:"{c.pal["accent"]}",duration:0.3,yoyo:true,repeat:1,stagger:0.018}},{t(rest_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-x{total - 1}",{{boxShadow:"0 0 0 0px rgba(229,180,90,0)"}},{{boxShadow:"0 0 0 6px {c.pal["accent"]}",duration:0.3}},{t(rest_at + 0.018 * (total - fill_to) + 0.2):.3f});')
    if goal:
        out.tl.append(f'tl.fromTo("#{s}-goal",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{t(rest_at + 0.2):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .question",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out"}},{t(q_at):.3f});')
    out.events = [c.start, t(q_at), t(fill_at), t(fill_at + fill_dur / 2), t(stamp_at), t(rest_at)]
    out.problems = _limits("tracker", [("question", d.get("question", "")), ("cue", d.get("cue", "")), ("action", d.get("action", "")),
                                       ("stamp", d.get("stamp", "")), ("counter_label", d.get("counter_label", "Tag")), ("goal", goal)])
    return out


# --- 2. explanation: the study as a habit card ------------------------------------------------------

def exp_study(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    weeks, days = int(d.get("weeks", 12)), int(d.get("days", 7))
    total = weeks * days
    box, gx, gy = 50, 16, 6
    card_at = _rel(c, d.get("card_at"), 0.5)
    people_at = _rel(c, d.get("people_at"), card_at + 1.5)
    fill_at = _rel(c, d.get("fill_at"), people_at + 1.0)
    fill_dur = float(d.get("fill_dur", 3.8))
    cue_hl_at = _rel(c, d.get("cue_hl_at"), fill_at + fill_dur)
    cue_to_at = _rel(c, d.get("cue_to_at"), cue_hl_at + 1.5)
    scale_at = _rel(c, d.get("scale_at"), cue_to_at + 0.8)
    rate_at = _rel(c, d.get("rate_at"), scale_at + 1.5)
    grid = _grid(s, total, box=box, gx=gx, gy=gy, rows=days) + _weeks(s, weeks, box, gx)
    people = d.get("people", "")
    head_right = f'<div class="gw-pchip" id="{s}-people">{_e(people)}</div>' if people else ""
    cue_html = (f'<div class="gw-cuebox"><div class="gw-cue" id="{s}-cue">{_e(d.get("cue", ""))}</div>'
                f'<div class="gw-cue gw-cue-to" id="{s}-cue2">{_e(d.get("cue_to", ""))}</div></div>')
    scale = (f'<div class="gw-scale" id="{s}-scale"><div class="gw-slabel">{_e(d.get("scale_label", ""))}</div>'
             f'<div class="gw-strack"><div class="gw-sfill" id="{s}-sfill"></div><div class="gw-sdot" id="{s}-sdot"></div></div>'
             f'<div class="gw-sends"><span>{_e(d.get("scale_lo", ""))}</span><span>{_e(d.get("scale_hi", ""))}</span></div></div>')
    html = f"""
<div class="scene-inner gw-scene gw-study">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    {_card(s, cue=d.get('cue', ''), action=d.get('action', ''), body=grid, foot=_foot(s, d.get('counter_label', 'Woche'), scale), head_right=head_right, cue_html=cue_html)}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-card",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power3.out"}},{t(card_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-grid .gw-box,#{s} .gw-weeks span",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.25,stagger:0.004,ease:"power2.out"}},{t(card_at + 0.2):.3f});')
    if people:
        out.tl.append(f'tl.fromTo("#{s}-people",{{opacity:0,scale:0.5,rotation:-8}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2.2)"}},{t(people_at):.3f});')
    fl, times = _fill_boxes(c, list(range(total)), fill_at, fill_dur)
    out.tl += fl
    wk_times = [times[k * days] for k in range(weeks)]
    for k, at in enumerate(wk_times):
        out.tl.append(f'tl.to("#{s}-wk{k}",{{color:"{c.pal.get("paper_ink", "#1B1712")}",duration:0.15}},{at:.3f});')
    spans, ctl = _counter(c, list(range(1, weeks + 1)), wk_times)
    _put_counter(out, s, spans)
    out.tl += ctl
    # the cue: "the same situation" gets the gold underline, then becomes concrete ("etwa nach dem Frühstück")
    out.tl.append(f'tl.fromTo("#{s}-cue",{{backgroundSize:"0% 6px"}},{{backgroundSize:"100% 6px",duration:0.4,ease:"power2.out"}},{t(cue_hl_at):.3f});')
    if d.get("cue_to"):
        out.tl += _swap_text(c, f"#{s}-cue", f"#{s}-cue2", cue_to_at)
    out.tl.append(f'tl.fromTo("#{s}-scale",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{t(scale_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-sfill",{{scaleX:0.12}},{{scaleX:0.62,duration:1.1,ease:"power2.inOut"}},{t(rate_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-sdot",{{x:{0.12 * SCALE_W:.0f}}},{{x:{0.62 * SCALE_W:.0f},duration:1.1,ease:"power2.inOut"}},{t(rate_at):.3f});')
    out.events = [c.start, t(card_at), t(people_at), t(fill_at), t(fill_at + fill_dur / 2), t(cue_hl_at), t(cue_to_at), t(scale_at), t(rate_at)]
    out.problems = _limits("study", [("headline", d.get("headline", "")), ("cue", d.get("cue", "")), ("cue_to", d.get("cue_to", "")),
                                     ("action", d.get("action", "")), ("people", people), ("scale_label", d.get("scale_label", "")),
                                     ("scale_lo", d.get("scale_lo", "")), ("scale_hi", d.get("scale_hi", ""))])
    return out


# --- 3. data: curve ---------------------------------------------------------------------------------

def flow_curve(c: SceneCtx, d: dict) -> SceneOut:
    """Schematic asymptotic curve A(t) = 1 - exp(-k t), k chosen so that A reaches 95 % at `plateau_day`."""
    s, t = c.sid, c.t
    W_, H_ = 864, 470
    x0, x1, y0, y1 = 70, 834, 410, 70
    x_max = float(d.get("x_max", 120))
    plateau = float(d.get("plateau_day", 66))
    k = math.log(20) / plateau

    def pt(day: float) -> tuple[float, float]:
        a = 1 - math.exp(-k * day)
        return x0 + (x1 - x0) * day / x_max, y0 - (y0 - y1) * a

    pts = [pt(x_max * i / 120) for i in range(121)]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    draw_at, draw_dur = _rel(c, d.get("draw_at"), 0.5), float(d.get("draw_dur", 3.0))
    chart_at = _rel(c, d.get("chart_at"), 0.2)
    marks, mtl, events = [], [], [c.start, t(chart_at), t(draw_at)]
    # pen dot riding along the curve while it is drawn (12 linear legs, deterministic)
    legs = 12
    pen = [pt(x_max * j / legs) for j in range(legs + 1)]
    mtl.append(f'tl.set("#{s}-pen",{{x:{pen[0][0]:.1f},y:{pen[0][1]:.1f},opacity:0}},{c.start:.3f});')
    mtl.append(f'tl.to("#{s}-pen",{{opacity:1,duration:0.15}},{t(draw_at):.3f});')
    # path length is not linear in x; distribute the legs by the drawn length so dot and stroke stay together
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(120)]
    cum = [0.0]
    for v in seg:
        cum.append(cum[-1] + v)
    for j in range(1, legs + 1):
        a, b = cum[(j - 1) * 10], cum[j * 10]
        mtl.append(f'tl.to("#{s}-pen",{{x:{pen[j][0]:.1f},y:{pen[j][1]:.1f},duration:{draw_dur * (b - a) / cum[-1]:.3f},ease:"none"}},{t(draw_at + draw_dur * a / cum[-1]):.3f});')
    tags = []
    for j, m in enumerate(d.get("markers", [])[:3]):
        day = float(m.get("day", 0))
        x, y = pt(day)
        tone = m.get("tone", "accent")
        marks.append(f'<line class="gw-mline {tone}" id="{s}-m{j}" x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y:.1f}"/>'
                     f'<circle class="gw-mdot {tone}" id="{s}-md{j}" cx="{x:.1f}" cy="{y:.1f}" r="12"/>')
        # paper tag (the habit card's day counter) next to the marker: under the curve near the axis or under the plateau
        below = m.get("label_pos", "above") == "below"
        tx, ty = x + 22, (y0 - 92) if below else (y + 34)
        tags.append(f'<div class="gw-tag {tone}" id="{s}-tg{j}" style="left:{tx:.0f}px;top:{ty:.0f}px"><i></i>{_e(m.get("label", ""))}</div>')
        at = _rel(c, m.get("at"), draw_at + draw_dur * day / x_max)
        mtl.append(f'tl.fromTo("#{s}-m{j}",{{opacity:0}},{{opacity:1,duration:0.3}},{t(at):.3f});')
        mtl.append(f'tl.fromTo("#{s}-md{j}",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t(at):.3f});')
        mtl.append(f'tl.fromTo("#{s}-tg{j}",{{opacity:0,y:14,rotation:-4}},{{opacity:1,y:0,rotation:0,duration:0.32,ease:"back.out(1.8)"}},{t(at + 0.08):.3f});')
        events.append(t(at))
    band_html = ""
    band = d.get("band") or {}
    if band:
        bx, by = pt(float(band.get("from_day", plateau)))
        band_html = (f'<rect class="gw-band" id="{s}-band" x="{bx:.1f}" y="{y1 - 22}" width="{x1 - bx + 6:.1f}" height="{by - y1 + 40:.1f}" rx="14"/>'
                     f'<text class="gw-bandl" id="{s}-bandl" x="{x1 - 8}" y="{y1 - 34}" text-anchor="end">{_e(band.get("label", ""))}</text>')
        b_at = _rel(c, band.get("at"), draw_at + draw_dur)
        mtl.append(f'tl.fromTo("#{s}-band",{{opacity:0,scaleY:0.2,transformOrigin:"50% 0%"}},{{opacity:1,scaleY:1,duration:0.45,ease:"power3.out"}},{t(b_at):.3f});')
        mtl.append(f'tl.fromTo("#{s}-bandl",{{opacity:0}},{{opacity:1,duration:0.3}},{t(b_at + 0.15):.3f});')
        events.append(t(b_at))
    rng = d.get("range") or {}
    range_html = ""
    if rng:
        lo, hi, scale = float(rng.get("from", 0)), float(rng.get("to", 0)), float(rng.get("scale_max", 260))
        meas = float(rng.get("measured_to", hi))
        tick = rng.get("tick")
        pl, pm, ph = 100 * lo / scale, 100 * meas / scale, 100 * hi / scale
        tick_html = f'<div class="gw-rtick" style="left:{100 * float(tick) / scale:.2f}%"></div>' if tick is not None else ""
        ends = [(pl, int(lo)), (ph, int(hi))] + ([(pm, int(meas))] if meas < hi else [])
        range_html = (f'<div class="gw-range" id="{s}-rg"><div class="gw-rlabel">{_e(rng.get("label", ""))}</div>'
                      f'<div class="gw-rtrack"><div class="gw-rseg" id="{s}-rs1" style="left:{pl:.2f}%;width:{pm - pl:.2f}%"></div>'
                      + (f'<div class="gw-rseg dashed" id="{s}-rs2" style="left:{pm:.2f}%;width:{ph - pm:.2f}%"></div>' if meas < hi else "")
                      + f'{tick_html}</div>'
                      f'<div class="gw-rends">{"".join(f"<span style=left:{p:.2f}%>{v}</span>" for p, v in ends)}</div>'
                      + (f'<div class="gw-rnote" id="{s}-rn">{_e(rng.get("note", ""))}</div>' if rng.get("note") else "")
                      + '</div>')
        r_at = _rel(c, rng.get("at"), draw_at + draw_dur + 1.5)
        x_at = _rel(c, rng.get("extra_at"), r_at + 1.6)
        mtl.append(f'tl.fromTo("#{s}-rg",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(r_at):.3f});')
        mtl.append(f'tl.fromTo("#{s}-rs1",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.out"}},{t(r_at + 0.15):.3f});')
        if meas < hi:
            mtl.append(f'tl.fromTo("#{s}-rs2",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out"}},{t(x_at):.3f});')
            events.append(t(x_at))
        if rng.get("note"):
            mtl.append(f'tl.fromTo("#{s}-rn",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.3}},{t(x_at + 0.3):.3f});')
        events.append(t(r_at))
    html = f"""
<div class="scene-inner gw-scene gw-curve">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="gw-chartbox" id="{s}-cb">
      <svg class="gw-chart" viewBox="0 0 {W_} {H_}" width="{W_}" height="{H_}">
        {band_html}
        <line class="gw-axis" x1="{x0}" y1="{y0}" x2="{x1 + 10}" y2="{y0}"/><line class="gw-axis" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1 - 30}"/>
        <text class="gw-alabel" x="{x0 + 14}" y="{y1 - 32}">{_e(d.get('y_label', ''))}</text>
        <text class="gw-alabel" x="{x1 + 10}" y="{y0 + 46}" text-anchor="end">{_e(d.get('x_label', ''))}</text>
        <path class="gw-path" d="{path}"/>
        {''.join(marks)}
      </svg>
      <div class="gw-pen" id="{s}-pen"></div>
      {''.join(tags)}
    </div>
    {range_html}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-cb",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(chart_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .gw-path",{{strokeDashoffset:1500}},{{strokeDashoffset:0,duration:{draw_dur:.2f},ease:"none"}},{t(draw_at):.3f});')
    out.tl += mtl
    out.events = events
    pairs = [("headline", d.get("headline", "")), ("y_label", d.get("y_label", "")), ("x_label", d.get("x_label", "")),
             ("range_label", rng.get("label", "")), ("range_note", rng.get("note", "")), ("band", band.get("label", ""))] + \
            [("marker_label", m.get("label", "")) for m in d.get("markers", [])]
    out.problems = _limits("curve", pairs)
    return out


# --- 4. comparison: streaks -------------------------------------------------------------------------

def cmp_streaks(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    rows = d.get("rows", [])[:2]
    n = int(d.get("boxes", 10))
    gap = 10
    box = min(72, (INNER_W - (n - 1) * gap) // n)
    # fill phases: [{from, to, at, dur}], each "at" on a spoken word
    phases = d.get("phases") or [{"from": 0, "to": n, "at": d.get("fill_at", 0.6), "dur": d.get("fill_dur", 4.0)}]
    parts, tl, events = [], [], [c.start]
    miss_at = _rel(c, d.get("miss_at"), 1.5)
    pulse_at = _rel(c, d.get("miss_pulse_at"), miss_at + 1.4)
    for r, row in enumerate(rows):
        missed = set(int(m) for m in row.get("missed", []))
        filled = set(int(m) for m in row["filled"]) if "filled" in row else None   # None = every box that is not missed
        cells = "".join(f'<div class="gw-box sm{" miss" if i in missed else ""}" id="{s}-r{r}x{i}" style="width:{box}px;height:{box}px"><div class="gw-fill"></div></div>' for i in range(n))
        tag = f'<span class="gw-stag" id="{s}-r{r}tag">{_e(row["tag"])}</span>' if row.get("tag") else ""
        parts.append(f'<div class="gw-srow" id="{s}-r{r}"><div class="gw-stitle">{_e(row.get("title", ""))}{tag}</div>'
                     f'<div class="gw-strip" style="grid-template-columns:repeat({n},{box}px);gap:{gap}px">{cells}</div></div>')
        row_at = _rel(c, row.get("at"), 0.2 + r * 0.4)
        tl.append(f'tl.fromTo("#{s}-r{r}",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t(row_at):.3f});')
        for ph in phases:
            a, b = int(ph["from"]), min(n, int(ph["to"]))
            p_at, p_dur = _rel(c, ph.get("at"), 0.6), float(ph.get("dur", 1.5))
            for i in range(a, b):
                if i in missed or (filled is not None and i not in filled):
                    continue
                at = t(p_at + p_dur * (i - a) / max(1, b - a))
                tl.append(f'tl.fromTo("#{s}-r{r}x{i} .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.16,ease:"back.out(2)"}},{at:.3f});')
        for i in missed:
            tl.append(f'tl.fromTo("#{s}-r{r}x{i}",{{borderColor:"rgba(27,23,18,0.16)"}},{{borderColor:"{c.pal.get("signal_amber", "#E8873A")}",duration:0.25}},{t(miss_at):.3f});')
            tl.append(f'tl.fromTo("#{s}-r{r}x{i}",{{scale:1}},{{scale:1.18,duration:0.22,yoyo:true,repeat:1,ease:"power2.inOut"}},{t(pulse_at):.3f});')
        if row.get("tag"):
            tag_at = _rel(c, row.get("tag_at"), row_at + 1.0)
            tl.append(f'tl.fromTo("#{s}-r{r}tag",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t(tag_at):.3f});')
            events.append(t(tag_at))
    if any(r.get("missed") for r in rows):
        events += [t(miss_at), t(pulse_at)]
    for ph in phases:
        events.append(t(_rel(c, ph.get("at"), 0.6)))
    # "tomorrow": the next box of the strip with the missed day gets a gold ring and then its tick
    nb = d.get("next") or {}
    if nb:
        r, i = int(nb.get("row", len(rows) - 1)), int(nb.get("box", n - 1))
        ring_at, tick_at = _rel(c, nb.get("ring_at"), 0.0), _rel(c, nb.get("tick_at"), 0.0)
        tl.append(f'tl.fromTo("#{s}-r{r}x{i}",{{boxShadow:"0 0 0 0px rgba(229,180,90,0)"}},{{boxShadow:"0 0 0 7px {c.pal["accent"]}",duration:0.3,ease:"power2.out"}},{t(ring_at):.3f});')
        for rr in range(len(rows)):
            tl.append(f'tl.fromTo("#{s}-r{rr}x{i} .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2.4)"}},{t(tick_at):.3f});')
        events += [t(ring_at), t(tick_at)]
    note = d.get("note", "")
    note_at = _rel(c, d.get("note_at"), 3.0)
    chip, chip_to = d.get("chip", ""), d.get("chip_to", "")
    chip_html = ""
    if chip:
        chip_html = (f'<div class="gw-chipbox"><div class="gw-chip2 muted" id="{s}-ch1">{_e(chip)}</div>'
                     + (f'<div class="gw-chip2" id="{s}-ch2">{_e(chip_to)}</div>' if chip_to else "") + '</div>')
        ch_at = _rel(c, d.get("chip_at"), note_at + 1.5)
        tl.append(f'tl.fromTo("#{s}-ch1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{t(ch_at):.3f});')
        events.append(t(ch_at))
        if chip_to:
            to_at = _rel(c, d.get("chip_to_at"), ch_at + 1.5)
            tl += _swap_text(c, f"#{s}-ch1", f"#{s}-ch2", to_at)
            events.append(t(to_at))
    html = f"""
<div class="scene-inner cmp gw-scene gw-streaks">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="gw-scard" id="{s}-sc">{''.join(parts)}</div>
    {f'<div class="gw-snote" id="{s}-note">{_e(note)}</div>' if note else ''}
    {chip_html}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.035, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-sc",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{t(0.1):.3f});')
    out.tl += tl
    if note:
        out.tl.append(f'tl.fromTo("#{s}-note",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(note_at):.3f});')
        events.append(t(note_at))
    out.events = events
    out.problems = _limits("streaks", [("headline", d.get("headline", "")), ("note", note), ("chip", chip), ("chip_to", chip_to)]
                           + [("row_title", r.get("title", "")) for r in rows])
    return out


# --- 5. benefit: the habit card assembles itself ----------------------------------------------------

def take_plan(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    weeks, days = int(d.get("weeks", 10)), int(d.get("days", 7))
    short = int(d.get("short_weeks", 3))
    total = weeks * days
    month = d.get("layout") == "month"
    box, gx, gy = (68, 16, 10) if month else (40, 24, 6)
    steps = d.get("steps", [])[:3]
    action_at = _rel(c, d.get("action_at"), 2.0)
    cue_at = _rel(c, d.get("cue_at"), 5.0)
    grow_at = _rel(c, d.get("grow_at"), 8.0)
    short_at = _rel(c, d.get("short_at"), grow_at + 1.0)
    grid = _grid(s, total, box=box, gx=gx, gy=gy, cols=days) if month else _grid(s, total, box=box, gx=gx, gy=gy, rows=days)

    def span_w(n: int) -> int:
        return n * box + (n - 1) * gx

    brackets = (f'<div class="gw-brk" style="width:{span_w(weeks)}px">'
                f'<div class="gw-bk short" id="{s}-bs" style="width:{span_w(short)}px"><span>{_e(d.get("short_label", ""))}</span></div>'
                f'<div class="gw-bk long" id="{s}-bl" style="width:{span_w(weeks)}px"><span>{_e(d.get("long_label", ""))}</span></div></div>')
    if month:
        brackets = ""
    cue_html = (f'<div class="gw-cuebox"><div class="gw-ph" id="{s}-cph">{_e(d.get("cue_ph", ""))}</div>'
                f'<div class="gw-cue gw-cue-to" id="{s}-cue">{_e(d.get("cue", ""))}</div></div>')
    act_html = (f'<div class="gw-actbox"><div class="gw-ph big" id="{s}-aph">{_e(d.get("action_ph", ""))}</div>'
                f'<div class="gw-act gw-cue-to" id="{s}-act">{_e(d.get("action", ""))}</div></div>')
    step_html = "".join(f'<div class="gw-step" id="{s}-st{i}"><div class="gw-snum">{i + 1}</div><div class="gw-stext">{_e(st.get("title", ""))}</div></div>'
                        for i, st in enumerate(steps))
    html = f"""
<div class="scene-inner gw-scene gw-plan">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    {_card(s, cue='', action='', body=grid + brackets, cue_html=cue_html, action_html=act_html)}
    <div class="gw-steps">{step_html}</div>
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-card",{{y:70,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power3.out"}},{t(0.15):.3f});')
    # only the first `short` weeks exist at first; the rest of the grid grows in when "zehn Wochen" is spoken
    out.tl += _swap_text(c, f"#{s}-aph", f"#{s}-act", action_at)
    out.tl += _swap_text(c, f"#{s}-cph", f"#{s}-cue", cue_at)
    events = [c.start, t(action_at), t(cue_at)]
    if month:   # a whole month of boxes; the first one may get its tick on a spoken word ("heute")
        out.tl.append(f'tl.fromTo("#{s}-grid .gw-box",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.25,stagger:0.012,ease:"power2.out"}},{t(0.4):.3f});')
        if d.get("tick_at") is not None:
            tk = _rel(c, d.get("tick_at"), 0.0)
            out.tl.append(f'tl.fromTo("#{s}-x0",{{boxShadow:"0 0 0 0px rgba(229,180,90,0)"}},{{boxShadow:"0 0 0 7px {c.pal["accent"]}",duration:0.3}},{t(tk - 0.3):.3f});')
            out.tl.append(f'tl.fromTo("#{s}-x0 .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2.4)"}},{t(tk):.3f});')
            events.append(t(tk))
    else:       # only the first `short` weeks exist at first; the rest of the grid grows in when "zehn Wochen" is spoken
        first = ",".join(f"#{s}-x{i}" for i in range(short * days))
        rest = ",".join(f"#{s}-x{i}" for i in range(short * days, total))
        out.tl.append(f'tl.fromTo("{first}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.25,stagger:0.01,ease:"power2.out"}},{t(0.4):.3f});')
        out.tl.append(f'tl.fromTo("{rest}",{{opacity:0,scale:0.6}},{{opacity:0.22,scale:0.86,duration:0.25,stagger:0.006,ease:"power2.out"}},{t(0.6):.3f});')
        out.tl.append(f'tl.to("{rest}",{{opacity:1,scale:1,duration:0.22,stagger:0.012,ease:"back.out(1.8)"}},{t(grow_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-bl",{{opacity:0,scaleX:0.2,transformOrigin:"0% 50%"}},{{opacity:1,scaleX:1,duration:0.7,ease:"power2.out"}},{t(grow_at + 0.2):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-bs",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{t(short_at):.3f});')
        events += [t(grow_at), t(short_at)]
    for i, st in enumerate(steps):
        at = _rel(c, st.get("at"), 0.5 + 3 * i)
        out.tl.append(f'tl.fromTo("#{s}-st{i}",{{opacity:0.25}},{{opacity:1,duration:0.35,ease:"power3.out"}},{t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-st{i} .gw-snum",{{scale:0.5}},{{scale:1,duration:0.35,ease:"back.out(2)"}},{t(at + 0.05):.3f});')
        events.append(t(at))
    out.events = events
    out.problems = _limits("plan", [("headline", d.get("headline", "")), ("cue", d.get("cue", "")), ("action", d.get("action", "")),
                                    ("cue_ph", d.get("cue_ph", "")), ("action_ph", d.get("action_ph", "")),
                                    ("short_label", d.get("short_label", "")), ("long_label", d.get("long_label", ""))]
                           + [("step", st.get("title", "")) for st in steps])
    return out


# --- 6. close: tracker_close ------------------------------------------------------------------------

def take_tracker_close(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    weeks, days = int(d.get("weeks", 10)), int(d.get("days", 7))
    total = weeks * days
    month = d.get("layout") == "month"
    box, gx, gy = (66, 14, 10) if month else (44, 24, 6)
    card_at = _rel(c, d.get("card_at"), 0.1)
    tick_at = _rel(c, d.get("tick_at"), 0.9)
    chip_at = _rel(c, d.get("chip_at"), tick_at + 0.8)
    name_at = min(_rel(c, d.get("name_at"), chip_at + 0.6), max(0.0, c.duration - 4.0))   # brand readable >= 4 s
    mark_at = _rel(c, d.get("mark_at"), name_at + 1.2)
    grid = (_grid(s, total, box=box, gx=gx, gy=gy, cols=days) if month
            else _grid(s, total, box=box, gx=gx, gy=gy, rows=days) + _weeks(s, weeks, box, gx))
    html = f"""
<div class="scene-inner take gw-scene gw-close">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    {_card(s, cue=d.get('cue', ''), action=d.get('action', ''), body=grid, foot=_foot(s, d.get('counter_label', 'Tag')))}
    {f'<div class="gw-chip" id="{s}-chip">{_e(d["chip"])}</div>' if d.get('chip') else ''}
    <div class="gw-sign" id="{s}-sign"><div class="gw-name"><span class="gw-nmark" id="{s}-nm"></span>{_e(d.get('name', 'Gritwerk'))}</div>
      {f'<div class="gw-claim">{_e(d["claim"])}</div>' if d.get('claim') else ''}
      {f'<div class="gw-disc">{_e(d["disclaimer"])}</div>' if d.get('disclaimer') else ''}</div>
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -6))
    out.tl.append(f'tl.fromTo("#{s}-card",{{y:70,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power3.out"}},{t(card_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-x0",{{boxShadow:"0 0 0 0px rgba(229,180,90,0)"}},{{boxShadow:"0 0 0 7px {c.pal["accent"]}",duration:0.3}},{t(max(0.3, tick_at - 0.5)):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-x0 .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2.4)"}},{t(tick_at):.3f});')
    if not month:
        out.tl.append(f'tl.to("#{s}-wk0",{{color:"{c.pal.get("paper_ink", "#1B1712")}",duration:0.2}},{t(tick_at):.3f});')
    spans, ctl = _counter(c, [1], [t(tick_at)])
    _put_counter(out, s, spans)
    out.tl += ctl
    if d.get("chip"):
        out.tl.append(f'tl.fromTo("#{s}-chip",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{t(chip_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-x1",{{borderColor:"rgba(27,23,18,0.16)"}},{{borderColor:"{c.pal["accent"]}",duration:0.35,yoyo:true,repeat:3}},{t(chip_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-sign",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(name_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-nm",{{scale:0.4,rotation:-20}},{{scale:1,rotation:0,duration:0.35,ease:"back.out(2.4)"}},{t(mark_at):.3f});')
    out.events = [c.start, t(tick_at), t(chip_at), t(name_at), t(mark_at)]
    out.problems = _limits("tracker_close", [("headline", d.get("headline", "")), ("cue", d.get("cue", "")), ("action", d.get("action", "")),
                                             ("chip", d.get("chip", "")), ("name", d.get("name", "")), ("claim", d.get("claim", "")),
                                             ("disclaimer", d.get("disclaimer", ""))])
    return out


# --- 7. generic: study card (paper index card with ticked fact rows) --------------------------------

def exp_paper(c: SceneCtx, d: dict) -> SceneOut:
    """One study as a paper card: chip (design), short citation, the finding in one sentence, up to three
    fact rows whose day box gets ticked when the row is spoken, and an optional big number."""
    s, t = c.sid, c.t
    card_at = _rel(c, d.get("card_at"), 0.1)
    claim_at = _rel(c, d.get("claim_at"), card_at + 0.6)
    rows = d.get("rows", [])[:3]
    stat = d.get("stat") or {}
    rows_html = "".join(
        f'<div class="gw-prow" id="{s}-pr{i}"><div class="gw-box pbox" id="{s}-pb{i}"><div class="gw-fill"></div></div>'
        f'<span class="gw-pk">{_e(r.get("k", ""))}</span><span class="gw-pv">{_e(r.get("v", ""))}</span></div>' for i, r in enumerate(rows))
    stat_html = ""
    if stat:
        stat_html = (f'<div class="gw-pstat {stat.get("tone", "accent")}" id="{s}-ps"><div class="gw-psv">{_e(stat.get("value", ""))}</div>'
                     f'<div class="gw-psl">{_e(stat.get("label", ""))}</div></div>')
    html = f"""
<div class="scene-inner gw-scene gw-paper">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="gw-card gw-pcard" id="{s}-card">
      <div class="gw-ptop"><span class="gw-ptag">{_e(d.get('tag', ''))}</span><span class="gw-pcite">{_e(d.get('cite', ''))}</span></div>
      <div class="gw-pclaim" id="{s}-claim">{_e(d.get('claim', ''))}</div>
      <div class="gw-prows">{rows_html}</div>
      {stat_html}
    </div>
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-card",{{y:80,opacity:0,rotation:-1.2}},{{y:0,opacity:1,rotation:0,duration:0.5,ease:"power3.out"}},{t(card_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-claim",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(claim_at):.3f});')
    events = [c.start, t(card_at), t(claim_at)]
    for i, r in enumerate(rows):
        at = _rel(c, r.get("at"), claim_at + 1.2 * (i + 1))
        out.tl.append(f'tl.fromTo("#{s}-pr{i}",{{opacity:0.18,x:-24}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}-pb{i} .gw-fill",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"back.out(2.4)"}},{t(at + 0.1):.3f});')
        events.append(t(at))
    if stat:
        at = _rel(c, stat.get("at"), claim_at + 4.0)
        out.tl.append(f'tl.fromTo("#{s}-ps",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)"}},{t(at):.3f});')
        events.append(t(at))
    out.events = events
    out.problems = _limits("paper", [("headline", d.get("headline", "")), ("tag", d.get("tag", "")), ("cite", d.get("cite", "")),
                                     ("claim", d.get("claim", "")), ("stat_value", stat.get("value", "")), ("stat_label", stat.get("label", ""))]
                           + [("row_k", r.get("k", "")) for r in rows] + [("row_v", r.get("v", "")) for r in rows])
    return out


# --- 8. generic: two studies, one after the other ---------------------------------------------------

def cmp_versus(c: SceneCtx, d: dict) -> SceneOut:
    """Two study cards stacked (e.g. the original and the replication), each with a big value, then a verdict line."""
    s, t = c.sid, c.t
    cards = d.get("cards", [])[:2]
    parts, tl, events = [], [], [c.start]
    for i, cd in enumerate(cards):
        tone = cd.get("tone", "muted")
        parts.append(f'<div class="gw-vcard {tone}" id="{s}-v{i}"><div class="gw-vl"><div class="gw-ptop"><span class="gw-ptag">{_e(cd.get("tag", ""))}</span>'
                     f'<span class="gw-pcite">{_e(cd.get("cite", ""))}</span></div><div class="gw-vline">{_e(cd.get("line", ""))}</div></div>'
                     + (f'<div class="gw-vval" id="{s}-vv{i}">{_e(cd["value"])}</div>' if cd.get("value") else "") + '</div>')
        if i == 0 and d.get("link"):
            parts.append(f'<div class="gw-vlink" id="{s}-lk"><i></i><span>{_e(d["link"])}</span><i></i></div>')
        at = _rel(c, cd.get("at"), 0.3 + 3 * i)
        tl.append(f'tl.fromTo("#{s}-v{i}",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{t(at):.3f});')
        events.append(t(at))
        if cd.get("value"):
            v_at = _rel(c, cd.get("value_at"), at + 0.6)
            tl.append(f'tl.fromTo("#{s}-vv{i}",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.32,ease:"power4.in"}},{t(v_at):.3f});')
            events.append(t(v_at))
    if d.get("link") and len(cards) > 1:
        tl.append(f'tl.fromTo("#{s}-lk",{{opacity:0}},{{opacity:1,duration:0.3}},{t(_rel(c, cards[1].get("at"), 3.3) - 0.2):.3f});')
    verdict = d.get("verdict", "")
    if verdict:
        v_at = _rel(c, d.get("verdict_at"), 6.0)
        tl.append(f'tl.fromTo("#{s}-vd",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(v_at):.3f});')
        events.append(t(v_at))
    html = f"""
<div class="scene-inner gw-scene gw-versus">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    {''.join(parts)}
    {f'<div class="gw-snote" id="{s}-vd">{_e(verdict)}</div>' if verdict else ''}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl += tl
    out.events = events
    out.problems = _limits("versus", [("headline", d.get("headline", "")), ("verdict", verdict), ("link", d.get("link", ""))]
                           + [(k, cd.get(k, "")) for cd in cards for k in ("tag", "cite", "line", "value")])
    return out


# --- 9. generic: bars for numbers that stand in the sources -------------------------------------------

def flow_bars(c: SceneCtx, d: dict) -> SceneOut:
    """Up to five horizontal bars (values from the sources only), each growing on its spoken word."""
    s, t = c.sid, c.t
    bars = d.get("bars", [])[:5]
    scale = float(d.get("scale_max", max([float(b.get("value", 0)) for b in bars] + [1.0])))
    rows, tl, events = [], [], [c.start]
    for i, b in enumerate(bars):
        w = max(0.0, min(1.0, float(b.get("value", 0)) / scale))
        rows.append(f'<div class="gw-brow" id="{s}-br{i}"><div class="gw-blab">{_e(b.get("label", ""))}</div>'
                    f'<div class="gw-btrack"><div class="gw-bfill {b.get("tone", "accent")}" id="{s}-bf{i}" style="width:{100 * w:.2f}%"></div></div>'
                    f'<div class="gw-bval" id="{s}-bv{i}">{_e(b.get("text", ""))}</div></div>')
        at = _rel(c, b.get("at"), 0.8 + 1.2 * i)
        tl.append(f'tl.fromTo("#{s}-br{i}",{{opacity:0.15}},{{opacity:1,duration:0.3}},{t(at):.3f});')
        tl.append(f'tl.fromTo("#{s}-bf{i}",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.out"}},{t(at):.3f});')
        tl.append(f'tl.fromTo("#{s}-bv{i}",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:0.3}},{t(at + 0.5):.3f});')
        events.append(t(at))
    note = d.get("note", "")
    if note:
        n_at = _rel(c, d.get("note_at"), 8.0)
        tl.append(f'tl.fromTo("#{s}-bn",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.35}},{t(n_at):.3f});')
        events.append(t(n_at))
    html = f"""
<div class="scene-inner gw-scene gw-bars">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="gw-barbox" id="{s}-bb">
      <div class="gw-bcap">{_e(d.get('caption', ''))}</div>
      {''.join(rows)}
    </div>
    {f'<div class="gw-snote" id="{s}-bn">{_e(note)}</div>' if note else ''}
  </div>
</div>"""
    out = SceneOut(html=html)
    out.tl += _enter(c)
    out.tl.append(_push(c, 1.03, -8))
    out.tl.append(_h2_in(c))
    out.tl.append(f'tl.fromTo("#{s}-bb",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(0.1):.3f});')
    out.tl += tl
    out.events = events
    out.problems = _limits("bars", [("headline", d.get("headline", "")), ("caption", d.get("caption", "")), ("note", note)]
                           + [(k, b.get(k, "")) for b in bars for k in ("label", "text")])
    return out


def _with_plate(fn):
    """data.plate = true (beats entered by an iris): a dark plate behind the scene, so the opening circle shows
    only the new scene; it gives way to the room after the iris."""
    def scene(c: SceneCtx, d: dict) -> SceneOut:
        out = fn(c, d)
        if d.get("plate"):
            out.html = f'<div class="gw-plate" id="{c.sid}-plate"></div>' + out.html
            out.tl.append(f'tl.to("#{c.sid}-plate",{{opacity:0,duration:0.4,ease:"power1.inOut"}},{c.t(0.75):.3f});')
        return out
    scene.__doc__ = fn.__doc__
    return scene


TEMPLATES = {k: _with_plate(f) for k, f in {
    "gritwerk_tracker": hook_tracker,
    "gritwerk_study": exp_study,
    "gritwerk_curve": flow_curve,
    "gritwerk_streaks": cmp_streaks,
    "gritwerk_plan": take_plan,
    "gritwerk_close": take_tracker_close,
    "gritwerk_paper": exp_paper,
    "gritwerk_versus": cmp_versus,
    "gritwerk_bars": flow_bars,
}.items()}
HOOK_SCENE_TYPES = ["gritwerk_tracker", "cinematic_hook"]
# flat limits on top-level string fields (fn.render.brand_scenes.text_limits); nested texts are checked in the templates
LIMITS = {
    "gritwerk_tracker": dict(_LIM["tracker"]),
    "gritwerk_study": dict(_LIM["study"]),
    "gritwerk_curve": {"headline": 30, "y_label": 26, "x_label": 12},
    "gritwerk_streaks": {"headline": 30, "note": 52, "chip": 26, "chip_to": 26},
    "gritwerk_plan": {k: v for k, v in _LIM["plan"].items() if k != "step"},
    "gritwerk_close": dict(_LIM["tracker_close"]),
    "gritwerk_paper": {k: v for k, v in _LIM["paper"].items() if not k.startswith(("row_", "stat_"))},
    "gritwerk_versus": {"headline": 30, "verdict": 56, "link": 24},
    "gritwerk_bars": {"headline": 30, "caption": 44, "note": 56},
}


# --- brand layer: depth under all scenes ------------------------------------------------------------

def _svg_uri(svg: str) -> str:
    return "data:image/svg+xml;utf8," + svg.replace("#", "%23").replace('"', "'").replace("\n", "")


def LAYER(plan, brand, project_dir, captions):  # noqa: N802
    """Warm desk under lamp light (code only, no images): a big calendar of day boxes lies in perspective as the
    desk, defocused paper cards at the edges, dust drifting in the light cone, a calm veil over the content zone.
    The camera moves one step per beat (pan, push, slight tilt); the calendar slides by a few day boxes per beat
    (parallax), so every scene sits in a slightly different place of the same room."""
    pal = brand.palette
    acc, bg = pal["accent"], pal["bg"]
    beats = [b for b in plan.beats if b.start is not None]
    total = max((b.start + b.duration for b in beats), default=60.0)
    rnd = random.Random(66)
    # calendar tile: 5 x 5 rounded day boxes, a few ticked (gold), the rest empty
    cells = []
    for r in range(5):
        for k in range(5):
            filled = (r * 5 + k) % 7 in (0, 3, 5)
            cells.append(f'<rect x="{k * 120 + 14}" y="{r * 120 + 14}" width="92" height="92" rx="16" '
                         + (f'fill="{acc}" fill-opacity="0.22" stroke="{acc}" stroke-opacity="0.35" stroke-width="3"/>' if filled
                            else f'fill="none" stroke="{acc}" stroke-opacity="0.26" stroke-width="3"/>'))
    tile = _svg_uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">{"".join(cells)}</svg>')
    paper_tile = _svg_uri('<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120">'
                          '<rect x="10" y="10" width="100" height="100" rx="14" fill="none" stroke="#1B1712" stroke-opacity="0.35" stroke-width="5"/></svg>')
    wood = _svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='700' height='700'><filter id='w'>"
                    "<feTurbulence type='fractalNoise' baseFrequency='0.004 0.09' numOctaves='3' seed='7' stitchTiles='stitch'/>"
                    "<feColorMatrix type='matrix' values='0 0 0 0 0.9  0 0 0 0 0.7  0 0 0 0 0.4  0 0 0 0.9 0'/></filter>"
                    "<rect width='100%' height='100%' filter='url(#w)'/></svg>")
    motes, mtl = [], []
    for i in range(22):
        x, y = rnd.uniform(-40, 1100), rnd.uniform(80, 1900)
        size = rnd.choice([6, 8, 10, 14, 18, 26])
        op = rnd.uniform(0.18, 0.55) if size < 18 else rnd.uniform(0.10, 0.22)
        motes.append(f'<i class="gwm" id="gwm{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;opacity:{op:.2f}"></i>')
        dy, dx = -rnd.uniform(140, 380), rnd.uniform(-60, 60)
        mtl.append(f'T.fromTo("#gwm{i}",{{x:0,y:0}},{{x:{dx:.0f},y:{dy:.0f},duration:{total:.2f},ease:"none"}},0);')
    # one camera position per beat (x, y, scale, rotation) and a calendar step per beat (parallax)
    cams = [(0, 0, 1.00, 0.0), (-46, -26, 1.05, -0.6), (38, -50, 1.08, 0.5), (-30, -16, 1.06, -0.4), (44, -40, 1.09, 0.6),
            (0, -60, 1.11, 0.0), (-20, -30, 1.07, -0.3)]
    ctl = ['T.set("#gwbg .gwbg-cam",{x:0,y:0,scale:1,rotation:0},0);', 'T.set("#gwbg .gwbg-cal",{y:0,x:0},0);']
    for i, b in enumerate(beats):
        x, y, sc, rot = cams[min(i, len(cams) - 1)]
        if i:
            ctl.append(f'T.to("#gwbg .gwbg-cam",{{x:{x},y:{y},scale:{sc},rotation:{rot},duration:1.6,ease:"power2.inOut"}},{b.start:.3f});')
            ctl.append(f'T.to("#gwbg .gwbg-cal",{{y:{i * 240},x:{(-1) ** i * 60},duration:1.8,ease:"power2.inOut"}},{b.start:.3f});')
            ctl.append(f'T.to("#gwbg .gwbg-ghosts",{{x:{(-1) ** (i + 1) * 40},y:{-i * 18},duration:1.8,ease:"power2.inOut"}},{b.start:.3f});')
        # a slow drift inside the beat keeps the room alive between the steps
        ctl.append(f'T.fromTo("#gwbg .gwbg-drift",{{x:0,y:0}},{{x:{(-1) ** i * 24},y:-18,duration:{max(1.0, b.duration):.2f},ease:"sine.inOut"}},{b.start:.3f});')
    breath = max(1, int(total / 5.0))
    ctl.append(f'T.fromTo("#gwbg .gwbg-lamp",{{opacity:0.82}},{{opacity:1,duration:{total / breath:.3f},repeat:{breath - 1},yoyo:true,ease:"sine.inOut"}},0);')
    ctl.append(f'T.fromTo("#gwbg .gwbg-rays",{{rotation:-3}},{{rotation:3,duration:{total:.2f},ease:"sine.inOut"}},0);')
    css = f"""<style>
#gwbg{{position:absolute;inset:0;z-index:1;overflow:hidden;pointer-events:none;background:{bg};}}
#gwbg .gwbg-cam{{position:absolute;inset:-140px;transform-origin:42% 30%;will-change:transform;}}
#gwbg .gwbg-drift{{position:absolute;inset:0;}}
.gwbg-base{{position:absolute;inset:0;background:linear-gradient(180deg,#1A1611 0%,#14120F 38%,#100E0C 100%);}}
.gwbg-wood{{position:absolute;inset:0;opacity:0.10;mix-blend-mode:screen;background-image:url("{wood}");background-size:700px 700px;}}
.gwbg-desk{{position:absolute;left:-500px;right:-500px;top:1040px;height:1500px;perspective:900px;perspective-origin:50% 0%;}}
.gwbg-plane{{position:absolute;inset:0;transform:rotateX(64deg);transform-origin:50% 0%;
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,rgba(0,0,0,0.55) 22%,#000 60%);mask-image:linear-gradient(180deg,transparent 0%,rgba(0,0,0,0.55) 22%,#000 60%);}}
.gwbg-cal{{position:absolute;left:0;right:0;top:-1800px;height:5200px;background-image:url("{tile}");background-size:600px 600px;background-position:50% 0;opacity:0.9;}}
.gwbg-ghosts{{position:absolute;inset:0;}}
.gwbg-ghost{{position:absolute;border-radius:18px;background-color:#F4F0E8;background-image:url("{paper_tile}");background-size:96px 96px;background-position:28px 90px;
  opacity:0.075;filter:blur(7px);box-shadow:0 40px 80px rgba(0,0,0,0.6);}}
.gwbg-lamp{{position:absolute;inset:0;background:
  radial-gradient(ellipse 900px 760px at 18% 6%,rgba(242,196,110,0.30) 0%,rgba(229,180,90,0.12) 38%,transparent 72%),
  radial-gradient(ellipse 760px 900px at 92% 88%,rgba(232,135,58,0.10) 0%,transparent 70%);}}
.gwbg-rays{{position:absolute;left:-520px;top:-520px;width:2200px;height:2200px;transform-origin:520px 520px;
  background:repeating-conic-gradient(from 96deg at 520px 520px,rgba(242,196,110,0.055) 0deg 3.5deg,transparent 3.5deg 9deg);
  -webkit-mask-image:radial-gradient(circle at 520px 520px,#000 0%,rgba(0,0,0,0.5) 40%,transparent 70%);mask-image:radial-gradient(circle at 520px 520px,#000 0%,rgba(0,0,0,0.5) 40%,transparent 70%);}}
.gwm{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(250,226,172,0.95) 0%,rgba(229,180,90,0.35) 45%,rgba(229,180,90,0) 72%);}}
.gwbg-veil{{position:absolute;inset:0;background:
  radial-gradient(ellipse 600px 520px at 50% 700px,rgba(16,14,12,0.50) 0%,rgba(16,14,12,0.22) 55%,transparent 80%),
  radial-gradient(ellipse 85% 62% at 50% 46%,transparent 52%,rgba(7,6,5,0.78) 100%);}}
</style>"""
    ghosts = ('<div class="gwbg-ghost" style="left:820px;top:300px;width:470px;height:330px;transform:rotate(11deg)"></div>'
              '<div class="gwbg-ghost" style="left:-210px;top:820px;width:420px;height:300px;transform:rotate(-9deg)"></div>'
              '<div class="gwbg-ghost" style="left:760px;top:1560px;width:520px;height:360px;transform:rotate(-6deg)"></div>'
              '<div class="gwbg-ghost" style="left:-120px;top:120px;width:300px;height:220px;transform:rotate(-14deg);opacity:0.05"></div>')
    under = f"""<div id="gwbg"><div class="gwbg-cam"><div class="gwbg-drift">
  <div class="gwbg-base"></div><div class="gwbg-wood"></div>
  <div class="gwbg-desk"><div class="gwbg-plane"><div class="gwbg-cal"></div></div></div>
  <div class="gwbg-ghosts">{ghosts}</div>
  <div class="gwbg-rays"></div><div class="gwbg-lamp"></div>
  {''.join(motes)}
</div></div><div class="gwbg-veil"></div></div>"""
    body_end = ("<script>(function(){var T=window.__timelines&&window.__timelines.main;if(!T)return;\n"
                + "\n".join(ctl + mtl) + "\nT.seek(0);})();</script>")
    return {"head_html": css, "under_scenes_html": under, "body_end_html": body_end,
            "events": [round(b.start, 3) for b in beats[1:]]}


def MANIFEST_EXTRA(plan):  # noqa: N802
    return {"brand_layer": {"name": "Gritwerk desk (lamp light, calendar in perspective, paper cards, dust)",
                            "source": "brands/motivation/scenes.py LAYER, CSS/SVG only, no images, no third-party rights"}}


# --- CSS --------------------------------------------------------------------------------------------

def gritwerk_css(pal: dict, display: str, display_w: int, mono: str, flat: bool = False) -> str:
    acc, text, surf, muted, bg = pal["accent"], pal["text"], pal["surface"], pal["muted"], pal["bg"]
    paper, ink = pal.get("paper", "#F4F0E8"), pal.get("paper_ink", "#1B1712")
    pmuted, empty, miss = pal.get("paper_muted", "#7D746A"), pal.get("box_empty", "#DDD5C8"), pal.get("signal_amber", "#E8873A")  # missed day = open (amber), not a risk
    hair = pal.get("hairline", "rgba(244,240,232,0.14)")
    on_acc = pal.get("on_accent", bg)
    shadow_paper = "0 2px 2px rgba(0,0,0,0.25),0 14px 30px rgba(0,0,0,0.35),0 46px 90px rgba(0,0,0,0.45)"
    grain = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'>"
             "<feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter>"
             "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
    tick = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><path d='M18 33 L28 43 L47 22' fill='none' "
            "stroke='%2317130D' stroke-width='7' stroke-linecap='round' stroke-linejoin='round'/></svg>\")")
    return f"""
/* Gritwerk brand layer (brands/motivation/scenes.py) */
#root::after{{content:"";position:absolute;inset:0;z-index:35;pointer-events:none;opacity:0.07;mix-blend-mode:overlay;background-image:url("{grain}");background-size:240px 240px;}}
.h2,.question,.statement{{font-variation-settings:"SOFT" 60,"opsz" 96;}}
.gw-scene .h2{{font-size:70px;line-height:1.06;letter-spacing:-0.02em;}}
.question{{font-weight:700;}}
#status .st-icon{{font-size:0;width:26px;height:26px;border-radius:7px;background:{acc} {tick} center/80% no-repeat;display:inline-block;}}
#status{{background:color-mix(in srgb,{surf} 88%,transparent);box-shadow:0 18px 40px rgba(0,0,0,0.45);}}
.st-accent{{color:{acc};}}
.gw-card{{position:relative;width:{CARD_W}px;margin:0 auto;background:{paper};color:{ink};border-radius:16px;padding:26px {PAD_X}px 22px;
  box-shadow:{shadow_paper};text-align:left;}}
.gw-card::before{{content:"";position:absolute;inset:0;border-radius:16px;pointer-events:none;
  background:linear-gradient(160deg,rgba(255,255,255,0.55) 0%,rgba(255,255,255,0) 38%),radial-gradient(ellipse at 100% 100%,rgba(125,116,106,0.16),transparent 60%);}}
.gw-head{{position:relative;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:18px;}}
.gw-headl{{display:flex;flex-direction:column;gap:2px;min-width:0;}}
.gw-cue{{font-family:'FN {mono}';font-size:28px;font-weight:600;color:{pmuted};letter-spacing:0.02em;white-space:nowrap;
  background-image:linear-gradient({acc},{acc});background-repeat:no-repeat;background-position:0 100%;background-size:0% 6px;padding-bottom:4px;}}
.gw-act{{font-family:'FN {display}';font-weight:700;font-size:50px;line-height:1.1;color:{ink};font-variation-settings:"SOFT" 80,"opsz" 72;white-space:nowrap;}}
.gw-cuebox,.gw-actbox{{position:relative;}}
.gw-cue-to{{position:absolute;left:0;top:0;opacity:0;}}
.gw-ph{{display:inline-block;font-family:'FN {mono}';font-size:28px;font-weight:600;color:{pmuted};border:3px dashed rgba(27,23,18,0.28);border-radius:12px;padding:2px 16px;margin-bottom:6px;}}
.gw-ph.big{{font-size:40px;padding:4px 20px;}}
.gw-grid{{display:grid;justify-content:center;}}
.gw-box{{position:relative;border:3px solid rgba(27,23,18,0.16);border-radius:9px;background:{empty};overflow:hidden;}}
.gw-box .gw-fill{{position:absolute;inset:-1px;background:{acc};border-radius:6px;opacity:0;
  background-image:{tick};background-size:72% 72%;background-position:center;background-repeat:no-repeat;}}
.gw-box.miss{{background:transparent;border-style:dashed;}}
.gw-weeks{{display:grid;justify-content:center;margin-top:8px;font-family:'FN {mono}';font-size:26px;font-weight:600;color:rgba(27,23,18,0.38);text-align:center;}}
.gw-foot{{position:relative;display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:14px;}}
.gw-footl{{display:flex;align-items:baseline;gap:14px;font-family:'FN {mono}';}}
.gw-clabel{{font-size:30px;font-weight:600;color:{pmuted};}}
.gw-count{{position:relative;display:inline-block;min-width:110px;height:58px;}}
.gw-n{{position:absolute;left:0;bottom:-6px;font-family:'FN {display}';font-weight:700;font-size:58px;line-height:1;color:{ink};font-variant-numeric:tabular-nums;}}
.gw-goal{{font-family:'FN {display}';font-weight:700;font-size:40px;color:{ink};background:linear-gradient(transparent 58%,color-mix(in srgb,{acc} 70%,transparent) 58%);padding:0 6px;}}
.gw-study .gw-head{{align-items:flex-start;}}
.gw-pchip{{flex:none;font-family:'FN {display}';font-weight:700;font-size:38px;color:{ink};border:3px solid {ink};border-radius:999px;padding:6px 24px;margin-bottom:6px;}}
.gw-plate{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 42%,#1D1913 0%,#121010 65%,#0A0908 100%);}}
.gw-scene .stage{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;}}
/* 1 hook */
.gw-hook{{gap:18px;}}
.gw-hook .question{{font-size:82px;line-height:1.02;margin-top:6px;}}
.gw-stamp{{position:absolute;right:-18px;top:210px;font-family:'FN {display}';font-weight:800;font-size:60px;color:{ink};background:{miss};
  border-radius:14px;padding:8px 28px;box-shadow:0 14px 34px rgba(0,0,0,0.4);transform:rotate(-6deg);}}
/* 2 study */
.gw-scale{{display:flex;flex-direction:column;gap:8px;width:{SCALE_W}px;}}
.gw-slabel{{font-size:30px;font-weight:700;color:{ink};}}
.gw-strack{{position:relative;height:16px;border-radius:8px;background:rgba(27,23,18,0.12);}}
.gw-sfill{{position:absolute;left:0;top:0;width:100%;height:16px;border-radius:8px;background:{acc};transform-origin:0 50%;transform:scaleX(0.12);}}
.gw-sdot{{position:absolute;left:0;top:50%;transform:translateX(46px);width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;background:{ink};border:5px solid {acc};}}
.gw-sends{{display:flex;justify-content:space-between;font-family:'FN {mono}';font-size:26px;font-weight:600;color:{pmuted};}}
/* 3 curve */
.gw-chartbox{{position:relative;width:{CARD_W}px;height:470px;background:color-mix(in srgb,{surf} 82%,transparent);border:2px solid {hair};border-radius:18px;
  box-shadow:0 24px 60px rgba(0,0,0,0.4);}}
.gw-chart{{position:absolute;left:0;top:0;display:block;overflow:visible;}}
.gw-axis{{stroke:{muted};stroke-width:3;opacity:0.6;}}
.gw-alabel{{fill:{muted};font-family:'FN {mono}';font-size:28px;font-weight:600;}}
.gw-path{{fill:none;stroke:{acc};stroke-width:10;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1500;stroke-dashoffset:1500;}}
.gw-pen{{position:absolute;left:-15px;top:-15px;width:30px;height:30px;border-radius:50%;background:{paper};border:6px solid {acc};box-shadow:0 0 0 8px color-mix(in srgb,{acc} 25%,transparent);}}
.gw-band{{fill:color-mix(in srgb,{acc} 13%,transparent);stroke:color-mix(in srgb,{acc} 45%,transparent);stroke-width:2;stroke-dasharray:8 8;}}
.gw-bandl{{fill:{acc};font-family:'FN {mono}';font-size:28px;font-weight:600;}}
.gw-mline{{stroke-width:3;stroke-dasharray:10 10;}}
.gw-mline.accent{{stroke:{acc};}} .gw-mline.muted{{stroke:{muted};}}
.gw-mdot.accent{{fill:{acc};}} .gw-mdot.muted{{fill:{muted};}}
.gw-tag{{position:absolute;display:flex;align-items:center;gap:12px;white-space:nowrap;background:{paper};color:{ink};border-radius:12px;padding:8px 18px;
  font-family:'FN {display}';font-weight:700;font-size:36px;box-shadow:0 10px 26px rgba(0,0,0,0.45);}}
.gw-tag i{{display:inline-block;width:24px;height:24px;border-radius:6px;border:3px solid rgba(27,23,18,0.25);background:{empty};}}
.gw-tag.accent i{{background:{acc} {tick} center/80% no-repeat;border-color:{acc};}}
.gw-tag.accent{{box-shadow:0 0 0 4px {acc},0 10px 26px rgba(0,0,0,0.45);}}
.gw-range{{width:{CARD_W}px;background:color-mix(in srgb,{surf} 88%,transparent);border:2px solid {hair};border-radius:18px;padding:20px 34px 18px;text-align:left;box-shadow:0 24px 60px rgba(0,0,0,0.4);}}
.gw-rlabel{{font-size:34px;font-weight:600;color:{text};margin-bottom:18px;}}
.gw-rtrack{{position:relative;height:18px;border-radius:9px;background:color-mix(in srgb,{text} 12%,transparent);}}
.gw-rseg{{position:absolute;top:0;height:18px;border-radius:9px;background:{acc};transform-origin:left center;}}
.gw-rseg.dashed{{background:repeating-linear-gradient(90deg,{acc} 0 16px,transparent 16px 26px);border-radius:0 9px 9px 0;opacity:0.85;}}
.gw-rtick{{position:absolute;top:-10px;width:6px;height:38px;margin-left:-3px;border-radius:3px;background:{text};}}
.gw-rends{{position:relative;height:32px;margin-top:8px;font-family:'FN {mono}';font-size:26px;font-weight:600;color:{muted};}}
.gw-rends span{{position:absolute;transform:translateX(-50%);}}
.gw-rnote{{margin-top:4px;font-family:'FN {mono}';font-size:26px;font-weight:600;color:{acc};text-align:right;}}
/* 4 streaks */
.gw-scard{{position:relative;width:{CARD_W}px;background:{paper};color:{ink};border-radius:16px;padding:30px {PAD_X}px 34px;display:flex;flex-direction:column;gap:30px;
  box-shadow:{shadow_paper};text-align:left;}}
.gw-stitle{{font-family:'FN {display}';font-weight:700;font-size:46px;margin-bottom:14px;}}
.gw-strip{{display:grid;}}
.gw-box.sm{{border-radius:11px;border-width:3px;}}
.gw-box.miss{{border-color:{miss};}}
.gw-snote{{width:{CARD_W}px;font-size:44px;font-weight:600;line-height:1.22;color:{text};text-align:left;border-left:6px solid {acc};padding:6px 0 6px 28px;}}
.gw-chipbox{{position:relative;width:{CARD_W}px;height:66px;}}
.gw-chip2{{position:absolute;left:0;top:0;font-size:34px;font-weight:700;color:{on_acc};background:{acc};border-radius:999px;padding:12px 30px;white-space:nowrap;}}
.gw-chip2.muted{{background:transparent;color:{text};border:3px solid color-mix(in srgb,{text} 40%,transparent);}}
/* 5 plan */
.gw-brk{{position:relative;margin:12px auto 0;height:44px;}}
.gw-bk{{position:absolute;left:0;top:0;height:40px;border:3px solid;border-top:none;border-radius:0 0 12px 12px;}}
.gw-bk span{{position:absolute;left:50%;top:14px;transform:translateX(-50%);padding:0 12px;background:{paper};font-family:'FN {mono}';font-size:26px;font-weight:700;white-space:nowrap;}}
.gw-bk.long{{border-color:{acc};}} .gw-bk.long span{{color:#9A6F1E;left:auto;right:18px;transform:none;}}
.gw-bk.short{{border-color:rgba(27,23,18,0.35);height:22px;}} .gw-bk.short span{{color:{pmuted};top:4px;}}
.gw-steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;width:{CARD_W}px;}}
.gw-step{{display:flex;align-items:center;gap:14px;background:color-mix(in srgb,{surf} 90%,transparent);border:2px solid {hair};border-radius:18px;padding:16px 16px;min-height:112px;}}
.gw-snum{{flex:0 0 52px;width:52px;height:52px;border-radius:50%;background:{acc};color:{on_acc};font-family:'FN {display}';font-weight:800;font-size:32px;display:flex;align-items:center;justify-content:center;}}
.gw-stext{{font-size:30px;font-weight:700;line-height:1.15;color:{text};}}
/* 7 study card */
.gw-pcard{{padding:30px {PAD_X}px 30px;}}
.gw-ptop{{position:relative;display:flex;align-items:center;gap:18px;margin-bottom:16px;}}
.gw-ptag{{font-family:'FN {mono}';font-size:26px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:{ink};border:3px solid {ink};border-radius:999px;padding:4px 18px;white-space:nowrap;}}
.gw-pcite{{font-family:'FN {mono}';font-size:28px;font-weight:600;color:{pmuted};white-space:nowrap;}}
.gw-pclaim{{position:relative;font-family:'FN {display}';font-weight:700;font-size:46px;line-height:1.14;color:{ink};font-variation-settings:"SOFT" 80,"opsz" 72;margin-bottom:22px;}}
.gw-prows{{position:relative;display:flex;flex-direction:column;gap:14px;border-top:3px dashed rgba(27,23,18,0.18);padding-top:20px;}}
.gw-prow{{display:flex;align-items:center;gap:18px;}}
.gw-box.pbox{{flex:none;width:46px;height:46px;border-radius:10px;}}
.gw-pk{{flex:none;width:210px;font-family:'FN {mono}';font-size:27px;font-weight:600;color:{pmuted};}}
.gw-pv{{font-size:36px;font-weight:700;line-height:1.15;color:{ink};}}
.gw-pstat{{position:relative;display:flex;align-items:baseline;gap:22px;margin-top:22px;padding-top:18px;border-top:3px dashed rgba(27,23,18,0.18);}}
.gw-psv{{font-family:'FN {display}';font-weight:800;font-size:84px;line-height:1;color:{ink};background:linear-gradient(transparent 62%,color-mix(in srgb,{acc} 75%,transparent) 62%);padding:0 8px;white-space:nowrap;}}
.gw-pstat.amber .gw-psv{{background:linear-gradient(transparent 62%,color-mix(in srgb,{miss} 70%,transparent) 62%);}}
.gw-pstat.muted .gw-psv{{background:none;}}
.gw-psl{{font-family:'FN {mono}';font-size:28px;font-weight:600;line-height:1.25;color:{pmuted};}}
/* 8 two studies */
.gw-versus .stage{{gap:18px;}}
.gw-versus .gw-ptop{{margin-bottom:10px;}}
.gw-vcard{{position:relative;width:{CARD_W}px;min-height:230px;display:flex;align-items:center;justify-content:space-between;gap:24px;background:{paper};color:{ink};border-radius:16px;padding:26px {PAD_X}px;box-shadow:{shadow_paper};text-align:left;}}
.gw-vcard.accent{{box-shadow:0 0 0 5px {acc},{shadow_paper};}}
.gw-vcard.amber{{box-shadow:0 0 0 5px {miss},{shadow_paper};}}
.gw-vl{{min-width:0;}}
.gw-vline{{font-family:'FN {display}';font-weight:700;font-size:46px;line-height:1.14;color:{ink};}}
.gw-vval{{flex:none;font-family:'FN {display}';font-weight:800;font-size:80px;line-height:1;color:{ink};white-space:nowrap;}}
.gw-vlink{{display:flex;align-items:center;gap:16px;width:{CARD_W}px;font-family:'FN {mono}';font-size:28px;font-weight:600;color:{acc};}}
.gw-vlink i{{flex:1;height:3px;background:repeating-linear-gradient(90deg,{acc} 0 12px,transparent 12px 22px);}}
/* 9 bars */
.gw-barbox{{position:relative;width:{CARD_W}px;background:color-mix(in srgb,{surf} 86%,transparent);border:2px solid {hair};border-radius:18px;padding:28px 34px 30px;box-shadow:0 24px 60px rgba(0,0,0,0.4);display:flex;flex-direction:column;gap:24px;text-align:left;}}
.gw-bcap{{font-family:'FN {mono}';font-size:28px;font-weight:600;color:{muted};}}
.gw-brow{{display:flex;align-items:center;gap:20px;}}
.gw-blab{{flex:none;width:250px;font-size:34px;font-weight:700;color:{text};}}
.gw-btrack{{position:relative;flex:1;height:44px;border-radius:12px;background:color-mix(in srgb,{text} 10%,transparent);overflow:hidden;}}
.gw-bfill{{position:absolute;left:0;top:0;bottom:0;border-radius:12px;background:{acc};transform-origin:0 50%;}}
.gw-bfill.muted{{background:{muted};}} .gw-bfill.amber{{background:{miss};}}
.gw-bval{{flex:none;width:130px;text-align:right;font-family:'FN {display}';font-weight:700;font-size:44px;color:{text};}}
.gw-stag{{margin-left:18px;font-family:'FN {mono}';font-size:28px;font-weight:600;color:{pmuted};}}
/* 6 close */
.gw-close{{top:224px !important;height:1000px !important;}}   /* no head in the close: the card may start higher and end above the captions */
.gw-close .stage{{gap:22px;}}
.gw-chip{{font-size:36px;font-weight:700;color:{on_acc};background:{acc};border-radius:999px;padding:14px 34px;}}
.gw-sign{{display:flex;flex-direction:column;align-items:center;gap:4px;}}
.gw-name{{display:flex;align-items:center;gap:20px;font-family:'FN {display}';font-weight:700;font-size:76px;letter-spacing:-0.01em;color:{text};font-variation-settings:"SOFT" 60,"opsz" 120;}}
.gw-nmark{{display:inline-block;width:52px;height:52px;border-radius:12px;background:{acc} {tick} center/78% no-repeat;}}
.gw-claim{{font-family:'FN {display}';font-weight:600;font-size:38px;color:{acc};}}
.gw-disc{{font-size:26px;color:{muted};margin-top:6px;}}
"""


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat=False) -> str:
    return gritwerk_css(pal, display, display_w, mono, flat)


# --- Format "Laborbuch" (02.11.2026): a published experiment retold as a lab notebook page, scene types lb_*,
# see laborbuch/scenes.py. A plan with layout.format == "laborbuch" gets the notebook layer instead of the desk.
import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("gw_laborbuch_scenes", _Path(__file__).resolve().with_name("laborbuch") / "scenes.py")
_lb = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_lb)
TEMPLATES.update(_lb.TEMPLATES)
LIMITS.update(_lb.LIMITS)
HOOK_SCENE_TYPES += _lb.HOOK_SCENE_TYPES
_gw_css, _gw_layer, _gw_manifest = CSS, LAYER, MANIFEST_EXTRA


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat=False) -> str:  # noqa: F811
    return _gw_css(pal, display, display_w, body, mono, zone_top, zone_h, flat) + _lb.CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat)


def LAYER(plan, brand, project_dir, captions):  # noqa: N802,F811
    if (getattr(plan, "layout", None) or {}).get("format") == "laborbuch":
        return _lb.LAYER(plan, brand, project_dir, captions)
    return _gw_layer(plan, brand, project_dir, captions)


def MANIFEST_EXTRA(plan):  # noqa: N802,F811
    if (getattr(plan, "layout", None) or {}).get("format") == "laborbuch":
        return _lb.MANIFEST_EXTRA(plan)
    return _gw_manifest(plan)
