# Frontlore – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Frontlore (Format 1.0).md`; den Rest der Vorlage schreibt die Frontlore-Sitzung. Erzeugt nach `Bibliothek Prompt-Blatt.md` mit Higgsfield Ultra, **34 Credits** (Budget 60; 26 zurück an die Reserve).

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\military_history\assets\higgsfield\library\`
Kontaktbogen: `index.html` im selben Ordner. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json`.

Alle 16 Bausteine sind **Standbilder**, JPEG, **1536 × 2752** (9:16), keine Schleifen. Bewegung entsteht im Code (langsame Kamerafahrt, Tönung, Schleier).

| Datei | Gruppe | Wofür | Szene im Code |
|---|---|---|---|
| `fl_table_olive.jpg` | T1 Tischgrund | Leinen oliv, ersetzt `assets\bg\base.jpg` | `LAYER` → `layout.ground`, alle Szenen |
| `fl_table_map.jpg` | T2 Tischgrund | Leinen mit leerem, schräg liegendem Kartenbogen | `layout.ground` unter `fr_task` |
| `fl_table_dark.jpg` | T3 Tischgrund | etwas dunkler, für Schlussszenen; nur wenig dunkler als T1, darum im Code zusätzlich abdunkeln | `layout.ground` im Schluss |
| `fl_paper_rag.jpg` | P1 Papier | leeres Hadernpapier, Rand rechts gerissen | Befundblatt, Notizzettel |
| `fl_paper_grid.jpg` | P2 Papier | altes Karopapier, Linien blass | Befundblatt, Rechnungen |
| `fl_map_aegean.jpg` | K1 Karte | Ägäis und Griechenland (Polybios, Hellespont) | `fr_task`, `fr_map` → `data.map` |
| `fl_map_britain.jpg` | K2 Karte | Britannien und Irland (Hadrianswall, Armada-Feuer, Martello) | wie K1 |
| `fl_map_channel.jpg` | K3 Karte | Ärmelkanal mit beiden Küsten (PLUTO, Mulberry, Wetter 1944) | wie K1 |
| `fl_map_upperrhine.jpg` | K4 Karte | Oberrhein und Alpenvorland (Limes, Rheinbrücke, Neuf-Brisach) | wie K1 |
| `fl_map_france.jpg` | K5 Karte | Frankreich (Cassini, Chappe) | wie K1 |
| `fl_map_danube.jpg` | K6 Karte | Mitteleuropa mit Donau (Josephinische Landesaufnahme) | wie K1 |
| `fl_map_finland.jpg` | K7 Karte | Finnischer Meerbusen (Suomenlinna) | wie K1 |
| `fl_map_atlantic.jpg` | K8 Karte | Nordatlantik (Knoten, LORAN) | wie K1 |
| `fl_museum_archive.jpg` | M1 Lesesaal und Museum | Archivregale mit Kartons, unscharf | Hintergrund Befund |
| `fl_museum_reading.jpg` | M2 | Lesesaaltisch mit Leselampe von oben, unscharf | Hintergrund Befund |
| `fl_museum_case.jpg` | M3 | leere Vitrine mit Stoffboden, unscharf | Hintergrund Befund |

## Wie im Code einbinden

- **Pfad** relativ zum Repository: `brands/military_history/assets/higgsfield/library/<datei>`. Der Renderer verlangt für jede verwendete Datei eine Zeile in `LICENSE.md` desselben Ordners; die Zeilen sind da.
- **Maße:** Quelle 1536 × 2752, Seitenverhältnis 0,558 (fast genau 9:16). Für 1080 × 1920 mit `object-fit: cover` einpassen; der Überstand reicht für eine langsame Kamerafahrt von etwa 5 % ohne Unschärfe.
- **Schleife:** keine. Für Bewegung im Code eine langsame Fahrt oder Skalierung (zum Beispiel 100 → 104 % über die Szene), nie ein Ruck am Szenenwechsel.
- **Karten:** Tinte auf Papier, im Code tönen (Multiplizieren mit Olive oder Papier der Palette). Orte, Linien und Beschriftung setzt weiterhin der Code. Die Küstenlinien stammen aus einem Bildmodell und sind **schematisch**: nie zum Verorten benutzen, im Bild immer der Chip „KARTE SCHEMATISCH · KI-ZEICHNUNG“ (gestricheltes Quadrat).
- **Bildmitte:** Zwischen y 440 und 1100 liegt das Linienmodell. Die Karten sind dort teilweise dicht schraffiert; unter dem Modell einen Schleier aus der Grundfarbe (etwa 0,5–0,6 Deckkraft) legen. Helligkeitswerte je Bild stehen in `manifest.json` unter `check`.
- **Kennzeichnung:** wie bisher „KI-generiert“; Karten zusätzlich mit dem Chip oben.

## Abnahme (durchgeführt am 02.11.2026)

Jedes Bild bei voller Auflösung auf Schrift, Zahlen, Zeichen, Kompassrose, Menschen, Waffen, Fahnen und Fahrzeuge geprüft: kein Fund. Verworfen und nicht abgelegt: K1 Fassung 1 (fotografierter Bogen auf weißem Grund statt randloser Zeichnung). Zwei Versuche für T3 schlugen fehl und wurden gutgeschrieben.

Abweichung vom Prompt-Blatt: Ablage unter `assets\higgsfield\library\` statt `assets\library\`, nach Auftrag der Hauptsitzung (einheitlich für alle Marken).

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Verteilung („Vorschlag so“, 03.11.2026) hat die Sitzung „Bibliotheken“ fotorealistisches Material ergänzt: 28 Bilder und 1 Clip, 72 Credits. Ziel: Die Marken-Sitzung nimmt im Takt von 2 Themen je Tag Bilder aus der Bibliothek, statt neue Credits auszugeben. Die Motive sind die, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** `C:\Automation\faceless-network\brands\military_history\assets\higgsfield\library\`, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und `fl_clip_optical_telegraph.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: Stempel „KI-REKONSTRUKTION“; farbig, nie als Archivfoto ausgeben.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`. Eigenes Testvideo-Material gehört in einen eigenen Ordner mit eigener `LICENSE.md`, nicht in `library\`.

| Datei | Motiv | passt zu |
|---|---|---|
| `fl_real_workbench.jpg` | Holzwerkbank im Tageslicht, Mitte frei | Aufbau Werkbank, Rekonstruktion |
| `fl_real_compass_parchment.jpg` | Haende mit Stechzirkel ueber leerem Pergament | Vermessen, Kartentisch |
| `fl_real_hills_mist.jpg` | Huegelkette im Morgennebel, Sichtachse | Signalketten, Landschaft |
| `fl_real_cliffs.jpg` | Steilkueste, Brandung, grauer Himmel | Kuestenschutz, Leuchtfeuer, Seefahrt |
| `fl_real_writing_room.jpg` | Schreibstube 18. Jh. mit Federkiel und leeren Boegen | Quellenprobe, Verwaltung, Archiv |
| `fl_real_ship_deck.jpg` | Deck eines Segelschiffs mit Tauen, ohne Flaggen und Geschuetze | Seefahrt, Navigation, Versorgung |
| `fl_real_survey_chain.jpg` | Messkette, Messlatten und Pfloecke auf der Wiese | Reihe Vermessen |
| `fl_real_theodolite.jpg` | Messing-Theodolit auf Holzstativ in der Daemmerung | Vermessen, Triangulation |
| `fl_real_chart_table.jpg` | Navigationstisch in der Kajuete mit leerer Seekarte | Navigation, Seefahrt |
| `fl_real_telegraph_desk.jpg` | Telegrafenpult um 1900 mit Morsetaste | Nachrichtentechnik |
| `fl_real_storeroom.jpg` | Vorratsraum mit Dosen ohne Etikett, Faessern, Saecken | Reihe Versorgt |
| `fl_real_earthwork.jpg` | Erdwall mit Graben und Palisade | Befestigung, Rekonstruktion |
| `fl_real_teleprinter.jpg` | Fernschreiber mit Lochstreifen | Nachrichtentechnik 20. Jh. |
| `fl_real_wall_ridge.jpg` | Steinmauerrest auf einem Huegelkamm | Grenzwaelle, Rekonstruktion |
| `fl_real_star_fort.jpg` | Sternfoermige Bastionsmauer mit Graben, ohne Kanonen | Festungsbau |
| `fl_real_fortress_model.jpg` | Holzmodell einer Festungsstadt | Festungsbau, Planung |
| `fl_real_field_kitchen.jpg` | Kupferkessel ueber Holzfeuer, Feldkueche | Reihe Versorgt |
| `fl_real_mail_room.jpg` | Postsaecke und Sortierregal, Briefe ohne Adresse | Feldpost, Versorgung |
| `fl_real_workshop_hall.jpg` | Werkhalle 19. Jh. mit Riemenantrieb | Industrie, Fertigung |
| `fl_real_steel_panels.jpg` | Gestapelte genormte Stahlpaneele auf dem Werkplatz | Vorfertigung, Normung |
| `fl_real_optical_telegraph.jpg` | Optischer Telegraf mit Fluegelarmen bei Tag (Startbild des Clips) | Signalketten, Chappe |
| `fl_real_cipher_discs.jpg` | Drehbare Messingscheiben ohne Buchstaben | Verschluesselung (nur Gegenstand) |
| `fl_real_valve_rack.jpg` | Roehrenregal mit schwachem Gluehen | Funk, Rechentechnik |
| `fl_real_log_line.jpg` | Sanduhr, Logbrett und Leine mit Knoten | Geschwindigkeit auf See |
| `fl_real_balloon.jpg` | Gasballon mit Korb im Nebel | Beobachtung, Aufklaerung |
| `fl_real_pigeon_loft.jpg` | Taubenschlag mit Tauben | Brieftauben, Nachrichten |
| `fl_real_sound_mirror.jpg` | Schallspiegel aus Beton an der Kueste | Fruehwarnung vor dem Radar |
| `fl_real_heliograph.jpg` | Heliograf-Spiegel auf Stativ, Hochebene | Signalgebung mit Licht |
| `fl_clip_optical_telegraph.mp4` | Fluegelarme des optischen Telegrafen wechseln die Stellung; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `fl_real_optical_telegraph.jpg` | Signalketten, Chappe, Codes |

**Verworfen** (nicht abgelegt): Stechzirkel Fassung 1: Wange und Augenpartie im Dreiviertelprofil sichtbar; Sternfestung Fassung 1: verzerrtes Spiegelbild statt Luftbild; Chronometer: Zifferblatt mit roemischen Ziffern; nicht ersetzt (Budget).

**Einbinden:** Im Plan `"assets": {"folder": "assets/higgsfield/library", ...}` (`src\fn\render\assets.py`). Standbilder mit langsamer Fahrt im Code (100 → 104 %); den Clip mit seinem Startbild davor oder danach. Kennzeichnung immer einblenden.
