# Kostenschätzung Pilot (Abschnitte 1–3)

Stand 02.11.2026 (Wien), Claude. **Es wurde nichts gebucht und nichts generiert.** Die Creditpreise sind mit der Kostenabfrage `get_cost` des Higgsfield-MCP-Servers ermittelt. Diese Abfrage reicht keinen Auftrag ein; vor den Abfragen lag das Guthaben bei **182 Credits, Tarif Starter**. Eine Kontrolle danach über den lesenden Konnektor „Higgsfield AI“ ergab ebenfalls 182 Credits; die Preisabfragen haben also nichts gekostet.

Regel dieser Datei: nur geprüfte Preise mit Quelle und Datum. Was nicht geprüft werden konnte, heißt „nicht ermittelbar“ oder „Annahme“.

## 1. Geprüfte Preise

### 1.1 Higgsfield (Credits, abgefragt am 02.11.2026 per `get_cost`)

| Modell | Einstellung | Credits | je Sekunde |
|---|---|---|---|
| Nano Banana Pro (`nano_banana_pro`) | 2K, 16:9 | 2 je Bild | – |
| Nano Banana Pro | 4K, 16:9 | 4 je Bild | – |
| Kling 3.0 Omni Frames (`kling_o3_flf`) | pro, ohne Ton, 5 s, 16:9 | 6,25 | 1,25 |
| Kling 3.0 Omni Frames | pro, ohne Ton, 10 s, 16:9 | 12,5 | 1,25 |
| Kling 3.0 Omni Frames | pro, ohne Ton, 5 s, **9:16** | 6,25 | 1,25 |
| Kling 3.0 Omni Frames | std, ohne Ton, 5 s, 16:9 | 5 | 1,0 |
| Kling 3.0 Omni Frames | Standard (std, mit Ton), 8 s, 16:9 | 10 | 1,25 |
| Kling 3.0 (`kling3_0`) | pro, ohne Ton, 5 s, 16:9 | 8,75 | 1,75 |
| Kling 3.0 | std, ohne Ton, 5 s, 9:16 | 7,5 | 1,5 |
| Seedance 2.5 (`seedance_2_5`) | 1080p, ohne Ton, 5 s, 16:9 | 80 | 16 |
| Seedance 2.5 | 720p, ohne Ton, 5 s, 16:9 | 35 | 7 |
| Seedance 2.0 (`seedance_2_0`) | fast, 720p, ohne Ton, 5 s, 16:9 | 12,5 | 2,5 |

Nicht geprüft:
- Nano Banana Pro im Hochformat 9:16. Ich nehme denselben Preis wie bei 16:9 an, weil Kling in beiden Formaten gleich viel kostet.
- Die Auflösung von Kling std.
- Was Kling in 16:9 in Pixeln liefert. Für 9:16 sind 1076 × 1928 px am 30.10.2026 bei Scutoria gemessen.

### 1.2 Higgsfield-Tarife (Euro)

| Tarif | Preis | Credits je Monat | Euro je Credit (gerechnet) |
|---|---|---|---|
| Starter (gebucht) | 19 € im Monat | 270 | 0,0704 |
| Plus monatlich | 59 € im Monat | 1.200 | 0,0492 |
| Plus jährlich | 47 € im Monat | 1.200 | 0,0392 |
| Ultra | 129 € monatlich, 99 € jährlich | **nicht ermittelbar** | nicht ermittelbar |
| Einmal-Pakete | 500, 1.000, 2.000 oder 4.000 Credits (laut Beschreibung des Higgsfield-Werkzeugs) | – | Preise **nicht ermittelbar** |

Quelle der Tarifpreise: higgsfield.ai/pricing, abgerufen am 29./30.10.2026, festgehalten in `01 Idee und Strategie\Übergabebericht 2026-10-30.md`. Am 02.11.2026 lud die Seite die Preise erst per Skript nach, ein erneuter Abruf brachte deshalb keine Zahlen. Vor einer Buchung prüft Stefan den Preis im Konto. Nicht ermittelbar ist auch, ob ungenutzte Credits in den nächsten Monat übergehen.

Bei Seedance 2.0 in der Stufe „std“ verlangt Higgsfield laut Modellbeschreibung mindestens den Tarif Plus. Kling 3.0 Omni Frames lief am 30.10.2026 im Starter.

### 1.3 Gemini-Stimmen (USD, Preisseite abgerufen am 02.11.2026)

| Modell | Text-Eingabe je 1 Mio. Token | Audio-Ausgabe je 1 Mio. Token |
|---|---|---|
| `gemini-3.8-flash-tts` | 0,50 USD bis 31.12.2026, ab 01.01.2027 1,00 USD | 9,00 USD bis 31.12.2026, ab 01.01.2027 18,00 USD |
| `gemini-2.5-flash-preview-tts` (bisher genutzt) | 0,50 USD | 10,00 USD |

Audio hat laut derselben Seite 25 Token je Sekunde. Quelle: ai.google.dev/gemini-api/docs/pricing. Ich gebe die Beträge in USD an; umgerechnet wird zum Tageskurs bei der Abrechnung.

## 2. Mengengerüst des Piloten

Aus `Pilot-Storyboard.md`, Abschnitt „Gesamtzahlen“:

| Posten | Menge |
|---|---|
| KI-Video (Kling Omni Frames pro, ohne Ton) | 35 Shots, 154 s je Format, 308 s in beiden Formaten |
| Startbilder 4K | 32 |
| Endbilder 4K | 7 |
| eigene Hochformat-Start- und -Endbilder 2K | 7 + 3 |
| Standbilder und Zweitbilder 4K | 16 |
| Schauplatz-Referenzen 4K | 8 |
| Sprechtext | 35 Sätze, gezählt etwa 239 Wörter, also etwa 109 s Sprache, bei angenommenen 2,2 Wörtern je Sekunde |

**Nachdrehfaktor (Annahme, nicht gemessen):** Nicht jedes Bild und nicht jedes Video ist beim ersten Versuch brauchbar. Ich rechne mit drei Stufen:
- günstig: 1,5 Versuche je Bild oder Video
- erwartet: 2,5
- vorsichtig: 3,5

Einziger Vergleichswert: Bei Scutoria reichte am 30.10.2026 je Clip ein Versuch (8 Clips, 96 Credits). Das waren aber abstrakte Hintergründe ohne Figuren, und das lässt sich auf Figurenanimation nicht übertragen. Der echte Faktor zeigt sich in Stufe 0.

## 3. Kosten je Arbeitsschritt

### Stufe 0: Stil, Modellblätter, Konsistenztest

Diese Stufe passt in das vorhandene Guthaben von 182 Credits; neues Geld fällt nicht an.

| Schritt | Rechnung | Credits |
|---|---|---|
| Stilfindung | 12 Bilder 2K × 2 | 24 |
| Modellblätter | 10 Blätter 4K × 4 × 2 Versuche (Plümo 2, Funzel 3 mit Graufassung, Kasimir 3 mit Graufassung, Grisel 2) | 80 |
| Größenvergleich | 1 Bild 4K × 4 × 2 Versuche | 8 |
| Schauplatz Farbbaum-Hügel bunt und grau | 2 Bilder 4K × 4 × 2 Versuche | 16 |
| Konsistenztest: 2 Startbilder (1-05, 1-07) | 2 × 4 | 8 |
| Konsistenztest: 2 Videos à 4 s, beide Formate | 4 Videos × 4 s × 1,25 | 20 |
| **Summe Stufe 0** | | **156** |

Danach sind noch 26 Credits übrig. Ergebnis der Stufe: freigegebene Modellblätter, ein gemessener Nachdrehfaktor und der Nachweis, ob Plümo in Bewegung gleich bleibt. **Erst danach lohnt sich eine Buchung.**

### Stufe 1: Pilot fertigstellen

| Schritt | Rechnung (ein Versuch) | netto | günstig ×1,5 | erwartet ×2,5 | vorsichtig ×3,5 |
|---|---|---|---|---|---|
| übrige Schauplatz-Referenzen | 6 × 4 | 24 | 36 | 60 | 84 |
| Startbilder 4K | 32 × 4 | 128 | 192 | 320 | 448 |
| Endbilder 4K | 7 × 4 | 28 | 42 | 70 | 98 |
| eigene 9:16-Bilder 2K | 10 × 2 | 20 | 30 | 50 | 70 |
| Standbilder 4K | 16 × 4 | 64 | 96 | 160 | 224 |
| **Bilder zusammen** | | **264** | **396** | **660** | **924** |
| KI-Video 16:9 | 154 s × 1,25 | 192,5 | 289 | 481 | 674 |
| KI-Video 9:16 | 154 s × 1,25 | 192,5 | 289 | 481 | 674 |
| **Videos zusammen** | | **385** | **578** | **963** | **1.348** |
| **Summe Stufe 1** | | **649** | **974** | **1.623** | **2.272** |

### Pilot gesamt (Stufe 0 + Stufe 1)

| Fall | Credits | in Euro zum Starter-Satz | zum Plus-Satz (monatlich) | zum Plus-Satz (jährlich) |
|---|---|---|---|---|
| günstig | 1.130 | 79,48 € | 55,53 € | 44,24 € |
| **erwartet** | **1.779** | **125,15 €** | **87,44 €** | **69,66 €** |
| vorsichtig | 2.428 | 170,82 € | 119,35 € | 95,08 € |

Die Credits sind auf ganze Zahlen gerundet (erwartet genau 1.778,5). Die Euro-Beträge sind mit den ungerundeten Sätzen 19/270, 59/1.200 und 47/1.200 gerechnet und per Skript nachgeprüft.

Wie die Euro-Spalten zu lesen sind:
- Die Beträge sind Credits mal Euro je Credit aus 1.2. Tatsächlich zahlt man Monatsbeiträge, keine einzelnen Credits.
- Der Starter-Satz ist theoretisch: Mit 270 Credits im Monat bräuchte der erwartete Fall etwa sieben Monate.
- Die 156 Credits der Stufe 0 sind mit dem Starter-Beitrag schon bezahlt.

Was bei einer Buchung praktisch anfällt (Rechenbeispiel, keine Empfehlung):
- Plus für einen Monat kostet 59 € und bringt 1.200 Credits. Zusammen mit dem Rest aus Starter reicht das für den günstigen Fall.
- Für den erwarteten Fall fehlen dann noch etwa 550 Credits, also ein zweiter Monat oder ein Einmal-Paket mit unbekanntem Preis.

### Stimmen (Gemini)

| Schritt | Rechnung | USD |
|---|---|---|
| Probehören | 5 Rollen × 3 Stimmen × 3 Sätze à etwa 4 s = 180 s × 25 Token = 4.500 Token × 9 USD/Mio. | 0,04 |
| Pilot Deutsch, 3 Versuche je Satz | 109 s × 3 × 25 = 8.175 Token × 9 USD/Mio. = 0,074; Eingabe etwa 35 × 3 × 100 Token = 10.500 × 0,50 USD/Mio. = 0,005 | 0,08 |
| Pilot Englisch, gleich gerechnet | | 0,08 |
| **Summe Stimmen** | | **etwa 0,20 USD** |

Die 100 Token je Satz für Stilanweisung und Text sind eine Annahme. Die Rechnung gilt für `gemini-3.8-flash-tts` bis 31.12.2026; danach verdoppelt sie sich. Mit dem bisher genutzten `gemini-2.5-flash-preview-tts` ist sie praktisch gleich.

### Weitere Posten

| Posten | Kosten |
|---|---|
| Schnitt per Skript, Geräusche selbst erzeugt | 0 € direkt; kostet Claude-Kontingent, Umfang **nicht ermittelbar** |
| Musik | **nicht ermittelbar**, keine Quelle gewählt |
| Namens- und Titelprüfung (Markenregister) | 0 € selbst recherchiert; eine anwaltliche Prüfung wäre **nicht ermittelbar** |

## 4. Sparhebel

Die Ersparnisse sind im erwarteten Fall gerechnet (Faktor 2,5).

| Hebel | Ersparnis | Nachteil |
|---|---|---|
| **Erst nur Hochformat** (Kurzclips), Querformat-Videos später | 481 Credits | Die Langfolge kommt später; die Startbilder sind schon für beide Formate gebaut |
| Kling std statt pro | 154 s × 2 Formate × 0,25 × 2,5 = 193 Credits | geringere Qualität; Auflösung std nicht geprüft |
| 30 s Video als Standbild mit Kamerafahrt lösen | 30 × 2 × 1,25 × 2,5 = 188 Credits, abzüglich etwa 6 neuer Standbilder (60 Credits) = 128 Credits | weniger Bewegung, für Kinder weniger lebendig |
| Animatic-Abnahme vor jedem Video (schon eingeplant) | senkt den Nachdrehfaktor; Höhe nicht ermittelbar | etwas mehr Arbeit vorab |

## 5. Hochrechnung auf die ganze Staffel (grob)

- Je Abschnitt im erwarteten Fall: 1.623 Credits ÷ 3 = 541 Credits.
- Die übrigen 33 Abschnitte: 33 × 541 = 17.853 Credits.
- Dazu Referenzen für neun weitere Schauplätze: 9 × 3 Bilder × 4 Credits × 2,5 = 270 Credits.
- Zusammen etwa 18.100 Credits, also etwa 709 € zum Plus-Jahressatz oder etwa 890 € zum Plus-Monatssatz.

Annahme dahinter: Die übrigen Abschnitte brauchen so viel Video wie der Pilot. Actionreiche Abschnitte (Höhle, See, Sandsturm) können mehr brauchen. Zum Vergleich: Im Fragenkatalog vom 29.10.2026 steht ein Gesamtbudget von 50 € im Monat für das ganze Vorhaben.

## 6. Entscheidungen für Stefan vor der Produktion

1. **Stufe 0 freigeben?**
   - Sie kostet 156 der vorhandenen 182 Credits und kein neues Geld.
   - Ergebnis sind Stil, Modellblätter, ein Konsistenztest und der echte Nachdrehfaktor.
   - Ohne diese Stufe ist jede weitere Zahl hier eine Schätzung.
2. **Budget für Zonkfruit.** Für den Piloten sind im erwarteten Fall etwa 1.780 Credits nötig, für die Staffel etwa 18.000. Soll es dafür ein eigenes Budget geben, oder gilt der Rahmen von 50 € im Monat? Und welcher Tarif: Plus monatlich, Plus jährlich oder ein Einmal-Paket?
3. **Bildformat-Verfahren.** Entweder beide Formate gleich erzeugen (Vorschlag im Storyboard) oder erst nur Hochformat (spart etwa 480 Credits beim Piloten).
4. **Altersgruppe 6–9 und Einstufung „speziell für Kinder“.** Die Einstufung halte ich bei dieser Zielgruppe für zwingend. Folgen:
   - keine personalisierte Werbung, also weniger Einnahmen
   - keine Kommentare
   - keine Endbildschirme und Infokarten, also keine Verlinkung vom Kurzclip zur Langfolge über diese Elemente
   - Einzelheiten in `Produktionsverfahren.md` 7
5. **Plattformen.** Nur YouTube (Shorts und Langfolgen)? TikTok und Instagram verlangen ein Mindestalter von 13 Jahren und erreichen die Zielgruppe nicht regelkonform.
6. **Takt.** Eine Staffel hat 36 Abschnitte. Beim Netzwerk-Takt von 6 Posts am Tag wäre sie nach sechs Tagen verbraucht. Vorschlag: Zonkfruit als Ausnahme mit 1 Abschnitt je Woche und Sprache, die Langfolge nach je 18 Abschnitten.
7. **Alter Zonkfruit-Kalender** (84 Faktenthemen ab 09.11.2026, freigegeben am 01.11.): ruhen lassen oder parallel weiterführen? Parallel hieße zwei sehr verschiedene Formate auf einem Kinderkanal. Die Faktenvideos wären dann wohl ebenfalls „speziell für Kinder“.
8. **Musik.** Quelle und Lizenz wählen, oder die Serie bleibt ohne Musik.
9. **Namen und Titel.** Tüpfelinsel, Funzel, Kasimir und Grisel sind Vorschläge. Ein Abgleich mit Markenregister und bestehenden Kinderfiguren ist noch nicht gemacht.
10. **Stimmen.** Probehören freigeben (etwa 0,04 USD), danach die Besetzung festlegen.
11. **Österreich.** Vor dem Start prüfen, ob eine Anzeige bei der KommAustria als Abrufdienst nötig ist (nicht geprüft).

## 7. Nachtrag nach Stufe 0 (02.11.2026)

Stufe 0 ist erledigt: **74 Credits verbraucht** (Guthaben 182 → 108). Ergebnisse, Messwerte und die neue Rechnung stehen in `Stufe 0\Ergebnis Stufe 0.md`. Was sich gegenüber dieser Datei ändert:

- **4K ist im Starter nicht verfügbar.** Startbilder, Endbilder und Standbilder entstehen deshalb je Format eigens in 2K (2 × 2 statt 1 × 4 Credits).
- **Gemessener Nachdrehfaktor:** 1,33 bei Bildern mit Figuren, 1,0 bei Videos. Die Stichprobe ist klein.
- **Neue Schätzung Pilot**, erwarteter Fall mit Faktor 1,5: **etwa 1.010 Credits** statt 1.779. Spanne 771 bis 1.627. Über die vorhandenen 108 Credits hinaus sind etwa 828 Credits nötig, also ein Monat Plus.
- **Staffel**, erwarteter Fall: etwa 10.260 Credits statt 18.100.

