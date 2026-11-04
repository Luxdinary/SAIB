# Shared design system (9:16, 1080 x 1920)

Proposal by Claude, 2026-10-30, for all nine brands. Brand-specific values (palette, fonts, motif, tempo, captions, intro, outro, voices) live in `brands/<id>/`. The layout below is identical for every brand so that the production chain (`src/fn/render/compose.py`) can render any brand from the same template.

## Zones (pixels from the top-left corner)

| Zone | Box | Purpose |
|---|---|---|
| Action-safe | 54..1026 x 96..1824 (90 %) | nothing important outside |
| Title-safe | 108..972 x 192..1728 (80 %) | all text, captions, logo |
| Logo | x 72, y 120, height 56 | wordmark top-left (accent mark + name) |
| Counter | right-aligned at x 1008, y 120 | scene counter `2/4` or progress dots |
| Main scene | y 300..1150 | headline, visual placeholder or image, one fact |
| Progress bar | y 1168, height 6, x 108..972 | scaleX over the video length |
| Captions | bottom anchor at y 1280 (640 px from the bottom), max width 900 | 2-4 word groups, one at a time |
| AI label | y 1770 (150 px from the bottom), 26 px | `KI-generiert` / `AI-generated`, always visible |
| Platform UI (avoid) | x > 940 for y 1100..1700; y > 1620 | TikTok side icons and caption area |

## Timeline of a 75-second video

| Segment | Time | Content |
|---|---|---|
| Intro | 0 .. 1.2-2.0 s (brand `intro_config.seconds`) | wordmark animation centered, then wordmark lands top-left |
| Art. 50 disclosure | 0 .. 2.5 s, only where `intro_config.art50_disclosure.enabled` | text card over the intro |
| Hook | intro end .. ~5 s | one headline, strong visual |
| Scenes | 5 .. ~68 s | one idea per scene, 6-12 s, scene counter updates |
| Payoff | ~68 .. 71 s | the one thing to remember |
| Outro | last 4 s | wordmark centered, CTA, AI label |

Captions run from the first spoken word to the last; the voice track starts at the intro end.

## Type scale

| Role | Size | Weight |
|---|---|---|
| Hook headline | 96 px | display weight |
| Scene headline | 72 px | display weight |
| Fact / body | 44 px | 400-600 |
| Captions | brand `subtitle_style.font_size_px` (56-74), minimum 42 | brand weight |
| Counter, source label | 30 px | 500, muted colour |
| AI label | 26 px | 500, muted colour |

## Motion rules

- Every animation is a function of timeline time (GSAP, paused root timeline, registered on `window.__timelines`).
- Children animate, never the `.clip` itself. Transforms, not `left/top/width/height`.
- Scene enter: 0.25 s (snappy brands 0.18 s, slow brands 0.4 s). Scene exit: 0.15 s fade.
- Caption groups: fade-up 0.12 s, hard kill at the group end.
- No `repeat: -1`, no timers, no randomness.

## Fonts

All faces under the SIL Open Font License 1.1, files and `OFL.txt` in `assets/fonts/<family>/`: Inter, Montserrat, JetBrains Mono, Playfair Display, Oswald. Projects embed them with `@font-face` under the family names `FN Inter`, `FN Montserrat`, `FN JetBrains Mono`, `FN Playfair Display`, `FN Oswald`, so renders never fetch fonts from the network.

## Placeholders (Phase 1)

Visuals are shapes, lines and panels in the brand palette, drawn in CSS/SVG by motif. Phase 2 replaces them with generated stills from `image_prompt.md`; Phase 3 adds an 8-second AI clip for the hook.
