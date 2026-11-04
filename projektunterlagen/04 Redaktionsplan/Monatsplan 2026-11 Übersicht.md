# Monatsplan 2026-11: Übersicht

Stand 04.11.2026 09:55. Erzeugt von `scripts/month_planner.py` (Tagesläufer-Sitzung), Auftrag der Hauptsitzung nach Stefans Vorgabe vom 03.11.2026, 20:45: je Marke täglich 2 Themen auf Deutsch und Englisch (4 Videos), 7 Tage die Woche. Der Lauf am 04.11. (1 Thema je Marke) bleibt wie geplant.

## Regeln und Annahmen

- **Auswahl:** Konzeptplan-Reihenfolge (zuerst die Tagestabellen, dann die Vorschlagstabelle), ohne schon produzierte Themen (Testvideos, Prototyp, Lauf am 04.11.), nur mit geprüfter Quelle, nur mit gebautem Bildaufbau; Wechsel des Bildaufbaus zwischen den Themen eines Tages und von Tag zu Tag.
- **Slots (Wien, von Stefan am 03.11.2026 bestätigt, änderbar in `config/brands.yaml` unter `slots_by_language`):** Thema 1 DE 12:00, EN 15:00; Thema 2 DE 18:00, EN 21:00. Plattformen je Video: TikTok, Instagram Reels, YouTube Shorts.
- **Revlore:** Technik-Themen zuerst, Motor-Themen höchstens jedes dritte Thema; nur Themen, die `brands/engines/aufbauten.yaml` mit Quellen nennt.
- **Promptwerk:** nur Themen mit vorhandener Aufzeichnung (der Tagesläufer nimmt nichts auf); Stimme DE mit `voice_tts.py --say Claude=Klohd`.
- **Lücken:** Ein Platz ohne Thema bleibt „offen“. Der Monatsplaner erfindet keine Themen; Vorschläge über `claude -p` erst auf Anweisung, immer als „Vorschlag, Quelle prüfen“.
- **Kalenderdateien:** Der Plan liegt in `data/calendars/<id>_2026-11.plan.json` (Schema von `fn.cli calendar init` plus Bildaufbau und Slots). Die vorhandenen `<id>_2026-11.json` bleiben unverändert: Markenwerkzeuge lesen sie und sie enthalten die geprüften Quellen und die Ids der produzierten Videos.

## Zahlen je Marke

| Marke | Konzeptplan | mit Quelle | eingeplant | Plätze | frei | Quelle fehlt | braucht Modell/Aufbau | noch einplanbar | Ersatz-Bildaufbau | Tage mit gleichem Bildaufbau |
|---|---|---|---|---|---|---|---|---|---|---|
| Revlore (`engines`) | 126 | 63 | 5 | 52 | 47 | 0 | 46 | 0 | 0 | 2 |
| Suitwerk (`menswear`) | 68 | 55 | 47 | 52 | 5 | 11 | 0 | 0 | 1 | 0 |
| Scutoria (`ai_security`) | 63 | 34 | 3 | 52 | 49 | 2 | 46 | 0 | 0 | 1 |
| Promptwerk (`claude_workflows`) | 60 | 52 | 12 | 52 | 40 | 0 | 45 | 0 | 0 | 0 |
| Gigastruct (`megaconstruction`) | 96 | 83 | 52 | 52 | 0 | 13 | 0 | 27 | 37 | 26 |
| Gritwerk (`motivation`) | 83 | 71 | 52 | 52 | 0 | 12 | 0 | 15 | 5 | 0 |
| Frontlore (`military_history`) | 70 | 68 | 52 | 52 | 0 | 2 | 0 | 14 | 1 | 0 |
| Dewlane (`beauty`) | 83 | 62 | 52 | 52 | 0 | 21 | 0 | 7 | 0 | 0 |
| **Summe** | | | **275** | **416** | **141** | | | | | |

„Plätze“ sind 2 je Tag über den Planungszeitraum. „frei“ sind Plätze ohne produzierbares Thema; sie füllen sich, wenn die Marken-Sitzungen Bildaufbauten bauen oder Quellen prüfen (dann den Plan neu erzeugen: `scripts/month_planner.py`).

## Lücken je Marke

- Revlore: 5 von 52 Plätzen belegt; 47 offen; braucht Modell, Aufbau oder Aufzeichnung: 46; 04.11. vorgesehen: Nr. 77 Wechselstrom: 100 Richtungswechsel pro Sekunde. Einzelheiten: `Monatsplan Revlore 2026-11.md`.
- Suitwerk: 47 von 52 Plätzen belegt; 5 offen; Quelle fehlt: 11; nicht geeignet: 7; 04.11. vorgesehen: Nr. 1 Stoffgewicht: Was die Zahl wirklich misst. Einzelheiten: `Monatsplan Suitwerk 2026-11.md`.
- Scutoria: 3 von 52 Plätzen belegt; 49 offen; Quelle fehlt: 2; braucht Modell, Aufbau oder Aufzeichnung: 46; 04.11. vorgesehen: Nr. 47 Was ein KI-Chat über deinen Betrieb speichert. Einzelheiten: `Monatsplan Scutoria 2026-11.md`.
- Promptwerk: 12 von 52 Plätzen belegt; 40 offen; braucht Modell, Aufbau oder Aufzeichnung: 45; 04.11. vorgesehen: Nr. 3 CLAUDE.md gegen Hook (Hooks – Regeln, die Claude Code nicht umgehen kann). Einzelheiten: `Monatsplan Promptwerk 2026-11.md`.
- Gigastruct: 52 von 52 Plätzen belegt; Quelle fehlt: 13; 04.11. vorgesehen: Nr. 3 Brenner Basistunnel: 230 km Röhren für 55 km Bahnstrecke. Einzelheiten: `Monatsplan Gigastruct 2026-11.md`.
- Gritwerk: 52 von 52 Plätzen belegt; Quelle fehlt: 12; 04.11. vorgesehen: Nr. 3 Aufgaben mischen statt blockweise üben. Einzelheiten: `Monatsplan Gritwerk 2026-11.md`.
- Frontlore: 52 von 52 Plätzen belegt; Quelle fehlt: 2; 04.11. vorgesehen: Nr. 24 Hadrianswall in Zahlen. Einzelheiten: `Monatsplan Frontlore 2026-11.md`.
- Dewlane: 52 von 52 Plätzen belegt; Quelle fehlt: 21; 04.11. vorgesehen: Nr. 62 Nachcremen verlängert den Schutz nicht. Einzelheiten: `Monatsplan Dewlane 2026-11.md`.

<!-- MANUELL:BEGIN -->
## Tintora (`brainrot`): Reels der Folge 1, Sonderplan

Grundlage: Tintora-Sitzung, `02 Marke\Tintora\Serie\Kostenschätzung Pilot.md`, Abschnitt 11 (Stand 03.11.2026; Stefan hat 500 Credits bis 30.11. für Folge 1 freigegeben). Tintora läuft nicht im Tagesläufer (eigener Renderer, Kling-Clips je Reel); gebucht wird erst nach Rückmeldung der Hauptsitzung. Die Termine sind der Vorschlag der Tintora-Sitzung, die Slots hat Stefan am 03.11.2026 bestätigt.

- **Umfang im November:** 8 Reels in Deutsch und Englisch (Abschnitte F1-01 bis F1-09 ohne das Testreel F1-06 vom 03.11.), 9:16.
- **Takt:** 1 Reel je Tag (Slots wie Thema 1: DE 12:00, EN 15:00 Wien), nur am 04.11. zwei (Slots Thema 1 und 2). Ab 11.11. steht kein weiteres Reel im Plan: Die 500 Credits gelten nur für Folge 1, Folgen 2 bis 6 und Staffel 2 sind nicht freigegeben.
- **Abweichung von 2 Themen je Tag:** Credits (500 für 8 Reels, rund 54 je Reel; nach 2 Reels 93,25 verbraucht) und das Pro-Limit der Stimmen (höchstens 12 Pro-Anfragen je Tag, Reset 09:00 Wien; ein Reel braucht je Sprache etwa 4 bis 5). Zwei Reels an einem Tag gehen nur, wenn die deutschen Stimmen schon vorliegen.

| Datum | Reel | Titel | Slot DE | Slot EN | Stand laut Tintora-Sitzung |
|---|---|---|---|---|---|
| Mi 04.11. | F1-04 | Der Weg zum Echoberg | 12:00 | 15:00 | DE und EN Prüfbericht bestanden |
| Mi 04.11. | F1-05 | Dunkel wie Tinte | 18:00 | 21:00 | DE bestanden, EN folgt am 04.11. |
| Do 05.11. | F1-07 | Der gelbe Kern | 12:00 | 15:00 | geplant, Stimmen fehlen |
| Fr 06.11. | F1-08 | Mira am Ausgang | 12:00 | 15:00 | geplant, Stimmen fehlen (5 Figuren) |
| Sa 07.11. | F1-09 | Tee am grauen Feuer | 12:00 | 15:00 | geplant, Stimmen fehlen |
| So 08.11. | F1-03 | Sechs Blätter | 12:00 | 15:00 | geplant, DE zur Hälfte vorhanden |
| Mo 09.11. | F1-01 | Das Farbfest | 12:00 | 15:00 | geplant, Stimmen fehlen |
| Di 10.11. | F1-02 | Die graue Laterne | 12:00 | 15:00 | geplant, Stimmen fehlen |

Lücke: Vom 11.11. bis 30.11. hat Tintora keine Reels im Plan (20 Tage). Was dafür nötig wäre: Freigabe weiterer Credits und Entscheidung zu Folge 2 oder Staffel 2 (Konzeptplan Tintora, Hinweise).

## Scutoria YouTube: Langvideos (Vorschlag)

Grundlage: `02 Marke\Scutoria\YouTube-Konzept.md` (10 Videos, 15 bis 25 min, 16:9) und der Stand der Scutoria-YouTube-Sitzung. Langvideos laufen nicht im Tagesläufer (markenlokaler Composer in `brands\ai_security\longform`). **Alles in diesem Abschnitt ist ein Vorschlag der Tagesläufer-Sitzung, kein Beschluss.**

- **Stand (Hauptsitzung, 03.11.):** Video 01 DE fertig, die englische Fassung am 05.11.; Video 02 in Arbeit.
- **Vorschlag:** ein Langvideo je Woche, Deutsch am Donnerstag 17:00, Englisch am Freitag 17:00 (Wien). Wochentag und Uhrzeit sind eine Annahme; sie hängt an Stefans Urteil zu Video 01 und an der Fertigstellung der englischen Fassungen.

| Woche | Deutsch (Do) | Englisch (Fr) | Video | Stand |
|---|---|---|---|---|
| 1 | Do 05.11. 17:00 | Fr 06.11. 17:00 | 01 Ihre Belegschaft nutzt schon KI. Womit die Regeln anfangen. | DE fertig, EN am 05.11. |
| 2 | Do 12.11. 17:00 | Fr 13.11. 17:00 | 02 Ihr Kunde schickt einen Sicherheitsfragebogen. So antworten Sie ehrlich. | in Arbeit |
| 3 | Do 19.11. 17:00 | Fr 20.11. 17:00 | 04 Was nie in ein KI-Tool darf. Fünf Datenarten und die Zweifelsregel. | laut Konzept „sofort“, noch nicht begonnen |
| 4 | Do 26.11. 17:00 | Fr 27.11. 17:00 | offen: 03 (braucht die fertige Website) oder 05 (Artikel 4 der KI-Verordnung) | Reihenfolge entscheidet die Sitzung |

## Was die Lücken schließen würde

- **Revlore:** weitere Themen mit gebautem Aufbau und Quellen (Aufbau F braucht je Thema Quelle und Stichworte in `brands/engines/aufbauten.yaml`); alle anderen Technik-Themen brauchen ein eigenes Modell.
- **Scutoria:** Aufbauten B bis D (Telefon- und Regelthemen) und Quellen für die Themen ohne Quelle; heute trägt nur Aufbau A neun Themen.
- **Promptwerk:** je Thema eine echte Aufzeichnung (`record_run.py`, Abo-Kontingent); der Tagesläufer nimmt nichts auf.
- **Suitwerk:** Quellen für die 11 Themen ohne Quelle; Szenencode für Fischgrat, Hahnentritt und die übrigen ausgeschlossenen Themen.
- **Gigastruct, Gritwerk, Frontlore, Dewlane:** alle Plätze belegt, aber teils mit Ersatz-Bildaufbau; mit weiteren gebauten Aufbauten würden Ersatz und gleiche Aufbauten am selben Tag entfallen (Zahlen in der Tabelle oben).
- **Alle Marken:** Quellenlücken je Marke stehen in der Datei `Monatsplan <Marke> 2026-11.md` unter „Ohne Quelle“.
<!-- MANUELL:END -->

## Dateien

- `Monatsplan Revlore 2026-11.md`, `data/calendars/engines_2026-11.plan.json`
- `Monatsplan Suitwerk 2026-11.md`, `data/calendars/menswear_2026-11.plan.json`
- `Monatsplan Scutoria 2026-11.md`, `data/calendars/ai_security_2026-11.plan.json`
- `Monatsplan Promptwerk 2026-11.md`, `data/calendars/claude_workflows_2026-11.plan.json`
- `Monatsplan Gigastruct 2026-11.md`, `data/calendars/megaconstruction_2026-11.plan.json`
- `Monatsplan Gritwerk 2026-11.md`, `data/calendars/motivation_2026-11.plan.json`
- `Monatsplan Frontlore 2026-11.md`, `data/calendars/military_history_2026-11.plan.json`
- `Monatsplan Dewlane 2026-11.md`, `data/calendars/beauty_2026-11.plan.json`
- Programm: `scripts/month_planner.py`, Modul `src/fn/daily/monthplan.py`, Aufgabenvorlage `automation/run_month_plan.ps1`; Beschreibung in `docs/daily-runner.md`.
