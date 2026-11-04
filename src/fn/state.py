"""SQLite state machine for videos: PLANNED -> ... -> VERIFIED plus side states.

Transitions are only allowed along ALLOWED; every transition is idempotent (re-applying the
current state is a no-op) and timestamped in the `transitions` table.
"""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from .config import DATA_DIR

MAIN_FLOW = ["PLANNED", "RESEARCHED", "SCRIPTED", "RENDERED", "VALIDATED", "APPROVED", "SCHEDULED", "PUBLISHED", "VERIFIED"]
SIDE_STATES = ["NEEDS_RESEARCH", "BLOCKED", "HUMAN_REVIEW", "REJECTED", "FAILED"]
ALL_STATES = MAIN_FLOW + SIDE_STATES

ALLOWED: dict[str, set[str]] = {
    "PLANNED": {"RESEARCHED", "NEEDS_RESEARCH", "REJECTED", "FAILED"},
    "NEEDS_RESEARCH": {"RESEARCHED", "REJECTED"},
    "RESEARCHED": {"SCRIPTED", "NEEDS_RESEARCH", "BLOCKED", "REJECTED", "FAILED"},
    "SCRIPTED": {"RENDERED", "NEEDS_RESEARCH", "BLOCKED", "FAILED", "REJECTED"},
    "RENDERED": {"VALIDATED", "FAILED", "BLOCKED", "HUMAN_REVIEW", "SCRIPTED"},
    "VALIDATED": {"APPROVED", "HUMAN_REVIEW", "REJECTED", "FAILED", "SCRIPTED"},
    "HUMAN_REVIEW": {"APPROVED", "REJECTED", "SCRIPTED"},   # SCRIPTED = re-produce before review
    "BLOCKED": {"SCRIPTED", "REJECTED"},
    "APPROVED": {"SCHEDULED", "REJECTED", "FAILED"},
    "SCHEDULED": {"PUBLISHED", "FAILED", "REJECTED"},
    "PUBLISHED": {"VERIFIED", "FAILED"},
    "VERIFIED": set(),
    "REJECTED": set(),
    "FAILED": {"SCRIPTED", "RENDERED", "APPROVED", "REJECTED"},   # retry from the step that failed
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
  video_id TEXT PRIMARY KEY,
  topic_id TEXT NOT NULL,
  brand_id TEXT NOT NULL,
  language TEXT NOT NULL,
  state TEXT NOT NULL,
  risk_level TEXT NOT NULL DEFAULT 'low',
  publish_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  meta TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS transitions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id TEXT NOT NULL,
  from_state TEXT,
  to_state TEXT NOT NULL,
  actor TEXT NOT NULL,
  reason TEXT,
  at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS publish_requests (
  video_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  request_id TEXT,
  external_id TEXT NOT NULL,
  status TEXT NOT NULL,
  response TEXT,
  at TEXT NOT NULL,
  PRIMARY KEY (video_id, platform)
);
CREATE INDEX IF NOT EXISTS idx_videos_state ON videos(state);
"""


class TransitionError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class StateDB:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else DATA_DIR / "state.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(str(self.path), timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # -- videos ---------------------------------------------------------------
    def upsert_planned(self, video_id: str, topic_id: str, brand_id: str, language: str,
                       risk_level: str = "low", publish_at: str | None = None, meta: dict | None = None) -> str:
        """Create the video in PLANNED if it does not exist. Returns the current state."""
        with self._conn() as c:
            row = c.execute("SELECT state FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if row:
                return row["state"]
            ts = now_iso()
            c.execute("INSERT INTO videos VALUES (?,?,?,?,?,?,?,?,?,?)",
                      (video_id, topic_id, brand_id, language, "PLANNED", risk_level, publish_at, ts, ts, json.dumps(meta or {})))
            c.execute("INSERT INTO transitions (video_id, from_state, to_state, actor, reason, at) VALUES (?,?,?,?,?,?)",
                      (video_id, None, "PLANNED", "scheduler", "created", ts))
            return "PLANNED"

    def get(self, video_id: str) -> dict | None:
        with self._conn() as c:
            row = c.execute("SELECT * FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if not row:
                return None
            d = dict(row)
            d["meta"] = json.loads(d["meta"] or "{}")
            return d

    def state(self, video_id: str) -> str | None:
        v = self.get(video_id)
        return v["state"] if v else None

    def transition(self, video_id: str, to_state: str, actor: str, reason: str = "", meta_update: dict | None = None) -> str:
        if to_state not in ALL_STATES:
            raise TransitionError(f"unknown state {to_state}")
        if to_state == "APPROVED" and actor not in ("auto_approval", "stefan"):
            raise TransitionError("APPROVED may only be set by auto_approval (after passed checks) or stefan")
        with self._conn() as c:
            row = c.execute("SELECT state, meta FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if not row:
                raise TransitionError(f"unknown video {video_id}")
            cur = row["state"]
            if cur == to_state:
                return cur  # idempotent
            if to_state not in ALLOWED.get(cur, set()):
                raise TransitionError(f"{video_id}: {cur} -> {to_state} not allowed")
            meta = json.loads(row["meta"] or "{}")
            if meta_update:
                meta.update(meta_update)
            ts = now_iso()
            c.execute("UPDATE videos SET state=?, updated_at=?, meta=? WHERE video_id=?", (to_state, ts, json.dumps(meta), video_id))
            c.execute("INSERT INTO transitions (video_id, from_state, to_state, actor, reason, at) VALUES (?,?,?,?,?,?)",
                      (video_id, cur, to_state, actor, reason, ts))
            return to_state

    def update_meta(self, video_id: str, **fields) -> None:
        with self._conn() as c:
            row = c.execute("SELECT meta FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if not row:
                raise TransitionError(f"unknown video {video_id}")
            meta = json.loads(row["meta"] or "{}")
            meta.update(fields)
            c.execute("UPDATE videos SET meta=?, updated_at=? WHERE video_id=?", (json.dumps(meta), now_iso(), video_id))

    def list(self, state: str | None = None, brand_id: str | None = None) -> list[dict]:
        q, params = "SELECT * FROM videos WHERE 1=1", []
        if state:
            q += " AND state=?"
            params.append(state)
        if brand_id:
            q += " AND brand_id=?"
            params.append(brand_id)
        q += " ORDER BY publish_at, video_id"
        with self._conn() as c:
            rows = c.execute(q, params).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["meta"] = json.loads(d["meta"] or "{}")
            out.append(d)
        return out

    def history(self, video_id: str) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute("SELECT * FROM transitions WHERE video_id=? ORDER BY id", (video_id,)).fetchall()]

    # -- publish requests (idempotency) ---------------------------------------
    def record_publish_request(self, video_id: str, platform: str, external_id: str, status: str,
                               request_id: str | None = None, response: dict | None = None) -> None:
        with self._conn() as c:
            c.execute("INSERT OR REPLACE INTO publish_requests VALUES (?,?,?,?,?,?,?)",
                      (video_id, platform, request_id, external_id, status, json.dumps(response or {}), now_iso()))

    def publish_request(self, video_id: str, platform: str) -> dict | None:
        with self._conn() as c:
            row = c.execute("SELECT * FROM publish_requests WHERE video_id=? AND platform=?", (video_id, platform)).fetchone()
            return dict(row) if row else None

    def counts(self) -> dict[str, int]:
        with self._conn() as c:
            rows = c.execute("SELECT state, COUNT(*) AS n FROM videos GROUP BY state").fetchall()
        return {r["state"]: r["n"] for r in rows}
