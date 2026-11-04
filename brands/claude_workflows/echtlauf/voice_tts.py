"""Promptwerk: record the Gemini voice for a plan with TTS-only spellings (Aussprache), then render with --reuse-voice.

The shared renderer sends the plan's spoken text unchanged to the voice and aligns the captions to the same text. A
German voice said "Cloud" for "Claude" (Whisper, 03.11.2026). This script replaces words only in the text that goes
to the voice (`--say Claude=Klohd`), keeps the plan text for captions and alignment, and writes the paid recording
like render_direction.py does: storage/direction/voice_<video_id>_<version>_gemini.wav plus a sidecar .json whose
`spoken_text` is the plan text (so --reuse-voice accepts it) and whose `tts_text` and `say` record what was spoken.
One run = one Gemini request; on any error (429 included) it stops, no retry loop.

Usage (repository root):
    .venv\\Scripts\\python.exe brands\\claude_workflows\\echtlauf\\voice_tts.py <plan.json> --version T5 --say Claude=Klohd [--voice Kore]
    .venv\\Scripts\\python.exe scripts\\render_queue.py claude_workflows -- scripts\\render_direction.py <plan.json> --version T5 \\
        --tts gemini --reuse-voice storage\\direction\\voice_<video_id>_T5_gemini.wav
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from fn.brands import load_brand  # noqa: E402
from fn.config import STORAGE_DIR  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.direction import story  # noqa: E402
from fn.tts import get_provider  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", required=True)
    ap.add_argument("--say", action="append", default=[], help="Word=Spelling, replaced as a whole word in the TTS text only")
    ap.add_argument("--voice", default=None, help="Gemini voice name (default: brand voice for the plan language)")
    a = ap.parse_args()
    plan = story.load_plan(Path(a.plan))
    brand = load_brand(plan.brand_id)
    lang = plan.language
    spoken = plan.spoken_text
    tts_text = spoken
    for pair in a.say:
        word, _, say = pair.partition("=")
        tts_text = re.sub(rf"\b{re.escape(word)}\b", say, tts_text)
    if len(tts_text.split()) != len(spoken.split()):
        print("a replacement changes the word count; alignment needs one word for one word")
        return 2
    cfg = brand.audio.get("tts", {})
    style = (cfg.get("style_instruction") or {}).get(lang, "")
    voice = a.voice or brand.voice(lang)
    video_id = f"{plan.video_id}-{a.version}"
    out = STORAGE_DIR / "direction" / f"voice_{plan.video_id}_{a.version}_gemini.wav"
    tmp = out.with_name(out.stem + "_raw.wav")
    tts = get_provider("gemini").synthesize(tts_text, lang, voice, tmp, style=style, rate=float(cfg.get("speaking_rate", 1.0)))
    CostLogger().log_tts(video_id, tts.provider, tts.input_chars, tts.output_tokens, tts.seconds)
    shutil.move(str(tts.path), out)
    info = {"provider": tts.provider, "model": tts.model, "voice": tts.voice, "seconds": tts.seconds, "usd": tts.usd,
            "input_chars": tts.input_chars, "output_tokens": tts.output_tokens, "notes": tts.notes, "video_id": video_id,
            "spoken_text": spoken, "tts_text": tts_text, "say": a.say,
            "made_by": "brands/claude_workflows/echtlauf/voice_tts.py (TTS-only spellings, captions keep the plan text)"}
    out.with_suffix(".json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"voice: {tts.provider} {tts.model} {tts.voice} {tts.seconds:.1f} s, {tts.usd:.4f} USD -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
