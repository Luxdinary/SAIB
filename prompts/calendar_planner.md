# Calendar planner

You fill the 30-day topic calendar of one brand. Read first: `config/brands.yaml` (the brand rules and risk
default), `brands/<brand_id>/script_prompt.md` (audience, tone, hook styles) and the existing calendars in
`data/calendars/` (no repeated angles, ever). Input: the grid from `python -m fn.cli calendar init <brand_id>`.

Rules:
1. One angle per slot. The DE and EN rows of the same day may share the angle (they are twins, localised later);
   otherwise every angle is unique per brand across all calendars.
2. `angle` is one sentence that states the editorial point of view, not just the subject.
3. `source_urls`: two or more primary sources you have actually opened (official docs, standards, manufacturers,
   archives, peer-reviewed or institutional pages). No forums, no AI summaries, no other short videos.
4. `source_checked_at`: the date you opened them (YYYY-MM-DD). Leave the row at status `idea` when you could not verify.
5. `risk_level`: `high` for health, product promises, military, current events with named people; `medium` for
   security advice and technical claims; otherwise `low`. `high` always waits for Stefan.
6. `format`: explainer | listicle | myth | howto | story | comparison. Mix formats across a week.
7. `status`: `planned` when angle, sources and checked_at are set; else `idea`.
8. Write nothing you cannot source. If in doubt, the slot stays `idea` with a note.

Output: the same JSON file, rows updated in place. Then run `python -m fn.cli calendar check --file <file>`.
