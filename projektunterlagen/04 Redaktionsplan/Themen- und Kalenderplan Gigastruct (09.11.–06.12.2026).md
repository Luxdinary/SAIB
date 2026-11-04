# Themen- und Kalenderplan Gigastruct (09.11.–06.12.2026)

**Freigegeben von Stefan am 01.11.2026.** Themen im Status `planned` gehen in die Produktion; Themen im Status `idea` erst nach Quellenprüfung; Risiko „high“ vor jeder Veröffentlichung einzeln an Stefan.

Stand: 01.11.2026 (Wien). Marke `megaconstruction`, Vorlage 1.0. Grundlage: `04 Redaktionsplan\Planungsrahmen Themen- und Kalenderplan.md` und `C:\Automation\faceless-network\prompts\calendar_planner.md`. Nicht veröffentlicht, nichts produziert außer dem schon fertigen Testvideo.

- Kalender: `C:\Automation\faceless-network\data\calendars\megaconstruction_2026-11.json` (168 Zeilen, 84 Themen als DE/EN-Paar). Prüfung `fn.cli calendar check`: ohne Befund.
- Recherche je Thema (Kernzahlen mit Quelle, Hook-Idee, Rechnung, Einschränkungen): `C:\Automation\faceless-network\data\calendars\megaconstruction_2026-11.research.json`.
- Takt: 3 Themen am Tag, je auf Deutsch (12:00, 14:00, 18:00) und Englisch (15:00, 20:00, 23:00), Wiener Zeit.
- Status: 80 Themen `planned`, 1 Thema mit fertiger deutscher Fassung (Fehmarnbelt, DE `produced`, EN `planned`), 3 Themen `idea`. Risiko: 66 low, 18 medium, kein high.
- Quellen: je Thema mindestens zwei geöffnete Primärquellen (Bauherr, Betreiber, Behörde, Planer, Hochschule oder Fachzeitschrift; Fachpresse nur als zweite Quelle). 30 Themen (darunter Fehmarnbelt) stammen aus der Recherche vom 30.10.2026 (Abrufdatum 30.10.), 54 wurden am 01.11.2026 recherchiert.

## Themenreihen

| Reihe | Ziel | Format | Takt je Woche | Beispiele |
|---|---|---|---|---|
| **Nachgerechnet** | Größe nicht behaupten, sondern aus zwei belegten Werten rechnen; der Vergleich ist der Hook | comparison | 5 (Mo, Di, Mi, Do, Sa) | Fehmarnbelt-Element gegen Eiffelturm, Danyang–Kunshan gegen Eurotunnel, Rotorblatt gegen A380 |
| **So wird's gebaut** | Ein Bauverfahren oder eine Maschine Schritt für Schritt am 3D-Modell erklären | howto, explainer | 5 (Mo, Mi, Do, Fr, So) | Taipei-101-Dämpfer, MOSE-Tore in Venedig, Brenner Basistunnel |
| **Rekord in Zahlen** | Drei bis fünf belegte Zahlen zu einem Rekordbauwerk, jede als eigenes Bildereignis | listicle | 4 (Di, Mi, Fr, Sa) | Kiel-Kanal, Shanghai Tower, Svalbard Seed Vault |
| **Baugeschichte** | Wie ein historisches Bauwerk entstand: Problem, Lösung, Bauzeit, Stand heute | story | 4 (Di, Do, Sa, So) | Brooklyn Bridge, Simplontunnel, Kölner Dom |
| **Mythos-Check** | Einen verbreiteten Irrtum mit Primärquellen auflösen, ohne Häme | myth | 3 (Mo, Fr, So) | Große Mauer aus dem All, Eiffelturm aus Stahl?, Pisa fällt bald? |

Wochenraster (Thema 1 / 2 / 3 des Tages): Mo Mythos-Check / Nachgerechnet / So wird's gebaut · Di Nachgerechnet / Rekord / Baugeschichte · Mi So wird's gebaut / Nachgerechnet / Rekord · Do Baugeschichte / So wird's gebaut / Nachgerechnet · Fr Rekord / Mythos-Check / So wird's gebaut · Sa Nachgerechnet / Baugeschichte / Rekord · So So wird's gebaut / Baugeschichte / Mythos-Check.

Verteilt ist so, dass dasselbe Bauwerk oder dasselbe Motiv nicht in derselben Woche zweimal kommt (zum Beispiel Eiffelturm-Themen in vier verschiedenen Wochen, Hoover-Damm und Hoover-Mythos getrennt, Sturmflutwehre MOSE, Maeslantkering, Afsluitdijk und Oosterscheldekering je eine Woche).

## Kalender

Uhrzeit DE / EN. Quellen = Zahl der geöffneten Quellen. Titel EN sind sprachlich angepasst, die englische Fassung wird beim Skript lokalisiert.

| Datum | Uhrzeit DE / EN | Reihe | Titel DE | Titel EN | Format | Risiko | Quellen | Status |
|---|---|---|---|---|---|---|---|---|
| Mo 09.11. | 12:00 / 15:00 | Mythos-Check | Große Mauer aus dem All sichtbar? NASA sagt: nein | Great Wall Visible From Space? NASA Says No | myth | low | 3 | planned |
| Mo 09.11. | 14:00 / 20:00 | Nachgerechnet | Fehmarnbelt-Tunnel: ein Tunnelelement wiegt mehr als sieben Eiffeltürme | Fehmarnbelt tunnel: one element outweighs seven Eiffel Towers | comparison | low | 4 | fertig (DE) |
| Mo 09.11. | 18:00 / 23:00 | So wird's gebaut | Brenner Basistunnel: 230 km Röhren für 55 km Bahnstrecke | Brenner Base Tunnel: 230 km of tubes for a 55 km railway | explainer | medium | 4 | planned |
| Di 10.11. | 12:00 / 15:00 | Nachgerechnet | 164 km Brücke: mehr als dreimal so lang wie der Eurotunnel | A 164 km bridge: over three times the Channel Tunnel | comparison | low | 4 | planned |
| Di 10.11. | 14:00 / 20:00 | Rekord in Zahlen | Gotthard-Basistunnel: 10 Jahre, 445.000 Züge durch den Berg | Gotthard Base Tunnel: 10 years, 445,000 trains through the mountain | listicle | low | 3 | planned |
| Di 10.11. | 18:00 / 23:00 | Baugeschichte | Großglockner Hochalpenstraße: 36 Kehren in fünf Jahren gebaut | Grossglockner High Alpine Road: 36 hairpins built in five years | story | low | 3 | planned |
| Mi 11.11. | 12:00 / 15:00 | So wird's gebaut | Wie eine 660-Tonnen-Kugel Taipei 101 ruhig hält | How a 660-tonne steel ball keeps Taipei 101 steady | howto | low | 4 | planned |
| Mi 11.11. | 14:00 / 20:00 | Nachgerechnet | Burj Khalifa: 828 Meter auf einer 3,7 Meter dicken Betonplatte | Burj Khalifa: 828 metres standing on a 3.7-metre concrete raft | comparison | low | 5 | planned |
| Mi 11.11. | 18:00 / 23:00 | Rekord in Zahlen | Kiel-Kanal in 5 Zahlen: 98,6 km, 24.866 Schiffe, 310-m-Schleuse | Kiel Canal in 5 Numbers: 98.6 km, 24,866 Ships, a 310 m Lock | listicle | low | 5 | planned |
| Do 12.11. | 12:00 / 15:00 | Baugeschichte | Brooklyn Bridge: Als der Bau Arbeiter und Chefingenieur krank machte | Brooklyn Bridge: The Caissons That Made Workers Sick | story | medium | 5 | planned |
| Do 12.11. | 14:00 / 20:00 | So wird's gebaut | Panamakanal: So spart eine Neopanamax-Schleuse 60 % Wasser | Panama Canal: how a Neopanamax lock saves 60% of its water | howto | low | 3 | planned |
| Do 12.11. | 18:00 / 23:00 | Nachgerechnet | 625 m über dem Fluss: fast zwei Eiffeltürme übereinander | 625 m above the river: almost two Eiffel Towers stacked | comparison | low | 4 | planned |
| Fr 13.11. | 12:00 / 15:00 | Rekord in Zahlen | Shanghai Tower: 632 m, 120° Drehung, 1.000-t-Pendel | Shanghai Tower: 632 m, a 120° Twist and a 1,000-Tonne Damper | listicle | low | 5 | planned |
| Fr 13.11. | 14:00 / 20:00 | Mythos-Check | Elbphilharmonie: Schwebt der Große Saal wirklich? | Elbphilharmonie: does the Grand Hall really float? | myth | low | 3 | planned |
| Fr 13.11. | 18:00 / 23:00 | So wird's gebaut | MOSE: 78 Tore, die mit Druckluft aus dem Meeresboden steigen | MOSE: 78 gates that rise from the seabed on compressed air | howto | medium | 4 | planned |
| Sa 14.11. | 12:00 / 15:00 | Nachgerechnet | Kölner Dom gegen Ulmer Münster: 4,31 m Unterschied im Turm | Cologne Cathedral vs Ulm Minster: a 4.31 m tower difference | comparison | low | 3 | planned |
| Sa 14.11. | 14:00 / 20:00 | Baugeschichte | Forth Bridge: Stahl-Antwort auf das Tay-Bridge-Unglück | Forth Bridge: Britain's Steel Answer to the Tay Disaster | story | low | 2 | planned |
| Sa 14.11. | 18:00 / 23:00 | Rekord in Zahlen | Grand Coulee Dam: fast 12 Mio. yd³ Beton, 6.809 MW | Grand Coulee Dam: Nearly 12 Million Cubic Yards, 6,809 MW | listicle | low | 4 | planned |
| So 15.11. | 12:00 / 15:00 | So wird's gebaut | Kölnbreinsperre: Österreichs höchste Staumauer auf 1.902 Metern | Kölnbrein Dam: Austria's tallest dam at 1,902 metres | explainer | low | 3 | planned |
| So 15.11. | 14:00 / 20:00 | Baugeschichte | Eiffelturm: 18.038 Teile in 2 Jahren, 2 Monaten, 5 Tagen | Eiffel Tower: 18,038 Parts Built in 26 Months | story | low | 3 | planned |
| So 15.11. | 18:00 / 23:00 | Mythos-Check | Pisa: 46 cm aufgerichtet - fällt der Turm bald? | Leaning Tower of Pisa: straightened 46 cm, will it fall? | myth | medium | 4 | planned |
| Mo 16.11. | 12:00 / 15:00 | Mythos-Check | Hoover-Damm: Liegen Arbeiter im Beton? Mythos-Check | Hoover Dam: Are Workers Buried in the Concrete? No | myth | medium | 2 | planned |
| Mo 16.11. | 14:00 / 20:00 | Nachgerechnet | Koralmtunnel: 33 Kilometer – das sind 100 Eiffeltürme | Koralm Tunnel: 33 kilometres – that is 100 Eiffel Towers | comparison | low | 6 | planned |
| Mo 16.11. | 18:00 / 23:00 | So wird's gebaut | Skytree: Ein 375-m-Betonschaft dämpft den 634-m-Turm | Skytree: how a 375 m concrete shaft tames a 634 m tower | explainer | low | 2 | planned |
| Di 17.11. | 12:00 / 15:00 | Nachgerechnet | Itaipu: im Rekordjahr 1,5-mal mehr Strom je Gigawatt | Itaipu: in its record year, 1.5x more power per gigawatt | comparison | low | 4 | planned |
| Di 17.11. | 14:00 / 20:00 | Rekord in Zahlen | Grand Paris Express: 200 km neue Metro, 68 neue Bahnhöfe | Grand Paris Express: 200 km of new metro, 68 new stations | listicle | medium | 2 | planned |
| Di 17.11. | 18:00 / 23:00 | Baugeschichte | Akashi-Kaikyō-Brücke: 24 Jahre Weltrekord über dem Meer | Akashi Kaikyo Bridge: a 24-year world record over the sea | story | low | 3 | planned |
| Mi 18.11. | 12:00 / 15:00 | So wird's gebaut | Maeslantkering: So schließt Rotterdam sein Tor zum Meer | Maeslantkering: how Rotterdam shuts its gate to the sea | howto | low | 2 | planned |
| Mi 18.11. | 14:00 / 20:00 | Nachgerechnet | Viadukt von Millau: Fahrbahn aus fast fünf Eiffeltürmen Stahl | Millau Viaduct: a deck made of almost five Eiffel Towers of steel | comparison | low | 3 | planned |
| Mi 18.11. | 18:00 / 23:00 | Rekord in Zahlen | Sagrada Família: 5 Zahlen vom Grundstein 1882 bis 172,5 m | Sagrada Família: 5 Numbers from the 1882 Cornerstone to 172.5 m | listicle | low | 5 | planned |
| Do 19.11. | 12:00 / 15:00 | Baugeschichte | Simplontunnel: 19,8 km, längster Bahntunnel seiner Zeit | Simplon Tunnel: The Longest Railway Tunnel of Its Time | story | medium | 5 | planned |
| Do 19.11. | 14:00 / 20:00 | So wird's gebaut | So funktioniert das Falkirk Wheel: 1,5 kWh pro Drehung | How the Falkirk Wheel works: 1.5 kWh per rotation | howto | medium | 4 | planned |
| Do 19.11. | 18:00 / 23:00 | Nachgerechnet | 115,5 m: Ein Rotorblatt ist länger als ein A380 breit | One 115.5 m blade is longer than an A380's wingspan | comparison | low | 5 | planned |
| Fr 20.11. | 12:00 / 15:00 | Rekord in Zahlen | Chenab-Brücke: 359 m über dem Fluss, 467 m Stahlbogen | Chenab Bridge: 359 m Above the River, a 467 m Steel Arch | listicle | low | 3 | planned |
| Fr 20.11. | 14:00 / 20:00 | Mythos-Check | Wächst der Eiffelturm im Sommer? Ja, um Millimeter | Does the Eiffel Tower grow in summer? By millimetres | myth | low | 2 | planned |
| Fr 20.11. | 18:00 / 23:00 | So wird's gebaut | Hongkong–Zhuhai–Macau: 55 km Brücke, Tunnel und Inseln | Hong Kong–Zhuhai–Macao: 55 km of bridge, tunnel and islands | explainer | low | 4 | planned |
| Sa 21.11. | 12:00 / 15:00 | Nachgerechnet | Die ISS ist 109 m lang – fast so lang wie das längste Länderspielfeld | The ISS is 109 m long, nearly the longest pitch allowed | comparison | low | 4 | planned |
| Sa 21.11. | 14:00 / 20:00 | Baugeschichte | Schwebebahn Wuppertal: 13,3 km Hochbahn, offen seit 1901 | Wuppertal Suspension Railway: 13.3 km, Running Since 1901 | story | low | 4 | planned |
| Sa 21.11. | 18:00 / 23:00 | Rekord in Zahlen | Seilbahn Zugspitze: 3 Weltrekorde an einer Bahn | Zugspitze cable car: 3 world records in one ride | listicle | low | 3 | planned |
| So 22.11. | 12:00 / 15:00 | So wird's gebaut | CERN LHC: 27 km Ring, 100 m unter der Erde, minus 271,3 °C | CERN LHC: a 27 km ring, 100 m underground, minus 271.3 °C | explainer | low | 3 | planned |
| So 22.11. | 14:00 / 20:00 | Baugeschichte | Suezkanal: 1869 nur 8 m tief, heute 24 m | Suez Canal: 8 m Deep in 1869, 24 m Today | story | low | 3 | planned |
| So 22.11. | 18:00 / 23:00 | Mythos-Check | Römischer Beton: Besser als unserer? Das sagt die Studie | Is Roman concrete better than modern concrete? | myth | low | 2 | planned |
| Mo 23.11. | 12:00 / 15:00 | Mythos-Check | Lötschberg-Basistunnel: seit 2007 offen, nur 40 % zweigleisig | Lötschberg Base Tunnel: open since 2007, only 40% double-track | myth | medium | 2 | planned |
| Mo 23.11. | 14:00 / 20:00 | Nachgerechnet | 1915-Çanakkale-Brücke: 32 Meter mehr als der alte Rekord | 1915 Çanakkale Bridge: 32 metres beyond the old record | comparison | low | 4 | planned |
| Mo 23.11. | 18:00 / 23:00 | So wird's gebaut | Storebælt: Warum die Ostbrücke 325.000-Tonnen-Klötze braucht | Great Belt: why the East Bridge needs 325,000-tonne anchors | explainer | low | 2 | planned |
| Di 24.11. | 12:00 / 15:00 | Nachgerechnet | Merdeka 118: Ein Viertel der Höhe liegt über dem letzten Stock | Merdeka 118: a quarter of its height is above the top floor | comparison | low | 2 | planned |
| Di 24.11. | 14:00 / 20:00 | Rekord in Zahlen | Golden Gate Bridge: 5 Zahlen, die man nicht sieht | Golden Gate Bridge: 5 numbers you can't see | listicle | low | 3 | planned |
| Di 24.11. | 18:00 / 23:00 | Baugeschichte | Seikan-Tunnel: 24 Jahre Bauzeit für 54 km unter Japans Meerenge | Seikan Tunnel: 24 years to build 54 km beneath Japan's strait | story | low | 3 | planned |
| Mi 25.11. | 12:00 / 15:00 | So wird's gebaut | Afsluitdijk: 32 km Damm von 1932 – 2026 verstärkt | Afsluitdijk: the 32 km dam from 1932, reinforced in 2026 | explainer | medium | 5 | planned |
| Mi 25.11. | 14:00 / 20:00 | Nachgerechnet | ITER: Ein Fusionsreaktor so schwer wie drei Eiffeltürme | ITER: a fusion machine as heavy as three Eiffel Towers | comparison | low | 2 | planned |
| Mi 25.11. | 18:00 / 23:00 | Rekord in Zahlen | Peking Daxing: 700.000 m² Terminal, 79 Gates, unter 8 Minuten | Beijing Daxing: 700,000 m² Terminal, 79 Gates, Under 8 Minutes | listicle | low | 5 | planned |
| Do 26.11. | 12:00 / 15:00 | Baugeschichte | Jungfraubahn: 16 Jahre Bau bis auf 3.454 Meter | Jungfraubahn: 16 Years of Building to 3,454 Metres | story | low | 3 | planned |
| Do 26.11. | 14:00 / 20:00 | So wird's gebaut | Hoover Dam: 3,25 Mio. Kubikyard Beton in knapp zwei Jahren | Hoover Dam: 3.25 million cubic yards of concrete in under two years | explainer | low | 2 | planned |
| Do 26.11. | 18:00 / 23:00 | Nachgerechnet | FAST: 500-m-Schüssel – Öffnung wie 24 bis 31 Fußballfelder | China's FAST dish: a 500 m opening, about 24 to 31 football pitches | comparison | low | 4 | planned |
| Fr 27.11. | 12:00 / 15:00 | Rekord in Zahlen | Svalbard Seed Vault: 120 m im Fels, −18 °C, 4,5 Mio. Proben | Svalbard Seed Vault: 120 m Into the Rock, −18 °C, 4.5M Samples | listicle | low | 5 | planned |
| Fr 27.11. | 14:00 / 20:00 | Mythos-Check | Eiffelturm: 7.300 Tonnen Eisen, aber kein Stahl | The Eiffel Tower is made of iron, not steel | myth | low | 5 | planned |
| Fr 27.11. | 18:00 / 23:00 | So wird's gebaut | Rio–Antirrio: Warum 90-m-Pfeiler auf Kies statt Fels stehen | Rion-Antirion Bridge: Piers Built on Gravel to Ride Out Quakes | howto | low | 4 | planned |
| Sa 28.11. | 12:00 / 15:00 | Nachgerechnet | Palm Jumeirah: 94 Mio. m³ Sand – 38× der Beton im Hoover-Damm | Palm Jumeirah: 94 million m³ of sand, 38 Hoover Dams of concrete | comparison | medium | 5 | idea |
| Sa 28.11. | 14:00 / 20:00 | Baugeschichte | Kölner Dom: 632 Jahre Bau, über 300 Jahre Pause | Cologne Cathedral: 632 Years, Over 300 on Pause | story | low | 3 | planned |
| Sa 28.11. | 18:00 / 23:00 | Rekord in Zahlen | Donauturm Wien: 5 Zahlen zu Österreichs höchstem Bauwerk | Vienna's Donauturm in 5 Numbers | listicle | low | 4 | planned |
| So 29.11. | 12:00 / 15:00 | So wird's gebaut | Sydney Harbour Bridge: So pflegt man sechs Millionen Nieten | Sydney Harbour Bridge: how to look after six million rivets | howto | low | 5 | planned |
| So 29.11. | 14:00 / 20:00 | Baugeschichte | Mont-Blanc-Tunnel: 11,6 km, von zwei Seiten gebohrt | Mont Blanc Tunnel: 11.6 km Dug From Two Sides | story | low | 3 | planned |
| So 29.11. | 18:00 / 23:00 | Mythos-Check | Klebreis im Mörtel: Was Chinas Bauleute wirklich nutzten | Sticky rice mortar: what ancient Chinese builders really used | myth | low | 2 | planned |
| Mo 30.11. | 12:00 / 15:00 | Mythos-Check | Golden Gate Bridge: Wirklich ständig komplett neu gestrichen? | Is the Golden Gate Bridge repainted end to end forever? | myth | low | 3 | planned |
| Mo 30.11. | 14:00 / 20:00 | Nachgerechnet | Kanaltunnel vs. Seikan: Wer liegt länger unter dem Meer? | Channel Tunnel vs Seikan: which runs longer under the sea? | comparison | low | 4 | planned |
| Mo 30.11. | 18:00 / 23:00 | So wird's gebaut | Oosterscheldekering: 62 Stahlschieber, in 75 Minuten dicht | Eastern Scheldt barrier: 62 steel gates, closed in 75 minutes | explainer | low | 5 | planned |
| Di 01.12. | 12:00 / 15:00 | Nachgerechnet | Empire State Building: doppelt so schnell gebaut wie der Eiffelturm | Empire State Building: built twice as fast as the Eiffel Tower | comparison | low | 2 | planned |
| Di 01.12. | 14:00 / 20:00 | Rekord in Zahlen | Drei-Schluchten-Damm: 5 Zahlen zum größten Wasserkraftwerk | Three Gorges Dam: 5 numbers behind the biggest hydropower plant | listicle | low | 5 | planned |
| Di 01.12. | 18:00 / 23:00 | Baugeschichte | Olympiadach München: Seilnetz, 80-m-Masten, Acrylglas | Munich's Olympic Roof: Cable Net, 80 m Masts, Acrylic | story | medium | 4 | planned |
| Mi 02.12. | 12:00 / 15:00 | So wird's gebaut | Thames Tideway: Londons 25-km-Supersammler unter der Themse | Thames Tideway: London's 25 km super sewer under the river | explainer | medium | 4 | planned |
| Mi 02.12. | 14:00 / 20:00 | Nachgerechnet | Semmering: Ghega-Bahn von 1854 gegen den neuen Basistunnel | Semmering: the 1854 Ghega railway versus the new base tunnel | comparison | medium | 2 | planned |
| Mi 02.12. | 18:00 / 23:00 | Rekord in Zahlen | Lærdal-Tunnel: 24,5 km und drei Lichthöhlen gegen Müdigkeit | Lærdal Tunnel: 24.5 km and Three Lit Caverns to Keep You Alert | listicle | low | 5 | planned |
| Do 03.12. | 12:00 / 15:00 | Baugeschichte | Alter Elbtunnel Hamburg: 426,5 m unter der Elbe, 1907-1911 | Hamburg's Old Elbe Tunnel: 426.5 m Under the River | story | low | 4 | planned |
| Do 03.12. | 14:00 / 20:00 | So wird's gebaut | Rogfast: 26,7-km-Tunnel, rund 390 m unter dem Meer | Rogfast: a 26.7 km road tunnel about 390 m below sea level | explainer | medium | 4 | planned |
| Do 03.12. | 18:00 / 23:00 | Nachgerechnet | ELT: 39-m-Spiegel aus 798 Segmenten – 4,8× so breit wie beim VLT | ESO's ELT: a 39 m mirror, 4.8 times wider than the VLT's | comparison | low | 8 | planned |
| Fr 04.12. | 12:00 / 15:00 | Rekord in Zahlen | Kaprun: 5 Zahlen zu zwei Stauseen auf 2.040 Metern | Kaprun's Alpine Reservoirs in 5 Numbers | listicle | medium | 6 | planned |
| Fr 04.12. | 14:00 / 20:00 | Mythos-Check | Pantheon: Größte Kuppel aus unbewehrtem Beton - noch heute? | Pantheon: still the largest unreinforced concrete dome? | myth | low | 2 | planned |
| Fr 04.12. | 18:00 / 23:00 | So wird's gebaut | Øresund: Brücke, Insel, Tunnel – 15,9 km in drei Teilen | Øresund: bridge, island, tunnel – 15.9 km in three parts | explainer | low | 3 | planned |
| Sa 05.12. | 12:00 / 15:00 | Nachgerechnet | Pontchartrain Causeway: 38,4 km Brücke, nachgerechnet | Lake Pontchartrain Causeway: 38.4 km, checked by maths | comparison | low | 3 | planned |
| Sa 05.12. | 14:00 / 20:00 | Baugeschichte | Atomium: 102 m hoch, nie für die Ewigkeit gebaut | Atomium: 102 m Tall, Never Meant to Last | story | low | 5 | planned |
| Sa 05.12. | 18:00 / 23:00 | Rekord in Zahlen | Elizabeth Line: 5 Zahlen zu 42 km Tunnel unter London | London's Elizabeth Line: 5 Numbers Under the City | listicle | low | 3 | planned |
| So 06.12. | 12:00 / 15:00 | So wird's gebaut | Allianz Arena: Die ETFE-Hülle aus aufgeblasenen Luftkissen | Allianz Arena: the ETFE skin made of inflated air cushions | explainer | medium | 5 | idea |
| So 06.12. | 14:00 / 20:00 | Baugeschichte | Panamakanal: Frankreich gab 1889 auf, die USA 1914 fertig | Panama Canal: France Quit in 1889, the US Finished in 1914 | story | medium | 4 | planned |
| So 06.12. | 18:00 / 23:00 | Mythos-Check | Venedig steht auf Holzpfählen - warum faulen sie nicht? | Venice stands on wooden piles - why don't they rot? | myth | low | 0 | idea |

## Themen im Status idea (warten auf Quellen)

| Datum | Thema | Was fehlt |
|---|---|---|
| Sa 28.11. | Palm Jumeirah: 94 Mio. m³ Sand gegen Hoover-Damm-Beton | Die Sandmenge stammt nur vom Bauherrn Nakheel (Pressemitteilung 2007); der Auftragnehmer Van Oord nennt eine andere Zahl. Zweite unabhängige Quelle fehlt. Rechnung vorbereitet: 94 Mio. m³ ÷ 2,485 Mio. m³ = 37,8 |
| So 06.12. | Allianz Arena: die ETFE-Hülle | Betreiberseiten (allianz-arena.com, fcbayern.com) waren nicht erreichbar, Kissenzahl uneinheitlich (2.600 bis 2.784) |
| So 06.12. | Venedig: warum die Holzpfähle nicht faulen | Keine Fachquelle ließ sich öffnen (Universität Padua, CNR, Verlage). Recherchehinweise stehen in der Recherche-Datei |

Wenn diese drei bis Ende November nicht belegt sind, werden sie durch Themen aus dem Vorrat ersetzt (Vorschläge unten).

## Hinweise zu einzelnen Themen

- **Risiko medium (18, davon 2 idea):** laufende Projekte mit datiertem Stand (Brenner, Lötschberg, Semmering, Grand Paris Express, Tideway, Rogfast, Kaprun-Erhöhung der Limbergsperre, Afsluitdijk, MOSE) oder Zahlen, die sich zwischen Quellen widersprechen (Brooklyn Bridge, Simplon, Falkirk, Olympiadach, Panamakanal Frankreich, Hoover-Mythos, Pisa). Im Skript nur die belegten Werte, keine Todeszahlen, wo die Quellen auseinandergehen.
- **Grenzfälle bei den Quellen:** Danyang–Kunshan (Guinness und Fachpresse, kein Bauherr), Chenab (Regierungsmeldung nur über IBEF-Wiedergabe plus Fachpresse und Planer WSP), Lærdal (Lichthöhlen nur in Fachpresse), Pantheon (Fachzeitschrift und Konferenzbeitrag). Vor dem Skript gegenprüfen.
- **Angepasste Winkel:** Itaipu (Strom je installiertem Gigawatt statt Jahresrekord; Drei-Schluchten liegt seit 2020 vorn), Rotorblatt (V236 ist nicht mehr das längste, ohne Superlativ), Klebreis-Mörtel (belegt für Gräber, Pagoden, Stadtmauern, nicht für die Große Mauer als Ganzes), Eiffelturm wächst (nur Millimeter, die Spitze beschreibt rund 15 cm Kreis).
- **toureiffel.paris** blockiert automatische Abrufe; die Eiffelturm-Themen wurden im Browser gegengeprüft (Key figures, „Why does the Eiffel Tower change size?“).
- **Aktueller Bezug:** Statens vegvesen sperrt den Lærdal-Tunnel nachts ab 16.11.2026 (Thema am 04.12.).
- **Fehmarnbelt (09.11., 14:00):** Die deutsche Fassung ist fertig (`05 Produktion\Gigastruct\2026-11\2026-11-05 Fehmarnbelt-Tunnelelement`, Fassung Q1). Die englische braucht eine eigene Gemini-Vertonung.

## Vorrat (nicht recherchiert, nicht eingeplant)

Ersatz für idea-Themen oder für Dezember: Hornsea-Windpark, Danyang-Bauweise, Olkiluoto 3, Chek Lap Kok (Flughafen auf künstlicher Insel), Qinghai–Tibet-Bahn, Ceneri-Basistunnel, Arlberg-Straßentunnel, Europabrücke, Tower Bridge (Klappen), Thames Barrier, Maasvlakte 2, Super-Kamiokande.

## Offene Punkte für Stefan

- Die englischen Uhrzeiten (15:00, 20:00, 23:00) sind eine Annahme für Großbritannien und die US-Ostküste.
- Für jedes Thema braucht es eine deutsche und eine englische Gemini-Vertonung: 168 Anfragen in vier Wochen. Das Free-Tier-Kontingent (10 Anfragen am Tag, Stand 30.10.) reicht dafür nicht.
