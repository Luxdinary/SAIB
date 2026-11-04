"""Story engine: Hook -> Problem -> Explanation -> Demonstration -> Insight -> Benefit -> Close.

A `DirectionPlan` lists beats in story order. Every beat has a function (one of BEATS), a scene
type (one of SCENE_TYPES, the reusable HyperFrames templates in fn.render.templates), the spoken
text, the data the template renders, and the source ids backing any claim. Timing (`start`,
`duration`) is filled in from the word timings at render time; authored plans may carry a
`duration_hint` only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from ..config import DATA_DIR

BEATS = ["hook", "problem", "explanation", "demonstration", "insight", "benefit", "close"]
SCENE_TYPES = ["cinematic_hook", "ui_demo", "data_flow", "comparison", "key_takeaway", "file_fork", "file_beside", "file_close"]
CLAIM_FUNCTIONS = {"problem", "explanation", "demonstration", "insight"}   # need a source id
MIN_DISTINCT_TYPES = 2          # hard rule from the analysis: at least two representation forms
TARGET_DISTINCT_TYPES = 3
MAX_BEAT_SECONDS = 16.0         # longer than this without an internal visual event = static slide


@dataclass
class Beat:
    id: str
    function: str
    scene_type: str
    spoken: str
    data: dict = field(default_factory=dict)
    source_ids: list[str] = field(default_factory=list)
    duration_hint: float | None = None
    start: float | None = None
    duration: float | None = None
    notes: str = ""
    overlay: dict = field(default_factory=dict)   # explainer layer per beat, see fn.render.explainer

    @property
    def end(self) -> float | None:
        return None if self.start is None or self.duration is None else self.start + self.duration


@dataclass
class DirectionPlan:
    video_id: str
    brand_id: str
    language: str
    title: str
    beats: list[Beat]
    hook: dict = field(default_factory=dict)          # chosen hook candidate (hooks.HookCandidate.to_dict)
    hook_candidates: list[dict] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)
    unverified: list[str] = field(default_factory=list)   # claims that were NOT used because unverified
    layout: dict = field(default_factory=dict)        # optional overrides (caption_bottom_px, scene_top ...)
    assets: dict = field(default_factory=dict)        # Fassung B: background/hero clips, see fn.render.assets
    notes: str = ""

    @property
    def spoken_text(self) -> str:
        return " ".join(b.spoken.strip() for b in self.beats if b.spoken.strip())

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def from_dict(d: dict) -> DirectionPlan:
    beats = [Beat(**{k: v for k, v in b.items() if k in Beat.__dataclass_fields__}) for b in d.get("beats", [])]
    return DirectionPlan(video_id=d["video_id"], brand_id=d["brand_id"], language=d.get("language", "de"),
                         title=d.get("title", ""), beats=beats, hook=dict(d.get("hook", {})),
                         hook_candidates=list(d.get("hook_candidates", [])), sources=list(d.get("sources", [])),
                         unverified=list(d.get("unverified", [])), layout=dict(d.get("layout", {})),
                         assets=dict(d.get("assets", {})), notes=d.get("notes", ""))


def plan_path(video_id: str) -> Path:
    return DATA_DIR / "direction" / f"{video_id}.json"


def load_plan(path: Path) -> DirectionPlan:
    return from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def save_plan(plan: DirectionPlan, path: Path | None = None) -> Path:
    path = path or plan_path(plan.video_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def validate(plan: DirectionPlan, *, partial: bool = False) -> list[str]:
    """Hard problems only (a plan with problems must not be rendered). Soft advice: `advice()`.

    `partial=True` (prototypes) skips the rules that need a complete story (close beat, distinct types).
    """
    p: list[str] = []
    if not plan.beats:
        return ["plan has no beats"]
    allowed, hook_types = _brand_types(plan.brand_id)
    known = {s["id"] for s in plan.sources}
    order = [BEATS.index(b.function) if b.function in BEATS else -1 for b in plan.beats]
    for b, o in zip(plan.beats, order):
        if o < 0:
            p.append(f"{b.id}: unknown function {b.function!r}")
        if b.scene_type not in allowed:
            p.append(f"{b.id}: unknown scene_type {b.scene_type!r}")
        if not b.spoken.strip():
            p.append(f"{b.id}: no spoken text")
        if b.function in CLAIM_FUNCTIONS and not b.source_ids:
            p.append(f"{b.id}: function {b.function} makes a claim and needs source ids")
        for s in b.source_ids:
            if s not in known:
                p.append(f"{b.id}: source {s} not in plan.sources")
        if "UNVERIFIED" in b.spoken or "UNVERIFIED" in json.dumps(b.data, ensure_ascii=False):
            p.append(f"{b.id}: UNVERIFIED marker inside the plan blocks rendering")
    if plan.beats[0].function != "hook":
        p.append("first beat must be the hook")
    if plan.beats[-1].function != "close" and not partial:
        p.append("last beat must be the close")
    if any(b > a for a, b in zip(order, order[1:]) if a >= 0 and b >= 0) and sorted(order) != order:
        p.append("beats must follow the story order hook -> problem -> explanation -> demonstration -> insight -> benefit -> close")
    if plan.beats[0].scene_type not in hook_types:
        p.append(f"the hook beat must use one of the hook scene types {hook_types}")
    distinct = {b.scene_type for b in plan.beats}
    if len(distinct) < MIN_DISTINCT_TYPES and not partial:
        p.append(f"only {len(distinct)} scene type(s); at least {MIN_DISTINCT_TYPES} representation forms are required")
    for s in plan.sources:
        if not (s.get("id") and s.get("url") and s.get("checked_at")):
            p.append(f"source {s.get('id')} needs id, url and checked_at")
    ids = [b.id for b in plan.beats]
    if len(set(ids)) != len(ids):
        p.append("duplicate beat ids")
    return p


def _brand_types(brand_id: str) -> tuple[list[str], list[str]]:
    """Allowed scene types and hook scene types: shared ones plus `brands/<id>/scenes.py` (fn.render.brand_scenes)."""
    try:
        from ..render import brand_scenes
        bs = brand_scenes.load(brand_id)
        return SCENE_TYPES + [t for t in bs.templates if t not in SCENE_TYPES], bs.hook_types
    except (ImportError, OSError):
        return list(SCENE_TYPES), ["cinematic_hook"]


def advice(plan: DirectionPlan) -> list[str]:
    """Soft findings: things a human should look at, not blockers."""
    a: list[str] = []
    distinct = {b.scene_type for b in plan.beats}
    if len(distinct) < TARGET_DISTINCT_TYPES:
        a.append(f"{len(distinct)} scene types used; {TARGET_DISTINCT_TYPES} or more look less like a slide deck")
    for x, y in zip(plan.beats, plan.beats[1:]):
        if x.scene_type == y.scene_type and not (x.data.get("mode") != y.data.get("mode")):
            a.append(f"{x.id} and {y.id} use the same scene type back to back")
    for b in plan.beats:
        d = b.duration if b.duration is not None else b.duration_hint
        if d and d > MAX_BEAT_SECONDS and not b.data.get("events"):
            a.append(f"{b.id}: {d:.0f} s without an internal visual event")
    for f in ("demonstration", "benefit"):
        if not any(b.function == f for b in plan.beats):
            a.append(f"no {f} beat")
    return a
