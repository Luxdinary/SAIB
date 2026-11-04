"""Fair render queue (first come, first served) around the shared render lock `data/render.lock`.

Why: with plain polling on data/render.lock the fastest poller always wins; Gigastruct waited 80 minutes without
getting the lock once (01.11.2026). Every render now goes through this wrapper:

    .venv\\Scripts\\python.exe scripts\\render_queue.py <brand_id> -- <script.py> <args...>
    e.g. ... render_queue.py engines -- scripts\\render_direction.py data\\direction\\engines-20261109-1-de.json --version V1 --tts gemini

How it works:
- The wrapper writes a ticket `data/render_queue/<ns-timestamp>_<brand>.ticket` and keeps it fresh (heartbeat 5 s).
  Tickets older than 60 s without heartbeat belong to dead processes and are removed.
- Only the oldest ticket may take the lock, and only when `data/render.lock` is free (absent, or older than
  20 minutes without heartbeat). The wrapper then holds the lock, refreshes it every 30 s while the command runs,
  and removes it afterwards. Exit code = exit code of the command.
- Do NOT take data/render.lock yourself anymore and do not wrap a script that takes it itself
  (Zonkfruit: call scripts\\render_direction.py directly; the brand scenes load automatically).
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data" / "render.lock"
QUEUE = ROOT / "data" / "render_queue"
LOCK_STALE_S = 20 * 60
TICKET_STALE_S = 60


def _touch_loop(path: Path, stop: threading.Event, every: float) -> None:
    while not stop.wait(every):
        try:
            os.utime(path, None)
        except FileNotFoundError:
            return


def _clean_tickets() -> list[Path]:
    now = time.time()
    alive = []
    for t in QUEUE.glob("*.ticket"):
        try:
            if now - t.stat().st_mtime > TICKET_STALE_S:
                t.unlink(missing_ok=True)
            else:
                alive.append(t)
        except FileNotFoundError:
            pass
    return sorted(alive, key=lambda p: p.name)


def _lock_free() -> bool:
    if (ROOT / "data" / "render.pause").exists():     # Stefan: pause all renders (01.11.2026); remove the file to resume
        return False
    try:
        return time.time() - LOCK.stat().st_mtime > LOCK_STALE_S
    except FileNotFoundError:
        return True


def main() -> int:
    if "--" not in sys.argv or sys.argv.index("--") != 2:
        print(__doc__)
        return 2
    brand = sys.argv[1]
    cmd = [sys.executable, *sys.argv[3:]]
    QUEUE.mkdir(parents=True, exist_ok=True)
    ticket = QUEUE / f"{time.time_ns()}_{brand}.ticket"
    ticket.write_text(" ".join(sys.argv[3:]), encoding="utf-8")
    stop_t = threading.Event()
    threading.Thread(target=_touch_loop, args=(ticket, stop_t, 5.0), daemon=True).start()
    last_report = 0.0
    try:
        while True:
            tickets = _clean_tickets()
            if tickets and tickets[0] == ticket and _lock_free():
                LOCK.unlink(missing_ok=True)              # stale or absent
                try:
                    with open(LOCK, "x", encoding="utf-8") as fh:
                        fh.write(f"{brand} {datetime.now().isoformat(timespec='seconds')} (render_queue)\n")
                    break
                except FileExistsError:
                    pass
            if time.time() - last_report > 60:
                pos = tickets.index(ticket) + 1 if ticket in tickets else "?"
                print(f"[render_queue] {brand}: waiting, position {pos} of {len(tickets)}", flush=True)
                last_report = time.time()
            time.sleep(2)
    finally:
        stop_t.set()
        ticket.unlink(missing_ok=True)
    stop_l = threading.Event()
    threading.Thread(target=_touch_loop, args=(LOCK, stop_l, 30.0), daemon=True).start()
    print(f"[render_queue] {brand}: lock taken, running {' '.join(sys.argv[3:])}", flush=True)
    try:
        return subprocess.run(cmd, cwd=ROOT).returncode
    finally:
        stop_l.set()
        try:
            if LOCK.read_text(encoding="utf-8").startswith(f"{brand} "):
                LOCK.unlink()
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    sys.exit(main())
