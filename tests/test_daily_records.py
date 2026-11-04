"""Daily runner: shared-file safety (CSV append, Konzeptplan markers by content), Aufbau lists, example excerpt."""
from __future__ import annotations

import json
from pathlib import Path

from fn.daily import context, records, topics
from fn.daily.pipeline import DailyRunner, Options
from fn.daily.records import append_csv_row, mark_konzeptplan

PLAN = """# Konzeptplan Probe

## Bildaufbauten
| Aufbau | Bild |
|---|---|
| **A Eins** | x |

| Tag | Thema 1 (Aufbau) | Thema 2 (Aufbau) |
|---|---|---|
| 06.11. | Erstes Thema (A) | Nr. 2 Zweites Thema (A) |

## Vorschläge
| Nr | Thema/Titel | Reihe | Format | Hook-Idee | Quellenstand | Risiko |
|---|---|---|---|---|---|---|
| 1 | Erstes Thema | R | Reel | h1 | belegt im Kalender probe-20261109-1-de | niedrig |
| 2 | Zweites Thema | R | Reel | h2 | belegt im Kalender probe-20261109-2-de | niedrig |
"""


def _kp(tmp_path: Path):
    f = tmp_path / "Konzeptplan Probe.md"
    f.write_text(PLAN, encoding="utf-8", newline="\r\n")
    kp = topics.load_konzeptplan("probe", f, {"kind": "day_table", "day_table_marker": "Thema 1 (Aufbau)", "tables": ["Vorschläge"]})
    cands = topics.ordered_candidates(kp, {"kind": "day_table"})
    return f, kp, cands


def test_marker_is_placed_by_content_even_when_lines_moved(tmp_path):
    f, kp, cands = _kp(tmp_path)
    first = next(c for c in cands if c.nr == "1")
    # a brand session inserts two lines at the top while the run is going: line numbers are stale now
    f.write_bytes(b"Zeile oben\r\nnoch eine\n" + f.read_bytes())                  # one CRLF line, one LF line, then CRLF content
    done = mark_konzeptplan(f, first, "Tagesläufer: produziert 2026-11-06 (x)")
    text = f.read_bytes().decode("utf-8")
    assert "Zeile oben" in text and any("Vorschlag Zeile" in d for d in done)
    rows = [ln for ln in text.splitlines() if "Tagesläufer: produziert" in ln]
    assert len(rows) == 2                                               # proposal row and day row
    assert any(ln.startswith("| 1 |") for ln in rows)
    day = next(ln for ln in rows if ln.startswith("| 06.11."))
    cells = day.strip("|").split("|")
    assert "Tagesläufer" in cells[1] and "Tagesläufer" not in cells[2]    # marker sits in the cell of the topic (Thema 1)
    raw = f.read_bytes().decode("utf-8")
    assert raw.startswith("Zeile oben\r\nnoch eine\n# Konzeptplan") and raw.count("\r\n") == PLAN.count("\n") + 1   # each line kept its own ending


def test_marker_skips_a_row_that_changed(tmp_path):
    f, kp, cands = _kp(tmp_path)
    second = next(c for c in cands if c.nr == "2")
    f.write_text(f.read_text(encoding="utf-8").replace("| 2 | Zweites Thema | R |", "| 2 | Zweites Thema reserviert | R |"), encoding="utf-8", newline="")
    done = mark_konzeptplan(f, second, "M")
    assert any("geändert" in d for d in done)
    assert "· M" not in f.read_text(encoding="utf-8").split("## Vorschläge")[1]


def test_csv_append_keeps_other_rows_and_bom(tmp_path):
    p = tmp_path / "Redaktionsplan.csv"
    p.write_bytes(b"\xef\xbb\xbfID;Thema\r\na;b")                       # no trailing newline, as another session may leave it
    append_csv_row("c;d\r\n", p)
    append_csv_row("e;f\r\n", p)
    raw = p.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf") and raw.decode("utf-8-sig").splitlines() == ["ID;Thema", "a;b", "c;d", "e;f"]


def test_slot_ids_ignore_calendar_ids_and_count_d_ids(tmp_path, monkeypatch):
    d = tmp_path / "direction"
    d.mkdir()
    for name in ("probe-20261106-d1-de.D1.json", "probe-20261106-3-de.json", "probe-20261107-d1-de.D1.json"):
        (d / name).write_text("{}", encoding="utf-8")
    monkeypatch.setattr(records, "DATA_DIR", tmp_path)
    monkeypatch.setattr(records, "STORAGE_DIR", tmp_path / "none")
    assert records.next_slot("probe", "20261106") == 2                    # d1 used; the calendar id with -3- counts as used number 3 only


def test_aufbau_whitelist_semantics(monkeypatch):
    runner = DailyRunner.__new__(DailyRunner)
    runner.s = type("S", (), {"aufbau": {"available": ["Z"]}})()
    built = [{"kuerzel": "A", "gebaut": True, "themen_declared": True, "themen": [33, {"nr": 47, "quellen": [{"url": "https://x"}], "hinweis": "h"}]},
             {"kuerzel": "B", "gebaut": True, "themen_declared": True, "themen": []},
             {"kuerzel": "C", "gebaut": True, "themen_declared": False, "themen": []}]
    opts = DailyRunner._aufbau_options(runner, built, built, "47")
    assert [o["kuerzel"] for o in opts] == ["A", "C"] and opts[0]["quellen"][0]["url"] == "https://x" and opts[0]["hinweis"] == "h"
    assert [o["kuerzel"] for o in DailyRunner._aufbau_options(runner, built, built, "99")] == ["C"]
    only_listed = [built[0], built[1]]
    assert DailyRunner._aufbau_options(runner, only_listed, only_listed, "99") == []             # Scutoria/Revlore: not listed -> "braucht Modell"
    assert [o["kuerzel"] for o in DailyRunner._aufbau_options(runner, [], [], "1")] == ["Z"]      # no aufbauten.yaml: config letters


def test_example_excerpt_keeps_requested_layout_blocks():
    beats = [{"id": f"b{i}", "function": "hook" if i == 1 else "insight", "scene_type": "x", "spoken": "s", "data": {}, "overlay": {}} for i in range(1, 8)]
    plan = {"video_id": "v", "beats": beats, "hook_candidates": [{"id": f"H{i}", "type": "t", "why": {"a": "x" * 200}} for i in range(1, 6)],
            "hook": {"id": "H1"}, "sources": [{"id": "S1"}, {"id": "S2"}], "unverified": ["a", "b", "c"],
            "layout": {"model3d": {"objects": ["o" * 100] * 20}, "media": [1, 2, 3, 4], "sound_cues": list(range(10))}}
    short = context.shorten_plan(plan, 2)
    assert len(short["beats"]) == 4 and len(short["sources"]) == 1 and len(short["unverified"]) == 1
    assert "…" in short["layout"]["model3d"] and len(short["layout"]["media"]) == 3
    kept = context.shorten_plan(plan, 2, ("model3d", "media"))
    assert len(kept["layout"]["model3d"]["objects"]) == 20 and len(kept["layout"]["media"]) == 4
    json.dumps(kept)                                                                                # still serialisable
