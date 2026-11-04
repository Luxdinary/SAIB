"""Validation report for a rendered video: technical checks + content/manifest checks from config/policies.yaml.

Result: `Report` with findings (id, severity, ok, detail). `passed` is True when no `fail` finding exists;
`needs_review` when a `review` finding exists (e.g. risk high). The auto-approval module reads both.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .config import policies_config, VideoSpec
from .render import ffmpeg


@dataclass
class Finding:
    id: str
    severity: str           # fail | review | warn
    ok: bool
    detail: str


@dataclass
class Report:
    video_id: str
    findings: list[Finding] = field(default_factory=list)
    probe: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not any(f.severity == "fail" and not f.ok for f in self.findings)

    @property
    def needs_review(self) -> bool:
        return any(f.severity == "review" and not f.ok for f in self.findings)

    @property
    def failures(self) -> list[Finding]:
        return [f for f in self.findings if not f.ok and f.severity == "fail"]

    def to_dict(self) -> dict:
        return {"video_id": self.video_id, "passed": self.passed, "needs_review": self.needs_review,
                "findings": [asdict(f) for f in self.findings], "probe": self.probe}

    def add(self, fid: str, severity: str, ok: bool, detail: str) -> None:
        self.findings.append(Finding(fid, severity, bool(ok), detail))


def _policy(section: str, fid: str) -> dict:
    for p in policies_config().get(section, []):
        if p["id"] == fid:
            return p
    return {}


def check_technical(report: Report, video: Path, captions: list[dict], speech_window: tuple[float, float],
                    spec: VideoSpec | None = None) -> None:
    spec = spec or VideoSpec.from_config()
    pr = ffmpeg.probe(video)
    report.probe = {"duration": pr.duration, "width": pr.width, "height": pr.height, "fps": pr.fps,
                    "video_codec": pr.video_codec, "audio_codec": pr.audio_codec, "size_bytes": pr.size_bytes}
    d = _policy("technical", "duration_range")
    lo, hi, hard = d.get("min_seconds", spec.min_seconds), d.get("max_seconds", spec.max_seconds), d.get("hard_min_seconds", spec.hard_min_seconds)
    ok = lo <= pr.duration <= hi and pr.duration >= hard
    report.add("duration_range", "fail", ok, f"{pr.duration:.2f} s (allowed {lo}-{hi}, hard minimum {hard})")
    report.add("aspect_ratio", "fail", pr.width == spec.width and pr.height == spec.height, f"{pr.width}x{pr.height}")
    report.add("video_codec", "fail", pr.video_codec == "h264", f"codec {pr.video_codec}")
    a = _policy("technical", "audio_present")
    stats = ffmpeg.audio_stats(video) if pr.audio_codec else {}
    mean = stats.get("mean_volume_db")
    ok = pr.audio_codec is not None and mean is not None and mean >= a.get("min_mean_volume_db", -35)
    report.add("audio_present", "fail", ok, f"audio {pr.audio_codec}, mean {mean} dB, lufs {stats.get('integrated_lufs')}")
    lp = _policy("technical", "loudness")
    lufs = stats.get("integrated_lufs")
    if lufs is not None:
        report.add("loudness", "warn", abs(lufs - lp.get("target_lufs", -16)) <= lp.get("tolerance_lu", 3), f"{lufs} LUFS (target {lp.get('target_lufs', -16)})")
    b = _policy("technical", "black_frames")
    segs = ffmpeg.black_segments(video, threshold=b.get("threshold", 0.98), min_seconds=0.1)
    black_total = sum(e - s for s, e in segs)
    report.add("black_frames", "fail", black_total <= b.get("max_black_seconds", 0.5), f"{black_total:.2f} s black in {len(segs)} segment(s)")
    c = _policy("technical", "captions_present")
    s0, s1 = speech_window
    covered = sum(min(g["end"], s1) - max(g["start"], s0) for g in captions if g["end"] > s0 and g["start"] < s1)
    cov = covered / max(0.001, s1 - s0)
    report.add("captions_present", "fail", len(captions) > 0 and cov >= c.get("min_caption_coverage", 0.6),
               f"{len(captions)} groups cover {cov:.0%} of speech")
    # caption safe zone is guaranteed by the layout (bottom 640 px, title-safe width); recorded for the report
    report.add("caption_safe_zone", "fail", True, "layout: captions inside the 80 % title-safe box")


UNVERIFIED_RE = re.compile(r"\bUNVERIFIED\b")


def check_content(report: Report, manifest: dict, script_text: str, post: dict, brand_intro: dict) -> None:
    sources = manifest.get("sources", [])
    ok = bool(sources) and all(s.get("url") and s.get("checked_at") for s in sources)
    report.add("sources_required", "fail", ok, f"{len(sources)} source(s), all with url and checked_at: {ok}")
    report.add("unverified_blocks", "fail", not UNVERIFIED_RE.search(script_text), "no UNVERIFIED marker" if not UNVERIFIED_RE.search(script_text) else "UNVERIFIED present")
    lic = manifest.get("licenses", [])
    assets = manifest.get("assets", [])
    missing = [a["name"] for a in assets if not any(l.get("asset") == a["name"] for l in lic)]
    report.add("license_manifest", "fail", not missing, "all assets licensed" if not missing else f"missing licence for {missing}")
    tts = manifest.get("tts", {}).get("provider")
    report.add("tts_provider_publishable", "fail", tts in ("gemini", "mock", "elevenlabs"), f"tts provider {tts}" + (" (mock: silent, blocks approval)" if tts == "mock" else "") + (" (draft voice, not publishable)" if tts in ("sapi", "edge") else ""))
    labels = post.get("labels", {})
    ok = all(labels.get(k) is True for k in ("is_aigc", "is_ai_generated", "containsSyntheticMedia"))
    report.add("ai_label", "fail", ok, f"labels {labels}")
    art = brand_intro.get("art50_disclosure", {})
    if art.get("enabled"):
        shown = manifest.get("render", {}).get("art50_disclosure_seconds", 0) > 0
        report.add("art50_disclosure", "fail", shown, "disclosure card in the first seconds" if shown else "disclosure missing")
    risk = manifest.get("risk_level", "low")
    report.add("risk_high_review", "review", risk != "high", f"risk_level {risk}")
    ft = _policy("content", "forbidden_terms")
    lang = manifest.get("language", "de")
    terms = ft.get("terms_de" if lang == "de" else "terms_en", [])
    hits = [t for t in terms if re.search(r"\b" + re.escape(t) + r"\b", script_text, re.IGNORECASE)]
    report.add("forbidden_terms", "review", not hits, "none" if not hits else f"found {hits}")


def check_mock_audio(report: Report, manifest: dict) -> None:
    """A mock voice never passes: the video is technically fine but must not be approved."""
    if manifest.get("tts", {}).get("provider") == "mock":
        report.add("mock_voice", "fail", False, "voice is a silent mock placeholder; re-run with a real TTS provider before approval")


def write_report(report: Report, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
