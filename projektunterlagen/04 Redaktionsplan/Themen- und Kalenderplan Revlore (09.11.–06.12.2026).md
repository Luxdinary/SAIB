# Themen- und Kalenderplan Revlore (09.11.–06.12.2026)

**Freigegeben von Stefan am 01.11.2026.** Themen im Status `planned` gehen in die Produktion; Themen im Status `idea` erst nach Quellenprüfung; Risiko „high“ vor jeder Veröffentlichung einzeln an Stefan.

Stand: 01.11.2026 (Wien). Marke Revlore (`engines`), Vorlage 1.0. Grundlage: `Planungsrahmen Themen- und Kalenderplan.md` und `C:\Automation\faceless-network\prompts\calendar_planner.md`. Maschinenlesbar: `C:\Automation\faceless-network\data\calendars\engines_2026-11.json` (168 Zeilen, je Thema eine deutsche und eine englische Zeile mit demselben Ansatz). Prüfung `fn.cli calendar check`: ohne Befund.

## Überblick

- 28 Tage, 84 Themen, 168 Posts. Je Tag 3 Themen, Deutsch 12:00 / 14:00 / 18:00, Englisch 15:00 / 20:00 / 23:00 (Wiener Zeit).
- Status: 167 Zeilen geplant, 1 produziert (Testvideo „Zwei Umdrehungen“, deutsch), 0 Idee.
- Jedes Thema hat mindestens zwei Primärquellen, die am 01.11.2026 geöffnet wurden (insgesamt 91 verschiedene Quellen: MIT 2.61 Vorlesungsfolien, NASA Glenn, US-Energieministerium und EPA, Sandia, ORNL, Bosch, Schaeffler, Garrett, BorgWarner, NGK, MAHLE, Chevron, Toyota, Honda, Mazda, Volkswagen, Mercedes-AMG F1, Patentschriften über DEPATISnet und Google Patents, Deutsches Museum, Smithsonian, Science Museum Group, Accelleron, National Inventors Hall of Fame). Die URLs und die belegenden Folien oder Absätze stehen je Zeile im Kalender (`source_urls`, `notes`).
- Risiko: alle Themen „medium“ (technische Aussagen) oder „low“ (Geschichte, Zündkerzen-Mythos). Kein Thema „high“.
- Formate je Woche gemischt: Erklärung 50, Geschichte 12, Vergleich 9, Mythos 8, Liste 3, Anleitung 2.

## Themenreihen

| Reihe | Wochenrhythmus | Ziel | Format | Anzahl |
|---|---|---|---|---|
| Mythos-Check | Montag und Samstag, Thema 1 | Eine verbreitete Annahme am Schnittmodell oder mit einer Zahl prüfen. Hook: „Klingt richtig, stimmt aber nicht.“ | Mythos | 8 |
| Nachgerechnet | Dienstag und Donnerstag, Thema 1 | Eine Zahl aus der Quelle im Bild nachrechnen (Drehzahlmesser, Rechenzeilen wie im Testvideo). Rechenbeispiele als Beispielwert kennzeichnen. | Erklärung, Liste | 8 |
| Gegenübergestellt | Mittwoch und Freitag Thema 1, dazu einmal Samstag Thema 3 (05.12.) | Zwei Lösungen nebeneinander im geteilten Bild: was jede besser kann und was sie kostet. Keine Kaufempfehlung. | Vergleich | 9 |
| Im Schnitt | täglich Thema 2, an den übrigen Tagen Thema 3 | Ein Bauteil oder Vorgang im laufenden Schnittmodell, Kern der Marke. | Erklärung, Anleitung, Liste | 47 |
| Motorgeschichte | Sonntag Thema 1, dazu Dienstag und Freitag Thema 3 | Erfindungen und Patente mit Datum und Primärquelle (Patentschrift, Museum, Firmenarchiv). | Geschichte | 12 |

Wochenschwerpunkte: Woche 1 Grundlagen (Takte, Zündung, Klopfen), Woche 2 Diesel und Abgas, Woche 3 Aufladung und Ventiltrieb, Woche 4 Wirkungsgrad, Hybrid und Kraftstoffe.

## Kalender

Spalten: Datum, Uhrzeit Deutsch / Englisch, Reihe, Titel Deutsch, Titel Englisch, Format, Risiko, Anzahl geöffneter Quellen, Status.

| Datum | Uhrzeit DE / EN | Reihe | Titel DE | Titel EN | Format | Risiko | Quellen | Status |
|---|---|---|---|---|---|---|---|---|
| Mo 09.11. | 12:00 / 15:00 | Mythos-Check | Der Kolben ist nicht in der Hubmitte am schnellsten | The piston is not fastest at mid-stroke | Mythos | medium | 2 | geplant |
| Mo 09.11. | 14:00 / 20:00 | Im Schnitt | Warum jeder Zylinder nur bei jeder zweiten Umdrehung zündet | Why each cylinder fires only every second turn | Erklärung | medium | 2 | produziert (EN geplant) |
| Mo 09.11. | 18:00 / 23:00 | Im Schnitt | Warum Verdichten die Luft heiß macht | Why compression heats the air | Erklärung | medium | 2 | geplant |
| Di 10.11. | 12:00 / 15:00 | Nachgerechnet | Ein Arbeitsspiel dauert 100 Millisekunden | One engine cycle takes 100 milliseconds | Erklärung | medium | 2 | geplant |
| Di 10.11. | 14:00 / 20:00 | Im Schnitt | Ventilüberschneidung: kurz sind beide Ventile offen | Valve overlap: both valves open at once | Erklärung | medium | 2 | geplant |
| Di 10.11. | 18:00 / 23:00 | Motorgeschichte | Vor Otto: Motoren ohne Verdichtung | Before Otto: engines without compression | Geschichte | low | 2 | geplant |
| Mi 11.11. | 12:00 / 15:00 | Gegenübergestellt | Otto gegen Diesel: Funke oder Hitze | Petrol versus diesel: spark or heat | Vergleich | medium | 3 | geplant |
| Mi 11.11. | 14:00 / 20:00 | Im Schnitt | Zu früh, zu spät, genau richtig: der Zündzeitpunkt | Too early, too late, just right: spark timing | Erklärung | medium | 2 | geplant |
| Mi 11.11. | 18:00 / 23:00 | Im Schnitt | So liest du ein Steuerzeitendiagramm | How to read a valve timing diagram | Anleitung | medium | 2 | geplant |
| Do 12.11. | 12:00 / 15:00 | Nachgerechnet | Hubraum selbst ausrechnen | Work out engine displacement yourself | Erklärung | low | 2 | geplant |
| Do 12.11. | 14:00 / 20:00 | Im Schnitt | Klopfen: wenn das Endgas sich selbst entzündet | Knock: when the end gas ignites by itself | Erklärung | medium | 2 | geplant |
| Do 12.11. | 18:00 / 23:00 | Im Schnitt | So wird die Oktanzahl gemessen | How an octane number is measured | Erklärung | medium | 2 | geplant |
| Fr 13.11. | 12:00 / 15:00 | Gegenübergestellt | Saugrohr- gegen Direkteinspritzung | Port injection versus direct injection | Vergleich | medium | 2 | geplant |
| Fr 13.11. | 14:00 / 20:00 | Im Schnitt | Direkteinspritzung kühlt die Ladung | Direct injection cools the charge | Erklärung | medium | 3 | geplant |
| Fr 13.11. | 18:00 / 23:00 | Motorgeschichte | 1902: die Zündung, die das Auto zuverlässig machte | 1902: the ignition that made cars reliable | Geschichte | low | 3 | geplant |
| Sa 14.11. | 12:00 / 15:00 | Mythos-Check | Mehr Oktan bringt nicht mehr Leistung | Higher octane does not mean more power | Mythos | medium | 2 | geplant |
| Sa 14.11. | 14:00 / 20:00 | Im Schnitt | Heiß oder kalt: der Wärmewert der Zündkerze | Hot or cold: the spark plug heat range | Erklärung | medium | 2 | geplant |
| Sa 14.11. | 18:00 / 23:00 | Im Schnitt | So liest du ein p-V-Diagramm | How to read a p-V diagram | Anleitung | medium | 2 | geplant |
| So 15.11. | 12:00 / 15:00 | Motorgeschichte | Ottos Viertakt-Patent | Otto's four-stroke patent | Geschichte | low | 3 | geplant |
| So 15.11. | 14:00 / 20:00 | Im Schnitt | Diesel: Zündung in vier Phasen | Diesel: ignition in four phases | Erklärung | medium | 2 | geplant |
| So 15.11. | 18:00 / 23:00 | Im Schnitt | Was in einer Zündkerze steckt | What is inside a spark plug | Erklärung | low | 2 | geplant |
| Mo 16.11. | 12:00 / 15:00 | Mythos-Check | Diesel hat mehr Energie? Nur pro Liter | Diesel has more energy? Only per litre | Mythos | medium | 3 | geplant |
| Mo 16.11. | 14:00 / 20:00 | Im Schnitt | Common Rail: Einspritzung mit über 2000 bar | Common rail: injection above 2,000 bar | Erklärung | medium | 2 | geplant |
| Mo 16.11. | 18:00 / 23:00 | Im Schnitt | Der Diesel hat keine Drosselklappe | A diesel has no throttle | Erklärung | medium | 2 | geplant |
| Di 17.11. | 12:00 / 15:00 | Nachgerechnet | Warum der Diesel 30 Prozent weniger braucht | Why a diesel uses 30 percent less fuel | Erklärung | medium | 2 | geplant |
| Di 17.11. | 14:00 / 20:00 | Im Schnitt | Dieselpartikelfilter: Ruß fangen und abbrennen | Diesel particulate filter: catch soot, burn it off | Erklärung | medium | 2 | geplant |
| Di 17.11. | 18:00 / 23:00 | Motorgeschichte | 1927: die Pumpe, die den Diesel ins Auto brachte | 1927: the pump that put diesel into cars | Geschichte | low | 3 | geplant |
| Mi 18.11. | 12:00 / 15:00 | Gegenübergestellt | Oktan und Cetan: zwei Zahlen, zwei Gegensätze | Octane and cetane: two numbers, opposite goals | Vergleich | medium | 3 | geplant |
| Mi 18.11. | 14:00 / 20:00 | Im Schnitt | SCR: wie Harnstoff Stickoxide zerlegt | SCR: how urea breaks down nitrogen oxides | Erklärung | medium | 2 | geplant |
| Mi 18.11. | 18:00 / 23:00 | Im Schnitt | Warum Diesel fast schwefelfrei wurde | Why diesel became almost sulphur-free | Erklärung | medium | 2 | geplant |
| Do 19.11. | 12:00 / 15:00 | Nachgerechnet | Wohin die Energie aus dem Tank geht | Where the energy in your tank goes | Liste | medium | 2 | geplant |
| Do 19.11. | 14:00 / 20:00 | Im Schnitt | Abgasrückführung: Abgas gegen Stickoxide | Exhaust gas recirculation: exhaust against NOx | Erklärung | medium | 2 | geplant |
| Do 19.11. | 18:00 / 23:00 | Im Schnitt | Fünf Stellen, an denen der Motor Arbeit verliert | Five places where an engine loses work | Liste | medium | 2 | geplant |
| Fr 20.11. | 12:00 / 15:00 | Gegenübergestellt | Aluminium- gegen Stahlkolben | Aluminium versus steel pistons | Vergleich | medium | 2 | geplant |
| Fr 20.11. | 14:00 / 20:00 | Im Schnitt | Die Lambdasonde riecht den Sauerstoff | The lambda sensor smells the oxygen | Erklärung | medium | 2 | geplant |
| Fr 20.11. | 18:00 / 23:00 | Motorgeschichte | 1951: Benzineinspritzung im Kleinwagen | 1951: fuel injection in a small car | Geschichte | low | 2 | geplant |
| Sa 21.11. | 12:00 / 15:00 | Mythos-Check | Der Katalysator putzt nicht alles weg | The catalytic converter does not clean everything | Mythos | medium | 2 | geplant |
| Sa 21.11. | 14:00 / 20:00 | Im Schnitt | Kaltstart: die schmutzigsten Sekunden | Cold start: the dirtiest seconds | Erklärung | medium | 2 | geplant |
| Sa 21.11. | 18:00 / 23:00 | Im Schnitt | Biodiesel: Pflanzenöl umgeestert | Biodiesel: vegetable oil, transesterified | Erklärung | medium | 2 | geplant |
| So 22.11. | 12:00 / 15:00 | Motorgeschichte | Rudolf Diesel: Patent 1893, Motor 1897 | Rudolf Diesel: patent 1893, engine 1897 | Geschichte | low | 3 | geplant |
| So 22.11. | 14:00 / 20:00 | Im Schnitt | Warum das Gemisch absichtlich pendelt | Why the mixture swings on purpose | Erklärung | medium | 2 | geplant |
| So 22.11. | 18:00 / 23:00 | Im Schnitt | Abgasgrenzwerte: zehnmal strenger alle 15 Jahre | Emission limits: ten times stricter every 15 years | Liste | medium | 3 | geplant |
| Mo 23.11. | 12:00 / 15:00 | Mythos-Check | Der Turbo ist keine Gratisleistung | A turbo is not free power | Mythos | medium | 3 | geplant |
| Mo 23.11. | 14:00 / 20:00 | Im Schnitt | Turboloch: woher es kommt | Turbo lag: where it comes from | Erklärung | medium | 3 | geplant |
| Mo 23.11. | 18:00 / 23:00 | Im Schnitt | Warum der Turbo einen Ladeluftkühler braucht | Why a turbo needs an intercooler | Erklärung | medium | 3 | geplant |
| Di 24.11. | 12:00 / 15:00 | Nachgerechnet | Wie schnell dreht ein Turbolader? | How fast does a turbocharger spin? | Erklärung | medium | 3 | geplant |
| Di 24.11. | 14:00 / 20:00 | Im Schnitt | Nockenwellenversteller: Steuerzeiten, die sich bewegen | Cam phasers: valve timing that moves | Erklärung | medium | 3 | geplant |
| Di 24.11. | 18:00 / 23:00 | Motorgeschichte | 1905: Büchis Idee vom Abgasturbolader | 1905: Büchi's idea of the exhaust turbocharger | Geschichte | low | 2 | geplant |
| Mi 25.11. | 12:00 / 15:00 | Gegenübergestellt | Kompressor gegen Turbo | Supercharger versus turbo | Vergleich | medium | 2 | geplant |
| Mi 25.11. | 14:00 / 20:00 | Im Schnitt | VTEC: zwei Nocken für ein Ventil | VTEC: two cams for one valve | Erklärung | medium | 2 | geplant |
| Mi 25.11. | 18:00 / 23:00 | Im Schnitt | Variable Turbinengeometrie im Benziner | Variable turbine geometry in a petrol engine | Erklärung | medium | 3 | geplant |
| Do 26.11. | 12:00 / 15:00 | Nachgerechnet | Die Formel hinter der Verdichtung | The formula behind compression ratio | Erklärung | medium | 2 | geplant |
| Do 26.11. | 14:00 / 20:00 | Im Schnitt | Ventilhub ohne feste Nocke | Valve lift without a fixed cam profile | Erklärung | medium | 2 | geplant |
| Do 26.11. | 18:00 / 23:00 | Im Schnitt | 14 zu 1: ein Benziner mit Dieselverdichtung | 14 to 1: a petrol engine with diesel compression | Erklärung | medium | 2 | geplant |
| Fr 27.11. | 12:00 / 15:00 | Gegenübergestellt | Wastegate gegen variable Turbinengeometrie | Wastegate versus variable turbine geometry | Vergleich | medium | 3 | geplant |
| Fr 27.11. | 14:00 / 20:00 | Im Schnitt | Miller und Atkinson: weniger verdichten als expandieren | Miller and Atkinson: compress less than you expand | Erklärung | medium | 3 | geplant |
| Fr 27.11. | 18:00 / 23:00 | Motorgeschichte | 1885: Daimlers Reitwagen | 1885: Daimler's riding car | Geschichte | low | 2 | geplant |
| Sa 28.11. | 12:00 / 15:00 | Mythos-Check | Der Zweitakter leistet nicht doppelt so viel | A two-stroke does not make twice the power | Mythos | medium | 3 | geplant |
| Sa 28.11. | 14:00 / 20:00 | Im Schnitt | Zylinderabschaltung: ein Vierzylinder als Zweizylinder | Cylinder deactivation: a four running on two | Erklärung | medium | 2 | geplant |
| Sa 28.11. | 18:00 / 23:00 | Im Schnitt | Die Drosselklappe kostet Sprit | The throttle costs fuel | Erklärung | medium | 2 | geplant |
| So 29.11. | 12:00 / 15:00 | Motorgeschichte | 1886: das Patent zum Benz-Motorwagen | 1886: the patent for the Benz Motorwagen | Geschichte | low | 2 | geplant |
| So 29.11. | 14:00 / 20:00 | Im Schnitt | MGU-H: der Generator zwischen Turbine und Verdichter | MGU-H: the generator between turbine and compressor | Erklärung | medium | 2 | geplant |
| So 29.11. | 18:00 / 23:00 | Im Schnitt | Super-Knock: Vorentflammung im Turbobenziner | Super-knock: pre-ignition in turbo petrol engines | Erklärung | medium | 2 | geplant |
| Mo 30.11. | 12:00 / 15:00 | Mythos-Check | Start-Stopp: Neustarten kostet weniger, als man denkt | Stop-start: restarting costs less than you think | Mythos | medium | 3 | geplant |
| Mo 30.11. | 14:00 / 20:00 | Im Schnitt | 41 Prozent: ein Serienbenziner am Limit | 41 percent: a production petrol engine at the limit | Erklärung | medium | 2 | geplant |
| Mo 30.11. | 18:00 / 23:00 | Im Schnitt | Was ein Mildhybrid wirklich macht | What a mild hybrid actually does | Erklärung | medium | 3 | geplant |
| Di 01.12. | 12:00 / 15:00 | Nachgerechnet | Tanken mit elf Megawatt | Refuelling at eleven megawatts | Erklärung | medium | 2 | geplant |
| Di 01.12. | 14:00 / 20:00 | Im Schnitt | Benziner mit Selbstzündung | Petrol engines that self-ignite | Erklärung | medium | 2 | geplant |
| Di 01.12. | 18:00 / 23:00 | Motorgeschichte | Der elektrische Anlasser ersetzt die Kurbel | The electric starter replaces the crank | Geschichte | low | 2 | geplant |
| Mi 02.12. | 12:00 / 15:00 | Gegenübergestellt | Wasserstoff im Motor oder in der Brennstoffzelle | Hydrogen in an engine or in a fuel cell | Vergleich | medium | 2 | geplant |
| Mi 02.12. | 14:00 / 20:00 | Im Schnitt | Lkw-Diesel mit über 52 Prozent Wirkungsgrad | Truck diesels above 52 percent efficiency | Erklärung | medium | 2 | geplant |
| Mi 02.12. | 18:00 / 23:00 | Im Schnitt | Erdgas im Motor: Methan unter Hochdruck | Natural gas engines: high pressure in the tank | Erklärung | medium | 2 | geplant |
| Do 03.12. | 12:00 / 15:00 | Nachgerechnet | Mitteldruck: die faire Vergleichszahl | Mean effective pressure: the fair comparison | Erklärung | medium | 2 | geplant |
| Do 03.12. | 14:00 / 20:00 | Im Schnitt | Über 50 Prozent: der Formel-1-Motor | Above 50 percent: the Formula 1 engine | Erklärung | medium | 2 | geplant |
| Do 03.12. | 18:00 / 23:00 | Im Schnitt | Sommer- und Winterbenzin | Summer and winter petrol | Erklärung | medium | 2 | geplant |
| Fr 04.12. | 12:00 / 15:00 | Gegenübergestellt | Benzin gegen Ethanol | Petrol versus ethanol | Vergleich | medium | 3 | geplant |
| Fr 04.12. | 14:00 / 20:00 | Im Schnitt | Warum der Prius einen Atkinson-Motor hat | Why the Prius uses an Atkinson engine | Erklärung | medium | 2 | geplant |
| Fr 04.12. | 18:00 / 23:00 | Motorgeschichte | Wankels Drehkolben | Wankel's rotary engine | Geschichte | low | 2 | geplant |
| Sa 05.12. | 12:00 / 15:00 | Mythos-Check | Mehr Masseelektroden, mehr Funken? | More ground electrodes, more sparks? | Mythos | low | 2 | geplant |
| Sa 05.12. | 14:00 / 20:00 | Im Schnitt | Der Wankel als Stromerzeuger | The rotary as a generator | Erklärung | medium | 2 | geplant |
| Sa 05.12. | 18:00 / 23:00 | Gegenübergestellt | Literleistung: Benziner gegen Diesel | Power per litre: petrol versus diesel | Vergleich | medium | 3 | geplant |
| So 06.12. | 12:00 / 15:00 | Motorgeschichte | Der Motor der Wright Flyer: gebaut in sechs Wochen | The Wright Flyer engine: built in six weeks | Geschichte | low | 3 | geplant |
| So 06.12. | 14:00 / 20:00 | Im Schnitt | Drei Kolbenringe, drei Aufgaben | Three piston rings, three jobs | Erklärung | medium | 2 | geplant |
| So 06.12. | 18:00 / 23:00 | Im Schnitt | Platin, Palladium, Rhodium: was im Katalysator arbeitet | Platinum, palladium, rhodium: what works in a catalyst | Erklärung | medium | 2 | geplant |

## Vorsicht bei einzelnen Themen (Quellenlage)

- **Datum Benz-Patent (29.11.) und Daimler-Reitwagen (27.11.):** DEPATISnet nennt 28.01.1886 und 28.08.1885, Deutsches Museum und Mercedes-Benz 29.01.1886 und 29.08.1885. Im Video nur Monat und Jahr nennen.
- **Wright-Motor (06.12.):** NASA und NASM-Objekt nennen 12 PS, die NASM-Seite zu Charles Taylor 13 PS Bremsleistung. Nur „rund 12 PS“ sagen oder beide Angaben zeigen.
- **Büchi (24.11.):** Die Patentschrift DRP 204630 zeigt kein lesbares Datum; Accelleron nennt 1905. Nur das Jahr nennen.
- **Otto (15.11.):** Im DRP 532 ist die Gasmotorenfabrik Deutz Anmelderin, das Erfinderfeld ist leer; Beau de Rochas (1862) ist ohne Primärquelle und bleibt weg.
- **Bosch-Zündung (13.11.):** Bosch-Geschichtsseiten nennen 1902; eine Bosch-Zündkerzenseite nennt 1901 (nur Suchtreffer, nicht geöffnet).
- **Start-Stopp (30.11.):** fueleconomy.gov nennt auf der Technikseite 2 %, ein Ratgeber angeblich bis 5 % (nicht geöffnet). Nur die 0,7 Sekunden von Bosch und das Prinzip verwenden.
- **Herstellerwerte (Toyota 41 %, Mercedes über 50 %, Mazda „world's highest“, Schaeffler, BorgWarner):** als Herstellerangaben kennzeichnen.
- **MIT 2.61 (Stand 2017):** Zahlen zu Grenzwerten, Schwefel und Marktanteilen sind US-Werte oder älter; im Video als „laut MIT-Vorlesung 2017“ einordnen. MIT-Abbildungen sind teils nicht CC-lizenziert: nur Fakten nutzen, Grafiken selbst bauen.
- **Erdgas (02.12.):** Die Quelle nennt 3.600 psi; Bar-Werte nur als gekennzeichnete Umrechnung.

## Reserve (belegt, nicht eingeplant)

- Einlass schließt nach UT, Ram-Effekt (MIT L8, L3).
- Klopfsensor im Detail (Bosch Klopfsensor, MIT L10).
- Mehrfacheinspritzung beim Diesel (Bosch Common Rail, MIT L16).
- Flammenkern 1 mm in 100 µs; verbranntes Gas 2.800 K (nur MIT L9 und L10, zweite unabhängige Quelle fehlt).
- Stöchiometrie 14,7 zu 1 als eigenes Thema (MIT L4, Bosch, NGK).
- Weitere Geschichte: Bleitetraethyl hob die Verdichtung von 5 auf 9 (MIT L1, zweite Quelle fehlt); erste turboaufgeladene Schiffe 1926 (Accelleron).

## Offene Punkte

- Englische Fassung des Testvideos „Zwei Umdrehungen“ (09.11., 15:00) ist noch nicht produziert; der deutsche Post steht als „produziert“.
- Keine Videos produziert, keine Gemini-Anfrage, nichts veröffentlicht. Vertonung aller übrigen 166 Posts offen.
- Der alte Kalender vom 30.10. und der alte Entwurf „Themenplan November 2026 – Revlore.md“ liegen in `C:\Users\Stefa\Documents\_zum_loeschen\2026-11-01 Kalender alt`. Übernommen wurden daraus die belegbaren Winkel (Takte, Steuerzeiten, Klopfen, Diesel, Aufladung, Abgas), jetzt mit zweiter Quelle.
