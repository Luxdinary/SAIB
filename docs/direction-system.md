# Regie-System (direction) – Hook-Engine, Story-Engine, fünf Szenentypen

Stand 30.10.2026, Abschnitt 1 (Scutoria). Antwort auf die Reel-Analyse vom 30.10.2026 („animierte Präsentation, kein Reel"). Markenübergreifend angelegt, zuerst für `ai_security` konkret.

## 1. Bestandsaufnahme des Phase-1-Renderers

| Datei | Befund | Konsequenz |
|---|---|---|
| `src/fn/render/compose.py` | Eine Vorlage für alle Szenen: Headline + Platzhalter-SVG je Marken-Motiv + Body + Quellenzeile, zentriert in der Zone y 300–1150. Bewegung = Einblenden + 14 px Drift. Keine Szenentypen, keine Kamerabewegung, keine Objektanimation. | **bleibt für Phase 1 unverändert**; neue Templates in `templates.py`, neuer Composer `director.py` (importiert Hilfsfunktionen aus compose). |
| `src/fn/pipeline.py` (`plan_scenes`, `produce`) | Szenen = Skriptabschnitte 1:1, Startzeit aus Wortzeiten; keine Dramaturgie, keine Hook-Auswahl. | **nicht angefasst** (Gemini-Durchlauf läuft). Später: Feature-Flag `--direction <plan.json>` in `produce`, das `director.build_direction_project` statt `compose.build_project` ruft. |
| `src/fn/scripting.py` | `> visual:` kennt nur headline/body/number/code/kind. | Bleibt; der Szenenplan liegt als eigene Datei `data/direction/<video_id>.json` (datengetriebene Szenenbeschreibung) neben dem Skript. |
| `src/fn/compliance.py` | Technische und Inhaltsprüfungen; nichts zu Szenenvielfalt, Bildwechsel, Lesbarkeit. | **nicht angefasst**; neue Prüfungen in `src/fn/direction/checks.py`, die in denselben `Report` schreiben. |
| `brands/<id>/visual_style.md`, `design-system.md` | Layoutzonen passen (Logo, Safe-Zones, AI-Label), aber Fokus liegt oben (Zone 300–1150) und Untertitel bei y 1280. | Director nutzt Zone 320–1200 und Untertitel 560 px vom unteren Rand (y 1360); Logo nur 40 px. |

Neu angelegt (keine bestehende Datei verändert): `src/fn/direction/{__init__,hooks,story,checks}.py`, `src/fn/render/{templates,director}.py`, `data/direction/*.json`, `scripts/render_prototype.py`, `tests/test_direction.py`, diese Datei.

## 2. Hook-Engine (`fn.direction.hooks`)

- Je Video **mindestens fünf Kandidaten**, einer je Typ: `question` (vertretbare Frage), `misconception` (Denkfehler), `surprising_fact` (belegbarer Sachverhalt), `concrete_risk` (Risiko aus dem Alltag), `demonstration` (sichtbare Demonstration). `validate_set()` erzwingt die Abdeckung.
- **Bewertung** 1–5 je Kriterium mit Gewicht: Klarheit 1,0 · Relevanz 1,2 · Neugier 1,2 · Wahrheitsgehalt 1,5 · visuelle Umsetzbarkeit 1,0 → Score 0–100.
- **Wahrheits-Schranke**: `truth < 4` macht den Kandidaten unwählbar, egal wie dramatisch. Fakten-, Denkfehler- und Risiko-Hooks brauchen eine Quelle. Gesprochen ≤ 90 Zeichen, auf dem Bildschirm ≤ 64 Zeichen.
- `rank()` sortiert, `winner()` liefert den stärksten **vertretbaren** Hook. Die Scores vergibt der Skript-Schreiber (Claude) mit Begründung je Kriterium im Plan (`why`); die Engine prüft und sortiert nur.

## 3. Story-Engine (`fn.direction.story`)

Reihenfolge **Hook → Problem → Erklärung → Demonstration → Erkenntnis → Nutzen → Abschluss**. Jeder Beat hat `function`, `scene_type`, `spoken`, `data` (für das Template), `source_ids`. Regeln in `validate()`:

- erster Beat `hook` mit `cinematic_hook`, letzter Beat `close`; Funktionen in Story-Reihenfolge (eine Funktion darf mehrfach vorkommen, z. B. zwei Erkenntnisse), keine Rücksprünge;
- `problem`, `explanation`, `demonstration`, `insight` brauchen Quellen-IDs; jede Quelle hat `id`, `url`, `checked_at`; ein `UNVERIFIED` im Plan blockiert das Rendern;
- **mindestens zwei Darstellungsformen** (Szenentypen) je Video, Ziel drei oder mehr (`advice()`).

`assign_timing()` im Director setzt Start/Dauer aus den Wortzeiten (Schnitt dort, wo der nächste Satz beginnt, 0,15 s vorgezogen). Wiederholungen werden beim Schreiben gestrichen; ein Beat ohne inneres Bildereignis über 16 s wird gemeldet.

## 4. Fünf Szenentypen (`fn.render.templates`)

Gleiche Identität (Palette, Schriften, Hex-Raster, kleines Logo), fünf unterscheidbare Layouts. Alle Bewegungen laufen auf Kindern des `.clip` (HyperFrames-Regel), die Kamera auf `.stage`.

| Typ | Was passiert | Daten (`data`) |
|---|---|---|
| `cinematic_hook` | Chatfenster, Dokumentkarte fliegt von links unten in das Eingabefeld, Text tippt sich, Nachricht erscheint; große Frage (84 px) und gelbe Warnmarke beim Fragezeichen; langsamer Kamera-Push 1,07×, Glow pulsiert. | `question`, `doc_label`, `chat_title`, `typed`, `bot_line`, `badge`, `fly_at`, `question_at` |
| `data_flow` | 2–4 Knoten vertikal, Verbinder zeichnen sich, Datenpaket wandert, Hervorhebung (Chip + Glow) an einem Knoten zum passenden Wort. | `headline`, `nodes[]`, `edges[]`, `packet_at`, `highlight{node,at,label}` |
| `ui_demo` | Browserfenster mit echter Aufnahme (`image`) oder schematischer Einstellungsliste; Cursor fährt zum Schalter, Zoom 1,5× auf den Schalter, Ring, Schalter kippt. Ohne echte Aufnahme steht „Schematische Darstellung" im Bild und der Prüfbericht setzt `schematic_ui` (HUMAN_REVIEW). | `headline`, `url`, `title`, `rows[]`, `focus_row`, `cursor_at`, `zoom_at`, `flip_at`, `zoom`, `image` |
| `comparison` | `versus`: zwei gestapelte Karten (9:16-tauglich) mit ✓/✗-Zeilen, zeitversetzt; `negate`: Aussage-Karte, großer Stempel „NEIN" schlägt ein, Unterzeile. | `headline`, `mode`, `left/right{title,rows[{text,ok}]}`, `left_at`, `right_at`, `negate{statement,stamp,stamp_at,subline,subline_at}` |
| `key_takeaway` | Drei nummerierte Check-Karten erscheinen nacheinander, oder eine große Aussage; `mode: closing` = Abschlusskarte mit gezeichnetem Schild-Motiv, Aussage und CTA-Chip (anderes Layout als die Liste). | `headline`, `items[{title,sub,at}]`, `statement`, `mode`, `chip` |

**Füllung der Bildfläche** (Befund „untere Hälfte leer"): Inhaltszone y 290–1200, Bühne (`.stage`) zentriert ihren Inhalt vertikal (UI-Fenster, Karten, Abschluss), Karten und Knoten sind größer (Zeilen 40–44 px), Untertitel 500 px vom unteren Rand (y 1420, innerhalb der sicheren Zone). Hintergrund bewegt sich immer: Raster-Parallaxe (`#bg` driftet 80 px über die Videolänge) und ein weicher Lichtverlauf (`#light`) wandert diagonal; damit ist kein Frame statisch.

### Asset-Schicht (Fassung B, `fn.render.assets`)

Der Plan deklariert `assets.background` (Clip je Szenentyp), `assets.hero` (Clip je Beat, im Hook hinter dem Chatfenster) und `assets.transition`; Dateinamen aus dem Prompt-Blatt, Ablage `brands/<id>/assets/higgsfield/` mit `LICENSE.md` (`<datei>: <Lizenztext>` je Zeile). `render_direction.py --assets` legt je Beat ein stummes `<video class="clip">` auf Spur 0 unter die Szene (`object-fit: cover`), darüber einen dunklen Verlauf (`#scrim`, Stärke `assets.scrim`). Fehlt eine Datei, zeichnet der Director einen **Platzhalter** (CSS-Verlauf je Szenentyp, ohne Text) und der Bericht setzt `asset_placeholders` (review); fehlt die Lizenzzeile, bleibt `license_manifest` rot. Logo, Text, Untertitel, Diagramme bleiben Renderer-Grafik.

**Lesbarkeit**: Headline 62 px, Frage 84 px, Zeilen 36–42 px, Labels 30 px; Textlängen je Feld begrenzt (`LIMITS`, z. B. Frage ≤ 64, Vergleichszeile ≤ 44 Zeichen) – Überschreitung ist ein `fail` im Prüfbericht. **Fokus in der Bildmitte**: Zone y 320–1200, ein dominantes Motiv je Szene. **Logo klein und konstant**: 40 px oben links. **Untertitel** 560 px vom unteren Rand, Montserrat 700, Highlight-Wort.

## 5. Neue Prüfungen im Prüfbericht (`fn.direction.checks.check_direction`)

| id | Schwere | Regel |
|---|---|---|
| `scene_variety` | fail | < 2 Szenentypen |
| `scene_variety_target` | warn | < 3 Szenentypen |
| `identical_consecutive_scenes` | warn | gleiches Layout zweimal hintereinander |
| `visual_cuts_static` | fail | längste Strecke ohne Bildereignis > 14 s |
| `visual_cuts_rhythm` | warn | Median der Bildwechsel außerhalb 1,2–8 s |
| `readability_text_limits` | fail | Text länger als das Template-Limit |
| `readability_captions` | fail | Untertitel < 42 px |
| `schematic_ui` | review | UI-Demo ohne echte Bildschirmaufnahme |
| `asset_placeholders` | review | Fassung B: deklarierter Clip fehlt, Platzhalter gezeichnet |
| `audio_level_lufs` | warn | integrierte Lautheit außerhalb −16 ± 2 LUFS |
| `audio_level_peak` | fail | Spitzenpegel > −0,5 dB |

## 6. Ablauf je Video (Abschnitt für Abschnitt, mit Freigabe)

1. Skript-Schreiber liefert Plan-JSON: Quellen (geprüft, mit Datum), ≥ 5 Hook-Kandidaten mit Scores, Beats mit Template-Daten, Liste `unverified` (nicht verwendete Aussagen).
2. `story.validate()` + `hooks.validate_set()` müssen leer sein.
3. Prototyp (Hook + erste Szene, 15 s) → Stefan gibt Optik frei.
4. TTS für den neuen Text (Gemini Flash, ca. 0,02 USD je Video) **nur nach Freigabe**, dann Wortzeiten, `assign_timing`, voller Render, Prüfbericht inkl. Regie-Checks, HUMAN_REVIEW bei `schematic_ui`.
5. Echte Bildschirmaufnahmen kommen von Stefan (Demo-Konto) nach `brands/<id>/assets/ui/`; Claude meldet sich in kein Konto an.

## 6a. Produktion aus dem Plan

`.venv\Scripts\python.exe scripts\render_direction.py data\direction\<video_id>.json --version A --tts gemini` (eine Vertonung, geloggt in `data/costs`), danach Korrekturen ohne neue Kosten mit `--reuse-voice <wav>`; `--no-render` ist der Trockenlauf (Lint, Layout, Textlimits, Regie-Checks ohne Video). `--assets` schaltet die Asset-Schicht ein (Fassung B). Ergebnis in `storage/direction/<video_id>-<version>/` und Spiegel `_Demos\scutoria-regie\<mirror>\` (video.mp4, cover.jpg, report.json, manifest.json, plan.timed.json, Standbilder 5/30/60 s); die Seite `scutoria-regie\index.html` bekommt je Fassung einen Abschnitt.

## 6b. Fassung A2/A3: Datei als roter Faden (zweite Kritik, 30.10.2026)

Drei weitere Szenentypen in `src/fn/render/templates_file.py`: `file_fork` (Datei über zwei Zugängen plus Freigabe-Karte), `file_beside` (Datei neben Vertrags-/Zugangskarte), `file_close` (Datei mit blockiertem Upload, Domain mindestens 4 s lesbar, Claim und Pflichtzeile; kein Logo-Intro, keine Endkarte). `cinematic_hook` hat den Modus `approach` (Datei stoppt vor dem Upload, kein Tippen, keine Nachricht). `key_takeaway` kennt `marker: "?"` (offene Fragen, keine Haken). Plan-Layout: `status_bar` (Datei plus Zustand je Beat, Amber = offen, Rot = Sperre), `caption_transform: none`, `caption_width_px: 800`, `outro: false`, `tail_seconds`, `progress_y`/`ai_label_bottom_px`/`status_y` oberhalb y 1620 (Plattform-Beschriftung). Checks: `visual_cuts_static` mit `--max-static 13`, `no_check_icons_open_questions` (Beats mit `risk_open`), `logo_intro_seconds` (0), `platform_overlay` (Untertitel x ≤ 940, Zone y ≤ 1100, Leisten y < 1620); `overlay_*.jpg` zeigt simulierte Plattform-Bedienelemente über den Standbildern. Quellen und der Satz „Mehr Informationen: https://scutoria.com …" stehen in `post.json`, nicht im Bild.

## 6c. Markentokens Scutoria (A3)

`brands/ai_security/brand.yaml` trägt die Tokens aus `C:\Users\Stefa\OneDrive\scutoria\design\project\tokens.json` (Kopie `brands/ai_security/tokens.json`): `flat: true` schaltet im Director und in den Templates Glow, Lichtverlauf, Pulsieren und farbige Kartenränder ab (Haarlinien, `shadow-card`/`shadow-paper`, Radius 20, Kamera höchstens 2 %). Schriften aus `brand.yaml fonts.*.file` (Manrope woff2, IBM Plex Mono ttf, Lizenzdateien werden ins Projekt kopiert), Scutum-Marke als `<img>` plus Wortzeichen SCUTORIA als Text. Marker als Formen: Fakt (gefülltes Quadrat, accent), Unsicher (halber Kreis, amber, als Chip mit Wort), Lücke (gestrichelter Kreis, rot), Geregelt (grünes Quadrat, nur bei Erfolg). Die acht anderen Marken behalten ihr bisheriges Aussehen (Fallbacks). Abweichung vom Markenbuch: Untertitel 56 px und Headlines 62–84 px statt des Web-Maßstabs (Lesbarkeit am Handy), siehe `subtitle_style.json` `note`.

## 6d. Markeneigene Szenentypen (seit 30.10.2026)

Jede Marke kann eigene Szenentypen in `brands/<id>/scenes.py` anlegen, ohne den gemeinsamen Code zu ändern (`fn.render.brand_scenes`):

- Modulort: `brands/<id>/scenes.py` oder der Pfad in `scenes:` in `brands/<id>/brand.yaml` (relativ zum Repository).
- `TEMPLATES = {"<typ>": funktion(ctx, data) -> SceneOut}`: neue Typen oder markeneigene Varianten gemeinsamer Typen (z. B. ein eigenes `cinematic_hook`); eine Variante gilt nur für diese Marke, der gemeinsame Typ bleibt für alle anderen unverändert.
- `LIMITS = {"<typ>": {"feld": max_zeichen}}`: Textgrenzen der neuen Typen (Lesbarkeitsprüfung).
- `HOOK_SCENE_TYPES = [...]` oder `hook_scene_types` in `brands/<id>/brand.yaml`: erlaubte Szenentypen für den Hook-Beat (Standard `cinematic_hook`).
- `CSS(...)` oder `scene_css(...)` mit den ersten N Argumenten aus (pal, display, display_w, body, mono, zone_top, zone_h, flat): CSS der Markentypen, wird nach dem gemeinsamen CSS angehängt.
- Clips eigener Herkunft: `"assets": {"folder": "assets/clips", ...}` im Plan (relativ zu `brands/<id>/`, Standard `assets/higgsfield`); die Lizenzzeile steht in `LICENSE.md` im selben Ordner.
- Helle Paletten (z. B. Dewlane) in `palette`: `scheme: light` (Stempel ohne `mix-blend-mode:screen`), `shadow: "r,g,b"` (färbt alle Schatten statt Schwarz), `toggle_off` (Farbe des ausgeschalteten Schalters). Dunkle Marken ohne diese Schlüssel rendern unverändert.
- `LAYER(plan, brand, project_dir, captions) -> dict` im Markenmodul: markenweite Ebene über das ganze Video (z. B. eine WebGL-Leinwand unter allen Szenen). Rückgabe optional `head_html` (vor `</head>`), `under_scenes_html` (direkt nach `#bg`), `body_end_html` (vor `</body>`), `events` (absolute Zeiten, zählen für die Bildwechsel-Prüfung), `problems` (gehen in den Prüfbericht). Eigene Dateien kopiert LAYER selbst nach `project_dir/assets`.
- `MANIFEST_EXTRA(plan) -> dict` im Markenmodul: zusätzliche Manifestfelder (z. B. Rechenwege); Felder der Pipeline werden nie überschrieben.
- Soundeffekte: `"assets": {"sfx": [{"at": 4.2, "file": "pop.wav", "volume": 0.4}], "sfx_folder": "assets/sfx"}` im Plan (Dateien relativ zu `brands/<id>/`, Lizenzzeile in `LICENSE.md` daneben); funktioniert auch ohne `--assets`, liegt auf Tonspur 8 bis 11 unter der Stimme und erscheint mit Lizenz im Manifest.
- Signalfarben haben echte Rückfallwerte (#ffd166, #0a0c10, #ff6b6b); Marken ohne `signal_*` brechen nicht mehr mit `css_parse_error` ab.
- Dateikarte (`file_fork`, `file_beside`, `file_close`): Datenfeld `file_marker` = `open` (Standard, Chip „Unsicher"), `fact` (Quadrat „Fakt") oder `none` (kein Chip).
- `scripts/render_direction.py` schreibt `risk_level` ins Manifest: das Höhere aus `risk_default` der Marke und `plan.layout.risk_level`; Marken mit `high` landen immer in HUMAN_REVIEW.
- `SceneCtx.words`: die gesprochenen Wörter im Beat mit absoluten Zeiten (`.text`, `.start`, `.end`), damit Bildereignisse wortgenau sitzen.

Typen gelten nur für ihre Marke (`story.validate` und der Director schlagen je `plan.brand_id` nach). `scripts/export_production_folder.py` nimmt Abschlusssatz und Domain aus `brands/<id>/brand.yaml` (`production.closing_sentence.<sprache>`, `production.domain`) und die Vorlage aus `config/brands.yaml` (`brand_version`, `template_doc`); für Scutoria gilt ohne Eintrag der bisherige Satz.

## 7. Noch offen

- `produce --direction` (Feature-Flag) erst nach Ende des laufenden Gemini-Durchlaufs einbauen.
- Musik/Übergangsgeräusche (Analyse: Sound 7/10): Lizenzquelle fehlt noch, `music.file` in `audio_style.yaml` bleibt leer.
- KI-Hintergrundbilder/Clips (Mediengenerierung) sind Phase 2+; die Templates sind programmatische Grafik.

## 6e. Erklärschicht (Schnitt- und Layout-Vorlage, 30.10.2026)

Stefans Vorlage für die Scutoria-Langvideos, auf 9:16 übertragen: `src/fn/render/explainer.py` (Doku im Modulkopf),
eingeschaltet über `explainer.enabled` in `brands/<id>/brand.yaml` oder `layout.explainer` im Plan. Bausteine:
Kicker-Zeile je Szene (y 186, der Szenentitel ist der Kopftitel), "SYNTHETISCHE STIMME" oben rechts, Einstiegszeile,
Marker-Kapsel (Fakt/Auslegung/Unsicher/Lücke, Form + Wort) mit Quellenleiste aus `sources[].label` und `checked_at`
(Standard y 1396, `source_y`), Kreisübergang (`iris`) oder Überblendung (`blende`) in eine Szene, Vignette.
Szenen liegen bei eingeschalteter Schicht abwechselnd auf Spur 1 und 5, damit ein Übergang zwei Szenen überlappt.
Felder je Szene in `beats[].overlay`. Regeln für Stefan: OneDrive `Business\02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`.
Tests: `tests/test_explainer.py`.

## 6f. Nur Google-Stimmen (Stefan, 30.10.2026)

Keine Windows-Stimme (SAPI) und keine Edge-Stimme, auch nicht als Entwurf. `fn.tts.get_provider` wirft für
`sapi` und `edge` einen Fehler, `render_direction.py` verweigert `--reuse-voice` mit einer SAPI-Aufnahme (Exit 8),
`export_production_folder.py` exportiert nur Renders mit `tts.provider == "gemini"` (Exit 4). Bei Gemini 429:
warten, „Vertonung offen" vermerken. Prüfen ohne Stimme mit `--tts mock --no-render`.

## 6g. Überschneidungs-Prüfung (Pflicht vor jedem Export, ab 31.10.2026)

`node scripts/overlap_check.mjs storage/direction/<id>-<version>/project` lädt das gerenderte Projekt in Chrome, spult
die Zeitleiste in 0,25-s-Schritten ab und meldet sichtbare Texte verschiedener Ebenen (Erklärschicht, Szene, Untertitel,
Statusleiste, Abspann), die sich überdecken. Exit 1 bei Befund. Überblendungen zweier Szenen zählen nicht. Grund:
Die HyperFrames-Layoutprüfung hat Überdeckungen von Marker und Szene nicht erkannt (Scutoria V2, 30.10.2026).
puppeteer-core kommt aus dem npx-Cache von HyperFrames (oder `FN_PUPPETEER`), Chrome aus dem Standardpfad (`FN_CHROME`).

Seit 02.11.2026 (Wunsch Dewlane): Auch Marken-Ebenen mit eigener id (z. B. `#nhx-stamp`) zählen als Ebene. Überdeckungen
zweier Texte innerhalb einer Ebene stehen als `warnings` in der Ausgabe (Exit-Code unverändert); gezählt wird nur echte
Deckung der Schrifthöhe über mindestens zwei Prüfschritte. Die Fenstergröße folgt `data-width`/`data-height` von `#root`,
also auch 16:9 für Langvideos. Der Export schreibt den Schlusssatz der Marke nur noch einmal je Beschreibung (auch nicht,
wenn `companion_text` fast gleich lautet), und die KI-Zeile kommt aus `brand.yaml` › `production.ai_note.<lang>`.

## 6g2. Änderungen nach der Prüfrunde (02.11.2026, `OneDrive\Business\02 Marke\Prüfrunde 2026-11-03.md`, R1–R7)

- R1 KI-Zeile: `#ailabel` sitzt mindestens 430 px über dem unteren Rand (`AI_LABEL_MIN_BOTTOM` in `director.py`),
  also über der Beschreibung von TikTok und Reels; kräftiger (Textfarbe, 85 % Deckkraft). Kleinere Werte im Plan werden angehoben.
- R2 Cover: `scripts/make_cover.mjs` rendert das Cover aus dem Projekt ohne Untertitel, Balken und KI-Zeile, mit dem
  Hook-Text groß bei 58 % der Höhe (innerhalb der 1:1- und 3:4-Rasteransicht), Zeitpunkt Ende des ersten Beats.
  Schlägt das fehl, bleibt das Videobild wie bisher.
- R3 Export: Quellen in öffentlichen Texten mit kurzem `label`, „retrieved“ auf Englisch, `file:`-Quellen als „eigene
  Aufzeichnung“; Warnung bei Instagram über 2.200 Zeichen; `Skript.md` nennt bei `layout.format` die Format-Bibel.
- R4 `overlap_check.mjs`: Text wird mit dem Clip-Rechteck der Vorfahren (`overflow` ≠ visible) geschnitten; neue Liste
  `small_text` für sichtbare Texte unter 24 px (SVG-Skalierung berücksichtigt, Untertitel ausgenommen).
- R6 Ton: nach `loudnorm` ein Limiter bei −1,6 dBFS auf 192 kHz gegen Spitzen zwischen den Abtastwerten.
- R5 (leerer Streifen y 1000–1300): Die Szenenzone darf bis knapp über die Untertitel reichen (höchstens y 1250,
  mindestens 120 px über `caption_bottom_px`), wenn der Plan `zone_lower_right_px` ≤ 940 setzt. Dann muss die Szene
  unterhalb von y 1100 links von x 940 bleiben (Symbolspalte der Apps). Ohne diesen Wert bleibt die Grenze y 1100.
- R7 (Mindestgröße) setzen die Marken in ihren Szenen um.

## 6h. Faire Render-Warteschlange (ab 01.11.2026)

Jeder Render läuft über `scripts/render_queue.py <brand_id> -- <script.py> <args>`: Ticket in `data/render_queue/`,
wer zuerst ansteht, rendert zuerst; die Sperre `data/render.lock` nimmt nur noch der Wrapper (Herzschlag alle 30 s,
verwaist nach 20 min). Grund: Beim direkten Abfragen der Sperre bekam Gigastruct 80 Minuten lang nie die Sperre.
Ein Platz (RAM 32 GB, unter Last nur wenige GB frei); zwei Plätze erst nach Messung.

## 6i. Tonebene (ab 03.11.2026; die Nummer 6h war schon an die Warteschlange vergeben)

Stefans Urteil vom 02.11.2026: kein Ton außer der Stimme. Seit 03.11.2026 legt der gemeinsame Renderer unter jedes
Video Geräusche an Übergängen und Einblendungen und ein leises Musikbett, das beim Sprechen abgesenkt wird.
Module: `src/fn/render/sound.py` (Konfiguration, Cues, Mischung), `src/fn/render/sound_synth.py` (Geräusche und
Musikbett, reines numpy), `assets/sfx/` (12 Geräusche plus `LICENSE.md`), `assets/music/README.md` (Haken für
Lizenzmusik). Die Tonebene ist in `scripts/render_direction.py` immer an; `--no-sound` rendert wie vorher nur die Stimme,
`--sound palette=tech,mood=dark` probiert eine Einstellung ohne Änderung an `brand.yaml`.

**Ablauf im Render.** Der Director liefert die Beats mit Zeiten, die Bildereignisse der Templates (`build.events`)
und optional benannte Ereignisse (`SceneOut.named_events`). `sound.cues_from_plan()` leitet daraus die Cues ab und
nimmt die Cues aus dem Plan dazu; `sound.mix_sound()` mischt Stimme, Geräusche und Bett zu
`storage/direction/<id>/sound/mix.wav` (48 kHz, stereo, 24 bit; daneben die Stems `voice_stem.wav`, `sfx_stem.wav`,
`music_stem.wav` zum Nachmessen). `ffmpeg.encode_nvenc(raw, video, audio=mix.wav)` legt die Mischung unter das Bild;
die bisherige Kette `loudnorm I=-16, aresample=48000, alimiter=limit=0.79` bleibt unverändert am Ende, die Prüfung
`audio_level_peak` (höchstens -0,5 dB) gilt weiter. Der Trockenlauf (`--no-render`, auch mit `--tts mock`) schreibt
`sound.json` mit allen Cues und Problemen, ohne zu mischen; `--excerpt` kürzt die Cues mit.

**Automatische Cues** (ohne Angaben im Plan, Palette `subtle`):

| Rolle | Zeitpunkt | Standardklang (`subtle`) |
|---|---|---|
| `scene_change` | Start jedes Beats ab dem zweiten | abwechselnd `swipe` / `swipe2`, leicht links/rechts |
| `hook_end` | Ende des Hook-Beats (= Start des zweiten) | `whoosh` |
| `close` | Start des Schluss-Beats | `whoosh2` |
| `outro` | Start der Endkarte (nur mit Outro) | `thud` |
| `event` | Bildereignisse der Templates (Einblendungen), ausgedünnt auf `event_min_gap` 1,2 s, nie näher als 0,35 s an einem Übergang | `tick` |
| `intro` | 0,15 s vor der Stimme (nur wenn die Palette einen Klang nennt) | keiner |

Cues aus dem Plan ersetzen automatische Cues in ihrer Nähe (Übergänge innerhalb 0,2 s, Ticks innerhalb 0,35 s).

**Marke: Palette und Pegel** in `brands/<id>/brand.yaml`, Schlüssel `sound` (im Code `brand.design["sound"]`; alles optional):

```yaml
sound:
  palette: tech                 # subtle (Standard) | tech | paper | soft | none, oder eine Liste von Klangnamen
  sounds: {transition: [whoosh, whoosh2], event: click, hook_end: stamp, close: swipe2, outro: stamp, intro: null}
  levels: {sfx_peak_db: -16, event_peak_db: -20, music_db: -10, duck_db: 5}
  music: procedural             # procedural | none | <datei>.wav (Lizenz nötig, siehe assets/music/README.md)
  mood: calm                    # calm | tech | warm | dark | bright
  events: true                  # Ticks an Einblendungen
  event_min_gap: 1.2
  seed: 7                       # fest, sonst aus der video_id
```

Paletten: `subtle` (swipe/swipe2, tick, whoosh, whoosh2, thud), `tech` (whoosh/whoosh2, click, stamp, swipe2, stamp),
`paper` (paper/swipe, tick, stamp, paper, thud, Intro paper), `soft` (swipe/whoosh2, pop, chime, swipe2, chime), `none`.
Eine Liste wie `palette: [whoosh, click, stamp]` wird zu Übergängen (Sweeps), Ticks (click/tick/pop) und Akzent
(stamp/thud/chime/pop) sortiert. Klangnamen: `whoosh`, `whoosh2` (fallend), `swipe`, `swipe2`, `click`, `tick`, `stamp`,
`paper`, `pop`, `thud`, `chime`, `riser`; deutsche Aliasse `papier`, `klick`, `klack`, `tastatur`, `stempel`, `wusch`,
`wischen`, `marker` (= pop), `wumms`, `glocke`, `anstieg`. Ein markeneigenes `brands/<id>/assets/sfx/<name>.wav` mit
Lizenzzeile in `LICENSE.md` daneben überschreibt den gemeinsamen Klang gleichen Namens.

**Plan: eigene Cues.** Drei Wege, alle mit demselben Namensraum:

- `layout.sound_cues`: Liste von `{"beat": "b2", "at": "start" | "end" | 1.2 | "w:Wort", "word": "Wort", "event": "name",
  "cue": "whoosh", "gain_db": -3, "pan": 0.3}`. `word` trifft das erste gesprochene Wort des Beats, das so beginnt
  (`Wort#2` = das zweite). `event` braucht einen Namen aus `SceneOut.named_events` des Markentemplates
  (`out.named_events["stamp_lands"] = t`); fehlt er, fällt der Cue mit Hinweis in `sound.json` und im Prüfbericht
  (`sound_cues`, warn) weg.
- je Beat ein Feld `sound`: `"sound": "stempel"` (am Beat-Start), `{"cue": "stamp", "at": 1.2}` oder eine Liste davon.
  `story.Beat` kennt das Feld nicht; `render_direction.py` liest es aus der Rohdatei, in `plan.timed.json` fehlt es.
  Wer es auch dort sehen will, schreibt es nach `data.sound` (gleiche Form) oder bittet die Hauptsitzung, `story.py` zu erweitern.
- `layout.sound`: dieselben Schlüssel wie in `brand.yaml`, gelten nur für dieses Video (unbekannte Schlüssel wie
  freier Text werden übergangen).

Rollen als Cue-Name (`uebergang`, `einblendung`, `hook_ende`, `schluss`, `abspann`) nehmen den Klang der Palette;
`_leise` senkt um 6 dB; `file:name.wav` nimmt eine eigene Datei aus `brands/<id>/assets/sfx/` (Lizenzzeile nötig);
das alte `assets.sfx` im Plan läuft weiter, landet jetzt aber in der Mischung statt in der HyperFrames-Tonspur
(`data-volume` 0,5 = Palettenpegel). Musiksteuerung: `bett_ein` (Start des Betts), `bett_aus` (Ende mit 2,5 s
Ausblendung), `bett_aus_schlussakkord` (die letzten 3,5 s halten die Tonika). Promptwerk-Schreibweise vom 02.11.2026
(`layout.sound_cues` mit `beat`, `at`, `word`, `event`, `cue`) wird unverändert gelesen.

**Musikbett.** Entscheidung Stefan, 03.11.2026: vorerst selbst erzeugt. `sound_synth.music_bed()` baut je Video ein
Bett (additive Akkordflächen mit verstimmten Teiltönen, Suboktave, weicher Puls oder Zupfer auf dem Takt, bei `tech`
und `bright` ein leises Achtel-Arpeggio, gefiltertes Rauschen als Luft, Tiefpass; Akkordwechsel alle zwei Takte mit
1,5 s Überblendung; Startwert aus der `video_id`, deshalb bei jedem Neurender gleich):

| Stimmung | Tonart und Folge | Tempo |
|---|---|---|
| `calm` (Standard) | D-Dur, I add9 - vi7 - IVmaj7 - V add9 | 72, weicher Puls auf 1 und 3 |
| `tech` | a-Moll, i - VImaj7 - III - VII | 100, Puls je Zählzeit, Arpeggio |
| `warm` | F-Dur, Imaj7 - IVmaj7 - ii7 - V | 66, ohne Puls |
| `dark` | d-Moll, i5 - i7 - VI - VII | 60, tiefer Bordun |
| `bright` | G-Dur, I - V - vi - IV | 96, Puls je Zählzeit, Arpeggio |

Im Manifest steht `sound.music.source: "procedural"` mit Stimmung, Startwert und Generator. Lizenzmusik:
`music: <datei>.wav` (Ablage `brands/<id>/assets/music/` oder `assets/music/`), Nachweis als Zeile in einer
`LICENSE.md` daneben oder als Tabellenzeile mit dem Dateinamen in `08 Recht und Verwaltung\Lizenzen\Lizenzübersicht.md`;
ohne Nachweis bleibt das Bett prozedural und der Bericht setzt `music_license` (review). `audio_style.yaml` › `music.file`
wirkt als derselbe Haken, wenn `brand.yaml` nichts sagt. `music: none` schaltet das Bett ab.

**Pegel** (Standard, `levels`; gemessen auf den Stems vor `loudnorm`, Werte in `manifest.json` › `sound.measured`):

| Was | Regel |
|---|---|
| Stimme | Leitpegel: statisch auf -16 LUFS gebracht (höchstens ±12 dB), dann Spitzenbegrenzer bei -3,5 dBFS (`voice_ceiling_db`, 1-ms-Blöcke, Release 60 ms) |
| Sweeps (whoosh, swipe, paper, riser) | Spitze -16 dBFS (`sfx_peak_db`; bis 03.11.2026 mittags -9 dBFS, Stefan: „die Wisch-Geräusche sind in allen Videos zu laut“), Stereo-Panorama ±0,3 bei Szenenwechseln |
| Kurze Impulse | von Haus aus leiser: click -8, tick -10, pop -5, stamp -3, thud -2, chime -4 dB gegenüber `sfx_peak_db` (`SOUND_LEVEL_OFFSETS`); ein `gain_db` im Plan kommt dazu |
| Ticks an Einblendungen | Spitze -20 dBFS (`event_peak_db`, unabhängig von `sfx_peak_db`) |
| Geräusch-Stem gesamt | nie über -6 dBFS (`sfx_max_peak_db`, sonst wird der Stem abgesenkt); Prüfung `sfx_peak` (fail) |
| Musikbett | `music_db` 10 dB unter der Stimme, wie sie in der Mischung liegt (Manifest `sound.music.voice_reference_lufs`), beim Sprechen um `duck_db` 5 dB weiter abgesenkt (Hüllkurven-Ducker: 10-ms-Blöcke, Schwelle -40 dBFS, Attack 50 ms, Hold 250 ms, Release 600 ms; entspricht einem Sidechain-Kompressor mit fester Tiefe), Ein- 1,5 s, Ausblendung 2,5 s; Prüfung `music_bed_level` (warn, 8-22 dB unter der Stimme über das Video) |
| Mischung | Spitzenbegrenzer bei -3 dBFS (`mix_ceiling_db`), dann statischer Abgleich der ganzen Mischung auf -16 LUFS (`mix_trim_db`) vor dem Encode; `loudnorm` läuft für die Tonebene **linear** (zweistufig: erst messen, dann eine feste Verstärkung, `encode_nvenc(..., loudnorm="linear")`, LRA-Ziel 20). Würde die Verstärkung den True Peak über -1,5 dBTP heben, senkt der Encoder das Ziel um den Überschuss statt in den dynamischen Modus zu fallen (`sound.measured.encode.target_i`); die Prüfung `sound_loudnorm` (warn) meldet, wenn doch dynamisch normalisiert wurde. Danach `aresample`, `alimiter` wie bisher |

Weitere Prüfungen in `fn.direction.checks.check_sound`: `sound_layer` (warn, Cues oder Bett vorhanden), `sfx_stem_peak`
(fail, Stem vor loudnorm über -6 dBFS), `sfx_peak` (fail, Spitze des **kodierten** Tons in den Cue-Fenstern über -0,5 dBFS;
Wert in `sound.measured.sfx_encoded_peak_dbfs`), `music_license` (review), `sound_cues` (warn, weggefallene Cues).

**Befund Gritwerk (03.11.2026):** Kurze Cues (click, tick, stamp) mit 0 dB erreichten nach AAC 0,0 dB. Ursache: das
einstufige `loudnorm` arbeitet dynamisch und hebt Sprechpausen an; ein Impuls in der Pause wurde um mehrere dB verstärkt,
lief in den Limiter und überschoss nach der AAC-Kodierung. Abhilfe seit 03.11. mittags: Impulse leiser (Tabelle), Begrenzer auf
Stimme und Mischung, lineares `loudnorm` für den Tonebenen-Pfad (keine Anhebung in Pausen), Prüfung auf dem kodierten Ton.
Kettentest mit Pausen (3 s Sprache, 3 s Pause, Impulse in den Pausen): dynamisch hob das `loudnorm` einen Stempel in der
Pause um 4,4 dB an; linear blieben alle Cue-Fenster unter -3,7 dBFS, `normalization_type: linear` im loudnorm-Bericht.
Der Pfad ohne Tonebene (`--no-sound`, Langvideo-Composer) läuft unverändert dynamisch. Im Manifest ergänzt der Block `sound` Palette,
Klangzuordnung, Pegel, Cues (`at`, `sound`, `role`, `source` auto/plan/file), Musikquelle und Messwerte; die genutzten
Geräusche erscheinen als `sfx:<datei>` mit Lizenzzeile aus `assets/sfx/LICENSE.md`, das Bett als `music:procedural`.

**Wiederverwendung im 16:9-Composer** (`brands/ai_security/longform/`, dort nichts geändert): die Mischung braucht
keinen DirectionPlan.

```python
from fn.render import sound, ffmpeg
cfg = sound.config_for(brand)                                   # oder sound.SoundConfig(palette="tech", mood="dark")
cues = sound.auto_cues([s["start"] for s in scenes[1:]], total, cfg, hook_end=scenes[1]["start"],
                       close_start=scenes[-1]["start"], events=visual_events, voice_start=vstart)
mix = sound.mix_sound(voice_wav, cues, cfg, out / "sound" / "mix.wav", total=total, voice_start=vstart,
                      brand_dir=brand.dir, video_id=video_id)
ffmpeg.encode_nvenc(raw, out_mp4, audio=mix.path, loudness_lufs=-16.0)
manifest["sound"] = mix.manifest()
```

Eigene Cues dazu: `sound.Cue(at=12.4, sound="stamp", role="plan", source="plan")` an die Liste anhängen, oder
`sound.merge_cues(auto, manual, total)`. Geräusche neu erzeugen (byte-identisch): `python -m fn.render.sound sfx`;
Selbsttest der Mischung mit Kunststimme: `python -m fn.render.sound selftest`.

**Higgsfield-Audio, Lizenzbefund (Nutzungsbedingungen higgsfield.ai/terms, Stand „Last updated: October 23, 2026“,
gelesen 03.11.2026):** Abschnitt 4.4 beansprucht kein Eigentum an Outputs und schränkt die kommerzielle Nutzung nicht
ein; Musik und Audio werden aber nirgends eigens geregelt (nur in der Inhaltsdefinition 3.1 genannt), Abschnitt 8
unterwirft Ausgaben von Drittanbieter-Modellen deren Richtlinien (die strengere gilt), Abschnitt 13.2 legt die
Rechteklärung dem Nutzer auf, und Outputs dürfen zum Training verwendet werden. Welches Modell hinter `generate_audio`
steht und welche Drittrichtlinie dann gilt, ist aus den Bedingungen nicht ermittelbar. Befund: für Musik nicht ohne
Prüfung des konkreten Audiomodells und seiner Anbieterbedingungen nutzen; bis dahin bleibt das Bett prozedural.

**Nachweis (03.11.2026, beide Demos unter `OneDrive\Business\05 Produktion\_Demos\tonebene\`, Stimmen wiederverwendet, keine Gemini-Anfrage):**

| Demo | Einstellung | Cues | Video (nach linearem loudnorm) | Stimme / Geräusche / Bett vor loudnorm | kodierte Spitze um die Cues | Prüfungen |
|---|---|---|---|---|---|---|
| `engines-20261109-2-en-SND` (Revlore, Zeitlupe) | Standard: Palette `subtle`, Bett `calm` | 33: 6 Szenenwechsel, Hook-Ende, Schluss, 25 Ticks | -16,0 LUFS, Spitze -2,8 dB (True Peak -2,4) | -16,2 LUFS (Begrenzer 3,0 dB) / Spitze -16,0 dBFS / -26,0 LUFS, beim Sprechen -30,8 LUFS (14,6 dB unter der Stimme) | -2,8 dBFS (`whoosh2` am Schluss, unter der Stimme) | VALIDATED, `overlap_check` 0, `sfx_peak` ok, loudnorm `linear` (Ziel -16,0) |
| `ai_security-20261115-3-de-SND` (Scutoria, mit Higgsfield-Clips) | `--assets --sound palette=tech,mood=dark` | 26: 4 Szenenwechsel, Hook-Ende `stamp`, Schluss `swipe2`, 20 Klicks | -16,0 LUFS, Spitze -2,7 dB | -16,1 LUFS (Begrenzer 1,0 dB) / Spitze -16,0 dBFS / -26,0 LUFS, beim Sprechen -30,8 LUFS (14,7 dB unter der Stimme) | -2,9 dBFS (`whoosh2` am Szenenwechsel 22,7 s, unter der Stimme) | VALIDATED, `overlap_check` 0, `sfx_peak` ok, loudnorm `linear` (Ziel -16,0) |

Stand der Tabelle: 03.11.2026 nachmittags, nach Stefans Rückmeldung zu den Wisch-Geräuschen (Sweeps -16 dBFS) und der
Absicherung des linearen loudnorm. Ein Szenenwechsel ohne Sprache (Revlore 17,4 s) liegt im Video jetzt bei -12,8 dB
Spitze (vorher -6,6 dB bei -9 dBFS Sweep-Pegel).

Gemessen mit `ffmpeg -af volumedetect,ebur128=peak=true` auf `video.mp4` und den Stems in `storage\direction\<id>-SND\sound\`.
Der Mock-Trockenlauf läuft weiter (`--tts mock --excerpt 15`: VALIDATED, 7 Cues; mit `--no-render` entsteht `sound.json` ohne Mischung).
Die Mischung kostet je Video etwa 12 s zusätzlich (Bett 5 s, ffmpeg-Messungen, loudnorm-Vormessung). Die Stimme wird als
Dual-Mono gemessen (`ffmpeg.audio_stats(..., dual_mono=True)`, +3 LU gegenüber der Mono-Messung), weil sie so in der
Stereo-Mischung liegt; das Stimm-Stem ist deshalb ebenfalls stereo.
