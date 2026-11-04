"""Sound layer (Tonebene) of the shared renderer: cue points from the plan, a brand palette of procedural sound
effects, a procedural (or licensed) music bed ducked under the voice, and the mix that goes under the video.

Pipeline (scripts/render_direction.py): plan + word timings -> `cues_from_plan()` -> `mix_sound()` ->
`ffmpeg.encode_nvenc(raw, video, audio=mix.path)`; loudnorm, aresample and alimiter stay at the very end.

Reusable without the 9:16 path (e.g. brands/ai_security/longform, 16:9):

    from fn.render import sound
    cfg = sound.config_for(brand)                              # or sound.SoundConfig(palette="tech", mood="dark")
    cues = sound.auto_cues(scene_starts, total, cfg, hook_end=..., close_start=..., events=[...])
    mix = sound.mix_sound(voice_wav, cues, cfg, out_wav, total=total, voice_start=0.4, video_id="...")
    ffmpeg.encode_nvenc(raw, out_mp4, audio=mix.path, loudness_lufs=-16.0)

Brand configuration (brands/<id>/brand.yaml, key `sound`, read as brand.design["sound"]; all optional):

    sound:
      palette: tech                 # subtle (default) | tech | paper | soft | none, or a list of sound names
      sounds: {transition: [whoosh, whoosh2], event: click, hook_end: stamp, close: swipe2, outro: stamp, intro: null}
      levels: {sfx_peak_db: -16, event_peak_db: -20, music_db: -10, duck_db: 5}
      music: procedural             # procedural | none | <file>.wav (brands/<id>/assets/music or assets/music, licence required)
      mood: calm                    # calm | tech | warm | dark | bright (procedural bed)
      events: true                  # ticks at the templates' visual events (thinned to event_min_gap)
      event_min_gap: 1.2
      seed: 7                       # optional; default from the video id

Plan: `layout.sound` (same keys, overrides the brand), `layout.sound_cues` (list of {beat, at|word|event, cue,
gain_db, pan}) and a `sound` field per beat ("stamp", {"cue": "stamp", "at": 1.2}, or a list). Cue names: the
sound names (whoosh, whoosh2, swipe, swipe2, click, tick, stamp, paper, pop, thud, chime, riser), German aliases
(papier, klick, stempel, wusch, wischen ...), roles (transition, event, hook_end, close, outro) and the music
controls bett_ein / bett_aus / bett_aus_schlussakkord. `_leise` lowers a cue by 6 dB.

Levels: the voice stays the lead at -16 LUFS (static gain, then a peak limiter at -2.5 dBFS); sweeps peak at
-16 dBFS (Stefan, 03.11.2026: -9 dBFS was too loud), short impulses lower by default (click -8, tick -10, pop -5,
stamp -3, thud -2, chime -4 dB), event ticks at -20 dBFS regardless, the sfx stem never above -6 dBFS; the bed sits
`music_db` (10 dB) under the voice as measured in the mix
and a further `duck_db` (5 dB) while speaking (envelope ducker: attack 50 ms, hold 250 ms, release 600 ms; a sidechain
compressor with a fixed depth); the whole mix is limited at -2 dBFS. The encode then runs loudnorm in linear
(two-pass) mode, so nothing is lifted in pauses. Measured values go to manifest.json `sound.measured`, checked by
fn.direction.checks.check_sound (stem peak and the encoded peak around the cues).
"""
from __future__ import annotations

import json
import re
import subprocess
import zlib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from ..config import ASSETS_DIR, mirror_dir
from . import ffmpeg
from . import sound_synth as synth
from .sound_synth import SR, write_wav

VERSION = "1.0"
SOUND_NAMES = list(synth.SFX)
TRANSITION_SOUNDS = ("whoosh", "whoosh2", "swipe", "swipe2", "paper", "riser")
ACCENT_SOUNDS = ("stamp", "thud", "chime", "pop")
ROLES = ("transition", "event", "hook_end", "close", "outro", "intro")
AUTO_ROLES = ("scene_change", "hook_end", "close", "outro", "intro")

PALETTES: dict[str, dict] = {
    "subtle": {"transition": ["swipe", "swipe2"], "event": "tick", "hook_end": "whoosh", "close": "whoosh2", "outro": "thud", "intro": None},
    "tech": {"transition": ["whoosh", "whoosh2"], "event": "click", "hook_end": "stamp", "close": "swipe2", "outro": "stamp", "intro": None},
    "paper": {"transition": ["paper", "swipe"], "event": "tick", "hook_end": "stamp", "close": "paper", "outro": "thud", "intro": "paper"},
    "soft": {"transition": ["swipe", "whoosh2"], "event": "pop", "hook_end": "chime", "close": "swipe2", "outro": "chime", "intro": None},
    "none": {"transition": None, "event": None, "hook_end": None, "close": None, "outro": None, "intro": None},
}
DEFAULT_PALETTE = "subtle"
# sfx_peak_db: Stefan, 03.11.2026 ("die Wisch-Geräusche sind in allen Videos zu laut"): sweeps were at -9 dBFS, now -16.
DEFAULT_LEVELS = {"voice_lufs": -16.0, "sfx_peak_db": -16.0, "event_peak_db": -20.0, "music_db": -10.0, "duck_db": 5.0,
                  "sfx_max_peak_db": -6.0, "voice_ceiling_db": -3.5, "mix_ceiling_db": -3.0}
DEFAULT_EVENT_MIN_GAP = 1.2
# Short impulse sounds sit lower than the sweeps by default (Gritwerk finding 03.11.2026: click/tick/stamp at the full
# sfx level reached 0.0 dB after loudnorm and AAC). Offsets in dB on top of `sfx_peak_db`; a plan `gain_db` adds to it.
SOUND_LEVEL_OFFSETS: dict[str, float] = {"click": -8.0, "tick": -10.0, "pop": -5.0, "stamp": -3.0, "thud": -2.0, "chime": -4.0}
MUSIC_FADE_IN, MUSIC_FADE_OUT = 1.5, 2.5
PROCEDURAL_LICENSE = ("selbst erzeugt im Renderer (fn.render.sound_synth, additive Synthese, mathematisch), "
                      "keine Samples, keine Rechte Dritter")

ALIASES: dict[str, str] = {
    "papier": "paper", "rascheln": "paper", "blatt": "paper", "paper": "paper",
    "klick": "click", "klack": "click", "schnitt_klick": "click", "schnittklick": "click", "enter_klack": "click",
    "enter": "click", "tastatur": "click", "taste": "click", "cursor": "click", "click": "click",
    "tick": "tick", "ticken": "tick", "ticker": "tick",
    "stempel": "stamp", "schlag": "stamp", "hit": "stamp", "stamp": "stamp",
    "marker": "pop", "plopp": "pop", "plop": "pop", "blase": "pop", "pop": "pop",
    "wusch": "whoosh", "woosh": "whoosh", "whoosh": "whoosh", "whoosh_auf": "whoosh", "whoosh2": "whoosh2",
    "whoosh_ab": "whoosh2", "wusch_ab": "whoosh2",
    "wischen": "swipe", "wisch": "swipe", "swipe": "swipe", "swipe2": "swipe2", "swipe_zurueck": "swipe2", "wisch_zurueck": "swipe2",
    "wumms": "thud", "dumpf": "thud", "thud": "thud",
    "glocke": "chime", "ping": "chime", "chime": "chime", "klang": "chime",
    "riser": "riser", "anstieg": "riser", "aufbau": "riser",
}
ROLE_ALIASES: dict[str, str] = {
    "transition": "transition", "uebergang": "transition", "szenenwechsel": "transition", "wechsel": "transition",
    "event": "event", "einblendung": "event", "ereignis": "event",
    "hook_end": "hook_end", "hook_ende": "hook_end", "hookende": "hook_end",
    "close": "close", "schluss": "close", "abschluss": "close",
    "outro": "outro", "abspann": "outro", "endkarte": "outro",
    "intro": "intro", "anfang": "intro", "start": "intro",
}
MUSIC_IN = ("bett_ein", "musik_ein", "music_in", "bed_in", "musik_an", "bett_an")
MUSIC_OUT = ("bett_aus", "musik_aus", "music_out", "bed_out")


# --- configuration ----------------------------------------------------------------------------------

@dataclass
class SoundConfig:
    enabled: bool = True
    palette: str = DEFAULT_PALETTE
    sounds: dict = field(default_factory=dict)        # role -> name | [names] | None, palette defaults filled in
    levels: dict = field(default_factory=lambda: dict(DEFAULT_LEVELS))
    music: str = "procedural"                         # procedural | none | <file>
    mood: str = synth.DEFAULT_MOOD
    events: bool = True
    event_min_gap: float = DEFAULT_EVENT_MIN_GAP
    seed: int | None = None
    music_license: str = ""                           # licence text of a file bed
    source: str = "defaults"

    def sound_for(self, role: str, index: int = 0) -> str | None:
        v = self.sounds.get(role)
        if isinstance(v, (list, tuple)):
            return str(v[index % len(v)]) if v else None
        return str(v) if v else None

    def level(self, key: str) -> float:
        return float(self.levels.get(key, DEFAULT_LEVELS[key]))

    def to_dict(self) -> dict:
        return {"enabled": self.enabled, "palette": self.palette, "sounds": dict(self.sounds), "levels": dict(self.levels),
                "music": self.music, "mood": self.mood, "events": self.events, "event_min_gap": self.event_min_gap,
                "seed": self.seed, "source": self.source}


def _palette_from_list(names: list) -> dict:
    """`palette: [whoosh, click, stamp]` -> roles: transitions from the transition sounds, ticks from the rest."""
    norm = [ALIASES.get(_slug(str(n)), _slug(str(n))) for n in names]
    trans = [n for n in norm if n in TRANSITION_SOUNDS] or ["swipe"]
    ev = next((n for n in norm if n in ("tick", "click", "pop")), None)
    acc = next((n for n in norm if n in ACCENT_SOUNDS), None)
    return {"transition": trans, "event": ev, "hook_end": acc or trans[0], "close": trans[-1], "outro": acc, "intro": None}


def _apply(cfg: SoundConfig, d: dict) -> None:
    if not isinstance(d, dict):
        return
    if "enabled" in d:
        cfg.enabled = bool(d["enabled"])
    pal = d.get("palette")
    if isinstance(pal, (list, tuple)):
        cfg.palette = "custom"
        cfg.sounds = {**cfg.sounds, **_palette_from_list(list(pal))}
    elif pal:
        name = _slug(str(pal))
        if name in PALETTES:
            cfg.palette = name
            cfg.sounds = {**PALETTES[name]}
        elif name == "custom":
            cfg.palette = "custom"
    if isinstance(d.get("sounds"), dict):
        for role, v in d["sounds"].items():
            r = ROLE_ALIASES.get(_slug(str(role)), _slug(str(role)))
            if r in ROLES:
                cfg.sounds[r] = v
    if isinstance(d.get("levels"), dict):
        for k, v in d["levels"].items():
            if k in DEFAULT_LEVELS and v is not None:
                cfg.levels[k] = float(v)
    if d.get("music") is not None:
        cfg.music = str(d["music"]).strip() or "procedural"
    if d.get("mood"):
        cfg.mood = _slug(str(d["mood"]))
    if "events" in d:
        cfg.events = bool(d["events"])
    if d.get("event_min_gap") is not None:
        cfg.event_min_gap = float(d["event_min_gap"])
    if d.get("seed") is not None:
        cfg.seed = int(d["seed"])
    if d.get("music_license"):
        cfg.music_license = str(d["music_license"])


def config_for(brand=None, layout: dict | None = None, overrides: dict | None = None) -> SoundConfig:
    """Defaults <- brand.yaml `sound` (and audio_style.yaml `music.file` as the licensed-music hook) <- plan
    `layout.sound` <- overrides. Unknown keys (e.g. free-text `klangfarbe`) are ignored."""
    cfg = SoundConfig(sounds={**PALETTES[DEFAULT_PALETTE]})
    src = []
    if brand is not None:
        d = (getattr(brand, "design", {}) or {}).get("sound")
        if isinstance(d, dict):
            _apply(cfg, d)
            src.append("brand.yaml")
        am = (getattr(brand, "audio", {}) or {}).get("music") or {}
        if isinstance(am, dict) and am.get("file") and not (isinstance(d, dict) and d.get("music")):
            cfg.music = str(am["file"])
            cfg.music_license = str(am.get("license_proof") or "")
            src.append("audio_style.yaml music.file")
    if layout and isinstance(layout.get("sound"), dict):
        _apply(cfg, layout["sound"])
        src.append("plan.layout.sound")
    if overrides:
        _apply(cfg, overrides)
        src.append("call")
    cfg.source = ", ".join(src) or "defaults"
    if cfg.mood not in synth.MOODS:
        cfg.mood = synth.DEFAULT_MOOD
    return cfg


# --- cues -------------------------------------------------------------------------------------------

@dataclass
class Cue:
    at: float
    sound: str                      # sound name, file name, or "" for music controls
    role: str = "plan"              # scene_change | event | hook_end | close | outro | intro | plan | file | music_in | music_out
    gain_db: float = 0.0
    pan: float = 0.0                # -1 left .. 1 right
    source: str = "auto"            # auto | plan | file
    path: Path | None = None        # resolved file for file cues
    note: str = ""
    seconds: float = 0.0            # length of the placed sample (filled by mix_sound; the encoded-peak check uses it)

    def to_dict(self) -> dict:
        d = {"at": round(self.at, 3), "sound": self.sound, "role": self.role, "source": self.source}
        if self.seconds:
            d["seconds"] = round(self.seconds, 3)
        if self.gain_db:
            d["gain_db"] = round(self.gain_db, 1)
        if self.pan:
            d["pan"] = round(self.pan, 2)
        if self.path is not None:
            d["file"] = self.path.name
        if self.note:
            d["note"] = self.note
        return d


def _slug(s: str) -> str:
    s = s.strip().lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[\s\-]+", "_", s)


def normalize_cue(name: str) -> tuple[str | None, str, float]:
    """Cue name -> (kind, value, gain_db): kind sound | role | file | music_in | music_out | None (unknown)."""
    raw = str(name or "").strip()
    if raw.lower().startswith("file:"):
        return "file", raw[5:].strip(), 0.0
    if raw.lower().endswith((".wav", ".mp3", ".flac", ".ogg", ".m4a")):
        return "file", raw, 0.0
    s = _slug(raw)
    gain = 0.0
    if s.endswith("_leise") or s.endswith("_soft") or s.endswith("_quiet"):
        s, gain = s.rsplit("_", 1)[0], -6.0
    elif s.endswith("_laut") or s.endswith("_loud"):
        s, gain = s.rsplit("_", 1)[0], 3.0
    if "schlussakkord" in s or s in ("music_out_chord", "bed_out_chord", "bett_aus_akkord"):
        return "music_out", "chord", 0.0
    if s in MUSIC_IN:
        return "music_in", "", 0.0
    if s in MUSIC_OUT:
        return "music_out", "", 0.0
    if s in ALIASES:
        return "sound", ALIASES[s], gain
    if s in ROLE_ALIASES:
        return "role", ROLE_ALIASES[s], gain
    return None, s, gain


def _norm_word(w: str) -> str:
    return re.sub(r"[^\wäöüß]", "", str(w).lower())


def word_time(words, spec: str) -> float | None:
    """Start of the n-th word beginning with `spec` ("Wort" or "Wort#2") among `words` (.text/.start)."""
    m = re.fullmatch(r"(.+?)(?:#(\d+))?", str(spec).strip())
    if not m:
        return None
    key, nth = _norm_word(m.group(1)), int(m.group(2) or 1)
    hits = [w for w in words if _norm_word(w.text).startswith(key)]
    return float(hits[nth - 1].start) if len(hits) >= nth else None


def auto_cues(scene_starts, total: float, cfg: SoundConfig, *, hook_end: float | None = None,
              close_start: float | None = None, outro_start: float | None = None, events=(),
              voice_start: float = 0.0) -> list[Cue]:
    """Derived cues: a transition at every scene start (the hook end and the close get their own sound), the
    outro hit, and ticks at the templates' visual events (thinned, never near a transition)."""
    cues: list[Cue] = []
    intro = cfg.sound_for("intro")
    if intro:
        cues.append(Cue(max(0.0, voice_start - 0.15), intro, role="intro"))
    k = 0
    for s in sorted(float(x) for x in scene_starts):
        if s <= 0.05 or s >= total - 0.3:
            continue
        role, snd, pan = "scene_change", cfg.sound_for("transition", k), (-0.3 if k % 2 == 0 else 0.3)
        if hook_end is not None and abs(s - hook_end) < 0.05 and cfg.sound_for("hook_end"):
            role, snd, pan = "hook_end", cfg.sound_for("hook_end"), 0.0
        if close_start is not None and abs(s - close_start) < 0.05 and cfg.sound_for("close"):
            role, snd, pan = "close", cfg.sound_for("close"), 0.0
        if snd:
            cues.append(Cue(s, snd, role=role, pan=pan))
        k += 1
    if outro_start is not None and cfg.sound_for("outro") and 0 < outro_start < total - 0.3:
        cues.append(Cue(float(outro_start), cfg.sound_for("outro"), role="outro"))
    ev_sound = cfg.sound_for("event")
    if cfg.events and ev_sound:
        bounds = [c.at for c in cues]
        stop = (outro_start if outro_start is not None else total) - 0.3
        last = -1e9
        for e in sorted({round(float(x), 3) for x in events}):
            if e < voice_start + 0.3 or e >= stop:
                continue
            if any(abs(e - b) < 0.35 for b in bounds):
                continue
            if e - last < cfg.event_min_gap:
                continue
            cues.append(Cue(e, ev_sound, role="event"))
            last = e
    return sorted(cues, key=lambda c: c.at)


def _resolve_time(spec: dict, beat, words, named: dict) -> tuple[float | None, str]:
    """Time of a plan cue inside `beat` (None if the beat has no timing): at start|end|seconds|w:Wort, word, event."""
    if beat is None:
        at = spec.get("at")
        return (float(at), "") if isinstance(at, (int, float)) else (None, "cue without beat needs a numeric 'at'")
    if beat.start is None or beat.duration is None:
        return None, f"beat {beat.id} has no timing"
    b0, b1 = float(beat.start), float(beat.start + beat.duration)
    beat_words = [w for w in words if b0 <= float(w.start) < b1]
    if spec.get("word"):
        t = word_time(beat_words, spec["word"])
        return (t, "") if t is not None else (None, f"word {spec['word']!r} not spoken in beat {beat.id}")
    if spec.get("event"):
        t = (named.get(beat.id) or {}).get(str(spec["event"]))
        if t is None:
            return None, f"event {spec['event']!r} not named by the scene of beat {beat.id} (SceneOut.named_events)"
        return float(t), ""
    at = spec.get("at", "start")
    if isinstance(at, str):
        a = at.strip().lower()
        if a.startswith(("w:", "@")):
            t = word_time(beat_words, a.split(":", 1)[1] if a.startswith("w:") else a[1:])
            return (t, "") if t is not None else (None, f"word {at!r} not spoken in beat {beat.id}")
        if a in ("start", "anfang", "beginn", ""):
            return b0, ""
        if a in ("end", "ende", "schluss"):
            return max(b0, b1 - 0.05), ""
        if a in ("mid", "mitte", "middle"):
            return (b0 + b1) / 2, ""
        try:
            at = float(a.replace(",", "."))
        except ValueError:
            return None, f"unknown 'at' {at!r} in beat {beat.id}"
    return min(b1 - 0.02, max(b0, b0 + float(at))), ""


def _file_cue(name: str, at: float, brand_dir: Path | None, gain_db: float, source: str) -> tuple[Cue | None, str]:
    p = Path(name)
    if not p.is_absolute():
        cands = ([brand_dir / "assets" / "sfx" / name] if brand_dir else []) + [ASSETS_DIR / "sfx" / name]
        p = next((c for c in cands if c.exists()), cands[-1])
    if not p.exists():
        return None, f"sfx file missing: {name} -> {p}"
    from .assets import _licenses                   # same `<file>: <text>` convention as the clip layer
    lic = _licenses(p.parent).get(p.name, "")
    return Cue(at, p.name, role="file", gain_db=gain_db, source=source, path=p, note=lic or "no licence line"), ("" if lic else f"sfx without licence line in {p.parent / 'LICENSE.md'}: {p.name}")


def plan_cues(plan, cfg: SoundConfig, *, words=(), named_events: dict | None = None, beat_sounds: dict | None = None,
              brand_dir: Path | None = None) -> tuple[list[Cue], list[str]]:
    """Cues written into the plan: layout.sound_cues, `data.sound` per beat and the top-level beat `sound` field
    (passed in `beat_sounds`, because story.Beat does not keep unknown keys)."""
    named = named_events or {}
    beats = {b.id: b for b in plan.beats}
    specs: list[tuple[dict, object]] = []
    for e in (plan.layout or {}).get("sound_cues") or []:
        if isinstance(e, dict):
            specs.append((e, beats.get(e.get("beat"))))
    for b in plan.beats:
        for raw in (b.data.get("sound"), (beat_sounds or {}).get(b.id)):
            for e in (raw if isinstance(raw, list) else [raw]):
                if isinstance(e, str):
                    specs.append(({"cue": e, "at": "start"}, b))
                elif isinstance(e, dict):
                    specs.append((e, b))
    cues: list[Cue] = []
    problems: list[str] = []
    k = 0
    for spec, beat in specs:
        if spec.get("beat") and beat is None:
            problems.append(f"sound cue for unknown beat {spec.get('beat')!r}")
            continue
        name = spec.get("cue") or spec.get("sound") or spec.get("name") or ""
        kind, value, g = normalize_cue(name)
        gain = g + float(spec.get("gain_db") or 0.0)
        pan = float(spec.get("pan") or 0.0)
        t, why = _resolve_time(spec, beat, words, named)
        if t is None:
            problems.append(f"{why}: cue {name!r} dropped")
            continue
        if kind == "music_in":
            cues.append(Cue(t, "", role="music_in", source="plan"))
        elif kind == "music_out":
            cues.append(Cue(t, "", role="music_out", source="plan", note=value))
        elif kind == "sound":
            cues.append(Cue(t, value, role="plan", gain_db=gain, pan=pan, source="plan"))
        elif kind == "role":
            snd = cfg.sound_for(value, k)
            k += 1
            if snd:
                cues.append(Cue(t, snd, role="plan", gain_db=gain, pan=pan, source="plan", note=f"role {value}"))
            else:
                problems.append(f"cue {name!r}: palette has no sound for role {value}")
        elif kind == "file":
            c, p = _file_cue(value, t, brand_dir, gain, "plan")
            if c is not None:
                cues.append(c)
            if p:
                problems.append(p)
        else:
            problems.append(f"unknown cue name {name!r} (beat {getattr(beat, 'id', '?')}); known: {', '.join(SOUND_NAMES)}")
    return sorted(cues, key=lambda c: c.at), problems


def merge_cues(auto: list[Cue], manual: list[Cue], total: float) -> list[Cue]:
    """Manual cues win: an automatic transition within 0.2 s of a manual cue and ticks within 0.35 s are dropped."""
    man_t = [m.at for m in manual if m.role not in ("music_in", "music_out")]
    out: list[Cue] = []
    for c in auto:
        near = 0.35 if c.role == "event" else 0.2
        if any(abs(c.at - t) < near for t in man_t):
            continue
        out.append(c)
    out += manual
    return sorted([c for c in out if c.role in ("music_in", "music_out") or 0.0 <= c.at < total - 0.02], key=lambda c: c.at)


def cues_from_plan(plan, cfg: SoundConfig, *, events=(), words=(), total: float, outro_start: float | None = None,
                   voice_start: float = 0.0, named_events: dict | None = None, beat_sounds: dict | None = None,
                   file_sfx=(), brand_dir: Path | None = None) -> tuple[list[Cue], list[str]]:
    """All cues of a timed DirectionPlan: automatic ones from the beats and events, plan cues, and the plan's
    `assets.sfx` files (`file_sfx`: iterable of (at, path, volume, licence))."""
    beats = [b for b in plan.beats if b.start is not None]
    starts = [float(b.start) for b in beats[1:]]
    hook_end = float(beats[0].start + beats[0].duration) if len(beats) > 1 else None
    # the close sound only for a real close beat (an --excerpt ends on whatever beat fits into the window)
    close = float(beats[-1].start) if len(beats) > 1 and getattr(beats[-1], "function", "close") == "close" else None
    auto = auto_cues(starts, total, cfg, hook_end=hook_end, close_start=close, outro_start=outro_start, events=events,
                     voice_start=voice_start)
    manual, problems = plan_cues(plan, cfg, words=words, named_events=named_events, beat_sounds=beat_sounds, brand_dir=brand_dir)
    for at, path, volume, lic in file_sfx:
        # the old `data-volume` (0..1, 0.5 = palette level) becomes a gain relative to sfx_peak_db
        gain = 20 * np.log10(max(0.01, float(volume)) / 0.5)
        manual.append(Cue(float(at), Path(path).name, role="file", gain_db=float(gain), source="file", path=Path(path), note=lic or "no licence line"))
    return merge_cues(auto, manual, total), problems


def cues_summary(cfg: SoundConfig, cues: list[Cue], problems: list[str]) -> dict:
    return {"version": VERSION, "config": cfg.to_dict(), "cues": [c.to_dict() for c in cues], "problems": list(problems),
            "counts": {r: sum(1 for c in cues if c.role == r) for r in sorted({c.role for c in cues})}}


# --- audio helpers ----------------------------------------------------------------------------------

def decode(path: Path, sr: int = SR, channels: int = 1) -> np.ndarray:
    """Decode any audio file with ffmpeg to float32 at `sr` (mono (n,) or stereo (n, 2))."""
    proc = subprocess.run([ffmpeg._bin("ffmpeg"), "-v", "error", "-i", str(path), "-f", "f32le", "-acodec", "pcm_f32le",
                           "-ac", str(channels), "-ar", str(sr), "-"], capture_output=True, check=True)
    x = np.frombuffer(proc.stdout, dtype=np.float32).astype(np.float64)
    return x.reshape(-1, channels) if channels > 1 else x


def _db(x: float) -> float:
    return float(10 ** (x / 20))


def _peak_db(x: np.ndarray) -> float | None:
    p = float(np.max(np.abs(x))) if x.size else 0.0
    return round(20 * np.log10(p), 2) if p > 0 else None


def duck_gain(voice: np.ndarray, duck_db: float, *, sr: int = SR, block: float = 0.01, attack: float = 0.05,
              hold: float = 0.25, release: float = 0.6, threshold_db: float = -40.0) -> np.ndarray:
    """Per-sample gain (1 .. 10^(-duck/20)) that follows speech: RMS per 10 ms block above `threshold_db`
    means speaking; attack 50 ms down, hold 250 ms, release 600 ms up (equivalent to a sidechain compressor
    with a fixed depth, but independent of how loud the voice happens to be)."""
    n = len(voice)
    bs = max(1, int(sr * block))
    nb = (n + bs - 1) // bs
    padded = np.zeros(nb * bs)
    padded[:n] = voice
    rms = np.sqrt(np.mean(padded.reshape(nb, bs) ** 2, axis=1))
    active = rms > _db(threshold_db)
    hold_b = int(round(hold / block))
    if hold_b > 0 and active.any():                 # hold: keep ducking for `hold` after the last active block
        idx = np.flatnonzero(active)
        ext = np.zeros(nb, dtype=bool)
        for i in idx:
            ext[i:i + hold_b + 1] = True
        active = ext
    target = np.where(active, _db(-abs(duck_db)), 1.0)
    ca, cr = 1 - np.exp(-block / max(attack, 1e-3)), 1 - np.exp(-block / max(release, 1e-3))
    g = np.empty(nb)
    cur = 1.0
    for i in range(nb):
        cur += (target[i] - cur) * (ca if target[i] < cur else cr)
        g[i] = cur
    return np.interp(np.arange(n), np.arange(nb) * bs + bs / 2, g)


def limit_peaks(x: np.ndarray, ceiling_db: float, *, sr: int = SR, block: float = 0.001, release: float = 0.06) -> tuple[np.ndarray, float]:
    """Brick-wall peak limiter with 1 ms blocks: gain = ceiling / block peak, lookahead over the neighbouring blocks,
    exponential release (60 ms), linear gain ramps between block centres. Stereo input is limited by the louder
    channel. Returns (limited signal, largest gain reduction in dB)."""
    n = len(x)
    if n == 0:
        return x, 0.0
    mono = np.max(np.abs(x), axis=1) if x.ndim == 2 else np.abs(x)
    bs = max(1, int(sr * block))
    nb = (n + bs - 1) // bs
    padded = np.zeros(nb * bs)
    padded[:n] = mono
    peaks = padded.reshape(nb, bs).max(axis=1)
    g = np.minimum(1.0, _db(ceiling_db) / np.maximum(peaks, 1e-9))
    if not np.any(g < 1.0):
        return x, 0.0
    la = g.copy()
    la[:-1] = np.minimum(la[:-1], g[1:])
    la[1:] = np.minimum(la[1:], g[:-1])
    k = 1.0 - np.exp(-block / max(release, 1e-3))
    out = np.empty(nb)
    cur = 1.0
    for i in range(nb):
        cur = min(la[i], cur + (1.0 - cur) * k)
        out[i] = cur
    env = np.interp(np.arange(n), np.arange(nb) * bs + bs / 2, out)
    red = float(-20 * np.log10(max(out.min(), 1e-9)))
    return (x * env[:, None] if x.ndim == 2 else x * env), round(red, 2)


def _pan_gains(pan: float) -> tuple[float, float]:
    """Constant-power pan, scaled so the louder channel keeps the cue's target peak (centre = 1/1)."""
    a = (max(-1.0, min(1.0, pan)) + 1.0) * np.pi / 4
    gl, gr = float(np.cos(a)), float(np.sin(a))
    m = max(gl, gr, 1e-6)
    return gl / m, gr / m


def _place(dst: np.ndarray, src: np.ndarray, at_s: float) -> None:
    i0 = int(round(at_s * SR))
    if i0 >= len(dst) or i0 + len(src) <= 0:
        return
    s0 = max(0, -i0)
    i0 = max(0, i0)
    n = min(len(src) - s0, len(dst) - i0)
    if n <= 0:
        return
    if dst.ndim == 2 and src.ndim == 1:
        dst[i0:i0 + n] += src[s0:s0 + n, None]
    else:
        dst[i0:i0 + n] += src[s0:s0 + n]


def _license_overview_text(file_name: str) -> str:
    """Licence text for a music file from OneDrive `08 Recht und Verwaltung\\Lizenzen\\Lizenzübersicht.md`
    (the table row that names the file), or '' when it is not listed."""
    p = mirror_dir().parent / "08 Recht und Verwaltung" / "Lizenzen" / "Lizenzübersicht.md"
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            if file_name in line and line.strip().startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                return f"{cells[-1]} (Lizenzübersicht.md)" if cells else "Lizenzübersicht.md"
    except OSError:
        pass
    return ""


def resolve_music_file(name: str, brand_dir: Path | None, cfg_license: str = "") -> tuple[Path | None, str, str]:
    """(path, licence text, problem) for a licensed bed: brands/<id>/assets/music then assets/music; the licence is
    the LICENSE.md line next to the file, the row in Lizenzübersicht.md, or `music_license` of the config."""
    p = Path(name)
    if not p.is_absolute():
        cands = ([brand_dir / "assets" / "music" / name] if brand_dir else []) + [ASSETS_DIR / "music" / name]
        p = next((c for c in cands if c.exists()), cands[-1])
    if not p.exists():
        return None, "", f"music file missing: {name} -> {p}"
    from .assets import _licenses
    lic = _licenses(p.parent).get(p.name, "") or _license_overview_text(p.name) or cfg_license
    return p, lic, ("" if lic else f"music file without licence proof (LICENSE.md next to it or Lizenzübersicht.md): {p.name}")


# --- mix --------------------------------------------------------------------------------------------

@dataclass
class MixResult:
    path: Path
    config: SoundConfig
    cues: list[Cue]
    music: dict
    measured: dict
    problems: list[str] = field(default_factory=list)
    stems: dict = field(default_factory=dict)
    assets: list[dict] = field(default_factory=list)
    licenses: list[dict] = field(default_factory=list)

    def manifest(self) -> dict:
        return {"enabled": True, "version": VERSION, "palette": self.config.palette, "sounds": dict(self.config.sounds),
                "levels": dict(self.config.levels), "config_source": self.config.source, "music": dict(self.music),
                "cues": [c.to_dict() for c in self.cues], "measured": dict(self.measured), "problems": list(self.problems),
                "mix": str(self.path), "stems": {k: str(v) for k, v in self.stems.items()}}


_SFX_CACHE: dict[str, np.ndarray] = {}


def _load_sfx(cue: Cue, brand_dir: Path | None) -> tuple[np.ndarray | None, Path | None, str]:
    """Mono sample for a cue: a file cue, else brands/<id>/assets/sfx/<name>.wav (brand override), else the shared
    assets/sfx/<name>.wav (generated on first use when missing)."""
    if cue.path is not None:
        p = cue.path
    else:
        cands = ([brand_dir / "assets" / "sfx" / f"{cue.sound}.wav"] if brand_dir else []) + [ASSETS_DIR / "sfx" / f"{cue.sound}.wav"]
        p = next((c for c in cands if c.exists()), None)
        if p is None:
            if cue.sound in synth.SFX:
                synth.write_sfx_set(ASSETS_DIR / "sfx")
                p = ASSETS_DIR / "sfx" / f"{cue.sound}.wav"
            else:
                return None, None, f"unknown sound {cue.sound!r}"
    key = str(p.resolve())
    if key not in _SFX_CACHE:
        _SFX_CACHE[key] = decode(p, SR, 1)
    return _SFX_CACHE[key], p, ""


def mix_sound(voice_wav: Path | str | None, cues: list[Cue], palette, out_wav: Path | str, *, total: float,
              voice_start: float = 0.0, brand_dir: Path | None = None, video_id: str = "", work_dir: Path | None = None,
              keep_stems: bool = True) -> MixResult:
    """Mix voice + sound effects + music bed into `out_wav` (48 kHz stereo 24 bit, exactly `total` seconds).

    `palette`: a SoundConfig, a palette name, or a dict with the brand.yaml keys. `voice_wav` may be None (no voice:
    the bed is not ducked). The voice is brought to `levels.voice_lufs`; every cue is scaled to its role's peak;
    the sfx stem never exceeds `sfx_max_peak_db`; the bed is set `music_db` under the voice and ducked by
    `duck_db` while speaking. Stems (voice, sfx, music) stay next to the mix for measurement.
    """
    cfg = palette if isinstance(palette, SoundConfig) else config_for(None, overrides=(palette if isinstance(palette, dict) else {"palette": palette}))
    out_wav = Path(out_wav)
    work = Path(work_dir) if work_dir else out_wav.parent
    work.mkdir(parents=True, exist_ok=True)
    n = int(round((total + 0.05) * SR))
    problems: list[str] = []
    measured: dict = {}
    stems: dict = {}
    target = cfg.level("voice_lufs")

    # voice: normalise to the target loudness (bounded) with a static gain, then limit the peaks (voice_ceiling_db)
    # so the final loudnorm can run as a static gain too (linear mode) and nothing is pushed into the limiter later
    voice_tl = np.zeros(n)
    voice_gain = 0.0
    if voice_wav is not None and Path(voice_wav).exists():
        v = decode(Path(voice_wav), SR, 1)
        st = ffmpeg.audio_stats(Path(voice_wav), dual_mono=True)      # as dual mono, like it sits in the stereo mix
        lufs = st.get("integrated_lufs")
        if lufs is not None and lufs > -60:
            voice_gain = max(-12.0, min(12.0, target - lufs))
        v, v_red = limit_peaks(v * _db(voice_gain), cfg.level("voice_ceiling_db"))
        _place(voice_tl, v, voice_start)
        measured.update({"voice_lufs_in": lufs, "voice_gain_db": round(voice_gain, 2), "voice_limiter_db": v_red,
                         "voice_lufs": (round(lufs + voice_gain, 2) if lufs is not None else None)})
    else:
        measured.update({"voice_lufs_in": None, "voice_gain_db": 0.0, "voice_lufs": None})
    # the bed is set relative to the voice as it really sits in the mix (the peak cap may keep it under the target)
    voice_ref = measured["voice_lufs"] if measured.get("voice_lufs") is not None else target

    # sound effects
    sfx = np.zeros((n, 2))
    used: dict[str, tuple[Path, str]] = {}
    cue_out: list[Cue] = []
    for c in cues:
        if c.role in ("music_in", "music_out"):
            cue_out.append(c)
            continue
        sample, path, why = _load_sfx(c, brand_dir)
        if sample is None:
            problems.append(f"{why} at {c.at:.2f} s: cue dropped")
            continue
        peak = float(np.max(np.abs(sample))) if sample.size else 0.0
        if peak <= 0:
            continue
        if c.role == "event":                       # ticks at fade-ins keep their own, fixed level
            level = cfg.level("event_peak_db")
        else:                                       # sweeps at sfx_peak_db, short impulses lower (SOUND_LEVEL_OFFSETS)
            level = cfg.level("sfx_peak_db") + SOUND_LEVEL_OFFSETS.get(c.sound, 0.0)
        c.seconds = len(sample) / SR
        g = _db(level + c.gain_db) / peak
        gl, gr = _pan_gains(c.pan)
        st2 = np.stack([sample * g * gl, sample * g * gr], axis=1)
        _place(sfx, st2, c.at)
        used[path.name] = (path, c.note if c.source == "file" else "")
        cue_out.append(c)
    sfx_peak = float(np.max(np.abs(sfx))) if sfx.size else 0.0
    cap = _db(cfg.level("sfx_max_peak_db"))
    if sfx_peak > cap:
        sfx *= cap / sfx_peak
        measured["sfx_stem_trim_db"] = round(20 * np.log10(cap / sfx_peak), 2)
    measured["sfx_peak_dbfs"] = _peak_db(sfx)
    measured["sfx_count"] = len([c for c in cue_out if c.role not in ("music_in", "music_out")])

    # music bed
    music_info: dict = {"source": "none"}
    bed_tl = np.zeros((n, 2))
    m_in = next((c.at for c in cues if c.role == "music_in"), 0.0)
    m_out_cue = next((c for c in cues if c.role == "music_out"), None)
    m_end = min(total - 0.1, float(m_out_cue.at)) if m_out_cue is not None else total - 0.1
    final_chord = bool(m_out_cue is not None and m_out_cue.note == "chord")
    if cfg.music and cfg.music.lower() != "none" and m_end > m_in + 2.0:
        seed = cfg.seed if cfg.seed is not None else (zlib.crc32(str(video_id).encode("utf-8")) & 0xFFFF)
        bed = None
        if cfg.music.lower() == "procedural":
            bed = synth.music_bed(total + 0.05 - m_in, cfg.mood, seed, end_at=m_end - m_in, final_chord=final_chord,
                                  fade_in=MUSIC_FADE_IN, fade_out=MUSIC_FADE_OUT).astype(np.float64)
            music_info = {"source": "procedural", "mood": cfg.mood, "seed": int(seed), "generator": f"{synth.GENERATOR} {synth.GENERATOR_VERSION}",
                          "description": synth.MOODS[cfg.mood]["desc"], "license": PROCEDURAL_LICENSE}
        else:
            p, lic, why = resolve_music_file(cfg.music, brand_dir, cfg.music_license)
            if p is None:
                problems.append(f"{why}; procedural bed used instead")
                bed = synth.music_bed(total + 0.05 - m_in, cfg.mood, seed, end_at=m_end - m_in, final_chord=final_chord).astype(np.float64)
                music_info = {"source": "procedural", "mood": cfg.mood, "seed": int(seed), "generator": f"{synth.GENERATOR} {synth.GENERATOR_VERSION}",
                              "license": PROCEDURAL_LICENSE, "fallback_for": cfg.music}
            else:
                if why:
                    problems.append(why)
                x = decode(p, SR, 2)
                need = int(round((m_end - m_in) * SR))
                if len(x) < need:                     # loop with a short crossfade
                    reps = int(np.ceil(need / max(1, len(x))))
                    x = np.concatenate([x] * reps)
                bed = np.zeros((int(round((total + 0.05 - m_in) * SR)), 2))
                bed[:need] = synth.fade(x[:need], MUSIC_FADE_IN, MUSIC_FADE_OUT)
                music_info = {"source": "file", "file": p.name, "path": str(p), "license": lic}
        if bed is not None:
            raw_stem = work / "music_raw.wav"
            write_wav(raw_stem, synth.normalize(bed, -6.0), bits=16)
            st = ffmpeg.audio_stats(raw_stem)
            bed_lufs = st.get("integrated_lufs")
            want = voice_ref + cfg.level("music_db")
            m_gain = (want - bed_lufs) if bed_lufs is not None and bed_lufs > -60 else 0.0
            bed = synth.normalize(bed, -6.0) * _db(max(-40.0, min(30.0, m_gain)))
            gains = duck_gain(voice_tl, cfg.level("duck_db")) if voice_tl.any() else np.ones(n)
            placed = np.zeros((n, 2))
            _place(placed, bed, m_in)
            bed_tl = placed * gains[:, None]
            if not keep_stems:
                raw_stem.unlink(missing_ok=True)
            else:
                stems["music_raw"] = raw_stem
            music_info.update({"start": round(m_in, 3), "end": round(m_end, 3), "final_chord": final_chord,
                               "lufs_unducked": round(want, 2) if bed_lufs is not None else None, "voice_reference_lufs": round(voice_ref, 2),
                               "duck_db": cfg.level("duck_db"), "music_db": cfg.level("music_db")})
            ducked_share = float(np.mean(gains < 0.999)) if n else 0.0
            measured["music_ducked_share"] = round(ducked_share, 3)

    # stems for measurement
    if keep_stems:
        stems["voice"] = write_wav(work / "voice_stem.wav", np.stack([voice_tl, voice_tl], axis=1), bits=16)
        stems["sfx"] = write_wav(work / "sfx_stem.wav", sfx, bits=16)
        if bed_tl.any():
            stems["music"] = write_wav(work / "music_stem.wav", bed_tl, bits=16)
            measured["music_lufs"] = ffmpeg.audio_stats(stems["music"]).get("integrated_lufs")
            measured["music_lufs_unducked"] = music_info.get("lufs_unducked")
        vs = ffmpeg.audio_stats(stems["voice"]) if voice_tl.any() else {}
        if vs.get("integrated_lufs") is not None:
            measured["voice_lufs"] = vs["integrated_lufs"]
            measured["voice_peak_dbfs"] = vs.get("max_volume_db")

    # mix, limited once more where a cue meets a voice peak (mix_ceiling_db)
    mix = np.stack([voice_tl, voice_tl], axis=1) + sfx + bed_tl
    mix, m_red = limit_peaks(mix, cfg.level("mix_ceiling_db"))
    measured["mix_limiter_db"] = m_red
    # static trim to the target loudness, so the encoder's linear loudnorm has (almost) nothing left to do and never
    # has to fall back to its dynamic mode (true peak stays under the ceiling, gain stays near 0 dB)
    pre_path = write_wav(work / "mix_pre.wav", mix, bits=16)
    pre = ffmpeg.audio_stats(pre_path).get("integrated_lufs")
    trim = 0.0
    if pre is not None and pre > -60:
        trim = max(-6.0, min(6.0, target - pre))
        if abs(trim) >= 0.05:
            mix = mix * _db(trim)
            if trim > 0:
                mix, _ = limit_peaks(mix, cfg.level("mix_ceiling_db"))
    pre_path.unlink(missing_ok=True)
    measured["mix_trim_db"] = round(trim, 2)
    write_wav(out_wav, mix, bits=24)
    ms = ffmpeg.audio_stats(out_wav)
    measured.update({"mix_lufs": ms.get("integrated_lufs"), "mix_peak_dbfs": ms.get("max_volume_db"), "seconds": round(total, 3)})
    if measured.get("music_lufs") is not None and measured.get("voice_lufs") is not None:
        measured["music_below_voice_db"] = round(measured["voice_lufs"] - measured["music_lufs"], 1)

    # manifest entries
    assets_l: list[dict] = []
    licenses: list[dict] = []
    from .assets import _licenses
    for name, (path, note) in used.items():
        assets_l.append({"name": f"sfx:{name}", "kind": "audio", "role": "sfx"})
        lic = _licenses(path.parent).get(path.name, "")
        if lic:
            licenses.append({"asset": f"sfx:{name}", "license": lic, "proof": str(path.parent / "LICENSE.md")})
        else:
            problems.append(f"sfx without licence line in {path.parent / 'LICENSE.md'}: {name}")
    if music_info.get("source") == "procedural":
        assets_l.append({"name": "music:procedural", "kind": "audio", "role": "music"})
        licenses.append({"asset": "music:procedural", "license": f"{PROCEDURAL_LICENSE}; mood {music_info.get('mood')}, seed {music_info.get('seed')}",
                         "proof": "manifest.sound.music"})
    elif music_info.get("source") == "file":
        assets_l.append({"name": f"music:{music_info['file']}", "kind": "audio", "role": "music"})
        if music_info.get("license"):
            licenses.append({"asset": f"music:{music_info['file']}", "license": music_info["license"], "proof": "08 Recht und Verwaltung/Lizenzen/Lizenzübersicht.md"})
    return MixResult(path=out_wav, config=cfg, cues=cue_out, music=music_info, measured=measured, problems=problems,
                     stems=stems, assets=assets_l, licenses=licenses)


# --- command line -----------------------------------------------------------------------------------

def _selftest(work: Path) -> int:
    """Synthetic 20 s "voice" (speech-like noise bursts), default palette, procedural bed; prints the levels."""
    rng = np.random.default_rng(3)
    n = 20 * SR
    t = np.arange(n) / SR
    bursts = (np.sin(2 * np.pi * 0.9 * t) > 0.1).astype(float) * (np.sin(2 * np.pi * 4.0 * t) > -0.6)
    voice = synth.stft_filter(rng.standard_normal(n), [300, 1200, 400, 900], 2.0) * bursts * 0.4
    voice[: 2 * SR] = 0.0
    vw = write_wav(work / "selftest_voice.wav", voice, bits=16)
    cfg = config_for(None, overrides={"palette": "tech"})
    cues = auto_cues([5.0, 10.0, 15.0], 20.0, cfg, hook_end=5.0, close_start=15.0, outro_start=18.0,
                     events=[6.2, 6.4, 7.5, 9.9, 12.0, 13.1], voice_start=0.4)
    cues = merge_cues(cues, [Cue(8.0, "stamp", role="plan", source="plan"), Cue(19.0, "", role="music_out", source="plan", note="chord")], 20.0)
    res = mix_sound(vw, cues, cfg, work / "selftest_mix.wav", total=20.0, voice_start=0.4, video_id="selftest")
    print(json.dumps(res.manifest(), indent=1, ensure_ascii=False, default=str))
    ok = (res.measured.get("sfx_peak_dbfs") or 0) <= cfg.level("sfx_max_peak_db") + 0.1
    ok = ok and (res.measured.get("mix_peak_dbfs") or 0) <= -0.9
    print("selftest", "ok" if ok else "FAILED", "->", res.path)
    return 0 if ok else 1


def _main(argv: list[str]) -> int:
    import sys
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "sfx":
        files = synth.write_sfx_set(ASSETS_DIR / "sfx")
        print(f"{len(files)} sound effects + LICENSE.md -> {ASSETS_DIR / 'sfx'}")
        return 0
    if argv[0] == "selftest":
        work = Path(argv[1]) if len(argv) > 1 else ASSETS_DIR.parent / "storage" / "sound_selftest"
        return _selftest(work)
    if argv[0] == "probe":
        for p in argv[1:]:
            print(p, ffmpeg.audio_stats(Path(p)))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv[1:]))
