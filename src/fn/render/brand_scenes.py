"""Brand-specific scene types, loaded from an optional brand module.

The module is `brands/<id>/scenes.py`, or the path in `scenes:` of `brands/<id>/brand.yaml` (relative to the
repository root). Contract (all names optional except TEMPLATES):

    TEMPLATES: dict[str, Callable[[SceneCtx, dict], SceneOut]]   # new scene types, or brand variants of shared ones
    LIMITS: dict[str, dict[str, int]]                             # text limits per brand scene type
    HOOK_SCENE_TYPES: list[str]                                   # scene types allowed for the hook beat
    def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat) -> str   # also accepted as `scene_css`,
                                                                  # with the first N of these arguments
    def LAYER(plan, brand, project_dir, captions) -> dict         # brand-wide layer, see layer_for()
    def MANIFEST_EXTRA(plan) -> dict                              # extra manifest fields, see manifest_extra()

A brand may override a shared name (e.g. its own `cinematic_hook`); the override applies to that brand only,
because lookups go through `template_for(brand_id, ...)` and never mutate fn.render.templates.TEMPLATES.
`hook_scene_types` in brand.yaml overrides HOOK_SCENE_TYPES; the default is ["cinematic_hook"].
"""
from __future__ import annotations

import importlib.util
import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from ..config import BRANDS_DIR, ROOT, read_yaml
from . import templates as shared

DEFAULT_HOOK_TYPES = ["cinematic_hook"]


@dataclass
class BrandScenes:
    brand_id: str
    templates: dict[str, Callable] = field(default_factory=dict)
    limits: dict[str, dict[str, int]] = field(default_factory=dict)
    hook_types: list[str] = field(default_factory=lambda: list(DEFAULT_HOOK_TYPES))
    css: Callable | None = None
    layer: Callable | None = None            # LAYER(plan, brand, project_dir, captions) -> dict
    manifest_extra: Callable | None = None   # MANIFEST_EXTRA(plan) -> dict
    source: Path | None = None


_cache: dict[str, BrandScenes] = {}


def _module_path(brand_id: str, design: dict) -> Path | None:
    if design.get("scenes"):
        p = Path(design["scenes"])
        return p if p.is_absolute() else ROOT / p
    p = BRANDS_DIR / brand_id / "scenes.py"
    return p if p.exists() else None


def load(brand_id: str) -> BrandScenes:
    if brand_id in _cache:
        return _cache[brand_id]
    bs = BrandScenes(brand_id)
    design_file = BRANDS_DIR / brand_id / "brand.yaml"
    design = (read_yaml(design_file) or {}) if design_file.exists() else {}
    path = _module_path(brand_id, design)
    if path is not None:
        if not path.exists():
            raise FileNotFoundError(f"scene module of brand {brand_id} not found: {path}")
        spec = importlib.util.spec_from_file_location(f"fn_brand_scenes_{brand_id}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        bs.source = path
        bs.templates = dict(getattr(mod, "TEMPLATES", {}))
        bs.limits = dict(getattr(mod, "LIMITS", {}))
        bs.hook_types = list(getattr(mod, "HOOK_SCENE_TYPES", DEFAULT_HOOK_TYPES))
        bs.css = getattr(mod, "CSS", None) or getattr(mod, "scene_css", None)
        bs.layer = getattr(mod, "LAYER", None)
        bs.manifest_extra = getattr(mod, "MANIFEST_EXTRA", None)
    if design.get("hook_scene_types"):
        bs.hook_types = list(design["hook_scene_types"])
    _cache[brand_id] = bs
    return bs


def scene_types(brand_id: str) -> list[str]:
    own = load(brand_id).templates
    return list(shared.TEMPLATES) + [t for t in own if t not in shared.TEMPLATES]


def template_for(brand_id: str, scene_type: str) -> Callable | None:
    return load(brand_id).templates.get(scene_type) or shared.TEMPLATES.get(scene_type)


def text_limits(brand_id: str, scene_type: str, data: dict) -> list[str]:
    """Brand limits (flat check of string fields) where the brand defines them, shared limits otherwise."""
    lim = load(brand_id).limits.get(scene_type)
    if lim is None:
        return shared.text_limits(scene_type, data)
    return [f"{scene_type}.{k}: {len(str(data[k]))} chars > {n}" for k, n in lim.items()
            if isinstance(data.get(k), str) and len(data[k]) > n]


LAYER_KEYS = ("head_html", "under_scenes_html", "body_end_html", "events", "problems")


def layer_for(brand_id: str, plan, brand, project_dir: Path, captions) -> dict:
    """Brand-wide layer (e.g. one WebGL canvas under all scenes). The module copies its own files into
    project_dir/assets. Returns head_html, under_scenes_html, body_end_html, events, problems (all optional)."""
    fn = load(brand_id).layer
    if not fn:
        return {}
    out = fn(plan, brand, project_dir, captions) or {}
    unknown = set(out) - set(LAYER_KEYS)
    if unknown:
        raise ValueError(f"LAYER of brand {brand_id} returned unknown keys {sorted(unknown)}")
    return out


def manifest_extra(brand_id: str, plan) -> dict:
    """Extra manifest fields of the brand (e.g. calculation trail); may not overwrite pipeline keys."""
    fn = load(brand_id).manifest_extra
    return dict(fn(plan) or {}) if fn else {}


def css_for(brand_id: str, *args) -> str:
    """Call the brand CSS function with as many of (pal, display, display_w, body, mono, zone_top, zone_h, flat) as it takes."""
    fn = load(brand_id).css
    if not fn:
        return ""
    params = inspect.signature(fn).parameters.values()
    if any(p.kind is p.VAR_POSITIONAL for p in params):
        return fn(*args)
    n = sum(1 for p in params if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
    return fn(*args[:n])
