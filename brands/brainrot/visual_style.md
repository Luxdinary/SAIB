# Zonkfruit - Visual style (surreal_3d)

Proposal by Claude, 2026-10-30. Shared 9:16 layout (1080 x 1920) from `docs/design-system.md`; this file holds only what is brand-specific.

## Look in one line

surreal 3D comedy, black background, acid lime accents, hot pink text, wobbling shapes, checkerboard floors, neon outlines, glitch cuts, the original Zonkfruit character (character sheet pending).

## Palette

| Role | Hex | Use |
|---|---|---|
| bg | `#101010` | full-frame background |
| surface | `#212121` | cards, code panels, caption scrim |
| accent | `#B7FF00` | highlight word in captions, progress bar, logo mark, lines |
| text | `#FF43C0` | headlines and body |
| muted | `#932C71` | counters, dates, secondary labels |

Scheme: dark. Contrast of text on bg must stay above 4.5:1 (checked by `npx hyperframes check`).

## Type

- Display: **Montserrat** 900 (headlines, hook card, outro).
- Body: **Montserrat** 400-600 (facts, labels).
- No monospace face.
- All fonts under SIL OFL 1.1, files and licences in `assets/fonts/`.

## Motion

Tempo: **chaotic**. Motif: **neon-wobble**. Background pattern: **checkerboard**.

- Intro: character-bounce (1.2 s), wordmark lands top-left.
- Scenes: one idea per scene, 6-12 s each, hard cuts or 0.25 s crossfades, no transition zoo.
- Captions: Montserrat 900, uppercase, 2 words per group, style `pop-rotate`.
- Outro: logo centered, CTA, AI label, 4 s.

## Imagery

surreal 3D comedy, black background, acid lime accents, hot pink text, wobbling shapes, checkerboard floors, neon outlines, glitch cuts, the original Zonkfruit character (character sheet pending). Generated images follow `image_prompt.md`; placeholders in Phase 1 are shapes and gradients in the palette.

## Never

no copied characters or memes with rights holders, no licensed music without proof, no shock content.
