# Dewlane – Testvideo-Konzept (Neustart, November 2026)

Stand 03.11.2026, Dewlane-Sitzung. Grundlage: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md` (Abschnitt 4 und 5) und Codex-Bericht 01.11., Abschnitt 6. Noch nichts erzeugt, nichts gerendert. Zur Freigabe durch die Hauptsitzung.

**Thema:** „Wie viel Sonnencreme? Die Testmenge hinter dem LSF“ (Konzeptplan Nr. 16, `beauty-20261117-3-de`, Reihe Unter der Lupe). Quellen am 02.11. im Original gelesen: EU-Empfehlung 2006/647/EG (Erwägungsgrund 14, Nr. 7), AAD „How to apply sunscreen“. **Sprechtext bleibt wie im Piloten**, damit wird die vorhandene, bezahlte Gemini-Stimme wiederverwendet: **0 Flash-Anfragen.** Länge 78,8 s.

**Warum dieses Thema:** Es trägt genau, was Stefan vermisst. Man sieht, wie Creme aus der Tube kommt, wie viel sechs Teelöffel sind und wie sie verteilt wird. Dazu kommen Textur in Nahaufnahme und echte Situationen (vor dem Rausgehen, nach dem Schwimmen).

## Bildkonzept: Realbild trägt, Code erklärt

Jede Szene hat ein **fotorealistisches Higgsfield-Bild oder einen Clip als Hauptbild**. Die bisherige Code-Grafik bleibt nur als dünne Erklärschicht darüber: Zahl, Lupenring, Balkenschema, Beleg-Chips. Das erfundene Produkt ist eine weiße Tube ohne Text; „SONNENSCHUTZ · LSF 30“ setzt der Code als Etikett darauf.

| Zeit | Szene | Hauptbild (Higgsfield) | Code darüber | Bewegung |
|---|---|---|---|---|
| 0–10 s | Hook: sechs Löffel | Clip: Hand drückt Creme aus der Tube in einen Teelöffel; dann Standbild sechs volle Löffel von oben | Zähler 1…6, „Teelöffel“ | Kling-Clip, dann langsamer Zoom |
| 10–23 s | Unter der Lupe | Makro: Tube mit Etikettfläche, dann Makro eines dünnen Cremefilms | Lupenring, „2 mg/cm²“, Chip **Beleg** EU | Schwenk mit Lupen-Übergang |
| 23–44 s | Die Menge | Standbild: Schnapsglas voll Creme neben der Tube; Makro der Textur | „≈ 36 g“, AAD-Karte | Parallaxe (zwei Ebenen), Textur-Clip |
| 44–56 s | Wirkung laut Quelle | Unscharfer Strand im Hintergrund, abgedunkelt | Balkenschema „Schema nach EU-Beispiel · keine Messung“ | Balken animiert, Hintergrund ruhig |
| 56–68 s | Im Alltag | Clips: Hände verteilen Creme auf dem Unterarm (vor dem Fenster, Morgenlicht); Handtuch und Tube am Beckenrand | drei Hinweise mit Symbol, Chip EU Nr. 7 | Kling-Clips, harte Schnitte im Sprechrhythmus |
| 68–79 s | Merksatz | Tube aufrecht auf Stein, Gegenlicht | Merksatz, Frage, Dewlane-Absender | langsamer Push-in |

**Kennzeichnung nach Codex 6:** Im Bild stehen drei feste Marken. **Packungsangabe** steht für den Hersteller, hier „LSF 30“ auf dem erfundenen Produkt. **Beleg** steht für die Quelle (EU, AAD). **KI-Bild · Veranschaulichung** steht auf jedem Higgsfield-Bild mit Händen oder Haut. Es gibt kein Vorher-nachher, keine Hautnahaufnahme als Ergebnis und kein „getestet“. Der Stempel oben lautet „KI-Bilder · erfundenes Produkt · kein Produkttest“.

## Higgsfield-Liste (Kappe 100 Credits)

Preise: Nano Banana Pro am 03.11. per `get_cost` geprüft, 2 Credits je Bild (9:16). Kling-Preise stammen aus der Prüfung vom 30.10. (Kling 3.0 Omni pro, 8 s, 10 Credits) und werden vor der Buchung neu geprüft. Guthaben am 03.11.: 2.299,75 Credits.

| Nr | Art | Prompt (gekürzt; immer: no text, no logo, no brand, soft daylight, ivory and warm stone tones, 9:16) | Credits |
|---|---|---|---|
| B1 | Bild | plain white sunscreen tube standing on its cap on warm ivory stone, blank label area, soft shadow | 2 |
| B2 | Bild | top view of six silver teaspoons in a row, each filled with white sunscreen lotion, on ivory linen | 2 |
| B3 | Bild | macro of a thin even film of white lotion with fine sheen on a matte surface | 2 |
| B4 | Bild | a shot glass filled with white lotion next to a plain white tube on stone | 2 |
| B5 | Bild | blurred sunny beach background, bright, calm, no people | 2 |
| B6 | Bild | adult hand holding a plain white tube, squeezing a strand of lotion onto a teaspoon, close-up, no face | 2 |
| B7 | Bild | forearm with a line of white lotion before spreading, morning window light, natural skin, no face | 2 |
| B8 | Bild | towel and plain white tube at the edge of a swimming pool, water drops, no people | 2 |
| B9 | Bild | plain white tube upright on stone, backlight, minimal | 2 |
| | Varianten | je Motiv eine zweite Fassung zur Auswahl | 18 |
| K1 | Clip | from B6: lotion flows from the tube into the spoon, slow, static camera | 10 |
| K2 | Clip | from B7: two hands spread the lotion over the forearm, calm, natural | 10 |
| K3 | Clip | from B3: sheen travels slowly over the lotion film, seamless loop | 10 |
| K4 | Clip | from B8: a hand takes the tube from the pool edge, water drops, no face | 10 |
| | **Summe** | 18 Bilder + 4 Clips | **76** (Reserve 24) |

Hände und Unterarm sind die einzige „Haut“ im Video, immer mit „KI-Bild · Veranschaulichung“. Es gibt keine Gesichter, keine Hautprobleme und keinen Glow-Effekt. Ablage: `brands\beauty\assets\higgsfield\` mit `LICENSE.md` und `manifest.json`.

## Was Dewlane von den anderen Marken unterscheidet

Hell, warm und tageslichtig, mit **Händen und Produkt in Nahaufnahme** als Hauptdarsteller. Scutoria ist dunkel und zeigt Bürosituationen. Gigastruct und Revlore zeigen Technik im Großformat. Suitwerk zeigt Stoff am Bügel. Eigene Erkennungszeichen sind der Lupenring über dem Realbild, die Mengen in Alltagsmaßen (Löffel, Schnapsglas) und die drei Marken Packungsangabe/Beleg/KI-Bild.

## Ton-Cues (Klangfarbe: weich, hell, „Bad am Morgen“)

| Zeit | Ereignis | Klang |
|---|---|---|
| 0,3 s und je Löffel (6×) | Creme fällt in den Löffel / Zähler springt | weicher Tropfen-Plopp, leise |
| 10,6 / 22,8 / 44,3 / 56,1 / 67,7 s | Szenenwechsel | sanfter Swipe (Stoff/Luft), kein harter Whoosh |
| 11–12 s | Lupenring öffnet | leiser Glas-Ping |
| 45–50 s | Balken schrumpft | kurzer absteigender Ton |
| 57–60 s | Creme wird verteilt | Hautreibung, sehr leise |
| 72 s | Merksatz | weicher Akkord |
| durchgehend | Musikbett | leichte Akustik, 80 bpm, −18 dB, unter Stimme −10 dB (laut `audio_style.yaml`; Lizenz offen, nur mit Nachweis) |

## Offen für das Go

1. Freigabe der Bilder B1–B9 mit Varianten (18 Bilder, 36 Credits); diese kann ich sofort erzeugen.
2. Die Clips K1–K4 (etwa 40 Credits) erst, wenn Kling läuft.
3. Wunsch an den gemeinsamen Renderer: Realbild bzw. Clip als Szenenhintergrund mit Ken-Burns-Zoom je Szene, dazu die Ton-Cues aus dem Plan.
4. Die DE-Stimme bleibt. Soll der Text die Codex-Trennung stärker aussprechen („Auf der Packung steht …, die EU belegt …“), wäre eine neue Vertonung nötig (1 Flash-Anfrage).

## Stand 02.11.2026, 23:40

- **Bilder erzeugt:** 11 Bilder mit Nano Banana Pro (je 2 Credits), **22 Credits**. Zweite Varianten waren nicht nötig; neu erzeugt wurden nur B1 (sah wie eine Dose aus statt wie eine Tube) und B2 (zeigte sieben statt sechs Löffel). Ablage: `C:\Automation\faceless-network\brands\beauty\assets\higgsfield\dl_b*.png` mit `LICENSE.md` (Job-IDs). Für das Video gelten `dl_b1_tube_v2`, `dl_b2_spoons_v2`, `dl_b3`–`dl_b9`.
- **Offen:** Clips K1–K4 (etwa 40 Credits), sobald Kling läuft. Danach bleiben etwa 38 Credits unter der Kappe von 100.
- Rendern und Gemini erst nach dem Go der Hauptsitzung.

## Stand 03.11.2026, morgens: Clips und Trockenlauf fertig

- **Clips:** K1–K4 mit Kling 3.0 pro, 8 s, ohne Ton, je 14 Credits (`get_cost` geprüft), zusammen 56 Credits. Gesamtverbrauch Dewlane 78 von 100 Credits. Dateien `brands\beauty\assets\higgsfield\dl_k1_squeeze.mp4`, `dl_k2_spread.mp4`, `dl_k3_film.mp4`, `dl_k4_pool.mp4`; Nachweis in `LICENSE.md`.
- **Plan:** `data\direction\beauty-20261117-3-de.T1.json`. Sprechtext, Quellen und Stimme sind wie im Piloten (0 Gemini-Anfragen). `layout.media` legt je Abschnitt ein Bild oder einen Clip fest, `layout.sound` enthält die Ton-Cues für die Tonebene.
- **Umsetzung:** nur in `brands\beauty\nahaufnahme\scenes.py`. Die Medienebene zeigt Bild oder Clip vollflächig mit langsamer Fahrt und Überblendung. Oben und unten liegt ein Elfenbein-Schleier, oben rechts steht das Etikett „KI-Bild“ bzw. „KI-Bild · Veranschaulichung“. Szenen mit `photo: true` blenden die gezeichneten Produkte aus und legen Freitexte auf Tafeln.
- **Trockenlauf T1dry:** Prüfungen ohne Fehler, `overlap_check` ohne Überschneidungen, ohne Warnungen und ohne kleine Schrift.
- Wartet auf das Go der Hauptsitzung (Tonebene) für den finalen Render und den Export.
