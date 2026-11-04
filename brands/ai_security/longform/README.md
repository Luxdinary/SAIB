# Scutoria Langvideo (16:9) und Reels aus denselben Szenen (9:16)

Stand 02.11.2026. Konzept: `OneDrive\Business\02 Marke\Scutoria\YouTube-Konzept.md`. Markenlokal, weil der gemeinsame
Renderer auf 1080 × 1920 und 65–90 s gebaut ist; gemeinsamer Code wird nur importiert (HyperFrames, ffmpeg, Whisper,
Gemini, Kostenprotokoll), nie geändert.

## Dateien

| Datei | Aufgabe |
|---|---|
| `fmt.py` | die zwei Formate 16x9 und 9x16 mit allen Positionen |
| `blocks.py` | 12 Szenentypen, Textgrenzen (`LIMITS`), CSS je Format |
| `compose.py` | baut ein HyperFrames-Projekt (Kapitel oder Reel): Hintergrund, Schleier, Szene, Marker und Quellenleiste, Kopf, Kapitelkarte, Untertitel (nur 9:16), Stimme |
| `render_long.py` | Ablauf: Stimme je Kapitel (Gemini, Teilung bei 2.800 Zeichen), Wortzeiten (Whisper large-v3), Zeiten, Bau, Prüfung, Render, Verkettung, Kapitelmarken, SRT, Reels |
| `thumbnail.py` | Thumbnail 1280 × 720 aus Higgsfield-Hintergrund und höchstens fünf Wörtern |
| `plans/<NN>-<slug>.<de|en>.json` | ein Plan je Video und Sprache |

## Plan

```json
{"video_id": "yt01-ai-rules-start-de", "lang": "de", "title": "...",
 "sources": [{"id": "S1", "label": "voller Quellentext mit Abruf", "short": "Kurzform für Reels"}],
 "chapters": [{"id": "c1", "num": "1", "title": "Kapiteltitel", "kicker": "1 · Kurz", "card": true, "end_seconds": 0,
   "scenes": [{"type": "paper", "bg": "yt/lib_office_night.mp4", "scrim": 0.62, "new": false,
               "data": {"...": "siehe blocks.py"},
               "say": [{"text": "gesprochener Absatz", "marker": "fakt|auslegung|unsicher|luecke|beispiel", "source": "S1"}]}]}],
 "reels": [{"id": "r1", "chapter": "c1", "title": "...", "kicker": "Aus Video 01 · ...", "scenes": ["c1s1", "c1s2"]}]}
```

- Szenen-IDs entstehen aus der Position: `c1s0`, `c1s1`, …
- Wortanker in `data`: `"@Wort"` oder `"@Wort+0.6"` (erstes Wort der Szene, das so beginnt).
- `fakt` und `unsicher` brauchen eine Quelle, `luecke` nicht (dort fehlt sie ja). Die Quellenleiste steht, solange der Absatz gesprochen wird.
- `new: true` markiert Text, der nicht aus einem freigegebenen Skript stammt (Freigabe nötig).
- Das letzte Kapitel trägt `end_seconds: 20` für das ruhige Endbild (YouTube-Endscreen).

## Aufbau (für die Hauptsitzung, falls er in den gemeinsamen Code wandert)

1. **Plan** je Video und Sprache: Kapitel → Szenen → Absätze (Sprechtext, Marker, Quelle). Szenen sind Daten, keine Videos.
2. **Stimme je Kapitel** (Gemini Charon, Teilung bei 2.800 Zeichen, 0,45 s Pause zwischen Teilen), Zwischenspeicher mit
   Text-Hash in `storage\longform\<id>\voice\`; Whisper large-v3 liefert Wortzeiten, `align_to_script` bindet sie an den Plan.
3. **Zeiten**: Szene beginnt 0,15 s vor ihrem ersten Wort; Bildereignisse über Wortanker `@Wort`. Kapitelkarte 2,4 s vor der Stimme.
4. **Composer** `compose.build(seg, fmt, project)`: ein HyperFrames-Projekt je Kapitel (16:9) oder je Reel (9:16), aus denselben
   Szenen; Formate in `fmt.py`, Szenen in `blocks.py`.
5. **Render**: je Kapitel ein eigener Auftrag in `scripts\render_queue.py` (`--chapters cX --no-concat`), damit andere Marken
   dazwischen drankommen; danach `--concat` ohne Sperre (ffmpeg concat ohne Neukodierung, `chapters.txt`, `captions.srt`,
   `manifest.json` mit `tts.provider` je Kapitel). Reels je eines ein Auftrag (`--reels rN`). `night_run.py` macht das der Reihe nach.
6. **Prüfungen**: HyperFrames-Lint, Textgrenzen, Wortanker, `overlap_check.mjs` je Kapitel und Reel, Gemini-Pflicht im Manifest,
   KI-Kennzeichnung im Bild (oben rechts, Einstiegszeile) und in `Veröffentlichung.md`, Quellenleiste mit Abrufdatum.
7. **Export** `export_long.py` nach `fn.config.production_folder("ai_security", Datum, Kurztitel)`.

Gemessen 02.11.2026: Render-Faktor 1,06–1,37 der Laufzeit (16:9, Standbild-Hintergrund, 4 Worker, NVENC).

## Ablauf

```
.venv\Scripts\python.exe brands\ai_security\longform\render_long.py <plan> --tts mock --no-render --tag dry       # Trockenlauf
.venv\Scripts\python.exe brands\ai_security\longform\render_long.py <plan> --tts gemini --no-render               # nur Stimme und Wortzeiten
.venv\Scripts\python.exe scripts\render_queue.py ai_security -- brands\ai_security\longform\render_long.py <plan> --overlap   # Langvideo
.venv\Scripts\python.exe scripts\render_queue.py ai_security -- brands\ai_security\longform\render_long.py <plan> --reels --overlap  # Reels
```

Ergebnis in `storage\longform\<video_id>\`: `video.mp4`, `chapters\<cid>\video.mp4`, `chapters.txt` (YouTube-Kapitel),
`captions.srt`, `report.json`, `reels\<rid>\video.mp4`. Die Stimme liegt in `storage\longform\<video_id>\voice\` und
wird wiederverwendet, solange der Text eines Kapitels gleich bleibt (keine doppelten Kosten).

## Bibliothek

Higgsfield-Clips und Standbilder 16:9 in `assets\higgsfield\yt\` mit Nachweis, Job und Prompt in
`assets\higgsfield\LICENSE.md`. Clips sind 8-s-Schleifen (Start- gleich Endbild) und werden in Abschnitten wiederholt;
Standbilder bekommen eine langsame Kamerafahrt (Bild vor Video).
