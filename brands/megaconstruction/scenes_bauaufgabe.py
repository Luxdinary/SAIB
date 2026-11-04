# Format "Bauaufgabe" (Format-Bibel 02.11.2026, OneDrive\Business\02 Marke\Gigastruct\Format-Bibel.md).
# Executed at the end of brands/megaconstruction/scenes.py in that module's namespace (shares SceneCtx, SceneOut,
# _rel, _e, de_num, X0, WIDTH, COMPUTED, TEMPLATES, LIMITS, HOOK_SCENE_TYPES, css); not imported on its own.
#
# Every episode is one construction problem: Aufgabe -> Lastfall -> Prinzip -> Bau (Stückliste) -> Rechenblatt ->
# Probe -> Schriftfeld. The 2D layer looks like an engineering drawing (thin rules, square corners, mono labels,
# drawing frame and chapter rail drawn by render_gigastruct.py); the 3D model stays the main motif. Plans of this
# format set layout.format = "bauaufgabe" and layout.explainer = false; old gs_* plans render unchanged.
#
# | scene type   | beat           | data |
# |--------------|----------------|------|
# | gb_task      | Aufgabe (hook) | kicker, question, question_at, tag{text, at}, pins[] |
# | gb_load      | Lastfall       | headline, load{value, unit, label, sub, at}, goal{text, at}, pins[] |
# | gb_principle | Prinzip        | headline, rule{text, at}, pins[], note |
# | gb_build     | Bau            | headline, rows[{pos, part, qty, at}], pins[] |
# | gb_calc      | Rechenblatt    | headline, calcs[{label, a{value, unit, show}, op, b{...}, unit, round, decimals, prefix, expect, at}] |
# | gb_proof     | Probe          | headline, stamp{date, event, at}, limit{value, unit, label, at, ticks}, pins[] |
# | gb_close     | Schriftfeld    | statement, sheet, rows[[key, value]], cta{text, at} |
#
# pins: [{anchor, text, at, out, kind: "dim"|"label", side: "up"|"down"}] follow 3D anchors (gigastruct3d.js).
# _src (set by render_gigastruct.py from the beat's source_ids) is the source line under the zone.
# gb_calc computes every result here from its operands; "expect" (the spoken result) must match, else a problem.

_GB_LIMITS = {
    "gb_task": {"kicker": 34, "question": 70, "tag": 34},
    "gb_load": {"headline": 40, "value": 9, "label": 28, "sub": 44, "goal": 48},
    "gb_principle": {"headline": 40, "rule": 60, "note": 30},
    "gb_build": {"headline": 40, "part": 30, "qty": 8},
    "gb_calc": {"headline": 40, "label": 44},
    "gb_proof": {"headline": 40, "date": 16, "event": 30, "label": 34},
    "gb_close": {"statement": 60, "key": 10, "value": 34, "cta": 30},
    "pin": {"text": 26},
}


def _gb_lim(scene, key, val, where, out):
    lim = _GB_LIMITS.get(scene, {}).get(key)
    if lim and len(str(val)) > lim:
        out.problems.append(f"{scene}.{where}: {len(str(val))} chars > {lim}")


def _T(ctx, de, en):
    return en if getattr(ctx, "lang", "de") == "en" else de


def _fit(text, n, px):
    """inline font-size that keeps a value of more than n characters in its fixed column"""
    k = len(str(text))
    return f' style="font-size:{max(28, int(px * n / k))}px"' if k > n else ""


def _num(ctx, x, d):
    return de_num(x, d) if getattr(ctx, "lang", "de") != "en" else f"{x:,.{d}f}"


def _fade_in(out, sel, at, dy=16, dur=0.32):
    out.tl.append(f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"}},{at:.3f});')


def _gb_head(ctx, data, scene, out):
    h = data.get("headline", "")
    if not h:
        return ""
    _gb_lim(scene, "headline", h, "headline", out)
    at = ctx.t(0.1)
    _fade_in(out, f"#{ctx.sid}h", at, 14)
    out.events.append(at)
    return f'<div class="gb-head" style="top:{ctx.zone_top}px"><div class="gb-headline" id="{ctx.sid}h">{_e(h)}</div></div>'


def _gb_pins(ctx, data, out):
    parts = []
    for i, p in enumerate(data.get("pins", [])):
        _gb_lim("pin", "text", p.get("text", ""), f"pin {i + 1}", out)
        at = ctx.t(_rel(ctx, p, 0.6 + i * 0.8, out))
        pid = f"{ctx.sid}p{i}"
        if p.get("kind", "label") == "dim":
            parts.append(f'<div class="gs-dim" id="{pid}" data-anchor="{_e(p["anchor"])}"><span>{_e(p.get("text", ""))}</span></div>')
            out.tl.append(f'tl.fromTo("#{pid} span",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{at:.3f});')
        else:
            side = p.get("side", "up")
            parts.append(f'<div class="gb-pin gb-pin-{side}" id="{pid}" data-anchor="{_e(p["anchor"])}"><span class="gb-pin-dot"></span>'
                         f'<span class="gb-pin-line"></span><span class="gb-pin-text">{_e(p.get("text", ""))}</span></div>')
            out.tl.append(f'tl.fromTo("#{pid} .gb-pin-line",{{scaleY:0}},{{scaleY:1,duration:0.25}},{at:.3f});')
            out.tl.append(f'tl.fromTo("#{pid} .gb-pin-dot",{{scale:0}},{{scale:1,duration:0.2}},{at:.3f});')
            _fade_in(out, f"#{pid} .gb-pin-text", at + 0.1, 8, 0.28)
        if p.get("out"):
            t_out = ctx.t(_rel(ctx, {"at": p["out"]}, ctx.duration - 0.3, out))
            out.tl.append(f'tl.to("#{pid}",{{opacity:0,duration:0.25}},{t_out:.3f});')
        out.events.append(at)
    return "".join(parts)


def _gb_src(ctx, data):
    s = data.get("_src", "")
    if not s:
        return ""
    return f'<div class="gb-src" style="top:{int(data.get("src_y", 1112))}px">{_e(s)}</div>'


def gb_task(ctx, data):
    """Aufgabe: the construction problem as a question; a task stamp and an optional tag (place, height)."""
    out = SceneOut(html="")
    sid = ctx.sid
    k, q = data.get("kicker", ""), data.get("question", "")
    _gb_lim("gb_task", "kicker", k, "kicker", out)
    _gb_lim("gb_task", "question", q, "question", out)
    q_at = ctx.t(_rel(ctx, data, 0.1, out, "question_at"))
    parts = [f'<div class="gb-head" style="top:{ctx.zone_top}px">']
    if k:
        parts.append(f'<div class="gb-stamp-k" id="{sid}k">{_e(k)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}k",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.28,ease:"power2.out"}},{ctx.t(0.05):.3f});')
    parts.append(f'<div class="gb-question" id="{sid}q">{_e(q)}</div></div>')
    _fade_in(out, f"#{sid}q", q_at, 26, 0.4)
    out.events.append(q_at)
    tag = data.get("tag") or {}
    if tag:
        _gb_lim("gb_task", "tag", tag.get("text", ""), "tag", out)
        at = ctx.t(_rel(ctx, tag, 2.0, out))
        parts.append(f'<div class="gb-row" style="top:{int(tag.get("y", 1010))}px"><div class="gb-tag" id="{sid}t">{_e(tag.get("text", ""))}</div></div>')
        _fade_in(out, f"#{sid}t", at, 12)
        out.events.append(at)
    parts.append(_gb_pins(ctx, data, out))
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


def gb_load(ctx, data):
    """Lastfall: the design load as a drawing box (label, big value, sub line) and the goal the solution must reach."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_gb_head(ctx, data, "gb_load", out)]
    ld = data.get("load") or {}
    if ld:
        for key in ("value", "label", "sub"):
            _gb_lim("gb_load", key, ld.get(key, ""), f"load.{key}", out)
        at = ctx.t(_rel(ctx, ld, 0.8, out))
        top = ctx.zone_top + int(ld.get("dy", 470))
        parts.append(f'<div class="gb-box gb-load" id="{sid}l" style="top:{top}px"><div class="gb-box-k">{_e(ld.get("label", "Lastfall"))}</div>'
                     f'<div class="gb-load-v">{_e(ld.get("value", ""))}<small>{_e(ld.get("unit", ""))}</small></div>'
                     f'<div class="gb-box-s">{_e(ld.get("sub", ""))}</div></div>')
        if ld.get("enter") == "swipe":   # Neustart 2026-11: the load box swipes in from the right edge
            out.tl.append(f'tl.fromTo("#{sid}l",{{opacity:0,x:760}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{at:.3f});')
        else:
            _fade_in(out, f"#{sid}l", at, 22, 0.35)
        out.tl.append(f'tl.fromTo("#{sid}l .gb-load-v",{{scale:0.86}},{{scale:1,duration:0.45,ease:"back.out(2)"}},{at:.3f});')
        out.events.append(at)
    goal = data.get("goal") or {}
    if goal:
        _gb_lim("gb_load", "goal", goal.get("text", ""), "goal", out)
        at = ctx.t(_rel(ctx, goal, 3.0, out))
        top = ctx.zone_top + int(goal.get("dy", 720))
        parts.append(f'<div class="gb-row" style="top:{top}px"><div class="gb-goal" id="{sid}g"><b>{_e(goal.get("key", _T(ctx, "ZIEL", "GOAL")))}</b>{_e(goal.get("text", ""))}</div></div>')
        _fade_in(out, f"#{sid}g", at, 14)
        out.events.append(at)
    parts.append(_gb_pins(ctx, data, out))
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


def gb_principle(ctx, data):
    """Prinzip: the solution in one rule; labels pinned to the model; a 'vereinfacht' note."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_gb_head(ctx, data, "gb_principle", out), _gb_pins(ctx, data, out)]
    rule = data.get("rule") or {}
    if rule:
        _gb_lim("gb_principle", "rule", rule.get("text", ""), "rule", out)
        at = ctx.t(_rel(ctx, rule, 3.0, out))
        top = ctx.zone_top + int(rule.get("dy", 640))
        parts.append(f'<div class="gb-row" style="top:{top}px"><div class="gb-rule" id="{sid}r">{_e(rule.get("text", ""))}</div></div>')
        _fade_in(out, f"#{sid}r", at, 18)
        out.events.append(at)
    note = data.get("note", "")
    if note:
        _gb_lim("gb_principle", "note", note, "note", out)
        parts.append(f'<div class="gb-row" style="top:{ctx.zone_top + int(data.get("note_dy", 110))}px"><div class="gb-note" id="{sid}n">{_e(note)}</div></div>')
        out.tl.append(f'tl.fromTo("#{sid}n",{{opacity:0}},{{opacity:1,duration:0.3}},{ctx.t(0.5):.3f});')
        if data.get("note_out"):   # the note belongs to the model; it leaves when a picture takes over (Neustart 2026-11)
            out.tl.append(f'tl.to("#{sid}n",{{opacity:0,duration:0.25}},{ctx.t(_rel(ctx, {"at": data["note_out"]}, ctx.duration - 0.3, out)):.3f});')
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


def gb_build(ctx, data):
    """Bau: a bill of materials (Stückliste) filling row by row while the 3D model is assembled at the same words."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_gb_head(ctx, data, "gb_build", out), _gb_pins(ctx, data, out)]
    rows = data.get("rows", [])[:5]
    top = ctx.zone_top + int(data.get("table_dy", 1100 - ctx.zone_top - 90 * len(rows) - 110))
    trs = [f'<div class="gb-tr gb-th"><span>POS</span><span>{_T(ctx, "BAUTEIL", "PART")}</span><span>{_T(ctx, "MENGE", "QTY")}</span></div>']
    for i, r in enumerate(rows):
        _gb_lim("gb_build", "part", r.get("part", ""), f"row {i + 1} part", out)
        _gb_lim("gb_build", "qty", r.get("qty", ""), f"row {i + 1} qty", out)
        at = ctx.t(_rel(ctx, r, 0.6 + i * 1.6, out))
        trs.append(f'<div class="gb-tr" id="{sid}r{i}"><span>{_e(r.get("pos", i + 1))}</span><span>{_e(r.get("part", ""))}</span>'
                   f'<span class="gb-qty" id="{sid}q{i}"{_fit(r.get("qty", ""), 6, 46)}>{_e(r.get("qty", ""))}</span></div>')
        out.tl.append(f'tl.fromTo("#{sid}r{i}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}q{i}",{{scale:1.25}},{{scale:1,duration:0.4,ease:"back.out(2)"}},{at + 0.1:.3f});')
        out.events.append(at)
    parts.append(f'<div class="gb-table" id="{sid}tb" style="top:{top}px"><div class="gb-box-k">{_e(data.get("table_title", _T(ctx, "Stückliste", "Bill of materials")))}</div>{"".join(trs)}</div>')
    first = min((ctx.t(_rel(ctx, r, 0.6 + i * 1.6, SceneOut(html=""))) for i, r in enumerate(rows)), default=ctx.t(0.3))
    out.tl.append(f'tl.fromTo("#{sid}tb",{{opacity:0}},{{opacity:1,duration:0.3}},{max(ctx.start, first - 0.3):.3f});')
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


_OPS = {"×": lambda a, b: a * b, "÷": lambda a, b: a / b, "−": lambda a, b: a - b, "+": lambda a, b: a + b}


def _side(ctx, d):
    if d.get("show"):
        return d["show"]
    v = float(d["value"])
    dd = 0 if v.is_integer() else len(repr(v).split(".")[1])
    return f'{_num(ctx, v, dd)} {d.get("unit", "")}'.strip()


def gb_calc(ctx, data):
    """Rechenblatt: up to three calculation lines on squared paper. Results are computed here (never typed into the plan);
    'expect' is the value spoken in the script and must equal the rounded result, else a problem is reported."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_gb_head(ctx, data, "gb_calc", out)]
    lines = []
    for i, c in enumerate(data.get("calcs", [])[:3]):
        _gb_lim("gb_calc", "label", c.get("label", ""), f"calc {i + 1} label", out)
        a, b, op = c["a"], c["b"], c.get("op", "÷")
        res = _OPS[op](float(a["value"]), float(b["value"]))
        rnd = c.get("round")
        shown = round(res / rnd) * rnd if rnd else res
        dec = int(c.get("decimals", 0 if float(shown).is_integer() else 2))
        r_txt = f'{c.get("prefix", "")}{_num(ctx, shown, dec)}'
        expr = f"{_side(ctx, a)} {op} {_side(ctx, b)}"
        exact = _num(ctx, res, 0 if float(res).is_integer() else 4)
        COMPUTED.append({"beat_scene": sid, "label": c.get("label", ""), "calculation": f"{expr} = {exact}",
                         "shown": f"{r_txt} {c.get('unit', '')}".strip(), "result": round(res, 6)})
        if "expect" in c and abs(float(c["expect"]) - float(shown)) > 1e-9:
            out.problems.append(f"gb_calc {i + 1}: spoken {c['expect']} != computed {shown}")
        at = ctx.t(_rel(ctx, c, 0.6 + i * 3.0, out))
        r_at = ctx.t(_rel(ctx, c, at - ctx.start + 0.9, out, "result_at"))
        lines.append(f'<div class="gb-cl" id="{sid}c{i}"><div class="gb-cl-l">{_e(c.get("label", ""))}</div>'
                     f'<div class="gb-cl-e"><span class="gb-cl-x" id="{sid}c{i}x">{_e(expr)} =</span>'
                     f'<span class="gb-cl-r" id="{sid}c{i}r"{_fit(r_txt + c.get("unit", ""), 9, 76)}>{_e(r_txt)}<small>{_e(c.get("unit", ""))}</small></span></div></div>')
        _fade_in(out, f"#{sid}c{i}", at, 12, 0.28)
        out.tl.append(f'tl.fromTo("#{sid}c{i}x",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.7,ease:"none"}},{at:.3f});')
        out.tl.append(f'tl.fromTo("#{sid}c{i}r",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{max(r_at, at + 0.5):.3f});')
        out.events += [at, max(r_at, at + 0.5)]
    top = ctx.zone_top + int(data.get("sheet_dy", 470))
    parts.append(f'<div class="gb-sheet" id="{sid}s" style="top:{top}px"><div class="gb-box-k">{_e(data.get("sheet_title", _T(ctx, "Nachgerechnet", "Checked")))}</div>{"".join(lines)}</div>')
    out.tl.append(f'tl.fromTo("#{sid}s",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{ctx.t(0.2):.3f});')
    if data.get("scale"):
        parts.append(_gb_scale(ctx, data["scale"], out))
    parts.append(_gb_pins(ctx, data, out))
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


_TOWER_SVG = ('<svg viewBox="0 0 40 100" aria-hidden="true"><path d="M20 0 L22.5 28 L29 62 L38 100 H28 C26 86 14 86 12 100 H2 '
              'L11 62 L17.5 28 Z M14 70 H26 M16 52 H24"/></svg>')


def _gb_scale(ctx, sc, out):
    """Balkenwaage (Neustart 2026-11): one element on the left pan, schematic towers stacking on the right pan; the beam
    levels with every tower. Weights come from the plan (a source), the tilt is computed from them, never typed."""
    sid = ctx.sid
    left_t, unit_t, n = float(sc["left_t"]), float(sc["unit_t"]), int(sc["count"])
    for key in ("left", "right", "note"):
        if len(str(sc.get(key, ""))) > 26:
            out.problems.append(f"gb_calc.scale.{key}: {len(str(sc.get(key, '')))} chars > 26")
    top = ctx.zone_top + int(sc.get("dy", 96))
    tilt0 = float(sc.get("tilt", 9.0))
    ang = [-tilt0 * max(-1.0, min(1.0, (left_t - k * unit_t) / left_t)) for k in range(n + 1)]
    towers = "".join(f'<i class="gb-twr" id="{sid}w{k}">{_TOWER_SVG}</i>' for k in range(n))
    html_ = (f'<div class="gb-scalebox" id="{sid}sb" style="top:{top}px"><div class="gb-box-k">{_e(sc.get("title", _T(ctx, "Waage", "Balance")))}</div>'
             f'<div class="gb-beam" id="{sid}bm"><div class="gb-pan gb-pan-l"><div class="gb-blk">{_e(sc.get("left", ""))}</div></div>'
             f'<div class="gb-pan gb-pan-r"><div class="gb-twrs">{towers}</div><div class="gb-pan-k">{_e(sc.get("right", ""))}</div></div></div>'
             f'<div class="gb-fulcrum"></div>' + (f'<div class="gb-scale-note">{_e(sc["note"])}</div>' if sc.get("note") else "") + '</div>')
    at = ctx.t(_rel(ctx, sc, 0.5, out))
    step = float(sc.get("step", 0.32))
    out.tl.append(f'tl.fromTo("#{sid}sb",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.3}},{max(ctx.start, at - 0.4):.3f});')
    out.tl.append(f'tl.set("#{sid}bm",{{rotation:{ang[0]:.2f}}},{max(ctx.start, at - 0.4):.3f});')
    for k in range(n):
        tk = at + k * step
        out.tl.append(f'tl.fromTo("#{sid}w{k}",{{opacity:0,y:-90}},{{opacity:1,y:0,duration:0.22,ease:"power2.in"}},{tk:.3f});')
        out.tl.append(f'tl.to("#{sid}bm",{{rotation:{ang[k + 1]:.2f},duration:0.3,ease:"back.out(2)"}},{tk + 0.2:.3f});')
    out.events += [at, at + (n - 1) * step]
    return html_


def _gb_clock(ctx, ck, out):
    """Zeitraffer-Uhr (Neustart 2026-11): a dial whose hand runs through the hours of an event from a source and a
    counter 0 .. hours; the last value can be worded like the script ("gut 14 h")."""
    sid = ctx.sid
    hours = int(ck["hours"])
    at = ctx.t(_rel(ctx, ck, 0.5, out))
    end = ctx.t(_rel(ctx, {"at": ck.get("until", ck.get("at"))}, at - ctx.start + 2.4, out))
    end = max(end, at + 1.2)
    top = ctx.zone_top + int(ck.get("dy", 470))
    nums = "".join(f'<span id="{sid}n{k}">{k} h</span>' for k in range(hours))
    end_text = ck.get("end_text", f"{hours} h")
    nums += f'<span id="{sid}n{hours}">{_e(end_text)}</span>'
    fs = min(96, int(600 / (0.5 * max(1, len(end_text)))))   # Oswald 700 runs about 0.5 em a character; keeps "just over 14 h" in the box
    html_ = (f'<div class="gb-clockbox" id="{sid}cb" style="top:{top}px"><div class="gb-dial"><i class="gb-hand" id="{sid}hd"></i><b></b></div>'
             f'<div><div class="gb-box-k">{_e(ck.get("label", _T(ctx, "Dauer", "Duration")))}</div>'
             f'<div class="gb-count" style="font-size:{fs}px;min-width:{max(330, int(0.52 * fs * len(end_text)))}px">{nums}</div></div></div>')
    out.tl.append(f'tl.fromTo("#{sid}cb",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3}},{at - 0.3:.3f});')
    out.tl.append(f'tl.fromTo("#{sid}hd",{{rotation:0}},{{rotation:{hours * 30},duration:{end - at:.3f},ease:"none"}},{at:.3f});')
    for k in range(hours + 1):
        tk = at + (end - at) * k / hours
        out.tl.append(f'tl.set("#{sid}n{k}",{{opacity:0}},{ctx.start:.3f});')
        out.tl.append(f'tl.set("#{sid}n{k}",{{opacity:1}},{tk:.3f});')
        if k < hours:
            out.tl.append(f'tl.set("#{sid}n{k}",{{opacity:0}},{at + (end - at) * (k + 1) / hours:.3f});')
    out.events += [at, end]
    return html_


def gb_proof(ctx, data):
    """Probe: a dated test-log stamp (real event from a source) and a limit gauge (design limit of the solution)."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = [_gb_head(ctx, data, "gb_proof", out), _gb_pins(ctx, data, out)]
    if data.get("clock"):
        parts.append(_gb_clock(ctx, data["clock"], out))
    st = data.get("stamp") or {}
    if st:
        _gb_lim("gb_proof", "date", st.get("date", ""), "stamp.date", out)
        _gb_lim("gb_proof", "event", st.get("event", ""), "stamp.event", out)
        at = ctx.t(_rel(ctx, st, 0.6, out))
        parts.append(f'<div class="gb-row" style="top:{ctx.zone_top + int(st.get("dy", 150))}px"><div class="gb-stamp" id="{sid}st">'
                     f'<div class="gb-stamp-d">{_e(st.get("date", ""))}</div><div class="gb-stamp-e">{_e(st.get("event", ""))}</div></div></div>')
        out.tl.append(f'tl.fromTo("#{sid}st",{{opacity:0,scale:1.35,rotation:-3}},{{opacity:1,scale:1,rotation:-3,duration:0.3,ease:"power2.in"}},{at:.3f});')
        out.events.append(at)
    lim = data.get("limit") or {}
    if lim:
        _gb_lim("gb_proof", "label", lim.get("label", ""), "limit.label", out)
        at = ctx.t(_rel(ctx, lim, 3.0, out))
        v = float(lim["value"])
        ticks = lim.get("ticks") or [0, v / 3, 2 * v / 3, v]
        w = WIDTH - 52 - 60
        tk = "".join(f'<i style="left:{30 + w * (x / v):.0f}px"><em>{_e(_num(ctx, x, 0))}</em></i>' for x in ticks)
        top = ctx.zone_top + int(lim.get("dy", 600))
        parts.append(f'<div class="gb-box gb-gauge" id="{sid}g" style="top:{top}px"><div class="gb-box-k">{_e(lim.get("label", ""))}</div>'
                     f'<div class="gb-gauge-v"><b>{_e(_num(ctx, v, 0))}</b> {_e(lim.get("unit", ""))}</div>'
                     f'<div class="gb-scale"><div class="gb-scale-fill" id="{sid}gf" style="width:{w}px"></div>{tk}</div></div>')
        _fade_in(out, f"#{sid}g", at, 18)
        out.tl.append(f'tl.fromTo("#{sid}gf",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:"power2.out"}},{at + 0.2:.3f});')
        out.events.append(at)
    parts.append(_gb_src(ctx, data))
    out.html = "".join(parts)
    return out


def gb_close(ctx, data):
    """Schriftfeld: the episode as the title block of a drawing (Aufgabe, Lösung, Bauteil, Stand) plus the follow chip."""
    out = SceneOut(html="")
    sid = ctx.sid
    parts = []
    s = data.get("statement", "")
    if s:
        _gb_lim("gb_close", "statement", s, "statement", out)
        parts.append(f'<div class="gb-head" style="top:{ctx.zone_top}px"><div class="gb-headline" id="{sid}h">{_e(s)}</div></div>')
        _fade_in(out, f"#{sid}h", ctx.t(0.2), 14)
        out.events.append(ctx.t(0.2))
    rows = data.get("rows", [])[:5]
    trs = []
    for i, (k, v) in enumerate(rows):
        _gb_lim("gb_close", "key", k, f"row {i + 1} key", out)
        _gb_lim("gb_close", "value", v, f"row {i + 1} value", out)
        trs.append(f'<div class="gb-tb-r" id="{sid}r{i}"><span>{_e(k)}</span><b>{_e(v)}</b></div>')
        out.tl.append(f'tl.fromTo("#{sid}r{i}",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:0.25}},{ctx.t(0.75 + i * 0.3):.3f});')
    top = ctx.zone_top + int(data.get("block_dy", 1100 - ctx.zone_top - 70 * len(rows) - 64))
    parts.append(f'<div class="gb-tblock" id="{sid}tb" style="top:{top}px"><div class="gb-tb-h"><span>GIGASTRUCT</span><span>{_e(data.get("sheet", ""))}</span></div>{"".join(trs)}</div>')
    out.tl.append(f'tl.fromTo("#{sid}tb",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{ctx.t(0.6):.3f});')
    out.events.append(ctx.t(0.6))
    seal = data.get("seal", _T(ctx, "Quellen geprüft", "Sources checked"))
    if seal:   # stamped onto the title block in the middle of the beat (a long closing line keeps the frame changing)
        at = ctx.t(max(2.2, 0.5 * ctx.duration))
        parts.append(f'<div class="gb-seal" id="{sid}se" style="top:{top - 86}px">{_e(seal)}</div>')
        out.tl.append(f'tl.fromTo("#{sid}se",{{opacity:0,scale:1.4,rotation:-6}},{{opacity:1,scale:1,rotation:-6,duration:0.28,ease:"power2.in"}},{at:.3f});')
        out.events.append(at)
    cta = data.get("cta") or {}
    if cta:
        _gb_lim("gb_close", "cta", cta.get("text", ""), "cta", out)
        at = ctx.t(_rel(ctx, cta, 3.0, out))
        parts.append(f'<div class="gb-row" style="top:{top - 96}px"><div class="gb-cta" id="{sid}ct">{_e(cta.get("text", ""))}</div></div>')
        _fade_in(out, f"#{sid}ct", at, 12)
        out.events.append(at)
    out.html = "".join(parts)
    return out


def css_gb(pal, display, body, mono):
    acc, bg, text, muted = pal["accent"], pal["bg"], pal["text"], pal.get("muted", "#8F9CA8")
    line = f"color-mix(in srgb,{text} 70%,transparent)"
    panel = f"color-mix(in srgb,{bg} 92%,transparent)"
    thin = f"color-mix(in srgb,{text} 30%,transparent)"
    return f"""
.gb-head{{position:absolute;left:{X0}px;width:{WIDTH}px;text-align:left;}}
.gb-headline{{font-family:'FN {display}';font-weight:700;font-size:74px;line-height:1.04;color:{text};text-transform:uppercase;letter-spacing:0.01em;text-shadow:0 3px 18px rgba(6,14,24,0.7);}}
.gb-question{{font-family:'FN {display}';font-weight:700;font-size:86px;line-height:1.02;color:{text};text-shadow:0 4px 24px rgba(6,14,24,0.75);}}
.gb-stamp-k{{display:inline-block;font-family:'FN {mono}';font-weight:700;font-size:30px;letter-spacing:0.12em;text-transform:uppercase;color:{acc};border:3px solid {acc};padding:6px 16px;margin-bottom:22px;background:{panel};}}
.gb-row{{position:absolute;left:{X0}px;width:{WIDTH}px;display:flex;justify-content:flex-start;}}
.gb-tag{{font-family:'FN {mono}';font-weight:700;font-size:34px;color:{text};background:{panel};border-left:8px solid {acc};padding:10px 20px;}}
.gb-box{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:18px 26px 22px;background:{panel};border:2px solid {line};}}
.gb-box-k{{font-family:'FN {mono}';font-weight:700;font-size:26px;letter-spacing:0.14em;text-transform:uppercase;color:{muted};margin-bottom:8px;}}
.gb-box-s{{font-family:'FN {mono}';font-size:30px;color:{text};margin-top:6px;}}
.gb-load{{border-left:16px solid {acc};background-image:repeating-linear-gradient(135deg,transparent 0 18px,color-mix(in srgb,{acc} 10%,transparent) 18px 22px);}}
.gb-load-v{{font-family:'FN {display}';font-weight:700;font-size:150px;line-height:1;color:{acc};}}
.gb-load-v small{{font-size:58px;margin-left:12px;color:{text};}}
.gb-goal{{font-family:'FN {display}';font-weight:600;font-size:46px;line-height:1.1;color:{text};background:{panel};border:2px solid {line};padding:14px 22px;display:flex;gap:18px;align-items:baseline;}}
.gb-goal b{{font-family:'FN {mono}';font-size:26px;letter-spacing:0.14em;color:{acc};}}
.gb-rule{{font-family:'FN {display}';font-weight:700;font-size:58px;line-height:1.08;color:{text};background:{panel};border-top:6px solid {acc};padding:16px 24px 20px;}}
.gb-note{{font-family:'FN {mono}';font-size:26px;letter-spacing:0.08em;text-transform:uppercase;color:{text};border:2px dashed {muted};padding:6px 14px;background:{panel};}}
.gb-pin{{position:absolute;width:0;height:0;}}
.gb-pin-dot{{position:absolute;left:-9px;top:-9px;width:18px;height:18px;border-radius:50%;border:4px solid {acc};background:{bg};box-sizing:border-box;}}
.gb-pin-line{{position:absolute;left:-1px;width:2px;height:110px;background:{text};transform-origin:50% 100%;}}
.gb-pin-up .gb-pin-line{{bottom:9px;}}
.gb-pin-down .gb-pin-line{{top:9px;transform-origin:50% 0%;}}
.gb-pin-text{{position:absolute;white-space:nowrap;transform:translateX(-50%);font-family:'FN {mono}';font-weight:700;font-size:36px;color:{text};background:{panel};border:2px solid {text};padding:6px 16px;}}
.gb-pin-up .gb-pin-text{{bottom:118px;}}
.gb-pin-down .gb-pin-text{{top:118px;}}
.gb-table{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:14px 22px 6px;background:{panel};border:2px solid {line};}}
.gb-tr{{display:grid;grid-template-columns:70px 1fr 190px;align-items:center;border-top:2px solid {thin};min-height:86px;font-family:'FN {display}';font-weight:600;font-size:42px;color:{text};}}
.gb-tr span:first-child{{font-family:'FN {mono}';font-size:28px;color:{muted};}}
.gb-th{{min-height:40px;border-top:none;font-family:'FN {mono}';font-size:24px;letter-spacing:0.1em;color:{text};opacity:0.8;font-weight:700;}}
.gb-th span:first-child{{font-size:24px;}}
.gb-qty{{font-family:'FN {mono}';font-weight:700;font-size:46px;color:{acc};text-align:right;padding-right:10px;transform-origin:right center;}}
.gb-th span:last-child{{text-align:right;padding-right:10px;}}
.gb-sheet{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;padding:16px 24px 8px;background-color:{panel};
  background-image:linear-gradient({thin} 1px,transparent 1px),linear-gradient(90deg,{thin} 1px,transparent 1px);background-size:36px 36px;border:2px solid {line};}}
.gb-cl{{border-top:2px solid {thin};padding:12px 0 16px;}}
.gb-cl-l{{font-family:'FN {mono}';font-size:26px;color:{text};opacity:0.8;letter-spacing:0.04em;}}
.gb-cl-e{{display:flex;align-items:baseline;justify-content:space-between;gap:18px;margin-top:4px;}}
.gb-cl-x{{font-family:'FN {mono}';font-weight:700;font-size:40px;color:{text};white-space:nowrap;}}
.gb-cl-r{{font-family:'FN {display}';font-weight:700;font-size:76px;line-height:1;color:{bg};background:{acc};padding:6px 16px 4px;white-space:nowrap;}}
.gb-cl-r small{{font-size:40px;margin-left:8px;}}
.gb-stamp{{border:5px solid {acc};padding:10px 26px 14px;background:{panel};color:{acc};font-family:'FN {mono}';font-weight:700;text-transform:uppercase;}}
.gb-stamp-d{{font-size:56px;letter-spacing:0.06em;}}
.gb-stamp-e{{font-size:32px;letter-spacing:0.08em;color:{text};margin-top:4px;}}
.gb-gauge-v{{font-family:'FN {display}';font-weight:600;font-size:52px;color:{text};}}
.gb-gauge-v b{{font-size:104px;color:{acc};line-height:1;}}
.gb-scale{{position:relative;height:84px;margin-top:10px;}}
.gb-scale-fill{{position:absolute;left:30px;top:12px;height:22px;background:{acc};transform-origin:left center;}}
.gb-scale i{{position:absolute;top:4px;width:3px;height:38px;margin-left:-1px;background:{text};}}
.gb-scale i em{{position:absolute;top:42px;left:0;transform:translateX(-50%);font-style:normal;font-family:'FN {mono}';font-size:26px;color:{text};opacity:0.8;}}
.gb-tblock{{position:absolute;left:{X0}px;width:{WIDTH}px;box-sizing:border-box;background:{panel};border:3px solid {text};}}
.gb-tb-h{{display:flex;justify-content:space-between;padding:10px 20px;border-bottom:3px solid {text};font-family:'FN {mono}';font-weight:700;font-size:26px;letter-spacing:0.16em;color:{text};}}
.gb-tb-r{{display:grid;grid-template-columns:200px 1fr;align-items:center;min-height:68px;border-bottom:2px solid {thin};}}
.gb-tb-r:last-child{{border-bottom:none;}}
.gb-tb-r span{{font-family:'FN {mono}';font-size:24px;letter-spacing:0.12em;text-transform:uppercase;color:{text};opacity:0.75;padding-left:20px;border-right:2px solid {thin};align-self:stretch;display:flex;align-items:center;}}
.gb-tb-r b{{font-family:'FN {display}';font-weight:600;font-size:42px;color:{text};padding-left:20px;}}
.gb-cta{{font-family:'FN {mono}';font-weight:700;font-size:36px;color:{bg};background:{acc};padding:12px 26px;}}
.gb-src{{position:absolute;left:{X0}px;max-width:820px;font-family:'FN {mono}';font-size:24px;line-height:1.3;color:{text};opacity:0.88;background:{panel};padding:4px 12px;}}
#gbframe{{position:absolute;left:36px;top:36px;width:1004px;height:1844px;box-sizing:border-box;z-index:3;pointer-events:none;border:3px solid color-mix(in srgb,{text} 34%,transparent);
  background-image:linear-gradient(color-mix(in srgb,{text} 6%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,{text} 6%,transparent) 1px,transparent 1px);background-size:100px 100px;background-position:-2px -2px;}}
#gbframe::before,#gbframe::after{{content:"";position:absolute;width:44px;height:44px;border:4px solid color-mix(in srgb,{text} 55%,transparent);}}
#gbframe::before{{left:-4px;top:-4px;border-right:none;border-bottom:none;}}
#gbframe::after{{right:-4px;bottom:-4px;border-left:none;border-top:none;}}
.gb-seal{{position:absolute;right:{X0 + 16}px;z-index:7;font-family:'FN {mono}';font-weight:700;font-size:24px;letter-spacing:0.12em;text-transform:uppercase;color:{acc};border:4px solid {acc};padding:6px 14px;background:color-mix(in srgb,{bg} 85%,transparent);}}
#gbframe i{{position:absolute;width:2px;height:22px;background:color-mix(in srgb,{text} 40%,transparent);top:-2px;}}
#gbframe b{{position:absolute;width:22px;height:2px;background:color-mix(in srgb,{text} 40%,transparent);left:-2px;}}
#gbrail{{position:absolute;left:{X0}px;width:{WIDTH}px;top:190px;z-index:6;display:flex;gap:10px;font-family:'FN {mono}';font-weight:700;font-size:24px;line-height:1.05;letter-spacing:0.01em;}}
#gbrail b{{display:block;font-size:24px;}}
#gbrail div{{flex:1;min-width:0;white-space:nowrap;overflow:hidden;padding:6px 0 4px;border-top:5px solid color-mix(in srgb,{text} 28%,transparent);color:color-mix(in srgb,{text} 55%,transparent);}}
#gbrail div.done{{border-top-color:color-mix(in srgb,{text} 75%,transparent);color:color-mix(in srgb,{text} 80%,transparent);}}
#gbrail div.on{{border-top-color:{acc};color:{acc};}}
.gb-scalebox{{position:absolute;left:{X0}px;width:{WIDTH}px;height:320px;box-sizing:border-box;padding:14px 22px;background:{panel};border:2px solid {line};}}
.gb-beam{{position:absolute;left:90px;right:90px;top:190px;height:10px;background:{text};transform-origin:50% 50%;}}
.gb-fulcrum{{position:absolute;left:50%;top:200px;margin-left:-34px;width:0;height:0;border-left:34px solid transparent;border-right:34px solid transparent;border-bottom:70px solid {line};}}
.gb-pan{{position:absolute;bottom:10px;width:300px;display:flex;flex-direction:column;align-items:center;}}
.gb-pan-l{{left:-20px;}}
.gb-pan-r{{right:-20px;}}
.gb-blk{{font-family:'FN {display}';font-weight:700;font-size:40px;color:{bg};background:{acc};padding:8px 16px;white-space:nowrap;}}
.gb-twrs{{display:flex;align-items:flex-end;gap:2px;height:96px;}}
.gb-twr{{display:block;width:36px;height:90px;}}
.gb-twr svg{{width:100%;height:100%;fill:none;stroke:{text};stroke-width:3;}}
.gb-pan-k{{position:absolute;top:104px;font-family:'FN {mono}';font-weight:700;font-size:24px;color:{text};white-space:nowrap;}}
.gb-scale-note{{position:absolute;right:20px;top:14px;font-family:'FN {mono}';font-size:24px;letter-spacing:0.08em;text-transform:uppercase;color:{text};border:2px dashed {muted};padding:3px 10px;}}
.gb-clockbox{{position:absolute;left:{X0}px;display:flex;gap:28px;align-items:center;box-sizing:border-box;padding:18px 26px;background:{panel};border:2px solid {line};border-left:16px solid {acc};}}
.gb-dial{{position:relative;width:150px;height:150px;border-radius:50%;border:5px solid {text};box-sizing:border-box;background:repeating-conic-gradient(from -1deg,{text} 0deg 2deg,transparent 2deg 30deg);}}
.gb-dial b{{position:absolute;inset:14px;border-radius:50%;background:{bg};}}
.gb-hand{{position:absolute;left:50%;top:8px;width:8px;height:62px;margin-left:-4px;background:{acc};transform-origin:50% 100%;z-index:2;}}
.gb-count{{position:relative;height:110px;min-width:330px;}}
.gb-count span{{position:absolute;left:0;top:0;font-family:'FN {display}';font-weight:700;font-size:inherit;line-height:1.1;color:{acc};white-space:nowrap;}}
"""


TEMPLATES.update({"gb_task": gb_task, "gb_load": gb_load, "gb_principle": gb_principle, "gb_build": gb_build,
                  "gb_calc": gb_calc, "gb_proof": gb_proof, "gb_close": gb_close})
if "gb_task" not in HOOK_SCENE_TYPES:
    HOOK_SCENE_TYPES.append("gb_task")
LIMITS.update({t: {k: v for k, v in lim.items() if k in ("kicker", "headline", "question", "statement", "note")}
               for t, lim in _GB_LIMITS.items() if t != "pin"})
_css_gs = css


def css(pal, display, body, mono):  # noqa: F811 (the old gs_* styles plus the Bauaufgabe styles)
    return _css_gs(pal, display, body, mono) + css_gb(pal, display, body, mono)
