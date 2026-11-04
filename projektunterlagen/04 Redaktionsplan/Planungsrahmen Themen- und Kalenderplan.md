# Planungsrahmen: Themen- und Kalenderplan je Marke

**Freigegeben von Stefan am 01.11.2026.** Themen im Status `planned` gehen in die Produktion; Themen im Status `idea` erst nach Quellenprüfung; Risiko „high“ vor jeder Veröffentlichung einzeln an Stefan.

Stand: 01.11.2026 (Wien). Grundlage: Stefans Freigabe der neun Testvideos und seine Entscheidung vom 01.11.2026.

## Takt

- Je Konto 6 Posts am Tag: 3 auf Deutsch und 3 auf Englisch, auf demselben Konto.
- Ein Thema läuft als Paar: dasselbe Thema auf Deutsch und auf Englisch am selben Tag. Die englische Fassung ist sprachlich angepasst, keine wörtliche Übersetzung. Je Marke und Tag sind das 3 Themen.
- Uhrzeiten in Wiener Zeit:

| Thema des Tages | Deutsch | Englisch |
|---|---|---|
| 1 | 12:00 | 15:00 |
| 2 | 14:00 | 20:00 |
| 3 | 18:00 | 23:00 |

Die englischen Uhrzeiten zielen auf Großbritannien und die US-Ostküste. Das ist eine Annahme von Claude, Stefan kann sie ändern (`config/brands.yaml` › `slots_by_language`).

## Zeitraum und Umfang

- Erster Plan: 4 Wochen, Montag 09.11.2026 bis Sonntag 06.12.2026. Das sind 28 Tage, je Marke 84 Themen und 168 Posts. Der Starttermin verschiebt sich, wenn die Konten später stehen.
- Puffer laut Fragenkatalog: 7 bis 14 Tage fertige Videos im Voraus.

## Was je Marke entsteht

1. **Themenreihen:** 3 bis 5 wiederkehrende Reihen mit Wochenrhythmus, zum Beispiel „Mythos-Montag“ oder „Nachgerechnet“. Jede Reihe mit Ziel, Format und Beispielthemen.
2. **Kalender:** `C:\Automation\faceless-network\data\calendars\<id>_2026-11.json` im bestehenden Schema. Das Raster erzeugt `.venv\Scripts\python.exe -m fn.cli calendar init <id> --start 2026-11-09 --days 28 --force` (nach dem Verschieben der alten Datei): 6 Zeilen je Tag, Topic-ID `<id>-JJJJMMTT-<n>-<de|en>`. Arbeitsregeln: `prompts\calendar_planner.md`. Die alte Datei vom 30.10. vorher nach `C:\Users\Stefa\Documents\_zum_loeschen\2026-11-01 Kalender alt` verschieben; brauchbare Themen daraus übernehmen.
3. **Lesbarer Plan:** `04 Redaktionsplan\Themen- und Kalenderplan <Marke> (09.11.–06.12.2026).md` mit den Themenreihen und einer Tabelle (Datum, Uhrzeit DE/EN, Reihe, Titel DE, Titel EN, Format, Risiko, Anzahl Quellen, Status). Den alten Entwurf `Themenplan November 2026 – <Marke>.md` nach `_zum_loeschen\2026-11-01 Kalender alt` verschieben.

## Qualitätsregeln

- Jedes Thema mit mindestens zwei Primärquellen, die tatsächlich geöffnet wurden, mit Abrufdatum. Was nicht belegbar ist, bleibt im Status `idea` mit Notiz. Nichts erfinden.
- Kein Winkel doppelt über alle Kalender einer Marke, außer dem DE/EN-Paar.
- Formate über die Woche mischen. Risiko „high“ wartet immer auf Stefan.
- Markenregeln und Tabus aus `config/brands.yaml` und `brands\<id>\script_prompt.md` gelten.
- Prüfung: `.venv\Scripts\python.exe -m fn.cli calendar check --file <datei>` ohne Befund.
- Gemeinsamer Code (`src\fn`, `scripts`) nur lesen. Nichts veröffentlichen, keine Commits, nichts löschen.
