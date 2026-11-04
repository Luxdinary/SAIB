"""Scene types of the Scutoria long-form template. Every builder works for 16:9 and 9:16 (fmt.FORMATS).

A builder gets a Ctx (scene id, absolute start/end, format, language, spoken words of the beat with absolute times)
and the scene's `data` dict from the plan; it returns html, GSAP lines, visual event times and problems.
Times in data ("at", "obj_at", ...): seconds from the scene start, or "@Wort+0.4" (start of that spoken word in the
scene). Text fields use *Stern* for one accent-coloured word. Text limits per field in LIMITS (checked, reported).

| type      | use                                   | data |
|-----------|---------------------------------------|------|
| statement | one key sentence, optional sub line   | kicker, text, sub, at, sub_at |
| paper     | a document as paper card              | headline, note, doc{label, title, lines[{text, at, mark, mark_at}]} |
| steps     | numbered steps, the current one blue  | headline, items[{title, sub, at}] |
| compare   | two columns                           | headline, left/right{title, tone, rows[{text, at}]} |
| quote     | short quote from a source             | kind, text, origin, at |
| case      | the case opens (clock, place, object) | kicker, time, place, obj{label, from, subject, lines[]}, obj_at, highlight{line, label, at} |
| choice    | A/B/C with thinking bar               | question, options[{key, text, at}], think{at, seconds} |
| timeline  | consequence on the clock              | kicker, tag, headline, items[{time, text, tone, at}] |
| step      | the right step, wrong ones struck     | kicker, card{letter, title, sub, at}, strikes[{text, note, at}] |
| broll     | B-roll pause with one keyword         | word, sub, at |
| chapters  | chapter overview                      | headline, items[{num, title, at}] |
| close     | pointer, sign-off, end screen         | rule, memo{label, url}, toolkit{label, url}, claim, disclaimer, end_at |
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

LIMITS: dict[str, dict[str, int]] = {
    "statement": {"kicker": 40, "text": 150, "sub": 130},
    "paper": {"headline": 70, "note": 160, "label": 44, "title": 60, "line": 74},
    "steps": {"headline": 60, "title": 52, "sub": 80},
    "compare": {"headline": 70, "title": 34, "row": 56},
    "quote": {"text": 240, "origin": 110},
    "case": {"kicker": 40, "time": 14, "place": 50, "label": 40, "from": 40, "subject": 54, "line": 60, "hl": 22},
    "choice": {"question": 60, "option": 64},
    "timeline": {"kicker": 40, "tag": 16, "headline": 70, "time": 20, "text": 56},
    "step": {"kicker": 40, "title": 46, "sub": 90, "strike": 44, "note": 50},
    "broll": {"word": 40, "sub": 80},
    "chapters": {"headline": 50, "title": 48},
    "close": {"rule": 70, "label": 60, "url": 60, "claim": 40, "disclaimer": 60},
}

MARK_WORDS = {
    "de": {"fakt": "Fakt", "auslegung": "Auslegung", "unsicher": "Unsicher", "luecke": "Lücke", "beispiel": "Beispiel"},
    "en": {"fakt": "Fact", "auslegung": "Interpretation", "unsicher": "Uncertain", "luecke": "Gap", "beispiel": "Example"},
}
TONES = {"neutral": "var(--muted)", "blue": "var(--accent)", "amber": "var(--amber)", "red": "var(--red)", "green": "var(--green)", "violet": "var(--violet)"}


@dataclass
class Ctx:
    sid: str
    start: float
    end: float
    f: dict
    lang: str
    words: list = field(default_factory=list)       # objects with .text .start .end (absolute seconds)
    problems: list = field(default_factory=list)

    def t(self, rel: float) -> float:
        return round(min(self.end - 0.3, self.start + max(0.0, rel)), 3)

    def at(self, v, default: float) -> float:
        """Absolute time from beat-relative seconds or an "@Wort+0.4" anchor."""
        if isinstance(v, (int, float)):
            return self.t(float(v))
        if isinstance(v, str) and v.startswith("@"):
            m = re.match(r"^@(.+?)([+\-]\d+(?:\.\d+)?)?$", v)
            if m:
                target = _norm(m.group(1))
                for w in self.words:
                    if _norm(w.text).startswith(target):
                        return self.t(w.start - self.start + float(m.group(2) or 0))
            self.problems.append(f"{self.sid}: word anchor '{v}' not found; default used")
        return self.t(default)


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", s.lower())


def e(s) -> str:
    """Escape and turn *Wort* into an accent word."""
    out = html.escape(str(s or ""))
    return re.sub(r"\*(.+?)\*", r'<em>\1</em>', out)


def plain(s) -> str:
    return re.sub(r"\*", "", str(s or ""))


def chk(ctx: Ctx, scene: str, key: str, val, where: str) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(plain(val)) > lim:
        ctx.problems.append(f"{ctx.sid} {scene}.{where}: {len(plain(val))} chars > {lim}")


def fin(ctx: Ctx, sel: str, at: float, *, dy: int = 16, dx: int = 0, dur: float = 0.45) -> str:
    return (f'tl.fromTo("#{ctx.sid} {sel}",{{opacity:0,x:{dx},y:{dy}}},'
            f'{{opacity:1,x:0,y:0,duration:{dur:.2f},ease:"power3.out"}},{at:.3f});')


def mark_html(kind: str, lang: str, *, label: bool = True) -> str:
    word = MARK_WORDS.get(lang, MARK_WORDS["de"]).get(kind, kind)
    return f'<span class="mk mk-{html.escape(kind)}"><i></i>{"<b>" + html.escape(word) + "</b>" if label else ""}</span>'


@dataclass
class Out:
    html: str
    tl: list
    events: list


# --- builders ----------------------------------------------------------------------------------------

def statement(ctx: Ctx, d: dict) -> Out:
    for k in ("kicker", "text", "sub"):
        chk(ctx, "statement", k, d.get(k, ""), k)
    a = ctx.at(d.get("at", 0.3), 0.3)
    parts = [f'<div class="st-k">{e(d["kicker"])}</div>' if d.get("kicker") else "",
             f'<div class="st-t">{e(d.get("text"))}</div>',
             f'<div class="st-s">{e(d["sub"])}</div>' if d.get("sub") else ""]
    tl = [fin(ctx, ".st-k", ctx.t(0.1)), fin(ctx, ".st-t", a, dy=22)]
    ev = [a]
    if d.get("sub"):
        sa = ctx.at(d.get("sub_at", 2.0), 2.0)
        tl.append(fin(ctx, ".st-s", sa))
        ev.append(sa)
    return Out(f'<div class="cb center"><div class="st">{"".join(parts)}</div></div>', tl, ev)


def _paper(ctx: Ctx, doc: dict, tl: list, ev: list, scene: str = "paper") -> str:
    chk(ctx, scene, "label", doc.get("label", ""), "doc.label")
    chk(ctx, scene, "title", doc.get("title", ""), "doc.title")
    rows = []
    for i, ln in enumerate(doc.get("lines", [])):
        ln = ln if isinstance(ln, dict) else {"text": ln}
        chk(ctx, scene, "line", ln.get("text", ""), f"doc.lines[{i}]")
        rows.append(f'<div class="pl pl{i}"><span class="pl-t">{e(ln.get("text"))}</span></div>')
        a = ctx.at(ln.get("at", 0.6 + 0.5 * i), 0.6 + 0.5 * i)
        tl.append(fin(ctx, f".pl{i}", a, dy=10, dur=0.35))
        ev.append(a)
        mk = ln.get("mark")
        if mk:
            ma = ctx.at(ln.get("mark_at", ln.get("at", 0.6 + 0.5 * i)), 0.6 + 0.5 * i + 0.4)
            ma = max(ma, a + 0.3)
            tl.append(f'tl.set("#{ctx.sid} .pl{i}",{{className:"pl pl{i} m-{html.escape(mk)}"}},{ma:.3f});')
            ev.append(ma)
    label = f'<div class="pp-l">{e(doc["label"])}</div>' if doc.get("label") else ""
    title = f'<div class="pp-h">{e(doc["title"])}</div>' if doc.get("title") else ""
    return f'<div class="pp">{label}{title}<div class="pp-b">{"".join(rows)}</div></div>'


def paper(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "paper", "headline", d.get("headline", ""), "headline")
    chk(ctx, "paper", "note", d.get("note", ""), "note")
    tl, ev = [], []
    a0 = ctx.t(0.2)
    tl.append(fin(ctx, ".pp", a0, dy=30, dur=0.6))
    side = ""
    if d.get("headline") or d.get("note"):
        side = (f'<div class="side"><div class="sd-h">{e(d.get("headline"))}</div>'
                f'{"<div class=sd-n>" + e(d["note"]) + "</div>" if d.get("note") else ""}</div>')
        tl.append(fin(ctx, ".sd-h", ctx.t(0.1)))
        if d.get("note"):
            na = ctx.at(d.get("note_at", 1.5), 1.5)
            tl.append(fin(ctx, ".sd-n", na))
            ev.append(na)
    body = _paper(ctx, d.get("doc") or {}, tl, ev)
    return Out(f'<div class="cb split">{side}{body}</div>', tl, ev + [a0])


def steps(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "steps", "headline", d.get("headline", ""), "headline")
    items = d.get("items", [])
    tl, ev, rows = [], [], []
    times = []
    for i, it in enumerate(items):
        chk(ctx, "steps", "title", it.get("title", ""), f"items[{i}].title")
        chk(ctx, "steps", "sub", it.get("sub", ""), f"items[{i}].sub")
        a = ctx.at(it.get("at", 0.5 + 2.0 * i), 0.5 + 2.0 * i)
        times.append(a)
        num = it.get("num", i + 1)
        rows.append(f'<div class="si si{i}"><span class="sn">{e(num)}</span><div class="sx"><div class="stt">{e(it.get("title"))}</div>'
                    f'{"<div class=ssb>" + e(it["sub"]) + "</div>" if it.get("sub") else ""}</div></div>')
    for i, a in enumerate(times):
        tl.append(fin(ctx, f".si{i}", a, dx=-18, dy=0))
        tl.append(f'tl.set("#{ctx.sid} .si{i}",{{className:"si si{i} on"}},{a:.3f});')
        if i > 0:
            tl.append(f'tl.set("#{ctx.sid} .si{i-1}",{{className:"si si{i-1} done"}},{a:.3f});')
        ev.append(a)
    side = ""
    if d.get("headline"):
        side = f'<div class="side"><div class="sd-h">{e(d["headline"])}</div></div>'
        tl.append(fin(ctx, ".sd-h", ctx.t(0.1)))
    if len(items) > (5 if ctx.f["dir"] == "row" else 6):
        ctx.problems.append(f"{ctx.sid} steps: {len(items)} items; split into two scenes (max 5 in 16:9, 6 in 9:16)")
    dense = " dense" if len(items) > 4 else ""
    return Out(f'<div class="cb split">{side}<div class="sl{dense}">{"".join(rows)}</div></div>', tl, ev)


def compare(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "compare", "headline", d.get("headline", ""), "headline")
    tl, ev, cols = [], [], []
    for side_key, base in (("left", 0.4), ("right", 2.5)):
        c = d.get(side_key) or {}
        chk(ctx, "compare", "title", c.get("title", ""), f"{side_key}.title")
        tone = TONES.get(c.get("tone", "neutral"), TONES["neutral"])
        ca = ctx.at(c.get("at", base), base)
        rows = []
        for i, r in enumerate(c.get("rows", [])):
            r = r if isinstance(r, dict) else {"text": r}
            chk(ctx, "compare", "row", r.get("text", ""), f"{side_key}.rows[{i}]")
            ra = ctx.at(r.get("at", base + 0.6 + 0.8 * i), base + 0.6 + 0.8 * i)
            ra = max(ra, ca + 0.2)
            rows.append(f'<div class="cr cr-{side_key}{i}"><i style="background:{tone}"></i><span>{e(r.get("text"))}</span></div>')
            tl.append(fin(ctx, f".cr-{side_key}{i}", ra, dy=8, dur=0.3))
            ev.append(ra)
        cols.append(f'<div class="cc cc-{side_key}" style="border-top-color:{tone}"><div class="cc-h" style="color:{tone}">{e(c.get("title"))}</div>{"".join(rows)}</div>')
        tl.insert(0, fin(ctx, f".cc-{side_key}", ca, dy=24))
        ev.append(ca)
    head = f'<div class="cmp-h">{e(d["headline"])}</div>' if d.get("headline") else ""
    if head:
        tl.append(fin(ctx, ".cmp-h", ctx.t(0.1)))
    return Out(f'<div class="cb stack">{head}<div class="cmp">{"".join(cols)}</div></div>', tl, ev)


def quote(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "quote", "text", d.get("text", ""), "text")
    chk(ctx, "quote", "origin", d.get("origin", ""), "origin")
    kind = d.get("kind", "fakt")
    a = ctx.at(d.get("at", 0.3), 0.3)
    oa = ctx.at(d.get("origin_at", 1.6), 1.6)
    # quotation marks only for a verbatim quote; a paraphrase ("verbatim": false) is shown without them
    q = (("„", "“") if ctx.lang == "de" else ("“", "”")) if d.get("verbatim", True) else ("", "")
    h = (f'<div class="cb center"><div class="qt qt-{html.escape(kind)}">{mark_html(kind, ctx.lang) if kind != "none" else ""}'
         f'<div class="qt-t">{q[0]}{e(d.get("text"))}{q[1]}</div><div class="qt-o">{e(d.get("origin"))}</div></div></div>')
    return Out(h, [fin(ctx, ".qt", a, dy=24, dur=0.55), fin(ctx, ".qt-o", oa, dy=6)], [a, oa])


def case(ctx: Ctx, d: dict) -> Out:
    for k in ("kicker", "time", "place"):
        chk(ctx, "case", k, d.get(k, ""), k)
    o = d.get("obj") or {}
    for k in ("label", "from", "subject"):
        chk(ctx, "case", k, o.get(k, ""), f"obj.{k}")
    tl, ev = [], []
    t0 = ctx.t(0.1)
    tl += [fin(ctx, ".cs-k", t0), fin(ctx, ".cs-c", ctx.t(0.35), dy=10), fin(ctx, ".cs-p", ctx.t(0.8))]
    oa = ctx.at(d.get("obj_at", 1.6), 1.6)
    tl.append(f'tl.fromTo("#{ctx.sid} .ob",{{opacity:0,x:120,rotation:2}},{{opacity:1,x:0,rotation:0,duration:0.8,ease:"power3.out"}},{oa:.3f});')
    ev += [t0, oa]
    lines = []
    for i, ln in enumerate(o.get("lines", [])):
        chk(ctx, "case", "line", ln, f"obj.lines[{i}]")
        lines.append(f'<div class="ob-l ob-l{i}">{e(ln)}</div>')
    hl = d.get("highlight") or {}
    hl_html = ""
    if hl:
        chk(ctx, "case", "hl", hl.get("label", ""), "highlight.label")
        ha = max(ctx.at(hl.get("at", oa - ctx.start + 2.0), oa - ctx.start + 2.0), oa + 0.9)
        i = int(hl.get("line", 0))
        tl.append(f'tl.set("#{ctx.sid} .ob-l{i}",{{className:"ob-l ob-l{i} hl"}},{ha:.3f});')
        hl_html = f'<div class="ob-flag">{e(hl.get("label"))}</div>'
        tl.append(fin(ctx, ".ob-flag", ha + 0.1, dx=-12, dy=0, dur=0.3))
        ev.append(ha)
    obj = (f'<div class="ob">{"<div class=pp-l>" + e(o["label"]) + "</div>" if o.get("label") else ""}'
           f'{"<div class=ob-f>" + e(o["from"]) + "</div>" if o.get("from") else ""}'
           f'{"<div class=ob-s>" + e(o["subject"]) + "</div>" if o.get("subject") else ""}'
           f'<div class="ob-b">{"".join(lines)}</div>{hl_html}</div>')
    left = (f'<div class="side cs"><div class="cs-k">{mark_html("beispiel", ctx.lang, label=False)}<span>{e(d.get("kicker"))}</span></div>'
            f'<div class="cs-c">{e(d.get("time"))}</div><div class="cs-p">{e(d.get("place"))}</div></div>')
    return Out(f'<div class="cb split">{left}{obj}</div>', tl, ev)


def choice(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "choice", "question", d.get("question", ""), "question")
    tl, ev, cards = [fin(ctx, ".ch-q", ctx.t(0.1), dy=20)], [], []
    last = 0.0
    for i, op in enumerate(d.get("options", [])):
        chk(ctx, "choice", "option", op.get("text", ""), f"options[{i}]")
        a = ctx.at(op.get("at", 0.9 + 1.2 * i), 0.9 + 1.2 * i)
        last = max(last, a)
        cards.append(f'<div class="co co{i}"><span class="co-k">{e(op.get("key", "ABC"[i]))}</span><span class="co-t">{e(op.get("text"))}</span></div>')
        tl.append(fin(ctx, f".co{i}", a, dy=26, dur=0.45))
        ev.append(a)
    th = d.get("think") or {}
    bar = ""
    if th:
        ta = max(ctx.at(th.get("at", last - ctx.start + 1.0), last - ctx.start + 1.0), last + 0.4)
        secs = float(th.get("seconds", 2.5))
        bar = '<div class="ch-bar"><i></i></div>'
        tl.append(f'tl.fromTo("#{ctx.sid} .ch-bar",{{opacity:0}},{{opacity:1,duration:0.2}},{ta:.3f});')
        tl.append(f'tl.fromTo("#{ctx.sid} .ch-bar i",{{scaleX:1}},{{scaleX:0,duration:{secs:.2f},ease:"none"}},{ta:.3f});')
        ev.append(ta)
    return Out(f'<div class="cb stack"><div class="ch-q">{e(d.get("question"))}</div><div class="chs">{"".join(cards)}</div>{bar}</div>', tl, ev)


def timeline(ctx: Ctx, d: dict) -> Out:
    for k in ("kicker", "tag", "headline"):
        chk(ctx, "timeline", k, d.get(k, ""), k)
    tl, ev, items = [], [], []
    for i, it in enumerate(d.get("items", [])):
        chk(ctx, "timeline", "time", it.get("time", ""), f"items[{i}].time")
        chk(ctx, "timeline", "text", it.get("text", ""), f"items[{i}].text")
        tone = TONES.get(it.get("tone", "neutral"), TONES["neutral"])
        a = ctx.at(it.get("at", 0.6 + 2.2 * i), 0.6 + 2.2 * i)
        items.append(f'<div class="ti ti{i}"><i style="background:{tone};border-color:{tone}"></i><div class="ti-c" style="color:{tone}">{e(it.get("time"))}</div>'
                     f'<div class="ti-t">{e(it.get("text"))}</div></div>')
        tl.append(fin(ctx, f".ti{i}", a, dy=14, dur=0.4))
        ev.append(a)
    head = ""
    if d.get("kicker") or d.get("headline"):
        tag = f'<span class="tag">{mark_html("beispiel", ctx.lang)}</span>' if d.get("tag", True) else ""
        head = f'<div class="tm-h"><div class="tm-k">{e(d.get("kicker"))}{tag}</div><div class="tm-t">{e(d.get("headline"))}</div></div>'
        tl.append(fin(ctx, ".tm-h", ctx.t(0.1)))
    n = max(1, len(items))
    return Out(f'<div class="cb stack">{head}<div class="tml n{n}"><div class="tml-line"></div>{"".join(items)}</div></div>', tl, ev)


def step(ctx: Ctx, d: dict) -> Out:
    c = d.get("card") or {}
    chk(ctx, "step", "kicker", d.get("kicker", ""), "kicker")
    chk(ctx, "step", "title", c.get("title", ""), "card.title")
    chk(ctx, "step", "sub", c.get("sub", ""), "card.sub")
    tl, ev = [], []
    ca = ctx.at(c.get("at", 0.4), 0.4)
    tl.append(fin(ctx, ".sp-card", ca, dy=26, dur=0.55))
    ev.append(ca)
    strikes = []
    for i, s in enumerate(d.get("strikes", [])):
        chk(ctx, "step", "strike", s.get("text", ""), f"strikes[{i}].text")
        chk(ctx, "step", "note", s.get("note", ""), f"strikes[{i}].note")
        a = ctx.at(s.get("at", 2.5 + 1.5 * i), 2.5 + 1.5 * i)
        strikes.append(f'<div class="sk sk{i}"><div class="sk-t"><b>{e(s.get("key", ""))}</b> {e(s.get("text"))}<i class="sk-x"></i></div>'
                       f'<div class="sk-n">{e(s.get("note"))}</div></div>')
        tl.append(fin(ctx, f".sk{i}", a, dy=10, dur=0.3))
        tl.append(f'tl.fromTo("#{ctx.sid} .sk{i} .sk-x",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out"}},{a + 0.35:.3f});')
        ev.append(a)
    kicker = f'<div class="sp-k">{e(d["kicker"])}</div>' if d.get("kicker") else ""
    card = (f'<div class="sp-card"><span class="sp-l">{e(c.get("letter", "B"))}</span><div><div class="sp-t">{e(c.get("title"))}</div>'
            f'<div class="sp-s">{e(c.get("sub"))}</div></div></div>')
    return Out(f'<div class="cb split"><div class="side">{kicker}{card}</div><div class="sks">{"".join(strikes)}</div></div>', tl, ev)


def broll(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "broll", "word", d.get("word", ""), "word")
    chk(ctx, "broll", "sub", d.get("sub", ""), "sub")
    a = ctx.at(d.get("at", 0.6), 0.6)
    sub = f'<div class="br-s">{e(d["sub"])}</div>' if d.get("sub") else ""
    return Out(f'<div class="cb low"><div class="br"><div class="br-w">{e(d.get("word"))}</div>{sub}</div></div>',
               [fin(ctx, ".br", a, dy=20, dur=0.6)], [a])


def chapters(ctx: Ctx, d: dict) -> Out:
    chk(ctx, "chapters", "headline", d.get("headline", ""), "headline")
    tl, ev, rows = [fin(ctx, ".chp-h", ctx.t(0.1))], [], []
    for i, it in enumerate(d.get("items", [])):
        chk(ctx, "chapters", "title", it.get("title", ""), f"items[{i}].title")
        a = ctx.at(it.get("at", 0.5 + 0.7 * i), 0.5 + 0.7 * i)
        rows.append(f'<div class="cp cp{i}"><span class="cp-n">{e(it.get("num", i + 1))}</span><span class="cp-t">{e(it.get("title"))}</span></div>')
        tl.append(fin(ctx, f".cp{i}", a, dx=-14, dy=0, dur=0.35))
        ev.append(a)
    return Out(f'<div class="cb stack"><div class="chp-h">{e(d.get("headline"))}</div><div class="cps">{"".join(rows)}</div></div>', tl, ev)


def close(ctx: Ctx, d: dict, logo_rel: str = "") -> Out:
    for k in ("rule", "claim", "disclaimer"):
        chk(ctx, "close", k, d.get(k, ""), k)
    tl, ev = [], []
    links = []
    for key, base in (("memo", 1.2), ("toolkit", 3.0)):
        it = d.get(key)
        if not it:
            continue
        chk(ctx, "close", "label", it.get("label", ""), f"{key}.label")
        a = ctx.at(it.get("at", base), base)
        links.append(f'<div class="cl-a cl-{key}"><span class="cl-al">{e(it.get("label"))}</span><span class="cl-u">{e(it.get("url"))}</span></div>')
        tl.append(fin(ctx, f".cl-{key}", a, dy=12))
        ev.append(a)
    ra = ctx.at(d.get("rule_at", 0.3), 0.3)
    tl.insert(0, fin(ctx, ".cl-r", ra, dy=18))
    ea = ctx.at(d.get("end_at", max(0.5, ctx.end - ctx.start - 20.0)), max(0.5, ctx.end - ctx.start - 20.0))
    tl.append(f'tl.to("#{ctx.sid} .cl-top",{{opacity:0,duration:0.6}},{ea - 0.6:.3f});')
    tl.append(fin(ctx, ".cl-end", ea, dy=0, dur=0.8))
    ev += [ra, ea]
    logo = f'<img class="cl-logo" src="{logo_rel}" alt="">' if logo_rel else ""
    end = (f'<div class="cl-end">{logo}<div class="cl-wm">SCUTORIA</div><div class="cl-claim">{e(d.get("claim"))}</div>'
           f'<div class="cl-disc">{e(d.get("disclaimer"))}</div></div>')
    top = f'<div class="cl-top"><div class="cl-r">{e(d.get("rule"))}</div>{"".join(links)}</div>'
    return Out(f'<div class="cb center">{top}{end}</div>', tl, ev)


BUILDERS = {"statement": statement, "paper": paper, "steps": steps, "compare": compare, "quote": quote, "case": case,
            "choice": choice, "timeline": timeline, "step": step, "broll": broll, "chapters": chapters, "close": close}


def css(f: dict) -> str:
    """Scene CSS for one format. Sizes scale with f['scale'] (9:16 is larger: phone)."""
    s = float(f["scale"])
    col = f["dir"] == "col"
    px = lambda v: f"{round(v * s)}px"   # noqa: E731
    W, X0, top, bottom = f["W"], f["X0"], f["top"], f["bottom"]
    split_dir = "column" if col else "row"
    return f"""
.cb{{position:absolute;left:{X0}px;width:{W - 2 * X0}px;top:{top}px;height:{bottom - top}px;display:flex;}}
.cb.center{{align-items:center;justify-content:center;}}
.cb.split{{flex-direction:{split_dir};align-items:{'stretch' if col else 'center'};justify-content:center;gap:{px(56 if not col else 36)};}}
.cb.stack{{flex-direction:column;justify-content:center;gap:{px(34)};}}
.cb.low{{align-items:flex-end;justify-content:flex-start;padding-bottom:{px(30)};}}
em{{font-style:normal;color:var(--accent);}}
.side{{flex:{'0 0 auto' if col else '0 0 40%'};display:flex;flex-direction:column;gap:{px(22)};}}
.sd-h{{font-family:'FN Display';font-weight:800;font-size:{px(52)};line-height:1.12;letter-spacing:-0.02em;}}
.sd-n{{font-size:{px(30)};line-height:1.4;color:var(--muted);}}
.st{{max-width:{'100%' if col else '1400px'};}}
.st-k{{font-family:'FN Mono';font-size:{px(24)};color:var(--accent);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:{px(22)};}}
.st-t{{font-family:'FN Display';font-weight:800;font-size:{px(66 if not col else 58)};line-height:1.12;letter-spacing:-0.02em;}}
.st-s{{margin-top:{px(28)};font-size:{px(34)};line-height:1.4;color:var(--muted);}}
.pp{{flex:1 1 auto;background:var(--paper);color:var(--paper-ink);border-radius:20px;padding:{px(34)} {px(40)};box-shadow:0 24px 60px rgba(0,0,0,0.45);max-height:100%;overflow:hidden;}}
.pp-l{{font-family:'FN Mono';font-size:{px(20)};letter-spacing:0.12em;text-transform:uppercase;color:#4a5568;margin-bottom:{px(10)};}}
.pp-h{{font-family:'FN Display';font-weight:800;font-size:{px(36)};line-height:1.15;margin-bottom:{px(18)};}}
.pp-b{{display:flex;flex-direction:column;gap:{px(10)};}}
.pl{{font-size:{px(28)};line-height:1.35;padding:{px(6)} {px(12)};border-radius:8px;border-left:4px solid transparent;}}
.pl.m-hl{{background:rgba(79,140,255,0.16);border-left-color:var(--accent);}}
.pl.m-open{{background:rgba(255,209,102,0.22);border-left:4px dashed #b8860b;}}
.pl.m-ok{{background:rgba(46,196,182,0.16);border-left-color:var(--green);}}
.pl.m-risk{{background:rgba(255,107,107,0.16);border-left-color:var(--red);}}
.pl.m-strike .pl-t{{text-decoration:line-through;text-decoration-color:var(--red);text-decoration-thickness:3px;color:#6b7280;}}
.sl{{flex:1 1 auto;display:flex;flex-direction:column;gap:{px(18)};}}
.sl.dense{{gap:{px(10)};}}
.sl.dense .si{{padding:{px(8)} {px(18)};}}
.sl.dense .stt{{font-size:{px(30)};}}
.sl.dense .ssb{{font-size:{px(22)};}}
.si{{display:flex;align-items:flex-start;gap:{px(24)};padding:{px(14)} {px(22)};border-radius:16px;background:color-mix(in srgb,var(--surface) 88%,transparent);border:1px solid var(--hairline);}}
.si.on{{border-color:var(--accent);}}
.si.done{{opacity:0.62;}}
.sn{{flex:0 0 auto;width:{px(54)};height:{px(54)};border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'FN Mono';font-size:{px(26)};border:2px solid var(--muted);color:var(--muted);}}
.si.on .sn{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.stt{{font-family:'FN Display';font-weight:800;font-size:{px(34)};line-height:1.2;}}
.ssb{{font-size:{px(24)};line-height:1.35;color:var(--muted);margin-top:{px(4)};}}
.cmp-h,.ch-q,.chp-h{{font-family:'FN Display';font-weight:800;font-size:{px(52)};line-height:1.12;letter-spacing:-0.02em;}}
.cmp{{display:flex;flex-direction:{split_dir};gap:{px(30)};}}
.cc{{flex:1 1 0;background:color-mix(in srgb,var(--surface) 90%,transparent);border:1px solid var(--hairline);border-top:6px solid;border-radius:20px;padding:{px(28)} {px(32)};display:flex;flex-direction:column;gap:{px(14)};}}
.cc-h{{font-family:'FN Mono';font-size:{px(24)};letter-spacing:0.1em;text-transform:uppercase;margin-bottom:{px(6)};}}
.cr{{display:flex;align-items:flex-start;gap:{px(16)};font-size:{px(30)};line-height:1.35;}}
.cr i{{flex:0 0 auto;width:{px(14)};height:{px(14)};border-radius:3px;margin-top:{px(13)};}}
.qt{{max-width:{'100%' if col else '1360px'};background:color-mix(in srgb,var(--surface) 92%,transparent);border-left:8px solid var(--accent);border-radius:16px;padding:{px(40)} {px(48)};display:flex;flex-direction:column;gap:{px(22)};}}
.qt-auslegung{{border-left-color:var(--violet);}} .qt-unsicher{{border-left-color:var(--amber);}} .qt-luecke{{border-left-color:var(--red);}} .qt-beispiel{{border-left-color:#8a93a6;}}
.qt-t{{font-size:{px(42)};line-height:1.32;}}
.qt-o{{font-family:'FN Mono';font-size:{px(22)};color:var(--muted);line-height:1.4;}}
.cs{{gap:{px(10)};}}
.cs-k{{display:flex;align-items:center;gap:{px(12)};font-family:'FN Mono';font-size:{px(22)};letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);}}
.cs-c{{font-family:'FN Mono';font-weight:500;font-size:{px(92 if not col else 100)};line-height:1;letter-spacing:-0.02em;white-space:nowrap;}}
.cs-p{{font-size:{px(32)};color:var(--muted);}}
.ob{{position:relative;flex:1 1 auto;background:var(--paper);color:var(--paper-ink);border-radius:20px;padding:{px(30)} {px(38)};box-shadow:0 24px 60px rgba(0,0,0,0.45);}}
.ob-f{{font-family:'FN Mono';font-size:{px(22)};color:#4a5568;}}
.ob-s{{font-family:'FN Display';font-weight:800;font-size:{px(34)};margin:{px(8)} 0 {px(16)};}}
.ob-b{{display:flex;flex-direction:column;gap:{px(8)};}}
.ob-l{{font-size:{px(27)};line-height:1.35;padding:{px(4)} {px(10)};border-radius:6px;border-left:4px solid transparent;}}
.ob-l.hl{{background:rgba(255,209,102,0.30);border-left:4px dashed #b8860b;}}
.ob-flag{{position:absolute;right:{px(24)};top:{px(-22)};background:var(--amber);color:#0a0c10;font-family:'FN Mono';font-size:{px(20)};padding:{px(6)} {px(14)};border-radius:999px;}}
.chs{{display:flex;flex-direction:{split_dir};gap:{px(24)};}}
.co{{flex:1 1 0;display:flex;align-items:center;gap:{px(20)};background:color-mix(in srgb,var(--surface) 92%,transparent);border:1px solid var(--hairline);border-radius:18px;padding:{px(24)} {px(26)};}}
.co-k{{flex:0 0 auto;width:{px(62)};height:{px(62)};border-radius:14px;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'FN Display';font-weight:800;font-size:{px(34)};}}
.co-t{{font-size:{px(30)};line-height:1.3;}}
.ch-bar{{height:{px(10)};border-radius:6px;background:color-mix(in srgb,var(--amber) 22%,transparent);overflow:hidden;}}
.ch-bar i{{display:block;height:100%;background:var(--amber);transform-origin:left center;}}
.tm-k{{font-family:'FN Mono';font-size:{px(22)};letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;gap:{px(16)};}}
.tm-t{{font-family:'FN Display';font-weight:800;font-size:{px(46)};line-height:1.15;margin-top:{px(10)};}}
.tml{{position:relative;display:flex;flex-direction:{'column' if col else 'row'};gap:{px(22 if col else 26)};{'padding-left:' + px(44) if col else 'padding-top:' + px(56)};}}
.tml-line{{position:absolute;{'left:' + px(14) + ';top:' + px(18) + ';bottom:' + px(18) + ';width:3px' if col else 'top:' + px(18) + ';left:0;right:0;height:3px'};background:var(--hairline);}}
.ti{{position:relative;flex:1 1 0;}}
.ti i{{position:absolute;{'left:' + px(-42) + ';top:' + px(8) if col else 'left:0;top:' + px(-50)};width:{px(26)};height:{px(26)};border-radius:50%;border:3px solid;}}
.ti-c{{font-family:'FN Mono';font-size:{px(28)};margin-bottom:{px(6)};}}
.ti-t{{font-size:{px(28)};line-height:1.35;}}
.sp-k{{font-family:'FN Mono';font-size:{px(22)};letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);}}
.sp-card{{display:flex;gap:{px(26)};align-items:flex-start;background:color-mix(in srgb,var(--surface) 94%,transparent);border:2px solid var(--green);border-radius:22px;padding:{px(34)};}}
.sp-l{{flex:0 0 auto;width:{px(78)};height:{px(78)};border-radius:16px;background:var(--green);color:#0a0c10;display:flex;align-items:center;justify-content:center;font-family:'FN Display';font-weight:800;font-size:{px(44)};}}
.sp-t{{font-family:'FN Display';font-weight:800;font-size:{px(44)};line-height:1.15;}}
.sp-s{{font-size:{px(28)};line-height:1.4;color:var(--muted);margin-top:{px(10)};}}
.sks{{flex:1 1 auto;display:flex;flex-direction:column;gap:{px(20)};}}
.sk-t{{position:relative;display:inline-block;font-size:{px(30)};color:var(--muted);}}
.sk-x{{position:absolute;left:0;right:0;top:52%;height:3px;background:var(--red);transform-origin:left center;}}
.sk-n{{font-size:{px(24)};color:var(--muted);margin-top:{px(4)};}}
.br{{background:color-mix(in srgb,var(--bg) 70%,transparent);border-radius:16px;padding:{px(22)} {px(30)};}}
.br-w{{font-family:'FN Display';font-weight:800;font-size:{px(64)};line-height:1.05;}}
.br-s{{font-size:{px(28)};color:var(--muted);margin-top:{px(10)};}}
.cps{{display:grid;grid-template-columns:{'1fr' if col else '1fr 1fr'};gap:{px(16)} {px(40)};}}
.cp{{display:flex;align-items:center;gap:{px(20)};font-size:{px(34)};padding:{px(14)} 0;border-bottom:1px solid var(--hairline);}}
.cp-n{{font-family:'FN Mono';color:var(--accent);font-size:{px(28)};width:{px(46)};}}
.cl-top{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:{px(26)};}}
.cl-r{{font-family:'FN Display';font-weight:800;font-size:{px(56)};line-height:1.15;letter-spacing:-0.02em;}}
.cl-a{{display:flex;flex-direction:column;gap:{px(6)};padding:{px(18)} {px(26)};border-radius:16px;background:color-mix(in srgb,var(--surface) 92%,transparent);border:1px solid var(--hairline);}}
.cl-al{{font-size:{px(30)};}}
.cl-u{{font-family:'FN Mono';font-size:{px(24)};color:var(--accent);}}
.cl-end{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:{'center' if col else 'flex-start'};justify-content:center;gap:{px(18)};opacity:0;}}
.cl-logo{{width:{px(84)};height:{px(84)};}}
.cl-wm{{font-family:'FN Display';font-weight:700;font-size:{px(40)};letter-spacing:0.18em;}}
.cl-claim{{font-size:{px(34)};}}
.cl-disc{{font-family:'FN Mono';font-size:{px(22)};color:var(--muted);}}
.mk{{display:inline-flex;align-items:center;gap:10px;}}
.mk i{{display:inline-block;width:18px;height:18px;}}
.mk b{{font-weight:600;}}
.mk-fakt i{{background:var(--accent);border-radius:3px;}}
.mk-auslegung i{{background:var(--violet);transform:rotate(45deg) scale(0.85);}}
.mk-unsicher i{{background:var(--amber);border-radius:18px 18px 0 0;height:9px;margin-top:9px;}}
.mk-luecke i{{border:2px dashed var(--red);border-radius:50%;}}
.mk-beispiel i{{background:#8a93a6;border-radius:3px;}}
"""
