# Ausgabe- und Arbeitsplan Higgsfield Ultra (November 2026)

Stand: 02.11.2026 abends (Wien), Claude. **Freigegeben von Stefan am 02.11.2026 („Plan freigeben“).**

## 1. Ausgangslage

- **Tarif:** Higgsfield Ultra, Guthaben **3.000 Credits** (Abfrage über den Higgsfield-Konnektor am 02.11.2026 abends). Ob nicht verbrauchte Credits am Monatsende verfallen, ist nicht ermittelbar. Der Plan verbraucht sie deshalb bis spätestens 30.11.2026.
- **Preise** (geprüft am 02.11.2026 mit der Kostenabfrage `get_cost`, siehe `02 Marke\Zonkfruit\Serie\Kostenschätzung Pilot.md`):
  - Bild Nano Banana Pro: 2K 2 Credits, 4K 4 Credits.
  - Video Kling 3.0 Omni Frames pro ohne Ton: 1,25 Credits je Sekunde (8 s = 10 Credits).
  - Fehlgeschlagene Aufträge werden gutgeschrieben.
- **Stefans Ziele (02.11.2026):**
  1. Alles prüfen und verbessern, auch das bereits Freigegebene.
  2. Für alle Marken Vorlagen, mit denen später ohne Higgsfield in gleicher Qualität produziert werden kann.
  3. Scutoria: YouTube-Vorlage und YouTube-Videos von 15–25 min. Dazu Reels als Ausschnitte daraus und eigene Reels von 65–95 s. Mindestens 10 Videos: 3 sofort, 7 in Planung.
  4. Tintora: YouTube-Folge von 12–25 min, Reels von 65–120 s direkt aus der Folge geschnitten. 1 Folge sofort, 5 in Planung.
  5. Das Higgsfield-Limit ausnutzen, mit einem konkreten Ausgabeplan.

## 2. Grundsatz

Higgsfield erzeugt zwei Dinge:
- **Bibliotheken,** also wiederverwendbare Bausteine je Marke: Hintergründe, Texturen, Schleifen und Zwischenschnitte. Sie liegen mit Nachweis und Prompt im Repository unter `brands\<id>\assets\higgsfield\` und dürfen danach beliebig oft verwendet werden.
- **die Tintora-Folge,** weil eine Anime-Serie ohne KI-Bild nicht geht.

Alles andere baut der Code aus diesen Bausteinen. Wenn die Credits verbraucht sind, laufen alle Marken ohne Higgsfield in derselben Qualität weiter. Ausnahme ist Tintora: Ab Folge 2 braucht Tintora wieder Credits.

## 3. Ausgabeplan

| Block | Inhalt | Credits | Sitzung |
|---|---|---|---|
| **A Tintora Folge 1** | etwa 14 min in 16:9. Etwa 10 Abschnitte im Stil der klassischen TV-Animation: Bewegtbild nur dort, wo es die Handlung braucht, sonst Standbilder mit Kamerafahrt (wie bei klassischen TV-Serien). Rechnung je Abschnitt von 80 s: etwa 30 s Video × 1,25 = 38 Credits, etwa 20 Bilder × 2 = 40 Credits. Mit Faktor 1,5 für Ausschuss sind das etwa 117 Credits je Abschnitt, für 10 Abschnitte etwa 1.170. Dazu neue Schauplätze 42 und Thumbnails für 6 Folgen 72. | **1.300** | Tintora |
| **B Scutoria YouTube** | Bibliothek in 16:9: 24 Zwischenschnitte zu 8 s (Büro, Werkstatt, Praxis, Dokumente, Bildschirme ohne echte Marken; 24 × 10 + 24 Startbilder × 2 = 288). Dazu 12 Einstellungen eigens für die ersten 3 Videos (12 × 12 = 144) und Thumbnail-Entwürfe für 10 Videos (10 × 3 × 4 = 120). | **550** | Scutoria YouTube (neu) |
| **C Bibliotheken der anderen sieben Marken** | je Marke Hintergründe, Texturen und Schleifen nach ihrer Format-Bibel: Dewlane 120 (Texturen und neutrale Produktbilder, das Paket der Sitzung von 88 plus Reserve), Gigastruct 120 (Baustellen- und Luftbilder als Einstieg), Suitwerk 120 (Stoffe in Nahaufnahme, Kleidungsdetails), Revlore 100 (Werkstatt- und Motorraum-Stimmung; die Mechanik bleibt im Code-Modell), Gritwerk 100 (erst nach Stefans Entscheidung über den neuen Kern), Frontlore 60 (nur gezeichnete Karten, Papier- und Museumshintergründe; keine Bilder, die wie echte Archivfotos aussehen, keine Waffen im Einsatz), Promptwerk 40 (Intro- und Hintergrundflächen; der Kern bleibt die echte Aufzeichnung) | **660** | Bibliotheken (neu) |
| **D Reserve** | Nachbesserungen, Ausschuss über Faktor 1,5, Thumbnails, Wünsche nach der Prüfrunde | **490** | Hauptsitzung gibt frei |
| **Summe** | | **3.000** | |

**Ausgaberegeln:**
1. Vor jedem Auftrag eine Kostenabfrage mit `get_cost`. Die Kosten jeder Erzeugung werden mit Job-Nummer in `LICENSE.md` des jeweiligen Ordners vermerkt, dazu der Prompt.
2. Jeder Block beginnt mit einer Probe von höchstens 10 % seines Budgets. Erst wenn die Probe sauber ist (Stil, Konsistenz, keine Schrift im Bild, keine echten Marken), läuft der Rest.
3. Überschreitet ein Block sein Budget um mehr als 10 %, hält die Sitzung an und fragt die Hauptsitzung, die Stefan fragt. Die Reserve gibt nur die Hauptsitzung frei.
4. Bild vor Video: Wo ein Standbild mit Kamerafahrt im Code reicht, wird kein Video erzeugt.
5. Jede Erzeugung ist KI-Material. Die Kennzeichnung in den Videos bleibt wie bisher.

## 4. Scutoria YouTube

**Vorhanden** in `C:\Users\Stefa\OneDrive\scutoria\marketing\youtube` (vom 29./30.10.2026):
- Konzept (`KONZEPT.md`), Kanalplan, Themen.
- **10 fertige Skripte** auf Deutsch und Englisch, `SKRIPTE\01` bis `10`.
- Kennzeichnungsregeln und Shorts-Plan.
- Deine Originalvorlage für das Langvideo und eine begonnene Animationskette (`ANIMATION\`).
- Für diesen Ordner gilt dessen eigene `CLAUDE.md`.

**Vorschlag:**
- **Länge:** Die Skripte waren für 10–15 min geschrieben. Sie werden je nach Thema auf 15–25 min ausgebaut, mit Beispielbetrieb, Entscheidungsfall im Stil von „Was tust du?“ und Quellen am Bildschirm.
- **Die ersten 3 Videos:** 01 „KI-Regeln für den Start“, 02 „Sicherheitsfragebogen“, 04 „Was nie hineingehört“. Video 03 ist ein Rundgang durch die Toolkits und braucht die fertige Website; es rückt in die Planung.
- **In Planung:** die übrigen 7 Videos (03, 05–10): Skript ausgebaut, Szenenplan, Thumbnail-Entwurf.
- **Vorlage:** eine 16:9-Langvideo-Vorlage im Renderer von `faceless-network`, damit Warteschlange, Überschneidungs-Prüfung und Export für alle gleich sind. Bildsprache aus dem Scutoria-Designsystem und deiner Originalvorlage.
- **Reels aus dem Langvideo:** Je Video werden 4–6 Kapitel eigens im Hochformat aus denselben Szenen gerendert. Weil das Bild aus Code entsteht, ist das scharf und kostet keine Credits.
- **Eigene Reels:** Die eigenständigen Reels von 65–95 s laufen im Format „Was tust du?“ weiter, wie in Woche 1.
- **Risiko Render-Zeit:** Wie lange ein Video von 20 min rendert, ist nicht ermittelbar, bis die erste Probe gelaufen ist. Langvideos rendern nachts.

## 5. Tintora YouTube

- **Folge 1:** 12–25 min, Vorschlag etwa 14 min. Etwa 10 Abschnitte aus dem Staffelbogen, verdichtet, sodass die Folge mit einem Cliffhanger endet.
- **Reels von 65–120 s:** Sie werden direkt aus der Folge geschnitten, ein Abschnitt je Reel, mit dem Cliffhanger am Ende. Das 16:9-Bild steht mittig im Hochformat, dahinter eine unscharfe Vergrößerung, oben Titel und „Teil N“, unten Untertitel. Das kostet keine Credits.
- **5 weitere Folgen in Planung:** Der Staffelbogen (bisher 36 Abschnitte für 2 Langfolgen) wird auf 6 Folgen aufgeteilt. Für die Folgen 2 bis 6 gibt es Exposé und Abschnittsliste, aber noch keine Bilder.
- **Musik:** lizenzfrei, die Quelle ist offen. Die Bedingungen von YouTube Audio Library und Pixabay werden vor der Nutzung geprüft und in `08 Recht und Verwaltung\Lizenzen` belegt.
- **Stimmen:** Gemini, etwa 0,5 USD für Folge 1 in Deutsch und Englisch.

## 6. Vorlagen für alle Marken

Je Marke entsteht `02 Marke\<Marke>\Vorlage <Marke> (Format 1.0).md` mit:
- dem Format aus der Format-Bibel als Arbeitsanleitung
- den Szenentypen im Code und ihren Parametern
- der Bibliothek mit Vorschau (Kontaktbogen), Nachweis und Prompt je Baustein
- einem Muster-Plan, aus dem ein neues Video entsteht
- der Prüfliste vor dem Export

Ziel: Eine neue Sitzung baut ein Video in Format-Qualität, ohne Higgsfield und ohne Rückfragen.

## 7. Prüf- und Verbesserungsrunde für alle neun Marken

- **Unabhängige Prüfung:** Eine eigene Sitzung prüft alle Marken, auch die freigegebenen Piloten und die ersten Videos aus Woche 1. Sie war an der Produktion nicht beteiligt.
- **Prüfpunkte:**
  - Format-Bibel gegen das tatsächliche Video
  - Bildfüllung, Lesbarkeit, Überschneidungen
  - Quellen und Datum
  - KI-Kennzeichnung
  - Ton und Länge
  - Abstand zu den anderen Marken
- **Ergebnis:** `02 Marke\Prüfrunde 2026-11-03.md` mit Befunden je Marke, nach Schwere geordnet.
- **Umsetzung:** Die Marken-Sitzungen beheben die Befunde in ihrer Marke. Die Hauptsitzung behebt die Befunde am gemeinsamen Renderer, dazu die drei offenen Wünsche aus Dewlane:
  - `overlap_check` prüft auch die Hintergrundebene
  - der Schlusssatz steht in `Veröffentlichung.md` nicht mehr doppelt
  - die KI-Zeile kommt je Marke aus `brand.yaml`

## 8. Sitzungen

| Sitzung | Aufgabe | Higgsfield |
|---|---|---|
| Tintora (vorhanden) | Block A, Folge 1, Planung Folgen 2–6 | ja |
| Scutoria YouTube (neu) | Block B, Vorlage 16:9, Videos 01, 02, 04, Planung der übrigen 7 | ja |
| Bibliotheken (neu) | Block C für sieben Marken nach den Prompt-Blättern `02 Marke\<Marke>\Bibliothek Prompt-Blatt.md`, mit Kontaktbogen, Nachweis und Prompt; den Bibliotheksteil der Vorlage schreibt sie, den Rest der Vorlage die Marken-Sitzung | ja |
| Prüfrunde (neu, unabhängig) | Abschnitt 7, nur lesen und bewerten | nein |
| Marken-Sitzungen (vorhanden) | Woche 1 weiter, dann Befunde beheben und Bibliothek einbauen | nein |

Die Bibliothek für sieben Marken erzeugt eine einzige Sitzung, damit Ausgaben und Anmeldung an einer Stelle bleiben.

## 9. Was Stefan tun muss

1. Diesen Plan freigeben oder ändern.
2. In jeder Sitzung mit Higgsfield einmal `/mcp` ausführen und Higgsfield anmelden: Tintora, Scutoria YouTube, Bibliotheken. Ohne Anmeldung kann eine Sitzung keine Bilder erzeugen.
3. Später: die Musikquelle für Tintora wählen.

## Neue Verteilung 03.11.2026 (Stefan: „Vorschlag so“, 13:03 Wien)

Der Plan oben ist überholt: Nach Stufe 0 Tintora, den Konzeptbildern, den neun Testvideos (etwa 700 Credits), der Scutoria-YouTube-Vorbereitung (80) und den ersten vier Bibliotheken (186) waren am 03.11. um 12:40 Wien noch 1.416 von 3.000 Credits übrig. Stefan hat diese Verteilung für den Rest des Novembers freigegeben:

| Posten | Credits | Regeln |
|---|---|---|
| Bibliotheken Rest (Frontlore, Gritwerk, Promptwerk) | 214 | je etwa 70, fotorealistische Bilder nach Häufigkeit im Konzeptplan plus höchstens ein Clip; alte abstrakte Schleifen entfallen |
| Tintora Folge 1 | 500 | Kostenschätzung darauf kürzen, Plan vor der nächsten Buchung an die Hauptsitzung; Rest der Folge im Dezember oder nach Nachkauf |
| Scutoria YouTube | 250 | Video 01 und 02, Einschübe für Reels daraus |
| Tagesproduktion (9 Marken) | 300 | 33 je Marke bis 30.11., höchstens 2 je Thema, Bibliotheks- und Testvideo-Material zuerst |
| Reserve | 152 | nur über die Hauptsitzung mit Begründung |
| Summe | 1.416 | Guthaben 03.11., 12:40 Wien |

Verbrauch: Jede Sitzung führt ihre Credits im Prüfbericht und im Konzeptplan mit; die Hauptsitzung prüft das Guthaben bei jeder Übersichts-Aktualisierung. Preise am 03.11.: Nano Banana Pro 2 Credits je Bild, Kling 5 s 6,25, Kling 8 s pro 10.
