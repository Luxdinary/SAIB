# Gigastruct – Format-Bibel „Bauaufgabe“

Stand 02.11.2026, Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026** (mit dem Piloten „Taipei 101“, über die Hauptsitzung: „Alle Videos freigegeben“). Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke ein eigenes Format) und die Bewertung von Codex (jede Folge eine konkrete Bauherausforderung, 3D-Modell, gerechnete Größenvergleiche). Ersetzt für neue Videos die `Vorlage Gigastruct.md` (Version 0.9); die alte Vorlage bleibt als Nachweis liegen, alte Pläne rendern unverändert.

Umsetzung: `C:\Automation\faceless-network\brands\megaconstruction\` – Szenentypen `gb_*` in `scenes_bauaufgabe.py` (eingebunden am Ende von `scenes.py`), 3D-Ebene `render\gigastruct3d.js` (neu: `tmd`, `wind`, Kapitelleiste), Renderaufruf `render\render_gigastruct.py` (neu: Quellenzeile, Zeichnungsrahmen, Kapitelleiste). Pilotplan `data\direction\megaconstruction-20261111-1-de.P1.json`.

## 1. Versprechen an den Zuschauer

**„In 80 Sekunden verstehst du eine echte Bauaufgabe: was das Problem war, welche Idee es gelöst hat und wie das Bauteil tatsächlich gebaut wurde. Jede Zahl mit Quelle, jeder Vergleich vor deinen Augen nachgerechnet.“**

- Eine Folge, **eine** Aufgabe. Nicht „das größte Bauwerk der Welt“, sondern „wie hält man 508 Meter im Taifun ruhig?“.
- Der Zuschauer sieht das Problem als Kraft (Wind, Wasser, Last, Boden), die Lösung als Mechanismus im Modell und den Bau als Stückliste, die sich im Modell zusammensetzt.
- Größe wird nicht behauptet, sondern auf einem Rechenblatt gerechnet; das Ergebnis erscheint erst, wenn die Rechnung dasteht.
- Am Ende steht die Probe: ein datiertes, belegtes Ereignis oder eine Grenze aus der Auslegung, kein „und es funktioniert perfekt“.

Zielgruppe unverändert: Menschen, die große Bauwerke faszinieren und die verstehen wollen, wie sie funktionieren (DACH; EN-Fassung international).

## 2. Bildsprache: „Werkplan“

Das ganze Bild ist ein technisches Zeichenblatt, über dem das 3D-Modell arbeitet.

| Element | Regel |
|---|---|
| Blatt | Dünner Zeichnungsrahmen mit Teilstrichen 36 px vom Bildrand (`#gbframe`), das ganze Video. Erkennungsmerkmal Nr. 1. |
| Kapitelleiste | Unter dem Logo (y 196) fünf Felder mit Nummer: `01 AUFGABE · 02 PRINZIP · 03 BAU · 04 RECHNUNG · 05 PROBE`. Aktives Kapitel orange, erledigte hell, kommende gedämpft. Ersetzt Statusleiste, Szenenzähler und Erklärschicht. |
| 3D-Modell | Hauptmotiv jeder Szene, Architekturmodell-Optik wie bisher (Three.js, matt `#D6DDE3`, Kanten `#3A5874`, Himmelskuppel). Neu: das **Lösungsbauteil** wird als eigenes, zusammensetzbares Modell gebaut (beim Piloten 41 Lagen, 92 Seile, 8 Dämpfer, Prallring). Lasten als hellblaue Pfeile (`wind`), nie orange. |
| Orange `#FF8A2A` | nur das Lösungsbauteil, gemessene Werte und Rechenergebnisse. |
| Flächen | eckig (kein Radius), 2 px helle Linie, Fläche aus der Grundfarbe zu 92 %. Kein Schatten, kein Glow. Bewusst anders als die alten Karten mit Radius 14 und Schatten. |
| Schrift | Oswald 700 in Versalien für Kapitelüberschriften („DER LASTFALL“, „SO WURDE SIE GEBAUT“), JetBrains Mono für alles Technische (Stückliste, Rechnung, Quelle, Stempel), Oswald 600 für Werte. Überschriften links bündig, nicht mittig. |
| Wiederkehrende Bausteine | **Lastfall-Kasten** (orange schraffierte Kante, großer Wert), **Stückliste** (Pos · Bauteil · Menge, füllt sich Zeile für Zeile), **Rechenblatt** (Karopapier, Rechnung schreibt sich von links, Ergebnis als oranger Block), **Prüfstempel** (Datum und Ereignis, leicht schräg), **Schriftfeld** (Abschluss als Zeichnungskopf: Aufgabe, Lösung, Bremse/Bauteil, Stand, „BLATT nn“). |
| Quellen | eine Monozeile unter der Szenenzone (y 1112) je Szene, automatisch aus den `source_ids` („Quelle: Taipei 101 (Betreiber)“). |
| Kennzeichnung | „KI-generiert“ dauerhaft unten; Hinweise „vereinfacht“, „überhöht“, „schematisch“ als gestrichelte Monoplakette in der Szene, in der sie gelten. |
| Entfällt | Statusleiste, Erklärschicht (Kicker oben, Stimmen-Tag, Marker-Chips Fakt/Auslegung), Leitobjekt-Kette, Logo-Intro, Endkarte, Turm-Glyphen. |

Untertitel wie bisher: Phrasen bis vier Wörter, Oswald 600, Highlight orange, 540 px vom unteren Rand. Inhalte zwischen y 290 und y 1100.

## 3. Dramaturgie (Ablauf in Sekunden, gemessen am Piloten)

Fünf bis sieben Beats, Länge 70–85 s. Die Länge wird vor der Vertonung mit `brands\megaconstruction\tools\bauaufgabe_len.py` geschätzt (kalibriert an drei echten Gemini-Stimmen: DE 15,0 Zeichen/s plus 0,32 s je Ziffer, EN 15,2 Zeichen/s plus 0,41 s je Ziffer; Ziffern werden langsam gesprochen). Ziel: Schätzung 70–84 s. Die Wortzahl allein taugt nicht: 136 deutsche Wörter ohne Zahlen ergaben 56 s, 147 Wörter mit vielen Zahlen 75 s.

| Zeit (Pilot) | Kapitel | Szenentyp | Inhalt |
|---|---|---|---|
| 0–9,0 | 01 Aufgabe | `gb_task` | Die Bauaufgabe als Frage (Hook). Stempel „BAUAUFGABE · <Bauwerk>“, Maßchip am Modell, Ortsangabe. Erster Satz ist die Frage, nicht eine Rekordzahl. |
| 9,0–17,6 | 01 Aufgabe | `gb_load` | Der Lastfall: die Kraft, gegen die gebaut wird (Bemessungswind, Wasserdruck, Last), mit Wert und Quelle; darüber das Ziel in einem Satz. Lastpfeile im Modell. |
| 17,6–25,4 | 02 Prinzip | `gb_principle` | Die Idee in einem Satz, im Modell vorgeführt (Turm hin, Kugel zurück). Plakette „vereinfacht · überhöht“. |
| 25,4–40,6 | 03 Bau | `gb_build` | Wie das Bauteil gebaut ist: Stückliste mit 3–5 Positionen, das Modell setzt sich am selben Wort zusammen. |
| 40,6–57,6 | 04 Rechnung | `gb_calc` | Zwei Rechnungen, die Größe oder Sicherheit greifbar machen. Ergebnis nur aus dem Renderer, nie getippt. |
| 57,6–68,3 | 05 Probe | `gb_proof` | Ein datiertes Ereignis aus einer Quelle (Prüfstempel) und eine Grenze der Auslegung (Skala). |
| 68,3–78,1 | – | `gb_close` | Schriftfeld mit der Folge in vier Zeilen, „Folge Gigastruct für die nächste Bauaufgabe.“ |

Jede Szene hat 3–5 wortgenaue Ereignisse (`"@Wort"`-Anker in Szenen und 3D-Keyframes); längste Strecke ohne Bildereignis höchstens 8 s.

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender |
|---|---|---|---|
| **Bauaufgabe** (Hauptreihe) | Ein Problem, eine Lösung, ein gebautes Bauteil: Dämpfer, Schleuse, Senkkasten, Tunnelelement, Hängebrückenseil. | task → load → principle → build → calc → proof → close | So wird's gebaut (5/Woche), dazu Rekord in Zahlen, wenn der Rekord eine Aufgabe löst |
| **Nachgerechnet** | Eine Behauptung oder ein Vergleich („mehr als dreimal der Eurotunnel“) wird zur Aufgabe; das Rechenblatt ist die Hauptszene mit 2–3 Zeilen, die Probe ist die zweite Quelle. | task → calc → build (woraus die Zahl kommt) → calc → close | Nachgerechnet (5), Rekord in Zahlen (4) |
| **Damals gelöst** | Eine historische Bauaufgabe: Problem mit den Mitteln der Zeit, Lösung, was danach anders gebaut wurde. Stempel mit historischen Daten; Kapitelleiste `AUFGABE · DAMALS · LÖSUNG · BAU · HEUTE`. | task → load → principle → build → proof (Datum) → close | Baugeschichte (4) |
| **Prüfstand** | Ein verbreiteter Satz über ein Bauwerk („Schwebt der Große Saal?“) wird geprüft; der Prüfstempel urteilt `BELEGT` / `TEILWEISE` / `NICHT BELEGT`, nie „Lüge“. | task → principle (was stimmt) → calc oder build → proof (Stempel) → close | Mythos-Check (3) |

Beim Neuschreiben bekommt jede Kalenderzeile eine dieser vier Reihen im Feld `notes`. Für „Damals gelöst“ und „Prüfstand“ fehlen noch: freie Kapitelbeschriftung je Reihe (geht schon über `layout.chapters`) und ein Urteilsstempel in `gb_proof` (siehe 7).

## 5. Was Gigastruct von den anderen acht Marken unterscheidet

| Marke | Format | Gigastruct dagegen |
|---|---|---|
| Scutoria | Fall aus dem Büro, A/B/C-Wahl, Uhr, Folge | keine Entscheidung des Zuschauers, keine Uhr; Gigastruct zeigt **Kräfte und Bauteile**, nicht menschliches Verhalten. |
| Promptwerk | echte Terminal-Aufzeichnung | kein Bildschirm, keine Software; ein räumliches Modell aus Grundkörpern. |
| Zonkfruit | Anime-Serie mit Figur | keine Figuren, keine Geschichte als Fiktion; Dokumentation an einem Modell. |
| Dewlane | KI-animierte Beauty-Anwendung | keine KI-Bilder, keine Fotorealistik; stilisierte Modelle, Werkplan-Optik. |
| Revlore | Motorentechnik | Gigastruct zeigt **ortsfeste Großbauwerke** und rechnet in Tonnen, Metern, Lastfällen; keine Maschinen im Betrieb. |
| Suitwerk | Herrenstil | kein Produkt, kein Körper. |
| Frontlore | historische Militärtechnik | keine Konflikte, keine Waffen; historische Themen nur als Bauaufgaben. |
| Gritwerk | Motivation | kein Appell an den Zuschauer, nur Sache. |

Erkennungsmerkmale, die keine andere Marke nutzt: Zeichnungsrahmen mit Teilstrichen, nummerierte Kapitelleiste AUFGABE → PROBE, Lastfall-Kasten, Stückliste im Bild, die sich mit dem Modell füllt, Rechenblatt auf Karopapier, Prüfstempel, Schriftfeld als Schluss.

## 6. Prüfregeln (vor jedem Render, zusätzlich zu den gemeinsamen Prüfungen)

Rechnungen:
1. **Jede Rechnung nachvollziehbar.** Operanden stehen im Plan (`gb_calc.calcs[].a/b/op`), das Ergebnis rechnet `scenes_bauaufgabe.py`; `expect` ist die gesprochene Zahl und muss gleich dem gerundeten Ergebnis sein, sonst bricht der Trockenlauf ab (Problem im Bericht). Jede Rechnung steht zusätzlich in `layout.computations` mit Quellen und landet im `manifest.json`.
2. **Beide Werte belegt.** Kein Operand ohne Quelle. Rundungen werden im Bild mit „≈“ und im Sprechtext mit „rund/etwa“ gezeigt; wenn die Quelle „etwa“ sagt, ist auch das Ergebnis „etwa“.
3. **Einheiten eindeutig.** Tonnen metrisch; US-Tonnen nur mit Umrechnung in `companion_text`. Formulierungen so, dass sie in jeder plausiblen Lesart der Quelle stimmen.
4. **Modellrechnung offen.** Was das Modell maßstäblich zeigt (z. B. 150 cm Ausschlag an 42 m Seil = 2,05°) steht in `computations`; was schematisch ist, steht in `unverified` und im Bild als Plakette.

Quellen:
5. Jede Zahl aus einer Primärquelle (Betreiber, Bauherr, Behörde, Tragwerksplaner, Fachzeitschrift) mit URL, Abrufdatum und kurzem `label`; die Quelle wurde für das Video **selbst geöffnet** (Pilot: 02.11.2026). Unbelegtes nur in `unverified`, nie ins Video (Pilot: keine Prozentzahl für die Schwingungsminderung, kein gemessener Ausschlag bei Soudelor).
6. **Probe nur mit Datum und Quelle.** Ereignisse wie Taifune oder Erdbeben nur so, wie die Quelle sie beschreibt („der Betreiber zeigt die Kugel in Bewegung“), keine erfundenen Messwerte.
7. Laufende Projekte nur mit „Stand <Monat Jahr>“; Eröffnungstermine nur aus aktueller Primärquelle.
8. Zweck einer Lösung so, wie der Betreiber oder Planer ihn nennt (Pilot: Komfort bei Wind, nicht „damit der Turm nicht umfällt“).

Bild und Recht:
9. Nur stilisierte Modelle aus Grundkörpern; keine Fotos, keine KI-Bilder realer Bauwerke. Überhöhungen und schematische Teile im Bild gekennzeichnet.
10. „KI-generiert“ dauerhaft im Bild; Labels `is_aigc`, `is_ai_generated`, `containsSyntheticMedia` in `post.json`. Keine Musik ohne Lizenz.

Technik (gemeinsam, unverändert): Gemini-Stimme (nie SAPI/Edge), 65–90 s, `story.validate` und Trockenlauf ohne Fehler, Textgrenzen der `gb_*`-Typen (`_GB_LIMITS`), `node scripts\overlap_check.mjs` ohne Befund am Render, Render nur über `scripts\render_queue.py`.

## 7. Plan-Parameter

```json
"layout": {"format": "bauaufgabe", "explainer": false,
           "chapters": {"labels": ["AUFGABE", "PRINZIP", "BAU", "RECHNUNG", "PROBE"], "beats": {"b1": 0, "b2": 0, "b3": 1, "b4": 2, "b5": 3, "b6": 4, "b7": 5}},
           "computations": [...], "model3d": {"objects": [...], "anchors": {...}, "shots": {...}}}
```

Szenendaten (Kurzform, Details im Kopf von `scenes_bauaufgabe.py`): `gb_task{kicker, question, tag, pins}`, `gb_load{headline, load{label, value, unit, sub}, goal}`, `gb_principle{headline, note, pins, rule}`, `gb_build{headline, rows[{pos, part, qty, at}]}`, `gb_calc{headline, calcs[{label, a, op, b, unit, round, prefix, expect, at, result_at}]}`, `gb_proof{headline, stamp{date, event}, limit{label, value, unit, ticks}, pins}`, `gb_close{statement, sheet, rows[[key, value]], cta}`. `pins` hängen an 3D-Ankern (`kind: dim|label`, `side: up|down`).

3D neu: `tmd` (Lagen `plates`, Seile `cables`, hervorgehobene Seile `hl`, Dämpfer `dampers`, Prallring `ring`, Ausschlag `swing` in Metern), `wind` (Lastpfeile, Stärke `wind` 0–1). Weitere Lösungsbauteile (Schleusenkammer mit Sparbecken, Senkkasten, Pendelschaft) werden nach demselben Muster als zusammensetzbare Grundkörper ergänzt.

Ablauf je Video: Plan schreiben → Trockenlauf `render_gigastruct.py <plan> --version dry --tts mock --no-render` → Standbilder mit `npx hyperframes snapshot` prüfen → Render über `scripts\render_queue.py megaconstruction -- brands\megaconstruction\render\render_gigastruct.py <plan> --version P1 --tts gemini` → `node scripts\overlap_check.mjs <projekt>` → `scripts\export_production_folder.py`.

### Kapitelleiste je Reihe

| Reihe | DE | EN |
|---|---|---|
| Bauaufgabe | AUFGABE · PRINZIP · BAU · RECHNUNG · PROBE | TASK · IDEA · BUILD · MATHS · TEST |
| Nachgerechnet | BEHAUPTUNG · DATEN · RECHNUNG · VERGLEICH · ERGEBNIS | CLAIM · DATA · MATHS · COMPARE · RESULT |
| Damals gelöst | AUFGABE · DAMALS · LÖSUNG · BAU · HEUTE | TASK · THEN · SOLUTION · BUILD · TODAY |
| Prüfstand | BEHAUPTUNG · BEFUND · GRUND · GEGENPROBE · URTEIL | CLAIM · FINDING · REASON · CHECK · VERDICT |

### Serienproduktion (Woche 1, 02.11.2026)

- `tools\bauaufgabe_w1.py`, `_w1b.py`, `_w1c.py`: je Thema eine kompakte Beschreibung (Szenen, Sprechtext und Szenendaten DE/EN, Kamera, 3D-Eigenschaften mit `%`-Zeiten).
- `tools\bauaufgabe_build.py <thema> …`: baut daraus `data\direction\megaconstruction-<thema>-<de|en>.P1.json`; Quellen, unbelegte Punkte, Hook-Kandidaten, Beschreibung, Rechnungen und 3D-Modell kommen aus dem alten, belegten Plan des Themas. Alte Pläne bleiben unverändert.
- `tools\bauaufgabe_batch2.sh <log> "thema|sprache|Kurztitel[|Fassung]" …`: Render über die Warteschlange, `overlap_check`, Export nur bei bestandenem Prüfbericht und leerem Überschneidungsbefund. Läuft ohne Claude.

## 8. Offene Punkte

- **Pilot:** `05 Produktion6-11-11 Pilot Taipei 101 Export6-11-11 Pilot Taipei 101 – 9x16.mp4`, 78,1 s, VALIDATED, `overlap_check` ohne Befund, Warnung `visual_cuts_rhythm` (Median 1,0 s, wie beim Fehmarnbelt-Testvideo). Kontaktbogen in `03 Schnittprojekt`. Gemini-Kosten 0,042 USD (davon 0,023 USD für die verworfene 91-s-Fassung).
- Woche 1 im neuen Format: 21 Themen DE und EN in Produktion (Stand siehe Redaktionsplan). Die alten Stimmen passen nicht, weil sich der Sprechtext ändert; je Video eine neue Gemini-Stimme (rund 0,02 USD).
- EN-Pilot: `05 Produktion6-11-11 Pilot Taipei 101 EN`, 85,5 s, VALIDATED, ohne Überschneidungen.
- 3D-Bild bei Tunnel- und Streckenthemen (Brenner, Gotthard, Danyang–Kunshan) noch schwach: dünne Linien in viel Fläche. Eigene Grundkörper (Tunnelquerschnitt, Pfeilerreihe in Nahsicht) würden helfen.
- Weitere Lösungsbauteile als 3D-Grundkörper (Schleusenkammer mit Sparbecken, Pendelschaft Skytree, Tübbingring, Senkkasten).
- Urteilsstempel `BELEGT / TEILWEISE / NICHT BELEGT` in `gb_proof` für die Reihe „Prüfstand“.
- Musiklizenz weiterhin offen (keine Musik).
