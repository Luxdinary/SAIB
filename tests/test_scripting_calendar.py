from datetime import date

from fn import calendar as cal
from fn import scripting
from fn.config import brands_config


def test_script_parse_and_check_ok(sample_script_text):
    s = scripting.parse(sample_script_text)
    assert s.brand_id == "ai_security" and s.language == "de"
    assert [sc.kind for sc in s.scenes] == ["hook", "card", "payoff"]
    assert s.scenes[1].source_ids == ["S1"]
    assert "[S1]" not in s.scenes[1].spoken
    assert s.scenes[1].visual["headline"] == "Karte"
    assert scripting.check(s) == []


def test_unverified_blocks(sample_script_text):
    s = scripting.parse(sample_script_text.replace("Die eine Sache.", "UNVERIFIED: Die eine Sache."))
    problems = scripting.check(s)
    assert any("UNVERIFIED" in p for p in problems)


def test_missing_source_marker_and_unknown_ref(sample_script_text):
    s = scripting.parse(sample_script_text.replace(" [S1]", " [S9]"))
    problems = scripting.check(s)
    assert any("unknown source S9" in p for p in problems)
    s2 = scripting.parse(sample_script_text.replace(" [S1]", ""))
    assert any("no source marker" in p for p in scripting.check(s2))


def test_calendar_grid_and_validation():
    # the grid follows config/brands.yaml (slots_by_language): until 03.11.2026 3 DE + 3 EN a day, since Stefan's order of 03.11. (20:45)
    # 2 DE (12:00, 18:00) + 2 EN (15:00, 21:00 Vienna); topic i of a day is a DE/EN twin
    by_lang = brands_config()["defaults"]["slots_by_language"]
    n = len(by_lang["de"])
    rows = cal.build_grid("ai_security", date(2026, 11, 5), days=2)
    assert len(rows) == 2 * 2 * n
    assert rows[0].publish_at.startswith(f"2026-11-05T{by_lang['de'][0]}:00+01:00")
    day0 = rows[:2 * n]
    assert [r.language for r in day0].count("de") == n and [r.language for r in day0].count("en") == n
    assert rows[n].publish_at.startswith(f"2026-11-05T{by_lang['en'][0]}:00+01:00") and rows[n].language == "en"
    assert cal.validate(rows) == []
    rows[0].status = "planned"
    problems = cal.validate(rows)
    assert any("needs an angle" in p for p in problems)
    rows[0].angle = "Warum die Kundenliste nicht in den Chat gehört"
    rows[0].source_urls = ["https://example.org/a"]
    rows[0].source_checked_at = "2026-10-30"
    rows[2 * n].angle = "Warum die Kundenliste nicht in den Chat gehört"   # next day, same angle -> duplicate
    rows[2 * n].status = "planned"
    rows[2 * n].source_urls = ["https://example.org/a"]
    rows[2 * n].source_checked_at = "2026-10-30"
    problems = cal.validate(rows)
    assert any("duplicate angle" in p for p in problems)
    rows[n].angle = rows[0].angle   # same day, other language -> twin, allowed
    assert cal.twin_topic(rows, rows[0]) is rows[n]
