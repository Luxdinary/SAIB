# Vorlage Revlore (nur Claude Code) – Version 0.9

Stand: 30.10.2026 (Wien), Qualitätsrunde Q1 am 31.10.2026 ergänzt. Erstellt von der Kanal-Sitzung Revlore. Version 0.9 = Entwurf zur Abnahme; 1.0 erst nach Stefans Freigabe. Mit dieser Datei kann jede Sitzung Revlore-Videos nur mit Claude Code und dem lokalen Renderer bauen, ohne Higgsfield und ohne Fremdmaterial. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`engines`, `brand_version: "0.9"`, `template_doc`).

## Marke in einem Satz

Revlore (brand_id `engines`) erklärt Motorentechnik an einem laufenden, gerechneten Schnittmodell: Präzision statt Effekt, jede Bewegung physikalisch richtig, jede Zahl belegt oder im Bild nachgerechnet.

## Bausteine

| Baustein | Ort |
|---|---|
| Renderer-Marke (Palette, Schriften, Logo, Abschlusssatz) | `C:\Automation\faceless-network\brands\engines\brand.yaml` |
| Revlore-Szenentypen (Kinematik, Steuerzeiten, Zeichnung, CSS) | `brands\engines\scenes.py`, geladen über `fn.render.brand_scenes` (`docs\direction-system.md`, Abschnitt 6d) |
| Logo | `brands\engines\assets\logo\revlore-mark.svg` (Kurbelzapfen-Marke) |
| Untertitel, Stimme | `brands\engines\subtitle_style.json`, `audio_style.yaml` |
| Regie-System | `docs\direction-system.md` (Hook-Engine, Story-Engine, Prüfungen) |
| Beispiel-Plan | `data\direction\engines-20261105-1-de.json` |
| Themenkalender | `data\calendars\engines_2026-11.json` (30 Themen ab 05.11.2026) |

## Gestaltung

**Stil „Precision Engineering, technisch“**: Schnittansichten mit 45-Grad-Schraffur für geschnittene Flächen, Explosionszeichnung, Bemaßungslinien (OT, UT, Hub), Bauteile mit kausaler Bewegung. Keine dekorativen Motorbilder, kein Neon, kein Glow, keine Lichtkegel (`flat: true`). Bewegung kommt aus der Mechanik selbst.

**Palette** (geändert gegenüber dem Entwurf in brands.yaml, Begründung: blauer Fließtext auf Graphit ermüdet und konkurriert mit Blau als Bewegungsfarbe; Silber als Akzent war zu schwach):

| Rolle | Hex | Verwendung |
|---|---|---|
| bg | #171C22 | Graphit-Grund (unverändert), Haarlinienraster |
| surface | #222932 | Schnittflächen, Leistenfelder, Chips |
| text | #E7ECF1 | Titel, Untertitel |
| muted | #8D99A6 | Nebenbeschriftungen |
| accent | #2F9BFF | der eine Akzent: Bauteil im Fokus, Frischladung, Marker der Arbeitsspiel-Leiste |
| steel / steel_dark | #AEB9C5 / #5E6A76 | Metallteile; Beschriftungen in Stahl |
| hatch | #4A5562 | Schnitt-Schraffur |
| combustion | #FF7A2F | nur Zündfunke und brennende Ladung |
| exhaust | #7D8794 | Abgas, Auslassventil |

**Schriften** (alle SIL OFL 1.1, Dateien und Lizenzen in `C:\Automation\faceless-network\assets\fonts\`): Oswald 600 (Titel, Zahlen), Inter 700 (Untertitel), JetBrains Mono (Beschriftungen, Rechnungen).

**Logo**: Kurbelzapfen-Marke (Lagerkreis, Hubzapfen in Akzentblau, Pleuel) 40 px oben links plus Wortzeichen REVLORE als Text, ab dem ersten Bild. Kein Logo-Intro, keine Endkarte, kein Handle im Bild (exakte Handles @revlore sind von Kleinstkonten belegt).

## Roter Faden

1. **Zylinder 1 im Schnitt**: dasselbe Modell (Zweiventiler mit zwei obenliegenden Nockenwellen, Dachbrennraum) erscheint im Hook, in den Takt-Szenen und im Abschluss.
2. **Arbeitsspiel-Leiste** unten (y 1468, seit der Erklärschicht unter den Untertiteln): vier Felder Ansaugen, Verdichten, Arbeiten, Ausstoßen über 0–720 Grad Kurbelwinkel, blauer Marker läuft mit dem Kurbelwinkel. Sie ersetzt die Statusleiste von Scutoria.

## Mechanik (gerechnet, nicht gezeichnet)

- Kurbeltrieb: Kurbelradius 100 px, Pleuel 320 px (Verhältnis 0,31). Kolbenbolzen y = CY − (R cos θ + √(L² − R² sin² θ)); Pleuel folgt Bolzen und Hubzapfen.
- Drehrichtung im Bild: Kurbelwelle im Uhrzeigersinn; Nockenwellen gleichsinnig mit halber Drehzahl (Riemen oder Kette, S1, S5).
- Kurbelwinkel 0 = OT zu Beginn des Ansaugtakts. Steuerzeiten im Modell: Einlass öffnet 10 Grad vor OT, schließt 40 Grad nach UT; Auslass öffnet 40 Grad vor UT, schließt 10 Grad nach OT (innerhalb der Spannen in MIT 2.61 Lecture 8). Ventilhub aus demselben Nockenprofil, das gezeichnet ist (Nockenspitze trifft den Stößel im Hubmaximum).
- Zündung 30 Grad vor OT (MBT-Beispiel MIT 2.61 Lecture 9). Im gesprochenen Text nur „kurz vor dem oberen Totpunkt“.
- Diese Werte sind typische Werte, kein bestimmter Motor; das steht in `post.json` und `Veröffentlichung.md`.

## Szenentypen (fünf, für Revlore angepasst)

| Typ im Plan | Rolle | Was sich bewegt | Daten (`data`) |
|---|---|---|---|
| `rv_hook` (einziger Hook-Typ, `HOOK_SCENE_TYPES`) | Mechanischer Hook | laufender Schnittmotor, Zähler „Umdrehungen“ und „Zündungen“, große Aussage | `claim`, `claim_lines`, `claim_highlight`, `claim_at`, `theta` |
| `rv_exploded` | Explosionsansicht | Kolben, Bolzen, Pleuel, Kurbelwelle auseinander, beschriftet, fügen sich zusammen, drehen; Bemaßung OT, UT, Hub, Bogen „½ Umdrehung“ | `title`, `assemble_at`, `dims_at`, `theta` |
| `rv_cutaway` | Schnittansicht | Kolben, Pleuel, Kurbel, Ventile, Nocken, Gasfüllung (blau frisch, orange Verbrennung, grau Abgas), Zündfunke, Strömungspfeile; Beschriftungen mit Führungslinie; Abschluss mit Chips und Markenzeile | `mode`, `num`, `title`, `labels`, `labels_at`, `stroke_dims`, `chips`, `cta`, `theta` |
| `rv_drive` | Bewegungsablauf Steuertrieb | Kurbel- und Nockenwellenrad 1 : 2 mit laufendem Riemen, Zähler Umdrehungen | `title`, `teeth_crank`, `teeth_cam`, `note`, `theta` |
| `rv_readout` | Messwert und Rechnung | Drehzahlmesser, Zeiger, Rechenzeilen erscheinen zum gesprochenen Wort | `gauge_max`, `gauge_value`, `gauge_unit`, `gauge_at`, `lines[{text, hl, at}]`, `theta` |

Zeitangaben: `at` ist ein Anteil des Beats (0 bis 1) oder `"w:<Wort>"` = Beginn dieses gesprochenen Worts (`SceneCtx.words`, Wortzeiten aus der Transkription). `theta` ist eine Liste von Stützpunkten `[at, Grad]`; Winkel laufen fortlaufend weiter, aufeinanderfolgende Beats schließen ohne Sprung an (Positionen werden modulo 720 gezeichnet). Szenen ohne Ventiltrieb (Explosionsansicht, Steuertrieb) dürfen bei einem Vielfachen von 360 Grad neu ansetzen.

Textgrenzen (Prüfbericht `readability_text_limits`): Titel 30, Aussage 64, Chip 18, Rechenzeile 36 Zeichen.

## Regeln

- Kein Logo-Intro, keine Endkarte; Abschluss in der Handlung (`rv_cutaway` mit `chips` und `cta`, der Motor läuft bis zum letzten Bild). „KI-generiert“ dauerhaft im Bild.
- Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), normale Schreibweise, Hervorhebung in Akzentblau.
- Bildmitte gefüllt: Das Modell steht zwischen y 345 und 1175 und füllt rund 90 % der Inhaltsbreite, Beschriftungskarten links ab x 120 und rechts bis x 918 (seit Q1). Darunter folgen Marker und Quelle (y 1190 bis 1308), die Untertitel (unten bei y 1452) und die Leiste (ab y 1468). Siehe Abschnitt „Erklärschicht“.
- Gesprochener Aufruf am Ende: „Motorentechnik verstehen: Folge Revlore.“ Anrede „du“.
- Länge 65–90 s; etwa 160–170 Wörter ergeben mit Gemini (Iapetus) voraussichtlich 70–80 s. Vertont wird nur mit Gemini; die Windows-Stimme (SAPI) ist seit 30.10.2026 nicht mehr zulässig.
- Jede technische Aussage aus Hersteller-, Norm- oder Fachquelle mit URL und Abrufdatum; Typwerte als Typwerte kennzeichnen; Unbelegtes in `unverified`.
- Keine Wartungs-, Reparatur- oder Tuningempfehlung, keine Schadensdramatik, keine Marken-Abwertung.
- Bewegung muss physikalisch stimmen: Taktfolge, Drehrichtung, Ventilsteuerung, Übersetzung. Neue Mechanik (z. B. Zweitakt, Turbolader) erst mit eigener Szene und Quelle.

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 468, "caption_width_px": 800, "caption_transform": "none",
           "outro": false, "tail_seconds": 2.6, "progress_y": 1556, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4,
           "description": "...", "companion_text": "...", "hashtags": ["motorentechnik", "..."]},
"assets": {}
```

## Erklärschicht

Seit 30.10.2026 gelten die Regeln aus `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`. Technisch erledigt das der gemeinsame Renderer `src\fn\render\explainer.py`. Revlore schaltet die Schicht in `brands\engines\brand.yaml` ein, im Block `explainer`.

**Feste Elemente**
- Oben rechts steht durchgehend „SYNTHETISCHE STIMME“.
- Die Einstiegszeile läuft von 0 bis 3,5 s: „Synthetische Stimme · Quellen am Bildschirm · Schema, keine Wartungsanleitung“.
- Der Kopf besteht aus Kicker und Titel:
  - Kicker in Mono 24 px bei y 186, zum Beispiel „3 · TAKT 1 VON 4“.
  - Darunter steht der Szenentitel der Revlore-Szene als Kopftitel, mittig (x 540), Grundlinie y 318, Oswald 64 px (seit Q1, 31.10.2026; vorher links bei y 272, das überdeckte die Kicker-Zeile).
  - Die Taktnummer steht im Kicker, nicht mehr im Titel; das Feld `num` bleibt leer.
  - Der Hook hat keinen Kopf, der Abschluss auch nicht (`"head": false`).

**Senkrechte Aufteilung (1080 × 1920)**

| Bereich | y |
|---|---|
| Logo, Stimmenhinweis | 120–160 |
| Kicker | 186–218 |
| Szenentitel (mittig) | 242–335 |
| Modell, Szene | 345–1175 |
| Marker (Kapsel) | 1190–1234 (`source_y: 1190`) |
| Quellenleiste, höchstens zwei Zeilen | 1246–1308 |
| Untertitel, ein oder zwei Zeilen | bis 1452 (`caption_bottom_px: 468`) |
| Arbeitsspiel-Leiste | 1468–1534 |
| Fortschritt | 1556 (`progress_y`) |
| „KI-generiert“ | bis 1602; darunter liegt der Plattformtext |

Rechts bleibt x ab 930 frei für die Plattform-Symbole. Die rechten Beschriftungen enden bei x 920, die Hook-Zähler stehen bei x 190 und 860.

**Farben mit fester Bedeutung** (`explainer.colors`)

| Bedeutung | Farbe | Form im Marker |
|---|---|---|
| Fakt, aktiver Vorgang | #2F9BFF (Akzent) | Quadrat |
| Auslegung | #9B6BFF | Raute |
| Unsicher, offen | #F5B342 | Halbkreis |
| Lücke, nur bei einem Risiko | #FF5A5A | gestrichelter Kreis |
| erreicht | #3FCF8E | nur für einen erreichten Zustand |
| Beispielwert | #8D99A6 | Rahmen |

Orange (#FF7A2F) zeigt nur die brennende Ladung und den Funken. Es ist ein physikalischer Zustand, keine Bedeutungsfarbe.

**Im Plan je Szene (`beats[].overlay`)**
- `kicker`: eigener Text.
  - Takte als „TAKT n VON 4“.
  - Sonst „DER GRUND“, „STEUERTRIEB“, „DER KERN“.
- `marker`: `fakt` bei belegter Aussage.
  - `marker_at` liegt auf dem Wort, das die belegte Aussage trägt, zum Beispiel `w:Totpunkt` oder `w:öffnet`. Wenn möglich auf ein Wort, an dem ohnehin eine Bildaktion liegt, damit keine Bildwechsel im Abstand unter einer Sekunde entstehen.
  - Im Hook hat der Marker keine Quellenleiste (`"source": false`): Sie wäre nur etwa 1,4 s sichtbar, und die Quelle folgt in Szene 2.
- `example: true`: Chip „Beispielwert“ für erfundene Zahlen.
  - Beispiele: Zähnezahlen im Steuertrieb, die gewählte Drehzahl in der Rechnung.
  - Belegte Typwerte (Steuerzeiten innerhalb der MIT-Spannen, Zündung 30 Grad vor OT als MIT-Beispiel) laufen als Fakt mit Quelle. Gradzahlen werden nicht genannt.
- `transition`:
  - Kreis (`iris`) aus der Kurbelwellenmitte (540, 1010) dort, wo dasselbe Bauteil weiterläuft, also von der Explosionsansicht in die Schnittansicht und von der Schnittansicht in den Steuertrieb.
  - Sonst Überblendung (`blende`, 0,7 s).
  - Zwischen den Takten harter Schnitt, die Bewegung läuft durch.
  - Szenen an einem Übergang bekommen `fade_in: false` beziehungsweise `fade_out: false`, sonst blendet die Szene unter dem Kreis aus.
- `vignette`: nur bei einer Nahaufnahme. Bisher gibt es keine.

**Quellen**: Jede Quelle bekommt ein kurzes `label`, zum Beispiel „NASA Glenn, Viertaktmotor“, „MIT 2.61, Vorlesung 8“ oder „Schaeffler, Steuertrieb“. So passt die Leiste mit Abrufdatum in höchstens zwei Zeilen (100 Zeichen).

**Eigene Marker der Szenen**: Der Steuertrieb zeigt keinen eigenen Hinweis „Zähnezahlen: Beispiel“ mehr (`"note": ""`). Stattdessen leuchten die Zähnezahlen beim Wort `note_at` blau auf, und den Hinweis gibt der Chip „Beispielwert“.

**Storyboard**: Je Video kommt `01 Skript\Storyboard.md` in den Produktionsordner, mit den Spalten Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild und Text im Bild. Muster ist `05 Produktion\Revlore\2026-11\2026-11-05 Zwei Umdrehungen\01 Skript\Storyboard.md`.

**Prüfen ohne Stimme**:
- Das Layout prüft nur ein Trockenlauf ohne Stimme: `--version V2dry --tts mock --no-render`. Er prüft Layout und Wortanker.
- Standbilder entstehen mit `npx hyperframes snapshot . -o ../snapshots --at <Zeiten>` im Ordner `project` des Trockenlaufs. Dabei die Übergangsmomente mitnehmen.
- `04 Export` bleibt leer, bis die Gemini-Stimme da ist. Die Endfassung rendert die Hauptsitzung.
- Die Mock-Stimme ist schneller als Gemini, deshalb sind ihre Zeiten nur ein Anhalt. Am 30.10.2026 lag der Median der Bildwechsel damit knapp unter 1,2 s (Warnung, kein Fehler); mit den Gemini-Zeiten neu prüfen.

**Deckender Szenengrund**: Revlore-Szenen haben einen eigenen deckenden Grund mit demselben Haarlinienraster (`.scene-inner.rv`). Sonst scheint bei Kreisübergang und Überblendung die alte Szene durch.

## Qualitätsrunde Q1 (31.10.2026)

Grundlage: `02 Marke\Qualitätsrunde 2026-10-31.md`. Umgesetzt in `brands\engines\scenes.py`, gilt für jedes neue Revlore-Video.

- **Hintergrund mit Tiefe, nur Code** (`_backdrop`): Graphit-Verlauf, Lichtabfall von oben links, abgedunkelter Rand, feines (24 px) und grobes (96 px) Zeichenraster, die mit 5 px/s nach oben wandern, Geisterzeichnungen (Kettenrad, Kurbelkröpfung, Kreise mit Mittellinien) mit Schwebebewegung und Drehung als Parallaxe. Alles hängt an der absoluten Zeit, deshalb läuft es über harte Schnitte durch. Kein Glühen, keine Lichtkegel (`flat` bleibt).
- **Motor groß**: Ansaugsammler und Saugrohr links, Abgaskrümmer rechts, Kopf x 330–750, Block mit Wassermantel x 350–730, Kurbelgehäuse im Schnitt. Schnittansicht mit `view` (Standard Maßstab 0,9, Oberkante y 371): x 162–918, y 353–1154, Kurbelwellenmitte bleibt bei 540/1010 (Kreisübergänge treffen die Kurbel). Hook 0,74 (Oberkante 470), Abschluss 0,85 (Oberkante 400); im Plan je Szene `data.view: {s, top}`.
- **Material**: Stahlverlauf auf Kolben, Ventilen und Zündkerze, Lichtkante am Pleuel, Schlagschatten und Bodenschatten. Strömung als bewegte Striche durch Saugrohr (blau) und Krümmer (grau), nur solange das Ventil offen ist.
- **Beschriftungen als Karten** (`_card`): Mono 30 px, Karte mit Farbleiste, Führungslinie mit Punkt. Links ab x 120, rechts bis x 918. Im Plan: `labels` als Schlüssel oder `{key, side, y}`; freie Notizen `notes: [{text, at, side, y, to: [x, y nativ], color}]`, nur Gesprochenes wiederholen.
- **Leitobjekt und Statusleiste**: Zylinder 1 in allen Szenen; die Arbeitsspiel-Leiste (x 108–922) hat links die Kachel „Zyl. 1“ mit mitlaufendem Kolben und steht in allen Szenen, auch Hook und Explosionsansicht. Explosionsansicht: `count_at` lässt die vier Felder beim Wort nacheinander aufleuchten.
- **Bewegung**: Push-in 2,5 % je Szene; mindestens drei Bildereignisse je Szene an Wörtern (Karten, Marker, Zähler, Funke). Steuertrieb: `half_at` lässt die Nockenwellenkarte beim Wort aufleuchten.
- **Prüfen**: Trockenlauf mit echter Stimme ohne Video (`--reuse-voice <wav> --no-render --version <x>dry`) liefert das Projekt mit Gemini-Zeiten; daran `node scripts\overlap_check.mjs` und `npx hyperframes snapshot`, erst dann rendern.

## Ablauf je Video

1. Thema aus `data\calendars\engines_2026-11.json`, Quellen lesen, Plan `data\direction\<video_id>.json` schreiben (Vorlage: Beispiel-Plan), mit `overlay` je Szene und `label` je Quelle (Abschnitt „Erklärschicht“). Storyboard in `01 Skript\Storyboard.md`.
2. Trockenlauf ohne Kosten:
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --no-render --mirror revlore-regie/dry`
3. Render-Sperre `data\render.lock` prüfen (jünger als 20 Minuten: warten), freien Platz prüfen (`fn.cli status`, Grenze 30 GB), Sperre mit `engines` und Uhrzeit anlegen.
4. Vertonung (Gemini Flash TTS, eine Anfrage) und Vollfassung:
   `... --version V1 --tts gemini --mirror revlore-regie/<datum>`; Korrekturen ohne Kosten mit `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`. Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme.
5. Sperre entfernen. Produktionsordner füllen: `.venv\Scripts\python.exe scripts\export_production_folder.py data\direction\<id>.json --version V1 --short "<Kurztitel>"`, Skript-Abschnitt „Roter Faden“ auf Revlore anpassen.
6. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`, nichts veröffentlichen.

## Offen bis Version 1.0

- Stefans Abnahme von Optik, Palette und Stimme (Testvideo `05 Produktion\Revlore\2026-11\2026-11-05 Zwei Umdrehungen`).
- Gemini-Vertonung des Testvideos: erledigt (Fassung V2, Iapetus, 71,9 s Sprache); Fassung Q1 der Qualitätsrunde verwendet sie unverändert wieder.
- Zweites Thema mit derselben Vorlage rendern (Wiederverwendungstest, z. B. „Ventilüberschneidung“).
- Musik: keine Lizenzquelle; bisher ohne Musik.
