"""Wrapper around the HyperFrames CLI (npx hyperframes) installed in node_modules."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from ..config import ROOT


class HyperFramesError(RuntimeError):
    pass


def _npx() -> str:
    return shutil.which("npx.cmd") or shutil.which("npx") or "npx"


def _run(args: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.setdefault("HYPERFRAMES_SKIP_SKILLS", "1")
    env.setdefault("CI", "1")
    return subprocess.run([_npx(), "--prefix", str(ROOT), "hyperframes", *args], cwd=str(cwd),
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, env=env, shell=False)


@dataclass
class RenderResult:
    output: Path
    seconds: float
    stdout: str
    stderr: str


def check(project_dir: Path, timeout: int = 600) -> dict:
    """Run `hyperframes check --json`; returns the parsed report (errors/warnings)."""
    proc = _run(["check", "--json", "."], project_dir, timeout)
    text = proc.stdout.strip()
    try:
        start = text.index("{")
        return json.loads(text[start:])
    except (ValueError, json.JSONDecodeError):
        return {"raw": text, "stderr": proc.stderr[-3000:], "returncode": proc.returncode}


def render(project_dir: Path, output: Path, *, quality: str = "looks", gpu: bool = True,
           workers: int | str = 4, fps: int = 30, timeout: int = 3600) -> RenderResult:
    output.parent.mkdir(parents=True, exist_ok=True)
    args = ["render", ".", "-o", str(output), "-q", quality, "-f", str(fps), "-w", str(workers), "--quiet"]
    if gpu:
        args.append("--gpu")
    t0 = time.perf_counter()
    proc = _run(args, project_dir, timeout)
    elapsed = time.perf_counter() - t0
    if proc.returncode != 0 or not output.exists():
        raise HyperFramesError(f"hyperframes render failed ({proc.returncode}):\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
    return RenderResult(output=output, seconds=elapsed, stdout=proc.stdout, stderr=proc.stderr)


def snapshot(project_dir: Path, at: list[float], out_dir: Path, timeout: int = 600) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = _run(["snapshot", ".", "--at", ",".join(f"{t:g}" for t in at), "-o", str(out_dir.resolve())], project_dir, timeout)
    if proc.returncode != 0:
        raise HyperFramesError(proc.stderr[-2000:] or proc.stdout[-2000:])
    return sorted(out_dir.glob("*.png"))
