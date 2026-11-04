"""Publisher adapters. The mock and the Upload-Post adapter share one interface (base.Publisher)."""
from __future__ import annotations

from .base import PublishRequest, PublishResponse, Publisher, build_request  # noqa: F401


def get_publisher(name: str = "mock", *, dry_run: bool = True) -> Publisher:
    if name == "mock":
        from .mock import MockPublisher
        return MockPublisher(dry_run=dry_run)
    if name == "upload-post":
        from .uploadpost import UploadPostPublisher
        return UploadPostPublisher(dry_run=dry_run)
    raise ValueError(f"unknown publisher {name!r}")
