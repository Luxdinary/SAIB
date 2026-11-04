"""Word timings: faster-whisper on CUDA (RTX 5080) with a mock fallback for silent placeholder audio.

The mock spreads the script's words evenly over the audio length, so the chain can run end to end
before a real TTS key exists. The manifest records which path was used.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path

from .render.compose import Word
from .render.ffmpeg import audio_duration


@dataclass
class TranscriptResult:
    words: list[Word]
    seconds: float            # audio length
    elapsed: float            # compute time
    model: str
    device: str
    language: str
    mock: bool = False


def _add_cuda_dll_dirs() -> None:
    """Make the pip-installed cuBLAS / cuDNN DLLs visible to ctranslate2 on Windows."""
    if os.name != "nt":
        return
    try:
        import nvidia  # type: ignore
    except ImportError:
        return
    for base in nvidia.__path__:
        for sub in ("cublas", "cudnn"):
            d = Path(base) / sub / "bin"
            if d.exists():
                os.add_dll_directory(str(d))
                os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")


def _decode_audio(path: Path, sample_rate: int = 16000):
    """Decode with FFmpeg to float32 mono PCM (avoids the PyAV dependency of faster-whisper)."""
    import subprocess
    import numpy as np
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-f", "f32le", "-ac", "1",
                           "-ar", str(sample_rate), "-"], capture_output=True, check=True)
    return np.frombuffer(proc.stdout, dtype=np.float32)


def mock_words(text: str, seconds: float, start: float = 0.0) -> list[Word]:
    tokens = text.split()
    if not tokens:
        return []
    weights = [max(1, len(t)) + (2 if t.endswith((".", "!", "?")) else 0) for t in tokens]
    total = sum(weights)
    out, t = [], start
    for tok, w in zip(tokens, weights):
        d = seconds * w / total
        out.append(Word(text=tok, start=round(t, 3), end=round(t + d * 0.9, 3)))
        t += d
    return out


def transcribe(audio: Path, language: str, *, script_text: str | None = None, model_size: str = "small",
               device: str = "auto", force_mock: bool = False) -> TranscriptResult:
    seconds = audio_duration(audio)
    if force_mock:
        return TranscriptResult(words=mock_words(script_text or "", seconds), seconds=seconds, elapsed=0.0,
                                model="mock", device="none", language=language, mock=True)
    t0 = time.perf_counter()
    _add_cuda_dll_dirs()
    from faster_whisper import WhisperModel  # heavy import, kept local

    dev = device
    compute = "float16"
    if device == "auto":
        try:
            import ctranslate2  # type: ignore
            dev = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
        except Exception:  # noqa: BLE001
            dev = "cpu"
    if dev == "cpu":
        compute = "int8"
    model = WhisperModel(model_size, device=dev, compute_type=compute)
    segments, info = model.transcribe(_decode_audio(audio), language=language, word_timestamps=True, vad_filter=True)
    words: list[Word] = []
    for seg in segments:
        for w in seg.words or []:
            txt = w.word.strip()
            if txt and not all(ch in "♪�" for ch in txt):
                words.append(Word(text=txt, start=round(float(w.start), 3), end=round(float(w.end), 3)))
    elapsed = time.perf_counter() - t0
    if script_text and len(words) < 0.5 * len(script_text.split()):
        # whisper failed on this audio (e.g. silent mock) -> fall back to even spacing, flagged as mock
        return TranscriptResult(words=mock_words(script_text, seconds), seconds=seconds, elapsed=elapsed,
                                model=f"{model_size} (fallback mock)", device=dev, language=language, mock=True)
    return TranscriptResult(words=words, seconds=seconds, elapsed=elapsed, model=model_size, device=dev, language=language)


def align_to_script(words: list[Word], script_text: str) -> list[Word]:
    """Captions show the script's own words; timings come from whisper.

    Tokens are matched with difflib (case- and punctuation-insensitive). Script words whisper missed get
    timings interpolated between their matched neighbours, so every script word has a time.
    """
    import difflib
    import re

    tokens = script_text.split()
    if not tokens:
        return []
    if not words:
        return []
    norm = lambda t: re.sub(r"[^" + chr(92) + "w]", "", t.lower())  # noqa: E731
    a = [norm(t) for t in tokens]
    b = [norm(w.text) for w in words]
    times: list[tuple[float, float] | None] = [None] * len(tokens)
    for blk in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w = words[blk.b + k]
            times[blk.a + k] = (w.start, w.end)
    # interpolate gaps
    known = [i for i, t in enumerate(times) if t is not None]
    if not known:
        return mock_words(script_text, words[-1].end - words[0].start, words[0].start)
    out: list[Word] = []
    i = 0
    while i < len(tokens):
        if times[i] is not None:
            out.append(Word(tokens[i], times[i][0], times[i][1]))
            i += 1
            continue
        j = i
        while j < len(tokens) and times[j] is None:
            j += 1
        t0 = out[-1].end if out else max(0.0, (times[j][0] if j < len(tokens) else words[0].start) - 0.4 * (j - i))
        t1 = times[j][0] if j < len(tokens) else (out[-1].end + 0.4 * (j - i) if out else words[-1].end)
        n = j - i
        step = max(0.05, (t1 - t0) / n)
        for k in range(n):
            s0 = t0 + k * step
            out.append(Word(tokens[i + k], round(s0, 3), round(max(s0 + 0.05, min(t1, s0 + step * 0.9)), 3)))
        i = j
    return out
