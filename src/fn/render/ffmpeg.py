"""FFmpeg / FFprobe helpers: probe, NVENC encode, black-frame and audio analysis, cover frame."""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class FFmpegError(RuntimeError):
    pass


def _bin(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise FFmpegError(f"{name} not found on PATH")
    return path


def run(args: list[str], timeout: int = 1800) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if proc.returncode != 0:
        raise FFmpegError(f"{args[0]} failed ({proc.returncode}): {proc.stderr[-2000:]}")
    return proc


@dataclass
class ProbeResult:
    duration: float
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: str | None
    audio_channels: int
    audio_sample_rate: int
    size_bytes: int

    @property
    def aspect(self) -> float:
        return self.width / self.height if self.height else 0.0


def probe(path: Path) -> ProbeResult:
    proc = run([_bin("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    data = json.loads(proc.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    if video is None:
        raise FFmpegError(f"no video stream in {path}")
    num, _, den = video.get("r_frame_rate", "30/1").partition("/")
    fps = float(num) / float(den or 1)
    return ProbeResult(
        duration=float(data["format"].get("duration", 0.0)),
        width=int(video["width"]), height=int(video["height"]), fps=fps,
        video_codec=video.get("codec_name", ""),
        audio_codec=audio.get("codec_name") if audio else None,
        audio_channels=int(audio.get("channels", 0)) if audio else 0,
        audio_sample_rate=int(audio.get("sample_rate", 0)) if audio else 0,
        size_bytes=int(data["format"].get("size", 0)),
    )


def audio_duration(path: Path) -> float:
    proc = run([_bin("ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(proc.stdout.strip() or 0.0)


def loudnorm_measure(path: Path, *, target: float = -16.0, tp: float = -1.5, lra: float = 20.0) -> dict:
    """First pass of a two-pass loudnorm: the input values (input_i, input_tp, input_lra, input_thresh) as floats."""
    proc = subprocess.run([_bin("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af",
                           f"loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", proc.stderr, re.S)
    if not m:
        return {}
    out: dict = {}
    for k, v in json.loads(m.group(0)).items():
        try:
            out[k] = float(v)
        except (TypeError, ValueError):
            out[k] = v
    return out


def encode_nvenc(src: Path, dst: Path, *, audio: Path | None = None, cq: int = 23,
                 fps: int = 30, loudness_lufs: float | None = -16.0, timeout: int = 1800,
                 loudnorm: str = "dynamic") -> dict:
    """Re-encode to H.264 NVENC + AAC in a 9:16 MP4 with faststart. Optionally mux a separate audio file.

    `loudnorm="dynamic"` (default, unchanged): single-pass loudnorm, which rides its gain and lifts quiet passages.
    `loudnorm="linear"` (sound layer, since 03.11.2026): measures the audio first and applies loudnorm as one static
    gain (two-pass, `linear=true`, LRA target 20 so it never falls back to dynamic for narration with pauses), so a
    short sound effect in a pause keeps its level instead of being pushed into the limiter (Gritwerk finding,
    03.11.2026: clicks reached 0.0 dB after AAC). Falls back to dynamic when the measurement is unusable.
    Returns {"loudnorm": "dynamic" | "linear" | "off", "measured": {...}, "normalization_type": <loudnorm report>}.
    """
    info: dict = {"loudnorm": "off", "measured": {}}
    linear = False
    chain = ""
    if loudness_lufs is not None:
        # loudnorm runs at 192 kHz; resample to the 48 kHz output first so the limiter sees the final samples
        # (Prüfrunde 03.11.2026, R6: single-pass loudnorm let true peaks reach -0.8 dBFS; Revlore 02.11.: limiting
        # at 192 kHz still let -0.4 dB through after resampling and AAC, so limit at 48 kHz to -2 dBFS)
        chain = f"loudnorm=I={loudness_lufs}:TP=-1.5:LRA=11"
        info["loudnorm"] = "dynamic"
        if loudnorm == "linear":
            meas = loudnorm_measure(audio if audio is not None else src, target=loudness_lufs)
            vals = {k: meas.get(k) for k in ("input_i", "input_tp", "input_lra", "input_thresh")}
            ok = all(isinstance(v, float) and math.isfinite(v) for v in vals.values()) and vals["input_i"] > -60
            if ok:
                # loudnorm refuses linear mode (and silently goes dynamic) when the static gain would push the true peak
                # over the TP target; then aim a little lower instead (the LUFS check tolerates +/- 2 LU)
                target_i = float(loudness_lufs)
                tp_after = vals["input_tp"] + (target_i - vals["input_i"])
                if tp_after > -1.5:
                    target_i = round(target_i - (tp_after + 1.5) - 0.1, 2)
                chain = (f"loudnorm=I={target_i}:TP=-1.5:LRA=20:measured_I={vals['input_i']:.2f}:measured_TP={vals['input_tp']:.2f}:"
                         f"measured_LRA={vals['input_lra']:.2f}:measured_thresh={vals['input_thresh']:.2f}:linear=true:print_format=json")
                info["loudnorm"] = "linear"
                info["measured"] = vals
                info["target_i"] = target_i
                linear = True
        chain += ",aresample=48000,alimiter=limit=0.79:attack=5:release=50:level=false"
    args = [_bin("ffmpeg"), "-y", "-hide_banner", "-nostats", "-loglevel", "info" if linear else "error", "-i", str(src)]
    if audio is not None:
        args += ["-i", str(audio), "-map", "0:v:0", "-map", "1:a:0"]
    args += ["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", str(cq), "-b:v", "0",
             "-maxrate", "12M", "-bufsize", "24M", "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-r", str(fps), "-g", str(fps * 2), "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
    if chain:
        args += ["-af", chain]
    args += ["-movflags", "+faststart", "-shortest", str(dst)]
    proc = run(args, timeout=timeout)
    if linear:
        m = re.search(r"\"normalization_type\"\s*:\s*\"([A-Za-z]+)\"", proc.stderr or "")
        info["normalization_type"] = m.group(1) if m else "unknown"
    return info


def black_segments(path: Path, threshold: float = 0.98, min_seconds: float = 0.1) -> list[tuple[float, float]]:
    proc = subprocess.run([_bin("ffmpeg"), "-hide_banner", "-i", str(path), "-vf",
                           f"blackdetect=d={min_seconds}:pic_th={threshold}", "-an", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = []
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", proc.stderr):
        out.append((float(m.group(1)), float(m.group(2))))
    return out


def audio_stats(path: Path, *, dual_mono: bool = False) -> dict:
    """mean/max volume (dB) and integrated loudness (LUFS) of the first audio stream.

    `dual_mono=True` (mono input only) measures the file as the same signal on both stereo channels at full level
    (EBU R128 sums the channels: +3 LU against the mono reading), i.e. the way a mono voice sits in the stereo mix
    (sound layer, 03.11.2026). ffmpeg's own mono-to-stereo upmix would attenuate by 3 dB and hide that."""
    pre = "pan=stereo|c0=c0|c1=c0," if dual_mono else ""
    proc = subprocess.run([_bin("ffmpeg"), "-hide_banner", "-i", str(path), "-vn",
                           "-af", f"{pre}volumedetect,ebur128=framelog=quiet", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    stats: dict = {"mean_volume_db": None, "max_volume_db": None, "integrated_lufs": None}
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", proc.stderr)
    if m:
        stats["mean_volume_db"] = float(m.group(1))
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", proc.stderr)
    if m:
        stats["max_volume_db"] = float(m.group(1))
    m = re.search(r"I:\s*(-?[\d.]+) LUFS", proc.stderr)
    if m:
        stats["integrated_lufs"] = float(m.group(1))
    return stats


def extract_frame(path: Path, dst: Path, at_seconds: float, *, quality: int = 3) -> None:
    run([_bin("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{at_seconds:.3f}",
         "-i", str(path), "-frames:v", "1", "-q:v", str(quality), str(dst)])


def silent_wav(dst: Path, seconds: float, sample_rate: int = 24000) -> None:
    run([_bin("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
         "-i", f"anullsrc=r={sample_rate}:cl=mono", "-t", f"{seconds:.3f}", "-c:a", "pcm_s16le", str(dst)])


def tone_wav(dst: Path, seconds: float, sample_rate: int = 24000, gain_db: float = -18.0) -> None:
    """Quiet test tone with a slow pulse, so audio checks have something to measure in mock runs."""
    run([_bin("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
         "-i", f"sine=frequency=220:sample_rate={sample_rate}", "-t", f"{seconds:.3f}",
         "-af", f"tremolo=f=0.5:d=0.7,volume={gain_db}dB", "-c:a", "pcm_s16le", str(dst)])


def nvenc_available() -> bool:
    try:
        proc = subprocess.run([_bin("ffmpeg"), "-hide_banner", "-encoders"], capture_output=True, text=True)
    except FFmpegError:
        return False
    return "h264_nvenc" in proc.stdout
