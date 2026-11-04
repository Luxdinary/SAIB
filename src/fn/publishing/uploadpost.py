"""Upload-Post adapter (Phase 2). Same interface as the mock; every network call is behind dry_run=False
and needs UPLOADPOST_API_KEY in .env. Endpoints and parameters follow docs.upload-post.com (read 2026-10-29);
anything else is marked NOT_VERIFIED and raises instead of guessing.

Verified (Faktencheck 2026-10-29): POST /api/upload (multipart), scheduled_date, AI labels is_aigc /
is_ai_generated / containsSyntheticMedia, commercial flags, status by request_id, analytics per profile,
MCP server https://mcp.upload-post.com/mcp, rate limits TikTok 15 / Instagram 50 / YouTube 30 per day.
Exact paths of the status, profiles and analytics endpoints must be confirmed against the docs before the
first real call; until then the methods raise NotVerifiedError.
"""
from __future__ import annotations

from pathlib import Path

from ..config import env, has_secret
from .base import PublishRequest, PublishResponse, validate_request

BASE_URL = "https://api.upload-post.com"
UPLOAD_PATH = "/api/upload"                     # verified
PROFILES_PATH = "/api/uploadposts/users"        # NOT_VERIFIED - confirm in docs before use
STATUS_PATH = "/api/uploadposts/status"         # NOT_VERIFIED - confirm in docs before use
ANALYTICS_PATH = "/api/analytics"               # NOT_VERIFIED - confirm in docs before use


class NotVerifiedError(RuntimeError):
    pass


class UploadPostPublisher:
    name = "upload-post"

    def __init__(self, dry_run: bool = True, timeout: int = 120):
        self.dry_run = dry_run
        self.timeout = timeout

    def _headers(self) -> dict:
        key = env("UPLOADPOST_API_KEY")
        if not key:
            raise RuntimeError("UPLOADPOST_API_KEY missing in .env")
        return {"Authorization": f"ApiKey {key}"}

    def connection_test(self) -> dict:
        return {"ok": has_secret("UPLOADPOST_API_KEY"), "provider": "upload-post", "dry_run": self.dry_run,
                "note": "key presence only; no request sent"}

    def profiles(self) -> list[dict]:
        if self.dry_run:
            return []
        raise NotVerifiedError("profiles endpoint path not verified against docs.upload-post.com")

    def schedule(self, request: PublishRequest) -> PublishResponse:
        problems = validate_request(request)
        if problems:
            return PublishResponse(ok=False, request_id=None, status="failed", platform=request.platform,
                                   external_id=request.external_id, message="; ".join(problems))
        payload = request.to_payload()
        files = {"video": Path(request.video_path).name}
        if self.dry_run:
            return PublishResponse(ok=True, request_id=None, status="dry_run", platform=request.platform,
                                   external_id=request.external_id, message="dry run: would POST /api/upload",
                                   raw={"url": BASE_URL + UPLOAD_PATH, "payload": payload, "files": files})
        import requests  # local import: only needed for real calls

        data = {
            "user": request.profile,
            "platform[]": request.platform,
            "title": request.title,
            "description": request.description + ("\n\n" + " ".join("#" + h.lstrip("#") for h in request.hashtags) if request.hashtags else ""),
            "scheduled_date": request.scheduled_date,
            "privacy_level": request.privacy_level,
            "is_aigc": str(request.is_aigc).lower(),
            "is_ai_generated": str(request.is_ai_generated).lower(),
            "containsSyntheticMedia": str(request.containsSyntheticMedia).lower(),
            "brand_content_toggle": str(request.brand_content_toggle).lower(),
            "brand_organic_toggle": str(request.brand_organic_toggle).lower(),
            "hasPaidProductPlacement": str(request.hasPaidProductPlacement).lower(),
        }
        with open(request.video_path, "rb") as fh:
            resp = requests.post(BASE_URL + UPLOAD_PATH, headers=self._headers(), data=data,
                                 files={"video": (Path(request.video_path).name, fh, "video/mp4")}, timeout=self.timeout)
        try:
            body = resp.json()
        except ValueError:
            body = {"text": resp.text[:500]}
        ok = resp.status_code in (200, 201, 202)
        rid = body.get("request_id") or body.get("job_id")
        return PublishResponse(ok=ok, request_id=rid, status="scheduled" if ok else "failed", platform=request.platform,
                               external_id=request.external_id, message=f"HTTP {resp.status_code}", raw=body)

    def status(self, request_id: str) -> dict:
        raise NotVerifiedError("status endpoint path not verified against docs.upload-post.com")

    def unschedule(self, request_id: str) -> dict:
        raise NotVerifiedError("unschedule endpoint not verified against docs.upload-post.com")

    def analytics(self, profile: str) -> dict:
        raise NotVerifiedError("analytics endpoint path not verified against docs.upload-post.com")
