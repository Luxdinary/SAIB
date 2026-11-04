"""Build plans in the format "Bauaufgabe" (Format-Bibel 1.0, 02.11.2026) from a compact topic spec plus the old plan.

The old plan of the topic (data/direction/megaconstruction-<date>-<n>-<lang>.json) supplies what does not change with
the format: title, sources, unverified items, hook candidates, description/companion text/hashtags, computations and
the 3D objects and anchors. The spec (tools/bauaufgabe_w1.py) supplies the new beats (scene type, spoken text and
scene data per language) and the camera per beat. Keyframes in "props" use language-independent "%share" times.

Run:  .venv\\Scripts\\python.exe brands\\megaconstruction\\tools\\bauaufgabe_build.py 20261109-1 [20261109-3 ...]
Writes data/direction/megaconstruction-<topic>-<lang>.P1.json for de and en (old plans stay unchanged).
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bauaufgabe_w1 import TOPICS  # noqa: E402

FUNCS = ["hook", "problem", "explanation", "demonstration", "insight", "benefit", "close"]
CHAPTERS = {"de": ["AUFGABE", "PRINZIP", "BAU", "RECHNUNG", "PROBE"], "en": ["TASK", "IDEA", "BUILD", "MATHS", "TEST"]}
CH_OF = {"gb_task": 0, "gb_load": 0, "gb_principle": 1, "gb_build": 2, "gb_calc": 3, "gb_proof": 4, "gb_close": 5}
# camera framing per scene type: free zone between the 2D blocks (zone = height in px, cy = centre)
FRAME = {"gb_task": (560, 830), "gb_load": (300, 545), "gb_principle": (330, 560), "gb_build": (300, 470),
         "gb_calc": (300, 560), "gb_proof": (260, 680), "gb_close": (300, 520)}
LAYOUT = {"format": "bauaufgabe", "explainer": False, "zone_top": 290, "zone_h": 810, "caption_bottom_px": 540,
          "caption_width_px": 800, "caption_transform": "none", "outro": False, "tail_seconds": 2.6, "progress_y": 1548,
          "ai_label_bottom_px": 318, "caption_mode": "phrases", "caption_max_words": 4}


EN_LABEL = [("(Eiffelturm)", "(Eiffel Tower)"), ("Pressemitteilung", "press release"), ("Broschüre", "brochure"),
            ("Faltblatt Schleusen", "lock leaflet"), ("Geschichte", "history"), ("Startseite", "home page"),
            ("Projektüberblick", "project overview"), ("Baufortschritt", "progress"), ("Meldung", "news"),
            ("Fassadenpapier", "facade paper"), ("Dämpfer", "damper"), ("Dompfarre St. Stephan", "St. Stephen's parish"),
            ("Huajiang-Brücke", "Huajiang bridge"), ("Eiffelturm", "Eiffel Tower")]


def _label(s: dict, lang: str) -> dict:
    if lang == "en" and s.get("label"):
        for a, b in EN_LABEL:
            s["label"] = s["label"].replace(a, b)
    return s


def old_plan(spec: dict, lang: str) -> dict:
    name = spec.get("old", {}).get(lang) or f"megaconstruction-{spec['id']}-{lang}"
    return json.loads((ROOT / "data" / "direction" / f"{name}.json").read_text(encoding="utf-8"))


def build(topic: str, lang: str) -> dict:
    spec = TOPICS[topic]
    spec["id"] = topic
    old = old_plan(spec, lang)
    om3 = (old.get("layout") or {}).get("model3d") or {}
    p = {"video_id": f"megaconstruction-{topic}-{lang}", "brand_id": "megaconstruction", "language": lang,
         "title": spec.get("title", {}).get(lang) or old["title"],
         "notes": f"Format \"Bauaufgabe\" (Format-Bibel 1.0, freigegeben 02.11.2026), Reihe {spec['series']}. Woche 1, "
                  f"gebaut mit tools/bauaufgabe_build.py aus {old['video_id']}.json (Quellen, Modell, Hook-Kandidaten; "
                  f"Quellen geprüft {old['sources'][0].get('checked_at', '')}). Alter Plan unverändert.",
         "assets": {}, "sources": [_label(s, lang) for s in copy.deepcopy(old["sources"]) + spec.get("sources_extra", [])],
         "unverified": list(old.get("unverified", [])) + spec.get("unverified_extra", {}).get(lang, [])}
    cands = old.get("hook_candidates", [])
    want = spec.get("hook_type", "question")
    hid = next((c["id"] for c in cands if c.get("type") == want), cands[0]["id"] if cands else "H1")
    p["hook"], p["hook_candidates"] = {"id": hid}, cands
    beats, shots = [], {}
    objs = copy.deepcopy(om3.get("objects", []))
    for o in spec.get("objects_drop", []):
        objs = [x for x in objs if x["id"] != o]
    objs += copy.deepcopy(spec.get("objects_extra", []))
    for i, b in enumerate(spec["beats"]):
        bid = f"b{i + 1}"
        loc = b[lang]
        fn = b.get("fn") or FUNCS[min(i, 6) if i < len(spec["beats"]) - 1 else 6]
        beats.append({"id": bid, "function": fn, "scene_type": b["scene"], "spoken": loc["spoken"], "data": loc["data"],
                      "source_ids": b.get("src", [])})
        zone, cy = FRAME[b["scene"]]
        cam = {"target": spec.get("focus", [objs[-1]["id"]]), "az0": 35 + 20 * (i % 3), "az1": 25 + 20 * (i % 3),
               "el0": 12, "el1": 8, "fit0": 0.7, "fit1": 0.78, "zone": zone, "cy": cy}
        cam.update(spec.get("cam", {}))
        cam.update(b.get("cam", {}))
        shot = {"cam": cam, "props": {**spec.get("props", {}), **b.get("props", {})}}
        if b.get("fog"):
            shot["fog"] = b["fog"]
        shots[bid] = shot
    labels = spec.get("chapters", {}).get(lang) or CHAPTERS[lang]
    lay = dict(LAYOUT)
    ol = old.get("layout") or {}
    chmap = spec.get("chmap") or [CH_OF[b["scene"]] for b in spec["beats"]]
    lay["chapters"] = {"labels": labels, "beats": {f"b{i + 1}": c for i, c in enumerate(chmap)}}
    for k in ("description", "companion_text", "hashtags"):
        lay[k] = spec.get(k, {}).get(lang) or ol.get(k)
        if isinstance(lay[k], str):   # the export appends the new closing line; drop the old one from the old plans
            lay[k] = lay[k].replace(" Folge Gigastruct für das nächste Bauwerk.", "").replace(" Follow Gigastruct for the next megastructure.", "")
    lay["computations"] = list(ol.get("computations", [])) + spec.get("computations", [])
    lay["model3d"] = {"fov": om3.get("fov", 40), "fog": om3.get("fog"), "objects": objs,
                      "anchors": {**om3.get("anchors", {}), **spec.get("anchors", {})}, "shots": shots}
    p["beats"], p["layout"] = beats, lay
    return p


def main(topics: list[str]) -> None:
    for t in topics:
        for lang in ("de", "en"):
            p = build(t, lang)
            out = ROOT / "data" / "direction" / f"megaconstruction-{t}-{lang}.P1.json"
            out.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            words = sum(len(b["spoken"].split()) for b in p["beats"])
            print(f"{out.name}: {len(p['beats'])} beats, {words} words")


if __name__ == "__main__":
    main(sys.argv[1:])
