import pytest

from fn.state import TransitionError


def test_main_flow_and_idempotency(tmp_db):
    db = tmp_db
    assert db.upsert_planned("v1", "t1", "ai_security", "de") == "PLANNED"
    assert db.upsert_planned("v1", "t1", "ai_security", "de") == "PLANNED"  # idempotent create
    for s in ["RESEARCHED", "SCRIPTED", "RENDERED", "VALIDATED"]:
        assert db.transition("v1", s, "module") == s
    assert db.transition("v1", "VALIDATED", "module") == "VALIDATED"  # re-apply is a no-op
    assert db.transition("v1", "APPROVED", "auto_approval") == "APPROVED"
    hist = db.history("v1")
    assert [h["to_state"] for h in hist] == ["PLANNED", "RESEARCHED", "SCRIPTED", "RENDERED", "VALIDATED", "APPROVED"]
    assert all(h["at"] for h in hist)


def test_approved_only_by_auto_approval_or_stefan(tmp_db):
    db = tmp_db
    db.upsert_planned("v2", "t2", "ai_security", "de")
    for s in ["RESEARCHED", "SCRIPTED", "RENDERED", "VALIDATED"]:
        db.transition("v2", s, "module")
    with pytest.raises(TransitionError):
        db.transition("v2", "APPROVED", "claude")
    assert db.transition("v2", "APPROVED", "stefan") == "APPROVED"


def test_illegal_transition_and_side_states(tmp_db):
    db = tmp_db
    db.upsert_planned("v3", "t3", "ai_security", "de")
    with pytest.raises(TransitionError):
        db.transition("v3", "PUBLISHED", "module")
    assert db.transition("v3", "NEEDS_RESEARCH", "script_writer", "no source") == "NEEDS_RESEARCH"
    assert db.transition("v3", "RESEARCHED", "research") == "RESEARCHED"
    assert db.transition("v3", "SCRIPTED", "script_writer") == "SCRIPTED"
    assert db.transition("v3", "FAILED", "pipeline", "render crashed") == "FAILED"
    assert db.transition("v3", "SCRIPTED", "pipeline", "retry") == "SCRIPTED"
    assert db.counts() == {"SCRIPTED": 1}


def test_publish_request_idempotency_record(tmp_db):
    db = tmp_db
    db.upsert_planned("v4", "t4", "ai_security", "de")
    db.record_publish_request("v4", "tiktok", "v4:tiktok", "scheduled", "req-1")
    r = db.publish_request("v4", "tiktok")
    assert r["request_id"] == "req-1" and r["status"] == "scheduled"
    assert db.publish_request("v4", "youtube") is None
