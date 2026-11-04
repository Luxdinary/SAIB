"""Publisher interface, modelled on the documented Upload-Post upload call (docs.upload-post.com/api/upload-video).

Documented fields used here (read 2026-10-29/30): user (profile), platform[] (tiktok, instagram, youtube), title,
description/caption, scheduled_date (ISO 8601, <= 365 days ahead), privacy_level, is_aigc (TikTok),
is_ai_generated (Instagram), containsSyntheticMedia (YouTube), brand_content_toggle, brand_organic_toggle,
hasPaidProductPlacement, and status by request_id. `external_id` is our own idempotency key and is kept locally
in state.db (whether Upload-Post accepts it as a field is NOT_VERIFIED, so it is never relied on remotely).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Protocol

PLATFORMS = ("tiktok", "instagram", "youtube")
AI_LABEL_FIELDS = {"tiktok": "is_aigc", "instagram": "is_ai_generated", "youtube": "containsSyntheticMedia"}


@dataclass
class PublishRequest:
    video_id: str
    external_id: str                 # idempotency key: "<video_id>:<platform>"
    profile: str                     # Upload-Post profile name (= brand account)
    platform: str
    video_path: str
    title: str
    description: str
    hashtags: list[str]
    scheduled_date: str              # ISO 8601 with offset
    privacy_level: str = "PUBLIC_TO_EVERYONE"
    is_aigc: bool = True
    is_ai_generated: bool = True
    containsSyntheticMedia: bool = True
    brand_content_toggle: bool = False
    brand_organic_toggle: bool = False
    hasPaidProductPlacement: bool = False
    extra: dict = field(default_factory=dict)

    def to_payload(self) -> dict:
        d = asdict(self)
        d.pop("extra", None)
        d.pop("video_id", None)
        return d


@dataclass
class PublishResponse:
    ok: bool
    request_id: str | None
    status: str                      # scheduled | published | failed | dry_run | duplicate
    platform: str
    external_id: str
    message: str = ""
    raw: dict = field(default_factory=dict)


class Publisher(Protocol):
    name: str
    dry_run: bool

    def connection_test(self) -> dict: ...
    def profiles(self) -> list[dict]: ...
    def schedule(self, request: PublishRequest) -> PublishResponse: ...
    def status(self, request_id: str) -> dict: ...
    def unschedule(self, request_id: str) -> dict: ...
    def analytics(self, profile: str) -> dict: ...


def validate_request(req: PublishRequest, *, now: datetime | None = None) -> list[str]:
    problems = []
    if req.platform not in PLATFORMS:
        problems.append(f"unknown platform {req.platform}")
    if not (req.is_aigc and req.is_ai_generated and req.containsSyntheticMedia):
        problems.append("AI labels must all be true (Stefan's rule: label every video)")
    try:
        dt = datetime.fromisoformat(req.scheduled_date)
        if dt.tzinfo is None:
            problems.append("scheduled_date needs a timezone offset")
        else:
            ref = now or datetime.now(dt.tzinfo)
            if (dt - ref).days > 365:
                problems.append("scheduled_date more than 365 days ahead")
    except ValueError:
        problems.append(f"bad scheduled_date {req.scheduled_date}")
    if not req.title.strip():
        problems.append("title empty")
    if req.platform == "youtube" and len(req.title) > 100:
        problems.append("youtube title over 100 chars")
    if not req.external_id or ":" not in req.external_id:
        problems.append("external_id must be <video_id>:<platform>")
    return problems


def build_request(video_id: str, platform: str, profile: str, video_path: str, post: dict, scheduled_date: str) -> PublishRequest:
    p = post.get("platforms", {}).get(platform, {})
    labels = post.get("labels", {})
    return PublishRequest(
        video_id=video_id, external_id=f"{video_id}:{platform}", profile=profile, platform=platform,
        video_path=video_path, title=p.get("title", post.get("title", "")),
        description=p.get("description", post.get("description", "")), hashtags=list(p.get("hashtags", post.get("hashtags", []))),
        scheduled_date=scheduled_date, privacy_level=p.get("privacy_level", "PUBLIC_TO_EVERYONE"),
        is_aigc=bool(labels.get("is_aigc", True)), is_ai_generated=bool(labels.get("is_ai_generated", True)),
        containsSyntheticMedia=bool(labels.get("containsSyntheticMedia", True)),
        brand_content_toggle=bool(post.get("commercial", {}).get("brand_content_toggle", False)),
        brand_organic_toggle=bool(post.get("commercial", {}).get("brand_organic_toggle", False)),
        hasPaidProductPlacement=bool(post.get("commercial", {}).get("hasPaidProductPlacement", False)),
    )
