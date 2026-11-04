# Frontlore - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Frontlore (`military_history`), niche: military technology and history (historical, publicly documented only).
- Audience: history and technology viewers; strictly historical and publicly documented.
- Tone: measured, factual, respectful; no glorification.
- Default risk level: high.

## Brand rules (binding)

- historical and technical only; no tactics, no weapon handling or construction, no current conflicts
- nothing from Stefan's service, no uniform, no unit references
- realistic AI scenes of real events require Art. 50 disclosure at the start; prefer stylized visuals
- no graphic violence (not ad-eligible on YouTube; FYF-ineligible on TikTok)
- no tactics, no weapon handling or construction, no current conflicts, nothing from Stefan's service, no uniform, no graphic violence; realistic AI scenes of real events need the Art. 50 disclosure at the start, so prefer stylized visuals.

## Hook styles that fit this brand

- a documented technical decision and its consequence
- a date and a number from an archive
- why a design looked the way it did

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
