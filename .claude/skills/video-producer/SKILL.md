---
name: video-producer
description: Produce one video end to end from a script (TTS, timings, HyperFrames, NVENC, checks).
---

# video-producer

`python -m fn.cli produce data/scripts/<file>.md [--tts gemini] [--quality draft|looks]`. Check free space first (`fn status`). Result folder in `storage/<stage>/<video_id>/`; read `report.json`.

Rules that apply to every skill here (from CLAUDE.md): no invented facts, every claim with URL and access date,
`UNVERIFIED` blocks production, never set APPROVED, never publish, never enter keys, never delete (move to
`C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`). Answer in German; code and commits in English.
Run Python through `.venv\Scripts\python.exe` with `PYTHONIOENCODING=utf-8`.
