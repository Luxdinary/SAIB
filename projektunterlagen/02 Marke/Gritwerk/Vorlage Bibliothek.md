# Gritwerk – Vorlage, Teil Bibliothek

Stand: 02.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Gritwerk (Format 1.0).md`; den Rest der Vorlage schreibt die Gritwerk-Sitzung. Erzeugt nach `Bibliothek Prompt-Blatt.md` (Kern A „Laborbuch“, von Stefan am 02.11.2026 entschieden) mit Higgsfield Ultra, Budget 100 Credits.

**Stand der Erzeugung:** Die Standbilder G1–G6 und die Thumbnail-Gründe T1–T6 sind abgelegt (30 Credits, davon 6 für drei verworfene Bilder). Die vier Clips V1–V4 (je 10 Credits) fehlen noch: Seit dem 02.11.2026 etwa 15:29 Wien wird am ganzen Higgsfield-Konto kein Video fertig, und die Hauptsitzung hat neue Video-Aufträge angehalten. Startbilder für V1 (G1) und V4 (G2) liegen bereit.

**Grundregel:** Der Kern bleibt Code (Laborbuchseite, Punkte, Balken, Stempel). Die Bilder geben nur Atmosphäre um die Seite und Material für Thumbnails. Keine Menschen, Hände oder Silhouetten, keine Schrift, Zahlen oder Diagramme.

## Was es gibt

Ordner: `C:\Automation\faceless-network\brands\motivation\assets\higgsfield\library\`
Kontaktbogen: `index.html`. Nachweis je Datei (Job-Nummer, Modell, Credits, Prompt): `LICENSE.md`. Maschinenlesbar: `manifest.json`.

Alle Bausteine sind Standbilder, JPEG, **1536 × 2752** (9:16).

| Datei | Nr. | Motiv | Einsatz |
|---|---|---|---|
| `gw_desk_top.jpg` | G1 | Schreibtisch von oben unter Lampenlicht, Mitte frei | `LAYER` statt gezeichnetem Raum, unter Schleier; Startbild für V1 |
| `gw_desk_low.jpg` | G2 | Schreibtisch schräg (30°), geringe Schärfentiefe | Einstieg; Startbild für V4 |
| `gw_readingroom.jpg` | G3 | Lesesaal unscharf, grüne Leselampen | Hintergrund bei Lernlabor-Themen |
| `gw_labbench.jpg` | G4 | Laborbank neutral: Klemmbrett leer, Stiftebecher, Becherglas ohne Skala | Aufbau und Messung, nie als Behauptung einer echten Messung. **Ohne Stoppuhr:** zwei Versuche mit Uhr zeigten ein Zifferblatt mit Ziffern und wurden verworfen |
| `gw_paper_grid.jpg` | G5 | Karopapier Makro | Füllung der Laborbuchseite; das Raster (32 px) und der rote Doppelrand bleiben Code |
| `gw_paper_card.jpg` | G6 | Karteikarte mit radierten Bleistiftspuren, nichts lesbar | Notizkarten, „Dein Versuch“ |
| `gw_thumb_desk_a.jpg` | T1 | Schreibtisch, starker Kontrast, Mitte dunkel | Thumbnail |
| `gw_thumb_desk_b.jpg` | T2 | Schreibtisch mit diagonalem Lichtstreifen, offenes leeres Heft | Thumbnail |
| `gw_thumb_reading_a.jpg` | T3 | Lesesaal, Lampen an den Rändern | Thumbnail |
| `gw_thumb_reading_b.jpg` | T4 | Lesesaal, Lampen oben, Mitte sehr dunkel (6 %) | Thumbnail |
| `gw_thumb_bench_a.jpg` | T5 | Laborbank mit Stehlampe | Thumbnail |
| `gw_thumb_bench_b.jpg` | T6 | Laborbank nah, Klemmbrett unten | Thumbnail |

Ausstehend (nach Freigabe der Hauptsitzung): V1 Staub im Lampenlicht (Schleife aus G1), V2 Notizbuchseite blättert (Makro), V3 analoge Stoppuhr (nur Teilstriche, keine Ziffern; muss geprüft werden), V4 Lampe geht an (aus G2).

## Wie im Code einbinden

- **Pfad:** relativ zum Repository `brands/motivation/assets/higgsfield/library/<datei>`; für Pläne mit `assets`-Block `"folder": "assets/higgsfield/library"` (`src\fn\render\assets.py`). Je Datei steht eine Zeile in `LICENSE.md` desselben Ordners.
- **Laborbuchseite:** liegt im Video bei x 92–952, y 300–1146. G1 und G2 haben dort dunkle, ruhige Flächen (mittlere Helligkeit 32 % bzw. 17 %); die Seite liegt deckend darüber, ein Schleier ist nur für die Ränder nötig.
- **Maße:** 1536 × 2752; für 1080 × 1920 mit `cover` einpassen. Bewegung im Code (langsame Fahrt 100 → 104 %), bis V1–V4 da sind.
- **Thumbnails:** Titel und Stempel in die dunkle Mitte; Gold `#E5B45A` nur als Akzent aus dem Code.
- **Kennzeichnung:** Jedes Bild im Video als KI-Darstellung („KI-generiert“).

## Abnahme (durchgeführt am 02.11.2026)

Probe zuerst G1 allein (verworfen wegen einer ins Bild gesetzten, abgerundeten Rahmenkante; Fassung 2 randlos). Dann G2–G6 und T1–T6. Jedes Bild auf Menschen, Hände, Silhouetten, Schrift, Zahlen und Logos geprüft, Details vergrößert. Verworfen: G1 Fassung 1 (Rahmen), G4 Fassung 1 und 2 (Uhr mit Ziffern).

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Verteilung („Vorschlag so“, 03.11.2026) hat die Sitzung „Bibliotheken“ fotorealistisches Material ergänzt: 27 Bilder und 1 Clip, 74 Credits. Ziel: Die Marken-Sitzung nimmt im Takt von 2 Themen je Tag Bilder aus der Bibliothek, statt neue Credits auszugeben. Die Motive sind die, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** `C:\Automation\faceless-network\brands\motivation\assets\higgsfield\library\`, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und `gw_clip_phone_buzz.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: „KI-Darstellung“; nie als Aufnahme einer echten Studie oder Einrichtung ausgeben.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`. Eigenes Testvideo-Material gehört in einen eigenen Ordner mit eigener `LICENSE.md`, nicht in `library\`.

| Datei | Motiv | passt zu |
|---|---|---|
| `gw_real_cubicle.jpg` | Versuchskabine, Person von hinten | Reihe Laborbuch, Nachstellung |
| `gw_real_lecture_hall.jpg` | Hoersaal, Studierende von hinten | Lernen, Studien mit Studierenden |
| `gw_real_test_sheet.jpg` | Hand mit Stift ueber Testbogen | Tests, Abfragen |
| `gw_real_stopwatch_hand.jpg` | Stoppuhr ohne Ziffern in der Hand | Messung, Zeit |
| `gw_real_textbook_highlighter.jpg` | Haende blaettern im Lehrbuch, Textmarker | Lernstrategien |
| `gw_real_laptop_headphones.jpg` | Person von hinten am Laptop mit Kopfhoerer | Konzentration, Online-Versuch |
| `gw_real_index_cards.jpg` | Haende mit leeren Karteikarten | Abfragen, Wiederholen |
| `gw_real_phone_facedown.jpg` | Handy mit Display nach unten neben Lernmaterial (Startbild des Clips) | Ablenkung, Unterbrechung |
| `gw_real_checklist.jpg` | Hand hakt Kaestchen auf leerer Liste ab | Gewohnheiten, Wenn-dann-Plaene |
| `gw_real_classroom.jpg` | Leeres Klassenzimmer, leere Tafel | Schule, Lernen (ohne Kinder) |
| `gw_real_open_office.jpg` | Grossraumbuero, Menschen von hinten | Arbeit, Fokus im Alltag |
| `gw_real_wall_calendar.jpg` | Wandkalender als Raster ohne Zahlen, Hand setzt Markierung | Planen, Fristen, Gewohnheiten |
| `gw_real_sticky_wall.jpg` | Moderationswand mit leeren Haftzetteln | Planen, Brainstorming |
| `gw_real_hand_writing.jpg` | Hand schreibt mit Stift | Mitschreiben, Expressives Schreiben |
| `gw_real_keyboard_hands.jpg` | Haende auf Tastatur ohne Beschriftung | Mitschreiben am Laptop |
| `gw_real_meeting_standing.jpg` | Gruppe am Stehtisch von hinten | Stehen statt Sitzen, Gruppen |
| `gw_real_hallway_walk.jpg` | Person geht im Flur, von hinten | Pausen, Bewegung, Wege |
| `gw_real_stamp_card.jpg` | Stempelkarte mit leeren Kreisen im Cafe | Belohnung, Fortschritt |
| `gw_real_messy_desk.jpg` | Unordentlicher Schreibtisch | Ordnung, Paar mit aufgeraeumt |
| `gw_real_tidy_desk.jpg` | Aufgeraeumter Schreibtisch | Ordnung, Paar mit unordentlich |
| `gw_real_moving_boxes.jpg` | Studentenzimmer mit Umzugskartons | Neuanfang, Gewohnheiten aendern |
| `gw_real_cinema_popcorn.jpg` | Kinoreihe von hinten, Hand in Popcorntuete | Gewohnheit, Automatismen |
| `gw_real_tablet_tiles.jpg` | Tablet mit abstrakten Farbkacheln | Versuche am Bildschirm |
| `gw_real_window_green.jpg` | Buerofenster mit Blick auf Gruendach | Natur und Aufmerksamkeit, Paar mit Betondach |
| `gw_real_window_concrete.jpg` | Buerofenster mit Blick auf Betondach | Paar mit Gruendach |
| `gw_real_jam_jars.jpg` | Marmeladenglaeser ohne Etikett am Probierstand | Auswahl, zu viele Optionen |
| `gw_real_flatpack.jpg` | Haende bauen Moebel aus Flachpaket | IKEA-Effekt (ohne Marke) |
| `gw_clip_phone_buzz.mp4` | Handy vibriert neben dem Buch, die Hand zoegert; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `gw_real_phone_facedown.jpg` | Ablenkung, Unterbrechung, Multitasking |

**Verworfen** (nicht abgelegt): Testbogen Fassung 1: lesbare Ziffern; Checkliste Fassung 1: halb lesbare Ueberschrift; Wandkalender Fassung 1: Jahreszahl und Wochentage lesbar; Besprechung im Sitzen: Bild um 90 Grad gedreht, Profile sichtbar; nicht ersetzt (Budget); Lernende vor Whiteboard: Kursleiter von vorn mit Gesicht; nicht ersetzt (Budget).

**Einbinden:** Im Plan `"assets": {"folder": "assets/higgsfield/library", ...}` (`src\fn\render\assets.py`). Standbilder mit langsamer Fahrt im Code (100 → 104 %); den Clip mit seinem Startbild davor oder danach. Kennzeichnung immer einblenden.
