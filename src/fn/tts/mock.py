"""Mock TTS: writes a quiet pulsing tone of the estimated speech length. Costs nothing, needs no key."""
from __future__ import annotations

from pathlib import Path

from ..config import voices_config
from ..render.ffmpeg import tone_wav
from . import TTSResult


class MockTTS:
    name = "mock"

    def estimate_seconds(self, text: str, language: str, rate: float = 1.0) -> float:
        wps = voices_config()["providers"]["mock"]["words_per_second"].get(language, 2.5) * rate
        words = max(1, len(text.split()))
        # a short pause per sentence end
        pauses = text.count(".") + text.count("!") + text.count("?")
        return round(words / wps + pauses * 0.35, 2)

    def synthesize(self, text: str, language: str, voice: str, out_path: Path, *, style: str = "", rate: float = 1.0) -> TTSResult:
        seconds = self.estimate_seconds(text, language, rate)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tone_wav(out_path, seconds)
        return TTSResult(path=out_path, seconds=seconds, provider="mock", model="mock", voice=voice,
                         input_chars=len(text), output_tokens=0, usd=0.0, notes="silent placeholder, not for publishing")
