# Dewlane – Prompt-Blatt KI-Bibliothek (Format „Nahaufnahme“)

Stand 02.11.2026, erstellt von der Dewlane-Sitzung. Grundlage: `Format-Bibel.md` Abschnitt 7. **Nichts davon ist erzeugt.** Erzeugen darf erst die Sitzung „Bibliotheken“ nach Stefans Freigabe des Ausgabeplans (`01 Idee und Strategie\Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md`, Dewlane 120 Credits).

## Zweck

Das Format „Nahaufnahme“ läuft vollständig aus Code. Die Bibliothek ergänzt zwei Dinge, die Code schlecht kann: glaubwürdige **Texturen** (als ruhiger Hintergrund hinter Lupe, Mengen- und Schlussszene) und **neutrale Produktfotos** als Vorlage für die Bühne. Die Clips werden in vielen Folgen wiederverwendet; kein Motiv ist an ein Thema gebunden.

## Feste Regeln für jedes Motiv

- Keine Marken, keine Schrift, keine Logos, keine Etiketten mit Text, keine erkennbaren Verpackungsformen bekannter Hersteller.
- Keine Menschen, keine Gesichter, keine Hände, keine Haut, keine Anwendung am Körper. Nichts, was wie ein Test, Labor, Vorher-nachher oder Messergebnis aussieht (Verordnung (EU) 655/2013).
- Palette der Marke: Elfenbein `#F8F3EF`, Porzellan `#FFFCF9`, Blush `#C98F93`, Mauve `#4A2F34` nur als dunkelster Ton; weiches Tageslicht von oben links, keine harten Schatten, kein Glow, keine Neonfarben.
- Ruhige Bewegung, keine Schnitte, keine Kamerasprünge; Schleifen beginnen und enden im selben Bild.
- Hochformat 9:16. Die mittlere Bildzone (y 290–1100 bei 1080 × 1920) bleibt ruhig und hell genug für Text darüber.

## Teil A: Textur-Schleifen (6 Clips)

Verfahren je Clip (Preise laut Prüfung vom 30.10.2026, vor dem Erzeugen mit `get_cost` neu prüfen): Startbild mit Nano Banana Pro 2k (2 Credits), dann Kling 3.0 Omni Frames pro, 8 s, stumm, mit demselben Bild als Start- und Endbild (10 Credits). Summe je Clip 12 Credits.

| Datei | Motiv | Prompt (Startbild) | Bewegung (Clip) |
|---|---|---|---|
| `dl_tex_cream.mp4` | Cremeschliere | Macro close-up of a soft white cream swirl on an ivory porcelain surface, glossy highlights, gentle peaks, soft daylight from top left, pale blush shadows, minimal, no text, no packaging, no people, 9:16 | the swirl slowly settles and gleams, very slow camera drift, seamless loop |
| `dl_tex_gel.mp4` | Gel | Macro of a clear, slightly blush-tinted gel with tiny suspended air bubbles on an ivory surface, soft daylight, calm, no text, no packaging, no people, 9:16 | bubbles drift upward very slowly, light shimmer, seamless loop |
| `dl_tex_serum.mp4` | Serumtropfen | A single drop of clear golden serum hanging and falling onto a smooth ivory surface, soft ripple, macro, soft daylight, no dropper visible, no text, no people, 9:16 | one drop falls and spreads in slow motion, returns to start frame, seamless loop |
| `dl_tex_foam.mp4` | Schaum | Macro of fine white foam bubbles on ivory, airy, soft daylight from top left, subtle blush reflections, no text, no packaging, no people, 9:16 | bubbles breathe and shift very slowly, seamless loop |
| `dl_tex_film.mp4` | Sonnenschutz-Film | Macro of a thin, even layer of white lotion spread on a smooth matte ivory surface (not skin), soft sheen, a few fine streaks, daylight, no text, no people, 9:16 | the sheen travels slowly across the film, seamless loop |
| `dl_tex_powder.mp4` | Puderwolke | Soft cloud of fine blush-coloured powder settling over an ivory surface, macro, airy, daylight, no compact, no brush, no text, no people, 9:16 | powder drifts and settles very slowly, seamless loop |

Summe Teil A: 6 × 12 = **72 Credits**.

## Teil B: Neutrale Produktfotos (8 Bilder)

Nano Banana Pro 2k, je 2 Credits. Freigestellt auf einheitlichem Elfenbein, damit die Bühne sie wie die Code-Produkte verwenden kann; die Szenen setzen ihr eigenes Etikett (Kategorie, Kennzahl) darüber.

| Datei | Prompt |
|---|---|
| `dl_prod_tube.png` | Studio product photo of a plain, unbranded white cosmetic tube standing on its cap, matte finish, blank label area, on a seamless ivory background, soft daylight from top left, soft shadow, no text, no logo, centered, 9:16 |
| `dl_prod_jar.png` | Studio product photo of a plain, unbranded white porcelain-look cream jar with a pale grey lid, blank, on seamless ivory, soft daylight, soft shadow, no text, no logo, centered, 9:16 |
| `dl_prod_jar_open.png` | Same plain white cream jar with the lid leaning against it, white cream visible inside with a soft swirl, seamless ivory, soft daylight, no text, no logo, 9:16 |
| `dl_prod_dropper.png` | Studio photo of a plain amber glass dropper bottle with a mauve rubber bulb, blank, on seamless ivory, soft daylight, no text, no logo, centered, 9:16 |
| `dl_prod_pump.png` | Studio photo of a plain white pump bottle for lotion, unbranded, blank, seamless ivory background, soft daylight, no text, no logo, centered, 9:16 |
| `dl_prod_spray.png` | Studio photo of a plain white aerosol deodorant can with a pale grey cap, unbranded, blank, seamless ivory, soft daylight, no text, no logo, centered, 9:16 |
| `dl_prod_bottle.png` | Studio photo of a plain white flip-cap bottle for shampoo or body lotion, unbranded, blank, seamless ivory, soft daylight, no text, no logo, centered, 9:16 |
| `dl_prod_group.png` | Group of the plain unbranded white tube, jar, dropper and pump bottle arranged on an ivory plinth, seamless ivory background, soft daylight, gentle shadows, no text, no logo, 9:16 |

Summe Teil B: 8 × 2 = **16 Credits**.

## Summe und Reserve

| Posten | Credits |
|---|---|
| Teil A Textur-Schleifen | 72 |
| Teil B Produktfotos | 16 |
| Reserve für Fehlversuche (fehlgeschlagene Aufträge werden laut Prüfung vom 30.10. erstattet, misslungene nicht) | 32 |
| **Rahmen laut Ausgabeplan** | **120** |

## Ablage und Abnahme

- Ziel: `C:\Automation\faceless-network\brands\beauty\assets\higgsfield\` mit `LICENSE.md` (je Datei eine Zeile `<datei>: Higgsfield, <Modell>, erzeugt <Datum>, Lizenz laut Higgsfield-Tarif Ultra`) und `manifest.json` (Prompt, Modell, Credits, Job-ID).
- Abnahme vor dem Einsatz: kein Text, keine Marke, keine Haut oder Hände im Bild; Schleife ohne sichtbaren Sprung; die Mitte hell genug, dass Mauve-Text darauf WCAG 4,5:1 erreicht (sonst Schleier `scrim` im Plan).
- Kennzeichnung im Video: Szenen mit diesen Motiven bekommen zusätzlich den Hinweis „KI-Bild“; der Stempel „Animation · neutrales Produkt · kein Produkttest“ bleibt.
- Einbau macht danach die Dewlane-Sitzung (LAYER des Formats: Clip unter der Bühne je Szenentyp; Produktfoto statt SVG nur, wenn es neben dem Code-Etikett ruhig wirkt).
