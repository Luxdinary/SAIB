"""Sound for a range of world chapters through the shared sound layer (fn.render.sound): the chapter cues.json files
(from cues.py) become sound.Cue objects on one continuous timeline, the chapter voices are laid at their global
offsets, and sound.mix_sound writes one mix (voice + sfx + procedural bed, ducked under the voice).

One mix over the whole range instead of one per chapter, so the bed runs through chapter cuts without restarting.
For the full video the range is all chapters and the mix goes under the concatenated picture.

Scutoria setting (main session 03.11.): palette subtle, mood dark, quiet bed (music_db -15 instead of -10).
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

import numpy as np

from fn.render import sound

SETTING = {"palette": "subtle", "mood": "dark", "levels": {"music_db": -15.0}}

# cue names of cues.py and the acts' klang() -> (sound.py sound, extra gain dB, role)
# role "event" sits at event_peak_db (-20), everything else at sfx_peak_db (-9)
NAMES = {
    "whoosh_soft": ("whoosh", -6.0, "scene_change"),
    "swish_soft": ("swipe2", -8.0, "scene_change"),
    "swipe": ("swipe", -4.0, "plan"),
    "tick": ("tick", 0.0, "event"),
    "clock_tick": ("tick", 0.0, "event"),
    "click_soft": ("click", 0.0, "event"),
    "stamp_soft": ("stamp", -5.0, "plan"),     # sound.py adds -3 dB for stamp
    "paper_slide": ("paper", -3.0, "plan"),
    "pop": ("pop", 0.0, "event"),
    "strike": ("swipe2", -4.0, "plan"),
    "thud_low": ("thud", -6.0, "plan"),
    "chime_soft": ("chime", -8.0, "plan"),
}
KEY_STEP = (0.11, 0.19)          # keys_typing: single clicks at a human pace


def to_cues(cq: dict, shift: float, seed: int = 7) -> tuple[list[sound.Cue], list[str]]:
    """cues.json of one chapter -> sound cues on the range timeline (chapter-local t + shift)."""
    out, problems = [], []
    rnd = random.Random(seed)
    for c in cq["cues"]:
        name, at = c["sfx"], c["t"] + shift
        laut = max(0.05, float(c.get("laut", 1.0) or 1.0))
        g_laut = 20 * math.log10(laut)
        note = c.get("von", "")
        if name == "keys_typing":
            t, end = at, at + max(0.4, float(c.get("dauer") or 1.5))
            while t < end:
                out.append(sound.Cue(t, "click", "event", g_laut - 4 + rnd.uniform(-3, 1), rnd.uniform(-0.25, 0.25), "plan", note=note))
                t += rnd.uniform(*KEY_STEP)
            continue
        if name in NAMES:
            snd, g, role = NAMES[name]
        else:
            kind, val, g = sound.normalize_cue(name)
            if kind != "sound":
                problems.append(f"unknown cue {name!r} at {at:.2f} s ({note}): dropped")
                continue
            snd, role = val, "plan"
        out.append(sound.Cue(at, snd, role, g + g_laut, 0.0, "plan", note=note))
    return out, problems


def voice_track(parts: list[tuple[Path, float]], total: float, dst: Path) -> Path:
    """One mono voice file of `total` seconds with each chapter wav at its start time."""
    n = int(round((total + 0.05) * sound.SR))
    tl = np.zeros(n)
    for wav, at in parts:
        sound._place(tl, sound.decode(wav, sound.SR, 1), at)
    sound.write_wav(dst, tl, bits=16)
    return dst


def mix_range(plan: dict, timed: dict, offsets: dict, ids: list[str], projects: dict, out_dir: Path, *,
              brand_dir: Path | None = None, final: bool = False) -> dict:
    """Mix chapters `ids` (consecutive) into out_dir/mix.wav. `projects[cid]` holds that chapter's cues.json."""
    out_dir.mkdir(parents=True, exist_ok=True)
    base = offsets[ids[0]]
    total = offsets[ids[-1]] + timed[ids[-1]]["total"] - base
    cues_all, problems, parts = [], [], []
    for i, cid in enumerate(ids):
        tm, shift = timed[cid], offsets[cid] - base
        parts.append((Path(tm["wav"]), shift + tm["vstart"]))
        cq = json.loads((projects[cid] / "cues.json").read_text(encoding="utf-8"))
        cs, pr = to_cues(cq, shift, seed=i + 7)
        cues_all += cs
        problems += pr
    cues_all.sort(key=lambda c: c.at)
    if final:
        cues_all.append(sound.Cue(max(0.0, total - 3.0), "", "music_out", note="chord"))
    voice = voice_track(parts, total, out_dir / "voice_range.wav")
    cfg = sound.config_for(None, overrides=SETTING)
    res = sound.mix_sound(voice, cues_all, cfg, out_dir / "mix.wav", total=total, voice_start=0.0, brand_dir=brand_dir,
                          video_id=plan["video_id"], work_dir=out_dir)
    report = {"chapters": ids, "start_in_video": round(base, 3), "seconds": round(total, 3), "setting": SETTING,
              "cues": len(res.cues), "music": res.music, "measured": res.measured, "problems": problems + res.problems,
              "licenses": res.licenses}
    (out_dir / "mix.json").write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return report


def reel_cues(scenes: list[dict], inserts: list[dict], span: float, total: float) -> dict:
    """cues.json-like dict for a reel (scene changes, markers, inserts, end card); times are reel-local seconds."""
    cues = []

    def add(t: float, name: str, laut: float, von: str) -> None:
        if 0.0 <= t <= total:
            cues.append({"t": round(t, 3), "sfx": name, "dauer": 0, "laut": laut, "von": von})

    for k, s in enumerate(scenes):
        if k:
            add(s["start"], "whoosh_soft", 0.8, "Szenenwechsel")
        for m in s.get("marks", []):
            if m.get("marker") or m.get("source"):
                add(m["start"], "stamp_soft", 0.6, "Marker")
    for ins in inserts:
        add(ins["start"], "swipe", 0.7, "Einschub")
        add(ins["start"] + ins["dur"] - 0.35, "swipe", 0.5, "Einschub Ende")
    add(span, "whoosh_soft", 0.8, "Endkarte")
    cues.sort(key=lambda c: c["t"])
    thinned, last = [], {}
    for c in cues:
        if c["t"] - last.get(c["sfx"], -9) >= 0.6:
            thinned.append(c)
            last[c["sfx"]] = c["t"]
    return {"cues": thinned}


def mix_reel(video_id: str, reel_id: str, voice: Path, scenes: list[dict], inserts: list[dict], span: float, total: float,
             out_dir: Path, brand_dir: Path | None = None) -> dict:
    """One reel mix (voice clip + cues + quiet bed with closing chord) -> out_dir/mix.wav; returns the report dict."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cq = reel_cues(scenes, inserts, span, total)
    cues, problems = to_cues(cq, 0.0, seed=sum(map(ord, reel_id)))
    cues.append(sound.Cue(max(0.0, total - 3.0), "", "music_out", note="chord"))
    cues.sort(key=lambda c: c.at)
    cfg = sound.config_for(None, overrides=SETTING)
    res = sound.mix_sound(voice, cues, cfg, out_dir / "mix.wav", total=total, voice_start=0.0, brand_dir=brand_dir,
                          video_id=f"{video_id}-{reel_id}", work_dir=out_dir)
    rep = {"reel": reel_id, "cues": len(res.cues), "music": res.music, "measured": res.measured,
           "problems": problems + res.problems, "licenses": res.licenses, "path": str(res.path)}
    (out_dir / "mix.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return rep
