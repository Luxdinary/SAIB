"""Fehmarnbelt EN (megaconstruction-20261109-2-en): the approved Q1 plan (data/direction/megaconstruction-20261105-1-de.json)
with an English script, English on-screen texts and the 3D word anchors moved to the English words."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
de = json.loads((ROOT / "data" / "direction" / "megaconstruction-20261105-1-de.json").read_text(encoding="utf-8"))
p = json.loads(json.dumps(de))
p["video_id"], p["language"] = "megaconstruction-20261109-2-en", "en"
p["title"] = "Fehmarnbelt tunnel: one element outweighs seven Eiffel Towers"
p["notes"] = "Gigastruct Woche 1 (01.11.2026): English version of the approved test video Q1 (Fehmarnbelt), same model, shots and sources."

ANCHOR = {"Eiffeltürme": "Eiffel", "fünf": "five", "Becken": "basin", "schwimmt": "floats", "erste": "first", "neun": "nine",
          "Schotten": "Bulkheads", "Fünf": "Five", "Absenkpontons": "pontoons", "Eiffelturm": "Eiffel", "10.100": "10,100",
          "Zug": "train", "Minuten": "minutes", "Auto": "car", "Fähre": "ferry", "rund": "around", "89": "89", "drei": "three"}


def move(v):
    if isinstance(v, str) and v.startswith("@"):
        m = re.match(r"^@([^+\-]+)([+\-][\d.]+)?$", v)
        return "@" + ANCHOR[m.group(1)] + (m.group(2) or "")
    if isinstance(v, list):
        return [move(x) for x in v]
    if isinstance(v, dict):
        return {k: move(x) for k, x in v.items()}
    return v


p["layout"]["model3d"]["shots"] = move(p["layout"]["model3d"]["shots"])
B = {b["id"]: b for b in p["beats"]}
B["b1"].update(spoken="This concrete block weighs more than seven Eiffel Towers. And yet it floats.")
B["b1"]["data"].update(kicker="Fehmarnbelt · tunnel element", question="Heavier than 7 Eiffel Towers. And it floats.", question_at="@This",
                       number={**B["b1"]["data"]["number"], "value": "73,500", "at_word": "Eiffel"},
                       badge={**B["b1"]["data"]["badge"], "text": "floats: bulkheads shut", "at_word": "floats"})
B["b1"]["overlay"]["marker_at"] = "w:And"
B["b2"].update(spoken="It is one piece of the Fehmarnbelt tunnel between Denmark and Germany: around 18 kilometres, 89 elements, and according to the builder the longest immersed tunnel in the world.")
B["b2"]["data"].update(headline="World's longest immersed tunnel (per builder)",
                       items=[{"value": "18", "unit": "km", "label": "tunnel length, approx.", "at_word": "18"},
                              {"value": "89", "unit": "", "label": "elements", "at_word": "89"}])
if "note" in B["b2"]["data"]:
    B["b2"]["data"].update(note="Schematic row: 89 elements", note_at="@89")
B["b2"]["overlay"].update(kicker="2 · Denmark – Germany", marker_at="w:Fehmarnbelt")
B["b3"].update(spoken="A standard element is 217 metres long, 42 wide and 9 high. Inside are five tubes: two for the motorway, two for the railway and one for services.")
B["b3"]["data"].update(headline="Five tubes in one block", note="Schematic cross-section",
                       dims=[{"anchor": "len", "text": "217 m", "at_word": "217"}, {"anchor": "wid", "text": "42 m", "at_word": "42"},
                             {"anchor": "hgt", "text": "9 m", "at_word": "9"}],
                       callouts=[{"anchor": "road", "text": "2 × motorway", "side": "up", "at_word": "motorway"},
                                 {"anchor": "rail", "text": "2 × railway", "side": "down", "at_word": "railway"},
                                 {"anchor": "tech", "text": "Services", "side": "up", "at_word": "services"}])
B["b3"]["overlay"].update(kicker="3 · Cross-section · standard element", marker_at="w:217")
B["b4"].update(spoken="It is cast on land in nine segments. Bulkheads shut, the basin is flooded, and the hollow body floats. Five tugs and two immersion pontoons take it out to the trench. The first lowering took a good 14 hours.")
B["b4"]["data"].update(headline="From factory floor to seabed",
                       steps=[{"label": "Cast on land", "sub": "9 segments of about 24 m", "at_word": "cast"},
                              {"label": "Bulkheads, flooding", "sub": "the hollow body floats", "at_word": "Bulkheads"},
                              {"label": "Towing", "sub": "5 tugs · 2 pontoons", "at_word": "Five"},
                              {"label": "Lowering", "sub": "first element: 14+ hours", "at_word": "first"}])
B["b4"]["overlay"].update(kicker="4 · Construction phases", marker_at="w:cast",
                          source="Sources: Femern A/S, fact sheet 8/2026 and news 2023, 2026 · retrieved 30.10.2026")
B["b5"].update(spoken="For comparison: the whole Eiffel Tower weighs 10,100 tonnes, according to its operator. One element: 73,500. More than seven times as much.")
B["b5"]["data"].update(headline="One element vs. the Eiffel Tower",
                       a={**B["b5"]["data"]["a"], "label": "Tunnel element"}, b={**B["b5"]["data"]["b"], "label": "Eiffel Tower, total"},
                       a_at="@73,500", b_at="@Eiffel", result_at="@seven")
B["b5"]["overlay"].update(kicker="5 · Calculated, not estimated", marker_at="w:Eiffel")
B["b6"].update(spoken="Once it is finished, the train will take 7 minutes and the car 10. The ferry takes 45 today, not counting waiting time.")
B["b6"]["data"].update(headline="Under the Belt",
                       items=[{"value": "7", "unit": "min", "label": "train", "at_word": "train"},
                              {"value": "10", "unit": "min", "label": "car", "at_word": "car"},
                              {"value": "45", "unit": "min", "label": "ferry today", "ref": True, "at_word": "ferry"}])
B["b6"]["overlay"].update(kicker="6 · After completion", marker_at="w:train",
                          source="Source: Femern A/S, fact sheet 8/2026 (planned values) · retrieved 30.10.2026")
B["b7"].update(spoken="Status August 2026: three elements are on the seabed, 86 still to go. Follow Gigastruct to see the next one.")
B["b7"]["data"].update(statement="Three elements are on the seabed.",
                       counter={**B["b7"]["data"]["counter"], "label": "elements on the seabed", "at_word": "three"},
                       chip={**B["b7"]["data"]["chip"], "text": "Follow Gigastruct", "at_word": "Follow"})
B["b7"]["overlay"].update(kicker="7 · Status August 2026", marker_at="w:Status")
p["layout"]["status_bar"] = {"file": "Element 1 / 89", "states": [
    {"beat": "b1", "text": "73,500 t of concrete", "tone": "muted", "offset": 0.3},
    {"beat": "b1", "text": "floats", "tone": "accent", "at": "@floats"},
    {"beat": "b2", "text": "bound for Fehmarnbelt", "tone": "muted", "offset": 0.3},
    {"beat": "b2", "text": "1 of 89", "tone": "accent", "at": "@89"},
    {"beat": "b3", "text": "217 × 42 × 9 m", "tone": "muted", "at": "@217"},
    {"beat": "b3", "text": "5 tubes", "tone": "accent", "at": "@five"},
    {"beat": "b4", "text": "cast on land", "tone": "accent", "offset": 0.15},
    {"beat": "b4", "text": "floating", "tone": "accent", "at": "@Bulkheads"},
    {"beat": "b4", "text": "under tow", "tone": "accent", "at": "@Five"},
    {"beat": "b4", "text": "being lowered", "tone": "accent", "at": "@first"},
    {"beat": "b5", "text": "compared: Eiffel Tower", "tone": "muted", "at": "@Eiffel"},
    {"beat": "b5", "text": "73,500 t", "tone": "accent", "at": "@73,500"},
    {"beat": "b5", "text": "7.3 × Eiffel Tower", "tone": "accent", "at": "@seven"},
    {"beat": "b6", "text": "train: 7 min (plan)", "tone": "amber", "at": "@train"},
    {"beat": "b7", "text": "status August 2026", "tone": "muted", "offset": 0.3},
    {"beat": "b7", "text": "on the seabed since May 2026", "tone": "green", "at": "@three"},
]}
p["layout"]["description"] = ("A standard Fehmarnbelt tunnel element is 217 metres long and weighs 73,500 tonnes, more than seven Eiffel Towers. "
                              "How it is cast on land, towed out floating and lowered onto the seabed. Status: Femern A/S fact sheet, August 2026.")
p["layout"]["companion_text"] = ("Calculated: 73,500 t ÷ 10,100 t (total weight of the Eiffel Tower per its operator) = 7.28. 89 − 3 = 86 elements still to go "
                                 "(status August 2026). Stylised 3D models, schematic cross-section. Follow Gigastruct for the next megastructure.")
p["layout"]["hashtags"] = ["fehmarnbelt", "tunnel", "megaproject", "civilengineering", "engineering"]
H = {
    "surprising_fact": ("This concrete block weighs more than seven Eiffel Towers. And yet it floats.", "Heavier than 7 Eiffel Towers. And it floats."),
    "question": ("How do you put 73,500 tonnes of concrete on the floor of the Fehmarnbelt?", "How do 73,500 tonnes reach the seabed?"),
    "misconception": ("This tunnel is not bored. It is cast on land and sunk into the sea.", "Not bored. Cast on land and sunk."),
    "concrete_risk": ("One element, 73,500 tonnes: the first lowering took more than 14 hours.", "14 hours for one element"),
    "demonstration": ("Watch a 217 metre element float out and sink to the seabed.", "217 m: floated out, sunk down"),
}
for c in p["hook_candidates"]:
    if c["type"] in H:
        c["spoken"], c["on_screen"] = H[c["type"]]
(ROOT / "data" / "direction" / "megaconstruction-20261109-2-en.json").write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sp = Path(__file__).resolve().parent / "shorts.json"
s = json.loads(sp.read_text(encoding="utf-8"))
s["megaconstruction-20261109-2-en"] = "Fehmarnbelt-Tunnelelement EN"
sp.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("words", sum(len(b["spoken"].split()) for b in p["beats"]))
