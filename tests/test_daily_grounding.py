"""Daily runner: every number, year and date of the public texts must stand in the evidence."""
from __future__ import annotations

from fn.daily.validate import evidence_digits, spoken_numbers, ungrounded_numbers

EVIDENCE = ("Das BfR hält gesundheitliche Beeinträchtigungen für unwahrscheinlich. Stellungnahme SCCS/1662/23. "
            "Super 100s höchstens 18,75 µm, Super 150s 16,25 µm, je Zehnerstufe 0,5 µm feiner. Element 73.500 t, Eiffelturm 10.100 t. "
            "Stand 20.07.2020.")


def test_numbers_glued_to_letters_are_not_numbers():
    assert spoken_numbers("Super 100s, H4, 50Hz und 18,75 µm, 20. Juli 2020, 73.500 Tonnen") == ["18,75", "20", "2020", "73.500"]


def test_evidence_digits_include_parts_and_joined_forms():
    d = evidence_digits(EVIDENCE)
    assert {"1875", "18", "75", "73500", "20", "07", "2020", "1662", "23"} <= d


def test_invented_date_is_found_but_written_variants_pass():
    texts = {"a": "Die Neubewertung stammt vom 20. Juli 2019.", "b": "Höchstens 18,75 und 16.25 Mikrometer, je Stufe 0,5, Element 73,500 Tonnen.",
             "c": "Zwei Auslöser, 12 Stück, 7 Türme."}
    bad = ungrounded_numbers(texts, EVIDENCE)
    assert bad == [("a", "2019")]                       # '20' stands in the evidence (20.07.2020); only the year is invented


def test_number_without_any_evidence_is_reported():
    assert ungrounded_numbers({"x": "Das kostet 99 Euro und dauert 45 Minuten."}, EVIDENCE) == [("x", "99"), ("x", "45")]
    assert ungrounded_numbers({"x": "Das kostet 99 Euro."}, EVIDENCE + " 99 Euro") == []
