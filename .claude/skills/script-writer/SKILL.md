---
name: script-writer
description: Write the German 65-90 s script for one topic in the brand voice, with source markers.
---

# script-writer

Read `brands/<brand_id>/script_prompt.md` first, then follow `prompts/script_writer.md`. Save to `data/scripts/<topic_id>-de.md` and run `python -m fn.cli script check <file>`.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
