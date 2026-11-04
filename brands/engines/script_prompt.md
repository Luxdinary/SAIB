# Revlore - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Revlore (`engines`), niche: engine technology.
- Audience: car and motorcycle enthusiasts who want to understand how engines work, not buy parts.
- Tone: exact, sober, engineering language explained; every number has a source.
- Default risk level: medium.

## Brand rules (binding)

- technical claims from manufacturer or engineering sources; no maintenance advice that can cause damage
- no maintenance advice that can damage an engine, no tuning instructions, no brand bashing.

## Hook styles that fit this brand

- a number that sounds wrong but is right (with source)
- why a design choice exists
- what happens inside the engine in one second

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
