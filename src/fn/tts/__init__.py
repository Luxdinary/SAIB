"""TTS adapters with one interface: synthesize(text, language, voice, out_path) -> TTSResult."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..config import has_secret, voices_config


@dataclass
class TTSResult:
    path: Path
    seconds: float
    provider: str
    model: str
    voice: str
    input_chars: int
    output_tokens: int          # audio tokens billed (0 for mock)
    usd: float = 0.0
    notes: str = ""


class TTSProvider(Protocol):
    name: str

    def synthesize(self, text: str, language: str, voice: str, out_path: Path, *, style: str = "", rate: float = 1.0) -> TTSResult: ...


def get_provider(name: str | None = None) -> "TTSProvider":
    """Pick the provider: explicit name, else gemini if GEMINI_API_KEY is set, else mock."""
    cfg = voices_config()
    name = name or ("gemini" if has_secret("GEMINI_API_KEY") else cfg.get("default_provider", "mock"))
    if name == "gemini":
        from .gemini import GeminiTTS
        return GeminiTTS()
    if name == "mock":
        from .mock import MockTTS
        return MockTTS()
    if name in ("sapi", "edge"):
        raise RuntimeError(f"TTS provider {name!r} is blocked: Stefan, 30.10.2026 - only Google (Gemini) voices, no Windows voice")
    raise ValueError(f"unknown TTS provider {name!r}")
