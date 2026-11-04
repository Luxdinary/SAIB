# Dewlane – Format-Bibel „Nahaufnahme“

Stand 02.11.2026, Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026 (mit dem Piloten „Testmenge“).** Nicht freigegeben: Kalender-Anpassung (Abschnitt 9) und KI-Bilder-Paket (Abschnitt 7). Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md`, Abschnitt 5 (Stefans Entscheidung vom 02.11.2026: Dewlane wird animiert bzw. mit KI erstellt, Produkte erfunden oder neutral, jede KI- und Animationsdarstellung gekennzeichnet, Wirkung nur mit Quelle, nichts wirkt wie ein echter Produkttest). Ersetzt für neue Videos die `Vorlage Dewlane.md` (Etikett als roter Faden, Statusleiste, Erklärschicht); die alte Vorlage bleibt als Nachweis liegen. Die frühere Regel „keine Produkte, keine Haut“ entfällt.

Umsetzung: `C:\Automation\faceless-network\brands\beauty\nahaufnahme\scenes.py` (Szenentypen `nh_*`, Hintergrund, Stempel), eingebunden am Ende von `brands\beauty\scenes.py`. Pilotplan `data\direction\beauty-20261117-3-de.P1.json`. Pläne ohne `layout.format: "nahaufnahme"` rendern unverändert im alten Format.

## 1. Versprechen an den Zuschauer

**„Du siehst ein Beauty-Produkt so nah, wie du es im Laden nie siehst: was die Zahl und die Wörter auf der Packung bedeuten, wie viel und wie man es aufträgt, und was eine Quelle über die Wirkung sagt. Ohne Marke, ohne Verkauf, ohne Wundertest.“**

- Ein Produkt, eine Frage. Jedes Video stellt einen neutralen Produkttyp auf die Bühne (Sonnencreme, Serum, Deo, Shampoo, Nagellack) und geht nah heran.
- Der Zuschauer sieht Menge, Textur und Anwendung, statt nur davon zu hören: sechs Löffel füllen sich, ein Film legt sich auf die Haut, ein Balken schrumpft.
- Wirkung kommt nur aus einer Quelle und wird als Schema gezeigt, nie als Ergebnis eines Tests.
- Am Ende steht ein Merksatz und eine Frage, die der Zuschauer an seiner eigenen Packung prüfen kann.

Zielgruppe unverändert: Menschen, die Hautpflege und Kosmetik verstehen wollen, ohne dass man ihnen etwas verkauft (DE; EN-Fassung lokalisiert).

## 2. Bildsprache

| Element | Regel |
|---|---|
| Bühne | Helles Studio aus Code: Elfenbein-Rückwand, weicher Boden mit Horizont, ein Lichtkegel, der langsam wandert, Tautropfen-Unschärfen am Rand in drei Ebenen, feines Korn. Ersetzt Etikett-Hintergrund, Statusleiste und Erklärschicht. |
| Das Produkt | **Neutrales, erfundenes Produkt** als SVG: Tube, Tiegel, Pipettenflasche, Sprühflasche. Nur Kategorie und Kennzahl auf dem Etikett („SONNENSCHUTZ · LSF 30“), nie ein Markenname, nie das Dewlane-Logo auf dem Produkt (Dewlane verkauft nichts). Kennzahlen sind Beispielwerte. |
| Die Lupe | Wiederkehrendes Leitbild: ein runder Lupenausschnitt mit dunklem Rand zeigt erst die Angabe auf der Packung groß, dann den Querschnitt dazu (Film auf der Haut, Tropfen, Textur). |
| Haut | Nur als neutrale Illustration: Querschnittstreifen mit der Beschriftung „Haut · schematisch“, flaches Piktogramm (Körper, Unterarm mit Hand) mit „Illustration“. Keine Gesichter, keine fotorealistische Haut, kein Vorher-nachher. |
| Menge und Textur | Alltagsmaße statt Zahlenkolonnen: Teelöffel, Schnapsglas, Tropfen. Cremetupfer, Film, Strang aus Code, mit Glanzlicht. |
| Wirkung | Balkenschema mit der festen Zeile „Schema nach Quelle · keine Messung“ (gestricheltes Quadrat). Nie Prozentwerte, die wie ein Messergebnis aussehen, nie zwei Hautbilder nebeneinander. |
| Belege | Chips in der Szene: Quadrat Rosé = **Fakt** (Quelle mit Nummer und Stelle), gestricheltes Quadrat = **Schema**, Halbkreis Honig = **Unsicher**. |
| Kennzeichnung | Oben im ganzen Video der Stempel „Animation · neutrales Produkt · kein Produkttest“, unten „KI-generiert“ (Stimme). In `post.json` die KI-Kennzeichnung der Plattformen. |
| Schluss | Merksatz (≤ 40 Zeichen, Playfair), Frage an den Zuschauer zur eigenen Packung, Dewlane-Tropfen mit Wortzeichen, „Wissen statt Versprechen.“, „Keine medizinische Beratung.“ |

Nach der Prüfrunde vom 03.11.2026 (Note 2,7) gilt zusätzlich: Inhalte enden rechts bei x 930 (Spalte der Plattform-Symbole bleibt frei); Schrift mindestens 28 px, Beleg-Chips, Stempel und Hinweise in Mauve statt Grau; Piktogramme (Körper, Unterarm) mit Kontur in Rosé #9B5560 und kräftiger Blush-Füllung, mindestens 3 : 1 gegen Elfenbein; Schutzbalken der halben Menge startet leer; Merksatz ohne „nur“. Farben und Schriften aus `brand.yaml` (Elfenbein #F8F3EF, Mauve #4A2F34, Rosé #9B5560, Blush nur für Formen; Playfair Display und Inter). Inhalte zwischen y 290 und y 1100, Untertitel in Phrasen bis vier Wörter, 800 px breit, 540 px vom unteren Rand.

## 3. Dramaturgie (Ablauf in Sekunden, gemessen am Piloten)

| Zeit | Beat | Szenentyp | Inhalt |
|---|---|---|---|
| 0–10,6 | Hook: Das Produkt auf der Bühne | `nh_stage` | Neutrales Produkt fährt herein, die Menge oder Eigenschaft wird sichtbar (Löffel füllen sich, Zähler läuft), Quelle als Chip, die Angabe auf der Packung wird markiert, die Lupe kommt. |
| 10,6–22,8 | Unter der Lupe | `nh_lens` | „Was heißt …?“ Die Lupe zeigt die Angabe groß, dann den Querschnitt: was die Angabe physisch bedeutet. Ergebnis als große Zahl mit Unterzeile und grünem Haken „nur so: …“. |
| 22,8–44,3 | Menge und Textur | `nh_amount` | Die Menge auf einen ganzen Körper oder ein Gesicht übertragen: Piktogramm füllt sich, Gesamtmenge groß, Alltagsmaß, zweite Quelle als Karte, ein Befund. |
| 44,3–56,1 | Wirkung laut Quelle | `nh_effect` | Zwei Karten (richtig angewendet / typischer Fehler) mit Menge- und Schutzbalken als Schema; Strichlinie „im gleichen Maß“, dann der tatsächliche Wert aus der Quelle. |
| 56,1–67,7 | Im Alltag | `nh_apply` | Strang auf einem neutralen Unterarm, verteilt sich; drei Anwendungshinweise aus der Quelle mit Symbol. |
| 67,7–78,8 | Merksatz und Abschluss | `nh_close` | Merksatz, Frage zur eigenen Packung, Absender. |

Die Sekunden oben sind am Piloten gemessen (78,8 s, 1.265 Zeichen Sprechtext). Länge 65–90 s (Ziel 74–82 s), Sprechtempo Gemini Leda etwa 15,8 Zeichen/s, also 1.150–1.270 Zeichen Sprechtext. Längste Strecke ohne Bildereignis höchstens 13 s; jede Szene hat 4–7 wortgenaue Ereignisse (`"@Wort"`-Anker). Nicht jede Folge braucht alle sechs Beats: Bei „Direkter Vergleich“ ersetzt `nh_effect` mit zwei Produkten die Mengen-Szene.

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender |
|---|---|---|---|
| **Unter der Lupe** (Hauptreihe) | Eine Angabe auf einem neutralen Produkt: LSF, Sanduhr, offener Tiegel, „(nano)“, CI-Nummer, „Parfum“. Was steht da, was heißt es, wie viel, wie anwenden. | stage → lens → amount → effect → apply → close | Sonnenschutz-Wissen, Etikett entschlüsselt |
| **Direkter Vergleich** | Zwei neutrale Produkte oder zwei Aussagen nebeneinander: mineralischer und organischer UV-Filter, Deo und Antitranspirant, „hypoallergen“ und „allergiefrei“, Mythos und Quelle. Kein Sieger, sondern der Unterschied. | stage (zwei Produkte) → lens → effect (zwei Karten) → close | Mythos-Check, Werbeversprechen geprüft |
| **Beauty verständlich** | Ein Inhaltsstoff oder Begriff im Produkt: Retinol (Vitamin A) in der Creme, Salicylsäure im Peeling, Zinkpyrithion im Shampoo, TPO im Nagelgel. Wo er steckt, wofür, welche Grenze laut Quelle gilt. | stage → lens (Querschnitt, Molekül als Form) → effect (Grenzwert als Schema) → close | Regel-Check (Stoffthemen) |
| **Im Alltag angewendet** | Anwendung Schritt für Schritt als gekennzeichnete Veranschaulichung: Nachcremen, Wasserfestigkeit, Haltbarkeit nach dem Öffnen. Ausdrücklich **kein** „getestet“: Codex' Vorschlag „im Alltag getestet“ ist umbenannt, weil ein animierter Test nach Verordnung (EU) 655/2013 wie ein Beleg wirken könnte, den es nicht gibt. | stage → apply → amount → close | Sonnenschutz-Wissen, Etikett entschlüsselt |

## 5. Was Dewlane von den anderen acht Marken unterscheidet

| Marke | Format | Dewlane dagegen |
|---|---|---|
| Scutoria | Fall „Was tust du?“, dunkel, Uhr, A/B/C-Entscheidung | hell, kein Fall und keine Wahl; **ein Gegenstand** in der Nahaufnahme, Menge und Textur statt Zeitdruck. |
| Promptwerk | echte Terminal-Aufzeichnung | keine Aufzeichnung; ausdrücklich Animation, gekennzeichnet. |
| Zonkfruit | Anime-Serie mit Figur Plümo | keine Figur, keine Geschichte; das Produkt ist der Hauptdarsteller. |
| Gigastruct | 3D-Bauwerk, gerechnete Größenvergleiche | Größenvergleiche im Kleinen (Löffel, Tropfen, mg/cm²), am Körper statt an Bauwerken. |
| Revlore | bewegte Schnittmodelle von Motoren | Querschnitt durch eine Hautschicht statt durch Mechanik, ruhig statt technisch. |
| Suitwerk | Stoffe und Passform als Illustration | Kosmetik statt Kleidung; die Lupe und die Packungsangabe sind Dewlane-eigen. |
| Frontlore, Gritwerk | Geschichte, Motivation | Alltagsprodukt, das der Zuschauer im Bad stehen hat und sofort selbst prüfen kann. |

Erkennungsmerkmale, die keine andere Marke nutzt: das neutrale Produkt auf der Elfenbein-Bühne, die Lupe mit Querschnitt, Mengen in Alltagsmaßen, das Wirkungsschema mit „keine Messung“, der Stempel „Animation · neutrales Produkt · kein Produkttest“ und die Schlussfrage an die eigene Packung.

## 6. Prüf- und Rechtsregeln (vor jedem Render, zusätzlich zu den gemeinsamen Prüfungen)

Inhalt und Recht:
1. **Keine echten Marken.** Produkte sind erfunden und neutral: keine Markennamen, keine erkennbaren Verpackungen, keine Logos, auch nicht angedeutet. Kein Dewlane-Logo auf einem Produkt. Kennzahlen (z. B. LSF 30) sind als Beispielwert im Plan vermerkt.
2. **Kein Produkttest, kein Vorher-nachher.** Nichts darf wie ein durchgeführter Test, eine Messung oder ein Anwendungsergebnis aussehen: keine Hautbilder vorher/nachher, keine „Tag 1 / Tag 28“, keine Prozentwerte als Messergebnis, keine Kittel, Labore oder Probanden. Wirkungsdiagramme tragen „Schema nach Quelle · keine Messung“. Grund: Verordnung (EU) Nr. 655/2013 (gemeinsame Kriterien für Werbeaussagen bei kosmetischen Mitteln: Belegbarkeit, Wahrhaftigkeit, Redlichkeit).
3. **Wirkung nur mit Quelle.** Jede Aussage über Wirkung, Menge oder Anwendung steht in einer Quelle mit URL und Abrufdatum (Behörde, EU-Rechtstext, Fachgesellschaft). Die Quelle wird im Original gelesen; die Stelle steht im Chip („Erwägungsgrund 14“, „Nr. 7“). Was nicht belegt ist, steht in `unverified` und wird nicht gesagt.
4. **Keine eigene Empfehlung.** Dewlane gibt keine eigene Dosis, Häufigkeit oder Produktwahl vor, sondern sagt, was die Quelle nennt („laut EU-Empfehlung“, „die AAD nennt“). Keine Kaufempfehlung, keine Markennennung als Empfehlung.
5. **Kennzeichnung.** Stempel „Animation · neutrales Produkt · kein Produkttest“ im ganzen Video, „KI-generiert“ unten, KI-Kennzeichnung in `post.json` (TikTok `is_aigc`, Instagram `is_ai_generated`, YouTube `containsSyntheticMedia`), Art. 50 KI-Verordnung. KI-Bilder (falls freigegeben, siehe 7) zusätzlich mit „KI-Bild“ in der Ecke.
6. **Haut nur als Illustration.** Schematisch, flach, beschriftet. Keine Gesichter, keine KI-Haut, keine Hauttypen-Zuordnung von Personen.
7. **Keine medizinische Beratung, keine Heilversprechen.** Bei Hautproblemen der Verweis auf Ärztin oder Arzt nur, wenn die Quelle ihn nennt. Schluss immer mit „Keine medizinische Beratung.“
8. Anrede „du“, ruhig, warm, ohne Verkaufston; „kann“ bleibt „kann“, wenn die Quelle „kann“ sagt.

Technik (gemeinsam, unverändert): Gemini-Stimme (DE Leda, EN Aoede; nie SAPI/Edge), 65–90 s, `story.validate` und Trockenlauf ohne Fehler, Textgrenzen der `nh_*`-Typen (`LIMITS` in `nahaufnahme\scenes.py`), `node scripts\overlap_check.mjs` ohne Befund, Prüfbericht mit `risk_level` high (Marke) → HUMAN_REVIEW, Freigabe durch Stefan.

## 7. Bedarf an KI-Bildern (Vorschlag, nichts erzeugt, keine Credits ausgegeben)

Der Pilot ist vollständig aus Code (HTML/SVG/CSS). Das trägt für Mengen, Schemata, Lupe und Etikett. Schwächer ist es bei dem, was Beauty-Zuschauer am stärksten anzieht: glaubwürdige **Texturen** (Creme, Gel, Serumtropfen, Schaum) und ein hochwertiges **Produktfoto**. Hier würden KI-Clips das Format deutlich verbessern:

| Bedarf | Modell (Preise laut Prüfung vom 30.10.2026, vor Buchung mit `get_cost` neu prüfen) | Menge | Credits |
|---|---|---|---|
| Textur-Schleifen als Hintergrund der Lupe und der Mengen-Szene: Cremeschliere, Gel, Serumtropfen, Schaum, Sonnenschutz-Film, Puderwolke; neutral, ohne Verpackung, ohne Haut | Startbild Nano Banana Pro 2k (2 Credits) + Kling 3.0 Omni Frames pro 8 s Schleife (10 Credits) | 6 Clips | 6 × 12 = **72** |
| Neutrale Produktfotos als Vorlage für die Bühne (Tube, Tiegel, Pipette, Sprühflasche, ohne Schrift) | Nano Banana Pro 2k | 8 Bilder | 8 × 2 = **16** |
| Summe einmaliges Paket, in allen Folgen wiederverwendbar | | | **≈ 88 Credits** |

Laufende Kosten entstehen nur, wenn eine Folge ein eigenes Motiv braucht (etwa 2–12 Credits je Thema). Hinweis: Von den 182 vorhandenen Higgsfield-Credits sind 156 für Zonkfruit Stufe 0 freigegeben; das Dewlane-Paket bräuchte also neue Credits. Regeln für diese Clips: keine Gesichter, keine Haut, keine Marken, keine „Anwendung am Menschen“; im Bild „KI-Bild“, Lizenzzeile in `brands\beauty\assets\higgsfield\LICENSE.md`. Prompts, Dateinamen und Abnahme: `Bibliothek Prompt-Blatt.md` (für die Sitzung „Bibliotheken“; im Ausgabeplan Higgsfield Ultra sind für Dewlane 120 Credits vorgesehen, Freigabe offen). Codex' Briefing vom 30.10. liegt in `02 Marke\_Higgsfield-Briefings (Codex, 2026-10-30)\08-Dewlane.md`.

## 8. Pilot

- Thema: „Wie viel Sonnenschutz: die Testmenge“ (Kalender `beauty-20261117-3`, Reihe Unter der Lupe).
- Quellen, am 02.11.2026 im Original gelesen: Empfehlung der Kommission 2006/647/EG, Erwägungsgrund 14 (2 mg/cm², sechs Teelöffel, etwa 36 g, mehr als Verbraucher normalerweise auftragen, halbe Menge kann die Schutzwirkung um zwei Drittel verringern) und Nr. 7 (vor dem Sonnenaufenthalt auftragen, mehrfach auftragen, besonders bei Schwitzen oder nach Schwimmen und Abtrocknen); American Academy of Dermatology, „How to apply sunscreen“ (mindestens etwa eine Unze, ein Schnapsglas voll, für unbedeckte Haut der meisten Erwachsenen).
- Export: `05 Produktion\Dewlane\2026-11\2026-11-17 Pilot Testmenge\`.
- Ergebnis: 78,8 s, Gemini Leda 0,019 USD, Prüfbericht bestanden mit HUMAN_REVIEW (nur `risk_high_review`, Marke Risiko hoch), `overlap_check` ohne Befund, 46 Bildereignisse (Median 1,4 s), −15,7 LUFS.

## 9. Kalender 09.11.–06.12.2026: was zur neuen Richtung passt (Vorschlag, Kalender nicht geändert)

Geprüft wurden die 84 deutschen Themen von `data\calendars\beauty_2026-11.json` (die englischen sind Spiegelthemen). Maßstab: Lässt sich ein neutrales Produkt, eine Menge, Textur oder Anwendung zeigen?

| Kalender-Reihe | Themen | passt gut | passt mit Umbau | passt schlecht | neue Reihe |
|---|---|---|---|---|---|
| Sonnenschutz-Wissen | 12 | 12 | 0 | 0 | Unter der Lupe, Im Alltag angewendet |
| Mythos-Check | 16 | 12 | 2 | 2 | Direkter Vergleich |
| Etikett entschlüsselt | 16 | 10 | 2 | 4 | Unter der Lupe |
| Werbeversprechen geprüft | 12 | 4 | 6 | 2 | Direkter Vergleich |
| Regel-Check | 28 | 6 | 10 | 12 | Beauty verständlich |
| **Summe** | **84** | **44** | **20** | **20** | |

Einzeln:
- **Passt gut (44):** alle Sonnenschutz-Themen; Mythen mit Produkt (Parabene, Aluminium im Deo, mineralischer Sonnenschutz und Nano, Haarfarbe für Wimpern, Mikroplastik, Seife, Winter-UV, LSF 50, LSF im Make-up, Fruchtsäure in der Sonne, Deo und Arzneimittel, Sonnencreme vom letzten Sommer); Etikett (INCI-Liste, offener Tiegel, Sanduhr, „(nano)“, CI-Nummern, „Parfum“, Duftstoff-Allergene, Warnhinweise Salicylsäure, 0,001/0,01 %, „+/-“ bei Make-up); Werbeaussagen „Mit Inhaltsstoff X“, „Hypoallergen“, „Dermatologisch getestet“ (als Vergleich: was der Satz belegt und was nicht), „Frei von …“; Stoffthemen mit klarem Produkt (TPO im Nagelgel, Zinkpyrithion im Schuppenshampoo, Vitamin A, Arbutin, Kojisäure, Salicylsäure).
- **Passt mit Umbau (20):** Themen, die heute eine Regel erklären, aber ein Produkt haben könnten: Was ist Kosmetik (Produktreihe auf der Bühne), Lilial, Triclosan, MIT, Haarfarben, BHT, Methylsalicylat, Profi-Produkte, Nano-Gold/Silber/Kupfer, Talk; Sieben Pflichtangaben und kleine Tuben (als Etikett unter der Lupe); Allergen-Hinweis, „Nano ist nicht geregelt“; „Gesetzliche Pflicht ist kein Vorteil“, „Ohne Tierversuche“, „Bio“, „Natürlichen Ursprungs“, „Heilversprechen“, „Vegan und clean“ (als Vergleich Aussage gegen Bedeutung).
- **Passt schlecht (20):** reine Verfahrens- und Behördenthemen ohne sichtbares Produkt: verantwortliche Person, Produktinformationsdatei, ISO 22716, CPNP, Meldung ernster Wirkungen, Anhang II, CMR-Stoffe, Positivlisten, INCI-Glossar, SCCS, CosIng, MoCRA, „Kosmetik prüft niemand“, Tierversuche in der EU, „Behördlich zugelassen“, „Sechs Regeln für Werbeaussagen“, Chargennummer und Anschrift, Geschäftsgeheimnis EU/USA, Verunreinigungen, Sprache auf dem Etikett.

Vorschläge für die Anpassung (Stefans Entscheidung):
1. **Reihen umbenennen** wie in der Tabelle; die Kalenderzeilen behalten Thema und Quellen, `notes` bekommt die neue Reihe.
2. **Die 20 schwachen Themen bündeln** zu etwa vier Folgen „Beauty verständlich: Der Weg einer Creme in den Handel“ (verantwortliche Person, Produktinformationsdatei, CPNP, Meldung, Behörde) und „Wer prüft Kosmetik?“ (SCCS, Anhang II und Positivlisten, CMR, Tierversuche). Das neutrale Produkt wandert dabei als Faden durch die Stationen.
3. **Die frei werdenden etwa 15 Plätze mit Anwendungs- und Texturthemen füllen**, die der neuen Richtung entsprechen, zum Beispiel Serum und Creme (Reihenfolge), chemisches und mechanisches Peeling, Mizellenwasser, Retinol und Sonnenschutz, Deo und Antitranspirant als Vergleich, Haltbarkeit nach dem Öffnen im Alltag, Lippenpflege mit LSF. Für diese Themen gibt es noch keine geprüften Quellen; sie brauchen eine Recherche vor der Aufnahme in den Kalender.
4. **Taktung:** täglich eine Folge „Unter der Lupe“ oder „Im Alltag“, eine „Beauty verständlich“ und eine „Direkter Vergleich“, damit nicht drei Sonnenschutz- oder drei Regelthemen am selben Tag laufen.
5. **Woche 1 (09.–15.11.)**: Die 41 vorhandenen Pläne und die bezahlten Stimmen bleiben als Vorrat. Der Sprechtext der guten Themen kann bleiben, wenn die Szenen neu gebaut werden; für schwache Themen lohnt eine neue Vertonung erst nach der Bündelung.

## 10. Offene Punkte für Stefans Freigabe

- ~~Format und Pilot freigeben~~: erledigt, Stefan 02.11.2026.
- Reihen und Kalender-Anpassung nach Abschnitt 9: bündeln und ersetzen, ja oder nein.
- KI-Bilder-Paket nach Abschnitt 7 (≈ 88 Credits, neue Credits nötig) oder vorerst nur Code-Grafik.
- EN-Fassung des Piloten (gleiche Szenen, Stempel und Wortlisten sind zweisprachig angelegt).
- Für „Direkter Vergleich“ und „Beauty verständlich“ fehlen noch Varianten: `nh_stage` mit zwei Produkten, weitere Produktformen (Tiegel, Pipette, Sprühflasche) und ein Querschnitt-Motiv für Inhaltsstoffe.

## 11. Woche 1 (09.–15.11.2026) im Format „Nahaufnahme“

Auftrag der Hauptsitzung vom 02.11.2026 (Stefan: „Alle Videos freigegeben“): Woche 1 im neuen Format, DE und EN, nur aus Code.

- **Verfahren:** `C:\Automation\faceless-network\brands\beauty\nahaufnahme\convert_w1.py` baut aus den vorhandenen Woche-1-Plänen neue Pläne `data\direction\beauty-<Thema>-<de|en>.N1.json`. Sprechtext, Quellen, Hook-Kandidaten und Beschreibung bleiben unverändert (am 01.11. geprüft); neu sind die Szenen. Die alten Pläne bleiben unberührt.
- **Allgemeine Szenentypen** für Reihen-Themen (in `nahaufnahme\scenes.py`): `nh_hook` (Produkt auf der Bühne, Frage, Ring und Lupe), `nh_facts` (Produkt und Lupe mit dem Stichwort, belegte Zeilen), `nh_list` (Namen lösen sich vom Produkt), `nh_versus` (zwei neutrale Produkte nebeneinander), `nh_time` (Fristen auf einer Schiene), `nh_steps` (So liest du es), dazu `nh_close`. Weitere neutrale Produktformen: Tiegel, Pumpflasche, Pipettenflasche, Sprühdose. Wo eine Szene länger als 5 s still stünde, kippt das Produkt kurz (ruhiges Bildereignis).
- **Produziert werden 13 Themen × 2 Sprachen = 26 Videos:** INCI-Liste, Was ist Kosmetik, Parabene, LSF-Kategorien, Sieben Pflichtangaben, Aluminium im Deo, „Mit Inhaltsstoff X“, UVA-Schutz, Tiegel-Symbol, Pflicht ist kein Vorteil, Sunblock und 100 %, Sanduhr, Mineralisch und Nano. Export je Video nach `05 Produktion\<Datum> <Kurztitel>[ EN]`.
- **Bezahlte Stimmen wiederverwendet**, wo der Sprechtext gleich ist: INCI-Liste DE und EN, Was ist Kosmetik DE. Alle anderen bekommen eine neue Gemini-Stimme (je etwa 0,02 USD).
- **Nicht produziert, offen für Stefan (passen schlecht, Abschnitt 9):** 10.11. Sechs Regeln für Werbeaussagen, 10.11. Die verantwortliche Person, 11.11. Produktinformationsdatei, 12.11. ISO 22716, 13.11. CPNP, 13.11. „Kosmetik prüft niemand“, 14.11. Ernste unerwünschte Wirkungen, 15.11. Anhang II. Vorschlag dazu in Abschnitt 9 (bündeln oder ersetzen).
- Das alte Woche-1-Video „INCI-Liste EN“ (altes Format) liegt in `Documents\_zum_loeschen\2026-11-02 Dewlane Nahaufnahme`.
