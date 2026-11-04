# Vorlage Zonkfruit – Version 0.9 (Entwurf)

Stand: 30.10.2026, 23:40 (Wien), mit Qualitätsrunde Q1 (Abschnitt 3b). Erstellt von der Kanal-Sitzung Zonkfruit (Claude Code), nur mit Code: SVG-Figur, HyperFrames-Szenen, programmatische Soundeffekte, Gemini-Stimme. Kein Higgsfield, kein KI-Bild, keine Musik. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`brainrot`, `brand_version: "0.9"`). **Version 1.0 erst nach Stefans Freigabe von Figur und Vorlage.**

## 1. Idee in einem Satz

Plümo, eine erfundene Frucht, versteht etwas Alltägliches falsch, probiert es aus und kippt um; die Pointe ist immer ein **echter, belegter Sachverhalt**.

Warum so: Brainrot hat laut Faktencheck geringes Werbepotenzial und ein hohes Risiko austauschbarer Inhalte; YouTube schließt „AI-generated content made with generic or unoriginal templates“ von der Monetarisierung aus (Faktencheck, Abschnitt 6.1 Übergabebericht). Gegenmittel: eigene Figur mit festem Charakterblatt, wiederkehrende Running Gags und je Folge ein eigener redaktioneller Kern (ein Fakt mit Quelle). Das Format bleibt absurd und schnell, ist aber nicht beliebig.

## 2. Bausteine

| Baustein | Ort |
|---|---|
| Figur Plümo (Charakterblatt, Ansichten, Posen, Merkmale, Ähnlichkeitsprüfung) | `brands\brainrot\assets\character\` (`character.md`, `plumo_sheet.png`, SVGs); Vorschau `02 Marke\Tintora\Plümo Charakterblatt (Entwurf).png` |
| Figuren-Generator | `brands\brainrot\renderer\plumo.py` |
| Szenentypen | `brands\brainrot\renderer\zonk_templates.py`, für den gemeinsamen Renderer freigegeben über `brands\brainrot\scenes.py` (Schnittstelle `docs\direction-system.md` 6d) |
| Render-Starter (hält nur `data\render.lock`, ruft `scripts\render_direction.py` unverändert auf) | `brands\brainrot\renderer\render_zonkfruit.py` |
| Produktionsordner füllen | `brands\brainrot\renderer\export_zonkfruit.py` |
| Soundeffekte (selbst erzeugt, `LICENSE.md`) | `brands\brainrot\assets\sfx\` (Generator `renderer\sfx.py`) |
| Schrift Fredoka (OFL-1.1) | `brands\brainrot\assets\fonts\fredoka\` |
| Logo-Marke | `brands\brainrot\assets\logo\zonkfruit-mark.svg` |
| Markenwerte | `brands\brainrot\brand.yaml`, `subtitle_style.json`, `audio_style.yaml` |
| Beispielplan | `data\direction\brainrot-20261105-1-de.json` |
| Themenkalender | `data\calendars\brainrot_2026-11.json` (30 Tage ab 05.11.2026) |

## 3. Gestaltung

- **Stil „Surreal 3D, verspielt“:** dunkle Dämmerbühne (#2C1638 → #101010), perspektivischer Schachbrettboden in Pflaume, drei schwebende Kugeln (magenta, lime, violett), die langsam driften. Plümo mit Verlaufsschattierung, magenta Randlicht und Bodenschatten; Text mit „extrudiertem“ Schatten (#4B1640).
- **Palette:** Grund #101010, Fläche #212121, Akzent lime #B7FF00, zweiter Akzent magenta #FF43C0, Text warmes Weiß #FFF4FA, Pflaume #4B1640 (Schatten, Tiefe), Etikett-Creme #FFF2C7. **Begründete Änderung:** Text war in brands.yaml #FF43C0; Magenta auf bewegtem, dunklem Grund ist schlechter lesbar als warmes Weiß, deshalb Text weiß und Magenta nur für Akzente (Blatt, Ablehnung, Merke-Chip).
- **Schrift:** Fredoka 700 (rund, verspielt, OFL-1.1) für Titel, Labels und Untertitel. Montserrat entfällt für diese Marke.
- **Logo:** Plümos Kopf plus Wortzeichen ZONKFRUIT klein oben links ab dem ersten Bild; kein Logo-Intro, keine Endkarte.
- **Untertitel:** Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), normale Schreibweise, 62 px, warmes Weiß, Highlight lime, seit Fassung V2 500 px über dem unteren Rand (eine Zeile y 1349–1420, darüber Marker und Quellenleiste), Breite 800 px.
- **„KI-generiert“** dauerhaft im Bild (unten, über der Plattform-Beschriftung).

## 3a. Erklärschicht (seit 30.10.2026, Fassung V2)

Grundlage ist `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`; technisch ist es der gemeinsame Renderer `src\fn\render\explainer.py`, eingeschaltet in `brands\brainrot\brand.yaml` im Block `explainer`. Für Zonkfruit ist die Schicht angepasst, nicht kopiert: Plümo und die Pointen bleiben vorn, die Schicht ist leise und klein.

- **Durchgehend:**
  - „SYNTHETISCHE STIMME“ steht oben rechts.
  - Die Einstiegszeile läuft von 0 bis 3,5 s: „Synthetische Stimme · Quellen am Bildschirm · Plümo ist erfunden, die Fakten nicht“.
  - Der Hook bekommt keinen Kicker, weil die Hook-Szene ihren eigenen Titel trägt (`head_on_hook: false`).
- **Kicker-Zeile** bei y 186, Mono 24 px, in Limette, im Zonkfruit-Ton:

  | Funktion | Kicker DE | Kicker EN |
  |---|---|---|
  | Problem | MOMENT MAL | WAIT, WHAT |
  | Erklärung | KURZ ERKLÄRT | QUICKLY EXPLAINED |
  | Demonstration | GENAU HINGESCHAUT | UP CLOSE |
  | Erkenntnis | DER KNACKPUNKT | THE TWIST |
  | Nutzen | ZUM MERKEN | REMEMBER THIS |
  | Abschluss | UND TSCHÜSS | AND BYE |

  Davor steht die laufende Nummer, zum Beispiel „2 · MOMENT MAL“.
- **Marker und Quellenleiste:** `source_y: 1170`.
  - Die Kapsel liegt bei y 1170–1214, die Quellenleiste (höchstens zwei Zeilen) bei y 1226–1288, links ab x 108, rechts bis x 930.
  - Darüber endet die Bühne mit Plümo und Tür bei etwa y 1100. Darunter stehen die Untertitel (eine Zeile bei y 1349–1420), dann Fortschrittsbalken und „KI-generiert“. Der Plattformtext beginnt ab y 1600.
  - Damit das passt, liegen die Untertitel 500 statt 540 px über dem unteren Rand. In `zonk_diagram` steht Plümo 40 px höher, in `zonk_zoom` stehen Plümo und das zweite Etikett 30 bis 40 px höher.
- **Farben mit fester Bedeutung** (`explainer.colors`):

  | Bedeutung | Farbe | Wo im Video |
  |---|---|---|
  | Fakt, aktive Farbe | Limette #B7FF00 (Markenakzent) | Fakt-Marker |
  | offen, unklar | Bernstein #FFD84D | Anzeige „Sorte: nicht ermittelbar“, früher Creme |
  | Risiko | Rot #FF4D4D | nur Lücke oder Risiko; `signal_red` von Magenta auf Rot umgestellt |
  | erreicht | Mintgrün #3EE08F | nur der Stempel EINLASS, früher Limette |
  | Auslegung | Violett #A97BFF | Auslegungs-Marker |

  Magenta #FF43C0 bleibt Markenfarbe und ist kein Signal: Blatt, Randlicht, Stempel ABGELEHNT, Merke-Chip. Die Mono-Schrift der Leiste ist JetBrains Mono, der gemeinsame Standard für Marken ohne eigene Mono-Schrift.
- **Im Plan je Szene** (`beats[].overlay`):
  - Fakt-Marker, wo eine Sachaussage fällt. `marker_at` steht immer an einem gesprochenen Wort, zum Beispiel `"w:Körnchen"`.
  - Der „Merke“-Beat (Nutzen) bekommt `auslegung`: Der Merksatz fasst zusammen, und Plümos Selbsttest ist erfunden. Deshalb erscheint dort keine Quellenleiste.
  - Der Abschluss bekommt `none`.
  - Je Quelle steht ein kurzes `label` in `sources[]`, zum Beispiel „Uni Potsdam, Botanischer Garten“ oder „wissen.de, Lexikon Beere“.
- **Übergänge:**
  - Kreisübergang aus einem Objekt der neuen Szene, zum Beispiel aus der Mitte des Beerenquerschnitts in `zonk_diagram` (`{"type": "iris", "x": 540, "y": 697}`).
  - Überblendung 0,7 s in die Lupen-Nahaufnahme.
  - Sonst ein harter Schnitt: Zwischen den Tür-Szenen und in den Loop bleibt der Schnitt hart, damit Plümos Umkippen und Aufstehen durchgehend wirkt.
- **Nahaufnahme** (`zonk_zoom`): Mit `vignette: true` wird der Rand abgedunkelt, und `dim_at` am ersten Fachwort nimmt den Kicker zurück.
- **Eigene Marker in den Szenen:** Die Stempel und Anzeigen gehören zur Handlung und sind keine Belegmarker. Keiner widerspricht dem unteren Marker, deshalb wurde keiner abgeschaltet; nur ihre Farben folgen jetzt den festen Bedeutungen.
- **Loop:** Der Kicker des Abschlusses endet auf „steh“ (`head_until`), sodass das letzte Bild wieder die leere Bühne des ersten zeigt. Abweichen dürfen nur die Einblendungen oben, also Logo und „SYNTHETISCHE STIMME“, die in den ersten 0,3 s einblenden.
- **Plattform-Symbole:** Die Tür steht seit V2 bei x 590, ihr Rahmen endet bei x 922. Die Anzeige „Sorte: nicht ermittelbar“ endet bei x 920.

## 3b. Qualitätsrunde (Fassung Q1, 30./31.10.2026)

Grundlage: `02 Marke\Qualitätsrunde 2026-10-31.md`. „Scutoria-Niveau“ heißt für Zonkfruit volle Bildfläche, Tiefe, mehr Bewegung an Wörtern und saubere Grafik, aber nicht Scutorias ruhiger Stil. Plümo und die Pointen bleiben vorn.

- **Hintergrund mit Tiefe (nur Code, in `zonk_templates.stage`):**
  - Nachthimmel mit fester Lichtlogik: Hauptlicht oben links, wie das Glanzlicht auf Plümo, und Magenta-Neon von rechts, wie sein Randlicht.
  - Kleiner Ringplanet, ferne surreale Landschaft (Dünen, Bogengang, halb versunkene Kugel, zwei schwebende Felsen) mit Parallaxe.
  - Drei Lichtkegel, Schachbrettboden mit Lichtpfütze und Horizontdunst.
  - Zwei Staubschichten, schwebende Kugeln, unscharfe Lichtflecken, Vignette.
  - Jede Bewegung ist eine periodische Funktion der absoluten Zeit (`drift`), mit der Videolänge als Periode. `scenes.LAYER` setzt sie vor dem Szenenbau. Darum läuft der Hintergrund über harte Schnitte ohne Sprung weiter, und das letzte Bild gleicht dem ersten.
- **Kamera:** Jede Szene steckt in einem Kamerarahmen (`.zcam`) und fährt langsam heran, 3,5 bis 5 %. Die Tür-Szenen setzen die Kamera fort: Erkenntnis 1,0 → 1,035, Nutzen 1,035 → 1,08, Abschluss 1,08 → 1,0 bis kurz nach dem Aufstehen. Ursprung bei x 860, damit rechts nichts über x 930 wandert.
- **Leitobjekt und Statusleiste:** Die gemeinsame Statusleiste (`layout.status_bar`, Doku `docs\direction-system.md` 6b) steht im Zonkfruit-Stil.
  - Sie zeigt „Beerenclub“ mit Türsymbol, Fredoka, Limettenrand. Sie liegt bei `status_y` 1440, unter den Untertiteln; der Fortschrittsbalken liegt bei `progress_y` 1550.
  - Die Zustände folgen der Geschichte, zum Beispiel „Erdbeere: abgelehnt“, „Erdbeere: Sammelnussfrucht“, „Plümo: nicht ermittelbar“.
  - Farbtöne als `tone`: `amber` (offen), `lime` (Fakt), `mint` (erreicht), `pop` (Magenta, Markenfarbe), `muted`.
- **Bewegung an Wörtern:** Jede Szene hat mindestens drei Bildereignisse an gesprochenen Wörtern. Neue Stichwörter im Plan:
  - Hook: `cue_scan`, `cue_verdict`, `cue_club`, `cue_know`.
  - `zonk_word`: `item`, `cue_shock`, `cue_item`, `cue_never`.
  - `zonk_diagram`: `cue_q`, `cue_hands`, `cue_leaf`.
  - `zonk_zoom`: `cue_nut`, `cue_fast`.
  - `zonk_scan` accept: `cue_all`, `cue_why`, `cue_shrug`; unknown: `cue_build`.
  - `zonk_loop`: `cue_lie`, `cue_ch`.
- **Größer und sauberer:**
  - Beerenquerschnitt 620 statt 520 px, Wort 160 px, Titel 72 bis 78 px.
  - Titel, Chips, Etiketten, Lupe, Stempel und CTA enden links von x 930.
  - Im Lupenbild überdeckt der Stempel kein Etikett mehr, weil die Lupe vorher Platz macht.
  - Die Lupen-Etiketten tragen `data-layout-allow-occlusion`, weil die Vignette der Erklärschicht sie gewollt halbdurchsichtig überlagert.
- **Übergänge:** zusätzlich ein Kreis aus der Türlampe in die Erkenntnis-Szene (`{"type": "iris", "x": 756, "y": 575}`). Der Kreis in die Erklärung kommt aus der Mitte des größeren Querschnitts (540, 730).

## 4. Dramaturgie und Tempo (abweichend von Scutoria)

Story-Engine wie bei allen Marken (Hook → Problem → Erklärung → Demonstration → Erkenntnis → Nutzen → Abschluss), aber als Sketch erzählt:

| Beat | Funktion bei Zonkfruit | Szenentyp |
|---|---|---|
| Hook | sofortige Bildpointe in den ersten 2 s (etwas prallt ab, kippt, scheitert) plus große Behauptung | `zonk_scan`, Modus `hook` (in `scenes.py` als Hook-Szenentyp erlaubt) |
| Problem | Plümos Denkfehler, sichtbar gemacht | `zonk_word` (Wortkarte, Teil durchgestrichen, zwei Urteile) |
| Erklärung | die echte Regel, als Schnittbild oder Schema | `zonk_diagram` (Plümo zeigt mit dem Blatt) |
| Demonstration | der Beweis unter der Lupe | `zonk_zoom` (Lupe, Callouts, Fachbegriff-Stempel) |
| Erkenntnis | Gegenprobe: was stattdessen gilt | `zonk_scan` Modus `accept` (Zähler) |
| Nutzen | „Merke“-Satz, dann probiert Plümo es selbst und kippt um | `zonk_scan` Modus `unknown` (Etikett „?“, PLUMPS) |
| Abschluss | Plümo bleibt liegen, Kanalaufruf, steht auf | `zonk_loop` |

- **Schnelle, aber lesbare Schnitte:** etwa alle 0,8–1,5 s ein Bildereignis (Hüpfer, Stempel, Label, Mimikwechsel). Der gemeinsame Prüfpunkt `visual_cuts_rhythm` (Ziel 1,2–8 s) meldet bei Zonkfruit deshalb absichtlich eine Warnung; hart ist nur `visual_cuts_static` (keine Strecke über 14 s ohne Bildwechsel). Jede Texteinblendung bleibt mindestens bis zum Ende ihres Satzes stehen.
- **Klare visuelle Pointe:** jede Folge hat einen Moment, der ohne Ton verständlich ist (Stempel ABGELEHNT, Umkippen, Etikett „?“).
- **Wiedererkennbarer Loop:** Plümo endet umgekippt, steht im Abschluss auf und hüpft an seinen Startplatz; die letzten 0,6 s entsprechen dem ersten Bild des Hooks (gleiche Bühne, gleiche Position, Kugeln in Ruhelage).
- **Running Gags:** „Sorte: nicht ermittelbar“ (Etikett auf dem Rücken), er hat keine Hände und zeigt mit dem Blatt, „Ich steh gleich wieder auf.“
- **Szenen synchron zur Stimme:** Jede Szene kennt Stichwörter (`cue_*` im Plan); sie findet sie in `SceneCtx.words` (Wortzeiten aus faster-whisper); Stempel, Labels und Effekte erscheinen beim gesprochenen Wort.

## 5. Ton

- **Stimme:** Gemini Flash TTS (`gemini-2.5-flash-preview-tts`), Stimme **Puck** für DE und EN. Plümo spricht selbst, in der Ich-Form. Stilanweisung: kleine, trockene Comicfigur, deadpan, kurze Pause vor jeder Pointe, nie gemein.
- **Soundeffekte:** acht selbst synthetisierte Klänge (boing, pop, whoosh, scan, buzz, chime, unknown, plumps), Lautstärke 0,15–0,4 unter der Stimme, von den Szenen selbst gesetzt (Tonspuren ab 20, damit sie die Spuren 13–17 der Erklärschicht nicht berühren; im Manifest unter `brand_sfx`); Lizenz `assets\sfx\LICENSE.md` (eigene Arbeit, keine Rechte Dritter). Lautheit des fertigen Videos −16 LUFS.
- **Keine Musik**, bis eine Lizenzquelle gewählt und in `08 Recht und Verwaltung\Lizenzen` belegt ist.

## 6. Inhaltsregeln

- Humor ohne Herabsetzung von Personen oder Gruppen; keine realen Personen, keine Marken, keine kopierten Memes, keine Fremdfiguren. Andere Früchte erscheinen nur als Gegenstände ohne Gesicht; nur Plümo hat ein Gesicht.
- Jede Tatsachenbehauptung mit Quelle (URL, Abrufdatum) im Plan; Unbelegtes in `unverified`, nicht ins Video. Quellen in `post.json` und `Veröffentlichung.md` und seit Fassung V2 auch im Bild (Quellenleiste der Erklärschicht, Abschnitt 3a).
- Hook-Engine: fünf Kandidaten (Frage, Denkfehler, überraschender Fakt, konkretes Risiko, Demonstration), Wahrheit mindestens 4.
- Keine Gesundheits- oder Heilversprechen, nichts Gefährliches zum Nachmachen (z. B. bei Blitz: „bei Gewitter drinnen bleiben“).
- Jedes Video als KI-Inhalt gekennzeichnet (`is_aigc`, `is_ai_generated`, `containsSyntheticMedia`). Plümo ist erkennbar eine Cartoonfigur, also kein Deepfake im Sinne von Art. 50 AI Act (Leitlinien C(2026) 5054, laut Übergabebericht Abschnitt 6.4).
- Länge 65–90 s. Messwert Testvideo: 162 Wörter ergaben mit der Windows-Entwurfsstimme 83,7 s Sprache und 86,5 s Video; für Puck (Gemini) noch nicht gemessen. Ziel daher 150–170 Wörter; ist die Gemini-Fassung zu kurz oder zu lang, `tail_seconds` anpassen und mit `--reuse-voice` neu rendern (ohne Kosten).

## 7. Parameter (Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 500, "caption_width_px": 800, "caption_transform": "none",
           "outro": false, "tail_seconds": 2.4, "progress_y": 1550, "ai_label_bottom_px": 318, "status_y": 1440,
           "status_bar": {"file": "Beerenclub", "states": [{"beat": "b1", "text": "Erdbeere: abgelehnt", "tone": "pop", "offset": 2.1}, ...]},
           "caption_mode": "phrases", "caption_max_words": 4,
           "description": "...", "companion_text": "...", "hashtags": [...],
           "platform_texts": {"tiktok": {...}, "instagram": {...}, "youtube": {...}}},
"assets": {}
```

Szenendaten (Auszug, vollständig im Beispielplan): `zonk_scan` als Hook mit `mode: "hook", head, items[{kind}]`; `zonk_word` mit `word_a, word_b, left, right, cue_*`; `zonk_diagram` mit `headline, labels[{text, pos: tr|l|b, cue}]`; `zonk_zoom` mit `kind, callouts[{text, cue}], stamp{text, cue}`; `zonk_scan` mit `mode: accept|unknown|reject, items[{kind, word}], merke, display, cue_*`; `zonk_loop` mit `cta, cue_cta, cue_up`. Früchte im Code: `strawberry`, `banana`, `tomato`, `grape` (weitere als SVG in `fruit_svg` ergänzen). Textgrenzen: Hook-Titel 44, Überschrift 40, Labels 28, Chips 26, Stempel 16, Anzeige 26 Zeichen.

## 8. Ablauf je Video

1. Thema aus `data\calendars\brainrot_2026-11.json` wählen, Quellen erneut öffnen, Plan `data\direction\brainrot-<JJJJMMTT>-<n>-de.json` schreiben (Vorlage: Beispielplan).
2. Trockenlauf ohne Kosten und ohne Stimme (Layout, Wortanker, Erklärschicht):
   `.venv\Scripts\python.exe brands\brainrot\renderer\render_zonkfruit.py data\direction\<id>.json --version dry --tts mock --no-render`
   Standbilder: `npx hyperframes snapshot project -o stills --at <Sekunden,...> --no-end` im Ordner `storage\direction\<id>-dry`. Prüfen: nichts überdeckt, Kicker, Marker und Quelle lesbar, nichts Wichtiges rechts ab x 930.
   Storyboard nach der Layout-Vorlage in `05 Produktion\<Ordner>\01 Skript\Storyboard.md`.
3. Vertonung und Render (eine Gemini-Anfrage; der Starter wartet auf `data\render.lock`):
   `... render_zonkfruit.py data\direction\<id>.json --version V1 --tts gemini --mirror zonkfruit/<datum>-V1`
4. Korrekturen ohne neue Kosten: `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`
5. Produktionsordner: `.venv\Scripts\python.exe brands\brainrot\renderer\export_zonkfruit.py data\direction\<id>.json --version V1 --short "<Kurztitel>"`
6. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`, nichts veröffentlichen.

Vorher: `fn.cli status` (mindestens 30 GB frei auf C:). Bei Gemini-Fehler 429 (Kontingent, laut Scutoria-Vorlage 10 Anfragen je Tag im kostenlosen Kontingent) nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme (Regel Stefan, 30.10.2026).

## 8a. Stand Testvideo (30.10.2026)

- Thema „Die Erdbeere ist keine Beere“ (Plan `data\direction\brainrot-20261105-1-de.json`, Quellen Uni Potsdam und wissen.de), Hook H1 (Denkfehler, Score 96, Wahrheit 5).
- Gemini-Vertonung scheiterte mit 429 (kostenloses Tageskontingent, 10 Anfragen je Tag für `gemini-2.5-flash-tts`, von den parallelen Marken verbraucht). Wie vorgegeben nicht wiederholt; Video mit Windows-Entwurfsstimme (SAPI) gerendert: 86,5 s, Prüfbericht alle Prüfungen bestanden außer `tts_provider_publishable` (Entwurfsstimme), Warnung `visual_cuts_rhythm` (Median 1,0 s, gewollt), Lautheit −16,1 LUFS, Spitze −1,5 dB.
- Seit 30.10.2026 abends gilt: keine Windows-Stimme mehr. Die Entwurfsdatei liegt deshalb in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-30 Layout-Umstellung\Zonkfruit`, und `04 Export` bleibt leer bis zur Gemini-Endfassung.
- Fassung V2 (Erklärschicht, Abschnitt 3a): Plan, `brand.yaml` und Szenen sind umgestellt, das Storyboard liegt in `01 Skript\Storyboard.md`.
  - Geprüft nur per Trockenlauf mit Platzhalterstimme (`--version V2dry --tts mock --no-render`): Lint und Layout ohne Fehler, Richtungsprüfungen bestanden, Warnung `visual_cuts_rhythm` (gewollt).
  - Standbilder liegen in `storage\direction\brainrot-20261105-1-de-V2dry\stills` und `stills2`.
- Endfassung: Die Hauptsitzung vertont alle Videos mit Gemini und rendert die Endfassung, zum Beispiel `render_zonkfruit.py ... --version V2 --tts gemini --mirror zonkfruit/2026-11-05-V2`, danach `export_zonkfruit.py ... --version V2 --short "Erdbeere keine Beere"` (ohne `--draft`).

- **Fassung Q1 (Qualitätsrunde, 30.10.2026, 23:33 Wien), exportiert:**
  - Gemini-Stimme Puck aus V2 mit `--reuse-voice` übernommen, Sprechtext unverändert, Kosten 0 USD. Länge 73,5 s.
  - Prüfbericht VALIDATED, Lint und Layout ohne Fehler. Lautheit −15,0 LUFS. Warnung `visual_cuts_rhythm` (75 Ereignisse, Median 0,8 s) ist gewollt.
  - `overlap_check.mjs` ohne Befund.
  - Export: `05 Produktion\Tintora\2026-11\2026-11-05 Erdbeere keine Beere\04 Export\2026-11-05 Erdbeere keine Beere – 9x16.mp4`. Kontaktbogen in `05 Thumbnail und Cover`.
  - Die alte V2-Datei und die alten Begleitdateien liegen in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde\Zonkfruit V2 Export`. Code, Plan, Storyboard und Vorlage vor Q1 liegen in `...\Zonkfruit-Code-vor-Q1`.
  - Bekannte Abweichung im Loop: Die gemeinsame Statusleiste steht im letzten Bild, im ersten noch nicht. Ein Ausblenden am Ende bräuchte eine Änderung am gemeinsamen Renderer.

## 9. Offen für Stefan

- Figur Plümo freigeben oder Änderungen nennen (Name, Farben, Merkmale).
- Vorlage 0.9 freigeben; danach `brand_version: "1.0"`.
- Zweites Thema als Wiederverwendungstest (Codex-Abnahmeregel), z. B. Tag 2 „Der Seestern ist gar kein Fisch“.
- Englische Fassung (zweite Vertonung, ca. 0,02 USD) erst nach Freigabe.

## 10. Bekannte Grenzen

- Seit 30.10.2026 abends lädt der gemeinsame Renderer `brands\brainrot\scenes.py` selbst (Typen gelten nur für Zonkfruit); der frühere Wrapper, der gemeinsame Register zur Laufzeit veränderte, ist ersetzt.
- Neue Früchte oder Requisiten brauchen eine SVG-Zeichnung in `zonk_templates.fruit_svg`.
