"""Produce a full video from a direction plan (Regie): TTS -> word timings -> beat timing -> director -> render -> checks.

Since 03.11.2026 the sound layer (fn.render.sound) mixes voice, transition sounds and a ducked music bed and
replaces the rendered audio before the NVENC encode; `--no-sound` keeps the old voice-only path.
Separate from `fn.pipeline.produce` (Phase-1 single template); nothing there is changed. Costs: one TTS run
per call when `--tts gemini` (logged in data/costs). Output: storage/direction/<video_id>-<version>/ and a mirror
folder under OneDrive\\Business\\05 Produktion\\_Demos\\scutoria-regie\\<mirror-name>\\.

Run:  .venv\\Scripts\\python.exe scripts\\render_direction.py data\\direction\\ai_security-20261105-1-de.json --version A --tts gemini
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn import __version__, compliance, transcribe  # noqa: E402
from fn.brands import load_brand  # noqa: E402
from fn.config import BRAND_FOLDERS, STORAGE_DIR, VideoSpec, mirror_dir  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.direction import checks, hooks, story  # noqa: E402
from fn.disk import check_free_space  # noqa: E402
from fn.render import ffmpeg, hyperframes  # noqa: E402
from fn.render import assets as asset_layer  # noqa: E402
from fn.render import brand_scenes  # noqa: E402
from fn.render import sound  # noqa: E402
from fn.render.compose import Word, group_words  # noqa: E402
from fn.render.director import assign_timing, build_direction_project, group_phrases  # noqa: E402
from fn.tts import get_provider  # noqa: E402

VOICE_START = 0.4          # the hook starts at once; no wordmark intro in the direction layout
TAIL = 0.4                 # silence after the last word before the outro


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", default="A")
    ap.add_argument("--tts", default="gemini", help="gemini | mock | sapi")
    ap.add_argument("--whisper", default="large-v3")
    ap.add_argument("--quality", default="looks")
    ap.add_argument("--workers", default="4")
    ap.add_argument("--mirror", default=None,
                    help="demo folder under 05 Produktion\\_Demos (default <marke>-regie/<video_id>-<version>, one per run; "
                         "a shared default let a Gritwerk probe overwrite the Scutoria demo on 03.11.2026)")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--reuse-voice", default=None, help="existing voice.wav to reuse instead of a new TTS run")
    ap.add_argument("--assets", action="store_true", help="Fassung B: use the plan's asset layer (clips or placeholders)")
    ap.add_argument("--tail", type=float, default=None, help="seconds after the last word (default TAIL, or plan.layout.tail_seconds)")
    ap.add_argument("--no-outro", action="store_true", help="no end card: the last beat runs to the end (or plan.layout.outro=false)")
    ap.add_argument("--excerpt", type=float, default=None, help="render only the first N seconds (voice and captions clipped)")
    ap.add_argument("--max-static", type=float, default=14.0, help="longest stretch without a visual change (s)")
    ap.add_argument("--no-sound", action="store_true", help="no sound layer: voice only, as before 03.11.2026")
    ap.add_argument("--sound", default=None,
                    help="sound layer override for this run: palette=tech,mood=dark,music=none,levels.music_db=-10 ... "
                         "or a JSON object with the brand.yaml `sound` keys (brands try a palette without editing brand.yaml)")
    a = ap.parse_args()

    plan = story.load_plan(Path(a.plan))
    if a.mirror is None:
        brand_folder = BRAND_FOLDERS.get(plan.brand_id, plan.brand_id).lower()
        a.mirror = f"{brand_folder}-regie/{plan.video_id}-{a.version}"
    problems = story.validate(plan)
    if problems:
        print("plan problems:", *problems, sep="\n  ")
        return 2
    cands = [hooks.from_dict(c) for c in plan.hook_candidates]
    hp = hooks.validate_set(cands)
    if hp:
        print("hook set problems:", *hp, sep="\n  ")
        return 2
    chosen = next((c for c in cands if c.id == plan.hook.get("id")), None)
    if chosen is None or not chosen.eligible:
        print(f"chosen hook {plan.hook.get('id')} missing or not eligible")
        return 2
    if plan.beats[0].spoken.strip() != chosen.spoken.strip():
        print(f"warning: hook beat text differs from candidate {chosen.id}; using the beat text")
    space = check_free_space()
    if not space.ok:
        print(space.message)
        return 4

    brand = load_brand(plan.brand_id)
    lang = plan.language
    spec = VideoSpec.from_config()
    costs = CostLogger()
    video_id = f"{plan.video_id}-{a.version}"
    out = STORAGE_DIR / "direction" / video_id
    project = out / "project"
    if project.exists():
        shutil.rmtree(project)
    (project / "assets").mkdir(parents=True)
    t_all = time.perf_counter()

    # 1) voice
    spoken = plan.spoken_text
    if a.reuse_voice:
        voice = project / "assets" / "voice.wav"
        shutil.copy2(a.reuse_voice, voice)
        # provenance of the reused recording from the sidecar <wav>.json (written by the run that paid for it)
        side = Path(a.reuse_voice).with_suffix(".json")
        info = json.loads(side.read_text(encoding="utf-8")) if side.exists() else {}
        if info.get("spoken_text") and info["spoken_text"].strip() != spoken.strip():
            print("reused voice was recorded for a different text; refusing (re-run TTS instead)")
            return 7
        if info.get("provider") in ("sapi", "edge") or "_sapi" in Path(a.reuse_voice).name:
            print("reused voice is a Windows/edge voice; blocked (Stefan, 30.10.2026: only Google/Gemini voices)")
            return 8
        tts_info = {"provider": info.get("provider", "unknown"), "model": info.get("model", ""), "voice": info.get("voice", ""),
                    "seconds": ffmpeg.audio_duration(voice), "usd": 0.0, "input_chars": len(spoken), "output_tokens": 0,
                    "notes": f"reused recording {Path(a.reuse_voice).name}; original cost {info.get('usd', '?')} USD logged under {info.get('video_id', '?')}"}
        provider_name = tts_info["provider"]
    else:
        provider = get_provider(a.tts)
        audio_cfg = brand.audio.get("tts", {})
        style = (audio_cfg.get("style_instruction") or {}).get(lang, "")
        tts = provider.synthesize(spoken, lang, brand.voice(lang), project / "assets" / "voice.wav",
                                  style=style, rate=float(audio_cfg.get("speaking_rate", 1.0)))
        costs.log_tts(video_id, tts.provider, tts.input_chars, tts.output_tokens, tts.seconds)
        voice = tts.path
        tts_info = {"provider": tts.provider, "model": tts.model, "voice": tts.voice, "seconds": tts.seconds,
                    "usd": tts.usd, "input_chars": tts.input_chars, "output_tokens": tts.output_tokens, "notes": tts.notes}
        provider_name = tts.provider
        # keep the paid recording and its provenance for later re-renders without new TTS cost
        keep = STORAGE_DIR / "direction" / f"voice_{plan.video_id}_{a.version}_{tts.provider}.wav"
        shutil.copy2(voice, keep)
        keep.with_suffix(".json").write_text(json.dumps({**tts_info, "video_id": video_id, "spoken_text": spoken}, indent=2, ensure_ascii=False), encoding="utf-8")
    voice_seconds = float(tts_info["seconds"])
    print(f"voice: {provider_name} {voice_seconds:.1f} s, {tts_info.get('usd', 0):.4f} USD")

    # 2) word timings
    mock = provider_name == "mock"
    tr = transcribe.transcribe(voice, lang, script_text=spoken, model_size=a.whisper, force_mock=mock)
    costs.log_transcribe(video_id, tr.elapsed, tr.model)
    words = transcribe.align_to_script(tr.words, spoken)
    print(f"timings: {len(words)} words via {tr.model} ({tr.device}, {tr.elapsed:.0f} s)")

    # 3) timing
    use_outro = not (a.no_outro or plan.layout.get("outro") is False)
    outro_s = float(brand.outro.get("seconds", 4.0)) if use_outro else 0.0
    tail = a.tail if a.tail is not None else float(plan.layout.get("tail_seconds", TAIL))
    total = VOICE_START + voice_seconds + tail + outro_s
    if a.excerpt is None and not spec.min_seconds <= total <= spec.max_seconds:
        print(f"length {total:.1f} s outside {spec.min_seconds}-{spec.max_seconds} s; adjust the plan text")
        return 5
    outro_start = total - outro_s
    shifted = [Word(w.text, round(w.start + VOICE_START, 3), round(w.end + VOICE_START, 3)) for w in words]
    assign_timing(plan, shifted, first_start=0.0, outro_start=outro_start)
    if plan.layout.get("caption_mode") == "phrases":
        captions = group_phrases(shifted, min_words=2, max_words=int(plan.layout.get("caption_max_words", 4)))
    else:
        captions = group_words(shifted, int(brand.subtitle_style.get("group_words", 3)))
    if a.excerpt is not None:
        total = float(a.excerpt)
        plan.beats = [b for b in plan.beats if b.start < total - 0.5]
        last = plan.beats[-1]
        last.duration = round(total - last.start, 3)
        captions = [g for g in captions if g.end <= total - 0.2]
        use_outro = False
        video_id = f"{video_id}-excerpt{int(total)}"
        out = STORAGE_DIR / "direction" / video_id
        project = out / "project"
        if project.exists():
            shutil.rmtree(project)
        (project / "assets").mkdir(parents=True)
        v2 = project / "assets" / "voice.wav"
        subprocess_run = __import__("subprocess").run
        subprocess_run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(voice), "-t", f"{total - VOICE_START - 0.2:.3f}",
                        "-af", f"afade=t=out:st={total - VOICE_START - 0.8:.3f}:d=0.6", "-c:a", "pcm_s16le", str(v2)], check=True)
        voice = v2
        print(f"excerpt: first {total:.0f} s, {len(plan.beats)} beats, {len(captions)} caption groups")
    for b in plan.beats:
        print(f"  {b.id:3} {b.function:13} {b.scene_type:15} {b.start:6.2f} +{b.duration:5.2f}")
    story.save_plan(plan, out / "plan.timed.json")

    # 4) build + check
    sfx_only = {k: v for k, v in (plan.assets or {}).items() if k in ("sfx", "sfx_folder")}
    if a.assets:
        aset = asset_layer.resolve_assets(plan, brand, allow_placeholders=True)
    elif sfx_only.get("sfx"):          # sound effects work without --assets (no clips, no scrim)
        aset = asset_layer.resolve_assets(plan, brand, sfx_only)
    else:
        aset = None
    if aset is not None:
        for p in aset.problems:
            print("  assets:", p)
        if not aset.enabled and not aset.sfx:
            print("plan has no 'assets' block; nothing to lay under the scenes")
    snd_cfg = sound.config_for(brand, plan.layout, overrides=_sound_overrides(a.sound))
    if a.no_sound:
        snd_cfg.enabled = False
    build = build_direction_project(plan, brand, captions, total=round(total, 3), project_dir=project, voice_file=voice,
                                    voice_start=VOICE_START, outro=use_outro, title=plan.title, assets=aset,
                                    sfx_in_project=not snd_cfg.enabled)
    # sound cues: scene changes, hook end, close, outro and visual events from the build; plan cues from
    # layout.sound_cues, data.sound and the beat field `sound` (read from the raw JSON: story.Beat drops unknown keys)
    raw_plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    beat_sounds = {b.get("id"): b.get("sound") for b in raw_plan.get("beats", []) if b.get("sound")}
    file_sfx = [(s.at, s.path, s.volume, s.license) for s in aset.sfx] if aset is not None else []
    cues, snd_problems = sound.cues_from_plan(plan, snd_cfg, events=build.events, words=shifted, total=round(total, 3),
                                              outro_start=(outro_start if use_outro else None), voice_start=VOICE_START,
                                              named_events=build.named_events, beat_sounds=beat_sounds, file_sfx=file_sfx,
                                              brand_dir=brand.dir)
    (out / "sound.json").write_text(json.dumps(sound.cues_summary(snd_cfg, cues, snd_problems), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_cues = sum(1 for c in cues if c.role not in ("music_in", "music_out"))
    print(f"sound: {'on' if snd_cfg.enabled else 'OFF'}, palette {snd_cfg.palette}, {n_cues} cues "
          f"({', '.join(f'{r} {k}' for r, k in sorted(sound.cues_summary(snd_cfg, cues, []).get('counts', {}).items()))}), "
          f"music {snd_cfg.music}" + (f"/{snd_cfg.mood}" if snd_cfg.music == 'procedural' else "") + f" [{snd_cfg.source}]")
    for p in snd_problems:
        print("  sound:", p)
    check = hyperframes.check(project)
    (out / "check.json").write_text(json.dumps(check, indent=2, ensure_ascii=False), encoding="utf-8")
    lint, layout = check.get("lint", {}), check.get("layout", {})
    print(f"hyperframes check: lint {lint.get('errorCount')} errors / layout {layout.get('errorCount')} errors, craft {check.get('craft', {}).get('warningCount')} warnings")
    if lint.get("errorCount", 0):
        for it in lint.get("findings", [])[:10]:
            if it.get("severity") == "error":
                print("  ", it.get("code"), it.get("selector"), (it.get("message") or "")[:140])
        return 3
    for it in layout.get("findings", [])[:12]:
        if it.get("severity") == "error":
            print("   layout:", it.get("time"), it.get("code"), it.get("selector"), (it.get("message") or "")[:120])
    chk_kw = dict(max_static=a.max_static, layout={**plan.layout, "caption_width_px": plan.layout.get("caption_width_px", 900)}, intro_seconds=0.0)
    if a.no_render:
        pre = compliance.Report(video_id)
        checks.check_direction(pre, plan, build.events, total, template_problems=build.problems,
                               caption_font_px=int(brand.subtitle_style.get("font_size_px", 58)), **chk_kw)
        bad = [f for f in pre.findings if not f.ok and f.severity == "fail"]
        for f in pre.findings:
            if not f.ok:
                print(f"  [{f.severity:6}] NOT {f.id}: {f.detail}")
        print("dry run:", "FAIL" if bad else "ok (direction checks pass without video)")
        return 6 if bad else 0

    # 5) render + encode
    t0 = time.perf_counter()
    raw = out / "render_raw.mp4"
    hyperframes.render(project, raw, quality=a.quality, gpu=True, workers=a.workers)
    video = out / "video.mp4"
    mix = None
    if snd_cfg.enabled:
        mix = sound.mix_sound(voice, cues, snd_cfg, out / "sound" / "mix.wav", total=round(total, 3), voice_start=VOICE_START,
                              brand_dir=brand.dir, video_id=video_id)
        for p in mix.problems:
            print("  sound:", p)
        # linear (two-pass) loudnorm: a static gain, nothing lifted in pauses (Gritwerk finding 03.11.2026)
        mix.measured["encode"] = ffmpeg.encode_nvenc(raw, video, audio=mix.path, loudness_lufs=-16.0, loudnorm="linear")
    else:
        ffmpeg.encode_nvenc(raw, video, loudness_lufs=-16.0)
    render_seconds = time.perf_counter() - t0
    costs.log_render(video_id, render_seconds, f"hyperframes {a.quality} + nvenc (direction)")
    raw.unlink(missing_ok=True)
    _cover(project, video, out / "cover.jpg", plan, chosen)
    frame_times = [t for t in (5, 30, 60) if t < total - 0.5] or [min(5.0, total / 2)]
    if a.excerpt is not None:
        frame_times = [2.0, 5.0, 9.0, min(14.0, total - 0.5)]
    for t in frame_times:
        ffmpeg.extract_frame(video, out / f"frame_{int(t):02d}s.jpg", float(t))
        _overlay(out / f"frame_{int(t):02d}s.jpg", out / f"overlay_{int(t):02d}s.jpg")
    print(f"render + encode: {render_seconds:.0f} s")

    # 6) report: technical + content + direction
    cap_json = [{"start": c.start, "end": c.end, "text": c.text, "words": [{"text": w.text, "start": w.start, "end": w.end} for w in c.words]} for c in captions]
    (out / "captions.json").write_text(json.dumps(cap_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    used_fonts = sorted({brand.fonts.get("display", {}).get("family", "Inter"), brand.fonts.get("body", {}).get("family", "Inter"),
                         (brand.fonts.get("mono") or {}).get("family") or "JetBrains Mono", brand.subtitle_style.get("font_family", "Inter")})
    assets = [{"name": f"font:{f}", "kind": "font"} for f in used_fonts] + [{"name": "lib:gsap", "kind": "library"}, {"name": "voice.wav", "kind": "audio"}]
    licenses = [{"asset": f"font:{f}", "license": "OFL-1.1", "proof": f"assets/fonts/{f.lower().replace(' ', '')}/OFL.txt"} for f in used_fonts]
    licenses.append({"asset": "lib:gsap", "license": "GSAP Standard License (free incl. commercial since 3.13)", "proof": "assets/vendor/LICENSE-gsap.txt"})
    licenses.append({"asset": "voice.wav", "license": f"generated by {provider_name} ({tts_info.get('model', '')}); terms of the provider", "proof": "manifest.tts"})
    if aset is not None and (aset.enabled or aset.sfx):
        ea, el = aset.manifest_entries()
        assets += ea
        licenses += el
    if mix is not None:
        assets += [x for x in mix.assets if x["name"] not in {y["name"] for y in assets}]
        licenses += [x for x in mix.licenses if x["asset"] not in {y["asset"] for y in licenses}]
        snd_manifest = mix.manifest()
    else:
        snd_manifest = {"enabled": False, "reason": "--no-sound or brand.yaml sound.enabled=false", "cues": [c.to_dict() for c in cues]}
    post_labels = {"is_aigc": True, "is_ai_generated": True, "containsSyntheticMedia": True}
    manifest = {
        "video_id": video_id, "plan": str(a.plan), "brand_id": brand.id, "brand_name": brand.name, "language": lang, "title": plan.title,
        "version": a.version, "pipeline_version": __version__, "direction": True, "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hook": chosen.to_dict(), "sources": plan.sources, "unverified_excluded": plan.unverified, "assets": assets, "licenses": licenses,
        "tts": tts_info, "transcription": {"model": tr.model, "device": tr.device, "mock": tr.mock, "elapsed": round(tr.elapsed, 2), "words": len(words)},
        "render": {"engine": "hyperframes 0.8.217", "quality": a.quality, "encoder": "h264_nvenc", "seconds": round(render_seconds, 1), "duration": round(total, 3),
                   "outro_seconds": outro_s, "art50_disclosure_seconds": build.art50_seconds, "beats": [{"id": b.id, "function": b.function, "scene_type": b.scene_type, "start": b.start, "duration": b.duration} for b in plan.beats],
                   "visual_events": build.events},
        "ai_disclosure": {"labels": post_labels, "text": brand.ai_label(lang)},
        "sound": snd_manifest,
        # never below the brand default (risk "high" brands always end in HUMAN_REVIEW)
        "risk_level": max(brand.risk_default, plan.layout.get("risk_level", "low"), key=["low", "medium", "high"].index),
    }
    extra = brand_scenes.manifest_extra(brand.id, plan)        # brands/<id>/scenes.py MANIFEST_EXTRA, never overrides
    manifest.update({k: v for k, v in extra.items() if k not in manifest})
    report = compliance.Report(video_id)
    if a.excerpt is None:
        compliance.check_technical(report, video, cap_json, (VOICE_START, VOICE_START + voice_seconds), spec)
    else:
        report.add("excerpt", "warn", True, f"excerpt of {total:.0f} s: duration check skipped")
    post = _post_json(plan, brand, video_id, chosen, post_labels)
    (out / "post.json").write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    compliance.check_content(report, manifest, spoken, post, brand.intro)
    checks.check_direction(report, plan, build.events, total, template_problems=build.problems,
                           caption_font_px=int(brand.subtitle_style.get("font_size_px", 58)), video=video, **chk_kw)
    checks.check_sound(report, manifest["sound"], video=video)
    manifest["cost"] = costs.summary(video_id)
    manifest["report"] = {"passed": report.passed, "needs_review": report.needs_review}
    manifest["status"] = "FAILED" if not report.passed else ("HUMAN_REVIEW" if report.needs_review else "VALIDATED")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    compliance.write_report(report, out / "report.json")
    for f in report.findings:
        if not f.ok or f.severity != "fail":
            print(f"  [{f.severity:6}] {'ok ' if f.ok else 'NOT'} {f.id}: {f.detail}")
    print(f"status {manifest['status']} · {total:.1f} s · variable cost {manifest['cost'].get('usd_variable')} USD · total {time.perf_counter() - t_all:.0f} s")

    # 7) mirror
    target = mirror_dir() / "_Demos" / Path(a.mirror)
    target.mkdir(parents=True, exist_ok=True)
    names = ["video.mp4", "cover.jpg", "report.json", "manifest.json", "plan.timed.json", "captions.json", "post.json", "sound.json"]
    names += [p.name for p in out.glob("frame_*.jpg")] + [p.name for p in out.glob("overlay_*.jpg")]
    for name in names:
        if (out / name).exists():
            shutil.copy2(out / name, target / name)
    _update_overview(target.parent, a.version, manifest, report, target.name)
    print(f"mirror -> {target}")
    return 0


def _sound_overrides(text: str | None) -> dict:
    """`--sound palette=tech,mood=dark,levels.music_db=-10` or a JSON object -> brand.yaml-style dict."""
    if not text or not text.strip():
        return {}
    t = text.strip()
    if t.startswith("{"):
        return json.loads(t)
    out: dict = {}
    for part in t.split(","):
        if "=" not in part:
            continue
        k, v = (s.strip() for s in part.split("=", 1))
        if k.startswith("levels."):
            out.setdefault("levels", {})[k[7:]] = float(v)
        elif k.startswith("sounds."):
            out.setdefault("sounds", {})[k[7:]] = (v.split("+") if "+" in v else (None if v.lower() in ("none", "null", "") else v))
        elif v.lower() in ("true", "false"):
            out[k] = v.lower() == "true"
        else:
            out[k] = v
    return out


def _cover(project: Path, video: Path, dst: Path, plan, hook) -> None:
    """Cover without captions, progress bar and AI label, hook title large (scripts/make_cover.mjs); at the end of the
    first beat, when the case object is on screen. Falls back to a plain video frame (Prüfrunde 03.11.2026, R2)."""
    b0 = plan.beats[0]
    at = (b0.end - 0.3) if b0.end else (b0.start or 0) + 3.6
    title = getattr(hook, "on_screen", "") or plan.title
    script = Path(__file__).with_name("make_cover.mjs")
    try:
        import subprocess
        subprocess.run(["node", str(script), str(project), f"{at:.2f}", str(dst), title],
                       check=True, capture_output=True, timeout=180)
    except Exception as exc:                      # noqa: BLE001 - the cover must never break a render
        print(f"cover fallback (video frame): {exc}")
        ffmpeg.extract_frame(video, dst, (b0.start or 0) + 3.6)


def public_source_line(s: dict, lang: str) -> str:
    """One source for public texts: short label, URL, retrieval date in the video's language; local `file:` sources
    (own recordings, Promptwerk) never show their path (Prüfrunde 03.11.2026, R3)."""
    name = s.get("label") or s.get("title", "")
    url = s.get("url", "")
    if not url or url.startswith("file:"):
        url = {"de": "eigene Aufzeichnung", "en": "own recording"}[lang]
    word = {"de": "abgerufen", "en": "retrieved"}[lang]
    return f"[{s['id']}] {name} - {url} ({word} {s.get('checked_at', '')})"


def _post_json(plan, brand, video_id: str, hook, labels: dict) -> dict:
    """Companion text: title, description with the full source list and the Scutoria sentence; no handle (not registered)."""
    lang = plan.language
    src_lines = [public_source_line(s, lang) for s in plan.sources]
    extra = plan.layout.get("companion_text", "")
    ai_note = (((brand.design.get("production") or {}).get("ai_note") or {}).get(lang)     # brand.yaml production.ai_note.<lang>
               or {"de": "KI-generiertes Video (Stimme und Grafik).", "en": "AI-generated video (voice and graphics)."}[lang])
    desc = "\n".join([plan.layout.get("description", plan.title), "", extra, "", "Quellen:" if lang == "de" else "Sources:", *src_lines, "", ai_note]).strip()
    tags = plan.layout.get("hashtags", ["kisicherheit", "datenschutz", "kleinunternehmen", "claude"])
    base = {"title": plan.title[:100], "description": desc, "hashtags": tags}
    return {"video_id": video_id, "brand_id": brand.id, "language": lang, "title": plan.title[:100], "description": desc, "hashtags": tags,
            "hook": hook.id, "labels": labels,
            "commercial": {"brand_content_toggle": False, "brand_organic_toggle": False, "hasPaidProductPlacement": False},
            "platforms": {"tiktok": {**base, "privacy_level": "PUBLIC_TO_EVERYONE"}, "instagram": {**base}, "youtube": {**base}},
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def _overlay(frame: Path, dst: Path) -> None:
    """Simulated platform controls (right icon column, bottom caption block) over a frame for the readability check."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    im = Image.open(frame).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(5):                                    # like/comment/share/save/profile column
        cy = 1160 + i * 120
        d.ellipse((958, cy - 42, 1042, cy + 42), fill=(255, 255, 255, 190))
        d.rectangle((960, cy + 50, 1040, cy + 70), fill=(255, 255, 255, 140))
    d.rectangle((60, 1640, 860, 1700), fill=(255, 255, 255, 120))     # @name
    d.rectangle((60, 1715, 760, 1760), fill=(255, 255, 255, 90))      # caption line
    d.rectangle((60, 1775, 640, 1820), fill=(255, 255, 255, 90))      # caption line 2
    d.rectangle((0, 1860, 1080, 1920), fill=(0, 0, 0, 200))           # system bar
    Image.alpha_composite(im, ov).convert("RGB").save(dst, quality=90)


def _update_overview(folder: Path, version: str, manifest: dict, report: compliance.Report, sub: str) -> None:
    """Add (or replace) a 'Fassung <version>' section in scutoria-regie/index.html."""
    idx = folder / "index.html"
    page = idx.read_text(encoding="utf-8") if idx.exists() else "<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\"><title>Scutoria Regie</title></head><body></body></html>"
    rows = "".join(f"<li><b>{f.id}</b> · {'ok' if f.ok else 'NICHT ok'} ({f.severity}) · {html.escape(f.detail)}</li>" for f in report.findings if not f.ok or f.severity != "fail")
    frame_files = sorted(p.name for p in (folder / sub).glob("frame_*.jpg")) + sorted(p.name for p in (folder / sub).glob("overlay_*.jpg"))
    frames = "".join(f'<img src="{sub}/{n}" alt="" title="{n}" style="width:23%;margin-right:1.5%;margin-bottom:8px;border-radius:12px">' for n in frame_files)
    r = manifest.get("render", {})
    section = f"""<!-- fassung-{version} --><section id="fassung-{version}" style="margin-top:36px;background:#151923;border-radius:16px;padding:18px">
<h2 style="font-size:17px;margin:0 0 8px">Fassung {version} · Vollfassung ({r.get('duration', 0):.1f} s) · Status {manifest.get('status')}</h2>
<p style="color:#9aa3b2;font-size:13px;margin:0 0 12px">Stimme {manifest.get('tts', {}).get('provider')} ({manifest.get('tts', {}).get('voice')}) · Render {r.get('seconds', 0):.0f} s · variable Kosten {manifest.get('cost', {}).get('usd_variable')} USD · Hook {manifest.get('hook', {}).get('id')} · {html.escape(str(manifest.get('created_at')))}</p>
<div style="display:flex;gap:20px;flex-wrap:wrap"><div style="flex:0 1 320px"><video controls preload="metadata" poster="{sub}/cover.jpg" src="{sub}/video.mp4" style="width:100%;aspect-ratio:9/16;background:#000;border-radius:12px"></video></div>
<div style="flex:1 1 400px"><div>{frames}</div><ul style="font-size:13px;line-height:1.5">{rows}</ul><p style="color:#9aa3b2;font-size:13px">Dateien: {sub}/video.mp4 · cover.jpg · report.json · manifest.json · plan.timed.json</p></div></div></section><!-- /fassung-{version} -->"""
    start, end = f"<!-- fassung-{version} -->", f"<!-- /fassung-{version} -->"
    if start in page and end in page:
        page = page[:page.index(start)] + section + page[page.index(end) + len(end):]
    else:
        page = page.replace("</body>", section + "\n</body>", 1)
    idx.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
