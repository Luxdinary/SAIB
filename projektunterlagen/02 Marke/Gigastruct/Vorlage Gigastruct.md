# Vorlage Gigastruct – Version 0.9

Stand: 30.10.2026, 23:45 (Wien), Qualitätsrunde Q1 eingearbeitet. Erstellt von Claude (Kanal-Sitzung Gigastruct) nur mit Claude Code und dem lokalen Renderer, ohne Higgsfield. Version 1.0 erst nach Stefans Freigabe. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`megaconstruction`, `brand_version: "0.9"`, `template_doc`).

Mit dieser Datei kann jede Sitzung Gigastruct-Videos reproduzieren: Plan schreiben, Trockenlauf, eine Vertonung, Render, Produktionsordner.

## Idee in einem Satz

Ein stilisiertes 3D-Architekturmodell des Bauwerks ist in jedem Bild das Hauptmotiv und der rote Faden; Größe wird nicht behauptet, sondern gerechnet und gezeigt (Maßketten, Bauphasen, Schnitt, maßstäblicher Vergleich). Keine Drohnenbilder, keine Fotos, keine KI-Renderings realer Bauwerke.

## Bausteine

| Baustein | Ort |
|---|---|
| Marke (Palette, Schriften, Logo, Modellfarben, Schlusssatz) | `C:\Automation\faceless-network\brands\megaconstruction\brand.yaml` |
| Regeln für Bild und Skript | `brands\megaconstruction\visual_style.md`, `script_prompt.md`, `subtitle_style.json`, `audio_style.yaml` |
| Fünf Szenentypen (Gigastruct-Bedeutung) | `brands\megaconstruction\scenes.py` (vom gemeinsamen Renderer über `fn.render.brand_scenes` geladen) |
| 3D-Ebene (Three.js, Seek-Protokoll von HyperFrames) | `brands\megaconstruction\render\gigastruct3d.js` |
| Renderaufruf (gemeinsame Regie-Kette plus 3D) | `brands\megaconstruction\render\render_gigastruct.py` |
| Bibliothek | `brands\megaconstruction\assets\vendor\three.module.min.js` (three.js r170, MIT, `LICENSE-three.txt`, `SOURCE.md`) |
| Logo | `brands\megaconstruction\assets\logo\gigastruct-mark.svg` (eigene Zeichnung: isometrischer Block mit zwei Röhren) |
| Beispiel-Plan | `data\direction\megaconstruction-20261105-1-de.json` (Fehmarnbelt-Tunnelelement) |
| Themenkalender November | `data\calendars\megaconstruction_2026-11.json` |

Der gemeinsame Renderer (`src\fn`, `scripts\render_direction.py`) bleibt unverändert. `render_gigastruct.py` registriert die fünf Gigastruct-Szenen nur im eigenen Prozess, löst Wortanker auf und legt eine durchgehende WebGL-Leinwand unter alle Szenen.

## Gestaltung

| Element | Regel |
|---|---|
| Grund | Stahlblau `#20384F`; die 3D-Szene füllt das ganze Bild. Seit Q1 mit Tiefe: Himmelskuppel (Zenit `#10223A`, Dunst am Horizont `#4B6F8F`, unter dem Horizont `#132536`), Nebel in Dunstfarbe je Einstellung, langsam treibendes Wasserraster, stilisierte Küsten `#2B4660` an den Bauwerksenden; darüber ein Schleier (oben und unten dunkler, Rand abgedunkelt, `#gsshade`) |
| Akzent | Bau-Orange `#FF8A2A`, einziges Akzent: Gemessenes, Zahlen, Maßchips, aktive Bauphase, Hervorhebungskante, Fortschritt |
| Schrift | `#E9EDF0` (Kontrast 10,2:1 auf dem Grund; Orange 5,1:1) |
| Modell | Architekturmodell: matt `#D6DDE3`, Innenflächen `#9FB0C0`, Zeichnungslinien `#3A5874`; Vergleichsobjekte gedämpft `#8FA6BC` |
| Schriften | Oswald 600/700 (Headlines, Zahlen, Untertitel), JetBrains Mono 700 (Kicker, Maße, Rechenweg, Statusleiste), Inter (selten); alle SIL OFL 1.1 |
| Logo | isometrischer Block plus „GIGASTRUCT“, 40 px oben links ab dem ersten Bild; kein Logo-Intro, keine Endkarte |
| Untertitel | Sinngruppen bis 4 Wörter (`caption_mode: phrases`), normale Schreibweise, Oswald 600, 62 px, Highlight-Wort orange, 540 px vom unteren Rand |
| Statusleiste | roter Faden in Worten: das Objekt (z. B. „Element 1 / 89“) und je Beat ein Zustand; Ton `accent` = aktiver Vorgang (orange), `green` = erreicht, `amber` = offen (Bernstein `#FFD166`), `red` = Risiko, `muted` = Info |
| Typografie (seit Q1) | Szenentitel Oswald 700, 78 px, mittig, höchstens zwei Zeilen; Hook-Frage 88 px; Karten (Kacheln, Schritte, Balken, Zähler, Chips, Hinweise) mit Radius 14 px und einheitlichem Schatten; Beschriftungen ab 28 px |
| Leitobjekt (seit Q1) | Das Bauteil ist in jeder Szene sichtbar: einzeln als Modell oder als erstes, orange markiertes Glied der ganzen Reihe (`chain`); erreichte Teile werden grün. Die Statusleiste wechselt mehrmals je Szene an gesprochenen Wörtern (mehrere `states` je Beat, `offset` in Sekunden ab Beatbeginn) |
| Licht | warmes Führungslicht mit Schatten, kühles Gegenlicht, kein Glow, kein Neon |
| Kamera | je Beat eine durchgehende Fahrt (Dive, Push, Rückzug); beim Beatwechsel harter Schnitt, Kreisübergang oder Überblendung (siehe Erklärschicht) |

## Erklärschicht (Schnitt- und Layout-Vorlage, seit 30.10.2026)

Grundlage ist `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`. Technisch übernimmt das der gemeinsame Renderer (`fn.render.explainer`). Gigastruct schaltet ihn in `brands\megaconstruction\brand.yaml` im Block `explainer` ein.

| Element | Gigastruct |
|---|---|
| Stimmhinweis | „SYNTHETISCHE STIMME“ oben rechts, das ganze Video |
| Einstiegszeile | 0 bis 3,5 s: „Synthetische Stimme · Quellen am Bildschirm · 3D-Modell vereinfacht“ |
| Kopf | Kicker in Mono 24 px bei y 186 mit Nummer, z. B. „3 · Schnitt · Standardelement“ (`overlay.kicker`). Den Titel liefert die Gigastruct-Szene (`headline`). Die Szenen tragen deshalb ab b2 keinen eigenen `kicker` mehr; nur der Hook behält ihn, weil der Kopf dort nicht erscheint |
| Marker und Quelle | ab y 1112 (`source_y`), unter der Szenenzone 290–1100, über den Untertiteln (ab etwa 1250) und der Statusleiste (1440), links von x 930. Die Quellenleiste hat höchstens zwei Zeilen; dafür steht in jeder Quelle ein kurzes `label` (z. B. „Femern A/S, Factsheet 8/2026“) |
| Farben mit fester Bedeutung | Fakt = Bau-Orange `#FF8A2A` (aktiver Vorgang), Bernstein `#FFD166` = offen oder unklar, Rot `#FF6B5B` = Risiko, Grün `#5CD08A` = erreichter Zustand (z. B. Elemente am Grund, Zählerblöcke), Violett `#9B6BFF` = Auslegung, Grau `#8A93A6` = Beispielwert |
| Marker je Szene | `fakt` für belegte Zahlen. Gerechnete Vergleiche („mehr als sieben Eiffeltürme“) sind Fakt mit beiden Quellen. Plan- und Prognosewerte (Fahrzeit nach Fertigstellung, Eröffnung) bekommen `unsicher` und eine Quellenleiste mit „Planwerte“. Erfundene Zahlen kommen bei Gigastruct nicht vor; falls doch, gilt `example: true` |
| Übergänge | Kreis (`iris`) bei einer Nahfahrt in das Objekt, Überblendung (`blende`, 0,7 s) bei einem Perspektivwechsel, sonst harter Schnitt. Die 3D-Ebene macht mit: Die alte Einstellung läuft auf `#gs3dprev` weiter, die neue öffnet sich als Kreis oder wird eingeblendet |
| Vignette | bei Nahfahrten (`vignette: true`), z. B. im Schnittmodell |
| Wortanker | Jede Bildaktion hängt an einem Wort: im Overlay `w:Wort`, in den Szenen `at_word` oder `@Wort`, in den 3D-Keyframes `@Wort±s`. Ausnahme ist die Statusleiste, die nur Sekunden ab Szenenbeginn kennt (`offset`). Sie muss bei neuer Stimme neu gesetzt werden |

Beispiel je Szene (`beats[].overlay`):

```json
{"kicker": "3 · Schnitt · Standardelement", "marker": "fakt", "marker_at": "w:217", "vignette": true,
 "transition": {"type": "iris", "x": 540, "y": 960, "seconds": 0.7}}
```

Storyboard je Video in `05 Produktion\<Ordner>\01 Skript\Storyboard.md` (Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild). Muster: Fehmarnbelt-Tunnelelement.

## Fünf Szenentypen

| Typ (Plan) | Gigastruct | Daten | Bildereignisse |
|---|---|---|---|
| `cinematic_hook` | Monument-Hook | `kicker`, `question` (≤ 64), `number{value, unit, at_word}`, `badge{text, at_word}` | Frage, Zahl mit Maßklammer, Chip |
| `data_flow` | Bauphasen in Schritten | `kicker`, `headline` (≤ 48), `steps[{label, sub, at_word}]` (bis 5), `rail_dy` | Phasenleiste, je Phase Label und Modellzustand |
| `ui_demo` | Schnittmodell | `headline`, `dims[{anchor, text, at_word}]`, `callouts[{anchor, text, side, at_word}]`, `note` | Dach wird aufgeschnitten, Maßchips und Beschriftungen hängen an 3D-Punkten |
| `comparison` | Größenvergleich, gerechnet | `a{label, value, unit}`, `b{…}`, `decimals`, `glyph: "tower"`, `a_at`/`b_at`/`result_at` als `@Wort` | Balken (Breite gerechnet), Verhältnis groß, Rechenweg, N Symbole (N = abgerundetes Verhältnis), im 3D N maßstäbliche Vergleichsobjekte |
| `key_takeaway` | Kennzahlen oder Abschluss | `items[{value, unit, label, ref, at_word}]` (bis 3) oder `mode: "closing"`: `statement`, `counter{done, total, label}`, `chip` | Kacheln; Abschluss mit Zähler aus Blöcken (gerechnet) und „Folge Gigastruct“ |

## 3D-Ebene (`layout.model3d` im Plan)

- `objects`: Grundkörper in Metern: `element` (extrudierter Querschnitt mit Röhren, Segmente, Schotten, Schnitt, Hervorhebung), `water`, `seabed` (mit Rinne), `ground`, `tower` (stilisierter Gitterturm für Vergleiche, kein Abbild), `boat` (Schlepper), `pontoon` (Absenkponton mit Seilen); seit Q1 `chain` (ganze Reihe aus `count` Teilen als Instanzen; Eigenschaften `reveal`, `done` = grün erreicht, `lead` = Index in Orange, `pulse`/`pulse_w` = wanderndes oranges Licht, z. B. ein Zug), `land` (stilisierte Küste) und `box` (Quader in einer Palettenfarbe). Neue Bauwerke brauchen meist nur neue Maße und Röhren; für Brücken, Türme oder Dämme können weitere Grundkörper in `gigastruct3d.js` ergänzt werden (gleiche Schnittstelle `apply(props)`).
- `anchors`: 3D-Punkte, an denen Beschriftungen und Maßchips hängen (`data-anchor`).
- `shots`: je Beat Kamera `p0→p1`, Blick `l0→l1` und Eigenschaften (`objekt.eigenschaft`) als fester Wert oder Keyframes `[[Zeit, Wert], …]`; Zeit in Sekunden ab Beatbeginn oder `"@Wort±s"` (wird aus den Wortzeiten aufgelöst). Seit Q1 je Shot `fog: [nah, fern]` (lange Blicke über das ganze Bauwerk) und in `cam` der Wert `dy` (Bildverschiebung in px, positiv = Inhalt nach oben), damit das Motiv in der freien Zone zwischen Titel und Karten steht. Kamerapositionen vor dem Render mit einem Trockenlauf und `npx hyperframes snapshot --at …` prüfen.
- Maßstab: Außenmaße aus den Quellen; was die Quellen nicht bemaßen (z. B. Röhren im Querschnitt), wird schematisch gezeichnet und im Bild als „Querschnitt schematisch“ gekennzeichnet.

## Regeln für Inhalt und Recht

- Jede Zahl aus einer Primärquelle (Bauherr, Betreiber, Behörde, Ingenieurbüro, Fachpresse) mit URL und Abrufdatum in `sources`; Unbelegtes in `unverified`, nie ins Video.
- Vergleiche werden gerechnet: beide Werte belegt, Verhältnis im Renderer aus den Werten berechnet, Rechenweg im Bild und in `layout.computations` sowie `manifest.computations`. Formulierung so wählen, dass sie in jeder plausiblen Lesart der Quelle stimmt.
- Laufende Projekte nur mit „Stand <Monat Jahr>“; Eröffnungstermine nur, wenn die aktuelle Primärquelle sie nennt.
- Bilder: nur stilisierte Modelle aus Grundkörpern. Das ist nach den Leitlinien der Kommission (C(2026) 5054) kein Deepfake; über das KI-Label hinaus ist keine Offenlegung am Videoanfang nötig. Fotorealistische Darstellungen realer Bauwerke sind ausgeschlossen.
- „KI-generiert“ dauerhaft im Bild; Labels `is_aigc`, `is_ai_generated`, `containsSyntheticMedia` in `post.json`.
- Keine Musik, bis eine Lizenzquelle gewählt ist.
- Gesprochener Aufruf am Schluss in der Handlung: „Folge Gigastruct, dann siehst du das nächste.“ Anrede „du“ nur im Aufruf.

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4,
           "status_bar": {"file": "<Objekt>", "states": [{"beat": "b1", "text": "…", "tone": "accent|green|amber|red|muted"}]},
           "computations": [{"id": "C1", "calculation": "…", "result": "…", "sources": ["S1"]}],
           "model3d": {"objects": [...], "anchors": {...}, "shots": {...}}}
```

Länge: 160–180 deutsche Wörter ergeben mit der Gemini-Stimme etwa 72–80 s.

## Ablauf je Video

1. Thema aus `data\calendars\megaconstruction_2026-11.json`, Quellen öffnen und prüfen, Plan `data\direction\megaconstruction-<JJJJMMTT>-1-de.json` nach dem Beispiel schreiben.
2. Trockenlauf (ohne Kosten, ohne Video):
   `.venv\Scripts\python.exe brands\megaconstruction\render\render_gigastruct.py data\direction\<id>.json --version dry --tts mock --no-render --mirror gigastruct\dry`
3. Sperrdatei `data\render.lock` prüfen und anlegen (brand_id, Uhrzeit), Speicher prüfen (`fn.cli status`, Grenze 30 GB).
4. Vertonung und Render (eine Gemini-Anfrage, ca. 0,02 USD):
   `… render_gigastruct.py data\direction\<id>.json --version V1 --tts gemini --mirror gigastruct\<datum>`
   Korrekturen ohne neue Kosten: `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`. Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme (Stefan, 30.10.2026). Layout prüfen ohne Stimme mit einem Trockenlauf: `--version V2dry --tts mock --no-render`, Standbilder mit `npx hyperframes snapshot` im Projektordner.
5. Sperrdatei entfernen. Produktionsordner füllen:
   `.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\<id>.json --version V1 --short "<Kurztitel>"`
6. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`. Nichts veröffentlichen.

## Testvideo (30.10.2026)

| | |
|---|---|
| Thema | Fehmarnbelt-Tunnel: ein Standardelement (217 × 42 × 9 m, 73.500 t) wiegt mehr als sieben Eiffeltürme und schwimmt |
| Hook | H1 (surprising_fact): „Dieses Betonteil wiegt mehr als sieben Eiffeltürme. Und trotzdem schwimmt es.“ Vier weitere Kandidaten im Plan |
| Szenenfolge | gs_hook → gs_numbers → gs_section → gs_phases → gs_compare → gs_numbers → gs_numbers (closing) |
| Rechnungen | 73.500 t ÷ 10.100 t = 7,28 (auch bei US short tons 8,02, „mehr als sieben“ gilt beidseitig); 89 − 3 = 86; 217 m ÷ 9 = 24,1 m |
| Länge, Prüfbericht | Q1 (Qualitätsrunde 31.10.2026): 78,7 s, VALIDATED, `overlap_check.mjs` ohne Befund, eine Warnung `visual_cuts_rhythm` (Median 1,0 s statt ab 1,2 s, mehr Bildereignisse als vorher). Eigene Note 2,0 |
| Stimme | Gemini-Aufnahme `storage\direction\voice_megaconstruction-20261105-1-de_V4_gemini.wav` (74,8 s, 134 Wörter), mit `--reuse-voice` wiederverwendet. Frühere Windows-Entwürfe verworfen |
| Kosten | Q1: 0 USD (Aufnahme wiederverwendet) |
| Ablage | `05 Produktion\Gigastruct\2026-11\2026-11-05 Fehmarnbelt-Tunnelelement\` (Export, Cover, Untertitel, Kontaktbogen `03 Schnittprojekt\Kontaktbogen Q1.jpg`); Vorschau `05 Produktion\_Demos\gigastruct\2026-11-05-q1`. Alter Produktionsstand in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde\` |

Neu rendern ohne neue Kosten (Sprechtext unverändert lassen, sonst verweigert der Renderer die Aufnahme):

```
.venv\Scripts\python.exe brands\megaconstruction\render\render_gigastruct.py data\direction\megaconstruction-20261105-1-de.json --version Q1 --reuse-voice storage\direction\voice_megaconstruction-20261105-1-de_V4_gemini.wav --mirror gigastruct/2026-11-05-q1
node scripts\overlap_check.mjs storage\direction\megaconstruction-20261105-1-de-Q1\project
.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\megaconstruction-20261105-1-de.json --version Q1 --short "Fehmarnbelt-Tunnelelement" --force
```

## Offen bis Version 1.0

- Stefans Freigabe von Optik, Stimme und Hook-Stil.
- Wiederverwendung mit einem zweiten Bauwerk anderer Art (Brücke oder Turm) prüfen; dafür eventuell Grundkörper `deck`/`pylon` ergänzen.
- EN-Fassung (zweite Vertonung).
- Musiklizenz.
