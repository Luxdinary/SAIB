"""Promptwerk format "Echtlauf": run a real Claude Code task in a sandbox folder and record it with timestamps.

Usage (from the repository root):
    .venv\\Scripts\\python.exe brands\\claude_workflows\\echtlauf\\record_run.py brands\\claude_workflows\\echtlauf\\specs\\<id>.json
    ... --repeat 2        run every Lauf twice (Prüfregel: same outcome required)
    ... --check           re-run once and compare with the stored outcome, write nothing but check.json

A spec describes the sandbox (sample files only, never Stefan's data) and one or more runs (Läufe). For every run
the sandbox is rebuilt from the spec, `.claude/settings.json` is written when the run has `settings`, and
`claude -p` runs with `--output-format stream-json`. Every stdout line is stamped with the seconds since the start
of the process. Results go to `brands/claude_workflows/echtlauf/recordings/<id>/`:

    meta.json           date, Claude Code version, model id, exact command lines, isolation flags
    <run>-<k>.jsonl     raw stream-json events with {"t": seconds, "event": {...}} (k = repetition, 1-based)
    transcript.json     display lines per run for the video (from repetition 1), paths redacted
    outcome.json        outcome per run and repetition, and whether all repetitions agree
    files_before/after  sandbox state per run (small text files only)

Isolation: user settings, MCP servers and slash commands are switched off (`--setting-sources project,local`,
`--strict-mcp-config`, `--disable-slash-commands`), no session is persisted, and the desktop app's environment
variables (CLAUDE*, ANTHROPIC*) are removed so the CLI behaves as in a plain terminal.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX_ROOT = Path(r"C:\Automation\promptwerk-sandbox")
ISOLATION = ["--setting-sources", "project,local", "--strict-mcp-config", "--disable-slash-commands",
             "--no-session-persistence"]
KEEP_ENV = {"CLAUDE_CODE_GIT_BASH_PATH"}
# display strings of the transcript per recording language (spec "language", default de)
L10N = {"de": {"start": "Start: {}", "think": "denkt nach (Inhalt ausgeblendet)", "more": "… ({} weitere Zeilen)",
               "end": "Ende nach {:.1f} s"},
        "en": {"start": "Start: {}", "think": "thinking (content hidden)", "more": "… ({} more lines)",
               "end": "Done after {:.1f} s"}}


def clean_env() -> dict:
    env = {k: v for k, v in os.environ.items()
           if k in KEEP_ENV or not (k.startswith(("CLAUDE", "ANTHROPIC")) or k in ("USE_LOCAL_OAUTH", "USE_STAGING_OAUTH"))}
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def claude_bin() -> str:
    """`PW_CLAUDE_BIN` (e.g. a newer native build) or the `claude` on PATH; the version goes into the stamp."""
    return os.environ.get("PW_CLAUDE_BIN") or shutil.which("claude") or "claude"


def claude_version(env: dict) -> str:
    out = subprocess.run([claude_bin(), "--version"], capture_output=True, text=True, encoding="utf-8", env=env)
    m = re.search(r"\d+\.\d+\.\d+", out.stdout or "")
    return m.group(0) if m else (out.stdout or "").strip()


def build_sandbox(spec: dict, run: dict) -> Path:
    box = SANDBOX_ROOT / spec["id"]
    if box.exists():
        # never delete: an old sandbox state moves to a dated folder next to it
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        (SANDBOX_ROOT / "_alt").mkdir(parents=True, exist_ok=True)
        box.rename(SANDBOX_ROOT / "_alt" / f"{spec['id']}-{stamp}")
    box.mkdir(parents=True)
    # run "files" add to or replace the spec files (e.g. a CLAUDE.md only in one run); null leaves a file out
    for rel, content in {**spec["files"], **(run.get("files") or {})}.items():
        if content is None:
            continue
        p = box / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
    if run.get("settings") is not None:
        p = box / ".claude" / "settings.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(run["settings"], indent=2) + "\n", encoding="utf-8", newline="\n")
    for argv in spec.get("setup_cmds", []) + run.get("setup_cmds", []):     # e.g. ["git", "init", "-q"]
        subprocess.run(argv, cwd=box, capture_output=True, text=True)
    return box


def big_file(text: str, lang: str = "de", keep: int = 12) -> str:
    """A large text file as its first lines plus a visible '… (n weitere Zeilen)' line."""
    rows = text.splitlines()
    return "\n".join(rows[:keep] + [L10N.get(lang, L10N["de"])["more"].format(len(rows) - keep)]) + "\n"


def snapshot(box: Path, lang: str = "de") -> dict:
    out = {}
    for p in sorted(box.rglob("*")):
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            out[p.relative_to(box).as_posix()] = f"<binary {p.stat().st_size} bytes>"
            continue
        out[p.relative_to(box).as_posix()] = text if p.stat().st_size <= 60000 else big_file(text, lang)
    return out


def command(spec: dict, run: dict) -> list[str]:
    # a spec may drop single isolation flags (skills need slash commands: "drop_isolation": ["--disable-slash-commands"])
    drop = set(spec.get("drop_isolation", []) + run.get("drop_isolation", []))
    iso = [x for x in ISOLATION if x not in drop]
    if "--setting-sources" in drop:
        iso = [x for x in iso if x != "project,local"]
    cmd = [claude_bin(), "-p", run["prompt"], "--model", spec.get("model", "haiku"),
           "--output-format", "stream-json", "--verbose"] + iso
    if run.get("tools", spec.get("tools")):
        cmd += ["--tools", run.get("tools", spec.get("tools"))]
    if run.get("allowed_tools"):
        cmd += ["--allowedTools", *run["allowed_tools"]]
    if run.get("permission_mode"):
        cmd += ["--permission-mode", run["permission_mode"]]
    cmd += spec.get("extra_args", []) + run.get("extra_args", [])
    return cmd


def run_once(spec: dict, run: dict, env: dict) -> dict:
    box = build_sandbox(spec, run)
    before = snapshot(box, spec.get("language", "de"))
    cmd = command(spec, run)
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=box, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    events = []
    for line in proc.stdout:
        t = round(time.monotonic() - t0, 3)
        line = line.strip()
        if not line:
            continue
        try:
            events.append({"t": t, "event": json.loads(line)})
        except json.JSONDecodeError:
            events.append({"t": t, "raw": line})
    stderr = proc.stderr.read()
    proc.wait()
    return {"cmd": cmd, "box": str(box), "exit": proc.returncode, "stderr": stderr[-4000:], "events": events,
            "before": before, "after": snapshot(box, spec.get("language", "de")), "wall": round(time.monotonic() - t0, 3)}


# ---------------------------------------------------------------------------------------------------------------
# display transcript and outcome

def _redact(s: str, box: str) -> str:
    s = str(s)
    for form in {box, box.replace("\\", "/"), "/" + box[0].lower() + box[2:].replace("\\", "/")}:
        s = s.replace(form, ".")
    s = re.sub(r"(?i)C:[\\/]+Users[\\/]+[^\\/\s\"']+", "~", s)
    return s


def _tool_label(name: str, inp: dict) -> str:
    if name == "Bash":
        return f"Bash: {inp.get('command', '')}"
    if name in ("Read", "Write", "Edit"):
        return f"{name}: {inp.get('file_path', '')}"
    if name in ("Grep", "Glob"):
        return f"{name}: {inp.get('pattern', '')}"
    return f"{name}: {json.dumps(inp, ensure_ascii=False)[:80]}"


def _result_text(content) -> str:
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return str(content or "")


def transcript(rec: dict, max_result_lines: int = 3, lang: str = "de") -> dict:
    """Display lines: prompt, tool calls, tool results (denied/ok), text, final result. Wording is never changed;
    long tool results are cut after `max_result_lines` lines with a visible '…' line that says how many were cut."""
    L = L10N.get(lang, L10N["de"])
    box = rec["box"]
    lines, meta = [], {}
    for item in rec["events"]:
        ev, t = item.get("event") or {}, item["t"]
        typ = ev.get("type")
        n0 = len(lines)
        if typ == "system" and ev.get("subtype") == "init":
            meta.update(model=ev.get("model"), tools=ev.get("tools"), permission_mode=ev.get("permissionMode"),
                        claude_code_version=ev.get("claude_code_version"))
            lines.append({"t": t, "kind": "init", "text": L["start"].format(ev.get("model"))})
        elif typ == "assistant":
            for c in (ev.get("message") or {}).get("content", []):
                if c.get("type") in ("thinking", "redacted_thinking"):
                    if not lines or lines[-1]["kind"] != "think":     # the content itself is never shown
                        lines.append({"t": t, "kind": "think", "text": L["think"]})
                elif c.get("type") == "text" and c.get("text", "").strip():
                    lines.append({"t": t, "kind": "text", "text": _redact(c["text"].strip(), box)})
                elif c.get("type") == "tool_use":
                    lines.append({"t": t, "kind": "tool", "id": c.get("id"),
                                  "text": _redact(_tool_label(c.get("name", ""), c.get("input") or {}), box)})
        elif typ == "user":
            content = (ev.get("message") or {}).get("content", [])
            for c in content if isinstance(content, list) else []:
                if c.get("type") != "tool_result":
                    continue
                txt = _redact(_result_text(c.get("content")), box).rstrip()
                rows = txt.splitlines() or [""]
                kind = "denied" if c.get("is_error") else "result"
                cut = rows[:max_result_lines]
                if len(rows) > max_result_lines:
                    cut.append(L["more"].format(len(rows) - max_result_lines))
                lines.append({"t": t, "kind": kind, "id": c.get("tool_use_id"), "text": "\n".join(cut)})
        elif typ == "result":
            meta.update(duration_ms=ev.get("duration_ms"), num_turns=ev.get("num_turns"),
                        total_cost_usd=ev.get("total_cost_usd"), is_error=ev.get("is_error"),
                        permission_denials=len(ev.get("permission_denials") or []))
            if lines and lines[-1]["kind"] == "end":      # a second result event (after a subagent) replaces the first
                lines.pop()
            lines.append({"t": t, "kind": "end", "text": L["end"].format(t)})
        if ev.get("parent_tool_use_id"):                  # lines written inside a subagent are marked for the frame
            for ln in lines[n0:]:
                ln["sub"] = True
    return {"lines": lines, "meta": meta}


def outcome(rec: dict, probe: str | None, where: str = "answer") -> dict:
    """probe_hit: the probe value appears in the final answer (where="answer"), in one sandbox file after the run
    (where="file:<path>"), or in any file the run created or changed (where="files")."""
    tools, denied, usage = [], 0, {}
    final = ""
    for item in rec["events"]:
        ev = item.get("event") or {}
        if ev.get("type") == "assistant":
            for c in (ev.get("message") or {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(c.get("name"))
        if ev.get("type") == "user":
            content = (ev.get("message") or {}).get("content", [])
            for c in content if isinstance(content, list) else []:
                if c.get("type") == "tool_result" and c.get("is_error"):
                    denied += 1
        if ev.get("type") == "result":
            final = str(ev.get("result") or "")
            u = ev.get("usage") or {}
            usage = {"input_tokens": sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                                        "cache_read_input_tokens")),
                     "output_tokens": int(u.get("output_tokens") or 0), "num_turns": ev.get("num_turns"),
                     "duration_s": round((ev.get("duration_ms") or 0) / 1000, 1)}
    in_answer = (probe in final) if probe else None
    hit = in_answer
    if probe and where.startswith("file:"):
        hit = probe in rec["after"].get(where[5:], "")
    elif probe and where == "files":
        hit = any(probe in v for k, v in rec["after"].items() if rec["before"].get(k) != v)
    elif probe and where == "tool":                  # probe = (part of) a tool name, e.g. "Skill" or "mcp__docs"
        hit = any(probe in (t or "") for t in tools)
    extra = {}
    if probe and where.startswith("rows:"):          # probe = expected number of data rows (header excluded)
        text = rec["after"].get(where[5:])
        rows = None if text is None else max(0, len([x for x in text.splitlines() if x.strip()]) - 1)
        hit, extra = rows == int(probe), {"rows": rows}
    return {"probe_in_answer": in_answer, "probe_hit": hit, "tool_errors": denied > 0,
            "tools_used": sorted(set(tools)), "exit": rec["exit"], **extra, **usage}


def same(outs: list[dict], keys=("probe_hit", "tool_errors", "exit")) -> bool:
    get =lambda o, k: o.get(k, o.get("probe_in_answer")) if k == "probe_hit" else o.get(k)
    return all(all(get(o, k) == get(outs[0], k) for k in keys) for o in outs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--only", default=None, help="comma-separated run ids")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--rebuild", action="store_true", help="rebuild transcript.json from the stored <run>-1.jsonl, no new run")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    lang = spec.get("language", "de")
    keys = tuple(spec.get("same_keys", ("probe_hit", "tool_errors", "exit")))
    probe_of = lambda r: (r.get("probe", spec.get("probe")), r.get("probe_where", spec.get("probe_where", "answer")))
    env = clean_env()
    out_dir = HERE / "recordings" / spec["id"]
    runs = [r for r in spec["runs"] if not a.only or r["id"] in a.only.split(",")]
    if a.rebuild:
        trans = json.loads((out_dir / "transcript.json").read_text(encoding="utf-8"))
        box = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))["sandbox"]
        for r in runs:
            events = [json.loads(x) for x in (out_dir / f"{r['id']}-1.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
            trans["runs"][r["id"]].update(transcript({"box": box, "events": events}, lang=lang))
        (out_dir / "transcript.json").write_text(json.dumps(trans, ensure_ascii=False, indent=2), encoding="utf-8")
        print("rebuilt", out_dir / "transcript.json")
        return 0
    version = claude_version(env)

    if a.check:
        stored = json.loads((out_dir / "outcome.json").read_text(encoding="utf-8"))
        res = {}
        for r in runs:
            o = outcome(run_once(spec, r, env), *probe_of(r))
            res[r["id"]] = {"now": o, "stored": stored["runs"][r["id"]]["repetitions"][0],
                            "same": same([o, stored["runs"][r["id"]]["repetitions"][0]], keys)}
        (out_dir / "check.json").write_text(json.dumps({"checked_at": dt.datetime.now().isoformat(timespec="seconds"),
                                                        "claude_code": version, "runs": res}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k: v["same"] for k, v in res.items()}))
        return 0 if all(v["same"] for v in res.values()) else 1

    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"spec": spec["id"], "recorded_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "claude_code": version, "model_alias": spec.get("model", "haiku"), "language": lang, "isolation": ISOLATION,
            "sandbox": str(SANDBOX_ROOT / spec["id"]), "runs": {}}
    trans = {"spec": spec["id"], "runs": {}}
    outc = {"runs": {}}
    if (out_dir / "outcome.json").exists() and a.only:
        outc = json.loads((out_dir / "outcome.json").read_text(encoding="utf-8"))
        trans = json.loads((out_dir / "transcript.json").read_text(encoding="utf-8"))
        meta = {**json.loads((out_dir / "meta.json").read_text(encoding="utf-8")), "recorded_at": meta["recorded_at"],
                "claude_code": version}
    for r in runs:
        reps = []
        for k in range(1, a.repeat + 1):
            rec = run_once(spec, r, env)
            with (out_dir / f"{r['id']}-{k}.jsonl").open("w", encoding="utf-8") as f:
                for e in rec["events"]:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            o = outcome(rec, *probe_of(r))
            reps.append(o)
            print(r["id"], k, json.dumps(o, ensure_ascii=False), f"{rec['wall']:.1f}s", flush=True)
            if k == 1:
                tr = transcript(rec, lang=lang)
                trans["runs"][r["id"]] = {"title": r.get("title", r["id"]), "prompt": r["prompt"],
                                          "settings": r.get("settings"), "allowed_tools": r.get("allowed_tools", []),
                                          "wall": rec["wall"], **tr}
                fb = out_dir / "files" / r["id"]
                fb.mkdir(parents=True, exist_ok=True)
                (fb / "before.json").write_text(json.dumps(rec["before"], ensure_ascii=False, indent=2), encoding="utf-8")
                (fb / "after.json").write_text(json.dumps(rec["after"], ensure_ascii=False, indent=2), encoding="utf-8")
                meta["runs"][r["id"]] = {"cmd": [_redact(x, rec["box"]) for x in rec["cmd"]], "exit": rec["exit"],
                                         "stderr": _redact(rec["stderr"], rec["box"]), **tr["meta"]}
        outc["runs"][r["id"]] = {"repetitions": reps, "reproducible": same(reps, keys)}
    outc["all_reproducible"] = all(v["reproducible"] for v in outc["runs"].values())
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "transcript.json").write_text(json.dumps(trans, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "outcome.json").write_text(json.dumps(outc, ensure_ascii=False, indent=2), encoding="utf-8")
    print("reproducible:", outc["all_reproducible"])
    return 0 if outc["all_reproducible"] else 3


if __name__ == "__main__":
    sys.exit(main())
