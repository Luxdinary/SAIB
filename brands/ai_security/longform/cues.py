"""Sound cues for one chapter project: transitions, heads and markers of the world, the sounds the acts register
with klang(), inserts and chapter cards. Output: <project>/cues.json for the shared sound layer (main session).

Names are proposals in Scutoria's sound colour (calm, dry, paper and office; no alarm, no siren, no bass drop):
whoosh_soft, swish_soft, swipe, tick, click_soft, stamp_soft, paper_slide, keys_typing, pop, clock_tick, strike,
thud_low, chime_soft. The music bed is one calm synth carpet under the whole video, ducked under the voice.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRANSITION = {"kreis": "whoosh_soft", "kreisRaus": "whoosh_soft", "schieben": "whoosh_soft", "schwarz": "whoosh_soft", "blende": "swish_soft"}
MUSIC = {"bed": "calm_synth_70_80bpm", "under_voice_db": -18, "in_pauses_db": -12, "end_image": "rise_then_fade_20s",
         "pause_for_thinking": "music drops out for the thinking bar in the A/B/C choices",
         "license": "open: only with a licence record in 08 Recht und Verwaltung\\Lizenzen (Stefan decides the source)"}


def world_events(project: Path) -> dict:
    p = subprocess.run(["node", str(HERE / "welt_check.mjs"), str(project)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    return json.loads(p.stdout)


def write(project: Path, offset: float, length: float, seg: dict) -> dict:
    ev = world_events(project) if seg.get("welt") else {"schnitte": [], "koepfe": [], "marken": [], "klang": [], "fehlt": [], "errors": []}
    cues: list[dict] = []

    def add(t: float, name: str, dauer: float = 0.0, laut: float = 1.0, quelle: str = "") -> None:
        local = round(t - offset, 3)
        if 0.0 <= local <= length:
            cues.append({"t": local, "sfx": name, "dauer": dauer, "laut": laut, "von": quelle})

    for s in ev.get("schnitte", []):
        if s["typ"] in TRANSITION and s["t"] > 0.5:
            add(s["t"], TRANSITION[s["typ"]], laut=0.8 if s["typ"] != "blende" else 0.5, quelle=f"Übergang {s['typ']}")
    for t in ev.get("koepfe", []):
        add(t, "tick", laut=0.35, quelle="Kopf")
    for m in ev.get("marken", []):
        add(m["t"], "stamp_soft", laut=0.6, quelle=f"Marker {m['art']}")
    for k in ev.get("klang", []):
        add(k["t"], k["name"], k.get("dauer", 0), k.get("laut", 1), "Akt")
    for c in seg.get("cards", []):
        cues.append({"t": round(c["start"], 3), "sfx": "whoosh_soft", "dauer": 0, "laut": 0.8, "von": "Kapitelkarte"})
    for ins in seg.get("inserts", []):
        cues.append({"t": round(ins["start"], 3), "sfx": "swipe", "dauer": 0, "laut": 0.7, "von": f"Einschub {Path(ins['file']).name}"})
        cues.append({"t": round(ins["start"] + ins["dur"] - 0.35, 3), "sfx": "swipe", "dauer": 0, "laut": 0.5, "von": "Einschub Ende"})
    cues.sort(key=lambda c: c["t"])
    thinned, last = [], {}
    for c in cues:                                    # at most one cue of the same name within 0.6 s
        if c["t"] - last.get(c["sfx"], -9) >= 0.6:
            thinned.append(c)
            last[c["sfx"]] = c["t"]
    out = {"chapter_seconds": round(length, 3), "voice_start": seg.get("voice_start"), "music": MUSIC, "cues": thinned,
           "check": {"missing_anchors": ev.get("fehlt", []), "errors": ev.get("errors", [])}}
    (project / "cues.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return out
