# Gritwerk - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Gritwerk (`motivation`), niche: motivation and self-development.
- Audience: people who want practical self-development, not slogans.
- Tone: warm, direct, grounded; methods are attributed to their sources.
- Default risk level: medium.

## Brand rules (binding)

- no psychological or medical claims; methods with named sources
- no psychological or medical claims, no guru quotes without source, no promises of outcomes.
- every method names its study, textbook or institution; findings are told as "in the study ..." with the study's limits when they change the number (sample size, extrapolation, mean vs median)
- no invented quotes, no celebrity quotes without a documented primary source
- one concrete small action per video (the habit card: cue + action + day boxes); address "du"

## Direction plans (Vorlage Gritwerk 0.9, 2026-10-30)

Direction plans in `data/direction/` follow `OneDrive\Business\02 Marke\Gritwerk\Vorlage Gritwerk.md` and the example
`data/direction/motivation-20261102-2-de.json`: hook `gritwerk_tracker`, then `data_flow`, `gritwerk_curve`, `gritwerk_streaks`,
`key_takeaway`, close `gritwerk_close` (brand scene types in `brands/motivation/scenes.py`). About 160-175 German words give 65-75 s
with the Gemini voice Sulafat. Spoken call to action: "Mehr Methoden mit Quelle: Folge Gritwerk."

## Hook styles that fit this brand

- a named method and where it comes from
- a question the viewer cannot answer quickly
- a small action for today

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
