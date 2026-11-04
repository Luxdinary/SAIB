"""Five reusable HyperFrames scene templates, data-driven.

Each template receives a `SceneCtx` (timing, palette, fonts, zone) and the beat's `data` dict and
returns `SceneOut`: the inner HTML of the scene, GSAP timeline lines (absolute times), and the
times of its visual events (used by the visual-cuts check). Templates never tween the `.clip`
itself (HyperFrames rule); every motion targets children. Camera moves animate `.stage`.

Readability floors (1080 px wide, phone viewing): headline >= 60 px, body/rows >= 36 px, labels
>= 30 px. Text limits are enforced by `text_limits()` so the layout never overflows.
"""
from __future__ import annotations

import html
from dataclasses import dataclass, field

W, H = 1080, 1920

# --- text limits per template (characters) --------------------------------------------------------
LIMITS: dict[str, dict[str, int]] = {
    "cinematic_hook": {"question": 64, "doc_label": 24, "chat_title": 18, "badge": 22},
    "data_flow": {"headline": 60, "node_label": 26, "edge_label": 22, "chip": 30},
    "ui_demo": {"headline": 60, "title": 28, "row_label": 34, "note": 40},
    "comparison": {"headline": 60, "card_title": 30, "row": 44, "statement": 70, "stamp": 8, "subline": 60},
    "key_takeaway": {"headline": 60, "item_title": 34, "item_sub": 48, "statement": 80},
}


@dataclass
class SceneCtx:
    sid: str                    # DOM id prefix, e.g. "b1"
    start: float
    duration: float
    pal: dict
    display_font: str
    body_font: str
    mono_font: str
    zone_top: int = 320
    zone_h: int = 880
    enter: float = 0.25
    lang: str = "de"
    flat: bool = False          # brand rule: no glow, no gradients, calm camera, one-time motion
    words: list = field(default_factory=list)   # spoken words inside the beat (.text/.start/.end, absolute times)

    @property
    def end(self) -> float:
        return self.start + self.duration

    def t(self, rel: float) -> float:
        """Absolute time for a relative offset inside the scene, clamped to the scene."""
        return round(min(self.end - 0.05, max(self.start, self.start + rel)), 3)


@dataclass
class SceneOut:
    html: str
    tl: list[str] = field(default_factory=list)
    events: list[float] = field(default_factory=list)   # absolute times of visual changes
    problems: list[str] = field(default_factory=list)
    # optional names for sound cues (fn.render.sound): {"stamp_lands": 12.4}; a plan cue {"event": "stamp_lands"} lands there
    named_events: dict[str, float] = field(default_factory=dict)


def _e(s: str) -> str:
    return html.escape(str(s))


def text_limits(scene_type: str, data: dict) -> list[str]:
    """Return readability problems (text too long for the fixed font sizes)."""
    lim = LIMITS.get(scene_type, {})
    p: list[str] = []

    def chk(key: str, val: str, where: str) -> None:
        if lim.get(key) and len(str(val)) > lim[key]:
            p.append(f"{scene_type}.{where}: {len(str(val))} chars > {lim[key]}")

    if scene_type == "cinematic_hook":
        chk("question", data.get("question", ""), "question")
        chk("doc_label", data.get("doc_label", ""), "doc_label")
        chk("chat_title", data.get("chat_title", ""), "chat_title")
        chk("badge", data.get("badge", ""), "badge")
    elif scene_type == "data_flow":
        chk("headline", data.get("headline", ""), "headline")
        for n in data.get("nodes", []):
            chk("node_label", n.get("label", ""), f"node {n.get('id')}")
        for e in data.get("edges", []):
            chk("edge_label", e.get("label", ""), "edge")
        chk("chip", (data.get("highlight") or {}).get("label", ""), "highlight.label")
    elif scene_type == "ui_demo":
        chk("headline", data.get("headline", ""), "headline")
        chk("title", data.get("title", ""), "title")
        for r in data.get("rows", []):
            chk("row_label", r.get("label", ""), "row")
        chk("note", data.get("note", ""), "note")
    elif scene_type == "comparison":
        chk("headline", data.get("headline", ""), "headline")
        for side in ("left", "right"):
            c = data.get(side) or {}
            chk("card_title", c.get("title", ""), f"{side}.title")
            for r in c.get("rows", []):
                chk("row", r.get("text", ""), f"{side}.row")
        neg = data.get("negate") or {}
        chk("statement", neg.get("statement", ""), "negate.statement")
        chk("stamp", neg.get("stamp", ""), "negate.stamp")
        chk("subline", neg.get("subline", ""), "negate.subline")
    elif scene_type == "key_takeaway":
        chk("headline", data.get("headline", ""), "headline")
        for it in data.get("items", []):
            chk("item_title", it.get("title", ""), "item.title")
            chk("item_sub", it.get("sub", ""), "item.sub")
        chk("statement", data.get("statement", ""), "statement")
    return p


# --- shared pieces --------------------------------------------------------------------------------

def _camera(c: SceneCtx, *, scale_to: float = 1.05, y_to: int = -12) -> str:
    if c.flat:
        scale_to, y_to = min(scale_to, 1.02), max(y_to, -6)
    return (f'tl.fromTo("#{c.sid} .stage",{{scale:1,y:0}},{{scale:{scale_to},y:{y_to},duration:{c.duration:.2f},ease:"none"}},{c.start:.3f});')


def _enter_exit(c: SceneCtx, sel: str = ".scene-inner") -> list[str]:
    return [
        f'tl.fromTo("#{c.sid} {sel}",{{opacity:0}},{{opacity:1,duration:{c.enter:.2f},ease:"power2.out"}},{c.start:.3f});',
        f'tl.to("#{c.sid} {sel}",{{opacity:0,duration:0.18,ease:"power2.in"}},{max(c.start + c.enter + 0.05, c.end - 0.18):.3f});',
    ]


def _doc_q(c: SceneCtx) -> str:
    if c.flat:
        return f'<span class="qchip doc-q"><i class="mk mk-unc"></i>{"Unsicher" if c.lang == "de" else "Open"}</span>'
    return '<div class="doc-q">?</div>'


def _headline(text: str, cls: str = "h2") -> str:
    return f'<div class="{cls}">{_e(text)}</div>' if text else ""


# --- 1. Cinematic Hook ----------------------------------------------------------------------------

def cinematic_hook(c: SceneCtx, d: dict) -> SceneOut:
    """Big question, a document that flies into a chat window, a warning badge when the question lands."""
    q = d.get("question", "")
    doc = d.get("doc_label", "Kundenliste.xlsx")
    chat_title = d.get("chat_title", "KI-Chat")
    badge = d.get("badge", "?")
    fly_at = float(d.get("fly_at", 0.6))
    land_at = fly_at + 1.6
    q_at = float(d.get("question_at", land_at + 1.2))
    out = SceneOut(html="")
    if d.get("mode") == "approach":
        # A2: the file approaches the chat and STOPS before the upload (no typed text, no bubble); amber question on the file
        out.html = f"""
<div class="scene-inner hook approach">
  <div class="question">{_e(q)}</div>
  <div class="stage">
    <div class="glow"></div>
    <div class="chat">
      <div class="chat-bar"><i></i><i></i><i></i><span class="chat-title">{_e(chat_title)}</span></div>
      <div class="chat-body"><div class="bubble bot">{_e(d.get('bot_line', 'Wie kann ich helfen?'))}</div></div>
      <div class="chat-input"><span class="chat-placeholder" data-layout-ignore>{_e(d.get('placeholder', 'Datei hier ablegen'))}</span></div>
    </div>
    <div class="doc big"><div class="doc-icon">&#9638;</div><div class="doc-label" data-layout-ignore>{_e(doc)}</div>{_doc_q(c)}</div>
  </div>
</div>"""
        s, t = c.sid, c.t
        stop_at = fly_at + 1.5
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.06, y_to=-14))
        if not c.flat:
            out.tl.append(f'tl.fromTo("#{s} .glow",{{opacity:0.25,scale:0.9}},{{opacity:0.55,scale:1.12,duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});')
        out.tl.append(f'tl.fromTo("#{s} .chat",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power3.out"}},{t(0.05):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .doc",{{y:700,opacity:0,scale:1}},{{y:232,opacity:1,scale:0.92,duration:{max(0.6, stop_at - fly_at):.2f},ease:"power2.out"}},{t(fly_at):.3f});')
        out.tl.append(f'tl.to("#{s} .doc",{{y:220,duration:0.25,ease:"power2.out"}},{t(stop_at):.3f});')
        out.tl.append(f'tl.to("#{s} .chat-placeholder",{{opacity:0,duration:0.2}},{t(max(0.0, stop_at - 0.4)):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .doc-q",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{t(stop_at + 0.1):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .question",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out"}},{t(q_at):.3f});')
        out.events = [c.start, t(fly_at), t(stop_at), t(q_at)]
        out.problems = text_limits("cinematic_hook", d)
        return out
    out.html = f"""
<div class="scene-inner hook">
  <div class="stage">
    <div class="glow"></div>
    <div class="chat">
      <div class="chat-bar"><i></i><i></i><i></i><span class="chat-title">{_e(chat_title)}</span></div>
      <div class="chat-body">
        <div class="bubble bot">{_e(d.get('bot_line', 'Wie kann ich helfen?'))}</div>
        <div class="bubble user"><span class="doc-mini">&#9638;</span> {_e(doc)}</div>
      </div>
      <div class="chat-input"><span class="chat-input-text">{_e(d.get('typed', doc))}</span><span class="caret"></span></div>
      <div class="badge"><span class="badge-icon">!</span><span class="badge-text">{_e(badge)}</span></div>
    </div>
    <div class="doc"><div class="doc-icon">&#9638;</div><div class="doc-label" data-layout-ignore>{_e(doc)}</div></div>
  </div>
  <div class="question">{_e(q)}</div>
</div>"""
    s = c.sid
    t = c.t
    out.tl += _enter_exit(c)
    out.tl.append(_camera(c, scale_to=1.07, y_to=-16))
    if not c.flat:
        out.tl.append(f'tl.fromTo("#{s} .glow",{{opacity:0.25,scale:0.9}},{{opacity:0.6,scale:1.15,duration:{c.duration:.2f},ease:"sine.inOut"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .chat",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power3.out"}},{t(0.1):.3f});')
    # document flies from bottom-left into the chat input
    out.tl.append(f'tl.fromTo("#{s} .doc",{{x:-520,y:620,rotation:-14,opacity:0}},{{x:0,y:0,rotation:0,opacity:1,duration:0.35,ease:"power2.out"}},{t(fly_at):.3f});')
    out.tl.append(f'tl.to("#{s} .doc",{{x:0,y:250,scale:0.42,rotation:4,duration:{max(0.4, land_at - fly_at - 0.35):.2f},ease:"power2.inOut"}},{t(fly_at + 0.35):.3f});')
    out.tl.append(f'tl.to("#{s} .doc",{{opacity:0,duration:0.15}},{t(land_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .chat-input-text",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.6,ease:"steps(14)"}},{t(land_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .caret",{{opacity:1}},{{opacity:0,duration:0.4,ease:"steps(1)"}},{t(land_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .bubble.user",{{opacity:0,y:30,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t(land_at + 0.7):.3f});')
    out.tl.append(f'tl.to("#{s} .chat-input-text",{{opacity:0,duration:0.1}},{t(land_at + 0.7):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .question",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out"}},{t(q_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .badge",{{opacity:0,scale:0.3,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2.2)"}},{t(q_at + 0.15):.3f});')
    if not c.flat:
        out.tl.append(f'tl.to("#{s} .badge",{{scale:1.08,duration:0.5,ease:"sine.inOut"}},{t(q_at + 0.55):.3f});')
    out.events = [c.start, t(fly_at), t(land_at), t(q_at)]
    out.problems = text_limits("cinematic_hook", d)
    return out


# --- 2. Data Flow ---------------------------------------------------------------------------------

def data_flow(c: SceneCtx, d: dict) -> SceneOut:
    """Vertical flow of 2-4 nodes with drawn connectors, a travelling packet and an optional highlight chip."""
    nodes = d.get("nodes", [])[:4]
    edges = d.get("edges", [])
    packet_at = float(d.get("packet_at", 1.0))
    hl = d.get("highlight") or {}
    n = len(nodes)
    node_h, gap = 140, 118
    total_h = n * node_h + (n - 1) * gap
    stage_h = c.zone_h - 190                               # zone minus headline (2 lines) and gap
    top = max(0, (stage_h - total_h) // 2)
    rows = []
    for i, nd in enumerate(nodes):
        y = top + i * (node_h + gap)
        icon = _e(nd.get("icon", "&#9679;")) if not str(nd.get("icon", "")).startswith("&") else nd.get("icon")
        rows.append(f'<div class="node" id="{c.sid}-n{i}" style="top:{y}px"><span class="node-icon">{icon}</span><span class="node-label">{_e(nd.get("label", ""))}</span></div>')
    conns = []
    for i in range(n - 1):
        y0 = top + i * (node_h + gap) + node_h
        y1 = y0 + gap
        label = edges[i].get("label", "") if i < len(edges) else ""
        conns.append(f'<svg class="conn" style="top:{y0}px;height:{gap}px" viewBox="0 0 400 {gap}"><line class="conn-line" x1="200" y1="4" x2="200" y2="{gap - 10}"/><polygon class="conn-head" points="186,{gap - 22} 214,{gap - 22} 200,{gap - 4}"/></svg>'
                     + (f'<div class="edge-label" style="top:{y0 + gap // 2 - 22}px">{_e(label)}</div>' if label else ""))
    chip = f'<div class="chip">{_e(hl.get("label", ""))}</div>' if hl.get("label") else ""
    out = SceneOut(html=f"""
<div class="scene-inner flow">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="flow-wrap">{''.join(rows)}{''.join(conns)}<div class="packet"></div>{chip}</div>
  </div>
</div>""")
    s = c.sid
    t = c.t
    out.tl += _enter_exit(c)
    out.tl.append(_camera(c, scale_to=1.04, y_to=-10))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    for i in range(n):
        out.tl.append(f'tl.fromTo("#{s}-n{i}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{t(0.25 + i * 0.25):.3f});')
    for i in range(n - 1):
        out.tl.append(f'tl.fromTo("#{s} .conn:nth-of-type({i + 1}) .conn-line",{{strokeDashoffset:300}},{{strokeDashoffset:0,duration:0.4,ease:"power1.inOut"}},{t(0.5 + i * 0.3):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .conn:nth-of-type({i + 1}) .conn-head",{{opacity:0}},{{opacity:1,duration:0.15}},{t(0.85 + i * 0.3):.3f});')
    for el in range(max(0, n - 1)):
        out.tl.append(f'tl.fromTo("#{s} .edge-label:nth-of-type({el + 1})",{{opacity:0}},{{opacity:1,duration:0.25}},{t(0.9 + el * 0.3):.3f});')
    if n >= 2:
        y_start = top + node_h // 2
        y_end = top + (n - 1) * (node_h + gap) + node_h // 2
        travel = max(0.8, min(2.4, (y_end - y_start) / 420))
        out.tl.append(f'tl.fromTo("#{s} .packet",{{y:{y_start},opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.2}},{t(packet_at):.3f});')
        out.tl.append(f'tl.to("#{s} .packet",{{y:{y_end},duration:{travel:.2f},ease:"power1.inOut"}},{t(packet_at + 0.2):.3f});')
        out.tl.append(f'tl.to("#{s} .packet",{{opacity:0,scale:1.6,duration:0.25}},{t(packet_at + 0.2 + travel):.3f});')
    events = [c.start, t(packet_at)]
    if hl.get("label"):
        idx = min(n - 1, int(hl.get("node", n - 1)))
        y = top + idx * (node_h + gap) - 34            # above the node's top-right corner
        hl_at = float(hl.get("at", packet_at + 2.0))
        out.tl.append(f'tl.set("#{s} .chip",{{y:{y}}},{c.start:.3f});')
        out.tl.append(f'tl.fromTo("#{s} .chip",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{t(hl_at):.3f});')
        if c.flat:
            out.tl.append(f'tl.to("#{s}-n{idx}",{{borderColor:"{c.pal["accent"]}",duration:0.4}},{t(hl_at):.3f});')
        else:
            out.tl.append(f'tl.fromTo("#{s}-n{idx}",{{boxShadow:"0 0 0px rgba(0,212,255,0)"}},{{boxShadow:"0 0 46px rgba(0,212,255,0.55)",duration:0.4}},{t(hl_at):.3f});')
        events.append(t(hl_at))
    out.events = events
    out.problems = text_limits("data_flow", d)
    return out


# --- 3. UI Demonstration --------------------------------------------------------------------------

def ui_demo(c: SceneCtx, d: dict) -> SceneOut:
    """Settings window (real screenshot via `image`, else schematic), cursor moves to a toggle, zoom, flip."""
    rows = d.get("rows", [])[:6]
    focus = int(d.get("focus_row", max(0, len(rows) - 1)))
    image = d.get("image")              # project-relative path to a real screenshot, optional
    note = d.get("note") or ("" if image else ("Schematische Darstellung" if c.lang == "de" else "Schematic view"))
    cursor_at = float(d.get("cursor_at", 1.2))
    zoom_at = float(d.get("zoom_at", cursor_at + 0.9))
    flip_at = float(d.get("flip_at", zoom_at + 0.9))
    zoom = min(1.2, float(d.get("zoom", 1.2)))        # frame 860 px wide must stay inside the 1080 px canvas
    frame_w, frame_h = 860, 560
    row_h = 92
    if image:
        body = f'<img class="shot" src="{_e(image)}" alt="">'
    else:
        items = []
        for i, r in enumerate(rows):
            state = "on" if r.get("state", "on") == "on" else "off"
            items.append(f'<div class="urow" id="{c.sid}-r{i}"><span class="ulabel">{_e(r.get("label", ""))}</span>'
                         f'<span class="toggle {state}"><span class="knob"></span></span></div>')
        body = f'<div class="ulist"><div class="utitle">{_e(d.get("title", "Settings"))}</div>{"".join(items)}</div>'
    # toggle centre inside the frame (for cursor target and zoom origin)
    tx = frame_w - 92
    ty = 96 + focus * row_h + row_h // 2 if not image else int(d.get("focus_y", frame_h // 2))
    if image:
        tx = int(d.get("focus_x", frame_w - 92))
    out = SceneOut(html=f"""
<div class="scene-inner demo">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="frame" style="width:{frame_w}px;height:{frame_h}px">
      <div class="frame-bar"><i></i><i></i><i></i><span class="frame-url">{_e(d.get('url', 'claude.ai/settings'))}</span></div>
      <div class="frame-body">{body}{f'<div class="note">{_e(note)}</div>' if note else ''}<div class="ring" style="left:{tx - 70}px;top:{ty - 40}px"></div>
      <svg class="cursor" viewBox="0 0 32 32" style="left:{tx - 16}px;top:{ty - 6}px"><path d="M6 3 L26 17 L16 19 L21 29 L17 31 L12 21 L6 26 Z"/></svg></div>
    </div>
  </div>
</div>""")
    s = c.sid
    t = c.t
    out.tl += _enter_exit(c)
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .frame",{{opacity:0,y:50,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{t(0.1):.3f});')
    for i in range(len(rows) if not image else 0):
        out.tl.append(f'tl.fromTo("#{s}-r{i}",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.25}},{t(0.4 + i * 0.1):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .cursor",{{x:-420,y:360,opacity:0}},{{x:0,y:0,opacity:1,duration:0.8,ease:"power2.inOut"}},{t(cursor_at):.3f});')
    stage_h = c.zone_h - 190
    frame_top = max(0, (stage_h - frame_h) // 2)        # frame is centred in the stage (flex)
    oy = min(95.0, max(5.0, (frame_top + 70 + ty) / stage_h * 100))
    out.tl.append(f'tl.set("#{s} .stage",{{transformOrigin:"50% {oy:.1f}%"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .stage",{{scale:1}},{{scale:{zoom:.2f},duration:0.9,ease:"power2.inOut"}},{t(zoom_at):.3f});')
    out.tl.append(f'tl.to("#{s} .h2",{{opacity:0,y:-20,duration:0.3}},{t(zoom_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .ring",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{t(zoom_at + 0.5):.3f});')
    if not image and rows:
        out.tl.append(f'tl.to("#{s}-r{focus} .knob",{{x:-44,duration:0.25,ease:"power2.inOut"}},{t(flip_at):.3f});')
        out.tl.append(f'tl.to("#{s}-r{focus} .toggle",{{backgroundColor:"#3a4258",duration:0.25}},{t(flip_at):.3f});')
    out.tl.append(f'tl.to("#{s} .cursor",{{scale:0.85,duration:0.1,yoyo:true,repeat:1}},{t(flip_at - 0.05):.3f});')
    out.events = [c.start, t(cursor_at), t(zoom_at), t(flip_at)]
    out.problems = text_limits("ui_demo", d)
    if not image:
        out.problems.append("ui_demo: schematic UI, no real screen recording (allowed for prototypes only)")
    return out


# --- 4. Comparison --------------------------------------------------------------------------------

def comparison(c: SceneCtx, d: dict) -> SceneOut:
    """mode 'versus': two stacked cards with check/cross rows. mode 'negate': a statement and a big stamp."""
    mode = d.get("mode", "versus")
    s = c.sid
    t = c.t
    out = SceneOut(html="")
    if mode == "negate":
        neg = d.get("negate") or {}
        stamp_at = float(neg.get("stamp_at", 1.4))
        sub_at = float(neg.get("subline_at", stamp_at + 0.8))
        out.html = f"""
<div class="scene-inner cmp negate">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="neg-wrap"><div class="statement">{_e(neg.get('statement', ''))}</div>
    <div class="stamp" data-layout-ignore>{_e(neg.get('stamp', 'NEIN'))}</div></div>
    <div class="subline">{_e(neg.get('subline', ''))}</div>
  </div>
</div>"""
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.04, y_to=-8))
        out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
        out.tl.append(f'tl.fromTo("#{s} .statement",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(0.2):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .stamp",{{opacity:0,scale:2.6,rotation:-18,xPercent:-50,yPercent:-50}},{{opacity:1,scale:1,rotation:-8,xPercent:-50,yPercent:-50,duration:0.28,ease:"power4.in"}},{t(stamp_at):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .statement",{{x:0}},{{x:6,duration:0.06,yoyo:true,repeat:3}},{t(stamp_at + 0.26):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .subline",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{t(sub_at):.3f});')
        out.events = [c.start, t(stamp_at), t(sub_at)]
    else:
        cards = []
        for side in ("left", "right"):
            card = d.get(side) or {}
            rws = []
            for j, r in enumerate(card.get("rows", [])[:3]):
                ok = r.get("ok")
                cls = "ok" if ok is True else ("bad" if ok is False else ("open" if ok == "open" else "neutral"))
                if c.flat:   # brand markers: Fakt = filled square, Unsicher = half circle, Luecke = dashed circle, Geregelt = green square
                    mark = {"ok": '<i class="mk mk-ok"></i>', "bad": '<i class="mk mk-gap"></i>', "open": '<i class="mk mk-unc"></i>', "neutral": '<i class="mk mk-fact"></i>'}[cls]
                else:
                    mark = "&#10003;" if ok is True else ("&#10007;" if ok is False else ("?" if ok == "open" else "&#8226;"))
                rws.append(f'<div class="crow {cls}" id="{s}-{side}-{j}"><span class="cmark">{mark}</span><span class="ctext">{_e(r.get("text", ""))}</span></div>')
            cards.append(f'<div class="card {side}" id="{s}-{side}"><div class="ctitle">{_e(card.get("title", ""))}</div>{"".join(rws)}</div>')
        out.html = f"""
<div class="scene-inner cmp versus">
  {_headline(d.get('headline', ''))}
  <div class="stage">{''.join(cards)}</div>
</div>"""
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.03, y_to=-8))
        out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
        left_at = float(d.get("left_at", 0.3))
        right_at = float(d.get("right_at", max(left_at + 1.6, c.duration * 0.45)))
        events = [c.start]
        for side, at in (("left", left_at), ("right", right_at)):
            out.tl.append(f'tl.fromTo("#{s}-{side}",{{opacity:0,x:{-60 if side == "left" else 60}}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t(at):.3f});')
            rows_n = len((d.get(side) or {}).get("rows", [])[:3])
            for j in range(rows_n):
                out.tl.append(f'tl.fromTo("#{s}-{side}-{j}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.25}},{t(at + 0.35 + j * 0.35):.3f});')
                events.append(t(at + 0.35 + j * 0.35))
        open_rows = [(side, j) for side in ('left', 'right') for j, r in enumerate((d.get(side) or {}).get('rows', [])[:3]) if r.get('ok') == 'open']
        if open_rows and not c.flat:
            pulse_at = float(d.get('pulse_at', c.duration * 0.72))
            for side, j in open_rows:
                out.tl.append(f'tl.fromTo("#{s}-{side}-{j} .cmark",{{scale:1}},{{scale:1.35,duration:0.25,yoyo:true,repeat:1,ease:"power2.inOut"}},{t(pulse_at):.3f});')
            events.append(t(pulse_at))
        out.events = events
    out.problems = text_limits("comparison", d)
    return out


# --- 5. Key Takeaway ------------------------------------------------------------------------------

def key_takeaway(c: SceneCtx, d: dict) -> SceneOut:
    """Up to three numbered check cards appearing in sequence, or one big statement."""
    items = d.get("items", [])[:3]
    s = c.sid
    t = c.t
    out = SceneOut(html="")
    if d.get("mode") == "closing":
        # closing card: brand motif (line-drawn shield) behind a big statement, optional chip; distinct from the list layout
        chip = f'<div class="close-chip">{_e(d["chip"])}</div>' if d.get("chip") else ""
        out.html = f"""
<div class="scene-inner take closing">
  <div class="stage">
    <svg class="close-shield" viewBox="0 0 400 440" fill="none"><path class="shield-path" d="M200 20 L360 80 V220 C360 320 290 390 200 420 C110 390 40 320 40 220 V80 Z"/><path class="shield-check" d="M130 220 L185 275 L280 170"/></svg>
    <div class="statement big">{_e(d.get('statement', ''))}</div>{chip}
  </div>
</div>"""
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.05, y_to=-10))
        out.tl.append(f'tl.fromTo("#{s} .shield-path",{{strokeDashoffset:1400}},{{strokeDashoffset:0,duration:1.4,ease:"power2.inOut"}},{t(0.1):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .shield-check",{{strokeDashoffset:300}},{{strokeDashoffset:0,duration:0.5,ease:"power2.out"}},{t(1.3):.3f});')
        out.tl.append(f'tl.fromTo("#{s} .statement",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{t(0.4):.3f});')
        if chip:
            out.tl.append(f'tl.fromTo("#{s} .close-chip",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{t(1.9):.3f});')
        out.events = [c.start, t(1.3), t(1.9)]
        out.problems = text_limits("key_takeaway", d)
        return out
    if items:
        marker = d.get("marker", "")          # "?" = open questions (amber), no numbers, no check marks
        cards = "".join(f'<div class="kcard" id="{s}-k{i}"><div class="knum{" q" if marker == "?" else ""}">{_e(marker) if marker else i + 1}</div><div class="ktext"><div class="ktitle">{_e(it.get("title", ""))}</div>'
                        f'<div class="ksub">{_e(it.get("sub", ""))}</div></div></div>' for i, it in enumerate(items))
        out.html = f"""
<div class="scene-inner take">
  {_headline(d.get('headline', ''))}
  <div class="stage"><div class="klist">{cards}</div></div>
</div>"""
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.03, y_to=-8))
        out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
        events = [c.start]
        for i, it in enumerate(items):
            at = float(it.get("at", 0.4 + i * max(1.2, (c.duration - 1.5) / max(1, len(items)))))
            # all cards are visible (dimmed) from the start so the frame is filled; each lights up on its word
            out.tl.append(f'tl.fromTo("#{s}-k{i}",{{opacity:0.22,y:0,scale:0.97}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out"}},{t(at):.3f});')
            out.tl.append(f'tl.fromTo("#{s}-k{i} .knum",{{scale:0.5}},{{scale:1,duration:0.35,ease:"back.out(2)"}},{t(at + 0.1):.3f});')
            events.append(t(at))
        out.events = events
    else:
        out.html = f"""
<div class="scene-inner take">
  <div class="stage"><div class="statement big">{_e(d.get('statement', ''))}</div></div>
</div>"""
        out.tl += _enter_exit(c)
        out.tl.append(_camera(c, scale_to=1.05, y_to=-10))
        out.tl.append(f'tl.fromTo("#{s} .statement",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{t(0.1):.3f});')
        out.events = [c.start]
    out.problems = text_limits("key_takeaway", d)
    return out


TEMPLATES = {
    "cinematic_hook": cinematic_hook,
    "data_flow": data_flow,
    "ui_demo": ui_demo,
    "comparison": comparison,
    "key_takeaway": key_takeaway,
}


def themed_css(css: str, pal: dict) -> str:
    """Palette hooks for light schemes: `shadow` ("r,g,b", default black) recolours every rgba(0,0,0,..) shadow;
    with `scheme: light` the screen-blended stamp is drawn normally (screen would vanish on a light ground)."""
    shadow = str(pal.get("shadow", "0,0,0")).replace(" ", "")
    if shadow != "0,0,0":
        css = css.replace("rgba(0,0,0,", f"rgba({shadow},")
    if pal.get("scheme", "dark") == "light":
        css = css.replace("mix-blend-mode:screen;", "")
    return css


def scene_css(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int, zone_h: int, flat: bool = False) -> str:
    """CSS for all five templates (one shared identity, five distinguishable layouts)."""
    acc, text, surf, muted, bg = pal["accent"], pal["text"], pal["surface"], pal["muted"], pal["bg"]
    amber, on_amber, red = pal.get("signal_amber", "#ffd166"), pal.get("on_signal", "#0a0c10"), pal.get("signal_red", "#ff6b6b")
    hair = pal.get("hairline", f"color-mix(in srgb,{acc} 35%,transparent)")
    card_border = hair if flat else f"color-mix(in srgb,{acc} 35%,transparent)"
    rad = 20 if flat else 26
    paper, paper_ink = pal.get("paper", text), pal.get("paper_ink", bg)
    shadow_card = "0 1px 2px rgba(0,0,0,0.3), 0 20px 50px rgba(0,0,0,0.35)" if flat else "0 40px 90px rgba(0,0,0,0.45)"
    shadow_paper = "0 1px 1px rgba(0,0,0,0.22), 0 6px 14px rgba(0,0,0,0.24), 0 24px 48px rgba(0,0,0,0.36)" if flat else "0 30px 70px rgba(0,0,0,0.5)"
    glow_css = "display:none;" if flat else ""
    tshadow = "none" if flat else "0 10px 40px rgba(0,0,0,0.5)"
    green = pal.get("signal_green", "#2ec4b6")
    toggle_off = pal.get("toggle_off", "#3a4258")
    css = f"""
.scene{{z-index:10;}}
.scene-inner{{position:absolute;left:108px;width:864px;top:{zone_top}px;height:{zone_h}px;display:flex;flex-direction:column;align-items:center;gap:26px;text-align:center;}}
.stage{{position:relative;width:864px;flex:1 1 auto;transform-origin:50% 50%;will-change:transform;}}
.demo .stage,.take .stage{{display:flex;flex-direction:column;align-items:center;justify-content:center;}}
.h2{{font-family:'FN {display}';font-weight:{display_w};font-size:62px;line-height:1.1;letter-spacing:-0.015em;color:{text};max-width:860px;}}
/* 1 cinematic hook */
.hook .stage{{height:720px;}}
.glow{{{glow_css}position:absolute;left:132px;top:40px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,{acc} 32%,transparent) 0%,transparent 65%);filter:blur(10px);}}
.chat{{position:absolute;left:52px;top:80px;width:760px;height:560px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;box-shadow:{shadow_card};overflow:visible;text-align:left;}}
.chat-bar{{height:72px;display:flex;align-items:center;padding:0 28px;border-bottom:1px solid color-mix(in srgb,{text} 12%,transparent);}}
.chat-bar i,.frame-bar i{{display:inline-block;width:16px;height:16px;border-radius:50%;background:{muted};opacity:0.55;margin-right:12px;}}
.chat-title{{margin-left:14px;font-family:'FN {mono}';font-size:30px;color:{muted};}}
.chat-body{{padding:30px 32px 0;display:flex;flex-direction:column;gap:22px;}}
.bubble{{max-width:560px;padding:20px 28px;border-radius:24px;font-size:36px;line-height:1.25;color:{text};}}
.bubble.bot{{background:color-mix(in srgb,{text} 8%,transparent);align-self:flex-start;}}
.bubble.user{{background:color-mix(in srgb,{acc} 22%,transparent);border:1px solid color-mix(in srgb,{acc} 50%,transparent);align-self:flex-end;}}
.doc-mini{{color:{acc};}}
.chat-input{{position:absolute;left:32px;right:32px;bottom:30px;height:84px;border-radius:20px;background:color-mix(in srgb,{bg} 70%,transparent);border:1px solid color-mix(in srgb,{text} 16%,transparent);display:flex;align-items:center;padding:0 26px;font-size:34px;color:{text};font-family:'FN {mono}';white-space:nowrap;overflow:hidden;}}
.caret{{display:inline-block;width:4px;height:40px;background:{acc};margin-left:8px;}}
.badge{{position:absolute;right:-30px;top:-34px;display:flex;align-items:center;gap:14px;background:{amber};color:{on_amber};border-radius:999px;padding:14px 30px 14px 18px;font-family:'FN {display}';font-weight:800;font-size:34px;box-shadow:0 14px 40px rgba(0,0,0,0.4);}}
.badge-icon{{display:inline-flex;width:48px;height:48px;border-radius:50%;background:{on_amber};color:{amber};align-items:center;justify-content:center;font-size:34px;}}
.doc{{position:absolute;left:300px;top:150px;width:260px;height:300px;background:{paper};color:{paper_ink};border-radius:{4 if flat else 18}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;box-shadow:{shadow_paper};}}
.doc-icon{{font-size:96px;line-height:1;color:{paper_ink};}}
.doc-label{{font-family:'FN {mono}';font-size:30px;color:{paper_ink};}}
.question{{font-family:'FN {display}';font-weight:{display_w};font-size:84px;line-height:1.04;letter-spacing:-0.02em;color:{text};max-width:860px;text-shadow:{tshadow};}}
/* 2 data flow */
.flow-wrap{{position:absolute;left:0;top:0;width:864px;height:100%;}}
.node{{position:absolute;left:92px;width:680px;height:140px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;display:flex;align-items:center;gap:22px;padding:0 34px;text-align:left;}}
.node-icon{{font-size:46px;color:{acc};width:60px;text-align:center;}}
.node-label{{font-size:40px;font-weight:600;color:{text};line-height:1.15;}}
.conn{{position:absolute;left:232px;width:400px;}}
.conn-line{{stroke:{acc};stroke-width:6;stroke-dasharray:300;stroke-dashoffset:300;stroke-linecap:round;}}
.conn-head{{fill:{acc};}}
.edge-label{{position:absolute;left:470px;width:300px;text-align:left;font-family:'FN {mono}';font-size:30px;color:{muted};line-height:1.2;}}
.packet{{position:absolute;left:412px;top:-20px;width:40px;height:40px;border-radius:50%;background:{acc};{'' if flat else 'box-shadow:0 0 30px ' + acc + ';'}}}
.chip{{position:absolute;left:400px;top:0;background:{amber};color:{on_amber};border-radius:999px;padding:12px 26px;font-size:32px;font-weight:700;white-space:nowrap;box-shadow:0 10px 30px rgba(0,0,0,0.4);}}
/* 3 ui demo */
.frame{{position:relative;flex:0 0 auto;background:{surf};border-radius:{rad}px;border:2px solid {card_border};box-shadow:{shadow_card};overflow:hidden;text-align:left;}}
.frame-bar{{height:70px;display:flex;align-items:center;padding:0 26px;border-bottom:1px solid color-mix(in srgb,{text} 12%,transparent);}}
.frame-url{{margin-left:12px;font-family:'FN {mono}';font-size:28px;color:{muted};white-space:nowrap;}}
.frame-body{{position:relative;height:calc(100% - 70px);}}
.shot{{width:100%;height:100%;object-fit:cover;object-position:top;display:block;}}
.ulist{{padding:26px 36px;}}
.utitle{{font-size:40px;font-weight:700;color:{text};margin-bottom:20px;}}
.urow{{height:92px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid color-mix(in srgb,{text} 10%,transparent);}}
.ulabel{{font-size:36px;color:{text};}}
.toggle{{position:relative;width:104px;height:56px;border-radius:999px;background:{acc};display:inline-block;}}
.toggle.off{{background:{toggle_off};}}
.knob{{position:absolute;top:6px;left:54px;width:44px;height:44px;border-radius:50%;background:#fff;}}
.toggle.off .knob{{left:6px;}}
.ring{{position:absolute;width:140px;height:80px;border:5px solid {amber};border-radius:999px;{'' if flat else 'box-shadow:0 0 30px rgba(245,179,66,0.6);'}pointer-events:none;}}
.cursor{{position:absolute;width:44px;height:44px;fill:#fff;stroke:#000;stroke-width:1.5;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.6));}}
.note{{position:absolute;right:18px;bottom:16px;font-family:'FN {mono}';font-size:28px;color:{muted};background:color-mix(in srgb,{bg} 75%,transparent);padding:6px 14px;border-radius:10px;white-space:nowrap;}}
/* 4 comparison */
.cmp .stage{{display:flex;flex-direction:column;gap:30px;align-items:stretch;justify-content:center;}}
.card{{background:{surf};border-radius:{rad}px;border:2px solid {card_border};padding:32px 36px;text-align:left;}}
.card.right{{border-color:{acc};{'' if flat else 'box-shadow:0 0 50px color-mix(in srgb,' + acc + ' 25%,transparent);'}}}
.ctitle{{font-family:'FN {display}';font-weight:700;font-size:40px;color:{acc};margin-bottom:14px;}}
.crow{{display:flex;align-items:flex-start;gap:18px;padding:12px 0;font-size:40px;line-height:1.22;color:{text};}}
.crow .cmark{{width:48px;flex:0 0 48px;font-size:40px;text-align:center;}}
.crow.ok .cmark{{color:#3DDC97;}}
.crow.bad .cmark{{color:{red};}}
.crow.neutral .cmark{{color:{muted};}}
.crow.open .cmark{{color:{amber};font-weight:800;}}
.knum.q{{background:{amber};color:{on_amber};}}
.mk{{display:inline-block;width:22px;height:22px;vertical-align:middle;}}
.mk-fact{{background:{acc};border-radius:2px;}}
.mk-ok{{background:{green};border-radius:2px;}}
.mk-unc{{border:3px solid {amber};border-radius:50%;background:linear-gradient(90deg,{amber} 50%,transparent 50%);}}
.mk-gap{{border:3px dashed {red};border-radius:50%;}}
.crow .cmark .mk{{margin-top:12px;}}
.doc.big{{left:272px;top:80px;width:320px;height:360px;}}
.hook.approach .stage{{height:600px;flex:0 0 600px;}}
.hook.approach .chat{{top:20px;}}
.hook.approach .glow{{top:-20px;}}
.doc.big .doc-icon{{font-size:120px;}}
.doc.big .doc-label{{font-size:32px;}}
.doc-q{{position:absolute;right:-26px;top:-26px;width:72px;height:72px;border-radius:50%;background:{amber};color:{on_amber};font-family:'FN {display}';font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,0.4);}}
.chat-placeholder{{color:{muted};font-size:32px;}}
.negate .stage{{justify-content:center;align-items:center;}}
.statement{{font-family:'FN {display}';font-weight:700;font-size:64px;line-height:1.12;color:{text};background:{surf};border-radius:28px;padding:40px 44px;max-width:860px;}}
.statement.big{{font-size:76px;background:none;padding:0;}}
.neg-wrap{{position:relative;}}
.stamp{{position:absolute;left:50%;top:50%;font-family:'FN {display}';font-weight:900;font-size:190px;line-height:1;color:{red};border:14px solid {red};border-radius:30px;padding:10px 40px;letter-spacing:0.04em;mix-blend-mode:screen;}}
.subline{{margin-top:40px;font-size:40px;line-height:1.25;color:{text};max-width:820px;}}
/* 5 key takeaway */
.klist{{display:flex;flex-direction:column;gap:30px;width:864px;}}
.kcard{{display:flex;align-items:center;gap:30px;background:{surf};border-radius:{rad}px;border:2px solid {card_border};padding:34px 36px;text-align:left;}}
.knum{{flex:0 0 104px;width:104px;height:104px;border-radius:50%;background:{acc};color:{bg};font-family:'FN {display}';font-weight:800;font-size:60px;display:flex;align-items:center;justify-content:center;}}
.ktitle{{font-size:44px;font-weight:700;color:{text};line-height:1.15;}}
.ksub{{font-size:34px;color:{muted};line-height:1.25;margin-top:8px;}}
.closing .stage{{gap:40px;}}
.close-shield{{width:300px;height:330px;position:absolute;left:282px;top:50%;margin-top:-330px;opacity:0.55;}}
.shield-path{{stroke:{acc};stroke-width:6;stroke-dasharray:1400;stroke-dashoffset:1400;}}
.shield-check{{stroke:{acc};stroke-width:10;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:300;stroke-dashoffset:300;}}
.closing .statement.big{{position:relative;margin-top:300px;text-shadow:{tshadow};}}
.close-chip{{position:relative;font-size:36px;font-weight:600;color:{bg};background:{acc};border-radius:999px;padding:14px 32px;}}
"""
    return themed_css(css, pal)


def _register_file_templates() -> None:
    from .templates_file import FILE_TEMPLATES
    TEMPLATES.update(FILE_TEMPLATES)


_register_file_templates()
