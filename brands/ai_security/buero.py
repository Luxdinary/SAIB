"""Scutoria test format "Du sitzt am Platz" (November 2026): the case "Was tust du?" in real office pictures.

Concept: OneDrive\\Business\\02 Marke\\Scutoria\\Testvideo-Konzept Reels 2026-11.md. The viewer sits at the desk of a
small business (first person, hands yes, faces never). Photos and clips from Higgsfield (assets/higgsfield/test2611,
licence lines in LICENSE.md there) lie under the scenes; the scenes draw what the photo cannot hold: the mail on the
real monitor, a magnifier on the mail, the frozen decision, stamps, step cards. Loaded by scenes.py of this brand.

Media per beat (beat.data["media"], drawn by LAYER below the scenes):
    {"shots": [{"still": "test2611/B1a.png", "clip": "test2611/C1_typing.mp4", "at": 0, "move": "push",
                "grey_at": "@Wort", "flash": true}, ...],
     "screen": [x, y, w, h],    # the monitor in frame pixels (1080x1920, object-fit cover)
     "dim": 0.5}                # extra darkening for text-heavy beats
A shot runs from its "at" to the next shot (or the beat end). A clip starts on its still (Kling start frame) and is
placed so that it ends with the shot; before that the still stands. Moves: push, pull, pan_l, pan_r, still.
Sound cues (beat.data["cues"] = [{"cue": "mail_in", "at": "@Mail"}]) are resolved to video seconds and written to
project/sound_cues.json for the shared sound layer; nothing is played from here.

| scene type | role                | data (besides media, cues) |
|------------|---------------------|----------------------------|
| sb_screen  | hook: mail arrives  | kicker, time, place, mail{from, addr, time, subject, lines[]}, mail_at, highlight{line, label, at} |
| sb_lens    | what you check      | kicker, headline, mail, rows[{label, value, verdict, field, at}], finding{text, at}, fact{kind, text, source, at} |
| sb_freeze  | the decision        | question, options[{key, text, at}], think{seconds, at}, hint, clock{file, cx, cy, r} |
| sb_montage | consequence in cuts | kicker, tag, items[{time, text, tone, at}], source{kind, label, at} |
| sb_action  | the one step        | mode rule|fallback, kicker, card{letter, title, sub, at}, stamp{text, at}, strikes[], steps[], sources[], sources_at |
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

HERE = Path(__file__).resolve().parent
MEDIA_DIR = HERE / "assets" / "higgsfield"
X0, W = 108, 832                  # title-safe column, right edge x 940 (R5)
CARD_W = 832                      # mail card layout width before scaling onto a screen

LIMITS: dict[str, dict[str, int]] = {
    "sb_screen": {"kicker": 34, "time": 14, "place": 40, "from": 30, "addr": 38, "subject": 28, "line": 36, "label": 14},
    "sb_lens": {"kicker": 34, "headline": 30, "label": 12, "value": 24, "verdict": 14, "finding": 26, "fact": 60, "source": 40},
    "sb_freeze": {"question": 20, "option": 36, "hint": 40},
    "sb_montage": {"kicker": 34, "tag": 14, "time": 12, "text": 34, "source": 40},
    "sb_action": {"kicker": 34, "title": 28, "sub": 40, "stamp": 12, "strike": 30, "note": 22, "step": 34, "source": 40},
}
HOOK_SCENE_TYPES = ["sb_screen"]
SEG_COLORS = {"plain": "#e9eef8", "amber": "#ffd166", "red": "#ff6b6b"}
MARK_WORDS = {
    "de": {"fakt": "Fakt", "auslegung": "Auslegung", "beispiel": "Beispiel", "unsicher": "Unsicher"},
    "en": {"fakt": "Fact", "auslegung": "Interpretation", "beispiel": "Example", "unsicher": "Open"},
}
MOVES = {   # GSAP from/to per move; the overlay of a screen beat gets the same tween as its photo
    "push": ("{scale:1}", "{scale:1.07}"),
    "pull": ("{scale:1.07}", "{scale:1}"),
    "pan_l": ("{scale:1.08,x:34}", "{scale:1.08,x:-34}"),
    "pan_r": ("{scale:1.08,x:-34}", "{scale:1.08,x:34}"),
}


def _e(s) -> str:
    return html.escape(str(s))


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", s.lower())


def _anchor(v, words, beat_start: float, default: float) -> tuple[float, bool]:
    """Beat-relative seconds from a number or "@Wort+0.4" over (text, start) words; (seconds, found)."""
    if isinstance(v, (int, float)):
        return float(v), True
    if isinstance(v, str) and v.startswith("@"):
        m = re.match(r"^@(.+?)((?:[+\-]\d+(?:\.\d+)?)*)$", v)        # "@Wort+0.4", also "@Wort+0.4+0.1"
        if m:
            target = _norm(m.group(1))
            shift = sum(float(x) for x in re.findall(r"[+\-]\d+(?:\.\d+)?", m.group(2)))
            for text, start in words:
                if _norm(text).startswith(target):
                    return max(0.0, start - beat_start + shift), True
        return default, False
    return default, True


def _rel(ctx: SceneCtx, v, default: float, out: SceneOut) -> float:
    words = [(w.text, w.start) for w in (getattr(ctx, "words", None) or [])]
    t, ok = _anchor(v, words, ctx.start, default)
    if not ok:
        out.problems.append(f"word anchor '{v}' not found in the beat; default time used")
    return t


def _hold(ctx: SceneCtx, at: float, hold: float = 1.8) -> float:
    return min(at, max(0.3, ctx.duration - hold))


def _chk(scene: str, key: str, val, where: str, out: SceneOut) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _in(ctx: SceneCtx, sel: str, at: float, *, dy: int = 18, dx: int = 0, dur: float = 0.35) -> str:
    return (f'tl.fromTo("#{ctx.sid} {sel}",{{opacity:0,x:{dx},y:{dy}}},'
            f'{{opacity:1,x:0,y:0,duration:{dur:.2f},ease:"power3.out"}},{ctx.t(at):.3f});')


def _out(ctx: SceneCtx, sel: str, at: float, dur: float = 0.15) -> str:
    return f'tl.to("#{ctx.sid} {sel}",{{opacity:0,duration:{dur:.2f}}},{ctx.t(at):.3f});'


def _frame(ctx: SceneCtx) -> list[str]:
    s = ctx.sid
    return [f'tl.fromTo("#{s} .sb-in",{{opacity:0}},{{opacity:1,duration:{min(ctx.enter, 0.2):.2f},ease:"power2.out"}},{ctx.start:.3f});',
            f'tl.to("#{s} .sb-in",{{opacity:0,duration:0.12,ease:"power2.in"}},{max(ctx.start + 0.3, ctx.end - 0.12):.3f});']


def _mark(kind: str) -> str:
    return f'<i class="sb-mk sb-mk-{_e(kind)}"></i>'


def _src_chip(lang: str, kind: str, label: str) -> str:
    word = MARK_WORDS.get(lang, MARK_WORDS["de"]).get(kind, kind)
    return f'<div class="sb-src">{_mark(kind)}<b>{_e(word)}</b><span>{_e(label)}</span></div>'


def _kicker(text: str, top: int, kind: str = "", tag: str = "") -> str:
    m = _mark(kind) if kind else '<i class="sb-tick"></i>'
    t = f'<span class="sb-tag">{_e(tag)}</span>' if tag else ""
    return f'<div class="sb-kicker" style="top:{top}px">{m}<span>{_e(text)}</span>{t}</div>'


def move_tween(sel: str, move: str, t0: float, dur: float) -> str:
    if move not in MOVES or dur <= 0:
        return ""
    a, b = MOVES[move]
    return f'tl.fromTo("{sel}",{a},{b[:-1]},duration:{dur:.3f},ease:"none"}},{t0:.3f});'


def _origin(media: dict) -> str:
    sc = media.get("screen")
    if sc:
        return f"{sc[0] + sc[2] / 2:.0f}px {sc[1] + sc[3] / 2:.0f}px"
    return "540px 960px"


# --- the mail card (drawn on the real screen) ---------------------------------------------------------

def _mail_html(sid: str, m: dict, hl: dict, *, ids: bool = True) -> str:
    body = []
    for i, ln in enumerate(m.get("lines", [])):
        mark = i == hl.get("line")
        hc_id = f' id="{sid}hc"' if ids else ""
        chip = f'<span class="sb-newchip"{hc_id}>{_e(hl.get("label", ""))}</span>' if mark and hl.get("label") else ""
        lid = f' id="{sid}l{i}"' if ids else ""
        body.append(f'<div class="sb-mail-line{" sb-hl" if mark else ""}"{lid}><span class="sb-hl-bg"></span>'
                    f'<span class="sb-hl-tx">{_e(ln)}</span>{chip}</div>')
    return (f'<div class="sb-mail"><div class="sb-mail-head"><span class="sb-avatar"></span><div class="sb-mail-who">'
            f'<div class="sb-mail-from">{_e(m.get("from", ""))}</div><div class="sb-mail-addr">{_e(m.get("addr", ""))}</div></div>'
            f'<span class="sb-mail-time">{_e(m.get("time", ""))}</span></div><div class="sb-mail-subj">{_e(m.get("subject", ""))}</div>'
            f'<div class="sb-mail-body">{"".join(body)}</div></div>')


def _mail_scale(screen: list, n_lines: int) -> tuple[float, int]:
    """Scale of the 832 px card on the screen rectangle and the card height before scaling."""
    h = 192 + 58 * n_lines + 40
    s = min((screen[2] - 24) / CARD_W, (screen[3] - 24) / h)
    return s, h


FIELD_Y = {"from": 62, "subject": 150}       # card y of a mail field (before scaling); lines: 192 + 58 i + 29


def _field_point(field: str) -> tuple[int, int]:
    if field.startswith("line:"):
        return 300, 192 + 58 * int(field.split(":", 1)[1]) + 29
    return 300, FIELD_Y.get(field, 62)


def _check_mail(scene: str, m: dict, hl: dict, out: SceneOut) -> None:
    for k in ("from", "addr", "subject"):
        _chk(scene, k, m.get(k, ""), f"mail.{k}", out)
    for i, ln in enumerate(m.get("lines", [])):
        _chk(scene, "line", ln, f"mail.lines[{i}]", out)
    _chk(scene, "label", hl.get("label", ""), "highlight.label", out)


# --- sb_screen: the mail arrives on the real monitor (hook) -------------------------------------------

def screen(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    for k in ("kicker", "time", "place"):
        _chk("sb_screen", k, d.get(k, ""), k, out)
    m, hl, media = d.get("mail") or {}, d.get("highlight") or {}, d.get("media") or {}
    _check_mail("sb_screen", m, hl, out)
    sc = media.get("screen") or [176, 500, 708, 384]
    sc_s, card_h = _mail_scale(sc, len(m.get("lines", [])))
    mail_at = min(_rel(ctx, d.get("mail_at", 0.8), 0.8, out), 1.0)   # the case object is on screen within the first second
    out.html = f"""<div class="sb-in">
  <div class="sb-mv" style="transform-origin:{_origin(media)}">
    <div class="sb-screen" style="left:{sc[0]}px;top:{sc[1]}px;width:{sc[2]}px;height:{sc[3]}px">
      <div class="sb-toast" id="{s}toast"><i></i><span>1</span></div>
      <div class="sb-card" id="{s}card" style="transform:scale({sc_s:.4f})">{_mail_html(s, m, hl)}</div>
    </div>
  </div>
  {_kicker(d.get("kicker", ""), zt, "beispiel")}
  <div class="sb-time" style="top:{zt + 46}px">{_e(d.get("time", ""))}</div>
  <div class="sb-place" style="top:{zt + 160}px;width:{max(300, sc[0] + sc[2] - X0)}px">{_e(d.get("place", ""))}</div>
</div>"""
    out.tl += _frame(ctx)
    shots = media.get("shots") or [{}]
    out.tl.append(move_tween(f"#{s} .sb-mv", shots[0].get("move", "still"), ctx.start, ctx.duration))
    out.tl.append(_in(ctx, ".sb-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sb-time", 0.15, dy=24))
    out.tl.append(_in(ctx, ".sb-place", 0.45))
    out.events.append(ctx.t(0.15))
    out.tl.append(f'tl.fromTo("#{s}toast",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2.4)"}},{ctx.t(mail_at):.3f});')
    out.tl.append(f'tl.to("#{s}toast",{{opacity:0,duration:0.2}},{ctx.t(mail_at + 0.6):.3f});')
    out.tl.append(f'tl.fromTo("#{s}card",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{ctx.t(mail_at + 0.5):.3f});')
    out.events += [ctx.t(mail_at), ctx.t(mail_at + 0.5)]
    for i in range(len(m.get("lines", []))):
        out.tl.append(_in(ctx, f"#{s}l{i}", mail_at + 0.8 + 0.15 * i, dy=8, dur=0.25))
    if hl:
        at = _rel(ctx, hl.get("at", mail_at + 2.0), mail_at + 2.0, out)
        out.tl.append(f'tl.fromTo("#{s}l{hl.get("line", 0)} .sb-hl-bg",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{ctx.t(at):.3f});')
        if hl.get("label"):
            out.tl.append(f'tl.fromTo("#{s}hc",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{ctx.t(at + 0.3):.3f});')
        out.events.append(ctx.t(at))
    return out


# --- sb_lens: a magnifier goes over sender, subject, account -----------------------------------------

def lens(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s = ctx.sid
    _chk("sb_lens", "kicker", d.get("kicker", ""), "kicker", out)
    _chk("sb_lens", "headline", d.get("headline", ""), "headline", out)
    m, media = d.get("mail") or {}, d.get("media") or {}
    sc = media.get("screen") or [150, 200, 900, 580]
    sc_s, card_h = _mail_scale(sc, len(m.get("lines", [])))
    sc_s = min(sc_s, float(d.get("card_scale", 0.56)))    # small card on the left, the lens beside it (no text over text)
    cx0, cy0 = sc[0] + 12, sc[1] + 12                     # card origin on the frame
    rows = list(d.get("rows", []))
    below = sc[1] + sc[3] + 18                            # text block under the monitor
    R, MAG = 140, 1.5
    lx = min(cx0 + CARD_W * sc_s + 22 + R, 940 - R)
    lens_html, row_html, spot_html = [], [], []
    for i, r in enumerate(rows):
        for k in ("label", "value", "verdict"):
            _chk("sb_lens", k, r.get(k, ""), f"rows[{i}].{k}", out)
        fx, fy = _field_point(r.get("field", "from"))
        py = min(max(cy0 + sc_s * fy, ctx.zone_top - 30 + R), sc[1] + sc[3] - R)   # below logo and AI label, on the screen
        inner = sc_s * MAG
        spot_html.append(f'<i class="sb-spot" id="{s}p{i}" style="left:6px;top:{12 + sc_s * (fy - 31):.0f}px;width:{CARD_W * sc_s + 12:.0f}px;height:{sc_s * 62:.0f}px"></i>')
        lens_html.append(f'<div class="sb-lens" id="{s}z{i}" style="left:{lx - R:.0f}px;top:{py - R:.0f}px;width:{2 * R}px;height:{2 * R}px">'
                         f'<div class="sb-lens-in" style="left:{R - inner * fx:.1f}px;top:{R - inner * fy:.1f}px;transform:scale({inner:.4f})">'
                         f'{_mail_html(s, m, {}, ids=False)}</div></div>')
        row_html.append(f'<div class="sb-row" id="{s}r{i}" style="top:{24 + i * 92}px"><span class="sb-row-label">{_e(r.get("label", ""))}</span>'
                        f'<span class="sb-row-value">{_e(r.get("value", ""))}</span><span class="sb-verdict" id="{s}v{i}">{_e(r.get("verdict", ""))}</span></div>')
    fin, fact = d.get("finding") or {}, d.get("fact") or {}
    _chk("sb_lens", "finding", fin.get("text", ""), "finding", out)
    _chk("sb_lens", "fact", fact.get("text", ""), "fact.text", out)
    _chk("sb_lens", "source", fact.get("source", ""), "fact.source", out)
    rows_h = 30 + 92 * len(rows)
    fact_html = ""
    if fact:
        word = MARK_WORDS.get(ctx.lang, MARK_WORDS["de"]).get(fact.get("kind", "fakt"), "")
        fact_html = (f'<div class="sb-fact" style="top:{below + 92}px"><div class="sb-fact-head">{_mark(fact.get("kind", "fakt"))}<b>{_e(word)}</b>'
                     f'<span>{_e(fact.get("source", ""))}</span></div><div class="sb-fact-text">{_e(fact.get("text", ""))}</div></div>')
    out.html = f"""<div class="sb-in">
  <div class="sb-screen" style="left:{sc[0]}px;top:{sc[1]}px;width:{sc[2]}px;height:{sc[3]}px">
    <div class="sb-card" data-layout-ignore style="transform:scale({sc_s:.4f})">{_mail_html(s, m, {}, ids=False)}</div>
    {"".join(spot_html)}
    {f'<div class="sb-finding" id="{s}fin" style="top:{12 + card_h * sc_s + 40:.0f}px"><span>{_e(fin.get("text", ""))}</span></div>' if fin else ""}
  </div>
  {"".join(lens_html)}
  {_kicker(d.get("kicker", ""), below)}
  <div class="sb-h2" style="top:{below + 40}px">{_e(d.get("headline", ""))}</div>
  <div class="sb-glass sb-rows" id="{s}rows" style="top:{below + 118}px;height:{rows_h}px">{"".join(row_html)}</div>
  {fact_html}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sb-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sb-h2", 0.15))
    out.tl.append(_in(ctx, ".sb-rows", 0.3, dy=24))
    out.events.append(ctx.t(0.15))
    prev, ats = 0.6, []
    for i, r in enumerate(rows):
        at = _rel(ctx, r.get("at", prev + 1.0), prev + 1.0, out)
        ats.append(at)
        prev = at
    fin_at = _rel(ctx, fin.get("at", prev + 1.2), prev + 1.2, out) if fin else None
    for i, at in enumerate(ats):
        out.tl.append(f'tl.fromTo("#{s}z{i}",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{ctx.t(at - 0.1):.3f});')
        end = ats[i + 1] - 0.15 if i + 1 < len(ats) else at + 2.2
        if fin_at is not None and i + 1 == len(ats):
            end = max(at + 0.8, min(end, fin_at - 0.15))   # the last lens is gone before the finding (EN: "maybe" comes early)
        out.tl.append(_out(ctx, f"#{s}z{i}", end))
        out.tl.append(f'tl.fromTo("#{s}p{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{ctx.t(at - 0.2):.3f});')
        out.tl.append(_out(ctx, f"#{s}p{i}", end))
        out.tl.append(_in(ctx, f"#{s}r{i}", at, dx=-16, dy=0, dur=0.3))
        out.tl.append(f'tl.fromTo("#{s}v{i}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{ctx.t(at + 0.4):.3f});')
        out.events.append(ctx.t(at))
    if fin:
        at = max(fin_at, ats[-1] + 0.95 if ats else 0.0)
        out.tl.append(f'tl.fromTo("#{s}fin",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{ctx.t(at):.3f});')
        out.events.append(ctx.t(at))
    if fact:
        at = _hold(ctx, _rel(ctx, fact.get("at", prev + 2.5), prev + 2.5, out), 2.5)
        out.tl.append(_out(ctx, ".sb-rows", at - 0.2, 0.2))
        out.tl.append(_out(ctx, ".sb-h2", at - 0.2, 0.2))
        out.tl.append(_in(ctx, ".sb-fact", at, dy=24, dur=0.4))
        out.events.append(ctx.t(at))
    return out


# --- sb_freeze: the picture stops, A/B/C, the clock ticks --------------------------------------------

def freeze(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    _chk("sb_freeze", "question", d.get("question", ""), "question", out)
    _chk("sb_freeze", "hint", d.get("hint", ""), "hint", out)
    opts = list(d.get("options", []))
    top0, step = zt + 270, 170                      # hint ends above the captions (y 1250)
    ohtml = []
    for i, o in enumerate(opts):
        _chk("sb_freeze", "option", o.get("text", ""), f"options[{i}].text", out)
        ohtml.append(f'<div class="sb-opt" id="{s}o{i}" style="top:{top0 + i * step}px"><span class="sb-key">{_e(o.get("key", "ABC"[i % 3]))}</span>'
                     f'<span class="sb-opt-tx">{_e(o.get("text", ""))}</span></div>')
    bar_top = top0 + len(opts) * step + 6
    think, clock = d.get("think") or {}, d.get("clock") or {}
    clock_html = ""
    if clock:
        D_ = 250                                   # inset diameter; the clock face of the photo fills it
        k = (D_ / 2) / float(clock.get("r", 420))
        img_l, img_t = D_ / 2 - k * float(clock.get("cx", 540)), D_ / 2 - k * float(clock.get("cy", 960))
        clock_html = (f'<div class="sb-clock" style="left:{940 - D_}px;top:{zt - 6}px;width:{D_}px;height:{D_}px">'
                      f'<img src="assets/buero/{_e(Path(clock.get("file", "")).name)}" alt="" style="left:{img_l:.1f}px;top:{img_t:.1f}px;width:{1080 * k:.1f}px;height:{1920 * k:.1f}px">'
                      f'<i class="sb-sec" id="{s}sec" style="height:{D_ * 0.42:.0f}px"></i><i class="sb-hub"></i></div>')
    out.html = f"""<div class="sb-in">
  <div class="sb-stopline" id="{s}stop"></div>
  <div class="sb-question" style="top:{zt + 20}px">{_e(d.get("question", ""))}</div>
  {clock_html}
  {"".join(ohtml)}
  {f'<div class="sb-bar" style="top:{bar_top}px"><div class="sb-bar-fill" id="{s}bar"></div></div><div class="sb-hint" style="top:{bar_top + 30}px">{_e(d.get("hint", ""))}</div>' if think else ""}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(f'tl.fromTo("#{s}stop",{{opacity:0.9,scaleY:1}},{{opacity:0,scaleY:0.02,duration:0.35,ease:"power2.in"}},{ctx.t(0.02):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sb-question",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{ctx.t(0.1):.3f});')
    out.events.append(ctx.t(0.1))
    prev = 0.4
    for i, o in enumerate(opts):
        at = _rel(ctx, o.get("at", prev + 1.2), prev + 1.2, out)
        prev = at
        out.tl.append(_in(ctx, f"#{s}o{i}", at, dx=48, dy=0, dur=0.3))
        out.tl.append(f'tl.fromTo("#{s}o{i} .sb-key",{{scale:0.6}},{{scale:1,duration:0.3,ease:"back.out(2.2)"}},{ctx.t(at + 0.1):.3f});')
        out.events.append(ctx.t(at))
    if think:
        at = _rel(ctx, think.get("at", prev + 1.0), prev + 1.0, out)
        secs = float(think.get("seconds", 3.0))
        out.tl.append(_in(ctx, ".sb-bar", at, dy=0, dur=0.2))
        out.tl.append(f'tl.fromTo("#{s}bar",{{scaleX:1}},{{scaleX:0,duration:{secs:.2f},ease:"none"}},{ctx.t(at):.3f});')
        out.tl.append(_in(ctx, ".sb-hint", at + 0.1, dy=10))
        out.events.append(ctx.t(at))
        if clock:
            out.tl.append(_in(ctx, ".sb-clock", at - 0.3, dy=0, dur=0.3))
            for k in range(int(secs) + 2):                 # the second hand jumps once a second (ticks in the sound layer)
                out.tl.append(f'tl.set("#{s}sec",{{rotation:{6 * (k + 1)}}},{ctx.t(at + k):.3f});')
    return out


# --- sb_montage: the wrong choice in hard cuts ---------------------------------------------------------

def montage(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    for k in ("kicker", "tag"):
        _chk("sb_montage", k, d.get(k, ""), k, out)
    items, src = list(d.get("items", [])), d.get("source") or {}
    _chk("sb_montage", "source", src.get("label", ""), "source", out)
    n = len(items)
    seg_w = (W - 12 * (n - 1)) / max(1, n)
    segs = "".join(f'<i class="sb-seg" id="{s}g{i}" style="left:{i * (seg_w + 12):.0f}px;width:{seg_w:.0f}px"></i>' for i in range(n))
    ihtml = []
    for i, it in enumerate(items):
        _chk("sb_montage", "time", it.get("time", ""), f"items[{i}].time", out)
        _chk("sb_montage", "text", it.get("text", ""), f"items[{i}].text", out)
        tone = it.get("tone", "plain")
        ihtml.append(f'<div class="sb-stamp sb-tone-{_e(tone)}" id="{s}t{i}" style="top:{zt + 120}px"><span>{_e(it.get("time", ""))}</span></div>'
                     f'<div class="sb-glass sb-mtext sb-tone-{_e(tone)}" id="{s}x{i}" style="top:{zt + 700}px">{_e(it.get("text", ""))}</div>')
    out.html = f"""<div class="sb-in">
  {_kicker(d.get("kicker", ""), zt, "", d.get("tag", ""))}
  <div class="sb-segs" style="top:{zt + 60}px">{segs}</div>
  {"".join(ihtml)}
  {f'<div class="sb-srcrow" style="top:{zt + 860}px">{_src_chip(ctx.lang, src.get("kind", "fakt"), src.get("label", ""))}</div>' if src else ""}
</div>"""
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sb-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(ctx, ".sb-segs", 0.1, dy=0))
    ats, prev = [], 0.0
    for i, it in enumerate(items):
        at = _hold(ctx, _rel(ctx, it.get("at", prev + 2.0), prev + 2.0, out))
        ats.append(at)
        prev = at
    for i, at in enumerate(ats):
        out.tl.append(f'tl.set("#{s}g{i}",{{backgroundColor:"{SEG_COLORS.get(items[i].get("tone", "plain"), SEG_COLORS["plain"])}"}},{ctx.t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}t{i}",{{opacity:0,scale:1.6,rotation:-9}},{{opacity:1,scale:1,rotation:-4,duration:0.22,ease:"power4.in"}},{ctx.t(at + 0.05):.3f});')
        out.tl.append(_in(ctx, f"#{s}x{i}", at + 0.25, dy=14, dur=0.3))
        if i + 1 < len(ats):
            out.tl.append(_out(ctx, f"#{s}t{i}", ats[i + 1] - 0.05, 0.05))
            out.tl.append(_out(ctx, f"#{s}x{i}", ats[i + 1] - 0.05, 0.05))
        out.events.append(ctx.t(at))
    if src:
        at = _hold(ctx, _rel(ctx, src.get("at", ats[-1] + 1.0 if ats else 1.0), 1.0, out))
        out.tl.append(_in(ctx, ".sb-srcrow", at, dy=12))
    return out


# --- sb_action: the one step, stamped on the real action ---------------------------------------------

def action(ctx: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = ctx.sid, ctx.zone_top
    mode = d.get("mode", "rule")
    tone = "amber" if mode == "fallback" else "green"
    _chk("sb_action", "kicker", d.get("kicker", ""), "kicker", out)
    card, stamp = d.get("card") or {}, d.get("stamp") or {}
    _chk("sb_action", "title", card.get("title", ""), "card.title", out)
    _chk("sb_action", "sub", card.get("sub", ""), "card.sub", out)
    _chk("sb_action", "stamp", stamp.get("text", ""), "stamp", out)
    strikes, steps, srcs = list(d.get("strikes", [])), list(d.get("steps", [])), list(d.get("sources", []))
    parts = [_kicker(d.get("kicker", ""), zt),
             f'<div class="sb-glass sb-stepcard sb-tone-{tone}" style="top:{zt + 52}px"><span class="sb-bigkey">{_e(card.get("letter", "C"))}</span>'
             f'<div><div class="sb-step-title">{_e(card.get("title", ""))}</div><div class="sb-step-sub">{_e(card.get("sub", ""))}</div></div></div>']
    if stamp:
        parts.append(f'<div class="sb-stamp sb-bigstamp sb-tone-{tone}" id="{s}st" style="top:{zt + 330}px"><span>{_e(stamp.get("text", ""))}</span></div>')
    y = zt + 560
    for i, st in enumerate(strikes):
        _chk("sb_action", "strike", st.get("text", ""), f"strikes[{i}].text", out)
        _chk("sb_action", "note", st.get("note", ""), f"strikes[{i}].note", out)
        parts.append(f'<div class="sb-glass sb-strike" id="{s}x{i}" style="top:{y}px"><span class="sb-strike-tx">{_e(st.get("text", ""))}'
                     f'<i class="sb-strike-line" id="{s}xl{i}"></i></span><span class="sb-strike-note" id="{s}xn{i}">{_e(st.get("note", ""))}</span></div>')
        y += 122
    for i, st in enumerate(steps):
        _chk("sb_action", "step", st.get("text", ""), f"steps[{i}].text", out)
        parts.append(f'<div class="sb-glass sb-numstep" id="{s}n{i}" style="top:{y}px"><span class="sb-num">{i + 1}</span><span>{_e(st.get("text", ""))}</span></div>')
        y += 112
    if srcs:
        for i, sc in enumerate(srcs):
            _chk("sb_action", "source", sc.get("label", ""), f"sources[{i}]", out)
        chips = "".join(_src_chip(ctx.lang, sc.get("kind", "fakt"), sc.get("label", "")) for sc in srcs)
        parts.append(f'<div class="sb-srcrow sb-srcs" style="top:{y + 6}px">{chips}</div>')
    out.html = '<div class="sb-in">' + "".join(parts) + "</div>"
    out.tl += _frame(ctx)
    out.tl.append(_in(ctx, ".sb-kicker", 0.05, dx=-20, dy=0))
    c_at = _rel(ctx, card.get("at", 0.2), 0.2, out)
    out.tl.append(f'tl.fromTo("#{s} .sb-stepcard",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{ctx.t(c_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .sb-bigkey",{{scale:0.5}},{{scale:1,duration:0.35,ease:"back.out(2.2)"}},{ctx.t(c_at + 0.15):.3f});')
    out.events.append(ctx.t(c_at))
    if stamp:
        at = _hold(ctx, _rel(ctx, stamp.get("at", c_at + 1.2), c_at + 1.2, out))
        out.tl.append(f'tl.fromTo("#{s}st",{{opacity:0,scale:1.8,rotation:-12}},{{opacity:1,scale:1,rotation:-6,duration:0.2,ease:"power4.in"}},{ctx.t(at):.3f});')
        out.events.append(ctx.t(at))
    prev = c_at + 1.0
    for i, st in enumerate(strikes):
        at = _hold(ctx, _rel(ctx, st.get("at", prev + 1.5), prev + 1.5, out))
        prev = at
        out.tl.append(_in(ctx, f"#{s}x{i}", at, dx=-16, dy=0, dur=0.3))
        out.tl.append(f'tl.fromTo("#{s}xl{i}",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out"}},{ctx.t(at + 0.35):.3f});')
        out.tl.append(f'tl.fromTo("#{s}xn{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{ctx.t(at + 0.6):.3f});')
        out.events.append(ctx.t(at))
    for i, st in enumerate(steps):
        at = _hold(ctx, _rel(ctx, st.get("at", prev + 1.5), prev + 1.5, out))
        prev = at
        out.tl.append(_in(ctx, f"#{s}n{i}", at, dx=-16, dy=0, dur=0.3))
        out.events.append(ctx.t(at))
    if srcs:
        at = _hold(ctx, _rel(ctx, d.get("sources_at", 1.0), 1.0, out))
        out.tl.append(_in(ctx, ".sb-srcs", at, dy=12))
        out.events.append(ctx.t(at))
    return out


TEMPLATES = {"sb_screen": screen, "sb_lens": lens, "sb_freeze": freeze, "sb_montage": montage, "sb_action": action}


# --- LAYER: photos and clips under the scenes, sound cues -------------------------------------------

def _clip_seconds(p: Path) -> float:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                           capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip())
    except (OSError, ValueError, subprocess.SubprocessError):
        return 0.0


def _files(obj) -> list[str]:
    """Every media file named in beat data (keys still, clip, file)."""
    found: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("still", "clip", "file") and isinstance(v, str):
                found.append(v)
            else:
                found += _files(v)
    elif isinstance(obj, list):
        for v in obj:
            found += _files(v)
    return found


def _licence_lines(plan) -> list[dict]:
    """Licence line of every used media file from assets/higgsfield/LICENSE.md (empty text = missing proof)."""
    lic: dict[str, str] = {}
    f = MEDIA_DIR / "LICENSE.md"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                name, text = line.split(":", 1)
                lic[name.strip()] = text.strip()
    names = sorted({n for b in plan.beats if isinstance(b.data, dict) for n in _files(b.data)})
    return [{"asset": n, "license": lic.get(n, ""), "proof": str(f)} for n in names]


def LAYER(plan, brand, project_dir, captions):  # noqa: N802 (contract name)
    beats = [b for b in plan.beats if b.start is not None and isinstance(b.data, dict)]
    if not any(b.data.get("media") for b in beats):
        return {}
    problems: list[str] = []
    words = [(w.text, w.start) for g in captions for w in g.words]
    total = max(b.start + b.duration for b in beats)
    dst = Path(project_dir) / "assets" / "buero"
    dst.mkdir(parents=True, exist_ok=True)
    seconds: dict[str, float] = {}
    for name in sorted({f for b in beats for f in _files(b.data)}):
        p = MEDIA_DIR / name
        if not p.exists():
            problems.append(f"media missing: {p}")
            continue
        if not (dst / p.name).exists():
            shutil.copy2(p, dst / p.name)
        if p.suffix == ".mp4":
            seconds[name] = _clip_seconds(p)
    problems += [f"media without licence line in {r['proof']}: {r['asset']}" for r in _licence_lines(plan) if not r["license"]]
    html_parts, js, cues = [], [], []
    for bi, b in enumerate(beats):
        bw = [w for w in words if b.start <= w[1] < b.start + b.duration]
        media = b.data.get("media") or {}
        shots = list(media.get("shots") or [])
        origin = _origin(media)
        starts = []
        for k, sh in enumerate(shots):
            t, ok = _anchor(sh.get("at", 0), bw, b.start, 0.0)
            if not ok:
                problems.append(f"{b.id} shot {k}: anchor {sh.get('at')} not found")
            starts.append(b.start + t)
        for k, sh in enumerate(shots):
            t0 = starts[k]
            t1 = starts[k + 1] if k + 1 < len(shots) else b.start + b.duration
            dur = max(0.1, t1 - t0)
            sid = f"sbm{bi}_{k}"
            still = Path(sh.get("still", "")).name
            html_parts.append(f'<div id="{sid}" class="clip sbm" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="0">'
                              f'<img class="sbm-img" id="{sid}i" src="assets/buero/{_e(still)}" alt="" style="transform-origin:{origin}"></div>')
            targets = [f"#{sid}i"]
            if sh.get("clip") and sh["clip"] in seconds:
                c = seconds[sh["clip"]] - 0.08
                v0, vd = (t0, dur) if dur <= c else (t1 - c, c)
                html_parts.append(f'<video id="{sid}v" class="clip sbv" src="assets/buero/{_e(Path(sh["clip"]).name)}" data-start="{v0:.3f}" '
                                  f'data-duration="{vd:.3f}" data-track-index="0" data-volume="0" muted playsinline style="transform-origin:{origin}"></video>')
                targets.append(f"#{sid}v")
            for tg in targets:
                tw = move_tween(tg, sh.get("move", "still"), t0, dur)
                if tw:
                    js.append(tw)
                if sh.get("grey_at") is not None:
                    g, ok = _anchor(sh["grey_at"], bw, b.start, 0.2)
                    js.append(f'tl.fromTo("{tg}",{{filter:"grayscale(0) brightness(1)"}},{{filter:"grayscale(0.92) brightness(0.55)",duration:0.3,ease:"power2.out"}},{b.start + g:.3f});')
            if sh.get("flash"):
                html_parts.append(f'<div id="{sid}f" class="clip sbflash" data-start="{t0:.3f}" data-duration="{min(0.6, dur):.3f}" data-track-index="0"></div>')
                js.append(f'tl.fromTo("#{sid}f",{{opacity:0.92}},{{opacity:0,duration:0.45,ease:"power2.out"}},{t0:.3f});')
        if media.get("dim"):
            html_parts.append(f'<div id="sbd{bi}" class="clip sbdim" data-start="{b.start:.3f}" data-duration="{b.duration:.3f}" data-track-index="0" '
                              f'style="opacity:{float(media["dim"]):.2f}"></div>')
        for c in b.data.get("cues") or []:
            t, ok = _anchor(c.get("at", 0), bw, b.start, 0.0)
            if not ok:
                problems.append(f"{b.id} cue {c.get('cue')}: anchor {c.get('at')} not found")
            cues.append({"t": round(b.start + t, 3), "cue": c.get("cue", ""), "beat": b.id, "anchor": c.get("at", 0)})
    html_parts.append(f'<div id="sbshade" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0"></div>')
    (Path(project_dir) / "sound_cues.json").write_text(json.dumps(sorted(cues, key=lambda c: c["t"]), indent=1, ensure_ascii=False), encoding="utf-8")
    head = """<style>
.sbm{z-index:1;overflow:hidden;}
.sbm-img,.sbv{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;}
.sbv{z-index:2;}
.sbflash{z-index:3;background:#fff;}
.sbdim{z-index:3;background:#0b1120;}
#sbshade{z-index:3;pointer-events:none;background:linear-gradient(180deg,rgba(11,17,32,0.82) 0px,rgba(11,17,32,0.55) 260px,rgba(11,17,32,0) 470px,
  rgba(11,17,32,0) 1020px,rgba(11,17,32,0.55) 1180px,rgba(11,17,32,0.88) 1420px,rgba(11,17,32,0.92) 1920px);}
</style>"""
    body_end = ("<script>\n(function(){var tl=window.__timelines&&window.__timelines.main;if(!tl)return;\n"
                + "\n".join(js) + "\ntl.seek(0);})();\n</script>")
    return {"head_html": head, "under_scenes_html": "\n".join(html_parts), "body_end_html": body_end,
            "events": [], "problems": problems}


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):  # noqa: N802 (contract name)
    acc, txt, mut = pal.get("accent", "#4f8cff"), pal.get("text", "#e9eef8"), pal.get("muted", "#a1adc4")
    raised = pal.get("surface_raised", "#19243b")
    hair = pal.get("hairline", "rgba(226,232,246,0.12)")
    amber, red, green = pal.get("signal_amber", "#ffd166"), pal.get("signal_red", "#ff6b6b"), pal.get("signal_green", "#2ec4b6")
    paper, ink = pal.get("paper", "#fbfbfd"), pal.get("paper_ink", "#141a24")
    violet = pal.get("marker_interpretation", "#b07cff")
    on_sig = pal.get("on_signal", "#0a0c10")
    D, B, M = f"'FN {display}'", f"'FN {body}'", f"'FN {mono}'"
    glass = "background:rgba(11,17,32,0.78);border:2px solid rgba(226,232,246,0.16);border-radius:20px;box-shadow:0 18px 40px rgba(0,0,0,0.4);"
    return f"""
.sb-in{{position:absolute;inset:0;}}
.sb-mv{{position:absolute;inset:0;}}
.sb-kicker{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:center;gap:14px;font-family:{M};font-size:28px;letter-spacing:0.12em;text-transform:uppercase;color:{txt};text-shadow:0 2px 8px rgba(0,0,0,0.6);}}
.sb-tick{{display:inline-block;width:28px;height:3px;background:{acc};}}
.sb-tag{{margin-left:auto;font-family:{M};font-size:28px;letter-spacing:0.1em;color:{txt};border:2px solid rgba(226,232,246,0.4);border-radius:999px;padding:4px 16px;background:rgba(11,17,32,0.6);}}
.sb-mk{{display:inline-block;width:20px;height:20px;flex:none;background:{acc};}}
.sb-mk-auslegung{{background:{violet};}}
.sb-mk-beispiel{{background:#8a93a6;}}
.sb-mk-unsicher{{background:linear-gradient(90deg,{amber} 50%,transparent 50%);border:2px solid {amber};border-radius:50%;}}
.sb-time{{position:absolute;left:{X0}px;font-family:{M};font-weight:500;font-size:96px;line-height:1.1;color:{txt};text-shadow:0 4px 18px rgba(0,0,0,0.6);}}
.sb-place{{position:absolute;left:{X0}px;font-family:{B};font-size:38px;color:{txt};text-shadow:0 2px 10px rgba(0,0,0,0.7);}}
.sb-screen{{position:absolute;overflow:hidden;}}
.sb-card{{position:absolute;left:12px;top:12px;width:{CARD_W}px;transform-origin:0 0;}}
.sb-mail{{background:{paper};color:{ink};border-radius:14px;padding:26px 36px 30px;box-sizing:border-box;box-shadow:0 6px 18px rgba(0,0,0,0.18);}}
.sb-mail-head{{display:flex;align-items:center;gap:20px;}}
.sb-avatar{{width:64px;height:64px;border-radius:50%;background:#d8dde8;flex:none;}}
.sb-mail-who{{flex:1;min-width:0;}}
.sb-mail-from{{font-family:{D};font-weight:700;font-size:36px;line-height:1.2;}}
.sb-mail-addr{{font-family:{M};font-size:35px;color:#5b6475;line-height:1.3;}}
.sb-mail-time{{font-family:{M};font-size:35px;color:#5b6475;}}
.sb-mail-subj{{margin-top:20px;font-family:{D};font-weight:800;font-size:46px;line-height:1.2;}}
.sb-mail-body{{margin-top:12px;}}
.sb-mail-line{{position:relative;font-family:{B};font-size:38px;line-height:58px;height:58px;display:flex;align-items:center;gap:14px;white-space:nowrap;}}
.sb-hl-bg{{position:absolute;left:-10px;right:-10px;top:4px;bottom:4px;background:rgba(255,209,102,0.6);transform-origin:left center;transform:scaleX(0);border-radius:6px;}}
.sb-lens .sb-hl-bg{{display:none;}}
.sb-hl-tx{{position:relative;}}
.sb-newchip{{position:relative;font-family:{M};font-size:33px;letter-spacing:0.08em;text-transform:uppercase;background:{ink};color:{amber};border-radius:999px;padding:2px 14px;}}
.sb-toast{{position:absolute;right:22px;top:18px;display:flex;align-items:center;gap:8px;background:{acc};color:#fff;border-radius:999px;padding:8px 18px;font-family:{M};font-size:28px;z-index:2;}}
.sb-toast i{{width:26px;height:18px;border:3px solid #fff;border-radius:3px;display:inline-block;}}
.sb-lens{{position:absolute;border-radius:50%;overflow:hidden;border:6px solid {acc};background:{paper};box-shadow:0 18px 50px rgba(0,0,0,0.55),0 0 0 3px rgba(255,255,255,0.5);}}
.sb-lens-in{{position:absolute;width:{CARD_W}px;transform-origin:0 0;}}
.sb-finding{{position:absolute;left:0;right:0;display:flex;justify-content:center;}}
.sb-spot{{position:absolute;border:4px solid {acc};border-radius:10px;background:rgba(79,140,255,0.12);}}
.sb-finding span{{font-family:{D};font-weight:800;font-size:56px;color:{txt};background:rgba(11,17,32,0.85);border-radius:16px;padding:16px 30px;}}
.sb-h2{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:{display_w};font-size:58px;line-height:1.12;color:{txt};text-shadow:0 3px 12px rgba(0,0,0,0.6);}}
.sb-glass{{position:absolute;left:{X0}px;width:{W}px;box-sizing:border-box;{glass}}}
.sb-row{{position:absolute;left:24px;right:24px;height:88px;display:flex;align-items:center;gap:16px;border-bottom:2px solid {hair};}}
.sb-row:last-of-type{{border-bottom:none;}}
.sb-row-label{{width:200px;flex:none;font-family:{M};font-size:28px;letter-spacing:0.08em;text-transform:uppercase;color:{mut};}}
.sb-row-value{{flex:1;font-family:{B};font-size:36px;line-height:1.15;color:{txt};}}
.sb-verdict{{font-family:{M};font-size:28px;color:{txt};border:2px solid {hair};border-radius:999px;padding:4px 14px;}}
.sb-fact{{position:absolute;left:{X0}px;width:{W}px;box-sizing:border-box;{glass}padding:22px 30px;border-left:6px solid {acc};}}
.sb-fact-head{{display:flex;align-items:center;gap:12px;font-family:{M};font-size:28px;color:{mut};}}
.sb-fact-head b{{color:{txt};font-weight:500;}}
.sb-fact-text{{margin-top:10px;font-family:{B};font-size:38px;line-height:1.3;color:{txt};}}
.sb-stopline{{position:absolute;left:0;right:0;top:0;bottom:0;background:linear-gradient(180deg,transparent 46%,rgba(255,255,255,0.85) 50%,transparent 54%);transform-origin:center;}}
.sb-question{{position:absolute;left:{X0}px;width:{W - 270}px;font-family:{D};font-weight:800;font-size:92px;line-height:1.05;color:{txt};text-shadow:0 4px 18px rgba(0,0,0,0.7);}}
.sb-clock{{position:absolute;border-radius:50%;overflow:hidden;border:5px solid rgba(255,255,255,0.85);box-shadow:0 14px 40px rgba(0,0,0,0.55);}}
.sb-clock img{{position:absolute;max-width:none;}}
.sb-sec{{position:absolute;left:50%;bottom:50%;width:4px;margin-left:-2px;background:{red};transform-origin:50% 100%;}}
.sb-hub{{position:absolute;left:50%;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:{red};}}
.sb-opt{{position:absolute;left:{X0}px;width:{W}px;height:162px;display:flex;align-items:center;gap:30px;{glass}padding:0 32px;box-sizing:border-box;}}
.sb-key{{width:84px;height:84px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:14px;background:{acc};color:#fff;font-family:{D};font-weight:800;font-size:52px;}}
.sb-opt-tx{{font-family:{B};font-size:44px;line-height:1.2;color:{txt};}}
.sb-bar{{position:absolute;left:{X0}px;width:{W}px;height:10px;background:rgba(226,232,246,0.25);border-radius:5px;overflow:hidden;}}
.sb-bar-fill{{width:100%;height:100%;background:{amber};transform-origin:left center;}}
.sb-hint{{position:absolute;left:{X0}px;width:{W}px;font-family:{M};font-size:30px;letter-spacing:0.06em;color:{amber};text-shadow:0 2px 8px rgba(0,0,0,0.7);}}
.sb-segs{{position:absolute;left:{X0}px;width:{W}px;height:10px;}}
.sb-seg{{position:absolute;top:0;height:10px;border-radius:5px;background:rgba(226,232,246,0.3);}}
.sb-stamp{{position:absolute;left:{X0}px;display:inline-flex;}}
.sb-stamp span{{font-family:{M};font-weight:500;font-size:84px;letter-spacing:0.04em;color:{txt};border:6px solid {txt};border-radius:14px;padding:6px 26px;background:rgba(11,17,32,0.55);}}
.sb-stamp.sb-tone-amber span{{color:{amber};border-color:{amber};}}
.sb-stamp.sb-tone-red span{{color:{red};border-color:{red};}}
.sb-mtext{{padding:24px 32px;font-family:{B};font-size:46px;line-height:1.2;color:{txt};}}
.sb-mtext.sb-tone-red{{border-color:{red};font-weight:700;}}
.sb-srcrow{{position:absolute;left:{X0}px;width:{W}px;display:flex;flex-direction:column;gap:10px;}}
.sb-src{{display:flex;align-items:center;gap:14px;font-family:{M};font-size:28px;line-height:40px;color:{txt};text-shadow:0 2px 8px rgba(0,0,0,0.8);}}
.sb-src b{{font-weight:500;}}
.sb-stepcard{{height:240px;display:flex;align-items:center;gap:34px;padding:0 36px;background:rgba(25,36,59,0.9);}}
.sb-stepcard.sb-tone-green{{border-color:{green};}} .sb-stepcard.sb-tone-amber{{border-color:{amber};}}
.sb-bigkey{{width:140px;height:140px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:20px;font-family:{D};font-weight:800;font-size:92px;color:{on_sig};}}
.sb-tone-green .sb-bigkey{{background:{green};}} .sb-tone-amber .sb-bigkey{{background:{amber};}}
.sb-step-title{{font-family:{D};font-weight:800;font-size:56px;line-height:1.1;color:{txt};}}
.sb-step-sub{{margin-top:10px;font-family:{B};font-size:36px;line-height:1.25;color:{mut};}}
.sb-bigstamp{{left:auto;right:140px;}}
.sb-bigstamp span{{font-size:96px;font-weight:700;border-width:8px;background:rgba(11,17,32,0.4);}}
.sb-bigstamp.sb-tone-green span{{color:{green};border-color:{green};}}
.sb-strike{{height:104px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 28px;}}
.sb-strike-tx{{position:relative;font-family:{B};font-size:40px;color:{mut};}}
.sb-strike-line{{position:absolute;left:-6px;right:-6px;top:52%;height:4px;background:{red};transform-origin:left center;transform:scaleX(0);}}
.sb-strike-note{{font-family:{M};font-size:28px;color:{red};white-space:nowrap;}}
.sb-numstep{{height:96px;display:flex;align-items:center;gap:26px;padding:0 26px;font-family:{B};font-size:42px;line-height:1.15;color:{txt};}}
.sb-num{{width:64px;height:64px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:12px;border:3px solid {amber};color:{amber};font-family:{D};font-weight:800;font-size:34px;}}
"""
