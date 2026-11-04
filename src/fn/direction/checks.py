"""Direction checks for the validation report: scene variety, visual cuts, readability, audio level.

Added to a `compliance.Report` next to the Phase-1 technical and content checks. Severities follow
config/policies.yaml semantics: fail -> FAILED, review -> HUMAN_REVIEW, warn -> noted.
"""
from __future__ import annotations

import statistics
from pathlib import Path

from ..compliance import Report
from ..render import ffmpeg
from .story import DirectionPlan, MIN_DISTINCT_TYPES, TARGET_DISTINCT_TYPES

MAX_STATIC_SECONDS = 14.0      # longest stretch without any visual change
MIN_MEDIAN_CUT = 1.2           # below this the video feels hectic
MAX_MEDIAN_CUT = 8.0           # above this it feels like a slide deck
CAPTION_MIN_PX = 42
LUFS_TARGET, LUFS_TOL = -16.0, 2.0
MAX_PEAK_DB = -0.5
MAX_SFX_PEAK_DB = -6.0                    # sound layer: sfx stem peak before loudnorm (Tonebene, 03.11.2026)
MUSIC_BELOW_VOICE_RANGE = (8.0, 22.0)     # bed integrated loudness this many dB under the voice (ducked)


def check_direction(report: Report, plan: DirectionPlan, events: list[float], total: float, *,
                    template_problems: list[str] | None = None, caption_font_px: int | None = None,
                    video: Path | None = None, max_static: float = MAX_STATIC_SECONDS, layout: dict | None = None,
                    intro_seconds: float = 0.0) -> None:
    MAX_STATIC = max_static
    # scene variety
    types = [b.scene_type for b in plan.beats]
    distinct = len(set(types))
    report.add("scene_variety", "fail", distinct >= MIN_DISTINCT_TYPES,
               f"{distinct} scene type(s) in {len(types)} beats: {sorted(set(types))}")
    if distinct < TARGET_DISTINCT_TYPES:
        report.add("scene_variety_target", "warn", False, f"{distinct} < {TARGET_DISTINCT_TYPES} recommended scene types")
    def layout_key(b):
        mode = b.data.get("mode") or ("items" if b.data.get("items") else "statement")
        return (b.scene_type, mode)
    repeats = [(a.id, b.id) for a, b in zip(plan.beats, plan.beats[1:]) if layout_key(a) == layout_key(b)]
    report.add("identical_consecutive_scenes", "warn", not repeats, "none" if not repeats else f"same layout back to back: {repeats}")

    # visual cuts: beat starts plus internal template events
    cuts = sorted(set([0.0] + [float(e) for e in events] + [b.start for b in plan.beats if b.start is not None] + [total]))
    gaps = [b - a for a, b in zip(cuts, cuts[1:]) if b - a > 0.05]
    longest = max(gaps) if gaps else total
    median = statistics.median(gaps) if gaps else total
    report.add("visual_cuts_static", "fail", longest <= MAX_STATIC,
               f"longest stretch without a visual change {longest:.1f} s (max {MAX_STATIC:.0f})")
    report.add("visual_cuts_rhythm", "warn", MIN_MEDIAN_CUT <= median <= MAX_MEDIAN_CUT,
               f"{len(cuts) - 2} visual events, median interval {median:.1f} s (target {MIN_MEDIAN_CUT}-{MAX_MEDIAN_CUT})")

    # readability: template text limits (fixed font sizes) and caption size
    probs = list(template_problems or [])
    hard = [p for p in probs if "chars >" in p]
    asset_p = [p for p in probs if p.startswith("assets:")]
    soft = [p for p in probs if p not in hard and p not in asset_p]
    report.add("readability_text_limits", "fail", not hard, "all texts within template limits" if not hard else "; ".join(hard))
    if soft:
        report.add("schematic_ui", "review", False, "; ".join(soft))
    if asset_p:
        missing = [p for p in asset_p if "placeholder used" in p]
        report.add("asset_placeholders", "review", not missing, "; ".join(asset_p) if asset_p else "all clips present")
    if caption_font_px is not None:
        report.add("readability_captions", "fail", caption_font_px >= CAPTION_MIN_PX, f"caption font {caption_font_px} px (min {CAPTION_MIN_PX})")

    # acceptance rules from the second critique (A2)
    import json as _json
    open_q = [b for b in plan.beats if b.data.get("risk_open")]
    bad = []
    for b in open_q:
        blob = _json.dumps(b.data, ensure_ascii=False)
        if '"ok": true' in blob or "✓" in blob or "&#10003;" in blob or "✔" in blob:
            bad.append(b.id)
    report.add("no_check_icons_open_questions", "fail", not bad,
               f"{len(open_q)} beats with open risk questions, check marks in: {bad or 'none'}")
    report.add("logo_intro_seconds", "fail", intro_seconds <= 0.0, f"logo intro {intro_seconds:.1f} s (must be 0: logo small from frame 1)")
    if layout:
        cap_w = int(layout.get("caption_width_px", 900))
        cap_right = (1080 + cap_w) // 2
        zone_bottom = int(layout.get("zone_top", 290)) + int(layout.get("zone_h", 910))
        status_right = min(972, 940)
        probs = []
        if cap_right > 940:
            probs.append(f"captions reach x={cap_right} (> 940, platform icon column)")
        # Below y 1100 only the icon column (x > 940) is in the way: a scene that keeps its lower part left of x 940
        # (`zone_lower_right_px` <= 940) may reach down to just above the captions (Prüfrunde 03.11.2026, R5).
        lower_right = int(layout.get("zone_lower_right_px", 1080))
        zone_limit = min(1250, 1920 - int(layout.get("caption_bottom_px", 560)) - 120) if lower_right <= 940 else 1100
        if zone_bottom > zone_limit:
            probs.append(f"scene zone ends at y={zone_bottom} (> {zone_limit}; below 1100 the lower part must stay left of x 940, "
                         f"set zone_lower_right_px)")
        if int(layout.get("status_y", 1480)) + 84 > 1620:
            probs.append("status bar inside the platform caption area (y > 1620)")
        if int(layout.get("progress_y", 1724)) + 6 > 1620:
            probs.append(f"progress bar at y={layout.get('progress_y', 1724)} inside the platform caption area (y > 1620)")
        if 1920 - int(layout.get("ai_label_bottom_px", 150)) > 1620:
            probs.append(f"AI label at y={1920 - int(layout.get('ai_label_bottom_px', 150))} inside the platform caption area (y > 1620): may be covered")
        report.add("platform_overlay", "fail", not probs, "; ".join(probs) if probs else
                   f"captions x<= {cap_right}, scene zone y<= {zone_bottom}, status bar x<= {status_right}: clear of simulated platform controls (x>940 for y 1100-1700, y>1620)")

    # audio level
    if video is not None and Path(video).exists():
        st = ffmpeg.audio_stats(Path(video))
        lufs, peak = st.get("integrated_lufs"), st.get("max_volume_db")
        if lufs is not None:
            report.add("audio_level_lufs", "warn", abs(lufs - LUFS_TARGET) <= LUFS_TOL, f"{lufs} LUFS (target {LUFS_TARGET} +/- {LUFS_TOL})")
        if peak is not None:
            report.add("audio_level_peak", "fail", peak <= MAX_PEAK_DB, f"max volume {peak} dB (max {MAX_PEAK_DB})")


def _encoded_cue_peak(video: Path, cues: list[dict]) -> tuple[float, str] | None:
    """Sample peak of the encoded audio inside the sound-cue windows (cue start .. start + sample length + 50 ms)."""
    import math
    import numpy as np
    from ..render.sound import decode, SR
    x = decode(Path(video), SR, 2)
    mono = np.max(np.abs(x), axis=1)
    best: tuple[float | None, str] = (None, "")
    for c in cues:
        if c.get("role") in ("music_in", "music_out"):
            continue
        a = max(0, int(float(c.get("at", 0.0)) * SR))
        b = a + int((float(c.get("seconds") or 1.0) + 0.05) * SR)
        seg = mono[a:b]
        if seg.size == 0:
            continue
        p = float(seg.max())
        if best[0] is None or p > best[0]:
            best = (p, f"{float(c.get('at', 0.0)):.2f} s {c.get('sound')} ({c.get('role')})")
    if best[0] is None:
        return None
    return (round(20 * math.log10(best[0]), 2) if best[0] > 0 else -120.0), best[1]


def check_sound(report: Report, snd: dict | None, video: Path | None = None) -> None:
    """Sound layer (manifest `sound`, fn.render.sound): cues present, sfx stem peak <= -6 dBFS before loudnorm,
    encoded peak around the cues <= -0.5 dBFS (Gritwerk finding 03.11.2026: clicks hit 0.0 dB after AAC), bed 8-22 dB
    under the voice, licence proof for a file bed, dropped cues. The encoded value is written back into
    `snd["measured"]` so it lands in manifest.json."""
    if not snd or not snd.get("enabled"):
        report.add("sound_layer", "warn", False, "sound layer off: voice only (brand.yaml sound.enabled=false or --no-sound)")
        return
    cues = snd.get("cues", [])
    music = snd.get("music", {}) or {}
    m = snd.setdefault("measured", {})
    n_sfx = sum(1 for c in cues if c.get("role") not in ("music_in", "music_out"))
    has_music = music.get("source") not in (None, "none")
    report.add("sound_layer", "warn", n_sfx > 0 or has_music,
               f"{n_sfx} sound cues (palette {snd.get('palette')}), music {music.get('source')}" + (f"/{music.get('mood')}" if music.get("mood") else ""))
    peak = m.get("sfx_peak_dbfs")
    if peak is not None:
        report.add("sfx_stem_peak", "fail", peak <= MAX_SFX_PEAK_DB + 0.1, f"sfx stem peak {peak} dBFS before loudnorm (max {MAX_SFX_PEAK_DB})")
    if video is not None and Path(video).exists() and n_sfx:
        try:
            enc = _encoded_cue_peak(Path(video), cues)
        except Exception as exc:                      # noqa: BLE001 - a measuring problem must be visible, not fatal
            enc = None
            report.add("sfx_peak", "fail", False, f"encoded peak around the cues could not be measured: {exc}")
        if enc is not None:
            enc_db, where = enc
            m["sfx_encoded_peak_dbfs"] = enc_db
            m["sfx_encoded_peak_at"] = where
            report.add("sfx_peak", "fail", enc_db <= MAX_PEAK_DB,
                       f"encoded peak around the sound cues {enc_db} dBFS (max {MAX_PEAK_DB}), loudest at {where}")
    enc_info = m.get("encode") or {}
    if enc_info:
        mode = str(enc_info.get("normalization_type") or enc_info.get("loudnorm") or "unknown")
        report.add("sound_loudnorm", "warn", mode.lower() == "linear",
                   f"loudnorm {mode} (linear = one static gain, pauses stay unlifted; dynamic = fallback that lifts pauses), "
                   f"target {enc_info.get('target_i')}")
    below = m.get("music_below_voice_db")
    if below is not None:
        lo, hi = MUSIC_BELOW_VOICE_RANGE
        report.add("music_bed_level", "warn", lo <= below <= hi,
                   f"bed {below} dB under the voice over the video (target {lo}-{hi}); unducked {music.get('lufs_unducked')} LUFS, "
                   f"ducked while speaking by {music.get('duck_db')} dB")
    if music.get("source") == "file":
        report.add("music_license", "review", bool(music.get("license")), f"music file {music.get('file')}: " + (music.get("license") or "no licence proof"))
    elif music.get("fallback_for"):
        report.add("music_license", "review", False, f"music file {music['fallback_for']} unusable, procedural bed used instead")
    probs = snd.get("problems", [])
    if probs:
        report.add("sound_cues", "warn", False, "; ".join(str(p) for p in probs))
