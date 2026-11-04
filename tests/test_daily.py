"""Daily runner: Konzeptplan parsing, topic matching, plan validation helpers, CSV rows, JSON extraction."""
from __future__ import annotations

import json
from pathlib import Path

from fn.daily import llm, records, topics, validate

SAMPLE = """# Konzeptplan Probe (ab November 2026)

## Bildaufbauten (ab 04.11.2026)

| Aufbau | Bild | passt zu |
|---|---|---|
| **A Anwendung** | Hände und Produkt | Alltag |
| **B Lupe** | Produktfoto groß | Unter der Lupe |

| Tag | Thema 1 (Aufbau) | Thema 2 (Aufbau) |
|---|---|---|
| 04.11. | Nr. 2 Zweites Thema (B) | Erstes Thema, Müller et al. 2020 (A) |
| 05.11. | Drittes Thema (A) | Nr. 4 Viertes Thema (B) reserviert |

## Vorschläge

| Nr | Thema/Titel | Reihe | Format | Hook-Idee | Quellenstand | Risiko |
|---|---|---|---|---|---|---|
| 1 | Erstes Thema: der Vergleich | Reihe X | Reel 70–80 s | Hook eins | belegt im Kalender probe-20261109-1-de | niedrig |
| 2 | Zweites Thema (Pilot produziert) | Reihe Y | Reel | Hook zwei | belegt im Kalender probe-20261109-2-de | niedrig |
| 3 | Drittes Thema ganz anders | Reihe X | Reel | Hook drei | Quelle zu prüfen | mittel |
| 4 | Viertes Thema | Reihe Y | Reel | Hook vier | belegt im Kalender probe-20261110-1-de | niedrig |
"""


def test_tables_and_day_topics():
    tables = topics.parse_tables(SAMPLE)
    assert len(tables) == 3
    auf = topics.aufbau_table(tables)
    assert set(auf) == {"A", "B"}
    props = topics.topics_from_proposals("probe", topics.proposal_tables(tables, ["Vorschläge"]))
    assert [p.nr for p in props] == ["1", "2", "3", "4"]
    assert props[1].done_marker and props[0].calendar_id == "probe-20261109-1-de"
    days = topics.topics_from_day_tables("probe", topics.day_tables(tables, "Thema 1 (Aufbau)"))
    assert [(d.nr, d.aufbau, d.day, d.slot) for d in days] == [("2", "B", "04.11.", 1), (None, "A", "04.11.", 2), (None, "A", "05.11.", 1), ("4", "B", "05.11.", 2)]
    assert topics.match_topic(days[1], props).nr == "1"
    assert topics.match_topic(days[2], props).nr == "3"
    assert [d.reserved for d in days] == [False, False, False, True]


def test_ordered_candidates_merge():
    tables = topics.parse_tables(SAMPLE)
    kp = topics.Konzeptplan(Path("probe.md"), SAMPLE, tables,
                            topics.topics_from_proposals("probe", topics.proposal_tables(tables, ["Vorschläge"])),
                            topics.topics_from_day_tables("probe", topics.day_tables(tables, "Thema 1 (Aufbau)")),
                            topics.aufbau_table(tables))
    cands = topics.ordered_candidates(kp, {"kind": "day_table", "day_table_marker": "Thema 1 (Aufbau)"})
    assert [c.nr for c in cands] == ["2", "1", "3", "4"]
    assert cands[1].aufbau == "A" and cands[1].day == "04.11." and cands[1].calendar_id == "probe-20261109-1-de"


def test_day_cell_parsing():
    assert topics._parse_day_cell("Nr. 47 „Was ein KI-Chat speichert“, A (Chatfenster statt Mail)") == ("47", "Was ein KI-Chat speichert", "A", "Chatfenster statt Mail")
    assert topics._parse_day_cell("Hadrianswall (Nr. 24)") == ("24", "Hadrianswall", None, "")
    assert topics._parse_day_cell("Stoffgewicht (B)") == (None, "Stoffgewicht", "B", "")
    assert topics._parse_day_cell("Super 100s (B, mit Ärmel-Makro statt Waage)") == (None, "Super 100s", "B", "mit Ärmel-Makro statt Waage")


def test_anchor_and_json_helpers():
    res = validate.ValidationResult()
    beat = {"id": "b1", "spoken": "Zwei Auslöser, zwei Uhren. Beim Kurzschluss nicht.", "data": {"a": "w:Uhren", "b": "w:Zwei", "c": "w:fehlt", "d": "@Kurzschluss+0.4", "e_word": "Beim"}}
    validate._check_anchors(beat, res, "beat b1")
    assert any("w:fehlt" in e for e in res.errors) and len(res.errors) == 1
    assert llm.extract_json('Hier ist der Plan:\n```json\n{"a": {"b": "x}"}, "c": [1, 2]}\n```\nEnde') == {"a": {"b": "x}"}, "c": [1, 2]}


def test_csv_row_format():
    row = records.csv_row("engines-20261104-2-de-D1", "Titel; mit Strich", "de", 77.25, "Revlore", r"05 Produktion\Revlore\2026-11\2026-11-04 Kurz", "Notiz")
    assert row.endswith("\r\n") and row.count(";") >= 9 and "77,2 s" in row and '"Titel; mit Strich (DE)"' in row


def test_compare_structure_detects_changes():
    de = {"beats": [{"id": "b1", "function": "hook", "scene_type": "x", "data": {"k": 1}, "source_ids": ["S1"]}],
          "sources": [{"id": "S1", "url": "https://a"}], "assets": {}, "layout": {"zone_top": 290, "description": "d"}, "hook": {"id": "H1"}}
    en = json.loads(json.dumps(de))
    assert validate.compare_structure(de, en) == []
    en["beats"][0]["data"] = {"k": 1, "extra": 2}
    en["layout"]["zone_top"] = 300
    probs = validate.compare_structure(de, en)
    assert len(probs) == 2
