# Gritwerk – Format-Bibel „Laborbuch“

Stand: 02.11.2026 (Wien), Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026**, Format „Laborbuch“ und Pilot „Abfragen“ (Weitergabe der Hauptsitzung, Stefans Antwort „Beide“; Bedingung: Fassung P2 besteht alle Prüfungen – erfüllt: VALIDATED, `overlap_check` ohne Überschneidungen, keine Schrift unter 24 px). Kern A „Laborbuch“ mit B als festem Schlussteil und C als eigener Reihe (Abschnitt 0). Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke ein eigenes Format; gemeinsam bleiben nur Technik und Prüfungen) und die Bewertung im `Statusbericht neun Marken 2026-11-02.md` („Gritwerk in der jetzigen Form am schwächsten unterscheidbar; neuer Kern nötig, mit überprüfbarem Ergebnis statt allgemeiner Tipps“). Ersetzt nach Freigabe für neue Videos die `Vorlage Gritwerk.md` (Version 0.9: Gewohnheitskarte, Schreibtisch mit Kalender, Erklärschicht). Die Vorlage bleibt als Nachweis liegen.

Umsetzung: `C:\Automation\faceless-network\brands\motivation\laborbuch\scenes.py` (Szenentypen `lb_*`, Ebene, CSS), eingebunden am Ende von `brands\motivation\scenes.py`. Pilotplan: `data\direction\motivation-20261111-1-de.P1.json`.

## 0. Kernvorschläge (Stefan entscheidet)

Ausgangslage: Es gibt keine reale Person hinter Gritwerk. Erfundene Selbstversuche oder Erfahrungsberichte dürfen deshalb nicht als echt erscheinen. „Dokumentierte Selbstversuche“ gehen nur ehrlich, wenn der Versuch entweder veröffentlicht ist (fremder Versuch, nacherzählt) oder der Zuschauer ihn selbst macht (eigene Messung, n = 1).

| | Kern | Versprechen (ein Satz) | Beispielthema | Risiko |
|---|---|---|---|---|
| **A** | **Laborbuch** – ein veröffentlichter Versuch, nacherzählt und sichtbar gemacht | „Ein echter Versuch pro Video: wer mitgemacht hat, was gemessen wurde, was herauskam, wo die Grenzen liegen und ob es einer Nachprüfung standhält.“ | Roediger & Karpicke 2006: nochmal lesen oder sich selbst abfragen? Nach 5 Minuten gewinnt das Lesen, nach 1 Woche das Abfragen (Pilot). | Aufwand: Zahlen müssen aus dem Volltext kommen, nicht aus Abstracts. Einzelstudien verleiten zum Überinterpretieren; deshalb Pflichtteil „Grenzen“ und Replikationsstempel. Kann trocken wirken, wenn das Bild nicht trägt. |
| **B** | **Mitmachversuch** – der Zuschauer ist die Versuchsperson | „Du machst in 60 Sekunden einen kleinen Versuch mit, misst dein Ergebnis nach einer klaren Regel und legst es neben das der Studie.“ | Vorab-Test: erst raten, dann lesen; der Zuschauer beantwortet drei Fragen vor der Erklärung und prüft danach, was hängen bleibt. | Nur wenige Effekte zeigen sich innerhalb eines Videos (Gedächtnis, Aufmerksamkeit). Ergebnisse mit n = 1 sind nicht überprüfbar und können irreführen. Wochenlange Effekte lassen sich im Video nicht messen. |
| **C** | **Hält das?** – berühmte Befunde gegen ihre Nachprüfung | „Bekannte Motivationsbefunde im direkten Vergleich mit ihrer großen Wiederholung: hält es, wackelt es oder kippt es?“ | Willenskraft als Akku: Baumeister 1998 gegen die Wiederholung mit 23 Laboren (Hagger et al. 2016). | Begrenzter Themenpool (gut dokumentierte Wiederholungen gibt es für etwa 20–30 Befunde). Kippt leicht in „Mythen-Zerstörer“-Ton. Eine gescheiterte Wiederholung widerlegt nicht alles. |

**Entscheidung Stefan, 02.11.2026 (über die Hauptsitzung): „A Laborbuch (Empfehlung)“.** Damit gilt A als Kern, B als fester Schlussteil („Dein Versuch“) und C als eigene Reihe („Hält das?“). Gründe der Empfehlung:
- **Überprüfbar und ehrlich.** Jede Zahl im Video stammt aus einer Veröffentlichung, mit Seitenangabe. Niemand behauptet, den Versuch selbst gemacht zu haben; das steht dauerhaft im Bild.
- **Größter Themenvorrat.** Fast alle 84 Kalenderthemen im November beruhen auf einem konkreten Versuch; A kann sie tragen, B und C nur einen Teil.
- **Unterscheidbar.** Keine andere Marke zeigt Menschen als Messpunkte, Versuchsaufbau und Replikationsstand. Das Bild ist nicht mehr „Tipp mit Karte“, sondern ein Protokoll mit Ergebnis.
- **B und C stärken A**, statt allein zu stehen: B gibt jedem Video eine Handlung mit Messregel für den Zuschauer, C wird zur Reihe, wo es eine große Nachprüfung gibt.

## 1. Versprechen

**„Ein echter Versuch pro Video: wer mitgemacht hat, was gemessen wurde, was herauskam, wo die Grenzen liegen und ob es einer Nachprüfung standhält. Und ein kleiner Versuch für dich, mit Messregel.“**

- Ein Video, **ein** veröffentlichter Versuch. Keine Liste von Tipps, kein „5 Gewohnheiten erfolgreicher Menschen“.
- Der Zuschauer sieht den Aufbau, bevor er das Ergebnis hört, und kann mitdenken.
- Ergebnis immer mit Grenzen und Replikationsstand; nie als Versprechen für den Einzelnen.
- Am Ende ein Versuch für den Zuschauer (n = 1) mit einer klaren Messregel und dem Hinweis, dass er nichts beweist.

Ein Satz für die Kanalbeschreibung: *„Gritwerk erzählt veröffentlichte Versuche zu Lernen, Motivation und Gewohnheiten nach: Aufbau, Messung, Ergebnis, Grenzen, Stand der Forschung. Nicht selbst durchgeführt, keine Therapie- oder Gesundheitsberatung.“*

Zielgruppe unverändert: Menschen, die sich selbst entwickeln wollen und Belege statt Parolen suchen; Studierende und Berufstätige, die lernen.

## 2. Bildsprache

| Element | Regel |
|---|---|
| Grund | Warmer, dunkler Raum (`#121110`), eine Lampe oben links, sonst nichts. Keine Gewohnheitskarte, kein Kalender-Schreibtisch, kein Staub, keine Kamerafahrt. |
| Laborbuchseite (Leitobjekt) | Eine große Seite Karopapier (`#F4F0E8`, Raster 32 px, roter Doppelrand links) liegt im ganzen Video an derselben Stelle (x 92–952, y 300–1146; Text endet links von x 932). Kopfzeile: **LABORBUCH · Versuch 001** links, die Studie rechts („Roediger & Karpicke 2006“). Alles Inhaltliche steht auf dieser Seite. |
| Umblättern | Jede Szene nach der ersten beginnt mit einem Blatt, das sich um den linken Rand wegdreht (0,6 s). Das ist der einzige Übergang des Formats. |
| Protokollleiste (Erkennungszeichen) | Oben unter dem Logo, durchgehend: sieben Tageskästchen (das Gritwerk-Motiv) und der Name des aktuellen Schritts mit Zähler: **1/7 Frage · 2/7 Aufbau · 3/7 Messung · 4/7 Ergebnis · 5/7 Grenzen · 6/7 Stand · 7/7 Dein Versuch**. Erledigte Schritte sind gedämpft gold, der aktuelle voll gold. |
| Ehrlichkeitszeile | Darunter, durchgehend, 27 px, hell (`#E2DACD`) mit goldenem Ring: „Nacherzählt aus der Studie · nicht selbst durchgeführt“. Ersetzt die Eröffnungszeile der alten Erklärschicht. Mindestgröße für alle Kleinschrift im Format (Quellen, Belege, Stufenskala): 24 px. |
| Teilnehmende | Nur als Punkte. Ein Punkt = eine Person (bei großen Stichproben ein Punkt = n Personen, dann im Bild beschriftet). Die Punkte teilen sich in die Gruppen des Versuchs auf. Keine Gesichter, keine Figuren, keine KI-Menschen. |
| Messinstrument | Was gemessen wurde, wird als Objekt gezeigt: Raster aus Einheiten (hier 30 Ideeneinheiten), Skala, Zähler, Stoppuhr. Darunter die Zählregel in einer Kapsel („1 Einheit = 1 Punkt“). |
| Ergebnis | Balken pro Bedingung und Messzeitpunkt, wachsen am gesprochenen Wert. Grau = Vergleichsbedingung, Gold = die untersuchte Methode. Werte in Fraunces über dem Balken, der höhere Wert je Gruppe schwarz umrandet. Wendepunkte bekommen eine bernsteinfarbene Marke („kippt“). |
| Replikationsstempel | Stempel mit vier Stufen und fester Farbe: **Hält** (grün `#4F7A3A`), **Gemischt** (bernstein `#D9772C`), **Nicht bestätigt** (rot `#C2452F`), **Offen** (grau). Darüber die Skala aller vier Stufen, damit man die Einordnung sieht. Darunter die Belege mit grünem, bernsteinfarbenem oder rotem Rand. |
| Grenzen | Liste mit bernsteinfarbenen Halbkreisen (offen, nicht „falsch“). |
| Dein Versuch | Eigene Karteikarte mit gestricheltem Goldrand auf der Seite, nummerierte Schritte, Messregel in der Kapsel, Hinweis „n = 1 zeigt dir etwas, beweist aber nichts“. Darunter Markenzeile mit Claim und Hinweis, mindestens 4 s lesbar. |
| Quelle | Jede Szene trägt unten auf der Seite ihre Quelle mit Seitenangabe („Roediger & Karpicke 2006, Psychological Science 17(3), Exp. 1, S. 251“). |
| Schrift | Fraunces 700 (Fragen, Überschriften, Werte, Stempel, Schrittname), Inter 500–800 (alles andere). Untertitel unverändert (Inter 700, Sinngruppen bis 4 Wörter). |
| Farben | Palette aus `brand.yaml`; auf Papier: Tinte `#1B1712`, gedämpft `#7D746A`, Gold `#E5B45A` als Fläche, `#8C6216` als Goldschrift. |
| Entfällt | Erklärschicht (Kicker, Marker-Kapseln, Quellenleiste, Stimmen-Tag), Statusleiste, Gewohnheitskarte als Leitobjekt, Kreisübergänge, Push-in, Filmkorn bleibt. „KI-generiert“ bleibt unten (gemeinsame Regel). |

Senkrechte Aufteilung (1080 × 1920, seit Fassung P2 nach Prüfrunde R5): Logo 100–160 · Protokollleiste 194–234 · Ehrlichkeitszeile 246–280 · Seite 300–1200 (Inhalt 384–1130, Quelle ab 1146) · Untertitel bis 1320 (`caption_bottom_px: 600`, damit zwischen Seite und Untertiteln kein leerer Streifen bleibt) · „KI-generiert“ mindestens 430 px über dem unteren Rand (gemeinsamer Renderer) · Fortschritt 1548. Texte bleiben links von x 932 (Plattform-Bedienelemente). Keine sichtbare Schrift unter 24 px (Prüfrunde R7; `overlap_check` meldet sie unter `small_text`).

## 3. Dramaturgie (gemessen am Piloten, Stimme 78,3 s, Video etwa 81 s; erlaubt 65–90 s)

| Sekunde | Protokollschritt | Szenentyp | Inhalt |
|---|---|---|---|
| 0–12,3 | 1 Frage | `lb_hook` | Die Frage des Versuchs groß auf der Seite. Die Teilnehmenden erscheinen als Punkte (n = 120), darunter Ort und Experiment. Andeutung des Ergebnisses („nach 5 Min: Lesen vorn“) und Stempel „Ergebnis kippt“, ohne die Zahlen zu verraten. |
| 12,3–29,2 | 2 Aufbau | `lb_setup` | Die Materialien (zwei Sachtexte), die Bedingungen nebeneinander (grau: nochmal lesen, gold: selbst abfragen), dann teilen sich die Punkte in die Gruppen des Versuchs (5 Min, 2 Tage, 1 Woche, je n = 40). |
| 29,2–38,1 | 3 Messung | `lb_measure` | Das Messinstrument: Der Text zerfällt in 30 Kästchen (Ideeneinheiten), die Zählregel erscheint, ein echter Wert aus dem Versuch füllt die Kästchen (Ø 20,9 von 30). |
| 38,1–50,6 | 4 Ergebnis | `lb_result` | Die drei Balkenpaare wachsen am gesprochenen Wert. Marke „kippt“ zwischen 5 Minuten und 2 Tagen; am Ende der Abstand (+14 Prozentpunkte). |
| 50,6–64,0 | 5 Grenzen, 6 Stand | `lb_verdict` | Drei Grenzen, dann wechselt die Leiste auf „Stand“: Skala der vier Stufen, Belege (Meta-Analyse, Übersicht), Stempel „Hält“. |
| 64,0–81 | 7 Dein Versuch | `lb_try` | Karteikarte mit drei Schritten, Messregel, Hinweis n = 1, dann Markenzeile. |

Regeln für Sprechtext und Bild:
- Sulafat spricht etwa 2,4 Wörter/s; 170–185 Wörter ergeben 72–78 s Stimme. Zahlen ausgeschrieben (Whisper-Abgleich), im Bild als Ziffern.
- Jede Szene hat mindestens drei Bildereignisse an gesprochenen Wörtern (`"@Wort"`, `"@Wort#2"`, `"@Wort+0.3"`).
- Die Stimme nennt erst den Aufbau, dann das Ergebnis. Ergebnisse immer als „in dem Versuch …“, „nach einer Woche … gegen …“, nie als „du wirst …“.
- Die Grenzen werden gesprochen, nicht nur gezeigt.
- Anrede „du“, ruhig, ohne Pathos, kein Ausrufezeichen. Schluss: „Mehr echte Versuche: Folge Gritwerk.“ Claim im Bild: „Methode statt Parole.“ (Vorschlag für später: „Versuch statt Parole.“, siehe Abschnitt 9).

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender `motivation_2026-11.json` (je 84 Themen DE und EN) |
|---|---|---|---|
| **Laborbuch** (Hauptreihe, Pilot) | Ein klassischer oder aktueller Versuch, vollständig nacherzählt. | hook → setup → measure → result → verdict → try | „Lernlabor“ (16), „Kleine Methode“ (20; der Versuch hinter der Methode, z. B. Wenn-dann-Pläne), „Fokus im Alltag“ (16) |
| **Hält das?** | Ein berühmter Befund neben seiner großen Wiederholung: zwei Spalten im Ergebnis (Original, Wiederholung), der Stempel entscheidet. | hook → setup → result (zwei Spalten) → verdict → try | „Mythos-Check“ (16): Willenskraft als Akku, Power Posing, Marshmallow-Test, Mozart-Effekt, Growth-Mindset, Grit, Pygmalion, Dunning-Kruger, hungrige Richter, Marmeladen-Studie |
| **Kleingedrucktes** | Eine berühmte Zahl und was genau gemessen wurde: 66 Tage, 47 Prozent, 10.000 Stunden, 75.000 Dollar. Schwerpunkt Messung und Grenzen. | hook → measure → result → verdict → try | „Nachgerechnet“ (16) |
| **Mitmachversuch** | Der Zuschauer macht im Video selbst mit (eine Wortliste, drei Fragen vorab, ein Lückentext), zählt nach der Messregel und sieht danach das Ergebnis der Studie. Nur für Effekte, die sich in Sekunden zeigen; nur Gedächtnis- und Aufmerksamkeitsaufgaben. | hook (Aufgabe) → measure (Zählregel) → result (Studie) → verdict → try | Einzelthemen aus „Lernlabor“: Vorab-Test, Selbst ergänzen, schwer lesbare Schrift, Warum-Fragen |

Für „Hält das?“ (zwei Spalten Original gegen Wiederholung, Konfidenzintervall) und „Mitmachversuch“ (Aufgabe mit Countdown) fehlen noch Code-Bausteine (Abschnitt 9). Themen ohne konkreten Versuch (reine Meinungen, Ratgeber, Zitate) passen nicht in das Format und werden zurückgestellt, nicht ausgeschmückt.

## 5. Abgrenzung zu den anderen acht Marken

| Marke | Kern ihres Formats | Was Gritwerk anders macht |
|---|---|---|
| Scutoria | „Was tust du?“: Fall aus einem Betrieb, Entscheidung A/B/C, Uhrzeit, Papierkarte des Falls | Keine Geschichte und keine Entscheidung des Zuschauers. Gritwerk zeigt einen Versuch mit vielen Menschen und Zahlen; Papier ist hier eine Laborbuchseite mit Raster, nicht eine Karte. |
| Promptwerk | „Echtlauf“: echte, aufgezeichnete Terminal-Abläufe | Gritwerk zeichnet nichts selbst auf und behauptet es auch nicht; es erzählt fremde, veröffentlichte Versuche nach. |
| Tintora (vormals Zonkfruit) | Anime-Kinderserie mit Figuren | Keine Figuren, keine Geschichte, Erwachsene als Zielgruppe. |
| Dewlane | „Nahaufnahme“: neutrales Produkt unter der Lupe | Kein Produkt; Menschen und Messung statt Gegenstand. Keine Wirkungsversprechen. |
| Revlore | „Zeitlupe“: gerechnetes Motorenmodell | Keine Mechanik und kein Modell; Daten aus Studien mit Menschen. Ergebnisse sind Messwerte der Studie, nicht gerechnet. |
| Gigastruct | „Bauaufgabe“: Bauwerk, 3D-Modell, Größenvergleich | Keine Größe und kein Raum; Gruppen, Bedingungen und Messzeitpunkte. |
| Suitwerk | Stoffe und Passform als Illustration (Format in Arbeit) | Keine Ästhetik, kein Stil. |
| Frontlore | Historische Technik mit Karten und Archivquellen (Format in Arbeit) | Gegenwartsforschung; Quellen sind Fachzeitschriften, keine Archive. |

Merkmale, die nur Gritwerk hat: Protokollleiste mit sieben Kästchen, Ehrlichkeitszeile, Laborbuchseite mit Umblättern, Teilnehmende als Punkte, die sich in Gruppen teilen, Replikationsstempel mit vier Stufen, „Dein Versuch“ mit Messregel und n = 1.

## 6. Prüfregeln (zusätzlich zu den gemeinsamen Prüfungen)

1. **Nur veröffentlichte Versuche.** Jeder Versuch stammt aus einer begutachteten Zeitschrift, einem vorab registrierten Bericht oder einer anerkannten Fachinstitution. Preprints nur mit Vermerk „noch nicht begutachtet“ im Bild. Keine Blogartikel, Bücher von Ratgeberautoren oder Medienberichte als Hauptquelle.
2. **Zahlen aus dem Volltext.** Stichprobe, Bedingungen, Messverfahren und Ergebniswerte werden im Volltext gelesen, mit Seitenangabe im Plan und im Bild. Steht ein Wert nur im Abstract oder nur in einer Abbildung ohne Zahl, wird er nicht als Zahl genannt. Ist der Volltext nicht zugänglich, wird das Thema zurückgestellt oder nur ohne Zahlen erzählt (Vermerk in `unverified`).
3. **Quellen mit URL und Abrufdatum.** In `plan.sources` je Quelle `url` (DOI-Link bevorzugt), `title` als vollständiges Zitat, `checked_at` (Abrufdatum) und `label`. Abruf höchstens 30 Tage vor dem Export, sonst neu prüfen.
4. **Replikationsstand ist Pflicht.** Vor dem Schreiben wird geprüft: Gibt es direkte Wiederholungen (z. B. Many Labs, Registered Replication Reports), Meta-Analysen oder systematische Übersichten? Einstufung:
   - **Hält:** mehrere unabhängige Wiederholungen oder mindestens eine Meta-Analyse bestätigen die Richtung des Befunds.
   - **Gemischt:** Wiederholungen oder Meta-Analysen finden den Effekt nur unter bestimmten Bedingungen, deutlich kleiner oder uneinheitlich.
   - **Nicht bestätigt:** eine große, vorab registrierte Wiederholung oder eine Meta-Analyse mit Korrektur für Publikationsverzerrung findet keinen oder einen vernachlässigbaren Effekt.
   - **Offen:** keine Wiederholung bekannt. Das Video sagt das ausdrücklich („noch nicht nachgeprüft“).
   Die Belege für die Stufe stehen im Bild und in `plan.sources`.
5. **Schwache oder umstrittene Studien.** Kleine Stichproben (unter etwa 50 je Gruppe), nicht registrierte Analysen, zurückgezogene Arbeiten, Arbeiten mit offener Datenkritik oder einer bekannten Korrektur werden nicht als Beleg erzählt, sondern nur in der Reihe „Hält das?“ zusammen mit der Kritik. Zurückgezogene Arbeiten nur mit Stempel „Zurückgezogen“ und Quelle der Rücknahme (Retraction Watch Database, Verlag). Bei Interessenkonflikten (Methode und Prüfung aus derselben Gruppe, kommerzielle Produkte) wird das gesagt.
6. **Grenzen werden gesprochen.** Mindestens drei: Wer (Stichprobe), Was (Material, Aufgabe), Wie (Labor, Feld, Messzeitpunkt). Keine Verallgemeinerung über die untersuchte Gruppe hinaus.
7. **Kein Versprechen, keine Gesundheit.** Keine Heilversprechen, keine Diagnosen, keine Diät-, Fasten-, Schlafentzugs-, Trainings- oder Medikamentenpläne. Themen zu Schlaf, Ernährung, Sport, psychischer Gesundheit nur, wenn die Quelle eine Fachgesellschaft, Behörde oder Leitlinie ist, und nie als Anleitung. „Dein Versuch“ ist auf harmlose Lern-, Gedächtnis-, Aufmerksamkeits- und Planungsaufgaben beschränkt.
8. **Ehrlich über die Herkunft.** Die Zeile „Nacherzählt aus der Studie · nicht selbst durchgeführt“ steht im ganzen Video. Niemand sagt „ich habe ausprobiert“ oder „unsere Testperson“. Beispielwerte (erfunden zur Veranschaulichung) sind grau und als Beispiel beschriftet; im Pilot gibt es keine.
9. **Dein Versuch ist eine Messidee, kein Studienbefund.** Er steht als n = 1 im Bild, mit dem Satz, dass er nichts beweist. Er darf die Studie nicht nachahmen, wenn das Risiken hätte.
10. **Keine Guru-Zitate, keine erfundenen Zitate.** Unverändert aus Vorlage 0.9. Unbelegtes steht in `unverified` und wird nicht gesagt.

Gemeinsam mit allen Marken, unverändert: Gemini-Stimme (Sulafat), Untertitel, Export, `node scripts\overlap_check.mjs` ohne Befund, KI-Kennzeichnung.

## 7. Produktion je Video

1. Thema aus `data\calendars\motivation_2026-11.json`, Reihe nach Abschnitt 4 festlegen. Volltext der Hauptstudie besorgen und lesen, Seitenangaben notieren. Replikationsstand recherchieren (Abschnitt 6, Regel 4).
2. Sprechtext schreiben (170–185 Wörter, Zahlen ausgeschrieben). Die Woche-1-Stimmen für Gritwerk (09.11.: 1-de, 1-en, 2-de, 2-en) passen nicht: Ihr Text spricht von Karte und Kästchen. Jedes Video wird neu vertont (Gemini etwa 0,02 USD).
3. Plan `data\direction\<video_id>.P1.json`: `layout.format: "laborbuch"`, `layout.explainer: false`, `layout.laborbuch {no, study, status}`, Szenen `lb_*`, `cite` je Szene mit Seite. Muster: Pilotplan.
4. Trockenlauf: `.venv\Scripts\python.exe scripts\render_direction.py <plan> --version P1dry --tts mock --no-render`, Standbilder mit `npx hyperframes snapshot . --at <Zeiten> --no-end -o <Pfad>` im Projektordner.
5. Vertonung: `... --version P1 --tts gemini --no-render`, dann Prüflauf mit echter Stimme `--version P1chk --reuse-voice storage\direction\voice_<id>_P1_gemini.wav --no-render` und `node scripts\overlap_check.mjs storage\direction\<id>-P1chk\project`.
6. Render über die Warteschlange: `.venv\Scripts\python.exe scripts\render_queue.py motivation -- scripts\render_direction.py <plan> --version P1 --reuse-voice <wav> --mirror gritwerk-regie/<name>`.
7. Überschneidungsprüfung, Sichtprüfung, Produktionsordner aus `05 Produktion\_Vorlage Video`, Zeile in `Redaktionsplan.csv`. Nichts veröffentlichen.

Szenen-Datenfelder (Kurzreferenz, Details im Docstring von `laborbuch\scenes.py`):
- `lb_hook`: `question`, `dots {n, label, at}`, `meta {text, at}`, `tease {text, at}`, `stamp {text, at}`, `cite`.
- `lb_setup`: `headline`, `sheets [{title, sub}]`, `sheets_at`, `read {text, at}`, `arms [{icon read|write|clock|count, title, sub, at}]`, `groups {n, label, at, split [{label, sub, at}]}`, `cite`.
- `lb_measure`: `headline`, `sheet_label`, `units {n, label, at}`, `rule {text, at}`, `sample {fill, text, at}`, `cite`.
- `lb_result`: `headline`, `unit`, `series [{label, kind a|b}]`, `groups [{label, values, fmt, at, value_at}]`, `turn_mark {text, at, between}`, `gap {text, group, at}`, `max`, `cite`.
- `lb_verdict`: `limits_title`, `limits [{text, at}]`, `status {level haelt|gemischt|nicht_bestaetigt|offen, at, stamp_at, title}`, `evidence [{text, cite, at}]`, `cite`.
- `lb_try`: `title`, `steps [{text, at}]`, `rule {text, at}`, `caveat {text, at}`, `sign_at`, `claim`, `disclaimer`.
- `lb_replicate` (Reihe „Hält das?“, seit 02.11.2026): `headline`, `axis {min, max, label, zero_label, ticks}`, `rows [{label, sub, value, ci [lo, hi], value_text, kind a|b, at}]`, `note {text, at}`, `cite`. Jede Studie eine Zeile, Punkt mit Intervall auf gemeinsamer Effektachse, Nullmarke „kein Effekt“. Werte nur so, wie die Studie sie berichtet; eine Zeile ohne Intervall sagt in `sub`, warum.
- Ergänzungen: `lb_result.groups[].labels` (eigene Wertbeschriftung, z. B. Dezimalkomma), `lb_setup.sheets[].icon`, `lb_measure.units.labels` und `units.highlight` (beschriftete Kästchen, z. B. Tage, und das gezählte Kästchen).
- Alle: `turn` (Umblättern, Standard an außer im Hook), `protocol` (Schritt überschreiben: Zahl oder Liste `{step, at}`).

## 8. Pilot „Abfragen statt nochmal lesen“

- Thema `motivation-20261111-1-de` (Reihe Lernlabor), im neuen Format Reihe „Laborbuch“. Ordner `05 Produktion\Gritwerk\2026-11\2026-11-11 Pilot Abfragen\`.
- Fassung P2 (02.11.2026) nach der Prüfrunde (Note 2,3, kein Muss-Befund): Ehrlichkeitszeile, Stufenskala, Belege und Quellen größer und heller; die 120 Punkte und die Texte der Aufbau-Szene stehen sofort im Bild statt erst am Wort; Seite rechts nur noch bis x 952; doppelter Gesundheitshinweis in der Beschreibung entfernt; R5 (Seite bis y 1200, Untertitel höher) und R7 (keine Schrift unter 24 px). Stimme unverändert (`--reuse-voice`).
- Englische Fassung P1: Plan `data\direction\motivation-20261111-1-en.P1.json`, eigene Gemini-Stimme (Sulafat, 83,5 s, 0,0209 USD), gleiche Fakten und Quellen; Bildtexte englisch („LAB NOTEBOOK“, „Retold from the study · not run by us“, Stempel „Holds“).
- Hauptquelle im Volltext gelesen (02.11.2026): Roediger & Karpicke 2006, Psychological Science 17(3), 249–255, https://doi.org/10.1111/j.1467-9280.2006.01693.x. Experiment 1: 120 Studierende der Washington University, 18–24 Jahre; zwei TOEFL-Sachtexte („The Sun“, 256 Wörter; „Sea Otters“, 275 Wörter), je 30 Ideeneinheiten; je 7 Minuten lesen, dann ein Text nochmal lesen, der andere freies Erinnern ohne Rückmeldung (innerhalb der Person); Abschlusstest nach 5 Minuten, 2 Tagen oder 1 Woche (zwischen den Gruppen, je 40). Erster Abruf Ø 20,9 von 30 (S. 250). Ergebnisse S. 251: 5 Min 81 % gegen 75 % (Wiederlesen vorn), 2 Tage 54 % gegen 68 %, 1 Woche 42 % gegen 56 % (Abfragen vorn).
- Replikationsstand „Hält“: Adesope, Trevisan & Sundararajan 2017, Review of Educational Research 87(3), 659–701, https://doi.org/10.3102/0034654316689306 (Meta-Analyse; Abstract: Übungstests nützen dem Lernen mehr als Wiederlesen und alle anderen Vergleichsbedingungen), abgerufen 02.11.2026 über Crossref. Dunlosky et al. 2013, Psychological Science in the Public Interest 14(1), 4–58, https://doi.org/10.1177/1529100612453266 (Übersicht; Abstract: Abfragen „high utility“, Wiederlesen „low utility“), abgerufen 02.11.2026 über Crossref. Rowland 2014 (Psychological Bulletin 140(6), 1432–1463) gelesen, aber nicht zitiert, weil das Abstract die Richtung nicht in einem Satz nennt. Effektstärken der Meta-Analysen nicht genannt (nur Abstracts gelesen).

## 9. Offene Punkte für Stefans Freigabe

- ~~Kern~~: entschieden, A „Laborbuch“ (Stefan, 02.11.2026).
- ~~Freigabe des Formats und des Piloten~~: erledigt, Stefan 02.11.2026. Nächster Schritt: Woche 1 (09.–15.11.) im neuen Format, DE und EN.
- Formatname „Laborbuch“, Kanalsatz in Abschnitt 1, Ehrlichkeitszeile im Wortlaut („Nacherzählt aus der Studie · nicht selbst durchgeführt“; die längere Fassung „Veröffentlichter Versuch, nacherzählt …“ passt in 27 px nicht in eine Zeile).
- Claim: „Methode statt Parole.“ beibehalten oder „Versuch statt Parole.“ (passt zum neuen Kern; `brand.yaml` bisher unverändert).
- Pilot freigeben (Optik, Stimme, Ablauf), deutsche Fassung P2 und englische Fassung P1.
- Reihenzuordnung der 84 Kalenderthemen (Abschnitt 4). Themen mit nur Abstract-Zugang müssen vor der Produktion im Volltext gelesen werden; das kostet je Thema mehr Recherchezeit als bisher.
- Code noch zu bauen: zwei Spalten Original gegen Wiederholung mit Konfidenzintervall (Reihe „Hält das?“), Aufgabe mit Countdown für den Mitmachversuch, Punkte mit Mengenangabe (ein Punkt = n Personen) für große Stichproben.
- Die Woche-1-Pläne im alten Format (42 Pläne, 4 bezahlte Gemini-Stimmen) sind nicht übernehmbar; jedes Video braucht einen neuen Text und eine neue Stimme (etwa 0,02 USD je Video und Sprache).
