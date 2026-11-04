"""Sort 05 Produktion by brand and month and write the overview (Stefan, 02.11.2026: Business folder sorted per brand).

Moves every flat video folder `05 Produktion\\JJJJ-MM-TT Kurztitel` to `05 Produktion\\<Marke>\\<JJJJ-MM>\\...` (brand from
the folder's manifest/plan), rewrites the paths in `04 Redaktionsplan\\Redaktionsplan.csv` and in the Markdown files of
OneDrive\\Business, and writes `05 Produktion\\Übersicht.md` (one table per brand). Safe to run again at any time:
folders already sorted stay where they are; a folder that is busy (export running) is skipped and reported.
Nothing is deleted.

Run: .venv\\Scripts\\python.exe scripts\\sort_production.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fn.config import BRAND_FOLDERS, mirror_dir  # noqa: E402

FLAT = re.compile(r"^\d{4}-\d{2}-\d{2} .+")
MONTH = re.compile(r"^\d{4}-\d{2}$")


def brand_of(folder: Path) -> str:
    for f in list(folder.glob("03 Schnittprojekt/*.json")) + list(folder.glob("**/manifest.json")):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        b = j.get("brand_id") or (j.get("brand") if isinstance(j.get("brand"), str) else (j.get("brand") or {}).get("id"))
        if b:
            return b
    return ""


def info(folder: Path) -> dict:
    """Date, title, language, format and files of one video folder, for the overview."""
    plan = {}
    for name in ("plan.timed.json", "plan.json"):
        p = folder / "03 Schnittprojekt" / name
        if p.exists():
            try:
                plan = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                pass
            break
    videos = sorted(x.name for x in (folder / "04 Export").glob("*.mp4")) if (folder / "04 Export").exists() else []
    lang = plan.get("language") or ("en" if folder.name.endswith(" EN") else "de")
    fmt = (plan.get("layout") or {}).get("format") or ("Langvideo" if any("16x9" in v for v in videos) else "altes Format")
    return {"date": folder.name[:10], "title": folder.name[11:], "lang": lang.upper(), "format": fmt, "videos": videos}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    base = mirror_dir()
    business = base.parent
    moved, busy, unknown = {}, [], []
    for d in sorted(p for p in base.iterdir() if p.is_dir() and FLAT.match(p.name)):
        bid = brand_of(d)
        if not bid:
            unknown.append(d.name)
            continue
        dst = base / BRAND_FOLDERS.get(bid, bid) / d.name[:7] / d.name
        if dst.exists():
            busy.append(f"{d.name} (Ziel existiert schon)")
            continue
        if a.dry_run:
            print(f"move {d.name} -> {dst.relative_to(base)}")
            moved[d.name] = dst
            continue
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(dst))
            moved[d.name] = dst
        except OSError as exc:
            busy.append(f"{d.name} ({exc.__class__.__name__})")
    # rewrite references: `05 Produktion\<folder>` -> `05 Produktion\<Marke>\<JJJJ-MM>\<folder>`
    if moved and not a.dry_run:
        files = [business / "04 Redaktionsplan" / "Redaktionsplan.csv"]
        files += [p for p in business.rglob("*.md") if base not in p.parents]
        for f in files:
            try:
                s = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            t = s
            for name, dst in moved.items():
                rel = "05 Produktion\\" + str(dst.relative_to(base))
                t = re.sub(r"05 Produktion[\\/]" + re.escape(name) + r"(?=[\\/`\"|;,)\s]|$)", rel.replace("\\", "\\\\"), t)
            if t != s:
                f.write_text(t, encoding="utf-8", newline="")
    write_overview(base, a.dry_run)
    print(f"moved {len(moved)}, busy/skipped {len(busy)}, brand unknown {len(unknown)}")
    for x in busy:
        print("  skipped:", x)
    for x in unknown:
        print("  unknown brand:", x)
    return 0


def write_overview(base: Path, dry: bool) -> None:
    lines = ["# Übersicht 05 Produktion", "",
             "Automatisch erzeugt von `scripts\\sort_production.py` (Code-Ordner). Je Marke alle Videoordner, neueste zuerst.",
             "„altes Format“ = Testvideo oder Woche 1 vor der Neuausrichtung vom 02.11.2026.", ""]
    total = 0
    for brand in sorted(set(BRAND_FOLDERS.values())):
        bdir = base / brand
        rows = []
        if bdir.exists():
            for m in sorted((p for p in bdir.iterdir() if p.is_dir() and MONTH.match(p.name)), reverse=True):
                for v in sorted((p for p in m.iterdir() if p.is_dir()), reverse=True):
                    i = info(v)
                    total += len(i["videos"])
                    rows.append(f"| {i['date']} | {i['title']} | {i['lang']} | {i['format']} | {len(i['videos'])} | "
                                f"`{brand}\\{m.name}\\{v.name}` |")
        lines += [f"## {brand}", ""]
        if rows:
            lines += ["| Datum | Titel | Sprache | Format | Videos | Ordner |", "|---|---|---|---|---|---|", *rows, ""]
        else:
            lines += ["Noch keine Videos.", ""]
    lines.insert(4, f"Videodateien insgesamt: {total}.")
    if not dry:
        (base / "Übersicht.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
