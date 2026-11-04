# Suitwerk – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Suitwerk (Format 1.0).md`; den Rest der Vorlage schreibt die Suitwerk-Sitzung. Erzeugt nach `Bibliothek Prompt-Blatt.md` mit Higgsfield Ultra (Budget 120 Credits).

**Stand der Erzeugung:** 10 Stoffmuster, 5 Kleidungsdetails und 2 Stimmungs-Startbilder sind abgelegt (40 Credits, davon 6 für drei verworfene Bilder). Die 2 Stimmungs-Schleifen (je 10 Credits) fehlen noch: Seit dem 02.11.2026 etwa 15:29 Wien wird am ganzen Higgsfield-Konto kein Video fertig; die Hauptsitzung hat neue Video-Aufträge angehalten. Bis dahin liegen die Startbilder als `sw_mood_*.jpg` bereit.

**Grundregel:** KI-Bilder zeigen nur, wie ein Stoff im Licht aussieht (Glanz, Haarigkeit, Fall) und geben Stimmung. Sie belegen **nie** eine Bindung, ein Maß oder eine Passform. Die Struktur bleibt im Code (`warp_up` in `brands\menswear\kreidestrich\scenes.py`).

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\menswear\assets\higgsfield\library\`
Kontaktbogen: `index.html`. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json`.

### Stoffmuster, 1:1, 2048 × 2048, Draufsicht mit Streiflicht

| Datei | Stoff | Hinweis |
|---|---|---|
| `sw_fabric_worsted_plain.jpg` | Kammgarn marine, Leinwandbindung, Zackenschnittkante | |
| `sw_fabric_twill.jpg` | Kammgarn-Köper marine, steiler Grat | **Grat läuft von links oben nach rechts unten**, also nicht wie im Prompt-Blatt verlangt (rechts oben nach links unten): nur als Stimmung, nie neben der gezeichneten Bindung |
| `sw_fabric_flannel.jpg` | Flanell grau, angeraut | |
| `sw_fabric_tweed.jpg` | Tweed braun, meliert, mit farbigen Noppen | |
| `sw_fabric_herringbone.jpg` | Fischgrat grau | |
| `sw_fabric_houndstooth.jpg` | Hahnentritt schwarz-weiß | sehr kontrastreich |
| `sw_fabric_glencheck.jpg` | Glencheck grau | |
| `sw_fabric_linen.jpg` | Leinen naturfarben, geknittert | |
| `sw_fabric_seersucker.jpg` | Seersucker blau-weiß | |
| `sw_fabric_mohair.jpg` | Mohair-Mischung marine | Glanz nur schwach sichtbar |

Alle Muster sind Anschauung. Wer ein Muster neben die gezeichnete Vergrößerung stellt („so sieht es aus“), prüft vorher, ob Grat und Bindung zur Zeichnung passen; sonst nur als Stimmung.

### Kleidungsdetails, 1:1, 2048 × 2048

| Datei | Detail |
|---|---|
| `sw_detail_buttonhole.jpg` | Knopfloch am Revers, handgenäht |
| `sw_detail_cuffbuttons.jpg` | vier überlappende Ärmelknöpfe, ohne Prägung |
| `sw_detail_lapeledge.jpg` | abgesteppte Revers-Kante, sehr nah |
| `sw_detail_flappocket.jpg` | Leistentasche mit Patte, darüber eine kleine Ticket-Tasche |
| `sw_detail_lining.jpg` | Sakko innen, halb gefüttert, ohne Etikett |

### Stimmung, 9:16

| Datei | Motiv | Form |
|---|---|---|
| `sw_mood_cuttingtable` | Zuschneidetisch von oben: marineblaues Tuch, Kreide, Zackenschere, Nadeln; Lampenlicht von links oben | Startbild `.jpg` da (1536 × 2752); Schleife `.mp4` folgt |
| `sw_mood_dressform` | Schneiderbüste vor dunkler Wand, Sakko ohne Ärmel, Streiflicht | wie oben |

## Wie im Code einbinden

- **Pfad:** Im Plan `"assets": {"folder": "assets/higgsfield/library", ...}` (`src\fn\render\assets.py`). Je verwendeter Datei steht eine Zeile in `LICENSE.md` desselben Ordners.
- **Felder** (laut Prompt-Blatt, baut die Suitwerk-Sitzung): `kw_hook.backdrop` und `kw_close.backdrop` nehmen `sw_mood_*` unter einem dunklen Schleier; `kw_flip.photo` nimmt ein Stoffmuster oder Detail neben der Zeichnung, mit Stempel „KI-Bild“.
- **Maße:** Stoffe und Details quadratisch; im Hochformat als Karte oder Ausschnitt setzen, nicht strecken. Stimmungsbilder 9:16, für 1080 × 1920 mit `cover` einpassen.
- **Schleife:** `sw_mood_*.mp4` werden Schleifen (1080 × 1920, 24 s, stumm). Bis dahin das `.jpg` mit langsamer Fahrt im Code. Stoffe und Details sind Standbilder.
- **Helligkeit:** Die Stimmungsbilder sind in der Mitte dunkel (9–21 %), Elfenbein-Schrift steht darauf ohne Schleier. Die Stoffe reichen von 13 % (Kammgarn) bis 68 % (Seersucker); auf hellen Stoffen keine Schrift ohne eigene Fläche.
- **Kennzeichnung:** „KI-Bild“ am Bild, dazu wie bisher „KI-generiert“.

## Abnahme (durchgeführt am 02.11.2026)

Jedes Bild auf Schrift, Logos, Etiketten, geprägte Knöpfe und Hände geprüft, Stimmungsbilder zusätzlich vergrößert. Verworfen und nicht abgelegt: Zuschneidetisch Fassung 1 (Maßband mit Pseudo-Ziffern), Büste Fassung 1 (Regal mit markentypischen Nähmaschinen-Silhouetten), Tasche Fassung 1 (aufgesetzte Knopftasche statt Leistentasche).

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Testvideos (03.11.2026, „Alle freigeben“) hat die Sitzung „Bibliotheken“ wiederverwendbares, fotorealistisches Material ergänzt (Neustart-Plan, Abschnitt 10). Ziel: Die Marken-Sitzung kann im Takt von 2 Themen je Tag Bilder aus der Bibliothek nehmen, statt neue Credits auszugeben. Auswahl der Motive: die Motive, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** derselbe Ordner wie oben, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und der Clip `sw_clip_chalk_line.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: Stempel „KI-Bild“; KI-Bilder belegen nie Bindung, Maß oder Passform.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`.

| Datei | Motiv | passt zu |
|---|---|---|
| `sw_real_back_suit.jpg` | Mann im marineblauen Anzug von hinten (Hinterkopf sichtbar, kein Gesicht) | Anprobe, Passform, Schulter |
| `sw_real_threadcounter.jpg` | Messing-Fadenzaehler auf Kammgarn, ohne Skala | Reihe Unter dem Fadenzaehler |
| `sw_real_chalk_line.jpg` | Hand zieht Kreidestrich ueber Tuch | Leitbild Kreidestrich, fast jedes Thema |
| `sw_real_pinning.jpg` | Schneiderhaende stecken Sakko am Ruecken ab (Traeger von hinten) | Anprobe, Aenderung, Passform |
| `sw_real_swatch_fan.jpg` | Aufgefaecherte Tuchmuster ohne Etiketten | Stoffkunde, Stoffwahl |
| `sw_real_trouser_break.jpg` | Hosenbein mit Buegelfalte ueber Oxford-Schuh | Hosenlaenge, Bruch, Nachgemessen |
| `sw_real_shoes.jpg` | Vier Schuhe: Oxford und Derby, schwarz und braun | Schuhe, Kleiderordnung |
| `sw_real_yarn.jpg` | Garnkonen und Rohwolle | Faser, Garn, Super-Zahl |
| `sw_real_tuxedo.jpg` | Smoking flach mit Hemd und Fliege | Kleiderordnung Black Tie |
| `sw_real_pattern_table.jpg` | Zuschneidetisch mit Papierschnitt und Schere | Schnitt, Massanfertigung |
| `sw_real_three_patterns.jpg` | Fischgrat, Hahnentritt, Glencheck nebeneinander | Muster, Stoffkunde |
| `sw_real_shirts.jpg` | Drei gefaltete weisse Hemden, Kragen sichtbar | Hemd, Kragen, Kleiderordnung |
| `sw_real_tie_tying.jpg` | Haende binden Krawatte (Blick von oben) | Krawatte, Knoten |
| `sw_real_wardrobe.jpg` | Anzug auf Holzbuegel im Schrank | Pflege, Lagerung, Grundgarderobe |
| `sw_real_cuff_back.jpg` | Mann im grauen Anzug richtet Manschette (von hinten, Hinterkopf sichtbar) | Aermellaenge, Manschette, Passform |
| `sw_real_loom.jpg` | Webstuhl mit Kettfaeden und Schiffchen | Bindung, Weben (nur Stimmung, kein Beleg) |
| `sw_real_waistcoat.jpg` | Weste flach gelegt (unterster Knopf im Bild nicht eindeutig offen) | Weste, Dreiteiler |
| `sw_clip_chalk_line.mp4` | Hand zieht Kreidestrich ueber das Tuch; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `sw_real_chalk_line.jpg` | Leitbild Kreidestrich, Einstieg und Uebergaenge |

**Einbinden:** wie oben, Ordner `assets/higgsfield/library`. Für einen Clip ohne Schleife das Startbild als Standbild davor oder danach setzen. Bei Bildern mit Händen oder Menschen immer die Kennzeichnung oben einblenden.
