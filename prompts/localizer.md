# Localizer (DE -> EN)

Produce the English version of a German script as a localisation, not a translation: same scenes, same facts,
same source markers and the same `sources` block; rewrite sentences the way an English-speaking creator in this
niche would say them. Keep the hook punchy, keep numbers and units exactly as in the source (add the imperial
equivalent only when the source gives it). Length 180-230 words. `title`, `description`, `hashtags` localised.
`topic_id` stays, `language: en`, file `data/scripts/<topic_id>-en.md`.

Do not add facts. If a German sentence relies on a DACH-only context (laws, institutions), replace it with the
equivalent fact from the same source or drop the sentence; never invent an English equivalent.
