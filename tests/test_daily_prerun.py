"""Before every daily run: invalid aufbauten.yaml falls back to the last valid copy, the re-plan arguments, the daily limit per brand."""
from __future__ import annotations

from datetime import date

from fn.daily import monthplan as mp
from fn.daily import settings
from fn.daily.pipeline import DailyRunner, Options

VALID = """aufbauten:
  - kuerzel: A
    name: Eins
    gebaut: true
    szenentypen: [x_photo]
    themen: [7]
"""
BROKEN = "aufbauten:\n  - kuerzel: A\n    name: [halb fertig\n    gebaut: tr"


def _setup(tmp_path, monkeypatch):
    import fn.config as cfg
    brands = tmp_path / "brands"
    (brands / "x").mkdir(parents=True)
    monkeypatch.setattr(cfg, "BRANDS_DIR", brands)
    monkeypatch.setattr(settings, "AUFBAUTEN_OK_DIR", tmp_path / "ok")
    monkeypatch.setattr(settings, "AUFBAUTEN_WARNINGS", [])
    monkeypatch.setattr(settings, "_REMEMBERED", {})
    return brands / "x" / "aufbauten.yaml"


def test_invalid_yaml_uses_the_last_valid_copy_and_warns(tmp_path, monkeypatch):
    f = _setup(tmp_path, monkeypatch)
    f.write_text(VALID, encoding="utf-8")
    good = settings.load_aufbauten("x")
    assert [a["kuerzel"] for a in good] == ["A"] and settings.AUFBAUTEN_WARNINGS == []
    assert (tmp_path / "ok" / "x.yaml").exists()                      # copy of the valid state
    f.write_text(BROKEN, encoding="utf-8")                             # a brand session is half way through writing
    again = settings.load_aufbauten("x")
    assert [a["kuerzel"] for a in again] == ["A"] and again[0]["themen"] == [7]
    assert len(settings.AUFBAUTEN_WARNINGS) == 1 and "letzten gültigen Stand" in settings.AUFBAUTEN_WARNINGS[0]
    settings.load_aufbauten("x")
    assert len(settings.AUFBAUTEN_WARNINGS) == 1                       # reported once


def test_invalid_yaml_without_a_copy_gives_no_aufbauten_and_says_so(tmp_path, monkeypatch):
    f = _setup(tmp_path, monkeypatch)
    f.write_text(BROKEN, encoding="utf-8")
    assert settings.load_aufbauten("x") == []
    assert "keinen letzten gültigen Stand" in settings.AUFBAUTEN_WARNINGS[0]


def test_replan_args_cover_the_run_day_or_assume_it(monkeypatch):
    monkeypatch.setattr(mp, "configured_brands", lambda: ["a", "b"])
    monkeypatch.setattr(mp, "plan_for_day", lambda b, d: [{"nr": "1"}] if d == "2026-11-05" else [])
    # the plan covers the day: plan again from that day
    assert mp.replan_args("2026-11-05", 2, ["all"]) == ["--month", "2026-11", "--from", "2026-11-05", "--brands", "a,b"]
    # not covered (04.11.): plan from the next day and assume this run's topics
    assert mp.replan_args("2026-11-04", 1, ["a"]) == ["--month", "2026-11", "--from", "2026-11-05", "--brands", "a", "--assume", "2026-11-04:1"]
    # last day of the month and not covered: the next month belongs to the monthly task
    assert mp.replan_args("2026-11-30", 2, ["a"]) is None


def test_a_rerun_never_produces_more_than_the_daily_target():
    runner = DailyRunner.__new__(DailyRunner)
    runner.brand_id, runner.opts = "x", Options(date="2026-11-05", topics=2)

    class S:
        def done_list(self, brand):
            return [{"date": "2026-11-05"}, {"date": "2026-11-05"}, {"date": "2026-11-04"}]

    runner.state = S()
    chosen, skipped = runner.select_topics()
    assert chosen == [] and skipped[0].startswith("Tageskontingent")
