"""Night run for the Scutoria long videos (rules of the main session, 02.11.2026):
- voices and word timings first, outside the render lock;
- every chapter and every reel is its own job in scripts/render_queue.py, so other brands get their turn in between;
- the chapters are joined with ffmpeg afterwards, without the lock.
Log: storage/longform/night_run.log.

  .venv\\Scripts\\python.exe brands\\ai_security\\longform\\night_run.py 01-ai-rules-start.de 02-security-questionnaire.de ...
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
LOG = ROOT / "storage" / "longform" / "night_run.log"
RL = str(HERE / "render_long.py")


def log(msg: str) -> None:
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")


def run(args: list[str]) -> int:
    log("$ " + " ".join(args))
    with LOG.open("a", encoding="utf-8") as f:
        p = subprocess.run(args, cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT)
    log(f"exit {p.returncode}")
    return p.returncode


def queued(extra: list[str]) -> int:
    return run([PY, "scripts/render_queue.py", "ai_security", "--", RL, *extra])


def main() -> int:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:]
    for n in names:                                     # voices, no lock
        run([PY, RL, str(HERE / "plans" / f"{n}.json"), "--tts", "gemini", "--no-render"])
    for n in names:
        plan_path = HERE / "plans" / f"{n}.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        t0 = time.time()
        for ch in plan["chapters"]:
            queued([str(plan_path), "--tts", "gemini", "--chapters", ch["id"], "--no-concat", "--overlap"])
        run([PY, RL, str(plan_path), "--tts", "gemini", "--concat"])
        for r in plan.get("reels", []):
            queued([str(plan_path), "--tts", "gemini", "--reels", r["id"], "--overlap"])
        log(f"== {n}: {time.time() - t0:.0f} s incl. queue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
