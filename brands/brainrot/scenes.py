"""Zonkfruit (brainrot) scene module for the shared renderer (fn.render.brand_scenes, docs/direction-system.md 6d).

The scene types live in renderer/zonk_templates.py (Plümo from renderer/plumo.py); this file only exposes them.
Types apply to this brand only. The hook beat uses zonk_scan (mode "hook"). Sound effects are emitted by the
scenes themselves; LAYER copies the files (own work, assets/sfx/LICENSE.md) into the project.
"""
from __future__ import annotations

import sys
from pathlib import Path

_RENDERER = Path(__file__).resolve().parent / "renderer"
if str(_RENDERER) not in sys.path:
    sys.path.insert(0, str(_RENDERER))

import zonk_templates as zt  # noqa: E402

TEMPLATES = dict(zt.ZONK_TEMPLATES)
HOOK_SCENE_TYPES = ["zonk_scan"]


def CSS(pal, display, display_w, body, mono, zone_top, zone_h, flat):  # noqa: N802 (contract name)
    return zt.zonk_css(display, body)


def LAYER(plan, brand, project_dir, captions):  # noqa: N802
    # runs before the scenes are built: the video length is the period of the backdrop motion (seamless loop)
    zt.TOTAL[0] = max((float(b.start) + float(b.duration) for b in plan.beats
                       if b.start is not None and b.duration is not None), default=0.0)
    zt.copy_sfx(Path(project_dir) / "assets")
    return {}


def MANIFEST_EXTRA(plan):  # noqa: N802
    names = sorted({c[1] for c in zt.SFX})
    return {
        "character": {"name": "Plümo", "sheet": "brands/brainrot/assets/character/plumo_sheet.png",
                      "generator": "brands/brainrot/renderer/plumo.py", "status": "draft, not approved by Stefan"},
        "brand_sfx": {"cues": len(zt.SFX), "files": [f"{n}.wav" for n in names],
                      "license": "own work, synthesised with brands/brainrot/renderer/sfx.py, no third-party rights",
                      "proof": "brands/brainrot/assets/sfx/LICENSE.md"},
    }
