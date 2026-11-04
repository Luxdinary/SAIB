"""End-to-end production of one video from a script file (no publishing).

script.md -> TTS -> word timings -> scenes + captions -> HyperFrames project -> render -> NVENC encode
-> cover, post.json, manifest.json, captions.json -> validation report -> state transitions -> queue.
"""
from __future__ import annotations

import json
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from . import __version__, compliance, queue, scripting, transcribe
from .brands import Brand, load_brand
from .config import VideoSpec, ensure_dirs
from .costs import CostLogger
from .disk import check_free_space
from .render import ffmpeg, hyperframes
from .render.compose import Composition, Scene, Word, build_project, group_words
from .state import StateDB
from .tts import get_provider

VOICE_LEAD = 0.25          # seconds between intro end and first spoken word
MAX_PAD = 6.0              # how much a short video may be stretched to reach the minimum


class ProductionError(RuntimeError):
    pass


@dataclass
class ProduceResult:
    video_id: str
    state: str
    folder: Path | None
    report: dict = field(default_factory=dict)
    manifest: dict = field(default_factory=dict)
    cost: dict = field(default_factory=dict)
    message: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:  # noqa: BLE001
        return url[:40]


def _scene_visual(sc: scripting.ScriptScene, sources: dict[str, dict], fallback_headline: str) -> dict:
    v = dict(sc.visual)
    headline = v.get("headline") or fallback_headline
    label = ""
    if sc.source_ids:
        src = sources.get(sc.source_ids[0], {})
        label = f"[{sc.source_ids[0]}] {_domain(src.get('url', ''))} · {src.get('checked_at', '')}".strip(" ·")
    code = [c.strip() for c in v.get("code", "").split("|") if c.strip()]
    return {"headline": headline, "body": v.get("body", ""), "number": v.get("number", ""),
            "kind": v.get("kind", sc.kind), "code_lines": code, "source_label": v.get("source", label)}


def _first_sentence(text: str, limit: int = 58) -> str:
    s = text.split(".")[0].strip()
    if len(s) > limit:
        cut = s[:limit].rsplit(" ", 1)[0]
        return cut + " …"
    return s


def plan_scenes(script: scripting.Script, words: list[Word], *, intro_s: float, outro_start: float, voice_start: float) -> list[Scene]:
    """Distribute script scenes along the word timings. Timings are absolute (video time)."""
    sources = {s["id"]: s for s in script.sources}
    counts = [len(s.spoken.split()) for s in script.scenes]
    starts: list[float] = []
    idx = 0
    for n in counts:
        if idx < len(words):
            starts.append(words[idx].start)
        else:
            starts.append(starts[-1] + 1.0 if starts else voice_start)
        idx += n
    scenes: list[Scene] = []
    for i, sc in enumerate(script.scenes):
        start = intro_s if i == 0 else max(intro_s, starts[i] - 0.15)
        end = outro_start if i == len(script.scenes) - 1 else max(start + 1.0, starts[i + 1] - 0.15)
        vis = _scene_visual(sc, sources, _first_sentence(sc.spoken))
        kind = "hook" if i == 0 else vis["kind"]
        if kind not in ("hook", "card", "fact", "code", "payoff", "outro"):
            kind = "card"
        scenes.append(Scene(id=f"scene{i + 1}", start=round(start, 3), duration=round(end - start, 3), headline=vis["headline"],
                            body=vis["body"], kind=kind, source_label=vis["source_label"], code_lines=vis["code_lines"], number=vis["number"]))
    return scenes


def _post_json(script: scripting.Script, brand: Brand, video_id: str) -> dict:
    m = script.meta
    title = str(m.get("title", ""))[:100]
    desc = str(m.get("description", "")) or title
    tags = [str(t).lstrip("#") for t in m.get("hashtags", [])]
    ai_note = {"de": "KI-generiertes Video (Stimme und Grafik).", "en": "AI-generated video (voice and graphics)."}[script.language]
    base = {"title": title, "description": f"{desc}\n\n{ai_note}", "hashtags": tags}
    return {
        "video_id": video_id, "brand_id": brand.id, "language": script.language, "topic_id": script.topic_id,
        "title": title, "description": base["description"], "hashtags": tags,
        "labels": {"is_aigc": True, "is_ai_generated": True, "containsSyntheticMedia": True},
        "commercial": {"brand_content_toggle": False, "brand_organic_toggle": False, "hasPaidProductPlacement": False},
        "platforms": {
            "tiktok": {**base, "privacy_level": "PUBLIC_TO_EVERYONE"},
            "instagram": {**base},
            "youtube": {**base, "title": title[:100]},
        },
        "generated_at": _now(),
    }


def produce(script_path: Path, *, tts_provider: str | None = None, quality: str = "looks", gpu: bool = True,
            workers: int | str = 4, whisper_model: str = "small", force_mock_words: bool = False,
            db: StateDB | None = None, costs: CostLogger | None = None, publish_at: str | None = None,
            mirror_subfolder: str | None = "_Test", keep_project: bool = True) -> ProduceResult:
    ensure_dirs()
    db = db or StateDB()
    costs = costs or CostLogger()
    spec = VideoSpec.from_config()

    script = scripting.load(script_path)
    brand = load_brand(script.brand_id)
    lang = script.language
    video_id = f"{script.topic_id}-{lang}"
    risk = str(script.meta.get("risk_level", brand.risk_default))
    db.upsert_planned(video_id, script.topic_id, brand.id, lang, risk_level=risk, publish_at=publish_at,
                      meta={"script": str(script_path)})

    problems = scripting.check(script)
    if problems:
        if any("UNVERIFIED" in p for p in problems) or any("source" in p for p in problems):
            db.transition(video_id, "NEEDS_RESEARCH", "script_writer", "; ".join(problems))
            return ProduceResult(video_id, "NEEDS_RESEARCH", None, message="; ".join(problems))
        db.transition(video_id, "FAILED", "script_writer", "; ".join(problems))
        return ProduceResult(video_id, "FAILED", None, message="; ".join(problems))
    if db.state(video_id) in ("RENDERED", "VALIDATED", "HUMAN_REVIEW", "FAILED"):
        db.transition(video_id, "SCRIPTED", "pipeline", "re-produce from script")
    if db.state(video_id) == "PLANNED":
        db.transition(video_id, "RESEARCHED", "research_factcheck", f"{len(script.sources)} sources")
    if db.state(video_id) == "RESEARCHED":
        db.transition(video_id, "SCRIPTED", "script_writer", f"{script.word_count} words")

    space = check_free_space()
    if not space.ok:
        db.transition(video_id, "FAILED", "pipeline", space.message)
        return ProduceResult(video_id, "FAILED", None, message=space.message)

    folder = queue.video_dir(video_id, "drafts")
    project = folder / "project"
    if project.exists():
        shutil.rmtree(project)
    (project / "assets").mkdir(parents=True)
    t_all = time.perf_counter()

    # 1) TTS
    provider = get_provider(tts_provider)
    audio_cfg = brand.audio.get("tts", {})
    voice = brand.voice(lang)
    style = (audio_cfg.get("style_instruction") or {}).get(lang, "")
    rate = float(audio_cfg.get("speaking_rate", 1.0))
    tts = provider.synthesize(script.spoken_text, lang, voice, project / "assets" / "voice.wav", style=style, rate=rate)
    costs.log_tts(video_id, tts.provider, tts.input_chars, tts.output_tokens, tts.seconds)

    # 2) word timings
    mock_words = force_mock_words or tts.provider == "mock"
    tr = transcribe.transcribe(tts.path, lang, script_text=script.spoken_text, model_size=whisper_model, force_mock=mock_words)
    costs.log_transcribe(video_id, tr.elapsed, tr.model)
    words = transcribe.align_to_script(tr.words, script.spoken_text)

    # 3) timing
    intro_s = float(brand.intro.get("seconds", 1.6))
    outro_s = float(brand.outro.get("seconds", 4.0))
    voice_start = intro_s + VOICE_LEAD
    total = voice_start + tts.seconds + 0.4 + outro_s
    padded = 0.0
    if total < spec.min_seconds:
        padded = min(MAX_PAD, spec.min_seconds - total)
        total += padded
    if total < spec.min_seconds or total > spec.max_seconds:
        msg = f"video length {total:.1f} s outside {spec.min_seconds}-{spec.max_seconds} s (speech {tts.seconds:.1f} s); adjust the script"
        db.transition(video_id, "FAILED", "pipeline", msg)
        return ProduceResult(video_id, "FAILED", folder, message=msg)
    outro_start = total - outro_s
    shifted = [Word(w.text, round(w.start + voice_start, 3), round(w.end + voice_start, 3)) for w in words]
    scenes = plan_scenes(script, shifted, intro_s=intro_s, outro_start=outro_start, voice_start=voice_start)
    captions = group_words(shifted, int(brand.subtitle_style.get("group_words", 3)))
    comp = Composition(brand=brand, language=lang, duration=round(total, 3), scenes=scenes, captions=captions,
                       voice_file=tts.path, voice_start=voice_start, title=str(script.meta.get("title", video_id)))
    build_project(comp, project)
    check_report = hyperframes.check(project)
    (folder / "check.json").write_text(json.dumps(check_report, indent=2, ensure_ascii=False), encoding="utf-8")
    lint = check_report.get("lint", {})
    if lint.get("errorCount", 0):
        msg = f"hyperframes check: {lint.get('errorCount')} lint error(s)"
        db.transition(video_id, "FAILED", "video_producer", msg)
        return ProduceResult(video_id, "FAILED", folder, message=msg)

    # 4) render + encode
    t0 = time.perf_counter()
    raw = folder / "render_raw.mp4"
    res = hyperframes.render(project, raw, quality=quality, gpu=gpu, workers=workers)
    video = folder / "video.mp4"
    ffmpeg.encode_nvenc(raw, video, loudness_lufs=-16.0)
    render_seconds = time.perf_counter() - t0
    costs.log_render(video_id, render_seconds, f"hyperframes {quality} + nvenc")
    ffmpeg.extract_frame(video, folder / "cover.jpg", scenes[0].start + 0.8)
    raw.unlink(missing_ok=True)

    # 5) sidecar files
    shutil.copy2(script_path, folder / "script.md")
    post = _post_json(script, brand, video_id)
    (folder / "post.json").write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cap_json = [{"start": c.start, "end": c.end, "text": c.text, "words": [{"text": w.text, "start": w.start, "end": w.end} for w in c.words]} for c in captions]
    (folder / "captions.json").write_text(json.dumps(cap_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    used_fonts = sorted({brand.fonts.get("display", {}).get("family", "Inter"), brand.fonts.get("body", {}).get("family", "Inter"),
                         (brand.fonts.get("mono") or {}).get("family") or "JetBrains Mono", brand.subtitle_style.get("font_family", "Inter")})
    assets = [{"name": f"font:{f}", "kind": "font"} for f in used_fonts] + [{"name": "lib:gsap", "kind": "library"}, {"name": "voice.wav", "kind": "audio"}]
    licenses = [{"asset": f"font:{f}", "license": "OFL-1.1", "proof": f"assets/fonts/{f.lower().replace(' ', '')}/OFL.txt"} for f in used_fonts]
    licenses.append({"asset": "lib:gsap", "license": "GSAP Standard License (free incl. commercial since 3.13)", "proof": "assets/vendor/LICENSE-gsap.txt"})
    licenses.append({"asset": "voice.wav", "license": f"generated by {tts.provider} ({tts.model}); terms of the provider", "proof": "manifest.tts"})
    manifest = {
        "video_id": video_id, "topic_id": script.topic_id, "brand_id": brand.id, "brand_name": brand.name, "language": lang,
        "title": script.meta.get("title", ""), "risk_level": risk, "pipeline_version": __version__, "created_at": _now(),
        "sources": script.sources,
        "assets": assets, "licenses": licenses,
        "tts": {"provider": tts.provider, "model": tts.model, "voice": tts.voice, "seconds": tts.seconds,
                "input_chars": tts.input_chars, "output_tokens": tts.output_tokens, "usd": tts.usd, "notes": tts.notes},
        "transcription": {"model": tr.model, "device": tr.device, "mock": tr.mock, "elapsed": round(tr.elapsed, 2), "words": len(words)},
        "render": {"engine": "hyperframes 0.8.217", "quality": quality, "encoder": "h264_nvenc", "seconds": round(render_seconds, 1),
                   "duration": round(total, 3), "padded_seconds": round(padded, 2), "intro_seconds": intro_s, "outro_seconds": outro_s,
                   "art50_disclosure_seconds": float(brand.intro.get("art50_disclosure", {}).get("seconds", 0)) if brand.intro.get("art50_disclosure", {}).get("enabled") else 0.0,
                   "scenes": [{"id": s.id, "start": s.start, "duration": s.duration, "kind": s.kind} for s in scenes]},
        "models": {"script": "Claude Code (Stefan's Max plan)", "tts": tts.model, "transcription": tr.model},
        "ai_disclosure": {"labels": post["labels"], "text": brand.ai_label(lang)},
    }
    db.transition(video_id, "RENDERED", "video_producer", f"{total:.1f} s in {render_seconds:.0f} s render")

    # 6) validation
    report = compliance.Report(video_id)
    compliance.check_technical(report, video, cap_json, (voice_start, voice_start + tts.seconds), spec)
    compliance.check_content(report, manifest, script.spoken_text, post, brand.intro)
    if tts.provider == "mock":
        report.add("mock_voice", "review", False, "silent mock voice: technically checked, approval withheld until a real TTS run")
    manifest["cost"] = costs.summary(video_id)
    manifest["report"] = {"passed": report.passed, "needs_review": report.needs_review}
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    compliance.write_report(report, folder / "report.json")

    if not report.passed:
        db.transition(video_id, "FAILED", "compliance_check", "; ".join(f"{f.id}: {f.detail}" for f in report.failures))
        queue.move(video_id, "failed")
        final = "FAILED"
    else:
        db.transition(video_id, "VALIDATED", "compliance_check", "all fail-level checks passed")
        if report.needs_review or risk == "high":
            db.transition(video_id, "HUMAN_REVIEW", "compliance_check", "; ".join(f"{f.id}: {f.detail}" for f in report.findings if not f.ok))
            final = "HUMAN_REVIEW"
        else:
            db.transition(video_id, "APPROVED", "auto_approval", "all checks passed, risk not high")
            queue.move(video_id, "approved")
            final = "APPROVED"
    if not keep_project:
        shutil.rmtree(project, ignore_errors=True)
    if mirror_subfolder:
        queue.mirror(video_id, subfolder=mirror_subfolder)
    costs.log_render(video_id, 0.0, f"total pipeline {time.perf_counter() - t_all:.0f} s")
    return ProduceResult(video_id, final, queue.find(video_id)[1] if queue.find(video_id) else folder,
                         report=report.to_dict(), manifest=manifest, cost=manifest["cost"], message=f"{final}: {total:.1f} s")
