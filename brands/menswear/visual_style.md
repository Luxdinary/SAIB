# Suitwerk - Visual style (quiet_luxury)

Updated 2026-10-30 (Vorlage Suitwerk 0.9, Claude Code only). Binding description in German:
`C:\Users\Stefa\OneDrive\Business\02 Marke\Suitwerk\Vorlage Suitwerk.md`.

## Look in one line

Quiet luxury, timeless: one jacket as a clean champagne-gold line illustration on midnight navy is the object
of every scene (brands/menswear/tools/garment.py). No people, no photos, no AI images, no slide layouts.

## Palette

| Role | Hex | Use |
|---|---|---|
| bg | `#172337` | ground with fine 45 degree twill lines (`fabric-gradient`) |
| surface | `#273245` | cards, status bar; jacket cloth `#26344D` with twill pattern |
| accent | `#D4B483` | jacket outlines, highlight word, progress bar, logo, "always" tags |
| text | `#F2EEE6` | headlines and body |
| muted | `#9AA0A8` | sub lines (raised from `#8F9397` for contrast) |
| signal_red | `#C9776B` | risk only: strain lines, "never", marker "Lücke" |
| signal_amber | `#E8A33D` | open/unclear only: "nach Geschmack", status "?", marker "Unsicher" |
| reached | `#8DBE96` | reached state only (green ring in the close); `explainer.colors.erreicht` |
| interpretation | `#A58BE0` | marker "Auslegung" only |

## Explainer layer (since 2026-10-30)

`explainer` block in brand.yaml (fn.render.explainer): voice tag top right, opening line, kicker at y 186, marker capsule
and source bar at `source_y: 1120`. Scenes stay above y 1100 and left of x 930; every time field takes a word anchor
"w:Wort"; `hold_end` / `backdrop` make iris and blende transitions overlap cleanly.

## Type

Playfair Display 600 (headlines, questions, card titles), Inter 400-600 (labels, captions 56 px). SIL OFL 1.1.

## Motion

Tempo slow, `flat: true` (no glow, no light sweep). Jacket lines draw in (stroke), cloth fades in, rings and
leader lines draw, zoom at most 1.6x in the fitting scene, camera push 3-7 %. No logo intro, no end card:
the close puts the mistake right on the jacket.

## Scene types (brands/menswear/scenes.py, brand prefix suitwerk_)

suitwerk_hook (question + jacket draws itself), suitwerk_fitting (pin, zoom, state change), suitwerk_ladder (rule
tags per button), suitwerk_compare (two jackets), suitwerk_takeaway (cards with mini jackets; `mode: closing`).

## Never

No affiliate link without product knowledge and disclosure, no brand names as recommendation, no product
promises, no body shaming, no brand ranking without criteria.
