"""Gritwerk format "Laborbuch" (02.11.2026): scene types lb_* (brand module part, loaded from brands/motivation/scenes.py).

Format bible: OneDrive\\Business\\02 Marke\\Gritwerk\\Format-Bibel.md. Every video retells ONE published experiment as
a page in a lab notebook: the question, how it was set up (who, which conditions, how the groups were split), what
exactly was measured, what came out (the numbers of the paper, drawn as bars), the limits, the replication status
(stamp: haelt / gemischt / nicht bestaetigt / offen) and finally a small test the viewer can run with a clear
measuring rule ("Dein Versuch", n = 1). Nobody in the video ran the experiment: the format-wide LAYER carries the line
"Nacherzaehlt aus der Studie · nicht selbst durchgefuehrt" for the whole video. People appear only as
dots (one dot = one participant, or n participants as labelled), never as faces or figures.

The LAYER draws the warm dark room, the notebook page (grid paper, header "LABORBUCH · Versuch <no>" and the study)
and the protocol strip at the top: seven day boxes (the Gritwerk motif) that fill in gold step by step, with the
name of the current step (Frage, Aufbau, Messung, Ergebnis, Grenzen, Stand, Dein Versuch). Each scene after the first
opens with a page turn. Only HTML/SVG/CSS, moved by the GSAP timeline; no images, no AI pictures.

| scene type | step(s)       | data |
|------------|---------------|------|
| lb_hook    | Frage         | question, dots{n, label, at}, meta{text, at}, tease{text, at}, stamp{text, at}, cite |
| lb_setup   | Aufbau        | headline, sheets[{title, sub}], sheets_at, read{text, at}, arms[{icon, title, sub, at}], |
|            |               | groups{n, label, at, split[{label, sub, at}]}, cite |
| lb_measure | Messung       | headline, sheet_label, units{n, label, at}, rule{text, at}, sample{fill, text, at}, cite |
| lb_result  | Ergebnis      | headline, unit, series[{label, kind}], groups[{label, values, at}], turn{text, at, between}, |
|            |               | gap{text, group, at}, cite |
| lb_verdict | Grenzen,Stand | limits_title, limits[{text, at}], status{level, at, title}, evidence[{text, cite, at}], cite |
| lb_try     | Dein Versuch  | title, steps[{text, at}], rule{text, at}, caveat{text, at}, sign_at, claim, disclaimer |
| lb_replicate | Ergebnis    | headline, axis{min, max, label, zero_label, ticks}, rows[{label, sub, value, ci, value_text, kind, at}], |
|            |               | note{text, at}, cite (series "Haelt das?": original against its replications on one effect axis) |

Times: seconds from the beat start or "@Wort[#n][+0.3]" (start of that spoken word in the beat, SceneCtx.words).
An anchor that is not spoken is reported as a problem and the default time is used. Animated elements carry no CSS
transform (GSAP would fold it); they are placed with left/top. Every beat may set data.protocol (int or a list of
{step, at}) to override the default protocol step of its scene type.
"""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

# page geometry (1080 x 1920): the notebook page lies in the content zone, text stays inside x 132..948
PX, PY, PW, PH = 92, 300, 860, 900          # page box (right edge 952, bottom 1200; header text ends at x 912)
CL, CW = 132, 800                           # content left, content width (right edge 932: platform icons from x 940)
CT, CB = 384, 1130                          # content top (below the page head), content bottom (cite line below)
CITE_Y = 1146

INK, PMUTED, PAPER = "#1B1712", "#7D746A", "#F4F0E8"
GOLD, GOLD_INK = "#E5B45A", "#8C6216"
AMBER, GREEN, RED = "#D9772C", "#4F7A3A", "#C2452F"

STEPS = {"de": ["Frage", "Aufbau", "Messung", "Ergebnis", "Grenzen", "Stand", "Dein Versuch"],
         "en": ["Question", "Setup", "Measure", "Result", "Limits", "Status", "Your test"]}
DEFAULT_STEP = {"lb_hook": 0, "lb_setup": 1, "lb_measure": 2, "lb_result": 3, "lb_replicate": 3, "lb_verdict": 4, "lb_try": 6, "lb_photo": 0, "lb_split": 2}
RECON = {"de": "KI-Nachstellung des veröffentlichten Versuchs · keine Originalaufnahme",
         "en": "AI reconstruction of the published experiment · not original footage"}
MEDIA_ROOTS = [Path(__file__).resolve().parents[1] / "assets" / "higgsfield" / n for n in ("testvideo", "library")]  # first hit wins
MEDIA_DIR = "assets/gw"                      # project-relative folder the LAYER copies photos and clips into
WIN_Y, WIN_H = 290, 920                      # photo window: full width, the height of the notebook page
SPLIT_H = 430                                # lb_split: photo part on top, measurement below
HONEST = {"de": "Nacherzählt aus der Studie · nicht selbst durchgeführt",
          "en": "Retold from the study · not run by us"}
LEVELS = {  # replication status stamp: key -> (de, en, colour)
    "haelt": ("Hält", "Holds", GREEN),
    "gemischt": ("Gemischt", "Mixed", AMBER),
    "nicht_bestaetigt": ("Nicht bestätigt", "Not confirmed", RED),
    "offen": ("Offen", "Open", PMUTED),
}
LEVEL_HEAD = {"de": "Stand der Forschung", "en": "State of research"}

LIMITS: dict[str, dict[str, int]] = {
    "lb_hook": {"question": 44, "label": 34, "meta": 40, "tease": 34, "stamp": 16, "cite": 66},
    "lb_setup": {"headline": 30, "title": 22, "sub": 24, "read": 30, "arm_title": 26, "arm_sub": 34, "group": 12, "group_sub": 10, "label": 48, "cite": 66},
    "lb_measure": {"headline": 30, "sheet_label": 22, "label": 34, "rule": 30, "sample": 44, "cite": 66},
    "lb_result": {"headline": 30, "unit": 36, "series": 20, "group": 24, "turn": 18, "gap": 26, "cite": 66},
    "lb_verdict": {"limits_title": 24, "limit": 40, "title": 24, "evidence": 46, "evidence_cite": 52, "cite": 66},
    "lb_try": {"title": 30, "step": 46, "rule": 44, "caveat": 46, "claim": 30, "disclaimer": 60},
    "lb_photo": {"title": 40, "pin": 30, "stamp": 18, "cite": 66},
    "lb_split": {"headline": 30, "label": 22, "value": 10, "unit": 16, "note": 40, "cite": 66},
    "lb_replicate": {"headline": 30, "axis": 46, "zero": 18, "label": 26, "sub": 48, "value": 22, "note": 56, "cite": 66},
}
HOOK_SCENE_TYPES = ["lb_hook", "lb_photo"]


def _e(s) -> str:
    return html.escape(str(s))


def _chk(scene: str, key: str, val, where: str, out: SceneOut) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", str(s).lower())


def _anchor(words, start: float, v, default: float) -> tuple[float, str | None]:
    """Beat-relative seconds from a number or an "@Wort[#n][+0.4]" string; (seconds, problem or None)."""
    if v is None or v == "":
        return float(default), None
    if isinstance(v, (int, float)):
        return float(v), None
    if isinstance(v, str) and v.startswith("@"):
        m = re.match(r"^@(.+?)(?:#(\d+))?([+\-]\d+(?:\.\d+)?)?$", v)
        if m:
            stem, nth = _norm(m.group(1)), int(m.group(2) or 1)
            hits = [w for w in (words or []) if _norm(w.text).startswith(stem)]
            if len(hits) >= nth:
                return max(0.0, hits[nth - 1].start - start + float(m.group(3) or 0)), None
    return float(default), f"word anchor '{v}' not found in the beat; default time used"


def _rel(c: SceneCtx, v, default: float, out: SceneOut) -> float:
    t, prob = _anchor(c.words, c.start, v, default)
    if prob:
        out.problems.append(prob)
    return t


def _in(c: SceneCtx, sel: str, at: float, *, dy: int = 18, dx: int = 0, dur: float = 0.4, ease: str = "power3.out") -> str:
    return (f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,x:{dx},y:{dy}}},'
            f'{{opacity:1,x:0,y:0,duration:{dur:.2f},ease:"{ease}"}},{c.t(at):.3f});')


def _pop(c: SceneCtx, sel: str, at: float, *, frm: float = 0.6, dur: float = 0.38) -> str:
    return (f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,scale:{frm}}},'
            f'{{opacity:1,scale:1,duration:{dur:.2f},ease:"back.out(1.8)"}},{c.t(at):.3f});')


def _frame(c: SceneCtx, turn: bool, out: SceneOut) -> str:
    """Fade in / out of the scene and (after the first scene) a page turn: a blank sheet lies over the new page and
    turns away to the left around the spine, so the new page shows underneath."""
    s = c.sid
    out.tl += [f'tl.fromTo("#{s} .lb-in",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power2.out"}},{c.start:.3f});',
               f'tl.to("#{s} .lb-in",{{opacity:0,duration:0.22,ease:"power2.in"}},{max(c.start + c.enter + 0.05, c.end - 0.22):.3f});']
    if not turn:
        return ""
    # the sheet becomes visible only at the scene start (no immediate render): a still taken outside the scene
    # (cover, contact sheet) must never show a blank sheet over the previous page
    out.tl += [f'tl.set("#{s}turn",{{opacity:1,rotationY:0,transformPerspective:2200,transformOrigin:"0% 50%"}},{c.start:.3f});',
               f'tl.to("#{s}turn",{{rotationY:-92,duration:0.62,ease:"power2.in"}},{c.start:.3f});',
               f'tl.fromTo("#{s}turn .lb-turnshade",{{opacity:0}},{{opacity:0.55,duration:0.62,ease:"power1.in",immediateRender:false}},{c.start:.3f});',
               f'tl.set("#{s}turn",{{opacity:0}},{c.start + 0.64:.3f});']
    out.events.append(round(c.start, 3))
    return f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>'


def _cite(c: SceneCtx, text: str, out: SceneOut, scene: str) -> str:
    if not text:
        return ""
    _chk(scene, "cite", text, "cite", out)
    out.tl.append(_in(c, ".lb-cite", 0.35, dy=8))
    return f'<div class="lb-cite" style="top:{CITE_Y}px">{_e(text)}</div>'


def _head(text: str, top: int, cls: str = "lb-h") -> str:
    return f'<div class="{cls}" style="top:{top}px">{_e(text)}</div>' if text else ""


ICONS = {
    "read": '<rect x="10" y="8" width="44" height="50" rx="5" fill="none" stroke="currentColor" stroke-width="4"/>'
            + "".join(f'<line x1="18" y1="{y}" x2="46" y2="{y}" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>' for y in (20, 30, 40, 50)),
    "write": '<rect x="8" y="10" width="38" height="46" rx="5" fill="none" stroke="currentColor" stroke-width="4"/>'
             '<path d="M30 46 L52 14 L58 19 L36 51 L28 54 Z" fill="currentColor"/>',
    "clock": '<circle cx="32" cy="32" r="24" fill="none" stroke="currentColor" stroke-width="4"/>'
             '<path d="M32 18 V33 L42 39" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
    "count": '<path d="M12 14 V52 M24 14 V52 M36 14 V52 M48 14 V52 M6 44 L56 22" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>',
}


def _icon(name: str) -> str:
    return f'<svg class="lb-ico" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">{ICONS.get(name, "")}</svg>'


def _dots(prefix: str, n: int, cols: int, pitch: int, size: int, left: int, top: int, targets=None) -> str:
    """n participant dots in a grid; targets[i] = (x, y) absolute end position for a later move (data-dx/dy)."""
    out = []
    for i in range(n):
        x, y = left + (i % cols) * pitch, top + (i // cols) * pitch
        extra = ""
        if targets:
            tx, ty = targets[i]
            extra = f' data-dx="{tx - x}" data-dy="{ty - y}"'
        out.append(f'<i class="lb-dot {prefix}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px"{extra}></i>')
    return "".join(out)


# --- lb_hook: the question, the participants, the twist ------------------------------------------------

def lb_hook(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_hook", "question", d.get("question", ""), "question", out)
    dots, meta, tease, stamp = d.get("dots") or {}, d.get("meta") or {}, d.get("tease") or {}, d.get("stamp") or {}
    _chk("lb_hook", "label", dots.get("label", ""), "dots.label", out)
    _chk("lb_hook", "meta", meta.get("text", ""), "meta.text", out)
    _chk("lb_hook", "tease", tease.get("text", ""), "tease.text", out)
    _chk("lb_hook", "stamp", stamp.get("text", ""), "stamp.text", out)
    n = int(dots.get("n", 120))
    cols = 20 if n > 120 else (15 if n > 60 else 10)
    rows = (n + cols - 1) // cols
    # the dot field stays within about 300 px height, so meta, tease and stamp keep their room above the cite line
    pitch = 38 if rows <= 8 else max(24, int(278 / (rows - 1)))
    size = min(22, int(pitch * 0.6))
    gw = (cols - 1) * pitch + size
    left, top = CL + (CW - gw) // 2, CT + 190
    label_top = top + (rows - 1) * pitch + size + 22
    cite = _cite(c, d.get("cite", ""), out, "lb_hook")
    out.html = f"""<div class="lb-in">
  <div class="lb-q" style="top:{CT}px">{_e(d.get("question", ""))}</div>
  <div class="lb-dotfield" id="{s}df" style="left:0;top:0">{_dots("lbh", n, cols, pitch, size, left, top)}</div>
  <div class="lb-nlabel" style="top:{label_top}px"><b>n = {n}</b><span>{_e(dots.get("label", ""))}</span></div>
  <div class="lb-meta" style="top:{label_top + 58}px">{_e(meta.get("text", ""))}</div>
  <div class="lb-tease" style="top:{label_top + 112}px"><span>{_e(tease.get("text", ""))}</span></div>
  {f'<div class="lb-stampwrap" style="left:{CL + 400}px;top:{label_top + 166}px"><div class="lb-stamp" id="{s}st">{_e(stamp.get("text", ""))}</div></div>' if stamp else ""}
  {cite}
</div>"""
    _frame(c, False, out)
    out.tl.append(_in(c, ".lb-q", 0.05, dy=24, dur=0.5))
    out.events.append(c.t(0.05))
    at = _rel(c, dots.get("at", 1.6), 1.6, out)
    out.tl.append(f'tl.fromTo("#{s} .lbh",{{opacity:0,scale:0.2}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(2)",'
                  f'stagger:{{each:{min(0.012, 1.2 / max(n, 1)):.4f},from:"start"}}}},{c.t(at):.3f});')
    out.tl.append(_in(c, ".lb-nlabel", at + 0.3))
    out.events += [c.t(at), c.t(at + 0.3)]
    if meta:
        at = _rel(c, meta.get("at", at + 1.0), at + 1.0, out)
        out.tl.append(_in(c, ".lb-meta", at))
        out.events.append(c.t(at))
    if tease:
        at = _rel(c, tease.get("at", c.duration - 3.0), c.duration - 3.0, out)
        out.tl.append(_in(c, ".lb-tease", at, dx=-20, dy=0))
        out.events.append(c.t(at))
    if stamp:
        at = _rel(c, stamp.get("at", c.duration - 1.4), c.duration - 1.4, out)
        out.tl.append(f'tl.fromTo("#{s}st",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:0.26,ease:"power4.in"}},{c.t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}df",{{x:0}},{{x:-6,duration:0.06,yoyo:true,repeat:3}},{c.t(at + 0.26):.3f});')
        out.events.append(c.t(at))
    return out


# --- lb_setup: texts, conditions, group split ----------------------------------------------------------

def lb_setup(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_setup", "headline", d.get("headline", ""), "headline", out)
    sheets, arms, grp, read = d.get("sheets") or [], d.get("arms") or [], d.get("groups") or {}, d.get("read") or {}
    for i, sh in enumerate(sheets):
        _chk("lb_setup", "title", sh.get("title", ""), f"sheets[{i}].title", out)
        _chk("lb_setup", "sub", sh.get("sub", ""), f"sheets[{i}].sub", out)
    for i, a in enumerate(arms):
        _chk("lb_setup", "arm_title", a.get("title", ""), f"arms[{i}].title", out)
        _chk("lb_setup", "arm_sub", a.get("sub", ""), f"arms[{i}].sub", out)
    _chk("lb_setup", "read", read.get("text", ""), "read.text", out)
    _chk("lb_setup", "label", grp.get("label", ""), "groups.label", out)
    k = max(1, len(arms) or len(sheets) or 2)
    colw = (CW - 24 * (k - 1)) // k
    y_sheet, y_read, y_arm, y_dots = CT + 76, CT + 184, CT + 250, CT + 440
    sheet_html = "".join(
        f'<div class="lb-sheet" id="{s}sh{i}" style="left:{CL + i * (colw + 24)}px;top:{y_sheet}px;width:{colw}px">'
        f'{_icon(sh.get("icon", "read"))}<div><b>{_e(sh.get("title", ""))}</b><span>{_e(sh.get("sub", ""))}</span></div></div>'
        for i, sh in enumerate(sheets[:k]))
    arm_html = "".join(
        f'<div class="lb-arm lb-arm{i}" id="{s}arm{i}" style="left:{CL + i * (colw + 24)}px;top:{y_arm}px;width:{colw}px">'
        f'<div class="lb-armhead">{_icon(a.get("icon", "read"))}<b>{_e(a.get("title", ""))}</b></div>'
        f'<span>{_e(a.get("sub", ""))}</span></div>'
        for i, a in enumerate(arms[:k]))
    arrows = "".join(
        f'<svg class="lb-arrow" style="left:{CL + i * (colw + 24) + colw // 2 - 14}px;top:{y_read + 2}px" width="28" height="60" viewBox="0 0 28 60">'
        f'<path id="{s}ar{i}" d="M14 2 V50 M4 40 L14 54 L24 40" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        for i in range(len(arms[:k])))
    # dots: one block first, then split into the groups
    n = int(grp.get("n", 120))
    split = grp.get("split") or []
    g = max(1, len(split))
    size, pitch = 18, 27
    cols_all = 24
    rows_all = (n + cols_all - 1) // cols_all
    block_w = (cols_all - 1) * pitch + size
    bx, by = CL + (CW - block_w) // 2, y_dots + 34
    per = n // g
    gcols = max(8, min((CW // g - 20) // pitch, -(-per // 5)))
    gpw = (gcols - 1) * pitch + size
    gslot = CW // g
    targets = []
    for i in range(n):
        gi, j = min(i // per, g - 1), i - min(i // per, g - 1) * per
        gx = CL + gi * gslot + (gslot - gpw) // 2
        targets.append((gx + (j % gcols) * pitch, by + (j // gcols) * pitch))
    grows = (per + gcols - 1) // gcols
    glabel_top = by + max(rows_all, grows) * pitch + 10
    glabels = "".join(
        f'<div class="lb-glabel" id="{s}gl{i}" style="left:{CL + i * gslot}px;top:{glabel_top}px;width:{gslot}px">'
        f'<b>{_e(sp.get("label", ""))}</b><span>{_e(sp.get("sub", ""))}</span></div>'
        for i, sp in enumerate(split))
    for i, sp in enumerate(split):
        _chk("lb_setup", "group", sp.get("label", ""), f"groups.split[{i}].label", out)
        _chk("lb_setup", "group_sub", sp.get("sub", ""), f"groups.split[{i}].sub", out)
    cite = _cite(c, d.get("cite", ""), out, "lb_setup")
    out.html = f"""<div class="lb-in">
  {_head(d.get("headline", ""), CT)}
  {sheet_html}
  <div class="lb-read" style="top:{y_read + 14}px"><span>{_e(read.get("text", ""))}</span></div>
  {arrows}
  {arm_html}
  <div class="lb-grouplabel" style="top:{y_dots - 8}px">{_e(grp.get("label", ""))}</div>
  {_dots("lbs", n, cols_all, pitch, size, bx, by, targets)}
  {glabels}
  {cite}
</div>"""
    out.html += _frame(c, d.get("turn", True), out)
    out.tl.append(_in(c, ".lb-h", 0.1))
    sheets_at = _rel(c, d.get("sheets_at", 0.8), 0.8, out)
    for i in range(len(sheets[:k])):
        out.tl.append(_in(c, f"#{s}sh{i}", sheets_at + 0.15 * i, dy=26))
    out.events.append(c.t(sheets_at))
    if read:
        at = _rel(c, read.get("at", sheets_at + 1.0), sheets_at + 1.0, out)
        out.tl.append(_pop(c, ".lb-read span", at))
        out.events.append(c.t(at))
    for i, a in enumerate(arms[:k]):
        at = _rel(c, a.get("at", 3.0 + 2.0 * i), 3.0 + 2.0 * i, out)
        out.tl.append(f'tl.fromTo("#{s}ar{i}",{{strokeDasharray:80,strokeDashoffset:80}},{{strokeDashoffset:0,duration:0.35,ease:"power2.out"}},{c.t(at):.3f});')
        out.tl.append(_in(c, f"#{s}arm{i}", at + 0.15, dy=22))
        out.events.append(c.t(at))
    at_g = _rel(c, grp.get("at", c.duration - 5.0), c.duration - 5.0, out)
    out.tl.append(_in(c, ".lb-grouplabel", at_g - 0.6, dy=10))
    out.tl.append(f'tl.fromTo("#{s} .lbs",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)",stagger:0.004}},{c.t(at_g - 0.6):.3f});')
    out.tl.append(f'tl.to("#{s} .lbs",{{x:function(i,t){{return +t.dataset.dx}},y:function(i,t){{return +t.dataset.dy}},'
                  f'duration:0.8,ease:"power3.inOut",stagger:0.003}},{c.t(at_g):.3f});')
    out.events += [c.t(at_g - 0.6), c.t(at_g)]
    for i, sp in enumerate(split):
        at = _rel(c, sp.get("at", at_g + 0.6 + 0.6 * i), at_g + 0.6 + 0.6 * i, out)
        out.tl.append(_in(c, f"#{s}gl{i}", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- lb_measure: what exactly was counted ----------------------------------------------------------------

def lb_measure(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_measure", "headline", d.get("headline", ""), "headline", out)
    _chk("lb_measure", "sheet_label", d.get("sheet_label", ""), "sheet_label", out)
    units, rule, sample = d.get("units") or {}, d.get("rule") or {}, d.get("sample") or {}
    _chk("lb_measure", "label", units.get("label", ""), "units.label", out)
    _chk("lb_measure", "rule", rule.get("text", ""), "rule.text", out)
    _chk("lb_measure", "sample", sample.get("text", ""), "sample.text", out)
    n = int(units.get("n", 30))
    cols = n if n <= 8 else 6
    box, gap = (60, 10) if n <= 8 else (66, 14)
    gx, gy = CL + 312, CT + 100
    clabels = units.get("labels") or []
    hl = int(units.get("highlight", 0))
    cells = "".join(f'<i class="lb-cell" id="{s}c{i}" style="left:{gx + (i % cols) * (box + gap)}px;top:{gy + (i // cols) * (box + gap)}px;--cb:{box}px">'
                    f'<b id="{s}cf{i}"></b><em>{_e(clabels[i]) if i < len(clabels) else ""}</em></i>' for i in range(n))
    rows = (n + cols - 1) // cols
    grid_bottom = gy + rows * (box + gap) - gap
    y_after = max(grid_bottom + 66, gy + 420)
    lines = "".join(f'<i style="top:{58 + k * 34}px;width:{[230, 250, 200, 244, 236, 180, 248, 214, 240, 120][k % 10]}px"></i>' for k in range(10))
    cite = _cite(c, d.get("cite", ""), out, "lb_measure")
    turn = f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>' if d.get("turn", True) else ""
    out.html = f"""<div class="lb-in">
  {_head(d.get("headline", ""), CT)}
  <div class="lb-textsheet" id="{s}ts" style="left:{CL}px;top:{gy}px"><b>{_e(d.get("sheet_label", ""))}</b>{lines}</div>
  {cells}
  <div class="lb-unitlabel" style="left:{gx}px;top:{grid_bottom + 18}px">{_e(units.get("label", ""))}</div>
  <div class="lb-rule" style="top:{y_after + 26}px"><span>{_icon("count")}{_e(rule.get("text", ""))}</span></div>
  <div class="lb-sample" style="top:{y_after + 110}px">{_e(sample.get("text", ""))}</div>
  {cite}
</div>{turn}"""
    _frame(c, bool(turn), out)
    out.tl.append(_in(c, ".lb-h", 0.1))
    out.tl.append(_in(c, f"#{s}ts", 0.3, dx=-30, dy=0))
    at = _rel(c, units.get("at", 1.5), 1.5, out)
    out.tl.append(f'tl.fromTo("#{s} .lb-cell",{{opacity:0,x:-140,scale:0.5}},{{opacity:1,x:0,scale:1,duration:0.4,ease:"power3.out",stagger:0.025}},{c.t(at):.3f});')
    out.tl.append(_in(c, ".lb-unitlabel", at + 0.6, dy=10))
    out.events += [c.t(0.3), c.t(at), c.t(at + 0.6)]
    if rule:
        at = _rel(c, rule.get("at", at + 2.0), at + 2.0, out)
        out.tl.append(_pop(c, ".lb-rule span", at))
        out.tl.append(f'tl.fromTo("#{s}cf{hl}",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2)"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if sample:
        fill = max(0, min(n, int(sample.get("fill", 0))))
        at = _rel(c, sample.get("at", at + 1.0), at + 1.0, out)
        if fill > 0 and not (fill == 1 and hl == 0):
            sels = ",".join(f'"#{s}cf{i}"' for i in range(0, fill) if i != hl)
            out.tl.append(f'tl.fromTo([{sels}],{{scale:0}},{{scale:1,duration:0.22,ease:"back.out(2)",stagger:0.03}},{c.t(at):.3f});')
        out.tl.append(_in(c, ".lb-sample", at + 0.2, dy=12))
        out.events.append(c.t(at))
    return out


# --- lb_result: the numbers of the paper as bars -----------------------------------------------------------

def lb_result(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_result", "headline", d.get("headline", ""), "headline", out)
    _chk("lb_result", "unit", d.get("unit", ""), "unit", out)
    series, groups = d.get("series") or [], d.get("groups") or []
    for i, se in enumerate(series):
        _chk("lb_result", "series", se.get("label", ""), f"series[{i}].label", out)
    vmax = float(d.get("max", 100))
    base_y, top_y = CB - 80, CT + 200          # bar baseline and top of the scale
    hmax = base_y - top_y
    k = max(1, len(series))
    bw, bgap = 104, 14
    gslot = CW // max(1, len(groups))
    legend = "".join(f'<span class="lb-leg lb-k{se.get("kind", "a")}"><i></i>{_e(se.get("label", ""))}</span>' for se in series)
    bars, labels, glabels = [], [], []
    for gi, gr in enumerate(groups):
        _chk("lb_result", "group", gr.get("label", ""), f"groups[{gi}].label", out)
        gw = k * bw + (k - 1) * bgap
        gx = CL + gi * gslot + (gslot - gw) // 2
        vals = gr.get("values") or []
        best = max(range(len(vals)), key=lambda j: vals[j]) if vals else -1
        for j, v in enumerate(vals[:k]):
            h = round(hmax * float(v) / vmax)
            x = gx + j * (bw + bgap)
            kind = series[j].get("kind", "a") if j < len(series) else "a"
            bars.append(f'<i class="lb-bar lb-k{kind}{" lb-best" if j == best else ""}" id="{s}b{gi}_{j}" '
                        f'style="left:{x}px;top:{base_y - h}px;width:{bw}px;height:{h}px"></i>')
            labels.append(f'<div class="lb-val lb-k{kind}{" lb-best" if j == best else ""}" id="{s}v{gi}_{j}" '
                          f'style="left:{x - 20}px;top:{base_y - h - 58}px;width:{bw + 40}px">'
                          f'{_e((gr.get("labels") or [])[j] if j < len(gr.get("labels") or []) else gr.get("fmt", "{}").format(v))}</div>')
        glabels.append(f'<div class="lb-gx" id="{s}g{gi}" style="left:{CL + gi * gslot}px;top:{base_y + 14}px;width:{gslot}px">{_e(gr.get("label", ""))}</div>')
    grid = "".join(f'<i class="lb-hline" style="top:{base_y - round(hmax * f)}px"></i>' for f in (0.25, 0.5, 0.75, 1.0))
    tn, gp = d.get("turn_mark") or {}, d.get("gap") or {}
    _chk("lb_result", "turn", tn.get("text", ""), "turn_mark.text", out)
    _chk("lb_result", "gap", gp.get("text", ""), "gap.text", out)
    turn_html = ""
    if tn:
        bi = int(tn.get("between", 0))
        tx = CL + (bi + 1) * gslot - 120
        turn_html = (f'<div class="lb-turnmark" id="{s}tm" style="left:{tx}px;top:{top_y - 62}px"><span>{_e(tn.get("text", ""))}</span>'
                     f'<svg width="240" height="54" viewBox="0 0 240 54"><path id="{s}tmp" d="M20 44 C80 4 160 4 220 44" fill="none" stroke="{AMBER}" '
                     f'stroke-width="5" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"/></svg></div>')
    gap_html = ""
    if gp:
        gi = int(gp.get("group", len(groups) - 1))
        gvals = (groups[gi].get("values") or [0]) if 0 <= gi < len(groups) else [0]
        gtop = base_y - round(hmax * max(float(v) for v in gvals) / vmax) - 136
        gap_html = f'<div class="lb-gap" id="{s}gp" style="left:{CL + gi * gslot}px;top:{gtop}px;width:{gslot}px"><span>{_e(gp.get("text", ""))}</span></div>'
    cite = _cite(c, d.get("cite", ""), out, "lb_result")
    turn = f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>' if d.get("turn", True) else ""
    out.html = f"""<div class="lb-in">
  {_head(d.get("headline", ""), CT)}
  <div class="lb-legend" style="top:{CT + 74}px">{legend}</div>
  <div class="lb-unit" style="top:{CT + 22}px">{_e(d.get("unit", ""))}</div>
  {grid}
  <i class="lb-base" style="top:{base_y}px"></i>
  {"".join(bars)}{"".join(labels)}{"".join(glabels)}
  {turn_html}{gap_html}
  {cite}
</div>{turn}"""
    _frame(c, bool(turn), out)
    out.tl.append(_in(c, ".lb-h", 0.1))
    out.tl.append(_in(c, ".lb-legend", 0.3, dy=10))
    out.tl.append(_in(c, ".lb-unit", 0.4, dy=10))
    out.events.append(c.t(0.3))
    for gi, gr in enumerate(groups):
        at = _rel(c, gr.get("at", 0.8 + 3.0 * gi), 0.8 + 3.0 * gi, out)
        out.tl.append(_in(c, f"#{s}g{gi}", at, dy=10))
        for j in range(min(k, len(gr.get("values") or []))):
            bat = at + 0.25 + 0.55 * j
            if gr.get("value_at") and j < len(gr["value_at"]):
                bat = _rel(c, gr["value_at"][j], bat, out)
            out.tl.append(f'tl.fromTo("#{s}b{gi}_{j}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:0.55,ease:"power3.out"}},{c.t(bat):.3f});')
            out.tl.append(_in(c, f"#{s}v{gi}_{j}", bat + 0.35, dy=10, dur=0.3))
            out.events.append(c.t(bat))
    if tn:
        at = _rel(c, tn.get("at", c.duration * 0.5), c.duration * 0.5, out)
        out.tl.append(_in(c, f"#{s}tm span", at, dy=8))
        out.tl.append(f'tl.to("#{s}tmp",{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if gp:
        at = _rel(c, gp.get("at", c.duration - 1.5), c.duration - 1.5, out)
        out.tl.append(_pop(c, f"#{s}gp span", at))
        out.events.append(c.t(at))
    return out


# --- lb_verdict: limits, then the replication stamp -------------------------------------------------------

def lb_verdict(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_verdict", "limits_title", d.get("limits_title", ""), "limits_title", out)
    limits, st, ev = d.get("limits") or [], d.get("status") or {}, d.get("evidence") or []
    for i, li in enumerate(limits):
        _chk("lb_verdict", "limit", li.get("text", ""), f"limits[{i}].text", out)
    for i, e in enumerate(ev):
        _chk("lb_verdict", "evidence", e.get("text", ""), f"evidence[{i}].text", out)
        _chk("lb_verdict", "evidence_cite", e.get("cite", ""), f"evidence[{i}].cite", out)
    level = st.get("level", "offen")
    if level not in LEVELS:
        out.problems.append(f"lb_verdict.status.level '{level}' unknown; use {sorted(LEVELS)}")
        level = "offen"
    de, en, col = LEVELS[level]
    word = de if c.lang == "de" else en
    _chk("lb_verdict", "title", st.get("title", LEVEL_HEAD.get(c.lang, LEVEL_HEAD["de"])), "status.title", out)
    rows = "".join(f'<div class="lb-limit" id="{s}l{i}" style="top:{CT + 74 + i * 70}px"><i></i><span>{_e(li.get("text", ""))}</span></div>'
                   for i, li in enumerate(limits))
    y_st = CT + 74 + max(1, len(limits)) * 70 + 44
    scale = "".join(f'<span class="lb-lv{" on" if key == level else ""}" style="--c:{LEVELS[key][2]}"><i></i>{_e(LEVELS[key][0 if c.lang == "de" else 1])}</span>'
                    for key in LEVELS)
    evid = "".join(f'<div class="lb-ev" id="{s}e{i}" style="top:{y_st + 240 + i * 92}px"><b>{_e(e.get("text", ""))}</b><span>{_e(e.get("cite", ""))}</span></div>'
                   for i, e in enumerate(ev))
    cite = _cite(c, d.get("cite", ""), out, "lb_verdict")
    turn = f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>' if d.get("turn", True) else ""
    out.html = f"""<div class="lb-in">
  {_head(d.get("limits_title", ""), CT, "lb-h lb-hs")}
  {rows}
  <i class="lb-sep" id="{s}sep" style="top:{y_st - 18}px"></i>
  <div class="lb-sthead" style="top:{y_st}px">{_e(st.get("title", LEVEL_HEAD.get(c.lang, LEVEL_HEAD["de"])))}</div>
  <div class="lb-levels" style="top:{y_st + 56}px">{scale}</div>
  <div class="lb-stampwrap lb-vstamp" style="left:{CL + 300}px;top:{y_st + 116}px"><div class="lb-stamp" id="{s}st" style="background:{col};font-size:{56 if len(word) <= 9 else 44}px">{_e(word)}</div></div>
  {evid}
  {cite}
</div>{turn}"""
    _frame(c, bool(turn), out)
    out.tl.append(_in(c, ".lb-hs", 0.1))
    out.events.append(c.t(0.1))
    for i, li in enumerate(limits):
        at = _rel(c, li.get("at", 0.8 + 1.2 * i), 0.8 + 1.2 * i, out)
        out.tl.append(_in(c, f"#{s}l{i}", at, dx=-24, dy=0))
        out.events.append(c.t(at))
    at = _rel(c, st.get("at", c.duration * 0.55), c.duration * 0.55, out)
    out.tl.append(f'tl.fromTo("#{s}sep",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.4,ease:"power2.out"}},{c.t(at - 0.3):.3f});')
    out.tl.append(_in(c, ".lb-sthead", at - 0.2, dy=12))
    out.tl.append(_in(c, ".lb-levels", at, dy=12))
    out.events.append(c.t(at))
    for i, e in enumerate(ev):
        eat = _rel(c, e.get("at", at + 0.8 + 1.2 * i), at + 0.8 + 1.2 * i, out)
        out.tl.append(_in(c, f"#{s}e{i}", eat, dy=14))
        out.events.append(c.t(eat))
    sat = _rel(c, st.get("stamp_at", c.duration - 1.6), c.duration - 1.6, out)
    out.tl.append(f'tl.fromTo("#{s}st",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:0.26,ease:"power4.in"}},{c.t(sat):.3f});')
    out.events.append(c.t(sat))
    return out


# --- lb_try: the viewer's own small test with a measuring rule, then the sign-off -----------------------------

def lb_try(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = c.sid
    for key in ("title", "claim", "disclaimer"):
        _chk("lb_try", key, d.get(key, ""), key, out)
    steps, rule, cav = d.get("steps") or [], d.get("rule") or {}, d.get("caveat") or {}
    for i, st in enumerate(steps):
        _chk("lb_try", "step", st.get("text", ""), f"steps[{i}].text", out)
    _chk("lb_try", "rule", rule.get("text", ""), "rule.text", out)
    _chk("lb_try", "caveat", cav.get("text", ""), "caveat.text", out)
    rows = "".join(f'<div class="lb-step" id="{s}s{i}" style="top:{CT + 116 + i * 104}px"><i>{i + 1}</i><span>{_e(st.get("text", ""))}</span></div>'
                   for i, st in enumerate(steps))
    y_rule = CT + 116 + max(1, len(steps)) * 104 + 14
    turn = f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>' if d.get("turn", True) else ""
    out.html = f"""<div class="lb-in">
  <div class="lb-slip" id="{s}slip" style="top:{CT - 14}px;height:{y_rule + 150 - CT}px"></div>
  {_head(d.get("title", ""), CT + 10, "lb-h lb-ht")}
  {rows}
  <div class="lb-trule" style="top:{y_rule}px"><span>{_icon("count")}{_e(rule.get("text", ""))}</span></div>
  <div class="lb-caveat" style="top:{y_rule + 84}px"><i></i><span>{_e(cav.get("text", ""))}</span></div>
  <div class="lb-sign" style="top:{CB - 118}px"><img class="lb-signmark" src="assets/logo/gritwerk-mark.svg" alt=""><b>GRITWERK</b>
    <span class="lb-claim">{_e(d.get("claim", ""))}</span></div>
  <div class="lb-disc" style="top:{CB - 46}px">{_e(d.get("disclaimer", ""))}</div>
</div>{turn}"""
    _frame(c, bool(turn), out)
    out.tl.append(f'tl.fromTo("#{s}slip",{{opacity:0,y:40,rotation:-2}},{{opacity:1,y:0,rotation:0,duration:0.5,ease:"power3.out"}},{c.t(0.1):.3f});')
    out.tl.append(_in(c, ".lb-ht", 0.2))
    out.events.append(c.t(0.1))
    for i, st in enumerate(steps):
        at = _rel(c, st.get("at", 0.8 + 1.6 * i), 0.8 + 1.6 * i, out)
        out.tl.append(_in(c, f"#{s}s{i}", at, dx=-24, dy=0))
        out.tl.append(f'tl.fromTo("#{s}s{i} i",{{scale:0.4}},{{scale:1,duration:0.35,ease:"back.out(2.4)"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if rule:
        at = _rel(c, rule.get("at", 6.0), 6.0, out)
        out.tl.append(_pop(c, ".lb-trule span", at))
        out.events.append(c.t(at))
    if cav:
        at = _rel(c, cav.get("at", 8.0), 8.0, out)
        out.tl.append(_in(c, ".lb-caveat", at, dy=12))
        out.events.append(c.t(at))
    at = _rel(c, d.get("sign_at", c.duration - 4.2), c.duration - 4.2, out)
    out.tl.append(_in(c, ".lb-sign", at, dy=16))
    out.tl.append(_in(c, ".lb-disc", at + 0.3, dy=10))
    out.events.append(c.t(at))
    if c.duration - at < 4.0:
        out.problems.append(f"lb_try: sign-off visible {c.duration - at:.1f} s < 4 s")
    return out


# --- lb_replicate: original against its replication on one effect axis (series "Hält das?") -----------------

def lb_replicate(c: SceneCtx, d: dict) -> SceneOut:
    """Each study is one row: label and sample on top, a point with its interval on a shared axis below. The zero
    line marks "no effect". Values are those reported in the papers (effect size d or another stated unit); a row
    without an interval shows only the point and must say why in `sub`."""
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_replicate", "headline", d.get("headline", ""), "headline", out)
    ax, rows, note = d.get("axis") or {}, d.get("rows") or [], d.get("note") or {}
    _chk("lb_replicate", "axis", ax.get("label", ""), "axis.label", out)
    _chk("lb_replicate", "zero", ax.get("zero_label", ""), "axis.zero_label", out)
    _chk("lb_replicate", "note", note.get("text", ""), "note.text", out)
    lo, hi = float(ax.get("min", -0.5)), float(ax.get("max", 1.0))
    x0, x1 = CL + 20, CL + CW - 20

    def X(v: float) -> int:
        return round(x0 + (min(hi, max(lo, float(v))) - lo) / (hi - lo) * (x1 - x0))

    top = CT + 140
    step = max(130, min(190, (CB - 120 - top) // max(1, len(rows))))
    body = []
    for i, r in enumerate(rows):
        for k, n in (("label", "label"), ("sub", "sub"), ("value_text", "value")):
            _chk("lb_replicate", n, r.get(k, ""), f"rows[{i}].{k}", out)
        y = top + i * step
        kind = r.get("kind", "a" if i == 0 else "b")
        ci = r.get("ci")
        bar = ""
        px = X(r.get("value", 0))
        right = px + 17
        if ci and len(ci) == 2:
            l, h = X(ci[0]), X(ci[1])
            right = max(right, h)
            bar = f'<i class="lb-ci lb-k{kind}" id="{s}ci{i}" style="left:{l}px;top:{y + 94}px;width:{max(4, h - l)}px"></i>'
        vx = right + 18 if right + 18 + 200 <= CL + CW else px - 17 - 18 - 200
        body.append(f'<div class="lb-rlabel" id="{s}rl{i}" style="top:{y}px"><b>{_e(r.get("label", ""))}</b><span>{_e(r.get("sub", ""))}</span></div>'
                    f'<i class="lb-track" style="top:{y + 98}px"></i>{bar}'
                    f'<i class="lb-pt lb-k{kind}" id="{s}pt{i}" style="left:{px - 17}px;top:{y + 82}px"></i>'
                    f'<div class="lb-ptval{" lb-ptl" if vx < px else ""}" id="{s}pv{i}" style="left:{vx}px;top:{y + 76}px">{_e(r.get("value_text", ""))}</div>')
    zx = X(0)
    zeros = "".join(f'<i class="lb-zero lb-zero{s}" style="left:{zx - 2}px;top:{top + i * step + 80}px;height:48px"></i>' for i in range(len(rows)))
    note_html = (f'<div class="lb-rnote" style="top:{top + max(1, len(rows)) * step + 86}px"><span>{_e(note.get("text", ""))}</span></div>'
                 if note.get("text") else "")
    y_end = top + max(1, len(rows)) * step
    ticks = "".join(f'<span class="lb-axt" style="left:{X(t) - 40}px;top:{y_end + 4}px">{_e(str(t).replace(".", "," if c.lang == "de" else "."))}</span>'
                    for t in (ax.get("ticks") or []))
    cite = _cite(c, d.get("cite", ""), out, "lb_replicate")
    turn = f'<div class="lb-turn" id="{s}turn"><div class="lb-turnshade"></div></div>' if d.get("turn", True) else ""
    out.html = f"""<div class="lb-in">
  {_head(d.get("headline", ""), CT)}
  <div class="lb-axlabel" style="top:{CT + 74}px">{_e(ax.get("label", ""))}</div>
  {zeros}
  <div class="lb-zerol" style="left:{zx - 120}px;top:{y_end + 40}px">{_e(ax.get("zero_label", ""))}</div>
  {ticks}
  {"".join(body)}
  {note_html}
  {cite}
</div>{turn}"""
    _frame(c, bool(turn), out)
    out.tl.append(_in(c, ".lb-h", 0.1))
    out.tl.append(_in(c, ".lb-axlabel", 0.3, dy=10))
    out.tl.append(f'tl.fromTo("#{s} .lb-zero{s}",{{scaleY:0,transformOrigin:"50% 50%"}},{{scaleY:1,duration:0.5,ease:"power2.out"}},{c.t(0.4):.3f});')
    out.tl.append(_in(c, ".lb-zerol", 0.6, dy=8))
    out.events += [c.t(0.1), c.t(0.4)]
    for i, r in enumerate(rows):
        at = _rel(c, r.get("at", 0.8 + 3.0 * i), 0.8 + 3.0 * i, out)
        out.tl.append(_in(c, f"#{s}rl{i}", at, dx=-20, dy=0))
        if r.get("ci"):
            out.tl.append(f'tl.fromTo("#{s}ci{i}",{{scaleX:0,transformOrigin:"50% 50%"}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{c.t(at + 0.3):.3f});')
        out.tl.append(f'tl.fromTo("#{s}pt{i}",{{opacity:0,scale:0.2}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{c.t(at + 0.5):.3f});')
        out.tl.append(_in(c, f"#{s}pv{i}", at + 0.7, dy=8))
        out.events += [c.t(at), c.t(at + 0.5)]
    if note:
        at = _rel(c, note.get("at", c.duration - 2.0), c.duration - 2.0, out)
        out.tl.append(_pop(c, ".lb-rnote span", at))
        out.events.append(c.t(at))
    return out


# --- lb_photo: a full-width AI reconstruction (still with camera move, or a Kling clip from the LAYER) -------------

def _media(name: str) -> str:
    return f"{MEDIA_DIR}/{name}"


def lb_photo(c: SceneCtx, d: dict) -> SceneOut:
    """A reconstruction of the published experiment as a photo window (full width, y 290-1210). A still gets a slow
    camera move (`move`: push | pan | pull); a clip (`clip`) is placed by the LAYER as a muted video under this scene.
    The tag "KI-Nachstellung ... keine Originalaufnahme" is always on. Pins point at things in the picture; an optional
    title and stamp make it a hook."""
    out = SceneOut(html="")
    s = c.sid
    title, stamp, pins = d.get("title") or {}, d.get("stamp") or {}, d.get("pins") or []
    _chk("lb_photo", "title", title.get("text", ""), "title.text", out)
    _chk("lb_photo", "stamp", stamp.get("text", ""), "stamp.text", out)
    img = ""
    clip_len = float(d.get("clip_len", 8.0))
    if d.get("image"):
        hold = 'opacity:0;' if d.get("clip") else ""
        img = f'<img class="lb-phimg" id="{s}img" src="{_media(d["image"])}" alt="" style="{hold}object-position:50% {int(d.get("focus", 50))}%">'
    pin_html = []
    for i, pn in enumerate(pins):
        _chk("lb_photo", "pin", pn.get("label", ""), f"pins[{i}].label", out)
        x, y = int(pn.get("x", 540)), WIN_Y + int(pn.get("y", 460))
        side = pn.get("side", "left" if x > 540 else "right")
        lx = x - 30 - 420 if side == "left" else x + 30
        lx = max(40, min(lx, 932 - 420))
        pin_html.append(f'<i class="lb-pin" id="{s}pin{i}" style="left:{x - 14}px;top:{y - 14}px"></i>'
                        f'<div class="lb-pinl lb-pin-{side}" id="{s}pl{i}" style="left:{lx}px;top:{y - 26}px"><span>{_e(pn.get("label", ""))}</span></div>')
    tag = RECON.get(c.lang, RECON["de"])
    cite = d.get("cite", "")
    _chk("lb_photo", "cite", cite, "cite", out)
    out.html = f"""<div class="lb-in lb-ph">
  <div class="lb-phwin" style="top:{WIN_Y}px;height:{WIN_H}px">{img}<div class="lb-phshade"></div></div>
  <div class="lb-phtag" style="top:{WIN_Y + 20}px"><i></i>{_e(tag)}</div>
  {f'<div class="lb-phtitle" style="top:{WIN_Y + 86}px">{_e(title.get("text", ""))}</div>' if title else ""}
  {"".join(pin_html)}
  {f'<div class="lb-stampwrap" style="left:{CL + 330}px;top:{WIN_Y + WIN_H - 210}px"><div class="lb-stamp" id="{s}st">{_e(stamp.get("text", ""))}</div></div>' if stamp else ""}
  {f'<div class="lb-phcite" style="top:{WIN_Y + WIN_H - 48}px">{_e(cite)}</div>' if cite else ""}
</div>"""
    _frame(c, False, out)
    # a hard cut with a short flash of the window edge instead of the page turn
    out.tl.append(f'tl.fromTo("#{s} .lb-phwin",{{opacity:0.0,y:30}},{{opacity:1,y:0,duration:0.32,ease:"power3.out"}},{c.start:.3f});')
    out.events.append(round(c.start, 3))
    if img and d.get("clip"):
        if c.duration > clip_len - 0.1:
            out.tl.append(f'tl.set("#{s}img",{{opacity:1}},{c.t(clip_len - 0.08):.3f});')
    elif img:
        mv = d.get("move", "push")
        frm, to = {"push": ("scale:1,x:0", "scale:1.09,x:0"), "pull": ("scale:1.1,x:0", "scale:1.0,x:0"),
                   "pan": ("scale:1.08,x:-40", "scale:1.08,x:40")}.get(mv, ("scale:1,x:0", "scale:1.09,x:0"))
        out.tl.append(f'tl.fromTo("#{s}img",{{{frm}}},{{{to},duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});')
    out.tl.append(_in(c, ".lb-phtag", 0.15, dx=-16, dy=0))
    if title:
        at = _rel(c, title.get("at", 0.1), 0.1, out)
        out.tl.append(f'tl.fromTo("#{s} .lb-phtitle",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    for i, pn in enumerate(pins):
        at = _rel(c, pn.get("at", 0.8 + 1.2 * i), 0.8 + 1.2 * i, out)
        out.tl.append(f'tl.fromTo("#{s}pin{i}",{{opacity:0,scale:0.2}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)"}},{c.t(at):.3f});')
        out.tl.append(_in(c, f"#{s}pl{i}", at + 0.15, dx=(-18 if pn.get("side", "left" if int(pn.get("x", 540)) > 540 else "right") == "left" else 18), dy=0))
        out.events.append(c.t(at))
    if stamp:
        at = _rel(c, stamp.get("at", c.duration - 1.2), c.duration - 1.2, out)
        out.tl.append(f'tl.fromTo("#{s}st",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:0.26,ease:"power4.in"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if cite:
        out.tl.append(_in(c, ".lb-phcite", 0.4, dy=8))
    return out


# --- lb_split: reconstruction on top, measurement below (two stopwatches) -------------------------------------------

def _watch(ident: str, frac: float, kind: str) -> str:
    r, cx = 92, 110
    circ = 2 * 3.14159 * r
    ticks = "".join(f'<line x1="{cx}" y1="{cx - r - 10}" x2="{cx}" y2="{cx - r + 2}" stroke="{INK}" stroke-width="4" transform="rotate({k * 30} {cx} {cx})"/>' for k in range(12))
    col = GOLD if kind == "b" else "#9A9184"
    return (f'<svg class="lb-watch" viewBox="0 0 220 220" width="220" height="220">'
            f'<circle cx="{cx}" cy="{cx}" r="{r + 12}" fill="#FFFDF8" stroke="{INK}" stroke-width="5"/>{ticks}'
            f'<circle id="{ident}arc" cx="{cx}" cy="{cx}" r="{r - 22}" fill="none" stroke="{col}" stroke-width="40" '
            f'stroke-dasharray="{circ * (r - 22) / r:.1f}" stroke-dashoffset="{circ * (r - 22) / r:.1f}" transform="rotate(-90 {cx} {cx})" data-frac="{frac:.4f}"/>'
            f'<g id="{ident}hand"><line x1="{cx}" y1="{cx}" x2="{cx}" y2="{cx - r + 16}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g>'
            f'<circle cx="{cx}" cy="{cx}" r="9" fill="{INK}"/></svg>')


def lb_split(c: SceneCtx, d: dict) -> SceneOut:
    """Top: the reconstruction (still or clip, y 290-760). Bottom: the measurement as stopwatches that run to the
    reported values at the spoken words. Values come from the paper; `max` scales the arcs."""
    out = SceneOut(html="")
    s = c.sid
    _chk("lb_split", "headline", d.get("headline", ""), "headline", out)
    watches, note = d.get("watches") or [], d.get("note") or {}
    _chk("lb_split", "note", note.get("text", ""), "note.text", out)
    vmax = float(d.get("max", 20))
    top_h = SPLIT_H
    img = ""
    clip_len = float(d.get("clip_len", 8.0))
    if d.get("image"):
        hold = 'opacity:0;' if d.get("clip") else ""
        img = f'<img class="lb-phimg" id="{s}img" src="{_media(d["image"])}" alt="" style="{hold}object-position:50% {int(d.get("focus", 50))}%">'
    y0 = WIN_Y + top_h + 24
    slot = CW // max(1, len(watches))
    wh = []
    for i, w in enumerate(watches):
        for k, n in (("label", "label"), ("value", "value"), ("unit", "unit")):
            _chk("lb_split", n, w.get(k, ""), f"watches[{i}].{k}", out)
        x = CL + i * slot + (slot - 220) // 2
        wh.append(f'<div class="lb-wl" id="{s}wl{i}" style="left:{CL + i * slot}px;top:{y0 + 62}px;width:{slot}px">{_e(w.get("label", ""))}</div>'
                  f'<div class="lb-wbox" style="left:{x}px;top:{y0 + 106}px">{_watch(f"{s}w{i}", min(1.0, float(w.get("to", 0)) / vmax), w.get("kind", "a"))}</div>'
                  f'<div class="lb-wv" id="{s}wv{i}" style="left:{CL + i * slot}px;top:{y0 + 330}px;width:{slot}px"><b>{_e(w.get("value", ""))}</b> {_e(w.get("unit", ""))}</div>')
    tag = RECON.get(c.lang, RECON["de"])
    cite = d.get("cite", "")
    _chk("lb_split", "cite", cite, "cite", out)
    out.html = f"""<div class="lb-in lb-ph">
  <div class="lb-phwin" style="top:{WIN_Y}px;height:{top_h}px">{img}<div class="lb-phshade"></div></div>
  <div class="lb-phtag" style="top:{WIN_Y + 20}px"><i></i>{_e(tag)}</div>
  <div class="lb-splitpage" style="top:{WIN_Y + top_h}px;height:{WIN_H - top_h}px"></div>
  <div class="lb-h" style="top:{y0}px">{_e(d.get("headline", ""))}</div>
  {"".join(wh)}
  {f'<div class="lb-rnote" style="top:{y0 + 404}px"><span>{_e(note.get("text", ""))}</span></div>' if note.get("text") else ""}
  {f'<div class="lb-cite" style="top:{CITE_Y}px">{_e(cite)}</div>' if cite else ""}
</div>"""
    _frame(c, False, out)
    out.tl.append(f'tl.fromTo("#{s} .lb-phwin",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.32,ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .lb-splitpage",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{c.t(0.1):.3f});')
    out.events += [round(c.start, 3), c.t(0.1)]
    if img and d.get("clip"):
        if c.duration > clip_len - 0.1:
            out.tl.append(f'tl.set("#{s}img",{{opacity:1}},{c.t(clip_len - 0.08):.3f});')
    elif img:
        out.tl.append(f'tl.fromTo("#{s}img",{{scale:1.06,y:0}},{{scale:1.12,y:-20,duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});')
    out.tl.append(_in(c, ".lb-phtag", 0.15, dx=-16, dy=0))
    out.tl.append(_in(c, ".lb-h", 0.3))
    for i, w in enumerate(watches):
        out.tl.append(_in(c, f"#{s}wl{i}", 0.5 + 0.2 * i, dy=10))
        run_at = _rel(c, w.get("start_at", 1.0), 1.0, out)
        stop_at = _rel(c, w.get("at", run_at + 3.0), run_at + 3.0, out)
        dur = max(0.6, stop_at - run_at)
        frac = min(1.0, float(w.get("to", 0)) / vmax)
        full = 2 * 3.14159 * 92 * 70 / 92
        out.tl.append(f'tl.to("#{s}w{i}arc",{{strokeDashoffset:{full * (1 - frac):.1f},duration:{dur:.2f},ease:"none"}},{c.t(run_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}w{i}hand",{{rotation:0,svgOrigin:"110 110"}},{{rotation:{360 * frac:.1f},svgOrigin:"110 110",duration:{dur:.2f},ease:"none"}},{c.t(run_at):.3f});')
        out.tl.append(_pop(c, f"#{s}wv{i}", stop_at))
        out.events += [c.t(run_at), c.t(stop_at)]
    if note.get("text"):
        at = _rel(c, note.get("at", c.duration - 2.0), c.duration - 2.0, out)
        out.tl.append(_pop(c, ".lb-rnote span", at))
        out.events.append(c.t(at))
    return out


TEMPLATES = {"lb_hook": lb_hook, "lb_setup": lb_setup, "lb_measure": lb_measure, "lb_result": lb_result,
             "lb_verdict": lb_verdict, "lb_try": lb_try, "lb_replicate": lb_replicate, "lb_photo": lb_photo, "lb_split": lb_split}


# --- format layer: room, notebook page, protocol strip, honesty line ---------------------------------------

def _protocol_marks(plan, captions) -> list[tuple[float, int]]:
    """(absolute time, step index) for every protocol change, from the scene type defaults or data.protocol."""
    words = [w for g in (captions or []) for w in g.words]
    marks: list[tuple[float, int]] = []
    for b in plan.beats:
        if b.start is None:
            continue
        spec = (b.data or {}).get("protocol")
        if spec is None:
            spec = DEFAULT_STEP.get(b.scene_type)
            if b.scene_type == "lb_verdict":
                st_at = ((b.data or {}).get("status") or {}).get("at")
                spec = [{"step": 4, "at": 0}, {"step": 5, "at": st_at if st_at is not None else b.duration * 0.55}]
        if spec is None:
            continue
        bw = [w for w in words if b.start <= w.start < b.start + b.duration]
        for item in (spec if isinstance(spec, list) else [{"step": spec, "at": 0}]):
            rel, _ = _anchor(bw, b.start, item.get("at", 0), 0.0)
            marks.append((round(b.start + rel, 3), int(item["step"])))
    # two marks at the same moment (e.g. an anchor that is not spoken): keep only the later step
    dedup = {}
    for t, st in sorted(marks):
        dedup[t] = st
    return sorted(dedup.items())


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: N802 (contract name)
    lang = getattr(plan, "language", "de")
    lay = getattr(plan, "layout", None) or {}
    lb = lay.get("laborbuch") or {}
    steps = STEPS.get(lang, STEPS["de"])
    marks = _protocol_marks(plan, captions)
    boxes = "".join(f'<i class="lbx-box" id="lbx-b{i}"><b id="lbx-f{i}"></b></i>' for i in range(len(steps)))
    names = "".join(f'<span class="lbx-name" id="lbx-n{i}"><em>{i + 1}/{len(steps)}</em>{_e(nm)}</span>' for i, nm in enumerate(steps))
    no, study = _e(lb.get("no", "")), _e(lb.get("study", ""))
    media_dir = Path(project_dir) / MEDIA_DIR
    clips = []
    for b in plan.beats:
        dd = b.data or {}
        for key in ("image", "clip"):
            if dd.get(key):
                src = next((r / dd[key] for r in MEDIA_ROOTS if (r / dd[key]).exists()), MEDIA_ROOTS[0] / dd[key])
                media_dir.mkdir(parents=True, exist_ok=True)
                if src.exists():
                    shutil.copy2(src, media_dir / dd[key])
        if dd.get("clip") and b.start is not None:
            top_h = SPLIT_H if b.scene_type == "lb_split" else WIN_H
            vdur = min(b.duration, float(dd.get("clip_len", 8.0)))
            clips.append(f'<video id="gwv-{b.id}" class="clip gwv{" gws" if b.scene_type == "lb_split" else ""}" src="{MEDIA_DIR}/{html.escape(dd["clip"])}" data-start="{b.start:.3f}" '
                         f'data-duration="{vdur:.3f}" data-track-index="1" data-volume="0" muted playsinline '
                         f'style="object-position:50% {int(dd.get("focus", 50))}%"></video>')
    head_l = "LABORBUCH" if lang == "de" else "LAB NOTEBOOK"
    vno = ("Versuch " if lang == "de" else "Experiment ") + no if no else ""
    html_ = f"""<div id="lbx">
<div class="lbx-room"></div><div class="lbx-lamp"></div>
<div class="lbx-page" id="lbx-page" style="left:{PX}px;top:{PY}px;width:{PW}px;height:{PH}px">
  <div class="lbx-grid"></div><div class="lbx-margin"></div><div class="lbx-gloss"></div>
  <div class="lbx-head"><span><b>{head_l}</b>{(" · " + vno) if vno else ""}</span><span class="lbx-study">{study}</span></div>
</div>
<div class="lbx-proto" id="lbx-proto"><span class="lbx-boxes">{boxes}</span><span class="lbx-names">{names}</span></div>
<div class="lbx-honest" id="lbx-honest"><i></i>{_e(HONEST.get(lang, HONEST["de"]))}</div>
</div>""" + "".join(clips)
    # the notebook page hides while a reconstruction fills the window (lb_photo, lb_split) and comes back after it
    photo_types = ("lb_photo", "lb_split")
    timed = [bb for bb in plan.beats if bb.start is not None]
    page_js = []
    shown = None
    for bb in timed:
        want = bb.scene_type not in photo_types
        if want != shown:
            if want:
                page_js.append(f'T.fromTo("#lbx-page",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{bb.start:.3f});')
            else:
                page_js.append(f'T.set("#lbx-page",{{opacity:0}},{bb.start:.3f});')
            shown = want
    js = ['T.set("#lbx-page",{opacity:0},0);'] + page_js + [
          'T.fromTo("#lbx-proto",{opacity:0,y:-10},{opacity:1,y:0,duration:0.4},0.1);',
          'T.fromTo("#lbx-honest",{opacity:0},{opacity:1,duration:0.4},0.2);',
          f'T.fromTo(".lbx-lamp",{{x:-40,y:20}},{{x:40,y:-20,duration:{max(1.0, plan.beats[-1].start + plan.beats[-1].duration):.2f},ease:"sine.inOut"}},0);']
    for i in range(len(steps)):
        js.append(f'T.set("#lbx-n{i}",{{opacity:0}},0);')
    events, prev = [], None
    for t, step in marks:
        step = max(0, min(len(steps) - 1, step))
        if prev is not None:
            js.append(f'T.to("#lbx-n{prev}",{{opacity:0,y:-12,duration:0.2}},{max(0.0, t - 0.2):.3f});')
        js.append(f'T.fromTo("#lbx-n{step}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{t:.3f});')
        for k in range(step + 1):
            js.append(f'T.to("#lbx-f{k}",{{scale:1,opacity:{1 if k == step else 0.55},duration:0.3,ease:"back.out(2)"}},{t:.3f});')
        js.append(f'T.fromTo("#lbx-b{step}",{{scale:1.25}},{{scale:1,duration:0.35,ease:"power2.out"}},{t:.3f});')
        events.append(t)
        prev = step
    css = f"""<style>
#lbx{{position:absolute;inset:0;overflow:hidden;pointer-events:none;background:#121110;}}  /* z auto: clips placed after it stay visible, scenes stay on top */
.lbx-room{{position:absolute;inset:0;background:radial-gradient(ellipse 120% 80% at 50% 38%,#26211B 0%,#17140F 55%,#0C0B09 100%);}}
.lbx-lamp{{position:absolute;left:-200px;top:-260px;width:1100px;height:1000px;background:radial-gradient(ellipse at 40% 40%,rgba(242,196,110,0.20) 0%,rgba(229,180,90,0.07) 45%,transparent 70%);}}
.lbx-page{{position:absolute;background:{PAPER};border-radius:6px 14px 14px 6px;box-shadow:0 2px 2px rgba(0,0,0,0.3),0 20px 40px rgba(0,0,0,0.45),0 60px 120px rgba(0,0,0,0.5);overflow:hidden;}}
.lbx-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(60,90,110,0.13) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba(60,90,110,0.13) 1.5px,transparent 1.5px);
  background-size:32px 32px;background-position:8px 8px;}}
.lbx-margin{{position:absolute;left:24px;top:0;bottom:0;width:6px;border-left:2px solid rgba(194,69,47,0.35);border-right:2px solid rgba(194,69,47,0.35);}}
.lbx-gloss{{position:absolute;inset:0;background:linear-gradient(150deg,rgba(255,255,255,0.5) 0%,rgba(255,255,255,0) 35%),radial-gradient(ellipse at 100% 100%,rgba(125,116,106,0.18),transparent 55%);}}
.lbx-head{{position:absolute;left:40px;right:40px;top:22px;height:44px;display:flex;align-items:center;justify-content:space-between;gap:20px;
  border-bottom:3px solid {INK};font-family:'FN Inter';font-size:24px;font-weight:600;letter-spacing:0.06em;color:{PMUTED};white-space:nowrap;}}
.lbx-head b{{color:{GOLD_INK};font-weight:700;}}
.lbx-study{{color:{INK};letter-spacing:0.02em;}}
.lbx-proto{{position:absolute;left:108px;top:194px;display:flex;align-items:center;gap:22px;height:40px;}}
.lbx-boxes{{display:flex;gap:9px;}}
.lbx-box{{position:relative;display:block;width:30px;height:30px;border-radius:8px;border:3px solid rgba(229,180,90,0.45);}}
.lbx-box b{{position:absolute;inset:-3px;border-radius:8px;background:{GOLD};opacity:0;transform:scale(0);}}
.lbx-names{{position:relative;display:block;width:520px;height:40px;}}
.lbx-name{{position:absolute;left:0;top:0;white-space:nowrap;font-family:'FN Fraunces';font-weight:700;font-size:34px;line-height:40px;color:#F4F0E8;font-variation-settings:"SOFT" 60,"opsz" 48;}}
.lbx-name em{{font-style:normal;font-family:'FN Inter';font-size:24px;font-weight:600;color:{GOLD};letter-spacing:0.06em;margin-right:14px;}}
.lbx-honest{{position:absolute;left:108px;top:246px;display:flex;align-items:center;gap:12px;font-family:'FN Inter';font-size:27px;font-weight:600;letter-spacing:0.01em;color:#E2DACD;white-space:nowrap;}}
.lbx-honest i{{display:inline-block;width:14px;height:14px;border-radius:50%;border:3px solid {GOLD};}}
</style>"""
    body_end = ("<script>(function(){var T=window.__timelines&&window.__timelines.main;if(!T)return;\n"
                + "\n".join(js) + "\nT.seek(0);})();</script>")
    return {"head_html": css, "under_scenes_html": html_, "body_end_html": body_end, "events": events}


def MANIFEST_EXTRA(plan) -> dict:  # noqa: N802 (contract name)
    used = sorted({b.scene_type for b in plan.beats if b.scene_type.startswith("lb_")})
    if not used:
        return {}
    lb = (getattr(plan, "layout", None) or {}).get("laborbuch") or {}
    return {"format": {"name": "Gritwerk Format \"Laborbuch\"", "version": "0.1 (Pilot)",
                       "bible": "OneDrive\\Business\\02 Marke\\Gritwerk\\Format-Bibel.md", "scene_types": used,
                       "experiment": lb.get("study", ""), "replication_status": lb.get("status", ""),
                       "visuals": "Animation aus HTML/SVG/CSS; Teilnehmende nur als Punkte; Zahlen aus der Veröffentlichung; "
                                  "veröffentlichter Versuch, nacherzählt, nicht selbst durchgeführt",
                       "ai_images": "keine (nur Code-Grafik)"}}


# --- CSS ----------------------------------------------------------------------------------------------------

def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat=False) -> str:  # noqa: N802
    D, B = f"'FN {display}'", f"'FN {body}'"
    return f"""
/* Gritwerk format "Laborbuch" (brands/motivation/laborbuch/scenes.py) */
.lb-in{{position:absolute;inset:0;}}
.lb-in > *{{position:absolute;}}
.lb-turn{{position:absolute;left:{PX}px;top:{PY + 80}px;width:{PW}px;height:{PH - 80}px;z-index:5;background:{PAPER};
  background-image:linear-gradient(rgba(60,90,110,0.13) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba(60,90,110,0.13) 1.5px,transparent 1.5px);
  background-size:32px 32px;background-position:8px 0px;opacity:0;box-shadow:0 10px 30px rgba(0,0,0,0.35);}}
.lb-turnshade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(27,23,18,0) 0%,rgba(27,23,18,0.6) 100%);opacity:0;}}
.lb-h{{left:{CL}px;width:{CW}px;font-family:{D};font-weight:700;font-size:52px;line-height:1.08;color:{INK};font-variation-settings:"SOFT" 70,"opsz" 72;letter-spacing:-0.01em;}}
.lb-q{{left:{CL}px;width:{CW}px;font-family:{D};font-weight:700;font-size:72px;line-height:1.02;color:{INK};font-variation-settings:"SOFT" 80,"opsz" 96;letter-spacing:-0.02em;}}
.lb-cite{{left:{CL}px;width:{CW}px;font-family:{B};font-size:24px;font-weight:600;color:#5E564C;letter-spacing:0;line-height:1.2;white-space:nowrap;}}
.lb-dot{{position:absolute;display:block;border-radius:50%;background:{INK};}}
.lb-nlabel{{left:{CL}px;width:{CW}px;display:flex;align-items:baseline;justify-content:center;gap:16px;font-family:{B};font-size:30px;font-weight:600;color:{PMUTED};}}
.lb-nlabel b{{font-family:{D};font-size:44px;color:{INK};}}
.lb-meta{{left:{CL}px;width:{CW}px;text-align:center;font-family:{B};font-size:26px;font-weight:500;color:{PMUTED};}}
.lb-tease{{left:{CL}px;}}
.lb-tease span{{display:inline-block;font-family:{B};font-size:32px;font-weight:700;color:{INK};border-left:8px solid {INK};padding:4px 0 4px 16px;}}
.lb-stampwrap{{transform:rotate(-7deg);}}
.lb-stamp{{font-family:{D};font-weight:800;font-size:46px;line-height:1;color:#FFF8EC;background:{AMBER};border:4px solid rgba(255,248,236,0.65);
  border-radius:12px;padding:12px 24px;white-space:nowrap;box-shadow:0 10px 24px rgba(0,0,0,0.25);letter-spacing:0.02em;}}
/* setup */
.lb-sheet{{display:flex;align-items:center;gap:16px;background:#FFFDF8;border:3px solid {INK};border-radius:12px;padding:14px 18px;box-sizing:border-box;color:{INK};}}
.lb-sheet b{{display:block;font-family:{D};font-size:30px;line-height:1.1;white-space:nowrap;}}
.lb-sheet span,.lb-arm span{{display:block;font-family:{B};font-size:24px;font-weight:500;color:{PMUTED};margin-top:2px;}}
.lb-ico{{width:52px;height:52px;flex:none;color:{INK};}}
.lb-read{{left:{CL}px;width:{CW}px;text-align:center;}}
.lb-read span{{display:inline-block;font-family:{B};font-size:26px;font-weight:700;color:{INK};background:{PAPER};padding:2px 14px;border-radius:8px;}}
.lb-arrow{{position:absolute;overflow:visible;}}
.lb-arm{{box-sizing:border-box;border-radius:12px;padding:14px 18px;min-height:132px;}}
.lb-arm0{{background:rgba(142,134,123,0.18);border:3px solid #8E867B;}}
.lb-arm1{{background:rgba(229,180,90,0.22);border:3px solid {GOLD};}}
.lb-armhead{{display:flex;align-items:center;gap:12px;}}
.lb-armhead b{{font-family:{D};font-size:31px;line-height:1.05;color:{INK};white-space:nowrap;}}
.lb-armhead .lb-ico{{width:44px;height:44px;}}
.lb-grouplabel{{left:{CL}px;width:{CW}px;font-family:{B};font-size:24px;font-weight:600;color:{PMUTED};letter-spacing:0.04em;text-align:center;}}
.lb-glabel{{text-align:center;}}
.lb-glabel b{{display:block;font-family:{D};font-size:32px;color:{INK};line-height:1.1;}}
.lb-glabel span{{display:block;font-family:{B};font-size:24px;font-weight:600;color:{PMUTED};}}
/* measure */
.lb-textsheet{{width:290px;height:420px;box-sizing:border-box;background:#FFFDF8;border:3px solid {INK};border-radius:12px;padding:16px 20px;}}
.lb-textsheet b{{display:block;font-family:{D};font-size:28px;color:{INK};}}
.lb-textsheet i{{position:absolute;left:22px;height:10px;border-radius:5px;background:rgba(27,23,18,0.22);}}
.lb-cell{{position:absolute;display:block;width:var(--cb,66px);height:var(--cb,66px);box-sizing:border-box;border:3px solid rgba(27,23,18,0.35);border-radius:10px;background:#FFFDF8;}}
.lb-cell b{{position:absolute;inset:6px;border-radius:6px;background:{GOLD};transform:scale(0);}}
.lb-cell em{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-style:normal;font-family:{D};font-size:28px;font-weight:700;color:{INK};}}
.lb-unitlabel{{width:{CW - 330}px;font-family:{B};font-size:26px;font-weight:700;color:{INK};}}
.lb-rule{{left:{CL}px;width:{CW}px;}}
.lb-rule span,.lb-trule span{{display:inline-flex;align-items:center;gap:14px;font-family:{B};font-size:30px;font-weight:700;color:{INK};
  background:rgba(229,180,90,0.30);border:3px solid {GOLD};border-radius:12px;padding:8px 18px;}}
.lb-rule .lb-ico,.lb-trule .lb-ico{{width:40px;height:40px;}}
.lb-sample{{left:{CL}px;width:{CW}px;font-family:{B};font-size:26px;font-weight:600;color:{PMUTED};}}
/* result */
.lb-legend{{left:{CL}px;width:{CW}px;display:flex;gap:34px;}}
.lb-leg{{display:inline-flex;align-items:center;gap:12px;font-family:{B};font-size:28px;font-weight:700;color:{INK};}}
.lb-leg i{{display:inline-block;width:28px;height:28px;border-radius:6px;}}
.lb-ka i,.lb-bar.lb-ka{{background:#9A9184;}}
.lb-kb i,.lb-bar.lb-kb{{background:{GOLD};}}
.lb-unit{{left:{CL}px;width:{CW}px;text-align:right;font-family:{B};font-size:24px;font-weight:500;color:{PMUTED};}}
.lb-hline{{position:absolute;left:{CL}px;width:{CW}px;height:0;border-top:2px dashed rgba(27,23,18,0.14);}}
.lb-tick{{position:absolute;left:{CL - 6}px;font-family:{B};font-size:20px;font-weight:600;color:{PMUTED};background:{PAPER};padding:0 4px;}}
.lb-base{{position:absolute;left:{CL}px;width:{CW}px;height:0;border-top:4px solid {INK};}}
.lb-bar{{position:absolute;display:block;border-radius:8px 8px 0 0;border:3px solid rgba(27,23,18,0.55);border-bottom:none;box-sizing:border-box;}}
.lb-bar.lb-best{{border:4px solid {INK};border-bottom:none;}}
.lb-val{{text-align:center;white-space:nowrap;font-family:{D};font-weight:700;font-size:40px;color:{PMUTED};}}
.lb-val.lb-best{{color:{INK};}}
.lb-gx{{text-align:center;font-family:{B};font-size:28px;font-weight:700;color:{INK};}}
.lb-turnmark{{width:240px;text-align:center;}}
.lb-turnmark span{{display:inline-block;font-family:{B};font-size:26px;font-weight:700;color:#FFF8EC;background:{AMBER};border-radius:8px;padding:2px 12px;}}
.lb-turnmark svg{{display:block;margin:2px auto 0;}}
.lb-gap{{text-align:center;}}
.lb-gap span{{display:inline-block;white-space:nowrap;font-family:{D};font-size:30px;font-weight:700;color:{INK};background:rgba(229,180,90,0.35);border-radius:8px;padding:2px 14px;}}
/* photo (AI reconstruction) */
.lb-ph .lb-phwin{{position:absolute;left:0;width:1080px;overflow:hidden;background:transparent;}}
.lb-phimg{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}}
.lb-phshade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,9,8,0.55) 0%,rgba(10,9,8,0) 22%,rgba(10,9,8,0) 70%,rgba(10,9,8,0.55) 100%);}}
.lb-phtag{{left:{CL - 24}px;display:flex;align-items:center;gap:10px;font-family:{B};font-size:24px;font-weight:600;color:#F4F0E8;
  background:rgba(18,17,16,0.72);border-radius:8px;padding:6px 14px;white-space:nowrap;}}
.lb-phtag i{{display:inline-block;width:12px;height:12px;border-radius:50%;background:{AMBER};}}
.lb-phtitle{{left:{CL - 24}px;width:{CW + 24}px;font-family:{D};font-weight:700;font-size:78px;line-height:1.02;color:#FFF8EC;
  text-shadow:0 4px 30px rgba(0,0,0,0.65);font-variation-settings:"SOFT" 80,"opsz" 96;letter-spacing:-0.02em;}}
.lb-pin{{position:absolute;display:block;width:28px;height:28px;border-radius:50%;background:{GOLD};border:5px solid #FFF8EC;box-shadow:0 0 0 6px rgba(229,180,90,0.35);box-sizing:border-box;}}
.lb-pinl{{width:420px;}}
.lb-pinl.lb-pin-left{{text-align:right;}}
.lb-pinl span{{display:inline-block;font-family:{B};font-size:30px;font-weight:700;color:{INK};background:#FFF8EC;border-radius:10px;padding:6px 14px;box-shadow:0 8px 20px rgba(0,0,0,0.35);}}
.lb-phcite{{left:{CL - 24}px;width:{CW + 24}px;font-family:{B};font-size:24px;font-weight:600;color:#F4F0E8;text-shadow:0 2px 10px rgba(0,0,0,0.8);}}
.lb-splitpage{{position:absolute;left:{PX}px;width:{PW}px;background:{PAPER};border-radius:0 0 14px 6px;
  background-image:linear-gradient(rgba(60,90,110,0.13) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba(60,90,110,0.13) 1.5px,transparent 1.5px);background-size:32px 32px;}}
.lb-wl{{text-align:center;font-family:{D};font-size:34px;font-weight:700;color:{INK};}}
.lb-wbox{{position:absolute;}}
.lb-wv{{text-align:center;font-family:{B};font-size:28px;font-weight:600;color:#5E564C;}}
.lb-wv b{{font-family:{D};font-size:52px;color:{INK};}}
/* the runtime positions clips itself; the window position needs priority over its inline styles */
.gwv{{position:absolute;object-fit:cover;inset:auto!important;left:0!important;top:{WIN_Y}px!important;width:1080px!important;height:{WIN_H}px!important;}}
.gwv.gws{{height:{SPLIT_H}px!important;}}
/* replicate */
.lb-axlabel{{left:{CL}px;width:{CW}px;font-family:{B};font-size:26px;font-weight:600;color:#5E564C;}}
.lb-zero{{position:absolute;display:block;width:4px;background:{INK};}}
.lb-zerol{{width:240px;text-align:center;font-family:{B};font-size:24px;font-weight:700;color:{INK};}}
.lb-axt{{width:80px;text-align:center;font-family:{B};font-size:24px;font-weight:600;color:#5E564C;}}
.lb-rlabel{{left:{CL}px;width:{CW}px;}}
.lb-rlabel b{{display:block;font-family:{D};font-size:38px;line-height:1.1;color:{INK};}}
.lb-rlabel span{{display:block;font-family:{B};font-size:26px;font-weight:600;color:#5E564C;margin-top:2px;}}
.lb-track{{position:absolute;display:block;left:{CL}px;width:{CW}px;height:0;border-top:2px dashed rgba(27,23,18,0.25);}}
.lb-ci{{position:absolute;display:block;height:10px;border-radius:5px;}}
.lb-ci.lb-ka{{background:#9A9184;}} .lb-ci.lb-kb{{background:{GOLD};}}
.lb-pt{{position:absolute;display:block;width:34px;height:34px;border-radius:50%;border:4px solid {INK};box-sizing:border-box;}}
.lb-pt.lb-ka{{background:#9A9184;}} .lb-pt.lb-kb{{background:{GOLD};}}
.lb-ptval.lb-ptl{{text-align:right;}}
.lb-ptval{{width:200px;text-align:left;font-family:{D};font-size:34px;font-weight:700;color:{INK};}}
.lb-rnote{{left:{CL}px;width:{CW}px;}}
.lb-rnote span{{display:inline-block;font-family:{B};font-size:30px;font-weight:700;color:{INK};background:rgba(229,180,90,0.30);border:3px solid {GOLD};border-radius:12px;padding:8px 18px;}}
/* verdict */
.lb-limit{{left:{CL}px;width:{CW}px;display:flex;align-items:center;gap:16px;font-family:{B};font-size:30px;font-weight:600;color:{INK};}}
.lb-limit i{{flex:none;width:26px;height:26px;border-radius:26px 26px 0 0;background:{AMBER};margin-top:-6px;}}
.lb-sep{{position:absolute;left:{CL}px;width:{CW}px;height:0;border-top:3px solid {INK};}}
.lb-sthead{{left:{CL}px;font-family:{D};font-weight:700;font-size:40px;color:{INK};}}
.lb-levels{{left:{CL}px;display:flex;flex-wrap:wrap;gap:10px 22px;width:480px;}}
.lb-lv{{display:inline-flex;align-items:center;gap:8px;font-family:{B};font-size:27px;font-weight:600;color:#5E564C;}}
.lb-lv i{{display:inline-block;width:22px;height:22px;border-radius:5px;border:3px solid var(--c);}}
.lb-lv.on{{color:{INK};font-weight:800;}}
.lb-lv.on i{{background:var(--c);}}
.lb-vstamp .lb-stamp{{padding:12px 28px;}}
.lb-ev{{left:{CL}px;width:{CW}px;border-left:8px solid {GREEN};padding-left:18px;box-sizing:border-box;}}
.lb-ev b{{display:block;font-family:{B};font-size:28px;font-weight:700;color:{INK};line-height:1.15;}}
.lb-ev span{{display:block;font-family:{B};font-size:24px;font-weight:600;color:#5E564C;margin-top:2px;}}
/* try */
.lb-slip{{left:{CL - 18}px;width:{CW + 36}px;box-sizing:border-box;background:#FFFDF8;border:3px dashed {GOLD_INK};border-radius:16px;box-shadow:0 8px 20px rgba(27,23,18,0.12);}}
.lb-ht{{left:{CL + 10}px;width:{CW - 20}px;color:{GOLD_INK};}}
.lb-step{{left:{CL + 10}px;width:{CW - 20}px;display:flex;align-items:center;gap:18px;font-family:{B};font-size:30px;font-weight:600;color:{INK};line-height:1.15;}}
.lb-step i{{flex:none;display:flex;align-items:center;justify-content:center;width:52px;height:52px;border-radius:12px;background:{GOLD};
  font-style:normal;font-family:{D};font-size:32px;font-weight:800;color:{INK};}}
.lb-trule{{left:{CL + 10}px;width:{CW - 20}px;}}
.lb-caveat{{left:{CL + 10}px;width:{CW - 20}px;display:flex;align-items:center;gap:14px;font-family:{B};font-size:28px;font-weight:600;color:{INK};}}
.lb-caveat i{{flex:none;width:26px;height:26px;border-radius:26px 26px 0 0;background:{AMBER};margin-top:-6px;}}
.lb-sign{{left:{CL}px;width:{CW}px;display:flex;align-items:center;gap:16px;}}
.lb-signmark{{width:46px;height:46px;}}
.lb-sign b{{font-family:{B};font-size:34px;font-weight:800;letter-spacing:0.16em;color:{INK};}}
.lb-claim{{font-family:{D};font-size:36px;font-weight:700;color:{GOLD_INK};margin-left:8px;}}
.lb-disc{{left:{CL}px;width:{CW}px;font-family:{B};font-size:25px;font-weight:500;color:{PMUTED};}}
"""
