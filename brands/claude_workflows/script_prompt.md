# Promptwerk - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Promptwerk (`claude_workflows`), niche: Claude workflows and prompts.
- Audience: people who use Claude or Claude Code for real work and want workflows that provably work.
- Tone: precise, friendly, zero hype; show the steps, name the Claude version.
- Default risk level: low.

## Brand rules (binding)

- real screen recordings from a demo project only, no private data
- every workflow must actually work; note the Claude version used
- no invented features, no screenshots with private data, no promises about model behaviour that was not tested.

## Hook styles that fit this brand

- a concrete result in one sentence
- a mistake everyone makes with Claude
- before/after of a prompt

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
