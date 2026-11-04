# Suitwerk - Script prompt

Used by Claude Code (skill `script-writer`) together with `prompts/script_writer.md`. The brand part is below; the shared part (format, sources, UNVERIFIED rule) is in `prompts/`.

## Brand

- Name: Suitwerk (`menswear`), niche: suits and menswear.
- Audience: men who want to dress well without following trends; international and DACH.
- Tone: composed, knowledgeable, never snobbish; short sentences.
- Default risk level: low.

## Brand rules (binding)

- affiliate links only with product knowledge and disclosure
- no affiliate link without product knowledge and disclosure, no body shaming, no brand ranking without criteria.

## Hook styles that fit this brand

- one rule and the exception
- what a detail says about a suit
- a mistake that is easy to fix

## Structure for 65-90 seconds (target 75 s, 170-210 words in German, 180-230 in English)

1. Hook (0-4 s): one sentence, no "in this video".
2. Setup (4-15 s): why it matters for this audience.
3. Body (15-65 s): three to four points, each with one fact that has a source id `[S1]`, `[S2]`.
4. Payoff (65-72 s): the one thing to remember or do.
5. Outro line (last 3 s): the CTA from `outro_config.json`, spoken naturally.

## Output

Return the script in the format of `prompts/script_writer.md` (front matter with `topic_id`, `brand_id`, `language`, `risk_level`, `sources`; then scenes). Any claim without a source is written as `UNVERIFIED: ...` and blocks production.
