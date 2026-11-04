# Gigastruct - Script prompt (Vorlage 0.9)

Used by Claude Code together with `prompts/script_writer.md` and the direction system (`docs/direction-system.md`). Output is a direction plan `data/direction/<video_id>.json`; the worked example is `data/direction/megaconstruction-20261105-1-de.json`.

## Brand

- Name: Gigastruct (`megaconstruction`), niche: megaconstructions and construction sites.
- Audience: viewers fascinated by huge structures and the engineering behind them.
- Tone: awe without exaggeration; scale comparisons are computed, never guessed. Address: "du" (only in the call to action).
- Default risk level: low.

## Brand rules (binding)

- Dimensions, dates, quantities only from primary sources (owner, operator, authority, engineering firm, trade press) with URL and access date.
- Every comparison is a calculation: both values sourced, the ratio computed (renderer computes it again from `a.value`/`b.value`), the calculation in `layout.computations`. Choose the wording so it holds under every plausible reading of the source (example: "tons" ambiguous -> "mehr als sieben" holds for metric and short tons).
- Ongoing projects: always "Stand <Monat Jahr>" from the source date; no forecasts as facts; opening dates only if the current primary source states them.
- Only stylised 3D models; inner layouts that the sources do not dimension are drawn schematically and labelled "Querschnitt schematisch".

## Hook styles that fit this brand

- a computed comparison with a twist ("schwerer als 7 Eiffeltürme, und es schwimmt")
- a construction misconception ("wird nicht gebohrt, sondern versenkt")
- a number and what it took ("14 Stunden für ein Bauteil")

## Story (65-90 s, 160-180 German words with the Gemini voice)

Hook (cinematic_hook) -> Problem/Einordnung (key_takeaway items) -> Erklärung (ui_demo = Schnittmodell) -> Demonstration (data_flow = Bauphasen) -> Erkenntnis (comparison) -> Nutzen (key_takeaway items) -> Abschluss (key_takeaway closing, dated status, "Folge Gigastruct").

## Output

A plan JSON with five hook candidates (one per type, truth >= 4), sources S1..Sn, `unverified`, `layout.computations`, `layout.model3d` (objects, anchors, shots; keyframes may use `@Wort` anchors) and beats whose `data` uses `at_word` to sync visual events to the spoken word.
