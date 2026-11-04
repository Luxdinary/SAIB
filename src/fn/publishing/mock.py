"""Mock publisher: same interface as Upload-Post, writes requests to data/publish_mock.jsonl, never uploads."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from ..config import DATA_DIR
from .base import PublishRequest, PublishResponse, validate_request


class MockPublisher:
    name = "mock"

    def __init__(self, dry_run: bool = True, log_path: Path | None = None):
        self.dry_run = dry_run
        self.log_path = Path(log_path) if log_path else DATA_DIR / "publish_mock.jsonl"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._seen: dict[str, str] = {}
        if self.log_path.exists():
            for line in self.log_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    e = json.loads(line)
                    if e.get("request_id"):
                        self._seen[e["external_id"]] = e["request_id"]

    def _log(self, entry: dict) -> None:
        entry["at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def connection_test(self) -> dict:
        return {"ok": True, "provider": "mock", "dry_run": self.dry_run}

    def profiles(self) -> list[dict]:
        return [{"username": "mock-profile", "platforms": ["tiktok", "instagram", "youtube"]}]

    def schedule(self, request: PublishRequest) -> PublishResponse:
        problems = validate_request(request)
        if problems:
            self._log({"event": "rejected", "external_id": request.external_id, "problems": problems})
            return PublishResponse(ok=False, request_id=None, status="failed", platform=request.platform,
                                   external_id=request.external_id, message="; ".join(problems))
        if request.external_id in self._seen:
            rid = self._seen[request.external_id]
            return PublishResponse(ok=True, request_id=rid, status="duplicate", platform=request.platform,
                                   external_id=request.external_id, message="already scheduled (idempotent)")
        if self.dry_run:
            self._log({"event": "dry_run", "external_id": request.external_id, "payload": request.to_payload()})
            return PublishResponse(ok=True, request_id=None, status="dry_run", platform=request.platform,
                                   external_id=request.external_id, message="dry run, nothing sent")
        rid = f"mock-{uuid.uuid4().hex[:12]}"
        self._seen[request.external_id] = rid
        self._log({"event": "scheduled", "external_id": request.external_id, "request_id": rid, "payload": request.to_payload()})
        return PublishResponse(ok=True, request_id=rid, status="scheduled", platform=request.platform,
                               external_id=request.external_id, message="mock scheduled", raw={"request_id": rid})

    def status(self, request_id: str) -> dict:
        known = request_id in self._seen.values()
        return {"request_id": request_id, "status": "scheduled" if known else "unknown", "provider": "mock"}

    def unschedule(self, request_id: str) -> dict:
        for ext, rid in list(self._seen.items()):
            if rid == request_id:
                del self._seen[ext]
                self._log({"event": "unscheduled", "external_id": ext, "request_id": rid})
                return {"ok": True, "request_id": request_id}
        return {"ok": False, "request_id": request_id, "message": "unknown"}

    def analytics(self, profile: str) -> dict:
        return {"profile": profile, "provider": "mock", "views": 0, "followers": 0}
