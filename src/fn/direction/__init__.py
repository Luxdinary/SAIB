"""Direction system (Regie): hook engine, story engine, scene templates and direction checks.

Feature-flagged add-on next to the Phase-1 pipeline: nothing here is imported by `fn.pipeline.produce`.
A video is described by a `DirectionPlan` (data/direction/<video_id>.json) whose beats map to the
five reusable scene templates in `fn.render.templates` and are rendered by `fn.render.director`.
"""
from .hooks import HOOK_TYPES, CRITERIA, HookCandidate, rank, validate_set  # noqa: F401
from .story import BEATS, SCENE_TYPES, Beat, DirectionPlan, load_plan, save_plan, validate  # noqa: F401
