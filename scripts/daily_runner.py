"""Tagesläufer: automatic daily production per brand over a model API (docs/daily-runner.md).

  .venv\\Scripts\\python.exe scripts\\daily_runner.py --brands engines,menswear --dry-run      plans + checks, no voice/render
  .venv\\Scripts\\python.exe scripts\\daily_runner.py --brands all                             full chain (needs ANTHROPIC_API_KEY or GEMINI_API_KEY)
  .venv\\Scripts\\python.exe scripts\\daily_runner.py --brands all --list-topics               what would be produced today

Per brand and day: the next N topics of the Konzeptplan (default 2), each as DE and EN plan from the model, validated,
dry run with the mock voice, then voice (Gemini Flash, at most 4 requests per brand and day), render through the
queue, overlap check, export to 05 Produktion, Redaktionsplan row, costs in data/costs/costs.jsonl, marker in the
Konzeptplan. Without an API key the model stage is a mock (the approved example plan) and the run stops after the
dry run. Nothing is published, nothing deleted, nothing booked at Higgsfield.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn.daily.pipeline import DailyRunner, Options, summary_markdown, today_vienna  # noqa: E402
from fn.daily.records import RunLock  # noqa: E402
from fn.daily.settings import RUNS_DIR, brand_settings, configured_brands  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Tagesläufer: daily production per brand over a model API")
    ap.add_argument("--brands", default="all", help="comma-separated brand ids or 'all' (enabled brands of config/daily.yaml)")
    ap.add_argument("--date", default=None, help="production date YYYY-MM-DD (default: today, Europe/Vienna)")
    ap.add_argument("--topics", type=int, default=None, help="topics per brand (default from config, 2)")
    ap.add_argument("--languages", default="de,en")
    ap.add_argument("--dry-run", action="store_true", help="plans and checks only: no voice, no render, no export")
    ap.add_argument("--provider", default=None, help="anthropic | gemini | mock (default: auto by available key)")
    ap.add_argument("--no-export", action="store_true")
    ap.add_argument("--pro-fallback", action="store_true", help="use the Pro voice when the Flash budget of the day is used up")
    ap.add_argument("--max-flash", type=int, default=None, help="Flash TTS requests per brand and day (default 4)")
    ap.add_argument("--no-source-check", action="store_true", help="skip the HTTP reachability check of the sources")
    ap.add_argument("--topic", default=None, help="force one Konzeptplan number (only with one brand)")
    ap.add_argument("--no-mark", action="store_true", help="do not mark topics as done (state file and Konzeptplan)")
    ap.add_argument("--no-plan", action="store_true", help="ignore the month plan (data/calendars/<id>_<month>.plan.json): next free topic as before")
    ap.add_argument("--no-replan", action="store_true", help="do not re-create the month plan before the run (scripts/month_planner.py)")
    ap.add_argument("--replan", action="store_true", help="re-create the month plan before the run even with --dry-run")
    ap.add_argument("--list-topics", action="store_true", help="show the topics that would be produced and exit")
    ap.add_argument("--prototype", action="store_true", help="label the outputs as Tagesläufer-Prototyp (Redaktionsplan, Veröffentlichung.md)")
    ap.add_argument("--effort", default=None, help="claude -p effort (low | medium | high); default from config/daily.yaml (medium)")
    a = ap.parse_args()

    date = a.date or today_vienna()
    brands = configured_brands() if a.brands == "all" else [b.strip() for b in a.brands.split(",") if b.strip()]
    lock = RunLock()
    if not a.list_topics and not lock.acquire():
        print("Ein anderer Lauf des Tagesläufers ist aktiv (data/daily/runner.lock, jünger als 3 Stunden); dieser Lauf startet nicht.")
        return 4
    try:
        return _run(a, date, brands)
    finally:
        if not a.list_topics:
            lock.release()


def replan_before_run(a, date: str, brands: list[str]) -> None:
    """Re-create the month plan of all brands (Hauptsitzung, 04.11.2026) so the run sees the newest Bildaufbauten, sources and recordings.
    A failure never stops the run: it then follows the plan file of the last successful planning."""
    import subprocess
    from fn.daily.monthplan import replan_args
    try:
        args = replan_args(date, a.topics or 2, brands)
        if args is None:
            print("Monatsplan: nichts neu zu erzeugen (den Folgemonat plant die Monatsaufgabe).")
            return
        cmd = [sys.executable, str(Path(__file__).resolve().parent / "month_planner.py"), *args]
        print("Monatsplan vor dem Lauf neu erzeugen: " + " ".join(args))
        import os
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, env=env)
        for line in (r.stdout or "").splitlines():
            if line.startswith(("[", "Hinweis", "Übersicht", "Meldung")) or "Befund" in line:
                print("   " + line)
        if r.returncode != 0:
            print(f"Monatsplan: Planer endete mit Exit {r.returncode}; der Lauf folgt dem letzten Plan. {(r.stderr or '').strip()[-300:]}")
    except Exception as exc:  # noqa: BLE001
        print(f"Monatsplan: Neuerzeugen fehlgeschlagen ({exc!r}); der Lauf folgt dem letzten Plan.")


def _run(a, date: str, brands: list[str]) -> int:
    if (not a.no_replan) and (not a.list_topics) and ((not a.dry_run) or a.replan):
        replan_before_run(a, date, brands)
    results = []
    for bid in brands:
        s = brand_settings(bid)
        if not s.enabled:
            print(f"[{bid}] nicht im Tagesläufer: {s.reason or 'enabled: false'}")
            continue
        opts = Options(date=date, topics=a.topics or int(s.get("topics_per_day", 2)), languages=tuple(x.strip() for x in a.languages.split(",")),
                       dry_run=a.dry_run, provider=a.provider, no_export=a.no_export, pro_fallback=True if a.pro_fallback else None,
                       max_flash=a.max_flash, source_check=False if a.no_source_check else None, topic_nr=a.topic, no_mark=a.no_mark,
                       prototype=a.prototype, effort=a.effort, use_plan=not a.no_plan)
        try:
            runner = DailyRunner(bid, opts)
        except Exception as exc:  # noqa: BLE001
            print(f"[{bid}] Start fehlgeschlagen: {exc!r}")
            continue
        if a.list_topics:
            chosen, skipped = runner.select_topics()
            print(f"[{bid}] {s.name}: {len(chosen)} Thema/Themen für {date}")
            for t in chosen:
                refs = t.extra.get("refs") or []
                print(f"   + {t.describe()} -> Aufbau {t.extra.get('aufbau_final')}" + (f" ({t.extra.get('aufbau_note')})" if t.extra.get("aufbau_note") else "")
                      + f"; Quellen {len(refs)}" + (f"; Kalender {t.calendar_id}" if t.calendar_id else "") + (f"; Aufzeichnung {t.extra.get('recording')}" if t.extra.get("recording") else ""))
            for sk in skipped[:12]:
                print(f"   - {sk}")
            if len(skipped) > 12:
                print(f"   - ... {len(skipped) - 12} weitere übersprungen")
            continue
        results.append(runner.run())
        if runner.rate_limited:
            print("Abbruch: Kontingent von claude -p erreicht; weitere Marken werden nicht gestartet.")
            break
    if results:
        md = summary_markdown(results)
        out = RUNS_DIR / f"{date}_summary.md"
        prev = out.read_text(encoding="utf-8") if out.exists() else ""
        out.write_text(prev + ("\n\n" if prev else "") + md, encoding="utf-8")
        print(md)
        print(f"Zusammenfassung: {out}")
        bad = any(br.errors or any(t.errors or any(lr.errors for lr in t.langs.values()) for t in br.topics) for br in results)
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
