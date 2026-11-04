"""Gemini Flash TTS adapter (paid tier). Only used when GEMINI_API_KEY is set in .env.

API shape per ai.google.dev/gemini-api/docs/speech-generation (read 2026-10-30):
  client.models.generate_content(model="gemini-2.5-flash-preview-tts", contents=text,
      config=GenerateContentConfig(response_modalities=["AUDIO"],
          speech_config=SpeechConfig(voice_config=VoiceConfig(prebuilt_voice_config=PrebuiltVoiceConfig(voice_name="Kore")))))
Response: inline_data.data = PCM 16-bit, 24 kHz, mono. Token usage in response.usage_metadata.
Anything beyond that is NOT_VERIFIED and not used here.
"""
from __future__ import annotations

import wave
from pathlib import Path

from ..config import env, voices_config
from . import TTSResult


class GeminiTTS:
    name = "gemini"

    def __init__(self, model: str | None = None):
        cfg = voices_config()["providers"]["gemini"]
        # GEMINI_TTS_MODEL=<fallback_model> switches a whole run to the fallback (Stefan, 02.11.2026: Pro voice only
        # when the Flash daily quota is used up, and only for whole videos, never mixed within one video or episode)
        self.model = model or env("GEMINI_TTS_MODEL") or cfg["model"]
        self.sample_rate = int(cfg.get("sample_rate", 24000))
        price_key = ("fallback_cost_usd_per_million_output_tokens" if self.model == cfg.get("fallback_model")
                     else "cost_usd_per_million_output_tokens")
        self.price_out = float(cfg.get(price_key, 10.0))
        key = env("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY not set in .env; use the mock provider")
        from google import genai  # imported lazily so the mock path has no dependency
        self._genai = genai
        self._client = genai.Client(api_key=key)

    def synthesize(self, text: str, language: str, voice: str, out_path: Path, *, style: str = "", rate: float = 1.0) -> TTSResult:
        types = self._genai.types
        prompt = f"{style.strip()}\n\n{text}" if style.strip() else text
        resp = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice))
                ),
            ),
        )
        part = resp.candidates[0].content.parts[0]
        pcm = part.inline_data.data
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(out_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm)
        seconds = len(pcm) / (2 * self.sample_rate)
        usage = getattr(resp, "usage_metadata", None)
        out_tokens = int(getattr(usage, "candidates_token_count", 0) or 0) if usage else 0
        in_tokens = int(getattr(usage, "prompt_token_count", 0) or 0) if usage else 0
        usd = out_tokens / 1e6 * self.price_out
        return TTSResult(path=out_path, seconds=round(seconds, 3), provider="gemini", model=self.model, voice=voice,
                         input_chars=len(text), output_tokens=out_tokens, usd=round(usd, 5),
                         notes=f"prompt_tokens={in_tokens}")
