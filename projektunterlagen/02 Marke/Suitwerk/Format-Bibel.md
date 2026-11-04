# Suitwerk – Format-Bibel „Kreidestrich“

Stand: 02.11.2026 (Wien), Fassung 1.0. **Gültig: freigegeben von Stefan, 02.11.2026, mit dem Piloten „Köper oder Leinwand“** (Weitergabe der Hauptsitzung: „Freigeben“). Folgeauftrag: englischer Pilot, Woche 1 (09.–15.11.) nur mit Stoffkunde-Themen; Passform-Themen erst mit besseren Quellen als Händlerratgebern. Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke bekommt ein eigenes Format; gemeinsam bleiben nur Technik und Prüfungen) und die Bewertung im `Statusbericht neun Marken 2026-11-02.md` (Suitwerk „lebt von Anschauung“; ohne echte Aufnahmen über präzise Illustration). Ersetzt für neue Videos die `Vorlage Suitwerk.md` (0.9 mit Qualitätsrunde Q1: Atelier-Hintergrund, Sakko-Strichzeichnung als Leitobjekt, Erklärschicht, Statusleiste, Karten). Die Vorlage bleibt als Nachweis liegen.

Umsetzung: `C:\Automation\faceless-network\brands\menswear\kreidestrich\scenes.py` (Szenentypen `kw_*`), eingebunden am Ende von `brands\menswear\scenes.py`. Pilotplan: `data\direction\menswear-20261202-3-de.P1.json`.

## 1. Versprechen

**„Wir legen es auf den Zuschneidetisch und zeichnen nach, was Worte nicht zeigen: Faden, Schnitt, Maß. Richtig und falsch nebeneinander, mit Kreide markiert.“**

Herrenstil wird meist behauptet („so trägt man das“). Suitwerk zeigt stattdessen, woraus die Regel folgt. Ein Stoff wird Faden für Faden gewebt, bis man sieht, warum ein Köper eine schräge Linie hat. Eine Passform wird am Kleidungsstück mit Kreide angezeichnet, wie bei einer Anprobe. Ein Maß wird mit Maßband und Bemaßungslinie gezeigt und nur genannt, wenn eine Quelle es nennt. Am Ende steht ein Test, den der Zuschauer an seiner eigenen Kleidung machen kann.

Ein Satz für die Kanalbeschreibung: *„Herrenstil im Detail: Stoff, Schnitt und Maß, gezeichnet statt behauptet.“*

Zielgruppe unverändert: Männer, die sich gut anziehen wollen, ohne Trends zu folgen; DACH und international. Ton: ruhig, kundig, nie herablassend.

## 2. Bildsprache

| Element | Regel |
|---|---|
| Grund (Erkennungszeichen) | **Dunkles Kammgarntuch auf dem Zuschneidetisch, von oben gesehen.** Der Hintergrund ist selbst ein feiner Köper (schräge Rippen), mit Körnung, einer langsam wandernden Tischlampe und Randabdunklung. Kein Atelier, keine Schnittmusterbögen, kein Push-in mehr. |
| Kreide | **Jede Markierung ist Schneiderkreide**: Striche, Pfeile, Ungleich-Zeichen, Unterstreichungen und kurze Beschriftungen in Kreideweiß mit rauer Kante (SVG-Filter `kw-chalk`). Rote Kreide nur für „falsch“, grüne nur für „richtig“, nie als Dekoration. |
| Band oben | Reihenname in Kreide („Unter dem Fadenzähler · Bindung“) über einem **Maßband**. Das Maßband ist Kennzeichen, kein Messwert. |
| Fadenzähler | Die Nahaufnahme im Stoff kommt immer durch einen **Fadenzähler** (Leinenprüfer): Metallrahmen mit Skalenstrichen, darin die Vergrößerung. Er fährt auf das Stoffmuster, so ist klar, dass es eine Vergrößerung ist. |
| Gewebe | **Faden für Faden aus der Bindung gerechnet** (`warp_up`): Kette senkrecht, Schuss waagerecht, an jeder Kreuzung liegt einer oben. Der Schuss wird Reihe für Reihe eingezogen, ein Kreidepfeil zeigt die Richtung. In der Vergrößerung sind Kette blau und Schuss hell, mit dem Hinweis „Farben nur zur Unterscheidung“. Stoffmuster in Originalgröße sind marineblau mit Zickzackkante (Zackenschere). |
| Karopapier | Die Bindung als Kästchen auf cremefarbenem Papier mit rotbraunem Raster, aus derselben Funktion wie das Gewebe. Legende im Bild („dunkel = Kettfaden oben“). |
| Richtig und falsch | Immer **nebeneinander** oder **nacheinander am selben Stück** (Stoff umdrehen, Knopf schließen, Länge ändern). Das Urteil steht in Kreide unter dem Stück, nicht auf einer Karte. |
| Kleidungsstücke (Reihen Anprobe, Nachgemessen) | Technische Zeichnung im Stil einer Schnittzeichnung auf der Schneiderbüste oder flach liegend, mit Bemaßungslinien. Grundlage: die vorhandenen Zeichenbaukästen `tools\garment.py` und `tools\objects.py`, neu eingefärbt (Tuch statt Goldlinie). |
| Farben | Palette aus `brand.yaml`: Tuch Marine (`#141E33`–`#22314F`), Text Elfenbein (`#F2EEE6`), Kreide (`#EEE7D7`), Maßband Creme (`#E8DCBC`), Gold (`#D4B483`) nur in Untertiteln und Logo. |
| Schrift | Playfair Display 600 (Titel, Merksatz), Inter (Kreidebeschriftung, Quellenzeile, Untertitel). |
| Quelle | Eigene Zeile über den Untertiteln (tiefe Bühne: y 1170, bis zu zwei Zeilen, 24 px): „Quelle Woolmark: Introduction to Wovenwear, S. 9 · Abruf 02.11.2026“. In den Plattformtexten steht das kurze `label` der Quelle. Nie ein Händlername im Bild. |
| Entfällt | Erklärschicht (Kicker, Stimmen-Tag, Marker-Kapseln, Kreisübergang), Statusleiste, Atelier-Ebene, goldene Sakko-Linie als Leitobjekt in jeder Szene, Karten mit Mini-Sakko. „KI-generiert“ bleibt unten (gemeinsame Regel). |

Senkrechte Aufteilung (1080 × 1920), seit 02.11.2026 mit tiefer Bühne nach Prüfrunde R5 (`layout.zone_h: 950`, `layout.zone_lower_right_px: 940`): Logo 120–160 · Reihenname 190 · Maßband 232–278 · Bühne 290–1160 · Quelle 1170–1228 · Untertitel bis 1360 · Fortschritt und „KI-generiert“ nach den gemeinsamen Regeln (R1). Bühne zwischen x 108 und 930; rechts ab x 930 bleibt frei. Mindestschrift 24 px für alles außer Untertiteln (R7, `small_text` im `overlap_check`). Fadenzähler 540 px, Stoffmuster bis 540 px hoch; der Klappfuß des Fadenzählers sitzt links, damit unter dem Rahmen Platz für den Farbhinweis bleibt.

## 3. Dramaturgie (Reihe „Unter dem Fadenzähler“, gemessen am Piloten, 83,1 s; erlaubt 65–90 s)

| Sekunde | Beat | Szenentyp | Inhalt |
|---|---|---|---|
| 0–9,6 | Zwei Stücke, die gleich aussehen (Hook) | `kw_hook` | Frage groß im Bild, ein Kreidestrich darunter (Kennzeichen jedes Anfangs), zwei Stoffmuster fallen auf den Tisch, Kreide setzt „≠“, der Fadenzähler fährt auf das erste Muster und dann auf das zweite. |
| 9,6–26,3 | Das erste Stück, gebaut | `kw_weave` | Kette und Schuss werden benannt (Kreidepfeile), der Schuss läuft Reihe für Reihe durch. Die Regel steht als Formel in Kreide („1 über · 1 unter“). |
| 26,3–41,4 | Das zweite Stück, gebaut | `kw_weave` | Gleiche Ansicht, andere Bindung („2 über · 2 unter“). Ein Kreidepfeil zeigt den Versatz um einen Faden, dann zieht die Kreide den Grat nach. |
| 41,4–53,3 | Auf Papier | `kw_draft` | Beide Bindungen auf Karopapier, Zeile für Zeile, Schachbrett gegen Treppe. |
| 53,3–65,0 | Der Vergleich am Stück | `kw_flip` | Beide Muster werden umgedreht und wieder zurück; Kreide schreibt das Urteil darunter; ein Kreidepfeil zeigt die Richtung des Grats. |
| 65,0–83,1 | Der Test für zuhause, Abschluss | `kw_close` | Beide Muster mit Urteil, Quellenkapsel, Licht streicht schräg darüber, Merksatz mit Kreide unterstrichen, Markenzeile. |

Regeln für Sprechtext und Bild:
- Gemini Orus spricht diesen ruhigen Sachtext mit etwa 2,3 Wörtern/s: Pilot 185 Wörter = 80,3 s Stimme, 83,1 s Video. Für 70–78 s also 155–175 Wörter. Der Mock-Trockenlauf unterschätzt die Länge deutlich (66 s statt 83 s).
- Jede Szene hat mindestens drei Bildereignisse an gesprochenen Wörtern (`"w:Wort[#n][+0.4]"`). Der Faden läuft, während die Stimme „einmal drüber, einmal drunter“ sagt.
- Die Stimme lenkt den Blick („Dreh beide Stoffe um“), das Bild liefert die Zahl oder Form.
- Anrede „du“, sachlich, kein Ausrufezeichen. Kein „besser“ ohne Quelle. Schluss: „Folge Suitwerk für Herrenstil mit Blick fürs Detail.“
- Hook immer als Vorführung: zwei Stücke, die gleich wirken und es nicht sind, oder ein Stück, an dem etwas nicht stimmt.

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender `menswear_2026-11.json` |
|---|---|---|---|
| **Unter dem Fadenzähler** (Pilot) | Woraus ein Stoff gebaut ist: Bindung (Leinwand, Köper, Fischgrat, Hahnentritt, Glencheck), Garn (Kammgarn, Streichgarn), Faser (Mohair, Kaschmir, Leinen), Gewicht und Zahlen auf dem Etikett. | hook → weave (ein oder zwei) → draft → flip oder Vergleich → close | Stoffkunde (16) |
| **Anprobe** | Ein Kleidungsstück auf der Schneiderbüste mit einem Passformfehler. Kreide zeichnet das Prüfzeichen an (Zugfalte, überhängende Schulternaht, abstehender Kragen), daneben dasselbe Stück richtig. Am Ende der Selbsttest vor dem Spiegel. Bewertet wird immer das Kleidungsstück, nie der Körper. | hook (Fehler) → Prüfzeichen anzeichnen → richtig daneben → was ein Schneider ändern kann → close | Passform-Check (16) |
| **Nachgemessen** | Proportion und Detail mit Bemaßung: Reversbreite zu Krawattenbreite, Sakkolänge, Manschette unter dem Ärmel, Hosenbruch, Knopfstand. Eine Größe ändert sich stufenlos, Kreide markiert die Stelle, die die Quelle nennt. | hook → Bemaßung → Schieber (falsch, richtig, falsch) → Ausnahme in Bernstein → close | Das Detail verrät (20) |
| **Die Kleiderordnung** | Ein Anlass als Zuschnittliste: Die Teile eines Dresscodes liegen flach auf dem Tisch (Black Tie, White Tie, Lounge Suit, Trauerfeier). Kreide hakt ab, was die Quelle verlangt, und streicht, was nicht dazugehört; Konvention und Ausnahme sind getrennt markiert. | hook (ein Teil zu viel) → Teile legen → abhaken und streichen → Ausnahme → close | Anlass und Zubehör (16), Regel und Ausnahme (16) |

Gebaut sind bisher nur die Szenen der Reihe „Unter dem Fadenzähler“ (seit 02.11.2026 auch Waage, Skala, Faserquerschnitt, Weg zum Garn und Ausrüstung). Für die anderen drei fehlen Code-Bausteine (Abschnitt 8). Bis sie gebaut sind, werden diese Themen zurückgestellt und nicht im alten Format weiterproduziert (Stefan, 02.11.2026: Passform-Themen erst mit besseren Quellen als Händlerratgebern).

## 5. Abgrenzung zu den anderen acht Marken

| Marke | Kern ihres Formats | Was Suitwerk anders macht |
|---|---|---|
| Scutoria | „Was tust du?“: Fall aus einem Betrieb, Entscheidung A/B/C, Uhrzeit, Papierkarte | Keine Geschichte, keine Entscheidung des Zuschauers. Gegenstand statt Situation; Kreide auf Tuch statt Karten. |
| Promptwerk | „Echtlauf“: echtes, aufgezeichnetes Terminal | Nichts ist aufgezeichnet; alles ist gezeichnet und aus einer Regel gerechnet. Bild ist Gegenstand, kein Text. |
| Tintora (vormals Zonkfruit) | Anime-Kinderserie mit Figuren, KI-Video | Keine Figur, keine Handlung, keine KI-Bilder. |
| Dewlane | „Nahaufnahme“: neutrales Produkt im hellen Studio, Lupe, Menge und Anwendung | Dunkles Tuch statt Elfenbein-Studio; Fadenzähler mit Skala statt runder Lupe; Struktur und Schnitt statt Menge und Wirkung; kein Produkt im Sinn einer Ware. |
| Revlore | „Zeitlupe“: Graphit-Messraum, Kinematik, Millisekunden | Kein Tempo, keine Zeitachse; Ruhe und Material. Kreide statt Messschrieb. |
| Gigastruct | „Bauaufgabe“: Bauwerk als 3D-Modell, Größenvergleich, Rechnung | Maßstab Körper und Faden statt Kilometer; flache Draufsicht auf den Tisch statt Kamera im Raum. |
| Frontlore | historische Technik mit Karten und Archivquellen | Gegenwartsbekleidung; Geschichte nur als Herkunft eines Stoffs oder Dresscodes, mit Museumsquelle. |
| Gritwerk | Motivation, künftig dokumentierte Selbstversuche | Kein Mensch, kein Gefühl; der Test am Ende ist ein Prüfgriff am eigenen Kleidungsstück. |

Merkmale, die nur Suitwerk hat: Tuch als Grund, Schneiderkreide als einzige Markierung, Maßband-Band, Fadenzähler, Gewebe Faden für Faden, Karopapier, Urteil in Kreide unter dem Stück, Test für zuhause am Schluss.

## 6. Prüfregeln (zusätzlich zu den gemeinsamen Prüfungen)

1. **Gewebe gerechnet, nicht gemalt.** Jede Stoffdarstellung kommt aus `warp_up(kind, i, j)` in `kreidestrich\scenes.py`; Vergrößerung, Stoffmuster und Karopapier nutzen dieselbe Funktion. Neue Bindungen (Fischgrat, Hahnentritt, Panama) erst mit eigener, belegter Bindungsregel einbauen.
2. **Vergrößerung gekennzeichnet.** Im Fadenzähler nie eine Fadenzahl oder ein Maßstab ohne Quelle. Zusatzfarben in der Vergrößerung tragen „Farben nur zur Unterscheidung“.
3. **Keine Zahl ohne Quelle.** Maße (Zentimeter, Gramm, Super-Zahlen, Fadendichten) nur mit Quelle im Bild. Das Maßband im Band ist Kennzeichen; Bemaßungslinien in „Nachgemessen“ tragen die Quelle.
4. **Regel heißt Konvention.** Stilregeln sind Konventionen; die Stimme sagt „üblich“, „laut …“, „meist“. Wo Quellen sich widersprechen, Bernstein-Kreide und beide Sichten. „Richtig“ und „falsch“ (grüne und rote Kreide) nur, wenn eine Quelle es so sagt.
5. **Kleidungsstück, nie Körper.** Passform wird am Stück beurteilt („das Sakko ist zu eng geschnitten“), nie an Figur, Größe oder Gewicht.
6. **Keine Marken, keine Händler, keine Kaufempfehlung.** Im Bild und im Sprechtext keine Firmen- oder Händlernamen, keine Produkte zum Kaufen. Ausnahme: geschützte Herkunfts- und Prüfzeichen als Sachinformation (zum Beispiel Harris Tweed), wenn das Thema genau das ist.
7. **Quellenrangfolge.** Zuerst Normen (ISO, DIN EN), Ausbildungsordnung und Fachliteratur des Schneiderhandwerks, Verbände (Woolmark), Museen (V&A), Etikette-Instanzen (Debrett's). Händlerratgeber nur, wenn es nichts anderes gibt, nie im Bild genannt und nur für weiche Aussagen. URL und Abrufdatum in `plan.sources`; Abruf höchstens 30 Tage vor dem Export. Unbelegtes steht in `unverified` und wird nicht gesagt.
8. **Darstellung ehrlich benennen.** Was eine Eigendarstellung ist (Legende im Karopapier, Testgriff), sagt die Stimme mit „hier“ oder „probier“, nicht als Norm.

Gemeinsam mit allen Marken, unverändert: Gemini-Stimme, Untertitel, Export, `node scripts\overlap_check.mjs` ohne Befund, KI-Kennzeichnung.

### Quellen für Regeln und Maße (Grundbestand)

| Quelle | Wofür | URL | Abgerufen | Stand der Prüfung |
|---|---|---|---|---|
| The Woolmark Company: *Introduction to Wovenwear*, Training Manual | Grundbindungen (S. 9), Gewebe je Kleidungsstück (S. 10), Garnarten | https://www.woolmark.com/globalassets/_06-new-woolmark/_industry/certification/_old-certification/_licensee-portal/learn-about-wool/training-manuals/intro-to-wovenwear.pdf | 02.11.2026 | Volltext gelesen (PDF), Grundlage des Piloten |
| ISO 3572:1976 *Textiles – Weaves – Definitions of general terms and basic weaves* | Begriffe der Bindungslehre, drei Grundbindungen | https://www.iso.org/standard/8977.html · Katalog DIN Media: https://www.dinmedia.de/en/standard/iso-3572/604135 | 02.11.2026 | Titel, Ausgabe 1976-02 und Status „current“ über DIN Media bestätigt; Volltext kostenpflichtig, nicht gelesen |
| ISO 8559-1:2017 *Size designation of clothes – Part 1: Anthropometric definitions for body measurement* | Wie Körpermaße definiert und gemessen werden (Reihe Anprobe, Nachgemessen) | https://www.iso.org/standard/61686.html | 02.11.2026 | Titel und Status über Suche bestätigt (iso.org sperrt automatische Abrufe); Volltext nicht gelesen |
| Verordnung über die Berufsausbildung zum Maßschneider/zur Maßschneiderin (MSchnAusbV 2004) | Was zum Schneiderhandwerk gehört (Maßnehmen, Anprobe, Änderung) | https://www.gesetze-im-internet.de/mschnausbv_2004/index.html | 02.11.2026 | Seite erreichbar; Inhalt vor erster Verwendung lesen |
| Eberle u. a.: *Fachmathematik Bekleidung*, 8. Auflage, Verlag Europa-Lehrmittel (Europa-Nr. 61912), Leseprobe | Maßberechnung, Schnittkonstruktion (Fachliteratur der Bekleidungsberufe) | https://www.europa-lehrmittel.de/leseprobe/61912-8.pdf | 02.11.2026 | Titelei gelesen; Fachinhalt nur aus dem Buch |
| Eberle u. a.: *Prüfungsbuch Bekleidung*, 6. Auflage, Verlag Europa-Lehrmittel (Europa-Nr. 61955), Leseprobe; Grundlage ist *Fachwissen Bekleidung* (Europa-Nr. 62013) | Fachbegriffe Stoff, Verarbeitung, Passform | https://www.europa-lehrmittel.de/leseprobe/61955-6.pdf | 02.11.2026 | Titelei gelesen; Fachinhalt nur aus dem Buch |
| Victoria and Albert Museum, Collections | Herkunft und Geschichte von Stoffen und Anzügen (Beispiel Fischgrat O350881) | https://collections.vam.ac.uk/item/O350881 | 01.11.2026 (Kalenderrecherche) | aus der Kalenderrecherche übernommen, vor Verwendung neu abrufen |
| Debrett's | Dresscodes (Reihe Die Kleiderordnung) | https://debretts.com/addressing-the-dress-code/ | 01.11.2026 (Kalenderrecherche) | aus der Kalenderrecherche übernommen, vor Verwendung neu abrufen |

Hinweis zum Kalender: Viele Themen der Reihen Passform-Check und Das Detail verrät stützen sich auf Händlerratgeber (Suitsupply, T.M. Lewin, Proper Cloth, Moss). Nach Regel 7 werden diese Themen vor der Produktion auf Normen oder Fachliteratur umgestellt oder als weiche Aussage ohne Namen formuliert.

## 7. Produktion je Video

1. Thema aus `data\calendars\menswear_2026-11.json`, Reihe festlegen, Quellen nach Abschnitt 6 lesen und Seite notieren.
2. Sprechtext so schreiben, dass er die Hand am Tisch führt („dreh um“, „schau auf die Schräge“). Passt ein Woche-1-Plan mit bezahlter Stimme Wort für Wort, Stimme mit `--reuse-voice` übernehmen. Für Suitwerk gibt es bis heute keine bezahlten Woche-1-Stimmen (nur Mock), nur die Test-Stimme „Unterer Sakkoknopf“.
3. Plan `data\direction\<video_id>.P1.json` (Muster: Pilotplan): `layout.format: "kreidestrich"`, `layout.series` (`stoff`, `anprobe`, `mass`, `anlass`), `layout.series_topic`, `layout.explainer: false`, Szenen `kw_*` mit Wortankern, `source` je Szene.
4. Trockenlauf: `.venv\Scripts\python.exe scripts\render_direction.py <plan> --version P1dry --tts mock --no-render`, dann `node scripts\overlap_check.mjs storage\direction\<id>-P1dry\project` und Standbilder mit `npx hyperframes snapshot . -o ..\snapshots --at <Zeiten>` im Projektordner.
5. Render über die Warteschlange: `.venv\Scripts\python.exe scripts\render_queue.py menswear -- scripts\render_direction.py <plan> --version P1 --tts gemini --mirror suitwerk-regie/<name>` (oder `--reuse-voice <wav>`).
6. Überschneidungsprüfung, Sichtprüfung, Export mit `brands\menswear\tools\export_suitwerk.py <plan> --version P1 --short "<Kurztitel>"`, Zeile im Redaktionsplan. Nichts veröffentlichen.

Szenen-Datenfelder (Kurzreferenz, Details im Modulkopf von `kreidestrich\scenes.py`):
- `kw_hook`: `question`, `question_at`, `chalk_at`, `swatches` [`kind`, `label`], `labels_at`, `neq_at`, `lens_at`, `lens2_at`, `source`.
- `kw_weave`: `kind` (plain, twill), `title`, `title_at`, `warp_at`, `weft_at`, `rows_at`, `first_row`, `row_step`, `formula` {text, at}, `shift_at`, `diag_at`, `note` {text, at}, `colors_note`, `source`.
- `kw_draft`: `left`/`right` {kind, title, word, word_at}, `start_at`, `row_step`, `legend` {text, at}, `source`.
- `kw_flip`: `flip_at`, `left`/`right` {kind, title, front, back, verdict, at, return_at}, `arrow_at`, `source`.
- `kw_close`: `kinds`, `fuzz` (Liste der haarigen Muster), `chip` {text, at}, `lines` [{text, at}], `tilt_at`, `rule` {text, at}, `sign_at`, `claim`, `sign_note`, `source`.
- `kw_weigh` (auch als Hook): `question` oder `title` {text, at}, `kind`, `fuzz`, `value`, `unit`, `weigh_at`, `readout_label`, `readout_at`, `len_at`, `len_label`, `width_at`, `width_label`, `source`. Stoffstreifen auf der Waage, Anzeige zählt hoch, Länge und Breite in Kreide.
- `kw_range`: `title`, `unit`, `min`, `max`, `step`, `label_every`, `decimals`, `marks` [{value, label, sub, at, up, tone}], `band` {from, to, label, at}, `drift` {from, to, label, at}, `note`, `source`. Maßband-Skala mit Kreidemarken (Gewichte, Mikrometer).
- `kw_fibre`: `title`, `px_per_um`, `items` [{label, um, sub, at}], `bar_um`, `stack_at`, `note`, `source`. Faserquerschnitte im Maßstab mit Kreide-Maßstabsbalken; `stack_at` schiebt sie übereinander.
- `kw_yarn`: `title`, `mode` (woollen, worsted), `steps` [{key: card, slub, comb, top, draw, spin; label; at}], `noil_label`, `source`. Fasern vom Flocken bis zum Garn; beim Kämmen fallen die kurzen heraus.
- `kw_finish`: `title`, `start_state` (milled), `stages` [{kind: woven, milled, cropped, checked; label; at}], `colors_note`, `source`. Gewebe im Fadenzähler wird gewalkt (dichter, Fasern), geschoren (kurz), geprüft.
- Zusätzlich: `fuzz: true` an Stoffmustern (`kw_hook`, `kw_flip`) für Streichgarn und gewalktes Tuch; `kw_flip` mit `flip: false` als reiner Vergleich.

## 8. Offene Punkte für Stefans Freigabe

- Formatname „Kreidestrich“, Kanalsatz in Abschnitt 1, die vier Reihen und ihre Namen.
- Pilot „Köper oder Leinwand“ (Abschnitt 9): Optik und Ablauf.
- Code noch zu bauen: Schneiderbüste mit Kleidungsstück und Kreide-Prüfzeichen (Anprobe), Bemaßungslinien mit Schieber (Nachgemessen), Flachlage mit Abhaken und Streichen (Die Kleiderordnung), weitere Bindungen (Fischgrat als gebrochener Köper, Hahnentritt als Farb- und Bindungseffekt).
- Quellen: Händlerquellen im Kalender ersetzen (Abschnitt 6, Hinweis); Begriff „Bindungspatrone“ mit einer Fachquelle belegen, dann im Sprechtext verwenden (im Piloten bewusst nur „Karopapier“).
- Woche 1 (09.–15.11.), entschieden von Stefan am 02.11.2026: nur die vier Stoffkunde-Themen im neuen Format, DE und EN (Pläne `data\direction\<id>.K1.json`): Stoffgewicht (10.11.), Super 100s (11.11.), Kammgarn oder Streichgarn (13.11.), Tweed (14.11., eingegrenzt: Flanell nur mit Weberei-Quellen belegbar, Fresko ist ein geschützter Name einer Weberei). Alle Zahlen aus Woolmark-Handbuch, Woolmark-Spezifikation F-6 und Harris Tweed Authority, im Original gelesen. Die übrigen 17 Woche-1-Themen ruhen.
- Englische Fassung des Piloten: Plan `data\direction\menswear-20261202-3-en.P1.json`, Stimme Algenib, Render in der Warteschlange.

## 9. Pilot „Köper oder Leinwand: woran man die Bindung erkennt“

- Kalenderthema `menswear-20261202-3-de` (Stoffkunde C14, Status planned), Reihe „Unter dem Fadenzähler“.
- Export: `05 Produktion\Suitwerk\2026-12\2026-12-02 Pilot Köper und Leinwand\04 Export\2026-12-02 Pilot Köper und Leinwand – 9x16.mp4`, 83,1 s, 1080 × 1920.
- Prüfung: Prüfbericht VALIDATED, Layout 0 Fehler, `overlap_check` ohne Befund, −15,6 LUFS, 56 Bildereignisse (Median 1,3 s). Hinweis ohne Folge: zwei `kw_weave`-Szenen hintereinander (gewollt: dieselbe Ansicht, andere Bindung).
- Render: `storage\direction\menswear-20261202-3-de-P1`, Spiegel `05 Produktion\_Demos\suitwerk-regie\kreidestrich-p1`, Plan `data\direction\menswear-20261202-3-de.P1.json`.
- Kosten: Gemini-Stimme Orus 0,0201 USD (neu vertont; zu diesem Thema gab es keinen Woche-1-Plan und für Suitwerk keine bezahlten Woche-1-Stimmen). Keine Credits, keine KI-Bilder.
- Quelle: Woolmark, *Introduction to Wovenwear*, S. 9 und 10, im Originaltext gelesen. Nicht gesagt, weil unbelegt: Fall, Knittern, Dichte, Haltbarkeit, „besser“; der Begriff „Bindungspatrone“.
- Sprechtext:
  1. Zwei Anzugstoffe, gleiche Farbe, gleiche Wolle. Und doch sind sie anders gewebt. Das zeigt dir erst der Fadenzähler.
  2. Stoff A ist eine Leinwand. Die Längsfäden heißen Kette, der Querfaden heißt Schuss. Er läuft einmal über einen Kettfaden, einmal darunter, immer im Wechsel. Der nächste Schuss macht es genau umgekehrt. Das ist die einfachste Bindung.
  3. Stoff B ist ein Köper. Hier geht der Schuss über zwei Kettfäden und unter zwei hindurch. Jeder neue Schuss rückt um einen Faden weiter. So entsteht eine schräge Linie, der Köpergrat. Sie ist sein Kennzeichen.
  4. Auf Karopapier sieht das so aus, Faden für Faden. Jedes dunkle Kästchen heißt hier: Kettfaden oben. Bei der Leinwand wird daraus ein Schachbrett, beim Köper eine Treppe.
  5. Jetzt dreh beide Stoffe um und vergleiche. Die Leinwand sieht hinten genauso aus wie vorne. Der Köper hat eine Vorderseite: Dort läuft der Grat meist von rechts oben nach links unten.
  6. Beides sind echte Anzugstoffe. Woolmark nennt für Anzüge aus Kammgarn Leinwand, Köper und Gabardine. Halte den Ärmel deines Sakkos schräg ins Licht: Siehst du feine Schrägen, ist es ein Köper. Folge Suitwerk für Herrenstil mit Blick fürs Detail.
- Selbstkritik: Das Video ist mit 83 s am oberen Rand; künftige Texte kürzer (Abschnitt 3). Die Schräglicht-Probe am Schluss ist als Bild noch schwach (Lichtstreif über den Mustern); mit einem KI-Stoffbild aus der Bibliothek könnte sie stärker werden, ohne die gezeichnete Bindung zu ersetzen.
