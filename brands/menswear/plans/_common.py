"""Shared parts of the Suitwerk plan generators (Woche 1 ab 09.11.2026).

Each topic has one generator `brands/menswear/plans/<topic>.py` that builds the German and the English plan from
the same scene data and writes `data/direction/<topic_id>-<de|en>.json`. Run: `.venv\\Scripts\\python.exe
brands\\menswear\\plans\\<datei>.py`. Layout and closing follow the approved test video Q1 (Unterer Sakkoknopf).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "direction"
RESEARCH = ROOT / "data" / "calendars" / "menswear_2026-11.research.json"

LAYOUT = {
    "zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
    "status_y": 1440, "outro": False, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
    "caption_mode": "phrases", "caption_max_words": 4,
}
COMPANION = {"de": "Folge Suitwerk für Herrenstil mit Blick fürs Detail. Keine Werbung, keine Produktempfehlung.",
             "en": "Follow Suitwerk for menswear with an eye for detail. No ads, no product recommendations."}
CHIP = {"de": "Suitwerk · Blick fürs Detail", "en": "Suitwerk · An eye for detail"}


def research(key: str) -> dict:
    return next(t for t in json.loads(RESEARCH.read_text(encoding="utf-8")) if t["key"] == key)


def words(text: str) -> int:
    return len(text.split())


def build(topic_id: str, lang: str, *, title: str, notes: str, sources: list[dict], hooks: list[dict], hook_note: str,
          beats: list[dict], status_file: str, states: list[dict], description: str, hashtags: list[str],
          unverified: list[str] | None = None) -> dict:
    """One plan. `beats[i]` = {id, function, scene_type, spoken, data, source_ids, overlay}; `states` as in
    layout.status_bar.states (offset in seconds after the beat start, default 0.3)."""
    layout = copy.deepcopy(LAYOUT)
    layout["status_bar"] = {"file": status_file, "states": states}
    layout.update({"description": description, "companion_text": COMPANION[lang], "hashtags": hashtags})
    plan = {
        "video_id": f"{topic_id}-{lang}", "brand_id": "menswear", "language": lang, "title": title, "notes": notes,
        "layout": layout, "sources": sources, "unverified": unverified or [], "hook_candidates": hooks,
        "hook": {"id": hooks[0]["id"], "note": hook_note}, "beats": beats,
    }
    return plan


def write(plan: dict) -> Path:
    p = OUT / f"{plan['video_id']}.json"
    p.write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(words(b["spoken"]) for b in plan["beats"])
    print(f"{p.name}: {n} words, {len(plan['beats'])} beats")
    return p


def hook(hid: str, htype: str, spoken: str, on_screen: str, source_ids: list[str], visual: str, scores: dict | None = None) -> dict:
    return {"id": hid, "type": htype, "spoken": spoken, "on_screen": on_screen,
            "scores": scores or {"clarity": 4, "relevance": 4, "curiosity": 4, "truth": 5, "visual": 4},
            "source_ids": source_ids, "visual": visual, "why": {}}


def closing_beat(lang: str, spoken: str, frm: dict, to: dict, target: str, statement: str, *, fix_at: str, ring_at: str,
                 statement_at: str, chip_at: str, iris: tuple[int, int] = (206, 1036)) -> dict:
    return {"id": "b7", "function": "close", "scene_type": "suitwerk_takeaway", "duration_hint": 6, "spoken": spoken,
            "data": {"mode": "closing", "from": frm, "to": to, "from_fastened": frm.get("fastened", [0]),
                     "to_fastened": to.get("fastened", [0]), "target": target, "fix_at": fix_at, "ring_at": ring_at,
                     "statement_at": statement_at, "chip_at": chip_at, "statement": statement, "chip": CHIP[lang],
                     "backdrop": True, "from_strain": bool(frm.get("strain"))},
            "source_ids": [], "overlay": {"head": False, "transition": {"type": "iris", "x": iris[0], "y": iris[1], "seconds": 0.7}}}
