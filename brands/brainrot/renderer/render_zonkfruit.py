"""Zonkfruit render starter: renders go through the shared fair queue scripts/render_queue.py (since 01.11.2026),
which holds data/render.lock only for the render itself; this starter never takes the lock on its own.

The Zonkfruit scene types come from brands/brainrot/scenes.py (loaded by the shared renderer itself); all arguments
are passed through to the unchanged scripts/render_direction.py, e.g.

  .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\render_zonkfruit.py data\\direction\\brainrot-20261109-1-de.json --version V1 --tts gemini --mirror zonkfruit/brainrot-20261109-1-de-V1
  (with --no-render, i.e. a dry run, no queue and no lock)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    argv = sys.argv[1:]
    render = [str(ROOT / "scripts" / "render_direction.py"), *argv]
    if "--no-render" in argv:
        return subprocess.call([sys.executable, "-u", *render], cwd=str(ROOT))
    return subprocess.call([sys.executable, "-u", str(ROOT / "scripts" / "render_queue.py"), "brainrot", "--", "-u", *render], cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(main())
