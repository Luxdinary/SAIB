# Vorlage Frontlore – Version 0.9 (Entwurf, nur Claude Code)

Stand: 31.10.2026 (Wien), Qualitätsrunde Q1 in Abschnitt 10. Erstellt von der Kanal-Sitzung Frontlore. Version 1.0 erst nach Stefans Freigabe. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`military_history`, `brand_version: "0.9"`, `template_doc`). Marke: Frontlore, brand_id `military_history`, Nische Militärtechnik und Geschichte, ausschließlich historisch und öffentlich dokumentiert. `risk_level` high: jedes Video endet in HUMAN_REVIEW und geht nur mit Stefans Freigabe hinaus.

## 1. Prüfliste harte Grenzen (vor Skript, vor Vertonung, vor Freigabe abhaken)

Jede Zeile muss mit „ja“ beantwortet sein. Ein „nein“ heißt: Thema ersetzen, nicht abmildern.

| Nr. | Prüffrage | Grundlage |
|---|---|---|
| G1 | Ist das Thema historisch (bis höchstens 1991) und öffentlich dokumentiert, mit mindestens zwei Quellen aus Museum, Archiv oder Fachliteratur (URL, Abrufdatum)? | Stefan 29.10.2026; `CLAUDE.md` des Repositorys |
| G2 | Enthält das Video keine Taktik und keine Anleitung (Vorgehen, Einsatzgrundsätze, Lagebeurteilung)? | Stefan; Plattformregeln |
| G3 | Keine Waffenhandhabung, kein Bau, Umbau oder Zerlegen von Waffen, keine Funktionsdetails, die als Anleitung taugen? | Stefan; YouTube- und TikTok-Richtlinien zu Waffen |
| G4 | Kein aktueller Konflikt, keine laufende politische Streitfrage? | Stefan; `brands.yaml` |
| G5 | Nichts aus Stefans Dienst, keine Uniform, keine Einheits-, Standort- oder Personenbezüge zum Bundesheer? | § 46 BDG (Verschwiegenheit) |
| G6 | Keine grafische Gewalt, keine Toten oder Verletzten im Bild oder in drastischer Sprache? | YouTube nicht werbefähig, TikTok nicht im For-You-Feed (`Faktencheck 2026-10-29.md`) |
| G7 | Keine Verherrlichung (Sprache sachlich, kein Heldenpathos, kein „legendär“, kein Kampfsound)? | Markenton |
| G8 | Keine Symbole verbotener Organisationen, auch nicht stilisiert oder angeschnitten? | österreichisches Verbotsgesetz, Plattformregeln |
| G9 | Nur stilisierte Darstellung (Archivkarte, Zeitleiste, Schnittzeichnung, Streckenkarte); keine realistische KI-Szene eines realen Ereignisses? Sonst wäre es ein Deepfake mit Offenlegungspflicht am Videoanfang. | EU-Leitlinien Art. 50 AI Act, C(2026) 5054 (`08 Recht und Verwaltung`) |
| G10 | KI-Label auf allen drei Plattformen gesetzt (`is_aigc`, `is_ai_generated`, `containsSyntheticMedia`) und „KI-generiert“ dauerhaft im Bild? | Stefans Vorgabe; `CLAUDE.md` |
| G11 | Jede Tatsachenbehauptung im Skript hat eine Quelle im Plan; Widersprüchliches steht in `unverified` und nicht im Video? | Regel „nichts erfinden“ |
| G12 | Keine Personen als Hauptmotiv, keine Porträts realer Personen, keine erfundenen Zitate? | Art. 50, Persönlichkeitsrechte |

## 2. Stil „Documentary Tech, sachlich“

- Look: olivgrüner Grund mit Höhenlinien (`map-contours`), eine helle Archivkarte als einzige Lichtfläche, Zeichnungen als Strichgrafik, die sich zeichnet, Stempel für Daten. Kein Glow, keine Lichtkegel, Kamera höchstens 2 % (`flat: true`).
- Palette (Basis aus `brands.yaml` unverändert, ergänzt in `brands\military_history\brand.yaml`):

| Rolle | Hex | Kontrast | Einsatz |
|---|---|---|---|
| bg | #29352D | – | Grund |
| surface | #38433C | – | Zeichenblatt, Karten |
| accent | #A9B29F | 5,8:1 auf bg | Linien, Marker, Fortschritt, Hervorhebungswort |
| text | #E6E9E5 | 10,5:1 auf bg | Überschriften, Text |
| muted | #B0B7AC | 5,0:1 auf surface | Mono-Beschriftungen; geändert von #919892 (nur 3,5:1 auf surface) |
| paper / paper_ink | #E9E4D4 / #1F2620 | 12,2:1 | Archivkarte |
| stamp | #2B4257 | 8,2:1 auf paper | Stempel auf Papier, Tintenblau; seit V2 statt Rostrot #A8452F, weil Rot nur noch ein Risiko bedeutet (Abschnitt 9) |
| signal_amber | #D9B45A | 6,5:1 auf bg | Statusleiste „unterwegs/offen“, Marker „Unsicher“ |
| signal_green | #7DBE8A | 5,9:1 auf bg | nur erreichter Zustand (die gemeinsame Statusleiste hat noch keinen grünen Ton) |

- Schriften (alle SIL OFL 1.1, Dateien und Lizenzen in `C:\Automation\faceless-network\assets\fonts\`): Oswald 500 (Überschriften in Versalien, Fragen, Jahreszahlen), Inter (Text, Untertitel), JetBrains Mono (Aktenzeichen, Codes, Beschriftungen).
- Logo: Entwurf `brands\military_history\assets\logo\frontlore-mark.svg` (Karteikarte mit Reiter und Höhenlinie, eigene Arbeit) plus Wortmarke FRONTLORE in Versalien, klein oben links ab dem ersten Bild. Kein Logo-Intro, keine Endkarte.
- Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), normale Schreibweise, Hervorhebungswort in accent.
- Bildmitte gefüllt: Szenenzone y 290–1100, ein dominantes Motiv je Szene; Statusleiste y 1440, Fortschritt y 1548, KI-Label darüber (alles oberhalb der Plattform-Beschriftung bei y 1620).

## 3. Die fünf Szenentypen in der Frontlore-Fassung

Code: `C:\Automation\faceless-network\brands\military_history\frontlore_scenes.py` (`TEMPLATES`, `LIMITS`, `HOOK_SCENE_TYPES`, `scene_css`). Der gemeinsame Renderer lädt es über `scenes:` in `brands\military_history\brand.yaml` (`fn.render.brand_scenes`, `docs\direction-system.md` Abschnitt 6d); die Varianten gelten nur für Frontlore-Pläne. Die Namen der Szenentypen bleiben gleich, Story- und Regieprüfungen gelten unverändert. `comparison` nutzt die gemeinsame Vorlage mit Frontlore-CSS.

| Szenentyp | Frontlore-Bild | Daten (`data`) |
|---|---|---|
| `cinematic_hook` | Archivkarte gleitet herein, Zeichnung des Objekts zeichnet sich, Stempel (Jahr) schlägt ein, große Frage oben | `question` ≤ 64, `card_title` ≤ 30, `card_meta`, `card_no`, `stamp` ≤ 12, `drawing`, `card_at`, `draw_at`, `stamp_at`, `question_at` |
| `data_flow` | Streckenkarte: gestrichelte Linie, Stationsmarker mit Codes, das Objekt (z. B. Depesche) wandert von Marker zu Marker, Marker färben sich, Chip | `headline`, `nodes[{label ≤ 22, code ≤ 14}]` (2–5), `edges[{label ≤ 28}]`, `packet_label`, `packet_at`, `travel`, `highlight{node,label,at}` |
| `ui_demo` | Schnittzeichnung auf Zeichenblatt: Striche zeichnen sich, Beschriftungen mit Führungslinien nacheinander, Detail-Zoom und zurück, Vermerk „Stilisierte Darstellung“. Keine Bildschirmaufnahme, daher kein `schematic_ui` | `headline`, `drawing`, `sheet_title`, `sheet_h`, `draw_top`, `callouts[{label ≤ 30, x, y, lx, ly, align, at}]`, `zoom{x,y,scale,at,back_at}` |
| `comparison` | gemeinsame Vorlage, als zwei Archivkarten (Reiterleiste oben, Mono-Titel, quadratische Faktmarker) | wie Scutoria (`versus`/`negate`); Marken neutral (`ok: null`), keine Haken |
| `key_takeaway` | `mode: timeline`: senkrechte Zeitleiste mit Jahreszahlen, Punkte leuchten nacheinander auf. `mode: closing`: die Archivkarte vom Anfang kehrt zurück, Stempel an einem gesprochenen Wort (z. B. „Nachbau“), Schlusssatz, Chip „Folge Frontlore“ = Abschluss in der Handlung | `items[{year ≤ 6, title ≤ 30, sub ≤ 40, at}]` bzw. `card_*`, `stamp`, `statement` ≤ 64, `chip` ≤ 34, `drawing` |

Zeichnungen: `brands\military_history\assets\drawings\*.svg`, eigene Arbeit, viewBox 760 × 620, Linien mit `class="ln"` und `pathLength="1"` (zeichnen sich), `sight` (gestrichelt), `pivot` (Punkte). Je Thema eine neue Zeichnung; stilisiert, nicht maßstäblich, keine Rekonstruktion eines bestimmten Objekts behaupten. Keine Waffe als Zeichnungsgegenstand (G3).

## 4. Roter Faden und Dramaturgie

- Ein durchgehendes Objekt je Video in der Statusleiste (`layout.status_bar.file`), z. B. „Depesche“, „Karte“, „Brücke“; je Beat ein Zustand. Das Objekt ist erzählerisch, nie eine erfundene historische Einzelheit (kein erfundener Inhalt einer echten Nachricht).
- Story-Engine: Hook → Problem → Erklärung → Demonstration → Erkenntnis → (Nutzen) → Abschluss. Hook-Engine: fünf Kandidaten, je einer pro Typ, Wahrheit mindestens 4. Für Frontlore ist der Typ `concrete_risk` meist schwach belegt; er wird trotzdem bewertet und darf verlieren.
- Ton: ruhig, sachlich, respektvoll, „du“ nur in der Handlungsaufforderung. Gesprochener Aufruf: „Historische Technik, sachlich erklärt: Folge Frontlore.“
- Länge 65–90 s: etwa 155–175 Wörter mit Gemini Charon (Tempo 0,97). Jahreszahlen als Ziffern schreiben (Untertitel lesbar).
- Quellen stehen am Bildschirm in der Quellenleiste (Abschnitt 9), zusätzlich in `post.json` und `Veröffentlichung.md`. Die frühere Regel „Quellen nur in post.json, nicht im Bild“ gilt seit 30.10.2026 nicht mehr; sie ist durch die Schnitt- und Layout-Vorlage ersetzt. Der Hinweis „Stilisierte Darstellung, keine Originalaufnahmen“ steht in der Einstiegszeile.

## 5. Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4, "status_bar": {"file": "<Objekt>", "states": [...]},
           "description": "...", "companion_text": "Historische Technik, sachlich erklärt: Folge Frontlore.", "hashtags": [...]}
```

Keine Asset-Schicht (keine Clips): Fassung nur Claude Code. Eine spätere Higgsfield-Fassung bräuchte Clips ohne realistische Ereignisse (G9).

## 6. Ablauf je Video (PowerShell im Repository, vorher `$env:PYTHONIOENCODING = "utf-8"`)

1. Thema aus `data\calendars\military_history_2026-11.json` wählen, Prüfliste G1–G12 durchgehen.
2. Plan `data\direction\military_history-<JJJJMMTT>-<n>-de.json` schreiben (Muster: `military_history-20261110-1-de.json`), Zeichnung anlegen.
3. Trockenlauf: `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --no-render`
4. Vertonung ohne Render (eine Gemini-Anfrage): `... --version V1 --tts gemini --no-render --mirror frontlore-regie/<datum>`. Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme (Regel Stefan, 30.10.2026). Layout wird bis dahin nur im Trockenlauf geprüft: `... --version V2dry --tts mock --no-render`, Standbilder mit `npx hyperframes snapshot` im Projektordner des Trockenlaufs. Die Hauptsitzung vertont mit Gemini und rendert die Endfassung.
5. Freien Speicher auf C: prüfen (mindestens 30 GB), Sperrdatei `data\render.lock` prüfen (jünger als 20 Minuten: warten), anlegen, rendern ohne neue Kosten: `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version V1 --reuse-voice storage\direction\voice_<id>_V1_<provider>.wav --mirror frontlore-regie/<datum>`, Sperrdatei entfernen.
6. Produktionsordner: `.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\<id>.json --version V1 --short "<Kurztitel>"` (Abschlusssatz aus `brand.yaml` › `production.closing_sentence`)
7. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`; nichts veröffentlichen. Status bleibt HUMAN_REVIEW bis Stefan freigibt.

## 7. Erstes Testvideo

`05 Produktion\Frontlore\2026-11\2026-11-10 Optischer Telegraf\` – „Nachricht ohne Strom: Preußens optischer Telegraf Berlin–Koblenz“. Aktuell Fassung Q1 (31.10.2026, Qualitätsrunde, Abschnitt 10): 79,4 s, Gemini-Stimme aus V2 unverändert, Prüfbericht HUMAN_REVIEW (risk_level high, keine weitere offene Prüfung), Überschneidungs-Prüfung ohne Befund, Export in `04 Export`, Kontaktbogen `03 Schnittprojekt\Kontaktbogen Q1.jpg`. Die Fassungen V1 (Windows-Stimme) und V2 liegen in `_zum_loeschen`. Details in `01 Skript\Skript.md`, `01 Skript\Storyboard.md` und `03 Schnittprojekt\report.json`. Themenkalender November: `C:\Automation\faceless-network\data\calendars\military_history_2026-11.json` (30 Themen, je mindestens zwei Quellen, Risiko je Thema in `notes`).

Art. 50: `brands\military_history\intro_config.json` › `art50_disclosure.enabled` steht auf false (Phase 1 hatte eine pauschale Offenlegungskarte aktiviert, die der Regie-Renderer nicht zeichnet). Begründung: nur stilisierte Zeichnungen (G9). Stefan entscheidet, ob er trotzdem eine Offenlegung am Anfang will.

## 8. Offen für Version 1.0

- Freigabe von Palette, Logo-Entwurf und den fünf Szenen durch Stefan.
- Gemini-Vertonung des Testvideos: erledigt (V2), seit Q1 hängen die Szenenzeiten als Wortanker an der Stimme; nur die Offsets der Statusleiste sind noch Sekunden.
- Zweites Thema mit anderer Zeichnung als Wiederverwendungstest.
- Musik: keine (Lizenzquelle fehlt).

## 9. Erklärschicht (Schnitt- und Layout-Vorlage, seit 30.10.2026)

Grundlage: `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`, Renderer `src\fn\render\explainer.py`. Eingeschaltet in `brands\military_history\brand.yaml` › `explainer`.

- **Oben rechts** steht durchgehend „SYNTHETISCHE STIMME“.
- **Einstiegszeile** von 0 bis 3,5 s: „Synthetische Stimme · Quellen am Bildschirm · Stilisierte Darstellung, keine Originalaufnahmen“.
- **Kopf:** Die Kicker-Zeile steht bei y 186 in Mono 24 px, in Frontlore-Wörtern, zum Beispiel „2 · DER ANLASS“, „3 · DIE TECHNIK“, „4 · DIE ARBEIT“, „5 · DIE LINIE“, „6 · DIE ZEIT“, „7 · HEUTE“. Den Titel liefert die Szene selbst (`headline`), einen eigenen Kopftitel gibt es nur ohne Szenentitel. Der Hook hat keinen Kopf.
- **Marker und Quellenleiste** stehen bei `source_y: 1112`, wie bei Scutoria. Die Szenenzone endet bei 1100, die Untertitel beginnen bei etwa 1250, die Statusleiste steht bei 1440 und der Plattformtext beginnt bei 1600. Rechts bleibt alles links von x 930.
  - Marker: Fakt (Quadrat), Auslegung (Raute), Unsicher (Halbkreis), Lücke (gestrichelter Kreis), dazu der Chip „Beispielwert“ für erfundene Zahlen. Immer Form und Wort, nie Farbe allein.
  - Die Quellenleiste nimmt kurze `label` aus `sources[]` und zeigt höchstens zwei Zeilen. Frontlore-Kürzel: „LVR KuLaDig: Telegrafenlinie“, „Stadtmuseum Brandenburg“, „GFZ Potsdam“, „zfv 2/2018“.
  - Je Szene höchstens drei kurze Quellen, sonst wird die Leiste zu lang.
- **Farben mit fester Bedeutung** (`explainer.colors`):

  | Bedeutung | Hex | Kontrast | Hinweis |
  |---|---|---|---|
  | Fakt | #A9B29F | 5,8:1 | = accent, aktiver Vorgang |
  | Auslegung | #B49CE6 | 5,4:1 | Violett |
  | Unsicher | #D9B45A | 6,5:1 | Bernstein, = signal_amber |
  | Lücke / Risiko | #D9775C | 4,1:1 auf bg, 3,3:1 auf surface | |
  | Beispielwert | #98A196 | 4,8:1 | |
  | erreicht | #7DBE8A | | Grün, nur erreichter Zustand |

  Der Stempel ist deshalb tintenblau. Rot gibt es in Frontlore nur für ein echtes Risiko, also praktisch nie.
- **Eigene Marker in den Szenen:** Die Faktquadrate in `comparison` (`ok: null`) passen zum unteren Marker „Fakt“. Haken, Kreuze und grüne Quadrate werden in Frontlore nicht verwendet.
- **Unsicher:** Strittige historische Angaben kommen nicht ins Video, sondern nach `unverified`. Muss eine solche Angabe doch gesprochen werden, bekommt die Szene `marker: "unsicher"` und eine Quellenleiste, die beide Angaben nennt.
- **Übergänge:**
  - Der Kreisübergang öffnet sich aus einem Objekt der vorigen Szene, zum Beispiel einem Stationsmarker der Streckenkarte (`transition: {type: iris, x, y}`). Koordinaten des Testvideos: Berlin-Knoten (224, 462), Koblenz-Knoten bei fünf Stationen (224, 1042).
  - Sonst gibt es eine Überblendung (`blende`, 0,7 s) oder einen harten Schnitt.
  - Bei der Schnittzeichnung (Nahaufnahme) ist `vignette: true` gesetzt, und auf das Zoom-Wort wird der Kopf zurückgenommen (`dim_at`).
- **Jede Bildaktion an einem Wort:** Kopf und Marker hängen über `w:Wort` am Wort, in der Schlussszene endet beides auf „Historische“ (`head_until`, `marker_until`). Die Szenenzeiten in `data` (`*_at`, Hinweise, Depesche, Stempel) und die Offsets der Statusleiste sind Sekunden; sie werden auf die gemessenen Wortanfänge der Stimme gesetzt. Nach einer neuen Vertonung müssen sie neu gesetzt werden.
- **Roter Faden:** Die Depesche kommt in der Szene an, in der der Zielort gesprochen wird. Die Schlusskarte erzählt, was heute bleibt.
- **Storyboard** je Video in `01 Skript\Storyboard.md` mit den Spalten Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild.
- **Stimme:** nur Gemini. Ohne Gemini-Stimme kein Export und nichts in `04 Export`; geprüft wird nur im Trockenlauf mit Mock-Stimme.

## 10. Qualitätsrunde Q1 (31.10.2026)

Grundlage: `02 Marke\Qualitätsrunde 2026-10-31.md` (Ziel Scutoria-Niveau, Note 1,7). Umgesetzt im Testvideo „Optischer Telegraf“, Fassung Q1, mit der vorhandenen Gemini-Stimme aus V2.

- **Hintergrund mit Tiefe:** `LAYER` in `frontlore_scenes.py` legt unter alle Szenen eine Vermessungskarte: `assets\bg\base.jpg` (Licht von links oben, Papierstruktur, Raster) und `assets\bg\contours.png` (Höhenlinien, jede fünfte stärker, gestrichelte Linie mit Stationsmarken als Schmuck). Beide erzeugt `brands\military_history\make_background.py` mit numpy und Pillow, eigene Arbeit, Nachweis `assets\bg\LICENSE.md`. Der Grund driftet langsam und wächst um 3,5 %, die Höhenlinien schwenken bei jedem Szenenwechsel an eine neue Stelle. Ein dunkler Rand liegt darüber. Kein Glow, kein Lichtkegel.
- **Leitobjekt Depesche:** ein Papierzettel (`_dep`) mit Reiter und Zeichenkästchen, ohne Nachrichtentext. Er läuft durch Hook, Karte, Weitergabe und Linie; je weitergegebenem Zeichen füllt sich ein Kästchen. Dazu bleibt die Statusleiste „Depesche“.
- **Wortanker in den Szenen:** Jede Zeit in `data` darf `"w:Wort"` oder `"w:Wort#2"` sein (erstes oder zweites gesprochenes Wort der Szene, das so beginnt). Zahlen bleiben Sekunden ab Szenenbeginn. Damit verschieben sich die Bildaktionen nach einer neuen Vertonung von selbst. Nur die Statusleiste braucht noch Sekunden.
- **Masten als Code:** `_mast` zeichnet stilisierte Stationen mit sechs drehbaren Flügeln, `STATES` hält vier stilisierte Stellungen (keine echte Zeichentabelle). In der Schnittzeichnung drehen sich die Flügel über `signals` an Wörtern.
- **Neue Szenenformen** (Szenentypen bleiben gleich):
  - `data_flow` mit `mode: "map"`: schematische Karte mit Punkt, Region, Weg, Sanduhr, Chip und Mastenkette (`places`, `route_*`, `wait_at`, `chip`, `masts`, `line_label`).
  - `data_flow` ohne `mode`: Linie mit Stationen; `nodes[].at` lässt die Depesche genau auf dem Ortsnamen ankommen, `count` und `total` zählen rechts oben (z. B. 62 Stationen, ca. 587 km).
  - `comparison` mit `mode: "relay"`: Nachbarstation und eigene Station mit Sichtlinie, zwei Rollenkarten, Chip „Diktat“, Flügel übernehmen die Stellung, Depesche wandert (`cards`, `sight_at`, `dictate_at`, `match_at`, `flip_at`).
  - `ui_demo`: `draw_scale` verkleinert die Zeichnung im Blatt, `zoom.grow: "up"` lässt das Blatt beim Heranfahren nur nach oben wachsen und nimmt den Titel zurück, `callouts[].count` zählt eine Zahl hoch.
  - `key_takeaway` `timeline`: Füllung der Zeitleiste bis zum jeweiligen Jahr, `sub_at`, `end_at`. `closing`: `sign` (Schild auf der Karte), `ghost_at` (Zeichnung verblasst), `note` (Vermerk auf der Karte).
- **Titel:** Oswald 74 px in Versalien, höchstens zwei Zeilen. `headline_lines` im Plan (1 oder 2) setzt die Bühnenhöhe; bei zwei Zeilen bleiben 624 px. Beschriftungen mindestens 26 px.
- **Bildereignisse:** Aktionen, die weniger als 0,8 s auseinanderliegen, zählen im Prüfbericht als ein Bildereignis (`_thin`).
- **Prüfen:** Probelauf ohne Video mit der vorhandenen Stimme (`--version Q1dry --reuse-voice <wav> --no-render`), Standbilder mit `npx hyperframes snapshot --at ...`, `node scripts\overlap_check.mjs <projekt>` schon am Probeprojekt. Fehler im Zeitleisten-Skript zeigt die HyperFrames-Prüfung nicht an: fehlen Zeichnungen oder Karten im Standbild, die Seite in Chrome laden und `pageerror` lesen.

