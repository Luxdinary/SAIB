# Vorlage Promptwerk – Version 0.9

Stand: 30.10.2026 (Wien). Erstellt von der Kanal-Sitzung Promptwerk (Claude Code). Mit dieser Datei kann jede Sitzung Promptwerk-Videos nur mit Claude Code und dem lokalen Renderer reproduzieren. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`claude_workflows`, `brand_version: "0.9"`, `template_doc`). Version 1.0 erst, wenn Stefan das Testvideo gesehen hat.

Erstes Testvideo: `05 Produktion\Promptwerk\2026-11\2026-11-06 Claude-Code-Hooks\` (Thema „CLAUDE.md ist eine Bitte, ein Hook ist ein Gesetz"). Noch ohne Endfassung: Die Gemini-Vertonung und den Endrender macht die Hauptsitzung. Layout-Standbilder des Trockenlaufs: `C:\Automation\faceless-network\storage\direction\claude_workflows-20261106-2-de-V2dry\`; Storyboard im Produktionsordner unter `01 Skript\Storyboard.md`.

## Bausteine

| Baustein | Ort |
|---|---|
| Szenentypen (Code) | `C:\Automation\faceless-network\brands\claude_workflows\scenes.py`, geladen über `fn.render.brand_scenes` (Eintrag `scenes:` in `brand.yaml`) |
| Marke | `brands\claude_workflows\brand.yaml` (Palette, Schriften, Abschlusssatz), `subtitle_style.json`, `audio_style.yaml` |
| Regie-System | `docs\direction-system.md` (Hook-Engine, Story-Engine, Prüfungen) |
| Beispiel-Plan | `data\direction\claude_workflows-20261106-2-de.json` |
| Demo-Projekt (Referenz zum Nachprüfen) | `brands\claude_workflows\assets\ui\demo-projekt\` (CLAUDE.md, `.claude\settings.json`, Hook-Skript, `env.beispiel`) |

## Bildsprache „Clean SaaS, didaktisch"

Ein App-Fenster ist die Bühne (Editor, Doku-Seite, Terminal). In jeder Szene passiert dasselbe Lehrmuster: ein violetter Textmarker fährt über die entscheidende Zeile, der Mauszeiger klickt sie an, die Kamera zoomt darauf, eine kurze Erklärblase oder ein Stempel ordnet ein. Keine Folienkarten mit Fließtext. Seit Q1 (Qualitätsrunde, 01.11.2026) hat der Hintergrund Tiefe, nur aus Code (`LAYER` in `scenes.py`): Punktraster unter weichem Licht, ein Bodenraster in Perspektive, das langsam auf den Zuschauer zuläuft, unscharfe Code-Splitter in drei Tiefenebenen mit Parallaxe, Filmkorn, Randschatten und ein Lichtkegel hinter der Bühne, dessen Farbe der Statusleiste folgt (Bernstein offen, Violett eingerichtet, Grün geschützt, Rot Fehler).

### Palette

Grundfarben aus `brands.yaml` übernommen (bg, accent, text, surface, muted). Begründung, sie zu behalten: Violett grenzt Promptwerk sichtbar von Anthropics eigenem Orange ab, damit kein Eindruck eines offiziellen Kanals entsteht, und unterscheidet die Marke vom Blau von Scutoria. Ergänzt um Fenster-, Terminal-, Signal- und Code-Farben.

| Rolle | Hex | Einsatz |
|---|---|---|
| bg | `#171923` | Grund, Punktraster |
| window | `#1E2029` | Editor- und Doku-Fenster, Karten |
| terminal | `#101218` | Terminal-Fenster, Statusleiste |
| surface | `#272932` | Tasten, Übersetzungsbox |
| accent | `#A78BFA` | Marker, Cursor-Klick, Hervorhebung, Logo, Fortschritt, „Gesetz" |
| text | `#F8FAFC` | Text |
| muted | `#93959A` | Zeilennummern, Nebenbeschriftung, „Bitte" |
| signal_amber | `#FBBF24` | nur offene Frage (Hook-Chip, Statusleiste „offen") |
| signal_red | `#F87171` | nur Fehler- und Sperrzeilen im Terminal, Stempel „exit 2" |
| signal_green | `#4ADE80` | nur erreichter Schutz (Schloss, Statusleiste „gesperrt") |
| Code | key `#C4B5FD`, str `#86EFAC`, punc `#94A3B8`, com `#7C8294` | Syntaxfarben in Editor-Szenen |

### Schriften (alle SIL OFL 1.1, Dateien und Lizenzen im Repository unter `assets\fonts\`)

- Inter 800 für Fragen, Überschriften, Abschluss; Inter 600–700 für Text und Untertitel.
- JetBrains Mono für Code, Dateinamen, Terminal, Statusleiste, Tabs.

### Logo

Kleines Zeichen oben links ab dem ersten Bild: violette Kachel mit Prompt-Pfeil und Unterstrich, daneben „Promptwerk" in Inter 800. Das Zeichen wird per CSS gezeichnet (`scenes.py`, Regel `.logo-inner .mark`). Eine SVG-Datei dafür hat der Sicherheitsfilter (Sage) am 30.10.2026 beim Schreiben blockiert; das wurde nicht umgangen. Kein Logo-Intro, keine Endkarte.

## Szenentypen (`scenes.py`)

Alle Szenen liegen in der Inhaltszone (x 108–972, seit Q1 y 372–1100). Ereigniszeiten folgen der Stimme: `<ereignis>_word` verankert ein Ereignis am ersten gesprochenen Wort, das so beginnt (Wortzeiten aus faster-whisper); sonst `<ereignis>_at` in Sekunden ab Szenenbeginn; sonst ein fester Anteil der Szenendauer.

| Typ | Rolle in der Story | Was passiert | Daten (Auszug) | Wortanker |
|---|---|---|---|---|
| `pw_hook` | hook (Pflicht) | Editor mit Regeldatei; Zeilen erscheinen, Marker auf der Fokuszeile, Klick, Zoom 1,1×; große Frage oben (außerhalb des Zooms); amberfarbener Chip in der Titelleiste | `question` (≤64), `chip` (≤22), `tabs`, `lines` (≤30 Zeichen), `focus_line` | `mark_word`, `click_word`, `question_word` |
| `pw_doc` | problem | Doku-Seite (Quelle, Seitentitel, angedeutete Textzeilen), bis zu zwei kurze wörtliche Zitate bekommen nacheinander den Marker, deutsche Übersetzung erscheint darunter | `kicker`, `page_title`, `quotes` (≤70, wörtlich, unter 15 Wörtern), `translation` | `quote1_word`, `quote2_word`, `translation_word` |
| `pw_flow` | explanation | senkrechte Ablaufschiene, Token läuft durch, jeder Punkt pulst, ein Punkt bekommt Rahmen und Chip | `headline` (≤48), `nodes` (≤22), `gate`, `chip` | `travel_word`, `gate_word` |
| `pw_editor` | demonstration | Konfigurationsdatei tippt sich Zeile für Zeile, Marker und Klick auf die Fokuszeile, Zoom 1,12×, Erklärblase unter dem Fenster | `tabs`, `lines` (≤40), `focus_line`, `callout` (≤30) | `mark_word`, `click_word`, `callout_word` |
| `pw_terminal` | demonstration (Kern: UI-Demo) | Claude-Code-Sitzung: Prompt tippt sich, Werkzeugaufruf, Hook-Meldung, rote Sperrzeile mit Marker, Klick, Zoom, Stempel, Anmerkung; „Animierte Darstellung" im Fenster | `title`, `lines` (≤38, `kind` prompt/tool/dim/err, je `at_word`), `focus_line`, `stamp` (≤10), `annotation` (≤34), `height`, `focus_x` | `mark_word`, `click_word`, `stamp_word`, `annotation_word` |
| `pw_compare` | insight | zwei gestapelte Karten: Dateichip, Urteil („Bitte" grau, „Gesetz" violett), je zwei Zeilen; die obere Karte tritt zurück, wenn die untere kommt | `top`/`bottom` mit `title` (≤22), `verdict` (≤10), `rows` (≤26) | `bottom_word` |
| `pw_steps` | benefit | bis zu drei Schritte mit Tastenkappe, Titel und dem exakten Namen in Mono; jeder leuchtet auf seinem Wort auf | `headline`, `steps[{title (≤28), code (≤32)}]` | `at_word` je Schritt |
| `pw_close` | close | kleines Terminal mit der Sperre, grünes Schloss in der Titelleiste, Merksatz, darunter Markenzeile; hält bis zum letzten Bild | `lines`, `badge` (≤24), `statement` (≤56), `claim` (≤40) | `statement_word`, `brand_word` |

Seit Q1 zusätzlich (alle freiwillig): `pw_hook` `env_word` (Tab der Datei leuchtet bernstein, offenes Schloss), `chip_word`, `line_h` (Standard 70), Fenster sitzt unten in der Zone, Frage darüber (74 px); `pw_doc` `page_word` (Unterstrich unter dem Seitentitel); `pw_flow` ohne `headline` (Titel kommt aus `overlay.title`), `shell_chip` + `shell_word` (Chip „$ …“ am Hook-Punkt bis zum Tor), Schienenkarte als Hintergrund; `pw_editor` `line_h`, `pre_line` + `pre_word` (leiser zweiter Marker); `pw_terminal` `file` + `file_open_word` + `file_word` (Datei-Chip mit Schloss im Fensterkopf, schließt grün), `top`; `pw_compare` `lock_word` (Schloss vor dem zweiten Urteil), zweite Karte steht von Anfang an als Umriss; `pw_steps` ohne `headline` (Schritte senkrecht mittig). Jede Szene hat eine Kamerafahrt (Push-in 4,5 %).

`pw_terminal` und `pw_close` schreiben „Animierte Darstellung" ins Fenster. Sie melden kein `schematic_ui` mehr, weil Stefan am 30.10.2026 entschieden hat: keine Bildschirmaufnahmen, die UI-Szenen sind Animationen. Die geteilten Szenentypen (`data_flow`, `comparison` …) sind weiter erlaubt, wirken aber wie Scutoria und werden für Promptwerk nicht genutzt.

## Regeln

- Ein durchgehendes Objekt als roter Faden: die Datei oder der Gegenstand, um den es geht (im Testvideo `.env`). Er steht als Tab in jedem Fenster und in der Statusleiste unten (`layout.status_bar`), je Beat ein Zustand. Töne: `amber` offen, `muted` neutral, `accent` eingerichtet, `ok` (grün) Schutz greift, `red` Fehler.
- Jede Szene hat ein Fenster oder eine Karte als Hauptmotiv in der Bildmitte; Marker, Klick und Zoom sind das Wiedererkennungszeichen. Keine Folienkarten mit Fließtext.
- Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), Inter 700, 58 px, Hervorhebung violett, normale Schreibweise.
- Logo klein oben links ab Bild 1; „KI-generiert" dauerhaft; keine URL-Zeilen im Bild, Quellen in `post.json` und `Veröffentlichung.md`.
- Abschluss in der Handlung (`pw_close`): die gezeigte Sperre bzw. das Ergebnis bleibt sichtbar, Merksatz, Markenzeile mindestens 4 s lesbar. Gesprochen: „Mehr Claude-Workflows Schritt für Schritt: Folge Promptwerk." Keine Website (keine bestätigte Domain), kein Handle.
- Anrede „du". Ton: präzise, freundlich, ohne Hype. Keine Versprechen über Modellverhalten, das nicht getestet ist; „getestet" nur sagen, wenn der Workflow tatsächlich mit der genannten Claude-Code-Version gelaufen ist (Markenregel). Das Wort „garantiert" löst die Richtlinienprüfung aus; Quellen-Sinn mit „eine Garantie gibt es nicht" wiedergeben.
- Zitate aus der Anthropic-Dokumentation nur wörtlich und kurz (unter 15 Wörtern), Originalsprache plus deutsche Übersetzung.
- Jede Aussage mit Primärquelle (Anthropic-Dokumentation, URL, Abrufdatum); Unbelegtes in `unverified`, nicht ins Video. Grenzen des gezeigten Workflows in der Beschreibung nennen (Beispiel: Matcher `Edit|Write` erfasst keine Bash-Befehle).
- Länge 65–90 s; 165–170 Wörter ergaben mit der früheren Entwurfsstimme 77,9 s (Mock-Schätzung 77,0 s). Mit Gemini (Stimme Kore, Rate 1,05) ist die Länge erst nach der Vertonung bekannt; der Renderer bricht außerhalb 65–90 s ab.
- Story: Hook → Problem → Erklärung → Demonstration (gern zweimal: Konfiguration, dann Terminal) → Erkenntnis → Nutzen → Abschluss; fünf Hook-Kandidaten, je einer pro Typ, Wahrheit mindestens 4.

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 372, "zone_h": 728, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4,
           "status_bar": {"file": "<Objekt>", "states": [{"beat": "b1", "text": "...", "tone": "amber"}]},
           "description": "...", "companion_text": "...", "hashtags": ["claudecode", "..."]}
```

Kein `assets`-Block (Fassung nur mit Claude Code, keine Clips). Seit Q1 beginnt die Szenenzone bei y 372 (V2: 310), weil der Kopftitel jetzt 64 px groß, mittig und bis zu zwei Zeilen lang ist (y 186–361; Kicker links darüber). Szenen mit eigener Überschrift (`pw_flow`, `pw_steps`) lassen `headline` leer und nutzen `overlay.title` (höchstens 26 Zeichen), damit alle Titel an derselben Stelle stehen.

## Qualitätsrunde Q1 (01.11.2026)

Auftrag: Scutoria-Niveau (Stefans Note 1,7 für „KI-Kennzeichnung“), Briefing `02 Marke\Qualitätsrunde 2026-10-31.md`. Umgesetzt im Szenencode, gilt für jedes weitere Promptwerk-Video:

- Hintergrund mit Tiefe nur aus Code (siehe Bildsprache), keine Clips, keine KI-Bilder.
- Leitobjekt: die Datei, um die es geht (im Testvideo `.env`), mit Schloss. Offen und bernstein, solange nichts erzwungen ist; grün und geschlossen, sobald die Sperre greift. Sie steht im Tab (Hook), als Datei-Chip im Terminal, auf der Karte „Gesetz“ und mit Schloss in der Statusleiste (`.st-amber` offen, `.st-ok` zu).
- Größe: Szenenzone y 372–1100, Hauptmotiv füllt die Breite (864 px) und den größten Teil der Höhe; Kopftitel groß und mittig.
- Bewegung: mindestens drei Bildereignisse je Szene an gesprochenen Wörtern, Kamerafahrt je Szene, Kreisübergänge aus einem Objekt.
- Prüfen: Trockenlauf mit der vorhandenen Gemini-Aufnahme (`--reuse-voice … --no-render`) statt Mock, weil dann die Wortzeiten stimmen; Standbilder mit `npx hyperframes snapshot`; nach dem Render `node scripts\overlap_check.mjs <projekt>` und Kontaktbogen.
- Vorher-Stand V2 gesichert unter `C:\Automation\faceless-network\storage\direction\claude_workflows-20261106-2-de-V2\stand_V2\`.

## Erklärschicht (seit 30.10.2026, Fassung V2)

Gemeinsame Regeln: `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`; Code `src\fn\render\explainer.py`. Für Promptwerk eingeschaltet in `brands\claude_workflows\brand.yaml`:

```yaml
explainer:
  enabled: true
  voice_tag: {de: SYNTHETISCHE STIMME, en: SYNTHETIC VOICE}
  opening: {de: "Synthetische Stimme · Quellen am Bildschirm · Terminal animiert", en: "Synthetic voice · Sources on screen · Terminal is animated"}
  opening_seconds: 3.5
  source_y: 1112
  colors: {fakt: "#A78BFA", auslegung: "#F0ABFC", unsicher: "#FBBF24", luecke: "#F87171", beispiel: "#8A93A6"}
```

- **Farben:** Fakt = Markenakzent Violett, weil das die aktive Farbe der Szenen ist (Marker, Cursor, Klick, „Gesetz"). Da die ganze Marke violett ist, steht Auslegung abweichend von der Regel „Violett nur für Auslegung" als helles Orchidee `#F0ABFC`; Form (Raute) und Wort unterscheiden zusätzlich. Bernstein nur für Offenes (Hook-Chip, Status „nicht erzwungen"), Rot nur für das abgewehrte Risiko (Sperrzeile im Terminal), Grün nur für den erreichten Schutz (Schloss, Status „gesperrt"). Der Stempel „exit 2" ist seit V2 violett (Vorgang), nicht mehr rot.
- **Lage:** Szenen y 372–1100 (seit Q1; V2: 310), Marker y 1112, Quellenleiste y 1168 (höchstens zwei Zeilen), Untertitel ab etwa y 1310, Statusleiste y 1440. Rechts bleibt alles links von x 930 (Quellenleiste) bzw. 940 (Statusleiste). Elemente, die beim Zoom nach unten wandern könnten (Erklärblase in `pw_editor`), liegen außerhalb des Zooms.
- **Wann welcher Marker:** belegte Szenen (problem, explanation, demonstration, benefit) „Fakt" mit Quelle; Merkbilder und Vergleiche wie „Bitte oder Gesetz" „Auslegung" (ohne Quellenleiste); Szenen mit erfundenen Pfaden, Prompts oder Beispieldateien zusätzlich „Beispielwert" (`example: true`); Hook und Abschluss ohne Marker.
- **Kopf:** Szenen mit eigenem Titel (`pw_flow`, `pw_steps`) bekommen nur den Kicker; sonst ein Kopftitel bis 26 Zeichen im `overlay.title`. Der Abschluss hat keinen Kopf (`head: false`).
- **Übergänge:** Kreis (`iris`) nur aus einem Objekt heraus: aus dem ersten Punkt der Ablaufschiene (x 241, y 532) und aus der Matcher-Zeile in das Terminal (x 400, y 588); sonst Überblendung 0,7 s. Nahaufnahme ins Terminal mit `vignette: true` und `dim_at` am Wort der Sperre.
- **Quellen-Labels:** `sources[].label`, zum Beispiel „Claude-Code-Doku, Hooks", „Claude-Code-Doku, Memory".
- **Wortanker:** Overlay mit `w:Wort` (`marker_at`, `dim_at`, `head_at`), Szenenereignisse mit `<ereignis>_word` (siehe Szenentypen). Jede Bildaktion hängt an einem gesprochenen Wort.
- **Storyboard** je Video in `01 Skript\Storyboard.md` (Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild), Muster: `05 Produktion\Promptwerk\2026-11\2026-11-06 Claude-Code-Hooks\01 Skript\Storyboard.md`.

## Ablauf je Video

Im Ordner `C:\Automation\faceless-network`, PowerShell, vorher `$env:PYTHONIOENCODING = "utf-8"`.

1. Plan `data\direction\<video_id>.json` schreiben (Vorlage: Beispiel-Plan), Quellen gegen die Anthropic-Dokumentation prüfen, Trockenlauf:
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --no-render --mirror promptwerk-regie/dry`
2. Standbilder ansehen (ohne Render): `npx hyperframes snapshot . --at 1,5,10,... --no-end -o <absoluter Pfad>` im Ordner `storage\direction\<id>-dry\project`.
3. Sperrdatei `data\render.lock` prüfen (jünger als 20 Minuten: warten), anlegen, freien Platz prüfen (`fn.cli status`, mindestens 30 GB), dann Vertonung und Vollrender (eine Gemini-Anfrage):
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version V1 --tts gemini --mirror promptwerk-regie/<datum-kurztitel>`
   Danach `data\render.lock` entfernen. Korrekturen ohne neue Kosten mit `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`.
4. Produktionsordner: `.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\<id>.json --version V1 --short "<Kurztitel>"`
5. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`, nichts veröffentlichen.

Grenze: Der Gemini-Schlüssel läuft im kostenlosen Kontingent, höchstens 10 Anfragen je Tag für `gemini-2.5-flash-tts` (429 am 30.10.2026). Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme (Stefans Regel vom 30.10.2026). Layout prüfen nur mit Trockenlauf ohne Stimme: `--version <V>dry --tts mock --no-render`, Standbilder mit `npx hyperframes snapshot` im Projektordner des Trockenlaufs.

## UI-Szenen als Animation (Stefan, 30.10.2026)

Stefan macht keine Bildschirmaufnahmen. Alle Oberflächen (Editor, Terminal, Doku-Seite) sind Animationen aus `scenes.py`. Regeln dafür:

- Terminal-Fenster tragen „Animierte Darstellung", die Einstiegszeile sagt „Terminal animiert". Pfade, Prompts und Beispieldateien bekommen den Chip „Beispielwert".
- Gezeigt wird nur, was die Anthropic-Dokumentation beschreibt (Dateinamen, Konfiguration, Ereignisse, Meldungen wie die `Blocked:`-Zeile des Doku-Skripts). Wie die Claude-Code-Oberfläche etwas genau anzeigt, ist nicht belegt; die Animation behauptet kein exaktes Aussehen. In der Beschreibung steht „animierte Darstellung, keine Bildschirmaufnahme".
- „Getestet" nur sagen, wenn der Workflow tatsächlich mit Claude Code gelaufen ist (Version nennen). Am 30.10.2026 war das nicht möglich, weil die Anmeldung der Claude-Code-Kommandozeile auf dem Laptop abgelaufen war; geprüft war nur das Hook-Skript selbst (Exit-Code 2 für einen `.env`-Pfad). Das Demo-Projekt unter `assets\ui\demo-projekt\` bleibt als Referenz, falls jemand den Ablauf nachprüfen will.

## Offen bis Version 1.0

- Stefan entscheidet zwischen V2 (laut Redaktionsplan am 01.11.2026 freigegeben, liegt in `04 Export`) und Q1 (Qualitätsrunde, gleiche Stimme, VALIDATED, Überschneidungs-Prüfung ohne Befund; Ansicht `05 Produktion\_Demos\promptwerk-regie\2026-11-06-q1\video.mp4`, Kontaktbogen `kontakt.jpg` daneben). Erst danach den Produktionsordner mit `export_production_folder.py … --version Q1 --short "Claude-Code-Hooks" --force` neu füllen (alte Datei vorher nach `Documents\_zum_loeschen\2026-10-31 Qualitätsrunde`).
- Stefan sieht das Testvideo (nach der Gemini-Vertonung durch die Hauptsitzung) und gibt die Optik frei oder nennt Änderungen. Bis dahin zeigen die Standbilder des Trockenlaufs unter `C:\Automation\faceless-network\storage\direction\claude_workflows-20261106-2-de-V2dry\` das Layout.
- Gemini-Vertonung (eine Anfrage, etwa 0,02 USD) nach Rückstellung des Kontingents, dann Endrender mit `--version V2` (macht die Hauptsitzung).
- Englische Fassung (`claude_workflows-20261106-1-en`) mit demselben Plan, lokalisiert, zweite Vertonung.
- Wiederverwendung mit einem zweiten Thema testen (Vorschlag: Deny-Regeln, Kalender 07.11.), bevor 1.0 festgelegt wird.
