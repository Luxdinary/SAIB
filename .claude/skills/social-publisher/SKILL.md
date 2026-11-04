---
name: social-publisher
description: Schedule APPROVED videos through the publisher adapter (mock in Phase 1, dry-run).
---

# social-publisher

`python -m fn.cli publish --dry-run [--publisher mock|upload-post]`. Live uploads need Stefan's explicit go, an API key in `.env` and Phase 2 verification of the Upload-Post endpoints.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
