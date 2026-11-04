# Script writer

Write the German script for one topic. Inputs: calendar row, the research block (sources), and the brand prompt
`brands/<brand_id>/script_prompt.md` (audience, tone, structure, hook styles, forbidden things). Use only facts
from the research block. Anything else is written as `UNVERIFIED: ...` and blocks production.

Length: 65-90 seconds spoken, target 75 s. German: 170-210 words. English: 180-230 words.
Spoken sentences short (max 18 words), no lists read aloud, no "in diesem Video".
Every scene with a fact ends with its source marker `[S1]`. The hook and the payoff may carry no marker only if
they contain no checkable claim.

File format (`data/scripts/<topic_id>-<lang>.md`):

```markdown
---
topic_id: ai_security-20261105-1
brand_id: ai_security
language: de
title: Was ein KI-Tool über deinen Betrieb weiß          # <= 100 characters
description: Eine Regel für Eingaben in KI-Tools, die mehr schützt als Software.
hashtags: [kisicherheit, kleinunternehmen, datenschutz]
risk_level: medium
sources:
  - id: S1
    url: https://...
    title: ...
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Gesprochener Text des Hooks.
> visual: headline="Kurze Schlagzeile" kind="hook"

## Scene 2 (card)
Gesprochener Text mit einer Tatsache. [S1]
> visual: headline="..." body="..." number="3" kind="fact"

## Scene 3 (code)
...
> visual: headline="..." code="$ claude|> /init|CLAUDE.md written" kind="code"

## Scene 5 (payoff)
Die eine Sache zum Mitnehmen. Dann die CTA-Zeile aus outro_config.json, natürlich gesprochen.
> visual: headline="..." kind="payoff"
```

`visual` keys: headline (<= 60 characters), body (<= 110), number (a big numeral), code (lines separated by `|`),
kind (hook | card | fact | code | payoff), source (overrides the auto label). Four to six scenes.

After writing: `python -m fn.cli script check <file>` must print `ok`.
