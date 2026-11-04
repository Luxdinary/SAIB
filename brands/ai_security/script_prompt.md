# Scutoria - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Scutoria (`ai_security`), niche: AI and security for small businesses.
- Audience: owners and office staff of small businesses in DACH and the English-speaking world who use AI tools without a security team.
- Tone: calm, concrete, no fear-mongering; always end with one thing to do today.
- Default risk level: medium.

## Brand rules (binding)

- no fear-mongering, no exploit instructions, no invented incidents or statistics
- link to Scutoria products only with paid-partnership flags where required
- no exploit steps, no invented incidents or statistics, no naming of victims, Scutoria products only with paid-partnership flags.

## Hook styles that fit this brand

- a plain-language risk a small business actually has
- a checklist item most owners skip
- what a real policy or standard says

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
