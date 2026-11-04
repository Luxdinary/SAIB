"""Make a 24 s background clip (1080x1920, slow push-in, no sound) from a still of the Revlore library, so a plan can use it as
`assets.hero` / `assets.background` (the asset layer plays <video>, not images), and add its licence line.

    .venv\\Scripts\\python.exe brands\\engines\\zeitlupe\\still_to_clip.py rl_real_piston.jpg [--out rl_t_piston.mp4]

Reads from brands/engines/assets/higgsfield/library/, writes to brands/engines/assets/higgsfield/testvideo/ (own folder
with its own LICENSE.md, not touched by the library script). The licence text of the clip repeats the line of its source.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "higgsfield"
LIB, OUT = ASSETS / "library", ASSETS / "testvideo"


def main() -> int:
    args = sys.argv[1:]
    src = args[0]
    name = args[args.index("--out") + 1] if "--out" in args else "rl_t_" + re.sub(r"^rl_(real_|bg_)?", "", Path(src).stem) + ".mp4"
    lic = LIB / "LICENSE.md"
    line = next((ln for ln in lic.read_text(encoding="utf-8").splitlines() if ln.startswith(src + ":")), "")
    if not line:
        print(f"no licence line for {src} in {lic}")
        return 2
    dst = OUT / name
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", str(LIB / src), "-vf",
                    "scale=1188:2112,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
                    "-t", "24", "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dst)], check=True)
    tos = "Higgsfield Terms of Service 4.4: no restriction on commercial use of Outputs, rights survive cancellation"
    with open(OUT / "LICENSE.md", "a", encoding="utf-8") as f:
        f.write(f"{name}: abgeleitet von {src} (eigene Bearbeitung mit FFmpeg, langsame Fahrt, 24 s, 0 Credits); {tos}; 0 credits. "
                f"Quelle: {line.split(':', 1)[1].strip()[:200]}\n")
    print(dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
