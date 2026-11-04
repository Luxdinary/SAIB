---
name: research-factcheck
description: Verify every fact for one topic against primary sources before a script is written.
---

# research-factcheck

Follow `prompts/research_factcheck.md`. Output the YAML sources block. Decision `needs_research` means the topic stays out of production.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
