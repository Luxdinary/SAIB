"""Promptwerk scene types (brand claude_workflows): clean SaaS, didactic.

Loaded by `fn.render.brand_scenes` (contract: TEMPLATES, LIMITS, HOOK_SCENE_TYPES, CSS). Scene types are
prefixed `pw_`; the hook beat uses `pw_hook`. Render with the shared `scripts/render_direction.py`.

Identity in one line: one app window as the stage (editor, docs page, terminal), a violet text marker that
sweeps over the decisive line, a cursor that clicks it, a zoom onto it, and short didactic callouts. Event times
follow the voice: `<event>_word` in the beat data anchors an event to the first spoken word that starts with
that text (word timings from the director), else `<event>_at` (seconds from the beat start), else a fraction
of the beat duration.

Stage geometry: scene zone 864 x zone_h (810 in the Promptwerk layout) starting at x 108, y zone_top.
Readability floors as in the shared templates: headline >= 56 px, code >= 30 px, labels >= 30 px.
"""
from __future__ import annotations

import html

from fn.render.templates import SceneCtx, SceneOut

LIMITS: dict[str, dict[str, int]] = {
    "pw_hook": {"question": 64, "line": 30, "chip": 22, "tab": 22},
    "pw_doc": {"page_title": 40, "kicker": 32, "quote": 70, "translation": 40},   # translation: one line, else it reaches the marker row
    "pw_flow": {"headline": 48, "node": 22, "chip": 22},
    "pw_editor": {"line": 40, "callout": 30, "tab": 24},
    "pw_terminal": {"line": 38, "title": 30, "stamp": 10, "annotation": 34},
    "pw_compare": {"title": 22, "verdict": 10, "row": 26},
    "pw_steps": {"headline": 48, "title": 28, "code": 32},          # up to 5 steps; 4-5 render compact
    "pw_close": {"statement": 56, "line": 38, "badge": 24, "claim": 40},
}

# Stefan, 2026-10-30: no screen recordings; UI scenes are animations, always labelled as such in the window
SCHEMATIC = {"de": "Animierte Darstellung", "en": "Animated view"}


def _e(s) -> str:
    return html.escape(str(s))


def _lim(kind: str, key: str, val, where: str, probs: list[str]) -> None:
    n = LIMITS.get(kind, {}).get(key)
    if n and len(str(val)) > n:
        probs.append(f"{kind}.{where}: {len(str(val))} chars > {n}")


def _word_time(c: SceneCtx, word: str) -> float | None:
    w0 = word.lower().strip(".,:;!?")
    for w in getattr(c, "words", None) or []:
        if w.text.lower().strip(".,:;!?\"'„“").startswith(w0):
            return float(w.start)
    return None


def _at(c: SceneCtx, d: dict, key: str, frac: float) -> float:
    """Absolute time: the `<event>_word` anchor, else data[key] seconds from the beat start, else `frac` of the duration."""
    wkey = key[:-3] + "_word" if key.endswith("_at") else key + "_word"
    if d.get(wkey):
        t = _word_time(c, str(d[wkey]))
        if t is not None:
            return c.t(t - c.start)
    rel = float(d[key]) if key in d else c.duration * frac
    return c.t(rel)


def _code(line) -> str:
    """A code line: plain string, or a list of [class, text] segments (key, str, punc, com, kw, err, ok, dim, acc)."""
    if isinstance(line, str):
        return _e(line)
    return "".join(f'<span class="tk-{_e(cls)}">{_e(txt)}</span>' for cls, txt in line)


def _plain(line) -> str:
    return line if isinstance(line, str) else "".join(t for _, t in line)


def _tabs(tabs: list, sid: str = "", lock_tab: str = "") -> str:
    """Window tabs; with `sid` each tab gets the id `<sid>-tab<k>`; the tab named `lock_tab` carries a hidden
    open padlock (`<sid>-tlk`) that a scene can reveal when the file comes into play."""
    out = []
    for k, t in enumerate(tabs):
        name, active = (t, False) if isinstance(t, str) else (t.get("name", ""), bool(t.get("active")))
        tid = f' id="{sid}-tab{k}"' if sid else ""
        lk = _lock(f"{sid}-tlk", "open") if sid and lock_tab and name == lock_tab else ""
        out.append(f'<span class="pw-tab{" on" if active else ""}"{tid}>{_e(name)}{lk}</span>')
    return "".join(out)


def _tab_index(tabs: list, name: str) -> int:
    for k, t in enumerate(tabs):
        if (t if isinstance(t, str) else t.get("name", "")) == name:
            return k
    return -1


def _lock(sid: str, state: str = "open") -> str:
    """Small padlock (inline SVG background, see CSS): `open` amber with lifted shackle, `shut` green and closed."""
    return f'<span class="pw-lk {state}" id="{sid}"></span>'


def _file_chip(sid: str, name: str) -> str:
    """The guiding object (Leitobjekt): a file chip with a padlock; starts open (amber), can shut (green)."""
    return (f'<span class="pw-file" id="{sid}-file"><span class="pw-fico"></span><span class="pw-fname">{_e(name)}</span>'
            f'{_lock(sid + "-lko", "open")}{_lock(sid + "-lks", "shut")}</span>')


def _file_shut_tl(sid: str, t: float, green: str = "#4ADE80") -> list[str]:
    """The file chip locks: open padlock out, closed padlock in, border turns green, a green ring pulses once."""
    return [f'tl.to("#{sid}-lko",{{opacity:0,y:-6,duration:0.2}},{t:.3f});',
            f'tl.fromTo("#{sid}-lks",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{t + 0.05:.3f});',
            f'tl.to("#{sid}-file",{{borderColor:"{green}",backgroundColor:"rgba(74,222,128,0.12)",duration:0.25}},{t:.3f});',
            f'tl.fromTo("#{sid}-file",{{boxShadow:"0 0 0 0 rgba(74,222,128,0.6)"}},{{boxShadow:"0 0 0 22px rgba(74,222,128,0)",duration:0.7,ease:"power2.out"}},{t + 0.05:.3f});']


def _cursor(sid: str, x: int, y: int) -> str:
    return (f'<svg class="pw-cursor" id="{sid}-cur" viewBox="0 0 32 32" style="left:{x - 6}px;top:{y - 4}px">'
            f'<path d="M6 3 L26 17 L16 19 L21 29 L17 31 L12 21 L6 26 Z"/></svg>'
            f'<div class="pw-click" id="{sid}-clk" style="left:{x - 30}px;top:{y - 30}px"></div>')


def _cursor_tl(sid: str, t_move: float, t_click: float) -> list[str]:
    return [f'tl.fromTo("#{sid}-cur",{{x:-380,y:300,opacity:0}},{{x:0,y:0,opacity:1,duration:0.8,ease:"power2.inOut"}},{t_move:.3f});',
            f'tl.to("#{sid}-cur",{{scale:0.82,duration:0.09,yoyo:true,repeat:1}},{t_click:.3f});',
            f'tl.fromTo("#{sid}-clk",{{opacity:0.9,scale:0.2}},{{opacity:0,scale:1.4,duration:0.5,ease:"power2.out"}},{t_click:.3f});']


def _zoom_tl(sid: str, t0: float, scale: float, ox: float, oy: float, dur: float = 0.8) -> list[str]:
    return [f'tl.set("#{sid} .pw-zoom",{{transformOrigin:"{ox:.0f}px {oy:.0f}px"}},{t0 - 0.01:.3f});',
            f'tl.fromTo("#{sid} .pw-zoom",{{scale:1}},{{scale:{scale:.3f},duration:{dur:.2f},ease:"power2.inOut"}},{t0:.3f});']


def _enter(c: SceneCtx) -> list[str]:
    s = c.sid
    # no fade-out at the end: with the explainer layer the director keeps the old scene under the incoming one
    # (blende/iris); a self-fade here left an empty frame at every scene change (Q1, 01.11.2026)
    return [f'tl.fromTo("#{s} .pw-scene",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power2.out"}},{c.start:.3f});',
            f'tl.fromTo("#{s} .pw-cam",{{scale:1,y:8}},{{scale:1.045,y:-10,duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});']


def _wrap(c: SceneCtx, inner: str, cls: str, outside: str = "") -> str:
    """Scene box in the content zone; `outside` stays out of the zoom (e.g. the hook question)."""
    return (f'<div class="pw-scene {cls}" style="top:{c.zone_top}px;height:{c.zone_h}px">{outside}<div class="pw-cam" style="height:{c.zone_h}px">'
            f'<div class="pw-zoom" style="height:{c.zone_h}px">{inner}</div></div></div>')


# --- 1. Hook: the rule file, a marked line, the question -----------------------------------------------

def pw_hook(c: SceneCtx, d: dict) -> SceneOut:
    """CLAUDE.md in an editor window; the marker sweeps over the rule, cursor clicks it, zoom, question lands."""
    s, probs = c.sid, []
    lines = d.get("lines", [])[:6]
    focus = int(d.get("focus_line", min(2, len(lines) - 1)))
    q = d.get("question", "")
    chip = d.get("chip", "")
    _lim("pw_hook", "question", q, "question", probs)
    _lim("pw_hook", "chip", chip, "chip", probs)
    for i, ln in enumerate(lines):
        _lim("pw_hook", "line", _plain(ln), f"line {i + 1}", probs)
    bar_h, pad, lh = 70, 34, int(d.get("line_h", 70))
    tabs = d.get('tabs', [{'name': 'CLAUDE.md', 'active': True}])
    file_name = d.get("file", ".env")
    env_k = _tab_index(tabs, file_name)
    rows = "".join(f'<div class="pw-line" id="{s}-l{i}" style="top:{pad + i * lh}px"><span class="pw-ln">{i + 1}</span>'
                   f'<span class="pw-code big">{_code(ln)}</span></div>' for i, ln in enumerate(lines))
    fy = pad + focus * lh
    mark_w = min(720, 60 + len(_plain(lines[focus])) * 23) if lines else 400
    win_h = bar_h + pad * 2 + len(lines) * lh
    win_top = int(d.get("win_top", max(220, c.zone_h - win_h - 10)))   # window low in the zone, the question above it
    inner = f"""
<div class="pw-win" style="top:{win_top}px;height:{win_h}px">
  <div class="pw-bar"><i></i><i></i><i></i>{_tabs(tabs, s, file_name if d.get("file_icon", "lock") != "none" else "")}</div>
  <div class="pw-body">
    <div class="pw-mark" id="{s}-mk" style="top:{fy + 6}px;width:{mark_w}px"></div>{rows}
  </div>
</div>
{f'<div class="pw-chip amber" id="{s}-chip" style="top:{win_top + 9}px">{_e(chip)}</div>' if chip else ''}
{_cursor(s, 62 + mark_w - 30, win_top + bar_h + fy + 44)}"""
    out = SceneOut(html=_wrap(c, inner, "pw-hook", f'<div class="pw-question" id="{s}-q">{_e(q)}</div>'))
    t_lines = c.t(0.15)
    t_mark = _at(c, d, "mark_at", 0.22)
    t_env = _at(c, d, "env_at", 0.3)
    t_click = _at(c, d, "click_at", 0.34)
    t_q = _at(c, d, "question_at", 0.55)
    t_chip = _at(c, d, "chip_at", (t_q - c.start + 0.25) / max(0.1, c.duration))
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s} .pw-win",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{c.start:.3f});')
    for i in range(len(lines)):
        out.tl.append(f'tl.fromTo("#{s}-l{i}",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.22}},{c.t(t_lines - c.start + i * 0.12):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-mk",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{t_mark:.3f});')
    events = [c.start, t_mark, t_click, t_q]
    if env_k >= 0:      # the guiding file shows up: its tab lights amber, an open padlock appears
        out.tl.append(f'tl.fromTo("#{s}-tab{env_k}",{{backgroundColor:"rgba(251,191,36,0)",color:"{c.pal["muted"]}"}},'
                      f'{{backgroundColor:"rgba(251,191,36,0.20)",color:"{c.pal.get("signal_amber", "#FBBF24")}",duration:0.3}},{t_env:.3f});')
        if d.get("file_icon", "lock") != "none":    # file_icon "none": the tab only lights up (topics without a lock)
            out.tl.append(f'tl.fromTo("#{s}-tlk",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)"}},{t_env + 0.05:.3f});')
        events.append(t_env)
    out.tl += _cursor_tl(s, c.t(t_click - c.start - 0.8), t_click)
    out.tl += _zoom_tl(s, t_click, float(d.get("zoom", 1.06)), 432, win_top + bar_h + fy + 30)
    out.tl.append(f'tl.fromTo("#{s}-q",{{opacity:0,y:30,scale:0.94}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{t_q:.3f});')
    if chip:
        out.tl.append(f'tl.fromTo("#{s}-chip",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t_chip:.3f});')
        events.append(t_chip)
    out.events = events
    out.problems = probs
    return out


# --- 2. Docs page: the primary source, quoted and marked -----------------------------------------------

def pw_doc(c: SceneCtx, d: dict) -> SceneOut:
    """A documentation page (source name, title, faded text bars); one or two short verbatim quotes get the
    marker in turn; the translation appears under the page. Quotes must be verbatim and short (< 15 words)."""
    s, probs = c.sid, []
    quotes = d.get("quotes", [])[:2]
    _lim("pw_doc", "page_title", d.get("page_title", ""), "page_title", probs)
    _lim("pw_doc", "kicker", d.get("kicker", ""), "kicker", probs)
    _lim("pw_doc", "translation", d.get("translation", ""), "translation", probs)
    for i, q in enumerate(quotes):
        _lim("pw_doc", "quote", q, f"quote {i + 1}", probs)
    bars = lambda n, w0: "".join(f'<div class="pw-bar-line" style="width:{w0 - (k % 3) * 90}px"></div>' for k in range(n))
    qhtml = "".join(f'<div class="pw-quote" id="{s}-qt{i}"><span class="pw-qmark" id="{s}-qm{i}"></span><span class="pw-qtext">{_e(q)}</span></div>'
                    for i, q in enumerate(quotes))
    inner = f"""
<div class="pw-page" style="top:0">
  <div class="pw-kicker"><span class="pw-pdot"></span>{_e(d.get('kicker', 'Claude Code Docs'))}</div>
  <div class="pw-page-title" id="{s}-pt">{_e(d.get('page_title', ''))}<span class="pw-ptline" id="{s}-ptl"></span></div>
  {bars(1, 720)}{qhtml}
</div>
<div class="pw-trans" id="{s}-tr" style="top:{c.zone_h - 150}px"><span class="pw-flag">{_e(d.get('translation_label', 'Auf Deutsch'))}</span>{_e(d.get('translation', ''))}</div>"""
    out = SceneOut(html=_wrap(c, inner, "pw-doc"))
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s} .pw-page",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    if d.get("page_word") or d.get("page_at") is not None:     # the source is named: its title gets an accent underline
        tp = _at(c, d, "page_at", 0.06)
        out.tl.append(f'tl.fromTo("#{s}-ptl",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{tp:.3f});')
        events.append(tp)
    fracs = [0.12, 0.55]
    for i in range(len(quotes)):
        tq = _at(c, d, f"quote{i + 1}_at", fracs[i])
        out.tl.append(f'tl.fromTo("#{s}-qm{i}",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{tq:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-qt{i} .pw-qtext",{{color:"{c.pal["muted"]}"}},{{color:"{c.pal["text"]}",duration:0.3}},{tq:.3f});')
        events.append(tq)
    ttr = _at(c, d, "translation_at", 0.32)
    out.tl.append(f'tl.fromTo("#{s}-tr",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{ttr:.3f});')
    events.append(ttr)
    zt = c.t(c.duration * 0.55 - 0.1)
    out.tl += _zoom_tl(s, zt, 1.06, 432, 420, 1.2)
    out.events = events
    out.problems = probs
    return out


# --- 3. Lifecycle rail: where Claude Code runs a hook --------------------------------------------------

def pw_flow(c: SceneCtx, d: dict) -> SceneOut:
    """Vertical lifecycle rail; a token travels down and pings every point; one point gets the gate chip."""
    s, probs = c.sid, []
    nodes = d.get("nodes", [])[:5]
    gate = int(d.get("gate", 1))
    _lim("pw_flow", "headline", d.get("headline", ""), "headline", probs)
    _lim("pw_flow", "chip", d.get("chip", ""), "chip", probs)
    for i, n in enumerate(nodes):
        _lim("pw_flow", "node", n.get("label", ""), f"node {i + 1}", probs)
    headline = d.get("headline", "")
    top = int(d.get("top", 190 if headline else 40))
    step = int(d.get("step", 128 if headline else 152))
    items = []
    for i, n in enumerate(nodes):
        y = top + i * step
        hook = " hookpt" if n.get("hook") else ""
        items.append(f'<div class="pw-node{hook}" id="{s}-n{i}" style="top:{y}px"><span class="pw-dot"></span>'
                     f'<span class="pw-nlabel">{_e(n.get("label", ""))}</span>'
                     + (f'<span class="pw-ntag">{_e(n.get("tag", ""))}</span>' if n.get("tag") else "") + '</div>')
    rail_h = (len(nodes) - 1) * step
    gy = top + gate * step
    shell = d.get("shell_chip", "")
    _lim("pw_flow", "chip", shell, "shell_chip", probs)
    # chips beside the gate node: x 520, or with chip_auto right of its label (and tag); chip_x sets it directly
    gn = nodes[gate] if 0 <= gate < len(nodes) else {}
    auto_x = max(520, 101 + 64 + 30 + len(gn.get("label", "")) * 27 + ((30 + len(gn.get("tag", "")) * 17) if gn.get("tag") else 0) + 34)
    chip_x = int(d.get("chip_x", auto_x if d.get("chip_auto") else 520))
    inner = f"""
{f'<div class="h2 pw-h2">{_e(headline)}</div>' if headline else ''}
<div class="pw-railbox" style="top:{top - 34}px;height:{rail_h + 132}px"></div>
<div class="pw-rail" style="top:{top + 32}px;height:{rail_h}px"><div class="pw-rail-fill" id="{s}-rf"></div></div>
{''.join(items)}
<div class="pw-token" id="{s}-tok" style="top:{top + 14}px"></div>
<div class="pw-gate" id="{s}-gate" style="top:{gy - 14}px"></div>
{f'<div class="pw-chip shell" id="{s}-sh" style="top:{gy + 6}px;left:{chip_x}px"><span class="pw-prompt">$</span>{_e(shell)}</div>' if shell else ''}
<div class="pw-chip accent" id="{s}-chip" style="top:{gy + 6}px;left:{chip_x}px">{_e(d.get('chip', ''))}</div>"""
    out = SceneOut(html=_wrap(c, inner, "pw-flow"))
    out.tl += _enter(c)
    if headline:
        out.tl.append(f'tl.fromTo("#{s} .pw-h2",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.3}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .pw-railbox",{{opacity:0,scale:0.96}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{c.start:.3f});')
    for i in range(len(nodes)):
        out.tl.append(f'tl.fromTo("#{s}-n{i}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.25}},{c.t(0.15 + i * 0.12):.3f});')
    t0 = _at(c, d, "travel_at", 0.25)
    t1 = _at(c, d, "travel_end", 0.75)
    seg = (t1 - t0) / max(1, len(nodes) - 1)
    out.tl.append(f'tl.fromTo("#{s}-rf",{{scaleY:0}},{{scaleY:1,duration:{t1 - t0:.2f},ease:"none"}},{t0:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-tok",{{y:0,opacity:0}},{{opacity:1,duration:0.15}},{t0 - 0.15:.3f});')
    out.tl.append(f'tl.to("#{s}-tok",{{y:{rail_h},duration:{t1 - t0:.2f},ease:"none"}},{t0:.3f});')
    events = [c.start, t0]
    for i in range(len(nodes)):
        tp = round(t0 + i * seg, 3)
        out.tl.append(f'tl.fromTo("#{s}-n{i} .pw-dot",{{scale:1}},{{scale:1.5,duration:0.16,yoyo:true,repeat:1}},{tp:.3f});')
        out.tl.append(f'tl.to("#{s}-n{i} .pw-dot",{{backgroundColor:"{c.pal["accent"]}",duration:0.2}},{tp:.3f});')
    tg = _at(c, d, "gate_at", 0.8)
    if shell:           # "a shell command": the hook point shows what runs there, until the gate takes over
        tsh = _at(c, d, "shell_at", 0.2)
        out.tl.append(f'tl.fromTo("#{s}-sh",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{tsh:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-n{gate} .pw-dot",{{boxShadow:"0 0 0 0 rgba(167,139,250,0.7)"}},{{boxShadow:"0 0 0 26px rgba(167,139,250,0)",duration:0.7}},{tsh:.3f});')
        out.tl.append(f'tl.to("#{s}-sh",{{opacity:0,x:20,duration:0.2}},{max(tsh + 0.4, tg - 0.05):.3f});')
        events.append(tsh)
    out.tl.append(f'tl.fromTo("#{s}-gate",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power3.out"}},{tg:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-chip",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{tg + 0.15:.3f});')
    events += [round(t0 + seg * (len(nodes) // 2), 3), tg]
    out.events = events
    out.problems = probs
    return out


# --- 4. Editor: a config file is written line by line, the decisive line is marked ----------------------

def pw_editor(c: SceneCtx, d: dict) -> SceneOut:
    """Config file in an editor: lines type in, marker + cursor on the focus line, zoom, callout."""
    s, probs = c.sid, []
    lines = d.get("lines", [])[:12]
    focus = int(d.get("focus_line", 3))
    for i, ln in enumerate(lines):
        _lim("pw_editor", "line", _plain(ln), f"line {i + 1}", probs)
    _lim("pw_editor", "callout", d.get("callout", ""), "callout", probs)
    bar_h, pad, lh = 70, 26, int(d.get("line_h", 46))
    win_h = bar_h + pad * 2 + len(lines) * lh
    win_top = max(0, (c.zone_h - win_h - 120) // 2)
    rows = "".join(f'<div class="pw-line" id="{s}-l{i}" style="top:{pad + i * lh}px;height:{lh}px"><span class="pw-ln sm">{i + 1}</span>'
                   f'<span class="pw-code">{_code(ln)}</span></div>' for i, ln in enumerate(lines))
    fy = pad + focus * lh
    mark_w = min(740, 70 + len(_plain(lines[focus])) * 18) if lines else 400
    call_top = win_top + win_h + 30
    pre = d.get("pre_line")
    pre_html = ""
    if pre is not None:   # a second, quieter marker on the line the voice names first (e.g. the event name)
        pre_w = min(740, 70 + len(_plain(lines[int(pre)])) * 18)
        pre_html = f'<div class="pw-mark sm soft" id="{s}-pm" style="top:{pad + int(pre) * lh + 2}px;width:{pre_w}px"></div>'
    inner = f"""
<div class="pw-win" style="top:{win_top}px;height:{win_h}px">
  <div class="pw-bar"><i></i><i></i><i></i>{_tabs(d.get('tabs', []))}</div>
  <div class="pw-body">{pre_html}<div class="pw-mark sm" id="{s}-mk" style="top:{fy + 2}px;width:{mark_w}px"></div>{rows}</div>
</div>
{_cursor(s, 52 + mark_w - 20, win_top + bar_h + fy + 30)}"""
    callout = f'<div class="pw-callout" id="{s}-co" style="top:{call_top}px"><span class="pw-num">{_e(d.get("callout_num", "1"))}</span>{_e(d.get("callout", ""))}</div>'
    out = SceneOut(html=_wrap(c, inner, "pw-editor", callout))   # callout outside the zoom: never drifts onto the marker row
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s} .pw-win",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{c.start:.3f});')
    t_type0 = c.t(0.3)
    t_type1 = _at(c, d, "typed_at", 0.4)
    step = (t_type1 - t_type0) / max(1, len(lines))
    for i in range(len(lines)):
        ti = round(t_type0 + i * step, 3)
        out.tl.append(f'tl.fromTo("#{s}-l{i} .pw-code",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{max(0.12, step * 0.9):.2f},ease:"steps(12)"}},{ti:.3f});')
    t_mark = _at(c, d, "mark_at", 0.48)
    t_click = _at(c, d, "click_at", 0.58)
    t_call = _at(c, d, "callout_at", 0.66)
    events = [c.start, t_type0, t_mark, t_click, t_call]
    if pre is not None:
        t_pre = _at(c, d, "pre_at", 0.35)
        out.tl.append(f'tl.fromTo("#{s}-pm",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power2.out"}},{t_pre:.3f});')
        out.tl.append(f'tl.to("#{s}-pm",{{opacity:0.35,duration:0.3}},{max(t_pre + 0.5, t_mark - 0.1):.3f});')
        events.append(t_pre)
    out.tl.append(f'tl.fromTo("#{s}-mk",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{t_mark:.3f});')
    out.tl += _cursor_tl(s, c.t(t_click - c.start - 0.8), t_click)
    out.tl += _zoom_tl(s, t_click, float(d.get("zoom", 1.12)), 300, win_top + bar_h + fy + 20)
    out.tl.append(f'tl.fromTo("#{s}-co",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t_call:.3f});')
    out.events = events
    out.problems = probs
    return out


# --- 5. Terminal: the UI demonstration (core scene) ------------------------------------------------------

def pw_terminal(c: SceneCtx, d: dict) -> SceneOut:
    """Claude Code session in a terminal window, drawn as an animation and labelled "Animierte Darstellung" in the
    frame (Stefan, 2026-10-30: no screen recordings). `image` (a still) is still supported; then no label is drawn."""
    s, probs = c.sid, []
    lines = d.get("lines", [])[:9]
    focus = int(d.get("focus_line", max(0, len(lines) - 2)))
    image = d.get("image")
    _lim("pw_terminal", "title", d.get("title", ""), "title", probs)
    _lim("pw_terminal", "stamp", d.get("stamp", ""), "stamp", probs)
    _lim("pw_terminal", "annotation", d.get("annotation", ""), "annotation", probs)
    for i, ln in enumerate(lines):
        _lim("pw_terminal", "line", _plain(ln.get("text") if isinstance(ln, dict) else ln), f"line {i + 1}", probs)
    bar_h, pad, lh = 70, 30, 56
    win_h = int(d.get("height", bar_h + pad * 2 + max(6, len(lines)) * lh + 30))
    win_top = int(d.get("top", 40))
    note = "" if image else SCHEMATIC.get(c.lang, SCHEMATIC["en"])
    if image:
        body = f'<img class="pw-shot" src="{_e(image)}" alt="">'
        fy = int(d.get("focus_y", 200))
        fx = int(d.get("focus_x", 600))
    else:
        rows = []
        for i, ln in enumerate(lines):
            item = ln if isinstance(ln, dict) else {"text": ln}
            kind = item.get("kind", "out")
            rows.append(f'<div class="pw-tline {kind}" id="{s}-t{i}" style="top:{pad + i * lh}px">{_code(item.get("text", ""))}</div>')
        body = "".join(rows)
        fy = pad + focus * lh + lh // 2
        fx = int(d.get("focus_x", 640))
    stamp = d.get("stamp", "")
    file_name = d.get("file", "")
    inner = f"""
<div class="pw-win term" style="top:{win_top}px;height:{win_h}px">
  <div class="pw-bar"><i></i><i></i><i></i><span class="pw-title">{_e(d.get('title', 'claude'))}</span>{_file_chip(s, file_name) if file_name else ''}</div>
  <div class="pw-body">{'' if image else f'<div class="pw-mark {"red" if d.get("mark_tone", "red") == "red" else "acc"}" id="{s}-mk" style="top:{pad + focus * lh + 4}px;width:{d.get("mark_w", 760)}px"></div>'}{body}
    {f'<div class="pw-note">{_e(note)}</div>' if note else ''}</div>
</div>
{f'<div class="pw-stamp" id="{s}-st" style="top:{win_top + bar_h + pad + (focus + 1) * lh - 12}px">{_e(stamp)}</div>' if stamp else ''}
{f'<div class="pw-anno" id="{s}-an" style="top:{win_top + win_h + 34}px"><span class="pw-arrow">&#8627;</span>{_e(d["annotation"])}</div>' if d.get('annotation') else ''}
{_cursor(s, fx, win_top + bar_h + fy)}"""
    out = SceneOut(html=_wrap(c, inner, "pw-term"))
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s} .pw-win",{{opacity:0,y:40,scale:0.97}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    if not image:
        n = len(lines)
        for i, ln in enumerate(lines):
            item = ln if isinstance(ln, dict) else {"text": ln}
            ti = _at(c, item, "at", 0.08 + 0.55 * i / max(1, n - 1))
            if item.get("kind") == "prompt":
                out.tl.append(f'tl.fromTo("#{s}-t{i}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.9,ease:"steps(24)"}},{ti:.3f});')
            else:
                out.tl.append(f'tl.fromTo("#{s}-t{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.2}},{ti:.3f});')
            if item.get("kind") in ("prompt", "tool", "err"):
                events.append(ti)
        t_mark = _at(c, d, "mark_at", 0.66)
        out.tl.append(f'tl.fromTo("#{s}-mk",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{t_mark:.3f});')
        events.append(t_mark)
    t_click = _at(c, d, "click_at", 0.72)
    out.tl += _cursor_tl(s, c.t(t_click - c.start - 0.8), t_click)
    out.tl += _zoom_tl(s, t_click, float(d.get("zoom", 1.12)), fx, win_top + bar_h + fy)
    events.append(t_click)
    if file_name:       # the guiding file: appears (open, amber) when it is named, locks (green) when the edit is blocked
        t_fo = _at(c, d, "file_open_at", 0.12)
        t_fs = _at(c, d, "file_at", 0.72)
        out.tl.append(f'tl.fromTo("#{s}-file",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.8)"}},{t_fo:.3f});')
        out.tl += _file_shut_tl(s, t_fs)
        events += [t_fo, t_fs]
    if stamp:
        t_st = _at(c, d, "stamp_at", 0.78)
        out.tl.append(f'tl.fromTo("#{s}-st",{{opacity:0,scale:2.2,rotation:-10}},{{opacity:1,scale:1,rotation:-4,duration:0.26,ease:"power4.in"}},{t_st:.3f});')
        events.append(t_st)
    if d.get("annotation"):
        t_an = _at(c, d, "annotation_at", 0.86)
        out.tl.append(f'tl.fromTo("#{s}-an",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3}},{t_an:.3f});')
        events.append(t_an)
    out.events = events
    out.problems = probs
    return out


# --- 6. Compare: request vs. law ------------------------------------------------------------------------

def pw_compare(c: SceneCtx, d: dict) -> SceneOut:
    """Two stacked cards (file chip, verdict word, two rows each); the second card wins the accent."""
    s, probs = c.sid, []
    cards = []
    for k, side in enumerate(("top", "bottom")):
        cd = d.get(side) or {}
        _lim("pw_compare", "title", cd.get("title", ""), f"{side}.title", probs)
        _lim("pw_compare", "verdict", cd.get("verdict", ""), f"{side}.verdict", probs)
        rows = []
        for j, r in enumerate(cd.get("rows", [])[:2]):
            _lim("pw_compare", "row", r, f"{side}.row", probs)
            rows.append(f'<div class="pw-crow" id="{s}-{side}-{j}"><span class="pw-cdot"></span>{_e(r)}</div>')
        lock = _lock(f"{s}-lk", "shut") if side == "bottom" and (d.get("lock_word") or d.get("lock_at") is not None) else ""
        cards.append(f'<div class="pw-ccard {side}" id="{s}-{side}"><div class="pw-chead"><span class="pw-fchip">{_e(cd.get("title", ""))}</span>'
                     f'<span class="pw-vwrap">{lock}<span class="pw-verdict" id="{s}-{side}-v">{_e(cd.get("verdict", ""))}</span></span></div>{"".join(rows)}</div>')
    inner = f'<div class="pw-cstack">{cards[0]}<div class="pw-vs" id="{s}-vs">vs</div>{cards[1]}</div>'
    out = SceneOut(html=_wrap(c, inner, "pw-compare"))
    out.tl += _enter(c)
    ta = _at(c, d, "top_at", 0.04)
    tb = _at(c, d, "bottom_at", 0.48)
    events = [c.start]
    # the second card waits as a faint outline from the start, so the frame is never half empty
    out.tl.append(f'tl.fromTo("#{s}-bottom",{{opacity:0}},{{opacity:0.22,duration:0.4}},{c.start:.3f});')
    for side, at in (("top", ta), ("bottom", tb)):
        out.tl.append(f'tl.fromTo("#{s}-{side}",{{opacity:{0.22 if side == "bottom" else 0},y:{14 if side == "bottom" else 40}}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-{side}-v",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.28,ease:"power4.in"}},{c.t(at - c.start + 0.35):.3f});')
        row_words = (d.get(side) or {}).get("row_words") or []     # optional: one spoken word per row
        for j in range(len((d.get(side) or {}).get("rows", [])[:2])):
            tj = c.t(at - c.start + 0.75 + j * 0.55)
            if j < len(row_words) and row_words[j]:
                wt = _word_time(c, str(row_words[j]))
                if wt is not None:
                    tj = c.t(max(wt, at + 0.4) - c.start)
            out.tl.append(f'tl.fromTo("#{s}-{side}-{j}",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.25}},{tj:.3f});')
            events.append(tj)
        events.append(at)
    out.tl.append(f'tl.fromTo("#{s}-vs",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.25}},{c.t(tb - c.start - 0.3):.3f});')
    out.tl.append(f'tl.to("#{s}-top",{{opacity:0.55,duration:0.4}},{c.t(tb - c.start + 0.2):.3f});')
    if d.get("lock_word") or d.get("lock_at") is not None:     # "it takes effect": the law card gets the closed padlock
        tl_ = _at(c, d, "lock_at", 0.78)
        out.tl.append(f'tl.fromTo("#{s}-lk",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{tl_:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-bottom",{{boxShadow:"0 0 0 0 rgba(167,139,250,0.55)"}},{{boxShadow:"0 0 0 26px rgba(167,139,250,0)",duration:0.8,ease:"power2.out"}},{tl_:.3f});')
        events.append(tl_)
    out.events = events
    out.problems = probs
    return out


# --- 7. Steps: what to do, with the exact names to type ---------------------------------------------------

def pw_steps(c: SceneCtx, d: dict) -> SceneOut:
    """Up to five steps (key-cap number, title, mono chip with the exact name); each lights up on its word.
    Four or five steps use a compact row (lists of commands, shortcuts, settings)."""
    s, probs = c.sid, []
    if len(d.get("steps", [])) > 5:
        probs.append(f"pw_steps: {len(d['steps'])} steps > 5 (split into two scenes)")
    steps = d.get("steps", [])[:5]
    compact = len(steps) > 3
    _lim("pw_steps", "headline", d.get("headline", ""), "headline", probs)
    rows = []
    for i, st in enumerate(steps):
        _lim("pw_steps", "title", st.get("title", ""), f"step {i + 1}.title", probs)
        _lim("pw_steps", "code", st.get("code", ""), f"step {i + 1}.code", probs)
        rows.append(f'<div class="pw-step" id="{s}-s{i}"><span class="pw-key">{i + 1}</span><div class="pw-stext">'
                    f'<div class="pw-stitle">{_e(st.get("title", ""))}</div><div class="pw-scode">{_e(st.get("code", ""))}</div></div></div>')
    headline = d.get("headline", "")
    cmp = " compact" if compact else ""
    inner = ((f'<div class="h2 pw-h2">{_e(headline)}</div><div class="pw-steps{cmp}">' if headline else
              f'<div class="pw-steps full{cmp}" style="height:{c.zone_h}px">') + f'{"".join(rows)}<div class="pw-sline"></div></div>')
    out = SceneOut(html=_wrap(c, inner, "pw-stepsc"))
    out.tl += _enter(c)
    if headline:
        out.tl.append(f'tl.fromTo("#{s} .pw-h2",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.3}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .pw-step",{{opacity:0,y:30}},{{opacity:0.25,y:0,duration:0.35,stagger:0.08,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    n = max(1, len(steps))
    for i, st in enumerate(steps):
        at = _at(c, st, "at", 0.1 + 0.8 * i / n)
        out.tl.append(f'tl.fromTo("#{s}-s{i}",{{opacity:0.25}},{{opacity:1,duration:0.35}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-s{i} .pw-key",{{backgroundColor:"{c.pal["surface"]}",color:"{c.pal["muted"]}"}},{{backgroundColor:"{c.pal["accent"]}",color:"{c.pal["bg"]}",duration:0.25}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-s{i} .pw-scode",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.5,ease:"steps(16)"}},{at + 0.15:.3f});')
        events.append(at)
    out.events = events
    out.problems = probs
    return out


# --- 8. Close in the action: the protected file, the rule, the brand -------------------------------------

def pw_close(c: SceneCtx, d: dict) -> SceneOut:
    """Small terminal with the blocked edit and a lock badge, the statement, then the brand line (>= 3 s)."""
    s, probs = c.sid, []
    lines = d.get("lines", [])[:3]
    _lim("pw_close", "statement", d.get("statement", ""), "statement", probs)
    _lim("pw_close", "badge", d.get("badge", ""), "badge", probs)
    _lim("pw_close", "claim", d.get("claim", ""), "claim", probs)
    for i, ln in enumerate(lines):
        _lim("pw_close", "line", _plain(ln.get("text") if isinstance(ln, dict) else ln), f"line {i + 1}", probs)
    rows = "".join(f'<div class="pw-tline {(ln.get("kind", "out") if isinstance(ln, dict) else "out")}" style="top:{24 + i * 54}px">'
                   f'{_code(ln.get("text") if isinstance(ln, dict) else ln)}</div>' for i, ln in enumerate(lines))
    win_h = 70 + 48 + len(lines) * 54 + 56          # last row keeps the animation label clear of the code
    note = SCHEMATIC.get(c.lang, SCHEMATIC["en"])
    inner = f"""
<div class="pw-win term small" style="top:0;height:{win_h}px">
  <div class="pw-bar"><i></i><i></i><i></i><span class="pw-title">{_e(d.get('title', 'claude'))}</span></div>
  <div class="pw-body">{rows}<div class="pw-note">{_e(note)}</div></div>
</div>
<div class="pw-lock{' ' + _e(d['badge_tone']) if d.get('badge_tone') else ''}" id="{s}-lock" style="top:10px">{'' if d.get('badge_icon') == 'none' else ('<span class="pw-checkico"></span>' if d.get('badge_icon') == 'check' else '<span class="pw-lockico"></span>')}{_e(d.get('badge', ''))}</div>
<div class="pw-statement" id="{s}-stm" style="top:{win_h + 90}px">{_e(d.get('statement', ''))}</div>
<div class="pw-brand" id="{s}-br"><span class="pw-brandmark"></span><span class="pw-brandname">{_e(d.get('brand', 'Promptwerk'))}</span><span class="pw-claim">{_e(d.get('claim', ''))}</span></div>"""
    out = SceneOut(html=_wrap(c, inner, "pw-close"))
    out.tl += [l for l in _enter(c) if "opacity:0,duration:0.16" not in l]    # the close holds to the last frame
    t_lock = _at(c, d, "badge_at", 0.5 / max(0.5, c.duration))      # optional badge_word
    t_stm = _at(c, d, "statement_at", 0.12)
    t_brand = _at(c, d, "brand_at", 0.5)
    out.tl.append(f'tl.fromTo("#{s} .pw-win",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-lock",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t_lock:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-stm",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{t_stm:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-br",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t_brand:.3f});')
    out.events = [c.start, t_lock, t_stm, t_brand]
    out.problems = probs
    return out


TEMPLATES = {
    "pw_hook": pw_hook,
    "pw_doc": pw_doc,
    "pw_flow": pw_flow,
    "pw_editor": pw_editor,
    "pw_terminal": pw_terminal,
    "pw_compare": pw_compare,
    "pw_steps": pw_steps,
    "pw_close": pw_close,
}


HOOK_SCENE_TYPES = ["pw_hook"]


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int = 290, zone_h: int = 810, flat: bool = False) -> str:
    """Stylesheet for the pw_* scenes plus overrides of the shared persistent layer (logo, status bar)."""
    acc, text, surf, muted, bg = pal["accent"], pal["text"], pal["surface"], pal["muted"], pal["bg"]
    win, term = pal.get("window", "#1E2029"), pal.get("terminal", "#101218")
    hair = pal.get("hairline", "rgba(248,250,252,0.10)")
    green, red, amber, on = pal.get("signal_green", "#4ADE80"), pal.get("signal_red", "#F87171"), pal.get("signal_amber", "#FBBF24"), pal.get("on_signal", "#0B0C10")
    k = pal.get("code_key", "#C4B5FD"), pal.get("code_str", "#86EFAC"), pal.get("code_punc", "#94A3B8"), pal.get("code_com", "#7C8294")
    return f"""
/* --- Promptwerk (pw_*) --- */
.pw-scene{{position:absolute;left:108px;width:864px;}}
.pw-cam,.pw-zoom{{position:absolute;left:0;top:0;width:864px;transform-origin:50% 50%;will-change:transform;}}
.pw-win{{position:absolute;left:0;width:864px;background:{win};border:1px solid {hair};border-radius:22px;box-shadow:0 2px 4px rgba(0,0,0,0.3),0 30px 70px rgba(0,0,0,0.45);overflow:hidden;text-align:left;}}
.pw-win.term{{background:{term};}}
.pw-bar{{height:70px;display:flex;align-items:center;padding:0 22px;gap:10px;background:color-mix(in srgb,{text} 4%,transparent);border-bottom:1px solid {hair};}}
.pw-bar i{{display:inline-block;width:15px;height:15px;border-radius:50%;background:{muted};opacity:0.45;margin-right:2px;}}
.pw-tab{{margin-left:10px;font-family:'FN {mono}';font-size:28px;color:{muted};padding:8px 16px;border-radius:10px;white-space:nowrap;}}
.pw-tab.on{{color:{text};background:color-mix(in srgb,{acc} 16%,transparent);}}
.pw-title{{margin-left:12px;font-family:'FN {mono}';font-size:28px;color:{muted};white-space:nowrap;}}
.pw-body{{position:relative;height:calc(100% - 70px);}}
.pw-line{{position:absolute;left:0;right:0;height:46px;display:flex;align-items:center;white-space:pre;}}
.pw-ln{{width:72px;flex:0 0 72px;text-align:right;padding-right:22px;font-family:'FN {mono}';font-size:30px;color:{muted};opacity:0.6;}}
.pw-ln.sm{{width:60px;flex:0 0 60px;padding-right:18px;font-size:26px;}}
.pw-code{{font-family:'FN {mono}';font-size:30px;color:{text};white-space:pre;}}
.pw-code.big{{font-size:36px;}}
.pw-hook .pw-line{{height:76px;}}
.tk-key{{color:{k[0]};}} .tk-str{{color:{k[1]};}} .tk-punc{{color:{k[2]};}} .tk-com{{color:{k[3]};}} .tk-kw{{color:{acc};font-weight:600;}}
.tk-err{{color:{red};font-weight:600;}} .tk-ok{{color:{green};}} .tk-dim{{color:{muted};}} .tk-acc{{color:{acc};}}
.pw-mark{{position:absolute;left:62px;height:58px;border-radius:10px;background:color-mix(in srgb,{acc} 30%,transparent);border-left:6px solid {acc};transform-origin:0 50%;}}
.pw-mark.sm{{left:52px;height:42px;}}
.pw-mark.red{{left:14px;height:48px;background:color-mix(in srgb,{red} 18%,transparent);border-left-color:{red};}}
.pw-chip{{position:absolute;right:28px;padding:10px 24px;border-radius:999px;font-family:'FN {display}';font-weight:700;font-size:32px;white-space:nowrap;box-shadow:0 10px 30px rgba(0,0,0,0.35);}}
.pw-chip.amber{{background:{amber};color:{on};}}
.pw-chip.accent{{background:{acc};color:{bg};right:auto;}}
.pw-question{{position:absolute;left:0;top:0;width:864px;text-align:center;font-family:'FN {display}';font-weight:{display_w};font-size:80px;line-height:1.04;letter-spacing:-0.02em;color:{text};}}
.pw-cursor{{position:absolute;width:46px;height:46px;fill:#fff;stroke:#111;stroke-width:1.5;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.6));z-index:5;}}
.pw-click{{position:absolute;width:60px;height:60px;border-radius:50%;border:4px solid {acc};opacity:0;z-index:4;}}
.pw-note{{position:absolute;right:16px;bottom:14px;font-family:'FN {mono}';font-size:26px;color:{muted};background:color-mix(in srgb,{bg} 80%,transparent);border:1px solid {hair};padding:6px 14px;border-radius:10px;white-space:nowrap;}}
/* docs page */
.pw-page{{position:absolute;left:0;width:864px;background:{win};border:1px solid {hair};border-radius:22px;padding:38px 44px 30px;text-align:left;box-shadow:0 30px 70px rgba(0,0,0,0.4);}}
.pw-kicker{{font-family:'FN {mono}';font-size:30px;color:{acc};margin-bottom:12px;}}
.pw-page-title{{font-family:'FN {display}';font-weight:800;font-size:46px;line-height:1.12;color:{text};margin-bottom:26px;}}
.pw-bar-line{{height:16px;border-radius:8px;background:color-mix(in srgb,{text} 9%,transparent);margin:14px 0;}}
.pw-quote{{position:relative;margin:26px 0 22px;padding:10px 16px;}}
.pw-qmark{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:10px;background:color-mix(in srgb,{acc} 26%,transparent);border-left:6px solid {acc};transform-origin:0 50%;}}
.pw-qtext{{position:relative;font-size:42px;line-height:1.25;font-weight:600;color:{muted};}}
.pw-trans{{position:absolute;left:0;width:864px;top:668px;background:{surf};border-radius:20px;padding:24px 30px;font-size:40px;line-height:1.2;font-weight:600;color:{text};text-align:left;border:1px solid {hair};}}
.pw-flag{{display:block;font-family:'FN {mono}';font-size:28px;font-weight:400;color:{muted};margin-bottom:8px;}}
/* lifecycle rail */
.pw-h2{{position:absolute;left:0;top:0;width:864px;font-size:58px;text-align:center;}}
.pw-rail{{position:absolute;left:130px;width:6px;border-radius:3px;background:color-mix(in srgb,{text} 14%,transparent);overflow:hidden;}}
.pw-rail-fill{{width:100%;height:100%;background:{acc};transform-origin:50% 0;}}
.pw-node{{position:absolute;left:104px;height:64px;display:flex;align-items:center;gap:30px;}}
.pw-dot{{width:58px;height:58px;border-radius:50%;background:{surf};border:4px solid color-mix(in srgb,{acc} 60%,transparent);flex:0 0 58px;}}
.pw-nlabel{{font-family:'FN {mono}';font-size:40px;color:{text};white-space:nowrap;}}
.pw-node.hookpt .pw-nlabel{{color:{acc};font-weight:700;}}
.pw-ntag{{font-size:30px;color:{muted};white-space:nowrap;}}
.pw-token{{position:absolute;left:117px;width:32px;height:32px;border-radius:50%;background:{text};border:6px solid {acc};z-index:3;}}
.pw-gate{{position:absolute;left:84px;width:420px;height:92px;border:4px solid {acc};border-radius:20px;transform-origin:0 50%;}}
/* callout, stamp, annotation */
.pw-callout{{position:absolute;left:150px;display:flex;align-items:center;gap:18px;background:{acc};color:{bg};font-weight:700;font-size:36px;padding:16px 28px 16px 16px;border-radius:18px;white-space:nowrap;box-shadow:0 14px 34px rgba(0,0,0,0.4);}}
.pw-callout::before{{content:"";position:absolute;left:60px;top:-14px;border:14px solid transparent;border-top:0;border-bottom-color:{acc};}}
.pw-num{{display:inline-flex;width:52px;height:52px;border-radius:50%;background:{bg};color:{acc};align-items:center;justify-content:center;font-family:'FN {mono}';font-size:30px;}}
.pw-tline{{position:absolute;left:28px;right:20px;height:56px;display:flex;align-items:center;font-family:'FN {mono}';font-size:32px;color:{text};white-space:pre;}}
.pw-tline.prompt{{color:{text};}}
.pw-tline.tool{{color:{text};}}
.pw-tline.dim{{color:{muted};}}
.pw-tline.err{{color:{red};font-weight:600;}}
.pw-shot{{width:100%;height:100%;object-fit:cover;object-position:top left;display:block;}}
.pw-stamp{{position:absolute;right:20px;font-family:'FN {mono}';font-weight:800;font-size:64px;color:{acc};border:7px solid {acc};border-radius:18px;padding:4px 24px;background:color-mix(in srgb,{term} 85%,transparent);z-index:6;}}
.pw-anno{{position:absolute;left:0;width:864px;text-align:center;font-size:40px;font-weight:600;color:{text};}}
.pw-arrow{{color:{acc};margin-right:14px;font-family:'FN {mono}';}}
/* compare */
.pw-cstack{{position:absolute;left:0;top:0;height:100%;width:864px;display:flex;flex-direction:column;gap:26px;align-items:stretch;justify-content:center;}}
.pw-ccard{{background:{win};border:1px solid {hair};border-radius:22px;padding:32px 40px;text-align:left;}}
.pw-ccard.bottom{{border:3px solid {acc};}}
.pw-chead{{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;}}
.pw-fchip{{font-family:'FN {mono}';font-size:36px;color:{text};background:color-mix(in srgb,{text} 7%,transparent);padding:8px 18px;border-radius:12px;}}
.pw-verdict{{font-family:'FN {display}';font-weight:800;font-size:76px;color:{muted};}}
.pw-ccard.bottom .pw-verdict{{color:{acc};}}
.pw-crow{{display:flex;align-items:center;gap:20px;font-size:46px;line-height:1.3;color:{text};padding:10px 0;}}
.pw-cdot{{width:20px;height:20px;border-radius:50%;border:4px solid {muted};flex:0 0 20px;}}
.pw-ccard.bottom .pw-cdot{{background:{acc};border-color:{acc};}}
.pw-vs{{align-self:center;font-family:'FN {mono}';font-size:34px;color:{muted};margin:-6px 0;}}
/* steps */
.pw-steps{{position:absolute;left:0;top:170px;width:864px;display:flex;flex-direction:column;gap:34px;}}
.pw-step{{position:relative;display:flex;align-items:center;gap:30px;background:{win};border:1px solid {hair};border-radius:22px;padding:34px 34px;text-align:left;z-index:1;}}
.pw-key{{flex:0 0 92px;width:92px;height:92px;border-radius:18px;background:{surf};color:{muted};font-family:'FN {mono}';font-weight:700;font-size:48px;display:flex;align-items:center;justify-content:center;border-bottom:6px solid color-mix(in srgb,{bg} 60%,transparent);}}
.pw-stitle{{font-size:44px;font-weight:700;color:{text};line-height:1.15;}}
.pw-scode{{margin-top:10px;font-family:'FN {mono}';font-size:32px;color:{acc};white-space:nowrap;}}
.pw-sline{{display:none;}}
/* close */
.pw-win.small{{left:42px;width:780px;}}
.pw-lock{{position:absolute;right:58px;display:flex;align-items:center;gap:14px;background:{green};color:{on};font-weight:700;font-size:32px;padding:12px 24px;border-radius:999px;box-shadow:0 12px 30px rgba(0,0,0,0.4);z-index:3;}}
.pw-lockico{{width:22px;height:18px;border-radius:4px;background:{on};position:relative;margin-top:8px;}}
.pw-lockico::before{{content:"";position:absolute;left:3px;top:-14px;width:10px;height:14px;border:4px solid {on};border-bottom:0;border-radius:10px 10px 0 0;}}
.pw-statement{{position:absolute;left:0;width:864px;text-align:center;font-family:'FN {display}';font-weight:{display_w};font-size:68px;line-height:1.08;letter-spacing:-0.02em;color:{text};}}
.pw-brand{{position:absolute;left:0;width:864px;bottom:0;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:18px;}}
.pw-brandmark{{width:58px;height:58px;border-radius:15px;background:{acc};position:relative;}}
.pw-brandmark::before{{content:"";position:absolute;left:14px;top:18px;width:14px;height:14px;border-right:5px solid {bg};border-bottom:5px solid {bg};transform:rotate(-45deg);}}
.pw-brandmark::after{{content:"";position:absolute;left:30px;top:36px;width:16px;height:5px;background:{bg};border-radius:2px;}}
.pw-brandname{{font-family:'FN {display}';font-weight:800;font-size:60px;letter-spacing:-0.02em;color:{text};}}
.pw-claim{{flex:0 0 100%;text-align:center;font-size:36px;color:{muted};}}
/* shared persistent layer, Promptwerk look */
.logo-inner .mark{{position:relative;width:44px;height:44px;border-radius:12px;background:{acc};}}
.logo-inner .mark::before{{content:"";position:absolute;left:9px;top:13px;width:11px;height:11px;border-right:4px solid {bg};border-bottom:4px solid {bg};transform:rotate(-45deg);}}
.logo-inner .mark::after{{content:"";position:absolute;left:22px;top:28px;width:13px;height:4px;background:{bg};border-radius:2px;}}
.logo-inner .wordmark{{font-family:'FN {display}';font-weight:800;font-size:36px;letter-spacing:-0.01em;}}
#status{{background:{term};border:1px solid {hair};border-left:6px solid {acc};border-radius:16px;font-family:'FN {mono}';}}
.st-file{{font-family:'FN {mono}';color:{text};}}
.st-icon{{color:{acc};}}
.st{{font-family:'FN {mono}';font-weight:500;}}
.st-ok{{color:{green};}}
.st-accent{{color:{acc};}}
/* --- Q1 (31.10.2026): depth, larger type, the .env as guiding object with a padlock --- */
.pw-win{{box-shadow:0 2px 4px rgba(0,0,0,0.35),0 40px 90px rgba(0,0,0,0.55),0 0 0 1px color-mix(in srgb,{acc} 10%,transparent);}}
.pw-win::before{{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,transparent,color-mix(in srgb,{acc} 70%,transparent),transparent);z-index:2;}}
.pw-lk{{display:inline-block;width:30px;height:30px;margin-left:12px;vertical-align:-5px;background:center/contain no-repeat;flex:none;}}
.pw-lk.open{{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='10.5' width='16' height='11.5' rx='3' fill='%23FBBF24'/%3E%3Cpath d='M8 10.5V7a4 4 0 0 1 7.6-1.8' fill='none' stroke='%23FBBF24' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E");}}
.pw-lk.shut{{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='10.5' width='16' height='11.5' rx='3' fill='%234ADE80'/%3E%3Cpath d='M8 10.5V7a4 4 0 0 1 8 0v3.5' fill='none' stroke='%234ADE80' stroke-width='2.6'/%3E%3C/svg%3E");}}
.pw-file{{position:relative;margin-left:auto;display:inline-flex;align-items:center;gap:10px;padding:6px 14px 6px 12px;border-radius:12px;border:2px solid {amber};background:rgba(251,191,36,0.12);font-family:'FN {mono}';font-size:28px;color:{text};white-space:nowrap;}}
.pw-fico{{width:22px;height:28px;background:{muted};clip-path:polygon(0 0,68% 0,100% 30%,100% 100%,0 100%);opacity:0.9;}}
.pw-file .pw-lk{{margin-left:4px;}}
.pw-file .pw-lk.shut{{position:absolute;right:14px;top:50%;margin-top:-15px;opacity:0;}}
.pw-mark.acc{{left:14px;height:48px;}}
.pw-lock.accent{{background:{acc};color:{bg};}}
.pw-lock.muted{{background:{surf};color:{text};border:1px solid {hair};}}
.pw-checkico{{width:22px;height:12px;border-left:5px solid currentColor;border-bottom:5px solid currentColor;transform:rotate(-45deg);margin:-6px 4px 0 2px;}}
.pw-mark.soft{{background:color-mix(in srgb,{acc} 14%,transparent);border-left-color:color-mix(in srgb,{acc} 55%,transparent);}}
.pw-pdot{{display:inline-block;width:14px;height:14px;border-radius:50%;background:{acc};margin-right:12px;vertical-align:2px;}}
.pw-ptline{{display:block;height:6px;width:260px;margin-top:14px;border-radius:3px;background:{acc};transform-origin:0 50%;}}
.pw-question{{font-size:74px;}}
.pw-hook .pw-line{{height:70px;}}
.pw-page-title{{font-size:40px;white-space:nowrap;margin-bottom:18px;}}
.pw-quote{{margin:20px 0 14px;}}
.pw-trans{{padding:20px 30px;font-size:40px;box-shadow:0 24px 60px rgba(0,0,0,0.5);}}
.pw-cstack{{height:calc(100% - 50px);gap:18px;}}
.pw-ccard{{padding:30px 40px;}}
.pw-railbox{{position:absolute;left:40px;width:784px;border-radius:26px;background:color-mix(in srgb,{win} 88%,transparent);border:1px solid {hair};box-shadow:0 40px 90px rgba(0,0,0,0.5);}}
.pw-dot{{width:64px;height:64px;flex:0 0 64px;}}
.pw-nlabel{{font-size:44px;}}
.pw-node{{left:101px;height:70px;}}
.pw-token{{left:120px;}}
.pw-chip.shell{{background:{term};color:{text};border:2px solid {acc};font-family:'FN {mono}';font-weight:500;}}
.pw-prompt{{color:{acc};margin-right:12px;}}
.pw-ccard{{padding:38px 44px;box-shadow:0 30px 80px rgba(0,0,0,0.45);}}
.pw-crow{{font-size:48px;}}
.pw-vwrap{{display:inline-flex;align-items:center;gap:18px;}}
.pw-vwrap .pw-lk{{width:54px;height:54px;margin:0;opacity:0;}}
.pw-steps.full{{top:0;justify-content:center;gap:30px;}}
.pw-step{{padding:40px 36px;box-shadow:0 26px 70px rgba(0,0,0,0.45);}}
.pw-stitle{{font-size:46px;}}
.pw-scode{{font-size:34px;}}
.pw-steps.compact{{gap:16px;}}
.pw-steps.compact .pw-step{{padding:20px 30px;gap:26px;}}
.pw-steps.compact .pw-key{{flex:0 0 72px;width:72px;height:72px;font-size:38px;border-radius:16px;}}
.pw-steps.compact .pw-stitle{{font-size:40px;}}
.pw-steps.compact .pw-scode{{font-size:30px;margin-top:6px;}}
/* explainer head, Promptwerk: kicker left, scene title large and centred (max two lines), as in the Scutoria reference */
#root .xtitle{{font-size:64px;line-height:1.04;letter-spacing:-0.02em;white-space:normal;text-wrap:balance;text-align:center;margin-top:12px;}}
/* status bar: file glyph and padlock follow the state (amber open, green shut) */
#root .st-icon{{display:inline-block;width:24px;height:30px;font-size:0;background:{acc};clip-path:polygon(0 0,68% 0,100% 30%,100% 100%,0 100%);}}
#root .st-amber::before,#root .st-ok::before{{content:"";display:inline-block;width:30px;height:30px;margin-right:12px;background:center/contain no-repeat;}}
#root .st-amber::before{{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='10.5' width='16' height='11.5' rx='3' fill='%23FBBF24'/%3E%3Cpath d='M8 10.5V7a4 4 0 0 1 7.6-1.8' fill='none' stroke='%23FBBF24' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E");}}
#root .st-ok::before{{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='10.5' width='16' height='11.5' rx='3' fill='%234ADE80'/%3E%3Cpath d='M8 10.5V7a4 4 0 0 1 8 0v3.5' fill='none' stroke='%234ADE80' stroke-width='2.6'/%3E%3C/svg%3E");}}
/* ground with depth: layered light over the dot grid (the LAYER below adds floor, code shards, story light) */
#root #bg{{background-color:#13141c;background-image:radial-gradient(rgba(248,250,252,0.075) 1.6px,transparent 2.3px),
  radial-gradient(ellipse 75% 42% at 18% 14%,color-mix(in srgb,{acc} 24%,transparent),transparent 72%),
  radial-gradient(ellipse 70% 40% at 92% 78%,rgba(99,102,241,0.18),transparent 70%),
  linear-gradient(180deg,#1b1c29 0%,#15161f 55%,#0e0f15 100%);background-size:48px 48px,100% 100%,100% 100%,100% 100%;}}
#root #light{{background:radial-gradient(ellipse at 50% 50%,color-mix(in srgb,{acc} 20%,transparent) 0%,transparent 55%);}}
"""


# --- brand-wide depth layer (fn.render.brand_scenes LAYER contract) ---------------------------------------

_TONE_GLOW = {"amber": "amber", "red": "red", "ok": "green", "accent": "violet", "muted": "violet"}
# code shards: (x, y, width, depth 0 far .. 2 near, colour key); fixed, so every render is identical
_SHARDS = [(70, 260, 260, 0, "acc"), (720, 330, 210, 0, "key"), (160, 620, 180, 0, "str"), (800, 760, 240, 0, "acc"),
           (60, 1010, 220, 0, "key"), (760, 1180, 180, 0, "str"), (220, 1460, 260, 0, "acc"), (700, 1650, 200, 0, "key"),
           (-40, 420, 300, 1, "acc"), (880, 560, 260, 1, "key"), (-60, 900, 240, 1, "str"), (900, 1280, 280, 1, "acc"),
           (40, 1720, 320, 1, "key"), (-120, 160, 420, 2, "acc"), (860, 1500, 380, 2, "acc")]


def LAYER(plan, brand, project_dir, captions) -> dict:
    """Code-only background with depth, under all scenes: a perspective floor grid that slowly moves toward the viewer,
    blurred code shards in three depth layers drifting at different speeds (parallax), film grain, edge shadow, and a
    story light behind the stage whose colour follows the status bar (amber open, violet set up, green protected)."""
    pal = dict(getattr(brand, "palette", {}) or {})
    acc = pal.get("accent", "#A78BFA")
    col = {"acc": acc, "key": pal.get("code_key", "#C4B5FD"), "str": pal.get("code_str", "#86EFAC")}
    glow = {"violet": acc, "amber": pal.get("signal_amber", "#FBBF24"), "green": pal.get("signal_green", "#4ADE80"),
            "red": pal.get("signal_red", "#F87171")}
    look = {0: ("blur(5px)", 0.16, 18), 1: ("blur(2.5px)", 0.13, 24), 2: ("blur(14px)", 0.12, 46)}
    shards = []
    for k, (x, y, w, depth, ck) in enumerate(_SHARDS):
        blur, op, h = look[depth]
        shards.append(f'<i class="pwd-sh d{depth}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                      f'background:{col[ck]};opacity:{op};filter:{blur}"></i>')
    glows = "".join(f'<div class="pwd-glow" id="pwd-g-{n}" style="background:radial-gradient(ellipse at 50% 50%,{c}55 0%,{c}18 35%,transparent 68%)"></div>'
                    for n, c in glow.items())
    grain = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E"
             "%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E"
             "%3Crect width='240' height='240' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E")
    html_ = f"""<div id="pwd" style="position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none">
<style>
#pwd-floor{{position:absolute;left:-60%;width:220%;top:1180px;height:1500px;transform:perspective(620px) rotateX(72deg);transform-origin:50% 0;
  background-image:linear-gradient(color-mix(in srgb,{acc} 34%,transparent) 2px,transparent 2px),linear-gradient(90deg,color-mix(in srgb,{acc} 34%,transparent) 2px,transparent 2px);
  background-size:120px 120px;-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%,#000 100%);mask-image:linear-gradient(180deg,transparent 0%,#000 30%,#000 100%);opacity:0.55;}}
#pwd-horizon{{position:absolute;left:0;right:0;top:1120px;height:160px;background:radial-gradient(ellipse 60% 50% at 50% 50%,color-mix(in srgb,{acc} 26%,transparent),transparent 70%);}}
.pwd-layer{{position:absolute;inset:-300px 0;}}
.pwd-sh{{position:absolute;border-radius:999px;}}
.pwd-glow{{position:absolute;left:-310px;top:-60px;width:1700px;height:1600px;opacity:0;}}
#pwd-grain{{position:absolute;inset:0;background-image:url("{grain}");background-size:240px 240px;opacity:0.10;mix-blend-mode:overlay;}}
#pwd-edge{{position:absolute;inset:0;background:radial-gradient(ellipse 85% 70% at 50% 42%,transparent 55%,rgba(6,6,12,0.62) 100%);}}
</style>
<div id="pwd-horizon"></div><div id="pwd-floor"></div>
{glows}
<div class="pwd-layer" id="pwd-l0">{''.join(s for s in shards if ' d0"' in s)}</div>
<div class="pwd-layer" id="pwd-l1">{''.join(s for s in shards if ' d1"' in s)}</div>
<div class="pwd-layer" id="pwd-l2">{''.join(s for s in shards if ' d2"' in s)}</div>
<div id="pwd-grain"></div><div id="pwd-edge"></div>
</div>"""
    # story light: one glow per status tone, crossfaded when the status bar changes (same times as the bar)
    lay = getattr(plan, "layout", None) or {}
    states = ((lay.get("status_bar") or {}).get("states")) or []
    starts = {b.id: float(b.start) for b in plan.beats if getattr(b, "start", None) is not None}
    tl, events, cur = [], [], None
    for st in states:
        if st.get("beat") not in starts:
            continue
        g = _TONE_GLOW.get(st.get("tone", "muted"), "violet")
        at = starts[st["beat"]] + float(st.get("offset", 0.3))
        if g == cur:
            continue
        if cur:
            tl.append(f't.to("#pwd-g-{cur}",{{opacity:0,duration:1.4,ease:"sine.inOut"}},{at:.3f});')
        tl.append(f't.to("#pwd-g-{g}",{{opacity:1,duration:{0.5 if cur else 1.0},ease:"sine.inOut"}},{at:.3f});')
        cur = g         # light changes sit on scene starts; not counted as extra visual events
    if not tl:
        tl.append('t.to("#pwd-g-violet",{opacity:1,duration:1.0},0);')
    script = f"""<script>
(function(){{var t=window.__timelines&&window.__timelines.main;if(!t)return;var T=Number(document.getElementById("root").dataset.duration)||60;
t.fromTo("#pwd-floor",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px "+(Math.round(T*16/120)*120)+"px",duration:T,ease:"none"}},0);
t.fromTo("#pwd-l0",{{y:70}},{{y:-70,duration:T,ease:"none"}},0);
t.fromTo("#pwd-l1",{{y:160,x:-10}},{{y:-160,x:10,duration:T,ease:"none"}},0);
t.fromTo("#pwd-l2",{{y:320,x:20}},{{y:-320,x:-20,duration:T,ease:"none"}},0);
t.fromTo("#pwd-horizon",{{opacity:0.7}},{{opacity:1,duration:T/2,ease:"sine.inOut",yoyo:true,repeat:1}},0);
{chr(10).join(tl)}
t.seek(0);}})();
</script>"""
    return {"under_scenes_html": html_, "body_end_html": script, "events": events}


# --- Format "Echtlauf" (02.11.2026): recorded real runs, scene types rec_*, see echtlauf/scenes.py ---------------
# A plan with layout.format == "echtlauf" gets the Echtlauf layer instead of the code-shard background.
import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("pw_echtlauf_scenes", _Path(__file__).resolve().with_name("echtlauf") / "scenes.py")
_el = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_el)
TEMPLATES.update(_el.TEMPLATES)
LIMITS.update(_el.LIMITS)
HOOK_SCENE_TYPES += _el.HOOK_SCENE_TYPES
_pw_css, _pw_layer = CSS, LAYER


def CSS(*a, **k) -> str:  # noqa: F811
    return _pw_css(*a, **k) + _el.CSS(*a, **k)


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: F811
    if (getattr(plan, "layout", None) or {}).get("format") == "echtlauf":
        return _el.LAYER(plan, brand, project_dir, captions)
    return _pw_layer(plan, brand, project_dir, captions)


MANIFEST_EXTRA = _el.MANIFEST_EXTRA
