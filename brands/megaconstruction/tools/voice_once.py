"""One Gemini TTS request for a plan, with a chosen speaker (Neustart 2026-11: the English test video keeps the speaker of
the German one). Writes storage/direction/voice_<video_id>_<version>_gemini.wav plus the .json sidecar exactly like
scripts/render_direction.py, so the render reuses it with --reuse-voice. Never repeats a request: an existing file or
an error (429 included) stops the script.

Run:  .venv\\Scripts\\python.exe brands\\megaconstruction\\tools\\voice_once.py data\\direction\\<plan>.json --version T1 --voice Charon
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from fn.brands import load_brand  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.direction import story  # noqa: E402
from fn.tts import get_provider  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", required=True)
    ap.add_argument("--voice", required=True)
    a = ap.parse_args()
    plan = story.load_plan(Path(a.plan))
    brand = load_brand(plan.brand_id)
    lang = plan.language
    out = ROOT / "storage" / "direction" / f"voice_{plan.video_id}_{a.version}_gemini.wav"
    if out.exists():
        print(f"{out.name} exists; no new request")
        return 1
    spoken = plan.spoken_text
    cfg = brand.audio.get("tts", {})
    style = (cfg.get("style_instruction") or {}).get(lang, "")
    tts = get_provider("gemini").synthesize(spoken, lang, a.voice, out, style=style, rate=float(cfg.get("speaking_rate", 1.0)))
    CostLogger().log_tts(f"{plan.video_id}-{a.version}", tts.provider, tts.input_chars, tts.output_tokens, tts.seconds)
    info = {"provider": tts.provider, "model": tts.model, "voice": tts.voice, "seconds": tts.seconds, "usd": tts.usd,
            "input_chars": tts.input_chars, "output_tokens": tts.output_tokens, "notes": tts.notes,
            "video_id": f"{plan.video_id}-{a.version}", "spoken_text": spoken}
    out.with_suffix(".json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"voice: {tts.model} {tts.voice} {tts.seconds:.1f} s, {tts.output_tokens} output tokens -> {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
