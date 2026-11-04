"""Planning folders for the Scutoria long videos that are not produced yet: readable script, scene plan, thumbnails.

  .venv\\Scripts\\python.exe brands\\ai_security\\longform\\export_planning.py 03 05 06 07 08 09 10

Writes OneDrive\\Business\\02 Marke\\Scutoria\\YouTube-Planung\\<NN Kurztitel>\\ (Skript DE.md, Szenenplan DE.md,
Thumbnails\\). Lengths come from the last dry run (storage\\longform\\<video_id>-dry\\report.json) when present.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2] / "src"))

from fn.config import STORAGE_DIR, mirror_dir  # noqa: E402
from longform.export_long import script_md  # noqa: E402

OUT = mirror_dir().parent / "02 Marke" / "Scutoria" / "YouTube-Planung"
SHORT = {"03": "Rundgang Toolkits", "05": "Artikel 4 Einweisung", "06": "MFA Sicherung Updates", "07": "Artikel 50 Kennzeichnung",
         "08": "Erste Stunde Vorfall", "09": "Sieben Fragen Freigabe", "10": "NIS2 betroffen", "01": "KI-Regeln",
         "02": "Sicherheitsfragebogen", "04": "Was nie hineingehört"}


def scene_plan(plan: dict, length: str) -> str:
    out = [f"# Szenenplan · {plan['title']}", "", f"Länge laut Trockenlauf: {length}. Szenentypen siehe `longform\\blocks.py`.", "",
           "| Szene | Typ | Hintergrund | Bild (Kurzform) | neu |", "|---|---|---|---|---|"]
    for ch in plan["chapters"]:
        out.append(f"| **{ch.get('num') or '0'} {ch['title']}** | | | | |")
        for k, sc in enumerate(ch["scenes"]):
            d = sc.get("data", {})
            what = d.get("headline") or d.get("text") or d.get("question") or d.get("time", "") + " " + str(d.get("place", "")) or d.get("word", "")
            if sc["type"] == "close":
                what = d.get("rule", "")
            out.append(f"| {ch['id']}s{k} | {sc['type']} | {sc.get('bg', '').replace('yt/', '')} | {str(what).replace('*', '').replace('|', '/')[:90]} | {'ja' if sc.get('new') else ''} |")
    out += ["", "## Reels", ""] + [f"- {r['id']}: {r['title']} ({', '.join(r['scenes'])})" for r in plan.get("reels", [])]
    return "\n".join(out) + "\n"


def main() -> int:
    for num in sys.argv[1:]:
        plan_file = next((HERE / "plans").glob(f"{num}-*.de.json"))
        plan = json.loads(plan_file.read_text(encoding="utf-8"))
        rep = STORAGE_DIR / "longform" / f"{plan['video_id']}-dry" / "report.json"
        length = "nicht ermittelt"
        if rep.exists():
            secs = sum(c.get("seconds", 0) for c in json.loads(rep.read_text(encoding="utf-8")).get("chapters", []))
            length = f"{int(secs // 60)}:{int(secs % 60):02d} min (Schätzung mit Sprechtempo, ohne Vertonung)"
        folder = OUT / f"{num} {SHORT.get(num, plan['slug'])}"
        (folder / "Thumbnails").mkdir(parents=True, exist_ok=True)
        (folder / "Skript DE.md").write_text(script_md(plan), encoding="utf-8")
        (folder / "Szenenplan DE.md").write_text(scene_plan(plan, length), encoding="utf-8")
        for th in sorted((STORAGE_DIR / "longform" / "thumbs").glob(f"{num}_*.png")):
            shutil.copy2(th, folder / "Thumbnails" / th.name)
        print(folder, length)
    return 0


if __name__ == "__main__":
    sys.exit(main())
