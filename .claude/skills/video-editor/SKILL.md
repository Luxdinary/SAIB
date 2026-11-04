---
name: video-editor
description: Adjust the look of a rendered video: scenes, captions, layout, brand files.
---

# video-editor

Edit `brands/<id>/*.json|yaml|md` or `src/fn/render/compose.py`, rebuild with `fn produce`, then `npx hyperframes snapshot --at <s>` on the project folder and look at the frames before re-rendering.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
