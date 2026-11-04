# Revlore – Format-Bibel „Zeitlupe“

Stand: 02.11.2026 (Wien), Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026, mit dem Piloten „Kolbentempo“** (Weitergabe der Hauptsitzung: „Alle Videos freigegeben“). Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke bekommt ein eigenes Format; gemeinsam bleiben nur Technik und Prüfungen) und die Bewertung im `Statusbericht neun Marken 2026-11-02.md` („bewegte Schnittmodelle, Mechanik im Bild statt erzählt“). Ersetzt für neue Videos die `Vorlage Revlore.md` (Version 0.9: Kopf mit Kicker und Titel, Erklärschicht, Arbeitsspiel-Leiste, Beschriftungskarten). Die Vorlage bleibt als Nachweis liegen.

Umsetzung: `C:\Automation\faceless-network\brands\engines\zeitlupe\scenes.py` (Szenentypen `zl_*`), eingebunden am Ende von `brands\engines\scenes.py`. Pilotplan: `data\direction\engines-20261109-1-de.zeitlupe.json`.

## 1. Versprechen

**„Wir bremsen den Motor so weit ab, bis du siehst, was passiert, und messen dabei mit.“**

Ein Motor dreht bei 3000/min fünfzigmal in der Sekunde. Mit bloßem Auge sieht man davon nichts, und ein Sprecher allein kann es kaum vermitteln. Revlore zeigt jedes Mal zuerst den Motor in Echtzeit, als verwischte Langzeitbelichtung. Dann fällt das Bild in Zeitlupe, mit dem Faktor im Bild. Das Video zeigt, was sich bewegt, wo es schnell ist und wie lange es dauert, in Grad Kurbelwinkel und in Millisekunden. Am Ende läuft der Motor wieder auf Echtzeit hoch: Das eben Gesehene dauert in Wirklichkeit nur wenige Millisekunden.

Ein Satz für die Kanalbeschreibung: *„Motorentechnik in Zeitlupe: gerechnete Schnittmodelle, gemessen statt behauptet.“*

Zielgruppe unverändert: Auto- und Motorradinteressierte, die verstehen wollen, wie Motoren arbeiten, keine Teile kaufen.

## 2. Bildsprache

| Element | Regel |
|---|---|
| Grund | Messraum: Graphit-Verlauf (`#171C22`), ein ruhendes 40-px-Raster, Randabdunklung. Kein wanderndes Zeichenraster, keine Geisterzeichnungen, kein Kameraschwenk und kein Push-in. **Bewegung kommt nur aus der Mechanik.** |
| Zeitlupen-Band (Erkennungszeichen) | Oben, durchgehend: **ECHTZEIT** (Bernstein), **ZEITLUPE 1:n** (Faktor in Akzentblau) oder **STANDBILD**. Rechts „Bezug 3000/min (Beispiel)“. Der Faktor wird aus der Kurbeldrehzahl im Bild gegen die Bezugsdrehzahl gerechnet, nie geschätzt. |
| Langzeitbelichtung | Echtzeit wird als Verwischung gezeigt: Kolbenband über den ganzen Hub, an den Totpunkten dichter (dort verweilt der Kolben am längsten), Kurbelscheibe als Kreis. Kennzeichen jedes Anfangs und jedes Endes. |
| Schnittmodell | Das gerechnete Revlore-Modell (Zylinder 1, Zweiventiler, zwei Nockenwellen) bleibt Hauptdarsteller: Kolben, Pleuel, Kurbel, Ventile, Nocken, Gas, Funke, alles aus der Kinematik. |
| Stroboskop-Lineal | Vergrößerter Kolbenweg neben dem Zylinder. Alle 15° Kurbelwinkel erscheint ein Strich, das heißt in gleichen Zeitabständen (bei 3000/min alle 0,83 ms). Große Abstände bedeuten schnelle Bewegung. Zeiger und Projektionslinie verbinden Kolbenboden und Lineal. |
| Messschrieb | Panel mit Gitter, Achse in Grad Kurbelwinkel und zweite Achse in ms bei der Bezugsdrehzahl. Ein Stift zeichnet die Kurve im Takt der Kurbel (`live`), eine Vergleichskurve gestrichelt. Senkrechte Marken für Stellen, über die gesprochen wird. |
| Uhr | Kleines Zifferblatt rechts unten: Zeiger = Kurbelwinkel, Skala in ms nach OT bei der Bezugsdrehzahl, gefüllter Sektor = verstrichene Zeit seit OT. |
| Vektoren und Hilfslinien | Geschwindigkeitspfeil am Kolben (Länge proportional zum Tempo), Winkelbogen β am Pleuel, Geisterkolben auf einer Vergleichsbahn. Bernstein für Hilfsgeometrie (Hubmitte, Zylinderachse, β), Blau für das bewegte Bauteil im Fokus. |
| Farben | Palette aus `brand.yaml` unverändert: Akzentblau = Bewegung und Bauteil im Fokus, Stahltöne = Metall, Orange nur für Funke und brennende Ladung, Grau für Abgas, Bernstein für Hilfslinien und das Wort ECHTZEIT. |
| Schrift | Oswald 600 (Band, Aussagen, Ergebniszeilen), JetBrains Mono (Lineal, Achsen, Notizen, Quelle), Inter in den gemeinsamen Untertiteln. |
| Quelle | Eigene Zeile über den Untertiteln (y 1290, im Messschrieb über dem Panel bei y 790), Mono 26 px: „Quelle: MIT 2.61, Vorlesung 8 · abgerufen 01.11.2026“. Seit der Prüfrunde vom 03.11.2026 nicht mehr unter den Untertiteln, weil dort die Plattform-Bedienelemente liegen. |
| Mindestgröße | Alle Texte im Bild mindestens 26 px (Achsen, Lineal und Legende 30 px). Legende kurz: „Sinus (90°)“, „Modell“. |
| Entfällt | Erklärschicht (Kicker, Kopftitel, Stimmen-Tag, Marker-Kapseln, Quellenleiste), Arbeitsspiel-Leiste mit „Zyl. 1“-Kachel, Beschriftungskarten mit Farbleiste, Push-in, wanderndes Raster. „KI-generiert“ bleibt unten (gemeinsame Regel). |

Senkrechte Aufteilung (1080 × 1920): Logo 120–160 · Band 200–292 · Bühne 300–1250 · Quelle 1266–1296 · Untertitel bis 1432 (`caption_bottom_px: 488`) · „KI-generiert“ ab etwa 1454 (gemeinsamer Renderer seit 03.11.2026, mindestens 430 px über dem unteren Rand) · Fortschritt 1556. Muss die Stimme die Arbeitsspiel-Leiste zeigen (`zl_strip`), steht sie bei y 1180. Rechts bleibt x ab 930 frei.

## 3. Dramaturgie (gemessen am Piloten, 73,7 s; erlaubt 65–90 s)

| Sekunde | Beat | Szenentyp | Inhalt |
|---|---|---|---|
| 0–8,6 | Echtzeit, dann Zeitlupe (Hook) | `zl_hook` | Langzeitbelichtung mit „ECHTZEIT“, die Frage groß im Bild. Beim ersten Schlüsselwort fällt das Bild in Zeitlupe. Optional Standbild an der entscheidenden Stellung und eine Hilfslinie. Die Gegenbehauptung streicht die Frage durch. |
| 8,6–21,7 | Hinsehen | `zl_strobe` | Modell groß, Geschwindigkeitspfeil, das Stroboskop-Lineal füllt sich Strich für Strich. Worte lösen „v = 0“ an den Totpunkten und die schnellste Strecke aus. |
| 21,7–31,5 | Erwartung | `zl_trace` | Messschrieb mit der naiven Erwartung (hier: Sinus, gestrichelt) und ihrer Marke. |
| 31,5–45,7 | Ursache | `zl_cause` | Das verursachende Bauteil wird hervorgehoben, Geometrie (Winkel β) und Vergleichsbahn sichtbar. Die Kurbel steht genau dann bei 90°, wenn die Stimme davon spricht; das Lineal zeigt 58 % statt 50 %. |
| 45,7–62,5 | Messung | `zl_trace` (`live`) | Der Stift zeichnet die echte Kurve im Takt der Kurbel. Quellenwert und Modellwert getrennt beschriftet. |
| 62,5–73,7 | Zurück in Echtzeit | `zl_realtime` | Ergebniszeilen erscheinen am Wort, der Motor beschleunigt (Faktor zählt herunter), Langzeitbelichtung und „ECHTZEIT“ wie am Anfang, Markenzeile. Ende und Anfang gleichen sich, das Video läuft als Schleife. |

Regeln für Sprechtext und Bild:
- Sprechtempo Gemini Iapetus DE etwa 15,6 Zeichen/s; 1.050–1.250 Zeichen ergeben 70–82 s.
- Jede Szene hat mindestens drei Bildereignisse an gesprochenen Wörtern (`"w:Wort"`). Die Kurbelstellung wird über `theta`-Stützpunkte an Wörter gekoppelt, damit die Mechanik genau dann an der besprochenen Stelle steht.
- Die Stimme beschreibt, was das Bild zeigt („Schau auf den blauen Pfeil“), und überlässt dem Bild die Zahl. Künftige Skripte nennen den Wechsel ausdrücklich („In Echtzeit siehst du nichts. In Zeitlupe …“).
- Anrede „du“, sachlich, kein Ausrufezeichen, keine Schadensdramatik. Schluss: „Motorentechnik verstehen: Folge Revlore.“

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender `engines_2026-11.json` |
|---|---|---|---|
| **Zeitlupe** (Hauptreihe) | Ein Vorgang, der in Echtzeit unsichtbar ist: Ventilüberschneidung, Zündung und Brennverlauf, Einspritzung, Klopfen, ein Arbeitsspiel in 40 ms. | hook → strobe oder cause → trace → realtime | „Im Schnitt“ (täglich) |
| **Nachgemessen** (Pilot) | Eine verbreitete Behauptung wird am gerechneten Modell gemessen. Der Messschrieb zeigt Erwartung und Ergebnis, die Quelle nennt den Wert echter Motoren. Urteil in einer Zeile. | hook → strobe → trace (Erwartung) → cause → trace (live) → realtime | „Mythos-Check“ und „Nachgerechnet“ |
| **Ein Schalter, zwei Schriebe** | Dasselbe Modell mit genau einem geänderten Wert: Pleuellänge, Zündzeitpunkt, Steuerzeiten, Saugrohr- gegen Direkteinspritzung, Otto gegen Diesel. Zwei Kurven im selben Schrieb, zwei Stroboskop-Lineale nebeneinander. | hook → cause (Schalter) → trace mit zwei Kurven → realtime | „Gegenübergestellt“ |
| **Erstes Modell** | Historische Mechanik als bewegtes Schema, aber nur, wenn Patentzeichnung oder Fachquelle die Mechanik belegen (zum Beispiel Ottos Viertakt, Wankel). Sonst wird das Thema zurückgestellt, nicht ausgeschmückt. | hook → strobe → realtime | „Motorgeschichte“ |

Für „Ein Schalter, zwei Schriebe“ und „Erstes Modell“ fehlen noch Code-Bausteine (siehe Abschnitt 8). Themen ohne Mechanik, zum Beispiel reine Regelwerke wie Abgasgrenzwerte, passen nicht in dieses Format und werden zu einem Vorgang umgebaut („Was der Katalysator in 0,1 s mit einem Abgaspaket macht“) oder fallen weg.

## 5. Abgrenzung zu den anderen acht Marken

| Marke | Kern ihres Formats | Was Revlore anders macht |
|---|---|---|
| Scutoria | „Was tust du?“: Fall aus einem Betrieb, Entscheidung A/B/C, Uhrzeit als Dramaturgie, Papierkarte | Keine Geschichte, keine Entscheidung, keine Karten. Die Zeit läuft in Millisekunden, nicht in Uhrzeit. |
| Promptwerk | „Echtlauf“: aufgezeichnetes Terminal, Protokoll, Wiederholungszahl | Nichts ist aufgezeichnet, alles ist gerechnet. Bild ist eine bewegte technische Zeichnung, kein Text. |
| Zonkfruit | Anime-Kinderserie mit Figuren, KI-Video | Keine Figur, keine Handlung, keine KI-Bilder. |
| Dewlane | Beauty mit KI-Bildern erfundener Produkte | Keine generierten Bilder, kein Produkt, keine Wirkungsbehauptung. |
| Gigastruct | Bauherausforderung, 3D-Modell, Größenvergleich | Nicht Größe, sondern Tempo und Zeit. Ein Bauteil im Schnitt statt eines Bauwerks im Raum. |
| Suitwerk | Stoffe und Passform als Illustration | Kein Stil, keine Ästhetik als Inhalt; Physik als Inhalt. |
| Frontlore | Historische Technik mit Karten und Archivquellen | Gegenwartstechnik; Geschichte nur als bewegtes Funktionsmodell (Reihe „Erstes Modell“). |
| Gritwerk | Motivation, künftig Selbstversuche | Kein Mensch, kein Gefühl; der Versuch ist eine Messung am Modell. |

Merkmale, die nur Revlore hat: Echtzeit-Langzeitbelichtung am Anfang und Ende, Zeitlupenfaktor aus der Drehzahl gerechnet, Stroboskop-Striche in gleichen Zeitabständen, Stift im Takt der Kurbel, Zeitachse in Millisekunden.

## 6. Prüfregeln (zusätzlich zu den gemeinsamen Prüfungen)

1. **Bewegung gerechnet, nicht gezeichnet.** Jede Lage von Kolben, Pleuel, Kurbel, Ventilen und Nocken kommt aus der Kinematik in `brands\engines\scenes.py` (Kolbenbolzen `y = CY − (R cos θ + √(L² − R² sin² θ))`, Kurbel im Uhrzeigersinn, Nockenwellen gleichsinnig mit halber Drehzahl, Ventilhub aus dem gezeichneten Nockenprofil, Zündung 30° vor OT). Keine Hand-Keyframes für Bauteile.
2. **Viertakt-Folge stimmt.** Die Kurbelwinkel laufen über die Beats fortlaufend weiter (Positionen modulo 720°), damit Gasfarbe, Ventile und Funke zum Takt passen. Ein Sprung ist nur an einem harten Schnitt in ein anderes Bildlayout zulässig, nie innerhalb einer Szene.
3. **Zeit ehrlich.** Zeitlupenfaktor, Standbild und Echtzeit stehen immer im Band und werden aus dem `theta`-Verlauf gegen `ref_rpm` gerechnet. Die Bezugsdrehzahl ist als „Beispiel“ gekennzeichnet. Millisekunden im Bild beziehen sich auf diese Drehzahl und stehen so in der Beschreibung.
4. **Gleiche Zeitabstände.** Stroboskop-Striche nur in gleichen Kurbelwinkelschritten (gleiche Zeit bei konstanter Drehzahl). Der Zeitabstand steht am Lineal.
5. **Eine Funktion für Modell und Schrieb.** Kurven im Messschrieb werden aus derselben Formel berechnet, die das Modell bewegt; der Stift ist an den Kurbelwinkel gekoppelt. Schematische Kurven (zum Beispiel Druckverlauf) heißen im Bild „Schema“.
6. **Modell und Quelle getrennt.** Werte aus dem Modell tragen „Modell“ (hier: Maximum bei 74°, Verhältnis Kurbelradius zu Pleuellänge 0,31). Werte echter Motoren kommen aus einer Quelle und stehen mit Quelle im Bild (hier: Pkw typisch etwa 70° nach OT, MIT 2.61, Vorlesung 8, Seite 1). Weichen beide ab, sagt die Stimme das.
7. **Quellen.** Primärquellen: Hersteller, Norm, Hochschule, Behörde (NASA Glenn, MIT OpenCourseWare, Bosch, Schaeffler). URL und Abrufdatum in `plan.sources`; Abruf höchstens 30 Tage vor dem Export, sonst neu prüfen. Jede Zahl im Video hat eine Quelle oder wird im Bild gerechnet. Unbelegtes steht in `unverified` und wird nicht gesagt.
8. **Langzeitbelichtung ist ein Schema.** Sie behauptet keine Kameraaufnahme. Dichte an den Totpunkten ist physikalisch begründet (Verweildauer), alles Weitere ist Darstellung.
9. **Neue Mechanik nur mit eigener Rechnung.** Zweitakt, Turbolader, Wankel, variable Steuerzeiten: erst eine gerechnete Szene mit Quelle bauen, dann das Thema produzieren. Bis dahin Thema zurückstellen.
10. **Schema, keine Wartungsanleitung.** Keine Wartungs-, Reparatur- oder Tuningempfehlung, keine Schadensdramatik, keine Marken-Abwertung (unverändert aus Vorlage 0.9).

Gemeinsam mit allen Marken, unverändert: Gemini-Stimme, Untertitel, Export, `node scripts\overlap_check.mjs` ohne Befund, KI-Kennzeichnung.

## 7. Produktion je Video

1. Thema aus `data\calendars\engines_2026-11.json`, Quellen lesen und Seite notieren. Reihe festlegen.
2. Sprechtext so schreiben, dass er das Bild lenkt (Pfeil, Linie, Strich). Wenn ein Woche-1-Plan schon einen passenden Text und eine bezahlte Stimme hat, Text Wort für Wort übernehmen und die Stimme mit `--reuse-voice` verwenden (Pilot: so gemacht, 0 USD).
3. Plan `data\direction\<video_id>.zeitlupe.json`: `layout.format: "zeitlupe"`, `layout.explainer: false`, Szenen `zl_*` mit `theta`-Stützpunkten an Wörtern, `source` je Szene. Muster: Pilotplan.
4. Trockenlauf mit echter Stimme ohne Video: `.venv\Scripts\python.exe scripts\render_direction.py <plan> --version P1dry --reuse-voice <wav> --no-render`, dann `node scripts\overlap_check.mjs storage\direction\<id>-P1dry\project` und `npx hyperframes snapshot . -o ../snapshots --at <Zeiten>` im Projektordner.
5. Render über die Warteschlange: `.venv\Scripts\python.exe scripts\render_queue.py engines -- scripts\render_direction.py <plan> --version P1 --reuse-voice <wav>` (oder `--tts gemini` bei neuem Text).
6. Überschneidungsprüfung, Sichtprüfung, Export mit `scripts\export_production_folder.py`, Redaktionsplan-Zeile. Nichts veröffentlichen.

Szenen-Datenfelder (Kurzreferenz, Details im Docstring von `zeitlupe\scenes.py`):
- `zl_hook`: `claim`, `claim_lines`, `claim_highlight`, `claim_at`, `slow_at`, `mid_at`, `strike_at`, `theta`, `source`.
- `zl_strobe`: `theta`, `arrow_at`, `zero_top_at`, `zero_bottom_at`, `gap_at`, `step`, `ticks_shown`, `notes`, `source`.
- `zl_cause`: `theta`, `rod_at`, `beta_at`, `pins_at`, `sine_at`, `rod_off_at`, `notes`, `ticks_shown`, `source`.
- `zl_trace`: `theta`, `series` [`kind` sine|real, `mode` live|draw|show, `at`], `marks`, `curve_notes`, `notes`, `dial`, `source`.
- `zl_realtime`: `theta` (beschleunigend), `real_at`, `rows`, `brand`, `source`.
- Alle: `ref_rpm` (Standard 3000), `view` `{s, top, x}`, `dial`.

## 7a. Übernahme von Woche 1 (09.–15.11.2026)

Die 40 vorhandenen Pläne von Woche 1 behalten ihren Sprechtext und ihre bezahlte Gemini-Stimme. Umgestellt werden sie mit `brands\engines\zeitlupe\convert_plan.py` (Ergebnis `data\direction\<id>.zeitlupe.json`, alter Plan unverändert):

- Hook wird `zl_hook`: die ersten 15 % Echtzeit als Langzeitbelichtung, dann Zeitlupe; Aussage unverändert.
- Schluss wird `zl_realtime`: die Chips werden Ergebniszeilen am Wort, der Motor läuft auf Echtzeit hoch, Markenzeile.
- Die Mitte bleibt inhaltlich die Q1-Szene, läuft aber im Zeitlupe-Rahmen (`zlx_*`): Messraum-Grund, kein Push-in, kein Kopftitel, keine Arbeitsspiel-Leiste (außer die Stimme spricht von ihr), Beschriftungen als Text mit Führungslinie statt Karten, Zeitlupen-Band nur dort, wo sich der Motor bewegt, Quellenzeile.
- Bezugsdrehzahl je Thema: 1200/min bei „Ein Arbeitsspiel dauert 100 Millisekunden“, 600/min bei „So wird die Oktanzahl gemessen“, 180/min bei „Ottos Viertakt-Patent“, sonst 3000/min.

Ab Woche 2 werden Texte für das Format neu geschrieben (Abschnitt 3) und die Mitte mit `zl_strobe`, `zl_cause` und `zl_trace` gebaut.

## 8. Offene Punkte für Stefans Freigabe

- Formatname „Zeitlupe“, Kanalsatz in Abschnitt 1, Bezugsdrehzahl 3000/min als fester Beispielwert.
- Pilot `05 Produktion\Revlore\2026-11\2026-11-09 Pilot Kolbentempo`: Freigabe von Optik und Ablauf. Der Sprechtext stammt unverändert aus dem Woche-1-Plan; er nennt den Echtzeit-Zeitlupe-Wechsel noch nicht ausdrücklich. Künftige Texte sollten das tun (Abschnitt 3).
- Reihenzuordnung der 84 Kalenderthemen (Abschnitt 4) und welche der 41 Woche-1-Pläne mit ihrer Stimme übernommen werden. Gut passen Texte, die schon auf das Bild zeigen; Pläne, deren Mitte eine Tafel (`rv_board`) oder Rechnung (`rv_readout`) ist, brauchen neuen Text und eine neue Stimme.
- Code noch zu bauen: zwei Kurven mit geändertem Modellwert in `zl_trace` und zwei Lineale nebeneinander (Reihe „Ein Schalter, zwei Schriebe“), Druck- und Ventilhubschrieb im Takt (`kind: pressure`, `valve_lift`), historische Modelle (Reihe „Erstes Modell“).
- Aussprache des Markennamens: Die Transkription hört in den wiederverwendeten Stimmen „Revolor“ (DE) und „RevLor“ (EN), Prüfrunde 03.11.2026. Stefan hört bitte den Schluss des Piloten an und legt die Aussprache fest; neue Stimmen bekommen dann einen Aussprachehinweis in `audio_style.yaml`.
- Unterscheidbarkeit zu Gigastruct (Prüfrunde: beide dunkel blaugrau mit Oswald und Mono): Revlores eigene Merkmale sind das Zeitlupen-Band, die Langzeitbelichtung und das Stroboskop-Lineal. Wenn das nicht reicht, wäre der nächste Schritt ein wärmerer Grundton (Graphit mit Bernstein-Hilfslinien) statt Blaugrau; nicht umgesetzt, Entscheidung Stefan.
