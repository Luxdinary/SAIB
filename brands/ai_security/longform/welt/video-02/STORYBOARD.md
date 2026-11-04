# Video 02: animierte Erklärwelt, Storyboard

Stand 30. Oktober 2026, abends. Für Stefan. Grundlage: Skript `SKRIPTE/02-security-questionnaire.de.md` und `.en.md` (freigegeben 29. Oktober, unverändert), Vorlage `ANIMATION/VORLAGE-PARALLEL.md`, Gestaltungsauftrag vom 30. Oktober, Muster `probe-01` (Note 1) und `video-01`.

## Grundlage

- Titel: „Ihr Kunde schickt einen Sicherheitsfragebogen. So antworten Sie ehrlich.“ (EN „Your customer sent a security questionnaire. How to answer honestly.“)
- Tonspur: Flash-Stimme Charon vom 31. Oktober 2026, zwei Dateien je Sprache (`stimme\01-03-<sprache>.wav`, `04-07-<sprache>.wav`).
- Zeitbindung: jede Bildaktion hängt an einem gesprochenen Wort (`cue`). Die Spalte „Anker“ nennt das Wort; die Sekunden stehen in Abschnitt „Zeiten“, sobald die Wortzeiten vorliegen.
- Marker und Quellen: `marken.js` aus `marken.py` (14 markierte Absätze). Absätze mit Quelle, aber ohne Marker (11 Stück, meist das Handbuch) bekommen nur die Quellenleiste ohne Kapsel; die Daten dafür erzeugt `video-02/quellen.py` wörtlich aus den Skripten.
- Freies Angebot in der Mitte (Abschnitt 3a): Handbuch des Sicherheitsnachweis-Toolkits, Kapsel rechts oben am Anker „Das Handbuch unseres Toolkits sagt es so“ / „handbook of our toolkit puts it this way“, etwa 7 Sekunden. Pfad DE `/de/toolkits/sicherheitsnachweis/handbuch`, EN `/toolkits/security-evidence/handbook`.

## Wiederkehrende Motive

- **Der Fragebogen:** ein helles Blatt mit Kopf „FRAGEBOGEN · INFORMATIONSSICHERHEIT“, Themenzeilen mit Symbol und einem Feld „Termin“. Er wandert durch das ganze Video: kommt an, wird falsch beantwortet, wird richtig beantwortet, wird zur Selbstauskunft.
- **Die vier Antworten:** vier Kapseln mit Form und Wort. Vorhanden: grüne Lampe mit Haken (erreichter Zustand). Teilweise: bernsteinfarbener Halbkreis. Noch nicht, mit Termin: bernsteinfarben gestrichelt mit Kalender. Nicht anwendbar, mit Grund: grau mit Stift. Ein „Ja“ ohne Stand ist ein graues Kästchen.
- **Kunde und Lieferant:** links ein großes Gebäude (der größere Kunde, erfunden, ohne Namen), rechts der kleine Beispielbetrieb Muster Elektrotechnik e.U. mit seiner festen Besetzung. Die Büroleitung ist „Büro A“ (kurzes Haar, graues Hemd). Die externe IT-Betreuung ist eine eigene Figur außerhalb des Hauses (Jacke, Laptop), die auf einer Baustelle steht.
- **Der Weg der fünf Schritte:** wie in Video 01 eine Prozesslandschaft, hier mit fünf Stationen: Verstehen, Vier Antworten, Größe, Nachweise, Senden. Jede Station öffnet sich als Kreis zu ihrer Szene, der Rückweg schrumpft in die Station.
- **Der Nachweisordner:** ein Ordner, in den datierte Belege fliegen; was fehlt, bleibt als gestrichelte Karte mit Kalender stehen.

## Storyboard

### 1 Einstieg (Absätze 0 bis 2)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| Satzbeginn | Ihr Kunde schickt einen Sicherheitsfragebogen. | Ein Fragebogen kommt an | Nacht, der Beispielbetrieb in der Totale; von links fliegt ein Umschlag auf einem Bogen zum Büro, landet auf dem Schreibtisch von Büro A und faltet sich zum Fragebogen auf | Fragebogen über dem Schreibtisch | „Fragebogen“ |
| „Ein Termin“ | Ein Termin, keine IT-Abteilung. | Frist und fehlende Fachabteilung | Am Fragebogen heftet sich eine Kalenderkapsel „Termin“ an; bei „keine IT-Abteilung“ erscheint über dem Dach ein leerer gestrichelter Raum „IT-Abteilung“, der leer bleibt | Termin am Blatt, leerer Raum | „Termin“, „IT-Abteilung: keine“ |
| „Hier ist Scutoria“ | Hier ist Scutoria … synthetisch … Skript … geprüft … Quelle am Bildschirm … keine Rechtsberatung | Transparenz | Wie Video 01: Zeichen zeichnet sich, Stimmwelle mit „Synthetische Stimme“, Skriptblatt mit KI-Tool und Haken je Zeile, Aussageblatt „Art. 32 DSGVO“ mit Quellenstreifen; zuletzt „Quellenbasiert“ und „Keine Rechtsberatung“ | Zwei Grundsätze | „Synthetische Stimme“, „Satz für Satz geprüft“, Quelle |
| „Warum er kommt“ | Warum er kommt, warum „noch nicht, mit Termin“ vollständig ist, und wie eine Selbstauskunft aussieht. | Vorschau auf drei Fragen | Drei Felder entstehen nacheinander: Kunde schickt Blatt an Lieferant; Kapsel „Noch nicht, mit Termin“ mit Haken „vollständig“; ein kleines Blatt „Selbstauskunft“ | Drei Felder nebeneinander | Kopf „In diesem Video“ |

Unten links ab Sekunde 0: „Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung“.

### 2 Was meistens schiefgeht (Absätze 3 bis 6)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „Die Lage ist“ | Ein größerer Kunde schickt ein Dokument mit Fragen … MFA, Sicherung, Updates, Vorfälle, Schulung, Dienstleister | Woraus der Fragebogen besteht | Großes Kundengebäude links, kleiner Betrieb rechts; das Blatt fliegt vom Kunden zum Betrieb; bei jedem Thema springt eine Zeile mit Symbol auf | Sechs Themen am Blatt | sechs Schlagworte |
| „einen Termin“ | Es gibt einen Termin … keine IT-Abteilung | Druck und Lücke | Kalenderkapsel heftet sich an; im Betrieb bleibt der gestrichelte Raum „IT-Abteilung“ leer | wie oben | „Termin“ |
| „Die Büroleitung“ | Die Büroleitung öffnet es, die IT-Betreuung ist auf einer Baustelle, die Fragen verwenden fremde Wörter | Wer im Betrieb davorsitzt | Kamera ins Büro: Büro A öffnet das Blatt am Bildschirm; Schwenk nach rechts aus dem Haus zur Baustelle, dort die IT-Betreuung mit Laptop; zurück: Fachwörter aus dem Blatt schweben über Büro A, mit Fragezeichen | Büro A mit fremden Wörtern | „Büroleitung“, „IT-Betreuung · Baustelle“ |
| „Zwei Dinge“ | Erstens: an die IT-Betreuung … Rest leer. Zweitens: überall „Ja“. | Zwei typische Fehler | Zwei Blätter nebeneinander. Links „1“: technische Zeilen füllen sich blau, „Verantwortlich“, „Notfallplan“, „Einweisung“ bleiben gestrichelt leer. Rechts „2“: eine Hand kreuzt in schneller Folge überall „Ja“ an | Zwei unbrauchbare Fragebögen | „Rest leer“, „überall Ja“ |
| „Das Handbuch unseres Toolkits“ | Ein ehrliches „noch nicht“ … „Ja“, das bei der ersten Nachfrage zerfällt … Protokoll Wiederherstellungstest | Warum „Ja“ ohne Beleg schadet | Ruhige Zitatszene: links Kapsel „noch nicht, mit Termin“, rechts „Ja“. Eine Nachfrage-Sprechblase kommt; das „Ja“ zerfällt in Stücke. Dann fordert der Kunde „Protokoll Wiederherstellungstest“, das Fach bleibt leer, und alle anderen „Ja“ des Formulars bekommen ein Fragezeichen | Formular voller fraglicher „Ja“ | „Nachfrage“, „Protokoll?“ |
| „Vier Arten von Anfragen“ | Fragebogen, Vertrag, Versicherer, Gütesiegel … dieses Video: die erste und der Vertrag | Einordnen | Vier Gegenstände kommen am Betrieb an; bei „Dieses Video handelt“ bleiben Fragebogen und Vertrag hell, die anderen zwei treten zurück | Zwei von vier hervorgehoben | vier Schlagworte |

Quellenleiste ohne Marker bei den Handbuch-Absätzen; freies Angebot rechts oben ab „Das Handbuch unseres Toolkits sagt es so“.

### 3 Fünf Schritte zu einer ehrlichen Antwort (Absätze 7 bis 15)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „in fünf Schritten“ | Was der Betrieb tut … ohne Toolkit; unseres macht sie nur schneller | Überblick | Der Weg zeichnet sich, fünf Stationen erscheinen; eine Toolkit-Kapsel legt sich gestrichelt daneben, dann läuft ein Licht schneller über den Weg | Weg mit fünf Stationen | Stationsnamen |
| „Schritt eins“ (Fakt) | NIS-2-Kunde, zehn Bereiche, Lieferkette, unmittelbare Anbieter, Praxis berücksichtigen | Wer fragt und warum | Station 1 öffnet sich: Kundengebäude mit zehn Kacheln a bis j im Bogen; bei „Sicherheit der Lieferkette“ leuchtet d, eine Linie läuft zu den Anbietern, der Beispielbetrieb ist einer davon; bei „berücksichtigen“ wandert eine Lupe zu den Anbietern | Kunde blickt auf Lieferanten | „10 Bereiche“, „d · Lieferkette“ |
| „Das ist der Fragebogen“ (Auslegung) | billigster Weg für hunderte Lieferanten; Fragen folgen den zehn Bereichen; bindet den Kunden, nicht Sie; Vertrag und DSGVO binden Sie | Woher der Fragebogen kommt, wen was bindet | Die Lupe wird zum Fragebogen, Kopien fächern zu vielen Lieferanten; Zeilen des Blatts verbinden sich mit den Kacheln; ein Ring „bindet“ legt sich um den Kunden; beim Lieferanten docken Vertrag und „DSGVO“ an | Bindungen klar getrennt | „bindet den Kunden“, „Vertrag“, „DSGVO“ |
| „der DSGVO verpflichtet“ (Fakt) | Art. 32: rasch wiederherstellen, regelmäßige Überprüfung | Was davon jeden trifft | Blatt „Art. 32 DSGVO“ legt sich vor den Lieferanten; zwei Zeilen leuchten auf: Wiederherstellen (Kreislauf), Überprüfen (Kalender) | Zwei Pflichten markiert | „wiederherstellen“, „überprüfen“ |
| „Schritt zwei“ | vier Antworten, nichts anderes; Beispielantwort mit Lücke, Termin, Person | Die vier Antworten | Rückweg in den Weg, Station 2 öffnet sich: eine Fragekarte, darunter erscheinen die vier Kapseln je auf ihrem Wort; „Ja“ und ein leeres Feld werden durchgestrichen und fallen weg; die Beispielantwort tippt sich, drei Etiketten heften sich an | Vollständige Antwort | vier Antworten, „Lücke“, „Termin“, „Person“ |
| „Schritt drei“ (Fakt) | Größe und Risikoexposition; begründen, warum nicht angemessen | Verhältnismäßigkeit | Station 3: zwei Gebäude unterschiedlicher Größe, daneben je ein Stapel Maßnahmen, der mit der Größe wächst; ein Blatt „Begründung“ mit Stift | Maßnahmen nach Größe | „Größe“, „Risiko“, „Begründung“ |
| „Die Verhältnismäßigkeit“ (Auslegung) | für den Kunden geschrieben; mehr verlangen ist erlaubt; an Ihrer Größe messen, im ersten Absatz; kein SOC, keine Penetrationstests, keine Zertifizierung | Was Sie daraus machen | Der Kunde schiebt einen höheren Stapel zum Lieferanten; das Antwortschreiben erscheint, sein erster Absatz leuchtet; drei Kapseln „SOC“, „Penetrationstest“, „Zertifizierung“ werden durchgestrichen | Erster Absatz markiert | drei gestrichene Begriffe |
| „Schritt vier“ | Prüfung vor Ort selten; je Antwort ein datiertes Dokument; neun Belege; Fehlendes mit Termin | Nachweise | Station 4: Prüferin mit Klemmbrett gestrichelt und klein (selten); ein Nachweisordner öffnet sich; neun Belegkarten entstehen je auf ihrem Wort und fliegen hinein; eine Karte bleibt gestrichelt mit Kalender | Ordner mit acht Belegen und einem Termin | neun Belegnamen |
| „Schritt fünf“ | als Selbstauskunft senden: Stand und Datum, unterschrieben; Anlagen nummeriert; Antwortschreiben mit Lücken und Zuordnung; datierte Fassung einfrieren | Senden und festhalten | Station 5: Selbstauskunft mit Statusfeldern, Unterschrift zeichnet sich; Anlagen 1 bis 3 stecken sich an; Antwortschreiben mit Linien von Kundenfragen zu Abschnitten; eine Kopie fliegt mit Datum in den Nachweisordner, ein Kalender „Überprüfung“ bleibt | Paket beim Kunden, Kopie im Ordner | „Selbstauskunft“, „Anlage 1“, „Überprüfung“ |

### 4 Die Quellen hinter „noch nicht, mit Termin“ (Absätze 16 bis 25)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „Jetzt die Quellen“ | Kernaussage | Was belegt wird | Kapsel „Noch nicht, mit Termin“ in der Mitte, daneben „vollständige Antwort“ | Kernaussage | wie gesprochen |
| „Fakt. Die NIS“ | Korrekturmaßnahmen unverzüglich; Prüfbericht mit Mängeln und Maßnahmenplan | Das Gesetz kennt die Lücke | Eine Einrichtung findet eine Lücke (gestrichelter Kreis), daraus gehen Pfeile zu „Korrekturmaßnahmen“; Österreich: zwei Blätter „Prüfbericht · Mängel“ und „Maßnahmenplan“ | Lücke mit Plan | „Korrekturmaßnahmen“, „Maßnahmenplan“ |
| „Fakt. Österreich sagt“ | strafbar nur, wenn nicht nur aus der Selbstdeklaration bekannt; wissentlich falsche Angaben eigens strafbar | Ehrlichkeit wird geschützt | Zwei Bahnen: „Lücke selbst gemeldet“ läuft durch, „wissentlich falsch“ endet am roten Paragrafen | Zwei Ausgänge | „selbst gemeldet“, „wissentlich falsch“ |
| „Das Gesetz behandelt“ (Auslegung) | Lücke mit Plan ist Normalzustand; der Lieferant liefert, was der Kunde selbst erzeugen muss | Begründung der vier Antworten | Die Beispielantwort des Lieferanten fliegt in den Maßnahmenplan des Kunden und passt dort in eine Zeile | Passende Zeile | „Normalzustand“ |
| „Fakt, für Österreich“ | Selbstdeklaration binnen zwölf Monaten, insbesondere Lieferketten | Frist beim Kunden | Zeitleiste: Registrierungspflicht, zwölf Monate, Selbstdeklaration an die Behörde; Zeile „Lieferketten“ hervorgehoben | Frist sichtbar | „12 Monate“ |
| „Für einen österreichischen“ (Auslegung) | Ihr Fragebogen ist Rohmaterial; 2026 fragen, 2027 senden; keine Eingabe bei der Behörde | Warum der Ton so ist | Antworten des Lieferanten fließen in die Selbstdeklaration des Kunden, Jahreszahlen 2026 und 2027; eine gestrichelte Linie vom Lieferanten zur Behörde wird gekappt | Weg nur über den Kunden | „2026“, „2027“ |
| „Fakt, zum Vertrag“ | acht Vertragsinhalte | Was im Vertrag folgt | Ein Vertragsblatt, acht Klauselzeilen erscheinen je auf ihrem Wort mit Symbol; zuletzt die Zahl 8 | Vertrag mit acht Zeilen | acht Schlagworte |
| „In Österreich erklärt“ (Fakt) | NISV: Anhang für jede wesentliche und wichtige Einrichtung | Geltung in Österreich | Kapsel „AT · NISV 2026“ legt sich an den Vertrag, Gebäude „wesentlich“ und „wichtig“ | Geltung markiert | „AT“ |
| „Diese acht Inhalte“ (Auslegung) | Muster der Klauseln; deutscher Kunde nicht gebunden, aber Prüfer lesen denselben Text | Was Sie erwartet | Der Vertrag vervielfacht sich zu vielen Verträgen; ein Kunde „DE“ steht gestrichelt außerhalb, eine Lupe liest dennoch denselben Text | Muster erkennbar | „DE · nicht gebunden“ |
| „Und was offen ist“ (Lücke) | kein amtlicher Muster-Fragebogen gefunden; Gericht zu „unverzüglich“ nicht gesucht | Offenes bleibt offen | Lupe über Regal, das Fach „amtliches Muster“ bleibt leer im gestrichelten roten Kreis; Hammer gestrichelt „nicht gesucht“; beide wandern ins Handbuch Abschnitt 6 | Zwei offene Zeilen | „6.6“, „6.22“ |

### 5 Der Beispielbetrieb und seine Dokumente (Absätze 26 bis 31)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „Der Beispielbetrieb“ | erfunden, 10 bis 49 Beschäftigte, Österreich; ein Kunde hat einen Fragebogen geschickt | Der Fall | Der Betrieb in der Totale, Stempel „erfunden“, Kapsel „10 bis 49 · AT“; der Fragebogen landet im Büro | Betrieb mit Fragebogen | „Muster Elektrotechnik e.U. · erfunden“ |
| „Seine Antworten zeigen“ | MFA E-Mail vorhanden; Cloud-Konsole Termin; Sicherung teilweise; Wiederherstellungstest Termin; Notfallplan keiner; alter Werkstattrechner | Ein ehrliches Mischbild | Kamera fährt durch das Haus; an jedem Ort springt die Antwort als Kapsel auf (Bildschirm Büro, Konsole, Sicherungsplatte, Werkstatt) und reiht sich in eine Liste rechts | Liste mit sechs Ständen | sechs Antworten |
| „Am Bildschirm sehen Sie“ | Selbstauskunft: neun Abschnitte, Übersichtstabelle, Stand und Datum, Unterschriftszeile; nichts sagt „alles in Ordnung“ | Wie die Selbstauskunft aussieht | Blatt D1 mit neun Reitern, Übersichtstabelle füllt sich mit den Ständen, Datumsspalte, Unterschriftszeile; eine Kapsel „alles in Ordnung“ wird durchgestrichen | Selbstauskunft | „D1 Selbstauskunft“ |
| „Das Antwortschreiben“ | kleiner Betrieb, Lücken mit Terminen | Ton des Schreibens | Blatt D5, erster Absatz leuchtet, zwei Lücken mit Terminen | Schreiben | „D5 Antwortschreiben“ |
| „Darunter die Abgleichstabelle“ | 18 Fragen und 10 Bereiche, je auf einen Abschnitt verwiesen | Zuordnung | Links 18 Fragepunkte, rechts zehn Bereiche a bis j, Linien laufen zu den Abschnitten der Selbstauskunft | Zuordnung sichtbar | „18 Fragen“, „10 Bereiche“ |
| „Die Nachweisliste“ | nur Vorhandenes bekommt eine Anlagennummer; Fehlendes behält Fragennummer und Termin; datiertes Bild, kein Versprechen | Nichts wird versteckt | Blatt D4: Zeile mit „Anlage 1“ (MFA E-Mail), Zeile mit Fragennummer und Termin (Wiederherstellungstest); das Paket geht mit Datumsstempel zum Kunden | Datiertes Bild | „Anlage 1“, „Termin“ |

### 6 Was das Toolkit nicht ist (Absätze 32 bis 35)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „Was dieses Toolkit“ | keine Rechtsberatung, kein Audit, kein Zertifikat; zeigt Datum, bis wann, wer | Grenzen | Drei Kapseln werden durchgestrichen; „sicher“ und „erfüllt“ erscheinen gar nicht erst, nur leere gestrichelte Rahmen; dann drei Felder: Kalender, Uhr, Person | Was die Dokumente zeigen | „an einem Datum“, „bis wann“, „wer“ |
| „Jede Aussage“ | vier Marker mit Bedeutung | Die Marker | Vier Kacheln, jede Form zeichnet sich auf ihrem Wort | Vier Marker | Fakt, Auslegung, Unsicher, Lücke |
| „Jede Unsicherheit“ | 23 Punkte, 13 offen | Offenheit messbar | 23 Punkte erscheinen im Raster, 13 bleiben gestrichelt offen | Raster | „23 Punkte · 13 offen“ |
| „Bekommen Sie damit“ | kein Zertifikat; Selbstauskunft mit Nachweisen; Ihr Betrieb entscheidet | Wer entscheidet | Zertifikat-Symbol wird gestrichen; Selbstauskunft mit Ordner; die Inhaberin setzt das Datum | Entscheidung beim Betrieb | „Nein“ |

### 7 Freies Memo, Handbuch, Toolkit (Absätze 36 bis 39)

| Anker | Gesprochen (gekürzt) | Erklärziel | Bildhandlung | Ergebnisbild | Text im Bild |
|---|---|---|---|---|---|
| „Wenn Sie anfangen wollen“ | Memo NIS2, fünf Fragen, datiertes Memo, PDF per E-Mail, frei | Freier Einstieg | Memo-Blatt mit fünf Fragezeilen (Sektor, Größe, Sonderfälle), Datum, ein Umschlag mit dem PDF | Memo | „frei auf scutoria.com“, Pfad |
| „Das Handbuch des“ | Handbuch vor dem Kauf lesbar; 47 Fragen; sieben Dokumente; Preis | Was das Toolkit liefert | Handbuch, dann Generator mit „47 Fragen“, daraus fächern sieben Blätter je auf ihrem Namen; Preiszeile ruhig in Mono | Sieben Dokumente | Dokumentnamen, Preis |
| „Die Stimme war“ | synthetisch, Quellen, keine Rechtsberatung | Abschluss | Drei Kapseln wie im Einstieg | | |
| „Als Nächstes“ | Rundgang durch beide Toolkits | Ausblick | Karte „Video 03“, dann 20 Sekunden ruhiges Endbild mit kleinem Zeichen und zwei freien Flächen für die Endelemente | Endbild | „Als Nächstes“ |

## Abweichungen und offene Punkte

- **Sprechtext:** unverändert.
- **Seitenzahl des Handbuchs:** das deutsche Skript sagt „vierzig Seiten“, das englische „thirty-seven pages“. Beide sind freigegeben und bleiben; das Bild zeigt keine Seitenzahl. Bitte prüfen, welche Zahl stimmt.
- **Beispielwerte im Bild:** Kundengebäude ohne Namen, Datumsangaben in den Musterblättern als Beispiel, Adressen nur mit `.example`. Der Beispielbetrieb ist laut Skript erfunden und trägt den Stempel „erfunden“.
- **Notfallplan:** Das Skript sagt nur „keiner“. Das Bild zeigt „keiner“ gestrichelt, ohne eine der vier Antworten zu unterstellen.
- **Preis:** wird im Bild nur als ruhige Mono-Zeile gezeigt, so wie gesprochen. Kein Preisblock der Website.
- **Ton:** keine Geräusche, keine Musik.

## Bausteine, die in `lib/` fehlen (stehen in `video-02/bausteine.js`)

Für den Chat von Video 01 zur Übernahme in die Bibliothek; `lib/` selbst ist unverändert.

- **Zahlwörter für Wortanker:** `ZAHLWORT` kennt nur einfache Zahlen. Skript 02 braucht dreizehn, achtzehn, einundzwanzig, dreiundzwanzig, zweiunddreißig, vierzig, siebenundvierzig, neunundvierzig (EN entsprechend) und „NIS-zwei“. `bausteine.js` ergänzt sie zur Laufzeit und normiert die Wortzeiten danach neu.
- **Quellenleiste ohne Marker:** `leiste()` und `quelle()`. `marken.py` gibt nur markierte Absätze aus; elf Absätze in 02 haben eine Quelle ohne Marker (meist das Handbuch). Daten dafür erzeugt `video-02/quellen.py` aus den Skripten. Vorschlag: `marken.py` gibt diese Absätze künftig mit `art: null` aus.
- **Freies Angebot (Abschnitt 3a):** kommt inzwischen aus der Bibliothek (`freiesAngebot()` in `welt.js`), wie in Video 01.
- **Die vier Antworten:** `ANTWORT`, `antwort()`; Vorhanden grün mit Haken, Teilweise halb gefülltes Rechteck, Noch nicht mit Termin bernsteinfarben gestrichelt mit Kalender, Nicht anwendbar grau mit Strich.
- **Fragebogen, Kunde, Lieferant, Behörde, IT-Betreuung, Baustelle, Belegkarte, Nachweisordner, Weg mit fünf Stationen** (`fragebogen`, `jaFeld`, `kundeHaus`, `kleinHaus`, `behoerde`, `itBetreuung`, `baustelle`, `belegKarte`, `nachweisOrdner`, `bauWeg5`, `weg5Zeichnen`, `streich`, `terminPille`).

## Wortanker, die im Englischen eine andere Reihenfolge haben

An drei Stellen steht das Ankerwort im Englischen vor dem deutschen Gegenstück („falls apart“ vor „first follow-up“, „into account“ vor „cybersecurity practices“, „structured self-declaration“ vor „twelve months“). Diese Anker werden mit `halten` gesucht und die Bildaktion an das frühere der beiden Wörter gebunden.

## Ton und Zeiten

- **Vertonung:** Flash-Stimme Charon am 30. Oktober 2026, 21:27 bis 21:38 Wien, bezahlt (Freigabe Stefan: „Ja, jetzt vertonen“). Vier Anfragen für 02: DE 10 308 und 12 544 Token, EN 9 695 und 11 650 Token (Ausgabe von `vertonen-tag.ps1`). Dauer DE 793,6 s, EN 753,0 s.
- **Stimmlage:** Zwischen den beiden Anfragen einer Sprache sprang die Tonhöhe um etwa 1,4 Halbtöne (`stimmlage.py`: DE 106,7 und 115,4 Hz, EN 114,8 und 106,0 Hz). Angeglichen mit `ton-fassung.py` und `video-02/ton-schnitt.json` (ganze Spur, keine Schnitte), Dauer unverändert. Danach je Minute DE 109 bis 117 Hz (vorher 100 bis 122), EN 105 bis 115 Hz nach zwei Durchgängen (vorher 98 bis 123). Gerendert wird mit `ton-de.angeglichen.wav` und `ton-en.angeglichen2.wav`; die Ausgangsspuren bleiben daneben liegen.
- **Wortzeiten:** `woerter.py` (Whisper large-v3, Pausenerkennung), dann `ausrichten.py` auf den Sprechtext: DE 1 768 von 1 790 Skriptwörtern sicher zugeordnet (98,8 %), EN 1 961 von 1 992 (98,4 %). Alle Wortanker gefunden.

| Abschnitt | Akt | Beginn DE (s) | Beginn EN (s) |
|---|---|---|---|
| 1 Einstieg | einstieg | 0 | 0 |
| 2 Was meistens schiefgeht | problem | 30,4 | 30,7 |
| 3 Fünf Schritte, Schritt 1 und 2 | loesung-1 | 123,4 | 116,2 |
| 3 Fünf Schritte, Schritt 3 bis 5 | loesung-2 | 227,7 | 217,9 |
| 4 Die Quellen | beleg | 358,1 | 343,0 |
| 5 Der Beispielbetrieb | beispiel | 554,8 | 525,1 |
| 6 Was das Toolkit nicht ist | nicht | 655,4 | 620,2 |
| 7 Verweis | verweis | 724,5 | 687,0 |
| Endbild (20 s) | verweis | 794,1 | 753,6 |
| Ende | | 814,1 | 773,6 |

Mit der echten Stimme dauert der Auftakt bis „Hier ist Scutoria“ nur etwa 5 Sekunden. Die erste Einstellung ist deshalb eine Totale mit leichter Drift statt einer Fahrt ins Büro und zurück.

## Ergebnis (30. Oktober 2026)

| Fassung | Datei unter `C:\Users\Stefa\Videos\scutoria\02-security-questionnaire\animation\` | Dauer | Größe | Rechenzeit |
|---|---|---|---|---|
| Deutsch | `02-security-questionnaire.de.mp4` (dazu `.de.klein.mp4`, 720p, 22,5 MB, zum Ansehen) | 13:34 | 64,6 MB | 15 min, `--parallel 3` |
| Englisch | `02-security-questionnaire.en.mp4` | 12:54 | 62,1 MB | 10 min, `--parallel 6` |

Deutsch lief mit `--parallel 3` statt 6, weil gleichzeitig die Fassung 2 von Video 01 renderte und der Arbeitsspeicher sonst nicht gereicht hätte (ein erster Versuch brach mit „malloc failed“ ab). Geprüft: Bilder aus beiden MP4, Tonpegel (Mittel −20,8 und −20,6 dB, Spitze −0,4 und −0,5 dB), Angebotskapsel in beiden Sprachen am Anker. Nichts veröffentlicht.

## Fassung 2 (1. November 2026)

Stefans Entscheidung („Ja, für alle“, wie Video 01): Der Einstieg beginnt mit einer Frage, der gesprochene Block „Hier ist Scutoria … keine Rechtsberatung“ steht am Schluss und ersetzt dort den kurzen Schlusssatz „Die Stimme war synthetisch …“. Der Bildschirmtext „Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung“ steht weiter ab Sekunde 0, „SYNTHETISCHE STIMME“ oben rechts das ganze Video. Den neuen Wortlaut hat Stefan am 1. November 2026 freigegeben („Ja, frei“).

- **Skript:** erster Satz „Hat Ihr Kunde einen Sicherheitsfragebogen geschickt?“ (EN „Has your customer sent a security questionnaire?“), der Hinweisblock steht vor „Als Nächstes“; Kopfzeile ergänzt, Kapitelzeiten neu gemessen. Sonst kein gesprochenes Wort geändert.
- **Ton:** nur Abschnitt 1 neu vertont (Flash, Charon, je Sprache eine Anfrage, DE 420 und EN 453 Token, `C:\Users\Stefa\Videos\scutoria\fassung-2\02-security-questionnaire\stimme\`). Die neue Spur setzt `ton-fassung.py` nach `video-02/schnitt-fassung2.json` aus dem neuen Einstieg und der unbearbeiteten Flash-Spur der ersten Fassung zusammen und gleicht die Stimmlage in einem Durchgang an: Spanne über alle Minuten DE 1,0, EN 0,8 Halbtöne.
- **Mitgesprochene Pausenmarken:** Die Flash-Stimme hat im Englischen die Regieanweisung `<short pause>` fünfmal als „Short pause“ und einmal „Long pause“ mitgesprochen (Fassung 1, bei 29, 114, 523, 618 und 683 s; dazu einmal im neuen Einstieg). Fassung 2 schneidet sie heraus und setzt 0,8 s Stille ein. Im Deutschen keine solche Stelle; geprüft an Wortliste und Pegel aller Lücken über 1,2 s (die einzige verdächtige Stelle, 553,9 s, ist ein Atemzug bei −41 dB).
- **Bild:** `teil-1.js` ohne Scutoria-Bühne (Frage, dann Vorschau), `teil-7.js` mit `offenlegungsBuehne()` aus `lib/dokumente.js` an Stelle des alten Schlusssatzes. Manrope setzt „(c)“ als Ligatur „©“; im englischen „Art. 32(1)(c)“ steht deshalb ein unsichtbarer Trenner (in Fassung 1 stand dort fälschlich „©“).
- **Wortzeiten:** `ausrichten.py` auf den Sprechtext der Fassung 2: DE 1 754 von 1 776 Skriptwörtern sicher zugeordnet (98,8 %), EN 1 946 von 1 977 (98,4 %); alle Wortanker gefunden.

| Abschnitt | Beginn DE (s) | Beginn EN (s) |
|---|---|---|
| 1 Einstieg | 0 | 0 |
| 2 Was meistens schiefgeht | 15,5 | 14,8 |
| 3 Fünf Schritte | 108,5 | 99,8 |
| 4 Die Quellen | 343,2 | 326,6 |
| 5 Der Beispielbetrieb | 540,0 | 508,1 |
| 6 Was das Toolkit nicht ist | 640,5 | 602,5 |
| 7 Verweis, Hinweisblock, Ausblick | 709,6 | 666,9 |
| Endbild (20 s) | 786,7 | 743,8 |
| Ende | 806,7 | 763,8 |

**Ergebnis Fassung 2 (1. November 2026):** `02-security-questionnaire.fassung2.de.mp4` (13:27, 64,3 MB, dazu `.fassung2.de.klein.mp4`, 720p, 22,3 MB, an Stefan geschickt) und `02-security-questionnaire.fassung2.en.mp4` (12:44, 61,2 MB), beide unter `C:\Users\Stefa\Videos\scutoria\02-security-questionnaire\animation\`, gerendert mit `--parallel 6` (9 und 7 Minuten). Tonpegel Mittel −20,8 und −20,5 dB, Spitze −0,5 und −0,4 dB. Die Dateien der Fassung 1 bleiben daneben liegen. Nichts veröffentlicht.
