"""Costs per video of the daily runner, from data/costs/costs.jsonl (model tokens, voice, render time).

  .venv\\Scripts\\python.exe scripts\\daily_costs.py                 # rendered videos of the daily runner (ids with -d<n>- and the prototype ids)
  .venv\\Scripts\\python.exe scripts\\daily_costs.py --date 2026-11-06 --brand menswear

One line per video (`<video_id>-<Fassung>`), then a sum per brand. Dry-run entries (mock voice, `...dry`, `-excerpt`) are left out.
Model tokens are subscription tokens (claude -p): there is no price per token ("Abo, kein Einzelpreis").
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COSTS = ROOT / "data" / "costs" / "costs.jsonl"
ID_RE = re.compile(r"^(?P<brand>[a-z_]+)-(?P<date>\d{8})-(?:d)?(?P<n>\d+)-(?P<lang>de|en)-(?P<ver>D\d+)$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (date in the video id)")
    ap.add_argument("--brand", default=None)
    ap.add_argument("--plans", action="store_true", help="also ids that only have plan (model) entries, no render")
    a = ap.parse_args()
    rows: dict[str, dict] = defaultdict(lambda: {"llm_calls": 0, "tok_in": 0, "tok_out": 0, "tok_cache": 0, "tts_usd": 0.0, "tts_n": 0,
                                                 "render_s": 0.0, "usd": 0.0})
    for line in COSTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        m = ID_RE.match(e.get("video_id", ""))
        if not m:
            continue
        if a.date and m["date"] != a.date.replace("-", ""):
            continue
        if a.brand and m["brand"] != a.brand:
            continue
        r = rows[e["video_id"]]
        r["usd"] += float(e.get("usd", 0))
        kind = e.get("kind")
        if kind == "llm":
            r["llm_calls"] += 1
            mm = re.search(r"in=(\d+) out=(\d+)(?: cache=(\d+))?", e.get("note", ""))
            if mm:
                r["tok_in"] += int(mm[1])
                r["tok_out"] += int(mm[2])
                r["tok_cache"] += int(mm[3] or 0)
        elif kind == "tts" and e.get("provider") == "gemini":
            r["tts_n"] += 1
            r["tts_usd"] += float(e.get("usd", 0))
        elif kind == "render":
            r["render_s"] += float(e.get("units", 0))
    if not a.plans:
        rows = {k: v for k, v in rows.items() if v["render_s"] > 0}
    if not rows:
        print("keine Einträge")
        return 0
    print(f"{'video':44} {'Modell-Aufr.':>12} {'Token ein':>9} {'Token aus':>9} {'Token Cache':>11} {'Stimme USD':>10} {'Render s':>8}")
    per_brand: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    for vid in sorted(rows):
        r = rows[vid]
        m = ID_RE.match(vid)
        print(f"{vid:44} {r['llm_calls']:12d} {r['tok_in']:9d} {r['tok_out']:9d} {r['tok_cache']:11d} {r['tts_usd']:10.4f} {r['render_s']:8.0f}")
        for k in ("llm_calls", "tok_in", "tok_out", "tok_cache", "tts_usd", "render_s"):
            per_brand[m["brand"]][k] += r[k]
        per_brand[m["brand"]]["videos"] += 1
    print()
    for b, s in sorted(per_brand.items()):
        print(f"{b:20} {int(s['videos'])} Videos, {int(s['llm_calls'])} Modellaufrufe, {int(s['tok_out'])} Ausgabe-Token, "
              f"Stimme {s['tts_usd']:.3f} USD, Render {s['render_s']:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
