"""Gigastruct: build direction plans (data/direction/<topic_id>.json) from compact topic specs.

A topic spec (see topics_week1.py) holds what both languages share (sources, 3D objects, anchors, camera per beat,
computations, unverified items) and per language the spoken text, the scene data, kickers and status-bar states.
The builder adds the fixed Gigastruct layout of the approved test video (Q1, Fehmarnbelt), the explainer overlay
per beat, five hook candidates and the post texts. Spoken text stays exactly as written in the spec.

Run: .venv\\Scripts\\python.exe brands\\megaconstruction\\tools\\plan_builder.py <key> [<key> ...] | --all
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "direction"
CAL = ROOT / "data" / "calendars" / "megaconstruction_2026-11.json"

BASE_LAYOUT = {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
               "status_y": 1440, "outro": False, "tail_seconds": 3.5, "progress_y": 1548, "ai_label_bottom_px": 318,
               "caption_mode": "phrases", "caption_max_words": 4}
SEA = [{"id": "water", "kind": "water", "size": 60000, "pos": [0, 0, 0]}]


def calendar_row(topic_id: str) -> dict:
    return next(r for r in json.loads(CAL.read_text(encoding="utf-8")) if r["topic_id"] == topic_id)


def hook_candidates(t: dict, L: dict, lang: str) -> list[dict]:
    """Five candidates, one per hook type. H1 is the written hook of the video; the others are honest alternatives."""
    h = L["hook"]
    name = L.get("name", t["key"])
    s1 = [t["sources"][0]["id"]]
    alt = {
        "de": {"question": L.get("hq") or (f"Wie groß ist {name} wirklich?", f"Wie groß ist {name} wirklich?"),
               "misconception": (f"Die meisten unterschätzen {name}.", f"{name}: größer als gedacht"),
               "surprising_fact": (f"{name} in Zahlen: belegt und nachgerechnet.", f"{name} in Zahlen"),
               "concrete_risk": (f"Was bei {name} schiefgehen kann, entscheidet die Bauweise.", f"{name}: die Bauweise entscheidet"),
               "demonstration": (f"Schau zu, wie {name} im Modell entsteht.", f"{name} im 3D-Modell")},
        "en": {"question": L.get("hq") or (f"How big is {name}, really?", f"How big is {name}, really?"),
               "misconception": (f"Most people underestimate {name}.", f"{name}: bigger than you think"),
               "surprising_fact": (f"{name} in numbers: sourced and calculated.", f"{name} in numbers"),
               "concrete_risk": (f"What can go wrong with {name} depends on how it is built.", f"{name}: how it is built"),
               "demonstration": (f"Watch {name} take shape in the model.", f"{name} as a 3D model")},
    }[lang]
    sp = h["spoken"] if len(h["spoken"]) <= 90 else h["spoken"].split(". ")[0].rstrip(".") + "."   # candidate limit 90 chars
    out = [{"id": "H1", "type": h["type"], "spoken": sp, "on_screen": h["screen"],
            "scores": {"clarity": 5, "relevance": 4, "curiosity": 5, "truth": 5, "visual": 5}, "source_ids": h.get("sids", s1),
            "visual": h.get("visual", "3D-Modell des Bauwerks, Zahl erscheint"), "why": {"truth": "aus den Quellen des Plans"}}]
    i = 2
    for typ, (sp, scr) in alt.items():
        if typ == h["type"]:
            continue
        out.append({"id": f"H{i}", "type": typ, "spoken": sp[:90], "on_screen": scr[:64],
                    "scores": {"clarity": 4, "relevance": 3, "curiosity": 3, "truth": 4, "visual": 3}, "source_ids": s1,
                    "visual": "3D-Modell", "why": {"truth": "allgemeine, belegbare Aussage"}})
        i += 1
    return out


def build(t: dict, lang: str) -> dict:
    L = t[lang]
    tid = f"megaconstruction-{t['date']}-{t['slot']}-{lang}"
    cal = calendar_row(tid)
    checked = t.get("checked_at") or cal.get("source_checked_at") or "2026-11-01"
    sources = [{**s, "checked_at": s.get("checked_at", checked)} for s in t["sources"]]
    beats, states = [], []
    n_kick = 1
    for i, b in enumerate(L["beats"]):
        bid = f"b{i + 1}"
        ov = {}
        if b["f"] != "hook" and b.get("k"):
            n_kick += 1
            ov["kicker"] = f"{n_kick} · {b['k']}"
        ov["marker"] = b.get("m", "fakt")
        if b.get("mat"):
            ov["marker_at"] = b["mat"]
        if "so" in b:
            ov["source"] = b["so"]
        if b.get("tr"):
            ov["transition"] = {"type": b["tr"], "seconds": 0.7, **({"x": 540, "y": 960} if b["tr"] == "iris" else {})}
        if b.get("vig"):
            ov["vignette"] = True
        if b.get("ex"):
            ov["example"] = True
        beats.append({"id": bid, "function": b["f"], "scene_type": b["s"], "spoken": b["t"], "data": b["d"],
                      "source_ids": b.get("src", []), "overlay": ov})
        for st in b.get("st", []):
            text, tone, at = st
            states.append({"beat": bid, "text": text, "tone": tone, **({"at": at} if isinstance(at, str) else {"offset": at})})
    shots = {}
    for i, sh in enumerate(t["shots"]):
        if i < len(beats):
            s = json.loads(json.dumps(sh))
            for k, v in (L.get("shot_props", {}).get(i, {}) or {}).items():
                s.setdefault("props", {})[k] = v
            shots[f"b{i + 1}"] = s
    layout = {**BASE_LAYOUT, **t.get("layout", {}),
              "status_bar": {"file": L["status_file"], "states": states},
              "description": L["description"], "companion_text": L["companion"], "hashtags": t["hashtags"][lang],
              "computations": t.get("computations", []),
              "model3d": {"fov": t.get("fov", 46), "fog": t.get("fog", [900, 9000]), "objects": t["objects"],
                          "anchors": t.get("anchors", {}), "shots": shots,
                          "default_cam": {"p0": [400, 200, 400], "l0": [0, 0, 0]}}}
    return {"video_id": tid, "brand_id": "megaconstruction", "language": lang, "title": L["title"] or cal["title"],
            "notes": f"Gigastruct Woche 1 (01.11.2026), Vorlage 1.0, Kalender {tid}. Thema: {t['key']}. "
                     f"Stilisierte 3D-Modelle aus Grundkörpern, schematisch; Zahlen nur aus den Quellen des Kalenders.",
            "layout": layout, "assets": {}, "sources": sources, "unverified": t.get("unverified", []),
            "hook": {"id": "H1"}, "hook_candidates": hook_candidates(t, L, lang), "beats": beats}


def word_count(plan: dict) -> int:
    return sum(len(b["spoken"].split()) for b in plan["beats"])


def main(argv: list[str]) -> int:
    mod = importlib.import_module("topics_week1")
    topics = {t["key"]: t for t in mod.TOPICS}
    keys = list(topics) if "--all" in argv else [a for a in argv if not a.startswith("--")]
    sp = Path(__file__).resolve().parent / "shorts.json"
    shorts = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    for k in keys:
        t = topics[k]
        for lang in t.get("langs", ("de", "en")):
            shorts[f"megaconstruction-{t['date']}-{t['slot']}-{lang}"] = t["short"]["de"] + (" EN" if lang == "en" else "")
        sp.write_text(json.dumps(shorts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for lang in t.get("langs", ("de", "en")):
            p = build(t, lang)
            path = OUT / f"{p['video_id']}.json"
            path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{path.name}: {word_count(p)} words")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main(sys.argv[1:]))
