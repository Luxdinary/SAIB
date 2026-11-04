"""Zonkfruit plan builder: a compact topic spec (brands/brainrot/topics/<topic>.json) -> one direction plan per language.

The spec holds what changes per episode (spoken text per beat, scene data, five hook candidates, status bar, post
texts); the builder adds what is the same for every episode (Q1 layout, explainer overlay defaults, kickers come from
brand.yaml, sources from the spec with labels) and lints the spec: every cue word must be spoken in its beat, the hook
beat must equal the chosen hook, five hook types, word count against the measured Puck speaking rate.

  .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\plan_builder.py brands\\brainrot\\topics\\brainrot-20261109-1.json
  -> data\\direction\\brainrot-20261109-1-de.json and -en.json

Spec (all text fields per language under "de"/"en"):
  topic, series (A-E), short {de, en}, sources [{id, url, title, checked_at, label {de, en}}],
  de/en: {title, hooks [5 x {type, spoken, on_screen, scores, source_ids, visual}] (first = chosen),
          beats [7 x {function, scene_type, spoken, data, overlay?, source_ids}], status [{beat, text, tone, offset}],
          post {title, description, hashtags}}
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK_TYPES = ["question", "misconception", "surprising_fact", "concrete_risk", "demonstration"]
SERIES = {"A": ("Faktentür", "Fact Door"), "B": ("Obst-Ausweis", "Fruit ID"), "C": ("Tierakte", "Animal File"),
          "D": ("Plümo-Labor", "Plümo Lab"), "E": ("Rekordhalle", "Record Hall")}
RATE = {"de": 2.25, "en": 2.28}     # words per second, Puck, measured 01.11.2026: DE 183 words 81.2 s, EN 205 words 90.0 s
TARGET = (70.0, 85.0)                # video seconds; speech + 0.4 s lead-in + 2.4 s tail

LAYOUT = {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 500, "caption_width_px": 800, "caption_transform": "none",
          "outro": False, "tail_seconds": 2.4, "progress_y": 1550, "ai_label_bottom_px": 318, "status_y": 1440,
          "caption_mode": "phrases", "caption_max_words": 4}

DEFAULT_OVERLAY = {"hook": {"marker": "fakt"}, "problem": {"marker": "fakt"}, "explanation": {"marker": "fakt"},
                   "demonstration": {"marker": "fakt"}, "insight": {"marker": "fakt"}, "benefit": {"marker": "auslegung"},
                   "close": {"marker": "none"}}


def _norm(w: str) -> str:
    return re.sub(r"[^a-zäöüß0-9]", "", w.lower())


def _cues(data: dict) -> list[str]:
    """Every cue word a scene will look up in its beat (keys cue_*, and cue/word inside lists and stamp)."""
    out = [v for k, v in data.items() if k.startswith("cue") and isinstance(v, str) and v]
    for key in ("labels", "callouts", "bars", "items"):
        for it in data.get(key, []) or []:
            for f in ("cue", "word"):
                if it.get(f):
                    out.append(it[f])
    if isinstance(data.get("stamp"), dict) and data["stamp"].get("cue"):
        out.append(data["stamp"]["cue"])
    return out


def lint(lang: str, L: dict, spec: dict) -> list[str]:
    p: list[str] = []
    beats = L["beats"]
    if [b["function"] for b in beats] != ["hook", "problem", "explanation", "demonstration", "insight", "benefit", "close"]:
        p.append("beats must be the seven story functions in order")
    if len(L["hooks"]) < 5 or {h["type"] for h in L["hooks"]} != set(HOOK_TYPES):
        p.append("five hook candidates covering all five hook types are needed")
    if L["hooks"][0]["spoken"].strip() != beats[0]["spoken"].strip():
        p.append("hook beat text must equal the first (chosen) hook candidate")
    ids = {s["id"] for s in spec["sources"]}
    for b in beats:
        words = [_norm(w) for w in b["spoken"].split()]
        for cw in _cues(b.get("data", {})):
            if not any(w.startswith(_norm(cw)) for w in words):
                p.append(f"{b['function']}: cue {cw!r} is not spoken in this beat")
        for s in b.get("source_ids", []):
            if s not in ids:
                p.append(f"{b['function']}: unknown source {s}")
        ov = b.get("overlay", {})
        for k in ("marker_at", "dim_at", "head_at", "head_until"):
            v = ov.get(k)
            if isinstance(v, str) and v.startswith("w:") and not any(w.startswith(_norm(v[2:])) for w in words):
                p.append(f"{b['function']}: overlay {k} word {v[2:]!r} is not spoken in this beat")
    n = sum(len(b["spoken"].split()) for b in beats)
    secs = n / RATE[lang] + 2.8
    if not TARGET[0] - 2 <= secs <= TARGET[1]:
        p.append(f"{n} words ~ {secs:.0f} s video at {RATE[lang]} words/s; target {TARGET[0]:.0f}-{TARGET[1]:.0f} s")
    for st in L.get("status", []):
        if st.get("word"):
            words = [_norm(w) for w in beats[int(st["beat"][1:]) - 1]["spoken"].split()]
            if not any(w.startswith(_norm(st["word"])) for w in words):
                p.append(f"status word {st['word']!r} is not spoken in {st['beat']}")
        if len(st["text"]) > 30:
            p.append(f"status text too long ({len(st['text'])} > 30): {st['text']}")
    return p


def _state(st: dict, beats: list[dict], lang: str) -> dict:
    """Status state; "word" instead of "offset" estimates the offset from the word's position in the beat (rate)."""
    out = {k: v for k, v in st.items() if k != "word"}
    if st.get("word") and "offset" not in st:
        b = beats[int(st["beat"][1:]) - 1]
        words = [_norm(w) for w in b["spoken"].split()]
        i = next((k for k, w in enumerate(words) if w.startswith(_norm(st["word"]))), 0)
        out["offset"] = round(0.2 + i / RATE[lang], 2)
    return out


def build(spec: dict, lang: str) -> dict:
    L = spec[lang]
    vid = f"{spec['topic']}-{lang}"
    sign_de, sign_en = SERIES[spec["series"]]
    beats = []
    for i, b in enumerate(L["beats"]):
        ov = dict(DEFAULT_OVERLAY[b["function"]])
        if b["function"] == "explanation" and b["scene_type"] == "zonk_diagram":
            ov["transition"] = {"type": "iris", "x": 540, "y": 730, "seconds": 0.7}
        if b["function"] == "demonstration" and b["scene_type"] == "zonk_zoom":
            ov.update({"transition": {"type": "blende", "seconds": 0.7}, "vignette": True})
        if b["function"] == "insight" and b["scene_type"] == "zonk_scan":
            ov["transition"] = {"type": "iris", "x": 756, "y": 575, "seconds": 0.7}
        if b["function"] == "close" and b.get("data", {}).get("cue_up"):
            ov["head_until"] = "w:" + b["data"]["cue_up"]
        ov.update(b.get("overlay", {}))
        beats.append({"id": f"b{i + 1}", "function": b["function"], "scene_type": b["scene_type"], "spoken": b["spoken"],
                      "data": b.get("data", {}), "overlay": ov, "source_ids": b.get("source_ids", [])})
    hooks = [{"id": f"H{k + 1}", **h} for k, h in enumerate(L["hooks"])]
    post = L["post"]
    tags = post["hashtags"]
    layout = dict(LAYOUT)
    layout.update({
        "description": post["description"], "companion_text": post.get("companion", (
            "Zonkfruit: eine erfundene Frucht, echte Fakten. Folge Zonkfruit für mehr." if lang == "de"
            else "Zonkfruit: a made-up fruit, real facts. Follow Zonkfruit for more.")),
        "hashtags": tags,
        "platform_texts": {
            "tiktok": {"title": post["title"], "description": post["description"], "hashtags": tags},
            "instagram": {"title": post["title"], "description": post["description"], "hashtags": tags + ["reels"]},
            "youtube": {"title": f"{post['title']} #Shorts", "description": post["description"], "hashtags": ["Shorts"] + tags[:4]},
        },
        "status_bar": {"file": sign_de if lang == "de" else sign_en, "states": [_state(st, L["beats"], lang) for st in L["status"]]},
    })
    return {
        "video_id": vid, "brand_id": "brainrot", "language": lang, "title": L["title"],
        "notes": (f"Zonkfruit Vorlage 1.0, Produktion Woche 1 (01.11.2026), Reihe {spec['series']}. Aufbau wie das freigegebene "
                  f"Testvideo Q1 (Erdbeere keine Beere). Nur Aussagen aus den Kalenderquellen."),
        "hook": {"id": "H1", "note": "erster Kandidat der Themenspezifikation"},
        "hook_candidates": hooks,
        "sources": [{"id": s["id"], "url": s["url"], "title": s["title"], "checked_at": s["checked_at"],
                     "label": s["label"][lang] if isinstance(s["label"], dict) else s["label"]} for s in spec["sources"]],
        "unverified": spec.get("unverified", []),
        "layout": layout, "assets": {}, "beats": beats,
    }


def main(argv: list[str]) -> int:
    rc = 0
    for f in argv:
        spec = json.loads(Path(f).read_text(encoding="utf-8"))
        for lang in ("de", "en"):
            if lang not in spec:
                continue
            probs = lint(lang, spec[lang], spec)
            n = sum(len(b["spoken"].split()) for b in spec[lang]["beats"])
            out = ROOT / "data" / "direction" / f"{spec['topic']}-{lang}.json"
            if probs:
                rc = 1
                print(f"{out.name}: NOT written ({n} words)", *probs, sep="\n  ")
                continue
            out.write_text(json.dumps(build(spec, lang), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{out.name}: ok ({n} words ~ {n / RATE[lang] + 2.8:.0f} s)")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
