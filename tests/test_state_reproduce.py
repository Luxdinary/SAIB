def test_reproduce_from_review_goes_back_to_scripted(tmp_db):
    db = tmp_db
    db.upsert_planned("v9", "t9", "ai_security", "de")
    for s in ["RESEARCHED", "SCRIPTED", "RENDERED", "VALIDATED", "HUMAN_REVIEW"]:
        db.transition("v9", s, "module")
    assert db.transition("v9", "SCRIPTED", "pipeline", "re-produce") == "SCRIPTED"
    assert db.transition("v9", "RENDERED", "video_producer") == "RENDERED"
