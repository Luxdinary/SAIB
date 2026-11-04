---
name: calendar-planner
description: Plan the 30-day topic calendar of one brand (angles, sources, risk, slots).
---

# calendar-planner

Follow `prompts/calendar_planner.md`. Create the grid with `python -m fn.cli calendar init <brand_id> --start <date>`, fill the rows, then run `python -m fn.cli calendar check --file <file>` until it prints ok.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
