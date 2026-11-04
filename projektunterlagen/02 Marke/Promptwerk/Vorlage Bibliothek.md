# Promptwerk – Vorlage, Teil Bibliothek

Stand: 03.11.2026 (Wien), Sitzung „Bibliotheken“. Dieser Teil gehört in `Vorlage Promptwerk (Format 1.0).md`; den Rest der Vorlage schreibt die Promptwerk-Sitzung.

**Geändert gegenüber dem 02.11.2026:** Damals bekam Promptwerk keine KI-Bausteine, weil die Format-Bibel KI-Bilder ausschloss. Mit dem Neustart (03.11.2026) und Stefans Freigabe der Verteilung gilt: Higgsfield-Bilder sind als Zwischen- und Kontextbilder erlaubt, die echte Aufzeichnung bleibt der Kern. Die Format-Bibel (Abschnitte 2 und 5) sagt noch „keine KI-Bilder“; das zieht die Promptwerk-Sitzung nach.

## Realbilder (03.11.2026)

Nach Stefans Freigabe der Verteilung („Vorschlag so“, 03.11.2026) hat die Sitzung „Bibliotheken“ fotorealistisches Material ergänzt: 29 Bilder und 1 Clip, 68 Credits. Ziel: Die Marken-Sitzung nimmt im Takt von 2 Themen je Tag Bilder aus der Bibliothek, statt neue Credits auszugeben. Die Motive sind die, die im Konzeptplan über die meisten Themen wiederkehren.

- **Ort:** `C:\Automation\faceless-network\brands\claude_workflows\assets\higgsfield\library\`, Dateien `*_real_*.jpg` (1536 × 2752, 9:16, JPEG) und `pw_clip_toggle_switch.mp4`.
- **Regeln:** Hände und Menschen nur von hinten, keine Gesichter, keine echten Marken, keine lesbare Schrift. Kennzeichnung: „KI-Bild“; nur Zwischen- und Kontextbild, die echte Aufzeichnung bleibt der Kern.
- **Nachweis:** Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md`, Prüfwerte in `manifest.json`, Vorschau in `index.html`. Eigenes Testvideo-Material gehört in einen eigenen Ordner mit eigener `LICENSE.md`, nicht in `library\`.

| Datei | Motiv | passt zu |
|---|---|---|
| `pw_real_desk_night.jpg` | Schreibtisch frontal bei Nacht, Laptop zu | Aufbau A Anfang und Ende |
| `pw_real_toggle_panel.jpg` | Kippschalterleiste ohne Beschriftung (Startbild des Clips) | Reihe Gleicher Auftrag, anderer Schalter |
| `pw_real_two_notes.jpg` | Zwei leere Haftzettel, gelb und blau | Vergleich zweier Laeufe |
| `pw_real_binders.jpg` | Aktenregal mit Ordnern ohne Rueckenschrift | Ablage, Dokumente |
| `pw_real_note_monitor.jpg` | Haftzettel am ausgeschalteten Monitor | Erinnerung, Regel |
| `pw_real_cabinet_lock.jpg` | Schloss an Aktenschrankschublade | Rechte, Sperren, Deny-Regel |
| `pw_real_stamp_pads.jpg` | Rotes und gruenes Stempelkissen mit Stempel | Freigabe, Ablehnung |
| `pw_real_inbox_full.jpg` | Uebervoller Ablagekorb (vorher) | Vorher-nachher Ordnung |
| `pw_real_inbox_sorted.jpg` | Sortierter Ablagekorb (nachher) | Vorher-nachher Ordnung |
| `pw_real_clipboard_checked.jpg` | Klemmbrett mit abgehakter Liste | Pruefung, erledigt |
| `pw_real_stopwatch_keyboard.jpg` | Stoppuhr ohne Ziffern neben Tastatur | Laufzeit, Dauer |
| `pw_real_cashbox_key.jpg` | Metallkassette mit Schluessel neben Laptop | Geheimnisse, Zugangsdaten |
| `pw_real_tool_wall.jpg` | Werkzeugwand mit leeren Halterungen | Werkzeuge, Rechte, fehlende Tools |
| `pw_real_handover.jpg` | Zweiter Arbeitsplatz, Mappe wird uebergeben | Uebergabe, Agenten |
| `pw_real_hanging_files.jpg` | Haengeregister mit leeren Reitern | Ablage, Suche |
| `pw_real_magnifier_stack.jpg` | Lupe ueber Papierstapel | Pruefen, Doku gegen Wirklichkeit |
| `pw_real_manual_leaflet.jpg` | Dickes Handbuch neben duennem Merkblatt | Doku gegen Wirklichkeit |
| `pw_real_patch_cable.jpg` | Netzwerkkabel ins Patchfeld | Verbindungen, Integrationen |
| `pw_real_invoice_stack.jpg` | Stapel Rechnungen mit Bueroklammern | Rechnungen, Buchhaltung |
| `pw_real_printer_output.jpg` | Drucker gibt Stapel aus | Ergebnis, Bericht |
| `pw_real_printed_chart.jpg` | Ausgedrucktes Diagramm ohne Schrift | Auswertung |
| `pw_real_card_box.jpg` | Karteikasten mit Kundenkarten | Kundenliste, Dubletten |
| `pw_real_hourglass.jpg` | Sanduhr auf dem Schreibtisch | Zeit, Wartezeit |
| `pw_real_indicator_lamps.jpg` | Kontrollleuchten rot und gruen | Bestanden, nicht bestanden |
| `pw_real_two_desks.jpg` | Zwei gleiche Schreibtische nebeneinander | Gleicher Auftrag, zwei Laeufe |
| `pw_real_archive_box.jpg` | Archivkarton, Hand hebt Deckel | Archiv, Altbestand |
| `pw_real_contract_folder.jpg` | Vertragsmappe mit Schleife | Vertraege, Pruefung |
| `pw_real_printed_email.jpg` | Ausgedruckte lange Mail mit Markierungen | E-Mail-Aufgaben |
| `pw_real_counter_bell.jpg` | Tischklingel an der Theke | Kundenkontakt, Anfrage |
| `pw_clip_toggle_switch.mp4` | Hand legt Kippschalter um, Leuchte wechselt; 1080 × 1920, 8 s, keine Schleife, stumm; Startbild `pw_real_toggle_panel.jpg` | Reihe Gleicher Auftrag, anderer Schalter |

**Einbinden:** Im Plan `"assets": {"folder": "assets/higgsfield/library", ...}` (`src\fn\render\assets.py`). Standbilder mit langsamer Fahrt im Code (100 → 104 %); den Clip mit seinem Startbild davor oder danach. Kennzeichnung immer einblenden.
