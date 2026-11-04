"""Script files: Markdown with YAML front matter, scenes with source ids, UNVERIFIED guard.

Format (data/scripts/<video_id>.md):

---
topic_id: ai_security-20261105-1
brand_id: ai_security
language: de
title: ...
risk_level: medium
sources:
  - id: S1
    url: https://...
    title: ...
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Spoken text ... [S1]
> visual: headline="..." number="..." body="..."

Every scene has spoken text; facts carry `[S1]` markers; a claim without a source is written as
`UNVERIFIED: ...` and blocks production (status NEEDS_RESEARCH).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

SCENE_RE = re.compile(r"^##\s*Scene\s+(\d+)\s*(?:\(([^)]*)\))?\s*$", re.IGNORECASE)
VISUAL_RE = re.compile(r"^>\s*visual:\s*(.*)$")
SRC_REF_RE = re.compile(r"\[(S\d+)\]")
KV_RE = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"')
UNVERIFIED_RE = re.compile(r"\bUNVERIFIED\b")


@dataclass
class ScriptScene:
    index: int
    kind: str
    text: str
    visual: dict[str, str] = field(default_factory=dict)
    source_ids: list[str] = field(default_factory=list)

    @property
    def spoken(self) -> str:
        """Text for TTS: source markers removed."""
        return SRC_REF_RE.sub("", self.text).replace("  ", " ").strip()


@dataclass
class Script:
    meta: dict
    scenes: list[ScriptScene]

    @property
    def language(self) -> str:
        return self.meta.get("language", "de")

    @property
    def brand_id(self) -> str:
        return self.meta["brand_id"]

    @property
    def topic_id(self) -> str:
        return self.meta["topic_id"]

    @property
    def sources(self) -> list[dict]:
        return list(self.meta.get("sources", []))

    @property
    def spoken_text(self) -> str:
        return " ".join(s.spoken for s in self.scenes)

    @property
    def word_count(self) -> int:
        return len(self.spoken_text.split())


def parse(text: str) -> Script:
    if not text.startswith("---"):
        raise ValueError("script needs YAML front matter")
    _, fm, body = text.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    for src in meta.get("sources", []) or []:
        for k, v in list(src.items()):
            if hasattr(v, "isoformat"):
                src[k] = v.isoformat()
    scenes: list[ScriptScene] = []
    cur: ScriptScene | None = None
    lines: list[str] = []

    def flush():
        if cur is not None:
            cur.text = " ".join(l.strip() for l in lines if l.strip())
            cur.source_ids = sorted(set(SRC_REF_RE.findall(cur.text)))
            scenes.append(cur)

    for raw in body.splitlines():
        m = SCENE_RE.match(raw.strip())
        if m:
            flush()
            cur = ScriptScene(index=int(m.group(1)), kind=(m.group(2) or "card").strip().lower(), text="")
            lines = []
            continue
        if cur is None:
            continue
        v = VISUAL_RE.match(raw.strip())
        if v:
            cur.visual = {k: val.replace('\\"', '"') for k, val in KV_RE.findall(v.group(1))}
            continue
        lines.append(raw)
    flush()
    return Script(meta=meta, scenes=scenes)


def load(path: Path) -> Script:
    return parse(path.read_text(encoding="utf-8"))


def check(script: Script, *, min_words: int = 150, max_words: int = 240) -> list[str]:
    """Problems that block production (empty list = ok)."""
    problems: list[str] = []
    for key in ("topic_id", "brand_id", "language", "title"):
        if not script.meta.get(key):
            problems.append(f"front matter missing {key}")
    if script.meta.get("risk_level") not in ("low", "medium", "high"):
        problems.append("risk_level must be low|medium|high")
    src_ids = {s.get("id") for s in script.sources}
    for s in script.sources:
        for key in ("id", "url", "checked_at"):
            if not s.get(key):
                problems.append(f"source {s.get('id', '?')} missing {key}")
    if not script.scenes:
        problems.append("no scenes")
    full = "\n".join(s.text for s in script.scenes)
    if UNVERIFIED_RE.search(full):
        problems.append("UNVERIFIED marker present -> NEEDS_RESEARCH")
    for s in script.scenes:
        for ref in s.source_ids:
            if ref not in src_ids:
                problems.append(f"scene {s.index} references unknown source {ref}")
    body_scenes = [s for s in script.scenes if s.kind not in ("hook", "outro", "payoff", "advice")]
    for s in body_scenes:
        if not s.source_ids:
            problems.append(f"scene {s.index} ({s.kind}) has no source marker")
    wc = script.word_count
    if wc < min_words or wc > max_words:
        problems.append(f"word count {wc} outside {min_words}-{max_words}")
    return problems


def estimate_seconds(script: Script, words_per_second: float) -> float:
    return script.word_count / words_per_second
