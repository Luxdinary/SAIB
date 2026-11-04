"""Month plan: which topics a brand produces on which day, planned ahead without any model call.

The plan simulates `DailyRunner.select_topics` day after day on a copy of the state, so it follows exactly the rules of the daily
runner: Konzeptplan order, only built Bildaufbauten (brands/<id>/aufbauten.yaml), only topics with a verified source, Bildaufbau
change, brand limits (Revlore Motor topics, Promptwerk recordings). Outputs per brand and month:

- `data/calendars/<id>_<YYYY-MM>.plan.json`: rows in the schema of `fn.calendar.TopicRow` (so `fn.cli calendar check` reads it) plus
  `nr`, `slot_index`, `slot`, `aufbau`, `aufbau_planned`, `aufbau_note`, `calendar_ref`, `plan_status`, `reihe`, `plattformen`;
  the existing `<id>_2026-11.json` calendars stay untouched (brand tools read them and they hold the verified sources),
- `04 Redaktionsplan/Monatsplan <Marke> <YYYY-MM>.md`: the table for people,
- `04 Redaktionsplan/Monatsplan <YYYY-MM> Übersicht.md`: numbers per brand, rules, assumptions, gaps.

The daily runner reads the plan file for its day (`plan_for_day`): the planned topics come first, everything else follows in the old order,
so a planned topic that fails a check falls back to the next free one. Without a plan file nothing changes.
"""
from __future__ import annotations

import copy
import json
import re
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from functools import lru_cache
from pathlib import Path

from ..calendar import FORMATS, VIENNA, TopicRow, validate
from ..config import DATA_DIR, brands_config
from .settings import BUSINESS_DIR, brand_settings, configured_brands
from .topics import Topic

WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
PLATFORMS = ["TikTok", "Instagram Reels", "YouTube Shorts"]
PLAN_DIR = BUSINESS_DIR / "04 Redaktionsplan"


# ------------------------------------------------------------------ files and slots
def plan_file(brand_id: str, month: str) -> Path:
    return DATA_DIR / "calendars" / f"{brand_id}_{month}.plan.json"


def language_slots() -> dict[str, list[str]]:
    """Slots per language (Europe/Vienna) from config/brands.yaml defaults.slots_by_language."""
    d = brands_config()["defaults"]
    by = d.get("slots_by_language") or {}
    return {lang: list(by.get(lang) or d.get("slots") or []) for lang in d.get("languages", ["de", "en"])}


def plan_for_day(brand_id: str, iso_date: str) -> list[dict]:
    """Planned German rows of one day in slot order ([] without a plan file or entry). Never raises: planning is an optional layer."""
    try:
        path = plan_file(brand_id, iso_date[:7])
        if not path.exists():
            return []
        rows = json.loads(path.read_text(encoding="utf-8"))
        out = [r for r in rows if isinstance(r, dict) and r.get("language") == "de" and r.get("plan_status") == "geplant"
               and str(r.get("publish_at", ""))[:10] == iso_date]
        out.sort(key=lambda r: int(r.get("slot_index") or 0))
        return out
    except Exception:  # noqa: BLE001
        return []


def replan_args(date_iso: str, topics: int, brands: list[str]) -> list[str] | None:
    """Arguments for scripts/month_planner.py before a daily run on `date_iso` (None: nothing to re-plan). The plan covers the run day
    -> plan again from that day (the runner then reads fresh rows for today). The plan does not cover it (04.11.: the run takes
    `topics` topics the old way) -> plan from the next day and assume this run's topics. A next month is the monthly task's business."""
    d = date.fromisoformat(date_iso)
    names = configured_brands() if (not brands or brands == ["all"]) else brands
    covered = any(plan_for_day(b, date_iso) for b in names)
    start, assume = (d, []) if covered else (d + timedelta(days=1), [f"{date_iso}:{topics}"])
    if start.strftime("%Y-%m") != d.strftime("%Y-%m"):
        return None
    args = ["--month", d.strftime("%Y-%m"), "--from", start.isoformat(), "--brands", ",".join(names)]
    for a in assume:
        args += ["--assume", a]
    return args


# ------------------------------------------------------------------ simulation
@dataclass
class PlannedTopic:
    slot_index: int
    nr: str | None
    title: str
    reihe: str
    aufbau: str | None
    aufbau_planned: str | None
    aufbau_note: str
    refs: list = field(default_factory=list)
    recording: str | None = None
    calendar_id: str | None = None
    risk: str = ""
    hook_idea: str = ""
    cal: dict | None = None

    @property
    def source_ok(self) -> bool:
        return bool(self.refs) or bool(self.recording)


@dataclass
class DayPlan:
    day: date
    topics: list[PlannedTopic] = field(default_factory=list)


@dataclass
class BrandPlan:
    brand_id: str
    brand_name: str
    start: date
    end: date
    per_day: int
    days: list[DayPlan] = field(default_factory=list)
    assumed: list[tuple[date, str]] = field(default_factory=list)      # topics taken for the days before the plan (not yet produced)
    total_candidates: int = 0
    with_source: int = 0
    done_before: int = 0
    from_earlier_plans: int = 0                                        # topics of the previous plan file taken for the days before this plan
    no_source: list[str] = field(default_factory=list)
    needs_model: list[str] = field(default_factory=list)
    not_suitable: list[str] = field(default_factory=list)
    other_skips: list[str] = field(default_factory=list)
    still_free: int = 0                                                # producible topics left after the last planned day

    @property
    def slots(self) -> int:
        return len(self.days) * self.per_day

    @property
    def planned(self) -> int:
        return sum(len(d.topics) for d in self.days)

    @property
    def missing(self) -> int:
        return self.slots - self.planned

    @property
    def substituted(self) -> int:
        """Planned topics whose Bildaufbau differs from the letter of the Konzeptplan (planned one not built or taken by the other topic of the day)."""
        return sum(1 for d in self.days for t in d.topics if t.aufbau_planned and t.aufbau != t.aufbau_planned)

    @property
    def same_aufbau_days(self) -> int:
        """Days on which both topics use the same Bildaufbau (only one fits)."""
        return sum(1 for d in self.days if len(d.topics) >= 2 and d.topics[0].aufbau == d.topics[1].aufbau)


@contextmanager
def cached_sources():
    """Calendar and research files are read once per planner process (select_topics asks for every candidate on every day)."""
    from . import context as cx
    orig_cal, orig_res = cx._calendar, cx._research
    cal_cache: dict[str, list] = {}
    res_cache: dict[str, list] = {}
    cx._calendar = lambda b: cal_cache.setdefault(b, orig_cal(b))
    cx._research = lambda b: res_cache.setdefault(b, orig_res(b))
    try:
        yield
    finally:
        cx._calendar, cx._research = orig_cal, orig_res


def _mem_state():
    from .records import State

    class MemState(State):
        """A copy of the real state that never writes to disk."""

        def __init__(self, data: dict):
            self.path = Path("<memory>")
            self.data = copy.deepcopy(data)

        def save(self) -> None:
            return None

    return MemState(State().data)


def _classify_skips(skipped: list[str], cands: list[Topic]) -> dict[str, list[str]]:
    by_desc = {t.describe(): t for t in cands}
    out: dict[str, list[str]] = {"no_source": [], "needs_model": [], "not_suitable": [], "done": [], "other": []}
    for line in skipped:
        t = next((by_desc[d] for d in by_desc if line.startswith(d + ": ")), None)
        label = f"Nr. {t.nr} {t.title}" if t is not None and t.nr else (f"{t.title}" if t is not None else line)
        if "keine geprüfte Quelle" in line:
            out["no_source"].append(label)
        elif "braucht Modell oder Aufbau" in line or "keine Aufzeichnung zugeordnet" in line:
            out["needs_model"].append(label)
        elif "nicht geeignet" in line:
            out["not_suitable"].append(label)
        elif "schon fertig" in line:
            out["done"].append(label)
        else:
            out["other"].append(f"{label} ({line.split(': ', 1)[-1][:80]})")
    return out


def plan_brand(brand_id: str, start: date, end: date, per_day: int = 2, assume_produced: list[tuple[date, int]] | None = None,
               log=lambda m: None, after: date | None = None) -> BrandPlan:
    """Simulate the daily runner from `start` to `end` (both included). `assume_produced`: (day, number of topics) taken before the
    plan starts because they are going to be produced but are not in the state yet (e.g. the run of tomorrow)."""
    from .pipeline import DailyRunner, Options

    s = brand_settings(brand_id)
    opts = Options(date=start.isoformat(), topics=per_day, provider="mock", dry_run=True, use_plan=False)
    runner = DailyRunner(brand_id, opts, log=lambda m: None)
    sim = _mem_state()
    runner.state = sim
    plan = BrandPlan(brand_id=brand_id, brand_name=s.name, start=start, end=end, per_day=per_day)
    from .topics import ordered_candidates
    cands = ordered_candidates(runner.kp, runner.s.topic_source)
    plan.total_candidates = len(cands)
    plan.done_before = len(sim.done_list(brand_id))

    def take(day: date, n: int, mark: bool = True):
        runner.opts.topics, runner.opts.date = n, day.isoformat()
        chosen, skipped = runner.select_topics()
        if mark:
            for t in chosen:
                sim.mark_done(brand_id, t, day.isoformat(), [], t.extra.get("aufbau_final"), {})
        return chosen, skipped

    if after is not None:
        # plan files of earlier months: topics planned for the days between `after` (today) and `start` are produced before this plan starts
        for f in sorted((DATA_DIR / "calendars").glob(f"{brand_id}_*.plan.json")):
            m = re.search(r"_(\d{4}-\d{2})\.plan\.json$", f.name)
            if not m or m.group(1) > start.strftime("%Y-%m"):
                continue
            try:
                old_rows = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for r in old_rows:
                if r.get("language") == "de" and r.get("plan_status") == "geplant":
                    d = date.fromisoformat(str(r["publish_at"])[:10])
                    if after < d < start:
                        sim.mark_done(brand_id, Topic(brand_id=brand_id, nr=r.get("nr"), title=str(r.get("title", ""))), d.isoformat(), [], r.get("aufbau"), {})
                        plan.from_earlier_plans += 1
    for day, n in (assume_produced or []):
        chosen, _ = take(day, n)
        for t in chosen:
            plan.assumed.append((day, f"Nr. {t.nr} {t.title}" if t.nr else t.title))
    day = start
    last_skipped: list[str] = []
    while day <= end:
        chosen, skipped = take(day, per_day)
        dp = DayPlan(day=day)
        for i, t in enumerate(chosen, 1):
            dp.topics.append(PlannedTopic(
                slot_index=i, nr=t.nr, title=t.title, reihe=t.reihe, aufbau=t.extra.get("aufbau_final"), aufbau_planned=t.aufbau,
                aufbau_note=t.extra.get("aufbau_note", ""), refs=list(t.extra.get("refs") or []), recording=t.extra.get("recording"),
                calendar_id=t.calendar_id, risk=t.risk, hook_idea=t.hook_idea, cal=t.extra.get("cal")))
        plan.days.append(dp)
        if len(chosen) < per_day:
            last_skipped = skipped          # this call looked at every remaining candidate
        day += timedelta(days=1)
    final, skipped_final = take(end, 10_000, mark=False)
    plan.still_free = len(final)
    cls = _classify_skips(skipped_final if skipped_final else last_skipped, cands)
    plan.no_source, plan.needs_model, plan.not_suitable, plan.other_skips = cls["no_source"], cls["needs_model"], cls["not_suitable"], cls["other"]
    # topics of the Konzeptplan with any source at all (calendar, research, aufbauten.yaml) independent of a built Bildaufbau
    from .context import calendar_entry, research_entry, source_refs
    from .settings import load_aufbauten
    named = {}
    for a in load_aufbauten(brand_id):
        for th in a.get("themen") or []:
            if isinstance(th, dict) and th.get("quellen"):
                named[str(th.get("nr"))] = True
    from .context import recording_for_title
    recordings = {str(k): v for k, v in (s.topic_source.get("recordings") or {}).items()}
    for t in cands:
        cal = calendar_entry(brand_id, t)
        refs = source_refs(t, cal, research_entry(brand_id, t, cal))
        rec = (recordings.get(str(t.nr)) or recording_for_title(brand_id, t.title)) if s.topic_source.get("require_recording") else None
        if refs or named.get(str(t.nr)) or rec:
            plan.with_source += 1
    return plan


# ------------------------------------------------------------------ plan file (calendar schema)
def _risk(t: PlannedTopic) -> str:
    r = (t.cal or {}).get("risk_level")
    if r in ("low", "medium", "high"):
        return r
    txt = (t.risk or "").lower()
    return "high" if ("hoch" in txt or "high" in txt) else "medium" if ("mittel" in txt or "medium" in txt) else "low"


def calendar_rows(plan: BrandPlan, slots: dict[str, list[str]], risk_default: str = "low") -> list[dict]:
    """Every slot of the plan as a calendar row; free slots stay `idea` with plan_status "offen"."""
    from .context import _calendar
    old = _calendar(plan.brand_id)
    by_id = {e.get("topic_id"): e for e in old}
    rows: list[dict] = []
    langs = list(slots)
    for dp in plan.days:
        for si in range(1, plan.per_day + 1):
            t = next((x for x in dp.topics if x.slot_index == si), None)
            for lang in langs:
                hh, mm = (int(x) for x in slots[lang][si - 1].split(":"))
                dt = datetime(dp.day.year, dp.day.month, dp.day.day, hh, mm, tzinfo=VIENNA)
                tid = f"{plan.brand_id}-{dp.day.strftime('%Y%m%d')}-{si}-{lang}"
                if t is None:
                    row = TopicRow(topic_id=tid, brand_id=plan.brand_id, language=lang, angle="", source_urls=[], source_checked_at=None,
                                   format="explainer", risk_level=risk_default, publish_at=dt.isoformat(), status="idea")
                    d = asdict(row)
                    d.update({"nr": None, "slot_index": si, "slot": slots[lang][si - 1], "aufbau": None, "plan_status": "offen"})
                    rows.append(d)
                    continue
                twin = by_id.get(re.sub(r"-de$", f"-{lang}", t.calendar_id)) if t.calendar_id and lang != "de" else None
                cal = t.cal or {}
                title = str((twin or cal).get("title") or t.title)
                angle = str(cal.get("angle") or t.hook_idea or t.title)
                fmt = cal.get("format") if cal.get("format") in FORMATS else "explainer"
                urls = [r.url for r in t.refs if getattr(r, "url", "")]
                checked = next((r.checked_at for r in t.refs if getattr(r, "checked_at", "")), None) or cal.get("source_checked_at")
                row = TopicRow(topic_id=tid, brand_id=plan.brand_id, language=lang, angle=angle, source_urls=urls,
                               source_checked_at=checked or None, format=fmt, risk_level=_risk(t), publish_at=dt.isoformat(),
                               status="planned", title=title,
                               notes=f"Konzeptplan Nr. {t.nr or '–'}, Reihe {t.reihe or '–'}, Bildaufbau {t.aufbau or '–'}"
                                     f"{' (' + t.aufbau_note + ')' if t.aufbau_note else ''}. Plan {plan.start:%d.%m.}–{plan.end:%d.%m.%Y}.",
                               tags=list(cal.get("tags") or []))
                d = asdict(row)
                d.update({"nr": t.nr, "slot_index": si, "slot": slots[lang][si - 1], "aufbau": t.aufbau, "aufbau_planned": t.aufbau_planned,
                          "aufbau_note": t.aufbau_note, "calendar_ref": t.calendar_id, "plan_status": "geplant", "reihe": t.reihe,
                          "recording": t.recording, "plattformen": PLATFORMS})
                rows.append(d)
    return rows


def write_calendar(plan: BrandPlan, rows: list[dict], month: str) -> Path:
    path = plan_file(plan.brand_id, month)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def check_calendar(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = [TopicRow(**{k: v for k, v in r.items() if k in TopicRow.__dataclass_fields__}) for r in data]
    return validate(rows)


# ------------------------------------------------------------------ Markdown
def _day_label(d: date) -> str:
    return f"{WEEKDAYS[d.weekday()]} {d:%d.%m.}"


def brand_markdown(plan: BrandPlan, slots: dict[str, list[str]], month: str, created: str) -> str:
    de, en = slots.get("de", []), slots.get("en", [])
    L: list[str] = []
    L.append(f"# Monatsplan {plan.brand_name} {month} ({plan.start:%d.%m.} bis {plan.end:%d.%m.%Y})")
    L.append("")
    L.append(f"Stand {created}. Erzeugt von `scripts/month_planner.py` (Tagesläufer-Sitzung) ohne Modellaufruf; Marken-ID `{plan.brand_id}`. "
             "Der Plan simuliert die Themenwahl des Tagesläufers: Konzeptplan-Reihenfolge, nur gebaute Bildaufbauten (`brands/<id>/aufbauten.yaml`), "
             "nur Themen mit geprüfter Quelle, Wechsel des Bildaufbaus. Der Tagesläufer liest ihn ab 05.11. aus "
             f"`data/calendars/{plan.brand_id}_{month}.plan.json`; ein Thema, das dort eine Prüfung nicht besteht, wird durch das nächste freie ersetzt.")
    L.append("")
    L.append(f"**Zahlen:** Konzeptplan {plan.total_candidates} Themen; davon mit Quelle {plan.with_source}; eingeplant {plan.planned} von {plan.slots} Plätzen "
             f"({plan.per_day} je Tag, {len(plan.days)} Tage); frei geblieben {plan.missing}; noch einplanbar nach dem {plan.end:%d.%m.} {plan.still_free}. "
             f"Ersatz-Bildaufbau (Konzeptplan-Buchstabe nicht gebaut oder vom anderen Thema des Tages belegt): {plan.substituted}; "
             f"Tage mit demselben Bildaufbau für beide Themen: {plan.same_aufbau_days}.")
    if plan.from_earlier_plans:
        L.append("")
        L.append(f"**Aus dem Plan des Vormonats für die Tage bis zum Start vorgesehen (nicht im Plan):** {plan.from_earlier_plans} Themen.")
    if plan.assumed:
        L.append("")
        L.append("**Schon produziert oder für den Vortag vorgesehen (nicht im Plan):** " + "; ".join(f"{d:%d.%m.}: {t}" for d, t in plan.assumed) + ".")
    L.append("")
    L.append("| Datum | Nr. und Titel | Bildaufbau | Quelle | Slot DE | Slot EN | Plattformen | Status |")
    L.append("|---|---|---|---|---|---|---|---|")
    for dp in plan.days:
        for si in range(1, plan.per_day + 1):
            t = next((x for x in dp.topics if x.slot_index == si), None)
            plats = ", ".join(PLATFORMS)
            if t is None:
                L.append(f"| {_day_label(dp.day)} | – (kein Thema verfügbar) | – | – | {de[si - 1]} | {en[si - 1]} | {plats} | offen |")
                continue
            auf = t.aufbau or "–"
            if t.aufbau_planned and t.aufbau and t.aufbau_planned != t.aufbau:
                auf = f"{t.aufbau} (Konzeptplan {t.aufbau_planned})"
            quelle = "ja" if t.refs else ("ja (Aufzeichnung)" if t.recording else "nein")
            title = t.title.replace("|", "/")
            L.append(f"| {_day_label(dp.day)} | Nr. {t.nr or '–'} {title} | {auf} | {quelle} | {de[si - 1]} | {en[si - 1]} | {plats} | geplant |")
    L.append("")
    L.append("## Ohne Quelle (Quelle fehlt, übersprungen)")
    L.append("")
    L.extend([f"- {x}" for x in plan.no_source] or ["- keine"])
    L.append("")
    L.append("## Braucht Modell, Aufbau oder Aufzeichnung (nicht einplanbar)")
    L.append("")
    if plan.needs_model:
        L.append(f"{len(plan.needs_model)} Themen; die ersten 20:")
        L.extend(f"- {x}" for x in plan.needs_model[:20])
        if len(plan.needs_model) > 20:
            L.append(f"- … und {len(plan.needs_model) - 20} weitere (`scripts/daily_runner.py --list-topics`)")
    else:
        L.append("- keine")
    if plan.not_suitable:
        L.append("")
        L.append("## Nicht geeignet (braucht neuen Szenencode laut `config/daily.yaml`)")
        L.append("")
        L.extend(f"- {x}" for x in plan.not_suitable)
    if plan.other_skips:
        L.append("")
        L.append("## Weitere Auslassungen")
        L.append("")
        L.extend(f"- {x}" for x in plan.other_skips[:20])
    L.append("")
    L.append("## Annahmen")
    L.append("")
    L.append(f"- 2 Themen je Tag in Deutsch und Englisch (Stefan, 03.11.2026, 20:45). Slots Wien (von Stefan am 03.11.2026 bestätigt, `config/brands.yaml`): "
             f"Thema 1 DE {de[0]}, EN {en[0]}; Thema 2 DE {de[1]}, EN {en[1]}.")
    L.append("- Das Datum ist der Tag der Veröffentlichung; der Tagesläufer produziert die Themen eines Tages mit `--date` dieses Tages.")
    L.append("- Themen mit Quelle: Kalender (`data/calendars`), Research-Dateien oder die Quellen je Thema in `brands/<id>/aufbauten.yaml`.")
    L.append("- Produziert wird nichts, was ein gebauter Bildaufbau nicht trägt; Lücken füllt der Monatsplaner nicht mit erfundenen Themen.")
    L.append("")
    return "\n".join(L)


def overview_markdown(plans: list[BrandPlan], slots: dict[str, list[str]], month: str, created: str, manual_sections: str = "",
                      warnings: list[str] | None = None) -> str:
    de, en = slots.get("de", []), slots.get("en", [])
    L: list[str] = []
    L.append(f"# Monatsplan {month}: Übersicht")
    L.append("")
    L.append(f"Stand {created}. Erzeugt von `scripts/month_planner.py` (Tagesläufer-Sitzung), Auftrag der Hauptsitzung nach Stefans Vorgabe vom 03.11.2026, 20:45: "
             "je Marke täglich 2 Themen auf Deutsch und Englisch (4 Videos), 7 Tage die Woche. Der Lauf am 04.11. (1 Thema je Marke) bleibt wie geplant.")
    L.append("")
    L.append("## Regeln und Annahmen")
    L.append("")
    L.append("- **Auswahl:** Konzeptplan-Reihenfolge (zuerst die Tagestabellen, dann die Vorschlagstabelle), ohne schon produzierte Themen "
             "(Testvideos, Prototyp, Lauf am 04.11.), nur mit geprüfter Quelle, nur mit gebautem Bildaufbau; Wechsel des Bildaufbaus zwischen den Themen eines Tages und von Tag zu Tag.")
    L.append(f"- **Slots (Wien, von Stefan am 03.11.2026 bestätigt, änderbar in `config/brands.yaml` unter `slots_by_language`):** Thema 1 DE {de[0]}, EN {en[0]}; Thema 2 DE {de[1]}, EN {en[1]}. "
             "Plattformen je Video: TikTok, Instagram Reels, YouTube Shorts.")
    L.append("- **Revlore:** Technik-Themen zuerst, Motor-Themen höchstens jedes dritte Thema; nur Themen, die `brands/engines/aufbauten.yaml` mit Quellen nennt.")
    L.append("- **Promptwerk:** nur Themen mit vorhandener Aufzeichnung (der Tagesläufer nimmt nichts auf); Stimme DE mit `voice_tts.py --say Claude=Klohd`.")
    L.append("- **Lücken:** Ein Platz ohne Thema bleibt „offen“. Der Monatsplaner erfindet keine Themen; Vorschläge über `claude -p` erst auf Anweisung, immer als „Vorschlag, Quelle prüfen“.")
    L.append("- **Kalenderdateien:** Der Plan liegt in `data/calendars/<id>_2026-11.plan.json` (Schema von `fn.cli calendar init` plus Bildaufbau und Slots). "
             "Die vorhandenen `<id>_2026-11.json` bleiben unverändert: Markenwerkzeuge lesen sie und sie enthalten die geprüften Quellen und die Ids der produzierten Videos.")
    L.append("")
    L.append("## Zahlen je Marke")
    L.append("")
    L.append("| Marke | Konzeptplan | mit Quelle | eingeplant | Plätze | frei | Quelle fehlt | braucht Modell/Aufbau | noch einplanbar | Ersatz-Bildaufbau | Tage mit gleichem Bildaufbau |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for p in plans:
        L.append(f"| {p.brand_name} (`{p.brand_id}`) | {p.total_candidates} | {p.with_source} | {p.planned} | {p.slots} | {p.missing} | "
                 f"{len(p.no_source)} | {len(p.needs_model)} | {p.still_free} | {p.substituted} | {p.same_aufbau_days} |")
    tot_planned, tot_slots = sum(p.planned for p in plans), sum(p.slots for p in plans)
    L.append(f"| **Summe** | | | **{tot_planned}** | **{tot_slots}** | **{tot_slots - tot_planned}** | | | | | |")
    L.append("")
    L.append("„Plätze“ sind 2 je Tag über den Planungszeitraum. „frei“ sind Plätze ohne produzierbares Thema; sie füllen sich, wenn die Marken-Sitzungen "
             "Bildaufbauten bauen oder Quellen prüfen (dann den Plan neu erzeugen: `scripts/month_planner.py`).")
    L.append("")
    L.append("## Lücken je Marke")
    L.append("")
    for p in plans:
        bits = [f"{p.brand_name}: {p.planned} von {p.slots} Plätzen belegt"]
        if p.missing:
            bits.append(f"{p.missing} offen")
        if p.no_source:
            bits.append(f"Quelle fehlt: {len(p.no_source)}")
        if p.needs_model:
            bits.append(f"braucht Modell, Aufbau oder Aufzeichnung: {len(p.needs_model)}")
        if p.not_suitable:
            bits.append(f"nicht geeignet: {len(p.not_suitable)}")
        if p.assumed:
            bits.append("04.11. vorgesehen: " + "; ".join(t for _, t in p.assumed))
        L.append("- " + "; ".join(bits) + f". Einzelheiten: `Monatsplan {p.brand_name} {month}.md`.")
    L.append("")
    if warnings:
        L.append("## Hinweise zum Neuerzeugen")
        L.append("")
        L.extend(f"- {w}" for w in warnings)
        L.append("")
    if manual_sections:
        L.append(manual_sections.rstrip())
        L.append("")
    L.append("## Dateien")
    L.append("")
    for p in plans:
        L.append(f"- `Monatsplan {p.brand_name} {month}.md`, `data/calendars/{p.brand_id}_{month}.plan.json`")
    L.append("- Programm: `scripts/month_planner.py`, Modul `src/fn/daily/monthplan.py`, Aufgabenvorlage `automation/run_month_plan.ps1`; Beschreibung in `docs/daily-runner.md`.")
    L.append("")
    return "\n".join(L)
