"""Material preparation without any booking: stills used as hero/background clips become 30-s clips with a slow move.

The shared asset layer (fn.render.assets) lays `<video>` clips under the scenes; a still picture from the library is
therefore converted once into `brands/<id>/assets/higgsfield/daily/<name>_d30.mp4` (ffmpeg zoompan, 1080x1920, 30 fps,
H.264) with a licence line copied from the source folder's LICENSE.md ("abgeleitet aus ..."). 0 credits.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from ..config import BRANDS_DIR
from .validate import resolve_media

DERIVED_DIR = "assets/higgsfield/daily"
DERIVED_SECONDS = 30


def _license_line(folder: Path, name: str) -> str:
    f = folder / "LICENSE.md"
    if not f.exists():
        return ""
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith(name + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def _ensure_license(folder: Path, name: str, text: str) -> None:
    f = folder / "LICENSE.md"
    if not f.exists():
        f.write_text("# Abgeleitete Clips des Tagesläufers (fn.daily.media)\n\nEine Zeile je Datei: `<datei>: <Lizenz>`. "
                     "Jeder Clip ist eine Kamerafahrt über ein Standbild der Bibliothek oder des Testvideo-Materials derselben Marke "
                     "(ffmpeg, 0 Credits); die Lizenz ist die des Ausgangsbilds.\n\n", encoding="utf-8")
    existing = f.read_text(encoding="utf-8")
    if any(line.startswith(name + ":") for line in existing.splitlines()):
        return
    with f.open("a", encoding="utf-8") as fh:
        fh.write(f"{name}: {text}\n")


def derive_clip(src: Path, dst: Path, seconds: int = DERIVED_SECONDS) -> None:
    frames = seconds * 30
    vf = ("scale=1296:2304:force_original_aspect_ratio=increase,crop=1296:2304,"
          f"zoompan=z='min(zoom+0.00025,1.18)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", str(src), "-vf", vf,
                    "-t", str(seconds), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-an", "-movflags", "+faststart", str(dst)],
                   check=True, capture_output=True, timeout=600)


def prepare_assets(plan: dict, brand_id: str, extra_bases: list[Path] | None = None) -> list[str]:
    """Replace still images in plan.assets.hero / .background by derived clips (absolute paths). Returns notes."""
    notes: list[str] = []
    assets = plan.get("assets") or {}
    if not assets:
        return notes
    out_dir = BRANDS_DIR / brand_id / DERIVED_DIR
    for role in ("hero", "background"):
        entries = assets.get(role) or {}
        for key, name in list(entries.items()):
            if not isinstance(name, str):
                continue
            src = resolve_media(name, brand_id, plan, extra_bases)
            if src is None:
                notes.append(f"assets.{role}.{key}: {name} nicht gefunden")
                continue
            if name.lower().endswith((".mp4", ".webm", ".mov")):
                entries[key] = str(src)                     # absolute: independent of assets.folder
                continue
            dst = out_dir / f"{src.stem}_d{DERIVED_SECONDS}.mp4"
            if not dst.exists():
                derive_clip(src, dst)
                notes.append(f"assets.{role}.{key}: {src.name} -> {dst.name} (Kamerafahrt, {DERIVED_SECONDS} s, 0 Credits)")
            lic = _license_line(src.parent, src.name) or "Lizenzzeile des Ausgangsbilds fehlt"
            _ensure_license(out_dir, dst.name, f"abgeleitet aus {src.parent.name}/{src.name} (Kamerafahrt im Tagesläufer, 0 Credits); {lic}")
            entries[key] = str(dst)
    if assets.get("transition") and not str(assets["transition"]).lower().endswith((".mp4", ".webm", ".mov")):
        notes.append("assets.transition ist kein Clip; unverändert gelassen")
    return notes
