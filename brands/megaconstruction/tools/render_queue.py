"""Gigastruct render queue (Woche 1): renders plans one after another under data/render.lock, checks and exports them.

Reads topic ids from brands/megaconstruction/tools/queue.txt (one per line, processed in order; new lines may be added
while it runs; a line STOP ends the queue once everything before it is done). State per id in queue_state.json:
rendered / length / failed / exported, with the report status, length and overlap result.

Per id: wait for the lock (free when missing or older than 20 min), take it, render V1 with Gemini
(render_gigastruct.py), release the lock at once, then overlap_check.mjs and, when VALIDATED (or HUMAN_REVIEW for risk
high), length 65-90 s and no overlap, export_production_folder.py with the short title from shorts.json.
Gemini errors (429 and others): wait 15 minutes and try again, at most 4 times; then mark failed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = Path(__file__).resolve().parent
QUEUE, STATE, SHORTS = TOOLS / "queue.txt", TOOLS / "queue_state.json", TOOLS / "shorts.json"
LOCK = ROOT / "data" / "render.lock"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
LOG = TOOLS / "queue.log"


def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(st: dict) -> None:
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def take_lock(tag: str) -> None:
    while True:
        if not LOCK.exists() or time.time() - LOCK.stat().st_mtime > 1200:
            LOCK.write_text(f"megaconstruction {tag} {datetime.now().astimezone().isoformat(timespec='seconds')}\n", encoding="utf-8")
            time.sleep(2)
            if LOCK.read_text(encoding="utf-8").startswith(f"megaconstruction {tag}"):
                return
        time.sleep(1)


def free_lock(tag: str) -> None:
    try:
        if LOCK.read_text(encoding="utf-8").startswith(f"megaconstruction {tag}"):
            LOCK.unlink()
    except FileNotFoundError:
        pass


def process(tid: str, version: str, st: dict) -> None:
    plan = ROOT / "data" / "direction" / f"{tid}.json"
    out = ROOT / "storage" / "direction" / f"{tid}-{version}"
    for attempt in range(5):
        # a Gemini recording of this version that was already paid for (e.g. before an interruption) is reused if the text matches
        voice = ROOT / "storage" / "direction" / f"voice_{tid}_{version}_gemini.wav"
        spoken = " ".join(b["spoken"].strip() for b in json.loads(plan.read_text(encoding="utf-8"))["beats"] if b["spoken"].strip())
        side = voice.with_suffix(".json")
        reuse = voice.exists() and side.exists() and json.loads(side.read_text(encoding="utf-8")).get("spoken_text", "").strip() == spoken.strip()
        tts = ["--reuse-voice", str(voice)] if reuse else ["--tts", "gemini"]
        take_lock(tid)
        log(f"{tid} {version}: render (attempt {attempt + 1}{', reused voice' if reuse else ''})")
        try:
            r = subprocess.run([PY, str(TOOLS.parent / "render" / "render_gigastruct.py"), str(plan), "--version", version, *tts,
                                "--mirror", f"gigastruct/woche1/{tid}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        finally:
            free_lock(tid)
        tail = (r.stdout + r.stderr)[-1500:]
        if r.returncode == 0:
            break
        if r.returncode == 5:   # length outside 65-90 s (voice already paid and kept)
            st[tid] = {"status": "length", "version": version, "detail": tail[-300:]}
            log(f"{tid}: length outside 65-90 s -> text must be adjusted")
            return
        log(f"{tid}: render failed rc={r.returncode}: {tail[-400:]}")
        if not any(k in tail for k in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "quota", "Quota", "timed out", "Timeout")):
            st[tid] = {"status": "failed", "version": version, "detail": tail[-500:]}
            return   # a plan or render error: no point in waiting
        if attempt < 4:
            time.sleep(900)
    else:
        st[tid] = {"status": "failed", "version": version, "detail": tail[-500:]}
        return
    rep = json.loads((out / "report.json").read_text(encoding="utf-8"))
    status = "VALIDATED" if rep.get("passed") and not rep.get("needs_review") else ("HUMAN_REVIEW" if rep.get("passed") else "FAILED")
    dur = rep["probe"]["duration"]
    ov = subprocess.run(["node", "scripts/overlap_check.mjs", str(out / "project")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    overlaps = json.loads(ov.stdout.strip().splitlines()[-1]).get("overlaps", []) if ov.stdout.strip() else ["no output"]
    entry = {"status": status, "version": version, "duration": dur, "overlaps": overlaps,
             "warnings": [f["id"] for f in rep["findings"] if not f["ok"]]}
    if status in ("VALIDATED", "HUMAN_REVIEW") and 65 <= dur <= 90 and not overlaps:
        short = json.loads(SHORTS.read_text(encoding="utf-8"))[tid]
        ex = subprocess.run([PY, "scripts/export_production_folder.py", str(plan), "--version", version, "--short", short, "--force"],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        entry["exported"] = ex.returncode == 0
        entry["export_log"] = (ex.stdout + ex.stderr)[-300:]
    else:
        entry["exported"] = False
    st[tid] = entry
    log(f"{tid}: {status} {dur:.1f} s, overlaps {len(overlaps)}, exported {entry['exported']}")


def main() -> int:
    log("queue started")
    st = state()
    for k in [k for k, v in st.items() if v.get("status") == "running"]:   # interrupted run: do it again
        del st[k]
    save(st)
    while True:
        ids = [l.strip() for l in QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()] if QUEUE.exists() else []
        st = state()
        todo = None
        for line in ids:
            if line == "STOP":
                break
            tid, _, version = line.partition(" ")
            if tid not in st or (st[tid].get("version") != (version or "V1") and st[tid].get("status") in ("length", "failed", "FAILED")):
                todo = (tid, version or "V1")
                break
        if todo is None:
            if "STOP" in ids:
                log("queue finished")
                return 0
            time.sleep(30)
            continue
        st[todo[0]] = {"status": "running", "version": todo[1]}
        save(st)
        process(todo[0], todo[1], st)
        save(st)


if __name__ == "__main__":
    sys.exit(main())
