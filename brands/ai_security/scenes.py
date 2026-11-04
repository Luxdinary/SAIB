"""Scutoria (ai_security) scene types for the case format "Was tust du?" (brand module, fn.render.brand_scenes).

Format bible: OneDrive\\Business\\02 Marke\\Scutoria\\Format-Bibel.md. A video is one concrete situation in a small
business: the case opens (time stamp, place, the object that arrives), the viewer inspects it, decides between
A/B/C, sees the consequence of a wrong choice played out on a clock, then gets the one right step with its
evidence chips, and an emergency step if it already happened. No status bar, no explainer layer, no file as red
thread: the clock and the object of the case carry the video. Loaded for this brand only (docs/direction-system.md 6d).

| scene type   | role in the case           | data |
|--------------|----------------------------|------|
| sc_case      | hook: the case opens       | kicker, time, place, mail{from, addr, time, subject, lines[]}, mail_at, highlight{line, label, at} |
| sc_inspect   | what you check, nothing odd | kicker, headline, rows[{label, value, verdict, at}], finding{text, at}, fact{kind, text, source, at} |
| sc_choice    | the decision A/B/C         | question, options[{key, text, at}], think{seconds, at}, hint |
| sc_timeline  | consequence on the clock   | kicker, tag, headline, items[{time, text, tone, at}], source{kind, label, at} |
| sc_step      | the one right step         | mode rule|fallback, kicker, card{letter, title, sub, at}, strikes[{text, note, at}], steps[{text, at}], sources[{kind, label}], sources_at |
| sc_close     | rule, question, sign-off   | kicker, rule, rule_at, question{text, at}, domain, domain_at, claim, disclaimer |

Times ("at", "mail_at", ...): seconds from the beat start, or "@Wort+0.4" (start of that spoken word in the beat,
from SceneCtx.words). A word that is not found is reported and the default is used. Evidence chips use the
Scutoria markers: fakt (filled square, accent), auslegung (square, violet), beispiel (square, grey), unsicher
(half circle, amber). The case itself is always marked "Beispielfall" (invented situation, sourced mechanism).
"""
from __future__ import annotations

import html
import re

from fn.render.templates import SceneCtx, SceneOut

X0 = 108                     # title-safe left edge
W = 940 - X0                 # 832: right edge x 940, clear of the app icon column (zone_lower_right_px, R5)

LIMITS: dict[str, dict[str, int]] = {
    "sc_case": {"kicker": 34, "time": 14, "place": 40, "from": 30, "addr": 38, "subject": 28, "line": 36, "label": 14},
    "sc_inspect": {"kicker": 34, "headline": 30, "label": 12, "value": 24, "verdict": 14, "finding": 26, "fact": 60, "source": 40},
    "sc_choice": {"question": 20, "option": 36, "hint": 40},
    "sc_timeline": {"kicker": 34, "tag": 14, "headline": 30, "time": 18, "text": 32, "source": 40},
    "sc_step": {"kicker": 34, "title": 28, "sub": 40, "strike": 30, "note": 22, "step": 34, "source": 40},
    "sc_close": {"kicker": 34, "rule": 34, "question": 36, "domain": 24, "claim": 34, "disclaimer": 40},
}
HOOK_SCENE_TYPES = ["sc_case", "cinematic_hook"]     # cinematic_hook keeps the week-1 plans of the old format valid

MARK_WORDS = {
    "de": {"fakt": "Fakt", "auslegung": "Auslegung", "beispiel": "Beispiel", "unsicher": "Unsicher"},
    "en": {"fakt": "Fact", "auslegung": "Interpretation", "beispiel": "Example", "unsicher": "Open"},
}


def _e(s) -> str:
    return html.escape(str(s))


def _chk(scene: str, key: str, val, where: str, out: SceneOut) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _word_start(ctx: SceneCtx, word: str) -> float | None:
    target = re.sub(r"[^\wäöüß]", "", word.lower())
    for w in getattr(ctx, "words", None) or []:
        if re.sub(r"[^\wäöüß]", "", w.text.lower()).startswith(target):
            return w.start
    return None


def _rel(ctx: SceneCtx, v, default: float, out: SceneOut) -> float:
    """Beat-relative seconds from a number or an "@Wort+0.4" string."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and v.startswith("@"):
        m = re.match(r"^@(.+?)([+\-]\d+(?:\.\d+)?)?$", v)
        t = _word_start(ctx, m.group(1)) if m else None
        if t is not None:
            return max(0.0, t - ctx.start + float(m.group(2) or 0))
        out.problems.append(f"word anchor '{v}' not found in the beat; default time used")
    return default


def _hold(ctx: SceneCtx, at: float, hold: float = 1.8) -> float:
    """Latest beat-relative time for a visual event, so the last one stays readable before the cut (Prüfrunde 03.11.2026)."""
    return min(at, max(0.3, ctx.duration - hold))


def _in(ctx: SceneCtx, sel: str, at: float, *, dy: int = 18, dx: int = 0, dur: float = 0.35) -> str:
    return (f'tl.fromTo("#{ctx.sid} {sel}",{{opacity:0,x:{dx},y:{dy}}},'
            f'{{opacity:1,x:0,y:0,duration:{dur:.2f},ease:"power3.out"}},{ctx.t(at):.3f});')


def _frame(ctx: SceneCtx) -> list[str]:
    s = ctx.sid
    return [f'tl.fromTo("#{s} .sc-in",{{opacity:0}},{{opacity:1,duration:{ctx.enter:.2f},ease:"power2.out"}},{ctx.start:.3f});',
            f'tl.to("#{s} .sc-in",{{opacity:0,duration:0.2,ease:"power2.in"}},{max(ctx.start + ctx.enter + 0.05, ctx.end - 0.2):.3f});']


def _mark(kind: str) -> str:
    return f'<i class="sc-mk sc-mk-{_e(kind)}"></i>'


def _src_chip(ctx: SceneCtx, kind: str, label: str, cls: str = "") -> str:
    word = MARK_WORDS.get(ctx.lang, MARK_WORDS["de"]).get(kind, kind)
    return f'<div class="sc-src {cls}">{_mark(kind)}<b>{_e(word)}</b><span>{_e(label)}</span></div>'


def _kicker(ctx: SceneCtx, text: str, top: int, kind: str = "", tag: str = "") -> str:
    m = _mark(kind) if kind else '<i class="sc-tick"></i>'
    t = f'<span class="sc-tag">{_e(tag)}</span>' if tag else ""
    return f'<div class="sc-kicker" style="top:{top}px">{m}<span>{_e(text)}</span>{t}</div>'


# --- sc_case: the case opens (hook) ------------------------------------------------------------------

def case(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    for k in ("kicker", "time", "place"):
        _chk("sc_case", k, d.get(k, ""), k, out)
    m = d.get("mail") or {}
    for k in ("from", "addr", "subject"):
        _chk("sc_case", k, m.get(k, ""), f"mail.{k}", out)
    lines = list(m.get("lines", []))
    for i, ln in enumerate(lines):
        _chk("sc_case", "line", ln, f"mail.lines[{i}]", out)
    hl = d.get("highlight") or {}
    _chk("sc_case", "label", hl.get("label", ""), "highlight.label", out)
    mail_at = min(_rel(ctx, d.get("mail_at", 0.8), 0.8, out), 1.0)   # the case object is on screen within the first second
    body = []
    for i, ln in enumerate(lines):
        mark = i == hl.get("line")
        chip = f'<span class="sc-newchip" id="{s}hc">{_e(hl.get("label", ""))}</span>' if mark and hl.get("label") else ""
        body.append(f'<div class="sc-mail-line{" sc-hl" if mark else ""}" id="{s}l{i}"><span class="sc-hl-bg"></span>'
                    f'<span class="sc-hl-tx">{_e(ln)}</span>{chip}</div>')
    out.html = f"""<div class="sc-in">
  {_kicker(ctx, d.get("kicker", ""), zt, "beispiel")}
  <div class="sc-time" style="top:{zt + 52}px">{_e(d.get("time", ""))}</div>
  <div class="sc-place" style="top:{zt + 168}px">{_e(d.get("place", ""))}</div>
  <div class="sc-paper sc-mail" style="top:{zt + 250}px">
    <div class="sc-mail-head"><span class="sc-avatar"></span><div class="sc-mail-who"><div class="sc-mail-from">{_e(m.get("from", ""))}</div>
      <div class="sc-mail-addr">{_e(m.get("addr", ""))}</div></div><span class="sc-mail-time">{_e(m.get("time", ""))}</span></div>
    <div class="sc-mail-subj">{_e(m.get("subject", ""))}</div>
    <div class="sc-mail-body">{"".join(body)}</div>
  </div>
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sc-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sc-time", 0.15, dy=24))
    out.tl.append(_in(ctx, ".sc-place", 0.45))
    out.events += [ctx.t(0.15)]
    out.tl.append(f'tl.fromTo("#{s} .sc-mail",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.55,ease:"power3.out"}},{ctx.t(mail_at):.3f});')
    out.tl.append(f'tl.to("#{s} .sc-mail",{{y:-10,duration:{max(0.5, ctx.duration - mail_at - 0.6):.2f},ease:"none"}},{ctx.t(mail_at + 0.55):.3f});')
    out.events.append(ctx.t(mail_at))
    for i in range(len(lines)):
        out.tl.append(_in(ctx, f"#{s}l{i}", mail_at + 0.35 + 0.15 * i, dy=10, dur=0.25))
    if hl:
        at = _rel(ctx, hl.get("at", mail_at + 1.6), mail_at + 1.6, out)
        out.tl.append(f'tl.fromTo("#{s}l{hl.get("line", 0)} .sc-hl-bg",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{ctx.t(at):.3f});')
        if hl.get("label"):
            out.tl.append(f'tl.fromTo("#{s}hc",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{ctx.t(at + 0.3):.3f});')
        out.events.append(ctx.t(at))
    return out


# --- sc_inspect: what you check, nothing stands out -------------------------------------------------

def inspect(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    _chk("sc_inspect", "kicker", d.get("kicker", ""), "kicker", out)
    _chk("sc_inspect", "headline", d.get("headline", ""), "headline", out)
    rows = list(d.get("rows", []))
    row_h, card_top = 104, zt + 160
    rhtml = []
    for i, r in enumerate(rows):
        for k in ("label", "value", "verdict"):
            _chk("sc_inspect", k, r.get(k, ""), f"rows[{i}].{k}", out)
        rhtml.append(f'<div class="sc-row" id="{s}r{i}" style="top:{24 + i * row_h}px"><span class="sc-row-label">{_e(r.get("label", ""))}</span>'
                     f'<span class="sc-row-value">{_e(r.get("value", ""))}</span><span class="sc-verdict" id="{s}v{i}">{_e(r.get("verdict", ""))}</span></div>')
    card_h = 48 + row_h * len(rows)
    fin = d.get("finding") or {}
    _chk("sc_inspect", "finding", fin.get("text", ""), "finding", out)
    fact = d.get("fact") or {}
    _chk("sc_inspect", "fact", fact.get("text", ""), "fact.text", out)
    _chk("sc_inspect", "source", fact.get("source", ""), "fact.source", out)
    fin_top = card_top + card_h + 30
    fact_top = fin_top + 92
    fact_html = ""
    if fact:
        word = MARK_WORDS.get(ctx.lang, MARK_WORDS["de"]).get(fact.get("kind", "fakt"), "")
        fact_html = (f'<div class="sc-fact" style="top:{fact_top}px"><div class="sc-fact-head">{_mark(fact.get("kind", "fakt"))}<b>{_e(word)}</b>'
                     f'<span>{_e(fact.get("source", ""))}</span></div><div class="sc-fact-text">{_e(fact.get("text", ""))}</div></div>')
    out.html = f"""<div class="sc-in">
  {_kicker(ctx, d.get("kicker", ""), zt)}
  <div class="sc-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="sc-card sc-rows" style="top:{card_top}px;height:{card_h}px"><div class="sc-scan" id="{s}scan"></div>{"".join(rhtml)}</div>
  {f'<div class="sc-finding" style="top:{fin_top}px">{_e(fin.get("text", ""))}</div>' if fin else ""}
  {fact_html}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sc-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sc-h2", 0.15))
    out.tl.append(_in(ctx, ".sc-rows", 0.3, dy=30))
    out.events.append(ctx.t(0.15))
    prev = 0.6
    for i, r in enumerate(rows):
        at = _rel(ctx, r.get("at", prev + 0.9), prev + 0.9, out)
        prev = at
        out.tl.append(f'tl.to("#{s}scan",{{y:{24 + i * row_h},opacity:1,duration:0.35,ease:"power2.inOut"}},{ctx.t(at - 0.2):.3f});')
        out.tl.append(_in(ctx, f"#{s}r{i}", at - 0.1, dx=-16, dy=0, dur=0.3))
        out.tl.append(f'tl.fromTo("#{s}v{i}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{ctx.t(at + 0.35):.3f});')
        out.events.append(ctx.t(at))
    if fin:
        at = _rel(ctx, fin.get("at", prev + 1.2), prev + 1.2, out)
        out.tl.append(f'tl.to("#{s}scan",{{opacity:0,duration:0.2}},{ctx.t(at - 0.2):.3f});')
        out.tl.append(_in(ctx, ".sc-finding", at, dy=16))
        out.events.append(ctx.t(at))
    if fact:
        at = _rel(ctx, fact.get("at", prev + 2.5), prev + 2.5, out)
        out.tl.append(_in(ctx, ".sc-fact", at, dy=24, dur=0.4))
        out.events.append(ctx.t(at))
    return out


# --- sc_choice: the decision -------------------------------------------------------------------------

def choice(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    _chk("sc_choice", "question", d.get("question", ""), "question", out)
    _chk("sc_choice", "hint", d.get("hint", ""), "hint", out)
    opts = list(d.get("options", []))
    step = int(min(220, (zt + ctx.zone_h - (zt + 150) - 110) / max(1, len(opts))))   # options spread over the zone
    ohtml = []
    for i, o in enumerate(opts):
        _chk("sc_choice", "option", o.get("text", ""), f"options[{i}].text", out)
        ohtml.append(f'<div class="sc-opt" id="{s}o{i}" style="top:{zt + 150 + i * step}px"><span class="sc-key">{_e(o.get("key", "ABC"[i % 3]))}</span>'
                     f'<span class="sc-opt-tx">{_e(o.get("text", ""))}</span></div>')
    bar_top = zt + 150 + len(opts) * step + 20
    think = d.get("think") or {}
    out.html = f"""<div class="sc-in">
  <div class="sc-question" style="top:{zt}px">{_e(d.get("question", ""))}</div>
  {"".join(ohtml)}
  {f'<div class="sc-bar" style="top:{bar_top}px"><div class="sc-bar-fill" id="{s}bar"></div></div><div class="sc-hint" style="top:{bar_top + 30}px">{_e(d.get("hint", ""))}</div>' if think else ""}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(f'tl.fromTo("#{s} .sc-question",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{ctx.t(0.05):.3f});')
    out.events.append(ctx.t(0.05))
    prev = 0.4
    for i, o in enumerate(opts):
        at = _rel(ctx, o.get("at", prev + 1.2), prev + 1.2, out)
        prev = at
        out.tl.append(_in(ctx, f"#{s}o{i}", at, dx=40, dy=0, dur=0.35))
        out.tl.append(f'tl.fromTo("#{s}o{i} .sc-key",{{scale:0.6}},{{scale:1,duration:0.3,ease:"back.out(2.2)"}},{ctx.t(at + 0.1):.3f});')
        out.events.append(ctx.t(at))
    if think:
        at = _rel(ctx, think.get("at", prev + 1.0), prev + 1.0, out)
        secs = float(think.get("seconds", 3.0))
        out.tl.append(_in(ctx, ".sc-bar", at, dy=0, dur=0.2))
        out.tl.append(f'tl.fromTo("#{s}bar",{{scaleX:1}},{{scaleX:0,duration:{secs:.2f},ease:"none"}},{ctx.t(at):.3f});')
        out.tl.append(_in(ctx, ".sc-hint", at + 0.1, dy=10))
        out.events.append(ctx.t(at))
    return out


# --- sc_timeline: the consequence on the clock -------------------------------------------------------

def timeline(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    for k in ("kicker", "tag", "headline"):
        _chk("sc_timeline", k, d.get(k, ""), k, out)
    items = list(d.get("items", []))
    src = d.get("source") or {}
    top0 = zt + 190
    avail = zt + ctx.zone_h - top0 - (64 if src else 0) - 16
    ih = int(min(175, avail / max(1, len(items))))      # spread the clock over the whole zone (y 290-1100)
    ihtml = []
    for i, it in enumerate(items):
        _chk("sc_timeline", "time", it.get("time", ""), f"items[{i}].time", out)
        _chk("sc_timeline", "text", it.get("text", ""), f"items[{i}].text", out)
        tone = it.get("tone", "")
        ihtml.append(f'<div class="sc-ti sc-tone-{_e(tone or "plain")}" id="{s}i{i}" style="top:{top0 + i * ih}px"><span class="sc-dot" id="{s}d{i}"></span>'
                     f'<div class="sc-ti-time">{_e(it.get("time", ""))}</div><div class="sc-ti-text">{_e(it.get("text", ""))}</div></div>')
    rail_h = max(0, (len(items) - 1) * ih)
    _chk("sc_timeline", "source", src.get("label", ""), "source", out)
    src_top = top0 + len(items) * ih + 12
    out.html = f"""<div class="sc-in">
  {_kicker(ctx, d.get("kicker", ""), zt, "", d.get("tag", ""))}
  <div class="sc-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="sc-rail" style="top:{top0 + 22}px;height:{rail_h}px"><div class="sc-rail-fill" id="{s}rail"></div></div>
  {"".join(ihtml)}
  {f'<div class="sc-srcrow" style="top:{src_top}px">{_src_chip(ctx, src.get("kind", "fakt"), src.get("label", ""))}</div>' if src else ""}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sc-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sc-h2", 0.15))
    out.events.append(ctx.t(0.15))
    prev, n = 0.5, len(items)
    for i, it in enumerate(items):
        at = _hold(ctx, _rel(ctx, it.get("at", prev + 2.0), prev + 2.0, out))
        if i > 0 and n > 1:
            frac = i / (n - 1)
            out.tl.append(f'tl.to("#{s}rail",{{scaleY:{frac:.3f},duration:{max(0.3, min(0.8, at - prev)):.2f},ease:"power1.inOut"}},{ctx.t(max(prev, at - 0.8)):.3f});')
        prev = at
        out.tl.append(f'tl.fromTo("#{s}d{i}",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{ctx.t(at):.3f});')
        out.tl.append(_in(ctx, f"#{s}i{i} .sc-ti-time", at + 0.05, dx=-14, dy=0, dur=0.3))
        out.tl.append(_in(ctx, f"#{s}i{i} .sc-ti-text", at + 0.15, dx=-14, dy=0, dur=0.3))
        out.events.append(ctx.t(at))
    if src:
        at = _hold(ctx, _rel(ctx, src.get("at", 0.8), 0.8, out))
        out.tl.append(_in(ctx, ".sc-srcrow", at, dy=12))
    return out


# --- sc_step: the one right step (rule) or the emergency step (fallback) ----------------------------

def step(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    mode = d.get("mode", "rule")
    _chk("sc_step", "kicker", d.get("kicker", ""), "kicker", out)
    card = d.get("card") or {}
    _chk("sc_step", "title", card.get("title", ""), "card.title", out)
    _chk("sc_step", "sub", card.get("sub", ""), "card.sub", out)
    tone = "amber" if mode == "fallback" else "green"
    parts = [_kicker(ctx, d.get("kicker", ""), zt),
             f'<div class="sc-card sc-stepcard sc-tone-{tone}" style="top:{zt + 60}px"><span class="sc-bigkey">{_e(card.get("letter", "C"))}</span>'
             f'<div class="sc-stepcard-tx"><div class="sc-step-title">{_e(card.get("title", ""))}</div><div class="sc-step-sub">{_e(card.get("sub", ""))}</div></div></div>']
    y = zt + 60 + 290 + 40
    strikes, steps = list(d.get("strikes", [])), list(d.get("steps", []))
    srcs = list(d.get("sources", []))
    rows = len(strikes) + len(steps)
    avail = zt + ctx.zone_h - y - (len(srcs) * 50 + 14 if srcs else 0) - 8
    gap = int(min(132, avail / rows)) if rows else 0      # rows fill the zone down to y 1100
    for i, st in enumerate(strikes):
        _chk("sc_step", "strike", st.get("text", ""), f"strikes[{i}].text", out)
        _chk("sc_step", "note", st.get("note", ""), f"strikes[{i}].note", out)
        parts.append(f'<div class="sc-strike" id="{s}x{i}" style="top:{y}px"><span class="sc-strike-tx">{_e(st.get("text", ""))}<i class="sc-strike-line" id="{s}xl{i}"></i></span>'
                     f'<span class="sc-strike-note" id="{s}xn{i}">{_e(st.get("note", ""))}</span></div>')
        y += gap
    for i, st in enumerate(steps):
        _chk("sc_step", "step", st.get("text", ""), f"steps[{i}].text", out)
        mk = st.get("mark")          # green|amber|red|q: content of the one step (classes, questions), not numbered to-dos
        badge = (f'<span class="sc-mark sc-mark-{_e(mk)}">{"?" if mk == "q" else ""}</span>' if mk
                 else f'<span class="sc-num">{i + 1}</span>')
        parts.append(f'<div class="sc-numstep" id="{s}n{i}" style="top:{y}px">{badge}<span>{_e(st.get("text", ""))}</span></div>')
        y += gap
    if srcs:
        for i, sc in enumerate(srcs):
            _chk("sc_step", "source", sc.get("label", ""), f"sources[{i}]", out)
        chips = "".join(_src_chip(ctx, sc.get("kind", "fakt"), sc.get("label", "")) for sc in srcs)
        parts.append(f'<div class="sc-srcrow sc-srcs" style="top:{y + 14}px">{chips}</div>')
    out.html = '<div class="sc-in">' + "".join(parts) + "</div>"
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sc-kicker", 0.05, dx=-20, dy=0))
    c_at = _rel(ctx, card.get("at", 0.2), 0.2, out)
    out.tl.append(f'tl.fromTo("#{s} .sc-stepcard",{{opacity:0,y:30,scale:0.97}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{ctx.t(c_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sc-bigkey",{{scale:0.5}},{{scale:1,duration:0.35,ease:"back.out(2.2)"}},{ctx.t(c_at + 0.15):.3f});')
    out.events.append(ctx.t(c_at))
    prev = c_at + 1.0
    for i, st in enumerate(strikes):
        at = _hold(ctx, _rel(ctx, st.get("at", prev + 1.5), prev + 1.5, out))
        prev = at
        out.tl.append(_in(ctx, f"#{s}x{i}", at, dx=-16, dy=0, dur=0.3))
        out.tl.append(f'tl.fromTo("#{s}xl{i}",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out"}},{ctx.t(at + 0.4):.3f});')
        out.tl.append(f'tl.fromTo("#{s}xn{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{ctx.t(at + 0.7):.3f});')
        out.events.append(ctx.t(at))
    for i, st in enumerate(steps):
        at = _hold(ctx, _rel(ctx, st.get("at", prev + 1.5), prev + 1.5, out))
        prev = at
        out.tl.append(_in(ctx, f"#{s}n{i}", at, dx=-16, dy=0, dur=0.3))
        out.events.append(ctx.t(at))
    if srcs:
        at = _hold(ctx, _rel(ctx, d.get("sources_at", 1.0), 1.0, out))
        out.tl.append(_in(ctx, ".sc-srcs", at, dy=12))
        out.events.append(ctx.t(at))
    return out


# --- sc_close: rule, question to the viewer, sign-off ------------------------------------------------

def close(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    for k in ("kicker", "rule", "domain", "claim", "disclaimer"):
        _chk("sc_close", k, d.get(k, ""), k, out)
    q = d.get("question") or {}
    _chk("sc_close", "question", q.get("text", ""), "question", out)
    out.html = f"""<div class="sc-in sc-close">
  <img class="sc-shield" src="assets/logo/scutum-mark.svg" alt="" style="top:{zt + 10}px">
  <div class="sc-close-kicker" style="top:{zt + 150}px">{_e(d.get("kicker", ""))}</div>
  <div class="sc-rule" style="top:{zt + 200}px">{_e(d.get("rule", ""))}</div>
  {f'<div class="sc-ask" style="top:{zt + 420}px"><span>{_e(q.get("text", ""))}</span></div>' if q else ""}
  <div class="sc-domain" style="top:{zt + 540}px">{_e(d.get("domain", ""))}</div>
  <div class="sc-claim" style="top:{zt + 618}px">{_e(d.get("claim", ""))}</div>
  <div class="sc-disc" style="top:{zt + 668}px">{_e(d.get("disclaimer", ""))}</div>
</div>"""
    out.tl.append(f'tl.fromTo("#{s} .sc-in",{{opacity:0}},{{opacity:1,duration:{ctx.enter:.2f}}},{ctx.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sc-shield",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{ctx.t(0.05):.3f});')
    out.tl.append(_in(ctx, ".sc-close-kicker", 0.2, dy=10))
    r_at = _rel(ctx, d.get("rule_at", 0.3), 0.3, out)
    out.tl.append(_in(ctx, ".sc-rule", r_at, dy=24, dur=0.45))
    out.events += [ctx.t(0.05), ctx.t(r_at)]
    if q:
        at = _rel(ctx, q.get("at", r_at + 2.5), r_at + 2.5, out)
        out.tl.append(f'tl.fromTo("#{s} .sc-ask",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{ctx.t(at):.3f});')
        out.events.append(ctx.t(at))
    d_at = _rel(ctx, d.get("domain_at", 0.8), 0.8, out)
    out.tl.append(_in(ctx, ".sc-domain", d_at, dy=12))
    out.tl.append(_in(ctx, ".sc-claim", d_at + 0.3, dy=10))
    out.tl.append(_in(ctx, ".sc-disc", d_at + 0.5, dy=10))
    out.events.append(ctx.t(d_at))
    return out


TEMPLATES = {"sc_case": case, "sc_inspect": inspect, "sc_choice": choice, "sc_timeline": timeline, "sc_step": step, "sc_close": close}


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):  # noqa: N802 (contract name)
    acc, txt, mut = pal.get("accent", "#4f8cff"), pal.get("text", "#e9eef8"), pal.get("muted", "#a1adc4")
    surf, raised = pal.get("surface", "#121b2f"), pal.get("surface_raised", "#19243b")
    hair = pal.get("hairline", "rgba(226,232,246,0.12)")
    amber, red, green = pal.get("signal_amber", "#ffd166"), pal.get("signal_red", "#ff6b6b"), pal.get("signal_green", "#2ec4b6")
    paper, pink = pal.get("paper", "#fbfbfd"), pal.get("paper_ink", "#141a24")
    violet = pal.get("marker_interpretation", "#b07cff")
    on_sig = pal.get("on_signal", "#0a0c10")
    D, B, M = f"'FN {display}'", f"'FN {body}'", f"'FN {mono}'"
    return f"""
.sc-in{{position:absolute;inset:0;}}
.sc-kicker{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:center;gap:14px;font-family:{M};font-size:28px;letter-spacing:0.12em;text-transform:uppercase;color:{mut};}}
.sc-tick{{display:inline-block;width:28px;height:3px;background:{acc};}}
.sc-tag{{margin-left:auto;font-family:{M};font-size:28px;letter-spacing:0.1em;color:{mut};border:2px solid {hair};border-radius:999px;padding:4px 16px;}}
.sc-mk{{display:inline-block;width:20px;height:20px;flex:none;background:{acc};}}
.sc-mk-fakt{{background:{acc};}}
.sc-mk-auslegung{{background:{violet};}}
.sc-mk-beispiel{{background:#8a93a6;}}
.sc-mk-unsicher{{background:linear-gradient(90deg,{amber} 50%,transparent 50%);border:2px solid {amber};border-radius:50%;}}
.sc-time{{position:absolute;left:{X0}px;font-family:{M};font-weight:500;font-size:96px;line-height:1.1;color:{txt};letter-spacing:0.02em;}}
.sc-place{{position:absolute;left:{X0}px;width:{W}px;font-family:{B};font-size:38px;color:{mut};}}
.sc-paper{{position:absolute;left:{X0}px;width:{W}px;background:{paper};color:{pink};border-radius:20px;box-shadow:0 24px 60px rgba(0,0,0,0.45);}}
.sc-mail{{padding:30px 40px 36px;box-sizing:border-box;}}
.sc-mail-head{{display:flex;align-items:center;gap:20px;}}
.sc-avatar{{width:64px;height:64px;border-radius:50%;background:#d8dde8;flex:none;}}
.sc-mail-who{{flex:1;min-width:0;}}
.sc-mail-from{{font-family:{D};font-weight:700;font-size:36px;line-height:1.2;}}
.sc-mail-addr{{font-family:{M};font-size:26px;color:#5b6475;line-height:1.3;}}
.sc-mail-time{{font-family:{M};font-size:26px;color:#5b6475;}}
.sc-mail-subj{{margin-top:22px;font-family:{D};font-weight:800;font-size:48px;line-height:1.2;}}
.sc-mail-body{{margin-top:14px;}}
.sc-mail-line{{position:relative;font-family:{B};font-size:38px;line-height:1.5;display:flex;align-items:center;gap:14px;}}
.sc-hl-bg{{position:absolute;left:-10px;right:-10px;top:4px;bottom:4px;background:rgba(255,209,102,0.55);transform-origin:left center;transform:scaleX(0);border-radius:6px;}}
.sc-hl-tx{{position:relative;}}
.sc-newchip{{position:relative;font-family:{M};font-size:28px;letter-spacing:0.08em;text-transform:uppercase;background:{pink};color:{amber};border-radius:999px;padding:2px 14px;}}
.sc-h2{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:{display_w};font-size:62px;line-height:1.12;color:{txt};}}
.sc-card{{position:absolute;left:{X0}px;width:{W}px;background:{surf};border:2px solid {hair};border-radius:20px;box-shadow:0 18px 40px rgba(0,0,0,0.35);box-sizing:border-box;}}
.sc-rows{{overflow:hidden;}}
.sc-row{{position:absolute;left:24px;right:24px;height:96px;display:flex;align-items:center;gap:16px;border-bottom:2px solid {hair};}}
.sc-row:last-of-type{{border-bottom:none;}}
.sc-row-label{{width:214px;flex:none;font-family:{M};font-size:28px;letter-spacing:0.08em;text-transform:uppercase;color:{mut};}}
.sc-row-value{{flex:1;font-family:{B};font-size:36px;line-height:1.15;color:{txt};}}
.sc-verdict{{font-family:{M};font-size:28px;color:{mut};border:2px solid {hair};border-radius:999px;padding:4px 14px;}}
.sc-scan{{position:absolute;left:0;right:0;top:0;height:96px;background:rgba(79,140,255,0.10);border-left:6px solid {acc};opacity:0;}}
.sc-finding{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:800;font-size:52px;color:{txt};}}
.sc-fact{{position:absolute;left:{X0}px;width:{W}px;background:{raised};border-radius:20px;padding:22px 30px;box-sizing:border-box;border-left:6px solid {acc};}}
.sc-fact-head{{display:flex;align-items:center;gap:12px;font-family:{M};font-size:28px;color:{mut};letter-spacing:0.04em;}}
.sc-fact-head b{{color:{txt};font-weight:500;}}
.sc-fact-text{{margin-top:10px;font-family:{B};font-size:36px;line-height:1.3;color:{txt};}}
.sc-question{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:800;font-size:96px;line-height:1.05;color:{txt};}}
.sc-opt{{position:absolute;left:{X0}px;width:{W}px;height:162px;display:flex;align-items:center;gap:30px;background:{surf};border:2px solid {hair};border-radius:20px;padding:0 32px;box-sizing:border-box;}}
.sc-key{{width:84px;height:84px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:14px;background:{acc};color:#fff;font-family:{D};font-weight:800;font-size:52px;}}
.sc-opt-tx{{font-family:{B};font-size:44px;line-height:1.2;color:{txt};}}
.sc-bar{{position:absolute;left:{X0}px;width:{W}px;height:10px;background:{hair};border-radius:5px;overflow:hidden;}}
.sc-bar-fill{{width:100%;height:100%;background:{amber};transform-origin:left center;}}
.sc-hint{{position:absolute;left:{X0}px;width:{W}px;font-family:{M};font-size:28px;letter-spacing:0.06em;color:{amber};}}
.sc-rail{{position:absolute;left:{X0 + 15}px;width:4px;background:{hair};}}
.sc-rail-fill{{width:100%;height:100%;background:{mut};transform-origin:top center;transform:scaleY(0);}}
.sc-ti{{position:absolute;left:{X0}px;width:{W}px;height:120px;padding-left:70px;box-sizing:border-box;}}
.sc-dot{{position:absolute;left:3px;top:14px;width:28px;height:28px;border-radius:50%;background:{mut};}}
.sc-ti-time{{font-family:{M};font-size:30px;letter-spacing:0.08em;color:{mut};text-transform:uppercase;}}
.sc-ti-text{{margin-top:6px;font-family:{B};font-size:46px;line-height:1.15;color:{txt};}}
.sc-tone-amber .sc-dot{{background:{amber};}} .sc-tone-amber .sc-ti-time{{color:{amber};}}
.sc-tone-red .sc-dot{{background:{red};}} .sc-tone-red .sc-ti-time{{color:{red};}} .sc-tone-red .sc-ti-text{{font-weight:700;}}
.sc-srcrow{{position:absolute;left:{X0}px;width:{W}px;display:flex;flex-direction:column;gap:10px;}}
.sc-src{{display:flex;align-items:center;gap:14px;font-family:{M};font-size:28px;line-height:40px;color:{mut};}}
.sc-src b{{color:{txt};font-weight:500;}}
.sc-stepcard{{height:290px;display:flex;align-items:center;gap:34px;padding:0 36px;background:{raised};}}
.sc-bigkey{{width:150px;height:150px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:20px;font-family:{D};font-weight:800;font-size:96px;color:{on_sig};}}
.sc-tone-green .sc-bigkey{{background:{green};}} .sc-tone-green{{border-color:{green};}}
.sc-tone-amber .sc-bigkey{{background:{amber};}} .sc-stepcard.sc-tone-amber{{border-color:{amber};}}
.sc-step-title{{font-family:{D};font-weight:800;font-size:58px;line-height:1.1;color:{txt};}}
.sc-step-sub{{margin-top:12px;font-family:{B};font-size:38px;line-height:1.25;color:{mut};}}
.sc-strike{{position:absolute;left:{X0}px;width:{W}px;display:flex;flex-direction:column;align-items:flex-start;gap:6px;}}
.sc-strike-tx{{position:relative;font-family:{B};font-size:40px;color:{mut};}}
.sc-strike-line{{position:absolute;left:-6px;right:-6px;top:52%;height:4px;background:{red};transform-origin:left center;transform:scaleX(0);}}
.sc-strike-note{{font-family:{M};font-size:28px;color:{red};white-space:nowrap;}}
.sc-numstep{{position:absolute;left:{X0}px;width:{W}px;height:96px;display:flex;align-items:center;gap:28px;font-family:{B};font-size:44px;line-height:1.15;color:{txt};}}
.sc-num{{width:72px;height:72px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:12px;border:3px solid {amber};color:{amber};font-family:{D};font-weight:800;font-size:36px;}}
.sc-mark{{width:56px;height:56px;flex:none;border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:{D};font-weight:800;font-size:36px;}}
.sc-mark-green{{background:{green};}} .sc-mark-amber{{background:{amber};}} .sc-mark-red{{background:{red};}}
.sc-mark-q{{border:3px solid {amber};color:{amber};}}
.sc-close .sc-shield{{position:absolute;left:{X0 + W // 2 - 55}px;width:110px;height:auto;}}
.sc-close-kicker{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{M};font-size:28px;letter-spacing:0.14em;text-transform:uppercase;color:{mut};}}
.sc-rule{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{D};font-weight:800;font-size:76px;line-height:1.1;color:{txt};}}
.sc-ask{{position:absolute;left:{X0}px;width:{W}px;display:flex;justify-content:center;}}
.sc-ask span{{font-family:{B};font-size:38px;color:{amber};border:3px solid {amber};border-radius:999px;padding:12px 34px;}}
.sc-domain{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{D};font-weight:700;font-size:50px;color:{acc};}}
.sc-claim{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{B};font-size:34px;color:{txt};}}
.sc-disc{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{B};font-size:30px;color:{mut};}}
"""


def MANIFEST_EXTRA(plan):  # noqa: N802 (contract name)
    used = sorted({b.scene_type for b in plan.beats if b.scene_type.startswith("sc_")})
    office = sorted({b.scene_type for b in plan.beats if b.scene_type.startswith("sb_")})
    if office:
        lic = _bu._licence_lines(plan)
        return {"format": {"name": "Scutoria \"Was tust du?\", Testformat \"Du sitzt am Platz\"", "version": "T1 (Testvideo 11/2026)",
                           "concept": "OneDrive\\Business\\02 Marke\\Scutoria\\Testvideo-Konzept Reels 2026-11.md",
                           "scene_types": sorted(set(used) | set(office)),
                           "case": "Beispielfall, nachgestellt: Situation erfunden, Mechanik und Empfehlungen aus den Quellen",
                           "media": "KI-generierte Bilder und Clips (Higgsfield), Hände ja, keine Gesichter, keine Schrift im Bild"},
                "media_licences": lic}
    if not used:
        return {}
    return {"format": {"name": "Scutoria Fall-Format \"Was tust du?\"", "version": "0.1 (Pilot)",
                       "bible": "OneDrive\\Business\\02 Marke\\Scutoria\\Format-Bibel.md", "scene_types": used,
                       "case": "Beispielfall, nachgestellt: Situation erfunden, Mechanik und Empfehlungen aus den Quellen"}}


# --- Testformat "Du sitzt am Platz" (03.11.2026): real office photos and clips, scene types sb_*, see buero.py
import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("ai_security_buero", _Path(__file__).resolve().with_name("buero.py"))
_bu = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_bu)
TEMPLATES.update(_bu.TEMPLATES)
LIMITS.update(_bu.LIMITS)
HOOK_SCENE_TYPES += _bu.HOOK_SCENE_TYPES
LAYER = _bu.LAYER
_sc_css = CSS


def CSS(*a):  # noqa: N802,F811 (contract name)
    return _sc_css(*a) + _bu.CSS(*a)
