# Scutoria – Higgsfield Asset-Paket, Prompt-Blatt Fassung 2

Stand: 30.10.2026, 13:50 (Wien). Ersetzt die Fassung 1 vom selben Tag (gleicher Ordner), deren Farben (#0B132B, Cyan #00D4FF, Glow, Partikel) nicht dem Scutoria-Designsystem entsprachen. Verbindlich sind `C:\Users\Stefa\OneDrive\scutoria\design\project\tokens.json` und `README.md` (nur lesen). Noch kein Clip erzeugt, keine Credits verbraucht; ein Clip in Fassung-1-Farben gilt als nicht verwendbar.

## Verbindliche Gestaltung (in jeden Prompt übernehmen)

- **Farben (Token):** Grund `ground` #0b1120 (Midnight-Blue), Flächen `surface` #121b2f und `surface-raised` #19243b, Haarlinien rgba(226,232,246,0.12), Akzent `accent` #4f8cff (Blau, nie Cyan), Papierblatt `paper` #fbfbfd als einziges Licht im Raum. Bedeutungsfarben nur dort, wo genannt: Amber #ffd166 für offene Fragen, Rot #ff6b6b nur für Sperren, Grün #2ec4b6 nur für Erfolg (im Paket nicht verwendet).
- **Kein** Neon, Glow, Glas, Lichtkegel, Bokeh-Lichter, Partikelnebel, Matrix-Regen, Lens Flare, Weißblitz, Strobe, Körnung; der Grund ist flach und matt.
- **Bewegung** ruhig und einmalig: ein Objekt setzt sich, eine Linie zeichnet sich, eine Fläche hebt sich; nichts blinkt, nichts zählt, nichts springt. Loops atmen nur (langsame Helligkeits- oder Lageänderung unter 2 %).
- **Komposition:** Motiv in der oberen Hälfte oder am Rand; mittleres und unteres Drittel (y 35–100 %) flach und dunkel, Leuchtdichte dort unter 15 %, weil Headline, Diagramm, Untertitel und Statusleiste aus dem Renderer kommen.
- **Verboten im Bild:** Schrift, Buchstaben, Zahlen, Logos, Wasserzeichen, UI-Elemente, Menschen, Gesichter, Hände, Schild-Symbol, Schloss-und-Kette, Totenkopf, Hoodie-Hacker, Marken-Geräte.
- **Format:** 9:16, mindestens 1080 × 1920, 24 oder 30 fps, stumm (`generate_audio` aus).
- **Negativ-Prompt (immer):** text, letters, numbers, captions, watermark, logo, UI, people, faces, hands, shield, lock, chain, skull, hoodie, matrix rain, neon, glow, bloom, glass, light rays, god rays, lens flare, bokeh lights, particles, sparks, bright center, white flash, strobe, film grain, camera shake, cyan, teal, orange, purple, low resolution, blurry.

## Modell und Ablauf (Starter-Tarif)

1. Standbild je Clip mit `nano_banana_pro` (2k, 9:16), Prompt unten.
2. Video aus dem Standbild mit `seedance1_5` (1080p, `generate_audio` false, 9:16): Loops mit demselben Bild als Start- **und** Endbild (8 s oder 12 s), Hero-Clips nur mit Startbild (8 s).
3. Creditbetrag je Auftrag vom Server anzeigen lassen und Stefans Ja abwarten; Abnahme je Clip (unten) vor der Ablage.

## Clip-Liste

| # | Dateiname | Zweck | Dauer | Loop | Stand |
|---|---|---|---|---|---|
| 1 | `bg_hook_dataroom.mp4` | Hintergrund Cinematic Hook | 8 s | ja | Higgsfield |
| 2 | `hero_document_to_chat.mp4` | Hero Hook: Kundenliste nähert sich dem Chat, stoppt | 8 s (genutzt 4,2 s) | nein | Higgsfield, **Qualitätsprobe zuerst** |
| 3 | `bg_flow_lanes.mp4` | Hintergrund Data Flow | 12 s | ja | Higgsfield |
| 4 | `bg_ui_desk.mp4` | Hintergrund UI Demonstration | 12 s | ja | Higgsfield |
| 5 | `bg_compare_split.mp4` | Hintergrund Comparison (versus) | 12 s | ja | Higgsfield |
| 6 | `bg_negate_pulse.mp4` | Hintergrund Comparison (negate) | 8 s | ja | Higgsfield |
| 7 | `bg_takeaway_calm.mp4` | Hintergrund Key Takeaway und Close | 12 s | ja | Higgsfield |
| 8 | `hero_shield_assemble.mp4` | – | – | – | **gestrichen** (kein Schild-Symbol) |
| 9 | `hero_server_corridor.mp4` | Hero-Variante Cloud/Speicher | 8 s | nein | nur bei Restbudget |
| 10 | `transition_cyan_sweep.mp4` | Übergang | – | – | **im Renderer als CSS** (umbenennen in `transition_sweep`), keine Credits |
| 11 | `bg_outro_orbit.mp4` | Outro-Hintergrund | 8 s | ja | Higgsfield |

## Prompts (Standbild; der Video-Prompt steht jeweils darunter)

### 1 · `bg_hook_dataroom.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120, a quiet dark office table surface seen from slightly above filling the upper third, matte surfaces in #121b2f and #19243b with thin hairline edges, one thin horizontal accent line in muted blue #4f8cff along the top edge, no light sources, no glow, the lower two thirds of the frame are a flat uniform #0b1120, vertical 9:16, clean, calm, premium corporate, no text.
```
Video (Start = Endbild, 8 s): `Very slow, barely visible drift of the table surface, the blue hairline brightens and dims once over the whole clip, nothing else moves, seamless loop, no camera shake.`

### 2 · `hero_document_to_chat.mp4` – Qualitätsprobe
Bild (Startbild):
```
A single white paper sheet #fbfbfd in portrait format, slightly rotated by two degrees, resting on a flat matte midnight-blue table #0b1120, soft layered shadow under the sheet, the sheet is blank with only faint grey ruled rows suggesting a spreadsheet (no readable characters), positioned in the lower left quarter of the frame, upper two thirds of the frame empty flat #0b1120, vertical 9:16, calm, corporate, no text.
```
Video (nur Startbild, 8 s): `The paper sheet slides slowly and smoothly from the lower left toward the upper center of the frame, decelerates and stops just below the upper third, settles with a subtle shadow, then holds still; nothing else moves, no glow, no particles.`
Verwendung: liegt hinter dem Chatfenster des Renderers (das Fenster bleibt Codegrafik); das Blatt ist die Kundenliste, die vor dem Upload anhält.

### 3 · `bg_flow_lanes.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120, two thin vertical hairlines in rgba(226,232,246,0.12) at the far left and far right edges, each with one small muted blue #4f8cff segment of about 5 percent height near the top, the whole center column is uniform flat #0b1120, vertical 9:16, minimal, no glow, no text.
```
Video (Start = Endbild, 12 s): `The two small blue segments travel slowly from the top to the bottom of their hairlines at constant speed and reappear at the top, forming a seamless loop; nothing else moves.`

### 4 · `bg_ui_desk.mp4`
Bild:
```
Strongly out-of-focus dark office desk at night from above, matte surfaces in #121b2f and #19243b, the only brighter area is a faint, soft, pale blue-grey rectangle at the very top edge suggesting a screen without any content, no visible devices or brands, no bokeh circles, lower two thirds a smooth flat #0b1120 gradient, vertical 9:16, no text.
```
Video (Start = Endbild, 12 s): `Extremely slow lateral drift of the blurred desk, the pale rectangle brightens and dims once, seamless loop, no camera shake.`

### 5 · `bg_compare_split.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120 divided at exactly mid-height by one thin horizontal hairline in muted blue #4f8cff, upper half a slightly lighter matte #121b2f, lower half #0b1120, no other elements, no glow, vertical 9:16, no text.
```
Video (Start = Endbild, 12 s): `The hairline brightens and dims once, slowly, over the whole clip; nothing else moves; seamless loop.`

### 6 · `bg_negate_pulse.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120 with a very thin solid frame line in signal red #ff6b6b along the outer edges of the image, two pixels wide, nothing else, center uniform #0b1120, vertical 9:16, no glow, no text.
```
Video (Start = Endbild, 8 s): `The red frame line fades in slowly over three seconds and fades out again, once; nothing else moves; seamless loop.`
Regel: Rot nur als Sperre; dieser Hintergrund liegt nur unter dem Beat „Training aus heißt nicht Datenschutz gelöst" (Stempel NEIN).

### 7 · `bg_takeaway_calm.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120, a single matte surface band #121b2f across the top 20 percent of the frame with a hairline bottom edge, below it uniform flat #0b1120, vertical 9:16, calm, premium, no glow, no text.
```
Video (Start = Endbild, 12 s): `The brightness of the band rises and falls once by a barely visible amount; seamless loop; nothing else moves.`

### 9 · `hero_server_corridor.mp4` (optional)
Bild:
```
Dark abstract corridor of matte cabinets in #121b2f and #19243b receding into the distance in the upper half of the frame, small muted blue #4f8cff status points on the cabinet edges, no labels, no readable panels, no glow, strong falloff to flat #0b1120 in the lower half, vertical 9:16, no text.
```
Video (nur Startbild, 8 s): `Slow steady dolly forward through the corridor, no camera shake, the status points stay constant; nothing else moves.`

### 11 · `bg_outro_orbit.mp4`
Bild:
```
Flat matte midnight-blue background #0b1120, one thin circle outline in muted blue #4f8cff, about 30 percent of the frame width, centered in the upper third, hairline weight, no glow, the center and lower part of the frame uniform flat #0b1120, vertical 9:16, no text.
```
Video (Start = Endbild, 8 s): `The circle outline rotates once slowly around its center over the clip (a small gap in the outline makes the rotation visible), seamless loop; nothing else moves.`

## Abnahme je Clip (vor der Ablage)

1. Keine Schrift, kein Logo, kein Gesicht, kein Schild (Bild für Bild bei 1×).
2. Farben: Grund #0b1120 mit Toleranz, Akzent Blau #4f8cff, kein Cyan, kein Glow; mittleres und unteres Drittel Leuchtdichte unter 15 % (per FFmpeg `signalstats` je Drittel messen).
3. Loop ohne sichtbaren Sprung (erstes und letztes Bild vergleichen), sonst als „kein Loop" markieren.
4. MP4 H.264, 1080 × 1920, Dateiname wie oben, Zeile in `LICENSE.md`, Eintrag in `manifest.json` (Modell, Prompt, Job-ID, Credits, Datum, Lizenz).

## Hinweis Renderer

Die Codegrafik in `brands\ai_security\brand.yaml` und `visual_style.md` nutzt noch die Phase-1-Palette (bg #0B132B, Akzent Cyan #00D4FF, Motiv „shield-lines"). Die Angleichung an die Scutoria-Tokens (Grund #0b1120, Akzent #4f8cff, kein Schild) ist eine eigene Entscheidung, weil `brand.yaml` von allen Fassungen (A, A2, B) gelesen wird und die A2-Sitzung gerade damit rendert.
