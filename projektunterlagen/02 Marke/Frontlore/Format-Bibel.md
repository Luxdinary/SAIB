# Frontlore – Format-Bibel „Rekonstruktion“

Stand: 02.11.2026 (Wien), Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026** (Format und Pilot „Fackeltelegraf“, über die Hauptsitzung: „Beide“; Bedingung: Der Neu-Render besteht alle Prüfungen. Für die DE-Fassung am 02.11.2026 erfüllt). Frontlore bleibt Risiko „hoch“: Jedes Video endet in HUMAN_REVIEW und geht einzeln an Stefan. Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke bekommt ein eigenes Format, gemeinsam bleiben nur Technik und Prüfungen) und die Bewertung im `Statusbericht neun Marken 2026-11-02.md` (historische technische Probleme mit Karten, Modellen und Archivquellen rekonstruieren). Ersetzt für neue Videos die `Vorlage Frontlore.md` (Version 0.9: Archivkarte, Statusleiste, Erklärschicht, Depesche als Leitobjekt). Die alte Vorlage bleibt als Nachweis liegen, alte Pläne rendern unverändert.

Umsetzung: `C:\Automation\faceless-network\brands\military_history\rekonstruktion.py` (Szenentypen `fr_*`, Ebene mit Zeitlineal), eingebunden am Ende von `frontlore_scenes.py`. Pilotplan: `data\direction\military_history-20261109-1-de.rekonstruktion.json`.

## 1. Versprechen

**„Ein technisches Problem aus der Geschichte, so wie es die Quellen beschreiben: was die Ingenieure damals lösen mussten, womit sie es gelöst haben und was davon wirklich belegt ist.“**

- Eine Folge, **ein** Problem. Nicht „die Geschichte des Nachrichtenwesens“, sondern „Wie sendet man einen ganzen Satz nur mit Feuer?“.
- Das Bild zeigt das Problem und die Lösung als Linienmodell, nie Kampf, nie Personen als Helden.
- Jede Szene nennt die Stelle, aus der sie stammt, wie in einer Fußnote: „POLYB. X 45,6–7“.
- Was die Quelle beschreibt, ist durchgezogen gezeichnet; was Frontlore ergänzt, ist gestrichelt; was fehlt oder unsicher ist, ist schraffiert. Der Zuschauer sieht so jederzeit, wo die Quelle endet.
- Am Ende steht ein Befund: was erhalten ist, was belegt ist, was umstritten bleibt.

Ein Satz für die Kanalbeschreibung: *„Historische Technik, aus den Quellen rekonstruiert: Problem, Lösung, Beleg.“*

Zielgruppe unverändert: Menschen, die Geschichte und Technik interessieren; streng historisch und öffentlich dokumentiert.

## 2. Bildsprache: „Kartentisch“

Das Bild ist ein Arbeitstisch mit Karte, auf dem rekonstruiert wird.

| Element | Regel |
|---|---|
| Grund | Olivgrund mit Papierstruktur (`assets\bg\base.jpg`, eigene Arbeit) und einem ruhenden **Gradnetz** (Meridiane und Breitenkreise einer Kegelkarte, sehr schwach). Keine Höhenlinien, kein Schwenk, keine Drift. Bewegung kommt nur aus dem Modell. |
| Zeitlineal (Erkennungszeichen 1) | Oben unter dem Logo, das ganze Video: Jahrhunderte mit Teilstrichen (`layout.ruler`). **Gesicherte Daten** als Strich oder volle Balken, **unsichere Daten** als schraffierte Enden oder schraffierte Spanne mit Wort („LEBENSDATEN UNSICHER“, „QUELLEN UNEINIG“). Einträge erscheinen mit dem Beat, in dem sie gelten. |
| Stellenangabe (Erkennungszeichen 2) | Über jedem Szenentitel in Mono und Akzentfarbe die Quellenstelle („POLYB. X 45,8–12“). Der Titel selbst in Oswald, Versalien, links bündig, mit Haarlinie. |
| Linienregel (Erkennungszeichen 3) | Durchgezogen = in der Quelle beschrieben. Gestrichelt = Rekonstruktion oder Vereinfachung (Form, Proportionen, Aufstellung). Schraffiert (Bernstein auf Olive) = nicht erhalten, nicht sendbar, unsicher. Beim ersten Modell steht die Legende „— Quelle · - - Rekon.“ im Bild. |
| Linienmodell | Hauptmotiv jeder Szene, aus Strichen gezeichnet, die sich am gesprochenen Wort zeichnen (Tafeln, Signalwand, Gefäße, Stationen, Schnitt durch Gelände). Keine Fotos, keine KI-Bilder, keine Waffen als Gegenstand. |
| Farben | Palette aus `brand.yaml` unverändert: Olive `#29352D`, Fläche `#38433C`, Linie Text `#E6E9E5`, Akzent `#A9B29F` (Stellenangabe, Belegt-Quadrat, Zustände), Bernstein `#D9B45A` **nur für Feuer, Licht und Unsicherheit**, Papier `#E9E4D4` nur für das Befundblatt und den Notizzettel, Tintenblau `#2B4257` für das gewählte Element. Rot gibt es nicht. |
| Prüfzeichen unten | Je Szene über der Quellenzeile ein bis zwei Chips mit Form und Wort: Quadrat voll = **BELEGT**, Quadrat gestrichelt = **REKONSTRUIERT**, Quadrat schraffiert = **UMSTRITTEN**, violette Raute = **AUSLEGUNG**. Darunter „Quelle: …“ mit Kurzzitat der Stellen (y 1176 und 1210, zweite Zeile 1242; bricht an den Trennpunkten um). Prüfzeichen und Quelle 28 px. |
| Wiederkehrende Bausteine | **Aufgabe** (Frage groß, Geländeschnitt Sender–Empfänger, leere Zeichenkästchen), **Mittel der Zeit** (zwei Spalten, Grenze als schraffiertes Feld mit Stempel), **Lösung** (Tafeln, Modell, Legende), **Ablauf** (Sequenz zwischen zwei Stationen, Zeit läuft nach unten), **Probe** (Fall aus der Quelle, Notizzettel mit Ergebnis), **Stufen** (nummerierte Karten mit „meldet: …“), **Befundblatt** (Papier, Zeilen GERÄT · TEXT · PRAXIS · FORSCHUNG). |
| Schrift | Oswald 500 (Titel, Frage, Werte), JetBrains Mono (Stellenangaben, Beschriftungen, griechische Buchstaben, Zeitlineal), Inter in den gemeinsamen Untertiteln. |
| Kennzeichnung | „KI-generiert“ dauerhaft unten (gemeinsame Regel). In `post.json` die Labels der Plattformen. |
| Entfällt | Erklärschicht (Kicker, „SYNTHETISCHE STIMME“, Marker-Kapsel, Einstiegszeile), Statusleiste, Depesche als Leitobjekt, Archivkarte mit Stempel als Hook, Höhenlinien mit Schwenk, Kreisübergänge. |

Senkrechte Aufteilung (1080 × 1920, seit der Prüfrunde R5): Logo 120–160 · Zeitlineal 196–282 · Stellenangabe 326 · Titel 396 · Bühne 440–1150 · Prüfzeichen 1176 · Quelle 1210/1242 · Szenenzone endet bei 1250 (`zone_h` 960, `zone_lower_right_px` 920) · Untertitel etwa 1300–1420 (`caption_bottom_px` 500) · „KI-generiert“ etwa 1460–1490 (gemeinsam, 430 px über dem Rand) · Fortschritt 1548. Unterhalb von y 1100 und rechts bleibt alles links von x 920. Schrift: Nebentexte mindestens 24 px, Belege 28 px (R7).

## 3. Dramaturgie (gemessen am Piloten, 74,9 s; erlaubt 65–90 s)

| Sekunde (Pilot) | Beat | Szenentyp | Inhalt |
|---|---|---|---|
| 0–6,8 | Aufgabe (Hook) | `fr_task` | Die Aufgabe als Frage, nie eine Rekordzahl. Am Wort zeichnet sich der Geländeschnitt, die leeren Kästchen des Satzes erscheinen, die Entfernung, dann das Feuer. Zeitlineal zeigt die Epoche. |
| 6,8–17,3 | Mittel der Zeit | `fr_means` | Was es schon gab, und genau eine Grenze. Zwei Spalten mit Modell (Leuchtfeuer mit vereinbarten Meldungen, Wasseruhr mit sinkendem Pegel). Die Grenze kommt als schraffiertes Feld mit Stempel („NICHT SENDBAR“). |
| 17,3–31,3 | Lösung | `fr_solution` | Die Idee der damaligen Ingenieure als Linienmodell: erst das Prinzip (Tafeln mit Buchstaben), dann das Gerät (Signalwand, Visier). Legende der Linienregel. |
| 31,3–41,1 | Ablauf | `fr_protocol` | Wie es benutzt wurde, als Sequenz zwischen zwei Stationen, Zeit läuft nach unten. Jede Zeile an ihrem Wort. |
| 41,1–50,1 | Probe | `fr_example` | Ein Fall, den die Quelle selbst gibt (Pilot: Polybios' Kappa, Tafel 2, Stelle 5). Fackeln zählen, Tafel und Feld leuchten, der Empfänger notiert das Ergebnis auf einem Zettel. |
| 50,1–60,2 | Stufen | `fr_stages` | Woher die Lösung kam und was sie besser konnte: zwei bis drei nummerierte Stufen mit „meldet: …“. Unsichere Datierung als schraffierter Chip und im Zeitlineal. |
| 60,2–74,9 | Befund | `fr_finding` | Befundblatt: was erhalten ist, wo es steht, was die Quelle selbst einschränkt, was die Forschung bestreitet. Markenzeile am Wort „Historische“. |

Regeln für Sprechtext und Bild:
- Gemini Charon DE spricht hier etwa 2,1 Wörter oder 14,1 Zeichen je Sekunde (Pilot: 152 Wörter, 1.016 Zeichen, 72,1 s). Ziel **140–175 Wörter** (1.000–1.200 Zeichen) für 70–85 s.
- Jede Szene hat mindestens drei Bildereignisse an gesprochenen Wörtern (`"w:Wort"`); längste Strecke ohne Bildereignis höchstens 8 s.
- Die Stimme beschreibt, was das Bild zeigt, und überlässt dem Bild Stellenangaben und Datierungen. Zahlen im Sprechtext nur gesicherte; Spannen sagt die Stimme mit „etwa“ oder „zwischen“.
- Ton ruhig und sachlich, „du“ nur in der Handlungsaufforderung, kein Pathos, kein „legendär“, keine Kampfgeräusche. Schluss: „Historische Technik, sachlich erklärt: Folge Frontlore.“

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Kalender `military_history_2026-11.json` |
|---|---|---|---|
| **Rekonstruktion** (Hauptreihe) | Ein Übertragungs-, Mess- oder Bauproblem und die Lösung der damaligen Ingenieure, aus der Quelle nachgebaut (Fackeltelegraf, Flügeltelegraf, Heliograf, Zeitball, Basislinie, Bailey-Brücke). | task → means → solution → protocol → example → stages → finding | Signal und Nachricht, Karte, Zeit und Kurs, Teile von Gebaut für den Ernstfall |
| **Versorgt** | Ein Problem der Versorgung: haltbar machen, transportieren, zählen (Konserve, Schiffszwieback, Lind 1747, Luftbrücke, PLUTO, Penicillin im Tiefentank). Der Ablauf ist eine Kette von Stationen, die Probe eine dokumentierte Menge mit Datum. Opfer und Folgen (z. B. Skorbut) sachlich mit Zahl und Quelle. | task → means → solution → protocol (Kette) → example → finding | Nachschub |
| **Quellenprobe** | Eine verbreitete Behauptung („Hörnerhelme“, „Karotten für Nachtsicht“, „SOS heißt Save Our Souls“). Das Zeitlineal zeigt, **wann die Behauptung zuerst in den Quellen auftaucht** und wann das Ereignis war; das Befundblatt urteilt nach Quellenlage: `QUELLE SAGT` · `QUELLE SAGT NICHT` · `SPÄTERE ZUTAT`, nie „Lüge“. | task (Behauptung) → stages (Belegkette) → example → finding (Urteil) | Mythos geprüft |
| **Vermessen** | Karten- und Navigationsaufgaben (Cassini-Karte, Josephinische Landesaufnahme, H4, LORAN, Transit): Problem auf der Karte, Messverfahren im Modell, erreichte Genauigkeit mit Quelle. Braucht noch eine Kartenszene (`fr_map`, siehe 8). | task → means → solution (Karte) → protocol (Messung) → finding | Karte, Zeit und Kurs |

Beim Neuschreiben bekommt jede Kalenderzeile eine dieser Reihen im Feld `notes`. Themen, die nur Kampfhandlung oder Waffenwirkung erzählen würden, passen nicht und werden ersetzt.

## 5. Abgrenzung zu den anderen acht Marken

| Marke | Kern ihres Formats | Frontlore dagegen |
|---|---|---|
| Scutoria | „Was tust du?“: Fall aus einem Betrieb, Uhrzeit, Entscheidung A/B/C, Papierkarte als Fallobjekt | Keine Entscheidung des Zuschauers, keine Uhrzeit, Gegenwart kommt nicht vor. Die Zeit läuft in Jahrhunderten auf dem Zeitlineal. |
| Promptwerk | „Echtlauf“: aufgezeichnetes Terminal | Nichts ist aufgezeichnet, alles ist aus Text rekonstruiert, und das Bild sagt, wie weit. |
| Tintora (vormals Zonkfruit) | Anime-Kinderserie mit Figuren | Keine Figuren, keine Fiktion, keine KI-Bilder. |
| Dewlane | „Nahaufnahme“: KI-animierte Beauty-Anwendung, Lupe | Kein Produkt, keine Lupe, keine Wirkungsbehauptung; Linienmodell statt weicher Studiobühne. |
| Revlore | „Zeitlupe“: gerechnete Mechanik in Millisekunden, Messschrieb | Keine Kinematik, keine Messkurve; Frontlore zeigt ein Verfahren und seine Belege, nicht eine Bewegung. |
| Gigastruct | „Bauaufgabe“: Werkplan, 3D-Modell, Stückliste, Rechenblatt | Kein 3D-Modell, keine Rechnung als Hauptszene, kein Zeichnungsrahmen, keine Kapitelleiste. Frontlore rechnet nicht Größe, sondern prüft Überlieferung: Stellenangabe, Linienregel, Zeitlineal, Befund. |
| Suitwerk | Stoffe und Passform | Kein Körper, keine Kleidung, keine Uniform. |
| Gritwerk | Motivation, künftig Selbstversuche | Kein Appell, kein Mensch im Mittelpunkt. |

Merkmale, die nur Frontlore hat: Zeitlineal mit schraffierten unsicheren Daten, Stellenangabe über jedem Titel, Linienregel durchgezogen / gestrichelt / schraffiert, Befundblatt als Schluss.

## 6. Prüfregeln (vor jedem Render, zusätzlich zu den gemeinsamen Prüfungen)

Harte Grenzen (ein „nein“ heißt: Thema ersetzen, nicht abmildern):
1. **Nur Geschichte:** kein Ereignis nach 1991, kein laufender Konflikt, keine laufende politische Streitfrage, auch nicht als Vergleich („wie heute in …“).
2. **Keine Verherrlichung:** keine Helden, kein „legendär“, „gefürchtet“, „genial“ für Kriegsgerät, keine Kampfgeräusche, keine Musik mit Marschcharakter.
3. **Keine Gewaltbilder:** keine Toten, Verletzten, Treffer, Explosionen, auch nicht stilisiert. Opfer und Folgen werden **sachlich genannt**, wo sie zum Thema gehören (Zahl mit Quelle und Spanne, ein Satz), nie gezeigt und nie dramatisiert.
4. **Keine Symbole verbotener Organisationen**, auch nicht stilisiert, angeschnitten oder auf Karten, Fahnen, Modellen und Archivbildern (Österreich: Verbotsgesetz 1947 und Abzeichengesetz; Deutschland: §§ 86, 86a StGB). Praktische Regel: Karten und Modelle zeigen **keine** Hoheitszeichen, Fahnen, Abzeichen oder Uniformen; Staaten und Verbände stehen nur als Text, wenn nötig.
5. **Keine nachbaubare Anleitung:** kein Bau, Umbau oder Betrieb von Waffen, Sprengstoffen, Brandmitteln oder Giften, keine Rezepturen, Mengen oder Maße, die heute zur Herstellung taugen. Das Verfahren wird so genau gezeigt, wie die Quelle es beschreibt, und nur, wenn es heute ungefährlich ist (Signal, Vermessung, Brücke, Konserve ja; Zündmechanismen, Ladungen nein). Im Zweifel: Thema ersetzen.
6. Nichts aus Stefans Dienst, keine Bezüge zum Bundesheer (§ 46 BDG), keine Taktik, keine Lagebeurteilung (unverändert aus Vorlage 0.9, G2–G5).
7. Keine Personen als Hauptmotiv, keine Porträts, keine erfundenen Zitate. Zitate nur kurz und mit Stelle.

Quellen:
8. **Mindestens zwei Quellen je Kernaussage**, davon mindestens eine Primärquelle (antiker Text in anerkannter Edition, Archivdokument, Patent, amtlicher Bericht) oder Fachpublikation; die zweite unabhängig davon (Fachliteratur, Museum, Archiv, Hochschule). Jede Quelle mit **URL, Abrufdatum und Stelle** (Buch/Kapitel/Abschnitt, Seite oder Anmerkung) in `plan.sources[]` (`url`, `checked_at`, `label`, `passages`). Für das Video selbst geöffnet; Abruf höchstens 30 Tage vor dem Export. Wikipedia und Suchergebnisse nur zum Finden, nie als Beleg.
9. **Kernaussage** heißt: jede gesprochene Tatsache und jede Zahl, jedes Datum und jede Beschriftung im Bild. Was nur eine Quelle hat, kommt nach `unverified` und nicht ins Video (Pilot: Datierung des Aineias, „das Visier vergrößerte nicht“).
10. **Aussagen über eine Quelle** („Polybios beschreibt …“, „sein eigenes Beispiel“) belegt die Quelle selbst mit Stellenangabe; dann steht der Chip „BELEGT“ oder „BEISPIEL AUS …“.
11. **Fehlen ist eine Auslegung.** „Kein Gerät erhalten“, „nie eingesetzt“ und Ähnliches tragen die Raute **AUSLEGUNG** und nennen, worauf sie sich stützen.
12. **Die Linienregel ist eine Aussage.** Durchgezogen nur, was die zitierte Stelle beschreibt; alles Ergänzte gestrichelt und als „REKONSTRUIERT“ ausgewiesen.

Umstrittene Zahlen und Daten:
13. **Spanne statt Einzelwert.** Weichen Quellen ab, zeigt das Bild die Spanne (schraffiert im Zeitlineal, „etwa 208 oder 200 v. Chr.“), nennt beide Quellen und nimmt nie den dramatischeren Wert. Die Stimme sagt die Spanne oder sagt keine Zahl.
14. **Opfer- und Verlustzahlen** nur als Spanne mit zwei Quellen und Jahr der Quelle; ohne belastbare Spanne fällt die Zahl weg, der Satz bleibt ohne Zahl.
15. **Forschungsstreit** darf mit einer Übersichtsquelle genannt werden, die den Stand referiert (Pilot: Moore 2017, Anm. 40, zu Riepl und Donaldson), nur als „umstritten“ mit schraffiertem Chip, nie als eigene Behauptung, und mit dem Vermerk in `unverified`, dass die referierten Werke nicht selbst eingesehen wurden.
16. Datierungen in Jahrhunderten, wenn die Quellen nur das hergeben. Widerspricht sich eine Einrichtung selbst (Pilot: Kotsanas-Museum nennt 3. und 2. Jh. v. Chr.), steht im Bild „QUELLEN UNEINIG“.

Bildrechte für Archivmaterial:
17. Das Format braucht **kein Archivmaterial**: Modelle, Karten und Tafeln sind eigene Linienzeichnungen (eigene Arbeit, Nachweis im Plan). Das ist der Normalfall.
18. Wird doch ein Archivbild gezeigt (Karte, Patentzeichnung, Seite einer Handschrift, Foto), dann nur:
    - gemeinfrei: Urheber seit mehr als 70 Jahren tot; bei Fotos zusätzlich Lichtbildschutz abgelaufen (Österreich § 74 UrhG, Deutschland § 72 UrhG: 50 Jahre). Für originalgetreue Wiedergaben gemeinfreier Werke der bildenden Kunst gilt Art. 14 der Richtlinie (EU) 2019/790; die Nutzungsbedingungen des Archivs werden trotzdem gelesen und eingehalten.
    - oder mit offener Lizenz (CC0, CC BY, CC BY-SA) mit Namensnennung im Bild und in der Beschreibung.
    - Nachweis vor dem Render in `08 Recht und Verwaltung\Lizenzen\Frontlore\<JJJJ-MM-TT> <Bild>.md`: Archiv, Signatur, URL, Lizenz oder Grund der Gemeinfreiheit, Abrufdatum, Bildschirmfoto der Lizenzangabe.
    - nie mit verbotenen Symbolen (Regel 4), nie mit Toten oder Verletzten (Regel 3), keine Fotos von Personen als Hauptmotiv, keine KI-Nachbildung realer Archivfotos.
    - Dies ist keine Rechtsberatung; vor der ersten Nutzung eines Archivbilds klärt Stefan den Einzelfall.
19. „KI-generiert“ dauerhaft im Bild; `is_aigc`, `is_ai_generated`, `containsSyntheticMedia` in `post.json`. Keine realistische KI-Szene eines realen Ereignisses (Art. 50 KI-Verordnung). Keine Musik ohne Lizenz.

Freigabe: `risk_level` high; jedes Video endet in **HUMAN_REVIEW** und geht nur mit Stefans Freigabe hinaus.

Technik (gemeinsam, unverändert): Gemini-Stimme (nie SAPI/Edge), 65–90 s, `story.validate` und Trockenlauf ohne Fehler, `node scripts\overlap_check.mjs` ohne Befund am Render, Render nur über `scripts\render_queue.py`.

## 7. Plan-Parameter und Ablauf je Video

```json
"layout": {"format": "rekonstruktion", "explainer": false, "outro": false, "zone_h": 960, "zone_lower_right_px": 920, "caption_bottom_px": 500, "progress_y": 1548,
           "ruler": {"from": -300, "to": -100, "major": 100, "minor": 25,
                     "items": [{"kind": "bar", "from": -208, "to": -118, "fuzzy": [[-208, -200], [-126, -118]], "label": "...", "beat": "b1"},
                               {"kind": "mark", "at": -167, "beat": "b1"},
                               {"kind": "range", "row": 1, "from": -300, "to": -101, "label": "... QUELLEN UNEINIG", "beat": "b6"}]}}
```

Szenendaten (Kurzform, Details im Kopf von `rekonstruktion.py`); jede Zeit darf eine Zahl (Sekunden ab Beat) oder ein Wortanker `"w:Wort"` / `"w:Wort#2"` sein. Alle Szenen: `cite_head` (Stellenangabe), `headline`, `status[{kind: belegt|rekonstruiert|umstritten|auslegung, text, at}]`, `cite`.
- `fr_task`: `question_lines`, `question_em`, `land_at`, `boxes_at`, `dist_at`, `distance`, `fire_at`, `from`, `to`, `boxes`.
- `fr_means`: `left{title, items}`, `right{title, marks, note}`, `left_at`, `items_at`, `right_at`, `flow_at`, `unforeseen{label, stamp}`, `unforeseen_at`, `mute_at`.
- `fr_solution`: `tablets_at`, `letters_at`, `note`, `legend`, `wall_at`, `left_at`, `right_at`, `left_label`, `right_label`, `tube_at`, `tube_label`.
- `fr_protocol`: `lanes`, `lanes_at`, `rows[{kind: pair|send|reply|line, text, y, at, torches}]`.
- `fr_example`: `left`, `right`, `labels`, `wall_at`, `tablet_at`, `cell_at`, `left_at`, `right_at`, `look_at`, `write_at`, `note`.
- `fr_stages`: `stages[{title, sub, can, at, chip, chip_at, stamp, stamp_at}]`.
- `fr_finding`: `sheet`, `sheet_at`, `rows[{key, value, kind: hatch|disputed, at}]`, `brand`, `brand_at`.

Ablauf (PowerShell im Repository, vorher `$env:PYTHONIOENCODING = "utf-8"`):
1. Thema aus dem Kalender, Grenzen 1–7 prüfen, Reihe festlegen.
2. Quellen öffnen, Stellen notieren, Kernaussagen gegen Regel 8–16 prüfen; Unbelegtes nach `unverified`.
3. Sprechtext schreiben. Passt ein Woche-1-Text Wort für Wort, wird die bezahlte Stimme mit `--reuse-voice` übernommen (Pilot: so gemacht, 0 USD).
4. Plan `data\direction\<video_id>.rekonstruktion.json` (Muster: Pilotplan).
5. Trockenlauf: `.venv\Scripts\python.exe scripts\render_direction.py <plan> --version P1dry --reuse-voice <wav> --no-render` (oder `--tts mock`), dann `node scripts\overlap_check.mjs storage\direction\<id>-P1dry\project` und `npx hyperframes snapshot . -o ..\snapshots --at <Zeiten>` im Projektordner.
6. Render: `.venv\Scripts\python.exe scripts\render_queue.py military_history -- scripts\render_direction.py <plan> --version P1 --reuse-voice <wav>` (oder `--tts gemini` bei neuem Text).
7. `node scripts\overlap_check.mjs storage\direction\<id>-P1\project`, Sichtprüfung, Export mit `scripts\export_production_folder.py`, Zeile im Redaktionsplan. Nichts veröffentlichen; Status HUMAN_REVIEW.

## 8. Offene Punkte

- Erledigt: Formatname, Kanalsatz, Bildsprache und Pilot sind freigegeben (02.11.2026).
- Ziel der Hauptsitzung bis 05.11.2026: drei Themen aus Woche 1 in DE und EN (Fackeltelegraf, Hadrianswall, Dose ohne Öffner). Dafür gibt es den allgemeinen Szenentyp `fr_model` (Linienmodell, Maße, Zähler, Raster, Stempel aus Plandaten).
- Reihenzuordnung der 84 Kalenderthemen (Abschnitt 4) und welche der 42 Woche-1-Pläne mit ihrer Stimme übernommen werden. Bezahlte Gemini-Stimmen gibt es für Woche 1 nur bei Polybios (DE, EN) und Neuf-Brisach (DE), dazu der alte Testvideo-Text Optischer Telegraf (DE, EN); alle anderen Pläne brauchen eine neue Stimme (etwa 0,02 USD je Video).
- Themen mit Überschneidung zu Gigastruct (Hadrianswall, Limes, Mulberry, Martello-Türme, Bailey-Brücke): Vorschlag Frontlore behält sie, erzählt sie aber aus den Quellen (Befund, Zeitlineal), Gigastruct baut sie nicht als „Damals gelöst“.
- Code noch zu bauen: Kartenszene `fr_map` (Küstenlinie schematisch, Stationen, Sichtlinien, Messdreiecke) für „Vermessen“ und Teile von „Rekonstruktion“; Urteilszeilen `QUELLE SAGT / QUELLE SAGT NICHT / SPÄTERE ZUTAT` im Befundblatt für „Quellenprobe“; Stationskette für „Versorgt“. Die Fackel-Bausteine (Signalwand, Tafeln) sind auf den Piloten zugeschnitten; weitere Geräte werden nach demselben Muster als Linienmodelle ergänzt.
- Englische Fassung: Szenentexte stehen im Plan; die englische Fassung braucht eigene Szenentexte (EN-Plandatei) und nutzt die vorhandene EN-Stimme, wenn der Text gleich bleibt.
- Kalenderzeile „Das Rote Kreuz: ein Schutzzeichen seit 1864“: das Zeichen ist geschützt (Genfer Abkommen); Darstellung vor Produktion rechtlich prüfen. „Enigma“ und „Jeffersons Chiffrierwalze“: nur Geschichte und Zahl, keine Bauanleitung.
- Musik weiterhin offen (keine Musik).

## 9. Pilot „Fackeltelegraf“

- Export: `05 Produktion\Frontlore\2026-11\2026-11-09 Pilot Fackeltelegraf\04 Export\2026-11-09 Pilot Fackeltelegraf – 9x16.mp4`, **75,1 s**, Kontaktbogen `03 Schnittprojekt\Kontaktbogen P1.png`. Render `storage\direction\military_history-20261109-1-de-P1`, Spiegel `05 Produktion\_Demos\frontlore-regie\p1`.
- Englische Fassung: `05 Produktion\Frontlore\2026-11\2026-11-09 Pilot Fackeltelegraf EN\04 Export\…EN – 9x16.mp4`, **83,1 s**, EN-Stimme aus Woche 1 (0 USD), Plan `data\direction\military_history-20261109-1-en.rekonstruktion.json`, HUMAN_REVIEW, `overlap_check` ohne Befund, `small_text` leer.
- Thema aus dem Kalender: „Polybios' Fackeltelegraf“ (09.11., Reihe Signal und Nachricht). Reihe im neuen Format: Rekonstruktion.
- Sprechtext Wort für Wort aus dem Woche-1-Plan, Gemini-Stimme Charon mit `--reuse-voice` übernommen: **0 USD** (bezahlt am 01.11. mit 0,018 USD).
- Prüfung: Prüfbericht **HUMAN_REVIEW** (einzige offene Prüfung `risk_high_review`, gewollt), `story.validate` und HyperFrames ohne Fehler (eine Craft-Warnung: Mono-Beschriftungen unter 28 px), Lautheit −15,4 LUFS, 40 Bildereignisse, Median 1,5 s, `node scripts\overlap_check.mjs` **ohne Befund**.
- Quellen selbst geöffnet am 02.11.2026: Polybios X 43–47 (Loeb 1925, LacusCurtius), Moore, Histos 2017 (PDF), Kotsanas-Museum (drei Seiten), Loeb-Einleitung, World History Encyclopedia. Jede gesprochene Aussage hat mindestens zwei Quellen; das Kappa-Beispiel ist Polybios' eigenes (X 46). Nicht im Video, sondern in `unverified`: Datierung des Aineias, „das Visier vergrößerte nicht“, die referierten Werke von Riepl und Donaldson.
- Umstrittenes im Bild: Lebensdaten des Polybios (geb. um 208 oder 200, gest. um 126/125 oder 118 v. Chr.) schraffiert im Zeitlineal, gesichert nur „167 in Rom“; Erfindung des Fackelalphabets „3. oder 2. Jh. v. Chr. · Quellen uneinig“; Alltagstauglichkeit „umstritten“; „kein Gerät erhalten“ als Auslegung.
- Eingearbeitet aus der unabhängigen Prüfrunde (02.11., Note 2,6): Flächen hinter Beschriftungen gefüllt (vorher kreuzten die Spurlinien im „Ablauf“ den Text), Tafeln und erste Stufe ab Szenenbeginn statt nach 1–3 s; nach R5 und R7 (Hauptsitzung) Bühne bis y 1150 mit größeren Modellen, Untertitel tiefer, Nebentexte ab 24 px, Belege 28 px, `overlap_check` ohne `small_text`. Nicht übernommen: „K bei x ≈ 1010“ (es steht bei x ≈ 860, links der Symbolspalte ab 930); „kein Untertitel bei 1:12“ (die Stimme endet bei 72,0 s, danach folgt der stille Nachlauf); „untere Bildhälfte leer“ ist mit R5 behoben, soweit die Untertitel es zulassen.
