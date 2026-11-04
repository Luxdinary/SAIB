"""Windows SAPI (System.Speech) draft voice: free, offline, no key. Drafts only, never for publishing.

Used to hear a script and to test the whisper word-timing path before a Gemini key exists.
The compliance check rejects manifests whose TTS provider is `sapi`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from ..render.ffmpeg import audio_duration
from . import TTSResult

CULTURE = {"de": "de-", "en": "en-"}


class SapiTTS:
    name = "sapi"

    def synthesize(self, text: str, language: str, voice: str, out_path: Path, *, style: str = "", rate: float = 1.0) -> TTSResult:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        raw = out_path.with_name(out_path.stem + "_sapi.wav")
        txt = out_path.with_name(out_path.stem + "_sapi.txt")
        txt.write_text(text, encoding="utf-8")
        sapi_rate = max(-10, min(10, int(round((rate - 1.0) * 10))))
        culture = CULTURE.get(language, "en-")
        ps = f"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$v = $s.GetInstalledVoices() | Where-Object {{ $_.VoiceInfo.Culture.Name -like '{culture}*' -and $_.Enabled }} | Select-Object -First 1
if ($v) {{ $s.SelectVoice($v.VoiceInfo.Name) }}
$s.Rate = {sapi_rate}
$s.SetOutputToWaveFile('{raw}')
$s.Speak([IO.File]::ReadAllText('{txt}', [Text.Encoding]::UTF8))
$s.Dispose()
Write-Output ($(if ($v) {{ $v.VoiceInfo.Name }} else {{ 'default' }}))
"""
        proc = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, text=True, timeout=600)
        if proc.returncode != 0 or not raw.exists():
            raise RuntimeError(f"SAPI synthesis failed: {proc.stderr[-500:]}")
        used_voice = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "default"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw), "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out_path)], check=True)
        raw.unlink(missing_ok=True)
        return TTSResult(path=out_path, seconds=audio_duration(out_path), provider="sapi", model="System.Speech", voice=used_voice,
                         input_chars=len(text), output_tokens=0, usd=0.0, notes="Windows draft voice, not for publishing")
