# Vorlage Gritwerk – Version 0.9 (Entwurf)

Stand: 30.10.2026, 17:20 (Wien); Erklärschicht ergänzt am 30.10.2026 abends. Erstellt von der Kanal-Sitzung Gritwerk, nur mit Claude Code und dem lokalen Renderer, ohne Higgsfield. Version 1.0 erst nach Stefans Freigabe. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`motivation`, `brand_version: "0.9"`, `template_doc`).

Marke: Gritwerk (brand_id `motivation`), Nische Motivation und Selbstentwicklung. Versprechen: belegte Methoden statt Durchhalteparolen. Jedes Video zeigt eine konkrete kleine Handlung mit sichtbarem Fortschritt und nennt die Studie dahinter.

## Bausteine

| Baustein | Ort |
|---|---|
| Markendatei (Palette, Schriften, Logo, Claim, Hinweis) | `C:\Automation\faceless-network\brands\motivation\brand.yaml` |
| Gritwerk-Szenentypen | `brands\motivation\scenes.py` (Vertrag `src\fn\render\brand_scenes.py`) |
| Untertitel, Stimme | `brands\motivation\subtitle_style.json`, `audio_style.yaml` |
| Logo-Marke | `brands\motivation\assets\logo\gritwerk-mark.svg` (eigene Zeichnung: goldenes Tageskästchen mit Haken) |
| Schrift Fraunces (OFL 1.1) | `brands\motivation\assets\fonts\fraunces\` mit `OFL.txt` |
| Regie-System | `docs\direction-system.md` (Hook-Engine, Story-Engine, Prüfungen) |
| Beispiel-Plan | `data\direction\motivation-20261102-2-de.json` |
| Themenkalender November | `data\calendars\motivation_2026-11.json` (30 Themen, DE und EN, Quellen geprüft) |
| Testvideo | `OneDrive\Business\05 Produktion\Gritwerk\2026-11\2026-11-02 Gewohnheit 66 Tage\` |

## Stil „Cinematic Human" ohne KI-Menschenbilder

Keine Gesichter, keine Silhouetten, keine generierten Personen. Das Menschliche kommt aus der Handlung: eine Papierkarte, auf der jemand Tag für Tag ein Kästchen abhakt. Warm statt kühl: fast schwarzer warmer Grund mit Vignette, leichtes Filmkorn, Papier als einzige helle Fläche, Gold als einziger Akzent.

### Roter Faden: die Gewohnheitskarte

Papierkarte mit Auslöser (klein, z. B. „Nach dem Frühstück"), Handlung (groß, Fraunces, z. B. „ein Glas Wasser"), Raster aus Tageskästchen und Zähler „Tag n". Sie erscheint im Einstieg, in den Vergleichsstreifen und im Abschluss; die Statusleiste unten trägt ihren Namen („Glas Wasser") und je Szene einen Zustand. Je Video eine neue, zum Thema passende Handlung.

### Sechs Szenentypen für Gritwerk (seit Qualitätsrunde 31.10.2026)

Alle Szenen sind Gritwerk-Typen; die Gewohnheitskarte steht in jeder Szene (Leitobjekt) und ist 864 px breit (volle Inhaltsbreite). Jede Szene hat einen Push-in der Bühne und mindestens drei Bildereignisse an gesprochenen Wörtern (`w:Wort`).

| Funktion | Szenentyp | Was passiert |
|---|---|---|
| Einstieg (Cinematic Hook) | `gritwerk_tracker` | Karte kippt aus der Tiefe ins Bild, Kästchen füllen sich golden, Zähler läuft mit, bernsteinfarbener Stempel schlägt auf (z. B. „21 Tage?“, offene Frage), goldene Welle über die leeren Kästchen bis zum letzten (Goldring), Ziel im Kartenfuß (`goal`, z. B. „66 im Schnitt“); große Frage oben. |
| Erklärung | `gritwerk_study` | Die Studie als Gewohnheitskarte: Wochenspalten × 7 Tage füllen sich Woche für Woche mit Wochenzähler, Chip für die Stichprobe (`people`), der Auslöser wird golden unterstrichen und dann konkret (`cue` → `cue_to`), Skala „Wie automatisch?“ ohne Zahlen mit wanderndem Regler. |
| Daten / Demonstration | `gritwerk_curve` | Schematische Lernkurve, gezeichnet von einem Stiftpunkt; Papieretiketten an den Tagesmarken (die Zähler der Karte), Plateauband (`band`), Spannenbalken mit gemessenem Teil (voll) und hochgerechnetem Teil (gestrichelt, `measured_to`, `note`). Immer als „Schema“ beschriftet. |
| Vergleich (Comparison) | `gritwerk_streaks` | Zwei Streifen aus Tageskästchen füllen sich in Phasen an Wörtern (`phases`); im zweiten bleibt ein Kästchen leer (gestrichelt, Bernstein = offen) und pulsiert; Aussage darunter; Chip, der umschlägt (`chip` → `chip_to`); das nächste Kästchen bekommt Goldring und Haken (`next`). |
| Nutzen | `gritwerk_plan` | Die Karte setzt sich zusammen: Platzhalter „Handlung?“ und „Situation?“ werden an den Wörtern ersetzt, die Wochen wachsen von 3 auf 10 (Klammern „3 Wochen“, „10 Wochen“), drei Schritte darunter leuchten nacheinander. |
| Abschluss in der Handlung | `gritwerk_close` | Die Plan-Karte (10 Wochen); das erste Kästchen bekommt Goldring und Haken („Tag 1“), Chip „Morgen: Kästchen 2“, Kästchen 2 blinkt, darunter Gritwerk mit Markenkästchen, Claim und Hinweis mindestens 4 s lesbar. Kein Logo-Intro, keine Endkarte. |

Hook-Szenentypen: `gritwerk_tracker` (Standard) oder `cinematic_hook`. `data_flow` und `key_takeaway` sind für Gritwerk abgelöst (zu klein, kein Leitobjekt).

### Hintergrund mit Tiefe (Markenebene, seit 31.10.2026)

`LAYER` in `brands\motivation\scenes.py`, nur CSS und SVG, keine Bilder, keine KI-Bilder, keine fremden Clips: warmer Schreibtisch unter Lampenlicht. Ein großer Kalender aus Tageskästchen liegt in Perspektive als Tischfläche im unteren Bilddrittel (einzelne Kästchen golden), Lichtkegel und Strahlen von oben links, unscharfe Papierkarten an den Rändern, Staub im Licht, Holzmaserung, ruhiger Schleier über der Inhaltszone, Vignette. Die Kamera fährt je Szene einen Schritt (Schwenk, Push-in, leichte Neigung), der Kalender rückt um zwei Kästchenreihen (Parallaxe). Alle Bewegungen laufen deterministisch über die GSAP-Zeitleiste.

Übergänge: Kreisübergang aus einem Objekt der vorigen Szene (letztes Kästchen, Regler, Kästchen „morgen“) mit `data.plate: true` in der neuen Szene (dunkle Platte, bis der Kreis offen ist), sonst Überblendung 0,7 s. Die alte Szene blendet erst im Übergang aus.

## Farben

| Rolle | Wert | Einsatz |
|---|---|---|
| Grund | #121110 | ganzflächig, Vignette zur Mitte #1F1C19 |
| Fläche | #1F1C19 | Karten, Statusleiste |
| Text | #F4F0E8 | Überschriften, Untertitel |
| Text gedämpft | #A39C91 | Achsen, Unterzeilen |
| Akzent Gold | #E5B45A | gefüllte Kästchen, Hervorhebungswort, Fortschritt, Logo |
| Papier / Tinte | #F4F0E8 / #1B1712 | Gewohnheitskarte |
| Leeres Kästchen | #DDD5C8 | auf Papier |
| Bernstein (offen) | #E8873A | Stempel mit der Mythos-Frage, ausgelassener Tag, offene Zustände in der Statusleiste |
| Rot (Risiko) | #D4553F | nur für ein echtes Risiko; im Testvideo nicht verwendet |
| Grün (erreicht) | #8FB573 | nur für einen erreichten Zustand; im Testvideo nicht verwendet |

Begründung gegenüber `brands.yaml` (#121212 / #E5B45A / #F4F0E8): Grund und Flächen leicht ins Warme verschoben, damit Karten nicht grau wirken; Gold bleibt der Akzent und die aktive Farbe. Seit der Erklärschicht (30.10.2026) haben Bernstein, Rot und Grün feste Bedeutungen (siehe unten); in Version 0.9 waren sie auf Gold umgelegt und der ausgelassene Tag war terrakotta.

## Schriften (alle SIL Open Font License 1.1)

- Fraunces 700 (weiche Serif, `SOFT` 60–80): Fragen, Überschriften, Handlung auf der Karte, Zähler, Wortmarke. Quelle: github.com/google/fonts/tree/main/ofl/fraunces, geladen 30.10.2026.
- Inter 500–700: Untertitel, Beschriftungen, Statusleiste. Liegt im Repository (`assets\fonts\inter`).
- Abgelöst: Montserrat 900 in Versalien (Phase 1) – wirkte wie austauschbare Durchhalte-Typografie.

## Regeln

- Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), normale Schreibweise, Inter 700, 56 px, Hervorhebungswort Gold, 540 px vom unteren Rand.
- Bildmitte gefüllt: Inhaltszone y 290–1100, ein dominantes Motiv je Szene; Statusleiste y 1440, Fortschrittsbalken y 1548, „KI-generiert" 318 px vom Rand (frei von Plattform-Bedienelementen).
- Logo klein oben links (Kästchen 34 px plus GRITWERK in Versalien, gesperrt) ab dem ersten Bild.
- Anrede „du", warm, ruhig, ohne Pathos. Gemini-Stimme Sulafat („warm"), Stilanweisung in `audio_style.yaml`.
- Inhalt: jede Methode mit benannter Studie, Fachbuch oder Institution, URL und Abrufdatum im Plan; Befunde als „in der Studie …", nie als Versprechen. Keine Heilversprechen, keine psychologischen oder medizinischen Ratschläge, keine Prominenten- oder Guru-Zitate ohne belegte Quelle, keine erfundenen Zitate. Grenzen der Studie (Stichprobe, Hochrechnung) werden im Bild oder Text benannt, wenn sie die Zahl betreffen.
- Unbelegtes kommt in `unverified` und nicht ins Video.
- Gesprochener Aufruf am Ende: „Mehr Methoden mit Quelle: Folge Gritwerk." Claim „Methode statt Parole." Hinweis „Studienbasiert. Keine Therapie- oder Gesundheitsberatung."
- Länge 65–90 s; rund 160–175 Wörter ergeben mit Sulafat etwa 65–75 s (160 Wörter = 65,3 s Stimme).
- Musik: keine (keine Lizenzquelle gewählt).

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4,
           "status_bar": {"file": "<Handlung kurz>", "states": [{"beat": "b1", "text": "…", "tone": "amber|muted"}]}},
"assets": {}
```

Daten der Gritwerk-Szenen siehe Beispiel-Plan; Textgrenzen in `scenes.py` (`_LIM`), z. B. Frage ≤ 64, Handlung ≤ 26, Stempel ≤ 16, Markierung ≤ 22 Zeichen.

## Erklärschicht (seit 30.10.2026)

Gritwerk folgt der gemeinsamen Schnitt- und Layout-Vorlage `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md` (Renderer `src\fn\render\explainer.py`). Eingeschaltet in `brands\motivation\brand.yaml`, Block `explainer`:

```yaml
explainer:
  enabled: true
  voice_tag: {de: "SYNTHETISCHE STIMME", en: "SYNTHETIC VOICE"}
  opening: {de: "Synthetische Stimme · Quellen am Bildschirm · Keine Therapie oder Beratung", en: "Synthetic voice · Sources on screen · No therapy or advice"}
  opening_seconds: 3.5
  source_y: 1160
  colors: {fakt: "#E5B45A", auslegung: "#A98BD6", unsicher: "#E8873A", luecke: "#D4553F", beispiel: "#A39C91"}
```

| Bedeutung | Farbe | Form im Marker | Gritwerk-Einsatz |
|---|---|---|---|
| Fakt, aktiver Vorgang | Gold #E5B45A | Quadrat | belegte Aussage; gefüllte Kästchen, Kurve, Hervorhebung |
| Auslegung | Violett #A98BD6 (warm abgetönt) | Raute | eigene Folgerung ohne direkte Quelle, nur Marker ohne Leiste |
| Offen, unklar | Bernstein #E8873A | Halbkreis | Mythos-Frage, ausgelassener Tag, offene Zustände |
| Lücke, Risiko | Rot #D4553F | gestrichelter Kreis | nur bei echtem Risiko oder fehlendem Beleg |
| Erreicht | Grün #8FB573 (`palette.signal_green`) | – | nur für einen erreichten Zustand |
| Beispielwert | Grau #A39C91 | Chip | erfundene Zahlen im Bild |

Lage im Bild:
- Kopf (Kicker, Mono 24 px) bei y 186 unter der Logozeile.
- „SYNTHETISCHE STIMME“ steht oben rechts.
- Marker ab y 1160 (Höhe 44).
- Quellenleiste ab y 1216, höchstens zwei Zeilen bis etwa y 1278.
- Untertitel ab etwa y 1315, Statusleiste bei y 1440, Plattformtext ab y 1600.
- Alles bleibt links von x 930.

`source_y` liegt bei 1160 statt 1112 (Scutoria), weil die Gewohnheitskarte im Einstieg bis y 1140 reicht.

Regeln im Plan:
- `sources[].label` kurz halten, etwa „Lally et al. 2010“ oder „Gardner et al. 2012“. Die Leiste mit allen drei Quellen hat 96 von höchstens 100 Zeichen.
- `beats[].overlay` je Szene:
  - `kicker` mit eigener Zeile, z. B. „2 · DIE STUDIE“.
  - `marker` mit `marker_at` an einem gesprochenen Wort.
  - `transition`: Kreisübergang aus einem Punkt der vorigen Szene (Station 3 der Erklärung, das leere Kästchen) oder Überblendung 0,7 s.
  - `vignette` bei Nahaufnahmen wie den Vergleichsstreifen.
  - Im Abschluss `head: false` und `marker: "none"`.
- Eigene Marker in den Szenen: keine. Quellen stehen nur in der Quellenleiste der Erklärschicht; die Szenen tragen keine Chips, die dem Marker widersprechen.
- Wortanker: Alle Zeitfelder der Gritwerk-Szenen nehmen Sekunden oder `w:Wort[#n]`, z. B. `stamp_at`, `fill_at`, `people_at`, `cue_to_at`, `rate_at`, `markers[].at`, `band.at`, `range.at`, `range.extra_at`, `phases[].at`, `miss_at`, `chip_to_at`, `next.tick_at`, `steps[].at`, `grow_at`, `tick_at` und `name_at`. Die Funktion `_rel` in `scenes.py` löst sie über die gesprochenen Wörter der Szene auf.
- Storyboard je Video unter `01 Skript\Storyboard.md`. Spalten: Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild.
- Vertonung nur mit Gemini, entweder neu oder vorhanden über `--reuse-voice`. Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme.

## Ablauf je Video

1. Thema aus `data\calendars\motivation_2026-11.json` (Quellen, Befund, Einschränkungen und „nicht verwenden" stehen in `notes`); Primärquelle selbst öffnen und Zahlen gegen Abstract oder Volltext prüfen.
2. Plan `data\direction\motivation-<JJJJMMTT>-<slot>-de.json` nach dem Beispiel schreiben (fünf Hook-Kandidaten, je einer pro Typ, Wahrheit mindestens 4), dann Trockenlauf:
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --no-render`
3. Standbilder prüfen: `npx hyperframes snapshot . --at <Zeiten> --no-end -o <absoluter Pfad>` im Ordner `storage\direction\<id>-dry\project`.
4. Vertonung (eine Gemini-Anfrage, ohne Sperre möglich): `... --version V1 --tts gemini --no-render`.
5. Sperrdatei `data\render.lock` prüfen und anlegen, Speicher prüfen (`fn.cli status`, Grenze 30 GB), dann Vollfassung ohne neue Kosten:
   `... --version V1 --reuse-voice storage\direction\voice_<id>_V1_gemini.wav --mirror gritwerk-regie/<datum>`; Sperrdatei danach entfernen.
6. Produktionsordner aus `_Vorlage Video` füllen (Skript, Export, Cover, Untertitel, `Veröffentlichung.md`), Zeile in `04 Redaktionsplan\Redaktionsplan.csv`. Nichts veröffentlichen.

Hinweis: `scripts\export_production_folder.py` liest seit 30.10.2026 Abschlusssatz und Domain aus `brand.yaml` (`production`, für Gritwerk eingetragen) und kann für Schritt 6 genutzt werden; es überschreibt dabei `Skript.md` und `Veröffentlichung.md` mit einer kürzeren Fassung. Das Testvideo wurde von Hand befüllt (ausführlichere Aussagenprüfung im Skript, Texte je Plattform).

## Testvideo 2026-11-02 (Stand 30.10.2026)

68,3 s, Prüfbericht VALIDATED (26 von 26 Prüfungen), −16,3 LUFS, Hook H1, Kosten 0,0163 USD (eine Gemini-Vertonung), Render 92 s. Ordner `05 Produktion\Gritwerk\2026-11\2026-11-02 Gewohnheit 66 Tage\`, Vorschau mit Standbildern `05 Produktion\_Demos\gritwerk-regie\`.

Fassung V2 (30.10.2026 abends): Erklärschicht, Wortanker, Farben mit fester Bedeutung, gleiche Gemini-Stimme (`--reuse-voice`, keine neuen Kosten). VALIDATED, 26 von 26, 68,3 s, 31 Bildereignisse, Render 242 s. Storyboard in `01 Skript\Storyboard.md`, Standbilder in `05 Produktion\_Demos\gritwerk-regie\2026-11-02-v2\` (`kontrolle_6_standbilder.jpg`). V1-Export liegt in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-30 Layout-Umstellung`.

Fassung Q1 (31.10.2026, Qualitätsrunde nach `02 Marke\Qualitätsrunde 2026-10-31.md`): Markenebene mit Tiefe, Gewohnheitskarte in allen sechs Szenen, `gritwerk_study` und `gritwerk_plan` statt `data_flow` und `key_takeaway`, 47 Bildereignisse (Median-Abstand 1,3 s), Kreisübergänge aus Objekten. Gleiche Gemini-Stimme (`--reuse-voice`, keine neuen Kosten). VALIDATED, 26 von 26, 68,3 s, −16,3 LUFS, Überschneidungs-Prüfung ohne Befund, Render 131 s. Eigene Note 1,8. Kontaktbogen `05 Produktion\Gritwerk\2026-11\2026-11-02 Gewohnheit 66 Tage\03 Schnittprojekt\Kontaktbogen Q1.jpg`, Vorschau `05 Produktion\_Demos\gritwerk-regie\2026-11-02-q1\`. V2-Export, alte Markendateien und die Exportfassungen von `Skript.md` und `Veröffentlichung.md` liegen in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde`. Die Handfassungen von `Skript.md` und `Veröffentlichung.md` bleiben gültig, weil `export_production_folder.py --force` weiterhin interne Prüfnotizen in die Quellen und den Abschlusssatz doppelt schreibt.

## Offen für Version 1.0

- Freigabe der Optik und der Stimme durch Stefan.
- Englische Fassung (zweite Vertonung nötig).
- Ob der Abschluss einen Handle zeigen soll, sobald das Konto existiert (derzeit nur der Name Gritwerk).
- Optional: Vergleich mit einer Higgsfield-Fassung (nicht beauftragt).
