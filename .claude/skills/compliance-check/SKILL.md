---
name: compliance-check
description: Review a video folder for sources, licences, AI labels, brand and platform rules.
---

# compliance-check

Follow `prompts/compliance_review.md`. Write `review.md` into the video folder. Only Stefan or the auto-approval module set APPROVED.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
