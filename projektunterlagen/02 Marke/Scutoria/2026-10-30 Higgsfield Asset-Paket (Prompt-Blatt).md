# Scutoria – Higgsfield Asset-Paket (Prompt-Blatt für Fassung B)

Von Claude, 30.10.2026. Vorbereitung, nicht ausgeführt: keine Clips erzeugt, keine Kosten. Ziel sind **11 Clips**, die für alle Scutoria-Videos wiederverwendet werden: ein Hintergrund-Loop je Szenentyp (5), ein Hero-Clip für den Hook plus Varianten (4), zwei Übergangs-/Outro-Clips. Logo, Text, Untertitel, Diagramme, Chatfenster und Schalter kommen weiterhin aus dem Renderer; die Clips liefern nur Bildwelt und Bewegung.

Ablage nach dem Erzeugen: `C:\Automation\faceless-network\brands\ai_security\assets\higgsfield\<Dateiname>` plus `LICENSE.md` dort (Higgsfield-Tarif, Datum, Nutzungsrechte, Prompt-Referenz = dieses Blatt). Jeder Clip wird im Manifest des Videos mit Modell, Prompt und Lizenz geführt (Regel: nur Material mit geklärter Lizenz). Alle Clips sind rein abstrakt oder zeigen Geräte ohne Menschen, damit keine Art.-50-Kennzeichnung „realistische Szenen" nötig wird; das KI-Label bleibt wie bisher dauerhaft im Bild.

## Gemeinsame Vorgaben (in jeden Prompt übernehmen)

- **Format:** 9:16 (1080 × 1920 oder höher), 24 oder 30 fps, mindestens 1080p.
- **Farbwelt:** deep navy background #0B132B, cyan accent #00D4FF, soft off-white highlights #F4F7FB; keine weiteren Buntfarben außer einem warmen Amber #FFB020 nur dort, wo genannt.
- **Komposition:** Motiv oben bzw. am Rand, **mittleres Drittel und unteres Drittel frei und ruhig** (dort liegen Headline, Diagramm und Untertitel); keine Details im Bereich y 25–75 %, geringe Helligkeit dort (unter 20 %).
- **Negativ (immer):** text, letters, numbers, captions, watermark, logo, UI, people, faces, hands, hacker hoodie, skull, lock-and-chain cliché, matrix rain, bright white flashes, strobe, lens flare across the center, film grain heavy, fast camera shake, warm orange/yellow except noted amber, low resolution, blurry.
- **Loop:** wo „ja", seamless loop (erstes und letztes Bild identisch, keine Schnitte). Der Renderer kann einen Clip ohne echten Loop über `data-media-start` neu starten; ein Zwischenschnitt bleibt dann sichtbar, deshalb echte Loops bevorzugen.
- **Modellvorschlag:** Higgsfield „Image-to-Video" mit einem vorher erzeugten Standbild (Higgsfield Soul oder ein anderes Bildmodell) ergibt die stabilsten Loops und die beste Farbtreue; „Text-to-Video" nur für den Hero-Clip. Modellnamen und Tarife im Higgsfield-Konto prüfen (Stand hier: NOT_VERIFIED, da kein Zugang).

## Clip-Liste

| # | Dateiname | Zweck (Szenentyp) | Dauer | Loop | Modell |
|---|---|---|---|---|---|
| 1 | `bg_hook_dataroom.mp4` | Hintergrund Cinematic Hook | 8 s | ja | Image-to-Video |
| 2 | `hero_document_to_chat.mp4` | Hero-Clip Hook (hinter dem Chatfenster) | 6 s | nein | Text-to-Video |
| 3 | `bg_flow_lanes.mp4` | Hintergrund Data Flow | 10 s | ja | Image-to-Video |
| 4 | `bg_ui_desk.mp4` | Hintergrund UI Demonstration | 10 s | ja | Image-to-Video |
| 5 | `bg_compare_split.mp4` | Hintergrund Comparison (versus) | 10 s | ja | Image-to-Video |
| 6 | `bg_negate_pulse.mp4` | Hintergrund Comparison (negate) | 8 s | ja | Image-to-Video |
| 7 | `bg_takeaway_calm.mp4` | Hintergrund Key Takeaway und Close | 10 s | ja | Image-to-Video |
| 8 | `hero_shield_assemble.mp4` | Hero-Variante Hook (Sicherheitsthemen) | 6 s | nein | Text-to-Video |
| 9 | `hero_server_corridor.mp4` | Hero-Variante Hook (Cloud/Speicher-Themen) | 6 s | nein | Image-to-Video |
| 10 | `transition_cyan_sweep.mp4` | Übergang zwischen Beats (0,5 s genutzt) | 2 s | nein | Text-to-Video |
| 11 | `bg_outro_orbit.mp4` | Outro-Hintergrund | 6 s | ja | Image-to-Video |

## Prompts

### 1 · `bg_hook_dataroom.mp4` – Hintergrund Cinematic Hook, 8 s, Loop
```
Abstract dark data room, deep navy background #0B132B, thin cyan #00D4FF light lines forming a faint hexagonal grid on the upper fifth of the frame, slow drifting particles like dust in a server room, very subtle depth-of-field bokeh at the top edge, the center and lower two thirds stay almost black and calm, cinematic, slow push-in, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, letters, watermark, logo, UI, people, faces, bright center, lens flare, matrix rain, strobe, orange, warm light.

### 2 · `hero_document_to_chat.mp4` – Hero-Clip Hook, 6 s, kein Loop
```
A single glowing paper document icon made of soft cyan #00D4FF light drifts from the lower left and dissolves into a stream of small particles that flow upward toward the top center of the frame, deep navy #0B132B void, subtle volumetric glow, elegant and calm, no interface, no text on the document, the middle and lower third of the frame remain dark and empty, vertical 9:16, 4K, 24 fps, 6 seconds.
```
Negativ: text, readable characters, logo, hands, people, chat bubbles, phone, laptop screen content, bright flashes, orange.

Verwendung: liegt hinter dem Chatfenster des Renderers; das Fenster bleibt die programmatische Grafik, der Clip liefert die Bewegung „Dokument wandert in die KI".

### 3 · `bg_flow_lanes.mp4` – Hintergrund Data Flow, 10 s, Loop
```
Minimal abstract background, deep navy #0B132B, three faint vertical lanes of slowly moving cyan #00D4FF light pulses traveling top to bottom at the far left and far right edges only, soft glow, slow and rhythmic, the center column of the frame stays dark and empty, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, arrows, icons, diagrams, nodes, boxes, UI, people, bright center, orange.

### 4 · `bg_ui_desk.mp4` – Hintergrund UI Demonstration, 10 s, Loop
```
Out-of-focus dark office desk at night seen from above, deep navy tones #0B132B, a faint cyan #00D4FF screen glow at the top edge, soft bokeh, no visible screen content, nothing recognizable, very slow lateral drift, the center and lower part of the frame are a smooth dark gradient, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, keyboard letters, logos, brand devices, people, hands, bright screen, warm lamp light, orange.

### 5 · `bg_compare_split.mp4` – Hintergrund Comparison (versus), 10 s, Loop
```
Abstract dark background split by a thin horizontal cyan #00D4FF light seam at exactly mid-height, upper half slightly cooler navy, lower half slightly deeper navy #0B132B, faint particles drifting in opposite directions in each half, very subtle, calm, the seam glows softly and breathes slowly, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, icons, checkmarks, crosses, UI, people, bright areas, orange, strobe.

### 6 · `bg_negate_pulse.mp4` – Hintergrund Comparison (negate), 8 s, Loop
```
Deep navy #0B132B void with a slow, faint red-coral #FF6B6B vignette pulse at the extreme edges of the frame only, once every four seconds, the center stays dark and calm, fine cyan #00D4FF dust particles, tense but minimal, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, warning signs, skulls, locks, red flashes in the center, strobe, orange, people.

### 7 · `bg_takeaway_calm.mp4` – Hintergrund Key Takeaway und Close, 10 s, Loop
```
Calm abstract navy #0B132B background with a very slow cyan #00D4FF aurora-like gradient moving along the top edge, soft, clean, premium, no particles, the middle and lower two thirds are a flat dark gradient, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, icons, checklists, UI, people, bright center, orange, grain.

### 8 · `hero_shield_assemble.mp4` – Hero-Variante Hook, 6 s, kein Loop
```
Thin cyan #00D4FF light lines draw and assemble into an abstract shield outline in the upper third of the frame, wireframe style, no fill, no text, no emblem inside, deep navy #0B132B background, gentle glow, the lower two thirds stay dark and empty, cinematic, vertical 9:16, 4K, 24 fps, 6 seconds.
```
Negativ: text, letters, checkmark, logo, metal shield, knight, weapons, people, orange, lens flare.

### 9 · `hero_server_corridor.mp4` – Hero-Variante Hook, 6 s, kein Loop
```
Slow dolly through a dark abstract server corridor, only faint cyan #00D4FF status lights on the upper walls, deep navy #0B132B, strong falloff to black toward the center and bottom of the frame, no labels, no readable panels, calm and clean, vertical 9:16, 4K, 24 fps, 6 seconds.
```
Negativ: text, labels, logos, cables mess, people, bright center, orange, strobe.

### 10 · `transition_cyan_sweep.mp4` – Übergang, 2 s, kein Loop
```
A single soft cyan #00D4FF light sweep moves from the top of the frame to the bottom over a transparent-feeling deep navy #0B132B background, thin, elegant, slightly blurred, nothing else in the frame, vertical 9:16, 4K, 24 fps, 2 seconds.
```
Negativ: text, flash to white, strobe, particles, orange. Verwendung: 0,5 s als Überblendung zwischen Beats (Renderer setzt `mix-blend-mode: screen`).

### 11 · `bg_outro_orbit.mp4` – Outro-Hintergrund, 6 s, Loop
```
Deep navy #0B132B background with a faint cyan #00D4FF ring of light slowly orbiting in the upper third of the frame, minimal, premium, the center of the frame stays empty for a wordmark, lower third dark, seamless loop, vertical 9:16, 4K, 24 fps.
```
Negativ: text, logo, planets, people, bright center, orange.

## Abnahme je Clip (vor der Ablage)

1. Keine Schrift, kein Logo, keine Gesichter im Bild (Bild für Bild bei 1×-Geschwindigkeit).
2. Mittleres und unteres Drittel dunkel genug für weißen Text (Leuchtdichte dort unter 20 %); der Renderer legt zusätzlich einen Verlauf (`scrim`) darüber, aber der Clip soll es nicht nötig machen.
3. Loops ohne sichtbaren Sprung; sonst als „kein Loop" markieren.
4. Datei als MP4 (H.264, 1080 × 1920 oder 2160 × 3840) ablegen, Dateiname wie oben, Eintrag in `LICENSE.md`.

## Wie der Renderer die Clips nutzt (Fassung B, vorbereitet)

- Plan-Datei: Feld `assets` mit `background` je Szenentyp und `hero` für den Hook, z. B.
  `"assets": {"background": {"cinematic_hook": "bg_hook_dataroom.mp4", "data_flow": "bg_flow_lanes.mp4", ...}, "hero": {"b1": "hero_document_to_chat.mp4"}, "transition": "transition_cyan_sweep.mp4"}`.
- Der Director legt je Beat ein `<video class="clip">` mit `data-start`/`data-duration` unter die Szene (Track 0), stumm, `object-fit: cover`, darüber einen dunklen Verlauf; der Hero-Clip liegt im Hook hinter dem Chatfenster. Fehlende Dateien werden gemeldet, nicht stillschweigend weggelassen.
- Lizenznachweis und Modell je Clip wandern in `manifest.json` (`assets`/`licenses`), die Prüfung `license_manifest` bleibt scharf.
