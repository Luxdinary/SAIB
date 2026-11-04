# Revlore – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Revlore (Format 1.0).md`; den Rest der Vorlage schreibt die Revlore-Sitzung. Erzeugt nach `Bibliothek Prompt-Blatt.md` mit Higgsfield Ultra (Budget 100 Credits).

**Stand der Erzeugung:** Die 5 Startbilder sind abgelegt (16 Credits, davon 6 für drei verworfene Bilder). Die 5 Schleifen (je 10 Credits) fehlen noch: Seit dem 02.11.2026 etwa 15:29 Wien wird am ganzen Higgsfield-Konto kein Video fertig; die Hauptsitzung hat neue Video-Aufträge angehalten. Zwei Schleifen sind eingereicht und hängen, drei sind noch nicht eingereicht. Bis dahin liegen die Startbilder als `rl_bg_*.jpg` bereit.

**Grundregel:** Die Bibliothek gibt nur Raum, Licht und Oberflächen hinter dem Modell. Die Mechanik bleibt das gerechnete Code-Modell; im Hintergrund läuft keine Mechanik.

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\engines\assets\higgsfield\library\`
Kontaktbogen: `index.html`. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json`.

| Datei | Motiv | Helligkeit Mitte | Form |
|---|---|---|---|
| `rl_bg_testcell` | Prüfstand-Raum bei Nacht, Motor als dunkle Silhouette im unteren Drittel | 21 % | Startbild `.jpg` da; Schleife `.mp4` folgt |
| `rl_bg_engbay` | Motorraum von oben, sehr dunkel (Low-Key), nur Lichtkanten | 5 % | wie oben |
| `rl_bg_bench` | Werkbank mit zerlegtem Zylinderkopf, leere dunkle Wand | 11 % | wie oben |
| `rl_bg_manifold` | glühender Abgaskrümmer, Glut nur unten rechts | 16 % | wie oben; nur für Themen zu Abgas und Verbrennung, weil Orange im Modell für Verbrennung steht |
| `rl_bg_hall` | leere dunkle Werkstatthalle mit Bodenraster, Hallenlicht oben | 21 % | wie oben; neutral für alle Themen |

Alle Bilder 1536 × 2752 (9:16), kein Hersteller, kein Logo, keine lesbare Schrift, keine Personen. Beim Motorraum sind auf Sicherungskasten und Deckel unlesbare Prägesymbole erst bei starker Aufhellung zu erkennen; im Video unter dem Schleier nicht sichtbar.

## Wie im Code einbinden

- **Pfad:** Im Plan `"assets": {"folder": "assets/higgsfield/library", "background": {...}, "scrim": 0.6}` (`src\fn\render\assets.py`). Je verwendeter Datei steht eine Zeile in `LICENSE.md` desselben Ordners.
- **Felder** (laut Prompt-Blatt, baut die Revlore-Sitzung): `zl_hook.backdrop` und `zl_realtime.backdrop`. In der Zeitlupe-Mitte (Lineal, Messschrieb) bleibt der ruhige Messraum-Grund aus Code.
- **Schleier:** etwa 0,6 Deckkraft aus Graphit, damit das Modell klar davor steht.
- **Maße und Schleife:** Schleifen werden 1080 × 1920, 24 s (8-s-Quelle dreimal aneinander), stumm. Bis dahin das `.jpg` mit langsamer Fahrt im Code (100 → 104 %).
- **Kennzeichnung:** wie bisher „KI-generiert“.

## Abnahme (durchgeführt am 02.11.2026)

Jedes Bild auf Hersteller, Logos, Schrift, Personen und laufende Mechanik geprüft, Details vergrößert. Verworfen und nicht abgelegt: Motorraum Fassung 1 (Prägeschrift auf der Motorabdeckung), Motorraum Fassung 2 (zu hell, Form in der Mitte wirkt wie ein Gesichtsprofil), Werkbank Fassung 1 (Personen-Silhouetten im Hintergrund). Abweichung: Beim Prüfstand ist der Motor schärfer als verlangt; unter dem Schleier unkritisch.

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Testvideos (03.11.2026, „Alle freigeben“) hat die Sitzung „Bibliotheken“ wiederverwendbares, fotorealistisches Material ergänzt (Neustart-Plan, Abschnitt 10). Ziel: Die Marken-Sitzung kann im Takt von 2 Themen je Tag Bilder aus der Bibliothek nehmen, statt neue Credits auszugeben. Auswahl der Motive: die Motive, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** derselbe Ordner wie oben, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und der Clip `rl_clip_brass_gears.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: „KI-generiert“; ein KI-Bauteilbild belegt nie das Innere eines Bauteils.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`.

| Datei | Motiv | passt zu |
|---|---|---|
| `rl_real_piston.jpg` | Kolben mit Pleuel und Ringen, Makro | Motor, Verbrennung |
| `rl_real_powertools.jpg` | Akkuschrauber, Schlagschrauber, Bohrhammer ohne Marke | Werkzeug |
| `rl_real_laundry.jpg` | Waschkueche mit Waschmaschine (Seitenansicht) und Heizkoerper mit Thermostatkopf | Haushaltstechnik |
| `rl_real_workbench_tools.jpg` | Dunkle Werkbank mit Handwerkzeug und Arbeitslampe | Werkzeug, Einstieg |
| `rl_real_engine_bay.jpg` | Motorraum von oben, normal ausgeleuchtet, ohne Abzeichen | Motor, Fahrzeuge |
| `rl_real_engine_stand.jpg` | Motorblock mit Zylinderkopf auf Montagebock | Motor |
| `rl_real_camshaft.jpg` | Nockenwelle mit Ventilen und Federn | Ventiltrieb |
| `rl_real_sparkplug.jpg` | Zuendkerze Makro (Geometrie vom Modell vereinfacht, nur Stimmung) | Zuendung |
| `rl_real_turbo.jpg` | Ausgebauter Turbolader, Verdichterrad sichtbar | Aufladung |
| `rl_real_brass_gears.jpg` | Messing-Zahnraeder im Eingriff | Getriebe, Uebersetzung, Mechanik |
| `rl_real_stationary_engine.jpg` | Alter Einzylinder-Stationaermotor mit Schwungrad im Museum | Reihe Erstes Modell |
| `rl_real_plug_socket.jpg` | Netzstecker in Steckdose, Makro | Elektrik, Haushalt |
| `rl_real_brake_lift.jpg` | Auto auf Hebebuehne, Bremsscheibe und Sattel (ohne Abzeichen) | Fahrzeuge, Bremsen |
| `rl_real_watch_balance.jpg` | Uhrwerk mit Unruh, Makro (nur Plus-/Minus-Zeichen am Ruecker) | Mechanik, Zeitmessung |
| `rl_real_pcb_relays.jpg` | Platine mit Relais und Tastern, Makro | Elektrik, Elektronik |
| `rl_real_wrenches.jpg` | Ratschen und Nuesse (der Drehmomentschluessel ist nicht eindeutig erkennbar) | Werkzeug, Drehmoment |
| `rl_real_bike_drivetrain.jpg` | Fahrradantrieb: Ritzelpaket, Kette, Schaltwerk | Fahrzeuge, Uebersetzung |
| `rl_real_crankshaft.jpg` | Kurbelwelle mit Schwungrad | Motor, Drehmoment |
| `rl_clip_brass_gears.mp4` | Messing-Zahnraeder im Eingriff (Schleife); 1080 × 1920, 24 s Schleife (8 s dreimal), stumm; Startbild `rl_real_brass_gears.jpg` | Getriebe, Uebersetzung, Mechanik |

**Einbinden:** wie oben, Ordner `assets/higgsfield/library`. Für einen Clip ohne Schleife das Startbild als Standbild davor oder danach setzen. Bei Bildern mit Händen oder Menschen immer die Kennzeichnung oben einblenden.
