"""Frontlore format "Rekonstruktion" (02.11.2026): scene types fr_*, see OneDrive\\Business\\02 Marke\\Frontlore\\Format-Bibel.md.

One historical technical problem per video, reconstructed from the sources: the task, the means of the time, the
solution of the engineers of the time as a line model, the procedure, a test case taken from the source, the stages
and the finding (what survives, what is disputed). The picture shows the problem and the solution, never combat.

Line grammar (the one rule every drawing follows):
- solid line   = described in the source (a passage is cited in the scene)
- dashed line  = reconstruction or simplification by Frontlore (shape, proportions, layout)
- hatched area = not preserved, not sendable, not known

Persistent elements:
- time ruler at the top (LAYER, `layout.ruler`): centuries, bars with hatched ends where dates are uncertain,
  marks for secure dates; items appear at the beat named in `beat`
- passage kicker above every headline (`cite_head`, e.g. "POLYB. X 45,6-7")
- verdict chip and source line at the bottom of every scene (`status`, `cite`), y 1176 / 1210 (+32 for a second line)

The brand module (frontlore_scenes.py) injects its namespace as `FL` before this file runs, so word anchors ("w:Wort")
resolve exactly as in the old scene types. Plans with the old types render unchanged.

Scene types: fr_task (hook), fr_means, fr_solution, fr_protocol, fr_example, fr_stages, fr_finding, and the generic
fr_model (line model, dimensions, counters, repeated modules and stamps from plan data, `_items`; fr_task takes `items` too).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from fn.render.templates import SceneOut

X0, X1 = 108, 920               # x >= 930 stays free for platform icons
KICK_Y, HEAD_Y = 326, 396
CHIP_Y, CITE_Y = 1176, 1210     # cite wraps to a second line at y 1242 (zone ends at 1250, zone_lower_right_px 920); captions start at about y 1300 (caption_bottom_px 500)
CITE_CHARS = 46                  # 28 px mono on 812 px
GREEK = ["ΑΒΓΔΕ", "ΖΗΘΙΚ", "ΛΜΝΞΟ", "ΠΡΣΤΥ", "ΦΧΨΩ"]   # Polybios X 45,7: five groups, the last one letter short
FLAME = "M0,0 C-15,-16 -9,-34 0,-54 C9,-34 15,-16 0,0 Z"
FLAME_IN = "M0,-2 C-7,-10 -4,-22 0,-32 C4,-22 7,-10 0,-2 Z"

LIMITS = {
    "fr_task": {"question": 64, "cite": 80, "line": 22, "label": 46},
    "fr_means": {"headline": 34, "cite": 80, "title": 26, "item": 26, "stamp": 18},
    "fr_solution": {"headline": 34, "cite": 80, "note": 46, "label": 24},
    "fr_protocol": {"headline": 34, "cite": 80, "row": 30, "lane": 14},
    "fr_example": {"headline": 34, "cite": 80, "label": 18, "note": 40},
    "fr_stages": {"headline": 34, "cite": 80, "title": 30, "sub": 40, "chip": 22, "stamp": 26},
    "fr_finding": {"headline": 34, "cite": 80, "key": 12, "value": 34, "brand": 46},
    "fr_model": {"headline": 34, "cite": 80, "label": 46},
}


# --- small helpers -----------------------------------------------------------------------------------

def _e(s) -> str:
    return FL._e(s)  # noqa: F821  (FL is injected by the brand module)


def js(d: dict) -> str:
    return json.dumps(d, separators=(",", ":"), ensure_ascii=False)


def ft(sel: str, a: dict, b: dict, at: float) -> str:
    return f'tl.fromTo("{sel}",{js(a)},{js(b)},{at:.3f});'


def show(sel: str, at: float, dur: float = 0.35, y: float = 0) -> str:
    return ft(sel, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0, "duration": dur, "ease": "power2.out"}, at)


def draw(sel: str, at: float, dur: float = 0.9) -> list[str]:
    """Solid source lines draw themselves (pathLength 1); the group becomes visible at the same moment."""
    return [f'tl.set("{sel}",{{opacity:1}},{at:.3f});',
            ft(f"{sel} .fr-d", {"strokeDashoffset": 1}, {"strokeDashoffset": 0, "duration": dur, "ease": "power1.inOut",
                                                          "stagger": {"amount": dur * 0.5}}, at)]


def rect_d(x: float, y: float, w: float, h: float) -> str:
    return f"M{x},{y} H{x + w} V{y + h} H{x} Z"


def _k(c) -> dict:
    p = c.pal
    return {"bg": p.get("bg", "#29352D"), "surface": p.get("surface", "#38433C"), "accent": p.get("accent", "#A9B29F"),
            "text": p.get("text", "#E6E9E5"), "muted": p.get("muted", "#B0B7AC"), "paper": p.get("paper", "#E9E4D4"),
            "ink": p.get("paper_ink", "#1F2620"), "stamp": p.get("stamp", "#2B4257"), "fire": p.get("signal_amber", "#D9B45A"),
            "water": "#6F8FA3"}


class _Scene:
    """Collects svg, timeline, events and problems of one scene; `at` resolves numbers and word anchors."""

    def __init__(self, c, d: dict, kind: str):
        self.c, self.d, self.kind = c, d, kind
        self.k = _k(c)
        self.svg: list[str] = []
        self.tl: list[str] = []
        self.ev: list[float] = [c.start]
        self.P: list[str] = []
        self.de = c.lang == "de"

    def at(self, key: str, default: float = 0.0) -> float:
        """Absolute time of the data field `key` (seconds from the beat start or word anchor "w:Wort")."""
        return self.atv(self.d.get(key), default)

    def atv(self, v, default: float = 0.0) -> float:
        """Absolute time of a value (number, word anchor or None for the default)."""
        return self.c.t(FL._at(self.c, v, default, self.P))  # noqa: F821

    def mark(self, t: float) -> float:
        self.ev.append(t)
        return t

    def check(self, field: str, text: str) -> None:
        lim = LIMITS.get(self.kind, {}).get(field)
        if lim and len(str(text)) > lim:
            self.P.append(f"{self.kind}.{field}: {len(str(text))} chars > {lim}")

    # chrome: passage kicker + headline, verdict chip + source line
    def head(self) -> None:
        d = self.d
        kick, head = d.get("cite_head", ""), d.get("headline", "")
        self.check("headline", head)
        if kick:
            self.svg.append(f'<text class="fr-kick" x="{X0}" y="{KICK_Y}">{_e(kick)}</text>')
        if head:
            self.svg.append(f'<text class="fr-head" x="{X0}" y="{HEAD_Y}">{_e(head)}</text>'
                            f'<path d="M{X0},{HEAD_Y + 22} H{X1}" class="fr-rule"/>')

    def foot(self) -> None:
        d, k, s = self.d, self.k, self.c.sid
        cite = d.get("cite", "")
        self.check("cite", cite)
        chips = d.get("status") or []
        x = X0
        out = []
        for i, ch in enumerate(chips):
            kind, text = ch.get("kind", "belegt"), ch.get("text", "")
            if kind == "belegt":
                icon = f'<rect x="{x}" y="{CHIP_Y - 20}" width="22" height="22" fill="{k["accent"]}"/>'
            elif kind == "rekonstruiert":
                icon = f'<rect x="{x + 1.5}" y="{CHIP_Y - 18.5}" width="19" height="19" fill="none" stroke="{k["accent"]}" stroke-width="3" stroke-dasharray="5 4"/>'
            elif kind == "umstritten":
                icon = f'<rect x="{x}" y="{CHIP_Y - 20}" width="22" height="22" fill="url(#{s}-hatch)" stroke="{k["fire"]}" stroke-width="2"/>'
            else:  # auslegung
                icon = f'<path d="M{x + 11},{CHIP_Y - 22} L{x + 23},{CHIP_Y - 9} L{x + 11},{CHIP_Y + 4} L{x - 1},{CHIP_Y - 9} Z" fill="#B49CE6"/>'
            w = 40 + 17.2 * len(text)
            out.append(f'<g id="{s}-chip{i}" opacity="0">{icon}<text class="fr-chip" x="{x + 34}" y="{CHIP_Y}">{_e(text)}</text></g>')
            self.tl.append(show(f"#{s}-chip{i}", self.atv(ch.get("at"), 0.2), 0.3))
            x += w + 28
        if cite:
            pre = "Quelle: " if self.de else "Source: "
            parts = cite.split(" · ")
            lines, cur = [], pre + parts[0]
            for part in parts[1:]:                 # wrap at the dots, never inside a source
                nxt = cur + " · " + part
                if len(nxt) > CITE_CHARS:
                    lines.append(cur + " ·")
                    cur = part
                else:
                    cur = nxt
            lines.append(cur)
            if len(lines) > 2:
                self.P.append(f"{self.kind}.cite: {len(lines)} lines > 2")
            for j, ln in enumerate(lines[:2]):
                out.append(f'<text id="{s}-cite{j}" class="fr-cite" x="{X0}" y="{CITE_Y + 32 * j}">{_e(ln)}</text>')
        self.svg += out

    def out(self) -> SceneOut:
        c, k, s = self.c, self.k, self.c.sid
        defs = (f'<defs><pattern id="{s}-hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<rect width="12" height="12" style="fill:{k["surface"]};fill-opacity:0.6"/>'
                f'<line x1="0" y1="0" x2="0" y2="12" stroke="{k["fire"]}" stroke-opacity="0.75" stroke-width="3"/></pattern>'
                f'<pattern id="{s}-hatchp" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<line x1="0" y1="0" x2="0" y2="12" stroke="{k["ink"]}" stroke-opacity="0.55" stroke-width="3"/></pattern>'
                f'<marker id="{s}-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{k["accent"]}"/></marker></defs>')
        html_ = (f'<div class="scene-inner fr"><svg class="fr-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
                 f'{defs}{"".join(self.svg)}</svg></div>')
        tl = [ft(f"#{s} .fr-svg", {"opacity": 0}, {"opacity": 1, "duration": 0.25}, c.start)] + self.tl
        evs = FL._thin(sorted(set(round(e, 3) for e in self.ev if c.start - 1e-3 <= e <= c.end + 1e-3)))  # noqa: F821
        return SceneOut(html=html_, tl=tl, events=evs, problems=self.P)


# --- drawing parts -----------------------------------------------------------------------------------

def _flame(k: dict, x: float, y: float, s: float = 1.0, gid: str = "", hidden: bool = True) -> str:
    op = ' opacity="0"' if hidden else ""
    idattr = f' id="{gid}"' if gid else ""
    return (f'<g{idattr} class="fr-flame"{op} transform="translate({x},{y}) scale({s})">'
            f'<path d="{FLAME}" fill="{k["fire"]}"/><path d="{FLAME_IN}" fill="#F4E3B0"/></g>')


def _torch_row(sid: str, k: dict, name: str, x0: float, y: float, n: int, gap: float, s: float = 1.0) -> str:
    """n torch posts with an empty socket each (dashed circle) and a hidden flame `#<sid>-<name>f<i>`."""
    out = []
    for i in range(n):
        x = x0 + i * gap
        out.append(f'<path d="M{x},{y} V{y - 46 * s}" class="fr-src" stroke-width="{5 * s:.1f}"/>'
                   f'<circle cx="{x}" cy="{y - 50 * s}" r="{9 * s:.1f}" class="fr-rek" stroke-width="3"/>'
                   + _flame(k, x, y - 50 * s, 0.95 * s, f"{sid}-{name}f{i}"))
    return "".join(out)


def _light(tl: list[str], sid: str, name: str, n: int, at: float, step: float = 0.18) -> None:
    for i in range(n):
        tl.append(ft(f"#{sid}-{name}f{i}", {"opacity": 0, "scale": 0.3, "transformOrigin": "50% 100%"},
                     {"opacity": 1, "scale": 1, "duration": 0.25, "ease": "back.out(2)"}, at + i * step))


def _tablets(sid: str, k: dict, x0: float, y0: float, w: float, gap: float, row: float, head: float,
             font: int, name: str = "tab") -> str:
    """Five letter tablets (Polybios X 45,7); tablet 5 holds four letters and one hatched cell."""
    out = []
    for i, grp in enumerate(GREEK):
        x = x0 + i * (w + gap)
        h = head + 5 * row + 10
        out.append(f'<g id="{sid}-{name}{i}" opacity="0">'
                   f'<path d="{rect_d(x, y0, w, h)}" class="fr-src fr-d" pathLength="1" style="fill:{k["surface"]};fill-opacity:0.85"/>'
                   f'<path d="M{x},{y0 + head} H{x + w}" class="fr-src fr-d" pathLength="1" stroke-width="3"/>'
                   f'<text class="fr-tabno" x="{x + w / 2}" y="{y0 + head - 12}" text-anchor="middle">{i + 1}</text>')
        for r in range(5):
            cy = y0 + head + 6 + r * row
            if r < len(grp):
                out.append(f'<rect id="{sid}-{name}{i}c{r}" x="{x + 8}" y="{cy}" width="{w - 16}" height="{row - 6}" fill="{k["accent"]}" opacity="0"/>'
                           f'<text id="{sid}-{name}{i}l{r}" class="fr-gr" x="{x + w / 2}" y="{cy + row * 0.72}" text-anchor="middle" '
                           f'font-size="{font}" opacity="0">{grp[r]}</text>')
            else:
                out.append(f'<rect x="{x + 8}" y="{cy}" width="{w - 16}" height="{row - 6}" fill="url(#{sid}-hatch)" id="{sid}-{name}{i}x"/>')
        out.append("</g>")
    return "".join(out)


def _wall(sid: str, k: dict, x0: float, x1: float, y: float, h: float, gap: float, n: int = 5, s: float = 1.0) -> tuple[str, float, float]:
    """Signal wall: two screens (Polybios X 46,3: screens hide the torches), torch posts above each half.
    Shape and proportions are a reconstruction (dashed)."""
    half = (x1 - x0 - gap) / 2
    lx, rx = x0, x0 + half + gap
    pad = half / (n + 1)
    out = [f'<path d="{rect_d(lx, y, half, h)}" class="fr-rek" style="fill:{k["surface"]};fill-opacity:0.7"/>',
           f'<path d="{rect_d(rx, y, half, h)}" class="fr-rek" style="fill:{k["surface"]};fill-opacity:0.7"/>',
           _torch_row(sid, k, "L", lx + pad, y, n, pad, s), _torch_row(sid, k, "R", rx + pad, y, n, pad, s)]
    return "".join(out), lx + half / 2, rx + half / 2


# --- fr_task: the task (hook) ---------------------------------------------------------------------------

def fr_task(c, d: dict):
    S = _Scene(c, d, "fr_task")
    k, s = S.k, c.sid
    lines = d.get("question_lines") or [d.get("question", "")]
    S.check("question", " ".join(lines))
    em = d.get("question_em", "")
    for i, ln in enumerate(lines):
        S.check("line", ln)
        t = _e(ln)
        if em and em in ln:
            t = t.replace(_e(em), f'<tspan class="fr-em">{_e(em)}</tspan>', 1)
        S.svg.append(f'<text id="{s}-q{i}" class="fr-q" x="{X0}" y="{440 + i * 100}" opacity="0">{t}</text>')
        S.tl.append(show(f"#{s}-q{i}", S.mark(S.at("question_at", 0.05) + 0.45 * i), 0.4, 24))
    if d.get("items"):                       # a plan-defined model instead of the landscape (other topics)
        _items(S, d["items"])
        S.foot()
        return S.out()
    # landscape section: two hills, a station on each (schematic, dashed), distance bracket, fire, empty sentence
    ground = 985
    S.svg.append(f'<g id="{s}-land" opacity="0">'
                 f'<path class="fr-src fr-d" pathLength="1" d="M{X0},{ground} C200,{ground} 230,820 300,820 C370,820 400,{ground} 520,{ground} '
                 f'C640,{ground} 700,{ground} 760,{ground} C800,{ground} 830,800 880,800 C910,800 920,850 {X1},880"/>'
                 f'<path class="fr-rek" d="{rect_d(282, 770, 36, 50)}"/><path class="fr-rek" d="{rect_d(862, 750, 36, 50)}"/>'
                 f'<text class="fr-lab" x="300" y="{ground + 44}" text-anchor="middle">{_e(d.get("from", "SENDER"))}</text>'
                 f'<text class="fr-lab" x="{X1}" y="{ground + 44}" text-anchor="end">{_e(d.get("to", "EMPFÄNGER"))}</text>'
                 f'</g>')
    S.tl += draw(f"#{s}-land", S.mark(S.at("land_at", 1.0)), 1.0)
    S.svg.append(f'<g id="{s}-dist" opacity="0"><path class="fr-src" d="M318,690 H862 M318,674 V706 M862,674 V706" stroke-width="3"/>'
                 f'<text class="fr-lab acc" x="590" y="662" text-anchor="middle">{_e(d.get("distance", ""))}</text></g>')
    S.tl.append(show(f"#{s}-dist", S.mark(S.at("dist_at", 3.0)), 0.35))
    S.svg.append(_flame(k, 300, 768, 1.4, f"{s}-fire"))
    t_fire = S.mark(S.at("fire_at", 4.5))
    S.tl.append(ft(f"#{s}-fire", {"opacity": 0, "scale": 0.2, "transformOrigin": "50% 100%"},
                   {"opacity": 1, "scale": 1.4, "duration": 0.4, "ease": "back.out(2)"}, t_fire))
    n = int(d.get("boxes", 11))
    bw, bg = 56, 12
    for i in range(n):
        x = X0 + i * (bw + bg)
        S.svg.append(f'<g id="{s}-bx{i}" opacity="0"><path class="fr-rek" d="{rect_d(x, 1080, bw, 64)}"/>'
                     f'<text class="fr-boxq" x="{x + bw / 2}" y="1128" text-anchor="middle">?</text></g>')
    t_box = S.mark(S.at("boxes_at", 2.0))
    S.tl.append(ft(f"#{s} [id^={s}-bx]", {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0, "duration": 0.25, "stagger": 0.06}, t_box))
    S.foot()
    return S.out()


# --- fr_means: what existed (means of the time) and its limit ------------------------------------------

def fr_means(c, d: dict):
    S = _Scene(c, d, "fr_means")
    k, s = S.k, c.sid
    S.head()
    L, R = d.get("left", {}), d.get("right", {})
    for col in (L, R):
        S.check("title", col.get("title", ""))
    top = 470
    # left: beacon with a list of agreed messages
    S.svg.append(f'<g id="{s}-lt" opacity="0"><text class="fr-ct" x="{X0}" y="{top}">{_e(L.get("title", ""))}</text>'
                 f'<path class="fr-src fr-d" pathLength="1" d="M180,{top + 410} L212,{top + 170} H268 L300,{top + 410} Z M190,{top + 410} H290"/>'
                 f'</g>')
    S.svg.append(_flame(k, 240, top + 170, 1.4, f"{s}-bf"))
    items = L.get("items", [])
    for i, it in enumerate(items):
        S.check("item", it)
        y = top + 90 + i * 100
        S.svg.append(f'<g id="{s}-li{i}" opacity="0"><path d="{rect_d(320, y, 196, 72)}" class="fr-src" style="fill:{k["surface"]}"/>'
                     f'<text class="fr-item" x="418" y="{y + 47}" text-anchor="middle">{_e(it)}</text></g>')
    S.tl += draw(f"#{s}-lt", S.mark(S.at("left_at", 0.1)), 0.8)
    t_items = S.mark(S.at("items_at", 1.6))
    S.tl.append(ft(f"#{s} [id^={s}-li]", {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0, "duration": 0.3, "stagger": 0.15}, t_items))
    S.tl.append(ft(f"#{s}-bf", {"opacity": 0, "scale": 0.3, "transformOrigin": "50% 100%"},
                   {"opacity": 1, "scale": 1.3, "duration": 0.35, "ease": "back.out(2)"}, t_items + 0.5))
    S.tl.append(ft(f"#{s}-li0 path", {"fill": k["surface"]}, {"fill": k["stamp"], "duration": 0.3}, t_items + 0.7))
    # right: water clock of Aineias: two equal vessels, float with a rod and marks, torch starts and stops
    rx = 560
    S.svg.append(f'<g id="{s}-rt" opacity="0"><text class="fr-ct" x="{rx}" y="{top}">{_e(R.get("title", ""))}</text>')
    vy, vh, vw = top + 170, 240, 140
    marks = R.get("marks", ["1", "2", "3"])
    for j, vx in enumerate((rx + 0, rx + 200)):
        S.svg.append(f'<rect id="{s}-w{j}" x="{vx + 4}" y="{vy + 30}" width="{vw - 8}" height="{vh - 34}" fill="{k["water"]}" fill-opacity="0.55"/>'
                     f'<path class="fr-src fr-d" pathLength="1" d="M{vx},{vy} V{vy + vh} H{vx + vw} V{vy}"/>'
                     f'<g id="{s}-rod{j}"><path class="fr-src" d="M{vx + vw / 2},{vy + 22} V{vy - 80}" stroke-width="4"/>'
                     f'<path d="{rect_d(vx + 18, vy + 22, vw - 36, 14)}" fill="{k["text"]}"/>')
        for m, lab in enumerate(marks):
            my = vy - 60 + m * 28
            S.svg.append(f'<path d="M{vx + vw / 2 - 12},{my} H{vx + vw / 2 + 12}" class="fr-src" stroke-width="3"/>'
                         f'<text class="fr-mk" id="{s}-mk{j}{m}" x="{vx + vw / 2 + 20}" y="{my + 9}">{_e(lab)}</text>')
        S.svg.append("</g>")
    S.svg.append(f'<text class="fr-lab" x="{rx}" y="{vy + vh + 44}">{_e(R.get("note", ""))}</text></g>')
    S.svg.append(_flame(k, rx + 330, vy - 40, 0.9, f"{s}-tf"))
    t_r = S.mark(S.at("right_at", 4.3))
    S.tl += draw(f"#{s}-rt", t_r, 0.8)
    t_flow = S.mark(S.at("flow_at", 5.5))
    S.tl.append(show(f"#{s}-tf", t_flow, 0.25))
    drop = 56
    for j in range(2):
        S.tl.append(ft(f"#{s}-w{j}", {"attr": {"y": vy + 30, "height": vh - 34}},
                       {"attr": {"y": vy + 30 + drop, "height": vh - 34 - drop}, "duration": 1.6, "ease": "none"}, t_flow + 0.2))
        S.tl.append(ft(f"#{s}-rod{j}", {"y": 0}, {"y": drop, "duration": 1.6, "ease": "none"}, t_flow + 0.2))
        S.tl.append(ft(f"#{s}-mk{j}1", {"fill": k["text"]}, {"fill": k["fire"], "duration": 0.2}, t_flow + 1.8))
    S.tl.append(f'tl.to("#{s}-tf",{{opacity:0,duration:0.2}},{t_flow + 1.8:.3f});')
    S.mark(t_flow + 1.8)
    # bottom: the unforeseen message cannot be sent
    nb = d.get("unforeseen", {})
    S.check("stamp", nb.get("stamp", ""))
    by = 1020
    S.svg.append(f'<g id="{s}-nb" opacity="0"><path d="{rect_d(X0, by, X1 - X0, 120)}" class="fr-rek" style="fill:{k["surface"]};fill-opacity:0.8"/>'
                 f'<text class="fr-ct" x="{X0 + 28}" y="{by + 76}">{_e(nb.get("label", ""))}</text>'
                 f'<rect id="{s}-nbh" x="{X0 + 2}" y="{by + 2}" width="{X1 - X0 - 4}" height="116" fill="url(#{s}-hatch)" opacity="0"/>'
                 f'<g id="{s}-nbs" opacity="0"><path d="{rect_d(X1 - 330, by + 30, 300, 60)}" fill="none" stroke="{k["fire"]}" stroke-width="4"/>'
                 f'<text class="fr-stamp" x="{X1 - 180}" y="{by + 72}" text-anchor="middle">{_e(nb.get("stamp", ""))}</text></g></g>')
    t_nb = S.mark(S.at("unforeseen_at", 9.0))
    S.tl.append(show(f"#{s}-nb", t_nb, 0.35, 20))
    t_st = S.mark(S.at("mute_at", 10.0))
    S.tl.append(show(f"#{s}-nbh", t_st, 0.3))
    S.tl.append(ft(f"#{s}-nbs", {"opacity": 0, "scale": 1.8, "rotation": -10, "transformOrigin": "50% 50%"},
                   {"opacity": 1, "scale": 1, "rotation": -4, "duration": 0.25, "ease": "power4.in"}, t_st + 0.1))
    S.foot()
    return S.out()


# --- fr_solution: the solution as a line model ---------------------------------------------------------

def fr_solution(c, d: dict):
    S = _Scene(c, d, "fr_solution")
    k, s = S.k, c.sid
    S.head()
    S.svg.append(_tablets(s, k, X0, 450, 140, 28, 56, 56, 42))
    t_tab = S.mark(S.at("tablets_at", 0.3))
    for i in range(5):
        S.tl += draw(f"#{s}-tab{i}", t_tab + i * 0.12, 0.6)
    t_let = S.mark(S.at("letters_at", 2.5))
    for i, grp in enumerate(GREEK):
        for r in range(len(grp)):
            S.tl.append(show(f"#{s}-tab{i}l{r}", t_let + (i * 5 + r) * 0.035, 0.2))
    note = d.get("note", "")
    S.check("note", note)
    S.svg.append(f'<text id="{s}-note" class="fr-lab" x="{X0}" y="850" opacity="0">{_e(note)}</text>')
    S.tl.append(show(f"#{s}-note", t_let + 1.0, 0.3))
    # legend of the line grammar (first appearance in a video)
    if d.get("legend", True):
        de = S.de
        S.svg.append(f'<g id="{s}-leg" opacity="0"><path d="M580,842 H620" class="fr-src"/><text class="fr-leg" x="630" y="850">{"Quelle" if de else "source"}</text>'
                     f'<path d="M740,842 H780" class="fr-rek"/><text class="fr-leg" x="790" y="850">{"Rekon." if de else "recon."}</text></g>')
        S.tl.append(show(f"#{s}-leg", t_let + 1.4, 0.3))
    # wall with torches left (tablet) and right (letter)
    wall, lc, rc = _wall(s, k, X0, 715, 1040, 110, 30, 5, 0.95)
    S.svg.append(f'<g id="{s}-wall" opacity="0">{wall}</g>')
    t_wall = S.mark(S.at("wall_at", 5.5))
    S.tl.append(show(f"#{s}-wall", t_wall, 0.35))
    for side, cx, key, lab in (("L", lc, "left_at", d.get("left_label", "")), ("R", rc, "right_at", d.get("right_label", ""))):
        S.check("label", lab)
        S.svg.append(f'<g id="{s}-lab{side}" opacity="0"><text class="fr-lab acc sm" x="{cx}" y="1105" text-anchor="middle">{_e(lab)}</text></g>')
        t = S.mark(S.at(key, 6.0 if side == "L" else 8.3))
        S.tl.append(show(f"#{s}-lab{side}", t, 0.3))
        _light(S.tl, s, side, 5, t, 0.12)
    # sight tube with two tubes (reconstructed shape; Loeb note: it did not magnify)
    tx, ty = 748, 930
    S.svg.append(f'<g id="{s}-tube" opacity="0">'
                 f'<path class="fr-rek" d="M{tx},{ty + 30} L{tx + 170},{ty} M{tx},{ty + 70} L{tx + 170},{ty + 60} '
                 f'M{tx},{ty + 100} L{tx + 170},{ty + 120} M{tx},{ty + 140} L{tx + 170},{ty + 180} '
                 f'M{tx},{ty + 30} V{ty + 70} M{tx},{ty + 100} V{ty + 140} M{tx + 170},{ty} V{ty + 60} M{tx + 170},{ty + 120} V{ty + 180}"/>'
                 f'<text class="fr-lab acc sm" x="{X1}" y="{ty - 18}" text-anchor="end">{_e(d.get("tube_label", ""))}</text></g>')
    t_tube = S.mark(S.at("tube_at", 10.5))
    S.tl.append(show(f"#{s}-tube", t_tube, 0.4))
    S.foot()
    return S.out()


# --- fr_protocol: the procedure as a sequence between two stations -------------------------------------

def fr_protocol(c, d: dict):
    S = _Scene(c, d, "fr_protocol")
    k, s = S.k, c.sid
    S.head()
    la, lb = 300, 760
    lanes = d.get("lanes", ["SENDER", "EMPFÄNGER"])
    for nm in lanes:
        S.check("lane", nm)
    S.svg.append(f'<g id="{s}-lanes" opacity="0">'
                 f'<text class="fr-ct" x="{la}" y="490" text-anchor="middle">{_e(lanes[0])}</text>'
                 f'<text class="fr-ct" x="{lb}" y="490" text-anchor="middle">{_e(lanes[1])}</text>'
                 f'<path class="fr-src fr-d" pathLength="1" d="M{la},515 V1145 M{lb},515 V1145"/>'
                 f'<path class="fr-rek" d="M124,560 V1140" marker-end="url(#{s}-arr)"/>'
                 f'<text class="fr-lab" x="124" y="540" text-anchor="middle">{"ZEIT" if S.de else "TIME"}</text></g>')
    S.tl += draw(f"#{s}-lanes", S.mark(S.at("lanes_at", 0.1)), 0.7)
    for i, row in enumerate(d.get("rows", [])):
        S.check("row", row.get("text", ""))
        y = row.get("y", 600 + i * 110)
        kind = row.get("kind", "send")
        t = S.mark(S.atv(row.get("at"), 1.0 + i))
        g = f"{s}-row{i}"
        if kind == "pair":                      # one letter = left signal + right signal
            S.svg.append(f'<g id="{g}" opacity="0"><path d="{rect_d(la - 140, y - 46, lb - la + 280, 72)}" class="fr-src" style="fill:{k["surface"]};fill-opacity:0.9"/>'
                         f'<text class="fr-row" x="{(la + lb) / 2}" y="{y + 2}" text-anchor="middle">{_e(row.get("text", ""))}</text></g>')
            S.tl.append(show(f"#{g}", t, 0.35, 12))
        elif kind == "line":                    # a state across both lanes
            S.svg.append(f'<g id="{g}" opacity="0"><path d="M{la - 60},{y} H{lb + 60}" stroke="{k["accent"]}" stroke-width="5"/>'
                         f'<text class="fr-row acc" x="{(la + lb) / 2}" y="{y - 18}" text-anchor="middle">{_e(row.get("text", ""))}</text></g>')
            S.tl.append(show(f"#{g}", t, 0.3))
            S.tl.append(ft(f"#{g} path", {"scaleX": 0.2, "transformOrigin": "50% 50%"}, {"scaleX": 1, "duration": 0.4}, t))
        else:                                   # send / reply: arrow between the lanes with two flames at the origin
            x_from, x_to = (la, lb) if kind == "send" else (lb, la)
            dx = 30 if kind == "send" else -30
            nt = int(row.get("torches", 2))
            fl = "".join(_flame(k, x_from + (j - (nt - 1) / 2) * 34, y + 22, 0.85, hidden=False) for j in range(nt))
            S.svg.append(f'<g id="{g}" opacity="0">{fl}'
                         f'<path d="M{x_from + dx + (40 if kind == "send" else -40)},{y + 14} H{x_to - dx}" class="fr-src" stroke-width="4" marker-end="url(#{s}-arr)"/>'
                         f'<text class="fr-row" x="{(la + lb) / 2}" y="{y - 16}" text-anchor="middle">{_e(row.get("text", ""))}</text></g>')
            S.tl.append(show(f"#{g}", t, 0.3))
            S.tl.append(ft(f"#{g} path", {"strokeDasharray": "0 600"}, {"strokeDasharray": "600 0", "duration": 0.5}, t + 0.1))
    S.foot()
    return S.out()


# --- fr_example: a test case taken from the source ---------------------------------------------------

def fr_example(c, d: dict):
    S = _Scene(c, d, "fr_example")
    k, s = S.k, c.sid
    S.head()
    left, right = int(d.get("left", 2)), int(d.get("right", 5))
    wall, lc, rc = _wall(s, k, X0, X1, 670, 90, 40, 5, 1.05)
    S.svg.append(f'<g id="{s}-wall" opacity="0">{wall}</g>')
    S.tl.append(show(f"#{s}-wall", S.mark(S.at("wall_at", 0.1)), 0.3))
    labs = d.get("labels", ["", ""])
    for lab in labs:
        S.check("label", lab)
    S.svg.append(f'<text id="{s}-cl" class="fr-count" x="{lc}" y="830" text-anchor="middle" opacity="0">{_e(labs[0])}</text>'
                 f'<text id="{s}-cr" class="fr-count" x="{rc}" y="830" text-anchor="middle" opacity="0">{_e(labs[1])}</text>')
    tw, tg = 118, 16
    S.svg.append(_tablets(s, k, X0, 858, tw, tg, 46, 46, 32))
    t_tab = S.mark(S.at("tablet_at", 1.0))
    for i in range(5):
        S.tl += draw(f"#{s}-tab{i}", t_tab, 0.4)
        for r in range(len(GREEK[i])):
            S.tl.append(f'tl.set("#{s}-tab{i}l{r}",{{opacity:1}},{t_tab:.3f});')
    ti, ri = left - 1, right - 1
    S.tl.append(ft(f"#{s}-tab{ti} path", {"stroke": k["text"]}, {"stroke": k["fire"], "duration": 0.25}, t_tab + 0.3))
    t_cell = S.mark(S.at("cell_at", 2.2))
    S.tl.append(ft(f"#{s}-tab{ti}c{ri}", {"opacity": 0}, {"opacity": 1, "duration": 0.25}, t_cell))
    S.tl.append(ft(f"#{s}-tab{ti}l{ri}", {"fill": k["text"]}, {"fill": k["ink"], "duration": 0.25}, t_cell))
    t_l = S.mark(S.at("left_at", 3.1))
    _light(S.tl, s, "L", left, t_l, 0.2)
    S.tl.append(show(f"#{s}-cl", t_l + 0.3, 0.3))
    t_r = S.mark(S.at("right_at", 4.5))
    _light(S.tl, s, "R", right, t_r, 0.14)
    S.tl.append(show(f"#{s}-cr", t_r + 0.5, 0.3))
    # receiver's slip: the looked-up letter
    sx, sy = X1 - 120, 905
    letter = GREEK[ti][ri]
    cx_cell = X0 + ti * (tw + tg) + tw / 2
    cy_cell = 858 + 46 + 6 + ri * 46 + 20
    S.svg.append(f'<path id="{s}-look" d="M{cx_cell + tw / 2 - 4},{cy_cell} C{sx - 60},{cy_cell} {sx - 60},{sy + 70} {sx - 6},{sy + 70}" '
                 f'class="fr-src" stroke="{k["fire"]}" stroke-width="4" marker-end="url(#{s}-arr)" opacity="0"/>'
                 f'<g id="{s}-slip" opacity="0"><path d="{rect_d(sx, sy, 120, 150)}" fill="{k["paper"]}"/>'
                 f'<text id="{s}-let" class="fr-slip" x="{sx + 60}" y="{sy + 112}" text-anchor="middle" opacity="0">{letter}</text></g>'
                 f'<text id="{s}-sn" class="fr-lab" x="{X1}" y="1100" text-anchor="end" opacity="0">{_e(d.get("note", ""))}</text>')
    S.check("note", d.get("note", ""))
    t_look = S.mark(S.at("look_at", 5.6))
    S.tl.append(show(f"#{s}-slip", t_look - 0.2, 0.3))
    S.tl.append(ft(f"#{s}-look", {"opacity": 0, "strokeDasharray": "0 900"}, {"opacity": 1, "strokeDasharray": "900 0", "duration": 0.6}, t_look))
    t_w = S.mark(S.at("write_at", 6.8))
    S.tl.append(ft(f"#{s}-let", {"opacity": 0, "scale": 0.4, "transformOrigin": "50% 70%"}, {"opacity": 1, "scale": 1, "duration": 0.3, "ease": "back.out(2)"}, t_w))
    S.tl.append(show(f"#{s}-sn", t_w + 0.3, 0.3))
    S.foot()
    return S.out()


# --- fr_stages: the development in stages -----------------------------------------------------------

def fr_stages(c, d: dict):
    S = _Scene(c, d, "fr_stages")
    k, s = S.k, c.sid
    S.head()
    stages = d.get("stages", [])
    y0, h, gap = 450, 214, 24
    for i, st in enumerate(stages):
        S.check("title", st.get("title", ""))
        S.check("sub", st.get("sub", ""))
        y = y0 + i * (h + gap)
        g = f"{s}-st{i}"
        cap = st.get("can", "")
        S.svg.append(f'<g id="{g}" opacity="0"><path d="{rect_d(X0, y, X1 - X0, h)}" class="fr-src fr-d" pathLength="1" style="fill:{k["surface"]};fill-opacity:0.85"/>'
                     f'<text class="fr-stno" x="{X0 + 38}" y="{y + 130}">{i + 1}</text>'
                     f'<text class="fr-ct" x="{X0 + 120}" y="{y + 72}">{_e(st.get("title", ""))}</text>'
                     f'<text class="fr-sub" x="{X0 + 120}" y="{y + 122}">{_e(st.get("sub", ""))}</text>'
                     f'<text class="fr-can" x="{X0 + 120}" y="{y + 176}">{_e(cap)}</text></g>')
        t = S.mark(S.atv(st.get("at"), 1.0 + 2 * i))
        S.tl += draw(f"#{g}", t, 0.5)
        S.tl.append(ft(f"#{g}", {"x": -30}, {"x": 0, "duration": 0.35, "ease": "power2.out"}, t))
        if i:
            S.svg.append(f'<path id="{g}-j" d="M{X0 + 58},{y - gap - 2} V{y + 2}" stroke="{k["accent"]}" stroke-width="6" opacity="0"/>')
            S.tl.append(show(f"#{g}-j", t, 0.2))
        if st.get("chip"):
            S.check("chip", st["chip"])
            cw = 30 + 14.6 * len(st["chip"])
            S.svg.append(f'<g id="{g}-chip" opacity="0"><rect x="{X1 - cw - 16}" y="{y + 18}" width="{cw}" height="42" fill="url(#{s}-hatch)" stroke="{k["fire"]}" stroke-width="2"/>'
                         f'<text class="fr-chipin" x="{X1 - 16 - cw / 2}" y="{y + 48}" text-anchor="middle">{_e(st["chip"])}</text></g>')
            S.tl.append(show(f"#{g}-chip", S.mark(S.atv(st.get("chip_at"), 0)) if st.get("chip_at") else t + 0.8, 0.3))
        if st.get("stamp"):
            S.check("stamp", st["stamp"])
            S.svg.append(f'<g id="{g}-stamp" opacity="0"><rect x="{X1 - 326}" y="{y + 132}" width="302" height="58" fill="none" stroke="{k["accent"]}" stroke-width="4"/>'
                         f'<text class="fr-stamp acc" x="{X1 - 175}" y="{y + 171}" text-anchor="middle">{_e(st["stamp"])}</text></g>')
            ts = S.mark(S.atv(st.get("stamp_at"), 0))
            S.tl.append(ft(f"#{g}-stamp", {"opacity": 0, "scale": 1.8, "rotation": -10, "transformOrigin": "50% 50%"},
                           {"opacity": 1, "scale": 1, "rotation": -3, "duration": 0.25, "ease": "power4.in"}, ts))
    S.foot()
    return S.out()


# --- fr_finding: what survives, what is disputed, brand line --------------------------------------------

def fr_finding(c, d: dict):
    S = _Scene(c, d, "fr_finding")
    k, s = S.k, c.sid
    S.head()
    rows = d.get("rows", [])
    y0, rh = 450, 138
    h = 70 + rh * len(rows)
    S.svg.append(f'<g id="{s}-sheet" opacity="0"><path d="{rect_d(X0, y0, X1 - X0, h)}" fill="{k["paper"]}"/>'
                 f'<text class="fr-sheet-h" x="{X0 + 30}" y="{y0 + 46}">{_e(d.get("sheet", ""))}</text>'
                 f'<path d="M{X0 + 30},{y0 + 64} H{X1 - 30}" stroke="{k["ink"]}" stroke-opacity="0.4" stroke-width="2"/></g>')
    S.tl.append(ft(f"#{s}-sheet", {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0, "duration": 0.45, "ease": "power3.out"}, S.mark(S.at("sheet_at", 0.05))))
    for i, r in enumerate(rows):
        S.check("key", r.get("key", ""))
        S.check("value", r.get("value", ""))
        y = y0 + 70 + i * rh
        g = f"{s}-r{i}"
        box = ""
        if r.get("kind") == "hatch":
            box = f'<rect x="{X1 - 150}" y="{y + 22}" width="110" height="64" fill="url(#{s}-hatchp)" stroke="{k["ink"]}" stroke-width="2"/>'
        elif r.get("kind") == "disputed":
            box = f'<rect x="{X1 - 150}" y="{y + 22}" width="110" height="64" fill="url(#{s}-hatch)" stroke="{k["ink"]}" stroke-width="2"/>'
        S.svg.append(f'<g id="{g}" opacity="0"><text class="fr-key" x="{X0 + 30}" y="{y + 46}">{_e(r.get("key", ""))}</text>'
                     f'<text class="fr-val" x="{X0 + 30}" y="{y + 98}">{_e(r.get("value", ""))}</text>{box}'
                     f'<path d="M{X0 + 30},{y + rh - 4} H{X1 - 30}" stroke="{k["ink"]}" stroke-opacity="0.15" stroke-width="2"/></g>')
        S.tl.append(show(f"#{g}", S.mark(S.atv(r.get("at"), 0.8 + i * 1.6)), 0.3, 10))
    brand = d.get("brand", "")
    S.check("brand", brand)
    if brand:
        S.svg.append(f'<text id="{s}-brand" class="fr-brand" x="{X0}" y="{y0 + h + 58}" opacity="0">{_e(brand)}</text>')
        S.tl.append(show(f"#{s}-brand", S.mark(S.at("brand_at", 8.5)), 0.4, 14))
    S.foot()
    return S.out()



# --- fr_model: a generic line model from plan data ---------------------------------------------------

def _items(S, items: list, prefix: str = "m") -> None:
    """Draw plan-defined elements; every element appears at its own word anchor (`at`).

    t: path {d, kind src|rek|acc|fire, w, fill}   t: rect {x, y, w, h, kind src|rek|hatch|paper|fill}
    t: text {x, y, text, cls lab|acc|ct|count|val|row|big|ink, anchor}   t: dim {x1, y1, x2, y2, label, side, anchor}
    t: count {x, y, to, suffix, prefix, cls, anchor, dur}   t: repeat {x0, x1, y, n, shape box|tower|tick, size, dur}
    t: stamp {x, y, text, w, kind}   t: hl {target, color}  (recolours an earlier element by its `id`)
    `id` names an element for `hl`; `out` (time) fades it out again.
    """
    k, sid = S.k, S.c.sid
    colors = {"src": k["text"], "rek": k["text"], "acc": k["accent"], "fire": k["fire"], "stamp": k["stamp"]}
    for n, it in enumerate(items):
        t = it.get("t", "path")
        gid = f"{sid}-{prefix}{it.get('id', n)}"
        at = S.mark(S.atv(it.get("at"), 0.2 + 0.4 * n))
        kind = it.get("kind", "src")
        if t == "hl":
            tgt = f"#{sid}-{prefix}{it['target']}"
            col = colors.get(it.get("color", "fire"), it.get("color", k["fire"]))
            S.tl.append(f'tl.to("{tgt} .fr-src,{tgt} .fr-rek,{tgt} rect",{{stroke:"{col}",duration:0.3}},{at:.3f});')
            S.tl.append(f'tl.to("{tgt} text",{{fill:"{col}",duration:0.3}},{at:.3f});')
            continue
        if t == "path":
            w = it.get("w", 5 if kind != "rek" else 4)
            cls = "fr-rek" if kind == "rek" else "fr-src fr-d"
            extra = "" if kind == "rek" else ' pathLength="1"'
            fill = f"fill:{it['fill']};" if it.get("fill") else ""
            style = f' style="{fill}stroke:{colors.get(kind, k["text"])};stroke-width:{w}"'
            S.svg.append(f'<g id="{gid}" opacity="0"><path d="{it["d"]}" class="{cls}"{extra}{style}/></g>')
            if kind == "rek":
                S.tl.append(show(f"#{gid}", at, 0.4))
            else:
                S.tl += draw(f"#{gid}", at, float(it.get("dur", 0.8)))
        elif t == "rect":
            x, y, w, h = it["x"], it["y"], it["w"], it["h"]
            if kind == "hatch":
                body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{sid}-hatch)" stroke="{k["fire"]}" stroke-width="2"/>'
            elif kind == "paper":
                body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{k["paper"]}"/>'
            elif kind == "fill":
                body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{it.get("fill", k["water"])}" fill-opacity="{it.get("opacity", 0.6)}"/>'
            else:
                cls = "fr-rek" if kind == "rek" else "fr-src"
                body = f'<path d="{rect_d(x, y, w, h)}" class="{cls}" style="fill:{k["surface"]};fill-opacity:{it.get("opacity", 0.85)}"/>'
            S.svg.append(f'<g id="{gid}" opacity="0">{body}</g>')
            S.tl.append(show(f"#{gid}", at, 0.35))
        elif t in ("text", "count"):
            cls = {"lab": "fr-lab", "acc": "fr-lab acc", "ct": "fr-ct", "count": "fr-count", "val": "fr-val", "row": "fr-row",
                   "big": "fr-big", "ink": "fr-ink"}.get(it.get("cls", "lab"), "fr-lab")
            anchor = it.get("anchor", "start")
            txt = it.get("text", "")
            S.check("label", txt)
            if t == "count":
                pre, suf = it.get("prefix", ""), it.get("suffix", "")
                S.svg.append(f'<text id="{gid}" class="{cls}" x="{it["x"]}" y="{it["y"]}" text-anchor="{anchor}" opacity="0">'
                             f'{_e(pre)}<tspan id="{gid}-n">0</tspan>{_e(suf)}</text>')
                S.tl.append(show(f"#{gid}", at, 0.2))
                S.tl.append(FL._count_tl(f"#{gid}-n", int(it["to"]), at, float(it.get("dur", 1.2))))  # noqa: F821
            else:
                S.svg.append(f'<text id="{gid}" class="{cls}" x="{it["x"]}" y="{it["y"]}" text-anchor="{anchor}" opacity="0">{_e(txt)}</text>')
                S.tl.append(show(f"#{gid}", at, 0.3, 8))
        elif t == "dim":
            x1, y1, x2, y2 = it["x1"], it["y1"], it["x2"], it["y2"]
            horiz = abs(y2 - y1) < abs(x2 - x1)
            tick = (f"M{x1},{y1 - 14} V{y1 + 14} M{x2},{y2 - 14} V{y2 + 14}" if horiz else f"M{x1 - 14},{y1} H{x1 + 14} M{x2 - 14},{y2} H{x2 + 14}")
            col = k["fire"] if kind == "fire" else k["accent"]
            dash = ' stroke-dasharray="10 8"' if kind == "rek" else ""
            lab = it.get("label", "")
            S.check("label", lab)
            if horiz:
                lx, anc = (x1 + x2) / 2, "middle"
                ly = min(y1, y2) - 18 if it.get("side", "up") == "up" else max(y1, y2) + 42
            else:
                lx, ly, anc = max(x1, x2) + 24, (y1 + y2) / 2 + 9, "start"
            S.svg.append(f'<g id="{gid}" opacity="0"><path d="M{x1},{y1} L{x2},{y2} {tick}" fill="none" stroke="{col}" stroke-width="3"{dash}/>'
                         f'<text class="fr-lab acc" x="{it.get("lx", lx)}" y="{it.get("ly", ly)}" text-anchor="{it.get("anchor", anc)}">{_e(lab)}</text></g>')
            S.tl.append(show(f"#{gid}", at, 0.35))
        elif t == "repeat":
            x0, x1, y, nn = it["x0"], it["x1"], it["y"], int(it["n"])
            shape, sz = it.get("shape", "box"), float(it.get("size", 22))
            parts = []
            for i in range(nn):
                x = x0 + (x1 - x0) * (i / max(1, nn - 1))
                if shape == "box":
                    parts.append(f'<rect class="fr-rp" x="{x - sz / 2:.1f}" y="{y - sz / 2:.1f}" width="{sz}" height="{sz}" fill="{k["surface"]}" stroke="{k["text"]}" stroke-width="4" opacity="0"/>')
                elif shape == "tower":
                    parts.append(f'<rect class="fr-rp" x="{x - sz / 4:.1f}" y="{y - sz / 4:.1f}" width="{sz / 2}" height="{sz / 2}" fill="{k["text"]}" opacity="0"/>')
                else:
                    parts.append(f'<path class="fr-rp" d="M{x:.1f},{y - sz / 2:.1f} V{y + sz / 2:.1f}" stroke="{k["accent"]}" stroke-width="4" opacity="0"/>')
            S.svg.append(f'<g id="{gid}">{"".join(parts)}</g>')
            S.tl.append(ft(f"#{gid} .fr-rp", {"opacity": 0, "scale": 0.4, "transformOrigin": "50% 50%"},
                           {"opacity": 1, "scale": 1, "duration": 0.2, "stagger": {"amount": float(it.get("dur", 1.2))}}, at))
        elif t == "stamp":
            txt = it.get("text", "")
            w = it.get("w", 40 + 20 * len(txt))
            col = k["accent"] if kind == "acc" else k["fire"]
            S.check("label", txt)
            S.svg.append(f'<g id="{gid}" opacity="0"><rect x="{it["x"] - w / 2}" y="{it["y"] - 44}" width="{w}" height="60" fill="none" stroke="{col}" stroke-width="4"/>'
                         f'<text class="fr-stamp" style="fill:{col}" x="{it["x"]}" y="{it["y"]}" text-anchor="middle">{_e(txt)}</text></g>')
            S.tl.append(ft(f"#{gid}", {"opacity": 0, "scale": 1.8, "rotation": -10, "transformOrigin": "50% 50%"},
                           {"opacity": 1, "scale": 1, "rotation": -3, "duration": 0.25, "ease": "power4.in"}, at))
        if it.get("out") is not None:
            S.tl.append(f'tl.to("#{gid}",{{opacity:0,duration:0.3}},{S.atv(it["out"], 0):.3f});')


def fr_model(c, d: dict):
    S = _Scene(c, d, "fr_model")
    S.head()
    _items(S, d.get("items", []))
    S.foot()
    return S.out()


TEMPLATES = {"fr_task": fr_task, "fr_means": fr_means, "fr_solution": fr_solution, "fr_protocol": fr_protocol,
             "fr_example": fr_example, "fr_stages": fr_stages, "fr_finding": fr_finding, "fr_model": fr_model}
HOOK_SCENE_TYPES = ["fr_task"]


# --- layer: map table with graticule and the time ruler ----------------------------------------------

def _yx(year: float, r: dict) -> float:
    return X0 + (year - r["from"]) / (r["to"] - r["from"]) * (X1 - X0)


def _year_label(y: int, de: bool) -> str:
    if y < 0:
        return f"{-y} v. Chr." if de else f"{-y} BC"
    if y < 1000:
        return f"{y} n. Chr." if de else f"AD {y}"
    return f"{y}"


def LAYER(plan, brand, project_dir, captions):  # noqa: N802
    """Static map table: paper ground, graticule (no drift, no contours), time ruler from `layout.ruler`."""
    lay = plan.layout or {}
    dst = Path(project_dir) / "assets" / "bg"
    dst.mkdir(parents=True, exist_ok=True)
    probs = []
    src = Path(__file__).resolve().parent / "assets" / "bg"
    for f in ("base.jpg", "LICENSE.md"):
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
        else:
            probs.append(f"background file {f} missing (run brands/military_history/make_background.py)")
    de = (plan.language or "de") == "de"
    acc, text, muted, fire = "#A9B29F", "#E6E9E5", "#B0B7AC", "#D9B45A"
    # graticule: meridians converge slightly towards the top, parallels are arcs (a conic map, schematic)
    g = []
    for i in range(-6, 7):
        xb = 540 + i * 150
        xt = 540 + i * 118
        g.append(f'<path d="M{xt},-40 Q{(xt + xb) / 2 + i * 6},960 {xb},1960" />')
    for j in range(9):
        y = 120 + j * 220
        g.append(f'<path d="M-60,{y + 60} Q540,{y - 50} 1140,{y + 60}" />')
    grat = f'<g fill="none" stroke="{acc}" stroke-opacity="0.075" stroke-width="2">{"".join(g)}</g>'
    # time ruler
    r = lay.get("ruler") or {}
    ruler, tl, events = "", [], []
    if r:
        major, minor = int(r.get("major", 100)), int(r.get("minor", 25))
        base_y = 226
        parts = [f'<path d="M{X0},{base_y} H{X1}" stroke="{text}" stroke-opacity="0.55" stroke-width="2"/>']
        y = r["from"]
        while y <= r["to"]:
            x = _yx(y, r)
            big = (y - r["from"]) % major == 0
            parts.append(f'<path d="M{x:.1f},{base_y} V{base_y - (14 if big else 7)}" stroke="{text}" stroke-opacity="{0.7 if big else 0.4}" stroke-width="2"/>')
            if big:
                anchor = "start" if y == r["from"] else ("end" if y == r["to"] else "middle")
                lab = _year_label(y, de) if (y == r["from"] or y < 0 or y >= 1000) else str(y)   # AD centuries: suffix only once
                parts.append(f'<text x="{x:.1f}" y="{base_y - 22}" text-anchor="{anchor}" class="frl-y">{lab}</text>')
            y += minor
        starts = {b.id: b.start for b in plan.beats if b.start is not None}
        for n, it in enumerate(r.get("items", [])):
            iid = f"frl-i{n}"
            row = int(it.get("row", 0))
            by = base_y + 8 + row * 16
            kind = it.get("kind", "bar")
            frag = []
            if kind == "mark":
                x = _yx(it["at"], r)
                frag.append(f'<path d="M{x:.1f},{base_y - 16} V{by + 12}" stroke="{acc}" stroke-width="4"/>')
            else:
                x0, x1 = _yx(it["from"], r), _yx(it["to"], r)
                if kind == "range":            # uncertain as a whole: hatched only
                    frag.append(f'<rect x="{x0:.1f}" y="{by}" width="{x1 - x0:.1f}" height="11" fill="url(#frl-hatch)" stroke="{fire}" stroke-width="1.5"/>')
                else:
                    a, b = x0, x1
                    for fz in it.get("fuzzy", []):   # hatched ends where the sources disagree
                        fx0, fx1 = _yx(fz[0], r), _yx(fz[1], r)
                        frag.append(f'<rect x="{fx0:.1f}" y="{by}" width="{fx1 - fx0:.1f}" height="11" fill="url(#frl-hatch)" stroke="{fire}" stroke-width="1.5"/>')
                        if abs(fx0 - x0) < 1:
                            a = fx1
                        if abs(fx1 - x1) < 1:
                            b = fx0
                    frag.append(f'<rect x="{a:.1f}" y="{by}" width="{b - a:.1f}" height="11" fill="{acc}"/>')
            if it.get("label"):
                lx = _yx(it.get("label_at", it.get("from", it.get("at"))), r)
                frag.append(f'<text x="{lx:.1f}" y="{base_y + 52}" class="frl-l" text-anchor="{it.get("anchor", "start")}">{FL._e(it["label"])}</text>')  # noqa: F821
            parts.append(f'<g id="{iid}" opacity="0">{"".join(frag)}</g>')
            t_in = starts.get(it.get("beat", ""), 0.0) + float(it.get("offset", 0.4))
            tl.append(f'tl.fromTo("#{iid}",{{opacity:0}},{{opacity:1,duration:0.4}},{t_in:.3f});')
            events.append(round(t_in, 3))
            if it.get("until"):
                t_out = starts.get(it["until"], 0.0) + float(it.get("until_offset", 0.2))
                tl.append(f'tl.to("#{iid} text",{{opacity:0,duration:0.3}},{t_out:.3f});')
        ruler = ("<defs><pattern id=\"frl-hatch\" width=\"10\" height=\"10\" patternUnits=\"userSpaceOnUse\" patternTransform=\"rotate(45)\">"
                 f"<line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"10\" stroke=\"{fire}\" stroke-width=\"3\"/></pattern></defs>" + "".join(parts))
    mono = (brand.design.get("fonts", {}).get("mono", {}) or {}).get("family", "JetBrains Mono") if hasattr(brand, "design") else "JetBrains Mono"
    head = ("<style>#frl{position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none;}"
            "#frl img{position:absolute;left:-120px;top:-120px;width:1320px;height:2280px;}"
            "#frl svg{position:absolute;left:0;top:0;width:1080px;height:1920px;}"
            f"#frl-ruler{{z-index:20;}}"
            f".frl-y{{font-family:'FN {mono}';font-size:24px;fill:{muted};}}"
            f".frl-l{{font-family:'FN {mono}';font-size:24px;fill:{text};letter-spacing:0;}}"
            "#frl-vig{position:absolute;inset:0;background:radial-gradient(ellipse 90% 75% at 45% 40%,rgba(0,0,0,0) 45%,rgba(12,16,13,0.62) 100%);}</style>")
    under = (f'<div id="frl"><img id="frl-base" src="assets/bg/base.jpg" alt="">'
             f'<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{grat}</svg><div id="frl-vig"></div></div>'
             f'<svg id="frl-ruler" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg" '
             f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none;">{ruler}</svg>')
    med = _media_layer(plan, project_dir, captions)
    if med:
        head += med["css"]
        under += med["html"]
        tl += med["tl"]
        events += med["events"]
        probs += med["problems"]
    body_end = "<script>(function(){const tl=window.__timelines&&window.__timelines.main;if(!tl)return;" + "".join(tl) + "tl.seek(0);})();</script>"
    return {"head_html": head, "under_scenes_html": under, "body_end_html": body_end, "events": events, "problems": probs}


def MANIFEST_EXTRA(plan):  # noqa: N802
    """Media used by the test video, with its licence line (assets/higgsfield/*/LICENSE.md)."""
    names = sorted({sh.get(k) for b in plan.beats if isinstance(b.data, dict)
                    for sh in (b.data.get("media") or {}).get("shots", []) for k in ("still", "clip") if sh.get(k)})
    if not names:
        return {}
    lic = {}
    for d in MEDIA_DIRS:
        lf = Path(__file__).resolve().parent / d / "LICENSE.md"
        if lf.exists():
            for line in lf.read_text(encoding="utf-8").splitlines():
                if ":" in line:
                    lic[line.split(":", 1)[0].strip()] = line.split(":", 1)[1].strip()
    return {"frontlore_media": [{"file": n, "license": lic.get(n, "")} for n in names]}



# --- media layer (Neustart 03.11.2026): realistic reconstruction stills and clips under the scenes -------------------

MEDIA_DIRS = ("assets/higgsfield/testvideo", "assets/higgsfield/library")
MOVES = {"push": ({"scale": 1.0}, {"scale": 1.07}), "pull": ({"scale": 1.07}, {"scale": 1.0}),
         "pan_l": ({"scale": 1.08, "x": 30}, {"scale": 1.08, "x": -30}), "pan_r": ({"scale": 1.08, "x": -30}, {"scale": 1.08, "x": 30}),
         "drift": ({"scale": 1.02, "y": 10}, {"scale": 1.05, "y": -10})}
SPLIT = {"left": "inset(0px 540px 0px 0px)", "right": "inset(0px 0px 0px 540px)",
         "top": "inset(0px 0px 960px 0px)", "bottom": "inset(960px 0px 0px 0px)"}
CUES = ("whoosh", "flare", "fire", "paper", "scratch", "stamp", "click", "bed_duck", "bed_up")


def _wnorm(t: str) -> str:
    import re as _re
    return _re.sub(r"[^\w]", "", str(t).lower())


def _wat(v, words, b, default=0.0, probs=None, what=""):
    """Absolute time for a number (seconds from the beat start) or "w:Wort" / "w:Wort#2" on the beat's words."""
    if v is None:
        return b.start + default
    if isinstance(v, (int, float)):
        return b.start + float(v)
    sv = str(v)
    if sv.startswith("w:"):
        tok, n = sv[2:], 1
        if "#" in tok:
            tok, k = tok.rsplit("#", 1)
            n = int(k)
        hits = [w for w in words if b.start - 0.05 <= w[1] < b.start + b.duration and _wnorm(w[0]).startswith(_wnorm(tok))]
        if len(hits) >= n:
            return hits[n - 1][1]
        if probs is not None:
            probs.append(f"{b.id} {what}: anchor {sv!r} not found")
    return b.start + default


def _find_media(name: str):
    here = Path(__file__).resolve().parent
    for d in MEDIA_DIRS:
        f = here / d / name
        if f.exists():
            return f
    return None


def _seconds(f) -> float:
    import subprocess
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                           capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip())
    except (OSError, ValueError, subprocess.SubprocessError):
        return 0.0


def _media_layer(plan, project_dir, captions):
    """Per beat `data.media` {shots[{still, clip, at, until, move, frame{scale,x,y}, split, enter flash|wipe|fade}],
    dim, foil{at, out, opacity}, blur_at, stamp} and `data.cues` [{at, cue}] -> html clips on track 0 (under the scenes),
    timeline tweens, events, problems, sound cues."""
    beats = [b for b in plan.beats if b.start is not None and isinstance(b.data, dict)]
    if not any(b.data.get("media") for b in beats):
        return None
    lang = plan.language or "de"
    probs: list[str] = []
    words = [(w.text, w.start) for g in (captions or []) for w in getattr(g, "words", [])]
    dst = Path(project_dir) / "assets" / "frmedia"
    dst.mkdir(parents=True, exist_ok=True)
    lic = {}
    for d in MEDIA_DIRS:
        lf = Path(__file__).resolve().parent / d / "LICENSE.md"
        if lf.exists():
            for line in lf.read_text(encoding="utf-8").splitlines():
                if ":" in line and line.split(":", 1)[0].strip().endswith((".jpg", ".png", ".mp4")):
                    lic[line.split(":", 1)[0].strip()] = line.split(":", 1)[1].strip()
    html_, tl, ev, cues, used = [], [], [], [], []
    stamp_spans: list[list[float]] = []
    for bi, b in enumerate(beats):
        m = b.data.get("media") or {}
        end = b.start + b.duration
        for k, sh in enumerate(m.get("shots", [])):
            t0 = _wat(sh.get("at"), words, b, 0.0, probs, f"shot {k}")
            t1 = _wat(sh.get("until"), words, b, b.duration, probs, f"shot {k} until") if sh.get("until") is not None else end
            dur = max(0.1, t1 - t0)
            fr = sh.get("frame") or {}
            sc, fx, fy = float(fr.get("scale", 1.0)), float(fr.get("x", 0)), float(fr.get("y", 0))
            box = f"left:{fx:.0f}px;top:{fy:.0f}px;width:{1080 * sc:.0f}px;height:{1920 * sc:.0f}px;"
            clip = f"clip-path:{SPLIT[sh['split']]};" if sh.get("split") in SPLIT else ""
            sid = f"frm{bi}_{k}"
            targets = []
            for kind, name in (("still", sh.get("still")), ("clip", sh.get("clip"))):
                if not name:
                    continue
                f = _find_media(name)
                if not f:
                    probs.append(f"{b.id} shot {k}: media {name} missing")
                    continue
                if not lic.get(name):
                    probs.append(f"{b.id} shot {k}: media {name} without licence line")
                if not (dst / name).exists():
                    import shutil as _sh
                    _sh.copy2(f, dst / name)
                used.append({"file": name, "license": lic.get(name, "")})
                if kind == "still":
                    html_.append(f'<div id="{sid}s" class="clip frm" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="0" style="{clip}">'
                                 f'<img id="{sid}si" class="frm-i" src="assets/frmedia/{name}" alt="" style="{box}"></div>')
                    targets.append(f"#{sid}si")
                else:
                    c = _seconds(f) - 0.08
                    v0, vd = (t0, dur) if dur <= c else (t0, c)
                    if c <= 0:
                        probs.append(f"{b.id} shot {k}: clip {name} unreadable")
                        continue
                    html_.append(f'<video id="{sid}cv" class="clip frm-i frv" src="assets/frmedia/{name}" data-start="{v0:.3f}" data-duration="{vd:.3f}" '
                                 f'data-track-index="0" data-volume="0" muted playsinline style="{box}{clip}"></video>')
                    targets.append(f"#{sid}cv")
            mv = MOVES.get(sh.get("move", ""))
            for tg in targets:
                if mv:
                    a, z = mv
                    tl.append(f'tl.fromTo("{tg}",{js(a)},{js({**z, "duration": round(dur, 3), "ease": "none"})},{t0:.3f});')
            enter = sh.get("enter", "fade")
            for tg in [f"#{sid}s", f"#{sid}cv"]:
                if enter == "wipe" and sh.get("split") in ("left", "right"):
                    side = sh["split"]
                    frm = "inset(0px 1080px 0px 0px)" if side == "left" else "inset(0px 0px 0px 1080px)"
                    tl.append(f'tl.fromTo("{tg}",{{clipPath:"{frm}"}},{{clipPath:"{SPLIT[side]}",duration:0.5,ease:"power2.out"}},{t0:.3f});')
                elif enter == "fade":
                    tl.append(f'tl.fromTo("{tg}",{{opacity:0}},{{opacity:1,duration:0.4}},{t0:.3f});')
            if enter == "flash":
                html_.append(f'<div id="{sid}f" class="clip frflash" data-start="{t0:.3f}" data-duration="0.6" data-track-index="0"></div>')
                tl.append(f'tl.fromTo("#{sid}f",{{opacity:0.85}},{{opacity:0,duration:0.5,ease:"power2.out"}},{t0:.3f});')
            ev.append(round(t0, 3))
        if m.get("shots"):
            dim = float(m.get("dim", 0.3))
            html_.append(f'<div id="frd{bi}" class="clip frdim" data-start="{b.start:.3f}" data-duration="{b.duration:.3f}" data-track-index="0" style="opacity:{dim:.2f}"></div>')
            if m.get("stamp", True):
                spans = stamp_spans
                if spans and b.start - spans[-1][1] <= 0.6:          # adjacent beats share one stamp (no double text at the cut)
                    spans[-1][1] = end
                else:
                    spans.append([b.start, end])
        if m.get("blur_at") is not None:
            tb = _wat(m["blur_at"], words, b, 0.4, probs, "blur")
            tl.append(f'tl.to("[id^=frm{bi}_] .frm-i",{{filter:"blur(9px) brightness(0.8)",duration:0.6,ease:"power2.out"}},{tb:.3f});')
            ev.append(round(tb, 3))
        fo = m.get("foil")
        if fo:
            ta = _wat(fo.get("at"), words, b, 0.0, probs, "foil")
            tz = _wat(fo.get("out"), words, b, b.duration, probs, "foil out") if fo.get("out") is not None else end
            html_.append(f'<div id="frf{bi}" class="clip frfoil" data-start="{ta:.3f}" data-duration="{max(0.2, tz - ta):.3f}" data-track-index="0" '
                         f'style="--fo:{float(fo.get("opacity", 0.6)):.2f}"></div>')
            tl.append(f'tl.fromTo("#frf{bi}",{{x:1080}},{{x:0,duration:0.55,ease:"power3.out"}},{ta:.3f});')
            cues.append({"t": round(ta, 3), "cue": "paper", "beat": b.id, "anchor": fo.get("at")})
            ev.append(round(ta, 3))
        for c in b.data.get("cues") or []:
            if c.get("cue") not in CUES:
                probs.append(f"{b.id}: unknown cue {c.get('cue')!r}")
            t = _wat(c.get("at"), words, b, 0.0, probs, f"cue {c.get('cue')}")
            cues.append({"t": round(t, 3), "cue": c.get("cue", ""), "beat": b.id, "anchor": c.get("at", 0)})
    txt = "KI-REKONSTRUKTION" if lang == "de" else "AI RECONSTRUCTION"
    for si, (t0, t1) in enumerate(stamp_spans):
        html_.append(f'<div id="frst{si}" class="clip frstamp" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-track-index="0">{_e(txt)}</div>')
    total = max(b.start + b.duration for b in beats) + float((plan.layout or {}).get("tail_seconds", 2.6))
    html_.append(f'<div id="frshade" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0"></div>')
    import json as _json
    snd = {"palette": (plan.layout or {}).get("sound", {}), "cues": sorted(cues, key=lambda c: c["t"])}
    (Path(project_dir) / "sound_cues.json").write_text(_json.dumps(snd, indent=1, ensure_ascii=False), encoding="utf-8")
    css = ("<style>.frm{z-index:1;overflow:hidden;}.frm-i{position:absolute;object-fit:cover;transform-origin:50% 50%;}"
           ".frv{z-index:2;}.frdim{z-index:3;background:#0d120f;}.frflash{z-index:4;background:#F4E3B0;}"
           ".frfoil{z-index:4;background:rgba(18,24,20,var(--fo));border-left:3px solid rgba(233,228,212,0.55);"
           "background-image:repeating-linear-gradient(0deg,rgba(233,228,212,0.05) 0 1px,transparent 1px 48px),"
           "repeating-linear-gradient(90deg,rgba(233,228,212,0.05) 0 1px,transparent 1px 48px);}"
           ".frstamp{z-index:5;inset:254px 160px auto auto;width:auto;height:auto;"
           "font-family:'FN JetBrains Mono';font-size:24px;font-weight:600;letter-spacing:0.06em;color:#F4E3B0;"
           "padding:3px 10px;border:2px solid rgba(244,227,176,0.7);background:rgba(13,18,15,0.55);}"
           "#frshade{z-index:3;pointer-events:none;background:linear-gradient(180deg,rgba(13,18,15,0.86) 0px,rgba(13,18,15,0.55) 300px,"
           "rgba(13,18,15,0.05) 520px,rgba(13,18,15,0.05) 1000px,rgba(13,18,15,0.6) 1160px,rgba(13,18,15,0.9) 1400px,rgba(13,18,15,0.94) 1920px);}</style>")
    return {"html": "".join(html_), "tl": tl, "events": ev, "problems": probs, "css": css, "used": used}

def CSS(pal: dict, display: str, display_w: int, body: str, mono: str) -> str:  # noqa: N802
    acc, text, muted = pal.get("accent", "#A9B29F"), pal.get("text", "#E6E9E5"), pal.get("muted", "#B0B7AC")
    ink, fire = pal.get("paper_ink", "#1F2620"), pal.get("signal_amber", "#D9B45A")
    return f"""
/* Frontlore format "Rekonstruktion" */
.scene-inner.fr{{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;gap:0;}}
.fr svg.fr-svg{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;}}
.fr .fr-src{{fill:none;stroke:{text};stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}}
.fr .fr-src.fr-d{{stroke-dasharray:1;stroke-dashoffset:1;}}
.fr .fr-rek{{fill:none;stroke:{text};stroke-opacity:0.85;stroke-width:4;stroke-dasharray:14 10;stroke-linecap:round;}}
.fr .fr-rule{{stroke:{acc};stroke-opacity:0.45;stroke-width:2;}}
.fr .fr-kick{{font-family:'FN {mono}';font-weight:600;font-size:26px;fill:{acc};letter-spacing:0.08em;}}
.fr .fr-head{{font-family:'FN {display}';font-weight:{display_w};font-size:62px;fill:{text};text-transform:uppercase;letter-spacing:0.02em;}}
.fr .fr-q{{font-family:'FN {display}';font-weight:{display_w};font-size:88px;fill:{text};}}
.fr .fr-q .fr-em{{fill:{fire};}}
.fr .fr-lab{{font-family:'FN {mono}';font-size:28px;fill:{muted};}}
.fr .fr-lab.acc{{fill:{acc};font-weight:600;}}
.fr .fr-leg{{font-family:'FN {mono}';font-size:26px;fill:{muted};}}
.fr .fr-ct{{font-family:'FN {display}';font-weight:{display_w};font-size:40px;fill:{text};letter-spacing:0.02em;}}
.fr .fr-item{{font-family:'FN {mono}';font-size:28px;fill:{text};}}
.fr .fr-mk{{font-family:'FN {mono}';font-size:30px;fill:{text};}}
.fr .fr-stamp{{font-family:'FN {display}';font-weight:{display_w};font-size:34px;fill:{fire};letter-spacing:0.08em;}}
.fr .fr-stamp.acc{{fill:{acc};font-size:26px;}}
.fr .fr-boxq{{font-family:'FN {mono}';font-size:34px;fill:{muted};}}
.fr .fr-tabno{{font-family:'FN {display}';font-weight:{display_w};font-size:34px;fill:{acc};}}
.fr .fr-gr{{font-family:'FN {mono}';font-weight:600;fill:{text};}}
.fr .fr-row{{font-family:'FN {mono}';font-size:28px;fill:{text};}}
.fr .fr-row.acc{{fill:{acc};font-weight:600;}}
.fr .fr-count{{font-family:'FN {display}';font-weight:{display_w};font-size:46px;fill:{fire};letter-spacing:0.04em;}}
.fr .fr-slip{{font-family:'FN {mono}';font-weight:700;font-size:92px;fill:{ink};}}
.fr .fr-stno{{font-family:'FN {display}';font-weight:{display_w};font-size:84px;fill:{acc};}}
.fr .fr-sub{{font-family:'FN {mono}';font-size:26px;fill:{muted};}}
.fr .fr-can{{font-family:'FN {mono}';font-size:26px;fill:{text};}}
.fr .fr-chipin{{font-family:'FN {mono}';font-size:24px;font-weight:600;fill:{text};}}
.fr .fr-sheet-h{{font-family:'FN {mono}';font-size:26px;font-weight:600;fill:{ink};letter-spacing:0.08em;}}
.fr .fr-key{{font-family:'FN {mono}';font-size:26px;fill:{ink};fill-opacity:0.7;letter-spacing:0.08em;}}
.fr .fr-val{{font-family:'FN {display}';font-weight:{display_w};font-size:40px;fill:{ink};}}
.fr .fr-brand{{font-family:'FN {display}';font-weight:{display_w};font-size:44px;fill:{text};}}
.fr .fr-chip{{font-family:'FN {mono}';font-size:28px;font-weight:600;fill:{text};letter-spacing:0.02em;}}
.fr .fr-cite{{font-family:'FN {mono}';font-size:28px;fill:{muted};}}
.fr .fr-big{{font-family:'FN {display}';font-weight:{display_w};font-size:96px;fill:{fire};}}
.fr .fr-ink{{font-family:'FN {mono}';font-size:28px;fill:{ink};}}
.fr .fr-lab.sm{{font-size:24px;}}
"""
