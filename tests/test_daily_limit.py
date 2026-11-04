"""Revlore rule (Hauptsitzung 03.11.2026): Technik topics first, Motor topics at most every third topic."""
from __future__ import annotations

from fn.daily.topics import limited_allowed


def test_limited_topic_needs_two_unlimited_topics_before_it():
    assert limited_allowed([], 3)                          # nothing produced yet
    assert limited_allowed([False, False], 3)
    assert not limited_allowed([False, True], 3)           # the previous topic was limited
    assert not limited_allowed([True, False], 3)           # the one before the previous was limited
    assert limited_allowed([True, False, False], 3)        # limited topic is two steps back: the third topic may be limited again


def test_pattern_over_a_sequence_is_every_third():
    history: list[bool] = []
    picked: list[bool] = []
    for _ in range(9):                                     # only limited candidates available: every third slot is used
        if limited_allowed(history, 3):
            history.append(True)
            picked.append(True)
        else:
            history.append(False)                          # an unlimited topic takes the slot
            picked.append(False)
    assert picked == [True, False, False] * 3


def test_rule_off_when_every_is_one_or_zero():
    assert limited_allowed([True, True], 1)
    assert limited_allowed([True, True], 0)
