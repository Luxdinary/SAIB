# Dewlane - Visual style (luxury_editorial, template 0.9)

Template draft 2026-10-30 (Claude Code only, no Higgsfield). Full template with checklist and ad slots:
`C:\Users\Stefa\OneDrive\Business\02 Marke\Dewlane\Vorlage Dewlane.md`. Shared 9:16 layout from `docs/design-system.md`
and `docs/direction-system.md`; this file holds only what is brand-specific.

## Look in one line

Light luxury editorial: ivory ground, porcelain cards with hairlines, deep mauve serif headlines, product textures as
abstract shapes (dew drop, cream swirl, unbranded flacon silhouette, petals), calm motion. No faces, no skin, no before/after.

## Palette (brand.yaml)

| Role | Hex | Use | Contrast on ivory |
|---|---|---|---|
| bg | `#F8F3EF` | ground | - |
| surface | `#FFFCF9` | cards, status bar | - |
| text | `#4A2F34` | headlines, body, captions | 10.9:1 |
| muted | `#7E6468` | labels, AI label | 4.9:1 |
| accent | `#9B5560` | highlight word, lines, numbers | 4.9:1 |
| blush | `#C98F93` | shapes and clips only, never text | 2.4:1 |
| signal_amber | `#946420` | open question ("Unsicher") | 5.0:1 |
| signal_red | `#8E2F45` | the one stop at the end | 7.8:1 |
| paper / paper_ink | `#FFFFFF` / `#4A2F34` | the INCI label card (red thread) | 11.8:1 |

The Phase-1 draft (accent `#C98F93`, muted `#AB9798`, text `#6C4B50`) failed 4.5:1 for text; it was darkened, the rose stays as blush.

## Type

Playfair Display 500 (headlines, question, wordmark DEWLANE in capitals with 0.18em tracking), Inter 400-600 (body, labels,
captions 56 px weight 600 with an ivory halo). No monospace. All SIL OFL 1.1 (`assets/fonts/`).

## Motion

`flat: true`: no glow, camera at most 2 %, one-time entrances, tempo gentle (0.4 s). Background loops per scene type from
`assets/higgsfield/` (own renders, see LICENSE.md there), scrim 0.3.

## Never

Efficacy claims, before/after, invented tests, AI faces or artificial skin as proof, product or brand recommendations,
medical advice, paid content before a media kit exists.
