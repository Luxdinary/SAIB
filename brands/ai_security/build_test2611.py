"""Testvideo 11/2026 ("Du sitzt am Platz"): plan T1 of the reel "Die Mail vom Chef" from the checked F2 plan, DE and EN.

DE: the spoken text stays exactly as in F2 (the paid Flash voice is reused, no Gemini request). EN (03.11.2026, after
Stefan's approval): the EN F2 plan with the same scenes, material and cues; three spoken lines brought closer to the
German text ("Decide now.", the reply rule, the emergency step). Scene types change to the office format of buero.py,
every beat gets its photos/clips and sound cues. Concept:
OneDrive\\Business\\02 Marke\\Scutoria\\Testvideo-Konzept Reels 2026-11.md. Run from the repository root:
    .venv/Scripts/python.exe brands/ai_security/build_test2611.py [de|en]
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRECTION = ROOT / "data" / "direction"
M = "test2611/"

SCREEN_B1 = [176, 500, 708, 384]      # monitor of B1a in frame pixels, measured on the 1080x1920 crop (03.11.2026)
SCREEN_B2 = [150, 200, 900, 580]      # monitor of B2
CLOCK_B4 = {"file": M + "B4.png", "cx": 534, "cy": 970, "r": 430}

# per language: word anchors and texts that are not in the F2 plan
LANG = {
    "de": {"vid": "ai_security-20261110-1-de", "mail": "@Mail", "flag": "@Ausland+0.3",
           "fields": {"Absender": "from", "Thema": "subject", "Konto": "line:2"},
           "think": "@Nummer", "pay_at": "@erledigen+0.4", "stamp": ("Rückruf", "@Rückruf")},
    "en": {"vid": "ai_security-20261110-1-en", "mail": "@email", "flag": "@abroad+0.3",
           "fields": {"Sender": "from", "Topic": "subject", "Account": "line:2"},
           "addr": "tom@electrical.example",            # shorter than the F2 address, which ran into the mail time
           "think": "@number", "pay_at": "@ahead+0.4", "stamp": ("Call back", "@calling"),
           "spoken": {  # closer to the German text than the F2 localisation
               "b3": "What do you do? A: You pay, your boss is in a hurry. B: You reply to the email and ask. "
                     "C: You call your boss on the number you know. Decide now.",
               "b5": "The right answer is C. Police advise: for unusual payments, check the sender's address and confirm "
                     "the order by calling back. A reply to the same email goes back to the sender.",
               "b6": "Already paid? Then call your bank immediately, ask them to recall the transfer, and report it to the police."},
           "hint": "Decide now.", "strike_b": "@reply", "b6_sources_at": "@immediately"},
}

# cue name in the beat data -> (sound of the shared sound layer, gain dB); None = not available there (left out)
CUE_SOUNDS = {"keys_typing": ("tastatur", -6), "mail_in": ("pop", 0), "tick": ("tick", 0), "click": ("click", -3),
              "whoosh_soft": ("whoosh", -6), "stamp_soft": ("stamp", -4), "freeze": ("thud", -6), "pop": ("pop", -3),
              "clock_tick": ("tick", 0), "thud_low": ("thud", 0), "chime_soft": ("chime", -4), "phone_pickup": ("klack", -2),
              "pen_strike": ("paper", -4), "music_off": None, "music_on": None, "dial_tone": None, "music_up": None}


def sound_cues(plan: dict, vid: str) -> list[dict]:
    """layout.sound_cues for the shared sound layer (docs/direction-system.md 6i). The cue times of the beat data use
    "@Wort+0.4"; the layer reads "@Wort" without offset, so the times come as beat seconds from the last build of T1
    (project/sound_cues.json, written by buero.LAYER; same voice, same word timings). Without that file: "@Wort"."""
    run = ROOT / "storage" / "direction" / f"{vid}-T1"
    resolved_f, timed_f = run / "project" / "sound_cues.json", run / "plan.timed.json"
    starts, resolved = {}, []
    if resolved_f.exists() and timed_f.exists():
        starts = {b["id"]: float(b["start"]) for b in json.loads(timed_f.read_text(encoding="utf-8"))["beats"]}
        resolved = json.loads(resolved_f.read_text(encoding="utf-8"))
    wanted = {(b["id"], c["cue"], str(c["at"])) for b in plan["beats"] for c in b["data"].get("cues", [])}
    out = []
    for c in resolved:
        snd = CUE_SOUNDS.get(c["cue"])
        if snd is None or c["beat"] not in starts or (c["beat"], c["cue"], str(c["anchor"])) not in wanted:
            continue
        at = round(c["t"] - starts[c["beat"]], 3)
        out.append({"beat": c["beat"], "at": at, "cue": snd[0], "gain_db": snd[1], "src": c["cue"]})
        if c["cue"] == "clock_tick":                   # the second hand jumps twice more
            out += [{"beat": c["beat"], "at": round(at + k, 3), "cue": "tick", "gain_db": -2, "src": "clock_tick"} for k in (1, 2)]
    # two sounds on the same instant add up (T2 measured -13.9 dBFS on the sfx stem, 03.11.2026): keep 0.18 s between cues
    out.sort(key=lambda x: (x["beat"], x["at"]))
    for prev, cur in zip(out, out[1:]):
        if cur["beat"] == prev["beat"] and cur["at"] - prev["at"] < 0.18:
            cur["at"] = round(prev["at"] + 0.18, 3)
    if not out:
        for b in plan["beats"]:
            for c in b["data"].get("cues", []):
                snd = CUE_SOUNDS.get(c["cue"])
                if snd:
                    a = c["at"]
                    a = "@" + str(a)[1:].split("+")[0] if isinstance(a, str) and a.startswith("@") else a
                    out.append({"beat": b["id"], "at": a, "cue": snd[0], "gain_db": snd[1], "src": c["cue"]})
    return out


def build(lang: str) -> Path:
    L = LANG[lang]
    src, dst = DIRECTION / f"{L['vid']}.F2.json", DIRECTION / f"{L['vid']}.T1.json"
    plan = json.loads(src.read_text(encoding="utf-8"))
    out = copy.deepcopy(plan)
    out["notes"] = ("T1 (Testvideo 11/2026, Format \"Du sitzt am Platz\"): Text und Quellen wie F2"
                    + (", Stimme aus F2 wiederverwendet" if lang == "de" else ", drei Sätze näher am deutschen Text, neue Flash-Stimme")
                    + "; Bilder und Clips Higgsfield (assets/higgsfield/test2611, LICENSE.md). " + plan.get("notes", ""))
    out["assets"] = {}
    b = {x["id"]: x for x in out["beats"]}
    for bid, text in L.get("spoken", {}).items():
        b[bid]["spoken"] = text
    if L.get("addr"):
        b["b1"]["data"]["mail"]["addr"] = L["addr"]
    mail = copy.deepcopy(b["b1"]["data"]["mail"])

    b["b1"]["scene_type"] = "sb_screen"
    b["b1"]["data"].update({
        "media": {"screen": SCREEN_B1, "shots": [{"still": M + "B1a.png", "clip": M + "C1_typing.mp4", "at": 0, "move": "push"}]},
        "cues": [{"cue": "keys_typing", "at": 0}, {"cue": "mail_in", "at": L["mail"]}, {"cue": "tick", "at": L["flag"]}],
    })

    d2 = b["b2"]["data"]
    for r in d2["rows"]:
        r["field"] = L["fields"].get(r["label"], "from")
    b["b2"]["scene_type"] = "sb_lens"
    d2.update({
        "mail": mail,
        "media": {"screen": SCREEN_B2, "shots": [{"still": M + "B2.png", "at": 0, "move": "still"}]},
        "cues": ([{"cue": "click", "at": r["at"]} for r in d2["rows"]]      # no whoosh on the same instant (stem peak)
                 + [{"cue": "tick", "at": f'{r["at"]}+0.4'} for r in d2["rows"]]
                 + [{"cue": "stamp_soft", "at": d2["fact"]["at"]}]),
    })

    d3 = b["b3"]["data"]
    b["b3"]["scene_type"] = "sb_freeze"
    d3["think"] = {"seconds": 2.0, "at": L["think"]}   # the voice has no pause after "Decide now": clock and hint from "number"
    if L.get("hint"):
        d3["hint"] = L["hint"]
    d3.update({
        "clock": CLOCK_B4,
        "media": {"shots": [{"still": M + "B5b.png", "at": 0, "move": "push", "grey_at": 0.05}]},
        "cues": ([{"cue": "freeze", "at": 0}] + [{"cue": "pop", "at": o["at"]} for o in d3["options"]]
                 + [{"cue": "music_off", "at": d3["think"]["at"]}, {"cue": "clock_tick", "at": d3["think"]["at"]},
                    {"cue": "music_on", "at": f'{d3["think"]["at"]}+{d3["think"]["seconds"]}'}]),
    })

    d4 = b["b4"]["data"]
    b["b4"]["scene_type"] = "sb_montage"
    d4.pop("headline", None)
    d4["items"][2]["at"] = L["pay_at"]                 # "you pay" is followed by "Monday" within 0.8 s
    at = [it["at"] for it in d4["items"]]
    d4.update({
        "media": {"shots": [{"still": M + "B2.png", "clip": M + "C2_mouse.mp4", "at": 0, "move": "still"},   # C2 zooms a little: no overlay on it
                            {"still": M + "B3.png", "clip": M + "C3_corridor.mp4", "at": at[1], "move": "still"},
                            {"still": M + "B5b.png", "at": at[2], "move": "push"},
                            {"still": M + "B6c.png", "clip": M + "C4_monday.mp4", "at": at[3], "move": "still", "flash": True}]},
        "cues": ([{"cue": "whoosh_soft", "at": a} for a in at] + [{"cue": "stamp_soft", "at": f"{a}+0.1"} for a in at[:3]]
                 + [{"cue": "thud_low", "at": at[3]}]),
    })

    d5 = b["b5"]["data"]
    b["b5"]["scene_type"] = "sb_action"
    if L.get("strike_b"):
        d5["strikes"][1]["at"] = L["strike_b"]
    stamp, stamp_at = L["stamp"]
    d5.update({
        "stamp": {"text": stamp, "at": stamp_at},
        "media": {"shots": [{"still": M + "B7.png", "clip": M + "C5_phone.mp4", "at": 0, "move": "still"}]},
        "cues": ([{"cue": "chime_soft", "at": d5["card"]["at"]}, {"cue": "phone_pickup", "at": stamp_at},
                  {"cue": "dial_tone", "at": f"{stamp_at}+0.6"}]
                 + [{"cue": "pen_strike", "at": f'{s["at"]}+0.35' if isinstance(s["at"], str) else s["at"] + 0.35} for s in d5["strikes"]]),
    })

    d6 = b["b6"]["data"]
    b["b6"]["scene_type"] = "sb_action"
    if L.get("b6_sources_at"):
        d6["sources_at"] = L["b6_sources_at"]
    d6.update({
        "media": {"shots": [{"still": M + "B8.png", "at": 0, "move": "push"}]},
        "cues": [{"cue": "whoosh_soft", "at": 0}] + [{"cue": "tick", "at": s["at"]} for s in d6["steps"]],
    })

    b["b7"]["data"].update({
        "media": {"shots": [{"still": M + "B9.png", "at": 0, "move": "push"}], "dim": 0.5},
        "cues": [{"cue": "music_up", "at": 0}, {"cue": "chime_soft", "at": b["b7"]["data"].get("rule_at", 0.3)}],
    })
    # own cues replace the automatic ticks; sweeps 3 dB under the shared -16 dBFS (Stefan 03.11.2026: effects too loud)
    out["layout"]["sound"] = {"palette": "tech", "mood": "dark", "events": False, "levels": {"sfx_peak_db": -19}}
    out["layout"]["sound_cues"] = sound_cues(out, L["vid"])
    dst.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dst


if __name__ == "__main__":
    for lg in (sys.argv[1:] or ["de"]):
        print(build(lg))
