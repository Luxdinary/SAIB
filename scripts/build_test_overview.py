"""Build an overview page of all produced test videos and mirror it to OneDrive\\Business\\05 Produktion\\_Test.

Run:  .venv\\Scripts\\python.exe scripts\\build_test_overview.py
"""
from __future__ import annotations

import html
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn import queue  # noqa: E402
from fn.config import STORAGE_DIR, mirror_dir  # noqa: E402
from fn.state import StateDB  # noqa: E402


def main() -> int:
    db = StateDB()
    rows = []
    for stage in queue.STAGES:
        for vid in queue.list_stage(stage):
            folder = STORAGE_DIR / stage / vid
            man = json.loads((folder / "manifest.json").read_text(encoding="utf-8")) if (folder / "manifest.json").exists() else {}
            rep = json.loads((folder / "report.json").read_text(encoding="utf-8")) if (folder / "report.json").exists() else {}
            v = db.get(vid) or {}
            rows.append({
                "video_id": vid, "stage": stage, "state": v.get("state", "?"), "brand": man.get("brand_name", ""),
                "language": man.get("language", ""), "title": man.get("title", ""),
                "duration": man.get("render", {}).get("duration"), "render_seconds": man.get("render", {}).get("seconds"),
                "tts": man.get("tts", {}).get("provider"), "passed": rep.get("passed"), "needs_review": rep.get("needs_review"),
                "not_ok": [f["id"] for f in rep.get("findings", []) if not f["ok"]],
                "cost_usd": man.get("cost", {}).get("usd_variable"),
                "has_video": (folder / "video.mp4").exists(),
            })
    rows.sort(key=lambda r: r["video_id"])
    cards = []
    for r in rows:
        video = f'<video controls preload="metadata" poster="{r["video_id"]}/cover.jpg" src="{r["video_id"]}/video.mp4"></video>' if r["has_video"] else "<p>kein Video</p>"
        cards.append(f"""
<article class="card"><header><h2>{html.escape(r['brand'])} · {r['language'].upper()}</h2><span class="id">{r['video_id']}</span></header>
<p class="t">{html.escape(r['title'])}</p>{video}
<footer><span>Zustand <b>{r['state']}</b> · Prüfung {'bestanden' if r['passed'] else 'nicht bestanden'}{' · Review: ' + ', '.join(r['not_ok']) if r['not_ok'] else ''}</span>
<span>{(r['duration'] or 0):.1f} s · Render {(r['render_seconds'] or 0):.0f} s · Stimme {r['tts']} · variable Kosten {r['cost_usd']} USD</span></footer></article>""")
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Testvideos Phase 1</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{margin:0;background:#0d0f14;color:#e8eaf0;font-family:Inter,Segoe UI,sans-serif;padding:24px}}h1{{font-size:22px;margin:0 0 6px}}p.sub{{color:#9aa3b2;font-size:14px;margin:0 0 20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}.card{{background:#151923;border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:8px}}
h2{{font-size:17px;margin:0}}.id{{color:#9aa3b2;font-size:12px}}.t{{margin:0;font-size:14px}}video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:12px}}footer{{display:flex;flex-direction:column;gap:4px;color:#9aa3b2;font-size:12px}}</style></head>
<body><h1>Phase 1 · Testvideos (65–90 s, Mock-Stimme, nur lokal)</h1><p class="sub">Stand {datetime.now().strftime('%Y-%m-%d %H:%M')} · {len(rows)} Videos · nichts veröffentlicht</p>
<div class="grid">{''.join(cards)}</div></body></html>"""
    target = mirror_dir() / "_Test"
    target.mkdir(parents=True, exist_ok=True)
    (STORAGE_DIR / "test_overview.html").write_text(page, encoding="utf-8")
    shutil.copy2(STORAGE_DIR / "test_overview.html", target / "index.html")
    (target / "results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} videos -> {target / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
