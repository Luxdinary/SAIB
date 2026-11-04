"""Cost logger per video: TTS tokens, clips, Claude calls, render time. JSON lines in data/costs/."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

from .config import DATA_DIR

# List prices (USD), from Faktencheck 2026-10-29 / provider pricing pages. Update with a date when they change.
PRICES = {
    "gemini_tts_output_per_million_tokens": 10.0,     # ai.google.dev pricing, upper end of 9-10 USD
    "gemini_tts_input_per_million_tokens": 0.5,       # NOT_VERIFIED exact; small share of the cost
    "runway_gen4_turbo_clip_8s": 0.40,
    "claude_max_per_video_estimate": 0.70,            # 100-200 USD/month over ~210 videos; measured, not billed
    "electricity_per_render_minute": 0.0,             # not accounted (Stefan's decision)
}


@dataclass
class CostEntry:
    video_id: str
    kind: str                 # tts | clip | claude_call | render | transcribe | image
    units: float              # tokens, clips, calls, seconds
    unit_name: str
    usd: float
    provider: str = ""
    note: str = ""
    at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


class CostLogger:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else DATA_DIR / "costs" / "costs.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: CostEntry) -> CostEntry:
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        return entry

    def log_tts(self, video_id: str, provider: str, input_chars: int, output_tokens: int, audio_seconds: float) -> CostEntry:
        usd = 0.0
        if provider == "gemini":
            usd = output_tokens / 1e6 * PRICES["gemini_tts_output_per_million_tokens"]
        return self.log(CostEntry(video_id, "tts", output_tokens, "audio_tokens", round(usd, 5), provider,
                                  f"{input_chars} chars -> {audio_seconds:.1f} s audio"))

    def log_render(self, video_id: str, seconds: float, note: str = "") -> CostEntry:
        return self.log(CostEntry(video_id, "render", round(seconds, 1), "seconds", 0.0, "local", note))

    def log_transcribe(self, video_id: str, seconds: float, model: str) -> CostEntry:
        return self.log(CostEntry(video_id, "transcribe", round(seconds, 1), "seconds", 0.0, "local", model))

    def log_claude_call(self, video_id: str, purpose: str, input_tokens: int = 0, output_tokens: int = 0) -> CostEntry:
        return self.log(CostEntry(video_id, "claude_call", 1, "call", 0.0, "claude_max",
                                  f"{purpose}; in={input_tokens} out={output_tokens} (covered by Max subscription)"))

    def log_clip(self, video_id: str, provider: str, usd: float, note: str = "") -> CostEntry:
        return self.log(CostEntry(video_id, "clip", 1, "clip", usd, provider, note))

    def entries(self, video_id: str | None = None) -> list[dict]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if video_id is None or e["video_id"] == video_id:
                out.append(e)
        return out

    def summary(self, video_id: str) -> dict:
        es = self.entries(video_id)
        by_kind: dict[str, dict] = {}
        for e in es:
            k = by_kind.setdefault(e["kind"], {"units": 0.0, "usd": 0.0, "count": 0})
            k["units"] += e["units"]
            k["usd"] += e["usd"]
            k["count"] += 1
        total = sum(v["usd"] for v in by_kind.values())
        claude_calls = by_kind.get("claude_call", {}).get("count", 0)
        return {
            "video_id": video_id,
            "by_kind": by_kind,
            "usd_variable": round(total, 4),
            "usd_with_claude_estimate": round(total + (PRICES["claude_max_per_video_estimate"] if claude_calls else 0.0), 4),
            "render_seconds": by_kind.get("render", {}).get("units", 0.0),
        }
