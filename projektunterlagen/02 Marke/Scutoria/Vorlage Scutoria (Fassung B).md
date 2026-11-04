# Vorlage Scutoria (Fassung B) – Version 1.0

> **Ersetzt für neue Videos (02.11.2026):** Stefan hat das Format „Was tust du?“ freigegeben, siehe `Format-Bibel.md` in diesem Ordner. Fassung B gilt nur noch für die bereits exportierten Videos im alten Format und bleibt als Nachweis liegen.

Stand: 30.10.2026, 16:46 (Wien). Von Stefan am 30.10.2026 als Vorlage gewählt. Mit dieser Datei kann jede Sitzung Scutoria-Videos nur mit Claude Code und dem lokalen Renderer reproduzieren, ohne neue Higgsfield-Generierungen. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`ai_security`, `brand_version: "1.0"`).

## Bausteine

| Baustein | Ort |
|---|---|
| Designsystem (nur lesen) | `C:\Users\Stefa\OneDrive\scutoria\design\project\` (`tokens.json`, Markenbuch, Scutum-Marke, Manrope) |
| Renderer-Marke | `C:\Automation\faceless-network\brands\ai_security\brand.yaml` (Scutoria-Tokens, flacher Grund) |
| Clips | `C:\Automation\faceless-network\brands\ai_security\assets\higgsfield\` (8 Clips, `LICENSE.md`, `manifest.json`) |
| Regie-System | `docs/direction-system.md` (Hook-Engine, Story-Engine, Szenentypen, Prüfungen) |
| Beispiel-Pläne | `data/direction/ai_security-20261105-1-de.B.json` (Fassung B), `ai_security-20261106-2-de.json`, `ai_security-20261107-1-de.json` |

## Clips je Szenentyp

Die Asset-Schicht ordnet je Plan einem Szenentyp einen Clip zu (`assets.background`). Clips dürfen sich wiederholen, die Reihenfolge soll von Video zu Video wechseln; zwei gleiche Clips nicht direkt hintereinander.

| Clip | Bild | passt zu |
|---|---|---|
| `bg_hook_dataroom.mp4` | matter Tisch oben, blaue Haarlinie | `cinematic_hook`, `file_fork`, `data_flow` |
| `hero_document_to_chat.mp4` | weißes Blatt gleitet nach oben und stoppt | Hero im Hook (`assets.hero.b1`), **nur wenn ein Dokument das Thema ist** |
| `bg_flow_lanes.mp4` | zwei Haarlinien am Rand, wandernde Segmente | `data_flow`, `file_beside`, `cinematic_hook`, `file_fork` |
| `bg_ui_desk.mp4` | unscharfer Laptop, blasser Bildschirm | `ui_demo`, `cinematic_hook` (Website, Chat), `file_beside` |
| `bg_compare_split.mp4` | Haarlinie in Bildmitte, zwei Flächen | `comparison` |
| `bg_negate_pulse.mp4` | roter Rahmen | **nur** unter einer Sperre (`file_close` mit rotem Block, `comparison` negate) |
| `bg_takeaway_calm.mp4` | mattes Band oben | `key_takeaway` |
| `bg_outro_orbit.mp4` | blauer Kreisumriss dreht sich | `file_close`, Abschluss |

Bisherige Folgen: B (05.11.) dataroom+Hero, lanes, split, desk, split, calm, calm · 06.11. desk, lanes, dataroom, lanes, split, calm, orbit · 07.11. lanes, dataroom, desk, split, lanes, calm, negate.

## Regeln (aus A2/A3.1 und Fassung B)

- Kein Logo-Intro, keine Endkarte; Scutum-Marke klein oben links ab dem ersten Bild; „KI-generiert" dauerhaft im Bild.
- Ein durchgehendes Objekt als roter Faden (z. B. Kundenliste.xlsx, Website-Chat, Firmen-E-Mail) mit Statusleiste unten (`layout.status_bar`): je Beat ein Zustand.
- Farben: Grund #0b1120, Flächen #121b2f/#19243b, Akzent #4f8cff, Text #e9eef8. Amber nur für Offenes (Status `amber`, Marker „Unsicher", Hervorhebungen als Frage formulieren). Rot nur für die konkrete Sperre am Schluss (`file_close`, Status `red`). Kein Neon, kein Glow, keine Schilde, keine Haken bei offenen Risikofragen.
- Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), normale Schreibweise.
- Keine URL-Zeilen im Bild; Quellen in `post.json` und `Veröffentlichung.md`.
- Abschluss in der Handlung (`file_close`): Sperre, scutoria.com mindestens 4 s lesbar, „Belegt. Datiert. Vorzeigbar.", „Quellenbasiert. Keine Rechtsberatung."
- Gesprochener Aufruf: „Mehr KI-Sicherheit für deinen Betrieb: Folge Scutoria." Anrede „du".
- Länge 65–90 s; etwa 165–180 Wörter ergeben mit der Gemini-Stimme Charon 75–80 s.
- Skript nach Hook-Engine (fünf Kandidaten, je einer pro Typ, Wahrheit mindestens 4) und Story-Engine (Hook → Problem → Erklärung → Demonstration → Erkenntnis → Nutzen → Abschluss). Jede Aussage mit Primärquelle (URL, Abrufdatum); Unbelegtes in `unverified`, nicht ins Video.
- UI-Demo (`ui_demo`) nur mit echter Bildschirmaufnahme; ohne sie bleibt der Prüfbericht in HUMAN_REVIEW. Themen ohne UI-Demo erzählen.

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4, "status_bar": {"file": "<Objekt>", "states": [...]}},
"assets": {"background": {"<scene_type>": "<clip>.mp4", ...}, "hero": {}, "scrim": 0.55}
```

## Ablauf je Video

1. Plan `data/direction/<video_id>.json` schreiben (Vorlage: einer der Beispiel-Pläne), dann prüfen:
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --assets --no-render`
2. Vertonung und 15-s-Ausschnitt (Gemini Flash TTS, eine Anfrage):
   `... --version V1 --tts gemini --assets --excerpt 15 --mirror scutoria-serie/<datum>-ausschnitt`
3. Vollfassung ohne neue Kosten:
   `... --version V1 --assets --reuse-voice storage\direction\voice_<id>_V1_gemini.wav --mirror scutoria-serie/<datum>`
4. Produktionsordner füllen:
   `.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\<id>.json --version V1 --short "<Kurztitel>"`
5. Zeile in `04 Redaktionsplan\Redaktionsplan.csv` (Status `fertig`), nichts veröffentlichen.

## Grenze: Gemini-Kontingent

Der Gemini-Schlüssel läuft im kostenlosen Kontingent: höchstens 10 Anfragen je Tag und Modell für `gemini-2.5-flash-tts` (Fehler 429 am 30.10.2026). Jede Vertonung ist eine Anfrage; Wiederholungen mit `--reuse-voice` kosten keine. Für mehr als 10 Vertonungen am Tag braucht es die Abrechnung im Google-Projekt (Stefans Entscheidung).

## Erklärschicht (ab 30.10.2026)

Stefans Schnitt- und Layout-Vorlage ist eingebaut, Regeln in `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`. Scutoria-Werte in `brands\ai_security\brand.yaml` › `explainer`:

- Kicker-Zeile bei y 186; der Szenentitel ist der Kopftitel.
- Oben rechts steht „SYNTHETISCHE STIMME“.
- Einstiegszeile: „Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung“.
- Marker und Quellenleiste liegen bei y 1112, zwischen Szene und Untertitel; die Statusleiste bleibt bei 1440.
- Je Quelle steht ein kurzes `label` im Plan.
- Der Datei-Chip in den Dateiszenen ist aus (`file_marker: none`), weil der untere Marker die Einordnung trägt.
- Kommt Szeneninhalt spät in die Markerzeile, endet der Marker mit `marker_until` vorher.

Stand:

- „KI-Kennzeichnung“ ist als Fassung V2 umgestellt: Prüfbericht VALIDATED, Layoutprüfung ohne Fehler, Gemini-Stimme unverändert. Der Export ist erneuert, die alte Datei liegt in `_zum_loeschen\2026-10-30 Layout-Umstellung`.
- „Passkeys“: Der Plan ist angepasst und geprüft (Trockenlauf ohne Layoutfehler). Gerendert wird nach der Vertonung.
