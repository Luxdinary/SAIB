"""Programmatic sound effects for Zonkfruit (synthesised with numpy, no samples, no third-party rights).

Run once: .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\sfx.py  -> brands/brainrot/assets/sfx/*.wav + LICENSE.md
Deterministic (fixed random seed), so the files can be regenerated identically at any time.
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SR = 48000
OUT = Path(__file__).resolve().parent.parent / "assets" / "sfx"
RNG = np.random.default_rng(20261030)


def _t(sec: float) -> np.ndarray:
    return np.arange(int(SR * sec)) / SR


def _env(n: int, attack: float, decay: float) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def _sine_sweep(f0: float, f1: float, sec: float, curve: float = 1.0) -> np.ndarray:
    t = _t(sec)
    f = f0 + (f1 - f0) * (t / sec) ** curve
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def boing() -> np.ndarray:
    t = _t(0.55)
    f = 180 + 140 * np.exp(-t * 6) * np.sin(2 * np.pi * 9 * t)       # wobbling pitch like a spring
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * _env(len(t), 0.004, 0.18)


def pop() -> np.ndarray:
    s = _sine_sweep(900, 260, 0.09, 0.5)
    return s * _env(len(s), 0.001, 0.03)


def whoosh() -> np.ndarray:
    n = int(SR * 0.42)
    noise = RNG.standard_normal(n)
    k = np.hanning(200)
    k /= k.sum()
    low = np.convolve(noise, k, mode="same")                          # soft low-passed noise
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return low * env * 6


def scan() -> np.ndarray:
    t = _t(0.7)
    s = np.sign(np.sin(2 * np.pi * (520 + 380 * np.sin(2 * np.pi * 2.2 * t)) * t)) * 0.25
    return s * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)) * _env(len(t), 0.02, 0.5)


def buzz() -> np.ndarray:
    t = _t(0.45)
    s = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 113 * t)) * 0.3
    env = np.clip(t / 0.01, 0, 1) * np.clip((0.45 - t) / 0.06, 0, 1)
    return s * env


def chime() -> np.ndarray:
    a = np.sin(2 * np.pi * 880 * _t(0.5)) * _env(int(SR * 0.5), 0.003, 0.18)
    b = np.sin(2 * np.pi * 1318.5 * _t(0.6)) * _env(int(SR * 0.6), 0.003, 0.22)
    out = np.zeros(int(SR * 0.72))
    out[:len(a)] += a
    off = int(SR * 0.12)
    out[off:off + len(b)] += b
    return out


def unknown() -> np.ndarray:
    a = _sine_sweep(660, 640, 0.22) * _env(int(SR * 0.22), 0.005, 0.12)
    b = _sine_sweep(520, 360, 0.42, 1.5) * _env(int(SR * 0.42), 0.005, 0.2)
    out = np.zeros(int(SR * 0.7))
    out[:len(a)] += a
    out[int(SR * 0.24):int(SR * 0.24) + len(b)] += b
    return out


def plumps() -> np.ndarray:
    t = _t(0.5)
    body = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 7) + 45) / SR)
    click = RNG.standard_normal(len(t)) * np.exp(-t / 0.008) * 0.4
    return (body + click) * _env(len(t), 0.002, 0.14)


SOUNDS = {"boing": boing, "pop": pop, "whoosh": whoosh, "scan": scan, "buzz": buzz, "chime": chime, "unknown": unknown, "plumps": plumps}


def write(name: str, s: np.ndarray) -> Path:
    s = s / (np.max(np.abs(s)) + 1e-9) * 0.7                          # peak -3 dBFS before mixing
    pcm = (s * 32767).astype(np.int16)
    p = OUT / f"{name}.wav"
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return p


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# Lizenz der Soundeffekte (Zonkfruit)", "",
             "Alle Dateien in diesem Ordner sind mit `brands/brainrot/renderer/sfx.py` aus Sinuswellen, Rechteckwellen und",
             "Rauschen synthetisiert (numpy, fester Zufallsstartwert). Keine Samples, keine Fremdaufnahmen, keine Rechte Dritter.",
             "Erstellt 30.10.2026 von Claude Code für Stefan Dallinger; frei verwendbar für alle Zonkfruit-Videos.", ""]
    for name, fn in SOUNDS.items():
        write(name, fn())
        lines.append(f"{name}.wav: selbst erzeugt (sfx.py, Funktion `{name}`), keine Fremdrechte")
    (OUT / "LICENSE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(SOUNDS)} sounds -> {OUT}")


if __name__ == "__main__":
    main()
