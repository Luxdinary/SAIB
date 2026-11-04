# Scutoria - Image prompt template

For AI-generated stills and clips (Higgsfield and others) and for the placeholder generator. Every generated image is logged in the manifest with model, prompt and licence.

Binding source: the Scutoria design system in `C:\Users\Stefa\OneDrive\scutoria\design\project\` (`tokens.json`, brand book `README.md`) and the Higgsfield prompt sheet, version 2 (`OneDrive\Business\02 Marke\Scutoria\2026-10-30 Higgsfield Asset-Paket (Prompt-Blatt, Fassung 2).md`). Aligned on 2 November 2026; the earlier phase-1 look (navy #0B132B, cyan #00D4FF, hexagonal grid, shield outline) is retired. The previous version of this file is kept in `C:\Users\Stefa\Documents\_zum_loeschen\2026-11-02 Markenpaket Zwischenstand\image_prompt.vorher.md`.

## Base prompt (English, prepend to every scene prompt)

```
Quiet editorial look, flat matte midnight-blue background #0b1120, matte surfaces in #121b2f and #19243b with thin hairline edges in rgba(226,232,246,0.12), one muted blue accent #4f8cff used sparingly, a white paper sheet #fbfbfd as the only light in the room when paper appears. Calm, premium, no glow. Vertical 9:16 composition, subject in the upper two thirds, lower third kept calm and dark for captions (luminance under 15 percent). No text, no letters, no numbers, no logos, no watermarks, no people.
```

## Negative prompt

```
text, letters, numbers, captions, watermark, logo, UI, people, faces, hands, real person, celebrity, uniform, blood, weapon handling, shield, lock, chain, skull, hoodie, matrix rain, cyan, neon, glow, bloom, glass, light rays, god rays, lens flare, bokeh lights, particles, sparks, hexagonal grid, stock photo look, low quality, blurry
```

## Scene prompt pattern

`<what is shown>, <camera or diagram type>, <mood word from tone>` - one subject per image, no collages.

## Rules

- Colours only from the tokens above; signal red #ff6b6b only for a frame or line that marks a risk. Never cyan, never neon.
- The Scutum mark is the brand's only logo and is added in code, never generated. No shield symbols in generated images.
- No realistic depictions of real people, places or events (EU AI Act Art. 50 disclosure would otherwise be required). Prefer stylized, diagrammatic or abstract imagery.
- No exploit steps, no invented incidents or statistics, no naming of victims, Scutoria products only with paid-partnership flags.
