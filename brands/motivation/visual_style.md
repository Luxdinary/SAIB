# Gritwerk - Visual style (cinematic_human, Vorlage 0.9)

Binding description: `C:\Users\Stefa\OneDrive\Business\02 Marke\Gritwerk\Vorlage Gritwerk.md` (2026-10-30). Short form for the renderer:

- Cinematic human without AI people: no faces, no silhouettes. The human part is the action: a paper habit card where a day box is ticked.
- Warm near-black ground `#121110` with vignette and static film grain; paper `#F4F0E8` is the only light surface; gold `#E5B45A` is the only accent.
- Recurring object: the habit card (cue, action, day boxes, counter "Tag n"); status bar carries its name.
- Type: Fraunces 700 (OFL) for questions, headlines, card action, counters, wordmark; Inter 500-700 (OFL) for captions and labels.
- Captions in sense groups (max 4 words), normal case, Inter 700 56 px, highlight word gold.
- Logo small top left from frame 1 (gold day box + GRITWERK); no logo intro, no end card; close inside the action (`gritwerk_close`).
- Brand scene types in `scenes.py`: `gritwerk_tracker`, `gritwerk_curve` (always labelled as schematic), `gritwerk_streaks`, `gritwerk_close`; shared `data_flow` and `key_takeaway` pick up the palette (`flat: true`).

Never: psychological or medical claims, guru quotes without source, promises of outcomes, warning colours for normal progress.
