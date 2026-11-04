# Folge 1: Shotliste und Credits je Abschnitt

Stand 02.11.2026, Claude. **Nichts erzeugt, keine Credits ausgegeben.** Vorbereitung für den Ausgabeplan der Hauptsitzung: Für Tintora sind 1.300 Credits vorgesehen, Folge 1 soll etwa 14 min dauern, Tarif ist Ultra. Freigegeben ist das noch nicht.

Grundlagen:
- `Folge 1 Drehbuch.md`: Die Shots von F1-04 bis F1-09 sind per Skript aus den Kennungen gezählt.
- `Pilot-Storyboard.md` für F1-01 bis F1-03, dort mit 8 Video-Shots weniger (siehe unten).

## Annahmen der Rechnung

- **Nur 16:9.** Die Reels entstehen aus der Folge: 16:9-Bild mittig im 9:16-Rahmen, kostet 0 Credits.
- **Video:** Kling 3.0 Omni Frames pro, ohne Ton, 1,25 Credits je Sekunde. Gemessen am 02.11.2026 im Starter. Ob Ultra andere Preise hat, ist **nicht geprüft**; vor dem ersten Auftrag mit `get_cost` abfragen.
- **Bilder:** Nano Banana Pro 2K, 2 Credits je Start-, End- oder Standbild. Dazu für etwa jedes fünfte Standbild ein Zweitbild (Augen- oder Mundwechsel) und je Abschnitt 1 Heftzeichnung.
- **Erwarteter Fall:** Faktor 1,5 auf alles. Gemessen wurden in Stufe 0 1,33 (Bilder) und 1,0 (Videos).
- **Folgendauer** ohne die Teile nur fürs Reel (Rückblick, „Fortsetzung folgt“).

## Tabelle

Stand nach der Korrektur der Sprechzeiten (Prüfrunde 03.11.2026, MUSS 1). Längere Standbild-Shots und Halte-Bilder kosten 0 Credits.

| Abschnitt | Dauer in der Folge | davon Video | Video-Shots | davon Standbild | Bilder | Heft | Sprechtext | Credits netto | erwartet (×1,5) |
|---|---|---|---|---|---|---|---|---|---|
| F1-01 | 98 s | 48 s (49 %) | 10 | 50 s | 12 Start-/End + 9 Stand | 1 | Pilot | 104,0 | 156 |
| F1-02 | 86 s | 46 s (53 %) | 10 | 40 s | 10 Start-/End + 9 Stand | 1 | Pilot | 97,5 | 146 |
| F1-03 | 97 s | 33 s (34 %) | 7 | 64 s | 8 Start-/End + 13 Stand | 1 | Pilot | 85,2 | 128 |
| F1-04 | 107 s | 33 s (31 %) | 6 | 74 s | 6 Start + 11 Stand | 1 | 105 W / 48 s | 77,2 | 116 |
| F1-05 | 92 s | 27 s (29 %) | 5 | 65 s | 5 Start + 11 Stand | 1 | 82 W / 37 s | 67,8 | 102 |
| F1-06 | 90 s | 22 s (24 %) | 4 | 68 s | 4 Start + 10 Stand | 1 | 89 W / 40 s | 57,5 | 86 |
| F1-07 | 95 s | 27 s (28 %) | 5 | 68 s | 5 Start + 10 Stand | 1 | 96 W / 44 s | 65,8 | 99 |
| F1-08 | 89 s | 27 s (30 %) | 5 | 62 s | 5 Start + 10 Stand | 1 | 76 W / 35 s | 65,8 | 99 |
| F1-09 | 91 s | 27 s (30 %) | 5 | 64 s | 5 Start + 10 Stand | 1 | 89 W / 40 s | 65,8 | 99 |
| Vorspann, Abspann | 25 s | 0 | 0 | 25 s | 2 Stand | – | – | 4,0 | 6 |
| neue Schauplatz-Referenzen | – | – | – | – | 7 | – | – | 14,0 | 21 |
| **Summe Folge 1** | **870 s = 14:30 min** | **290 s (33 %)** | | | | | | **704.5** | **1.057** |

**Spanne:** 937 Credits (gemessener Faktor 1,33) · **1057 erwartet** · 1761 vorsichtig (Faktor 2,5).

**Im Rahmen von 1.300:** Der erwartete Fall lässt 243 Credits Reserve. Der vorsichtige Fall läge 461 Credits darüber, siehe Haltepunkte.

## Bild- und Video-Anteil

- 290 s von 870 s sind KI-Video, also **33 %**. Der Rest sind Standbilder mit Kamerafahrt, Parallaxe und Zweitbildern. Das ist im Anime-Stil üblich und hält das Budget.
- Der Pilot (F1-01 bis F1-03) hat mehr Bewegung (41–59 %), weil dort Fest, Raub und Flucht spielen. Die ruhigeren Höhlen- und Lagerszenen (F1-04 bis F1-09) haben 26–32 %.

## Änderung am Pilot-Storyboard: 8 Video-Shots werden Standbilder

| Shot | bisher | neu | Begründung |
|---|---|---|---|
| 1-06 | V 3 s | S, 1 Bild | Juna spricht, kaum Bewegung |
| 1-17 | V 3 s | S, 2 Bilder (Licht an/aus, Überblendung) | gleiche Wirkung |
| 2-09 | V 3 s | S, 2 Bilder (Glas heil/gesprungen) | gleiche Wirkung |
| 2-13 | V 4 s | S, 2 Bilder (Mira/Nebel, Überblendung) | gleiche Wirkung |
| 3-05 | V 3 s | S, 1 Bild | Nicken als Zweitbild |
| 3-06 | V 4 s | S, 2 Bilder (Augen offen/zu) | gleiche Wirkung |
| 3-15 | V 4 s | S, 1 Bild mit Wackeln im Schnitt | einfache Bewegung |
| 3-16 | V 3 s | S, 2 Bilder (Augen zu/auf) | gleiche Wirkung |

Damit sinkt der Pilot von 154 s auf 127 s Video.

## Haltepunkte während der Produktion

1. **Vor dem ersten Auftrag:** Guthaben und die Preise im Ultra-Tarif mit `get_cost` prüfen.
2. **Nach F1-01 bis F1-03:** Verbrauch mit dem erwarteten Wert vergleichen: 156 + 146 + 128 = 430 Credits, mit Schauplatz-Referenzen etwa 450. Liegt er mehr als 20 % darüber, stoppen und den Video-Anteil der übrigen Abschnitte senken.
3. **Harte Grenze:** Bei 1.200 verbrauchten Credits hält die Produktion an und meldet an Stefan, auch wenn die Folge nicht fertig ist.
4. **Animatic vor dem Video:** Stimmen und Standbilder je Abschnitt zuerst zu einem Animatic schneiden. Erst nach dessen Abnahme werden die Videos erzeugt (`Produktionsverfahren.md` 5).

## Optional, nicht im Betrag enthalten

- **Je Reel zwei Shots eigens im Hochformat** (Hook, Cliffhanger): 9 Reels × 2 Shots × (5 s × 1,25 + 2) × 1,5 = etwa 223 Credits. Mit dem erwarteten Fall wären das 1.280 Credits, also kaum noch Reserve. Erst nach Folge 1 entscheiden.
- **Englische Fassung:** dasselbe Bild, nur Stimmen und Einblendungen, also 0 Higgsfield-Credits.

## Stimmen (Gemini)

- Sprechtext Folge 1: Pilot etwa 343 Wörter, F1-04 bis F1-09 zusammen 537 Wörter (per Skript gezählt). Zusammen etwa 880 Wörter, also etwa 400 s Sprache.
- 3 Versuche je Satz: 400 × 3 × 25 Token = 30.000 Token × 9 USD je Mio. = **etwa 0,27 USD** auf Deutsch, etwa 0,54 USD mit Englisch. Preis bis 31.12.2026.
