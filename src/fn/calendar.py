"""Topic calendar: 30 days ahead per brand, one row per topic and language.

Fields: topic_id, brand_id, language, angle, source_urls, source_checked_at, format, risk_level,
publish_at (ISO 8601 with Europe/Vienna offset), status. Stored as JSON in data/calendars/<brand>_<month>.json.
Claude Code fills `angle` and `source_urls` through prompts/calendar_planner.md; this module only
builds the slot grid, validates rows and detects duplicate angles.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import DATA_DIR, brands_config

VIENNA = ZoneInfo("Europe/Vienna")
FORMATS = ("explainer", "listicle", "myth", "howto", "story", "comparison")
RISK_LEVELS = ("low", "medium", "high")
STATUSES = ("idea", "planned", "researched", "scripted", "produced", "published", "dropped")
URL_RE = re.compile(r"^https?://[^\s]+$")


@dataclass
class TopicRow:
    topic_id: str
    brand_id: str
    language: str
    angle: str
    source_urls: list[str]
    source_checked_at: str | None
    format: str
    risk_level: str
    publish_at: str
    status: str = "idea"
    title: str = ""
    notes: str = ""
    tags: list[str] = field(default_factory=list)

    def angle_hash(self) -> str:
        norm = re.sub(r"[^a-z0-9äöüß ]", "", self.angle.lower())
        norm = " ".join(sorted(set(norm.split())))
        return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]


def slot_datetimes(start: date, days: int, slots: list[str]) -> list[datetime]:
    out = []
    for d in range(days):
        day = start + timedelta(days=d)
        for s in slots:
            hh, mm = (int(x) for x in s.split(":"))
            out.append(datetime(day.year, day.month, day.day, hh, mm, tzinfo=VIENNA))
    return out


def language_for_slot(slot_index: int, languages: list[str], day_index: int) -> str:
    """Alternate languages across slots and days so each day has both and the pattern shifts daily."""
    return languages[(slot_index + day_index) % len(languages)]


def build_grid(brand_id: str, start: date, days: int = 30) -> list[TopicRow]:
    cfg = brands_config()
    defaults = cfg["defaults"]
    entry = next(b for b in cfg["brands"] if b["id"] == brand_id)
    slots = defaults["slots"]
    languages = defaults["languages"]
    rows: list[TopicRow] = []
    by_lang = defaults.get("slots_by_language")
    if by_lang:      # Stefan, 01.11.2026: fixed times per language; topic i of a day is a DE/EN twin
        for d in range(days):
            day = start + timedelta(days=d)
            for lang in languages:
                for si, s in enumerate(by_lang[lang]):
                    hh, mm = (int(x) for x in s.split(":"))
                    dt = datetime(day.year, day.month, day.day, hh, mm, tzinfo=VIENNA)
                    tid = f"{brand_id}-{day.strftime('%Y%m%d')}-{si + 1}-{lang}"
                    rows.append(TopicRow(topic_id=tid, brand_id=brand_id, language=lang, angle="", source_urls=[],
                                         source_checked_at=None, format="explainer", risk_level=entry["risk_default"],
                                         publish_at=dt.isoformat(), status="idea"))
        return rows
    for d in range(days):
        day = start + timedelta(days=d)
        for si, s in enumerate(slots):
            hh, mm = (int(x) for x in s.split(":"))
            dt = datetime(day.year, day.month, day.day, hh, mm, tzinfo=VIENNA)
            lang = language_for_slot(si, languages, d)
            tid = f"{brand_id}-{day.strftime('%Y%m%d')}-{si + 1}"
            rows.append(TopicRow(topic_id=tid, brand_id=brand_id, language=lang, angle="", source_urls=[],
                                 source_checked_at=None, format="explainer", risk_level=entry["risk_default"],
                                 publish_at=dt.isoformat(), status="idea"))
    return rows


def calendar_path(brand_id: str, start: date) -> Path:
    return DATA_DIR / "calendars" / f"{brand_id}_{start.strftime('%Y-%m')}.json"


def save(rows: list[TopicRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(r) for r in rows], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load(path: Path) -> list[TopicRow]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [TopicRow(**{k: v for k, v in row.items() if k in TopicRow.__dataclass_fields__}) for row in data]


def validate(rows: list[TopicRow]) -> list[str]:
    """Return a list of problems; an empty list means the calendar is consistent."""
    problems: list[str] = []
    seen_ids: set[str] = set()
    seen_angles: dict[tuple[str, str], str] = {}
    seen_slots: set[tuple[str, str]] = set()
    for r in rows:
        if r.topic_id in seen_ids:
            problems.append(f"{r.topic_id}: duplicate topic_id")
        seen_ids.add(r.topic_id)
        if r.format not in FORMATS:
            problems.append(f"{r.topic_id}: unknown format {r.format}")
        if r.risk_level not in RISK_LEVELS:
            problems.append(f"{r.topic_id}: unknown risk_level {r.risk_level}")
        if r.status not in STATUSES:
            problems.append(f"{r.topic_id}: unknown status {r.status}")
        try:
            dt = datetime.fromisoformat(r.publish_at)
            if dt.tzinfo is None:
                problems.append(f"{r.topic_id}: publish_at without timezone")
        except ValueError:
            problems.append(f"{r.topic_id}: bad publish_at {r.publish_at}")
        key = (r.brand_id, r.publish_at)
        if key in seen_slots:
            problems.append(f"{r.topic_id}: two topics in the same slot {r.publish_at}")
        seen_slots.add(key)
        for u in r.source_urls:
            if not URL_RE.match(u):
                problems.append(f"{r.topic_id}: bad source url {u!r}")
        if r.status not in ("idea", "dropped"):
            if not r.angle.strip():
                problems.append(f"{r.topic_id}: status {r.status} needs an angle")
            if not r.source_urls:
                problems.append(f"{r.topic_id}: status {r.status} needs source_urls")
            if not r.source_checked_at:
                problems.append(f"{r.topic_id}: status {r.status} needs source_checked_at")
        if r.angle.strip():
            ah = r.angle_hash()
            k = (r.brand_id, ah)
            if k in seen_angles and seen_angles[k] != r.topic_id:
                # same angle in two languages on the same day is allowed (DE/EN twin); otherwise a duplicate
                other = next(x for x in rows if x.topic_id == seen_angles[k])
                same_day = other.publish_at[:10] == r.publish_at[:10] and other.language != r.language
                if not same_day:
                    problems.append(f"{r.topic_id}: duplicate angle of {seen_angles[k]}")
            seen_angles.setdefault(k, r.topic_id)
    return problems


def twin_topic(rows: list[TopicRow], topic: TopicRow) -> TopicRow | None:
    """The same-day row in the other language with the same angle (DE/EN twin), if any."""
    for r in rows:
        if r is not topic and r.brand_id == topic.brand_id and r.publish_at[:10] == topic.publish_at[:10] \
                and r.language != topic.language and r.angle_hash() == topic.angle_hash():
            return r
    return None
