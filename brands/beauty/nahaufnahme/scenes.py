"""Dewlane format "Nahaufnahme" (02.11.2026): scene types nh_* (brand module part, loaded from brands/beauty/scenes.py).

Format bible: OneDrive\\Business\\02 Marke\\Dewlane\\Format-Bibel.md. Every video puts one neutral, invented product
type (no brand, no real formula) on an animated studio stage and looks at it up close: what the number or word on the
pack means, the amount and texture, what a source says about the effect, how it is applied in everyday life, and one
sentence to keep. Skin appears only as a neutral illustration (cross-section strip, pictogram, flat forearm), never as
a photo-like face or as proof. Nothing may look like a product test or a before/after result: effect diagrams carry
the tag "Schema nach Quelle, keine Messung". A format-wide LAYER draws the ivory studio and the stamp
"Animation · neutrales Produkt · kein Produkttest" for the whole video. Only HTML/SVG/CSS, moved by the GSAP timeline.

| scene type | role                          | data |
|------------|-------------------------------|------|
| nh_stage   | hook: product on the stage,   | kicker, product{line1, line2, big}, count{to, unit, at, step}, sub{text, at}, ring_at, |
|            | spoons fill, counter          | lens_at, chip{kind, label, at} |
| nh_lens    | the number under the lens     | kicker, headline, product{...}, zoom{text, at}, section{at, label, film_label}, value{text, sub, at}, check{text, at}, chip{...} |
| nh_amount  | the amount on a whole body    | kicker, headline, fill_at, fill_end, total{text, at}, spoons{text, n, at}, card{title, text, at}, finding{text, at}, chip{...} |
| nh_effect  | what the source says (schema) | kicker, headline, rows[{title, amount, protect, label}], cut_at, same_at, drop_at, same_label, schema, chip{...} |
| nh_apply   | everyday application          | kicker, headline, arm_label, draw_at, spread_at, steps[{icon, title, sub, at}], chip{...} |
| nh_close   | rule, question, sign-off      | kicker, rule, rule_at, question{text, at}, sign_at, claim, disclaimer |

Times: seconds from the beat start or "@Wort+0.3" / "@Wort#2" (start of that spoken word in the beat, SceneCtx.words).
An anchor that is not spoken is reported as a problem and the default time is used. Animated elements carry no CSS
transform (GSAP would fold it); they are placed with left/top.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

X0 = 108                     # title-safe left edge
R = 930                      # right edge: x 930 and beyond stays free for platform icons
W = R - X0                   # 822

LIMITS: dict[str, dict[str, int]] = {
    "nh_stage": {"kicker": 34, "big": 18, "unit": 16, "sub": 30, "chip": 44},
    "nh_lens": {"kicker": 34, "headline": 26, "zoom": 8, "value": 14, "sub": 30, "check": 30, "label": 22, "chip": 44},
    "nh_amount": {"kicker": 34, "headline": 26, "total": 8, "spoons": 20, "title": 28, "text": 72, "finding": 64, "chip": 44},
    "nh_effect": {"kicker": 34, "headline": 26, "title": 24, "label": 30, "schema": 44, "chip": 44},
    "nh_apply": {"kicker": 34, "headline": 26, "arm_label": 16, "title": 30, "sub": 34, "chip": 44},
    "nh_close": {"kicker": 34, "rule": 40, "question": 42, "claim": 30, "disclaimer": 34},
}
HOOK_SCENE_TYPES = ["nh_stage"]

MARK_WORDS = {
    "de": {"fakt": "Fakt", "schema": "Schema", "unsicher": "Unsicher", "beispiel": "Beispiel"},
    "en": {"fakt": "Fact", "schema": "Diagram", "unsicher": "Open", "beispiel": "Example"},
}
STAMP = {"de": "Animation · neutrales Produkt · kein Produkttest", "en": "Animation · neutral product · not a product test"}


def _e(s) -> str:
    return html.escape(str(s))


def _chk(scene: str, key: str, val, where: str, out: SceneOut) -> None:
    lim = LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _norm(s: str) -> str:
    return re.sub(r"[^\wäöüß]", "", str(s).lower())


def _rel(c: SceneCtx, v, default: float, out: SceneOut) -> float:
    """Beat-relative seconds from a number or an "@Wort[#n][+0.4]" string."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and v.startswith("@"):
        m = re.match(r"^@(.+?)(?:#(\d+))?([+\-]\d+(?:\.\d+)?)?$", v)
        if m:
            stem, nth = _norm(m.group(1)), int(m.group(2) or 1)
            hits = [w for w in (c.words or []) if _norm(w.text).startswith(stem)]
            if len(hits) >= nth:
                return max(0.0, hits[nth - 1].start - c.start + float(m.group(3) or 0))
        out.problems.append(f"word anchor '{v}' not found in the beat; default time used")
    return default


def _in(c: SceneCtx, sel: str, at: float, *, dy: int = 18, dx: int = 0, dur: float = 0.4, ease: str = "power3.out") -> str:
    return (f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,x:{dx},y:{dy}}},'
            f'{{opacity:1,x:0,y:0,duration:{dur:.2f},ease:"{ease}"}},{c.t(at):.3f});')


def _pop(c: SceneCtx, sel: str, at: float, *, frm: float = 0.6, dur: float = 0.38) -> str:
    return (f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,scale:{frm}}},'
            f'{{opacity:1,scale:1,duration:{dur:.2f},ease:"back.out(1.8)"}},{c.t(at):.3f});')


def _frame(c: SceneCtx) -> list[str]:
    s = c.sid
    return [f'tl.fromTo("#{s} .nh-in",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power2.out"}},{c.start:.3f});',
            f'tl.to("#{s} .nh-in",{{opacity:0,duration:0.22,ease:"power2.in"}},{max(c.start + c.enter + 0.05, c.end - 0.22):.3f});']


def _mark(kind: str) -> str:
    return f'<i class="nh-mk nh-mk-{_e(kind)}"></i>'


def _chip(c: SceneCtx, ch: dict, top: int, out: SceneOut, scene: str, cls: str = "nh-chipline") -> str:
    if not ch:
        return ""
    _chk(scene, "chip", ch.get("label", ""), "chip.label", out)
    kind = ch.get("kind", "fakt")
    word = MARK_WORDS.get(c.lang, MARK_WORDS["de"]).get(kind, kind)
    return (f'<div class="{cls}" style="top:{top}px"><span class="nh-chip">{_mark(kind)}<b>{_e(word)}</b>'
            f'<span>{_e(ch.get("label", ""))}</span></span></div>')


def _kicker(text: str, top: int) -> str:
    return f'<div class="nh-kicker" style="top:{top}px"><i class="nh-dot"></i><span>{_e(text)}</span></div>'


# --- drawn objects (SVG, neutral, no brand) ---------------------------------------------------------------

def tube_svg(ident: str, p: dict, h: int = 520) -> str:
    """Standing tube on its cap: crimped end on top, neutral label band (category, word, big number)."""
    w = round(h * 260 / 620)
    l1, l2, big = _e(p.get("line1", "")), _e(p.get("line2", "")), _e(p.get("big", ""))
    ridges = "".join(f'<line x1="{x}" y1="12" x2="{x}" y2="44" stroke="#D9CCC6" stroke-width="2"/>' for x in range(22, 244, 12))
    return f"""<svg class="nh-tube" id="{ident}" viewBox="0 0 260 620" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
<defs>
 <linearGradient id="{ident}g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#E6D9D3"/><stop offset="0.28" stop-color="#FFFFFF"/>
  <stop offset="0.62" stop-color="#FBF6F2"/><stop offset="1" stop-color="#DCCBC4"/></linearGradient>
 <linearGradient id="{ident}c" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#C9B7B1"/><stop offset="0.35" stop-color="#EFE6E2"/>
  <stop offset="1" stop-color="#BFAEA8"/></linearGradient>
 <linearGradient id="{ident}l" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#F6E6DF"/><stop offset="1" stop-color="#EFD9D0"/></linearGradient>
</defs>
<ellipse cx="130" cy="612" rx="96" ry="8" fill="rgba(74,47,52,0.16)"/>
<rect x="8" y="6" width="244" height="44" rx="6" fill="url(#{ident}g)" stroke="#E2D5CF" stroke-width="2"/>{ridges}
<path d="M14 48 H246 C244 220 236 400 212 492 Q200 536 170 540 H90 Q60 536 48 492 C24 400 16 220 14 48 Z" fill="url(#{ident}g)" stroke="#E2D5CF" stroke-width="2"/>
<rect x="78" y="534" width="104" height="78" rx="14" fill="url(#{ident}c)"/>
<rect x="40" y="168" width="180" height="246" rx="14" fill="url(#{ident}l)"/>
{'<rect x="80" y="192" width="100" height="10" rx="5" fill="#CDB6B0"/>' if l1 else ""}
<text x="130" y="268" text-anchor="middle" font-family="'FN Inter'" font-weight="600" font-size="62" fill="#9B5560">{l2}</text>
<text x="130" y="384" text-anchor="middle" font-family="'FN Playfair Display'" font-weight="600" font-size="104" fill="#9B5560">{big}</text>
<path d="M30 70 C34 200 40 360 58 470" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round"/>
</svg>"""


def spoon_svg(ident: str, w: int = 210) -> str:
    h = round(w * 90 / 220)
    return f"""<svg class="nh-spoon" viewBox="0 0 220 90" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="{ident}s" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#EEE8E5"/><stop offset="1" stop-color="#CBC0BB"/></linearGradient></defs>
<path d="M110 40 Q160 34 210 36 Q218 40 210 46 Q160 50 110 50 Z" fill="url(#{ident}s)"/>
<ellipse cx="60" cy="45" rx="56" ry="36" fill="url(#{ident}s)"/>
<ellipse cx="60" cy="43" rx="46" ry="27" fill="#F6F2F0"/>
<g class="nh-dollop" id="{ident}d"><path d="M22 50 C20 34 40 22 60 22 C82 20 100 34 98 50 C90 60 30 60 22 50 Z" fill="#FFFFFF" stroke="#E9DCD6" stroke-width="2"/>
<path d="M40 34 C50 28 64 27 74 30" stroke="#F1E6E1" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M58 22 C60 14 66 12 70 16" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linecap="round"/></g>
</svg>"""


ICONS = {
    "sun": '<circle cx="32" cy="32" r="12" fill="none" stroke="currentColor" stroke-width="5"/>'
           + "".join(f'<line x1="32" y1="6" x2="32" y2="13" stroke="currentColor" stroke-width="5" stroke-linecap="round" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 45)),
    "repeat": '<path d="M14 26 A18 18 0 0 1 48 20" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M50 38 A18 18 0 0 1 16 44" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M42 12 L50 21 L40 26" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M22 52 L14 43 L24 38" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    "wave": '<path d="M6 26 Q15 18 24 26 T42 26 T60 26" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M6 42 Q15 34 24 42 T42 42 T60 42" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>',
    "glass": '<path d="M16 10 H48 L44 56 H20 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>',
}


def _icon(name: str) -> str:
    return f'<svg class="nh-ico" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">{ICONS.get(name, "")}</svg>'


# --- nh_stage: hook, the product on the stage ------------------------------------------------------------

def nh_stage(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    _chk("nh_stage", "kicker", d.get("kicker", ""), "kicker", out)
    cnt = d.get("count") or {}
    n_to = int(cnt.get("to", 6))
    _chk("nh_stage", "unit", cnt.get("unit", ""), "count.unit", out)
    sub = d.get("sub") or {}
    _chk("nh_stage", "sub", sub.get("text", ""), "sub", out)
    count_at = _rel(c, cnt.get("at", 0.4), 0.4, out)
    step = float(cnt.get("step", 0.42))
    digits = "".join(f'<span class="nh-digit" id="{s}n{i}">{i}</span>' for i in range(1, n_to + 1))
    spoons = []
    for i in range(n_to):
        col, row = i % 2, i // 2
        spoons.append(f'<div class="nh-spoonbox" id="{s}sp{i}" style="left:{450 + col * 236}px;top:{zt + 300 + row * 150}px">{spoon_svg(f"{s}s{i}")}</div>')
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-count" style="top:{zt + 40}px"><span class="nh-digits">{digits}</span><span class="nh-unit">{_e(cnt.get("unit", ""))}</span></div>
  <div class="nh-sub" style="top:{zt + 200}px">{_e(sub.get("text", ""))}</div>
  <div class="nh-stagebox" id="{s}tb" style="left:{X0 + 20}px;top:{zt + 270}px">{tube_svg(f"{s}t", d.get("product") or {}, 440)}
    <div class="nh-ring" id="{s}ring"></div><div class="nh-lensmini" id="{s}lm"></div></div>
  {"".join(spoons)}
  {_chip(c, d.get("chip") or {}, zt + 780, out, "nh_stage")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(f'tl.fromTo("#{s}tb",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},{c.t(0.1):.3f});')
    out.tl.append(f'tl.to("#{s}tb",{{y:-12,duration:{max(0.6, c.duration - 0.9):.2f},ease:"sine.inOut"}},{c.t(0.7):.3f});')
    out.events.append(c.t(0.1))
    for i in range(n_to):
        out.tl.append(_in(c, f"#{s}sp{i}", 0.25 + 0.06 * i, dy=26, dur=0.35))
    out.tl.append(_in(c, ".nh-unit", count_at, dx=-16, dy=0))
    for i in range(n_to):
        at = count_at + step * i
        out.tl.append(f'tl.fromTo("#{s}s{i}d",{{opacity:0,scale:0.2,transformOrigin:"50% 80%"}},'
                      f'{{opacity:1,scale:1,duration:0.32,ease:"back.out(2.2)"}},{c.t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}n{i + 1}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.22,ease:"power2.out"}},{c.t(at):.3f});')
        if i < n_to - 1:
            out.tl.append(f'tl.to("#{s}n{i + 1}",{{opacity:0,y:-30,duration:0.2,ease:"power2.in"}},{c.t(at + step - 0.05):.3f});')
        out.events.append(c.t(at))
    if sub:
        at = _rel(c, sub.get("at", count_at + step * n_to), count_at + step * n_to, out)
        out.tl.append(_in(c, ".nh-sub", at))
        out.events.append(c.t(at))
    if d.get("ring_at") is not None:
        at = _rel(c, d["ring_at"], c.duration * 0.6, out)
        out.tl.append(f'tl.fromTo("#{s}ring",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if d.get("lens_at") is not None:
        at = _rel(c, d["lens_at"], c.duration * 0.8, out)
        out.tl.append(f'tl.fromTo("#{s}lm",{{opacity:0,x:120,y:-60}},{{opacity:1,x:0,y:0,duration:0.55,ease:"power3.out"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 2.0), 2.0, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_lens: the number under the lens -------------------------------------------------------------------

def nh_lens(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline"):
        _chk("nh_lens", k, d.get(k, ""), k, out)
    z, sec, val, chk = d.get("zoom") or {}, d.get("section") or {}, d.get("value") or {}, d.get("check") or {}
    _chk("nh_lens", "zoom", z.get("text", ""), "zoom.text", out)
    _chk("nh_lens", "label", sec.get("label", ""), "section.label", out)
    _chk("nh_lens", "label", sec.get("film_label", ""), "section.film_label", out)
    _chk("nh_lens", "value", val.get("text", ""), "value.text", out)
    _chk("nh_lens", "sub", val.get("sub", ""), "value.sub", out)
    _chk("nh_lens", "check", chk.get("text", ""), "check.text", out)
    cy, r = zt + 440, 220                    # lens centre y and radius
    sparkle = "".join(f'<i class="nh-spark" style="left:{x}px;top:{y}px"></i>' for x, y in ((70, 236), (180, 228), (300, 240), (380, 232)))
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-stagebox" id="{s}tb" style="left:{X0}px;top:{zt + 200}px">{tube_svg(f"{s}t", d.get("product") or {}, 340)}</div>
  <svg class="nh-link" style="left:{X0 + 130}px;top:{zt + 260}px" width="240" height="160" viewBox="0 0 240 160"><path id="{s}lk" d="M4 150 C70 140 130 90 236 50" fill="none" stroke="#9B5560" stroke-width="3" stroke-dasharray="8 10"/></svg>
  <div class="nh-lens" id="{s}lens" style="left:{R - 2 * r - 20}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px">
    <div class="nh-lens-a" id="{s}la"><span>{_e(z.get("text", ""))}</span></div>
    <div class="nh-lens-b" id="{s}lb">
      <div class="nh-skin"><i></i><i></i><i></i></div>
      <div class="nh-film" id="{s}film">{sparkle}</div>
      <div class="nh-filmlabel" id="{s}fl">{_e(sec.get("film_label", ""))}</div>
      <div class="nh-skinlabel">{_e(sec.get("label", ""))}</div>
    </div>
  </div>
  <div class="nh-handle" id="{s}hd" style="left:{R - r - 20 + round(r * 0.6)}px;top:{cy + round(r * 0.68)}px"></div>
  <div class="nh-value" style="top:{cy + r + 14}px"><b>{_e(val.get("text", ""))}</b><span>{_e(val.get("sub", ""))}</span></div>
  <div class="nh-check" style="top:{cy + r + 114}px"><span>{_e(chk.get("text", ""))}</span></div>
  {_chip(c, d.get("chip") or {}, zt + 132, out, "nh_lens")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl.append(f'tl.fromTo("#{s}tb",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.5,ease:"power3.out"}},{c.t(0.2):.3f});')
    out.events.append(c.t(0.15))
    z_at = _rel(c, z.get("at", 0.6), 0.6, out)
    out.tl.append(f'tl.fromTo("#{s}lens",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.55,ease:"back.out(1.6)"}},{c.t(z_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}hd",{{opacity:0}},{{opacity:1,duration:0.4}},{c.t(z_at + 0.2):.3f});')
    out.tl.append(f'tl.fromTo("#{s}lk",{{strokeDashoffset:300,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.6,ease:"power2.out"}},{c.t(z_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s}la span",{{scale:0.7}},{{scale:1.06,duration:{max(0.8, 2.6):.2f},ease:"sine.out"}},{c.t(z_at):.3f});')
    out.events.append(c.t(z_at))
    if sec:
        at = _rel(c, sec.get("at", z_at + 2.5), z_at + 2.5, out)
        out.tl.append(f'tl.to("#{s}la",{{opacity:0,duration:0.35}},{c.t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}lb",{{opacity:0}},{{opacity:1,duration:0.35}},{c.t(at):.3f});')
        out.tl.append(f'tl.fromTo("#{s}film",{{scaleX:0}},{{scaleX:1,duration:1.4,ease:"power2.inOut"}},{c.t(at + 0.3):.3f});')
        out.tl.append(f'tl.fromTo("#{s}fl",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},{c.t(at + 1.5):.3f});')
        out.events += [c.t(at), c.t(at + 1.5)]
    if val:
        at = _rel(c, val.get("at", z_at + 3.0), z_at + 3.0, out)
        out.tl.append(_in(c, ".nh-value", at))
        out.events.append(c.t(at))
    if chk:
        at = _rel(c, chk.get("at", c.duration - 2.0), c.duration - 2.0, out)
        out.tl.append(_pop(c, ".nh-check span", at))
        out.events.append(c.t(at))
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 1.0), 1.0, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_amount: the amount on a whole body -----------------------------------------------------------------

BODY_SHAPES = ('<circle cx="150" cy="62" r="50"/>'
               '<rect x="88" y="124" width="124" height="250" rx="56"/>'
               '<rect x="40" y="134" width="44" height="236" rx="22"/>'
               '<rect x="216" y="134" width="44" height="236" rx="22"/>'
               '<rect x="94" y="330" width="52" height="300" rx="26"/>'
               '<rect x="154" y="330" width="52" height="300" rx="26"/>')


def nh_amount(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline"):
        _chk("nh_amount", k, d.get(k, ""), k, out)
    tot, sp, card, fin = d.get("total") or {}, d.get("spoons") or {}, d.get("card") or {}, d.get("finding") or {}
    _chk("nh_amount", "total", tot.get("text", ""), "total.text", out)
    _chk("nh_amount", "spoons", sp.get("text", ""), "spoons.text", out)
    _chk("nh_amount", "title", card.get("title", ""), "card.title", out)
    _chk("nh_amount", "text", card.get("text", ""), "card.text", out)
    _chk("nh_amount", "finding", fin.get("text", ""), "finding.text", out)
    n = int(sp.get("n", 6))
    minis = "".join(f'<span class="nh-minispoon" id="{s}ms{i}">{spoon_svg(f"{s}m{i}", 76)}</span>' for i in range(n))
    bh = 640
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-body" style="left:{X0 + 10}px;top:{zt + 180}px">
    <svg viewBox="0 0 300 640" width="{round(bh * 300 / 640)}" height="{bh}" xmlns="http://www.w3.org/2000/svg">
      <defs><clipPath id="{s}clip">{BODY_SHAPES}</clipPath>
        <linearGradient id="{s}fg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#D49A9E"/><stop offset="1" stop-color="#B9767D"/></linearGradient></defs>
      <g fill="#9B5560" stroke="#9B5560" stroke-width="12">{BODY_SHAPES}</g><g fill="#F6EAE6">{BODY_SHAPES}</g>
      <g clip-path="url(#{s}clip)"><rect id="{s}fill" x="0" y="640" width="300" height="640" fill="url(#{s}fg)"/>
        <rect id="{s}line" x="0" y="640" width="300" height="6" fill="#4A2F34"/></g>
    </svg>
    <div class="nh-illu">{_e(d.get("illu", "Illustration"))}</div>
  </div>
  <div class="nh-total" style="top:{zt + 200}px">{_e(tot.get("text", ""))}</div>
  <div class="nh-spoonrow" style="top:{zt + 370}px"><div class="nh-minis">{minis}</div><span>{_e(sp.get("text", ""))}</span></div>
  <div class="nh-card" style="top:{zt + 480}px"><div class="nh-card-head">{_icon("glass")}<b>{_e(card.get("title", ""))}</b></div>
    <div class="nh-card-text">{_e(card.get("text", ""))}</div></div>
  <div class="nh-finding" style="top:{zt + 730}px">{_e(fin.get("text", ""))}</div>
  {_chip(c, d.get("chip") or {}, zt + 128, out, "nh_amount")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl.append(_in(c, ".nh-body", 0.25, dy=40))
    out.events.append(c.t(0.15))
    f0 = _rel(c, d.get("fill_at", 0.6), 0.6, out)
    f1 = _rel(c, d.get("fill_end", f0 + 4.0), f0 + 4.0, out)
    out.tl.append(f'tl.fromTo("#{s}fill",{{attr:{{y:640}}}},{{attr:{{y:0}},duration:{max(0.8, f1 - f0):.2f},ease:"power1.inOut"}},{c.t(f0):.3f});')
    out.tl.append(f'tl.fromTo("#{s}line",{{attr:{{y:640}}}},{{attr:{{y:-6}},duration:{max(0.8, f1 - f0):.2f},ease:"power1.inOut"}},{c.t(f0):.3f});')
    out.events.append(c.t(f0))
    if tot:
        at = _rel(c, tot.get("at", f0 + 1.0), f0 + 1.0, out)
        out.tl.append(_pop(c, ".nh-total", at, frm=0.8))
        out.events.append(c.t(at))
    if sp:
        at = _rel(c, sp.get("at", f0 + 1.6), f0 + 1.6, out)
        out.tl.append(_in(c, ".nh-spoonrow span", at, dx=-12, dy=0))
        for i in range(n):
            out.tl.append(_pop(c, f"#{s}ms{i}", at + 0.1 * i, frm=0.4, dur=0.3))
        out.events.append(c.t(at))
    if card:
        at = _rel(c, card.get("at", f1 + 0.5), f1 + 0.5, out)
        out.tl.append(_in(c, ".nh-card", at, dy=30))
        out.events.append(c.t(at))
    if fin:
        at = _rel(c, fin.get("at", c.duration - 3.0), c.duration - 3.0, out)
        out.tl.append(_in(c, ".nh-finding", at))
        out.events.append(c.t(at))
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 1.2), 1.2, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_effect: what the source says, as a schema ---------------------------------------------------------

def nh_effect(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline", "schema"):
        _chk("nh_effect", k, d.get(k, ""), k, out)
    rows = list(d.get("rows", []))[:2]
    words = {"de": ("Menge", "Schutz"), "en": ("Amount", "Protection")}.get(c.lang, ("Menge", "Schutz"))
    cards = []
    for i, r in enumerate(rows):
        _chk("nh_effect", "title", r.get("title", ""), f"rows[{i}].title", out)
        _chk("nh_effect", "label", r.get("label", ""), f"rows[{i}].label", out)
        same = (f'<i class="nh-same" id="{s}same"></i><span class="nh-same-l" id="{s}samel">{_e(d.get("same_label", ""))}</span>'
                if i == 1 and d.get("same_label") else "")
        cards.append(f"""<div class="nh-ecard" id="{s}c{i}" style="top:{zt + 200 + i * 290}px">
    <div class="nh-ecard-title">{_e(r.get("title", ""))}</div>
    <div class="nh-erow"><span class="nh-erow-l">{_e(words[0])}</span><div class="nh-track"><i class="nh-bar nh-bar-amt" id="{s}a{i}"></i></div></div>
    <div class="nh-erow"><span class="nh-erow-l">{_e(words[1])}</span><div class="nh-track"><i class="nh-bar nh-bar-pro" id="{s}p{i}"></i>{same}</div></div>
    <div class="nh-ecard-label" id="{s}lab{i}">{_e(r.get("label", ""))}</div>
  </div>""")
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  {"".join(cards)}
  <div class="nh-schema" style="top:{zt + 775}px">{_mark("schema")}<span>{_e(d.get("schema", ""))}</span></div>
  {_chip(c, d.get("chip") or {}, zt + 132, out, "nh_effect")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.events.append(c.t(0.15))
    for i, r in enumerate(rows):
        at = 0.35 + 0.25 * i
        out.tl.append(_in(c, f"#{s}c{i}", at, dy=36))
        out.tl.append(f'tl.fromTo("#{s}a{i}",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{c.t(at + 0.2):.3f});')
        if i == 0:
            out.tl.append(f'tl.fromTo("#{s}p{i}",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{c.t(at + 0.3):.3f});')
        else:
            out.tl.append(f'tl.set("#{s}p{i}",{{scaleX:0}},{c.t(0):.3f});')
        if i == 0:
            out.tl.append(_in(c, f"#{s}lab0", at + 0.6, dy=8))
    out.events.append(c.t(0.6))
    if len(rows) > 1:
        r1 = rows[1]
        cut = max(_rel(c, d.get("cut_at", 1.5), 1.5, out), 0.35 + 0.25 + 0.2 + 0.65)   # after the bar has grown in
        out.tl.append(f'tl.to("#{s}a1",{{scaleX:{float(r1.get("amount", 0.5)):.3f},duration:0.6,ease:"power2.inOut"}},{c.t(cut):.3f});')
        out.events.append(c.t(cut))
        if d.get("same_label"):
            same = max(_rel(c, d.get("same_at", cut + 1.2), cut + 1.2, out), cut + 0.65)
            out.tl.append(f'tl.fromTo("#{s}same, #{s}samel",{{opacity:0}},{{opacity:1,duration:0.3}},{c.t(same):.3f});')
            out.tl.append(f'tl.fromTo("#{s}p1",{{scaleX:0}},{{scaleX:{float(r1.get("amount", 0.5)):.3f},duration:0.5,ease:"power2.inOut"}},{c.t(same):.3f});')
            out.events.append(c.t(same))
        drop = max(_rel(c, d.get("drop_at", cut + 2.5), cut + 2.5, out), cut + 1.25)
        out.tl.append(f'tl.to("#{s}p1",{{scaleX:{float(r1.get("protect", 0.33)):.3f},duration:0.7,ease:"power2.inOut"}},{c.t(drop):.3f});')
        out.tl.append(_pop(c, f"#{s}lab1", drop + 0.4, frm=0.85))
        out.events.append(c.t(drop))
    out.tl.append(_in(c, ".nh-schema", 0.9, dy=8))
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 1.0), 1.0, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_apply: everyday application ---------------------------------------------------------------------

ARM = ("M0 70 C200 60 420 58 600 70 C640 72 660 64 690 52 C720 36 760 30 790 44 C805 52 800 66 780 72 "
       "C820 70 850 80 856 100 C862 124 840 140 800 140 C740 142 680 138 620 136 C420 136 200 140 0 142 Z")
STRAND = "M80 100 C250 94 420 92 560 98"


def nh_apply(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline", "arm_label"):
        _chk("nh_apply", k, d.get(k, ""), k, out)
    steps = list(d.get("steps", []))
    shtml = []
    for i, st in enumerate(steps):
        _chk("nh_apply", "title", st.get("title", ""), f"steps[{i}].title", out)
        _chk("nh_apply", "sub", st.get("sub", ""), f"steps[{i}].sub", out)
        shtml.append(f'<div class="nh-step" id="{s}st{i}" style="top:{zt + 420 + i * 140}px"><span class="nh-step-ico">{_icon(st.get("icon", "sun"))}</span>'
                     f'<div><div class="nh-step-title">{_e(st.get("title", ""))}</div><div class="nh-step-sub">{_e(st.get("sub", ""))}</div></div></div>')
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-arm" style="left:{X0}px;top:{zt + 180}px">
    <svg viewBox="0 0 864 160" width="{W}" height="{round(160 * W / 864)}" xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="{s}ag" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#D9A9A6"/><stop offset="1" stop-color="#C98F93"/></linearGradient></defs>
      <path d="{ARM}" fill="url(#{s}ag)" stroke="#9B5560" stroke-width="4"/>
      <path d="{STRAND}" fill="none" stroke="#9B5560" stroke-opacity="0.45" stroke-width="20" stroke-linecap="round" stroke-dasharray="560" stroke-dashoffset="560" id="{s}strsh" transform="translate(0 4)"/>
      <path id="{s}sheen" d="{ARM}" fill="rgba(255,255,255,0.32)"/>
      <path id="{s}strand" d="{STRAND}" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" stroke-dasharray="560" stroke-dashoffset="560"/>
    </svg>
    <div class="nh-illu nh-illu-arm">{_e(d.get("arm_label", ""))}</div>
  </div>
  {"".join(shtml)}
  {_chip(c, d.get("chip") or {}, zt + 132 if d.get("photo") else zt + 780, out, "nh_apply")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl.append(_in(c, ".nh-arm", 0.25, dx=-30, dy=0))
    out.events.append(c.t(0.15))
    draw = _rel(c, d.get("draw_at", 0.7), 0.7, out)
    out.tl.append(f'tl.fromTo("#{s}strand, #{s}strsh",{{strokeDashoffset:560}},{{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"}},{c.t(draw):.3f});')
    out.events.append(c.t(draw))
    spread = _rel(c, d.get("spread_at", draw + 1.6), draw + 1.6, out)
    out.tl.append(f'tl.fromTo("#{s}sheen",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power2.out"}},{c.t(spread):.3f});')
    out.tl.append(f'tl.to("#{s}strand, #{s}strsh",{{opacity:0,duration:0.9,ease:"power2.out"}},{c.t(spread):.3f});')
    out.events.append(c.t(spread))
    prev = spread
    for i, st in enumerate(steps):
        at = _rel(c, st.get("at", prev + 1.2), prev + 1.2, out)
        out.tl.append(_in(c, f"#{s}st{i}", at, dx=-24, dy=0))
        out.tl.append(_pop(c, f"#{s}st{i} .nh-step-ico", at + 0.1, frm=0.5))
        out.events.append(c.t(at))
        prev = at
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 1.0), 1.0, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_close: rule, question, sign-off ---------------------------------------------------------------

LOGO = Path(__file__).resolve().parents[1] / "assets" / "logo" / "dewlane-mark.svg"


def nh_close(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "rule", "claim", "disclaimer"):
        _chk("nh_close", k, d.get(k, ""), k, out)
    q = d.get("question") or {}
    _chk("nh_close", "question", q.get("text", ""), "question.text", out)
    mark = LOGO.read_text(encoding="utf-8") if LOGO.exists() else ""
    mark = re.sub(r"<\?xml.*?\?>", "", mark)
    out.html = f"""<div class="nh-in nh-close">
  <div class="nh-close-kicker" style="top:{zt}px">{_e(d.get("kicker", ""))}</div>
  <div class="nh-rule" style="top:{zt + 60}px">{_e(d.get("rule", ""))}</div>
  <div class="nh-stagebox nh-close-tube" id="{s}tb" style="left:{540 - _prod_size(d.get("product") or {}, 300)[0] // 2}px;top:{zt + 300}px">{product_svg(f"{s}t", d.get("product") or {}, 300)}</div>
  <div class="nh-ask" style="top:{zt + 630}px"><span>{_e(q.get("text", ""))}</span></div>
  <div class="nh-sign" id="{s}sign" style="top:{zt + 300}px"><div class="nh-sign-mark">{mark}</div><div class="nh-sign-word">DEWLANE</div>
    <div class="nh-claim">{_e(d.get("claim", ""))}</div><div class="nh-disc">{_e(d.get("disclaimer", ""))}</div></div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-close-kicker", 0.05, dy=0))
    rule_at = _rel(c, d.get("rule_at", 0.2), 0.2, out)
    out.tl.append(_in(c, ".nh-rule", rule_at, dy=24, dur=0.5))
    out.tl.append(f'tl.fromTo("#{s}tb",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{c.t(rule_at + 0.3):.3f});')
    out.events.append(c.t(rule_at))
    if q:
        at = _rel(c, q.get("at", 2.5), 2.5, out)
        out.tl.append(_pop(c, ".nh-ask span", at, frm=0.85))
        out.events.append(c.t(at))
    sign = _rel(c, d.get("sign_at", c.duration - 3.5), c.duration - 3.5, out)
    out.tl.append(f'tl.to("#{s}tb",{{opacity:0,y:-20,duration:0.3,ease:"power2.in"}},{c.t(sign - 0.3):.3f});')
    out.tl.append(f'tl.fromTo("#{s}sign",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{c.t(sign):.3f});')
    out.events.append(c.t(sign))
    return out


TEMPLATES = {"nh_stage": nh_stage, "nh_lens": nh_lens, "nh_amount": nh_amount, "nh_effect": nh_effect,
             "nh_apply": nh_apply, "nh_close": nh_close}


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: N802 (contract name)
    acc, txt, mut = pal.get("accent", "#9B5560"), pal.get("text", "#4A2F34"), pal.get("muted", "#7E6468")
    surf, hair = pal.get("surface", "#FFFCF9"), pal.get("hairline", "#E8D9D4")
    blush, amber, green = pal.get("blush", "#C98F93"), pal.get("signal_amber", "#946420"), pal.get("signal_green", "#4F7A62")
    shadow = "rgba(74,47,52,0.14)"
    D, B = f"'FN {display}'", f"'FN {body}'"
    return f"""
.nh-in{{position:absolute;inset:0;}}
.nh-kicker{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:center;gap:14px;font-family:{B};font-weight:600;font-size:26px;letter-spacing:0.14em;text-transform:uppercase;color:{mut};}}
.nh-dot{{display:inline-block;width:14px;height:14px;border-radius:50% 50% 50% 0;background:{blush};}}
.nh-h2{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:500;font-size:64px;line-height:1.1;color:{txt};}}
.nh-count{{position:absolute;left:{X0}px;width:{W}px;height:150px;display:flex;align-items:baseline;gap:26px;}}
.nh-digits{{position:relative;width:110px;height:150px;flex:none;}}
.nh-digit{{position:absolute;left:0;top:0;font-family:{D};font-weight:600;font-size:150px;line-height:1;color:{acc};opacity:0;}}
.nh-unit{{font-family:{D};font-weight:500;font-size:84px;line-height:1;color:{txt};}}
.nh-sub{{position:absolute;left:{X0}px;width:{W}px;font-family:{B};font-size:44px;color:{mut};}}
.nh-stagebox{{position:absolute;}}
.nh-ring{{position:absolute;left:-8px;top:106px;width:200px;height:200px;border-radius:50%;border:5px solid {acc};opacity:0;}}
.nh-lensmini{{position:absolute;left:112px;top:52px;width:150px;height:150px;border-radius:50%;border:12px solid {txt};background:rgba(255,255,255,0.25);opacity:0;box-shadow:0 12px 30px {shadow};}}
.nh-spoonbox{{position:absolute;width:220px;height:90px;filter:drop-shadow(0 10px 14px {shadow});}}
.nh-chipline{{position:absolute;left:{X0}px;width:{W}px;display:flex;}}
.nh-chip{{display:inline-flex;align-items:center;gap:12px;white-space:nowrap;font-family:{B};font-size:30px;color:{txt};background:{surf};border:2px solid {hair};border-radius:999px;padding:8px 24px;}}
.nh-chip b{{color:{txt};font-weight:600;}}
.nh-mk{{display:inline-block;width:18px;height:18px;flex:none;background:{acc};}}
.nh-mk-schema{{background:transparent;border:3px dashed {mut};box-sizing:border-box;}}
.nh-mk-unsicher{{background:linear-gradient(90deg,{amber} 50%,transparent 50%);border:2px solid {amber};border-radius:50%;}}
.nh-mk-beispiel{{background:#8a93a6;}}
.nh-link{{position:absolute;overflow:visible;}}
.nh-lens{{position:absolute;border-radius:50%;overflow:hidden;background:{surf};border:16px solid {txt};box-sizing:border-box;box-shadow:0 26px 60px {shadow};}}
.nh-handle{{position:absolute;width:150px;height:34px;border-radius:17px;background:{txt};rotate:45deg;transform-origin:0 50%;opacity:0;}}
.nh-lens-a{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#F6E6DF;}}
.nh-lens-a span{{font-family:{D};font-weight:600;font-size:108px;color:{acc};white-space:nowrap;}}
.nh-lens-b{{position:absolute;inset:0;opacity:0;background:#FBF7F4;}}
.nh-skin{{position:absolute;left:0;right:0;top:250px;bottom:0;display:flex;flex-direction:column;}}
.nh-skin i{{display:block;flex:1;}}
.nh-skin i:nth-child(1){{flex:0.5;background:#E9CFC8;}} .nh-skin i:nth-child(2){{background:#E0BDB5;}} .nh-skin i:nth-child(3){{background:#D4ABA3;}}
.nh-film{{position:absolute;left:0;right:0;top:212px;height:40px;background:linear-gradient(180deg,#FFFFFF 0%,#FBF3EF 100%);border-top:2px solid #EADBD5;transform-origin:left center;}}
.nh-spark{{position:absolute;width:10px;height:10px;border-radius:50%;background:#FFFFFF;box-shadow:0 0 0 3px rgba(255,255,255,0.6);}}
.nh-filmlabel{{position:absolute;left:0;right:0;top:140px;text-align:center;font-family:{B};font-weight:600;font-size:30px;color:{acc};}}
.nh-skinlabel{{position:absolute;left:0;right:0;top:268px;text-align:center;font-family:{B};font-size:24px;letter-spacing:0.08em;text-transform:uppercase;color:#6E4B50;}}
.nh-value{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:baseline;justify-content:flex-start;gap:20px;}}
.nh-value b{{font-family:{D};font-weight:600;font-size:76px;color:{txt};}}
.nh-value span{{font-family:{B};font-size:36px;color:{mut};}}
.nh-check{{position:absolute;left:{X0}px;width:{W}px;display:flex;justify-content:flex-start;}}
.nh-check span{{font-family:{B};font-weight:600;font-size:32px;color:{green};border:3px solid {green};border-radius:999px;padding:8px 26px;background:{surf};}}
.nh-body{{position:absolute;width:300px;}}
.nh-illu{{margin-top:10px;text-align:center;font-family:{B};font-size:26px;letter-spacing:0.1em;text-transform:uppercase;color:{mut};}}
.nh-illu-arm{{position:absolute;left:0;top:162px;margin:0;}}
.nh-total{{position:absolute;left:470px;width:{R - 470}px;font-family:{D};font-weight:600;font-size:132px;line-height:1.1;color:{acc};}}
.nh-spoonrow{{position:absolute;left:470px;width:{R - 470}px;}}
.nh-minis{{display:flex;gap:4px;height:34px;}}
.nh-minispoon{{display:block;width:76px;height:32px;}}
.nh-spoonrow span{{display:block;margin-top:14px;font-family:{B};font-size:36px;color:{txt};}}
.nh-card{{position:absolute;left:470px;width:{R - 470}px;background:{surf};border:2px solid {hair};border-radius:22px;padding:22px 26px;box-sizing:border-box;box-shadow:0 14px 34px {shadow};}}
.nh-card-head{{display:flex;align-items:center;gap:12px;font-family:{B};font-size:30px;color:{txt};}}
.nh-card-head b{{color:{txt};font-weight:600;}}
.nh-card-text{{margin-top:10px;font-family:{B};font-size:34px;line-height:1.28;color:{txt};}}
.nh-ico{{width:44px;height:44px;flex:none;color:{acc};}}
.nh-finding{{position:absolute;left:470px;width:{R - 470}px;font-family:{D};font-weight:500;font-size:38px;line-height:1.18;color:{txt};}}
.nh-ecard{{position:absolute;left:{X0}px;width:{W}px;height:262px;background:{surf};border:2px solid {hair};border-radius:22px;padding:22px 30px;box-sizing:border-box;box-shadow:0 14px 34px {shadow};}}
.nh-ecard-title{{font-family:{D};font-weight:500;font-size:46px;color:{txt};}}
.nh-erow{{display:flex;align-items:center;gap:20px;margin-top:18px;}}
.nh-erow-l{{width:176px;flex:none;font-family:{B};font-weight:600;font-size:24px;letter-spacing:0.08em;text-transform:uppercase;color:{mut};}}
.nh-track{{position:relative;flex:1;height:30px;border-radius:15px;background:{hair};}}
.nh-bar{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:13px;transform-origin:left center;}}
.nh-bar-amt{{background:linear-gradient(90deg,#F3DCD6,#FFFFFF);border:2px solid {blush};box-sizing:border-box;}}
.nh-bar-pro{{background:{acc};}}
.nh-same{{position:absolute;left:50%;top:-12px;bottom:-12px;width:0;border-left:3px dashed {txt};opacity:0;}}
.nh-same-l{{position:absolute;left:50%;top:34px;margin-left:12px;font-family:{B};font-size:26px;color:{mut};white-space:nowrap;opacity:0;}}
.nh-ecard-label{{margin-top:16px;font-family:{B};font-weight:600;font-size:32px;color:{acc};}}
.nh-schema{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:center;gap:12px;font-family:{B};font-weight:500;font-size:30px;color:{txt};}}
.nh-arm{{position:absolute;width:864px;height:160px;}}
.nh-step{{position:absolute;left:{X0}px;width:{W}px;height:110px;display:flex;align-items:center;gap:26px;}}
.nh-step-ico{{width:84px;height:84px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:50%;background:{surf};border:2px solid {hair};box-shadow:0 10px 24px {shadow};}}
.nh-step-title{{font-family:{D};font-weight:500;font-size:44px;line-height:1.1;color:{txt};}}
.nh-step-sub{{margin-top:6px;font-family:{B};font-size:30px;color:{mut};}}
.nh-close-kicker{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{B};font-weight:600;font-size:26px;letter-spacing:0.16em;text-transform:uppercase;color:{mut};}}
.nh-rule{{position:absolute;left:{X0}px;width:{W}px;text-align:center;font-family:{D};font-weight:500;font-size:76px;line-height:1.12;color:{txt};}}
.nh-ask{{position:absolute;left:{X0}px;width:{W}px;display:flex;justify-content:center;}}
.nh-ask span{{font-family:{B};font-weight:600;font-size:36px;color:{acc};border:3px solid {acc};border-radius:999px;padding:12px 32px;background:{surf};}}
.nh-sign{{position:absolute;left:{X0}px;width:{W}px;display:flex;flex-direction:column;align-items:center;opacity:0;}}
.nh-sign-mark svg{{width:110px;height:110px;display:block;}}
.nh-sign-word{{margin-top:18px;font-family:{D};font-weight:500;font-size:56px;letter-spacing:0.18em;color:{txt};}}
.nh-claim{{margin-top:16px;font-family:{B};font-size:36px;color:{txt};}}
.nh-disc{{margin-top:12px;font-family:{B};font-size:32px;color:{txt};}}
"""


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: N802 (contract name)
    """Format-wide layer: ivory studio (back wall, soft floor sweep, slow light pool, dew bokeh at the edges, grain)
    and the stamp "Animation · neutrales Produkt · kein Produkttest" for the whole video."""
    lang = getattr(plan, "language", "de")
    pal = dict(getattr(brand, "palette", {}) or {})
    mut, acc, txt = pal.get("muted", "#7E6468"), pal.get("accent", "#9B5560"), pal.get("text", "#4A2F34")
    bokeh = "".join(
        f'<i class="nhx-b nhx-p{p}" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px"></i>'
        for x, y, r, p in ((-40, 420, 180, 0), (930, 360, 140, 1), (960, 1180, 220, 0), (-70, 1300, 160, 1), (880, 1700, 120, 2), (40, 1760, 90, 2)))
    grain = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
             "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>"
             "<feColorMatrix values='0 0 0 0 0.29 0 0 0 0 0.18 0 0 0 0 0.2 0 0 0 0.05 0'/></filter>"
             "<rect width='220' height='220' filter='url(%23n)'/></svg>\")")
    html_ = f"""<div id="nhx" style="position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:#F8F3EF">
<div style="position:absolute;left:0;right:0;top:0;height:1240px;background:linear-gradient(180deg,#F7F0EB 0%,#FBF7F3 70%,#F6EEE9 100%)"></div>
<div style="position:absolute;left:0;right:0;top:1180px;bottom:0;background:linear-gradient(180deg,#F3E9E3 0%,#EFE3DC 100%)"></div>
<div style="position:absolute;left:-200px;right:-200px;top:1120px;height:160px;background:radial-gradient(ellipse 60% 50% at 50% 50%,rgba(255,255,255,0.75),transparent 70%)"></div>
<div id="nhx-pool" style="position:absolute;left:90px;top:360px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.85) 0%,rgba(255,255,255,0.35) 45%,transparent 70%)"></div>
<div id="nhx-win" style="position:absolute;left:-260px;top:-240px;width:900px;height:900px;background:radial-gradient(circle,rgba(255,250,244,0.9) 0%,transparent 65%)"></div>
{bokeh}
<div class="nhx-grain"></div>
<style>.nhx-grain{{position:absolute;inset:0;background-image:{grain};opacity:0.6}}
.nhx-b{{position:absolute;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,0.95),rgba(201,143,147,0.18) 60%,rgba(201,143,147,0.05) 100%);border:2px solid rgba(255,255,255,0.7)}}
.nhx-p0{{opacity:0.55}} .nhx-p1{{opacity:0.7}} .nhx-p2{{opacity:0.85}}</style></div>
<div id="nhx-stamp" style="position:absolute;left:108px;top:194px;width:822px;z-index:21;display:flex;align-items:center;gap:12px;font-family:'FN Inter';font-weight:500;font-size:28px;letter-spacing:0.02em;color:{txt}">
<i style="display:inline-block;width:12px;height:12px;background:{acc};flex:none"></i><span>{html.escape(STAMP.get(lang, STAMP['de']))}</span></div>"""
    script = """<script>
(function(){var t=window.__timelines&&window.__timelines.main;if(!t)return;var T=Number(document.getElementById("root").dataset.duration)||60;
t.fromTo("#nhx-pool",{x:-60,y:30},{x:60,y:-30,duration:T,ease:"sine.inOut"},0);
t.fromTo("#nhx-win",{opacity:0.7},{opacity:1,duration:T/2,ease:"sine.inOut",yoyo:true,repeat:1},0);
t.fromTo(".nhx-p0",{y:40},{y:-40,duration:T,ease:"none"},0);
t.fromTo(".nhx-p1",{y:90},{y:-90,duration:T,ease:"none"},0);
t.fromTo(".nhx-p2",{y:160},{y:-160,duration:T,ease:"none"},0);
t.seek(0);})();
</script>"""
    return {"under_scenes_html": html_, "body_end_html": script, "events": []}


def MANIFEST_EXTRA(plan) -> dict:  # noqa: N802 (contract name)
    used = sorted({b.scene_type for b in plan.beats if b.scene_type.startswith("nh_")})
    if not used:
        return {}
    return {"format": {"name": "Dewlane Format \"Nahaufnahme\"", "version": "0.1 (Pilot)",
                       "bible": "OneDrive\\Business\\02 Marke\\Dewlane\\Format-Bibel.md", "scene_types": used,
                       "visuals": "Animation aus HTML/SVG/CSS, neutrales erfundenes Produkt ohne Marke; Haut nur als schematische "
                                  "Illustration; Wirkungsdiagramme als Schema nach Quelle, keine Messung, kein Produkttest",
                       "ai_images": "keine (nur Code-Grafik)"}}


# =========================================================================================================
# General "Nahaufnahme" scenes for series topics (02.11.2026, week 1): more neutral product forms and six
# scene types that take the data of the week-1 plans (dw_hook, dw_facts, dw_bars, dw_versus, dw_timeline,
# dw_steps, file_close) so that the checked spoken text and its sources stay as they are.
#
# | scene type | role                         | data |
# |------------|------------------------------|------|
# | nh_hook    | product on the stage, question | kicker, product{kind, line1, line2, big}, question, badge, question_at, badge_at, ring_at, lens_at, chip |
# | nh_facts   | product + lens, fact rows     | kicker, headline, product, zoom, flip, doc{act, ref, tag}, rows[{text, mark, value, at}] |
# | nh_list    | names peel off the product    | kicker, headline, caption, product, rows[{label, value, at}] |
# | nh_versus  | two products side by side     | kicker, headline, left/right{tag, title, product, rows[{text, mark, at}]} |
# | nh_time    | dates on a rail               | kicker, headline, product, nodes[{date, text, at}] |
# | nh_steps   | how to read / apply           | kicker, headline, product, items[{title, sub, icon, at}] |
# Items without "at" are anchored automatically on the first matching content word they share with the speech.
# =========================================================================================================

LIMITS.update({
    "nh_hook": {"kicker": 34, "question": 40, "badge": 14, "chip": 44},
    "nh_facts": {"kicker": 34, "headline": 30, "zoom": 14, "text": 60, "value": 6, "act": 30, "ref": 34},
    "nh_list": {"kicker": 34, "headline": 26, "caption": 48, "label": 24, "value": 10},
    "nh_versus": {"kicker": 34, "headline": 26, "tag": 22, "title": 26, "text": 34},
    "nh_time": {"kicker": 34, "headline": 30, "date": 14, "text": 50},
    "nh_steps": {"kicker": 34, "headline": 26, "title": 36, "sub": 36},
})
HOOK_SCENE_TYPES.append("nh_hook")

# label box of each product form in its own viewBox (x, y, w, h) and the viewBox size (w, h)
FORMS = {"tube": ((40, 168, 180, 246), (260, 620)), "jar": ((56, 128, 248, 132), (360, 300)),
         "bottle": ((36, 250, 148, 220), (220, 620)), "dropper": ((34, 300, 132, 170), (200, 560)),
         "spray": ((42, 270, 116, 230), (200, 620))}


def _label_text(p: dict, lx: int, ly: int, lw: int, lh: int, k: float = 1.0) -> str:
    """Label band of a neutral product. Text only where it renders at 24 px or more (Pruefrunde R7); smaller lines
    become abstract bars, so the product never carries unreadable print."""
    l1, l2, big = _e(p.get("line1", "")), _e(p.get("line2", "")), _e(p.get("big", ""))
    cx = lx + lw / 2
    out = [f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12" fill="#F3E2DB"/>']

    def bar(yy, ww):
        return f'<rect x="{cx - ww / 2:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{max(6, lh * 0.05):.0f}" rx="4" fill="#CDB6B0"/>'

    def txt(yy, size, s, fam, col):
        return (f'<text x="{cx}" y="{yy:.0f}" text-anchor="middle" font-family="{fam}" font-weight="600" '
                f'font-size="{size}" fill="{col}">{s}</text>')

    if l1:
        f1 = min(int(lh * 0.2), int(lw / max(1, len(p.get("line1", ""))) * 1.5))
        out.append(txt(ly + lh * 0.24, f1, l1, "'FN Inter'", "#7E6468") if f1 * k >= 24 else bar(ly + lh * 0.16, lw * 0.55))
    if l2:
        f2 = min(int(lh * 0.22), int(lw / max(1, len(p.get("line2", ""))) * 1.5))
        out.append(txt(ly + lh * 0.48, f2, l2, "'FN Inter'", "#9B5560") if f2 * k >= 24 else bar(ly + lh * 0.4, lw * 0.35))
    if big:
        fb = max(24, min(int(lh * 0.42), int(lw / max(1, len(p.get("big", ""))) * 1.55)))
        out.append(txt(ly + lh * 0.86, fb, big, "'FN Playfair Display'", "#9B5560") if fb * k >= 24 else bar(ly + lh * 0.7, lw * 0.4))
    return "".join(out)


def product_svg(ident: str, p: dict, h: int = 440) -> str:
    """Neutral invented product, no brand: tube, jar, bottle, dropper or spray."""
    kind = (p or {}).get("kind", "tube")
    if kind == "tube" or kind not in FORMS:
        return tube_svg(ident, p or {}, h)
    (lx, ly, lw, lh), (vw, vh) = FORMS[kind]
    w = round(h * vw / vh)
    g = (f'<defs><linearGradient id="{ident}g" x1="0" x2="1"><stop offset="0" stop-color="#E6D9D3"/><stop offset="0.3" stop-color="#FFFFFF"/>'
         f'<stop offset="0.65" stop-color="#FBF6F2"/><stop offset="1" stop-color="#DCCBC4"/></linearGradient>'
         f'<linearGradient id="{ident}c" x1="0" x2="1"><stop offset="0" stop-color="#C9B7B1"/><stop offset="0.35" stop-color="#EFE6E2"/><stop offset="1" stop-color="#BFAEA8"/></linearGradient>'
         f'<linearGradient id="{ident}a" x1="0" x2="1"><stop offset="0" stop-color="#D9B99C"/><stop offset="0.35" stop-color="#F4E3D2"/><stop offset="1" stop-color="#C9A585"/></linearGradient></defs>')
    if kind == "jar":
        body = (f'<ellipse cx="180" cy="292" rx="150" ry="7" fill="rgba(74,47,52,0.16)"/>'
                f'<rect x="20" y="96" width="320" height="192" rx="30" fill="url(#{ident}g)" stroke="#E2D5CF" stroke-width="2"/>'
                f'<rect x="32" y="22" width="296" height="80" rx="18" fill="url(#{ident}c)"/>'
                f'<path d="M44 40 H316" stroke="rgba(255,255,255,0.6)" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M40 120 C42 180 44 230 52 270" stroke="rgba(255,255,255,0.9)" stroke-width="9" fill="none" stroke-linecap="round"/>')
    elif kind == "bottle":
        body = (f'<ellipse cx="110" cy="612" rx="90" ry="8" fill="rgba(74,47,52,0.16)"/>'
                f'<rect x="72" y="8" width="76" height="74" rx="10" fill="url(#{ident}c)"/>'
                f'<path d="M64 80 H156 L176 130 Q200 140 200 180 V560 Q200 600 160 604 H60 Q20 600 20 560 V180 Q20 140 44 130 Z" fill="url(#{ident}g)" stroke="#E2D5CF" stroke-width="2"/>'
                f'<path d="M38 190 C38 330 40 460 46 560" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round"/>')
    elif kind == "dropper":
        body = (f'<ellipse cx="100" cy="552" rx="84" ry="7" fill="rgba(74,47,52,0.16)"/>'
                f'<ellipse cx="100" cy="66" rx="40" ry="56" fill="#8E6A6E"/><path d="M80 40 Q86 24 98 20" stroke="rgba(255,255,255,0.35)" stroke-width="8" fill="none" stroke-linecap="round"/>'
                f'<rect x="54" y="112" width="92" height="70" rx="10" fill="url(#{ident}c)"/>'
                f'<rect x="18" y="176" width="164" height="372" rx="38" fill="url(#{ident}a)" stroke="#CDAE92" stroke-width="2"/>'
                f'<path d="M36 210 C36 330 38 440 44 520" stroke="rgba(255,255,255,0.7)" stroke-width="9" fill="none" stroke-linecap="round"/>')
    else:  # spray
        body = (f'<ellipse cx="100" cy="612" rx="84" ry="8" fill="rgba(74,47,52,0.16)"/>'
                f'<rect x="44" y="12" width="112" height="118" rx="22" fill="url(#{ident}c)"/>'
                f'<rect x="84" y="30" width="32" height="18" rx="5" fill="#A8968F"/>'
                f'<rect x="30" y="126" width="140" height="478" rx="26" fill="url(#{ident}g)" stroke="#E2D5CF" stroke-width="2"/>'
                f'<path d="M46 150 C46 300 48 450 52 580" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round"/>')
    return (f'<svg class="nh-prod" id="{ident}" viewBox="0 0 {vw} {vh}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{g}{body}'
            f'{_label_text(p, lx, ly, lw, lh, h / vh)}</svg>')


def _prod_size(p: dict, h: int) -> tuple[int, int, tuple[float, float]]:
    """Width, height and the centre of the label band in px for a product drawn at height h."""
    kind = (p or {}).get("kind", "tube")
    (lx, ly, lw, lh), (vw, vh) = FORMS.get(kind, FORMS["tube"])
    k = h / vh
    return round(vw * k), h, ((lx + lw / 2) * k, (ly + lh / 2) * k)


def _fit(p: dict, h: int, maxw: int) -> int:
    """Height at which the product is at most maxw wide (wide forms such as the jar get lower)."""
    (_, _, _, _), (vw, vh) = FORMS.get((p or {}).get("kind", "tube"), FORMS["tube"])
    return min(h, int(maxw * vh / vw))


STOP = set(("der die das den dem des und oder ein eine einen einem einer eines ist sind wird werden nicht dass wie was mit von "
            "für auf aus bei nach vor zum zur auch nur noch schon dann wenn aber also sich sie ihr wir the and for with that this are "
            "was not from have has can may must its into than then when only also your you they their what which these those").split())


def _auto_at(c: SceneCtx, texts: list, given: list, lo: float = 0.8, hi: float | None = None) -> list[float]:
    """Start times (beat-relative) for list items: explicit 'at'; else a spoken content word of the item close to its
    evenly spaced slot (+-2.5 s); else the slot itself. All items are on screen by 80 % of the beat."""
    hi = hi if hi is not None else max(lo + 0.5, c.duration * 0.72)
    n = len(texts)
    even = [lo + (hi - lo) * i / max(1, n - 1) if n > 1 else lo for i in range(n)]
    words = [(_norm(w.text), w.start - c.start) for w in (c.words or [])]
    out, prev = [], lo - 0.6
    tmp = SceneOut(html="")
    for i, (t, g) in enumerate(zip(texts, given)):
        if g is not None:
            at = _rel(c, g, even[i], tmp)
        else:
            at = None
            for tok in re.findall(r"[\wäöüßÄÖÜ]+", str(t)):
                stem = _norm(tok)[:6]
                if len(stem) < 4 or stem in STOP:
                    continue
                hit = next((s for w, s in words if prev + 0.3 < s and abs(s - even[i]) <= 2.5 and w.startswith(stem)), None)
                if hit is not None:
                    at = hit
                    break
            if at is None:
                at = even[i]
        at = min(max(at, prev + 0.5, 0.3), max(hi, prev + 0.5), c.duration - 0.6)
        out.append(at)
        prev = at
    return out


def _ico2(name: str) -> str:
    extra = {
        "doc": '<path d="M18 8 H40 L50 18 V56 H18 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><path d="M26 30 H42 M26 40 H42" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
        "shield": '<path d="M32 6 L54 14 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V14 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>',
        "hourglass": '<path d="M16 8 H48 M16 56 H48 M20 8 C20 24 44 26 44 32 C44 38 20 40 20 56 M44 8 C44 24 20 26 20 32 C20 38 44 40 44 56" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>',
        "drop": '<path d="M32 6 C26 16 14 28 14 40 A18 18 0 0 0 50 40 C50 28 38 16 32 6 Z" fill="none" stroke="currentColor" stroke-width="5"/>',
        "check": '<path d="M12 34 L26 48 L52 18" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
        "lens": '<circle cx="28" cy="28" r="16" fill="none" stroke="currentColor" stroke-width="5"/><path d="M40 40 L54 54" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>',
    }
    inner = ICONS.get(name) or extra.get(name) or extra["check"]
    return f'<svg class="nh-ico" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'


def _mk2(mark: str) -> str:
    m = {"fact": "fakt", "gap": "luecke", "open": "unsicher", "ok": "ok", "interp": "auslegung"}.get(mark or "fact", "fakt")
    return f'<i class="nh-mk nh-mk-{m}"></i>'


def _prod_in(c: SceneCtx, sel: str, at: float, drift: bool = True) -> list[str]:
    tl = [f'tl.fromTo("#{c.sid} {sel}",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.55,ease:"power3.out"}},{c.t(at):.3f});']
    if drift:
        tl.append(f'tl.to("#{c.sid} {sel}",{{y:-10,duration:{max(0.6, c.duration - at - 0.8):.2f},ease:"sine.inOut"}},{c.t(at + 0.55):.3f});')
    return tl


# --- nh_hook ---------------------------------------------------------------------------------------------

def nh_hook(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "question", "badge"):
        _chk("nh_hook", k, d.get(k, ""), k, out)
    p = d.get("product") or {}
    pw, ph, (lcx, lcy) = _prod_size(p, _fit(p, 480, 380))
    px, py = 540 - pw // 2 - 110, zt + 290
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-q" style="top:{zt + 50}px">{_e(d.get("question", ""))}</div>
  <div class="nh-stagebox" id="{s}pb" style="left:{px}px;top:{py}px">{product_svg(f"{s}p", p, ph)}
    <div class="nh-ring" id="{s}ring" style="left:{lcx - 100:.0f}px;top:{lcy - 100:.0f}px"></div>
    <div class="nh-lensmini" id="{s}lm" style="left:{lcx + 10:.0f}px;top:{lcy - 140:.0f}px"></div></div>
  <div class="nh-badge" style="left:{px + pw + 70}px;top:{py + 120}px"><span>{_e(d.get("badge", ""))}</span></div>
  {_chip(c, d.get("chip") or {}, zt + 780, out, "nh_hook")}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl += _prod_in(c, f"#{s}pb", 0.1)
    qa = _rel(c, d.get("question_at", 0.25), 0.25, out)
    out.tl.append(_in(c, ".nh-q", qa, dy=24, dur=0.5))
    out.events += [c.t(0.1), c.t(qa)]
    if d.get("badge"):
        ba = _rel(c, d.get("badge_at", min(c.duration * 0.45, 3.0)), min(c.duration * 0.45, 3.0), out)
        out.tl.append(_pop(c, ".nh-badge span", ba, frm=0.5))
        out.events.append(c.t(ba))
    ra = _rel(c, d.get("ring_at", c.duration * 0.62), c.duration * 0.62, out)
    out.tl.append(f'tl.fromTo("#{s}ring",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{c.t(ra):.3f});')
    la = _rel(c, d.get("lens_at", c.duration * 0.8), c.duration * 0.8, out)
    out.tl.append(f'tl.fromTo("#{s}lm",{{opacity:0,x:120,y:-60}},{{opacity:1,x:0,y:0,duration:0.55,ease:"power3.out"}},{c.t(la):.3f});')
    out.events += [c.t(ra), c.t(la)]
    ch = d.get("chip") or {}
    if ch:
        at = _rel(c, ch.get("at", 1.5), 1.5, out)
        out.tl.append(_in(c, ".nh-chipline", at, dy=14))
        out.events.append(c.t(at))
    return out


# --- nh_facts --------------------------------------------------------------------------------------------

def nh_facts(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline", "zoom"):
        _chk("nh_facts", k, d.get(k, ""), k, out)
    doc = d.get("doc") or {}
    _chk("nh_facts", "act", doc.get("act", ""), "doc.act", out)
    _chk("nh_facts", "ref", doc.get("ref", ""), "doc.ref", out)
    rows = list(d.get("rows", []))[:4]
    p = d.get("product") or {}
    flip = bool(d.get("flip"))
    pw, ph, _ = _prod_size(p, _fit(p, 300, 300))
    r = 150
    prod_x = R - pw if flip else X0 + 10
    lens_cx = X0 + r + 20 if flip else R - r - 10
    lens_cy = zt + 190 + r
    zoom = str(d.get("zoom", ""))
    zf = max(34, min(96, int(250 / max(1, len(zoom)) * 1.7)))
    pitch = 104 if len(rows) <= 3 else 90
    top0 = zt + 510
    rh = []
    for i, rw in enumerate(rows):
        _chk("nh_facts", "text", rw.get("text", ""), f"rows[{i}].text", out)
        _chk("nh_facts", "value", rw.get("value", ""), f"rows[{i}].value", out)
        val = f'<b class="nh-fval">{_e(rw["value"])}</b>' if rw.get("value") else ""
        rh.append(f'<div class="nh-frow" id="{s}r{i}" style="top:{top0 + i * pitch}px">{_mk2(rw.get("mark", "fact"))}<span>{_e(rw.get("text", ""))}</span>{val}</div>')
    src = " · ".join(x for x in (doc.get("act", ""), doc.get("ref", "")) if x)
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-stagebox" id="{s}pb" style="left:{prod_x}px;top:{zt + 190}px">{product_svg(f"{s}p", p, ph)}</div>
  <div class="nh-lens nh-lens-sm" id="{s}lens" style="left:{lens_cx - r}px;top:{lens_cy - r}px;width:{2 * r}px;height:{2 * r}px">
    <div class="nh-lens-a"><span style="font-size:{zf}px">{_e(zoom)}</span></div></div>
  {"".join(rh)}
  {f'<div class="nh-chipline" style="top:{zt + 132}px"><span class="nh-chip">{_mark("fakt")}<b>{_e(MARK_WORDS.get(c.lang, MARK_WORDS["de"])["fakt"])}</b><span>{_e(src)}</span></span></div>' if src else ""}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl += _prod_in(c, f"#{s}pb", 0.2)
    out.tl.append(f'tl.fromTo("#{s}lens",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.6)"}},{c.t(0.55):.3f});')
    out.tl.append(f'tl.fromTo("#{s}lens .nh-lens-a span",{{scale:0.75}},{{scale:1,duration:1.6,ease:"sine.out"}},{c.t(0.55):.3f});')
    out.events += [c.t(0.15), c.t(0.55)]
    ats = _auto_at(c, [x.get("text", "") for x in rows], [x.get("at") for x in rows], lo=1.0)
    for i, at in enumerate(ats):
        out.tl.append(_in(c, f"#{s}r{i}", at, dx=-24, dy=0))
        out.events.append(c.t(at))
    if src:
        out.tl.append(_in(c, ".nh-chipline", min(1.4, c.duration * 0.3), dy=14))
    return out


# --- nh_list ---------------------------------------------------------------------------------------------

def nh_list(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline", "caption"):
        _chk("nh_list", k, d.get(k, ""), k, out)
    rows = list(d.get("rows", []))[:6]
    p = d.get("product") or {}
    pw, ph, _ = _prod_size(p, _fit(p, 500, 220))
    pitch = 96 if len(rows) <= 5 else 84
    x0 = X0 + pw + 40
    rh = []
    for i, rw in enumerate(rows):
        _chk("nh_list", "label", rw.get("label", ""), f"rows[{i}].label", out)
        _chk("nh_list", "value", rw.get("value", ""), f"rows[{i}].value", out)
        rh.append(f'<div class="nh-lrow" id="{s}r{i}" style="left:{x0}px;width:{R - x0}px;top:{zt + 210 + i * pitch}px">'
                  f'<span class="nh-lrow-l">{_e(rw.get("label", ""))}</span><b>{_e(rw.get("value", ""))}</b></div>')
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-stagebox" id="{s}pb" style="left:{X0}px;top:{zt + 210}px">{product_svg(f"{s}p", p, ph)}</div>
  {"".join(rh)}
  <div class="nh-schema" style="top:{zt + 760}px">{_mark("fakt")}<span>{_e(d.get("caption", ""))}</span></div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl += _prod_in(c, f"#{s}pb", 0.2)
    out.events.append(c.t(0.15))
    ats = _auto_at(c, [x.get("label", "") for x in rows], [x.get("at") for x in rows], lo=0.8)
    for i, at in enumerate(ats):
        out.tl.append(f'tl.fromTo("#{s}r{i}",{{opacity:0,x:-140}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{c.t(at):.3f});')
        out.events.append(c.t(at))
    if d.get("caption"):
        out.tl.append(_in(c, ".nh-schema", 0.9, dy=8))
    return out


# --- nh_versus -------------------------------------------------------------------------------------------

def nh_versus(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline"):
        _chk("nh_versus", k, d.get(k, ""), k, out)
    base = d.get("product") or {}
    gap = 22
    cw = (W - gap) // 2
    cards, texts, givens, ids = [], [], [], []
    for j, side in enumerate(("left", "right")):
        sd = d.get(side) or {}
        for k in ("tag", "title"):
            _chk("nh_versus", k, sd.get(k, ""), f"{side}.{k}", out)
        p = sd.get("product") or {k2: v for k2, v in base.items() if k2 in ("kind",)}
        pw, ph, _ = _prod_size(p, _fit(p, 200, 260))
        rows = list(sd.get("rows", []))[:3]
        rh = []
        for i, rw in enumerate(rows):
            _chk("nh_versus", "text", rw.get("text", ""), f"{side}.rows[{i}].text", out)
            rh.append(f'<div class="nh-vrow" id="{s}{side[0]}{i}">{_mk2(rw.get("mark", "fact"))}<span>{_e(rw.get("text", ""))}</span></div>')
            texts.append(rw.get("text", "")); givens.append(rw.get("at")); ids.append(f"#{s}{side[0]}{i}")
        cards.append(f"""<div class="nh-vcard" id="{s}{side}" style="left:{X0 + j * (cw + gap)}px;width:{cw}px;top:{zt + 150}px">
    <div class="nh-vprod" style="height:{ph}px">{product_svg(f"{s}{side}p", p, ph)}</div>
    <div class="nh-vtag"><span>{_e(sd.get("tag", ""))}</span></div>
    <div class="nh-vtitle">{_e(sd.get("title", ""))}</div>{"".join(rh)}</div>""")
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  {"".join(cards)}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl.append(_in(c, f"#{s}left", 0.3, dy=40))
    out.events.append(c.t(0.15))
    ats = _auto_at(c, texts, givens, lo=0.9)
    nl = len((d.get("left") or {}).get("rows", [])[:3])
    right_at = ats[nl] - 0.5 if len(ats) > nl else c.duration * 0.5
    out.tl.append(_in(c, f"#{s}right", max(0.6, right_at), dy=40))
    out.events.append(c.t(max(0.6, right_at)))
    for sel, at in zip(ids, ats):
        out.tl.append(_in(c, sel, at, dx=-16, dy=0))
        out.events.append(c.t(at))
    return out


# --- nh_time ---------------------------------------------------------------------------------------------

def nh_time(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline"):
        _chk("nh_time", k, d.get(k, ""), k, out)
    nodes = list(d.get("nodes", []))[:4]
    p = d.get("product") or {}
    pw, ph, _ = _prod_size(p, _fit(p, 300, 240))
    pitch = 170 if len(nodes) <= 3 else 140
    nh = []
    for i, n in enumerate(nodes):
        _chk("nh_time", "date", n.get("date", ""), f"nodes[{i}].date", out)
        _chk("nh_time", "text", n.get("text", ""), f"nodes[{i}].text", out)
        nh.append(f'<div class="nh-tnode" id="{s}n{i}" style="top:{zt + 190 + i * pitch}px"><i class="nh-tdot"></i>'
                  f'<div class="nh-tdate">{_e(n.get("date", ""))}</div><div class="nh-ttext">{_e(n.get("text", ""))}</div></div>')
    rail_h = max(60, (len(nodes) - 1) * pitch + 40)
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-trail" style="top:{zt + 210}px;height:{rail_h}px"><i id="{s}rail"></i></div>
  {"".join(nh)}
  <div class="nh-stagebox" id="{s}pb" style="left:{R - pw}px;top:{zt + 790 - ph}px">{product_svg(f"{s}p", p, ph)}</div>
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl += _prod_in(c, f"#{s}pb", 0.3)
    out.events.append(c.t(0.15))
    ats = _auto_at(c, [f'{n.get("date", "")} {n.get("text", "")}' for n in nodes], [n.get("at") for n in nodes], lo=0.8)
    if ats:
        out.tl.append(f'tl.fromTo("#{s}rail",{{scaleY:0}},{{scaleY:1,duration:{max(0.6, ats[-1] - ats[0] + 0.4):.2f},ease:"none"}},{c.t(ats[0]):.3f});')
    for i, at in enumerate(ats):
        out.tl.append(_in(c, f"#{s}n{i}", at, dx=-20, dy=0))
        out.events.append(c.t(at))
    return out


# --- nh_steps --------------------------------------------------------------------------------------------

def nh_steps(c: SceneCtx, d: dict) -> SceneOut:
    out = SceneOut(html="")
    s, zt = c.sid, c.zone_top
    for k in ("kicker", "headline"):
        _chk("nh_steps", k, d.get(k, ""), k, out)
    items = list(d.get("items", []))[:4]
    p = d.get("product") or {}
    pw, ph, _ = _prod_size(p, _fit(p, 250, 200))
    pitch = 160 if len(items) <= 3 else 130
    ih = []
    for i, it in enumerate(items):
        _chk("nh_steps", "title", it.get("title", ""), f"items[{i}].title", out)
        _chk("nh_steps", "sub", it.get("sub", ""), f"items[{i}].sub", out)
        ih.append(f'<div class="nh-step" id="{s}st{i}" style="top:{zt + 300 + i * pitch}px"><span class="nh-step-ico">{_ico2(it.get("icon", "check"))}</span>'
                  f'<div><div class="nh-step-title">{_e(it.get("title", ""))}</div><div class="nh-step-sub">{_e(it.get("sub", ""))}</div></div></div>')
    out.html = f"""<div class="nh-in">
  {_kicker(d.get("kicker", ""), zt)}
  <div class="nh-h2" style="top:{zt + 48}px;width:{W - pw - 30}px">{_e(d.get("headline", ""))}</div>
  <div class="nh-stagebox" id="{s}pb" style="left:{R - pw}px;top:{zt + 20}px">{product_svg(f"{s}p", p, ph)}</div>
  {"".join(ih)}
</div>"""
    out.tl += _frame(c)
    out.tl.append(_in(c, ".nh-kicker", 0.05, dx=-20, dy=0))
    out.tl.append(_in(c, ".nh-h2", 0.15))
    out.tl += _prod_in(c, f"#{s}pb", 0.2)
    out.events.append(c.t(0.15))
    ats = _auto_at(c, [f'{x.get("title", "")} {x.get("sub", "")}' for x in items], [x.get("at") for x in items], lo=0.9)
    for i, at in enumerate(ats):
        out.tl.append(_in(c, f"#{s}st{i}", at, dx=-24, dy=0))
        out.tl.append(_pop(c, f"#{s}st{i} .nh-step-ico", at + 0.1, frm=0.5))
        out.events.append(c.t(at))
    return out


TEMPLATES.update({"nh_hook": nh_hook, "nh_facts": nh_facts, "nh_list": nh_list, "nh_versus": nh_versus,
                  "nh_time": nh_time, "nh_steps": nh_steps})
_css_pilot = CSS


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: N802,F811
    acc, txt, mut = pal.get("accent", "#9B5560"), pal.get("text", "#4A2F34"), pal.get("muted", "#7E6468")
    surf, hair = pal.get("surface", "#FFFCF9"), pal.get("hairline", "#E8D9D4")
    amber, red, green = pal.get("signal_amber", "#946420"), pal.get("signal_red", "#8E2F45"), pal.get("signal_green", "#4F7A62")
    shadow = "rgba(74,47,52,0.14)"
    D, B = f"'FN {display}'", f"'FN {body}'"
    return _css_pilot(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
.nh-q{{position:absolute;left:{X0}px;width:{W}px;font-family:{D};font-weight:500;font-size:76px;line-height:1.1;color:{txt};}}
.nh-badge{{position:absolute;}}
.nh-badge span{{display:inline-block;font-family:{B};font-weight:600;font-size:36px;color:{amber};border:3px solid {amber};border-radius:999px;padding:10px 28px;background:{surf};white-space:nowrap;}}
.nh-lens-sm{{border-width:12px;}}
.nh-frow{{position:absolute;left:{X0}px;width:{W}px;display:flex;align-items:center;gap:18px;font-family:{B};font-size:36px;line-height:1.22;color:{txt};}}
.nh-frow .nh-mk{{width:20px;height:20px;}}
.nh-frow span{{flex:1;}}
.nh-fval{{font-family:{D};font-weight:600;font-size:52px;color:{acc};}}
.nh-mk-luecke{{background:transparent;border:3px dashed {red};border-radius:50%;box-sizing:border-box;}}
.nh-mk-ok{{background:{green};}}
.nh-mk-auslegung{{background:#7A5AC8;}}
.nh-lrow{{position:absolute;height:78px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 24px;box-sizing:border-box;
  background:{surf};border:2px solid {hair};border-radius:16px;box-shadow:0 10px 24px {shadow};}}
.nh-lrow-l{{font-family:{B};font-weight:500;font-size:32px;color:{txt};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.nh-lrow b{{font-family:{B};font-weight:600;font-size:28px;color:{acc};white-space:nowrap;}}
.nh-vcard{{position:absolute;min-height:470px;background:{surf};border:2px solid {hair};border-radius:22px;padding:22px 24px;box-sizing:border-box;box-shadow:0 14px 34px {shadow};}}
.nh-vprod{{display:flex;justify-content:center;}}
.nh-vtag{{margin-top:14px;display:flex;}}
.nh-vtag span{{font-family:{B};font-weight:600;font-size:24px;letter-spacing:0.06em;text-transform:uppercase;color:{txt};border:2px solid {hair};border-radius:999px;padding:4px 14px;}}
.nh-vtitle{{margin-top:12px;font-family:{D};font-weight:500;font-size:40px;line-height:1.12;color:{txt};hyphens:manual;}}
.nh-vrow{{margin-top:14px;display:flex;align-items:flex-start;gap:12px;font-family:{B};font-size:28px;line-height:1.25;color:{txt};}}
.nh-vrow .nh-mk{{margin-top:7px;}}
.nh-trail{{position:absolute;left:{X0 + 12}px;width:4px;background:{hair};}}
.nh-trail i{{display:block;width:100%;height:100%;background:{acc};transform-origin:top center;}}
.nh-tnode{{position:absolute;left:{X0}px;width:{W - 200}px;padding-left:64px;box-sizing:border-box;}}
.nh-tdot{{position:absolute;left:0;top:10px;width:28px;height:28px;border-radius:50%;background:{surf};border:5px solid {acc};box-sizing:border-box;}}
.nh-tdate{{font-family:{D};font-weight:600;font-size:46px;line-height:1.05;color:{acc};}}
.nh-ttext{{margin-top:6px;font-family:{B};font-size:32px;line-height:1.25;color:{txt};}}
"""


# --- keep-alive: a calm product nudge wherever a general scene would stand still longer than GAP seconds -----

GAP = 5.0


def _keepalive(c: SceneCtx, out: SceneOut, targets: list[str]) -> SceneOut:
    ev = sorted([c.start] + [e for e in out.events if c.start <= e <= c.end] + [c.end])
    k = 0
    for a, b in zip(ev, ev[1:]):
        n = int((b - a) // GAP)
        for j in range(1, n + 1):
            t = a + (b - a) * j / (n + 1)
            if t > c.end - 0.8:
                continue
            sel = targets[k % len(targets)]
            k += 1
            out.tl.append(f'tl.to("#{c.sid} {sel}",{{rotation:-4,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:1}},{t:.3f});')
            out.events.append(round(t, 3))
    return out


def _wrap(fn, targets):
    def run(c: SceneCtx, d: dict) -> SceneOut:
        return _keepalive(c, fn(c, d), [t.format(s=c.sid) for t in targets])
    run.__name__ = fn.__name__
    return run


TEMPLATES.update({
    "nh_hook": _wrap(nh_hook, ["#{s}pb", ".nh-badge span"]),
    "nh_facts": _wrap(nh_facts, ["#{s}pb", "#{s}lens"]),
    "nh_list": _wrap(nh_list, ["#{s}pb"]),
    "nh_versus": _wrap(nh_versus, ["#{s}left .nh-vprod svg", "#{s}right .nh-vprod svg"]),
    "nh_time": _wrap(nh_time, ["#{s}pb"]),
    "nh_steps": _wrap(nh_steps, ["#{s}pb"]),
    "nh_close": _wrap(nh_close, ["#{s}tb"]),
})


# =========================================================================================================
# Real pictures (Neustart 03.11.2026): Higgsfield stills and Kling clips as full-bleed background per beat section,
# slow camera move, cross-fades, an ivory veil top and bottom for readability and the tag "KI-Bild" /
# "KI-Bild · Veranschaulichung". Plan: layout.media = [{beat, at (0..1 of the beat), file, kind image|video,
# move in|out|left|right|up|down, tag ki|hand}], layout.stamp (optional text of the top stamp).
# Scenes with data.photo = true hide their drawn products (tube, spoons, body, arm) and put panels behind free text.
# =========================================================================================================

import shutil as _shutil

MEDIA_DIR = Path(__file__).resolve().parents[1] / "assets" / "higgsfield"
TAGS = {"de": {"ki": "KI-Bild", "hand": "KI-Bild · Veranschaulichung"}, "en": {"ki": "AI image", "hand": "AI image · illustration"}}
MOVES = {"in": ((1.04, 0, 0), (1.14, 0, -20)), "out": ((1.16, 0, -20), (1.04, 0, 0)), "left": ((1.12, 50, 0), (1.12, -50, 0)),
         "right": ((1.12, -50, 0), (1.12, 50, 0)), "up": ((1.12, 0, 50), (1.12, 0, -50)), "down": ((1.12, 0, -50), (1.12, 0, 50))}


def _media_file(name: str, project_dir) -> str:
    """Copy one picture or clip into the project (stills scaled to 1200 px width as JPEG) and return its src."""
    src = MEDIA_DIR / name
    out = Path(project_dir) / "assets" / "dlm"
    out.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        dst = out / (src.stem + ".jpg")
        if not dst.exists():
            from PIL import Image
            im = Image.open(src).convert("RGB")
            w = 1200
            im = im.resize((w, round(im.height * w / im.width)))
            im.save(dst, quality=88)
        return f"assets/dlm/{dst.name}"
    dst = out / src.name
    if not dst.exists():
        _shutil.copy2(src, dst)
    return f"assets/dlm/{dst.name}"


def _media_layer(plan, project_dir, lang: str) -> dict:
    lay = getattr(plan, "layout", None) or {}
    media = lay.get("media") or []
    beats = {b.id: b for b in plan.beats if b.start is not None}
    total = max([b.start + b.duration for b in beats.values()] + [1.0]) + float(lay.get("tail_seconds", 2.4))
    segs = []
    for m in media:
        b = beats.get(m.get("beat"))
        if not b:
            continue
        segs.append(dict(m, t0=b.start + float(m.get("at", 0)) * b.duration))
    segs.sort(key=lambda x: x["t0"])
    imgs, vids, tags, tl, events, probs = [], [], [], [], [], []
    for i, sg in enumerate(segs):
        t0 = sg["t0"]
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        if not (MEDIA_DIR / sg["file"]).exists():
            probs.append(f"media file {sg['file']} missing")
            continue
        src = _media_file(sg["file"], project_dir)
        (s0, x0, y0), (s1, x1, y1) = MOVES.get(sg.get("move", "in"), MOVES["in"])
        fade_in = 0.0 if i == 0 else 0.45
        if sg.get("kind") == "video":
            d = t1 - t0 + 0.45
            vids.append(f'<video id="nhmv{i}" class="clip nhmv" src="{html.escape(src)}" data-start="{max(0.0, t0 - fade_in):.3f}" '
                        f'data-duration="{d:.3f}" data-track-index="0" data-volume="0" muted playsinline></video>')
            sel = f"#nhmv{i}"
        else:
            imgs.append(f'<img id="nhmi{i}" class="nhmi" src="{html.escape(src)}" alt="">')
            sel = f"#nhmi{i}"
        tl.append(f'tl.to("{sel}",{{opacity:1,duration:{max(0.01, fade_in):.2f},ease:"power1.inOut"}},{max(0.0, t0 - fade_in):.3f});')
        tl.append(f'tl.fromTo("{sel}",{{scale:{s0},x:{x0},y:{y0}}},{{scale:{s1},x:{x1},y:{y1},duration:{max(0.5, t1 - t0 + 0.45):.2f},ease:"none"}},{max(0.0, t0 - fade_in):.3f});')
        if i + 1 < len(segs):
            tl.append(f'tl.to("{sel}",{{opacity:0,duration:0.45,ease:"power1.inOut"}},{t1:.3f});')
        tag = TAGS.get(lang, TAGS["de"]).get(sg.get("tag", "ki"), "")
        tags.append(f'<span id="nhmt{i}" class="nhmt">{html.escape(tag)}</span>')
        tl.append(f'tl.to("#nhmt{i}",{{opacity:1,duration:0.2}},{t0:.3f});')
        if i + 1 < len(segs):
            tl.append(f'tl.to("#nhmt{i}",{{opacity:0,duration:0.15}},{max(t0 + 0.3, t1 - 0.5):.3f});')
        events.append(round(t0, 3))
    if not segs:
        return {}
    under = (f'<div id="nhm">{"".join(imgs)}</div>{"".join(vids)}'
             '<div id="nhm-veil"></div>'
             f'<div id="nhm-tags">{"".join(tags)}</div>')
    css = ("<style>#nhm{position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none;}"
           ".nhmi,.nhmv{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:0;opacity:0;}"
           "#nhm-veil{position:absolute;inset:0;z-index:0;pointer-events:none;background:linear-gradient(180deg,"
           "rgba(248,243,239,0.94) 0px,rgba(248,243,239,0.86) 300px,rgba(248,243,239,0.0) 500px,rgba(248,243,239,0.0) 1120px,"
           "rgba(248,243,239,0.88) 1290px,rgba(248,243,239,0.94) 1920px);}"
           "#nhm-tags{position:absolute;left:108px;width:822px;top:246px;height:44px;z-index:21;pointer-events:none;}"
           ".nhmt{position:absolute;right:0;top:0;font-family:'FN Inter';font-weight:600;font-size:26px;color:#4A2F34;"
           "background:rgba(255,252,249,0.92);border:2px solid #E8D9D4;border-radius:999px;padding:4px 16px;white-space:nowrap;opacity:0;}</style>")
    return {"head_html": css, "under_scenes_html": under, "tl": tl, "events": events, "problems": probs}


_layer_studio = LAYER


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: N802,F811
    out = _layer_studio(plan, brand, project_dir, captions)
    lay = getattr(plan, "layout", None) or {}
    lang = getattr(plan, "language", "de")
    if lay.get("stamp"):
        out["under_scenes_html"] = out["under_scenes_html"].replace(html.escape(STAMP.get(lang, STAMP["de"])), html.escape(lay["stamp"]))
    m = _media_layer(plan, project_dir, lang)
    if m:
        out["head_html"] = out.get("head_html", "") + m["head_html"]
        out["under_scenes_html"] = out["under_scenes_html"] + m["under_scenes_html"]
        js = "".join(x.replace("tl.", "t.", 1) for x in m["tl"])
        out["body_end_html"] = out.get("body_end_html", "") + (
            "<script>(function(){var t=window.__timelines&&window.__timelines.main;if(!t)return;" + js + "t.seek(0);})();</script>")
        out["events"] = list(out.get("events", [])) + m["events"]
        out["problems"] = list(out.get("problems", [])) + m["problems"]
    return out


def _photo(fn):
    def run(c: SceneCtx, d: dict) -> SceneOut:
        o = fn(c, d)
        if d.get("photo"):
            o.html = o.html.replace('<div class="nh-in', '<div class="nh-photo nh-in', 1)
        return o
    run.__name__ = fn.__name__
    return run


for _k in list(TEMPLATES):
    TEMPLATES[_k] = _photo(TEMPLATES[_k])

_css_general = CSS


def CSS(pal, display, display_w, body, mono, zone_top=290, zone_h=810, flat=True):  # noqa: N802,F811
    panel = "background:rgba(255,252,249,0.9);border-radius:20px;box-shadow:0 10px 30px rgba(74,47,52,0.16);"
    return _css_general(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
.nh-photo .nh-stagebox,.nh-photo .nh-spoonbox,.nh-photo .nh-body,.nh-photo .nh-arm,.nh-photo .nh-link,.nh-photo .nh-ring,.nh-photo .nh-lensmini{{display:none;}}
.nh-photo .nh-count{{left:{X0 - 20}px;width:560px;padding:8px 28px 14px 20px;box-sizing:border-box;{panel}}}
.nh-photo .nh-sub{{width:auto;padding:4px 18px;left:{X0 - 8}px;{panel}}}
.nh-photo .nh-value{{width:auto;padding:4px 22px;{panel}}}
.nh-photo .nh-total,.nh-photo .nh-spoonrow,.nh-photo .nh-finding{{padding:8px 20px;box-sizing:border-box;{panel}}}
.nh-photo .nh-step{{width:auto;padding:10px 26px 10px 12px;{panel}}}
.nh-photo .nh-sign{{width:auto;left:{X0 + 120}px;right:{1080 - (X0 + 822) + 120}px;padding:28px 20px;{panel}}}
.nh-photo .nh-ask span{{box-shadow:0 10px 30px rgba(74,47,52,0.16);}}
.nh-photo .nh-frow{{width:auto;max-width:560px;padding:10px 22px;box-sizing:border-box;{panel}}}
.nh-photo .nh-tnode{{width:auto;max-width:620px;padding:12px 24px 12px 64px;{panel}}}
.nh-photo .nh-tdot{{left:22px;top:20px;}}
.nh-photo .nh-trail{{display:none;}}
.nh-photo .nh-schema{{width:auto;padding:8px 20px;{panel}}}
.nh-photo .nh-vrow{{max-width:none;}}
.nh-photo .nh-ask{{margin-top:70px;}}
.nh-photo .nh-sub{{margin-top:52px;}}
.nh-photo .nh-count{{height:196px;align-items:flex-end;}}
"""
