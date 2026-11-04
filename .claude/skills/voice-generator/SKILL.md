---
name: voice-generator
description: Generate the voice track with the configured TTS adapter (mock until a key exists).
---

# voice-generator

The pipeline calls `fn.tts.get_provider()`; Gemini is used only when GEMINI_API_KEY is in `.env` (paid, logged in the cost logger). For a standalone test: `python -c "from fn.tts import get_provider; ..."`. Never print key values.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
