# Gigastruct – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Gigastruct (Format 1.0).md`; den Rest der Vorlage schreibt die Gigastruct-Sitzung.

## Rahmen

Die freigegebene `Format-Bibel.md` schließt in Regel 9 Fotos und KI-Bilder realer Bauwerke aus und grenzt Gigastruct in Abschnitt 5 mit „keine KI-Bilder, keine Fotorealistik“ ab. Sie geht vor dem Ausgabeplan, der „Baustellen- und Luftbilder“ vorsah. Nach Freigabe der Hauptsitzung (02.11.2026) gibt es deshalb nur **Werkplan-Material ohne Bauwerk**: Papier, Zeichentisch, Himmel. Erzeugt wurden 11 Standbilder für **22 Credits** (Rahmen höchstens 40, Ausgabeplan 120); **98 Credits** gehen an die Reserve. Ein eigenes Prompt-Blatt gab es nicht; die Prompts stehen je Datei in `LICENSE.md`.

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\megaconstruction\assets\higgsfield\library\`
Kontaktbogen: `index.html`. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json`.

Alle Bausteine sind **Standbilder**, JPEG, **1536 × 2752** (9:16), keine Schleifen.

| Datei | Motiv | Helligkeit Mitte | Vorschlag Szene |
|---|---|---|---|
| `gs_paper_drafting.jpg` | Zeichenblatt stahlblau, leer, Papierstruktur | 34 % | Grund unter dem Zeichnungsrahmen, alle Szenen |
| `gs_paper_tracing.jpg` | Transparentpapier hell, leichte Kreuzfalte | 79 % | Schriftfeld `gb_close`, Stückliste |
| `gs_paper_grid.jpg` | Karopapier hell, jede fünfte Linie stärker | 93 % | Rechenblatt `gb_calc` |
| `gs_paper_grid_dark.jpg` | Karopapier dunkel stahlblau | 22 % | dunkles Rechenblatt, Lastfall-Kasten |
| `gs_paper_mm.jpg` | Millimeterpapier hell | 94 % | Rechenblatt, Skala in `gb_proof` |
| `gs_table_drafting.jpg` | Zeichentisch von oben bei Tag: leerer Bogen, Bleistift, Zirkel, Zeichendreieck ohne Skala | 72 % | Einstieg `gb_task`, Schluss `gb_close` |
| `gs_table_night.jpg` | Zeichentisch bei Nacht: stahlblauer Bogen, Bleistift, Zirkel, Papierrolle | 43 % | wie oben |
| `gs_sky_dusk.jpg` | Himmelsverlauf Abend `#10223A` → `#4B6F8F`, wolkenlos | 35 % | hinter der Himmelskuppel, `gb_task` |
| `gs_sky_day.jpg` | Himmel Tag, gedämpft, feine hohe Wolken | 60 % | `gb_principle`, `gb_build` |
| `gs_sky_storm.jpg` | Sturmwolken mit Regenschleiern | 28 % | Lastfall Wind `gb_load` (Stimmung, kein echtes Ereignis) |
| `gs_sky_fog.jpg` | Dunst in Stahlblau und Grau | 56 % | `gb_proof`, Übergänge |

Kein Bild zeigt ein Bauwerk, eine Landschaft, Schrift, Ziffern oder eine Skala (bei voller Auflösung geprüft).

## Wie im Code einbinden

- **Pfad:** relativ zum Repository `brands/megaconstruction/assets/higgsfield/library/<datei>`. Für Pläne mit `assets`-Block den Ordner setzen: `"folder": "assets/higgsfield/library"` (`src\fn\render\assets.py`). Je Datei steht eine Zeile in `LICENSE.md` desselben Ordners. Die 3D-Ebene (`render\gigastruct3d.js`) kann die Himmel als Textur der Kuppel oder als CSS-Hintergrund hinter dem Canvas nehmen.
- **Maße:** 1536 × 2752; für 1080 × 1920 mit `cover` einpassen. Langsame Fahrt im Code (100 → 104 %) statt Video.
- **Farbe:** Papier und Himmel sind an `brand.yaml` angelehnt (`bg #20384F`, `sky_top #10223A`, `haze #4B6F8F`, `grid #3A5874`). Orange `#FF8A2A` kommt nur aus dem Code.
- **Lesbarkeit:** Auf den hellen Papieren (Karo, Millimeter, Transparent) steht dunkle Schrift; auf Zeichenblatt, dunklem Karo, Abendhimmel und Sturm die helle Schrift `#E9EDF0`. Beim Nacht-Zeichentisch ist die Mitte unruhig (Bogen hell, Rand dunkel): Text nur auf eigener Fläche.
- **Kennzeichnung:** „KI-generiert“ wie bisher; da kein Bauwerk zu sehen ist, braucht es keine Plakette „schematisch“ für diese Flächen.

## Abnahme (durchgeführt am 02.11.2026)

Probe zuerst (Karopapier, Abendhimmel), dann der Rest. Ein Auftrag (Zeichenblatt, erster Versuch) schlug fehl und wurde gutgeschrieben. Kein Bild verworfen.

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Testvideos (03.11.2026, „Alle freigeben“) hat die Sitzung „Bibliotheken“ wiederverwendbares, fotorealistisches Material ergänzt (Neustart-Plan, Abschnitt 10). Ziel: Die Marken-Sitzung kann im Takt von 2 Themen je Tag Bilder aus der Bibliothek nehmen, statt neue Credits auszugeben. Auswahl der Motive: die Motive, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** derselbe Ordner wie oben, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und der Clip `gs_clip_concrete_pour.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: „KI-Darstellung · kein Foto“; die historische Baustelle nie als Archivfoto ausgeben.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`.

| Datei | Motiv | passt zu |
|---|---|---|
| `gs_real_engineer_plan.jpg` | Ingenieur von hinten mit Plan vor Baustelle | Bauaufgabe, Einstieg fast jedes Thema |
| `gs_real_cranes_aerial.jpg` | Krane ueber Hochhaus-Rohbau, Luftbild Daemmerung | Tuerme, Hochhaeuser |
| `gs_real_tbm_cutter.jpg` | Schneidrad einer Tunnelbohrmaschine, Mensch als Massstab | Tunnel |
| `gs_real_surveyor.jpg` | Vermesser von hinten am Tachymeter | Vermessung, Nachgerechnet |
| `gs_real_historic_site.jpg` | Historische Baustelle um 1900, Sepia (als KI-Darstellung kennzeichnen, nie als Archivfoto) | Reihe Damals geloest |
| `gs_real_tunnel_portal.jpg` | Tunnelportal im Gebirge mit Baustelleneinrichtung (Fassung 2, ohne Fahrzeuge) | Tunnel, Gebirge |
| `gs_real_concrete_pour.jpg` | Beton fliesst aus dem Pumpenschlauch in die Schalung | Bau, Beton, Damm, Pfeiler |
| `gs_real_cantilever_pier.jpg` | Bruecke im Freivorbau ueber Tal | Bruecken |
| `gs_real_sea_bridge.jpg` | Lange Meeresbruecke, Pfeilerreihe bis zum Horizont | Bruecken, Nachgerechnet (Laenge) |
| `gs_real_pylon_cable.jpg` | Pylon mit Hauptkabel, Arbeiter von hinten auf dem Laufsteg | Haengebruecken, Seile |
| `gs_real_dam_crest.jpg` | Staumauer-Krone mit Stausee, Luftbild | Daemme, Wasserdruck |
| `gs_real_lock_filling.jpg` | Schleusenkammer, Wasser stroemt ein | Schleusen, Kanaele |
| `gs_real_rivets.jpg` | Nietreihe an altem Stahltraeger, Makro | Stahlbau, Damals geloest |
| `gs_real_heavy_lift.jpg` | Schwerlastkran hebt Stahlsegment | Montage, Bruecken |
| `gs_real_surge_barrier.jpg` | Sturmflut-Sperrwerk mit Stahltor | Sturmflut, Kuestenschutz |
| `gs_real_piling_rig.jpg` | Bohrpfahlgeraet auf dem Baugrund | Gruendung, Baugrund |
| `gs_real_cavern.jpg` | Felskaverne mit Arbeitslicht, Mensch winzig | Kavernen, Forschungsanlagen, Tunnel |
| `gs_real_dredger_jet.jpg` | Baggerschiff spuelt Sand auf (Landgewinnung) | Landgewinnung, Inseln |
| `gs_clip_concrete_pour.mp4` | Beton fliesst aus dem Pumpenschlauch in die Schalung; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `gs_real_concrete_pour.jpg` | Bau, Beton, Damm, Pfeiler |

**Einbinden:** wie oben, Ordner `assets/higgsfield/library`. Für einen Clip ohne Schleife das Startbild als Standbild davor oder danach setzen. Bei Bildern mit Händen oder Menschen immer die Kennzeichnung oben einblenden.
