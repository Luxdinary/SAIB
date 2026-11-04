# Scutoria - Visual style (scutoria_brand)

Stand 2026-10-30. Verbindliche Quelle ist das Scutoria-Designsystem in `C:\Users\Stefa\OneDrive\scutoria\design\project\` (`tokens.json` v1, Markenbuch `README.md`, `assets/Logos`, `fonts/`); dort nur lesen, es gilt die dortige `CLAUDE.md`. Kopien hier: `tokens.json`, `assets/logo/`, `assets/fonts/manrope/` (mit Lizenz), `assets/fonts/ibmplexmono/` (OFL-Download vom Google-Fonts-Repository, 2026-10-30). Die frühere Palette (#0B132B/#00D4FF, Cyan, Glow) ist ungültig.

## Look in einem Satz

Ruhig, sachlich, überprüfbar: flacher Midnight-Blue-Grund, das Papierblatt als einziges Licht, ein Akzent (Blau), Bedeutungsfarben nur mit Wort oder Symbol.

## Farben (Thema dark)

| Rolle | Token | Hex | Einsatz im Video |
|---|---|---|---|
| bg | ground | `#0b1120` | Grund, flach; Raster höchstens als Haarlinien |
| surface | surface | `#121b2f` | Karten, Chatfenster, Statusleiste |
| surface_raised | surface-raised | `#19243b` | zweite Ebene in Karten |
| text | ink | `#e9eef8` | Headlines, Text, Untertitel |
| muted | ink-muted | `#a1adc4` | Nebentext, Quellenzeilen, KI-Label |
| hairline | hairline | `rgba(226,232,246,0.12)` | Kartenränder, Raster |
| accent | accent | `#4f8cff` | der eine Akzent: Scutum-Marke, Fakt-Marker, Highlight-Wort, Verbinder |
| button | button | `#2f6be6` | Knopffläche (Text `#ffffff`) |
| signal_amber | signal-amber | `#ffd166` | offene Fragen, Marker „Unsicher", Statusleiste „offen" |
| signal_red | signal-red | `#ff6b6b` | nur die konkrete Sperre des Uploads, Marker „Lücke" |
| signal_green | signal-green | `#2ec4b6` | nur Erfolg / „Geregelt" (im Video nicht verwendet, solange Fragen offen sind) |
| paper / paper_ink | paper / paper-ink | `#fbfbfd` / `#141a24` | das Dokument (Kundenliste), Schatten `shadow-paper` |

Marker (Form plus Wort, nie Farbe allein): Fakt = gefülltes Quadrat in accent, Auslegung = Raute `#b07cff` (sonst nirgends), Unsicher = halber Kreis amber, Lücke = gestrichelter Kreis rot.

## Schrift

- Manrope (variabel 200–800, selbst gehostet) für alles; Headlines 800 mit Laufweite −0,02em, Text 400–700.
- IBM Plex Mono nur für Dateinamen, Statusdaten, Quellenzeilen, Stempel.
- Normale Groß- und Kleinschreibung; Versalien nur im Wortzeichen SCUTORIA (700, Laufweite 0,18em) und in Mono-Stempeln. Keine Ausrufezeichen, keine Emojis, keine Gedankenstrich-Einschübe.
- Abweichung vom Web-Maßstab (gemeldet): Video-Untertitel 56 px (min 42), Headlines 62–84 px, Kartentext 36–40 px, damit Text am Handy lesbar bleibt.

## Logo

Scutum-Marke `assets/logo/scutum-mark.svg` (Strich 1,8, accent) 44 px klein oben links ab dem ersten Frame, daneben SCUTORIA als Text; Schutzraum eine Schildbreite; nie umfärben, füllen, drehen, kein Effekt; kein Logo-Intro, keine Endkarte. Das Schild ist kein Haken-Motiv und steht höchstens einmal als Wasserzeichen unter 5 % hinter einer Szene.

## Bewegung

Kurz und einmalig: Elemente setzen sich einmal (0,4–0,7 s), Linien zeichnen sich einmal (0,5 s), Kamera ruhig (höchstens 2 % Push), Wechsel an Satzgrenzen; nichts blinkt, nichts pulsiert, nichts zählt hoch. Kein Glow, kein Glas, keine Lichtkegel, keine Verläufe.

## Abschluss

In der Handlung (Datei mit blockiertem Upload), `scutoria.com` mindestens 4 s lesbar, Claim „Belegt. Datiert. Vorzeigbar." und klein „Quellenbasiert. Keine Rechtsberatung." in ink-muted; die Pflichtzeile steht zusätzlich im Begleittext (`post.json`).

## Never

Kein Neon, kein Glow, keine Cyan-Palette, keine Haken bei offenen Risikofragen, keine Emojis als Marker, keine URL-Zeilen im Bild (Quellen in `post.json`), kein Kanal-Handle vor der Registrierung.
