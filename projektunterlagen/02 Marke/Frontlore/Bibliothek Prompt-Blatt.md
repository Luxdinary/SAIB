# Frontlore – Bibliothek Prompt-Blatt (Higgsfield)

Stand: 02.11.2026 (Wien). Wunschliste der Frontlore-Sitzung für die Sitzung „Bibliotheken“, nach `Format-Bibel.md` (Format „Rekonstruktion“, Bildsprache „Kartentisch“). **Nichts davon ist erzeugt, keine Credits ausgegeben.** Budget laut `01 Idee und Strategie\Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md`: 60 Credits, erst nach Stefans Freigabe.

## Wofür die Bilder im Format gebraucht werden

Der Pilot kommt ohne KI-Bilder aus: Grund, Gradnetz, Modelle und Tafeln sind Code. KI-Bilder sollen nur die **Fläche unter dem Linienmodell** reicher machen. Sie sind nie Beleg und nie Inhalt:

- **Tischgründe** ersetzen `assets\bg\base.jpg` (olives Papier) durch echte Textur.
- **Gezeichnete Karten** liegen unter der Aufgabe (`fr_task`) und der künftigen Kartenszene (`fr_map`). Orte, Linien und Beschriftungen setzt weiterhin der Code. Die Karte gilt als **schematisch**: Im Bild steht der Chip „KARTE SCHEMATISCH · KI-ZEICHNUNG“ (gestricheltes Quadrat). Küstenlinien aus einem Bildmodell sind nicht verlässlich und werden nie zum Verorten benutzt.
- **Papierflächen** für das Befundblatt und den Notizzettel.
- **Museums- und Lesesaalgründe** nur unscharf als Hintergrund des Befunds, ohne erkennbare Objekte.

## Grenzen (gelten für jeden Prompt)

- Kein Bild darf wie ein echtes Archivfoto, eine echte Karte aus einem Archiv oder ein echtes Museumsobjekt wirken. Stil immer erkennbar gezeichnet oder als unscharfe Fläche.
- Keine Schrift, keine Zahlen, keine Wappen, Fahnen, Hoheitszeichen, Abzeichen, Uniformen, keine Symbole (Format-Bibel Regel 4). Keine Kompassrose mit Buchstaben.
- Keine Waffen, keine Soldaten, keine Menschen, keine Schiffe oder Fahrzeuge im Einsatz, keine Ruinen von Zerstörung, kein Feuer außer einer neutralen Fackel (nicht nötig, Fackeln zeichnet der Code).
- Palette Frontlore: Olive `#29352D`, Fläche `#38433C`, Linie `#A9B29F`, Papier `#E9E4D4`, Tinte `#1F2620`, Bernstein `#D9B45A` nur sparsam. Kein Glow, keine Lichtkegel, flaches Licht von oben links.
- Format 9:16 (1080 × 1920), Motiv ruhig, Bildmitte zwischen y 440 und 1100 frei von starken Kontrasten (dort liegt das Linienmodell), oben 196–330 ruhig (Zeitlineal, Stellenangabe).

## Wunschliste (Vorschlag: Nano Banana Pro 2k, laut Notiz vom 30.10.2026 2 Credits je Bild; vor dem Auftrag mit `get_cost` prüfen)

| Nr. | Gruppe | Motiv | Bilder |
|---|---|---|---|
| T1–T3 | Tischgrund | Draufsicht auf olivgrünes Leinen oder Filz mit feiner Webstruktur, gleichmäßig, leichte Randabdunklung; Variante 2 mit einem großen, leeren, leicht vergilbten Kartenbogen schräg darauf; Variante 3 dunkler für Schlussszenen | 3 |
| P1–P2 | Papier | leeres, leicht vergilbtes Hadernpapier, Draufsicht, ganz flach, feine Fasern, ein Rand gerissen; Variante 2 Karopapier alt, Linien sehr blass | 2 |
| K1–K8 | Gezeichnete Karten | Federzeichnung im Stil früher gestochener Landkarten, nur Küstenlinie, Gewässer schraffiert, Gelände als feine Schraffur, **ohne Schrift und ohne Zeichen**, einfarbig Tinte auf Papier, dann im Code getönt: K1 Ägäis und Griechenland (Polybios, Hellespont), K2 Britannien und Irland (Hadrianswall, Armada-Feuer, Martello), K3 Ärmelkanal mit beiden Küsten (PLUTO, Mulberry, Wetterprognose 1944), K4 Oberrhein und Alpenvorland (Limes, Rheinbrücke, Neuf-Brisach), K5 Frankreich ganz (Cassini, Chappe), K6 Mitteleuropa mit Donau (Josephinische Landesaufnahme), K7 Finnischer Meerbusen (Suomenlinna), K8 Nordatlantik (Knoten, LORAN) | 8 |
| M1–M3 | Lesesaal und Museum | stark unscharfe Fläche: M1 Archivregale mit Kartons, M2 Lesesaaltisch mit Leselampe von oben, M3 leere Vitrine mit Stoffboden; keine erkennbaren Objekte, keine Schrift | 3 |
| **Summe** | | | **16 Bilder ≈ 32 Credits** |

Probe zuerst (Ausgaberegel 2): T1 und K1, also 2 Bilder ≈ 4 Credits. Rest erst, wenn Stil, Schriftfreiheit und Zeichenfreiheit stimmen. Mit Ausschussfaktor 1,5 rund 48 Credits; 12 Credits Reserve.

## Prompts (englisch, für das Bildmodell)

Gemeinsamer Zusatz für alle: `no text, no letters, no numbers, no symbols, no flags, no coats of arms, no insignia, no people, no weapons, no vehicles, flat even light from top left, no glow, muted olive and paper palette, vertical 9:16`

- **T1:** `top-down view of a plain olive green linen tablecloth, fine woven texture, completely empty, subtle vignette at the edges, colour close to #29352D`
- **T2:** `top-down view of an olive green linen table with one large blank yellowed sheet of old laid paper lying slightly rotated across it, sheet empty, soft paper fibres`
- **T3:** `top-down view of a dark olive felt surface, very even, faint fibres, darker than #29352D, empty`
- **P1:** `flat scan of a blank sheet of old rag paper, slightly yellowed #E9E4D4, fine fibres, one torn edge, empty`
- **P2:** `flat scan of a blank sheet of old squared paper, very pale grid lines, slightly yellowed, empty`
- **K1–K8:** `hand-drawn pen and ink map in the style of an early engraved map, only coastlines, hatched water along the coast, fine hatching for hills, single ink colour on paper, completely without labels, without compass rose, without cartouche, region: <Region>`; Regionen: `the Aegean Sea and mainland Greece`, `Great Britain and Ireland`, `the English Channel with the coasts of England and northern France`, `the Upper Rhine valley and the northern Alpine foothills`, `France`, `Central Europe along the Danube`, `the Gulf of Finland`, `the North Atlantic between Europe and North America`.
- **M1:** `extremely blurred background of archive shelves with plain cardboard boxes, olive and paper tones, nothing recognisable`
- **M2:** `extremely blurred top-down view of a library reading table with a reading lamp, olive and paper tones, nothing recognisable`
- **M3:** `extremely blurred empty museum display case with a fabric base, olive tones, nothing inside`

## Abnahme durch die Frontlore-Sitzung

- Jedes Bild auf Schrift, Zeichen, Menschen, Waffen und Fahnen geprüft (auch angeschnitten); bei Treffer verworfen, nicht retuschiert.
- Karten nur als Fläche; im Video immer mit Chip „KARTE SCHEMATISCH · KI-ZEICHNUNG“.
- Ablage `C:\Automation\faceless-network\brands\military_history\assets\library\` mit `LICENSE.md` (Modell, Job-Nummer, Credits, Prompt, Datum) und Eintrag in `08 Recht und Verwaltung\Lizenzen`.
- Code-Anschluss (noch offen): `LAYER` nimmt `layout.ground` (Tischgrund) und `fr_task`/`fr_map` nehmen `data.map` (Kartenbild unter dem Modell).
