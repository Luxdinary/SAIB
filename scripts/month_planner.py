"""Month planner: plans the topics of a month per brand ahead, 2 per day in German and English (docs/daily-runner.md, section 6).

  .venv/Scripts/python.exe scripts/month_planner.py --month 2026-11 --from 2026-11-05 --assume 2026-11-04:1
  .venv/Scripts/python.exe scripts/month_planner.py                       next month, 1st to last day (what the monthly task does)
  .venv/Scripts/python.exe scripts/month_planner.py --dry-run             numbers only, writes nothing
  .venv/Scripts/python.exe scripts/month_planner.py --propose             also topic proposals through claude -p for brands with gaps

The plan simulates the topic choice of the daily runner (Konzeptplan order, built Bildaufbauten, verified sources, Bildaufbau change)
and writes per brand `04 Redaktionsplan/Monatsplan <Marke> <YYYY-MM>.md` and `data/calendars/<id>_<YYYY-MM>.plan.json`, plus the overview
`Monatsplan <YYYY-MM> Übersicht.md` and a report in data/daily/. No model call without --propose; proposals are only ideas
("Vorschlag, Quelle prüfen"), never part of the plan. Nothing is published, deleted or booked; older versions of a file go to an archive folder.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fn.config import DATA_DIR, brands_config  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.daily import monthplan as mp  # noqa: E402
from fn.daily import proposals as prop  # noqa: E402
from fn.daily.pipeline import today_vienna  # noqa: E402
from fn.daily import settings as st  # noqa: E402
from fn.daily.settings import brand_settings, configured_brands, daily_config  # noqa: E402

MANUAL_BEGIN, MANUAL_END = "<!-- MANUELL:BEGIN -->", "<!-- MANUELL:END -->"
MOCK_ANSWER = ('{"vorschlaege": [{"titel": "Beispielthema der Attrappe", "reihe": "Beispiel", "hook": "Ein Satz.", "bildaufbau": "A", '
               '"risiko": "niedrig", "quellen": [{"titel": "Beispiel", "institution": "Beispiel", "url": "", "suchhinweis": "Attrappe"}], "hinweis": "Attrappe"}]}')


def next_month(today: date) -> str:
    y, m = (today.year + (today.month == 12), today.month % 12 + 1)
    return f"{y}-{m:02d}"


def month_bounds(month: str) -> tuple[date, date]:
    y, m = (int(x) for x in month.split("-"))
    first = date(y, m, 1)
    last = date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)
    return first, last


def manual_block(path: Path) -> str:
    """The hand-written part of an existing overview (between the markers), so a regeneration keeps it."""
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if MANUAL_BEGIN in t and MANUAL_END in t:
            return t.split(MANUAL_BEGIN, 1)[1].split(MANUAL_END, 1)[0].strip("\n")
    return ("## Tintora und Scutoria YouTube\n\nVon Hand fortschreiben (Tintora-Sitzung, Scutoria-YouTube-Sitzung): Reels und Langvideos mit Datum und Slot, "
            "Abweichungen vom Takt mit Grund.")


def write_archived(path: Path, text: str, archive_dir: Path) -> bool:
    """Write `text`; an existing different file is copied to `archive_dir` first (nothing is deleted). True when the file changed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_text(encoding="utf-8")
        def strip(s: str) -> str:                                  # the time stamp line alone is no reason for a new version
            return re.sub(r"^Stand [^\n]*\n", "", s, flags=re.M)
        if old == text or strip(old) == strip(text):
            return False
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y%m%d-%H%M%S")
        (archive_dir / f"{path.stem} ({stamp}){path.suffix}").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Month planner: topics per brand and day, ahead for a month")
    ap.add_argument("--month", default=None, help="YYYY-MM (default: the month after today, Europe/Vienna)")
    ap.add_argument("--from", dest="start", default=None, help="first day (default: first of the month)")
    ap.add_argument("--to", dest="end", default=None, help="last day (default: last of the month)")
    ap.add_argument("--assume", action="append", default=[], metavar="DAY[:N]",
                    help="topics taken for a day before the plan because they will be produced but are not in the state yet (e.g. 2026-11-04:1)")
    ap.add_argument("--brands", default="all", help="comma-separated brand ids or 'all' (enabled brands of config/daily.yaml)")
    ap.add_argument("--per-day", type=int, default=None, help="topics per day (default: topics_per_day of config/daily.yaml, 2)")
    ap.add_argument("--dry-run", action="store_true", help="print the numbers, write nothing")
    ap.add_argument("--propose", action="store_true", help="topic proposals through claude -p for brands with open slots (ideas only)")
    ap.add_argument("--max-proposals", type=int, default=20, help="proposals per brand (default 20)")
    ap.add_argument("--provider", default=None, help="claude_cli (default) | mock")
    a = ap.parse_args()

    today = date.fromisoformat(today_vienna())
    month = a.month or next_month(today)
    first, last = month_bounds(month)
    start = date.fromisoformat(a.start) if a.start else first
    end = date.fromisoformat(a.end) if a.end else last
    assume = []
    for x in a.assume:
        d, _, n = x.partition(":")
        assume.append((date.fromisoformat(d), int(n or 1)))
    brands = configured_brands() if a.brands == "all" else [b.strip() for b in a.brands.split(",") if b.strip()]
    slots = mp.language_slots()
    risk = {b["id"]: b.get("risk_default", "low") for b in brands_config()["brands"]}
    created = datetime.now().strftime("%d.%m.%Y %H:%M")
    cfg_all = daily_config()
    plans: list[mp.BrandPlan] = []
    for bid in brands:
        s = brand_settings(bid)
        if not s.enabled:
            print(f"[{bid}] nicht im Tagesläufer: {s.reason or 'enabled: false'}")
            continue
        per_day = a.per_day or int(s.get("topics_per_day", 2))
        with mp.cached_sources():
            p = mp.plan_brand(bid, start, end, per_day, assume, log=print, after=today)
            rows = mp.calendar_rows(p, slots, risk.get(bid, "low"))
        plans.append(p)
        print(f"[{bid}] {p.brand_name}: eingeplant {p.planned} von {p.slots} Plätzen, frei {p.missing}, Quelle fehlt {len(p.no_source)}, "
              f"braucht Modell/Aufbau {len(p.needs_model)}, Konzeptplan {p.total_candidates} (mit Quelle {p.with_source})")
        if a.dry_run:
            continue
        path = mp.plan_file(bid, month)
        if path.exists() and start > first:             # re-planning from a later day keeps the days before it as they are
            try:
                rows = [r for r in json.loads(path.read_text(encoding="utf-8")) if str(r.get("publish_at", ""))[:10] < start.isoformat()] + rows
            except (OSError, json.JSONDecodeError):
                pass
        text_json = json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
        changed = write_archived(path, text_json, DATA_DIR / "calendars" / "archiv")
        problems = mp.check_calendar(path)
        md_path = mp.PLAN_DIR / f"Monatsplan {p.brand_name} {month}.md"
        write_archived(md_path, mp.brand_markdown(p, slots, month, created), mp.PLAN_DIR / "Frühere Fassungen")
        print(f"      {path.name} {'geschrieben' if changed else 'unverändert'}; Kalenderprüfung: {len(problems)} Befund(e)"
              + (f" ({'; '.join(problems[:2])})" if problems else "") + f"; {md_path.name}")
    if not plans:
        return 0
    warnings = list(st.AUFBAUTEN_WARNINGS)               # a brand's aufbauten.yaml that did not parse: planned with its last valid state
    for w in warnings:
        print(f"Hinweis: {w}")
    proposal_files: list[str] = []
    if a.propose and not a.dry_run:
        from fn.daily.llm import MockProvider, make_provider
        from fn.daily.pipeline import DailyRunner, Options
        from fn.daily.topics import ordered_candidates
        costs = CostLogger()
        for p in plans:
            n = min(p.missing, a.max_proposals)
            if n <= 0:
                continue
            s = brand_settings(p.brand_id)
            llm_cfg = dict(s.llm)
            llm_cfg["cli_effort"] = "low"
            provider = make_provider(llm_cfg, a.provider)
            if isinstance(provider, MockProvider):
                provider.queue.append(MOCK_ANSWER)
            runner = DailyRunner(p.brand_id, Options(date=start.isoformat(), provider="mock", dry_run=True, use_plan=False), log=lambda m: None)
            cands = ordered_candidates(runner.kp, runner.s.topic_source)
            titles = [t.title for t in cands]
            sample = [f"{t.nr} | {t.title} | {t.reihe} | {t.hook_idea} | {t.source_state} | {t.risk}" for t in runner.kp.proposals[:6]]
            series = sorted({t.reihe for t in cands if t.reihe})
            try:
                items = prop.propose(p.brand_id, n, titles, sample, series, provider, costs, llm_cfg, month, check=not isinstance(provider, MockProvider))
            except Exception as exc:  # noqa: BLE001
                print(f"[{p.brand_id}] Vorschläge fehlgeschlagen: {exc!r}")
                continue
            out = mp.PLAN_DIR / f"Themenvorschläge {p.brand_name} {month}.md"
            write_archived(out, prop.proposals_markdown(p.brand_name, p.brand_id, month, items, created), mp.PLAN_DIR / "Frühere Fassungen")
            proposal_files.append(f"{out.name} ({len(items)} Vorschläge)")
            print(f"[{p.brand_id}] {len(items)} Vorschläge -> {out.name}")
    if a.dry_run:
        return 0
    if not {p.brand_id for p in plans} >= set(configured_brands()):
        print("Übersicht und Meldung nicht neu geschrieben: nicht alle Marken geplant (sie zeigen sonst nur diese Marken).")
        return 0
    ov_path = mp.PLAN_DIR / f"Monatsplan {month} Übersicht.md"
    manual = manual_block(ov_path)
    body = mp.overview_markdown(plans, slots, month, created, MANUAL_BEGIN + "\n" + manual + "\n" + MANUAL_END, warnings=warnings)
    write_archived(ov_path, body, mp.PLAN_DIR / "Frühere Fassungen")
    # report for the Hauptsitzung: file in data/daily and, if configured, in the shared notes folder of the session group
    report = [f"# Monatsplan {month}: Meldung ({created})", "",
              f"Plan {start:%d.%m.} bis {end:%d.%m.%Y}, Übersicht: `{ov_path}`.", "",
              "| Marke | eingeplant | Plätze | frei | Quelle fehlt | braucht Modell/Aufbau |", "|---|---|---|---|---|---|"]
    report += [f"| {p.brand_name} | {p.planned} | {p.slots} | {p.missing} | {len(p.no_source)} | {len(p.needs_model)} |" for p in plans]
    if proposal_files:
        report += ["", "Themenvorschläge (Vorschlag, Quelle prüfen, nicht eingeplant): " + "; ".join(proposal_files)]
    if warnings:
        report += ["", "Hinweise: " + " | ".join(warnings)]
    text = "\n".join(report) + "\n"
    out = DATA_DIR / "daily" / f"month_plan_{month}_report.md"
    out.write_text(text, encoding="utf-8")
    rd = (cfg_all.get("month_plan") or {}).get("report_dir")
    if rd and Path(rd).exists():
        (Path(rd) / f"{today:%Y-%m-%d} Monatsplan {month} Meldung.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"Übersicht: {ov_path}\nMeldung: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
