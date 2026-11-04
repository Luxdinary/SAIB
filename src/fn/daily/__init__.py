"""Tagesläufer: automatic daily production per brand over a model API (plan -> voice -> render -> checks -> export).

Modules: settings (config/daily.yaml), topics (Konzeptplan tables, selection), context (brand files, scene docs,
material, calendar sources), prompts, llm (Anthropic / Gemini / mock), validate (plan checks before any cost),
media (derived clips, file resolution), records (ids, state, CSV, Konzeptplan markers), pipeline (orchestration).
Entry point: scripts/daily_runner.py. Documentation: docs/daily-runner.md.
"""
