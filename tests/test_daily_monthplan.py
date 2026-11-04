"""Month plan: plan file for a day, order of candidates, calendar rows in the fn.calendar schema, produced-by-title detection."""
from __future__ import annotations

import json
from datetime import date

from fn.calendar import validate, TopicRow
from fn.daily import monthplan as mp
from fn.daily.context import SourceRef
from fn.daily.pipeline import DailyRunner, Options
from fn.daily.records import csv_done_titles
from fn.daily.topics import Topic, _is_done_row


def test_pilot_export_marks_a_row_as_done():
    cells = ["5", "Deny-Regel gegen das Lesen der .env (Pilot)", "Hält das?", "Reel", "Hook", "belegt; Pilot-Export DE und EN vorhanden", "mittel"]
    assert _is_done_row(cells, cells[1]) is True
    assert _is_done_row(["6", "Anderes Thema", "x", "y", "z", "Quelle zu prüfen", "niedrig"], "Anderes Thema") is False


def test_csv_done_titles_ignore_language_suffix_and_other_brands(tmp_path):
    p = tmp_path / "Redaktionsplan.csv"
    p.write_text("ID;Thema;Format;Kanal;Status;Drehtermin;Veröffentlichung;Produktionsordner;Link;Notiz\n"
                 "claude_workflows-20261103-tv-de-echtlauf-T5;Testvideo Promptwerk: Kundenliste mit Dubletten bereinigen (Neustart, DE);r;k;fertig;;;;;\n"
                 "claude_workflows-20261103-tv-en-echtlauf-T1;Promptwerk test video: Clean up a customer list (EN);r;k;fertig;;;;;\n"
                 "menswear-20261103-2-de-D1;Super 100s und die Zahl (DE);r;k;fertig;;;;;\n"
                 "claude_workflows-x-1;Entwurf ohne Status;r;k;idee;;;;;\n", encoding="utf-8")
    titles = csv_done_titles("claude_workflows", p)
    assert any("kundenliste mit dubletten bereinigen" in t for t in titles)
    assert not any("super 100s" in t for t in titles)          # other brand
    assert not any("entwurf" in t for t in titles)             # status idee


def test_plan_for_day_returns_planned_german_rows_in_slot_order(tmp_path, monkeypatch):
    rows = [
        {"language": "en", "plan_status": "geplant", "publish_at": "2026-11-05T15:00:00+01:00", "slot_index": 1, "nr": "4"},
        {"language": "de", "plan_status": "geplant", "publish_at": "2026-11-05T18:00:00+01:00", "slot_index": 2, "nr": "6"},
        {"language": "de", "plan_status": "geplant", "publish_at": "2026-11-05T12:00:00+01:00", "slot_index": 1, "nr": "4"},
        {"language": "de", "plan_status": "offen", "publish_at": "2026-11-06T12:00:00+01:00", "slot_index": 1, "nr": None},
    ]
    f = tmp_path / "x_2026-11.plan.json"
    f.write_text(json.dumps(rows), encoding="utf-8")
    monkeypatch.setattr(mp, "plan_file", lambda brand, month: f)
    assert [r["nr"] for r in mp.plan_for_day("x", "2026-11-05")] == ["4", "6"]
    assert mp.plan_for_day("x", "2026-11-06") == []                  # free slot is not a plan entry
    assert mp.plan_for_day("x", "2026-12-01") == []


def test_apply_plan_moves_planned_topics_first_and_sets_the_planned_aufbau(monkeypatch):
    runner = DailyRunner.__new__(DailyRunner)
    runner.brand_id, runner.opts = "x", Options(date="2026-11-05")
    runner._note = lambda m: None
    cands = [Topic(brand_id="x", nr=str(n), title=f"Thema {n}", aufbau="A") for n in (1, 2, 3, 4)]
    monkeypatch.setattr(mp, "plan_for_day", lambda b, d: [{"nr": "3", "aufbau": "C", "slot_index": 1}, {"nr": "2", "aufbau": "B", "slot_index": 2}])
    out = runner._apply_plan(cands)
    assert [t.nr for t in out] == ["3", "2", "1", "4"]
    assert out[0].aufbau == "C" and out[1].aufbau == "B" and out[2].aufbau == "A"
    runner.opts.use_plan = False
    assert runner._apply_plan(cands) is cands                         # switched off: untouched
    monkeypatch.setattr(mp, "plan_for_day", lambda b, d: [])
    runner.opts.use_plan = True
    assert runner._apply_plan(cands) is cands                         # no plan for the day: nothing changes


def test_calendar_rows_follow_the_calendar_schema_with_slots():
    t = mp.PlannedTopic(slot_index=1, nr="7", title="Ein Thema", reihe="R", aufbau="A", aufbau_planned="B", aufbau_note="B ersetzt durch A",
                        refs=[SourceRef(id="S1", url="https://example.org/a", title="t", checked_at="2026-11-01")], risk="niedrig", hook_idea="Hook")
    plan = mp.BrandPlan(brand_id="x", brand_name="X", start=date(2026, 11, 5), end=date(2026, 11, 5), per_day=2,
                        days=[mp.DayPlan(day=date(2026, 11, 5), topics=[t])])
    rows = mp.calendar_rows(plan, {"de": ["12:00", "18:00"], "en": ["15:00", "21:00"]})
    assert len(rows) == 4                                              # 2 slots x 2 languages x 1 day (the free slot stays as an idea row)
    planned = [r for r in rows if r["plan_status"] == "geplant"]
    assert [r["publish_at"][11:16] for r in planned] == ["12:00", "15:00"] and {r["language"] for r in planned} == {"de", "en"}
    assert all(r["aufbau"] == "A" and r["nr"] == "7" for r in planned)
    free = [r for r in rows if r["plan_status"] == "offen"]
    assert [r["publish_at"][11:16] for r in free] == ["18:00", "21:00"]
    assert validate([TopicRow(**{k: v for k, v in r.items() if k in TopicRow.__dataclass_fields__}) for r in rows]) == []


def test_proposals_parse_and_render_as_unchecked_ideas(tmp_path):
    from fn.costs import CostLogger
    from fn.daily import proposals as prop
    from fn.daily.llm import MockProvider
    answer = ('Hier das Ergebnis:\n```json\n{"vorschlaege": [{"titel": "Beispielthema", "reihe": "R", "hook": "Ein Satz.", "bildaufbau": "A", '
              '"risiko": "niedrig", "quellen": [{"titel": "T", "institution": "I", "url": "", "suchhinweis": "suche"}], "hinweis": "prüfen"}, {"titel": ""}]}\n```')
    provider = MockProvider()
    provider.queue.append(answer)
    items = prop.propose("menswear", 3, ["Vorhandener Titel"], ["1 | Thema | Reihe | Hook | Quelle | niedrig"], ["Reihe"], provider,
                         CostLogger(tmp_path / "costs.jsonl"), {}, "2026-12", check=False)
    assert [i["titel"] for i in items] == ["Beispielthema"]                     # the empty title is dropped
    md = prop.proposals_markdown("Suitwerk", "menswear", "2026-12", items, "03.11.2026 22:00")
    assert "Vorschlag, Quelle prüfen" in md and "nicht einplanbar" in md and "| V1 |" in md
    assert (tmp_path / "costs.jsonl").exists()                                     # tokens are logged like every model call
    system, user = prop.build_prompt("menswear", 3, ["Vorhandener Titel"], [], [])
    assert "Erfinde keine URLs" in system and "Vorhandener Titel" in user
