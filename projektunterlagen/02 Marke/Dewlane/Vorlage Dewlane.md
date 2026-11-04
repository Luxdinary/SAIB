# Vorlage Dewlane – Version 0.9 (Entwurf)

Stand: 31.10.2026 (Wien), Qualitätsrunde Q1 eingearbeitet (der Abschnitt „Qualitätsrunde Q1“ am Ende gilt vor älteren Angaben). Erstellt von der Kanal-Sitzung Dewlane, nur mit Claude Code und dem lokalen Renderer, ohne Higgsfield und ohne Kosten außer der einen Vertonung. Version 1.0 erst nach Stefans Freigabe. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`beauty`, `brand_version: "0.9"`, `template_doc`).

Marke: Dewlane (brand_id `beauty`), Nische: Wissen über Inhaltsstoffe, Hauttypen, Routinen und Kennzeichnungen. Ziel laut Stefan: Beauty-Marken sollen später auf dem Kanal Werbung schalten; es gibt noch keine Produkte und keine Partner. Darum ist der Kanal reines Wissen, ohne Empfehlungen.

## Bausteine

| Baustein | Ort |
|---|---|
| Markendatei (Tokens, Schriften, Logo, Regeln) | `C:\Automation\faceless-network\brands\beauty\brand.yaml` |
| Stil und Skriptregeln | `brands\beauty\visual_style.md`, `brands\beauty\script_prompt.md` |
| Untertitel, Aufruf, Stimme | `brands\beauty\subtitle_style.json`, `outro_config.json`, `audio_style.yaml` |
| Logo | `brands\beauty\assets\logo\dewlane-mark.svg` (Tautropfen mit Haarlinie, selbst gezeichnet) |
| Markeneigene Szenen und Hintergrund | `brands\beauty\scenes.py`: seit Q1 sieben eigene Dewlane-Szenen um das Leitobjekt Etikett und `LAYER` (Hintergrund mit Tiefe aus Code); Stand V2 gesichert in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde\Dewlane V2 Stand (vor Q1)` |
| Hintergrundclips (seit Q1 nicht mehr im Plan, bleiben für spätere Videos) | `brands\beauty\assets\clips\` (5 Clips à 16 s, `LICENSE.md`, `manifest.json`, Quell-HTML in `sources\`); lokal aus SVG/CSS gerendert, kein Higgsfield, kein Fremdmaterial, 0 USD. Im Plan `"assets": {"folder": "assets/clips", ...}` |
| Regie-System | `docs\direction-system.md` (Hook-Engine, Story-Engine, Szenentypen, Prüfungen) |
| Beispielplan | `data\direction\beauty-20261105-1-de.json` (Testvideo INCI-Liste) |
| Themenkalender | `data\calendars\beauty_2026-11.json` (30 Themen, je DE und EN, Quellen) |
| Testvideo | `OneDrive\Business\05 Produktion\Dewlane\2026-11\2026-11-05 INCI-Liste\` |

## Stil: Luxury Editorial, hell

- Heller Elfenbeingrund, Karten in Porzellanweiß mit Haarlinie, Überschriften in Playfair Display, Text und Untertitel in Inter. Keine Monospace-Schrift.
- Produkttexturen nur als abstrakte Formen: Tautropfen mit Ringen, Cremeschliere, Flakon-Silhouette ohne Marke und ohne Schrift, Blütenflächen, Routinelinie mit drei Punkten. Keine Gesichter, keine Haut, keine echten Produkte.
- Ruhige Bewegung: `flat: true` (kein Glühen in den gemeinsamen Teilen). Seit Q1 in den eigenen Szenen Push-in 3 bis 5 % je Szene und eine Kamerafahrt des Hintergrunds bei jedem Szenenwechsel; Einblendungen einmalig, 0,3 bis 0,6 s.
- Logo klein oben links: Tropfen-Marke 40 px plus Wortzeichen DEWLANE (Playfair, Versalien, Laufweite 0,18 em). Kein Logo-Intro, keine Endkarte.

### Palette (begründet verbessert)

Der Phase-1-Entwurf aus `brands.yaml` (Akzent #C98F93, Text #6C4B50, gedämpft #AB9798) erreichte auf Elfenbein nur 2,4:1 bzw. 2,5:1; als Schriftfarbe zu schwach für Handy-Untertitel. Grund und Rosé bleiben, Schriftfarben sind abgedunkelt (WCAG-Kontrast berechnet):

| Rolle | Farbe | Kontrast | Verwendung |
|---|---|---|---|
| Grund | #F8F3EF | – | Fläche |
| Karte | #FFFCF9 | – | Karten, Statusleiste |
| Text | #4A2F34 | 10,9:1 | Überschriften, Untertitel |
| Gedämpft | #7E6468 | 4,9:1 | Beschriftungen, „KI-generiert“ |
| Akzent | #9B5560 | 4,9:1 | Hervorhebungswort, Linien, Nummern |
| Blush | #C98F93 | 2,4:1 | nur Formen und Clips, nie Schrift |
| Honig (offen) | #946420 | 5,0:1 | Kennzeichen „Unsicher“, offene Fragen |
| Beere (Stopp) | #8E2F45 | 7,8:1 | nur der eine Stopp am Schluss |
| Salbei | #4F7A62 | 4,8:1 | nur „geregelt“ |

Schriften: Playfair Display und Inter, beide SIL Open Font License 1.1 (Dateien und Lizenztexte in `C:\Automation\faceless-network\assets\fonts\`).

## Szenentypen (an Dewlane angepasst)

Die fünf Grundtypen des Regie-Systems werden über Markentokens, Daten und Hintergrundclips angepasst; der gemeinsame Renderer bleibt unverändert.

| Szenentyp | Dewlane-Fassung | Hintergrundclip |
|---|---|---|
| `cinematic_hook` (Dewlane-Variante) | neutrales Etikett „Ingredients“ mit abstrakten Zeilen (keine erfundene Rezeptur), ein Tautropfen landet darauf, Zeile 1 wird in Honig eingekreist, große Frage in Playfair | `bg_routine_line.mp4` (nie `bg_drop_ripple`, sonst doppelter Tropfen) |
| `data_flow` | Weg eines Begriffs: Stoff → Glossar-Name → Etikett; Kennzeichen am Glossar | `bg_petal_bands.mp4` |
| `comparison` (nur `versus`) | „Sie zeigt“ / „Sie zeigt nicht“; Quadrat = Fakt, gestrichelter Kreis = Lücke | `bg_flacon.mp4` |
| `key_takeaway` (Liste) | drei nummerierte Karten „So liest du …“ | `bg_petal_bands.mp4` |
| `ui_demo` | **nicht verwendet**: keine echten Bildschirmaufnahmen; Produktfotos wären Produktplatzierung | – |
| `file_beside`, `file_fork`, `file_close` (Dewlane-Varianten) | die INCI-Liste als weiße Etikettkarte mit Zeilen (roter Faden); Chip „Unsicher“ nur mit `risk_open: true`, je Route abschaltbar mit `"open": false`; Abschluss in der Handlung | `bg_cream_swirl.mp4`, `bg_drop_ripple.mp4`, `bg_flacon.mp4` |

Zusätzlich vorbereitet für Routinethemen: `bg_routine_line.mp4` als Hintergrund für Routinediagramme (`data_flow` mit Schritten Reinigen → Pflegen → Sonnenschutz, jeweils nur mit Quelle).

Nicht verwenden: `comparison` im Modus `negate` (der Stempel ist auf hellem Grund unsichtbar) und `key_takeaway` im Modus `closing` (zeichnet ein Schild, Scutoria-Motiv). Renderer-Wünsche dazu sind an die Hauptsitzung gemeldet; beides ließe sich auch als Dewlane-Variante in `scenes.py` lösen.

Clipfolge: zwei gleiche Clips nicht direkt hintereinander; die Reihenfolge je Video wechseln. Testvideo V2: routine, petals, swirl, drop, flacon, petals, flacon (V1 hatte petals im Hook und routine unter dem Datenfluss).

## Testvideo 30.10.2026 (Ergebnis)

- Thema „INCI-Liste lesen: Was ganz vorne auf deiner Creme steht“, Hook H1 („Das erste Wort auf deiner Creme verrät, wovon am meisten drin ist.“), 162 Wörter, 81,1 s.
- Prüfbericht: alle technischen, inhaltlichen und Regie-Prüfungen bestanden (Szenenvielfalt 7 Typen, längste Strecke ohne Bildwechsel 8,5 s, Untertitel 56 px, Plattform-Überdeckung frei, −16,1 LUFS). Offen: `tts_provider_publishable` (Windows-SAPI-Entwurfsstimme) und `risk_high_review` (gewollt).
- Vertonung offen (nur Gemini): Das Gemini-Tageskontingent (Free Tier, 10 Anfragen je Tag und Modell) war erschöpft (Fehler 429). Die Fassungen V1/V2 mit Windows-Stimme waren nur Layoutprüfungen; seit Stefans Regel (30.10.2026 abends) gibt es keine Windows-Stimme mehr. Die Hauptsitzung vertont mit Gemini und rendert die Endfassung; bis dahin bleibt `04 Export` leer (V1-Export liegt in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-30 Layout-Umstellung`).
- Ablage: `05 Produktion\Dewlane\2026-11\2026-11-05 INCI-Liste\` (Skript, Storyboard, Untertitel und Cover aus V1 als Arbeitsstand), Vorschau mit Standbildern `05 Produktion\_Demos\dewlane-regie\index.html`.

## Erklärschicht (seit 30.10.2026 abends)

Umsetzung von `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md` über den gemeinsamen Renderer (`fn.render.explainer`), Block `explainer` in `brands\beauty\brand.yaml`:

- Oben rechts durchgehend „SYNTHETISCHE STIMME“; Einstiegszeile 0–3,5 s „Synthetische Stimme · Quellen am Bildschirm · Keine medizinische Beratung“.
- Kicker-Zeile „<n> · DAS PROBLEM“ usw. bei y 186 in der Faktfarbe; der Szenentitel bleibt die Überschrift der Szene. Kein Kopf im Hook und im Abschluss.
- Marker-Kapsel und Quellenleiste bei `source_y: 1112` (Szene endet bei 1100, zweizeilige Untertitel beginnen bei etwa 1250, Statusleiste 1440, Plattformtext ab 1600; rechter Rand bleibt links von x 930). Kurze `label` je Quelle, damit die Leiste höchstens zwei Zeilen hat.
- Farben mit fester Bedeutung, auf die helle Palette abgestimmt: Fakt #9B5560 (Akzent, dieselbe Farbe wie die Fakt-Quadrate in den Szenen), Unsicher #946420 (Honig), Lücke #8E2F45 (Beere, wie die Lücken-Kreise in den Szenen), Auslegung #7A5AC8, Beispielwert #8a93a6. Grün (#4F7A62) nur für einen erreichten Zustand.
- Wortanker: In allen Dewlane-Szenen dürfen Zeitfelder `"w:Wort"` sein (`brands\beauty\scenes.py` löst sie über die gesprochenen Wörter auf); die Erklärschicht nutzt `marker_at`, `head_at`, `dim_at` ebenso. Damit hängt jede Bildaktion an einem Wort und wandert bei einer Neuvertonung mit.
- Eigene Kennzeichen „Unsicher“ in Szenen abschalten, wenn der untere Marker „Fakt“ sagt (`risk_open: false`, `routes[].open: false`, `approval_marker: false`); offene Fragen bleiben über den Honig-Rahmen sichtbar.
- Übergänge: Kreis aus dem Objekt (Etikettzeile, Etikettkarte) in die nächste Szene, sonst Überblendung 0,7 s oder harter Schnitt. Vignette nur bei der Etikett-Nahaufnahme im Hook; im hellen Schema hellt sie den Rand auf statt abzudunkeln (Rückmeldung an die Hauptsitzung).
- Chip „Beispielwert“ nur, wenn eine Szene erfundene Werte oder eine erfundene INCI-Liste zeigt; das Etikett im Hook zeigt bewusst nur abstrakte Zeilen.
- `bg_routine_line.mp4` nur in Szenen ohne Kicker-Zeile (Hook), weil die Linie sonst durch den Kicker läuft.
- Storyboard je Video unter `01 Skript\Storyboard.md` (Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild).

## Roter Faden und Statusleiste

Ein durchgehendes Objekt je Video, meist die INCI-Liste oder das Etikett eines neutralen Produkts ohne Marke („INCI-Liste“, „Sonnenschutz-Etikett“, „Tiegel“). Die Statusleiste unten „liest mit“: je Beat ein Zustand. Honig = offen oder unsichtbar, gedämpft = geklärt, Beere = der eine Stopp am Schluss („Erst lesen, dann auftragen“).

## Untertitel

Sinngruppen von höchstens vier Wörtern (`caption_mode: phrases`), normale Schreibweise, Inter 600, 56 px, Tiefmauve mit Elfenbein-Halo statt dunklem Schatten, Hervorhebungswort in Rosé. Untertitel 540 px vom unteren Rand, Statusleiste bei y 1440, alles oberhalb der Plattform-Bedienelemente (Prüfung `platform_overlay`).

## Abschluss in der Handlung

`file_close`: die Liste mit Knopf „Auftragen“, der gedimmt wird, Beere-Leiste „Erst die Liste lesen“, darunter „Dewlane“ mindestens 4 s lesbar, „Wissen statt Versprechen.“ und „Keine medizinische Beratung.“. Gesprochen: „Beauty-Wissen klar erklärt: Folge Dewlane.“ Keine Domain und kein Handle im Bild, solange beides nicht gesichert ist.

## Grenzen als Prüfliste (vor jeder Vertonung abhaken)

- [ ] Nur Wissen: Inhaltsstoff, Kennzeichnung, Regel, Routine-Begriff. Kein „wirkt“, „hilft gegen“, „repariert“, „verjüngt“.
- [ ] Keine Produktempfehlung, kein Markenname als Empfehlung, keine Produktbilder mit Marke; Beispielprodukte neutral („deine Creme“).
- [ ] Keine Vorher-Nachher-Bilder, keine erfundenen Tests oder Umfragen, keine KI-Gesichter, keine künstliche Haut als Beweis.
- [ ] Keine medizinische Beratung: Gesundheitsbezug nur als „laut Quelle“, Abschlusszeile „Keine medizinische Beratung.“ im Bild und in der Beschreibung.
- [ ] Jede Tatsachenaussage hat eine Quelle mit URL und Abrufdatum (EU-Kosmetikverordnung und Änderungen, CosIng, Kommission, Fachgesellschaft, Übersichtsarbeit mit DOI); Unbelegtes steht in `unverified` und nicht im Video.
- [ ] Zahlen nur mit Bezugsgruppe (z. B. „bei getesteten Dermatitis-Patienten“), nie als Bevölkerungswert.
- [ ] Rechtsstand prüfen: Fristen und Grenzwerte aus dem Amtsblatt; konsolidierte Fassung gegenlesen (EUR-Lex lässt automatisierte Abrufe nicht zu).
- [ ] Hook-Engine: fünf Kandidaten, je einer pro Typ, Wahrheit mindestens 4.
- [ ] Szenen: mindestens drei Typen, kein gleiches Layout zweimal hintereinander, kein `ui_demo`, kein `negate`.
- [ ] „KI-generiert“ dauerhaft im Bild; Labels `is_aigc`, `is_ai_generated`, `containsSyntheticMedia` gesetzt.
- [ ] risk_level `high`: Ende in HUMAN_REVIEW, Stefan gibt frei. Claude setzt nie APPROVED.

## Werbeplätze (für später, ohne Inhalt)

Noch gibt es keine Partner und kein Media-Kit; laut `brands.yaml` keine bezahlten Inhalte vor einem Media-Kit. Wo gekennzeichnete Partnerinhalte später stehen könnten, ohne den Wissensteil zu berühren:

1. **Eigener Beat nach dem Nutzen, vor dem Abschluss** (etwa 5–8 s, Szenentyp `file_beside` oder eigener Sponsor-Typ): deutlich als „Werbung“ bzw. „Anzeige“ gekennzeichnet, mit eigenem Hintergrund, nie innerhalb von Hook, Erklärung oder Erkenntnis. Der Faktenteil entsteht unabhängig vom Partner; der Partner liest ihn nicht vorab mit Änderungsrecht.
2. **Beschreibung und angepinnter Kommentar:** Hinweis „Werbung“ am Anfang, Link des Partners, Plattform-Schalter für bezahlte Partnerschaft setzen (TikTok `brand_content_toggle`, YouTube `hasPaidProductPlacement`, Instagram Label für bezahlte Partnerschaft). Kennzeichnung nach § 6 ECG (Hinweis WKO NÖ, siehe Übergabebericht 6.4).
3. **Ganze Partnerfolge** als eigenes Format im Kalender (Status und Kennzeichnung getrennt geführt), Thema weiterhin Wissen (z. B. „Wie man ein Etikett liest“ am Beispiel eines Partnerprodukts nur, wenn alle Aussagen belegt sind).
4. **Nie:** Partnerprodukt im Hook, Wirkversprechen des Partners, Vergleich mit Wettbewerbern, Rabattcodes ohne Kennzeichnung, Partnerlogo im Dewlane-Logo-Bereich.

Offen und von Stefan zu entscheiden: Gewerbe für Werbeeinnahmen, Media-Kit, Preisliste, ob Partnerfolgen in beiden Sprachen laufen.

## Parameter (Layout im Plan)

```json
"layout": {"zone_top": 290, "zone_h": 810, "caption_bottom_px": 540, "caption_width_px": 800, "caption_transform": "none",
           "status_y": 1440, "outro": false, "tail_seconds": 2.6, "progress_y": 1548, "ai_label_bottom_px": 318,
           "caption_mode": "phrases", "caption_max_words": 4, "status_bar": {"file": "INCI-Liste", "states": [...]}},
"assets": {"folder": "assets/clips",
           "background": {"cinematic_hook": "bg_routine_line.mp4", "data_flow": "bg_petal_bands.mp4", "file_beside": "bg_cream_swirl.mp4",
           "file_fork": "bg_drop_ripple.mp4", "comparison": "bg_flacon.mp4", "key_takeaway": "bg_petal_bands.mp4", "file_close": "bg_flacon.mp4"},
           "hero": {}, "scrim": 0.3}
```

Länge: 160–175 Wörter ergeben etwa 75–85 s. Stimme Gemini Flash TTS, Stimme „Leda“ (DE), Anrede „du“.

## Ablauf je Video

1. Thema aus `data\calendars\beauty_2026-11.json`, Quellen frisch prüfen, Plan `data\direction\<video_id>.json` schreiben (Vorlage: Beispielplan).
2. Trockenlauf: `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --assets --no-render`
3. Sperrdatei `data\render.lock` prüfen und anlegen, freien Speicher prüfen (`fn.cli status`, Grenze 30 GB).
4. Vertonung und Vollfassung: `... --version V1 --tts gemini --assets --mirror dewlane-regie/<datum>`; Korrekturen ohne neue Kosten mit `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`. Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme (Stefan, 30.10.2026). Layout vorher nur per Trockenlauf prüfen: `--version <V>dry --tts mock --assets --no-render`, Standbilder mit `npx hyperframes snapshot` im Projektordner des Trockenlaufs.
5. Sperrdatei entfernen. Produktionsordner füllen (`scripts\export_production_folder.py ... --short "<Kurztitel>"`); `Skript.md` und `Veröffentlichung.md` danach auf Dewlane-Texte prüfen (das Skript schreibt Scutoria-Sätze hinein).
6. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`; nichts veröffentlichen.

## Offene Punkte für Version 1.0

- Stefans Abnahme von Optik, Palette, Stimme und Abschlusszeile.
- Zweites Thema als Wiederholungstest (Empfehlung aus dem Codex-Entwurf), z. B. Tiegel-Symbol am 13.11.
- Renderer-Wünsche: Dateikarte ohne „Unsicher“-Chip, Schatten und Stempel für helles Schema.
- Musik: keine lizenzierte Quelle gewählt.
- Handle `@dewlane.beauty` ist von Privatkonten belegt (Markenregister); Konten legt Stefan an.

## Qualitätsrunde Q1 (31.10.2026)

Anlass: Stefan bewertete am 30.10.2026 Scutoria mit 1,7 und Dewlane mit 3 (Briefing `02 Marke\Qualitätsrunde 2026-10-31.md`). Umgesetzt im Testvideo „INCI-Liste“, Fassung Q1, ohne neue Vertonung (Gemini-Aufnahme aus V2 wiederverwendet, Sprechtext unverändert). Diese Angaben gelten vor den älteren Abschnitten oben.

**Hintergrund mit Tiefe, nur Code** (`LAYER` in `brands\beauty\scenes.py`, über `#bg`, unter den Szenen): feste Lichtlogik Fensterlicht von oben links; Grundverlauf Elfenbein zu warmem Sand; Lichtbahnen, die langsam durch das Bild wandern; Cremeschliere unten; unscharfer Glasflakon rechts und Tiegel links unten (ohne Marke, außerhalb der Inhaltszone); Tautropfen in drei Ebenen mit unterschiedlicher Unschärfe; Papierkorn (SVG-Rauschen); warmer Randschatten, oben frei, damit „SYNTHETISCHE STIMME“ und „KI-generiert“ den Kontrast halten. Bewegung nur über die GSAP-Zeitleiste (beim Rendern exakt wiederholbar): langsames Driften über das ganze Video plus eine Kamerafahrt je Szenenwechsel, nahe Ebenen stärker als ferne. Keine Clips mehr im Plan (`assets.background: {}`), kein Higgsfield, keine KI-Bilder.

**Leitobjekt Etikett**: In jeder Szene ist das Etikett „Ingredients“ das Hauptmotiv (740 bis 800 px der 864 px Inhaltsbreite) und ändert seinen Zustand mit der Geschichte. Die Zeilen bleiben abstrakte Balken; setzt eine Szene einen Namen auf eine Zeile (AQUA, PARFUM), ist die Position ein Beispiel und der Plan setzt `overlay.example: true` (Chip „Beispielwert“).

**Szenen (Q1)**, alle in `brands\beauty\scenes.py`, die gemeinsamen Szenen werden für Dewlane nicht mehr benutzt (sie sind für dunkle Marken gebaut):

| Szenentyp | Dewlane-Szene | Daten (Zeiten als `w:Wort`) |
|---|---|---|
| `cinematic_hook` | Tropfen landet auf Zeile 1, Welle, Ring, große Frage, Chip | `question`, `badge`, `fly_at`, `ring_at`, `question_at`, `badge_at`, `lines` |
| `data_flow` | Etikett plus EU-Glossar; ein Name fliegt vom Glossar auf das Etikett, Bedeutungs-Chip | `headline`, `label_at`, `head_at`, `gloss_at`, `word`, `word_line`, `word_at`, `meaning`, `meaning_at`, `gloss_title`, `gloss_sub`, `gloss_note` |
| `file_beside` | Etikettzeilen werden zum absteigenden Gewichtsdiagramm, Tropfen fallen in eine Schale | `headline`, `weights_at`, `drops_at`, `tag`, `tag_at`, `front_at`, `front_tag`, `front_tag_at` |
| `file_fork` | gestrichelte 1-%-Linie, Zeilen darunter tauschen die Plätze, Linie verblasst | `headline`, `end_at`, `line_at`, `shuffle_at`, `fade_at`, `chip`, `chip_at`, `upper`, `lower` |
| `comparison` | Etikett mit leeren Prozentfeldern, Karten „Sie zeigt“ und „Sie zeigt nicht“ | `headline`, `read_at`, `front_at`, `pct_at`, `left`/`right` mit `rows[{text, at}]` |
| `key_takeaway` | drei nummerierte Hinweise am Etikett, Lupe, Suchfeld CosIng | `headline`, `items[{title, sub, at}]`, `word`, `cosing_title`, `cosing_sub`, `cosing_at`, `db_at` |
| `file_close` | Lesestreifen, Sperre „Erst die Liste lesen“ wird grün „Liste gelesen“, Knopf aktiv, dann Markenzeichen | `headline`, `read_at`, `done_at`, `unlock_at`, `brand_at`, `button`, `block_text`, `done_text`, `domain`, `claim`, `disclaimer` |

Passt ein neues Thema nicht auf diese Bildhandlungen, eine weitere Dewlane-Szene in `scenes.py` ergänzen.

**Gestaltung**: Szenentitel mittig in Playfair Display 68 px, höchstens zwei Zeilen; Beschriftungen Inter mindestens 26 px; Karten Radius 18 px mit mauvefarbenen Schatten; Chips als Kapseln; Linien-Icons (Buch, Lupe, Tropfen, Waage) in Rosé. Vier bis sieben Bildereignisse je Szene, jedes an einem gesprochenen Wort. Die Statusleiste springt auf dem Wort um, das den Zustand ausspricht (`offset` je Zustand im Plan). Kreisübergänge öffnen sich aus einem Objekt der vorigen Szene (Glanzfleck des Tropfens, Zeile 1, Etikettmitte), sonst Überblendung 0,7 s. Vignette im Hook mit `explainer.vignette_color: rgba(74,47,52,0.10)`; kräftiger drückt den Kontrast von „SYNTHETISCHE STIMME“ unter WCAG AA (HyperFrames-Kontrastprüfung).

**Prüfung**: HyperFrames-Prüfung ohne Fehler und ohne Kontrastbefund, Überschneidungs-Prüfung (`node scripts\overlap_check.mjs`) ohne Befund, Kontaktbogen gegen Scutoria verglichen.

### Testvideo Q1 (Ergebnis, 30.10.2026 23:46)

- Fassung Q1, 67,1 s, 162 Wörter, Gemini-Stimme Leda aus V2 (`voice_beauty-20261105-1-de_V2_gemini.wav`), keine neuen Kosten.
- Prüfbericht HUMAN_REVIEW: alle Prüfungen bestanden bis auf `risk_high_review` (gewollt, Stefan gibt frei). 41 Bildereignisse, mittlerer Abstand 1,3 s, −16,0 LUFS. HyperFrames-Prüfung ohne Fehler und ohne Kontrastbefund.
- Überschneidungs-Prüfung: ohne Befund.
- Eigene Note: 2,0. Stärker als V2 (3): Hintergrund mit Tiefe statt flacher Fläche, Etikett als großes Leitobjekt in jeder Szene, vier bis sieben Ereignisse je Szene an Wörtern. Was zu 1,7 fehlt: Der helle Grund bleibt naturgemäß ruhiger als Scutorias Filmlicht, und die Szenen 5 und 7 sind eher ruhige Karten-Szenen.
- Export `05 Produktion\Dewlane\2026-11\2026-11-05 INCI-Liste\04 Export\2026-11-05 INCI-Liste – 9x16.mp4`, Kontaktbogen `03 Schnittprojekt\Kontaktbogen Q1.jpg`, Vorschau `05 Produktion\_Demos\dewlane-regie\2026-11-05-q1\`. Alter V2-Export in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde`.
