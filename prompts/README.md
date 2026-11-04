# Prompts for the Claude Code steps

Deterministic steps (TTS, Whisper, render, encode, checks, queue, publisher) run in Python without Claude.
Claude Code is used only for the editorial steps below, each with a prompt file and a skill in
`.claude/skills/`. Every prompt enforces: sources with URL and access date, `UNVERIFIED` for anything
without a source, brand rules from `brands/<id>/script_prompt.md`, no invented facts.

| Step | Prompt | Input | Output |
|---|---|---|---|
| Calendar | `calendar_planner.md` | brand, 30-day grid (`fn calendar init`), idea store, past angles | filled `data/calendars/<brand>_<month>.json` |
| Research and fact check | `research_factcheck.md` | one calendar row | sources list with checked_at, risk level, go / NEEDS_RESEARCH |
| Script | `script_writer.md` | calendar row + sources + brand script prompt | `data/scripts/<topic_id>-<lang>.md` |
| Localisation | `localizer.md` | DE script | EN script (localised, same scenes, same sources) |
| Compliance review | `compliance_review.md` | script + manifest + report | review note, HUMAN_REVIEW decision proposal |
