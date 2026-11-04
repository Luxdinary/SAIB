# Frontlore – Testvideo-Konzept (Neustart, 03.11.2026)

Stand: 02.11.2026, nachts (Wien). Grundlage: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md` (Abschnitt 4 und 5) und Codex-Bericht, Abschnitt 3 („historische technische Probleme mit Karten, Modellen und Archivquellen“). Format bleibt „Rekonstruktion“ (`Format-Bibel.md`). Neu sind realistische Rekonstruktionsbilder, mehr Variation und Ton. **Entwurf für die Hauptsitzung, nichts erzeugt.**

## Thema

**Polybios' Fackeltelegraf: Wie sendet man einen ganzen Satz nur mit Feuer?** (Konzeptplan Nr. 1, Reihe Rekonstruktion). Die Quellen sind geprüft (Polybios X 43–47 in der Loeb-Ausgabe, Moore, Histos 2017, Kotsanas-Museum). Der Sprechtext bleibt Wort für Wort gleich, deshalb **kann die bezahlte DE-Stimme wiederverwendet werden: 0 Gemini-Anfragen**, Länge 72 s (Video etwa 75 s). Erst wenn Stefan einen anderen Text will, braucht es eine Flash-Anfrage.

## Bildkonzept: „Nachtrekonstruktion mit Pausfolie“

Das Video wechselt zwischen **realistischer Szene** (Higgsfield-Bild oder Kling-Clip, warm, von Fackeln beleuchtet) und **Analyse**. Bei der Analyse zieht eine halbdurchsichtige Pausfolie über dieselbe Szene, und die Linienzeichnung (Tafeln, Fackeln links und rechts) zeichnet sich direkt auf dem echten Bild. So sieht der Zuschauer erst die Wirklichkeit, dann ihre Erklärung, am selben Ort. Erhalten bleiben Zeitlineal, Stellenangabe und Linienregel. Jedes realistische Bild trägt den Stempel „KI-REKONSTRUKTION · KEINE AUFNAHME“.

| Beat (Sekunde) | Szenentyp | Bild | Bewegung und Übergang |
|---|---|---|---|
| Hook (0–7) | **Szene** | H1: Hügelkuppe bei Nacht, zwei Schirmwände mit Fackelsockeln, weit entfernt ein zweiter Hügel mit einem Lichtpunkt | Kling-Clip, Fackeln flackern, langsamer Push-in; Frage groß darüber |
| Mittel der Zeit (7–17) | **Geteiltes Bild** | links H3: Leuchtfeuer auf einem Turm; rechts H4: zwei Tongefäße mit Schwimmer und Stab auf einer Werkbank | senkrechter Schnitt, der von der Mitte aufgeht; Pegel sinkt als Kling-Clip; Stempel „NICHT SENDBAR“ |
| Lösung (17–31) | **Pausfolie** | H5: Werkbank mit fünf leeren Holztafeln, H6: Fackeln hinter dem Schirm | die Folie gleitet ein, Buchstaben und Linien zeichnen sich auf den echten Tafeln, Schwenk zum Schirm |
| Ablauf (31–41) | **Doppelstation** | H1 und H2 (Gegenhügel) als Splitscreen oben/unten, Lichtsignal wandert zwischen beiden | Schnitt im Takt der Signale, Sequenzpfeile aus Code |
| Probe (41–50) | **Nahaufnahme** | H7: Hand mit Griffel über einer Wachstafel bei Öllampe, ohne Gesicht | Zoom auf das Feld, der Buchstabe Κ erscheint, Kling-Clip Hand schreibt |
| Stufen (50–60) | **Kartentisch** | vorhandene Karte `fl_map_aegean.jpg` auf `fl_table_map.jpg` | Draufsicht, drei Stufenkarten werden auf den Tisch gelegt, Zeitlineal mit schraffierter Datierung |
| Befund (60–75) | **Vitrine** | vorhandene `fl_museum_case.jpg` (unscharf) + Befundblatt aus Code | Fokuswechsel aus der Vitrine auf das Papier, Stempel |

Damit gibt es fünf verschiedene Szenentypen und vier Bewegungsarten (Clip, Push-in, Folie, Draufsicht) mit eigenen Übergängen (Lichtblitz, senkrechter Schnitt, Folie, Fokuswechsel). Keine andere Marke nutzt Nachtlicht, Pausfolie oder Zeitlineal.

## Higgsfield-Liste (neu; Nano Banana Pro 2k, laut Bibliothek 2 Credits je Bild; vor dem Auftrag `get_cost`)

Gemeinsam für alle Prompts: `photorealistic reconstruction, ancient Greece 2nd century BC, night, warm torchlight, no people's faces, no soldiers, no weapons, no armour, no shields, no flags, no symbols, no text, no letters, vertical 9:16`.

| Nr. | Motiv (Prompt-Kern) | Bilder |
|---|---|---|
| H1 | hilltop at night, two low stone-and-timber screen walls, five empty iron torch sockets on each, distant hill with one small fire on the horizon, starry sky | 1 |
| H2 | the distant receiving hilltop, same construction, seen from far, small torches | 1 |
| H3 | simple stone beacon tower with a bonfire at night, Mediterranean hills | 1 |
| H4 | two identical clay vessels with a cork float and a marked wooden rod, on a workshop bench, oil lamp | 1 |
| H5 | workshop bench with five blank wooden tablets in a row, wax and stylus, oil lamp, top-down three-quarter view | 1 |
| H6 | close view of burning torches held in sockets behind a stone screen, night | 1 |
| H7 | a hand with a bronze stylus above a blank wax tablet, oil lamp, no face visible | 1 |
| H8 | sighting device: two parallel wooden tubes on a stand, on a hilltop at dusk (Rekonstruktion, gestrichelt beschriftet) | 1 |
| **Summe** | Probe H1 + H5 zuerst (4 Credits), dann der Rest; mit Ausschuss 1,5 | **8 Bilder ≈ 16–24 Credits** |

Kling-Clips (erst nach Meldung der Hauptsitzung, Kling 3.0 Omni, pro 8 s, laut Notiz 10 Credits je Clip): K1 Fackeln flackern (H1), K2 Pegel sinkt (H4), K3 Fackeln werden gehoben (H6), K4 Hand schreibt (H7). **4 Clips ≈ 40 Credits.** Gesamt höchstens etwa 64 Credits, unter der Kappe von 100.

Prüfung jedes Bildes: keine Waffen, keine Rüstung, keine Fahnen und Zeichen, keine Gesichter, keine Schrift (sonst verwerfen). Nachweis in `assets\higgsfield\library\LICENSE.md`.

## Ton-Cues (Klangfarbe: warm, nächtlich, Holz und Feuer; kein Pathos, keine Trommeln, keine Kampfgeräusche)

| Stelle | Geräusch |
|---|---|
| ganzes Video | Musikbett leise, dunkle Bordun-Fläche mit gezupftem Saiteninstrument, unter der Stimme abgesenkt |
| Hook, Szenen mit Fackeln | Feuerknistern als Atmo (leise) |
| jeder Beatwechsel | weicher Whoosh; bei „Lichtblitz“ ein kurzes Aufflammen |
| Pausfolie gleitet ein | Papierrascheln |
| Buchstaben und Linien zeichnen sich | leises Kratzen (Griffel) |
| Stempel „NICHT SENDBAR“, „UMSTRITTEN“, Befund | dumpfer Stempelschlag |
| Fackeln einzeln anzünden (Probe: 2 links, 5 rechts) | je Fackel ein kurzes Aufflammen, damit das Zählen hörbar ist |

Lizenz: nur Material mit Nachweis in `08 Recht und Verwaltung\Lizenzen` (Auswahl durch die Hauptsitzung).

## Was das Video von den anderen Marken unterscheidet

Nachtlicht und Feuer statt Studio oder Baustelle; Rekonstruktion **mit sichtbarer Grenze**: das echte Bild ist als KI-Rekonstruktion gestempelt, die Pausfolie zeigt, was die Quelle sagt (durchgezogen) und was ergänzt ist (gestrichelt). Zeitlineal, Stellenangabe und Befundblatt bleiben Frontlores Kennzeichen. Gigastruct zeigt reale Bauwerke und rechnet, Revlore misst Bewegung, Frontlore rekonstruiert aus Text.

## Grenzen (unverändert, Risiko hoch)

Nur Geschichte, keine Soldaten, keine Waffen, keine Symbole, keine Darstellung eines bestimmten realen Ereignisses (nur die beschriebene Technik), kein Gesicht. Polybios' Beispielnachricht wird nicht gezeigt. HUMAN_REVIEW, Freigabe einzeln durch Stefan.

## Was ich von der Hauptsitzung brauche

1. Go für die Bildprobe (H1, H5, 4 Credits), danach für H2–H8.
2. Meldung, wann Kling läuft (K1–K4).
3. Die Tonebene im Renderer (Cue-Felder) und eine lizenzierte Auswahl von Musikbett und Geräuschen.
4. Go für die Produktion. Gemini-Bedarf: 0 Anfragen (bezahlte Stimme passt).

## Stand 03.11.2026, früh

- **Bilder und Clips erzeugt:** 8 Bilder (16 Credits), 4 Kling-Clips (40 Credits), zusammen **56 Credits**, kein Ausschuss. Ablage und Nachweis: `C:\Automation\faceless-network\brands\military_history\assets\higgsfield\testvideo\` mit `LICENSE.md`. H8 (Visier) wird nicht verwendet, weil zwei Rohre auf einem Dreibein wie ein Geschütz wirken können; das Visier bleibt Linienzeichnung. Karte, Vitrine und Tische stammen aus der Bibliothek.
- **Umgesetzt** in `brands\military_history\rekonstruktion.py` (Bildebene `_media_layer`): Bilder und Clips unter den Szenen, Rahmen je Bild, Bewegungen (Push-in, Pull, Schwenk, Drift), Splitscreen links und rechts mit Wischöffnung, Lichtblitz, Pausfolie, Unschärfe für die Vitrine, Stempel „KI-REKONSTRUKTION“ in der Zeile des Zeitlineals, Schattierung oben und unten für die Lesbarkeit. Ton-Cues stehen je Beat im Plan (`data.cues`: whoosh, flare, fire, paper, scratch, stamp, click, bed_up) und landen mit der Klangfarbe aus `layout.sound` in `sound_cues.json` des Projekts (35 Cues), für die Tonebene des gemeinsamen Renderers.
- **Plan:** `data\direction\military_history-20261109-1-de.testvideo.json` (Sprechtext unverändert, bezahlte Stimme, 0 Gemini-Anfragen).
- **Trockenlauf** `storage\direction\military_history-20261109-1-de-T1dry5`: Story- und Regieprüfung ohne Fehler, HyperFrames lint und layout 0 Fehler, `overlap_check` ohne Überschneidungen, `small_text` leer; Sichtprüfung der Standbilder ohne Linien über Beschriftungen.
- **Offen:** Tonebene im Renderer, Go der Hauptsitzung für den Render. Danach Render über die Warteschlange (`--version T1 --reuse-voice storage\direction\voice_military_history-20261109-1-de_V1_gemini.wav`) und Export.
