# Produktion Woche 1 (09.–15.11.2026)

Stand: 01.11.2026 (Wien). Auftrag von Stefan am 01.11.2026: „Woche 1 starten“. Grundlage sind die freigegebenen Themen- und Kalenderpläne (`Themen- und Kalenderplan <Marke> (09.11.–06.12.2026).md`).

## Umfang

- Je Marke 7 Tage mit je 3 Themen, jedes Thema auf Deutsch und Englisch. Das sind je Marke 42 Videos und für alle neun Marken 378.
- Nur Themen im Status `planned`. Themen im Status `idea` überspringen und im Bericht nennen.
- Reihenfolge: nach Veröffentlichungstermin, je Thema erst Deutsch, dann Englisch.

## Ablauf je Video

1. **Plan:** `C:\Automation\faceless-network\data\direction\<topic_id>.json` mit `video_id` = Topic-ID aus dem Kalender (z. B. `motivation-20261109-1-de`). Aufbau wie das freigegebene Testvideo der Marke: Story-Engine, Hook, Szenentypen der Marke, `overlay` der Erklärschicht, `sources` mit kurzem `label`. Nur Aussagen aus den Quellen des Kalenders. Die englische Fassung ist sprachlich angepasst, keine wörtliche Übersetzung.
2. **Länge:** Ziel 70–85 s. Die Wortzahl richtet sich nach der gemessenen Sprechgeschwindigkeit der Gemini-Stimme der Marke (in der Vorlage-Datei der Marke). Für Englisch die erste Messung festhalten.
3. **Trockenlauf:** `--tts mock --no-render` ohne Fehler.
4. **Vertonung und Render:** eine Gemini-Anfrage (`--tts gemini`), Fassung `V1`, mit dem Renderer der Marke. Liegt die Länge außerhalb 65–90 s, den Text anpassen und neu vertonen, höchstens zweimal. Keine Windows-Stimme.
5. **Prüfen:** Prüfbericht VALIDATED, bei Risiko „high“ HUMAN_REVIEW. `node scripts\overlap_check.mjs storage\direction\<id>-V1\project` ohne Befund. Jedes fünfte Video zusätzlich mit Kontaktbogen gegen das freigegebene Testvideo prüfen; die Qualität darf nicht darunter fallen.
6. **Export:** Deutsch mit `--short "<Kurztitel>"`, Englisch mit `--short "<Kurztitel> EN"`; dann gibt es je Sprache einen eigenen Ordner in `05 Produktion`. Exportskript der Marke verwenden (Suitwerk und Zonkfruit haben eigene).
7. **Nachtragen:** Zeile in `04 Redaktionsplan\Redaktionsplan.csv` mit Status `fertig` (bei Risiko „high“ Notiz „Freigabe Stefan offen“), im Kalender Status `produced`.

## Regeln

- **Ab 01.11.2026 nur noch über die faire Warteschlange rendern:** `.venv\Scripts\python.exe scripts\render_queue.py <brand_id> -- <renderer.py> <args>`. Wer zuerst ansteht, rendert zuerst. `data\render.lock` nicht mehr selbst nehmen oder abfragen. Zonkfruit ruft dabei `scripts\render_direction.py` direkt auf, weil `render_zonkfruit.py` die Sperre selbst nimmt.
- Bei Speicherschutz (unter 30 GB frei) zehn Minuten warten und erneut versuchen.
- Bei Gemini-Fehler 429 oder anderen API-Fehlern: nicht ausweichen, warten, im Bericht nennen.
- Nur die eigenen Markendateien, Pläne und Produktionsordner ändern. Gemeinsamen Code nur lesen, Wünsche an die Hauptsitzung.
- Nichts veröffentlichen, keine Konten, keine Commits, nichts löschen (nach `C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`).
- Zwischenberichte nur bei Problemen; Abschlussbericht, wenn alle Videos der Woche fertig sind: Zahl fertig, übersprungen, Kosten laut `data\costs\costs.jsonl`, Auffälligkeiten.

## Grobe Kapazität

| | Wert |
|---|---|
| Renderzeit je Video bisher | 3 bis 6,5 Minuten |
| Renderzeit für 378 Videos, nacheinander | rund 28 Stunden |
| Gemini-Stimme je Video bisher | etwa 0,02 USD |
