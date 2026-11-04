# Kostenschätzung Pilot (Abschnitte 1–3)

**Hinweis:** Die Abschnitte 1–6 zeigen den Stand vor Stufe 0 und vor dem Rebrand; Namen wie Plümo und Zonkfruit sind dort Geschichte. Gültig sind die Abschnitte 7 und 8 am Ende.

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

## 8. Nachtrag nach dem Rebrand (02.11.2026)

Stefan hat entschieden:
- Marke Tintora, klassischer TV-Anime
- Juna, Luci, Tassilo und Mira
- informative Serie mit Wissensmomenten

Was sich an den Kosten ändert:

- **Stufe 0 gesamt:** 88 Credits (Guthaben 182 → 94).
  - 74 für Stil A, Modellblätter und Konsistenztest
  - 8 für den Anime-Stiltest
  - 6 für die neuen Modellblätter (4 Aufträge, davon 1 vom Inhaltsfilter blockiert und erstattet)
- **Mengengerüst des Piloten** laut `Pilot-Storyboard.md`:
  - Video unverändert 154 s je Format
  - 2 Standbilder mehr, weil die Wissens-Shots 1-10a und 3-01a dazukommen; 2-14 ersetzt einen bestehenden Shot
  - 3 Heftzeichnungen
- **Stufe 1 netto:**

  | Posten | Rechnung | Credits |
  |---|---|---|
  | Schauplätze | 6 × 2 | 12 |
  | Startbilder | 128 | 128 |
  | Endbilder | 28 | 28 |
  | Standbilder | 18 × 2 × 2 | 72 |
  | Heftzeichnungen | 3 × 2 | 6 |
  | Video | | 385 |
  | **Summe** | | **631** |

- **Erwarteter Fall** (Faktor 1,5): 369 + 578 = 947 Credits. Dazu kommen etwa 10 Credits Restarbeit: Anime-Fassung der Schauplätze, Größenvergleich, Mängel an den Modellblättern.
- **Pilot gesamt:** etwa 1.045 Credits. Davon sind 88 schon verbraucht. Über die vorhandenen 94 Credits hinaus fehlen etwa 863. Ein Monat Plus mit 1.200 Credits reicht.

**Neues Risiko:** Der Inhaltsfilter von Higgsfield hat ein Ausdrucksblatt von Juna blockiert („nsfw“, erstattet), obwohl der Prompt harmlos war (Ausdrücke eines Mädchens im Regenmantel). Bei einer menschlichen Kinderfigur können solche Fehlblockaden öfter auftreten. Das kostet keine Credits, aber Zeit, und kann einzelne Shots verhindern. Gegenmittel, noch nicht getestet:
- Ganzkörper statt Nahaufnahme
- Prompts ohne Begriffe wie „girl“ allein, stattdessen „cartoon character Juna, 9-year-old adventurer in a raincoat“
- bei wiederholter Blockade ein anderes Modell


**Ergänzung (02.11.2026, nach dem Beheben der Mängel):**
- Stufe 0 hat jetzt insgesamt 102 Credits gekostet, das Guthaben liegt bei 80.
- Die Restarbeit ist erledigt und hat 14 statt 10 Credits gekostet.
- Pilot im erwarteten Fall: 102 + 947 = **etwa 1.049 Credits**. Über das Guthaben hinaus fehlen etwa 867.

## 9. Bedarf für Folge 1 (25–35 min, Stefans Format vom 02.11.2026)

**Format:**
- Eine YouTube-Folge in 16:9 aus den Abschnitten 1–18 des Staffelbogens.
- Die Reels werden daraus geschnitten, mit dem Cliffhanger des jeweiligen Abschnitts am Ende.
- Der Pilot (Abschnitte 1–3) ergab 4:02 min Langfassung. 18 Abschnitte ergeben also etwa 24 min. Damit die Folge sicher über 25 min kommt, dürfen die Abschnitte in der Langfassung bis 90 s lang sein. Das ergibt etwa 25–27 min.

**Reels aus 16:9:** Ein Hochformat-Ausschnitt aus dem 16:9-Video wäre nur etwa 600 px breit und damit unscharf. Vorschlag:
- Das 16:9-Bild steht in der Mitte des 9:16-Reels.
- Oben stehen Titel und „Teil N“, unten die Untertitel, dahinter eine unscharfe, vergrößerte Kopie des Bildes.
- Das kostet **keine Credits**.
- Optional werden je Reel die zwei wichtigsten Shots (Hook, Cliffhanger) eigens in 9:16 erzeugt. Dafür kommen etwa 450 Credits dazu: 18 × 2 Shots × 5 s × 1,25 × 1,5 = 338 für die Videos und 108 für die Startbilder.

**Rechnung je Abschnitt** (nur 16:9, Durchschnitt aus dem Piloten):
- Video: 51 s × 1,25 = 64 Credits
- Bilder: 19 Start-, End- und Standbilder × 2 + 1 Heftzeichnung × 2 = 40 Credits
- Netto: 104 Credits

| Fall | Faktor | 18 Abschnitte | dazu 7 neue Schauplätze (bunt und grau) | **Folge 1** |
|---|---|---|---|---|
| gemessen | 1,33 | 2.494 | 37 | **2.531** |
| **erwartet** | 1,5 | 2.812 | 42 | **2.854** |
| vorsichtig | 2,5 | 4.688 | 70 | **4.758** |

Bei Abschnitten von bis zu 90 s statt 80 s kommen etwa 12 % dazu, im erwarteten Fall also **etwa 3.200 Credits**.

**Woher die Credits kommen könnten**, Preise vom 29./30.10.2026, heute nicht neu prüfbar:
- Plus monatlich: 59 € für 1.200 Credits. 3 Monate ergeben 3.600 Credits plus 80 Guthaben, das deckt den erwarteten Fall. Das sind 177 €.
- Plus jährlich: 47 € im Monat. Vermutlich ist das eine Bindung für 12 Monate; die Bedingungen sind nicht geprüft.
- Einmal-Pakete mit 500, 1.000, 2.000 oder 4.000 Credits: Preis nicht ermittelbar, im Higgsfield-Konto nachsehen.
- Ultra: Credit-Menge nicht ermittelbar.

**Stimmen (Gemini):**
- Etwa 50 s Sprache je Abschnitt, 3 Versuche je Satz. Für 18 Abschnitte sind das etwa 0,61 USD auf Deutsch und etwa 1,22 USD für Deutsch und Englisch zusammen.
- Gerechnet mit `gemini-3.8-flash-tts` bis 31.12.2026; ab 2027 verdoppelt sich der Preis.
- Das vorhandene Gemini-Guthaben (20 € laut Übersicht) reicht.

**Musik:**
- Lizenzfrei, 0 €.
- Kandidaten: die YouTube Audio Library und Pixabay Music. Ihre Bedingungen, besonders für TikTok und Instagram, sind **nicht geprüft**. Vor der Verwendung prüfen und in `08 Recht und Verwaltung\Lizenzen` belegen.

## 10. Neue Vorgabe: Folge 1 mit etwa 14 min, Tarif Ultra (02.11.2026)

Abschnitt 9 (25–35 min) ist überholt. Gültig ist jetzt `Folge 1 Shotliste und Credits.md`:
- Folge 1 dauert 13:33 min, davon 36 % KI-Video.
- Erwarteter Fall etwa **1.057 Credits**, Spanne 937–1.761.
- Für Tintora sind 1.300 Credits vorgesehen, noch nicht freigegeben.


## 11. Gekürzter Plan: Folge 1 mit 500 Credits bis 30.11.2026 (03.11.2026)

Abschnitt 10 ist überholt. Stefan hat am 03.11. freigegeben: Tintora Folge 1 bekommt bis 30.11. **500 Credits** statt 1.300, dazu 33 Credits für Reel-Themen (höchstens 2 je Thema). Gebucht wird erst nach Rückmeldung der Hauptsitzung.

### Ausgangslage

- **Bilder:** Alle Standbilder der Folge liegen fertig vor: 170 Aufträge, 357,75 Credits, im 16:9-Format.
- **Testreel F1-06:** 127,75 Credits aus dem Testvideo-Budget, nicht aus den 500, und von Stefan freigegeben. Das Format ist durchgehend 9:16 mit Kling-Clips.
  - 13 Clips und 13 Hochformat-Startbilder.
  - Gemessener Nachdreh-Faktor dort: 127,75 / 113,75 = **1,12**.
- **Clips:** Für F1-01 bis F1-05 und F1-07 bis F1-09 fehlen alle Clips. Laut Schnittliste sind dort 61 Video-Shots geplant, im Pilot (F1-01 bis F1-03) allein 35.
- **Preise am 03.11.:** Nano Banana Pro 2 Credits je Bild, Kling 3.0 Omni Frames pro 1,25 Credits je Sekunde (5 s = 6,25).

### Was mit 500 geht: die acht übrigen Abschnitte als Reels im Hochformat

Der Takt ab 04.11. verlangt Reel-Abschnitte aus Folge 1 auf Deutsch und Englisch. Bezahlte Clips sollen deshalb zuerst den Reels dienen. Zwei Formate mit Clips gehen sich nicht aus: Ein 9:16-Clip passt nicht in die 16:9-Folge, ein 16:9-Clip verliert im Hochformat zwei Drittel der Breite.

**Je Abschnitt (Reel 65–90 s):**
- **5 Kling-Clips à 5 s** für die Handlungsshots aus der Schnittliste: Hook, Bewegung, Wende, Cliffhanger. Kosten 31,25.
- **5 Hochformat-Startbilder** für diese Clips. Kosten 10.
- **Etwa 2 weitere Hochformat-Bilder** für Totalen, die sich nicht aus dem 16:9-Bild zuschneiden lassen. Kosten 4.
- **Rest im Code, 0 Credits:** Die übrigen Shots sind ein 9:16-Ausschnitt aus dem vorhandenen Standbild mit Kamerafahrt, Licht und Hörlinien. Dazu kommen Heft-Animation, Übergänge und die Tonebene wie im Testreel.
- **Wiederverwendung:** Vorspann- und Abspannbilder kommen aus Stufe 0 (Schauplatz Farbbaum-Hügel bunt und grau), dazu die Heftzeichnungen.
- Netto 45,25 je Abschnitt, mit Faktor 1,2 also **etwa 54**.

| Posten | Credits |
|---|---|
| 8 Abschnitte × 45,25 netto | 362 |
| Nachdrehe (Faktor 1,2 statt gemessen 1,12) | 72 |
| **Erwartet** | **434** |
| Reserve, nur für sichtbare Fehler (Figur verändert, Licht falsch) | 66 |
| **Summe** | **500** |

**Haltepunkt:** Liegen nach drei Abschnitten mehr als 180 Credits verbraucht vor, sinken die übrigen Abschnitte auf 4 Clips je Reel.

**Bewegungsanteil:** etwa 25 s Kling-Bewegung je Reel von 80 bis 85 s, also etwa 30 %. Das Testreel hatte nahezu 100 %. Die übrigen Shots bekommen mehr Bewegung im Code als vor dem Neustart: Hochformat-Ausschnitt, Hörlinien, wechselnde Übergänge, Geräusche.

### Was sich auf Dezember oder einen Nachkauf verschiebt

- **Die 16:9-Folge für YouTube (etwa 14 min).** Sie braucht eigene Clips im Querformat: etwa 40 Clips à 5 s, das sind etwa 250 netto und etwa 300 mit Nachdrehen.
  - Bis dahin ließe sich die Folge zwar ohne Credits aus Standbildern mit Kamerafahrt bauen (`render.py`). Genau das hat Stefan am 02.11. mit Note 4 bewertet, deshalb empfehle ich das nicht.
- **Mehr Clips je Reel**, bis zum Niveau des Testreels mit 13 Clips: zusätzlich etwa 8 × 70 = 560.
- **Die 33 Credits für Reel-Themen** bleiben unangetastet für Themen außerhalb der Folge.

### Stimmen: der Takt ist durch Pro begrenzt, nicht durch Credits

| Abschnitt | DE fehlt | Anfragen DE | Anfragen EN | zusammen |
|---|---|---|---|---|
| F1-04, F1-05 | nichts | 0 | je etwa 4 | je etwa 4 |
| F1-03 | 8 von 15 Zeilen | etwa 4 | etwa 4 | etwa 8 |
| F1-01, F1-02, F1-07, F1-09 | alle | je etwa 4 | je etwa 4 | je etwa 8 |
| F1-08 | alle, 5 Figuren mit Mira | etwa 5 | etwa 5 | etwa 10 |

Bei höchstens 12 Pro-Anfragen am Tag gehen zwei Abschnitte mit DE und EN nur dann an einem Tag, wenn die deutschen Stimmen schon vorliegen.

**Vorschlag:**
- 04.11.: F1-04 und F1-05
- 05.11.: F1-07
- 06.11.: F1-08
- 07.11.: F1-09
- 08.11.: F1-03
- 09.11.: F1-01
- 10.11.: F1-02

Das ergibt neun Reels in DE und EN bis 10.11. Der Takt „2 Themen je Tag“ ist damit nur am 04.11. erreichbar.

### Verbrauch der 500 Credits (wird je Reel fortgeschrieben)

| Reel | Datum | Bilder | Clips | Credits | Summe | Prüfbericht |
|---|---|---|---|---|---|---|
| F1-04 Der Weg zum Echoberg | 03.11.2026 | 7 (davon 2 Nachbesserungen) | 5 (23 s) | 42,75 | 42,75 | DE und EN bestanden |

Pro-Anfragen am 03.11.2026: 10 von 12. Davon 1 für das Testreel DE (Zeile 083), 4 für das Testreel EN und 5 für F1-04 EN (darunter 1 Serverfehler 500 mit 1 Wiederholung).

| F1-05 Dunkel wie Tinte (DE fertig, EN folgt 04.11.) | 03.11.2026 | 4 | 7 Aufträge (4 verworfen) | 50,50 | 93,25 | DE bestanden |

Lehre aus F1-04 und F1-05: Kling lässt Luci im Dunkeln immer wieder leuchten und erfindet Nebenfiguren. Dagegen helfen Start- und Endbild gleich, „genau drei Figuren“ im Prompt und, wenn es nicht klappt, das Standbild mit Fahrt. Nachdrehen kostete bisher 4 Credits bei F1-04 (2 Bilder) und 25 bei F1-05 (4 verworfene Clips). F1-05 liegt mit 50,5 trotzdem unter den erwarteten 54 je Reel, weil ein Clip aus dem Testreel wiederverwendet wurde und einer als Standbild geschnitten ist. Zusammen sind 93,25 von 500 Credits verbraucht, nach 2 von 8 Reels.
