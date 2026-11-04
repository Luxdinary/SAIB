# Dewlane – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Dewlane (Format 1.0).md`; den Rest der Vorlage schreibt die Dewlane-Sitzung. Erzeugt nach `Bibliothek Prompt-Blatt.md` mit Higgsfield Ultra (Budget 120 Credits).

**Stand der Erzeugung:** 8 Produktfotos und 6 Textur-Startbilder sind abgelegt (30 Credits, davon 2 für einen verworfenen Tiegel). Die 6 Textur-Schleifen (je 10 Credits) sind noch nicht da: Seit dem 02.11.2026 etwa 15:29 Wien wird am ganzen Higgsfield-Konto kein Video fertig; die Hauptsitzung hat neue Video-Aufträge angehalten. Bis sie kommen, liegen die Startbilder als `dl_tex_*.jpg` bereit; sobald eine Schleife da ist, kommt `dl_tex_*.mp4` dazu und dieses Blatt wird nachgeführt.

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\beauty\assets\higgsfield\library\`
Kontaktbogen: `index.html`. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json` (mit Helligkeitswerten je Bild unter `check`).

### Texturen (Hintergrund hinter Lupe, Mengen- und Schlussszene)

| Datei | Motiv | Form |
|---|---|---|
| `dl_tex_cream` | Cremeschliere auf Porzellan | Startbild `.jpg` da; Schleife `.mp4` folgt |
| `dl_tex_gel` | blassrosa Gel mit Luftbläschen | wie oben |
| `dl_tex_serum` | goldener Serumtropfen über Elfenbein mit Welle | wie oben |
| `dl_tex_foam` | feiner weißer Schaum | wie oben |
| `dl_tex_film` | dünner Lotionsfilm auf Keramik (nicht Haut) | wie oben |
| `dl_tex_powder` | blassrosa Puderwolke in einer Schale | wie oben |

### Neutrale Produktfotos (Vorlage für die Bühne)

| Datei | Motiv |
|---|---|
| `dl_prod_tube.jpg` | Tube auf dem Deckel stehend |
| `dl_prod_jar.jpg` | Tiegel geschlossen, frontal |
| `dl_prod_jar_open.jpg` | Tiegel offen mit Creme, Deckel angelehnt |
| `dl_prod_dropper.jpg` | Pipettenflasche Braunglas, Mauve-Pipette |
| `dl_prod_pump.jpg` | Pumpflasche |
| `dl_prod_spray.jpg` | Sprühdose (Deo) |
| `dl_prod_bottle.jpg` | Flasche mit Klappdeckel |
| `dl_prod_group.jpg` | Gruppe Tube, Tiegel, Pipette, Pumpflasche auf Sockel, obere Hälfte frei |

Alle Produkte sind leer: keine Schrift, kein Etikett, kein Logo, keine bekannte Verpackungsform (bei voller Auflösung geprüft). Hintergrund einheitlich Elfenbein, Licht von links oben, frontal auf Augenhöhe.

## Wie im Code einbinden

- **Pfad:** Im Plan unter `assets` den Ordner setzen: `"assets": {"folder": "assets/higgsfield/library", "background": {"nh_lens": "dl_tex_cream.mp4", ...}, "scrim": 0.55}` (`src\fn\render\assets.py`). Der Renderer verlangt je verwendeter Datei eine Zeile in `LICENSE.md` desselben Ordners; die Zeilen sind da.
- **Maße:** Standbilder 1536 × 2752 (9:16), JPEG. Schleifen werden 1080 × 1920, 24 s (8-s-Quelle dreimal aneinander), H.264, stumm, wie bei Scutoria.
- **Schleife:** Texturen als `.mp4` sind Schleifen (Start- und Endbild gleich). Bis dahin das `.jpg` als Standbild mit langsamer Fahrt im Code (100 → 104 %).
- **Bildmitte:** Die Textzone y 290–1100 ist bei allen Texturen hell (mittlere Helligkeit 83–93 % laut `manifest.json`). Am unruhigsten sind dort Gel und Puder (Streuung 13 bzw. 11, die anderen 2–6); bei ihnen einen hellen Schleier `scrim` unter den Text legen.
- **Produktfotos:** Nur verwenden, wenn das Foto neben dem Code-Etikett ruhig wirkt; das Etikett (Kategorie, Kennzahl) setzt immer der Code über das Foto. Sonst bleibt das SVG-Produkt.
- **Kennzeichnung:** Szenen mit diesen Motiven zusätzlich „KI-Bild“ in der Ecke; der Stempel „Animation · neutrales Produkt · kein Produkttest“ bleibt.

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Testvideos (03.11.2026, „Alle freigeben“) hat die Sitzung „Bibliotheken“ wiederverwendbares, fotorealistisches Material ergänzt (Neustart-Plan, Abschnitt 10). Ziel: Die Marken-Sitzung kann im Takt von 2 Themen je Tag Bilder aus der Bibliothek nehmen, statt neue Credits auszugeben. Auswahl der Motive: die Motive, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** derselbe Ordner wie oben, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und der Clip `dl_clip_spray_mist.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: „KI-Bild · Veranschaulichung“ auf jedem Bild mit Händen.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`.

| Datei | Motiv | passt zu |
|---|---|---|
| `dl_real_pump_palm.jpg` | Hand drueckt Pumpflasche, Lotion in die Handflaeche | Anwendung, Menge, Pumpspender |
| `dl_real_shelf.jpg` | Badablage mit neutraler Tube, Tiegel, Pumpe, Spray | Einstieg, Alltag, Vergleich |
| `dl_real_shampoo_hands.jpg` | Haende mit Shampooschaum in der Dusche | Haarpflege, Tenside, Konservierung |
| `dl_real_two_bottles.jpg` | Zwei neutrale Flaschen nebeneinander, oben frei | Direkter Vergleich (Etiketten setzt der Code) |
| `dl_real_tube_back.jpg` | Hand dreht Tube, leere Rueckseite | Packungsangabe, INCI (Text setzt der Code) |
| `dl_real_magnifier.jpg` | Hand mit Lupe ueber leerer Tubenrueckseite | Reihe Unter der Lupe, Packungsangaben |
| `dl_real_beach_towel.jpg` | Sonnencreme-Tube auf Strandtuch, Mittagssonne | Sonnenschutz |
| `dl_real_jar_spatula.jpg` | Offener Tiegel von oben, Spatelspur | Hygiene, Haltbarkeit nach dem Oeffnen, Textur |
| `dl_real_fingers_strand.jpg` | Strang Sonnencreme auf zwei Fingern, Teeloeffel daneben | Menge, Zwei-Finger-Regel, Sonnenschutz |
| `dl_real_dropper_fingertip.jpg` | Pipette, Tropfen faellt auf Fingerspitze | Seren, Oele, Wirkstoffe |
| `dl_real_swatches.jpg` | Vier Texturen auf Glasplatte: Gel, Lotion, Creme, Balsam | Textur, Formulierung, Vergleich |
| `dl_real_spray_backlit.jpg` | Spruehnebel aus neutraler Flasche im Gegenlicht (Pumpzerstaeuber) | Sprays, Treibgas, Sonnenspray |
| `dl_real_perfume.jpg` | Neutraler Parfumflakon mit Spruehstoss | Duftstoffe, Allergene, Parfum |
| `dl_real_eyeshadow.jpg` | Lidschatten-Palette ohne Marke, Pinsel | Farbstoffe, CI-Nummern, Puder |
| `dl_real_soap.jpg` | Seifenstueck mit Schaum auf Schale | Seife, Tenside, pH |
| `dl_real_twophase_pad.jpg` | Zweiphasenflasche, Wattepad wird getraenkt | Reinigung, Abschminken |
| `dl_real_hair_dye.jpg` | Haende in Handschuhen mischen Haarfarbe | Haarfarbe, Allergietest-Hinweise laut Quelle |
| `dl_real_deo_pair.jpg` | Deo-Stick neben Spruehdose | Deo und Antitranspirant |
| `dl_clip_spray_mist.mp4` | Spruehnebel aus neutraler Flasche im Gegenlicht; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `dl_real_spray_backlit.jpg` | Sprays, Sonnenspray, Treibgas |

**Einbinden:** wie oben, Ordner `assets/higgsfield/library`. Für einen Clip ohne Schleife das Startbild als Standbild davor oder danach setzen. Bei Bildern mit Händen oder Menschen immer die Kennzeichnung oben einblenden.
