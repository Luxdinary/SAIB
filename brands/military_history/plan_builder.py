"""Frontlore plan builder: one bilingual topic spec -> two direction plans (DE, EN) plus the topic drawing.

A spec is a plain dict shaped like a direction plan, with two extras:
- any leaf may be {"de": ..., "en": ...}; `build(spec, lang)` keeps the value of that language;
- `status` (thread object states) uses word anchors ("at": "w:Wort"); the offset in seconds is estimated from the
  word position in the spoken beat text and the measured speaking rate of the brand voice (RATE), because the shared
  status bar only takes seconds. Scene data use word anchors directly (frontlore_scenes resolves them on the voice).
- `drawing`: {"name": "<file>.svg", "elems": [svg strings]} written to assets/drawings/ (viewBox 760 x 620).

Usage (repository root):  .venv\\Scripts\\python.exe brands\\military_history\\plan_builder.py <spec module.py> [...]
Each module defines SPECS = [spec, ...]; plans go to data/direction/<topic>-<lang>.json.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DRAWINGS = HERE / "assets" / "drawings"
RATE = {"de": 2.04, "en": 2.05}          # words per second, Gemini Charon (DE measured on Q1, EN on the telegraph EN, 01.11.2026)

LAYOUT = {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
          "status_y": 1440, "outro": False, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
          "caption_mode": "phrases", "caption_max_words": 4}
CLOSING = {"de": "Historische Technik, sachlich erklärt: Folge Frontlore.",
           "en": "Historical technology, plainly explained: follow Frontlore."}
KICKERS = {"de": ["", "2 · DER ANLASS", "3 · DIE TECHNIK", "4 · DER VERGLEICH", "5 · DER KERN", "6 · DIE ZEIT", "7 · HEUTE"],
           "en": ["", "2 · THE REASON", "3 · THE TECHNOLOGY", "4 · THE COMPARISON", "5 · THE POINT", "6 · THE TIMELINE", "7 · TODAY"]}


def pick(obj, lang):
    if isinstance(obj, dict):
        if set(obj) == {"de", "en"}:
            return pick(obj[lang], lang)
        return {k: pick(v, lang) for k, v in obj.items()}
    if isinstance(obj, list):
        return [pick(v, lang) for v in obj]
    return obj


def _norm(s: str) -> str:
    return re.sub(r"[^\w]", "", s.lower())


def word_offset(spoken: str, anchor: str, lang: str) -> float:
    """Seconds from beat start to the anchored word, estimated from its index and the speaking rate."""
    tok, n = anchor[2:], 1
    if "#" in tok:
        tok, k = tok.rsplit("#", 1)
        n = int(k)
    words = spoken.split()
    hits = [i for i, w in enumerate(words) if _norm(w).startswith(_norm(tok))]
    if len(hits) < n:
        raise ValueError(f"status anchor {anchor!r} not in beat text: {spoken[:60]}...")
    return round(0.25 + hits[n - 1] / RATE[lang], 1)


def build(spec: dict, lang: str) -> dict:
    s = pick({k: v for k, v in spec.items() if k not in ("drawing", "short")}, lang)
    topic = s.pop("topic")
    beats = s["beats"]
    for b in beats:                                   # title lines (Oswald 74 px caps: about 22 characters per line)
        d = b.get("data") or {}
        if d.get("headline") and "headline_lines" not in d:
            d["headline_lines"] = 1 if len(d["headline"]) <= 22 else 2
        if b["scene_type"] == "ui_demo":              # one geometry for all sheets: callout x/y stay valid
            d.setdefault("sheet_h", 620)
            d.setdefault("draw_scale", 0.9)
            d.setdefault("draw_top", 30)
    spoken = {b["id"]: b["spoken"] for b in beats}
    for i, b in enumerate(beats):
        ov = b.setdefault("overlay", {})
        if i and "kicker" not in ov:
            ov["kicker"] = KICKERS[lang][min(i, 6)]
    beats[-1]["spoken"] = beats[-1]["spoken"].rstrip() + " " + CLOSING[lang]
    beats[-1].setdefault("overlay", {}).update({"marker_until": "w:" + CLOSING[lang].split()[0],
                                               "head_until": "w:" + CLOSING[lang].split()[0]})
    states = []
    for st in s.pop("status"):
        off = word_offset(spoken[st["beat"]], st["at"], lang) if str(st.get("at", "")).startswith("w:") else float(st.get("offset", 0.5))
        states.append({"beat": st["beat"], "text": st["text"], "tone": st.get("tone", "muted"), "offset": off})
    layout = {**LAYOUT, "status_bar": {"file": s.pop("status_file"), "states": states},
              "description": s.pop("description"), "companion_text": CLOSING[lang], "hashtags": s.pop("hashtags")}
    for src in s["sources"]:
        src.setdefault("checked_at", s.get("checked", "2026-11-01"))
    s.pop("checked", None)
    hook_id = s.pop("hook_id", "H1")
    plan = {"video_id": f"{topic}-{lang}", "brand_id": "military_history", "language": lang, **s, "layout": layout,
            "hook": {"id": hook_id, "note": s.get("hook_note", "")}}
    plan.pop("hook_note", None)
    chosen = next(h for h in plan["hook_candidates"] if h["id"] == hook_id)
    chosen["spoken"] = beats[0]["spoken"]
    return plan


def write_drawing(d: dict) -> Path:
    body = "\n  ".join(d["elems"])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 620" fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
           f'  <!-- Frontlore drawing, own work (Claude Code, 2026-11-01), generated by plan_builder.py. Stylized, not to scale. -->\n'
           f'  {body}\n</svg>\n')
    f = DRAWINGS / d["name"]
    f.write_text(svg, encoding="utf-8", newline="\n")
    return f


# --- drawing primitives (viewBox 760 x 620); class ln = drawn stroke, thin = secondary, sight = dashed, pivot = dot ---

def L(x1, y1, x2, y2, cls="ln"):
    return f'<line class="{cls}" pathLength="1" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def R(x, y, w, h, cls="ln", rx=0):
    return f'<rect class="{cls}" pathLength="1" x="{x}" y="{y}" width="{w}" height="{h}"' + (f' rx="{rx}"' if rx else "") + "/>"


def C(cx, cy, r, cls="ln"):
    if cls == "pivot":
        return f'<circle class="pivot" cx="{cx}" cy="{cy}" r="{r}"/>'
    return f'<circle class="{cls}" pathLength="1" cx="{cx}" cy="{cy}" r="{r}"/>'


def E(cx, cy, rx, ry, cls="ln"):
    return f'<ellipse class="{cls}" pathLength="1" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>'


def PL(pts, cls="ln", closed=False):
    p = " ".join(f"{x},{y}" for x, y in pts)
    return f'<{"polygon" if closed else "polyline"} class="{cls}" pathLength="1" points="{p}"/>'


def PATH(d, cls="ln"):
    return f'<path class="{cls}" pathLength="1" d="{d}"/>'


def SIGHT(x1, y1, x2, y2):
    return f'<line class="sight" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def load_specs(path: Path) -> list[dict]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod.SPECS


def main(paths: list[str]) -> int:
    for p in paths:
        sys.path.insert(0, str(Path(p).resolve().parent))          # specs import their shared helpers (_common.py)
        for spec in load_specs(Path(p)):
            if spec.get("drawing"):
                write_drawing(spec["drawing"])
            for lang in ("de", "en"):
                plan = build(spec, lang)
                out = ROOT / "data" / "direction" / f"{plan['video_id']}.json"
                out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
                words = sum(len(b["spoken"].split()) for b in plan["beats"])
                print(f"{out.name}: {words} words, ~{words / RATE[lang] + 3.5:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
