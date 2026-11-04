"""File queue: storage/drafts -> approved -> published, failed. One folder per video_id.

Folder contents: video.mp4, cover.jpg, post.json, script.md, manifest.json, report.json, captions.json.
Moves are idempotent (a folder already in the target stage stays there). Mirror copies to OneDrive.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .config import STORAGE_DIR, mirror_dir

STAGES = ("drafts", "approved", "published", "failed")
REQUIRED_FILES = ("video.mp4", "cover.jpg", "post.json", "script.md", "manifest.json")


def stage_dir(stage: str) -> Path:
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage}")
    d = STORAGE_DIR / stage
    d.mkdir(parents=True, exist_ok=True)
    return d


def find(video_id: str) -> tuple[str, Path] | None:
    for s in STAGES:
        d = STORAGE_DIR / s / video_id
        if d.exists():
            return s, d
    return None


def video_dir(video_id: str, stage: str = "drafts") -> Path:
    d = stage_dir(stage) / video_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def is_complete(folder: Path) -> list[str]:
    return [f for f in REQUIRED_FILES if not (folder / f).exists()]


def move(video_id: str, to_stage: str) -> Path:
    found = find(video_id)
    if not found:
        raise FileNotFoundError(video_id)
    cur, src = found
    if cur == to_stage:
        return src
    dst = stage_dir(to_stage) / video_id
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    return dst


def mirror(video_id: str, *, subfolder: str | None = None) -> Path | None:
    """Copy the video folder to OneDrive\\Business\\05 Produktion\\<subfolder or stage>\\<video_id>."""
    found = find(video_id)
    if not found:
        return None
    stage, src = found
    target = mirror_dir() / (subfolder or f"_{stage}") / video_id
    target.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, target / f.name)
    return target


def list_stage(stage: str) -> list[str]:
    return sorted(p.name for p in stage_dir(stage).iterdir() if p.is_dir())
