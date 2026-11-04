"""Gigastruct test video (Neustart 2026-11, OneDrive\\Business\\02 Marke\\Gigastruct\\Testvideo-Konzept 2026-11.md).

Builds data/direction/megaconstruction-20261109-2-<lang>.T1.json from the released P1 plan of that language (same
spoken text). Adds: realistic Higgsfield stills and Kling clips (layout.media, drawn by render/render_gigastruct.py),
the dimension line on the hook picture, the balance in the calculation, the time-lapse clock in the proof, a load box
that swipes in, and the sound (layout.sound, layout.sound_cues in the format of the shared sound layer).

DE: voice P1 reused (Charon). EN (Stefan's release 03.11.2026): same scenes, material and cues, text from the EN P1
plan, same speaker Charon, voice made once with tools/voice_once.py.
Picture wipes sit 0.9 s before a word; the shared sound layer has no word offsets, so those cues get seconds after
the beat start, read from a timed run of the same voice (--timing storage/direction/<id>-<ver>); without it they fall
on the word itself.

Run:  .venv\\Scripts\\python.exe brands\\megaconstruction\\tools\\testvideo_fehmarn.py de --timing storage\\direction\\megaconstruction-20261109-2-de-T1
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FULL = [0, 0, 1080, 1920]

# words and texts per language: the picture changes on the same spoken moment in both versions
L = {
    "de": {
        "b1_to": "@steht", "b1_mark": "@Beton", "b1_mark_out": "@Vor", "b1_tag": "Fehmarnbelt",
        "b2_to": "@wiegt", "b2_load": "73.500", "b2_goal": "schwimmen",
        "b3_bulk": "Schotten", "b3_then": "dann", "b3_rule": "geflutet", "mark_bulk": "Schott",
        "b4_rows": ["neun", "fünf", "Schlepper", "Absenkpontons"], "b4_to": "fünf",
        "b5_tower": "Eiffelturm", "b5_calc": ["73.500", "7,3", "neun", "24"],
        "b6_stamp": "Mai", "b6_cut": "@Das", "b6_clock": "@abgesenkt", "b6_until": "@gut",
        "b7_to": "Drei", "b7_follow": "Folge",
        "scale": {"title": "Waage · schematisch", "left": "1 Element · 73.500 t", "right": "7 × Eiffelturm"},
        "clock": {"end_text": "gut 14 h", "label": "Absenken"},
    },
    "en": {
        "b1_to": "@Fehmarnbelt", "b1_mark": "@concrete", "b1_mark_out": "@Fehmarnbelt-1.0", "b1_tag": "Fehmarnbelt",
        "b2_to": "@Yet", "b2_load": "standard", "b2_goal": "float",
        "b3_bulk": "Bulkheads", "b3_then": "then", "b3_rule": "flooded", "mark_bulk": "Bulkhead",
        "b4_rows": ["nine", "five", "tugs", "pontoons"], "b4_to": "five",
        "b5_tower": "Eiffel", "b5_calc": ["73,500", "7.3", "nine", "24"],
        "b6_stamp": "May", "b6_cut": "@first-0.2", "b6_clock": "@lowered", "b6_until": "@just",
        "b7_to": "three", "b7_follow": "Follow",
        "scale": {"title": "Balance · schematic", "left": "1 element · 73,500 t", "right": "7 × Eiffel Tower"},
        "clock": {"end_text": "just over 14 h", "label": "Lowering"},
    },
}


class Timing:
    """Word times of a timed run (plan.timed.json + captions.json) for cues that sit before a word."""

    def __init__(self, folder: Path | None):
        self.beats, self.words, self.cues = {}, [], []
        if folder and (folder / "plan.timed.json").exists():
            tp = json.loads((folder / "plan.timed.json").read_text(encoding="utf-8"))
            self.beats = {b["id"]: (b["start"], b["start"] + b["duration"]) for b in tp["beats"]}
            if (folder / "captions.json").exists():   # a full render
                caps = json.loads((folder / "captions.json").read_text(encoding="utf-8"))
                groups = caps if isinstance(caps, list) else caps.get("groups", caps)
                self.words = [(w["start"], w["text"]) for g in groups for w in g["words"]]
            elif (folder / "sound.json").exists():   # a dry run: the word cues of a plan built without timing
                self.cues = [(c["at"], c["sound"]) for c in json.loads((folder / "sound.json").read_text(encoding="utf-8"))["cues"]
                             if c.get("source") == "plan"]

    def before(self, beat: str, word: str, sec: float, sound: str = "") -> dict:
        if beat in self.beats:
            b0, b1 = self.beats[beat]
            norm = lambda s: re.sub(r"[^\wäöüß]", "", s.lower())  # noqa: E731
            t = next((t for t, w in self.words if b0 <= t < b1 and norm(w).startswith(norm(word))), None)
            if t is None and sound:   # dry run: the first plan cue of this sound in the beat sat on the word
                t = next((t for t, s in self.cues if b0 <= t < b1 and s == sound), None)
            if t is not None:
                return {"at": round(max(0.0, t - b0 - sec), 2)}
        return {"word": word}


def _tower_cue(timing: Timing, word: str, k: int) -> dict:
    """Tick when tower k lands on the balance (scenes_bauaufgabe._gb_scale: step 0.32 s, lands 0.2 s after it starts)."""
    base = timing.before("b5", word, 0.0, "tick")
    if "at" in base:
        return {"at": round(base["at"] + k * 0.32 + 0.2, 2), "cue": "tick"}
    return {"word": word, "cue": "tick"}


def build(lang: str, timing: Timing) -> dict:
    t = L[lang]
    src = ROOT / "data" / "direction" / f"megaconstruction-20261109-2-{lang}.P1.json"
    p = copy.deepcopy(json.loads(src.read_text(encoding="utf-8")))
    p["notes"] = ("Testvideo Neustart 2026-11 (Konzept 02 Marke\\Gigastruct\\Testvideo-Konzept 2026-11.md), gebaut mit "
                  f"tools/testvideo_fehmarn.py aus dem Plan P1 ({lang}, Text unverändert). " + p.get("notes", ""))
    beats = {b["id"]: b for b in p["beats"]}
    # the 3D pins of b1, b3 and b6 would float over the pictures: the hook gets a dimension line on the picture instead
    for bid in ("b1", "b3", "b6"):
        beats[bid]["data"].pop("pins", None)
    beats["b2"]["data"]["load"]["enter"] = "swipe"
    beats["b3"]["data"]["note_out"] = f"@{t['b3_bulk']}-0.15"
    beats["b5"]["data"]["scale"] = {**t["scale"], "left_t": 73500, "unit_t": 10100, "count": 7, "at": f"@{t['b5_tower']}", "dy": 96}
    beats["b6"]["data"]["clock"] = {"hours": 14, **t["clock"], "at": t["b6_clock"], "until": t["b6_until"], "dy": 480}
    lay = p["layout"]
    lay["media_folder"] = "assets/higgsfield/fehmarnbelt"
    lay["media"] = [
        # T2 (03.11.): tighter crop and lower position, so the tugs at the near end (which seem to run towards the
        # element in the clip) mostly leave the frame; the line runs along the left long edge as it lies at 4.4 s
        {"beat": "b1", "kind": "video", "file": "clips/gs_fb_clip_tow.mp4", "from": 0, "to": t["b1_to"], "box": FULL,
         "enter": "cut", "exit": "wipe", "shade": 0.55, "move": {"scale": [1.3, 1.3], "y": [400, 400]},
         "marks": [{"x0": 200, "y0": 1054, "x1": 690, "y1": 490, "text": "217 m", "at": t["b1_mark"], "out": t["b1_mark_out"],
                    "tpos": 0.72}]},   # label towards the far end, clear of the source line
        {"beat": "b2", "kind": "video", "file": "clips/gs_fb_clip_hall.mp4", "from": 0, "to": t["b2_to"], "box": FULL,
         "enter": "swipe", "exit": "wipe", "shade": 0.68},
        {"beat": "b3", "kind": "image", "file": "gs_fb_bulkhead.png", "from": f"@{t['b3_bulk']}-0.15", "to": f"@{t['b3_then']}",
         "box": FULL, "enter": "fade", "exit": "cut", "shade": 0.45, "move": {"scale": [1.0, 1.06]},
         "marks": [{"x0": 365, "y0": 590, "x1": 950, "y1": 590, "text": t["mark_bulk"], "at": f"@{t['b3_bulk']}+0.2"}]},
        {"beat": "b3", "kind": "video", "file": "clips/gs_fb_clip_flood.mp4", "from": f"@{t['b3_then']}", "to": "%1", "box": FULL,
         "enter": "swipe", "exit": "fade", "shade": 0.45},
        {"beat": "b4", "kind": "strip", "files": ["gs_fb_rebar.png", "gs_fb_tube_inside.png"], "from": 0, "to": f"@{t['b4_to']}",
         "box": [36, 36, 1008, 1848], "tile_w": 700, "enter": "fade", "exit": "wipe", "shade": 0.5},
        # T2: the pontoon clip only carries the date; "the first element was lowered" runs on the underwater clip,
        # where the element visibly sinks (in the pontoon clip it does not)
        {"beat": "b6", "kind": "video", "file": "clips/gs_fb_clip_pontoon.mp4", "from": 0, "to": t["b6_cut"], "box": FULL,
         "enter": "fade", "exit": "cut", "shade": 0.5},
        {"beat": "b6", "kind": "video", "file": "clips/gs_fb_clip_underwater.mp4", "from": t["b6_cut"], "to": "%1", "box": FULL,
         "enter": "cut", "exit": "fade", "shade": 0.5},
        {"beat": "b7", "kind": "image", "file": "gs_fb_sea_dawn.png", "from": 0, "to": f"@{t['b7_to']}", "box": FULL,
         "enter": "fade", "exit": "wipe", "shade": 0.35, "move": {"scale": [1.0, 1.05]}},
    ]

    def w(beat, word, cue):
        return {"beat": beat, "word": word, "cue": cue}

    def wipe(beat, spec):   # the wipe starts 0.9 s before the media item's end word
        return {"beat": beat, **timing.before(beat, spec.lstrip("@").split("-")[0].split("+")[0], 0.9, "swipe2"), "cue": "swipe2"}

    calc = t["b5_calc"]
    lay["sound"] = {"palette": "tech", "mood": "dark", "levels": {"sfx_peak_db": -18}}   # "Hafen und Stahl"; sweeps 2 dB under the
    # shared -16 dBFS (03.11.: at -16 overlapping cues made the effects stem peak at -15.9 dBFS, Stefan: effects too loud)
    lay["sound_cues"] = [
        {"beat": "b1", "at": 0.05, "cue": "whoosh2"},            # title over the tow
        w("b1", t["b1_mark"][1:], "paper"),                       # dimension line 217 m
        wipe("b1", t["b1_to"]),                                   # picture -> drawing
        w("b1", t["b1_tag"], "click"),                            # place tag
        wipe("b2", t["b2_to"]),
        w("b2", t["b2_load"], "thud"),                            # load box
        w("b2", t["b2_goal"], "click"),                           # goal
        w("b3", t["b3_bulk"], "stamp_leise"),                     # steel bulkhead
        w("b3", t["b3_then"], "whoosh"),                          # flood clip swipes in
        w("b3", t["b3_rule"], "click"),                           # rule
        w("b4", t["b4_rows"][0], "click"),
        wipe("b4", t["b4_to"]),                                   # filmstrip -> model
        *(w("b4", r, "click") for r in t["b4_rows"][1:]),
        *({"beat": "b5", **_tower_cue(timing, t["b5_tower"], k)} for k in range(7)),   # towers land on the balance
        w("b5", calc[0], "paper"), w("b5", calc[1], "stamp_leise"), w("b5", calc[2], "paper"), w("b5", calc[3], "stamp_leise"),
        w("b6", t["b6_stamp"], "stamp"),                          # test stamp
        {"beat": "b6", "word": t["b6_cut"].lstrip("@").split("-")[0], "cue": "thud"},   # cut under water
        wipe("b7", "@" + t["b7_to"]),
        w("b7", t["b7_follow"], "click"),
    ]
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", choices=sorted(L))
    ap.add_argument("--timing", default=None, help="folder of a timed run with the same voice (plan.timed.json, captions.json)")
    a = ap.parse_args()
    p = build(a.lang, Timing(ROOT / a.timing if a.timing else None))
    dst = ROOT / "data" / "direction" / f"megaconstruction-20261109-2-{a.lang}.T1.json"
    dst.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    n_at = sum(1 for c in p["layout"]["sound_cues"] if "at" in c)
    print(f"{dst.name}: {len(p['beats'])} beats, {len(p['layout']['media'])} media, {len(p['layout']['sound_cues'])} cues ({n_at} timed)")


if __name__ == "__main__":
    main()
