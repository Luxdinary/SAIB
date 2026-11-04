from fn.costs import CostLogger
from fn.publishing import build_request, get_publisher
from fn.publishing.base import validate_request
from fn.publishing.mock import MockPublisher


def _post():
    return {"brand_id": "ai_security", "title": "T", "description": "D", "hashtags": ["a", "b"],
            "labels": {"is_aigc": True, "is_ai_generated": True, "containsSyntheticMedia": True},
            "commercial": {}, "platforms": {"tiktok": {"title": "T", "description": "D", "hashtags": ["a"]}}}


def test_build_request_sets_all_ai_labels():
    req = build_request("v1", "tiktok", "ai_security", "x.mp4", _post(), "2026-11-05T12:00:00+01:00")
    assert req.is_aigc and req.is_ai_generated and req.containsSyntheticMedia
    assert req.external_id == "v1:tiktok"
    assert validate_request(req) == []
    payload = req.to_payload()
    assert "scheduled_date" in payload and "privacy_level" in payload and "video_id" not in payload


def test_validate_rejects_missing_label_and_far_date():
    req = build_request("v1", "youtube", "p", "x.mp4", _post(), "2026-11-05T12:00:00+01:00")
    req.is_aigc = False
    assert any("AI labels" in p for p in validate_request(req))
    req.is_aigc = True
    req.scheduled_date = "2026-11-05T12:00:00"
    assert any("timezone" in p for p in validate_request(req))


def test_mock_publisher_dry_run_and_idempotent(tmp_path):
    pub = MockPublisher(dry_run=True, log_path=tmp_path / "log.jsonl")
    req = build_request("v1", "tiktok", "p", "x.mp4", _post(), "2026-11-05T12:00:00+01:00")
    r = pub.schedule(req)
    assert r.ok and r.status == "dry_run" and r.request_id is None
    live = MockPublisher(dry_run=False, log_path=tmp_path / "log2.jsonl")
    r1 = live.schedule(req)
    r2 = live.schedule(req)
    assert r1.status == "scheduled" and r2.status == "duplicate" and r1.request_id == r2.request_id
    assert live.status(r1.request_id)["status"] == "scheduled"
    assert live.unschedule(r1.request_id)["ok"]


def test_upload_post_adapter_dry_run_never_calls_network(monkeypatch):
    monkeypatch.delenv("UPLOADPOST_API_KEY", raising=False)
    pub = get_publisher("upload-post", dry_run=True)
    req = build_request("v1", "instagram", "p", "x.mp4", _post(), "2026-11-05T12:00:00+01:00")
    r = pub.schedule(req)
    assert r.status == "dry_run" and r.raw["url"].endswith("/api/upload")


def test_cost_logger_summary(tmp_path):
    c = CostLogger(tmp_path / "costs.jsonl")
    c.log_tts("v1", "gemini", 900, 2000, 75.0)
    c.log_render("v1", 120.0)
    c.log_claude_call("v1", "script")
    s = c.summary("v1")
    assert abs(s["usd_variable"] - 0.02) < 1e-6
    assert s["render_seconds"] == 120.0
    assert s["usd_with_claude_estimate"] > s["usd_variable"]
