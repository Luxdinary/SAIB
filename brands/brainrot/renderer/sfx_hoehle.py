"""Eigene Klänge für Tintora (ab Testreel F1-06): Tropfen, Flügelschwirren, Summen, Höhlen-Grundton, Bienen.

Synthetisiert mit numpy aus Sinuswellen und gefiltertem Rauschen, fester Zufallsstartwert, keine Samples, keine
Rechte Dritter. Schreibt brands/brainrot/assets/sfx/{bienen,tropfen,fluegel,summen,hoehle}.wav und ergänzt LICENSE.md.
  .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\sfx_hoehle.py
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SR = 48000
OUT = Path(__file__).resolve().parent.parent / "assets" / "sfx"
RNG = np.random.default_rng(20261103)


def _t(sec: float) -> np.ndarray:
    return np.arange(int(SR * sec)) / SR


def _lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    f = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    f *= 1 / (1 + (fr / cutoff) ** 4)
    return np.fft.irfft(f, len(x))


def _reverb(x: np.ndarray, seconds: float, decay: float, mix: float) -> np.ndarray:
    """Hall aus abklingendem Rauschen (Faltung), für die Höhle."""
    ir = RNG.standard_normal(int(SR * seconds)) * np.exp(-_t(seconds) / decay)
    ir = _lowpass(ir, 3500)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = np.fft.irfft(np.fft.rfft(np.concatenate([x, np.zeros(len(ir))])) * np.fft.rfft(np.concatenate([ir, np.zeros(len(x))])))
    dry = np.concatenate([x, np.zeros(len(ir))])
    return dry * (1 - mix) + wet[:len(dry)] * mix


def tropfen() -> np.ndarray:
    """Wassertropfen: kurzer Ton mit schnell steigender Tonhöhe, dann langer Höhlenhall."""
    t = _t(0.12)
    f = 900 + 1700 * (t / t[-1]) ** 0.6
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03) * np.clip(t / 0.002, 0, 1)
    return _reverb(s, 1.6, 0.45, 0.55)


def fluegel() -> np.ndarray:
    """Leises Flügelschwirren: Rauschen, im Flügeltakt (32 Hz) moduliert, weich ein und aus."""
    t = _t(1.6)
    n = _lowpass(RNG.standard_normal(len(t)), 2400)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 32 * t)
    env = np.clip(np.sin(np.pi * t / t[-1]), 0, None) ** 1.5
    return n * am * env


def summen() -> np.ndarray:
    """Tiefes, warmes Summen, das 8,4 s lang anschwillt und dann abbricht (kurze 40-ms-Blende)."""
    t = _t(8.4)
    base = 110.0
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
    s = sum(a * np.sin(2 * np.pi * base * k * np.cumsum(vib) / SR) for k, a in ((1, 1.0), (2, 0.45), (3, 0.22), (5, 0.08)))
    s *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * t)
    env = np.clip(t / 6.0, 0, 1) ** 1.6
    env[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
    return s * env


def hoehle() -> np.ndarray:
    """Höhlen-Grundton: dunkles gefiltertes Rauschen mit leiser Quinte, 9,6 s, weich ein und aus."""
    t = _t(9.6)
    n = _lowpass(RNG.standard_normal(len(t)), 260) * 3.0
    tone = 0.35 * np.sin(2 * np.pi * 55 * t) + 0.18 * np.sin(2 * np.pi * 82.4 * t)
    env = np.clip(t / 1.2, 0, 1) * np.clip((t[-1] - t) / 1.8, 0, 1)
    return (n + tone) * env


def bienen() -> np.ndarray:
    """Freundliches Bienensummen: Sägezahn um 230 Hz mit Flügel-Tremolo, leicht schwankend, 3 s, weich ein und aus."""
    t = _t(3.0)
    f = 230 * (1 + 0.03 * np.sin(2 * np.pi * 1.3 * t) + 0.01 * np.sin(2 * np.pi * 7 * t))
    ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1.0) - 1
    s = _lowpass(saw, 1800) * (0.7 + 0.3 * np.sin(2 * np.pi * 24 * t))
    env = np.clip(t / 0.4, 0, 1) * np.clip((t[-1] - t) / 0.6, 0, 1)
    return s * env


SOUNDS = {
    "bienen": (bienen, "Bienensummen"),
    "tropfen": (tropfen, "Wassertropfen mit Höhlenhall"),
    "fluegel": (fluegel, "leises Flügelschwirren"),
    "summen": (summen, "tiefes Summen, schwillt an, bricht ab"),
    "hoehle": (hoehle, "Höhlen-Grundton"),
}


def write(name: str, x: np.ndarray) -> Path:
    x = x / max(np.max(np.abs(x)), 1e-9) * 10 ** (-3 / 20)
    p = OUT / f"{name}.wav"
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    return p


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    lic = OUT / "LICENSE.md"
    text = lic.read_text(encoding="utf-8") if lic.exists() else "# Lizenz der Soundeffekte\n"
    for name, (fn, desc) in SOUNDS.items():
        print(write(name, fn()))
        line = f"{name}.wav: selbst erzeugt (sfx_hoehle.py, Funktion `{name}`, {desc}), keine Fremdrechte"
        if f"{name}.wav:" not in text:
            text = text.rstrip("\n") + "\n" + line + "\n"
    lic.write_text(text, encoding="utf-8")
