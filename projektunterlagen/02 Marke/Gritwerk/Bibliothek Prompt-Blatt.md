# Gritwerk – Bibliothek Prompt-Blatt (Entwurf)

Stand: 02.11.2026 (Wien). **Gültig für den Kern „Laborbuch“, den Stefan am 02.11.2026 gewählt hat** (`Format-Bibel.md`, Abschnitt 0). Erzeugt wird von der Bibliotheken-Sitzung nach dem Ausgabeplan `01 Idee und Strategie\Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md`. Von der Gritwerk-Sitzung am 02.11.2026 gegen die Format-Bibel 0.2 geprüft: passt, keine Änderung an Motiven oder Budget.

Budget laut Ausgabeplan: **100 Credits**. Angesetzte Preise aus dem Plan: Bild 2 Credits, Video 8 s etwa 10 Credits einschließlich Startbild. Vor jedem Auftrag `get_cost`, Probe zuerst (höchstens 10 Credits), Job-Nummer, Prompt und Kosten in `06 Bibliothek\Gritwerk\LICENSE.md`.

## Wozu Gritwerk überhaupt Bilder braucht

Der Kern des Formats bleibt Code: Laborbuchseite, Punkte, Balken, Stempel. KI-Bilder ersetzen davon nichts. Sie geben nur **Atmosphäre um die Seite** (der Raum, in dem das Laborbuch liegt) und **Material für Thumbnails**. Wo der Code-Hintergrund reicht, wird nichts erzeugt (Regel 4 des Ausgabeplans: Bild vor Video).

## Feste Regeln für jedes Motiv

- **Keine Menschen, keine Hände, keine Gesichter, keine Silhouetten.** Teilnehmende erscheinen im Format nur als Punkte; ein Bild mit Personen könnte wie eine echte Versuchsaufnahme wirken.
- Keine Schrift, keine Zahlen, keine Diagramme im Bild (Zahlen kommen nur aus Quellen und aus dem Code).
- Keine echten Marken, keine Universitäts- oder Zeitschriftenlogos, keine erkennbaren Gebäude.
- Nichts, was wie ein echtes Labor einer bestimmten Einrichtung oder wie ein Dokumentarfoto aussieht; Stil erkennbar als ruhige Illustration bzw. Stimmungsbild.
- Farbwelt der Marke: warmes Dunkel (#121110), Lampenlicht, Papier (#F4F0E8), Gold (#E5B45A) als einziger Akzent.
- 9:16, ruhig, viel Leerraum in der Bildmitte (dort liegt im Video die Laborbuchseite).
- Jedes Bild wird im Video als KI-Darstellung gekennzeichnet (gemeinsame Regel „KI-generiert“).

## Motive

| Nr. | Motiv | Art | Credits | Prompt (Kern, englisch) |
|---|---|---|---|---|
| G1 | Schreibtisch von oben unter Lampenlicht, Mitte frei für die Seite | Bild | 2 | "top-down view of a dark walnut desk at night, warm desk lamp light from upper left, empty center area, a closed graph-paper notebook and a pencil at the edges, soft vignette, no people, no text, calm illustrative photo style, warm gold and near-black palette, 9:16" |
| G2 | Wie G1, leicht schräge Perspektive | Bild | 2 | wie G1, "low angle 30 degrees, shallow depth of field" |
| G3 | Lesesaal unscharf (Bücherregale, Lampen) als Hintergrund für Lern-Themen | Bild | 2 | "blurred reading room at night, rows of bookshelves, warm green-shaded lamps, bokeh, no people, no text, 9:16" |
| G4 | Laborbank neutral (Stoppuhr, Klemmbrett, Becher mit Stiften), unscharf | Bild | 2 | "softly blurred neutral lab bench, analog stopwatch, clipboard with blank paper, cup of pencils, warm lamp light, no people, no logos, no text, 9:16" |
| G5 | Papierstruktur Karopapier, Nahaufnahme | Bild | 2 | "macro texture of cream graph paper with faint blue-grey grid, subtle paper fibers, even light, no text" |
| G6 | Papierstruktur Karteikarte mit Bleistiftspuren (ohne Schrift) | Bild | 2 | "macro texture of a cream index card with faint erased pencil smudges, no readable marks" |
| V1 | Staub im Lampenlicht über dem Schreibtisch, Schleife | Video 8 s | 10 | Startbild G1, "slow drifting dust particles in the lamp light, camera static, seamless loop" |
| V2 | Seite eines Notizbuchs blättert langsam um, Makro | Video 8 s | 10 | "macro shot of a graph-paper notebook page slowly turning by itself in a draft, warm lamp light, no hands, no text" |
| V3 | Analoge Stoppuhr, Zeiger läuft, Makro (für Messung und Zeitpunkte) | Video 8 s | 10 | "macro of an analog stopwatch on a dark desk, second hand moving, warm light, no brand, no text on the dial beyond tick marks" |
| V4 | Lampe geht an, Licht fällt auf das leere Notizbuch (Einstieg) | Video 8 s | 10 | Startbild G2, "desk lamp switches on, warm light spreads over an open blank graph-paper notebook, no hands" |
| T1–T6 | Thumbnail-Hintergründe (G1/G3/G4 als Varianten, Mitte frei für Titel und Stempel) | Bild | 12 | Varianten von G1, G3, G4 mit stärkerem Kontrast |
| | **Summe** | | **74** | |
| | Reserve für Ausschuss (Faktor etwa 1,35) | | 26 | |
| | **Gesamt** | | **100** | |

Probe zuerst: G1 und V1 (12 Credits; knapp über 10 % des Budgets, deshalb G1 allein als Probe, V1 erst nach Sichtprüfung).

## Einsatz im Format

- Die Ebene des Formats (`brands\motivation\laborbuch\scenes.py`, `LAYER`) könnte G1 oder G2 statt des gezeichneten Raums nutzen, unter einem Schleier; V1 als ruhige Schleife. Die Laborbuchseite bleibt Code.
- V2 könnte das gezeichnete Umblättern ersetzen; erst testen, ob es neben der Code-Seite glaubwürdig wirkt. Sonst bleibt das Code-Umblättern.
- V3 nur in Szenen mit Messzeitpunkten (Aufbau, Messung), nie als Behauptung einer echten Messung.

## Offen

- Stefans Entscheidung über den Kern und den Ausgabeplan.
- Ob überhaupt Bewegtbild nötig ist: Der Pilot ist ohne jedes KI-Bild gebaut. Eine Fassung mit G1 und V1 als Hintergrund wäre ein guter Vergleich, bevor der Rest ausgegeben wird.
