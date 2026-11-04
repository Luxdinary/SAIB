"""Two frame formats built from the same scenes: 16:9 long video (1920x1080) and 9:16 reel (1080x1920).

All positions in px. Content box = the area a scene may use; head, marker, source bar and captions sit outside it.
16:9 follows Stefan's original long-video template (head top left, voice tag top right, marker and source bar at the
bottom, side margin 96 px). 9:16 follows the format bible zones (content y 290-1100, nothing below y 1620).
"""
from __future__ import annotations

FORMATS: dict[str, dict] = {
    "16x9": {
        "name": "16x9", "W": 1920, "H": 1080, "X0": 96,
        "top": 196, "bottom": 880,                 # content box
        "kicker_y": 52, "title_y": 84, "title_px": 48, "kicker_px": 24,
        "tag_y": 56, "tag_px": 18,
        "marker_y": 900, "source_y": 958, "source_px": 22, "source_w": 1728,
        "opening_y": 958,
        "captions": False, "cap_bottom": 0, "cap_px": 0, "cap_w": 0,
        "scale": 1.3, "dir": "row",
    },
    "9x16": {
        "name": "9x16", "W": 1080, "H": 1920, "X0": 96,
        "top": 300, "bottom": 1060,
        "kicker_y": 196, "title_y": 0, "title_px": 0, "kicker_px": 26,
        "tag_y": 120, "tag_px": 20,
        "marker_y": 1080, "source_y": 1134, "source_px": 24, "source_w": 888,
        "opening_y": 1134,
        "captions": True, "cap_bottom": 440, "cap_px": 56, "cap_w": 820,
        "scale": 1.18, "dir": "col",
    },
}


def get(name: str) -> dict:
    if name not in FORMATS:
        raise ValueError(f"unknown format {name}; use 16x9 or 9x16")
    return dict(FORMATS[name])
