"""edge-tts adapter for audible drafts only (free Microsoft Edge voices; licence for commercial use unclear).

Never used for published videos: the compliance check rejects manifests whose TTS provider is `edge`.
Requires `pip install edge-tts`; absent package -> clear error, no silent fallback.
"""
from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

from ..config import voices_config
from ..render.ffmpeg import audio_duration
from . import TTSResult


class EdgeTTS:
    name = "edge"

    def synthesize(self, text: str, language: str, voice: str, out_path: Path, *, style: str = "", rate: float = 1.0) -> TTSResult:
        try:
            import edge_tts  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("edge-tts not installed (pip install edge-tts); drafts only") from exc
        cfg = voices_config()["providers"]["edge"]
        edge_voice = cfg["voices"].get(language, voice)
        pct = int(round((rate - 1.0) * 100))
        rate_str = f"{'+' if pct >= 0 else ''}{pct}%"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        mp3 = out_path.with_suffix(".mp3")

        async def _run():
            communicate = edge_tts.Communicate(text, edge_voice, rate=rate_str)
            await communicate.save(str(mp3))

        asyncio.run(_run())
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp3), "-ar", "24000", "-ac", "1", str(out_path)], check=True)
        return TTSResult(path=out_path, seconds=audio_duration(out_path), provider="edge", model="edge-tts", voice=edge_voice,
                         input_chars=len(text), output_tokens=0, usd=0.0, notes="draft only, not for publishing")
