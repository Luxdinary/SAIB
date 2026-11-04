# Tagesläufer (daily runner) – automatische Tagesproduktion je Marke über eine Modell-API

Stand 03.11.2026, Sitzung „Tagesläufer“ (Auftrag der Hauptsitzung nach Stefans Entscheidung „Sonnet + Tagesläufer“).
Ziel: Skript und Regie je Thema schreibt ein Modell in einem kurzen, eigenständigen Auftrag (seit Stefans Entscheidung vom
03.11.2026, 16:50 Wien, über `claude -p` im Ultra-Abo mit `claude-sonnet-5-5`; kein API-Schlüssel; Gemini nur für Stimmen),
nicht mehr eine Claude-Code-Sitzung mit Verlauf; der Rest der Kette (Vertonung, Render, Prüfungen, Export, Redaktionsplan,
Kosten) läuft unverändert über die vorhandenen Skripte. Code: `src/fn/daily/`, Einstieg `scripts/daily_runner.py`,
Konfiguration `config/daily.yaml`, Zustand `data/daily/`.

## 1. Bestandsaufnahme (03.11.2026, nichts am Code geändert)

### 1a. Die bestehende Kette je Video

| Schritt | Skript / Modul | Was passiert |
|---|---|---|
| Plan | `data/direction/<video_id>[.<fassung>].json` | Regie-Skript im Schema der Story-Engine (`fn.direction.story.DirectionPlan`), von Hand geschrieben |
| Vorprüfung | `story.validate()`, `hooks.validate_set()` in `scripts/render_direction.py` | Story-Reihenfolge, Quellen-IDs, Szenentypen der Marke, `UNVERIFIED`-Sperre, fünf Hook-Kandidaten (einer je Typ, `truth` >= 4) |
| Trockenlauf | `render_direction.py <plan> --version <v> --tts mock --no-render` | Stimme stumm (Mock), Wortzeiten geschätzt, Director baut das HyperFrames-Projekt, `hyperframes check` (Lint, Layout), Regie-Prüfungen ohne Video, `sound.json`; Exit 0 = ok, 6 = Regie-Prüfung rot, 5 = Länge außerhalb 65–90 s |
| Vertonung | `render_direction.py ... --tts gemini` (oder `--reuse-voice <wav>`) | eine Gemini-TTS-Anfrage je Lauf (`fn.tts.gemini`, Modell aus `config/voices.yaml`, `GEMINI_TTS_MODEL` schaltet auf Pro); die bezahlte Aufnahme bleibt als `storage/direction/voice_<id>_<v>_gemini.wav` + `.json` liegen |
| Wortzeiten | `fn.transcribe` (faster-whisper large-v3, CUDA) | Ausrichtung auf den Plantext, Beat-Zeiten über `director.assign_timing` |
| Render | `scripts/render_queue.py <brand_id> -- scripts/render_direction.py <plan> --version <v> ...` | faire Warteschlange (`data/render_queue/`, `data/render.lock`, `data/render.pause` hält alles an), HyperFrames + NVENC, Tonebene (`fn.render.sound`, `loudnorm` linear), Cover, Standbilder, `manifest.json`, `report.json`, `post.json`, `captions.json`, Spiegel nach `05 Produktion\_Demos\<marke>-regie\` |
| Überschneidung | `node scripts/overlap_check.mjs storage/direction/<id>-<v>/project` | Pflicht vor dem Export; Exit 1 bei Befund; Liste `small_text` (< 24 px) |
| Export | `scripts/export_production_folder.py <plan> --version <v> --short "<Kurztitel>"` | Ordner `05 Produktion\<Marke>\<JJJJ-MM>\<JJJJ-MM-TT Kurztitel>` aus `_Vorlage Video`; Skript.md, Schnittprojekt (plan.timed, manifest, report, post), 9x16.mp4, Cover, SRT, Veröffentlichung.md; verweigert Nicht-Gemini-Stimmen (Exit 4) und vorhandene Videos ohne `--force` (Exit 3) |
| Redaktionsplan | `04 Redaktionsplan\Redaktionsplan.csv` (Trennzeichen `;`, UTF-8 mit BOM) | eine Zeile je Fassung und Sprache, Status `fertig`, Produktionsordner relativ zu `Business`, Notiz mit Herkunft, Stimme, Prüfbericht, Überschneidung, Geräuschpegel, „Nicht veröffentlicht.“ |
| Kosten | `fn.costs.CostLogger` -> `data/costs/costs.jsonl` | je Lauf `tts` (Token, USD), `transcribe`, `render`; `manifest.cost` fasst alle Einträge mit derselben `video_id` (`<plan-id>-<fassung>`) zusammen |

Abweichungen je Marke: Gigastruct rendert über den eigenen Wrapper `brands/megaconstruction/render/render_gigastruct.py`
(gleiche Argumente wie `render_direction.py`, löst die 3D-Wortanker in `layout.model3d` auf und legt die WebGL-Leinwand
unter die Szenen). Promptwerk erzeugt die deutsche Stimme mit `brands/claude_workflows/echtlauf/voice_tts.py --say Claude=Klohd`
und rendert dann mit `--reuse-voice`. Tintora (`brainrot`) hat einen eigenen Renderer (`brands/brainrot/renderer/`, Serie
„Juna“, 13 Kling-Clips je Reel, alle Stimmen Pro) und keinen Plan im Story-Schema; der Testreel-Ordner enthält
`Prüfbericht.json` und `Tonmanifest.json` statt `plan.timed.json`/`manifest.json`.

### 1b. Aufbau der neun freigegebenen Testvideo-Pläne (Prüfbericht VALIDATED, HUMAN_REVIEW bei Risiko hoch)

Gemeinsame Felder (`story.DirectionPlan`): `video_id`, `brand_id`, `language`, `title`, `notes`, `beats[]` (`id`,
`function`, `scene_type`, `spoken`, `data`, `source_ids`, `duration_hint`, `overlay`), `hook` (`id`, `note`),
`hook_candidates[]` (`id`, `type`, `spoken`, `on_screen`, `scores{clarity,relevance,curiosity,truth,visual}`,
`source_ids`, `visual`, `why`), `sources[]` (`id`, `url`, `title`, `label`, `checked_at`), `unverified[]`, `layout`,
`assets`. In `layout` überall: `format`, `explainer: false`, `outro: false`, `caption_mode: phrases`,
`caption_max_words: 4`, `caption_width_px: 800`, `caption_transform: none`, `caption_bottom_px`, `zone_top`,
`zone_h`, `zone_lower_right_px` (teils), `progress_y`, `ai_label_bottom_px`, `tail_seconds` (2,4–2,6),
`description`, `companion_text`, `hashtags`, `sound` (Palette, Stimmung, `levels.sfx_peak_db` -16 bis -19), `sound_cues[]`
(`beat`, `at` = `start|end|Sekunden|w:Wort[#n][+s]`, `cue`, `gain_db`, `note`). Zeitanker in den Szenendaten je Marke:
`w:Wort`, `@Wort+0.5`, `<ereignis>_word`, `at_word`. Sprechtext 920–1.320 Zeichen (DE), Stimme 72–84 s.

| Marke (id) | Format | Szenentypen im Plan | Bildmaterial | Besonderes |
|---|---|---|---|---|
| Scutoria (`ai_security`) | „Du sitzt am Platz“ (Was tust du?) | `sb_screen`, `sb_lens`, `sb_freeze`, `sb_montage`, `sb_action`, `sc_close` | `assets/higgsfield/test2611/` (Bilder, 5 Clips) und `yt/`; keine Bibliothek | Medien je Beat in `data.media.shots`, Cues in `data.cues`; Aufbau B–D noch nicht gebaut |
| Promptwerk (`claude_workflows`) | Echtlauf | `rec_photo`, `rec_table`, `rec_replay`, `rec_diff`, `rec_answer`, `rec_split` (+ `rec_auftrag`, `rec_rule`, `rec_result`, `rec_protokoll`) | `library/` (29 Realbilder, 1 Clip), `tv_*` | braucht eine echte Aufzeichnung `echtlauf/recordings/<id>/` (`layout.echtlauf.recording`); 24 Aufzeichnungen (12 Themen DE+EN) liegen vor |
| Revlore (`engines`) | Zeitlupe (Technik-Kanal) | `zt_photo`, `zt_mcb`, `zt_curve` (Testvideo); Motorreihe `zl_hook`, `zl_strobe`, `zl_cause`, `zl_trace`, `zl_realtime` | `library/` (23 Bilder, 1 Clip), `testvideo/` | `zt_mcb` ist das Modell des Sicherungsautomaten; jedes neue Technik-Thema braucht ein eigenes gerechnetes Modell (neuer Code) |
| Gigastruct (`megaconstruction`) | Bauaufgabe | `gb_task`, `gb_load`, `gb_principle`, `gb_build`, `gb_calc`, `gb_proof`, `gb_close` | `library/` (29 Bilder, 1 Clip), `fehmarnbelt/` | `layout.model3d` (3D-Objekte, Kamera, Wortanker), `layout.media`, `layout.computations`, `chapters`; eigener Render-Wrapper; nur Aufbau A gebaut |
| Suitwerk (`menswear`) | Kreidestrich | `kw_photo`, `kw_weave`, `kw_draft`, `kw_flip`, `kw_close` (+ `kw_hook`, `kw_weigh`, `kw_range`, `kw_fibre`, `kw_yarn`, `kw_finish`) | `library/` (34 Bilder, 1 Clip), `testvideo/` | Fotos in `data.shots[].src` = `library/<datei>` oder `testvideo/<datei>`, `backdrop.src`; LAYER kopiert sie |
| Gritwerk (`motivation`) | Laborbuch | `lb_photo`, `lb_hook`, `lb_split`, `lb_replicate`, `lb_verdict`, `lb_try` (+ `lb_setup`, `lb_measure`, `lb_result`) | `library/` (39 Bilder, 1 Clip), `testvideo/` | `layout.laborbuch`, `layout.risk_level`; Aufbau A und C gebaut, B/D/E nicht |
| Frontlore (`military_history`) | Rekonstruktion | `fr_task`, `fr_model`, `fr_solution`, `fr_protocol`, `fr_example`, `fr_stages`, `fr_finding` (+ `fr_means`) | `library/` (44 Bilder, 1 Clip: Karten, Tische, Papiere), `testvideo/` | `layout.ruler` (Zeitlineal), `data.media`, `data.cues`; Risiko hoch -> HUMAN_REVIEW |
| Dewlane (`beauty`) | Nahaufnahme | `nh_stage`, `nh_lens`, `nh_amount`, `nh_effect`, `nh_apply`, `nh_close` (+ `nh_hook`, `nh_facts`, `nh_list`, `nh_steps`, `nh_time`, `nh_versus`) | `library/` (32 Bilder, 1 Clip), `assets/higgsfield/dl_*` | `layout.media[]` (Bild/Clip je Beat), `layout.stamp`; Risiko hoch -> HUMAN_REVIEW |
| Tintora (`brainrot`) | Serie „Juna“ (Anime, Kling-Clips) | kein Story-Plan; eigener Renderer | keine Bibliothek, Credits nicht freigegeben | nicht über diese Kette produzierbar |

Die Szenentypen und ihre Datenfelder stehen in den Docstrings der Markenmodule (`brands/<id>/scenes.py` und die
Format-Unterordner); `fn.render.brand_scenes.load(brand_id)` liefert `templates`, `limits`, `hook_types`.

### 1c. Prüfungen

- Plan: `story.validate` (hart), `story.advice` (weich), `hooks.validate_set`, gewählter Hook muss `eligible` sein.
- Director: Textgrenzen (`LIMITS`, „chars >“ = fail `readability_text_limits`), fehlende Wortanker werden als `problems` gemeldet.
- `hyperframes check`: Lint-Fehler brechen ab (Exit 3), Layout-Fehler werden gelistet.
- `checks.check_direction`: `scene_variety` (>= 2 Typen), `visual_cuts_static` (<= 14 s), `readability_*`, `platform_overlay`,
  `logo_intro_seconds`, `audio_level_*`; `checks.check_sound`: `sfx_stem_peak` (<= -6 dBFS), `sfx_peak` (kodiert <= -0,5 dBFS),
  `sound_loudnorm`, `music_bed_level`, `music_license`, `sound_cues`.
- `compliance.check_technical` (Dauer 65–90 s, Format) und `check_content` (Quellen, verbotene Begriffe, `risk_high_review`).
- Status: `FAILED` (ein fail), `HUMAN_REVIEW` (ein review, immer bei Risiko hoch), sonst `VALIDATED`.
- `overlap_check.mjs` vor dem Export (Exit 1 bei Überdeckung), `small_text` leer.

### 1d. Konzeptpläne (`04 Redaktionsplan\Konzeptplan <Marke> (ab November 2026).md`): wo die Reihenfolge steht

| Marke | Reihenfolge | Bildaufbau |
|---|---|---|
| Dewlane | Tabelle „Die ersten 28 Themen“ (`Tag | Nr. | Thema | Aufbau | Material | Neues Bild`) | Spalte Aufbau (A–D) |
| Frontlore | Tabelle „Erste Tage“ (`Tag | Thema 1 | Aufbau | Thema 2 | Aufbau | Stand`), danach Vorschläge mit Zuordnung A–D je Nr. | Listen je Aufbau |
| Gigastruct | Vorschläge-Tabelle (Spalte Bildaufbau), A -> B -> C in Tabellenreihenfolge, Prüfstand = D | Spalte; nur A gebaut |
| Gritwerk | Tabelle „Reihenfolge der ersten sieben Tage“ (`Tag | Thema 1 (Aufbau) | Thema 2 (Aufbau)`, Titel ohne Nr.) | Klammer; A und C gebaut |
| Promptwerk | Tabelle „Erste Tage“ (`Nr. 8 … (A)`), ab 09.11. Vorschläge in Tabellenreihenfolge | Klammer A–D (Reihe) |
| Revlore | Technik-Themen „Zuerst zu bauen“ 75, 103, 93, 121, 99, 91, 108, 86 (alle brauchen neue Modelle); Motor-Themen in Tabellenreihenfolge | Zuordnung A–E je Nr.; Wechselregel |
| Scutoria | Tabelle „Takt der ersten Tage“ (`Nr. 47 „…“, A`), danach nach Reihe/Objekt | A gebaut, B–D angekündigt |
| Suitwerk | Tabelle „Reihenfolge ab 04.11.2026“ (`Stoffgewicht (B)`), danach Nr. 6–16 und 56–64 | Klammer A–E |
| Tintora | Folgen und Abschnitte der Staffel 1 | – |

Gemeinsame Regeln: zwei Themen eines Tages nie mit demselben Aufbau, kein Aufbau an drei Themen hintereinander,
höchstens 2 Credits je Thema (der Tagesläufer bucht nichts: 0 Credits, nur Bibliothek und Testvideo-Material).

### 1e. Befunde für die Automatisierung

1. **Revlore:** Revlore ist seit 02.11.2026 ein Technik-Kanal. Die Technik-Themen 75–126 brauchen je ein eigenes gerechnetes
   Modell (`zt_mcb` gilt nur für den Sicherungsautomaten). Allgemein geht der Aufbau F „Kennlinie“ (`zt_chart`) der Revlore-Sitzung.
   Der Tagesläufer produziert nur Themen, die `brands/engines/aufbauten.yaml` mit Quellen nennt (Technik 77, 84, 87, 107, 111;
   Motor 38, 40, 10, 53, 50); alle anderen sind „braucht Modell“. Regel der Hauptsitzung (03.11., 18:52): Technik-Themen zuerst,
   Motor-Themen höchstens jedes dritte Thema (`topic_source.limited_heading` in `config/daily.yaml`: in je drei aufeinanderfolgenden
   Themen höchstens eines aus einer Tabelle mit „Motor“ in der Überschrift; die Folge zählt `data/daily/state.json`). Die Stichworte
   je Thema (`hinweis`: Formel, Zahlenvorgaben, Grenzen wie „nur schematisch“) gehen in den Prompt. Standbilder der Bibliothek macht
   der Tagesläufer selbst zu Clips (`media.py`, 30 s, Lizenzzeile); `brands/engines/zeitlupe/still_to_clip.py` ist dafür nicht nötig.
2. **Promptwerk:** jedes Thema braucht eine echte Aufzeichnung (`record_run.py`, `claude -p` mit dem Abo-Login der
   Desktop-App). Vorhanden: 12 Themen DE+EN (Takt 04.–08.11. und Testvideo). Der Tagesläufer nimmt nur Themen mit
   vorhandener Aufzeichnung und nimmt keine neuen auf (Abo-Kontingent).
3. **Tintora:** eigener Renderer, keine Bibliothek, Kling-Clips je Reel, Credits nicht freigegeben: nicht im Tagesläufer.
4. **Gigastruct:** Pläne tragen 3D-Objekte, Kamera-Keyframes und Rechnungen (`layout.model3d`, `computations`); nur
   Aufbau A ist gebaut. Das Modell muss das 3D-Schema aus dem Beispiel nachbilden; Risiko für Fehlanker.
5. **Aufbauten, die noch nicht gebaut sind** (Scutoria B–D, Gritwerk B/D/E, Gigastruct B–D): der Tagesläufer ersetzt
   sie durch einen gebauten Aufbau und vermerkt das in Plan, Veröffentlichung.md und Redaktionsplan.
6. **Mock-Stimme:** zu langsam für englische Pläne (Länge > 90 s im Trockenlauf, Exit 5). Der Tagesläufer prüft die
   Länge vorab mit markenbezogenen Zeichen-pro-Sekunde-Werten der freigegebenen Stimmen und wertet Exit 5 im
   Mock-Trockenlauf nur als Hinweis.
7. **Gemini-Kontingent:** 100 Flash-Anfragen je Tag für alle Marken; je Marke höchstens 4 am Tag (2 Themen x DE/EN),
   also keine Wiederholung bei Längenfehlern; Ausweich Pro nur, wenn `--pro-fallback` gesetzt ist.
8. **Quellen:** Das Modell darf keine URLs erfinden. Quellen kommen aus dem Kalender (`data/calendars/<id>_2026-11.json`:
   `source_urls`, `notes`, `source_checked_at`; Research-Dateien mit `source_evidence`), aus dem freigegebenen Plan und
   aus dem Konzeptplan; `checked_at` wird vom Tagesläufer gesetzt, wenn die URL erreichbar ist (HTTP 200/3xx), sonst
   bleibt das Kalenderdatum und der Plan bekommt einen Hinweis.
9. **Kosten des Modells:** Token (Eingabe, Ausgabe, Cache) werden je Video als `llm`-Eintrag in `data/costs/costs.jsonl`
   geloggt, 0 USD mit „Abo, kein Einzelpreis“ (Hauptsitzung, 03.11.2026); die CLI-Schätzung steht nur im Hinweis.
10. **`claude -p` headless (geprüft 03.11.2026, gegen 17:25 Wien):** `claude auth status` meldet Login über claude.ai, Konto
   stefan.dallinger.me@gmail.com, Abo „max“; ein Minimalaufruf `claude -p --model claude-sonnet-5-5 --output-format json
   --tools "" --no-session-persistence --disable-slash-commands --strict-mcp-config --setting-sources ""` antwortete in
   4,8 s mit JSON (Felder `result`, `usage.input_tokens`, `usage.output_tokens`, `cache_*`, `total_cost_usd`,
   `modelUsage`), ohne Fenster, aus einer Umgebung ohne die `CLAUDE*`/`ANTHROPIC*`-Variablen der Desktop-App (so läuft es
   auch in der Aufgabenplanung). Der Prompt geht über stdin (Windows-Befehlszeilen sind auf 32 k Zeichen begrenzt).

## 2. Aufbau des Tagesläufers

| Datei | Aufgabe |
|---|---|
| `scripts/daily_runner.py` | Einstieg (Argumente unten); je Marke ein `DailyRunner`, Zusammenfassung `data/daily/runs/<datum>_summary.md`; stoppt alle weiteren Marken, wenn das Kontingent von `claude -p` erreicht ist |
| `config/daily.yaml` | Vorgaben und je Marke: Konzeptplan, Format-Bibel, Testvideo-Konzept, Beispielpläne DE/EN, erlaubte Szenentypen, Materialordner, Render-Skript, Zeichen je Sekunde der Stimme, Themenquelle (inklusive `exclude_title_words`), Modell, Aufwand, Reservierungstage |
| `brands/<id>/aufbauten.yaml` | gebaute Bildaufbauten je Marke (pflegt die Marken-Sitzung, der Tagesläufer liest sie bei jedem Lauf); Vorlage `config/aufbauten.vorlage.yaml` |
| `src/fn/daily/settings.py` | Konfiguration lesen (Vorgaben + Markenblock); `load_aufbauten()` |
| `src/fn/daily/topics.py` | Konzeptplan-Tabellen lesen (Vorschläge, Tagestabellen, Bildaufbauten), Tagesthemen den Vorschlagszeilen zuordnen, Reihenfolge, „reserviert“ |
| `src/fn/daily/context.py` | Kontext je Marke: Format-Auszug, Beispielpläne (gekürzt), Szenen-Docstrings aus dem Code der Marke, Materialliste (nur Dateien mit Lizenzzeile), Kalenderquellen und Belegsätze, Erreichbarkeitsprüfung der URLs, Aufzeichnungen (Promptwerk) |
| `src/fn/daily/prompts.py` | Regeln und Aufgabe DE, Übersetzungsprompt EN (gleiche Szenen), Reparaturprompts (Validator und Renderer) |
| `src/fn/daily/llm.py` | `claude_cli` (Standard), `anthropic` (SDK, nur mit Schlüssel), `mock`; Token je Aufruf als `llm`-Eintrag im Kostenlog; `RateLimited` bei erreichtem Kontingent |
| `src/fn/daily/validate.py` | Planprüfung vor jedem Renderer-Aufruf (Abschnitt 3) und Strukturvergleich DE/EN |
| `src/fn/daily/media.py` | Standbilder in `assets.hero`/`assets.background` werden zu 30-s-Clips mit Kamerafahrt (`brands/<id>/assets/higgsfield/daily/`, Lizenzzeile abgeleitet, 0 Credits) |
| `src/fn/daily/records.py` | Plan-IDs, Zustand `data/daily/state.json`, Zeile in `Redaktionsplan.csv` (anhängen), Marker im Konzeptplan (nach Inhalt), Zähler des gemeinsamen Gemini-Kontingents |
| `src/fn/daily/pipeline.py` | Ablauf je Marke und Thema (2a), Protokoll `data/daily/runs/<datum>_<marke>.log` (alle Befehle, Ausgaben und Modellantworten), Ergebnis `data/daily/runs/<datum>_<marke>_<zeit>.json` |
| `scripts/daily_costs.py` | Token, Stimme und Renderzeit je Video aus `data/costs/costs.jsonl` (nur gerenderte Videos, `--plans` auch reine Plan-Einträge) |
| `automation/run_daily.ps1`, `register_tasks.ps1` | Aufgabenvorlage (der Eintrag „FN Daily Runner“ ist auskommentiert; Stefan registriert selbst) |
| `src/fn/daily/monthplan.py`, `proposals.py`, `scripts/month_planner.py`, `automation/run_month_plan.ps1` | Monatsplan und Monatsplaner (Abschnitt 6): Simulation der Themenwahl, Plan-Dateien, Übersicht, Themenvorschläge für Lücken, Monatsaufgabe |
| `tests/test_daily*.py` | 34 Tests: Tabellen, Tageszellen, Anker, JSON-Auszug, CSV und Marker, Positivliste, Beispiel-Auszug, Belegprüfung, Sperrdatei, Revlore-Regel, Monatsplan, Plan-Schicht, Titelabgleich, Themenvorschläge, Rückfall bei ungültiger Aufbautendatei, Neuplanung vor dem Lauf, Tagesgrenze (78 Tests im ganzen Repository) |

### 2a. Ablauf je Marke und Tag

1. **Themen.** Tagestabelle in Reihenfolge, dann die Vorschlagstabelle (Suitwerk: `then_nrs`). Übersprungen wird ein Thema, das
   erledigt ist (Zustand, Marker in der Zeile, Redaktionsplan-Zeile mit Status fertig oder geplant zum selben Kalendereintrag),
   **reserviert** (Hauptsitzung, 03.11.: `reserved_days` = 04.11. und 05.11. in `config/daily.yaml`, außerdem jede Zeile mit dem Wort
   „reserviert“), laut Konfiguration nicht geeignet (`exclude_title_words`, Suitwerk: Muster, die `warp_up()` nicht zeichnen kann),
   ohne geprüfte Quelle (`require_sources`), ohne Aufzeichnung (Promptwerk) oder ohne passenden Aufbau.
2. **Bildaufbau.** Liegt `brands/<id>/aufbauten.yaml` vor, gelten nur Aufbauten mit `gebaut: true`. Ein Aufbau ohne Schlüssel
   `themen` ist allgemein; mit `themen` (auch leer) trägt er nur die dort genannten Konzeptplan-Nummern (Revlore: Modelle,
   Scutoria: Mail und Chat). Hat kein gebauter Aufbau Platz für ein Thema, meldet `--list-topics` „braucht Modell oder Aufbau“.
   Gewählt wird der im Konzeptplan geplante Buchstabe, wenn er passt; sonst Ersatz nach Wechselregel (nicht wie das andere
   Thema des Tages, nicht wie das zuletzt erledigte). Der Ersatz steht in den Plan-`notes` und in der Redaktionsplan-Notiz.
   Ohne die Datei gilt `aufbau.available` aus `config/daily.yaml`. Je Aufbau fließen `szenentypen`, `beispielplan` (Few-Shot) und
   `hinweis` in den Prompt, je Thema `quellen` und `hinweis`.
3. **Quellen.** URLs aus dem Kalendereintrag (`belegt im Kalender <topic_id>` oder Titelabgleich) und Belegsätze aus der
   Research-Datei, bei Revlore aus `aufbauten.yaml`. HEAD/GET-Prüfung: erreichbar setzt `checked_at` auf das Laufdatum, sonst
   bleibt das Kalenderdatum und der Plan bekommt einen Hinweis.
4. **DE-Plan.** Ein kurzer, eigenständiger Auftrag an `claude -p` ohne Verlauf: Regeln des Regie-Systems, Format-Auszug,
   Kurzkonzept, Bildaufbau, Szenen-Docstrings, Materialliste, gekürzter Beispielplan, Aufgabe mit Belegen. Antwort ist ein JSON-Plan.
   Validator (Abschnitt 3); bei Fehlern bis zu `repair_rounds` (2) Reparaturrunden mit der Fehlerliste. Standbilder in `assets`
   werden zu Clips. Datei `data/direction/<id>.<Fassung>.json`.
5. **Trockenlauf DE.** `<render_script> <plan> --version <Fassung>dry --tts mock --no-render` (bei Exit 5 wegen der Mock-Länge
   erneut als `--excerpt`): Lint, Layout, Textgrenzen, Regie-Prüfungen, Ton-Cues, ohne Kosten. Lehnt der Renderer den Plan ab,
   geht seine Ausgabe (Traceback oder Befunde mit Beat-Tabelle) an das Modell zurück, bis zu `dry_run_repairs` (2) Runden; der
   Sprechtext darf dabei nicht geändert werden. Besteht auch der reparierte Plan nicht, entsteht keine englische Fassung.
6. **EN-Plan.** Übersetzungsprompt mit dem DE-Plan: gleiche Beats, Datenschlüssel, Dateien und Quellen, Wortanker auf englische
   Wörter, `file:`-Aufzeichnungen dürfen je Sprache verschieden sein. Validator, Strukturvergleich mit DE, Trockenlauf wie bei DE.
7. **Stimme und Render** (`--dry-run` und die Attrappe enden vorher). Flash-Zähler je Marke (`flash_requests_per_brand_per_day`,
   4) und gemeinsamer Zähler aller Sitzungen (100 minus 12 Reserve, aus `costs.jsonl` seit dem Reset um Mitternacht Pazifik);
   danach nur mit `--pro-fallback` Pro, sonst „Vertonung offen“. Promptwerk DE: `voice_tts.py --say Claude=Klohd`, dann `--reuse-voice`.
   Render über `scripts/render_queue.py <marke> -- <render_script> <plan> --version D1 --tts gemini [--assets]`; `data/render.pause` hält
   an. Die TTS-Kosten loggt `render_direction.py`.
8. **Prüfungen.** Status aus `manifest.json` (`FAILED` bricht ab, `HUMAN_REVIEW` bleibt bei Risiko hoch erhalten),
   `overlap_check.mjs` (Befund bricht ab, `small_text` als Hinweis).
9. **Export und Buchführung.** `export_production_folder.py <plan> --version D1 --short "<short_title>"` (EN: `… EN`); Zeile im
   Redaktionsplan (Status fertig, Produktionsordner relativ, Notiz mit Aufbau, Modell, Token, Stimme, Prüfbericht, Überschneidung,
   Geräusch-Stem, variable Kosten, „Nicht veröffentlicht.“); Zustand und Marker `Tagesläufer: produziert <datum> (<ids>)` in der
   Vorschlagszeile und in der Zelle des Themas in der Tagestabelle.

### 2b. Aufruf

```
.venv\Scripts\python.exe scripts\daily_runner.py --brands all --list-topics          # Auswahl zeigen, nichts schreiben
.venv\Scripts\python.exe scripts\daily_runner.py --brands engines,menswear --dry-run  # Pläne und Prüfungen, nur Modellaufrufe
.venv\Scripts\python.exe scripts\daily_runner.py --brands all                         # ganzer Tag (2 Themen je Marke, DE und EN)
```

Weitere Schalter: `--topics N`, `--date JJJJ-MM-TT`, `--languages de`, `--provider claude_cli|anthropic|mock`, `--effort low|medium|high`,
`--topic <Nr>` (ein Thema erzwingen), `--no-plan` (Monatsplan nicht lesen, Abschnitt 6c), `--prototype` (Kennzeichnung „Tagesläufer-Prototyp“ in Redaktionsplan, Veröffentlichung.md
und Plan-`notes`), `--no-export`, `--no-mark`, `--no-source-check`, `--pro-fallback`, `--max-flash N`. Standard ist `claude_cli`
(Abo-Login von Claude Code, Aufwand `low`); `--provider mock` (Beispielplan des gewählten Aufbaus unter neuer id, EN als Kopie des DE-Plans, Längenprüfung entfällt) endet immer nach dem Trockenlauf und kostet nichts.

### 2c. Kosten und Kontingente

- **Modell:** Token je Aufruf (Eingabe, Ausgabe, Cache) als `llm`-Eintrag unter `<video_id>-<Fassung>` in `data/costs/costs.jsonl`
  und damit im `manifest.cost` des Renders; 0 USD mit „Abo, kein Einzelpreis“ (die Schätzung der CLI steht im Hinweis). Der Preis in
  `price_usd_per_million` gilt nur für `provider: anthropic`.
- **Gemessen am 03.11.2026** (Prompt DE 19–26 k Zeichen je Marke, EN 1,9 k plus der DE-Plan):

  | Aufwand | Aufruf | Zeit | Ausgabe-Token |
  |---|---|---|---|
  | Standard | Suitwerk DE | 261 s | 37 k über mehrere Turns, Antwort abgeschnitten |
  | `medium` | Suitwerk DE | 126 s | 19,3 k (davon etwa 3,2 k sichtbares JSON) |
  | `low` | Dewlane DE | 22–38 s | 4,3–4,7 k je Aufruf |
  | `low` | Dewlane EN | 20–40 s | 4,0–4,6 k je Aufruf |

  Ein Video-Paar (DE und EN, mit Reparaturrunden) braucht danach etwa 20–30 k Ausgabe- und 40–50 k Cache-Token (Dewlane: DE 3 Aufrufe
  13,7 k, EN 2 Aufrufe 8,1 k). Für 16 Themen am Tag sind das rund 350 k Ausgabe-Token; was das für das Wochenkontingent bedeutet, ist
  nicht ermittelbar (die CLI meldet nur `allowed_warning`).
- **Stimme:** Flash je Marke höchstens 4 Anfragen am Tag, keine Wiederholung bei Längenfehlern; alle Sitzungen zusammen höchstens 88
  (100 minus Reserve).
- **Higgsfield:** nie; Material nur aus Bibliothek, Testvideo-Ordnern und den abgeleiteten Clips.

## 3. Prüfungen und Schutz

**Planprüfung (`validate.py`, vor jedem Renderer-Aufruf; Fehler gehen mit Klartext in eine Reparaturrunde):**
`story.validate` und `hooks.validate_set` (fünf Hook-Typen, `truth` mindestens 4); Szenentypen der Marke und des Aufbaus; Zeichengrenzen
(`LIMITS`, oberste Ebene); Feldtypen der Hook-Kandidaten; Wortanker gegen den Sprechtext (Schreibweise wie `_norm` der Templates,
auch `+0.4+0.1`); Quellen nur aus der Quellenliste oder als vorhandene `file:`-Aufzeichnung, `checked_at` als Datum; Dateien aus
Plan, Layout und Assets vorhanden (Materialordner der Marke); Aufzeichnung vorhanden (Promptwerk); Länge (hart: Video 65–90 s
nach Zeichen je Sekunde der Stimme, weich: Zielfenster); `short_title`; EN-Plan strukturgleich zu DE (Beats, Typen, Datenschlüssel,
Quellen, Dateien, Zahlen im Layout).

**Belegprüfung für Zahlen:** Jede Zahl, Jahreszahl und Datumsangabe in Sprechtext, Titel, Beschreibung und Begleittext muss in den
Belegen der Aufgabe stehen (Kalenderansatz und -hinweise, Belegsätze, Quellentitel, Hook-Idee, Hinweis der Marken-Sitzung zum Thema,
bei Promptwerk die aufgezeichnete Sitzung; Ergebnisse aus `layout.computations` und `gb_calc` zählen mit). Ganze Zahlen bis 12
werden nicht geprüft, Schreibvarianten (Dezimalkomma oder -punkt, Tausenderpunkt) sind gleichwertig. Beim ersten Dewlane-Entwurf
fand das Verfahren das vom Modell ergänzte Datum „20. Juli 2020“, das in keinem Beleg stand. Das Verfahren erkennt keine frei
formulierten Behauptungen ohne Zahl; dafür bleiben Quellenliste, Marker (`unverified`) und die Durchsicht von Stefan.

**Gemeinsame Dateien:** `Redaktionsplan.csv` wird nur angehängt (Zeilenende und BOM bleiben). Der Marker im Konzeptplan wird über den
Text der Zeile gefunden, nicht über die Zeilennummer vom Laufbeginn; ist die Zeile inzwischen geändert, steht „nicht markiert“ im
Ergebnis. Jede Zeile behält ihr Zeilenende. Nichts wird gelöscht; Plan-, Render- und Export-Dateien bekommen eigene Namen
(`<marke>-<JJJJMMTT>-d<n>-<sprache>`, Fassung `D1`, `D2` …, nie eine vorhandene Datei überschreiben).

**Ein Lauf zugleich:** `data/daily/runner.lock` (Prozess und Startzeit; jede Protokollzeile erneuert die Änderungszeit). Ein zweiter Start
meldet „anderer Lauf aktiv“ und endet mit Exit 4. Eine Sperre gilt als Rest eines abgestürzten oder beendeten Laufs, wenn ihr
Prozess nicht mehr läuft oder seit 3 Stunden kein Lebenszeichen kam; dann übernimmt der nächste Start sie sofort.
Am Ende schreibt der Lauf „released“ in die Datei (nichts wird gelöscht).

**Kontingente:** Erreicht `claude -p` das Abo-Limit (`rate_limit_event` mit Status rejected oder blocked, Fehlerstatus 429 oder ein
Limit-Text), bricht der Lauf ab und startet keine weitere Marke. Die Flash-Zähler stehen in 2c.

**Risiko hoch** (Frontlore, Dewlane): kommt aus `risk_default` der Marke und endet im Prüfbericht immer in `HUMAN_REVIEW`; der
Tagesläufer exportiert diese Videos, ohne sie freizugeben.

**Zeitangaben:** Wien = Laptopzeit minus 1 h. Der Tagesläufer nutzt für Dateinamen und Ordner das Datum in Wien.
Das Datum im Ordnernamen ist das Produktionsdatum; den Veröffentlichungstermin legt Stefan fest (offener Punkt).

## 4. Betrieb

1. **Voraussetzungen:** Laptop wach und am Strom; Claude Code angemeldet (`claude auth status`); mindestens 30 GB frei auf C:;
   `data\render.pause` nicht vorhanden; in `.env` steht `GEMINI_API_KEY` (nur für die Stimmen; der Modellaufruf braucht keinen Schlüssel).
2. **Registrieren (Stefan):** in `automation\register_tasks.ps1` das `#` vor „FN Daily Runner“ entfernen und
   `.\automation\register_tasks.ps1 -WhatIf`, dann ohne `-WhatIf` aus einer PowerShell mit Stefans Konto ausführen. Start 06:30,
   Laufzeitgrenze 10 Stunden. Von Hand: `.\automation\run_daily.ps1 [-Brands engines,menswear] [-Topics 1] [-DryRun] [-Provider mock] [-Date 2026-11-04] [-MaxFlash 2] [-StartAt 2026-11-04T08:05:00Z]` (`-StartAt` wartet bis zu dieser UTC-Zeit, der Vergleich der Uhren übersteht einen Ruhezustand; während das Skript läuft, verhindert es den Leerlauf-Ruhezustand).
   Mit `-Provider mock` läuft die Vorlage ohne Modellaufruf und ohne Markierung (Probe der Aufgabe, kostenlos). Das Protokoll der Vorlage ist UTF-8.
3. **Ergebnis:** `data\daily\runs\<datum>_summary.md` (je Marke und Thema: Aufbau, Modellaufrufe und Token, Trockenlauf, Render,
   Prüfbericht, Überschneidung, Exportordner, Fehler), `data\daily\runs\<datum>_<marke>.log`, `logs\daily_<datum>.log`.
4. **Dauer (Schätzung aus den Prototypen):** je Thema etwa 3 Minuten Plan DE und EN, 1–2 Minuten je Trockenlauf, 4–6 Minuten je
   Render mit Stimme; also etwa 15–20 Minuten je Thema, bei 16 Themen vier bis fünf Stunden, wenn die Warteschlange frei ist.
5. **Kosten je Video:** `.venv\Scripts\python.exe scripts\daily_costs.py [--date JJJJ-MM-TT] [--brand <id>]`.
6. **Wiederholen:** Ein Thema mit Fehler bleibt unmarkiert und kommt am nächsten Tag wieder an die Reihe; Pläne und Protokoll
   bleiben liegen. Einzelne Marke oder Nummer: `--brands <id> --topic <Nr>`.
7. **Erster Echtlauf (Mittwoch 04.11.2026):** Stefan hat den Prototyp freigegeben, die Hauptsitzung hat das Go gegeben (03.11. abends) und
   `reserved_days` leeren lassen (keine Reel-Sitzung produziert mehr selbst). Ein Thema je Marke in DE und EN, Aufwand low, höchstens
   2 Flash-Anfragen je Marke, kein Pro, Render über die Warteschlange, Kennzeichnung „Tagesläufer“ im Redaktionsplan, Risiko hoch
   (Frontlore, Dewlane) als HUMAN_REVIEW. Start 10:05 Laptopzeit (= 09:05 Wien = 08:05 UTC, nach dem Quota-Reset der Stimmen um Mitternacht
   Pacific), als Hintergrundaufgabe der Tagesläufer-Sitzung:
   ```
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation\run_daily.ps1 -Brands all -Topics 1 -Date 2026-11-04 -MaxFlash 2 -StartAt 2026-11-04T08:05:00Z
   ```
   Protokoll `logs\daily_2026-11-04.log`, Ergebnis `data\daily\runs\2026-11-04_summary.md`, danach
   `.venv\Scripts\python.exe scripts\daily_costs.py --date 2026-11-04` (Token, Stimme, Renderzeit je Video). Vorab ohne Modellaufruf:
   `scripts\daily_runner.py --list-topics --date 2026-11-04 --topics 1` und `--dry-run --provider mock --topics 1 --no-mark`.
   Themen laut Liste vom 03.11., 20:00 Laptopzeit: Revlore Nr. 77 (Aufbau F), Suitwerk Nr. 1 Stoffgewicht (B), Scutoria Nr. 47 (A),
   Promptwerk Nr. 3 (B, Aufzeichnung hook-env; Stimme DE über `voice_tts.py --say Claude=Klohd` mit `--reuse-voice`), Gigastruct Nr. 3
   (B nicht gebaut, ersetzt durch A), Gritwerk Nr. 3 (A), Frontlore Nr. 24 (B), Dewlane Nr. 62 (A). Nach einem Abbruch (Kontingent, Absturz)
   übernimmt der nächste Start die Sperre sofort; derselbe Befehl nimmt nur Themen ohne Markierung. Vor dem Start erzeugt der Lauf den Monatsplan neu (6c), am 04.11. zusätzlich um 08:55 Wien. Der Lauf hängt am offenen Claude-Fenster
   und am wachen Laptop (ein zugeklappter Deckel schläft trotzdem).

## 5. Offene Punkte (03.11.2026)

- Tintora ist kein Teil des Tagesläufers (Abschnitt 1e, Punkt 3).
- Revlore: nur die Technik-Themen, die `brands/engines/aufbauten.yaml` mit Quellen nennt; für alle anderen braucht die Revlore-Sitzung ein Modell.
- Scutoria B–D, Gritwerk B/D/E, Gigastruct B–D und Suitwerk E sind nicht gebaut; der Tagesläufer ersetzt sie und vermerkt es.
- Promptwerk: nur Themen mit vorhandener Aufzeichnung (12); der Tagesläufer nimmt nichts auf.
- Reservierungen: `reserved_days` ist leer (Hauptsitzung, 03.11. abends: keine Reel-Sitzung produziert mehr selbst); der Tagesläufer nimmt je Marke das erste freie Thema in der Reihenfolge des Konzeptplans.
- Datum im Ordnernamen (Produktions- statt Veröffentlichungsdatum) und die Verteilung auf die Slots 12:00/14:00/18:00 plant die Hauptsitzung.
- Layout-Feinheiten sieht nur ein Mensch (Beispiel: „höchstens 16,25 µm“ bricht im Suitwerk-Prototyp bei 30 s um); der
  Tagesläufer prüft Überdeckungen und Textgrößen, aber nicht jede Zeilenumbruchstelle.
- Quelleninhalt: Der Tagesläufer liest die Quellseiten nicht selbst; er verlässt sich auf die geprüften Belegsätze der Marken-Sitzungen.
  Ein Seitenleser (Abruf, Textauszug je Quelle) würde die Belegprüfung stärken und kostet Eingabe-Token.

## 6. Monatsplan und Monatsplaner (Auftrag der Hauptsitzung nach Stefans Vorgabe vom 03.11.2026, 20:45)

**Vorgabe:** Für November je Marke täglich 2 Themen auf Deutsch und Englisch (4 Videos), 7 Tage die Woche; danach automatisch eine Monats- und
Themenplanung eine Woche vor dem nächsten Monat. Der Lauf am 04.11. (1 Thema je Marke) bleibt davon unberührt.

### 6a. Was der Plan ist

Der Plan **simuliert die Themenwahl des Tagesläufers** Tag für Tag auf einer Kopie des Zustands (`src/fn/daily/monthplan.py`, ruft
`DailyRunner.select_topics` mit `--provider mock`, kein Modellaufruf, nichts Gemeinsames wird geschrieben). Es gelten also dieselben Regeln wie im
Betrieb: Reihenfolge des Konzeptplans (zuerst die Tagestabellen, dann die Vorschlagstabelle), nur Themen mit geprüfter Quelle (Kalender, Research-Datei
oder Quelle je Thema in `brands/<id>/aufbauten.yaml`), nur gebaute Bildaufbauten (ein nicht gebauter wird ersetzt und vermerkt), Wechsel des Bildaufbaus
zwischen den Themen eines Tages und von Tag zu Tag, Marken-Grenzen (Revlore: Technik zuerst, Motor höchstens jedes dritte Thema; Promptwerk: nur mit
Aufzeichnung), ohne schon produzierte Themen (Zustand, Konzeptplan-Marker, Redaktionsplan-Zeilen auch nach Titel, `--assume` für den Lauf am 04.11.).
Themen ohne Quelle erscheinen als „Quelle fehlt“, Themen ohne tragenden Aufbau oder ohne Aufzeichnung als „braucht Modell, Aufbau oder Aufzeichnung“;
ein Platz ohne Thema bleibt „offen“. Der Plan erfindet keine Themen.

| Datei | Inhalt |
|---|---|
| `04 Redaktionsplan\Monatsplan <Marke> <JJJJ-MM>.md` | Tabelle je Marke: Datum, Nr. und Titel, Bildaufbau (mit Konzeptplan-Buchstabe bei Ersatz), Quelle, Slot DE, Slot EN, Plattformen, Status; darunter „Ohne Quelle“, „Braucht Modell“, „Nicht geeignet“, Annahmen |
| `04 Redaktionsplan\Monatsplan <JJJJ-MM> Übersicht.md` | Regeln, Zahlen je Marke, Lücken; zwischen `<!-- MANUELL:BEGIN -->` und `<!-- MANUELL:END -->` die von Hand geführten Abschnitte (Tintora, Scutoria YouTube, Hinweise), die eine Neuerzeugung behält |
| `data/calendars/<id>_<JJJJ-MM>.plan.json` | Plan im Schema von `fn.calendar.TopicRow` (`fn.cli calendar check` liest ihn) plus `nr`, `slot_index`, `slot`, `aufbau`, `aufbau_planned`, `aufbau_note`, `calendar_ref`, `plan_status` (`geplant` oder `offen`), `reihe`, `recording`, `plattformen`; ids `<id>-<JJJJMMTT>-<Platz>-<Sprache>` wie bei `calendar init` |
| `data/daily/month_plan_<JJJJ-MM>_report.md` | Meldung (Zahlen je Marke); eine Kopie geht in `month_plan.report_dir` aus `config/daily.yaml`, wenn der Ordner existiert |
| `04 Redaktionsplan\Themenvorschläge <Marke> <JJJJ-MM>.md` | nur mit `--propose`: Ideen für offene Plätze, „Vorschlag, Quelle prüfen“, nicht eingeplant |
| `04 Redaktionsplan\Frühere Fassungen\` | ältere Fassungen überschriebener Dateien (nichts wird gelöscht; ein neuer Zeitstempel allein erzeugt keine neue Fassung) |

**Warum `.plan.json` und nicht `<id>_2026-11.json`:** Die vorhandenen Kalender `data/calendars/<id>_2026-11.json` (09.11. bis 06.12., 3 Themen je Tag) enthalten
die geprüften Quellen der Marken-Sitzungen und die Ids der produzierten Videos; Markenwerkzeuge lesen sie direkt (`brands/ai_security/run_specs.py`,
`megaconstruction/tools/plan_builder.py`, `brainrot/renderer/produce_week.py`). Ein Überschreiben würde Quellen und Zuordnungen vernichten. Der Tagesläufer
liest die Plandatei, `_calendar` in `context.py` überspringt sie. Soll der Plan die alten Kalender ersetzen: alte Datei nach `data/calendars/archiv`, Plandatei
umbenennen; dabei die Markenwerkzeuge prüfen.

**Slots (von Stefan am 03.11.2026 bestätigt, Wien):** Thema 1 DE 12:00, EN 15:00; Thema 2 DE 18:00, EN 21:00. Sie stehen in `config/brands.yaml` unter
`defaults.slots_by_language` (und `topics_per_day: 2`); der Plan liest sie von dort, `fn.cli calendar init` ebenso. Der Test `test_calendar_grid_and_validation`
folgt jetzt der Konfiguration statt der alten 6 Slots (3 DE: 12:00, 14:00, 18:00; 3 EN: 15:00, 20:00, 23:00).

### 6b. Aufruf

```
.venv\Scripts\python.exe scripts\month_planner.py --month 2026-11 --from 2026-11-05 --assume 2026-11-04:1   # November (so entstanden)
.venv\Scripts\python.exe scripts\month_planner.py --month 2026-12 --dry-run                               # nur Zahlen, nichts schreiben
.venv\Scripts\python.exe scripts\month_planner.py --brands menswear --from 2026-11-12                      # ab einem späteren Tag neu planen: frühere Tage bleiben
.venv\Scripts\python.exe scripts\month_planner.py                                                         # Folgemonat (was die Monatsaufgabe tut)
```

Schalter: `--month`, `--from`, `--to`, `--assume TAG[:N]` (Themen, die vor dem Plan produziert werden, aber noch nicht im Zustand stehen), `--brands`,
`--per-day`, `--dry-run`, `--propose`, `--max-proposals N` (Standard 20), `--provider claude_cli|mock`. Ein Folgemonatsplan nimmt Themen des Vormonatsplans für die Tage
zwischen heute und seinem Start als vergeben. Neu planen immer ab morgen (`--from`), weil der Zustand die schon produzierten Themen kennt, nicht die Tage davor. Übersicht und Meldung schreibt der Planer nur, wenn er alle Marken geplant hat; ein Lauf mit `--brands` einer Marke ändert nur deren Plan- und Markdown-Datei.

### 6c. Wie der Tagesläufer den Plan liest

Ab dem ersten Plantag liest `DailyRunner.select_topics` die Plandatei des Tages (`plan_for_day`): die geplanten Themen kommen zuerst, in der Reihenfolge der Plätze, mit
dem geplanten Bildaufbau; danach folgt die bisherige Reihenfolge. Besteht ein geplantes Thema eine Prüfung nicht (keine Quelle mehr, schon produziert, Aufbau nicht mehr
gebaut), rückt das nächste freie nach (Rückfall auf die bisherige Wahl). Ohne Plandatei oder ohne Eintrag für den Tag ändert sich nichts; jeder Fehler beim Lesen führt
zur bisherigen Wahl. `--no-plan` schaltet das Lesen aus, `--topic <Nr>` ebenfalls. Takt: `topics_per_day: 2` in `config/daily.yaml` (Standard), Kennzeichnung im Redaktionsplan
„Tagesläufer“ wie bisher. Probelauf: `scripts\daily_runner.py --dry-run --provider mock --no-mark --date 2026-11-05` (alle Marken, Plätze des 05.11. aus dem Plan, kein Render, kein Modellaufruf).

**Vor jedem Tageslauf wird der Plan neu erzeugt** (Hauptsitzung, 04.11.2026, damit der Lauf die neuesten Bildaufbauten, Quellen, Aufzeichnungen und
Revlore-Themen der Marken-Sitzungen sieht; die Marken-Sitzungen erzeugen den Plan nicht selbst): `scripts\daily_runner.py` startet zu Beginn jedes echten Laufs
`scripts\month_planner.py` für alle Marken (Argumente aus `monthplan.replan_args`). Deckt der Plan den Lauftag ab, wird ab diesem Tag neu geplant (der Lauf liest dann
frische Zeilen für heute); sonst, am 04.11., ab dem Folgetag mit den Themen dieses Laufs als vergeben (`--assume`). Der Planer scheitert nie auf Kosten des Laufs: Bei Fehler oder
Zeitüberschreitung (900 s) folgt der Lauf dem letzten Plan. `--no-replan` schaltet das aus, `--replan` erzwingt es auch bei `--dry-run`, `--list-topics` plant nie neu.
Am 04.11. lief der Planer zusätzlich um 08:55 Wien (09:55 Laptopzeit), vor dem Lauf um 09:05 Wien.

**Halb fertige Dateien der Marken-Sitzungen:** Ist eine `brands/<id>/aufbauten.yaml` beim Lesen ungültig (die Sitzung schreibt gerade), nutzen Planer und Lauf den letzten gültigen
Stand (`data/daily/aufbauten_ok/<id>.yaml`, bei jedem erfolgreichen Lesen aktualisiert) und planen oder produzieren die Marke damit. Das wird einmal gemeldet: Protokoll, Übersicht
unter „Hinweise zum Neuerzeugen“, Meldung des Planers, „Hinweis:“ in der Zusammenfassung des Laufs. Gibt es noch keinen gültigen Stand, gelten die Bildaufbauten aus `config/daily.yaml`.

**Tagesgrenze:** Ein zweiter Lauf am selben Tag erzeugt je Marke nie mehr Themen als das Tagesziel (`topics_per_day`, am 04.11. 1): Die schon produzierten Themen des Tages
(Zustand `data/daily/state.json`) werden abgezogen. Mit `--topic <Nr>` entfällt die Grenze.

### 6d. Themenvorschläge für Lücken (`--propose`, nur auf Anweisung oder in der Monatsaufgabe)

Für jede Marke mit offenen Plätzen fragt `src/fn/daily/proposals.py` einmal `claude -p` (Sonnet, effort low, Abo, kein Einzelpreis, Token im Kostenlog unter `monthplan-<Monat>-<Marke>`)
nach bis zu 20 Themen: Format-Bibel-Auszug, Muster aus dem Konzeptplan, vorhandene Titel (keine Wiederholung), gebaute Bildaufbauten. Jeder Vorschlag trägt Reihe, Hook,
Bildaufbau, Risiko und die Quellen, die das Modell nennt (URL nur, wenn es sie sicher kennt, sonst Institution und Suchhinweis); die URLs werden per HTTP auf Erreichbarkeit geprüft.
Die Datei `Themenvorschläge <Marke> <JJJJ-MM>.md` kennzeichnet alles als **„Vorschlag, Quelle prüfen“, nicht einplanbar bis geprüft**. Nichts davon geht in einen Konzeptplan,
einen Kalender oder den Redaktionsplan; ein Thema wird erst einplanbar, wenn eine Marken-Sitzung (oder Stefan) die Quelle geprüft und es mit Quelle, Bildaufbau und Risiko im
Konzeptplan eingetragen hat. Der November-Plan wurde ohne Vorschläge erzeugt: Die Hauptsitzung entscheidet zuerst, weil mehrere Marken weniger als 52 Themen tragen.

### 6e. Monatsaufgabe

`automation\run_month_plan.ps1` (Vorlage, **nicht registriert**; auskommentierter Eintrag „FN Month Plan“ in `register_tasks.ps1`, Stefan registriert). Regel: am 24. jedes Monats
um 19:30 Wien plant sie den Folgemonat wie in 6a (mit Vorschlägen für offene Plätze, `-NoPropose` schaltet sie aus), schreibt Monatsplan-Dateien, Übersicht, Plandateien und die
Meldung (6a). Weil Windows PowerShell 5.1 keinen Monatsauslöser kennt, feuert die Aufgabe täglich um 18:00 Laptopzeit (vor 19:30 Wien im Sommer wie im Winter); das Skript handelt nur,
wenn das Wiener Datum der 24. ist, wartet bis 19:30 Wien und hält den Laptop wach. `-Force` (sofort, ohne Wartezeit), `-Month`, `-DryRun`. Protokoll `logs\month_plan_<datum>.log` (UTF-8).
Die „Meldung an die Hauptsitzung“ ist eine Datei (6a), kein Nachrichtenversand: Eine geplante Aufgabe kann keiner Sitzung schreiben.

### 6f. Grenzen

- Die von Hand geführten Abschnitte der Übersicht (Tintora: eigener Renderer, Kling-Credits, Pro-Limit der Stimmen; Scutoria YouTube: markenlokaler Composer) liefern die Sitzungen dieser Marken; die Monatsaufgabe übernimmt sie nur unverändert.
- Der Plan folgt dem Konzeptplan und den Aufbauten-Dateien von heute. Ändern die Marken-Sitzungen sie, den Plan ab morgen neu erzeugen (6b).
- Nur ein gebauter Aufbau: Beide Themen eines Tages bekommen denselben Bildaufbau (Gigastruct); die Übersicht nennt die Zahl der Ersatz-Bildaufbauten und der Tage mit gleichem Aufbau.
- Der Plan sagt nichts über Rechenzeit und Kontingent: Die Schätzung für 8 Marken mit je 2 Themen steht in Abschnitt 4, Punkt 4 (vier bis fünf Stunden); gemessen wird zum ersten Mal am 04.11. (8 Themen), das Wochenkontingent von `claude -p` ist noch nicht belastbar bekannt.
