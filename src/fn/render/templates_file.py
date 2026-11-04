"""File-thread scene templates (Fassung A2): the customer list is the recurring object.

Three scene types next to the five in templates.py:
- file_fork:   the file above two access routes (private account / business access) and the company approval
- file_beside: the file next to one information card (contract / access card)
- file_close:  the file with a blocked upload, the domain readable for the last seconds (ending inside the story)

Colour rules: amber only for open questions / warnings, red only for the concrete upload block, otherwise brand.
No check-mark icons while a risk question is open.
"""
from __future__ import annotations

from .templates import SceneCtx, SceneOut, _e, _enter_exit, _camera, _headline, text_limits, themed_css

AMBER = "#F5B342"
RED = "#E5484D"

FILE_LIMITS = {
    "file_fork": {"headline": 60, "file_label": 24, "route_title": 26, "route_sub": 34, "approval": 36},
    "file_beside": {"headline": 60, "file_label": 24, "card_title": 30, "row": 44, "tag": 30},
    "file_close": {"headline": 60, "file_label": 24, "block_text": 34, "domain": 24, "button": 16},
}


def _limits(scene_type: str, d: dict) -> list[str]:
    lim = FILE_LIMITS[scene_type]
    p: list[str] = []

    def chk(key, val, where):
        if lim.get(key) and len(str(val)) > lim[key]:
            p.append(f"{scene_type}.{where}: {len(str(val))} chars > {lim[key]}")

    chk("headline", d.get("headline", ""), "headline")
    chk("file_label", d.get("file_label", ""), "file_label")
    if scene_type == "file_fork":
        for r in d.get("routes", []):
            chk("route_title", r.get("title", ""), "route.title")
            chk("route_sub", r.get("sub", ""), "route.sub")
        chk("approval", d.get("approval", ""), "approval")
    elif scene_type == "file_beside":
        c = d.get("card") or {}
        chk("card_title", c.get("title", ""), "card.title")
        for r in c.get("rows", []):
            chk("row", r.get("text", ""), "card.row")
        chk("tag", d.get("tag", ""), "tag")
    elif scene_type == "file_close":
        chk("block_text", d.get("block_text", ""), "block_text")
        chk("domain", d.get("domain", ""), "domain")
        chk("button", d.get("button", ""), "button")
    return p


def _qmark(c, cls: str) -> str:
    """Open-question marker: brand chip (half circle + word) when flat, amber question badge otherwise."""
    if c is not None and c.flat:
        word = "Unsicher" if c.lang == "de" else "Open"
        return f'<span class="qchip {cls}"><i class="mk mk-unc"></i>{word}</span>'
    return f'<div class="{cls}">?</div>'


def _file_marker(c, marker: str) -> str:
    """Chip on the file card: data `file_marker` = "open" (default, open question), "fact" (square) or "none"."""
    if marker == "none":
        return ""
    if marker == "fact":
        word = "Fakt" if c is None or c.lang == "de" else "Fact"
        return f'<span class="qchip fcard-q fact"><i class="mk mk-fact"></i>{word}</span>'
    return _qmark(c, "fcard-q")


def _file_card(label: str, cls: str = "", c=None, marker: str = "open") -> str:
    return (f'<div class="fcard {cls}"><div class="fcard-icon">&#9638;</div><div class="fcard-label">{_e(label)}</div>{_file_marker(c, marker)}</div>')


def _marker_tl(s: str, at: float, marker: str) -> list[str]:
    if marker == "none":
        return []
    return [f'tl.fromTo("#{s} .fcard-q",{{scale:0.3,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"}},{at:.3f});']


# --- file_fork -----------------------------------------------------------------------------------

def file_fork(c: SceneCtx, d: dict) -> SceneOut:
    routes = d.get("routes", [])[:2]
    s, t = c.sid, c.t
    route_html = "".join(
        f'<div class="route" id="{s}-r{i}"><div class="route-title">{_e(r.get("title", ""))}</div>'
        f'<div class="route-sub">{_e(r.get("sub", ""))}</div>{_qmark(c, "route-q") if d.get("route_marker", "open") != "none" else ""}</div>' for i, r in enumerate(routes))
    approval = d.get("approval", "")
    out = SceneOut(html=f"""
<div class="scene-inner fork">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'fork-file', c, d.get('file_marker', 'open'))}
    <svg class="fork-paths" viewBox="0 0 864 220"><path class="fp" d="M432 10 C 432 120, 200 90, 200 210"/><path class="fp" d="M432 10 C 432 120, 664 90, 664 210"/></svg>
    <div class="routes">{route_html}</div>
    {f'<div class="approval" id="{s}-ap">{_qmark(c, "approval-q")}{_e(approval)}</div>' if approval else ''}
  </div>
</div>""")
    out.tl += _enter_exit(c)
    out.tl.append(_camera(c, scale_to=1.04, y_to=-8))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fcard",{{opacity:0,y:-40,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out"}},{t(0.1):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fp",{{strokeDashoffset:600}},{{strokeDashoffset:0,duration:0.7,ease:"power1.inOut"}},{t(float(d.get("paths_at", 0.8))):.3f});')
    events = [c.start, t(float(d.get("paths_at", 0.8)))]
    for i in range(len(routes)):
        at = float(routes[i].get("at", 1.4 + i * 0.8))
        out.tl.append(f'tl.fromTo("#{s}-r{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(at):.3f});')
        if d.get("route_marker", "open") != "none":
            out.tl.append(f'tl.fromTo("#{s}-r{i} .route-q",{{scale:0.3}},{{scale:1,duration:0.35,ease:"back.out(2)"}},{t(at + 0.3):.3f});')
        events.append(t(at))
    if approval:
        ap_at = float(d.get("approval_at", 3.4))
        out.tl.append(f'tl.fromTo("#{s}-ap",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(ap_at):.3f});')
        events.append(t(ap_at))
    out.tl += _marker_tl(s, t(0.5), d.get('file_marker', 'open'))
    out.events = events
    out.problems = _limits("file_fork", d)
    return out


# --- file_beside ---------------------------------------------------------------------------------

def file_beside(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    card = d.get("card") or {}
    rows = []
    for j, r in enumerate(card.get("rows", [])[:4]):
        kind = r.get("ok")
        cls = "open" if kind == "open" else "neutral"
        if c.flat:
            mark = '<i class="mk mk-unc"></i>' if kind == "open" else '<i class="mk mk-fact"></i>'
        else:
            mark = "?" if kind == "open" else "&#8226;"
        rows.append(f'<div class="brow {cls}" id="{s}-row{j}"><span class="bmark">{mark}</span><span class="btext">{_e(r.get("text", ""))}</span></div>')
    tag = d.get("tag", "")
    out = SceneOut(html=f"""
<div class="scene-inner beside">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="beside-row">
      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'beside-file', c, d.get('file_marker', 'open'))}
      <div class="bcard" id="{s}-card"><div class="btitle">{_e(card.get('title', ''))}</div>{''.join(rows)}
      {f'<div class="btag">{_e(tag)}</div>' if tag else ''}</div>
    </div>
  </div>
</div>""")
    out.tl += _enter_exit(c)
    out.tl.append(_camera(c, scale_to=1.04, y_to=-8))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .fcard",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t(0.1):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-card",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t(0.4):.3f});')
    events = [c.start, t(0.4)]
    n = len(card.get("rows", [])[:4])
    step = float(d.get("row_step", max(1.2, (c.duration - 2.5) / max(1, n))))
    for j in range(n):
        at = 1.0 + j * step
        out.tl.append(f'tl.fromTo("#{s}-row{j}",{{opacity:0.18,x:0}},{{opacity:1,x:0,duration:0.35}},{t(at):.3f});')
        events.append(t(at))
    if tag:
        out.tl.append(f'tl.fromTo("#{s} .btag",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.3}},{t(1.0 + n * step):.3f});')
    out.tl += _marker_tl(s, t(0.6), d.get('file_marker', 'open'))
    out.events = events
    out.problems = _limits("file_beside", d)
    return out


# --- file_close ----------------------------------------------------------------------------------

def file_close(c: SceneCtx, d: dict) -> SceneOut:
    s, t = c.sid, c.t
    block_at = float(d.get("block_at", 1.0))
    domain_at = min(float(d.get("domain_at", 1.8)), max(0.0, c.duration - 4.0))   # domain readable >= 4 s
    out = SceneOut(html=f"""
<div class="scene-inner fclose">
  {_headline(d.get('headline', ''))}
  <div class="stage">
    <div class="upload-box">
      {_file_card(d.get('file_label', 'Kundenliste.xlsx'), 'close-file', c, d.get('file_marker', 'open'))}
      <div class="upload-btn">{_e(d.get('button', 'Hochladen'))}</div>
      <div class="block-bar"><span class="block-dot"></span>{_e(d.get('block_text', 'Upload blockiert: bis Freigabe'))}</div>
    </div>
    <div class="domain">{_e(d.get('domain', 'scutoria.com'))}</div>
    {f'<div class="claim">{_e(d["claim"])}</div>' if d.get('claim') else ''}
    {f'<div class="disclaimer">{_e(d["disclaimer"])}</div>' if d.get('disclaimer') else ''}
  </div>
</div>""")
    out.tl += _enter_exit(c)
    out.tl.append(_camera(c, scale_to=1.04, y_to=-6))
    out.tl.append(f'tl.fromTo("#{s} .h2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{c.enter:.2f},ease:"power3.out"}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s} .upload-box",{{opacity:0,y:40,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power3.out"}},{t(0.1):.3f});')
    out.tl += _marker_tl(s, t(0.5), d.get('file_marker', 'open'))
    out.tl.append(f'tl.fromTo("#{s} .block-bar",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{t(block_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .upload-btn",{{opacity:0.9}},{{opacity:0.35,duration:0.3}},{t(block_at):.3f});')
    out.tl.append(f'tl.fromTo("#{s} .domain",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(domain_at):.3f});')
    if d.get('claim'):
        out.tl.append(f'tl.fromTo("#{s} .claim",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.4}},{t(domain_at + 0.3):.3f});')
    if d.get('disclaimer'):
        out.tl.append(f'tl.fromTo("#{s} .disclaimer",{{opacity:0}},{{opacity:1,duration:0.4}},{t(domain_at + 0.5):.3f});')
    out.events = [c.start, t(block_at), t(domain_at)]
    out.problems = _limits("file_close", d)
    return out


FILE_TEMPLATES = {"file_fork": file_fork, "file_beside": file_beside, "file_close": file_close}


def file_css(pal: dict, display: str, display_w: int, mono: str, flat: bool = False) -> str:
    acc, text, surf, muted, bg = pal["accent"], pal["text"], pal["surface"], pal["muted"], pal["bg"]
    amber, on_amber, red = pal.get("signal_amber", AMBER), pal.get("on_signal", "#0a0c10"), pal.get("signal_red", RED)
    paper, paper_ink = pal.get("paper", text), pal.get("paper_ink", bg)
    card_border = pal.get("hairline", f"color-mix(in srgb,{acc} 35%,transparent)") if flat else f"color-mix(in srgb,{acc} 35%,transparent)"
    rad = 20 if flat else 26
    shadow_paper = "0 1px 1px rgba(0,0,0,0.22), 0 6px 14px rgba(0,0,0,0.24), 0 24px 48px rgba(0,0,0,0.36)" if flat else "0 30px 70px rgba(0,0,0,0.5)"
    tshadow = "none" if flat else "0 10px 40px rgba(0,0,0,0.6)"
    css = f"""
.qchip.fcard-q.fact{{background:{pal.get('surface_raised', surf)};color:{text};}}
.qchip.fcard-q.fact .mk-fact{{width:18px;height:18px;}}
.qchip{{position:absolute;right:-16px;top:-24px;display:inline-flex;align-items:center;gap:8px;background:{amber};color:{on_amber};border-radius:6px;padding:6px 14px;font-size:26px;font-weight:700;white-space:nowrap;}}
.qchip.fcard-q,.qchip.route-q,.qchip.approval-q,.qchip.doc-q{{width:auto;height:auto;border-radius:6px;font-size:26px;background:{amber};color:{on_amber};box-shadow:none;}}
.qchip.doc-q{{right:-20px;top:-26px;}}
.qchip .mk-unc{{border-color:{on_amber};background:linear-gradient(90deg,{on_amber} 50%,transparent 50%);width:18px;height:18px;}}
.approval .qchip{{position:static;margin-right:18px;}}
.claim{{font-family:'FN {display}';font-weight:700;font-size:36px;color:{text};margin-top:-18px;}}
.disclaimer{{font-size:28px;color:{muted};margin-top:-26px;}}
/* file thread */
.fcard{{position:relative;width:290px;height:290px;background:{paper};color:{paper_ink};border-radius:{4 if flat else 20}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;box-shadow:{shadow_paper};flex:0 0 auto;}}
.fcard-icon{{font-size:92px;line-height:1;}}
.fcard-label{{font-family:'FN {mono}';font-size:26px;}}
.fcard.fork-file{{width:340px;height:270px;}}
.fcard.fork-file .fcard-icon{{font-size:86px;}}
.fcard.fork-file .fcard-label{{font-size:30px;}}
.fcard.fork-file .fcard-icon{{font-size:72px;}}
.fcard-q{{position:absolute;right:-22px;top:-22px;width:64px;height:64px;border-radius:50%;background:{amber};color:{on_amber};font-family:'FN {display}';font-weight:800;font-size:40px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,0.4);}}
.fork .stage{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;}}
.fork-paths{{width:864px;height:200px;display:block;}}
.fp{{fill:none;stroke:{acc};stroke-width:6;stroke-dasharray:600;stroke-dashoffset:600;stroke-linecap:round;}}
.routes{{display:flex;gap:40px;width:864px;justify-content:center;}}
.route{{position:relative;width:412px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;padding:28px 30px 28px 30px;text-align:left;}}
.route-title{{font-size:38px;font-weight:700;color:{text};line-height:1.15;}}
.route-sub{{font-size:30px;color:{muted};margin-top:8px;line-height:1.25;}}
.route-q,.approval-q{{position:absolute;right:-18px;top:-18px;width:56px;height:56px;border-radius:50%;background:{amber};color:{on_amber};font-family:'FN {display}';font-weight:800;font-size:36px;display:flex;align-items:center;justify-content:center;}}
.approval{{position:relative;margin-top:36px;width:864px;background:{surf};border:2px solid {amber};border-radius:26px;padding:26px 30px;font-size:38px;font-weight:600;color:{text};text-align:left;}}
.approval-q{{position:static;display:inline-flex;margin-right:18px;vertical-align:middle;}}
.beside .stage{{display:flex;align-items:center;justify-content:center;}}
.beside-row{{display:flex;gap:34px;align-items:center;width:864px;}}
.bcard{{flex:1 1 auto;background:{surf};border:2px solid {card_border};border-radius:{rad}px;padding:28px 30px;text-align:left;}}
.btitle{{font-family:'FN {display}';font-weight:700;font-size:38px;color:{acc};margin-bottom:12px;line-height:1.15;}}
.brow{{display:flex;gap:16px;align-items:flex-start;padding:10px 0;font-size:36px;line-height:1.22;color:{text};}}
.bmark{{width:44px;flex:0 0 44px;text-align:center;font-weight:800;color:{muted};padding-top:8px;}}
.brow.open .bmark{{color:{amber};}}
.btag{{display:inline-block;margin-top:14px;background:color-mix(in srgb,{amber} 22%,transparent);border:2px solid {amber};color:{text};border-radius:999px;padding:8px 20px;font-size:30px;}}
.fclose .stage{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px;}}
.upload-box{{width:760px;background:{surf};border:2px solid {card_border};border-radius:{rad}px;padding:36px;display:flex;flex-direction:column;align-items:center;gap:26px;}}
.upload-btn{{width:420px;padding:18px 0;border-radius:999px;background:{pal.get('button', acc)};color:{pal.get('on_accent', bg)};font-size:36px;font-weight:700;text-align:center;}}
.block-bar{{display:flex;align-items:center;gap:16px;width:100%;background:color-mix(in srgb,{red} 22%,transparent);border:2px solid {red};border-radius:16px;padding:16px 24px;font-size:34px;font-weight:600;color:{text};}}
.block-dot{{width:22px;height:22px;border-radius:50%;background:{red};flex:0 0 22px;}}
.domain{{font-family:'FN {display}';font-weight:{display_w};font-size:76px;letter-spacing:-0.01em;color:{text};text-shadow:{tshadow};}}
"""
    return themed_css(css, pal)
