# Konzeptplan Suitwerk (ab November 2026)

Stand: 02.11.2026 (Wien), umgestellt am 03.11.2026 auf Stefans Vorgabe „realer, animierter Anzug“ (Abschnitt „Neuausrichtung“). Marke Suitwerk (`menswear`). Konzeptplan zur Planung, keine Freigabe einzelner Videos. Grundlage: `02 Marke\Suitwerk\Format-Bibel.md` (Format „Kreidestrich“, Fassung 1.0, freigegeben 02.11.2026), Kalender `C:\Automation\faceless-network\data\calendars\menswear_2026-11.json`, `04 Redaktionsplan\Themen- und Kalenderplan Suitwerk (09.11.–06.12.2026).md`.

## Kurzkonzept

- **Versprechen:** „Herrenstil im Detail: Stoff, Schnitt und Maß, gezeichnet statt behauptet.“ Faden, Schnitt und Maß kommen auf den Zuschneidetisch; richtig und falsch liegen nebeneinander, mit Kreide markiert.
- **Zielgruppe:** Männer, die sich gut anziehen wollen, ohne Trends zu folgen; DACH und international. Ton ruhig, kundig, nie herablassend, Anrede „du“.
- **Format:** „Kreidestrich“: dunkles Kammgarntuch von oben, Schneiderkreide als einzige Markierung, Fadenzähler, Gewebe aus der Bindung gerechnet, Test für zuhause am Schluss. Reel 9:16, Ziel 70–80 s (Netzwerk 65–95 s, Format-Bibel 65–90 s), 155–175 Wörter, Gemini Orus (DE).
- **Reihen:** Unter dem Fadenzähler (Szenen gebaut) · Anprobe · Nachgemessen · Die Kleiderordnung (für diese drei fehlen noch Code-Bausteine).
- **Takt (ab 04.11.2026, Stefan):** 2 Themen je Tag, jedes auf Deutsch und Englisch, also 4 Videos. Reihenfolge je Thema: Skript DE, Vertonung DE, Render DE, dann EN aus denselben Szenen. Gemini Flash höchstens 4 Anfragen je Tag. Higgsfield (Verteilung von Stefan freigegeben, 03.11.2026): Tagesproduktion zusammen 33 Credits bis 30.11.2026, höchstens 2 je Thema (ein Nano-Banana-Bild, keine Kling-Clips); mehr nur mit Begründung über die Hauptsitzung (Reserve 152). Zuerst die Realbild-Bibliothek (`brands\menswear\assets\higgsfield\library\`, 17 Bilder und 1 Clip, Tabelle in `02 Marke\Suitwerk\Vorlage Bibliothek.md`) und das Testvideo-Material (`…\higgsfield\testvideo\`) verwenden; neues eigenes Material nie in `library\`, sondern daneben mit eigener `LICENSE.md`.
- **Higgsfield-Verbrauch Tagesproduktion (Stand 03.11.2026):** 0 von 33 Credits. Wird je Thema hier und im Prüfbericht nachgetragen.
- **Regeln:** Stilregeln heißen Konvention; keine Marken, keine Händler, keine Kaufempfehlung; Normen und Fachliteratur vor Händlerratgebern; keine Zahl ohne Quelle im Bild; bewertet wird das Kleidungsstück, nie der Körper.

## Neuausrichtung 03.11.2026: in jedem Video ein realer, animierter Anzug

Stefan hat das Testvideo „Köper und Leinwand“ am 03.11.2026 freigegeben (`05 Produktion\Suitwerk\2026-11\2026-11-03 Testvideo Köper und Leinwand`). Es ist die Vorlage. Seine Vorgabe: In jedem Video ist ein realer, animierter Anzug zu sehen (KI-Bild oder KI-Clip, gekennzeichnet „KI-Bild“, ohne Gesichter; Hände und Menschen von hinten sind erlaubt). Stoffkunde bleibt die Grundlage, weil sie belegbar ist und am echten Stoff gezeigt werden kann. Die Kreide erklärt auf dem echten Bild, was das Auge nicht auflöst.

**Pflicht in jedem Video:**
1. Hook mit realem Anzug oder realem Stoff am Anzug (Bild mit langsamer Kamerafahrt oder Clip), Kreidefrage darüber.
2. Erklärung als Zeichnung (gerechnet, Faden für Faden oder Maß) auf echtem Tuch als Hintergrund.
3. Schluss am realen Anzug: Test für zuhause am Ärmel, Revers oder Saum, Abspann vor einem Anzugdetail.
4. Ton nach Tonebene (Palette `paper`, Bett `warm`, Geräusche höchstens −16 dBFS).

**Fünf Bildaufbauten, die über die Themen wechseln** (zwei aufeinanderfolgende Videos nie mit demselben Aufbau):

| Aufbau | Bild | passt zu | Material |
|---|---|---|---|
| A „Bügel und Fadenzähler“ | Zwei Sakkos am Bügel, Fadenzähler landet auf dem Tuch, Gewebe im Fenster | Bindungen (Köper, Fischgrat, Atlas, Panama) | Testvideo (K1, Paarbilder), Bibliothek Stoffe |
| B „Waage und Maßband“ | Stoffstreifen auf der Waage, Maßband-Skala; realer Anzug im Hook und im Schluss | Zahlen auf dem Etikett (Gewicht, Super-Zahl, Zwirn) | Sakko vorne (K3), Revers (K4) |
| C „Faser und Garn“ | Querschnitt und Weg zum Garn über einem Makro des Ärmels | Garn und Faser (Kammgarn, Mohair, Kaschmir, Leinen) | Ärmel im Licht (K2), Bibliothek Mohair, Leinen |
| D „Werkstatt“ | Tuch durchläuft die Stationen (gewebt, gewalkt, geschoren), Abschluss am fertigen Sakko | Ausrüstung (Tweed, Flanell, Loden, Kreidestreifen) | Bibliothek Tweed, Flanell, Zuschneidetisch, Schneiderbüste |
| E „Muster am Körper“ | Sakko von hinten oder Hand am Revers (ohne Gesicht), Muster wird mit Kreide aufgelöst | Muster (Hahnentritt, Glencheck, Seersucker, Streifen) | je Thema ein neues Bild (2 Credits) |

**Reihenfolge ab 04.11.2026** (je Tag zwei Themen, Aufbau wechselt; Pläne für 1–4 liegen als `data\direction\<id>.K1.json` vor und bekommen den Anzug dazu):

| Tag | Thema 1 (Aufbau) | Thema 2 (Aufbau) |
|---|---|---|
| 04.11. | Stoffgewicht (B) | Kammgarn oder Streichgarn (C) |
| 05.11. | Tweed nach dem Webstuhl (D) | Super 100s (B, mit Ärmel-Makro statt Waage) · Tagesläufer: produziert 2026-11-03 (menswear-20261103-2-de-D1, menswear-20261103-2-en-D1) |
| 06.11. | Fischgrat (A) | Hahnentritt (E) |
| 07.11. | Mohair (C) | Glencheck (E) |
| 08.11. | Kreidestreifen oder Nadelstreifen (D) | Leinen (C) |

Danach weiter mit den Nummern 6–16 und 56–64 der Tabelle. Die Reihen Anprobe, Nachgemessen und Die Kleiderordnung folgen erst mit besseren Quellen als Händlerratgebern (Stefan, 02.11.2026) und mit eigenen Code-Bausteinen; bis dahin gibt es Anzugdetails nur als Bild im Hook und im Schluss.

Lesehilfe: „belegt im Kalender“ heißt, Thema und Ansatz sind im Kalender mit Quellen hinterlegt (`source_urls`, `notes`). Vor der Produktion gelten trotzdem die Prüfregeln der Format-Bibel (Abschnitt 6): Quelle im Original lesen, Seite notieren, Händlerquellen ersetzen. Hooks nennen nur, was im Kalenderansatz steht; neue Vorschläge haben Hooks ohne Zahlen und Fakten.

## Vorschläge

| Nr | Thema/Titel | Reihe | Format | Hook-Idee | Quellenstand | Risiko |
|---|---|---|---|---|---|---|
| 1 | Stoffgewicht: Was die Zahl wirklich misst | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Stoffstreifen gleicher Breite liegen auf der Waage, und die Kreide fragt, wovon die Zahl auf dem Etikett eigentlich das Gewicht ist. | belegt im Kalender `menswear-20261110-1-de` | niedrig |
| 2 | Super 100s: was die Zahl bedeutet und was nicht | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Etiketten mit verschiedenen Super-Zahlen, und unter dem Fadenzähler zeigt sich: Die Zahl nennt nur eine Obergrenze für die Faserdicke. | belegt im Kalender `menswear-20261111-3-de` | niedrig · Tagesläufer: produziert 2026-11-03 (menswear-20261103-2-de-D1, menswear-20261103-2-en-D1) |
| 3 | Kammgarn oder Streichgarn: der Weg zum Garn | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Wollstoffe aus derselben Faser, einer glatt, einer haarig: Der Unterschied liegt im Weg vom Vlies zum Garn. | belegt im Kalender `menswear-20261113-1-de` | niedrig |
| 4 | Flanell, Tweed, Fresko: drei Tuche, drei Bauweisen (eingegrenzt auf Tweed) | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Tuch kommt glatt vom Webstuhl, und erst das Walken nach dem Weben macht daraus Tweed. | belegt im Kalender `menswear-20261114-3-de` · Woche 1 nur Tweed: Flanell nur mit Weberei-Quellen belegbar, Fresko ist ein geschützter Name einer Weberei | niedrig |
| 5 | Köper oder Leinwand: woran man die Bindung erkennt (Pilot produziert) | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Anzugstoffe, gleiche Farbe, gleiche Wolle, und erst der Fadenzähler zeigt, dass sie anders gewebt sind. | belegt im Kalender `menswear-20261202-3-de` | niedrig |
| 6 | Fischgrat: ein Köper, der die Richtung wechselt | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Köper, der mitten im Stoff die Richtung wechselt: Die Kreide zieht die Grate nach, bis das V sichtbar wird. | belegt im Kalender `menswear-20261125-3-de` | niedrig |
| 7 | Hahnentritt: gewebt, nicht gedruckt | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Das gezackte Muster ist nicht aufgedruckt: Der Fadenzähler zeigt, wie es aus der Folge farbiger Garne und der Bindung entsteht. | belegt im Kalender `menswear-20261201-1-de` | niedrig |
| 8 | Glencheck: ein Gutskaro aus Glen Urquhart | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein großes Karo zerfällt unter dem Fadenzähler in Blöcke kleinerer Muster wie Hahnentritt. | belegt im Kalender `menswear-20261128-3-de` · Herkunftslegende Edward VII. nicht verwenden | niedrig |
| 9 | Seersucker: woher die Kräuselstreifen kommen | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Glatte und gekräuselte Streifen im selben Stoff: Die Ursache liegt schon am Webstuhl, in der Spannung der Kettfäden. | belegt im Kalender `menswear-20261124-1-de` | niedrig |
| 10 | Mohair im Anzug: Glanz und Sprungkraft | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Stoffmuster werden zusammengedrückt und losgelassen, eines springt in die Form zurück: Mohair als Beimischung zur Wolle. | belegt im Kalender `menswear-20261120-1-de` | niedrig |
| 11 | Kaschmir im Anzugstoff: was das Etikett verspricht | Unter dem Fadenzähler | Reel 9:16, 70–80 s | „Kaschmir“ steht auf dem Etikett: Was das Wort genau meint und wie viel davon meist im Anzugstoff steckt. | belegt im Kalender `menswear-20261121-3-de` | niedrig |
| 12 | Leinen: knittert, kühlt aber im Sommer | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Leinenstück knittert sichtbar neben einem Wollstück, und die Kreide schreibt darunter, warum das zum Stoff gehört. | belegt im Kalender `menswear-20261118-3-de` | niedrig |
| 13 | Harris Tweed: Was das Orb-Siegel garantiert | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Tweedmuster sehen gleich aus, nur eines trägt das Orb-Siegel: Was das Zeichen nach dem Harris Tweed Act 1993 garantiert. | belegt im Kalender `menswear-20261117-1-de` · Herkunftszeichen als Sachinformation erlaubt (Regel 6) | niedrig |
| 14 | Kreidestreifen oder Nadelstreifen? | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Streifenstoffe nebeneinander: Auf dem einen ist die Linie scharf, auf dem anderen durch das Rauen weich gebrochen. | belegt im Kalender `menswear-20261127-1-de` | niedrig |
| 15 | Hemdstoffe: Popeline, Oxford, Twill | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Drei weiße Hemdstoffe wirken von weitem gleich, unter dem Fadenzähler sind es drei Bindungen. | belegt im Kalender `menswear-20261204-1-de` | niedrig |
| 16 | Gabardine: der Stoff hinter dem Trenchcoat | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Mantelstoff unter dem Fadenzähler: Was macht ein dicht gewebtes Tuch zum Wettertuch? | belegt im Kalender `menswear-20261205-3-de` · Kalender stützt sich auf die Darstellung eines Herstellers; im Bild und Text kein Firmenname (Regel 6) | niedrig |
| 17 | Revers: fallend, steigend oder Schal | Nachgemessen | Reel 9:16, 70–80 s | Drei Revers nacheinander am selben Sakko, und die Kreide markiert, welches als formeller gilt. | belegt im Kalender `menswear-20261109-2-de` | niedrig |
| 18 | Einreiher oder Zweireiher | Nachgemessen | Reel 9:16, 70–80 s | Zwei Sakkos, eines überlappt weit: Die Kreide zeigt, warum der Zweireiher geschlossen gedacht ist. | belegt im Kalender `menswear-20261110-3-de` | niedrig |
| 19 | Rückenschlitz: keiner, einer, zwei | Nachgemessen | Reel 9:16, 70–80 s | Kein Schlitz, einer, zwei: am Tagesanzug ein Wunsch, am Dinnerjacket eine Konvention. | belegt im Kalender `menswear-20261112-1-de` | niedrig |
| 20 | Taschen verraten den Anlass | Nachgemessen | Reel 9:16, 70–80 s | Drei Sakkos ohne Etikett, nur die Taschen sind verschieden, und daran lässt sich der Anlass ablesen. | belegt im Kalender `menswear-20261113-3-de` | niedrig |
| 21 | Echte Knopflöcher am Ärmel | Nachgemessen | Reel 9:16, 70–80 s | Warum öffnet man die Ärmelknopflöcher erst nach dem Kürzen? Die Kreide zeigt, wie sie die Ärmellänge festlegen. | belegt im Kalender `menswear-20261116-2-de` | niedrig |
| 22 | Die Einlage: geklebt, Half oder Full Canvas | Nachgemessen | Reel 9:16, 70–80 s | Zwei Sakkos sehen von außen gleich aus, innen ist die Einlage einmal aufgeklebt und einmal lose eingenäht. | belegt im Kalender `menswear-20261117-3-de` | niedrig |
| 23 | Bundfalten: wozu? | Nachgemessen | Reel 9:16, 70–80 s | Zwei Hosen, eine mit Falten am Bund: Die Kreide zeigt, wo die zusätzliche Weite beim Sitzen gebraucht wird. | belegt im Kalender `menswear-20261119-1-de` | niedrig |
| 24 | Hosenaufschlag: wann ja, wann nein | Nachgemessen | Reel 9:16, 70–80 s | Zwei gleiche Hosensäume, einer mit Aufschlag, und an der Abendhose streicht die Kreide ihn. | belegt im Kalender `menswear-20261120-3-de` | niedrig |
| 25 | Die Gorge: wo Kragen und Revers sich treffen | Nachgemessen | Reel 9:16, 70–80 s | Zwei Sakkos, die Naht zwischen Kragen und Revers sitzt verschieden hoch: Das ist Hausstil, keine Regel. | belegt im Kalender `menswear-20261130-2-de` | niedrig |
| 26 | Futter: voll, halb, ungefüttert | Nachgemessen | Reel 9:16, 70–80 s | Drei Sakkos werden umgedreht: voll gefüttert, halb gefüttert, ungefüttert. | belegt im Kalender `menswear-20261127-3-de` | niedrig |
| 27 | Hemdkragen: Kent, Haifisch, Button-down | Nachgemessen | Reel 9:16, 70–80 s | Drei Kragen am selben Hemd, und die Kreide markiert, welcher zur Krawatte gedacht ist. | belegt im Kalender `menswear-20261203-1-de` | niedrig |
| 28 | Doppelmanschette oder Knopfmanschette | Nachgemessen | Reel 9:16, 70–80 s | Zwei Manschetten am selben Ärmel, eine mit Manschettenknopf, und keine von beiden ist falsch. | belegt im Kalender `menswear-20261206-1-de` | niedrig |
| 29 | Wie viel Manschette unter dem Sakkoärmel? | Nachgemessen | Reel 9:16, 70–80 s | Wie viel Hemd gehört unter den Sakkoärmel? Die Kreide markiert eine Spanne statt eines festen Werts. | belegt im Kalender `menswear-20261113-2-de` · Spanne stützt sich auf Herstellerangaben; vor Produktion Fachquelle suchen | niedrig |
| 30 | Hosenbruch: kein, leicht, voll | Nachgemessen | Reel 9:16, 70–80 s | Drei Hosenlängen über demselben Schuh, und die Fußweite entscheidet mit, welcher Bruch passt. | belegt im Kalender `menswear-20261115-2-de` | niedrig |
| 31 | Krawattenlänge: Die Spitze endet am Hosenbund | Nachgemessen | Reel 9:16, 70–80 s | Die Krawattenspitze wandert am Schieber auf und ab, bis sie am Hosenbund endet. | belegt im Kalender `menswear-20261114-2-de` | niedrig |
| 32 | Krawattenbreite: Proportion zum Revers | Nachgemessen | Reel 9:16, 70–80 s | Eine Krawatte wird neben dem Revers schmaler und breiter, bis die Proportion zum Sakko stimmt. | belegt im Kalender `menswear-20261128-2-de` | niedrig |
| 33 | Krawattenklammer: zwischen drittem und viertem Knopf | Nachgemessen | Reel 9:16, 70–80 s | Die Klammer wandert von Hemdknopf zu Hemdknopf, und die Kreide markiert die übliche Stelle. | belegt im Kalender `menswear-20261202-2-de` | niedrig |
| 34 | Die Schulter muss passen | Anprobe | Reel 9:16, 70–80 s | Die Schulternaht steht über, und die Kreide zeigt, warum diese Stelle bei der Anprobe zuerst geprüft wird. | belegt im Kalender `menswear-20261111-1-de` | niedrig |
| 35 | Der Sakkokragen steht ab | Anprobe | Reel 9:16, 70–80 s | Im Nacken klafft eine Lücke zwischen Sakko- und Hemdkragen: ein Schnittproblem, keine Größenfrage. | belegt im Kalender `menswear-20261118-1-de` | niedrig |
| 36 | X-Falten am Knopf: das Sakko ist zu eng | Anprobe | Reel 9:16, 70–80 s | Vom geschlossenen Knopf ziehen Falten in X-Form: Die Kreide zeigt, was das Sakko damit verrät. | belegt im Kalender `menswear-20261120-2-de` | niedrig |
| 37 | Wie lang muss ein Sakko sein? | Anprobe | Reel 9:16, 70–80 s | Zwei Sakkos gleicher Größe, verschieden lang: Die Kreide markiert den üblichen Richtwert und sagt dazu, wie locker er ist. | belegt im Kalender `menswear-20261109-3-de` | niedrig |
| 38 | Westenlänge: der Bund bleibt bedeckt | Anprobe | Reel 9:16, 70–80 s | Zwischen Weste und Hose blitzt Hemd hervor, und die Kreide zeigt, wo die Weste enden soll. | belegt im Kalender `menswear-20261130-3-de` | niedrig |
| 39 | Hemdkragen: der Finger-Test | Anprobe | Reel 9:16, 70–80 s | Ein Kragen ohne Lücke und ohne Druck: der Test mit ein bis zwei Fingern. | belegt im Kalender `menswear-20261122-2-de` | niedrig |
| 40 | Was der Änderungsschneider kann und was nicht | Anprobe | Reel 9:16, 70–80 s | Die Kreide markiert auf einem Sakko, was ein Änderungsschneider üblicherweise ändern kann und was kaum. | belegt im Kalender `menswear-20261127-2-de` | niedrig |
| 41 | Konfektion, Maßkonfektion, Maßanfertigung | Anprobe | Reel 9:16, 70–80 s | Drei Sakkos sehen gleich aus, der Unterschied liegt im Schnittmuster, das daneben auf dem Tisch liegt. | belegt im Kalender `menswear-20261116-3-de` | niedrig |
| 42 | Leibhöhe: wo der Hosenbund sitzt | Anprobe | Reel 9:16, 70–80 s | Zwei Hosen gleicher Weite, der Bund sitzt einmal höher, einmal tiefer: ein Maß, das sich nachträglich nicht ändern lässt. | belegt im Kalender `menswear-20261123-3-de` | niedrig |
| 43 | Fußweite der Hose | Anprobe | Reel 9:16, 70–80 s | Ein Hosenbein bleibt im Sitzen an der Wade hängen: Woran man eine zu enge Fußweite erkennt. | belegt im Kalender `menswear-20261125-1-de` | niedrig |
| 44 | Black Tie: Was zum Smoking gehört | Die Kleiderordnung | Reel 9:16, 70–80 s | Auf dem Tisch liegt ein Teil zu viel für Black Tie, und die Kreide streicht es. | belegt im Kalender `menswear-20261110-2-de` | niedrig |
| 45 | White Tie: Der formellste Dresscode | Die Kleiderordnung | Reel 9:16, 70–80 s | Frack, Weste, Fliege, Kragen: Die Kreide hakt ab, was der formellste Dresscode verlangt. | belegt im Kalender `menswear-20261112-2-de` | niedrig |
| 46 | „Lounge Suit“ auf der Einladung | Die Kleiderordnung | Reel 9:16, 70–80 s | „Lounge Suit“ klingt nach Freizeit, und die Teile auf dem Tisch zeigen, was es wirklich meint. | belegt im Kalender `menswear-20261124-2-de` | niedrig |
| 47 | Smart Casual und Cocktail: dehnbare Dresscodes | Die Kleiderordnung | Reel 9:16, 70–80 s | Zwei dehnbare Dresscodes: Die Kreide hakt ab, was die Etikette-Quelle verlangt, und lässt offen, was am Anlass hängt. | belegt im Kalender `menswear-20261114-1-de` | niedrig |
| 48 | Dunkler Anzug bei der Trauerfeier | Die Kleiderordnung | Reel 9:16, 70–80 s | Schwarz ist traditionell, aber nicht zwingend: Die Kreide sortiert die Teile für eine Trauerfeier. | belegt im Kalender `menswear-20261205-1-de` | niedrig |
| 49 | Morning Dress und die Regeln von Royal Ascot | Die Kleiderordnung | Reel 9:16, 70–80 s | Ein Cutaway, eine gestreifte Hose, eine Weste: Die Kreide prüft, was die Konvention verlangt. | belegt im Kalender `menswear-20261122-3-de` · Ascot-Regeln vor dem Skript auf der Veranstalterseite prüfen | niedrig |
| 50 | Schwarzer Anzug ist kein Smoking | Die Kleiderordnung | Reel 9:16, 70–80 s | Zwei schwarze Sakkos auf dem Tisch, nur eines ist ein Smoking, und drei Details verraten es. | belegt im Kalender `menswear-20261118-2-de` | niedrig |
| 51 | Weste: Warum der unterste Knopf offen bleibt | Die Kleiderordnung | Reel 9:16, 70–80 s | Eine Weste, alle Knöpfe geschlossen, und die Kreide öffnet den untersten. | belegt im Kalender `menswear-20261109-1-de` · Edward VII. nur als unbelegte Legende, besser weglassen | niedrig |
| 52 | Hosenträger statt Gürtel – nicht zusätzlich | Die Kleiderordnung | Reel 9:16, 70–80 s | Gürtel und Hosenträger an derselben Hose, und die Kreide streicht eines davon. | belegt im Kalender `menswear-20261111-2-de` | niedrig |
| 53 | Fliege zum Smoking: selbst gebunden | Die Kleiderordnung | Reel 9:16, 70–80 s | Zwei Fliegen, eine vorgebunden, eine selbst gebunden und leicht schief: Welche verlangt die Konvention zum Smoking? | belegt im Kalender `menswear-20261130-1-de` | niedrig |
| 54 | Socken zum Anzug: zur Hose, nicht zum Schuh | Die Kleiderordnung | Reel 9:16, 70–80 s | Zwei Socken neben Hose und Schuh, und die Kreide zieht die Farblinie zur Hose. | belegt im Kalender `menswear-20261112-3-de` · Kalender stützt sich auf Hersteller; weiche Aussage ohne Namen | niedrig |
| 55 | Braune Schuhe zum Anzug: Was von „no brown“ bleibt | Die Kleiderordnung | Reel 9:16, 70–80 s | Braune Schuhe neben einem marineblauen, einem grauen und einem schwarzen Anzug: Bei einem streicht die Kreide. | belegt im Kalender `menswear-20261116-1-de` | niedrig |
| 56 | Atlas: die dritte Grundbindung | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Neben Leinwand und Köper liegt ein drittes Muster: Welche Bindung ist das, und wo kreuzen sich hier die Fäden? | Quelle zu prüfen (ISO 3572, Woolmark-Handbuch) | niedrig |
| 57 | Rechtsgrat oder Linksgrat: Woher die Richtung des Köpers kommt | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Köper nebeneinander, die Grate laufen in entgegengesetzte Richtungen: Ist das ein Unterschied in der Bindung? | Quelle zu prüfen | niedrig |
| 58 | Panama: die Bindung hinter dem Sommerstoff | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Sommeranzugstoff unter dem Fadenzähler: Welche Bindung steckt hinter dem Namen Panama? | Quelle zu prüfen (eigene, belegte Bindungsregel nötig, Regel 1) | niedrig |
| 59 | Faser, Garn oder Stück: Wo die Farbe in den Stoff kommt | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei marineblaue Stoffe, und unter dem Fadenzähler zeigt sich, ob die Farbe schon in der Faser, im Garn oder erst im fertigen Tuch steckt. | Quelle zu prüfen | niedrig |
| 60 | Zwirn: Was „zweifach“ auf dem Etikett meint | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Garne aus zwei Stoffen werden aufgedreht: eines einfach, eines aus zwei Fäden gezwirnt. | Quelle zu prüfen | niedrig |
| 61 | Loden: was ein Wolltuch zu Loden macht | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Was macht ein Wolltuch zu Loden? Der Fadenzähler folgt dem Tuch vom Webstuhl bis zur Ausrüstung. | Quelle zu prüfen | niedrig |
| 62 | Cord: woher die Rippen kommen | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Ein Stoff mit Rippen unter dem Fadenzähler: Woher kommen die Rillen? | Quelle zu prüfen | niedrig |
| 63 | Gewebt oder gestrickt: das Jersey-Sakko | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Zwei Sakkostoffe, einer gewebt, einer gestrickt: Der Fadenzähler zeigt hier Kreuzungen und dort Maschen. | Quelle zu prüfen | niedrig |
| 64 | Die Webkante: was am Rand des Tuchs steht | Unter dem Fadenzähler | Reel 9:16, 70–80 s | Am Rand des Tuchs läuft ein Streifen, der anders aussieht als der Stoff: Was verrät die Webkante? | Quelle zu prüfen | niedrig |
| 65 | Der Fadenlauf: gerade oder schräg zugeschnitten | Nachgemessen | Reel 9:16, 70–80 s | Zwei Zuschnitte aus demselben Tuch, einer im geraden Fadenlauf, einer schräg: Was ändert sich am Kleidungsstück? | Quelle zu prüfen (Fachliteratur Bekleidung) | niedrig |
| 66 | Knopfstand: wo der Schließknopf sitzt | Nachgemessen | Reel 9:16, 70–80 s | Der Schließknopf eines Sakkos wandert am Schieber auf und ab: Wo setzt ihn die Konvention, und sagt eine Fachquelle dazu etwas? | Quelle zu prüfen | niedrig |
| 67 | „Dunkler Anzug“ auf der Einladung im deutschen Sprachraum | Die Kleiderordnung | Reel 9:16, 70–80 s | Auf einer Einladung steht „dunkler Anzug“: Welche Teile legt die Kreide auf den Tisch, und welche streicht sie? | Quelle zu prüfen (Etikette-Quelle für DACH) | niedrig |

Zusammen 67 Vorschläge: 55 aus dem Kalender, 12 neu (Quelle zu prüfen).

## Hinweise zur Tabelle

- **Gebaut ist nur die Reihe „Unter dem Fadenzähler“** (Szenen `kw_*` inklusive Waage, Skala, Faserquerschnitt, Weg zum Garn, Ausrüstung). Für Anprobe, Nachgemessen und Die Kleiderordnung fehlen Schneiderbüste mit Prüfzeichen, Bemaßung mit Schieber und Flachlage mit Abhaken (Format-Bibel, Abschnitt 8). Diese Themen ruhen, bis die Bausteine stehen.
- **Passform- und Maßthemen** stützen sich im Kalender oft auf Händler- und Herstellerratgeber. Nach Stefans Vorgabe vom 02.11.2026 erst mit besseren Quellen (Normen wie ISO 8559-1, Ausbildungsordnung, Fachliteratur Bekleidung) produzieren oder als weiche Aussage ohne Namen formulieren.
- **Herkunftslegenden nie als Fakt:** Edward VII. (Weste, Glencheck), Namen von Windsor- und Four-in-Hand-Knoten, Earl of Derby, Brogue-Lochung als Entwässerung, Chirurgen-Geschichte zu Ärmelknöpfen, Eisenbahn-Herkunft der Ticket Pocket, Herkunft des Reversknopflochs.
- **Neue Vorschläge** (Nr. 56–67) sind nur Themenideen. Bevor eines davon in den Kalender kommt: Quelle nach der Rangfolge der Format-Bibel finden und im Original lesen; neue Bindungen erst mit eigener, belegter Bindungsregel in `warp_up` einbauen.

## Geeignet für die Produktion bis 05.11.2026 (zur Info)

1. **Stoffgewicht: Was die Zahl wirklich misst** (`menswear-20261110-1-de`, Veröffentlichung 10.11.).
2. **Super 100s: was die Zahl bedeutet und was nicht** (`menswear-20261111-3-de`, 11.11.).
3. **Kammgarn oder Streichgarn: der Weg zum Garn** (`menswear-20261113-1-de`, 13.11.).

Gründe: Stefan hat am 02.11.2026 für Woche 1 nur die Stoffkunde-Themen im neuen Format freigegeben; die Zahlen stammen aus dem Woolmark-Handbuch und der Woolmark-Spezifikation F-6, im Original gelesen; die nötigen Szenentypen der Reihe „Unter dem Fadenzähler“ sind gebaut; Pläne `data\direction\<id>.K1.json` liegen für DE und EN vor. Viertes Thema als Ersatz: Tweed (`menswear-20261114-3-de`, 14.11., eingegrenzt).

## Weitere Kalenderthemen (nicht in der Tabelle)

Diese Themen passen grundsätzlich in eine der Reihen, sind aber nachrangig: Anleitungen mit Handhabung (Binden, Falten, Packen, Pflege) haben im Format noch keinen Baustein, Schuh- und Zubehörthemen keine eigene Reihe, zwei Themen arbeiten mit der Schere am Sakko (Risiko mittel), und „Die Uhr unter der Manschette“ hat keine Primärquelle (Status `idea`). Sie bleiben Reserve für später.

- `menswear-20261115-1-de` Wozu das Knopfloch im Revers?
- `menswear-20261115-3-de` Drei Krawattenknoten im Vergleich
- `menswear-20261117-2-de` Einstecktuch: Drei Falttechniken
- `menswear-20261119-2-de` Oxford oder Derby? Die Schnürung entscheidet
- `menswear-20261119-3-de` Das X am Rückenschlitz gehört weg
- `menswear-20261121-1-de` Anzugpflege in vier Schritten
- `menswear-20261121-2-de` Das Etikett am Sakkoärmel kommt ab
- `menswear-20261122-1-de` Die Ticket Pocket
- `menswear-20261123-1-de` Einstecktuch und Krawatte: nicht im Partnerlook
- `menswear-20261123-2-de` Überlappende Ärmelknöpfe
- `menswear-20261124-3-de` Handstich am Revers: Zeichen oder Zierde?
- `menswear-20261125-2-de` Gürtel folgt dem Schuh
- `menswear-20261126-1-de` Schulter: gepolstert oder natürlich
- `menswear-20261126-2-de` Brogue: Lochmuster voll, halb, viertel
- `menswear-20261126-3-de` Kurzarmhemd unterm Sakko: Wo die Manschette fehlt
- `menswear-20261128-1-de` Schuhspanner aus Zedernholz: wozu?
- `menswear-20261129-1-de` Knöpfe aus Horn, Steinnuss oder Kunststoff
- `menswear-20261129-2-de` Hemdärmel: die richtige Länge
- `menswear-20261129-3-de` Die Fliege selbst binden
- `menswear-20261201-2-de` Krawattenstoffe nach Anlass: Seide, Strick, Wolle
- `menswear-20261201-3-de` Seitenversteller statt Gürtelschlaufen
- `menswear-20261202-1-de` Brustumfang richtig messen
- `menswear-20261203-2-de` Den Anzug im Koffer packen
- `menswear-20261203-3-de` Der Mantel muss das Sakko bedecken
- `menswear-20261204-2-de` Schuhpassform: Länge und Weite
- `menswear-20261204-3-de` Das Mailänder Knopfloch
- `menswear-20261205-2-de` Die Uhr unter der Manschette (Status `idea`)
- `menswear-20261206-2-de` Hosenbund: sitzt auch ohne Gürtel
- `menswear-20261206-3-de` Hemdfarbe zum Anzug: Weiß und Hellblau
