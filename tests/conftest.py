import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture
def tmp_db(tmp_path):
    from fn.state import StateDB
    return StateDB(tmp_path / "state.db")


@pytest.fixture
def sample_script_text():
    return """---
topic_id: ai_security-20261105-1
brand_id: ai_security
language: de
title: Testtitel
risk_level: medium
sources:
  - id: S1
    url: https://example.org/doc
    title: Example
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Erster Satz des Hooks ohne Behauptung.
> visual: headline="Hook" kind="hook"

## Scene 2 (card)
""" + " ".join(["Wort"] * 150) + """ [S1]
> visual: headline="Karte" body="Text" kind="card"

## Scene 3 (payoff)
Die eine Sache. Folgen.
> visual: headline="Payoff" kind="payoff"
"""
