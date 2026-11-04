"""Add a new render version to an existing production folder without touching the earlier export (Scutoria, 03.11.2026).

scripts/export_production_folder.py refuses to overwrite the video and rewrites Skript.md and Veröffentlichung.md;
for a re-render with the same text (e.g. the quieter sound layer) this copies the files with the version in the name
and adds a short section to Veröffentlichung.md. Nothing is deleted or replaced.
    .venv/Scripts/python.exe brands/ai_security/export_version.py <video_id> <version> "<production folder>" "<note>"
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from export_production_folder import write_srt  # noqa: E402
from fn.config import STORAGE_DIR  # noqa: E402


def main() -> int:
    vid, version, folder, note = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
    render = STORAGE_DIR / "direction" / f"{vid}-{version}"
    man = json.loads((render / "manifest.json").read_text(encoding="utf-8"))
    if (man.get("tts") or {}).get("provider") != "gemini":
        print("only Google/Gemini voices may be exported (Stefan, 30.10.2026)")
        return 4
    stem = folder.name                                      # "<date> <short>"
    video = folder / "04 Export" / f"{stem} – 9x16 {version}.mp4"
    if video.exists():
        print(f"{video} exists")
        return 3
    shutil.copy2(render / "video.mp4", video)
    shutil.copy2(render / "cover.jpg", folder / "05 Thumbnail und Cover" / f"{stem} – Cover {version}.jpg")
    write_srt(json.loads((render / "captions.json").read_text(encoding="utf-8")), folder / "06 Untertitel" / f"{stem} {version}.srt")
    proj = folder / "03 Schnittprojekt" / version
    proj.mkdir(parents=True, exist_ok=True)
    for n in ("plan.timed.json", "manifest.json", "report.json", "post.json", "captions.json"):
        if (render / n).exists():
            shutil.copy2(render / n, proj / n)
    snd = man.get("sound", {}).get("measured", {})
    tts = man.get("tts", {})
    pub = folder / "Veröffentlichung.md"
    with pub.open("a", encoding="utf-8") as f:
        f.write(f"\n## Fassung {version}\n\n- Datei: `04 Export\\{video.name}` (die frühere Datei bleibt daneben liegen)\n"
                f"- Dauer {man.get('render', {}).get('duration', '?')} s; Stimme (Modell): Google Gemini `{tts.get('model', '?')}`, "
                f"Sprecher {tts.get('voice', '?')}\n- Ton: Geräusch-Stem Spitze {snd.get('sfx_peak_dbfs')} dBFS, Mischung "
                f"{snd.get('mix_lufs')} LUFS, Bett {snd.get('music_below_voice_db')} dB unter der Stimme\n- {note}\n")
    print(video)
    return 0


if __name__ == "__main__":
    sys.exit(main())
