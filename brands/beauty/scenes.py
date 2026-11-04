"""Dewlane scene variants (brand module, loaded by fn.render.brand_scenes; docs/direction-system.md, 6d).

Quality round Q1 (31.10.2026, briefing OneDrive Business/02 Marke/Qualitätsrunde 2026-10-31.md): every scene is a
Dewlane scene built around one lead object, the INCI label of an unbranded cream (white porcelain card, header
"Ingredients", abstract line bars). The label is large (740-800 px of the 864 px content width) and changes its state
with the story; several image events per scene sit on spoken words. A brand-wide LAYER draws the background with
depth (window light from the top left, light shafts, cream ribbons, glass flacon and jar, dew drops in three parallax
planes, paper grain, warm edge shade), only HTML/SVG/CSS, moved by the GSAP timeline (deterministic for seeking).

| scene type     | Dewlane scene (Q1)                                   | data (times: seconds from beat start or "w:Wort") |
|----------------|------------------------------------------------------|---------------------------------------------------|
| cinematic_hook | drop lands on line 1 of the label, ring, question    | question, badge, fly_at, ring_at, question_at, badge_at, lines |
| data_flow      | label + EU glossary; a glossary name flies onto the  | headline, label_at, head_at, gloss_at, word, word_line, word_at, meaning, |
|                | label (example position: overlay example: true)      | meaning_at, gloss_title, gloss_sub, gloss_note    |
| file_beside    | label lines become a weight chart (descending),      | headline, weights_at, drops_at, tag, tag_at, front_at, front_tag, front_tag_at |
|                | drops fall into a bowl, line 1 = largest amount      |                                                   |
| file_fork      | dashed 1 % line, lines below it swap places, the     | headline, end_at, line_at, shuffle_at, fade_at, chip, chip_at, upper, lower |
|                | line fades: the limit is not printed                 |                                                   |
| comparison     | label with empty percent fields + two cards          | headline, read_at, front_at, pct_at, left/right{title, rows[{text, at}]} |
| key_takeaway   | three numbered callouts on the label + CosIng card   | headline, items[{title, sub, at}], word (row 5), cosing_title, cosing_sub, cosing_at, db_at |
| file_close     | reading sweep, the gate "Erst die Liste lesen" opens | headline, read_at, done_at, unlock_at, brand_at, button, block_text, done_text, |
|                | the button, then the Dewlane sign-off (>= 4 s)       | domain, claim, disclaimer                         |

Label lines are abstract bars, never a real formula. Where a scene puts a name on a line (AQUA, PARFUM) the position
is an example; the plan sets overlay.example so the "Beispielwert" chip is shown.

Word anchors: any time field (`at` or `*_at`, also inside lists) may be "w:Wort" or "w:Wort#2"; it resolves to the
start of that word in the beat, relative to the beat start. A word that is not spoken is a problem in the report and
the field falls back to 0.5 s.

Animated elements carry no CSS transform (GSAP would fold a percentage translate into px); vertical centring uses
top/margin-top instead.
"""
from __future__ import annotations

import re

from fn.render.templates import SceneCtx, SceneOut, _e


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", str(s).lower())


def _resolve(c: SceneCtx, d, problems: list[str], key: str = ""):
    """Copy of the beat data with every 'w:Wort[#n]' time field replaced by seconds from the beat start."""
    if isinstance(d, dict):
        return {k: _resolve(c, v, problems, k) for k, v in d.items()}
    if isinstance(d, list):
        return [_resolve(c, v, problems, key) for v in d]
    if isinstance(d, str) and (key == "at" or key.endswith("_at")) and d.startswith("w:"):
        m = re.fullmatch(r"w:(.+?)(?:#(\d+))?", d.strip())
        stem, nth = _norm(m.group(1)), int(m.group(2) or 1)
        hits = [w for w in (c.words or []) if _norm(w.text).startswith(stem)]
        if len(hits) < nth:
            problems.append(f"anchor {d!r} ({key}) not spoken in this beat")
            return 0.5
        return round(max(0.0, hits[nth - 1].start - c.start), 3)
    return d


_FT = re.compile(r'^tl\.fromTo\("([^"]+)",\{[^{}]*\},\{.*\},([\d.]+)\);$')


def _baseline(tl: list[str]) -> list[str]:
    """Several fromTo on one element: only the earliest renders its from-values at authoring time (HyperFrames lint
    gsap_repeated_fromto_without_baseline); the later ones get immediateRender:false."""
    groups: dict[str, list[tuple[float, int]]] = {}
    for i, line in enumerate(tl):
        m = _FT.match(line)
        if m:
            groups.setdefault(m.group(1), []).append((float(m.group(2)), i))
    for lst in groups.values():
        first = min(lst)[1]
        for _, i in lst:
            if i != first:
                tl[i] = re.sub(r"\},([\d.]+)\);$", r",immediateRender:false},\1);", tl[i])
    return tl


def _anchored(fn):
    def wrapped(c: SceneCtx, d: dict) -> SceneOut:
        problems: list[str] = []
        out = fn(c, _resolve(c, d, problems))
        out.tl = _baseline(list(out.tl))
        out.problems = list(out.problems) + problems
        return out
    wrapped.__name__ = f"dw_{fn.__name__}"
    return wrapped


DROP = "M0 -150 C-30 -95 -110 -10 -110 60 A110 110 0 0 0 110 60 C110 -10 30 -95 0 -150 Z"
BAR_WIDTHS = [86, 70, 78, 58, 66, 48, 60]
STAGE_TOP = 160                     # title block 0..150, stage below it (zone 290..1100 in the frame)

LIMITS = {
    "cinematic_hook": {"question": 52, "badge": 22},
    "data_flow": {"headline": 34, "word": 12, "meaning": 18, "gloss_title": 20, "gloss_sub": 34, "gloss_note": 30},
    "file_beside": {"headline": 34, "tag": 30, "front_tag": 26},
    "file_fork": {"headline": 34, "chip": 30, "upper": 30, "lower": 30},
    "comparison": {"headline": 34},
    "key_takeaway": {"headline": 34, "word": 12, "cosing_title": 16, "cosing_sub": 34},
    "file_close": {"headline": 34, "button": 16, "block_text": 30, "done_text": 30, "domain": 16, "claim": 32, "disclaimer": 34},
}


# --- small helpers ---------------------------------------------------------------------------------

def _ft(sel: str, frm: str, to: str, at: float) -> str:
    return f'tl.fromTo("{sel}",{{{frm}}},{{{to}}},{at:.3f});'


def _to(sel: str, to: str, at: float) -> str:
    return f'tl.to("{sel}",{{{to}}},{at:.3f});'


def _f(d: dict, key: str, default: float) -> float:
    v = d.get(key, default)
    return float(v) if isinstance(v, (int, float)) else float(default)


def _near(c: SceneCtx, rel: float) -> float:
    """Start of the spoken word nearest to `rel` seconds after the beat start (falls back to `rel`)."""
    starts = [round(w.start - c.start, 3) for w in (c.words or [])]
    return min(starts, key=lambda x: abs(x - rel)) if starts else rel


def _fw(c: SceneCtx, d: dict, key: str, frac: float) -> float:
    """Explicit time if given, else the spoken word nearest to `frac` of the beat (a value > 1 means seconds)."""
    v = d.get(key)
    if isinstance(v, (int, float)):
        return float(v)
    return _near(c, frac if frac > 1 else c.duration * frac)


def _frame(c: SceneCtx, title: str, body: str, *, push: float = 1.035) -> tuple[str, list[str]]:
    """Scene root (.dl), centred title (max two lines) and the stage with a slow push-in over the whole beat."""
    s = c.sid
    head = f'<div class="dl-title" id="{s}-title">{_e(title)}</div>' if title else ""
    html = f'<div class="dl" id="{s}-dl">{head}<div class="dl-stage{"" if title else " full"}" id="{s}-stage">{body}</div></div>'
    tl = [
        _ft(f"#{s}-dl", "opacity:0", f'opacity:1,duration:{c.enter:.2f},ease:"power2.out"', c.start),
        _to(f"#{s}-dl", 'opacity:0,duration:0.18,ease:"power2.in"', max(c.start + c.enter + 0.05, c.end - 0.18)),
        _ft(f"#{s}-stage", "scale:1,y:0", f'scale:{push},y:-8,duration:{c.duration:.2f},ease:"none"', c.start),
    ]
    if title:
        tl.append(_ft(f"#{s}-title", "opacity:0,y:-18", 'opacity:1,y:0,duration:0.5,ease:"power3.out"', c.t(0.05)))
    return html, tl


def _label(s: str, *, x: int, y: int, w: int, n: int, pitch: int = 56, head: int = 96, nums: bool = True,
           weights: list[int] | None = None, words: dict[int, str] | None = None, tag: str = "INCI-Liste",
           head_extra: str = "", bar_frac: float = 1.0, gap_after: dict[int, int] | None = None,
           pct: bool = False) -> tuple[str, dict]:
    """The INCI label (lead object), absolute geometry so other elements can aim at a row.
    Returns (html, geo): geo["cy"][i] = row centre y, geo["bar_x"] = left edge of the bars (stage px)."""
    pad, num_w = 40, (46 if nums else 0)
    wcol = 230 if weights else (150 if pct else 0)
    area = int((w - 2 * pad - num_w - wcol - (28 if wcol else 0)) * bar_frac)
    gap_after = gap_after or {}
    words = words or {}
    rows, cy, top = [], [], head + 16
    for i in range(n):
        bw = BAR_WIDTHS[i % len(BAR_WIDTHS)]
        num = f'<span class="dl-num">{i + 1}</span>' if nums else ""
        word = f'<b class="dl-word" id="{s}-word{i}" style="left:{num_w}px">{_e(words[i])}</b>' if i in words else ""
        extra = ""
        if weights:
            extra = (f'<span class="dl-wcol" style="left:{num_w + area + 28}px;width:{wcol}px">'
                     f'<i class="dl-wt" id="{s}-wt{i}" style="width:{weights[i] if i < len(weights) else 10}%"></i></span>')
        elif pct:
            extra = f'<span class="dl-pct" id="{s}-pct{i}" style="left:{num_w + area + 28}px;width:{wcol}px">? %</span>'
        rows.append(f'<div class="dl-row" id="{s}-r{i}" style="top:{top}px;height:{pitch}px">'
                    f'<i class="dl-hl" id="{s}-hl{i}"></i>{num}'
                    f'<i class="dl-bar{" strong" if i < 2 else ""}" id="{s}-bar{i}" style="left:{num_w}px;width:{int(area * bw / 100)}px"></i>'
                    f'{word}{extra}</div>')
        cy.append(y + top + pitch // 2)
        top += pitch + gap_after.get(i, 0)
    h = top + 22
    tag_html = f'<span class="dl-tag" id="{s}-tag">{_e(tag)}</span>' if tag else ""
    html = (f'<div class="dl-card dl-label" id="{s}-lab" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="dl-lab-head" style="height:{head}px"><span class="dl-ing" id="{s}-ing">Ingredients'
            f'<i class="dl-under" id="{s}-under"></i></span>{tag_html}{head_extra}</div>{"".join(rows)}</div>')
    return html, {"cy": cy, "bar_x": x + pad + num_w, "area": area, "h": h, "x": x, "y": y, "w": w, "head": head,
                  "wcol_x": x + pad + num_w + area + 28, "top0": y + head + 16, "pitch": pitch}


def _bars_in(s: str, n: int, at: float, step: float = 0.07) -> list[str]:
    return [_ft(f"#{s}-bar{i}", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.4,ease:"power2.out"', at + i * step)
            for i in range(n)]


def _card_in(sel: str, at: float, dy: int = 50) -> str:
    return _ft(sel, f"opacity:0,y:{dy}", 'opacity:1,y:0,duration:0.55,ease:"power3.out"', at)


def _pop(sel: str, at: float) -> str:
    return _ft(sel, "opacity:0,scale:0.7", 'opacity:1,scale:1,duration:0.35,ease:"back.out(2)"', at)


ICON = {
    "book": '<svg viewBox="0 0 48 48"><path d="M6 11h14a4 4 0 0 1 4 4v24a3 3 0 0 0-3-3H6z"/><path d="M42 11H28a4 4 0 0 0-4 4v24a3 3 0 0 1 3-3h15z"/></svg>',
    "lens": '<svg viewBox="0 0 48 48"><circle cx="20" cy="20" r="12"/><path d="M29 29l12 12"/></svg>',
    "drop": '<svg viewBox="0 0 48 48"><path d="M24 6C20 13 11 22 11 30a13 13 0 0 0 26 0c0-8-9-17-13-24z"/></svg>',
    "scale": '<svg viewBox="0 0 48 48"><path d="M24 8v32M12 40h24M8 16h32M8 16l-5 12a6 6 0 0 0 10 0zM40 16l-5 12a6 6 0 0 0 10 0z"/></svg>',
}


def _icon(name: str, cls: str = "dl-ico") -> str:
    return f'<span class="{cls}">{ICON[name]}</span>'


def _drop_svg(pal: dict, cls: str, ident: str, style: str = "") -> str:
    blush = pal.get("blush", pal["accent"])
    return (f'<svg class="{cls}" id="{ident}" style="{style}" viewBox="-120 -160 240 290"><defs><radialGradient id="{ident}-g" cx="40%" cy="58%" r="68%">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.98"/><stop offset="0.55" stop-color="{blush}" stop-opacity="0.6"/>'
            f'<stop offset="1" stop-color="{pal["accent"]}" stop-opacity="0.82"/></radialGradient></defs>'
            f'<path d="{DROP}" fill="url(#{ident}-g)"/><path d="M-62 58 A64 64 0 0 0 -10 118" fill="none" stroke="#FFFFFF" '
            f'stroke-width="11" stroke-linecap="round" opacity="0.9"/><ellipse cx="-38" cy="-8" rx="12" ry="22" fill="#FFFFFF" opacity="0.7"/></svg>')


# --- 1. hook: a drop lands on line 1 ---------------------------------------------------------------

def dw_hook(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    n = max(4, min(7, int(d.get("lines", 6))))
    lab, g = _label(s, x=62, y=34, w=740, n=n, pitch=58, head=100, tag="")
    fly = _f(d, "fly_at", 0.3)
    land = fly + 0.7
    ring = max(land + 0.1, _f(d, "ring_at", land + 0.2))
    q_at = _f(d, "question_at", ring + 0.8)
    badge_at = _f(d, "badge_at", q_at + 1.0)
    y1 = g["cy"][0]
    bar1 = int(g["area"] * BAR_WIDTHS[0] / 100)
    ring_w = bar1 + 52
    drop_x = g["bar_x"] + bar1 - 80
    body = f"""{lab}
<div class="dl-ring" id="{s}-ring" style="left:{g['bar_x'] - 26}px;top:{y1 - 33}px;width:{ring_w}px"></div>
<i class="dl-spot" id="{s}-spot" style="left:{drop_x + 14}px;top:{y1 - 16}px"></i>
<div class="dl-ripple" id="{s}-ripple" style="left:{drop_x - 44}px;top:{y1 - 26}px"></div>
{_drop_svg(c.pal, 'dl-drop', f'{s}-drop', f'left:{drop_x}px;top:{y1 - 152}px')}
<div class="dl-chip amber" id="{s}-chip" style="left:{g['bar_x'] + ring_w - 210}px;top:{y1 - 96}px">{_e(d.get('badge', 'Zeile 1?'))}</div>
<div class="dl-question" id="{s}-q">{_e(d.get('question', ''))}</div>"""
    html, tl = _frame(c, "", body, push=1.05)
    tl += [
        _ft(f"#{s}-lab", "opacity:0,y:80,rotation:-4", 'opacity:1,y:0,rotation:-1.5,duration:0.6,ease:"power3.out"', c.t(0.02)),
        *_bars_in(s, n, c.t(0.18), 0.06),
        _ft(f"#{s}-drop", "y:-560,opacity:0", f'y:0,opacity:1,duration:{land - fly:.2f},ease:"power2.in"', c.t(fly)),
        _to(f"#{s}-drop", 'scaleY:0.82,scaleX:1.12,transformOrigin:"50% 100%",duration:0.12,yoyo:true,repeat:1,ease:"sine.inOut"', c.t(land)),
        _ft(f"#{s}-ripple", "scale:0.2,opacity:0.9", 'scale:1.9,opacity:0,duration:1.2,ease:"power1.out"', c.t(land)),
        _ft(f"#{s}-hl0", "opacity:0", "opacity:1,duration:0.4", c.t(land + 0.05)),
        _to(f"#{s}-drop", 'opacity:0,scaleY:0.3,scaleX:1.4,transformOrigin:"50% 100%",duration:0.5,ease:"power2.in"', c.t(land + 0.5)),
        _ft(f"#{s}-spot", "opacity:0,scale:0.4", 'opacity:1,scale:1,duration:0.5,ease:"power2.out"', c.t(land + 0.55)),
        _ft(f"#{s}-ring", "opacity:0,scale:0.85", 'opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"', c.t(ring)),
        _ft(f"#{s}-q", "opacity:0,y:40", 'opacity:1,y:0,duration:0.5,ease:"power3.out"', c.t(q_at)),
        _pop(f"#{s}-chip", c.t(badge_at)),
    ]
    return SceneOut(html=html, tl=tl, events=[c.start, c.t(land), c.t(ring), c.t(q_at), c.t(badge_at)])


# --- 2. one name for the whole EU: label + glossary ------------------------------------------------

def dw_names(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    line = int(d.get("word_line", 2))
    word = d.get("word", "AQUA")
    lab, g = _label(s, x=32, y=0, w=800, n=4, pitch=54, head=92, words={line: word})
    gy = g["h"] + 34
    gloss = (f'<div class="dl-card dl-gloss" id="{s}-gloss" style="left:32px;top:{gy}px;width:800px;height:268px">'
             f'<div class="dl-ghead">{_icon("book")}<span class="dl-gtitle">{_e(d.get("gloss_title", "EU-Glossar"))}</span>'
             f'<span class="dl-gsub">{_e(d.get("gloss_sub", "gemeinsame Bezeichnungen"))}</span></div>'
             f'<div class="dl-grow" style="top:96px"><i class="dl-gbar" style="width:46%"></i><i class="dl-gbar soft" style="width:22%"></i></div>'
             f'<div class="dl-grow" id="{s}-ghit" style="top:150px"><b class="dl-gname">{_e(word)}</b>'
             f'<span class="dl-gdesc">{_e(d.get("gloss_note", "ein Name, EU-weit gleich"))}</span></div>'
             f'<div class="dl-grow" style="top:204px"><i class="dl-gbar" style="width:38%"></i><i class="dl-gbar soft" style="width:30%"></i></div></div>')
    hit_y = gy + 150 + 27
    fly = f'<div class="dl-fly" id="{s}-fly" style="left:{g["bar_x"] - 14}px;top:{hit_y - 29}px">{_e(word)}</div>'
    mean = (f'<div class="dl-chip drop" id="{s}-mean" style="left:{g["bar_x"] + 200}px;top:{g["cy"][line] - 29}px">'
            f'{_icon("drop", "dl-ico sm")}{_e(d.get("meaning", "= Wasser"))}</div>')
    html, tl = _frame(c, d.get("headline", ""), lab + gloss + fly + mean)
    label_at, head_at = _f(d, "label_at", 2.5), _f(d, "head_at", 3.9)
    gloss_at, word_at, mean_at = _f(d, "gloss_at", 6.5), _f(d, "word_at", 8.8), _f(d, "meaning_at", 9.6)
    tl += [
        _card_in(f"#{s}-lab", c.t(0.15)),
        *_bars_in(s, 4, c.t(label_at)),
        _ft(f"#{s}-under", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.5,ease:"power2.out"', c.t(head_at)),
        _to(f"#{s}-ing", f'color:"{c.pal["accent"]}",duration:0.3', c.t(head_at)),
        _card_in(f"#{s}-gloss", c.t(gloss_at), 120),
        _ft(f"#{s}-ghit", 'backgroundColor:"rgba(201,143,147,0)"', 'backgroundColor:"rgba(201,143,147,0.24)",duration:0.3', c.t(word_at - 0.25)),
        _ft(f"#{s}-fly", "opacity:0,y:0,scale:0.9", "opacity:1,y:0,scale:1,duration:0.2", c.t(word_at - 0.1)),
        _to(f"#{s}-fly", f'y:{g["cy"][line] - hit_y},duration:0.7,ease:"power2.inOut"', c.t(word_at + 0.1)),
        _to(f"#{s}-bar{line}", "opacity:0,duration:0.2", c.t(word_at + 0.7)),
        _ft(f"#{s}-word{line}", "opacity:0", "opacity:1,duration:0.2", c.t(word_at + 0.72)),
        _to(f"#{s}-fly", "opacity:0,duration:0.15", c.t(word_at + 0.8)),
        _ft(f"#{s}-hl{line}", "opacity:0", "opacity:1,duration:0.3", c.t(word_at + 0.75)),
        _pop(f"#{s}-mean", c.t(mean_at)),
    ]
    ev = [c.start, c.t(label_at), c.t(head_at), c.t(gloss_at), c.t(word_at), c.t(mean_at)]
    return SceneOut(html=html, tl=tl, events=ev)


# --- 3. order by weight ----------------------------------------------------------------------------

WEIGHTS = [100, 72, 50, 34, 23, 15]


def dw_order(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    extra = (f'<span class="dl-wlabel" id="{s}-wlab">{_icon("scale", "dl-ico sm")}{_e(d.get("weight_label", "Gewicht"))}</span>'
             f'<span class="dl-chip acc dl-front" id="{s}-front" style="top:{(92 - 48) // 2}px">{_e(d.get("front_tag", "Zeile 1 = größte Menge"))}</span>')
    lab, g = _label(s, x=32, y=0, w=800, n=6, pitch=54, head=92, weights=WEIGHTS, tag="", head_extra=extra)
    arrow = (f'<div class="dl-arrow" id="{s}-arrow" style="left:{g["wcol_x"] + 230 + 10}px;top:{g["top0"] + 14}px;'
             f'height:{g["pitch"] * 5 + 4}px"></div>')
    by = g["h"] + 30
    acc, blush = c.pal["accent"], c.pal.get("blush", c.pal["accent"])
    bowl = (f'<div class="dl-card dl-mix" id="{s}-mix" style="left:32px;top:{by}px;width:800px;height:150px">'
            f'<svg class="dl-bowl" viewBox="0 0 200 120"><path d="M14 44h172a86 68 0 0 1-172 0z" fill="#F5E9E5" stroke="{acc}" stroke-width="4"/>'
            f'<path d="M34 58h132" stroke="{blush}" stroke-width="7" stroke-linecap="round" opacity="0.6"/></svg>'
            + "".join(f'<span class="dl-mdrop" id="{s}-md{k}" style="left:{88 + k * 36}px;width:{34 - k * 8}px;height:{42 - k * 10}px"></span>' for k in range(3))
            + f'<div class="dl-mtext" id="{s}-mtext">{_e(d.get("tag", "gemessen beim Hinzufügen"))}</div></div>')
    html, tl = _frame(c, d.get("headline", ""), lab + arrow + bowl)
    w_at, drops_at, tag_at = _f(d, "weights_at", 1.7), _f(d, "drops_at", 4.2), _f(d, "tag_at", 4.6)
    front_at, ftag_at = _f(d, "front_at", 6.2), _f(d, "front_tag_at", 8.0)
    tl += [_card_in(f"#{s}-lab", c.t(0.1)), *_bars_in(s, 6, c.t(0.3), 0.05)]
    tl += [_ft(f"#{s}-wt{i}", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.6,ease:"power3.out"', c.t(w_at + i * 0.08)) for i in range(6)]
    tl += [
        _ft(f"#{s}-wlab", "opacity:0,y:-10", "opacity:1,y:0,duration:0.3", c.t(w_at)),
        _ft(f"#{s}-arrow", 'scaleY:0,transformOrigin:"50% 0%"', 'scaleY:1,duration:0.7,ease:"power2.out"', c.t(w_at + 0.3)),
        _card_in(f"#{s}-mix", c.t(drops_at - 0.5), 60),
        *[_ft(f"#{s}-md{k}", "y:-90,opacity:0", 'y:0,opacity:1,duration:0.45,ease:"power2.in"', c.t(drops_at + k * 0.22)) for k in range(3)],
        _ft(f"#{s}-mtext", "opacity:0,x:30", 'opacity:1,x:0,duration:0.4,ease:"power2.out"', c.t(tag_at)),
        _ft(f"#{s}-hl0", "opacity:0", "opacity:1,duration:0.35", c.t(front_at)),
        _to(f"#{s}-wt0", f'backgroundColor:"{acc}",duration:0.3', c.t(front_at)),
        _to(f"#{s}-wlab", "opacity:0,duration:0.2", c.t(ftag_at - 0.15)),
        _pop(f"#{s}-front", c.t(ftag_at)),
    ]
    ev = [c.start, c.t(w_at), c.t(drops_at), c.t(tag_at), c.t(front_at), c.t(ftag_at)]
    return SceneOut(html=html, tl=tl, events=ev)


# --- 4. the invisible 1 % limit ---------------------------------------------------------------------

def dw_limit(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    lab, g = _label(s, x=32, y=0, w=800, n=7, pitch=50, head=92, weights=[100, 72, 50, 34, 9, 7, 8], gap_after={3: 34})
    p = g["pitch"]
    line_y = g["cy"][3] + p // 2 + 17
    limit = (f'<div class="dl-limit" id="{s}-limit" style="left:{g["x"] + 22}px;top:{line_y - 2}px;width:{g["w"] - 44}px"></div>'
             f'<div class="dl-chip lim" id="{s}-lim" style="left:{g["x"] - 16}px;top:{line_y - 23}px">1 %</div>'
             f'<div class="dl-chip lim q" id="{s}-limq" style="left:{g["x"] - 16}px;top:{line_y - 23}px">? %</div>')
    ly = g["h"] + 26
    legend = (f'<div class="dl-legend" id="{s}-up" style="left:32px;top:{ly}px"><i class="sq"></i>{_e(d.get("upper", "über 1 %: nach Gewicht"))}</div>'
              f'<div class="dl-legend" id="{s}-low" style="left:32px;top:{ly + 56}px"><i class="sq dash"></i>{_e(d.get("lower", "unter 1 %: Reihenfolge frei"))}</div>'
              f'<div class="dl-chip amber big" id="{s}-chip" style="left:{g["x"] + 388}px;top:{ly + 20}px">{_e(d.get("chip", "Grenze: nicht angegeben"))}</div>')
    html, tl = _frame(c, d.get("headline", ""), lab + limit + legend)
    end_at, line_at, sh_at = _f(d, "end_at", 1.8), _f(d, "line_at", 3.6), _f(d, "shuffle_at", 4.7)
    fade_at, chip_at = _f(d, "fade_at", 7.1), _f(d, "chip_at", 8.5)
    amber = c.pal.get("signal_amber", "#946420")
    tl += [_card_in(f"#{s}-lab", c.t(0.05), 30)]
    tl += [_ft(f"#{s}-wt{i}", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.5,ease:"power3.out"', c.t(0.25 + i * 0.05)) for i in range(7)]
    tl += [_ft(f"#{s}-r{i}", "opacity:1", "opacity:0.55,duration:0.3", c.t(end_at)) for i in (4, 5, 6)]
    tl += [_to(f"#{s}-r{i}", 'x:6,duration:0.08,yoyo:true,repeat:3,ease:"sine.inOut"', c.t(end_at)) for i in (4, 5, 6)]
    tl += [
        _ft(f"#{s}-limit", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.6,ease:"power2.out"', c.t(line_at)),
        _pop(f"#{s}-lim", c.t(line_at + 0.1)),
        _card_in(f"#{s}-up", c.t(line_at + 0.3), 20),
        _card_in(f"#{s}-low", c.t(line_at + 0.5), 20),
        # lines under the limit swap places (row 5 <-> row 7): any order is allowed there
        _to(f"#{s}-r4", f'y:{2 * p},opacity:1,duration:0.6,ease:"power2.inOut"', c.t(sh_at)),
        _to(f"#{s}-r6", f'y:{-2 * p},opacity:1,duration:0.6,ease:"power2.inOut"', c.t(sh_at)),
        _to(f"#{s}-r5", 'opacity:1,x:-14,duration:0.3,yoyo:true,repeat:1,ease:"sine.inOut"', c.t(sh_at + 0.1)),
        _to(f"#{s}-limit", f'borderTopColor:"{amber}",opacity:0.3,duration:0.6', c.t(fade_at)),
        _to(f"#{s}-lim", "opacity:0,duration:0.2", c.t(fade_at)),
        _pop(f"#{s}-limq", c.t(fade_at + 0.15)),
        _pop(f"#{s}-chip", c.t(chip_at)),
    ]
    ev = [c.start, c.t(end_at), c.t(line_at), c.t(sh_at), c.t(fade_at), c.t(chip_at)]
    return SceneOut(html=html, tl=tl, events=ev)


# --- 5. what the list shows / does not show ---------------------------------------------------------

def dw_shows(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    lab, g = _label(s, x=32, y=0, w=800, n=3, pitch=48, head=86, pct=True)
    left, right = d.get("left") or {}, d.get("right") or {}
    top_l = g["h"] + 20

    def card(side: str, data: dict, top: int, kind: str) -> str:
        rows = "".join(f'<div class="dl-crow" id="{s}-{side}{k}"><i class="dl-mk {kind}"></i>{_e(r.get("text", ""))}</div>'
                       for k, r in enumerate((data.get("rows") or [])[:2]))
        return (f'<div class="dl-card dl-cmp {side}" id="{s}-{side}" style="left:32px;top:{top}px;width:800px;height:166px">'
                f'<div class="dl-ctitle">{_e(data.get("title", ""))}</div>{rows}</div>')
    html, tl = _frame(c, d.get("headline", ""), lab + card("L", left, top_l, "fact") + card("R", right, top_l + 182, "gap"))
    read_at, front_at, pct_at = _f(d, "read_at", 0.6), _f(d, "front_at", 4.6), _f(d, "pct_at", 6.2)
    tl += [_card_in(f"#{s}-lab", c.t(0.05), 30), *_bars_in(s, 3, c.t(0.2), 0.05)]
    tl += [_ft(f"#{s}-hl{i}", "opacity:0", "opacity:1,duration:0.2", c.t(read_at + i * 0.25)) for i in range(3)]
    tl += [_to(f"#{s}-hl{i}", "opacity:0,duration:0.25", c.t(read_at + i * 0.25 + 0.35)) for i in range(3)]
    tl += [_card_in(f"#{s}-L", c.t(read_at + 0.3), 30), _card_in(f"#{s}-R", c.t(pct_at - 0.3), 30)]
    ev = [c.start, c.t(read_at), c.t(front_at), c.t(pct_at)]
    for k, r in enumerate((left.get("rows") or [])[:2]):
        at = _f(r, "at", read_at + 1.0 + k * 2.0)
        tl.append(_ft(f"#{s}-L{k}", "opacity:0,x:-24", 'opacity:1,x:0,duration:0.4,ease:"power2.out"', c.t(at)))
        ev.append(c.t(at))
    tl += [_ft(f"#{s}-hl0", "opacity:0", "opacity:1,duration:0.3", c.t(front_at + 0.05)),
           _to(f"#{s}-hl0", "opacity:0,duration:0.3", c.t(pct_at - 0.2))]
    tl += [_pop(f"#{s}-pct{i}", c.t(pct_at + i * 0.08)) for i in range(3)]
    for k, r in enumerate((right.get("rows") or [])[:2]):
        at = _f(r, "at", pct_at + k * 3.0)
        tl.append(_ft(f"#{s}-R{k}", "opacity:0,x:-24", 'opacity:1,x:0,duration:0.4,ease:"power2.out"', c.t(at)))
        ev.append(c.t(at))
    return SceneOut(html=html, tl=tl, events=ev)


# --- 6. how to read it: three callouts on the label + CosIng ---------------------------------------

def dw_howto(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    items = (d.get("items") or [])[:3]
    lab, g = _label(s, x=32, y=0, w=800, n=7, pitch=48, head=86, nums=False, bar_frac=0.42, words={4: d.get("word", "PARFUM")})
    cx = g["bar_x"] + int(g["area"] * 0.92) + 30        # callout column right of the bars
    cw = g["x"] + g["w"] - 24 - cx

    def callout(k: int, y_mid: int, h: int) -> str:
        it = items[k] if k < len(items) else {}
        return (f'<div class="dl-call" id="{s}-c{k}" style="left:{cx}px;top:{y_mid - h // 2}px;width:{cw}px;height:{h}px">'
                f'<span class="dl-cnum">{k + 1}</span><span class="dl-ctext">{_e(it.get("sub") or it.get("title", ""))}</span></div>')
    brace = f'<div class="dl-brace" id="{s}-brace" style="left:{cx - 24}px;top:{g["cy"][0] - 20}px;height:{g["cy"][2] - g["cy"][0] + 40}px"></div>'
    lens = f'<div class="dl-lens" id="{s}-lens" style="left:{g["bar_x"] + 70}px;top:{g["cy"][6] - 50}px">{ICON["lens"]}</div>'
    cos_y = g["h"] + 22
    cos = (f'<div class="dl-card dl-cos" id="{s}-cos" style="left:32px;top:{cos_y}px;width:800px;height:134px">'
           f'<div class="dl-search">{_icon("lens")}<span class="dl-cname">{_e(d.get("cosing_title", "CosIng"))}</span>'
           f'<span class="dl-caret" id="{s}-caret"></span></div>'
           f'<div class="dl-csub" id="{s}-csub">{_e(d.get("cosing_sub", "Datenbank der EU-Kommission"))}</div></div>')
    body = (lab + brace + callout(0, (g["cy"][0] + g["cy"][2]) // 2, 96) + callout(1, g["cy"][4], 52)
            + callout(2, g["cy"][6], 52) + lens + cos)
    html, tl = _frame(c, d.get("headline", ""), body)
    at = [_f(it, "at", 1.5 + k * 3.0) for k, it in enumerate(items)] + [9.0] * (3 - len(items))
    cos_at, db_at = _f(d, "cosing_at", at[2] + 1.6), _f(d, "db_at", at[2] + 2.8)
    tl += [_card_in(f"#{s}-lab", c.t(0.05), 30), *_bars_in(s, 7, c.t(0.2), 0.05)]
    tl += [_ft(f"#{s}-hl{i}", "opacity:0", "opacity:1,duration:0.3", c.t(at[0] + i * 0.1)) for i in range(3)]
    tl += [
        _ft(f"#{s}-brace", 'scaleY:0,transformOrigin:"50% 0%"', 'scaleY:1,duration:0.45,ease:"power2.out"', c.t(at[0])),
        _card_in(f"#{s}-c0", c.t(at[0] + 0.2), 20),
        *[_to(f"#{s}-hl{i}", "opacity:0,duration:0.3", c.t(at[1] - 0.2)) for i in range(3)],
        _to(f"#{s}-bar4", "opacity:0,duration:0.2", c.t(at[1] - 0.05)),
        _ft(f"#{s}-word4", "opacity:0,y:10", "opacity:1,y:0,duration:0.3", c.t(at[1])),
        _ft(f"#{s}-hl4", "opacity:0", "opacity:1,duration:0.3", c.t(at[1])),
        _card_in(f"#{s}-c1", c.t(at[1] + 0.2), 20),
        _to(f"#{s}-hl4", "opacity:0,duration:0.3", c.t(at[2] - 0.2)),
        _ft(f"#{s}-lens", "opacity:0,x:-160,rotation:-20", 'opacity:1,x:0,rotation:0,duration:0.6,ease:"power3.out"', c.t(at[2])),
        _ft(f"#{s}-hl6", "opacity:0", "opacity:1,duration:0.3", c.t(at[2] + 0.3)),
        _card_in(f"#{s}-c2", c.t(at[2] + 0.35), 20),
        _card_in(f"#{s}-cos", c.t(cos_at - 0.2), 60),
        _ft(f"#{s}-caret", "opacity:0", "opacity:1,duration:0.05,repeat:5,yoyo:true", c.t(cos_at + 0.3)),
        _ft(f"#{s}-csub", "opacity:0,y:12", "opacity:1,y:0,duration:0.4", c.t(db_at)),
    ]
    ev = [c.start] + [c.t(a) for a in at] + [c.t(cos_at), c.t(db_at)]
    return SceneOut(html=html, tl=tl, events=ev)


# --- 7. close: read first, then apply; sign-off ----------------------------------------------------

def dw_close(c: SceneCtx, d: dict) -> SceneOut:
    s = c.sid
    lab, g = _label(s, x=32, y=0, w=470, n=6, pitch=46, head=86, nums=False, tag="")
    blush, acc = c.pal.get("blush", c.pal["accent"]), c.pal["accent"]
    jar = (f'<div class="dl-jarbox" id="{s}-jar" style="left:532px;top:6px;width:300px;height:{g["h"]}px">'
           f'<svg class="dl-jar" viewBox="0 0 300 260"><defs><linearGradient id="{s}-jg" x1="0" x2="1">'
           f'<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#F6ECE8"/><stop offset="1" stop-color="#E6D3CE"/></linearGradient></defs>'
           f'<rect x="56" y="30" width="188" height="56" rx="12" fill="{blush}" opacity="0.85"/>'
           f'<rect x="40" y="84" width="220" height="160" rx="26" fill="url(#{s}-jg)" stroke="#E8D9D4" stroke-width="3"/>'
           f'<path d="M66 110v100" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity="0.9"/></svg>'
           f'<div class="dl-btn" id="{s}-btn">{_e(d.get("button", "Auftragen"))}</div></div>')
    gy = g["h"] + 24
    gate = (f'<div class="dl-gate" id="{s}-gate" style="left:32px;top:{gy}px;width:800px">'
            f'<i class="dl-gdot"></i><span>{_e(d.get("block_text", "Erst die Liste lesen"))}</span></div>'
            f'<div class="dl-gate ok" id="{s}-ok" style="left:32px;top:{gy}px;width:800px">'
            f'<i class="dl-gsq"></i><span>{_e(d.get("done_text", "Liste gelesen"))}</span></div>')
    sweep = f'<i class="dl-sweep" id="{s}-sweep" style="left:{g["x"] + 18}px;top:{g["top0"] + 5}px;width:{g["w"] - 36}px"></i>'
    sign = (f'<div class="dl-sign" id="{s}-sign" style="top:{gy + 6}px">'
            f'<div class="dl-sword">{_drop_svg(c.pal, "dl-sdrop", f"{s}-sd")}<span>{_e(d.get("domain", "Dewlane"))}</span></div>'
            f'<div class="dl-sclaim">{_e(d.get("claim", ""))}</div><div class="dl-sdisc">{_e(d.get("disclaimer", ""))}</div></div>')
    html, tl = _frame(c, d.get("headline", ""), lab + sweep + jar + gate + sign, push=1.03)
    read_at, done_at = _fw(c, d, "read_at", 0.08), _fw(c, d, "done_at", 0.16)
    unlock_at, brand_at = _fw(c, d, "unlock_at", 0.26), _fw(c, d, "brand_at", 0.36)
    done_at, unlock_at = max(done_at, read_at + 0.3), max(unlock_at, read_at + 0.7)
    brand_at = max(brand_at, unlock_at + 0.6)
    sweep_end = max(read_at + 0.6, unlock_at - 0.1)
    tl += [_card_in(f"#{s}-lab", c.t(0.02), 30), *_bars_in(s, 6, c.t(0.12), 0.04),
           _card_in(f"#{s}-jar", c.t(0.15), 30), _card_in(f"#{s}-gate", c.t(0.3), 20),
           _ft(f"#{s}-sweep", "opacity:0,y:0", "opacity:1,duration:0.15", c.t(read_at)),
           _to(f"#{s}-sweep", f'y:{g["pitch"] * 5},duration:{sweep_end - read_at:.2f},ease:"none"', c.t(read_at)),
           _to(f"#{s}-sweep", "opacity:0,duration:0.2", c.t(sweep_end))]
    tl += [_to(f"#{s}-bar{i}", f'backgroundColor:"{blush}",duration:0.2', c.t(read_at + (sweep_end - read_at) * i / 6)) for i in range(6)]
    tl += [
        _to(f"#{s}-gate", "opacity:0,duration:0.15", c.t(unlock_at - 0.2)),
        _ft(f"#{s}-ok", "opacity:0,scale:0.96", 'opacity:1,scale:1,duration:0.3,ease:"power2.out"', c.t(unlock_at - 0.04)),
        _to(f"#{s}-btn", f'backgroundColor:"{acc}",color:"#FFFFFF",opacity:1,duration:0.3', c.t(unlock_at + 0.1)),
        _to(f"#{s}-ok", "opacity:0,y:-10,duration:0.3", c.t(brand_at - 0.1)),
        _ft(f"#{s}-sign", "opacity:0,y:30", 'opacity:1,y:0,duration:0.6,ease:"power3.out"', c.t(brand_at)),
    ]
    ev = [c.start, c.t(read_at), c.t(done_at), c.t(unlock_at), c.t(brand_at)]
    return SceneOut(html=html, tl=tl, events=ev)


# --- general Dewlane scenes (production week 1, 01.11.2026) ---------------------------------------
# Same look as Q1 (porcelain cards, radius 18, Playfair + Inter, mauve shadows), but data-driven for any topic.
# Item times: an explicit "at" (seconds or "w:Wort") wins; otherwise _auto_times puts each item on the first spoken
# word that shares a five-letter stem with the item text, else on the spoken word nearest an even spacing.

STOP = set("der die das den dem des und oder ein eine einen einem einer eines ist sind wird werden nicht dass wie was "
           "wer mit auf aus bei von zum zur für über unter auch noch nur the and with for from that this are was not "
           "your you has have will into than then".split())


def _auto_times(c: SceneCtx, texts: list, given: list | None = None, lo: float = 0.35, hi: float | None = None) -> list[float]:
    hi = c.duration - 0.6 if hi is None else hi
    cand = [(round(w.start - c.start, 3), _norm(w.text)) for w in (c.words or []) if lo <= w.start - c.start <= hi]
    out, prev, n = [], lo - 0.5, len(texts)
    for k, t in enumerate(texts):
        g = (given or [None] * n)[k]
        if isinstance(g, (int, float)):
            out.append(float(g))
            prev = float(g)
            continue
        stems = {_norm(x)[:5] for x in re.split(r"[\s/,.;:()„“\"+–-]+", str(t)) if len(_norm(x)) >= 4 and _norm(x) not in STOP}
        # latest acceptable time: an even schedule over the beat, so no card sits empty while the voice talks
        latest = lo + (hi - lo) * (k + 0.6) / n
        hit = next((s for s, wn in cand if prev + 0.45 < s <= latest and len(wn) >= 4 and wn[:5] in stems), None)
        if hit is None:
            rest = [s for s, _ in cand if s > prev + 0.45]
            target = min(latest, lo + (hi - lo) * (k + 0.3) / n)
            hit = min(rest, key=lambda s: abs(s - target)) if rest else min(hi, prev + 1.0)
        out.append(hit)
        prev = hit
    return out


GLYPH = {
    "openjar": '<svg viewBox="0 0 120 120"><path d="M24 56h72v38a12 12 0 0 1-12 12H36a12 12 0 0 1-12-12z"/><path d="M26 44l62-24 5 13-62 24z"/></svg>',
    "hourglass": '<svg viewBox="0 0 120 120"><path d="M34 16h52M34 104h52M40 16c0 30 40 32 40 44S40 74 40 104M80 16c0 30-40 32-40 44s40 14 40 44"/></svg>',
    "book": '<svg viewBox="0 0 120 120"><path d="M14 30h36a10 10 0 0 1 10 10v58a8 8 0 0 0-8-8H14z"/><path d="M106 30H70a10 10 0 0 0-10 10v58a8 8 0 0 1 8-8h38z"/><path d="M76 64h20M76 76h14"/></svg>',
    "sun": '<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="20"/><path d="M60 14v14M60 92v14M14 60h14M92 60h14M28 28l10 10M82 82l10 10M28 92l10-10M82 38l10-10"/></svg>',
    "drop": '<svg viewBox="0 0 120 120"><path d="M60 14C50 32 28 54 28 74a32 32 0 0 0 64 0c0-20-22-42-32-60z"/></svg>',
    "doc": '<svg viewBox="0 0 120 120"><path d="M30 12h44l18 18v78H30z"/><path d="M74 12v18h18M42 54h36M42 68h36M42 82h24"/></svg>',
    "shield": '<svg viewBox="0 0 120 120"><path d="M60 12l38 14v30c0 26-17 44-38 52-21-8-38-26-38-52V26z"/></svg>',
    "scale": '<svg viewBox="0 0 48 48"><path d="M24 8v32M12 40h24M8 16h32M8 16l-5 12a6 6 0 0 0 10 0zM40 16l-5 12a6 6 0 0 0 10 0z"/></svg>',
}


def _glyph(name: str, cls: str = "dl-glyph", ident: str = "") -> str:
    return f'<span class="{cls}"{f" id={chr(34)}{ident}{chr(34)}" if ident else ""}>{GLYPH.get(name, GLYPH["drop"])}</span>' if name else ""


def _pack(s: str, kind: str, x: int, y: int, w: int, h: int, title: str, sub: str = "", glyph: str = "", gtext: str = "") -> tuple[str, dict]:
    """Unbranded pack (tube or jar) with a white label: big title (Playfair), sub line, optional symbol with text."""
    cap_h = 70 if kind == "tube" else 90
    body_y = y + cap_h
    lab_x, lab_w = x + 34, w - 68
    lab_y = body_y + (60 if kind == "tube" else 40)
    lab_h = h - cap_h - (120 if kind == "tube" else 80)
    sym = (f'<div class="dl-psym" id="{s}-psym">{_glyph(glyph, "dl-glyph lg")}<span>{_e(gtext)}</span></div>' if glyph else "")
    html = (f'<div class="dl-pack {kind}" id="{s}-pack" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="dl-pcap" style="height:{cap_h}px"></div><div class="dl-pbody" style="top:{cap_h}px"></div>'
            f'<div class="dl-plab" style="left:34px;top:{lab_y - y}px;width:{lab_w}px;height:{lab_h}px">'
            f'<div class="dl-ptitle" id="{s}-ptitle">{_e(title)}</div><div class="dl-psub">{_e(sub)}</div>{sym}</div></div>')
    geo = {"title_y": lab_y + 70, "sym_y": lab_y + lab_h - 90, "lab_x": lab_x, "lab_w": lab_w, "lab_y": lab_y, "top": y}
    return html, geo


def dw_hook_any(c: SceneCtx, d: dict) -> SceneOut:
    """Hook for any topic: a drop lands on the lead object (label with a word, or a tube/jar with title or symbol),
    a honey ring marks the point, the question appears, a chip names the doubt."""
    s = c.sid
    obj = d.get("obj", "label")
    fly = _fw(c, d, "fly_at", 0.01)
    land = fly + 0.7
    ring = max(land + 0.1, _fw(c, d, "ring_at", land + 0.25))
    q_at = max(ring + 0.3, _fw(c, d, "question_at", 0.42))
    badge_at = max(q_at + 0.5, _fw(c, d, "badge_at", 0.72))
    if obj == "label":
        line = int(d.get("line", 0))
        words = {line: d["word"]} if d.get("word") else None
        lab, g = _label(s, x=62, y=34, w=740, n=6, pitch=58, head=100, tag="", words=words)
        fy = g["cy"][line]
        ring_html = f'<div class="dl-ring" id="{s}-ring" style="left:{g["bar_x"] - 26}px;top:{fy - 33}px;width:{int(g["area"] * 0.8) + 52}px"></div>'
        drop_x, drop_y = g["bar_x"] + int(g["area"] * 0.8) - 80, fy - 152
        chip_xy = (g["bar_x"] + int(g["area"] * 0.8) - 160, g["y"] + 22)
        objects = lab
        reveal = [_to(f"#{s}-bar{line}", "opacity:0,duration:0.2", c.t(land + 0.05)),
                  _ft(f"#{s}-word{line}", "opacity:0", "opacity:1,duration:0.25", c.t(land + 0.1))] if words else []
        enter = _ft(f"#{s}-lab", "opacity:0,y:80,rotation:-4", 'opacity:1,y:0,rotation:-1.5,duration:0.6,ease:"power3.out"', c.t(0.02))
        bars = _bars_in(s, 6, c.t(0.18), 0.06)
    else:
        pw, ph = (330, 500) if obj == "tube" else (420, 400)
        px = 864 - 40 - pw
        pack, g = _pack(s, obj, px, 20 if obj == "tube" else 100, pw, ph, d.get("title", ""), d.get("sub", ""), d.get("glyph", ""), d.get("gtext", ""))
        lab, _ = _label(s, x=24, y=70, w=440, n=5, pitch=52, head=86, nums=False, tag="")
        focus_sym = d.get("focus", "glyph") == "glyph" and d.get("glyph")
        fy = g["sym_y"] + 40 if focus_sym else g["title_y"]
        rw = g["lab_w"] + 30
        ring_html = f'<div class="dl-ring" id="{s}-ring" style="left:{g["lab_x"] - 15}px;top:{fy - 50}px;width:{rw}px;height:100px"></div>'
        drop_x, drop_y = g["lab_x"] + g["lab_w"] - 90, fy - 190
        chip_xy = (max(0, g["lab_x"] - 120), fy - 112)
        objects = f'<div class="dl-back" id="{s}-back">{lab}</div>' + pack
        reveal = []
        enter = _ft(f"#{s}-pack", "opacity:0,y:90", 'opacity:1,y:0,duration:0.6,ease:"power3.out"', c.t(0.02))
        bars = [_ft(f"#{s}-back", "opacity:0,x:-60,rotation:-6", 'opacity:0.95,x:0,rotation:-4,duration:0.6,ease:"power3.out"', c.t(0.12)),
                *_bars_in(s, 5, c.t(0.3), 0.05)]
    body = f"""{objects}{ring_html}
<i class="dl-spot" id="{s}-spot" style="left:{drop_x + 14}px;top:{drop_y + 136}px"></i>
{_drop_svg(c.pal, 'dl-drop', f'{s}-drop', f'left:{drop_x}px;top:{drop_y}px')}
<div class="dl-chip amber" id="{s}-chip" style="left:{chip_xy[0]}px;top:{chip_xy[1]}px">{_e(d.get('badge', ''))}</div>
<div class="dl-question" id="{s}-q">{_e(d.get('question', ''))}</div>"""
    html, tl = _frame(c, "", body, push=1.05)
    tl += [enter, *bars,
           _ft(f"#{s}-drop", "y:-560,opacity:0", f'y:0,opacity:1,duration:{land - fly:.2f},ease:"power2.in"', c.t(fly)),
           _to(f"#{s}-drop", 'scaleY:0.82,scaleX:1.12,transformOrigin:"50% 100%",duration:0.12,yoyo:true,repeat:1,ease:"sine.inOut"', c.t(land)),
           _to(f"#{s}-drop", 'opacity:0,scaleY:0.3,scaleX:1.4,transformOrigin:"50% 100%",duration:0.5,ease:"power2.in"', c.t(land + 0.5)),
           _ft(f"#{s}-spot", "opacity:0,scale:0.4", 'opacity:1,scale:1,duration:0.5,ease:"power2.out"', c.t(land + 0.55)),
           *reveal,
           _ft(f"#{s}-ring", "opacity:0,scale:0.85", 'opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"', c.t(ring)),
           _ft(f"#{s}-q", "opacity:0,y:40", 'opacity:1,y:0,duration:0.5,ease:"power3.out"', c.t(q_at))]
    if d.get("badge"):
        tl.append(_pop(f"#{s}-chip", c.t(badge_at)))
    return SceneOut(html=html, tl=tl, events=[c.start, c.t(land), c.t(ring), c.t(q_at)] + ([c.t(badge_at)] if d.get("badge") else []))


MARK = {"fact": "fact", "gap": "gap", "open": "open", "ok": "ok", "interp": "interp"}


def dw_facts(c: SceneCtx, d: dict) -> SceneOut:
    """Document card (act and article) above a card of 2-4 fact rows; rows appear on their words."""
    s = c.sid
    rows = (d.get("rows") or [])[:4]
    doc = d.get("doc")
    top = 0
    parts = []
    if doc:
        parts.append(f'<div class="dl-card dl-doc" id="{s}-doc" style="left:32px;top:0;width:800px;height:118px">'
                     f'<span class="dl-par">§</span><div class="dl-dtxt"><b>{_e(doc.get("act", ""))}</b><span>{_e(doc.get("ref", ""))}</span></div>'
                     + (f'<span class="dl-chip acc dl-dtag" id="{s}-dtag">{_e(doc["tag"])}</span>' if doc.get("tag") else "") + "</div>")
        top = 140
    rh = 124 if len(rows) <= 3 else 100
    rws = "".join(f'<div class="dl-frow" id="{s}-f{k}" style="top:{24 + k * rh}px;height:{rh - 8}px"><i class="dl-mk {MARK.get(r.get("mark", "fact"), "fact")}"></i>'
                  f'<span class="dl-ftxt">{_e(r.get("text", ""))}</span>'
                  + (f'<b class="dl-fval">{_e(r["value"])}</b>' if r.get("value") else "") + "</div>" for k, r in enumerate(rows))
    parts.append(f'<div class="dl-card dl-fcard" id="{s}-fc" style="left:32px;top:{top}px;width:800px;height:{48 + len(rows) * rh}px">{rws}</div>')
    html, tl = _frame(c, d.get("headline", ""), "".join(parts))
    times = _auto_times(c, [r.get("text", "") + " " + str(r.get("value", "")) for r in rows], [r.get("at") for r in rows])
    if doc:
        tl.append(_card_in(f"#{s}-doc", c.t(0.1), 30))
        if doc.get("tag"):
            tl.append(_pop(f"#{s}-dtag", c.t(_f(doc, "tag_at", 0.9))))
    tl.append(_card_in(f"#{s}-fc", c.t(0.25 if doc else 0.1), 40))
    for k, t in enumerate(times):
        tl.append(_ft(f"#{s}-f{k}", "opacity:0,x:-28", 'opacity:1,x:0,duration:0.45,ease:"power2.out"', c.t(t)))
    ev = [c.start] + [c.t(t) for t in times] + ([c.t(_f(doc, "tag_at", 0.9))] if doc and doc.get("tag") else [])
    return SceneOut(html=html, tl=tl, events=ev)


def dw_bars(c: SceneCtx, d: dict) -> SceneOut:
    """Bar card: a caption line and 2-5 rows (label, bar, value); bars grow on their words; optional note chip."""
    s = c.sid
    rows = (d.get("rows") or [])[:5]
    mx = max([float(r.get("w", 1)) for r in rows] or [1.0])
    rh = 96 if len(rows) <= 4 else 84
    rws = "".join(f'<div class="dl-brow" id="{s}-r{k}" style="top:{78 + k * rh}px">'
                  f'<span class="dl-blab">{_e(r.get("label", ""))}</span>'
                  f'<span class="dl-btrack"><i class="dl-bfill" id="{s}-bf{k}" style="width:{max(4, float(r.get("w", 1)) / mx * 100):.1f}%"></i></span>'
                  f'<b class="dl-bval" id="{s}-bv{k}">{_e(r.get("value", ""))}</b></div>' for k, r in enumerate(rows))
    h = 100 + len(rows) * rh
    note = (f'<div class="dl-chip {d.get("note_tone", "acc")} dl-note" id="{s}-note" style="top:{h + 22}px">{_e(d["note"])}</div>' if d.get("note") else "")
    body = (f'<div class="dl-card dl-bcard" id="{s}-bc" style="left:32px;top:0;width:800px;height:{h}px">'
            f'<div class="dl-bcap">{_icon("scale", "dl-ico sm") if d.get("icon", True) else ""}<span>{_e(d.get("caption", ""))}</span></div>{rws}</div>{note}')
    html, tl = _frame(c, d.get("headline", ""), body)
    times = _auto_times(c, [f'{r.get("label", "")} {r.get("value", "")}' for r in rows] + ([d["note"]] if d.get("note") else []),
                        [r.get("at") for r in rows] + ([d.get("note_at")] if d.get("note") else []))
    tl.append(_card_in(f"#{s}-bc", c.t(0.1), 40))
    for k in range(len(rows)):
        tl += [_ft(f"#{s}-r{k}", "opacity:0", "opacity:1,duration:0.3", c.t(times[k])),
               _ft(f"#{s}-bf{k}", 'scaleX:0,transformOrigin:"0% 50%"', 'scaleX:1,duration:0.7,ease:"power3.out"', c.t(times[k] + 0.05))]
    if d.get("note"):
        tl.append(_pop(f"#{s}-note", c.t(times[-1])))
    return SceneOut(html=html, tl=tl, events=[c.start] + [c.t(t) for t in times])


def dw_timeline(c: SceneCtx, d: dict) -> SceneOut:
    """Vertical timeline with 2-4 dated steps; the line draws on, each step appears on its word."""
    s = c.sid
    nodes = (d.get("nodes") or [])[:4]
    step = 180 if len(nodes) <= 3 else 138
    items = "".join(f'<div class="dl-tnode" id="{s}-n{k}" style="top:{30 + k * step}px"><i class="dl-tdot"></i>'
                    f'<b class="dl-tdate">{_e(n.get("date", ""))}</b><span class="dl-ttxt">{_e(n.get("text", ""))}</span></div>' for k, n in enumerate(nodes))
    h = 60 + len(nodes) * step
    body = (f'<div class="dl-card dl-tcard" id="{s}-tc" style="left:32px;top:0;width:800px;height:{h}px">'
            f'<i class="dl-tline" id="{s}-tl" style="height:{h - 90}px"></i>{items}</div>')
    html, tl = _frame(c, d.get("headline", ""), body)
    times = _auto_times(c, [f'{n.get("date", "")} {n.get("text", "")}' for n in nodes], [n.get("at") for n in nodes])
    tl += [_card_in(f"#{s}-tc", c.t(0.1), 40),
           _ft(f"#{s}-tl", 'scaleY:0,transformOrigin:"50% 0%"', f'scaleY:1,duration:{max(0.6, times[-1] - 0.2):.2f},ease:"none"', c.t(0.3))]
    for k, t in enumerate(times):
        tl.append(_ft(f"#{s}-n{k}", "opacity:0,x:30", 'opacity:1,x:0,duration:0.45,ease:"power2.out"', c.t(t)))
    return SceneOut(html=html, tl=tl, events=[c.start] + [c.t(t) for t in times])


def _vt_size(title: str) -> int:
    """Card title size in the 392 px versus cards: the longest word must fit (Playfair, about 0.55 em per letter)."""
    longest = max((len(w) for w in str(title).split()), default=0)
    return 46 if longest <= 13 else 40 if longest <= 15 else 34 if longest <= 18 else 30


def dw_versus(c: SceneCtx, d: dict) -> SceneOut:
    """Two cards side by side (EU/USA, claim/source, shows/does not show); optional verdict chip below."""
    s = c.sid
    mode = d.get("mode", "compare")
    sides = [d.get("left") or {}, d.get("right") or {}]
    cards, texts, given = [], [], []
    for i, sd in enumerate(sides):
        cls = "myth" if (mode == "myth" and i == 0) else ""
        rows = (sd.get("rows") or [])[:3]
        rws = "".join(f'<div class="dl-vrow" id="{s}-v{i}{k}"><i class="dl-mk {MARK.get(r.get("mark", "gap" if cls else "fact"), "fact")}"></i>'
                      f'<span>{_e(r.get("text", ""))}</span></div>' for k, r in enumerate(rows))
        tag = f'<span class="dl-vtag">{_e(sd.get("tag", ""))}</span>' if sd.get("tag") else ""
        cards.append(f'<div class="dl-card dl-vcard {cls}" id="{s}-c{i}" style="left:{32 + i * 408}px;top:0;width:392px;height:500px">'
                     f'{tag}<div class="dl-vtitle" style="font-size:{_vt_size(sd.get("title", ""))}px">{_e(sd.get("title", ""))}</div>{rws}</div>')
        for r in rows:
            texts.append(r.get("text", ""))
            given.append(r.get("at"))
    verdict = f'<div class="dl-chip acc dl-verdict" id="{s}-vd">{_e(d["verdict"])}</div>' if d.get("verdict") else ""
    html, tl = _frame(c, d.get("headline", ""), "".join(cards) + verdict)
    if d.get("verdict"):
        texts.append(d["verdict"])
        given.append(d.get("verdict_at"))
    times = _auto_times(c, texts, given)
    n0 = len((sides[0].get("rows") or [])[:3])
    tl.append(_card_in(f"#{s}-c0", c.t(0.1), 40))
    tl.append(_card_in(f"#{s}-c1", c.t(max(0.3, (times[n0] if len(times) > n0 else 2.0) - 0.35)), 40))
    k = 0
    for i, sd in enumerate(sides):
        for j in range(len((sd.get("rows") or [])[:3])):
            tl.append(_ft(f"#{s}-v{i}{j}", "opacity:0,x:-20", 'opacity:1,x:0,duration:0.4,ease:"power2.out"', c.t(times[k])))
            k += 1
    if d.get("verdict"):
        tl.append(_pop(f"#{s}-vd", c.t(times[-1])))
    return SceneOut(html=html, tl=tl, events=[c.start] + [c.t(t) for t in times])


def dw_steps(c: SceneCtx, d: dict) -> SceneOut:
    """Three (max four) numbered steps as cards with an icon; each appears on its word and the previous one dims."""
    s = c.sid
    items = (d.get("items") or [])[:4]
    step = 190 if len(items) <= 3 else 146
    cards = "".join(f'<div class="dl-card dl-scard" id="{s}-s{k}" style="left:32px;top:{k * step}px;width:800px;height:{step - 18}px">'
                    f'<span class="dl-snum">{k + 1}</span><div class="dl-stxt"><b>{_e(it.get("title", ""))}</b><span>{_e(it.get("sub", ""))}</span></div>'
                    f'{_glyph(it.get("icon", ""), "dl-glyph sm")}</div>' for k, it in enumerate(items))
    html, tl = _frame(c, d.get("headline", ""), cards)
    times = _auto_times(c, [f'{it.get("title", "")} {it.get("sub", "")}' for it in items], [it.get("at") for it in items])
    for k, t in enumerate(times):
        tl.append(_card_in(f"#{s}-s{k}", c.t(t), 30))
    return SceneOut(html=html, tl=tl, events=[c.start] + [c.t(t) for t in times])


TEMPLATES = {
    "cinematic_hook": _anchored(dw_hook),
    "data_flow": _anchored(dw_names),
    "file_beside": _anchored(dw_order),
    "file_fork": _anchored(dw_limit),
    "comparison": _anchored(dw_shows),
    "key_takeaway": _anchored(dw_howto),
    "file_close": _anchored(dw_close),
    "dw_hook": _anchored(dw_hook_any),
    "dw_facts": _anchored(dw_facts),
    "dw_bars": _anchored(dw_bars),
    "dw_timeline": _anchored(dw_timeline),
    "dw_versus": _anchored(dw_versus),
    "dw_steps": _anchored(dw_steps),
}
HOOK_SCENE_TYPES = ["cinematic_hook", "dw_hook"]
LIMITS.update({
    "dw_hook": {"question": 52, "badge": 24, "title": 14, "sub": 22, "gtext": 8, "word": 14},
    "dw_facts": {"headline": 34},
    "dw_bars": {"headline": 34, "caption": 46, "note": 40},
    "dw_timeline": {"headline": 34},
    "dw_versus": {"headline": 34, "verdict": 44},
    "dw_steps": {"headline": 34},
})


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):
    acc, text, muted = pal["accent"], pal["text"], pal["muted"]
    paper, hair, surf = pal.get("paper", "#FFFFFF"), pal.get("hairline", "#E8D9D4"), pal.get("surface", "#FFFCF9")
    blush, amber, on_amber = pal.get("blush", acc), pal.get("signal_amber", acc), pal.get("on_signal", "#FFFFFF")
    red, green = pal.get("signal_red", "#8E2F45"), pal.get("signal_green", "#4F7A62")
    sh = "0 1px 2px rgba(74,47,52,0.08),0 14px 30px rgba(74,47,52,0.12),0 38px 70px rgba(155,85,96,0.14)"
    disp, bod = f"'FN {display}'", f"'FN {body}'"
    return f"""
/* Dewlane Q1 scenes: one lead object (INCI label), radius 18, mauve-tinted shadows, Playfair + Inter */
.dl{{position:absolute;left:108px;top:{zone_top}px;width:864px;height:{zone_h}px;text-align:left;}}
.dl-title{{position:absolute;left:0;top:0;width:864px;height:150px;display:flex;align-items:center;justify-content:center;text-align:center;
  font-family:{disp};font-weight:500;font-size:68px;line-height:1.04;letter-spacing:-0.012em;color:{text};}}
.dl-stage{{position:absolute;left:0;top:{STAGE_TOP}px;width:864px;height:{zone_h - STAGE_TOP}px;transform-origin:50% 40%;}}
.dl-stage.full{{top:0;height:{zone_h}px;}}
.dl-card{{position:absolute;background:{paper};border:1px solid {hair};border-radius:18px;box-shadow:{sh};}}
.dl-lab-head{{position:absolute;left:40px;right:40px;top:0;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid {hair};}}
.dl-ing{{position:relative;font-family:{disp};font-style:italic;font-weight:500;font-size:50px;line-height:1.2;color:{text};}}
.dl-tag{{font-family:{bod};font-size:26px;font-weight:600;color:{muted};letter-spacing:0.06em;}}
.dl-under{{position:absolute;left:0;right:0;bottom:-2px;height:4px;border-radius:2px;background:{acc};transform:scaleX(0);}}
.dl-row{{position:absolute;left:40px;right:40px;}}
.dl-hl{{position:absolute;left:-18px;right:-18px;top:4px;bottom:4px;border-radius:12px;background:color-mix(in srgb,{blush} 26%,transparent);opacity:0;}}
.dl-num{{position:absolute;left:0;top:50%;height:32px;margin-top:-16px;line-height:32px;font-family:{bod};font-size:26px;font-weight:600;color:{muted};}}
.dl-bar{{position:absolute;top:50%;height:20px;margin-top:-10px;border-radius:10px;background:{hair};}}
.dl-bar.strong{{background:color-mix(in srgb,{blush} 58%,{hair});}}
.dl-word{{position:absolute;top:50%;height:42px;margin-top:-21px;line-height:42px;font-family:{bod};font-weight:700;font-size:34px;letter-spacing:0.1em;color:{acc};opacity:0;}}
.dl-wcol{{position:absolute;top:50%;height:22px;margin-top:-11px;border-radius:11px;background:color-mix(in srgb,{hair} 45%,transparent);}}
.dl-wt{{position:static !important;display:block;height:100%;border-radius:11px;background:color-mix(in srgb,{acc} 55%,{blush});}}
.dl-pct{{position:absolute;top:50%;height:40px;margin-top:-20px;border:2px dashed {amber};border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-family:{bod};font-weight:700;font-size:28px;color:{amber};background:color-mix(in srgb,{amber} 6%,{paper});opacity:0;}}
.dl-chip{{position:absolute;display:inline-flex;align-items:center;gap:10px;white-space:nowrap;border-radius:999px;padding:8px 22px;font-family:{bod};font-weight:700;font-size:30px;
  line-height:1.2;box-shadow:0 10px 24px rgba(74,47,52,0.18);opacity:0;}}
.dl-chip.amber{{background:{amber};color:{on_amber};}}
.dl-chip.acc{{background:{acc};color:#FFFFFF;}}
.dl-chip.drop{{background:{paper};color:{text};border:2px solid {blush};}}
.dl-chip.big{{padding:10px 24px;}}
.dl-front{{right:0;font-size:28px;padding:6px 18px;}}
.dl-ico{{display:inline-flex;width:44px;height:44px;flex:none;}}
.dl-ico.sm{{width:34px;height:34px;}}
.dl-ico svg,.dl-lens svg{{width:100%;height:100%;fill:none;stroke:{acc};stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;}}
/* hook */
.dl-ring{{position:absolute;height:66px;border:4px solid {amber};border-radius:999px;opacity:0;}}
.dl-ripple{{position:absolute;width:240px;height:52px;border:3px solid {blush};border-radius:50%;opacity:0;}}
.dl-spot{{position:absolute;display:block;width:110px;height:32px;border-radius:50%;opacity:0;
  background:radial-gradient(ellipse at 40% 40%,#FFFFFF 0%,color-mix(in srgb,{blush} 55%,transparent) 60%,transparent 100%);}}
.dl-drop{{position:absolute;width:132px;height:160px;filter:drop-shadow(0 16px 18px rgba(155,85,96,0.3));}}
.dl-question{{position:absolute;left:0;top:548px;width:864px;text-align:center;font-family:{disp};font-weight:500;font-size:82px;line-height:1.04;letter-spacing:-0.02em;color:{text};opacity:0;}}
/* glossary */
.dl-ghead{{position:absolute;left:36px;right:36px;top:20px;height:60px;display:flex;align-items:center;gap:16px;}}
.dl-gtitle{{font-family:{disp};font-weight:500;font-size:42px;color:{text};}}
.dl-gsub{{font-family:{bod};font-size:26px;font-weight:500;color:{muted};margin-left:auto;}}
.dl-grow{{position:absolute;left:24px;right:24px;height:54px;border-radius:12px;display:flex;align-items:center;gap:22px;padding:0 16px;}}
.dl-gbar{{display:block;height:18px;border-radius:9px;background:{hair};}}
.dl-gbar.soft{{opacity:0.55;}}
.dl-gname{{font-family:{bod};font-weight:700;font-size:34px;letter-spacing:0.1em;color:{acc};}}
.dl-gdesc{{font-family:{bod};font-size:28px;color:{muted};}}
.dl-fly{{position:absolute;height:58px;line-height:44px;padding:5px 14px;border-radius:10px;background:{paper};border:2px solid {acc};font-family:{bod};font-weight:700;font-size:34px;
  letter-spacing:0.1em;color:{acc};box-shadow:0 14px 30px rgba(155,85,96,0.28);opacity:0;}}
/* weight chart and mixing bowl */
.dl-wlabel{{display:flex;align-items:center;gap:8px;font-family:{bod};font-size:26px;font-weight:600;color:{muted};opacity:0;}}
.dl-arrow{{position:absolute;width:4px;border-radius:2px;background:color-mix(in srgb,{acc} 60%,transparent);}}
.dl-arrow::after{{content:"";position:absolute;left:-9px;bottom:-4px;border-left:11px solid transparent;border-right:11px solid transparent;border-top:16px solid color-mix(in srgb,{acc} 60%,transparent);}}
.dl-mix{{opacity:0;}}
.dl-bowl{{position:absolute;left:34px;top:18px;width:200px;height:120px;}}
.dl-mdrop{{position:absolute;top:24px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;background:radial-gradient(circle at 38% 35%,#FFFFFF 0%,{blush} 55%,{acc} 100%);opacity:0;}}
.dl-mtext{{position:absolute;left:270px;right:30px;top:0;bottom:0;display:flex;align-items:center;font-family:{disp};font-style:italic;font-size:42px;line-height:1.1;color:{text};opacity:0;}}
/* 1 % limit */
.dl-limit{{position:absolute;height:0;border-top:4px dashed {acc};}}
.dl-chip.lim{{background:{acc};color:#FFFFFF;font-size:28px;padding:6px 16px;}}
.dl-chip.lim.q{{background:{amber};}}
.dl-legend{{position:absolute;display:flex;align-items:center;gap:16px;font-family:{bod};font-size:32px;font-weight:500;color:{text};opacity:0;}}
.dl-legend .sq{{display:inline-block;width:22px;height:22px;background:{acc};}}
.dl-legend .sq.dash{{background:none;border:3px dashed {muted};border-radius:50%;}}
/* comparison */
.dl-cmp{{padding:20px 36px 14px;opacity:0;}}
.dl-ctitle{{font-family:{disp};font-weight:500;font-size:40px;line-height:1.15;color:{text};margin-bottom:4px;}}
.dl-cmp.R .dl-ctitle{{color:{red};}}
.dl-crow{{display:flex;align-items:center;gap:18px;height:46px;font-family:{bod};font-size:32px;line-height:1.2;color:{text};}}
.dl-mk{{display:inline-block;flex:none;width:22px;height:22px;}}
.dl-mk.fact{{background:{acc};}}
.dl-mk.gap{{border:3px dashed {red};border-radius:50%;}}
/* callouts and CosIng */
.dl-brace{{position:absolute;width:10px;border:4px solid {acc};border-left:none;border-radius:0 12px 12px 0;}}
.dl-call{{position:absolute;display:flex;align-items:center;gap:14px;opacity:0;}}
.dl-cnum{{display:inline-flex;flex:none;width:46px;height:46px;border-radius:50%;background:{acc};color:#FFFFFF;align-items:center;justify-content:center;font-family:{bod};font-weight:700;font-size:28px;}}
.dl-ctext{{font-family:{bod};font-weight:600;font-size:28px;line-height:1.12;color:{text};}}
.dl-lens{{position:absolute;width:96px;height:96px;opacity:0;filter:drop-shadow(0 8px 12px rgba(74,47,52,0.2));}}
.dl-cos{{opacity:0;}}
.dl-search{{position:absolute;left:30px;right:30px;top:18px;height:62px;border-radius:999px;border:2px solid {hair};background:{surf};display:flex;align-items:center;gap:14px;padding:0 22px;}}
.dl-cname{{font-family:{disp};font-weight:500;font-size:40px;color:{text};}}
.dl-caret{{display:inline-block;width:3px;height:36px;background:{acc};opacity:0;}}
.dl-csub{{position:absolute;left:52px;top:88px;font-family:{bod};font-size:28px;font-weight:500;color:{muted};opacity:0;}}
/* close */
.dl-jarbox{{position:absolute;opacity:0;}}
.dl-jar{{position:absolute;left:0;top:0;width:300px;height:260px;filter:drop-shadow(0 18px 24px rgba(74,47,52,0.18));}}
.dl-btn{{position:absolute;left:30px;width:240px;top:284px;height:66px;border-radius:999px;display:flex;align-items:center;justify-content:center;
  font-family:{bod};font-weight:700;font-size:30px;background:{hair};color:{muted};opacity:0.75;}}
.dl-gate{{position:absolute;height:76px;border-radius:16px;display:flex;align-items:center;gap:16px;padding:0 28px;font-family:{bod};font-weight:700;font-size:32px;
  color:{red};background:color-mix(in srgb,{red} 9%,{paper});border:2px solid {red};opacity:0;}}
.dl-gate.ok{{color:{green};background:color-mix(in srgb,{green} 9%,{paper});border-color:{green};}}
.dl-gdot{{width:16px;height:16px;border-radius:50%;background:{red};}}
.dl-gsq{{width:20px;height:20px;background:{green};}}
.dl-sweep{{position:absolute;display:block;height:36px;border-radius:10px;opacity:0;
  background:linear-gradient(90deg,transparent,color-mix(in srgb,{blush} 45%,transparent) 20%,color-mix(in srgb,{blush} 45%,transparent) 80%,transparent);}}
.dl-sign{{position:absolute;left:0;width:864px;text-align:center;opacity:0;}}
.dl-sword{{display:flex;align-items:center;justify-content:center;gap:18px;font-family:{disp};font-weight:500;font-size:96px;line-height:1.05;letter-spacing:0.03em;color:{text};}}
.dl-sdrop{{width:64px;height:78px;}}
.dl-sclaim{{margin-top:12px;font-family:{disp};font-style:italic;font-size:44px;color:{acc};}}
.dl-sdisc{{margin-top:8px;font-family:{bod};font-size:28px;font-weight:500;color:{muted};}}
"""


_CSS_Q1 = CSS


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):  # noqa: F811 (Q1 CSS plus the general scenes)
    acc, text, muted = pal["accent"], pal["text"], pal["muted"]
    paper, hair, surf = pal.get("paper", "#FFFFFF"), pal.get("hairline", "#E8D9D4"), pal.get("surface", "#FFFCF9")
    blush, amber = pal.get("blush", acc), pal.get("signal_amber", acc)
    red, green = pal.get("signal_red", "#8E2F45"), pal.get("signal_green", "#4F7A62")
    disp, bod = f"'FN {display}'", f"'FN {body}'"
    return _CSS_Q1(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
/* general Dewlane scenes (week 1) */
.dl-glyph{{display:inline-flex;flex:none;}}
.dl-glyph svg{{width:100%;height:100%;fill:none;stroke:{acc};stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}}
.dl-glyph.lg{{width:96px;height:96px;}}
.dl-glyph.sm{{width:64px;height:64px;margin-left:auto;opacity:0.9;}}
.dl-pack{{position:absolute;opacity:0;filter:drop-shadow(0 26px 36px rgba(74,47,52,0.22));}}
.dl-pcap{{position:absolute;left:22%;right:22%;top:0;border-radius:16px 16px 6px 6px;background:linear-gradient(90deg,#F3E3DE,#CDB1AC);}}
.dl-pack.jar .dl-pcap{{left:6%;right:6%;border-radius:22px;background:linear-gradient(90deg,{blush},color-mix(in srgb,{blush} 70%,{acc}));}}
.dl-pbody{{position:absolute;left:0;right:0;bottom:0;border-radius:44px 44px 30px 30px;background:linear-gradient(90deg,#FFFFFF 0%,#F6ECE8 55%,#E3CFCA 100%);border:2px solid {hair};}}
.dl-pack.jar .dl-pbody{{border-radius:40px;}}
.dl-plab{{position:absolute;background:{paper};border:1px solid {hair};border-radius:14px;padding:22px 20px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:6px;}}
.dl-ptitle{{font-family:{disp};font-weight:500;font-size:52px;line-height:1.05;color:{text};}}
.dl-psub{{font-family:{bod};font-weight:600;font-size:26px;letter-spacing:0.08em;color:{muted};text-transform:uppercase;}}
.dl-psym{{margin-top:auto;display:flex;align-items:center;gap:12px;font-family:{bod};font-weight:700;font-size:40px;color:{acc};}}
.dl-back{{position:absolute;left:0;top:0;opacity:0;}}
.dl-doc{{display:flex;align-items:center;gap:22px;padding:0 30px;opacity:0;background:linear-gradient(180deg,{paper},{surf});}}
.dl-par{{font-family:{disp};font-size:76px;line-height:1;color:{acc};}}
.dl-dtxt{{display:flex;flex-direction:column;gap:4px;}}
.dl-dtxt b{{font-family:{bod};font-weight:700;font-size:34px;color:{text};}}
.dl-dtxt span{{font-family:{bod};font-weight:500;font-size:28px;color:{muted};}}
.dl-dtag{{position:relative;margin-left:auto;font-size:26px;padding:6px 16px;}}
.dl-fcard{{opacity:0;}}
.dl-frow{{position:absolute;left:36px;right:36px;display:flex;align-items:center;gap:20px;border-bottom:1px solid {hair};opacity:0;}}
.dl-frow:last-child{{border-bottom:none;}}
.dl-ftxt{{flex:1;font-family:{bod};font-weight:500;font-size:36px;line-height:1.18;color:{text};}}
.dl-fval{{flex:none;font-family:{disp};font-weight:600;font-size:42px;color:{acc};}}
.dl-mk.open{{width:26px;height:13px;background:{amber};border-radius:13px 13px 0 0;}}
.dl-mk.ok{{background:{green};}}
.dl-mk.interp{{width:20px;height:20px;background:#7A5AC8;transform:rotate(45deg);}}
.dl-bcard{{opacity:0;}}
.dl-bcap{{position:absolute;left:36px;right:36px;top:22px;display:flex;align-items:center;gap:12px;font-family:{bod};font-weight:600;font-size:28px;color:{muted};}}
.dl-brow{{position:absolute;left:36px;right:36px;height:72px;display:flex;align-items:center;gap:18px;opacity:0;}}
.dl-blab{{flex:0 0 270px;font-family:{bod};font-weight:600;font-size:30px;line-height:1.12;color:{text};}}
.dl-btrack{{flex:1;height:26px;border-radius:13px;background:color-mix(in srgb,{hair} 55%,transparent);}}
.dl-bfill{{display:block;height:100%;border-radius:13px;background:linear-gradient(90deg,color-mix(in srgb,{acc} 55%,{blush}),{acc});}}
.dl-bval{{flex:0 0 150px;text-align:right;font-family:{disp};font-weight:600;font-size:40px;color:{acc};}}
.dl-note{{left:32px;}}
.dl-chip.amber.dl-note{{}}
.dl-tcard{{opacity:0;}}
.dl-tline{{position:absolute;left:96px;top:56px;width:4px;border-radius:2px;background:color-mix(in srgb,{acc} 55%,transparent);}}
.dl-tnode{{position:absolute;left:70px;right:36px;display:flex;align-items:flex-start;gap:26px;opacity:0;}}
.dl-tdot{{flex:none;width:56px;height:56px;border-radius:50%;background:{paper};border:5px solid {acc};}}
.dl-tdate{{flex:0 0 180px;font-family:{disp};font-weight:600;font-size:44px;line-height:56px;color:{acc};}}
.dl-ttxt{{flex:1;font-family:{bod};font-weight:500;font-size:32px;line-height:1.2;color:{text};padding-top:8px;}}
.dl-vcard{{padding:26px 26px;opacity:0;}}
.dl-vcard.myth{{border:3px dashed {amber};background:color-mix(in srgb,{amber} 5%,{paper});}}
.dl-vtag{{display:inline-block;font-family:{bod};font-weight:700;font-size:26px;letter-spacing:0.08em;text-transform:uppercase;color:{muted};margin-bottom:6px;}}
.dl-vcard.myth .dl-vtag{{color:{amber};}}
.dl-vtitle{{font-family:{disp};font-weight:500;font-size:46px;line-height:1.08;color:{text};margin-bottom:18px;overflow-wrap:anywhere;hyphens:manual;}}
.dl-vrow{{display:flex;align-items:flex-start;gap:16px;padding:12px 0;font-family:{bod};font-weight:500;font-size:30px;line-height:1.2;color:{text};opacity:0;}}
.dl-vrow .dl-mk{{margin-top:8px;}}
.dl-verdict{{left:32px;top:524px;max-width:800px;white-space:normal;}}
.dl-scard{{display:flex;align-items:center;gap:26px;padding:0 34px;opacity:0;}}
.dl-snum{{flex:none;display:inline-flex;width:72px;height:72px;border-radius:50%;background:{acc};color:#FFFFFF;align-items:center;justify-content:center;font-family:{disp};font-weight:600;font-size:40px;}}
.dl-stxt{{display:flex;flex-direction:column;gap:6px;}}
.dl-stxt b{{font-family:{bod};font-weight:700;font-size:36px;line-height:1.12;color:{text};}}
.dl-stxt span{{font-family:{bod};font-weight:500;font-size:29px;line-height:1.2;color:{muted};}}
"""


# --- brand-wide background layer --------------------------------------------------------------------

# camera path per beat (x, y in px for the nearest plane); far planes move less (parallax)
CAM = [(0, 0), (-46, -36), (34, -70), (-30, -104), (42, -132), (-38, -160), (10, -186), (-20, -200)]
DEW = [  # x, y, size, plane (0 far .. 2 near); mostly at the edges, never a big drop behind the scene centre
    (70, 330, 26, 0), (1010, 420, 34, 1), (960, 760, 18, 0), (40, 980, 44, 2), (1030, 1180, 70, 2), (120, 1640, 30, 1),
    (900, 1700, 22, 0), (520, 1830, 48, 2), (300, 150, 16, 0), (760, 230, 20, 1), (1000, 1520, 26, 1), (30, 1320, 18, 0),
    (210, 1860, 60, 2), (640, 1680, 14, 0),
]
GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.29 0 0 0 0 0.18 0 0 0 0 0.2 0 0 0 0.55 0'/></filter>"
         "<rect width='240' height='240' filter='url(%23n)'/></svg>\")")


def _dew_html(x: int, y: int, size: int, plane: int, blush: str) -> str:
    blur, op = (2, 0, 3)[plane], (0.45, 0.75, 0.6)[plane]
    return (f'<i class="dlbg-dew" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;opacity:{op};filter:blur({blur}px);'
            f'background:radial-gradient(circle at 35% 30%,#FFFFFF 0%,#FFFFFF 18%,color-mix(in srgb,{blush} 35%,transparent) 55%,'
            f'color-mix(in srgb,{blush} 70%,transparent) 100%);box-shadow:0 {max(2, size // 6)}px {max(4, size // 3)}px rgba(155,85,96,0.18)"></i>')


def LAYER(plan, brand, project_dir, captions):  # noqa: N802
    pal = brand.palette
    blush, acc, bg = pal.get("blush", pal["accent"]), pal["accent"], pal["bg"]
    beats = [b for b in plan.beats if b.start is not None]
    total = max((b.start + b.duration for b in beats), default=60.0)
    planes: dict[int, list[str]] = {0: [], 1: [], 2: []}
    for x, y, sz, pl in DEW:
        planes[pl].append(_dew_html(x, y, sz, pl, blush))
    flacon = (f'<svg class="dlbg-flacon" viewBox="0 0 300 640"><defs>'
              f'<linearGradient id="dlfg" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>'
              f'<stop offset="0.45" stop-color="{blush}" stop-opacity="0.32"/><stop offset="1" stop-color="{acc}" stop-opacity="0.42"/></linearGradient>'
              f'<linearGradient id="dlfc" x1="0" x2="1"><stop offset="0" stop-color="#F3E3DE"/><stop offset="1" stop-color="#CDB1AC"/></linearGradient></defs>'
              f'<rect x="96" y="0" width="108" height="120" rx="14" fill="url(#dlfc)"/><rect x="118" y="112" width="64" height="44" fill="#EADAD5"/>'
              f'<path d="M60 170 Q60 150 90 150 H210 Q240 150 240 170 V600 Q240 636 204 636 H96 Q60 636 60 600 Z" fill="url(#dlfg)" '
              f'stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3"/>'
              f'<path d="M88 200 V580" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.75"/>'
              f'<path d="M214 230 V420" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.5"/></svg>')
    jar = (f'<svg class="dlbg-jar" viewBox="0 0 360 260"><defs><linearGradient id="dljg" x1="0" x2="1">'
           f'<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#F1E3DE"/><stop offset="1" stop-color="#D9C2BC"/></linearGradient></defs>'
           f'<rect x="40" y="20" width="280" height="64" rx="14" fill="{blush}" opacity="0.7"/>'
           f'<rect x="20" y="80" width="320" height="170" rx="34" fill="url(#dljg)"/>'
           f'<path d="M58 110 V220" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.85"/></svg>')
    ribbons = (f'<svg class="dlbg-ribbons" viewBox="0 0 1080 1920" preserveAspectRatio="none"><defs>'
               f'<linearGradient id="dlr1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/>'
               f'<stop offset="1" stop-color="{blush}" stop-opacity="0.26"/></linearGradient>'
               f'<linearGradient id="dlr2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{blush}" stop-opacity="0.34"/>'
               f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient></defs>'
               f'<path d="M-80 1380 C 180 1240 380 1520 640 1420 S 1000 1220 1180 1330 L1180 2000 L-80 2000 Z" fill="url(#dlr1)"/>'
               f'<path d="M-80 1500 C 220 1420 420 1660 700 1560 S 1020 1420 1180 1500" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.7"/>'
               f'<path d="M1180 640 C 1060 700 1050 860 1180 940 Z" fill="url(#dlr2)"/>'
               f'<path d="M-60 520 C 40 600 30 760 -60 860" fill="none" stroke="{blush}" stroke-width="40" stroke-linecap="round" opacity="0.18"/></svg>')
    under = f"""<div id="dlbg">
<div class="dlbg-base"></div>
<div class="dlbg-far" id="dlbg-far"><div class="dlbg-far-in" id="dlbg-far-in">
  <i class="dlbg-blob" style="left:-260px;top:-200px;width:980px;height:900px;background:radial-gradient(closest-side,rgba(255,255,255,0.95),rgba(255,255,255,0))"></i>
  <i class="dlbg-blob" style="left:560px;top:-320px;width:900px;height:760px;background:radial-gradient(closest-side,rgba(255,255,255,0.85),rgba(255,255,255,0))"></i>
  <i class="dlbg-blob" style="left:520px;top:520px;width:900px;height:900px;background:radial-gradient(closest-side,color-mix(in srgb,{blush} 34%,transparent),transparent)"></i>
  <i class="dlbg-blob" style="left:-300px;top:1200px;width:1000px;height:900px;background:radial-gradient(closest-side,color-mix(in srgb,{blush} 28%,transparent),transparent)"></i>
  {''.join(planes[0])}
</div></div>
<div class="dlbg-shafts" id="dlbg-shafts"></div>
<div class="dlbg-mid" id="dlbg-mid"><div class="dlbg-mid-in" id="dlbg-mid-in">{ribbons}{flacon}{jar}{''.join(planes[1])}</div></div>
<div class="dlbg-near" id="dlbg-near"><div class="dlbg-near-in" id="dlbg-near-in">{''.join(planes[2])}</div></div>
<div class="dlbg-grain"></div>
<div class="dlbg-shade"></div>
</div>"""
    head = f"""<style>
#dlbg{{position:absolute;inset:0;z-index:2;overflow:hidden;pointer-events:none;}}
#dlbg i{{position:absolute;display:block;border-radius:50%;}}
.dlbg-base{{position:absolute;inset:0;background:radial-gradient(120% 75% at 16% 6%,#FFFDFB 0%,{bg} 42%,#F1E5E0 78%,#ECDDD7 100%);}}
.dlbg-far,.dlbg-mid,.dlbg-near{{position:absolute;inset:-160px;}}
.dlbg-far-in,.dlbg-mid-in,.dlbg-near-in{{position:absolute;left:160px;top:160px;width:1080px;height:1920px;}}
.dlbg-shafts{{position:absolute;left:-600px;top:-500px;width:2400px;height:2600px;transform:rotate(28deg);opacity:0.5;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,0) 0px,rgba(255,255,255,0) 120px,rgba(255,255,255,0.55) 190px,rgba(255,255,255,0) 300px,rgba(255,255,255,0) 520px);
  -webkit-mask-image:radial-gradient(60% 45% at 30% 30%,#000 0%,transparent 100%);mask-image:radial-gradient(60% 45% at 30% 30%,#000 0%,transparent 100%);}}
.dlbg-ribbons{{position:absolute;left:0;top:0;width:1080px;height:1920px;}}
.dlbg-flacon{{position:absolute;left:868px;top:900px;width:290px;height:620px;opacity:0.6;filter:blur(1.5px);}}
.dlbg-jar{{position:absolute;left:-150px;top:1700px;width:360px;height:260px;opacity:0.55;filter:blur(2px);}}
.dlbg-grain{{position:absolute;inset:0;background-image:{GRAIN};background-size:240px 240px;opacity:0.09;mix-blend-mode:multiply;}}
.dlbg-shade{{position:absolute;inset:0;background:radial-gradient(70% 58% at 50% 46%,transparent 62%,rgba(74,47,52,0.06) 84%,rgba(74,47,52,0.11) 100%);
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 22%);mask-image:linear-gradient(180deg,transparent 0%,#000 22%);}}
</style>"""
    js = [
        f'T.fromTo("#dlbg-far-in",{{x:0,y:0}},{{x:-30,y:-40,duration:{total:.2f},ease:"none"}},0);',
        f'T.fromTo("#dlbg-mid-in",{{x:0,y:0}},{{x:24,y:-60,duration:{total:.2f},ease:"none"}},0);',
        f'T.fromTo("#dlbg-near-in",{{x:0,y:0}},{{x:-20,y:-140,duration:{total:.2f},ease:"none"}},0);',
        f'T.fromTo("#dlbg-shafts",{{x:-260,opacity:0.35}},{{x:260,opacity:0.6,duration:{total:.2f},ease:"sine.inOut"}},0);',
    ]
    for k, b in enumerate(beats):
        cx, cy = CAM[k % len(CAM)]
        t0 = max(0.0, b.start - 0.2)
        for sel, f in (("#dlbg-far", 0.3), ("#dlbg-mid", 0.65), ("#dlbg-near", 1.0)):
            js.append(f'T.to("{sel}",{{x:{cx * f:.1f},y:{cy * f:.1f},duration:1.4,ease:"power2.inOut"}},{t0:.3f});')
    body_end = ("<script>\n(function(){var T=window.__timelines&&window.__timelines.main;if(!T)return;\n"
                + "\n".join(js) + "\nT.seek(0);})();\n</script>")
    return {"head_html": head, "under_scenes_html": under, "body_end_html": body_end, "events": [], "problems": []}


# --- Format "Nahaufnahme" (02.11.2026): animated neutral product up close, scene types nh_*, see nahaufnahme/scenes.py
# A plan with layout.format == "nahaufnahme" gets the studio layer instead of the INCI-label background.
import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("dl_nahaufnahme_scenes", _Path(__file__).resolve().with_name("nahaufnahme") / "scenes.py")
_nh = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_nh)
TEMPLATES.update(_nh.TEMPLATES)
LIMITS.update(_nh.LIMITS)
HOOK_SCENE_TYPES += _nh.HOOK_SCENE_TYPES
_dl_css, _dl_layer = CSS, LAYER


def CSS(*a, **k) -> str:  # noqa: F811
    return _dl_css(*a, **k) + _nh.CSS(*a, **k)


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: F811
    if (getattr(plan, "layout", None) or {}).get("format") == "nahaufnahme":
        return _nh.LAYER(plan, brand, project_dir, captions)
    return _dl_layer(plan, brand, project_dir, captions)


MANIFEST_EXTRA = _nh.MANIFEST_EXTRA
