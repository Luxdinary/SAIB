# Frontlore - Visual style (documentary_tech)

Proposal by Claude, 2026-10-30. Shared 9:16 layout (1080 x 1920) from `docs/design-system.md`; this file holds only what is brand-specific.

## Look in one line

documentary tech, olive green, paper grain, contour map lines, archive labels with dates in monospace, stylized diagrams, never photorealistic battle scenes.

## Palette

| Role | Hex | Use |
|---|---|---|
| bg | `#29352D` | full-frame background |
| surface | `#38433C` | cards, code panels, caption scrim |
| accent | `#A9B29F` | highlight word in captions, progress bar, logo mark, lines |
| text | `#E6E9E5` | headlines and body |
| muted | `#919892` | counters, dates, secondary labels |

Scheme: dark. Contrast of text on bg must stay above 4.5:1 (checked by `npx hyperframes check`).

## Type

- Display: **Oswald** 500 (headlines, hook card, outro).
- Body: **Inter** 400-600 (facts, labels).
- Mono: **JetBrains Mono** (code, dates, measurements).
- All fonts under SIL OFL 1.1, files and licences in `assets/fonts/`.

## Motion

Tempo: **measured**. Motif: **archive-stamp**. Background pattern: **map-contours**.

- Intro: archive-stamp (2.0 s), wordmark lands top-left.
- Scenes: one idea per scene, 6-12 s each, hard cuts or 0.25 s crossfades, no transition zoo.
- Captions: Inter 600, none, 4 words per group, style `highlight-word`.
- Outro: logo centered, CTA, AI label, 4 s.

## Imagery

documentary tech, olive green, paper grain, contour map lines, archive labels with dates in monospace, stylized diagrams, never photorealistic battle scenes. Generated images follow `image_prompt.md`; placeholders in Phase 1 are shapes and gradients in the palette.

## Never

no tactics, no weapon handling or construction, no current conflicts, nothing from Stefan's service, no uniform, no graphic violence; realistic AI scenes of real events need the Art. 50 disclosure at the start, so prefer stylized visuals.
