"""Promptwerk format "Echtlauf" (02.11.2026): scene types rec_* that replay a real recorded Claude Code run.

Loaded by `brands/claude_workflows/scenes.py`, which merges TEMPLATES, LIMITS, HOOK_SCENE_TYPES, CSS, LAYER and
MANIFEST_EXTRA. A plan opts in with `layout.format = "echtlauf"` and `layout.echtlauf.recording = "<id>"`; every
rec_* scene reads its text from `echtlauf/recordings/<id>/` (transcript.json, outcome.json, meta.json, files/), so
the frame shows the recorded wording, never retyped text. Verdict stamps come from outcome.json, not from the plan.

Scene types:
  rec_auftrag   hook: question, the exact command typed into a terminal, the planned runs as open chips
  rec_setup     the sandbox: file tree and one file shown verbatim, labelled as sample data
  rec_rule      the rule file as written for a run, plus a quote from the documentation
  rec_replay    one run replayed: lines appear at their recorded times (real time or a labelled time-lapse),
                gutter with the recorded seconds, verdict from outcome.json
  rec_result    all runs with their recorded outcome and repetition count
  rec_protokoll close: recording protocol (date, version, model, runs, repetitions) and claim

Event times follow the voice like the pw_* scenes: `<event>_word` anchors to a spoken word, else `<event>_at`
seconds from the beat start, else a fraction of the beat. Geometry: scene box 864 px wide at x 108, zone_top/zone_h.
"""
from __future__ import annotations

import html
import json
import math
from pathlib import Path

from fn.render.templates import SceneCtx, SceneOut

HERE = Path(__file__).resolve().parent
REC_DIR = HERE / "recordings"

LIMITS: dict[str, dict[str, int]] = {
    "rec_auftrag": {"question": 48, "chip": 30},
    "rec_setup": {"label": 40, "caption": 40},
    "rec_rule": {"quote": 90, "translation": 70, "kicker": 40},
    "rec_replay": {"label": 30},
    "rec_result": {"headline": 40, "note": 90, "row": 26},
    "rec_protokoll": {"statement": 56, "claim": 40},
}
HOOK_SCENE_TYPES = ["rec_auftrag"]

MONO_CH = 0.6           # JetBrains Mono advance width in em
WRAP_W = 680            # replay text column (864 - 2*24 padding - 136 gutter)
WIN_BG = "#1C1F29"      # window fill; light enough that a frame with one window is not counted as black (blackdetect)
FS = 30                 # code size floor
ROW = 42
FULL_H = 800            # full-width (864 px) elements end here (y 1100); below only narrow ones (<= 832 px, left of x 940)
RES_STEP = 150          # row pitch in rec_result

# fixed frame wording per recording language (meta.json "language", set from the spec; default de)
UI = {
    "de": {"run": "Lauf {}: {}", "run_no": "Lauf {}", "term": "Terminal · Testordner", "folder": "Testordner {}",
           "sample": "Beispieldaten, keine echten Zugangsdaten", "realtime": "Echtzeit", "lapse": "Zeitraffer {:g}×",
           "more": "… ({} weitere Zeilen)", "rep": "Wiederholt: {} von {} gleich", "agree": "{} von {} gleich",
           "head": "{} Läufe, aufgezeichnet", "hit": "Wert ausgegeben", "miss": "Wert nicht ausgegeben",
           "hit_short": "ausgegeben", "miss_short": "gesperrt", "q": ("„", "“"), "proto": "Protokoll",
           "kv": ("Aufgezeichnet", "Claude Code", "Modell", "Läufe", "Wiederholung", "Testordner"),
           "at": "{}, {} Uhr", "runs": "{}, je {}-mal", "all_same": "alle gleich", "not_same": "NICHT alle gleich",
           "only_sample": "nur Beispieldaten", "stamp": "Echter Ablauf, aufgezeichnet am {}"},
    "en": {"run": "Run {}: {}", "run_no": "Run {}", "term": "Terminal · test folder", "folder": "Test folder {}",
           "sample": "Sample data, no real credentials", "realtime": "Real time", "lapse": "Time-lapse {:g}×",
           "more": "… ({} more lines)", "rep": "Repeated: {} of {} identical", "agree": "{} of {} identical",
           "head": "{} runs, recorded", "hit": "Value shown", "miss": "Value not shown",
           "hit_short": "shown", "miss_short": "blocked", "q": ("“", "”"), "proto": "Run log",
           "kv": ("Recorded", "Claude Code", "Model", "Runs", "Repetition", "Test folder"),
           "at": "{}, {}", "runs": "{}, {} times each", "all_same": "all identical", "not_same": "NOT all identical",
           "only_sample": "sample data only", "stamp": "Real run, recorded on {}"},
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _lang(r: dict) -> str:
    return r["meta"].get("language", "de")


def _ui(r: dict) -> dict:
    return UI.get(_lang(r), UI["de"])


def _hit(x: dict):
    return x.get("probe_hit", x.get("probe_in_answer"))


def _e(s) -> str:
    return html.escape(str(s))


def _lim(kind, key, val, where, probs):
    n = LIMITS.get(kind, {}).get(key)
    if n and len(str(val)) > n:
        probs.append(f"{kind}.{where}: {len(str(val))} chars > {n}")


def _word_time(c: SceneCtx, word: str):
    w0 = word.lower().strip(".,:;!?")
    for w in getattr(c, "words", None) or []:
        if w.text.lower().strip(".,:;!?\"'„“").startswith(w0):
            return float(w.start)
    return None


def _at(c: SceneCtx, d: dict, key: str, frac: float) -> float:
    wkey = key[:-3] + "_word" if key.endswith("_at") else key + "_word"
    if d.get(wkey):
        t = _word_time(c, str(d[wkey]))
        if t is not None:
            return c.t(t - c.start)
    return c.t(float(d[key]) if key in d else c.duration * frac)


_cache: dict[str, dict] = {}


def rec(rid: str) -> dict:
    """The recording: transcript, outcome, meta, files per run."""
    if rid not in _cache:
        base = REC_DIR / rid
        r = {k: json.loads((base / f"{k}.json").read_text(encoding="utf-8")) for k in ("transcript", "outcome", "meta")}
        r["files"] = {}
        for run_dir in (base / "files").glob("*"):
            r["files"][run_dir.name] = {k: json.loads((run_dir / f"{k}.json").read_text(encoding="utf-8")) for k in ("before", "after")}
        _cache[rid] = r
    return _cache[rid]


def _run_no(r: dict, run: str) -> int:
    return list(r["transcript"]["runs"]).index(run) + 1


def _wrap_rows(text: str, width_px: int = WRAP_W, fs: int = FS) -> list[str]:
    """Hard wrap for the mono column (same width the browser uses: white-space:pre, one row per entry)."""
    per = max(8, int(width_px // (fs * MONO_CH)))
    rows = []
    for para in str(text).replace("\t", "  ").split("\n"):
        while len(para) > per:
            cut = para.rfind(" ", 0, per + 1)
            cut = cut if cut > per * 0.5 else per
            rows.append(para[:cut].rstrip())
            para = para[cut:].lstrip()
        rows.append(para)
    return rows


def _scene(c: SceneCtx, inner: str, cls: str) -> str:
    return f'<div class="el-scene {cls}" style="top:{c.zone_top}px;height:{c.zone_h}px">{inner}</div>'


def _enter(c: SceneCtx) -> list[str]:
    # no camera move and no self-fade: the record is the picture (format rule "kein Zierrat")
    return [f'tl.fromTo("#{c.sid} .el-scene",{{opacity:0.4}},{{opacity:1,duration:{c.enter:.2f},ease:"power1.out"}},{c.start:.3f});']


def _type_tl(sel: str, t: float, n_chars: int, cps: float = 38.0) -> str:
    dur = max(0.4, min(2.2, n_chars / cps))
    return (f'tl.fromTo("{sel}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{dur:.2f},'
            f'ease:"steps({max(6, min(60, n_chars))})"}},{t:.3f});')


def _cmd_rows(prompt: str, allowed: list[str]) -> list[tuple[str, str]]:
    """The command line as display rows (kind, text): the prompt wraps, extra flags go on a dim row."""
    rows = [("cmd", r) for r in _wrap_rows(f'$ claude -p "{prompt}"', 864 - 48, FS)]
    if allowed:
        rows += [("flag", r) for r in _wrap_rows("  --allowedTools " + " ".join(f'"{a}"' for a in allowed), 864 - 48, FS)]
    return rows


# --- rec_auftrag ------------------------------------------------------------------------------------------

def rec_auftrag(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    runs = r["transcript"]["runs"]
    run = runs[d.get("run") or next(iter(runs))]
    q = d.get("question", "")
    _lim("rec_auftrag", "question", q, "question", probs)
    rows = _cmd_rows(run["prompt"], [])
    show = d.get("chips") or [{"run": k, "text": _ui(r)["run"].format(i + 1, v["title"])} for i, (k, v) in enumerate(runs.items())]
    for ch in show:
        _lim("rec_auftrag", "chip", ch["text"], "chip", probs)
    q_lines = max(1, math.ceil(len(q) * 76 * 0.55 / 864))
    win_top, row_h = 40 + q_lines * 82, 48
    win_h = 70 + 34 + len(rows) * row_h + 30
    cmd_html = "".join(f'<div class="el-row {k}" id="{s}-c{i}" style="top:{34 + i * row_h}px">{_e(t)}</div>' for i, (k, t) in enumerate(rows))
    chip_top = win_top + win_h + 40
    chips = "".join(f'<div class="el-chip" id="{s}-k{i}" style="top:{chip_top + i * 80}px"><span class="el-q">?</span>{_e(ch["text"])}</div>'
                    for i, ch in enumerate(show))
    inner = f"""
<div class="el-question" id="{s}-q">{_e(q)}</div>
<div class="el-win" style="top:{win_top}px;height:{win_h}px"><div class="el-bar"><i></i><i></i><i></i><span>{_e(_ui(r)["term"])}</span></div>
<div class="el-body">{cmd_html}</div></div>
{chips}"""
    out = SceneOut(html=_scene(c, inner, "el-auftrag"), problems=probs)
    out.tl += _enter(c)
    tq = _at(c, d, "question_at", 0.02)
    out.tl.append(f'tl.fromTo("#{s}-q",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{tq:.3f});')
    tt = _at(c, d, "type_at", 0.18)
    for i, (_, t) in enumerate(rows):
        out.tl.append(_type_tl(f"#{s}-c{i}", tt + i * 0.55, len(t)))
    events = [c.start, tq, tt]
    tk = _at(c, d, "chips_at", 0.55)
    for i in range(len(show)):
        ti = c.t(tk - c.start + i * 0.35)
        out.tl.append(f'tl.fromTo("#{s}-k{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{ti:.3f});')
        events.append(ti)
    out.events = events
    return out


# --- rec_setup --------------------------------------------------------------------------------------------

def _file_rows(text: str, fs: int = FS) -> list[tuple[str, str]]:
    """(line number or '', row text): a wrapped line keeps its number on the first row only."""
    out = []
    for n, line in enumerate(text.rstrip("\n").split("\n"), 1):
        for k, row in enumerate(_wrap_rows(line, 864 - 48 - 60, fs)):
            out.append((str(n) if k == 0 else "", row))
    return out


def _find_row(rows, needle, default=-1) -> int:
    return next((i for i, (_, t) in enumerate(rows) if needle and needle in t), default)


def _window(rows, hl: int, n, more: str):
    """At most n rows around the highlight; cut parts become one visible '… (k weitere Zeilen)' row each."""
    if not n or len(rows) <= int(n):
        return rows, hl
    n = int(n)
    a = max(0, min(hl - n // 2, len(rows) - n)) if hl >= 0 else 0
    while a > 0 and not rows[a][0]:                    # start on a file line, not inside a wrapped one
        a -= 1
    e = a + n
    while e < len(rows) and not rows[e][0]:            # end after a whole file line
        e += 1
    lines = lambda part: sum(1 for num, _ in part if num)   # count file lines, not wrapped display rows
    out = ([("", more.format(lines(rows[:a])))] if a else []) + rows[a:e]
    if e < len(rows):
        out.append(("", more.format(lines(rows[e:]))))
    return out, (hl - a + (1 if a else 0)) if hl >= 0 else -1


def rec_setup(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    run = d.get("run") or next(iter(r["transcript"]["runs"]))
    files = r["files"][run][d.get("state", "before")]      # state "after": the sandbox as the run left it
    label = d.get("label", _ui(r)["sample"])
    _lim("rec_setup", "label", label, "label", probs)
    names = sorted(files, key=lambda n: (n.count("/"), n))
    tree_h = 70 + 24 + len(names) * 52 + 20
    tree = "".join(f'<div class="el-file{" on" if n == d.get("show") else ""}" id="{s}-f{i}" style="top:{24 + i * 52}px">'
                   f'<span class="el-ficon"></span>{_e(n)}</div>' for i, n in enumerate(names))
    show = d.get("show") or names[0]
    rows = _file_rows(files.get(show, ""))
    hl = _find_row(rows, d.get("highlight_text"), int(d.get("highlight", -1)))
    rows, hl = _window(rows, hl, d.get("max_rows"), _ui(r)["more"])
    view_top = tree_h + 40
    view_h = 70 + 24 + len(rows) * 46 + 24
    lines = "".join(f'<div class="el-fline" id="{s}-l{i}" style="top:{24 + i * 46}px"><span class="el-ln">{n}</span>{_e(t)}</div>'
                    for i, (n, t) in enumerate(rows))
    mark = (f'<div class="el-hl" id="{s}-hl" style="top:{70 + 24 + hl * 46 - 2}px"></div>' if 0 <= hl < len(rows) else "")
    inner = f"""
<div class="el-win" style="top:0;height:{tree_h}px"><div class="el-bar"><i></i><i></i><i></i><span>{_e(_ui(r)["folder"].format(d.get("folder_name", d["rec"])))}</span></div>
<div class="el-body">{tree}</div></div>
<div class="el-win" id="{s}-view" style="top:{view_top}px;height:{view_h}px"><div class="el-bar"><i></i><i></i><i></i><span>{_e(show)}</span></div>
<div class="el-body">{lines}</div>{mark}</div>
<div class="el-tag amber" id="{s}-tag" style="top:{view_top + view_h + 30}px">{_e(label)}</div>"""
    out = SceneOut(html=_scene(c, inner, "el-setup"), problems=probs)
    out.tl += _enter(c)
    events = [c.start]
    for i in range(len(names)):
        ti = c.t(0.15 + i * 0.18)
        out.tl.append(f'tl.fromTo("#{s}-f{i}",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.25}},{ti:.3f});')
    tv = _at(c, d, "view_at", 0.25)
    out.tl.append(f'tl.fromTo("#{s}-view",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{tv:.3f});')
    events.append(tv)
    if mark:
        th = _at(c, d, "highlight_at", 0.5)
        out.tl.append(f'tl.fromTo("#{s}-hl",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power2.out"}},{th:.3f});')
        events.append(th)
    tg = _at(c, d, "tag_at", 0.7)
    out.tl.append(f'tl.fromTo("#{s}-tag",{{opacity:0,scale:1.3}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out"}},{tg:.3f});')
    events.append(tg)
    out.events = events
    return out


# --- rec_rule ---------------------------------------------------------------------------------------------

def rec_rule(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    run = d["run"]
    fname = d.get("file", ".claude/settings.json")
    text = r["files"][run]["before"].get(fname, "")
    rows = _file_rows(text)
    hl = _find_row(rows, d.get("highlight_text", "deny"))
    rows, hl = _window(rows, hl, d.get("max_rows"), _ui(r)["more"])
    for k in ("quote", "translation", "kicker"):
        _lim("rec_rule", k, d.get(k, ""), k, probs)
    win_h = 70 + 24 + len(rows) * 46 + 24
    lines = "".join(f'<div class="el-fline" style="top:{24 + i * 46}px"><span class="el-ln">{n}</span>{_e(t)}</div>'
                    for i, (n, t) in enumerate(rows))
    mark = f'<div class="el-hl" id="{s}-hl" style="top:{70 + 24 + hl * 46 - 2}px"></div>' if hl >= 0 else ""
    doc_top = win_h + 36
    inner = f"""
<div class="el-win" id="{s}-w" style="top:0;height:{win_h}px"><div class="el-bar"><i></i><i></i><i></i><span>{_e(_ui(r)["run"].format(_run_no(r, run), fname))}</span></div>
<div class="el-body">{lines}</div>{mark}</div>
<div class="el-doc" id="{s}-d" style="top:{doc_top}px">
  <div class="el-kicker">{_e(d.get('kicker', ''))}</div>
  <div class="el-quote">{_ui(r)["q"][0]}{_e(d.get('quote', ''))}{_ui(r)["q"][1]}</div>
  <div class="el-trans" id="{s}-tr">{_e(d.get('translation', ''))}</div>
</div>"""
    out = SceneOut(html=_scene(c, inner, "el-rule"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-w",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    if mark:
        th = _at(c, d, "highlight_at", 0.3)
        out.tl.append(f'tl.fromTo("#{s}-hl",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power2.out"}},{th:.3f});')
        events.append(th)
    td = _at(c, d, "doc_at", 0.5)
    out.tl.append(f'tl.fromTo("#{s}-d",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{td:.3f});')
    # the translation follows the quote at once (Prüfrunde 03.11.2026: the quote must not stand alone in English)
    tr = _at(c, d, "translation_at", 0.72) if d.get("translation_at") else c.t(td - c.start + 0.5)
    out.tl.append(f'tl.fromTo("#{s}-tr",{{opacity:0}},{{opacity:1,duration:0.3}},{tr:.3f});')
    out.events = events + [td, tr]
    return out


# --- rec_replay -------------------------------------------------------------------------------------------

SPEEDS = [1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20]
PREFIX = {"init": "○ ", "think": "✻ ", "tool": "● ", "result": "  ⎿ ", "denied": "  ⎿ ", "text": "", "end": ""}
TEXT_ROWS = 7            # an answer longer than this is cut with a visible "… (n weitere Zeilen)" row


def replay_speed(span: float, avail: float) -> float:
    need = span / max(0.5, avail)
    return next((x for x in SPEEDS if x >= need - 1e-6), SPEEDS[-1])


def rec_replay(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    run_id = d["run"]
    run = r["transcript"]["runs"][run_id]
    oc = r["outcome"]["runs"][run_id]
    first = oc["repetitions"][0]
    ui = _ui(r)
    label = d.get("label") or ui["run"].format(_run_no(r, run_id), run["title"])
    _lim("rec_replay", "label", label, "label", probs)

    lines = [ln for ln in run["lines"] if ln["kind"] in PREFIX]
    t_end = max((ln["t"] for ln in lines), default=1.0)
    lead = float(d.get("lead", 1.4))                 # command typed and entered
    hold = float(d.get("hold", 1.6))                 # verdict readable at the end
    avail = c.duration - lead - hold
    speed = float(d["speed"]) if d.get("speed") else replay_speed(t_end, avail)
    badge = ui["realtime"] if speed == 1 else ui["lapse"].format(speed)

    cmd = _cmd_rows(run["prompt"], run.get("allowed_tools") or [])
    win_h = min(c.zone_h, FULL_H)
    body_h = win_h - 70 - 110                          # bar 70, footer 110 (verdict strip)
    rows_html, y, scroll, t_rows, ev_rows = [], 20, [], [], []
    boxes = []                                         # (element id, top) of every display row, for hiding scrolled-out rows
    for i, (k, t) in enumerate(cmd):
        rows_html.append(f'<div class="el-row {k}" id="{s}-c{i}" style="top:{y}px">{_e(t)}</div>')
        boxes.append((f"{s}-c{i}", y))
        y += ROW
    y += 14
    for j, ln in enumerate(lines):
        wrapped = _wrap_rows(("┆ " if ln.get("sub") else "") + PREFIX[ln["kind"]] + ln["text"])   # ┆ = inside a subagent
        cap = int(d.get("text_rows", TEXT_ROWS))
        if ln["kind"] == "text" and len(wrapped) > cap + 1:
            wrapped = wrapped[:cap] + [ui["more"].format(len(wrapped) - cap)]
        h = len(wrapped) * ROW
        for k, row in enumerate(wrapped):              # one element per display row, so a row that scrolls out can be hidden alone
            ts = f'{ln["t"]:.1f} s' if k == 0 else ""
            rows_html.append(f'<div class="el-ev {ln["kind"]} {s}-e{j}" id="{s}-e{j}r{k}" style="top:{y + k * ROW}px;height:{ROW}px">'
                             f'<span class="el-ts">{ts}</span><span class="el-tx">{_e(row)}</span></div>')
            boxes.append((f"{s}-e{j}r{k}", y + k * ROW))
        at = c.t(lead + ln["t"] / speed)
        t_rows.append(at)
        if ln["kind"] in ("tool", "denied", "text"):
            ev_rows.append(at)
        if y + h > body_h - 10:
            scroll.append((at, -(y + h - (body_h - 10))))
        y += h + 8
    hit = bool(_hit(first))
    verdict_bad = hit != bool(d.get("probe_good"))        # probe_good: the probe showing up is the wanted result
    stamp = d.get("stamp_true" if hit else "stamp_false") or (ui["hit"] if hit else ui["miss"])
    reps = oc["repetitions"]
    agree = sum(1 for x in reps if _hit(x) == _hit(first))
    inner = f"""
<div class="el-win replay" style="top:0;height:{win_h}px">
  <div class="el-bar"><i></i><i></i><i></i><span>{_e(label)}</span><b class="el-speed">{_e(badge)}</b></div>
  <div class="el-body" style="height:{body_h}px;overflow:hidden"><div class="el-scroll" id="{s}-sc">{''.join(rows_html)}</div></div>
  <div class="el-foot"><span class="el-verdict {'bad' if verdict_bad else 'ok'}" id="{s}-v">{_e(stamp)}</span>
  <span class="el-rep" id="{s}-r">{_e(ui["rep"].format(agree, len(reps)))}</span></div>
</div>"""
    out = SceneOut(html=_scene(c, inner, "el-replay"), problems=probs)
    out.tl += _enter(c)
    events = [c.start]
    for i, (_, t) in enumerate(cmd):
        out.tl.append(_type_tl(f"#{s}-c{i}", c.t(0.1 + i * 0.4), len(t), 60))
    for j, at in enumerate(t_rows):
        out.tl.append(f'tl.fromTo(".{s}-e{j}",{{opacity:0}},{{opacity:1,duration:0.08}},{at:.3f});')
    events += ev_rows
    hidden = set()
    for at, dy in scroll:
        out.tl.append(f'tl.to("#{s}-sc",{{y:{dy},duration:0.25,ease:"power2.out"}},{at:.3f});')
        for bid, top in boxes:                         # rows above the window edge are clipped anyway; hidden so checks see them gone
            if bid not in hidden and top < -dy:
                hidden.add(bid)
                out.tl.append(f'tl.set("#{bid}",{{visibility:"hidden"}},{at:.3f});')
    tv = c.t((t_rows[-1] - c.start if t_rows else lead) + 0.35)
    out.tl.append(f'tl.fromTo("#{s}-v",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.22,ease:"power4.in"}},{tv:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-r",{{opacity:0}},{{opacity:1,duration:0.3}},{c.t(tv - c.start + 0.4):.3f});')
    events.append(tv)
    out.named_events = {"line": t_rows[0] if t_rows else c.start, "verdict": tv}   # sound cues (layout.sound_cues event)
    out.events = sorted(set(round(e, 2) for e in events))
    if speed > 1 and t_end / speed > avail + 0.05:
        probs.append(f"rec_replay: run {run_id} needs {t_end / speed:.1f} s at {speed:g}x, beat has {avail:.1f} s")
    return out


# --- rec_result -------------------------------------------------------------------------------------------

def rec_result(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    runs = r["transcript"]["runs"]
    ui = _ui(r)
    head = d.get("headline", ui["head"].format(len(runs)))
    _lim("rec_result", "headline", head, "headline", probs)
    _lim("rec_result", "note", d.get("note", ""), "note", probs)
    rows_html = []
    sel = d.get("runs") or list(runs)
    # few runs get taller rows, so the rows and the note at the bottom fill the zone (Prüfrunde R5)
    step = max(RES_STEP, min(220, (c.zone_h - 210 - 120) // max(1, len(sel))))
    for i, rid in enumerate(sel):
        oc = r["outcome"]["runs"][rid]
        reps = oc["repetitions"]
        hit = bool(_hit(reps[0]))
        bad = hit != bool(d.get("probe_good"))
        word = d.get("stamp_true" if hit else "stamp_false") or (ui["hit_short"] if hit else ui["miss_short"])
        cls = "bad" if bad else "ok"
        if d.get("metric"):                      # a measured number instead of the verdict, e.g. input_tokens
            v = reps[0].get(d["metric"], 0)
            word = f"{v:,}".replace(",", "." if _lang(r) == "de" else ",") + " " + d.get("metric_unit", "Tokens")
            cls = "neu"
        title = (d.get("titles") or {}).get(rid, runs[rid]["title"])
        _lim("rec_result", "row", title, f"row {rid}", probs)
        agree = sum(1 for x in reps if _hit(x) == _hit(reps[0]))
        rows_html.append(f'<div class="el-res" id="{s}-r{i}" style="top:{96 + i * step}px;height:{step - 18}px"><div class="el-rl">{_e(ui["run_no"].format(_run_no(r, rid)))}'
                         f'<span>{_e(title)}</span></div><div class="el-rr"><b class="{cls}" id="{s}-b{i}">{_e(word)}</b>'
                         f'<em>{_e(ui["agree"].format(agree, len(reps)))}</em></div></div>')
    # the note sits at the bottom of the zone (narrow, left of x 940, so it may use the band below y 1100)
    note_top = max(96 + len(sel) * step + 24, c.zone_h - 210)
    inner = f"""<div class="el-head">{_e(head)}</div>{''.join(rows_html)}
<div class="el-note" id="{s}-n" style="top:{note_top}px">{_e(d.get('note', ''))}<span>{_e(d.get('note_source', ''))}</span></div>"""
    out = SceneOut(html=_scene(c, inner, "el-result"), problems=probs)
    out.tl += _enter(c)
    events = [c.start]
    t0 = _at(c, d, "rows_at", 0.08)
    for i in range(len(sel)):
        ti = c.t(t0 - c.start + i * float(d.get("row_gap", 0.9)))
        out.tl.append(f'tl.fromTo("#{s}-r{i}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{ti:.3f});')
        tb = c.t(ti - c.start + 0.45)                  # the verdict lands after its row: a second visible event per run
        out.tl.append(f'tl.fromTo("#{s}-b{i}",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.22,ease:"power4.in"}},{tb:.3f});')
        events += [ti, tb]
    tn = _at(c, d, "note_at", 0.65)
    out.tl.append(f'tl.fromTo("#{s}-n",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{tn:.3f});')
    out.events = events + [tn]
    return out


# --- rec_protokoll ----------------------------------------------------------------------------------------

def _date(iso: str, lang: str = "de") -> str:
    if lang == "en":
        return f"{MONTHS[int(iso[5:7]) - 1]} {int(iso[8:10])}, {iso[0:4]}"
    return f"{iso[8:10]}.{iso[5:7]}.{iso[0:4]}"


def rec_protokoll(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    meta, outc = r["meta"], r["outcome"]
    model = next((v.get("model") for v in meta["runs"].values() if v.get("model")), meta.get("model_alias"))
    nrep = max(len(v["repetitions"]) for v in outc["runs"].values())
    vals = [ui["at"].format(_date(meta["recorded_at"], _lang(r)), meta["recorded_at"][11:16]),
            meta["claude_code"], model, ui["runs"].format(len(outc["runs"]), nrep),
            ui["all_same"] if outc.get("all_reproducible") else ui["not_same"], ui["only_sample"]]
    kv = list(zip(ui["kv"], vals))
    for k in ("statement", "claim"):
        _lim("rec_protokoll", k, d.get(k, ""), k, probs)
    rows = "".join(f'<div class="el-kv" id="{s}-k{i}"><span>{_e(a)}</span><b>{_e(b)}</b></div>' for i, (a, b) in enumerate(kv))
    inner = f"""<div class="el-proto" id="{s}-pc"><div class="el-ptitle">{_e(ui["proto"])}</div>{rows}</div>
<div class="el-statement" id="{s}-st">{_e(d.get('statement', ''))}</div>
<div class="el-claim" id="{s}-cl">{_e(d.get('claim', ''))}</div>"""
    out = SceneOut(html=_scene(c, inner, "el-protokoll"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-pc",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    for i in range(len(kv)):
        ti = c.t(0.25 + i * 0.22)
        out.tl.append(f'tl.fromTo("#{s}-k{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{ti:.3f});')
    ts = _at(c, d, "statement_at", 0.45)
    tc = _at(c, d, "claim_at", 0.7)
    out.tl.append(f'tl.fromTo("#{s}-st",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{ts:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-cl",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.3}},{tc:.3f});')
    out.events = events + [ts, tc]
    return out


TEMPLATES = {"rec_auftrag": rec_auftrag, "rec_setup": rec_setup, "rec_rule": rec_rule, "rec_replay": rec_replay,
             "rec_result": rec_result, "rec_protokoll": rec_protokoll}


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int = 300, zone_h: int = 930, flat: bool = False) -> str:
    text, muted = pal["text"], pal["muted"]
    acc = pal["accent"]
    term = pal.get("terminal", "#101218")
    hair = pal.get("hairline", "rgba(248,250,252,0.10)")
    green, red, amber, on = (pal.get("signal_green", "#4ADE80"), pal.get("signal_red", "#F87171"),
                             pal.get("signal_amber", "#FBBF24"), pal.get("on_signal", "#0B0C10"))
    return f"""
/* --- Promptwerk Echtlauf (rec_*) --- */
.el-scene{{position:absolute;left:108px;width:864px;text-align:left;}}
.el-win{{position:absolute;left:0;width:864px;background:{WIN_BG};border:2px solid {hair};border-radius:16px;overflow:hidden;}}
.el-bar{{height:70px;display:flex;align-items:center;gap:10px;padding:0 22px;border-bottom:2px solid {hair};font-family:'FN {mono}';font-size:30px;color:{muted};white-space:nowrap;}}
.el-bar i{{display:inline-block;width:14px;height:14px;border-radius:50%;background:{muted};opacity:0.4;}}
.el-bar span{{margin-left:10px;color:{text};}}
.el-speed{{margin-left:auto;font-weight:500;font-size:30px;color:{on};background:{amber};padding:4px 14px;border-radius:8px;}}
.el-body{{position:relative;}}
.el-row{{position:absolute;left:24px;right:24px;height:44px;font-family:'FN {mono}';font-size:{FS}px;line-height:44px;white-space:pre;color:{text};}}
.el-row.flag{{color:{muted};}}
.el-scroll{{position:absolute;left:0;right:0;top:0;}}
.el-ev{{position:absolute;left:24px;right:24px;display:flex;font-family:'FN {mono}';font-size:{FS}px;line-height:{ROW}px;}}
.el-ts{{flex:0 0 136px;color:{muted};font-size:30px;}}
.el-tx{{white-space:pre;tab-size:2;color:{text};}}
.el-ev.tool .el-tx{{color:{acc};}}
.el-ev.result .el-tx{{color:{muted};}}
.el-ev.denied .el-tx{{color:{red};}}
.el-ev.end .el-tx,.el-ev.init .el-tx,.el-ev.think .el-tx{{color:{muted};}}
.el-foot{{position:absolute;left:0;right:0;bottom:0;height:110px;border-top:2px solid {hair};display:flex;align-items:center;justify-content:space-between;padding:0 24px;}}
.el-verdict{{font-family:'FN {display}';font-weight:800;font-size:40px;padding:8px 20px;border-radius:10px;color:{on};white-space:nowrap;}}
.el-verdict.bad{{background:{red};}} .el-verdict.ok{{background:{green};}}
.el-rep{{font-size:32px;color:{muted};white-space:nowrap;}}
.el-question{{position:absolute;left:0;top:0;width:864px;font-family:'FN {display}';font-weight:{display_w};font-size:76px;line-height:1.06;letter-spacing:-0.02em;color:{text};}}
.el-chip{{position:absolute;left:0;height:68px;display:flex;align-items:center;gap:18px;padding:0 24px 0 10px;border:2px solid {hair};border-radius:12px;font-size:34px;color:{text};background:color-mix(in srgb,{text} 4%,transparent);}}
.el-q{{display:inline-flex;width:48px;height:48px;align-items:center;justify-content:center;border-radius:8px;background:{amber};color:{on};font-weight:800;font-size:32px;}}
.el-file{{position:absolute;left:24px;height:48px;display:flex;align-items:center;gap:16px;font-family:'FN {mono}';font-size:{FS}px;color:{muted};}}
.el-file.on{{color:{text};}}
.el-ficon{{width:22px;height:28px;border:3px solid currentColor;border-radius:4px;}}
.el-fline{{position:absolute;left:24px;right:24px;height:46px;display:flex;align-items:center;font-family:'FN {mono}';font-size:{FS}px;white-space:pre;color:{text};}}
.el-ln{{flex:0 0 60px;color:{muted};opacity:0.6;}}
.el-hl{{position:absolute;left:12px;right:12px;height:50px;border-radius:8px;background:color-mix(in srgb,{acc} 22%,transparent);border-left:6px solid {acc};transform-origin:0 50%;}}
.el-tag{{position:absolute;left:0;padding:10px 20px;border-radius:10px;font-size:32px;font-weight:700;white-space:nowrap;}}
.el-tag.amber{{background:{amber};color:{on};}}
.el-path{{position:absolute;left:0;top:0;font-family:'FN {mono}';font-size:32px;color:{muted};}}
.el-doc{{position:absolute;left:0;width:832px;padding:28px 30px;border-left:6px solid {acc};background:color-mix(in srgb,{text} 4%,transparent);border-radius:0 12px 12px 0;}}
.el-kicker{{font-size:30px;color:{muted};margin-bottom:14px;}}
.el-quote{{font-size:38px;line-height:1.3;color:{text};}}
.el-trans{{margin-top:18px;font-size:36px;line-height:1.3;color:{acc};font-weight:600;}}
.el-head{{position:absolute;left:0;top:0;font-family:'FN {display}';font-weight:{display_w};font-size:60px;color:{text};}}
.el-res{{position:absolute;left:0;width:864px;height:132px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border:2px solid {hair};border-radius:14px;background:{WIN_BG};}}
.el-rl{{font-family:'FN {mono}';font-size:30px;color:{muted};display:flex;flex-direction:column;gap:6px;}}
.el-rl span{{font-family:'FN {body}';font-size:36px;color:{text};}}
.el-rr{{display:flex;flex-direction:column;align-items:flex-end;gap:8px;}}
.el-rr b{{font-family:'FN {display}';font-size:36px;padding:4px 16px;border-radius:8px;color:{on};white-space:nowrap;}}
.el-rr b.bad{{background:{red};}} .el-rr b.ok{{background:{green};}} .el-rr b.neu{{background:{amber};}}
.el-rr em{{font-style:normal;font-size:32px;color:{muted};}}
.el-note{{position:absolute;left:0;width:832px;font-size:36px;line-height:1.3;color:{text};padding:22px 26px;border-left:6px solid {amber};background:color-mix(in srgb,{amber} 10%,transparent);border-radius:0 12px 12px 0;}}
.el-note span{{display:block;margin-top:10px;font-size:30px;color:{muted};}}
.el-proto{{position:absolute;left:0;top:0;width:864px;padding:26px 30px 16px;border:2px solid {hair};border-radius:16px;background:{WIN_BG};}}
.el-ptitle{{font-family:'FN {mono}';font-size:30px;color:{acc};margin-bottom:10px;letter-spacing:0.08em;text-transform:uppercase;}}
.el-kv{{display:flex;justify-content:space-between;gap:20px;padding:12px 0;border-top:2px solid {hair};font-size:32px;}}
.el-kv span{{color:{muted};white-space:nowrap;}} .el-kv b{{color:{text};font-family:'FN {mono}';font-weight:500;font-size:30px;text-align:right;}}
.el-statement{{position:absolute;left:0;top:540px;width:864px;font-family:'FN {display}';font-weight:{display_w};font-size:56px;line-height:1.1;color:{text};}}
.el-claim{{position:absolute;left:0;top:710px;padding:12px 24px;border-radius:12px;background:{acc};color:{on};font-size:34px;font-weight:700;white-space:nowrap;}}
"""


def LAYER(plan, brand, project_dir, captions) -> dict:
    """Format-wide layer: a plain dark ground (no decoration, the record is the picture) and the recording stamp
    "Echter Ablauf, aufgezeichnet am <Datum>" / "Claude Code <Version> · <Modell>" for the whole video."""
    lay = getattr(plan, "layout", None) or {}
    r = rec((lay.get("echtlauf") or {})["recording"])
    meta = r["meta"]
    model = next((v.get("model") for v in meta["runs"].values() if v.get("model")), meta.get("model_alias"))
    pal = dict(getattr(brand, "palette", {}) or {})
    red, muted, text = pal.get("signal_red", "#F87171"), pal.get("muted", "#93959A"), pal.get("text", "#F8FAFC")
    lang = getattr(plan, "language", "de")
    line1 = UI.get(lang, UI["de"])["stamp"].format(_date(meta["recorded_at"], lang))
    line2 = f"Claude Code {meta['claude_code']} · {model}"
    html_ = f"""<div id="elx" style="position:absolute;inset:0;z-index:0;pointer-events:none;background:#0B0C10">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 90% 70% at 50% 45%,transparent 60%,rgba(0,0,0,0.5) 100%)"></div></div>
<div id="elx-stamp" style="position:absolute;left:108px;top:192px;width:832px;z-index:21;font-size:30px;line-height:40px;text-align:left">
<div style="color:{text};white-space:nowrap"><span id="elx-dot" style="display:inline-block;width:18px;height:18px;border-radius:50%;background:{red};margin-right:14px;vertical-align:1px"></span>{_e(line1)}</div>
<div style="color:{muted};white-space:nowrap">{_e(line2)}</div></div>"""
    script = """<script>
(function(){var t=window.__timelines&&window.__timelines.main;if(!t)return;var T=Number(document.getElementById("root").dataset.duration)||60;
t.fromTo("#elx-dot",{opacity:1},{opacity:0.25,duration:0.8,ease:"sine.inOut",yoyo:true,repeat:Math.max(1,Math.floor(T/0.8)-1)},0);
t.seek(0);})();
</script>"""
    return {"under_scenes_html": html_, "body_end_html": script, "events": []}


def MANIFEST_EXTRA(plan) -> dict:
    lay = getattr(plan, "layout", None) or {}
    rid = (lay.get("echtlauf") or {}).get("recording")
    if not rid:
        return {}
    r = rec(rid)
    return {"echtlauf": {"recording": rid, "recorded_at": r["meta"]["recorded_at"], "claude_code": r["meta"]["claude_code"],
                         "all_reproducible": r["outcome"].get("all_reproducible"),
                         "runs": {k: v["repetitions"] for k, v in r["outcome"]["runs"].items()}}}


# =========================================================================================================
# Neustart 03.11.2026 (Testvideo-Konzept 2026-11): variation and the real world around the run.
#
#   rec_photo   full-bleed Higgsfield still or Kling clip (the workplace, never a screen), slow camera move,
#               stamp "KI-Bild"; optional question, command card, close statement
#   rec_table   a CSV from the sandbox as a scrolling list, duplicate rows marked as they pass, then the tricky
#               pairs as close-up cards with the differing characters marked (computed, not typed)
#   rec_diff    before/after: one strip per row, removed rows turn red and collapse, the row counter rolls down,
#               verdict against the expected count
#   rec_answer  Claude's final answer as a card, verbatim quotes picked from it, a slow push-in, key phrases marked
#   rec_split   two runs side by side: the extra instruction of the second run marked, both results, same rows?
#
# Photos and clips are named relative to brands/claude_workflows/assets/higgsfield/ and copied to
# <project>/assets/pw/ by LAYER. A clip (Kling, started from the still) plays under the scenes from its shot's `at`;
# the scene's dim gradient stays above it. The "Echter Ablauf" stamp is hidden while a KI-Bild is on screen.
# =========================================================================================================

import difflib
import re
import shutil

PHOTO_ROOT = HERE.parent / "assets" / "higgsfield"
CLIP_SECONDS = 8.0
UI["de"].update({"ai_image": "KI-Bild", "dup": "doppelt: {}", "rows": "{} Zeilen", "rows_in": "Zeilen in {}",
                 "expect": "Soll: {}", "ok": "stimmt", "off": "weicht ab", "answer": "Antwort von Claude · Lauf {}",
                 "same_rows": "Entfernte Zeilen: in beiden Läufen dieselben {}", "diff_rows": "Entfernte Zeilen: NICHT dieselben",
                 "plus": "gleicher Auftrag, dazu:", "list": "{} · {} Zeilen"})
UI["en"].update({"ai_image": "AI image", "dup": "duplicates: {}", "rows": "{} rows", "rows_in": "rows in {}",
                 "expect": "expected: {}", "ok": "correct", "off": "off", "answer": "Claude's answer · run {}",
                 "same_rows": "Removed rows: the same {} in both runs", "diff_rows": "Removed rows: NOT the same",
                 "plus": "same prompt, plus:", "list": "{} · {} rows"})
LIMITS.update({"rec_photo": {"question": 48, "label": 34, "statement": 56, "claim": 40},
               "rec_table": {"why": 24}, "rec_diff": {"note": 60}, "rec_answer": {}, "rec_split": {}})
HOOK_SCENE_TYPES.append("rec_photo")


def _href(src: str) -> str:
    return "assets/pw/" + Path(str(src)).name


def _media_files(d: dict) -> list[str]:
    return [v for sh in d.get("shots") or [] for k, v in sh.items() if k in ("src", "clip") and isinstance(v, str)]


def _csv_rows(text: str) -> list[str]:
    return [x for x in text.splitlines()[1:] if x.strip()]


def _key(row: str) -> str:
    parts = row.split(";")
    return (parts[1] if len(parts) > 1 else row).strip().lower()


def _removed(before: list[str], after: list[str]) -> list[int]:
    """Indexes of `before` rows that are not in `after` (multiset match on the exact row text)."""
    left = {}
    for x in after:
        left[x] = left.get(x, 0) + 1
    out = []
    for i, x in enumerate(before):
        if left.get(x, 0):
            left[x] -= 1
        else:
            out.append(i)
    return out


def _marked(a: str, b: str) -> tuple[str, str]:
    """Both strings as HTML with the characters that differ wrapped in <mark> (a space shows as a marked gap)."""
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ha, hb = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        sa, sb = _e(a[i1:i2]), _e(b[j1:j2])
        if op == "equal":
            ha.append(sa), hb.append(sb)
        else:
            ha.append(f"<mark>{sa}</mark>" if sa else "")
            hb.append(f"<mark>{sb}</mark>" if sb else "")
    return "".join(ha), "".join(hb)


def _shot_times(c: SceneCtx, shots: list[dict]) -> list[float]:
    """Relative start of every shot: `at_word` (spoken word), else `at` seconds, the first shot at 0."""
    out = []
    for i, sh in enumerate(shots):
        t = None
        if i and sh.get("at_word"):
            w = _word_time(c, str(sh["at_word"]))
            t = None if w is None else w - c.start
        if t is None:
            t = float(sh.get("at", 0.0)) if i else 0.0
        out.append(max(0.0, min(c.duration - 0.3, t)))
    return out


def _photo_layer(c: SceneCtx, shots: list[dict], dim: float, events: list) -> tuple[str, list[str]]:
    """Full-frame stills with a slow zoom; a shot with `clip` leaves its slot empty (LAYER plays the clip below)."""
    s, zt = c.sid, c.zone_top
    times = _shot_times(c, shots)
    html_, tl = [], []
    for i, sh in enumerate(shots):
        a = times[i]
        b = times[i + 1] if i + 1 < len(shots) else c.duration
        if not sh.get("clip"):
            z0, z1 = (sh.get("zoom") or [1.0, 1.08])[:2]
            px = sh.get("pan") or [0, 0, 0, -24]
            html_.append(f'<img class="el-phimg" id="{s}-p{i}" src="{_href(sh["src"])}" style="opacity:{1 if i == 0 else 0}"/>')
            tl.append(f'tl.fromTo("#{s}-p{i}",{{scale:{z0},x:{px[0]},y:{px[1]}}},{{scale:{z1},x:{px[2]},y:{px[3]},duration:{max(0.5, b - a):.2f},ease:"none"}},{c.t(a):.3f});')
            if i:
                tl.append(f'tl.to("#{s}-p{i}",{{opacity:1,duration:0.35}},{c.t(a):.3f});')
        else:
            events += [c.t(x) for x in [a + k * 2.0 for k in range(int((b - a) // 2.0) + 1)]]   # the clip moves on its own
        if i and not shots[i - 1].get("clip"):
            tl.append(f'tl.to("#{s}-p{i - 1}",{{opacity:0,duration:0.35}},{c.t(a + 0.05):.3f});')
        events.append(c.t(a))
    grad = (f"linear-gradient(180deg,rgba(8,10,16,{min(0.92, dim + 0.4):.2f}) 0%,rgba(8,10,16,{dim:.2f}) 26%,"
            f"rgba(8,10,16,{dim:.2f}) 52%,rgba(8,10,16,{min(0.94, dim + 0.5):.2f}) 100%)")
    return (f'<div class="el-ph" style="top:-{zt}px">{"".join(html_)}<div class="el-phdim" style="background:{grad}"></div></div>', tl)


# --- rec_photo --------------------------------------------------------------------------------------------

def rec_photo(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    events = [c.start]
    ph, tl = _photo_layer(c, d.get("shots") or [], float(d.get("dim", 0.3)), events)
    parts = [ph, f'<div class="el-aistamp" id="{s}-ai" style="top:{c.zone_h - 66}px">{_e(ui["ai_image"])}</div>']
    for k in ("question", "label", "statement", "claim"):
        _lim("rec_photo", k, d.get(k, ""), k, probs)
    if d.get("question"):
        parts.append(f'<div class="el-question el-shadow" id="{s}-q">{_e(d["question"])}</div>')
    card_rows = []
    if d.get("cmd"):
        run = r["transcript"]["runs"][d["cmd"]]
        card_rows = _cmd_rows(run["prompt"], run.get("allowed_tools") or [])
        top = int(d.get("card_top", 300))
        if d.get("label"):
            parts.append(f'<div class="el-tag amber" id="{s}-lb" style="top:{top - 76}px">{_e(d["label"])}</div>')
        rows = "".join(f'<div class="el-row {k}" id="{s}-c{i}" style="top:{34 + i * 48}px">{_e(t)}</div>' for i, (k, t) in enumerate(card_rows))
        parts.append(f'<div class="el-win el-glass" id="{s}-w" style="top:{top}px;height:{70 + 34 + len(card_rows) * 48 + 30}px">'
                     f'<div class="el-bar"><i></i><i></i><i></i><span>{_e(ui["term"])}</span></div><div class="el-body">{rows}</div></div>')
    if d.get("statement"):
        parts.append(f'<div class="el-statement el-shadow" id="{s}-st" style="top:{int(d.get("statement_top", 330))}px">{_e(d["statement"])}</div>')
    if d.get("claim"):
        parts.append(f'<div class="el-claim" id="{s}-cl" style="top:{int(d.get("statement_top", 330)) + 190}px">{_e(d["claim"])}</div>')
    if d.get("proto"):
        meta = r["meta"]
        model = next((v.get("model") for v in meta["runs"].values() if v.get("model")), meta.get("model_alias"))
        nrep = max(len(v["repetitions"]) for v in r["outcome"]["runs"].values())
        n = len(r["outcome"]["runs"])
        runs_txt = f"{n} Läufe, je {nrep}-mal" if _lang(r) == "de" else f"{n} runs, {nrep} times each"
        line = f'Claude Code {meta["claude_code"]} · {model}'      # two rows: one row would run past the 832 px column
        parts.append(f'<div class="el-pline" id="{s}-pl" style="top:{int(d.get("statement_top", 330)) + 290}px">{_e(line)}<br/>{_e(runs_txt)}</div>')
    out = SceneOut(html=_scene(c, "".join(parts), "el-photo"), problems=probs)
    out.tl += _enter(c) + tl
    out.tl.append(f'tl.fromTo("#{s}-ai",{{opacity:0}},{{opacity:1,duration:0.3}},{c.start:.3f});')
    if d.get("question"):
        tq = _at(c, d, "question_at", 0.04)
        out.tl.append(f'tl.fromTo("#{s}-q",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{tq:.3f});')
        events.append(tq)
    if card_rows:
        tw = _at(c, d, "card_at", 0.12)
        if d.get("label"):
            out.tl.append(f'tl.fromTo("#{s}-lb",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3}},{tw:.3f});')
        out.tl.append(f'tl.fromTo("#{s}-w",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.t(tw - c.start + 0.15):.3f});')
        tt = c.t(tw - c.start + 0.55)
        for i, (_, t) in enumerate(card_rows):
            out.tl.append(_type_tl(f"#{s}-c{i}", c.t(tt - c.start + i * 0.5), len(t), 48))
        events += [tw, tt]
        out.named_events["typing"] = tt
    for key, sel, frac in (("statement_at", "st", 0.2), ("claim_at", "cl", 0.55), ("proto_at", "pl", 0.7)):
        if f"#{s}-{sel}" in out.html or f'id="{s}-{sel}"' in out.html:
            ta = _at(c, d, key, frac)
            out.tl.append(f'tl.fromTo("#{s}-{sel}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{ta:.3f});')
            events.append(ta)
    out.events = sorted(set(round(e, 2) for e in events))
    return out


# --- rec_table --------------------------------------------------------------------------------------------

def rec_table(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    run = d.get("run") or next(iter(r["transcript"]["runs"]))
    fname = d.get("file", "kunden.csv")
    rows = _csv_rows(r["files"][run]["before"][fname])
    seen, dup, first_of = {}, [], {}
    for i, x in enumerate(rows):
        k = _key(x)
        if k in seen:
            dup.append(i)
            first_of[i] = seen[k]
        else:
            seen[k] = i
    pal_idx = {seen[_key(rows[i])]: n for n, i in enumerate(dup)}
    win_h = min(c.zone_h, FULL_H)
    body_h = win_h - 70
    pitch = 80
    items = []
    for i, x in enumerate(rows):
        name, mail = (x.split(";") + [""])[:2]
        mark = " dup" if i in dup or i in pal_idx else ""
        items.append(f'<div class="el-trow{mark}" id="{s}-t{i}" style="top:{12 + i * pitch}px"><span class="el-tn">{i + 1}</span>'
                     f'<div class="el-tc"><b>{_e(name)}</b><em>{_e(mail)}</em></div></div>')
    total_h = 12 + len(rows) * pitch
    dist = max(0, total_h - body_h + 12)
    counters = "".join(f'<b class="el-cnt" id="{s}-n{k}" style="opacity:{1 if k == 0 else 0}">{_e(ui["dup"].format(k))}</b>' for k in range(len(dup) + 1))
    win = (f'<div class="el-win" id="{s}-w" style="top:0;height:{win_h}px"><div class="el-bar"><i></i><i></i><i></i>'
           f'<span>{_e(ui["list"].format(fname, len(rows)))}</span>{counters}</div>'
           f'<div class="el-body" style="height:{body_h}px;overflow:hidden"><div class="el-scroll" id="{s}-sc">{"".join(items)}</div></div></div>')
    # close-up cards: the pairs named in the plan by a part of their e-mail key, characters that differ are marked
    cards = []
    for n, pk in enumerate(d.get("pairs") or []):
        hit = [x for x in rows if pk.lower() in _key(x)]
        if len(hit) < 2:
            probs.append(f"rec_table: pair {pk!r} not found twice in {fname}")
            continue
        ha, hb = _marked(hit[0], hit[1])
        why = (d.get("why") or [""] * 9)[n] if n < len(d.get("why") or []) else ""
        _lim("rec_table", "why", why, f"why{n}", probs)
        cards.append(f'<div class="el-pair" id="{s}-k{n}" style="top:{40 + n * 236}px"><div class="el-pl">{ha}</div>'
                     f'<div class="el-pl">{hb}</div><div class="el-why">{_e(why)}</div></div>')
    out = SceneOut(html=_scene(c, win + "".join(cards), "el-table"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-w",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    t0 = _at(c, d, "scroll_at", 0.1)
    tp = _at(c, d, "pairs_at", 0.6) if cards else c.end
    sdur = max(1.5, min(float(d.get("scroll_seconds", 5.0)), tp - t0 - 0.6))
    out.tl.append(f'tl.to("#{s}-sc",{{y:{-dist},duration:{sdur:.2f},ease:"none"}},{t0:.3f});')
    for n, i in enumerate(dup):                         # a duplicate lights up when it reaches the lower third of the window
        y = 12 + i * pitch
        frac = min(1.0, max(0.0, (y - body_h * 0.66) / max(1, dist)))
        ti = c.t(t0 - c.start + frac * sdur)
        out.tl.append(f'tl.fromTo("#{s}-t{i}, #{s}-t{first_of[i]}",{{"--hl":0}},{{"--hl":1,duration:0.25}},{ti:.3f});')
        out.tl.append(f'tl.set("#{s}-n{n}",{{opacity:0}},{ti:.3f});tl.set("#{s}-n{n + 1}",{{opacity:1}},{ti:.3f});')
        if n in (0, len(dup) - 1):
            events.append(ti)
        out.named_events.setdefault("duplicate_marked", ti)
    for i in range(len(rows)):                          # rows scrolled out above the window are hidden, so checks see them gone
        y = 12 + i * pitch
        if y + pitch < dist:
            out.tl.append(f'tl.set("#{s}-t{i}",{{visibility:"hidden"}},{c.t(t0 - c.start + (y + pitch) / dist * sdur):.3f});')
    if cards:
        out.tl.append(f'tl.to("#{s}-w",{{opacity:0,y:-40,duration:0.35}},{tp:.3f});tl.set("#{s}-w",{{visibility:"hidden"}},{c.t(tp - c.start + 0.4):.3f});')
        gap = float(d.get("pair_gap", 1.1))
        for n in range(len(cards)):
            tk = c.t(tp - c.start + 0.25 + n * gap)
            out.tl.append(f'tl.fromTo("#{s}-k{n}",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{tk:.3f});')
            out.tl.append(f'tl.fromTo("#{s}-k{n} mark",{{backgroundColor:"rgba(251,191,36,0)"}},{{backgroundColor:"rgba(251,191,36,0.85)",duration:0.3}},{c.t(tk - c.start + 0.4):.3f});')
            events += [tk, c.t(tk - c.start + 0.4)]
            out.named_events.setdefault("pair_mark", c.t(tk - c.start + 0.4))
    out.events = sorted(set(round(e, 2) for e in events))
    return out


# --- rec_diff ---------------------------------------------------------------------------------------------

def rec_diff(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    run = d.get("run") or next(iter(r["transcript"]["runs"]))
    fb, fa = d.get("file_before", "kunden.csv"), d.get("file_after", "bereinigt.csv")
    before = _csv_rows(r["files"][run]["before"][fb])
    after = _csv_rows(r["files"][run]["after"].get(fa, ""))
    gone = _removed(before, after)
    expect = int(d.get("expected", len(after)))
    ok = len(after) == expect
    reps = r["outcome"]["runs"][run]["repetitions"]
    agree = sum(1 for x in reps if x.get("rows") == reps[0].get("rows"))
    _lim("rec_diff", "note", d.get("note", ""), "note", probs)
    pitch = 18
    strips = "".join(f'<div class="el-strip" id="{s}-s{i}" style="top:{i * pitch}px"></div>' for i in range(len(before)))
    nums = list(range(len(before), len(before) - len(gone) - 1, -1))
    counter = "".join(f'<div class="el-big" id="{s}-n{k}" style="opacity:{1 if k == 0 else 0}">{v}</div>' for k, v in enumerate(nums))
    inner = f"""<div class="el-dhead" id="{s}-h">{_e(fb)} → {_e(fa)}</div>
<div class="el-strips" id="{s}-ss">{strips}</div>
<div class="el-dright">{counter}
  <div class="el-dlab">{_e(ui["rows_in"].format(fa))}</div>
  <div class="el-dexp" id="{s}-e">{_e(ui["expect"].format(expect))}</div>
  <div class="el-dstamp {'ok' if ok else 'bad'}" id="{s}-v">{_e(ui["ok"] if ok else ui["off"])}</div>
  <div class="el-drep" id="{s}-r">{_e(ui["rep"].format(agree, len(reps)))}</div>
  <div class="el-dnote" id="{s}-no">{_e(d.get("note", ""))}</div>
</div>"""
    out = SceneOut(html=_scene(c, inner, "el-diff"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-h",{{opacity:0}},{{opacity:1,duration:0.3}},{c.start:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-ss .el-strip",{{scaleX:0}},{{scaleX:1,duration:0.25,stagger:0.015,ease:"power2.out"}},{c.t(0.1):.3f});')
    events = [c.start, c.t(0.1)]
    t0 = _at(c, d, "remove_at", 0.2)
    gap = min(0.45, max(0.2, (c.duration * 0.5) / max(1, len(gone))))
    for k, i in enumerate(gone):
        ti = c.t(t0 - c.start + k * gap)
        out.tl.append(f'tl.to("#{s}-s{i}",{{backgroundColor:"var(--red)",duration:0.12}},{ti:.3f});')
        tc = c.t(ti - c.start + 0.18)
        out.tl.append(f'tl.to("#{s}-s{i}",{{scaleY:0,opacity:0,duration:0.25,ease:"power2.in"}},{tc:.3f});')
        below = ",".join(f"#{s}-s{j}" for j in range(i + 1, len(before)))
        if below:                                      # every row below moves up by the rows removed so far (transform only)
            out.tl.append(f'tl.to("{below}",{{y:{-(k + 1) * pitch},duration:0.25,ease:"power2.inOut"}},{tc:.3f});')
        out.tl.append(f'tl.set("#{s}-n{k}",{{opacity:0}},{ti:.3f});tl.set("#{s}-n{k + 1}",{{opacity:1}},{ti:.3f});')
        if k in (0, len(gone) - 1):
            events.append(ti)
        out.named_events.setdefault("row_removed", ti)
    tv = _at(c, d, "verdict_at", 0.7)
    tv = max(tv, c.t(t0 - c.start + len(gone) * gap + 0.2))
    out.tl.append(f'tl.fromTo("#{s}-e",{{opacity:0}},{{opacity:1,duration:0.3}},{c.t(tv - c.start - 0.4):.3f});')
    out.tl.append(f'tl.fromTo("#{s}-v",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.22,ease:"power4.in"}},{tv:.3f});')
    out.tl.append(f'tl.fromTo("#{s}-r",{{opacity:0}},{{opacity:1,duration:0.3}},{c.t(tv - c.start + 0.4):.3f});')
    if d.get("note"):
        out.tl.append(f'tl.fromTo("#{s}-no",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3}},{_at(c, d, "note_at", 0.85):.3f});')
    events += [tv, c.t(tv - c.start + 0.4), _at(c, d, "note_at", 0.85)]
    out.named_events["verdict"] = tv
    if not ok:
        probs.append(f"rec_diff: {fa} has {len(after)} rows, expected {expect} (shown as '{ui['off']}')")
    out.events = sorted(set(round(e, 2) for e in events))
    return out


# --- rec_answer -------------------------------------------------------------------------------------------

ANS_FS = 32
ANS_CH = 0.56            # average advance of the body font in em (conservative, so a row never runs wider than the card)


def _plain(text: str) -> str:
    return text.replace("**", "").replace("`", "")


def _wrap_prose(text: str, width_px: int, fs: int) -> list[str]:
    """Like _wrap_rows, but a long word breaks after '-' or '/' instead of in the middle of the word."""
    per = max(8, int(width_px // (fs * MONO_CH)))
    rows, para = [], str(text)
    while len(para) > per:
        cut = para.rfind(" ", 0, per + 1)
        if cut < per * 0.5:
            cut = max(para.rfind("-", 0, per), para.rfind("/", 0, per)) + 1 or per
        rows.append(para[:cut].rstrip())
        para = para[cut:].lstrip()
    return rows + [para]


def rec_answer(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    run = d["run"]
    ans = next((ln["text"] for ln in reversed(r["transcript"]["runs"][run]["lines"]) if ln["kind"] == "text"), "")
    plain = _plain(ans)
    width = int((800 - 60) * MONO_CH / ANS_CH)         # _wrap_rows counts mono cells; scale the width to the body font
    marks = d.get("highlights") or []
    rows, last = [], -1                                # rows: (kind, html)
    for p in d.get("picks") or []:
        pos = plain.find(p)
        if pos < 0:
            probs.append(f"rec_answer: pick not in the recorded answer: {p[:50]!r}")
            continue
        if rows and pos > last + 4:                  # a skipped part of the answer shows as one "…" row
            rows.append(("gap", "…"))
        spans = [(p.find(m), p.find(m) + len(m), n) for n, m in enumerate(marks) if m in p]
        off = 0
        for w in _wrap_prose(p, width, ANS_FS):      # mark by character position, so a phrase may cross a row break
            o = p.find(w, off)
            cut = sorted({0, len(w)} | {min(len(w), max(0, x - o)) for a_, b_, _ in spans for x in (a_, b_)})
            h = ""
            for x, y in zip(cut, cut[1:]):
                n = next((n for a_, b_, n in spans if a_ <= o + x and o + y <= b_), None)
                h += _e(w[x:y]) if n is None else f'<mark class="m{n}">{_e(w[x:y])}</mark>'
            rows.append(("txt", h))
            off = o + len(w)
        last = pos + len(p)
    row_h = 46
    card_h = 70 + 30 + len(rows) * row_h + 30
    if card_h * 1.08 > min(c.zone_h, FULL_H):
        probs.append(f"rec_answer: {len(rows)} rows, card {card_h} px too tall for the zone")
    body = "".join(f'<div class="el-arow {k}" id="{s}-a{i}" style="top:{30 + i * row_h}px">{t}</div>' for i, (k, t) in enumerate(rows))
    inner = (f'<div class="el-win el-ans" id="{s}-w" style="top:20px;left:32px;width:800px;height:{card_h}px">'
             f'<div class="el-bar"><i></i><i></i><i></i><span>{_e(ui["answer"].format(_run_no(r, run)))}</span></div>'
             f'<div class="el-body">{body}</div></div>')
    out = SceneOut(html=_scene(c, inner, "el-answer"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-w",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});')
    events = [c.start]
    for i in range(len(rows)):
        ti = c.t(0.3 + i * 0.12)
        out.tl.append(f'tl.fromTo("#{s}-a{i}",{{opacity:0}},{{opacity:1,duration:0.15}},{ti:.3f});')
    tz = _at(c, d, "zoom_at", 0.3)                      # slow push-in (the card grows to the full 864 px width)
    out.tl.append(f'tl.to("#{s}-w",{{scale:1.08,transformOrigin:"50% 30%",duration:{max(1.0, c.end - tz - 0.3):.2f},ease:"sine.inOut"}},{tz:.3f});')
    events.append(tz)
    words = d.get("highlight_words") or []            # one spoken word per highlight: the phrase lights up there
    for n, m in enumerate(marks):
        tm = _at(c, {"m_word": words[n]} if n < len(words) else {}, "m_at", 0.35 + 0.18 * n)
        out.tl.append(f'tl.to("#{s}-w .m{n}",{{backgroundColor:"rgba(251,191,36,0.85)",color:"#0B0C10",duration:0.3}},{tm:.3f});')
        events.append(tm)
        out.named_events.setdefault("highlight", tm)
    out.events = sorted(set(round(e, 2) for e in events))
    return out


# --- rec_split --------------------------------------------------------------------------------------------

def rec_split(c: SceneCtx, d: dict) -> SceneOut:
    s, probs = c.sid, []
    r = rec(d["rec"])
    ui = _ui(r)
    ra, rb = (d.get("runs") or list(r["transcript"]["runs"])[:2])[:2]
    runs = r["transcript"]["runs"]
    pa, pb = runs[ra]["prompt"], runs[rb]["prompt"]
    pre = pa.rstrip(" ?!.").rsplit(".", 1)[0] + "."      # the shared first sentence
    extra = pb[len(pre):].strip() if pb.startswith(pre) else pb
    tail = pa[len(pre):].strip()
    if extra.endswith(tail):
        extra = extra[: len(extra) - len(tail)].strip()  # drop the shared closing question from the marked part
    fa = d.get("file_after", "bereinigt.csv")
    fb_ = d.get("file_before", "kunden.csv")
    gone = [set(_removed(_csv_rows(r["files"][x]["before"][fb_]), _csv_rows(r["files"][x]["after"].get(fa, "")))) for x in (ra, rb)]
    same = gone[0] == gone[1]
    expect = int(d.get("expected", 0)) or None
    cols = []
    W, FSP = 420, 28
    for n, rid in enumerate((ra, rb)):
        after = _csv_rows(r["files"][rid]["after"].get(fa, ""))
        reps = r["outcome"]["runs"][rid]["repetitions"]
        agree = sum(1 for x in reps if x.get("rows") == reps[0].get("rows"))
        ok = expect is None or len(after) == expect
        if n == 0:
            lines = _wrap_rows(pre, W - 40, FSP)
            ptxt = "".join(f'<div class="el-prow">{_e(x)}</div>' for x in lines)
        else:
            lines = _wrap_rows(extra, W - 40, FSP)
            ptxt = f'<div class="el-prow dim">{_e(ui["plus"])}</div>' + "".join(f'<div class="el-prow"><mark>{_e(x)}</mark></div>' for x in lines)
        cols.append(f"""<div class="el-col" id="{s}-c{n}" style="left:{n * (W + 24)}px;width:{W}px">
  <div class="el-chead"><span>{_e(ui["run_no"].format(_run_no(r, rid)))}</span><b>{_e(runs[rid]["title"])}</b></div>
  <div class="el-cprompt" id="{s}-p{n}">{ptxt}</div>
  <div class="el-cres" id="{s}-r{n}"><div class="el-cnum">{len(after)}</div><div class="el-cside"><span>{_e(ui["rows"].format("").strip())}</span>
  <b class="{'ok' if ok else 'bad'}">{_e(ui["ok"] if ok else ui["off"])}</b><em>{_e(ui["agree"].format(agree, len(reps)))}</em></div></div>
</div>""")
    bar = f'<div class="el-sbar {"ok" if same else "bad"}" id="{s}-b">{_e(ui["same_rows"].format(len(gone[0])) if same else ui["diff_rows"])}</div>'
    out = SceneOut(html=_scene(c, "".join(cols) + bar, "el-split"), problems=probs)
    out.tl += _enter(c)
    out.tl.append(f'tl.fromTo("#{s}-c0",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{c.start:.3f});')
    tw = _at(c, d, "swipe_at", 0.2)
    out.tl.append(f'tl.fromTo("#{s}-c1",{{opacity:0,x:160}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{tw:.3f});')
    tm = _at(c, d, "mark_at", 0.35)
    out.tl.append(f'tl.fromTo("#{s}-p1 mark",{{backgroundSize:"0% 100%"}},{{backgroundSize:"100% 100%",duration:0.6,stagger:0.12}},{tm:.3f});')
    tr = _at(c, d, "result_at", 0.6)
    for n in range(2):
        out.tl.append(f'tl.fromTo("#{s}-r{n}",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.25,ease:"power4.in"}},{c.t(tr - c.start + n * 0.35):.3f});')
    tb = _at(c, d, "same_at", 0.8)
    out.tl.append(f'tl.fromTo("#{s}-b",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{tb:.3f});')
    out.named_events = {"swipe": tw, "result": tr, "same": tb}
    out.events = sorted(set(round(e, 2) for e in [c.start, tw, tm, tr, c.t(tr - c.start + 0.35), tb]))
    return out


TEMPLATES.update({"rec_photo": rec_photo, "rec_table": rec_table, "rec_diff": rec_diff, "rec_answer": rec_answer, "rec_split": rec_split})
_css_base = CSS


def CSS(pal: dict, display: str, display_w: int, body: str, mono: str, zone_top: int = 300, zone_h: int = 930, flat: bool = False) -> str:  # noqa: F811
    text, muted, acc = pal["text"], pal["muted"], pal["accent"]
    hair = pal.get("hairline", "rgba(248,250,252,0.10)")
    green, red, amber, on = (pal.get("signal_green", "#4ADE80"), pal.get("signal_red", "#F87171"),
                             pal.get("signal_amber", "#FBBF24"), pal.get("on_signal", "#0B0C10"))
    return _css_base(pal, display, display_w, body, mono, zone_top, zone_h, flat) + f"""
/* --- Echtlauf Neustart 03.11.2026: photo, table, diff, answer, split --- */
.el-scene{{--red:{red};}}
.el-ph{{position:absolute;left:-108px;width:1080px;height:1920px;overflow:hidden;}}
.el-phimg{{position:absolute;left:-2%;top:-2%;width:104%;height:104%;object-fit:cover;}}
.el-phdim{{position:absolute;inset:0;}}
.el-aistamp{{position:absolute;left:0;padding:8px 18px;border-radius:8px;background:rgba(11,12,16,0.78);border:2px solid {hair};color:{text};font-size:30px;font-weight:600;white-space:nowrap;}}
.el-shadow{{text-shadow:0 3px 18px rgba(0,0,0,0.65);}}
.el-glass{{background:rgba(28,31,41,0.94);}}
.el-pline{{position:absolute;left:0;width:832px;font-family:'FN {mono}';font-size:30px;line-height:42px;color:{text};text-shadow:0 2px 12px rgba(0,0,0,0.7);white-space:nowrap;}}
.el-cnt{{position:absolute;right:22px;font-weight:600;font-size:30px;color:{on};background:{amber};padding:4px 14px;border-radius:8px;}}
.el-trow{{position:absolute;left:12px;right:12px;height:74px;display:flex;align-items:center;gap:14px;border-radius:8px;padding:0 12px;--hl:0;
  background:color-mix(in srgb,{amber} calc(var(--hl) * 20%),transparent);border-left:6px solid color-mix(in srgb,{amber} calc(var(--hl) * 100%),transparent);}}
.el-tn{{flex:0 0 56px;font-family:'FN {mono}';font-size:28px;color:{muted};opacity:0.7;}}
.el-tc{{display:flex;flex-direction:column;line-height:34px;white-space:nowrap;}}
.el-tc b{{font-weight:600;font-size:30px;color:{text};}} .el-tc em{{font-style:normal;font-family:'FN {mono}';font-size:28px;color:{muted};}}
.el-pair{{position:absolute;left:0;width:864px;height:212px;padding:22px 26px;border:2px solid {hair};border-radius:14px;background:{WIN_BG};}}
.el-pl{{font-family:'FN {mono}';font-size:30px;line-height:50px;color:{text};white-space:pre;}}
.el-pl mark,.el-arow mark{{background:transparent;color:inherit;border-radius:6px;padding:0 2px;}}
.el-pl mark{{color:{on};}}
.el-why{{margin-top:10px;display:inline-block;padding:4px 14px;border-radius:8px;background:color-mix(in srgb,{amber} 16%,transparent);color:{amber};font-size:30px;font-weight:600;}}
.el-dhead{{position:absolute;left:0;top:0;font-family:'FN {mono}';font-size:32px;color:{text};white-space:nowrap;}}
.el-strips{{position:absolute;left:0;top:70px;width:400px;}}
.el-strip{{position:absolute;left:0;width:400px;height:14px;border-radius:4px;background:color-mix(in srgb,{text} 26%,transparent);transform-origin:0 50%;}}
.el-dright{{position:absolute;left:440px;top:60px;width:424px;}}
.el-big{{position:absolute;left:0;top:0;font-family:'FN {display}';font-weight:{display_w};font-size:200px;line-height:200px;color:{text};}}
.el-dlab{{position:absolute;left:0;top:214px;width:424px;font-size:32px;line-height:40px;color:{muted};}}
.el-dexp{{position:absolute;left:0;top:300px;font-family:'FN {mono}';font-size:32px;color:{text};}}
.el-dstamp{{position:absolute;left:0;top:360px;font-family:'FN {display}';font-weight:800;font-size:44px;padding:8px 22px;border-radius:10px;color:{on};white-space:nowrap;}}
.el-dstamp.ok{{background:{green};}} .el-dstamp.bad{{background:{red};}}
.el-drep{{position:absolute;left:0;top:460px;font-size:30px;color:{muted};white-space:nowrap;}}
.el-dnote{{position:absolute;left:0;top:520px;width:424px;font-size:30px;line-height:40px;color:{text};}}
.el-ans .el-body{{position:relative;}}
.el-arow{{position:absolute;left:30px;right:30px;height:46px;font-size:{ANS_FS}px;line-height:46px;white-space:pre;color:{text};}}
.el-arow.gap{{color:{muted};}}
.el-col{{position:absolute;top:0;height:640px;border:2px solid {hair};border-radius:14px;background:{WIN_BG};overflow:hidden;}}
.el-chead{{padding:18px 20px 12px;border-bottom:2px solid {hair};display:flex;flex-direction:column;gap:4px;}}
.el-chead span{{font-family:'FN {mono}';font-size:28px;color:{muted};}} .el-chead b{{font-size:34px;color:{text};white-space:nowrap;}}
.el-cprompt{{padding:16px 20px;}}
.el-prow{{font-family:'FN {mono}';font-size:28px;line-height:40px;color:{text};white-space:pre;}}
.el-prow.dim{{color:{muted};}}
.el-prow mark{{color:{on};background:linear-gradient({amber},{amber}) no-repeat 0 0/100% 100%;border-radius:4px;}}
.el-cres{{position:absolute;left:20px;right:20px;bottom:18px;display:flex;align-items:center;gap:18px;}}
.el-cnum{{font-family:'FN {display}';font-weight:{display_w};font-size:120px;line-height:120px;color:{text};}}
.el-cside{{display:flex;flex-direction:column;gap:6px;}}
.el-cside span{{font-size:30px;color:{muted};}} .el-cside em{{font-style:normal;font-size:28px;color:{muted};white-space:nowrap;}}
.el-cside b{{font-family:'FN {display}';font-size:34px;padding:2px 14px;border-radius:8px;color:{on};white-space:nowrap;align-self:flex-start;}}
.el-cside b.ok{{background:{green};}} .el-cside b.bad{{background:{red};}}
.el-sbar{{position:absolute;left:0;top:670px;width:864px;padding:18px 24px;border-radius:12px;font-size:32px;font-weight:600;color:{on};}}
.el-sbar.ok{{background:{green};}} .el-sbar.bad{{background:{red};}}
"""


_layer_base = LAYER


def LAYER(plan, brand, project_dir, captions) -> dict:  # noqa: F811,N802 (contract name)
    """The Echtlauf ground and stamp, plus: copy photos and clips to <project>/assets/pw/, play each clip under the
    scenes from its shot's start, and hide the "Echter Ablauf" stamp while a KI-Bild is on screen."""
    res = _layer_base(plan, brand, project_dir, captions)
    words = [w for g in captions for w in getattr(g, "words", [])]
    dst = Path(project_dir) / "assets" / "pw"
    problems, html_, js = list(res.get("problems", [])), [], []
    for b in getattr(plan, "beats", []):
        d = getattr(b, "data", {}) or {}
        if getattr(b, "scene_type", "") != "rec_photo":
            continue
        for src in _media_files(d):
            p = PHOTO_ROOT / src
            if not p.exists():
                problems.append(f"{b.id}: {src} not found under {PHOTO_ROOT}")
                continue
            dst.mkdir(parents=True, exist_ok=True)
            if not (dst / p.name).exists():
                shutil.copy2(p, dst / p.name)
        st, du = float(getattr(b, "start", 0) or 0), float(getattr(b, "duration", 0) or 0)
        js.append(f'T.to("#elx-stamp",{{opacity:0,duration:0.25}},{st:.3f});T.to("#elx-stamp",{{opacity:1,duration:0.25}},{st + du - 0.1:.3f});')
        shots = d.get("shots") or []
        bw = [w for w in words if st <= w.start < st + du]
        times = []
        for i, sh in enumerate(shots):
            t = None
            if i and sh.get("at_word"):
                hit = next((w for w in bw if w.text.lower().strip(".,:;!?\"'„“").startswith(str(sh["at_word"]).lower())), None)
                t = None if hit is None else hit.start - st
            times.append(max(0.0, (t if t is not None else float(sh.get("at", 0.0))) if i else 0.0))
        for i, sh in enumerate(shots):
            if not sh.get("clip"):
                continue
            a = times[i]
            e = times[i + 1] if i + 1 < len(shots) else du
            if e - a > CLIP_SECONDS + 0.05:
                problems.append(f"{b.id}: clip {sh['clip']} covers {e - a:.1f} s, the clip has {CLIP_SECONDS:.0f} s")
            vid = f"pwclip-{b.id}-{i}"
            html_.append(f'<video id="{vid}" class="clip pw-clip" src="{_href(sh["clip"])}" data-start="{st + a:.3f}" '
                         f'data-duration="{min(e - a + 0.35, CLIP_SECONDS):.3f}" data-track-index="0" data-volume="0" muted playsinline '
                         f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:1"></video>')
            if i == 0:
                js.append(f'T.fromTo("#{vid}",{{opacity:0}},{{opacity:1,duration:0.35}},{st + a:.3f});')
    if html_:
        res["under_scenes_html"] = res.get("under_scenes_html", "") + "".join(html_)
    if js:
        res["body_end_html"] = res.get("body_end_html", "") + (
            "<script>(function(){var T=window.__timelines&&window.__timelines.main;if(!T)return;" + "".join(js) + "T.seek(0);})();</script>")
    res["problems"] = problems
    return res
