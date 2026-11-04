# Vorlage Suitwerk – Version 0.9 (nur Claude Code)

Stand: 30.10.2026 (Wien), ergänzt am 30.10.2026 23:30 um die Qualitätsrunde Q1 (Abschnitt „Qualitätsrunde Q1“). Entwurf zur Freigabe durch Stefan; Version 1.0 erst nach seiner Abnahme. Mit dieser Datei kann jede Sitzung Suitwerk-Videos nur mit Claude Code und dem lokalen Renderer reproduzieren, ohne Higgsfield und ohne KI-Bilder. Verweis in `C:\Automation\faceless-network\config\brands.yaml` (`menswear`, `brand_version: "0.9"`, `template_doc`).

## Idee in einem Satz

Quiet Luxury, zeitlos: ein Sakko als saubere goldene Linienillustration auf Mitternachtsblau ist in jeder Szene der Gegenstand, an dem erklärt wird. Keine Menschen, keine Fotos, keine Folien.

## Bausteine

| Baustein | Ort |
|---|---|
| Marke (Palette, Schriften, Logo, `flat`) | `C:\Automation\faceless-network\brands\menswear\brand.yaml` |
| Sakko-Zeichnung (Geometrie, Varianten, Zustände) | `brands\menswear\tools\garment.py` |
| Fünf Suitwerk-Szenentypen | `brands\menswear\scenes.py` (Markenmodul nach `docs\direction-system.md` Abschnitt 6d: `TEMPLATES`, `HOOK_SCENE_TYPES`) |
| Atelier-Hintergrund unter allen Szenen (seit Q1) | `brands\menswear\scenes.py`, Funktion `LAYER` (Markenebene nach Abschnitt 6d), nur Code |
| Render-Aufruf | `scripts\render_direction.py` (gemeinsam, unverändert) |
| Produktionsordner | `brands\menswear\tools\export_suitwerk.py` (mit Kennzeichnung von Entwürfen über `--draft`); Abschlusssatz für das gemeinsame Exportskript steht in `brand.yaml` unter `production.closing_sentence` |
| Logo (Vorschlag) | `brands\menswear\assets\logo\suitwerk-mark.svg` (zwei Revers, die sich am Knopf treffen; eigene Zeichnung) |
| Regie-System | `docs\direction-system.md` (Hook-Engine, Story-Engine, Prüfungen) |
| Beispielplan | `data\direction\menswear-20261105-1-de.json` |
| Themenkalender | `data\calendars\menswear_2026-11.json` (30 Themen ab 05.11.2026, je DE und EN am selben Tag, mit Quellen und Vorsichtshinweisen in `notes`) |

Der gemeinsame Renderer (`src\fn\`) ist unverändert. Die Suitwerk-Szenen sind eigene Typen mit Markenpräfix (`suitwerk_hook`, `suitwerk_fitting`, `suitwerk_ladder`, `suitwerk_compare`, `suitwerk_takeaway`), je eine Entsprechung zu den fünf gemeinsamen Typen; die gemeinsamen Typen bleiben unverändert. Der Hook-Beat nutzt `suitwerk_hook`.

## Gestaltung

| Rolle | Wert | Begründung |
|---|---|---|
| Grund | `#172337` Mitternachtsblau, feine 45°-Köperlinien (`fabric-gradient`) | aus `brands.yaml`; die Linien wirken wie Stoff, nicht wie Raster |
| Fläche | `#273245`, Sakko-Tuch `#26344D` mit Köpermuster | Sakko eine Stufe heller als der Grund |
| Akzent | `#D4B483` Champagnergold: Konturen, Hervorhebung, Fortschritt | aus `brands.yaml` |
| Text | `#F2EEE6` | aus `brands.yaml` |
| Gedämpft | `#9AA0A8` statt `#8F9397` | etwas mehr Kontrast für Unterzeilen (ca. 6:1 statt 5,2:1 auf dem Grund, eigene Rechnung) |
| Fehlerzustand | `#C9776B` gedämpftes Ziegelrot, nur für Risiko: Zugfalten, „nie", Marker „Lücke" | keine grelle Warnfarbe |
| Offen | `#E8A33D` Bernstein (seit 30.10.2026 `signal_amber`, vorher gleich dem Gold): „nach Geschmack", Zustand unklar, Marker „Unsicher" | muss sich vom Gold der Fakten unterscheiden |
| Erreicht | `#8DBE96` Salbeigrün, nur für den erreichten Zustand (Ring am Schluss) | |
| Auslegung | `#A58BE0` Violett, nur für den Marker „Auslegung" | |
| Überschriften | Playfair Display 600 (SIL OFL 1.1, Datei und Lizenz in `assets\fonts\playfairdisplay`) | Serifenschrift, ruhig, ab 46 px gut lesbar |
| Text, Untertitel | Inter 400–600, Untertitel 56 px (SIL OFL 1.1) | |
| Logo | Revers-Zeichen 40 px plus Wortzeichen SUITWERK in Versalien, Laufweite 0,18 em, oben links ab dem ersten Bild | klein, kein Logo-Intro |
| Bewegung | Tempo `slow`, `flat: true`: kein Glow, kein Lichtverlauf, Kamera höchstens 3–7 % | Ruhe statt Effekt |

Das Sakko kennt vier Schnitte (`sb1`, `sb2`, `sb3` Einreiher mit 1–3 Knöpfen und fallendem Revers, `db6` Zweireiher mit steigendem Revers) und Zustände (`fastened`: geschlossene Knöpfe). Die Vorderkanten bleiben bis zum untersten geschlossenen Knopf zusammen und öffnen sich darunter; ein geschlossener unterer Knopf am Einreiher zeichnet Zugfalten. Benannte Punkte für Ringe, Zoom und Beschriftung: `button:N`, `lapel`, `notch`, `collar`, `pocket`, `chest`, `hem`, `shoulder`, `quarters`, `break`, `sleeve`, `waist`. Für spätere Themen (Revers, Taschen, Schlitze, Hose, Schuhe) wird `garment.py` um weitere Teile erweitert; die Szenen bleiben gleich.

## Fünf Szenentypen im Suitwerk-Look

| Szenentyp | Suitwerk-Layout | wichtigste Daten |
|---|---|---|
| `suitwerk_hook` (zu `cinematic_hook`) | große Frage (64 px) oben, Sakko zeichnet sich in 1,5 s, Ring und „?" am Detail, langsamer Push zum Detail | `question` (≤ 56), `variant`, `fastened`, `target`, `badge`, `question_at`, `badge_at` |
| `suitwerk_fitting` („Anprobe", zu `ui_demo`) | Nadel fährt zum Detail, Zoom 1,5–1,6× in einem Fenster bis y 1100, Zustand wechselt (z. B. Knopf geht zu, Zugfalten zeichnen sich), Karte mit Befund unten im Fenster | `headline` (≤ 44), `from_fastened`, `to_fastened`, `target`, `pointer_at`, `zoom_at`, `flip_at`, `label` (≤ 30), `label_at` |
| `suitwerk_ladder` („Regel-Leiter", zu `data_flow`) | Sakko links, je Knopf eine Leitlinie zu einer Regel rechts; zweite Stufe mit anderem Schnitt möglich | `headline`, `stages[{variant, fastened, at, tags[{button, text ≤ 18, sub, tone: always (Gold)/sometimes (Bernstein)/never (Rot), at}]}]` |
| `suitwerk_compare` (zu `comparison`) | zwei Sakkos (440 px) nebeneinander bei x 290 und 750, Titel darüber, Befund darunter (höchstens 340 px breit), Haarlinie in der Mitte | `left/right{title ≤ 18, variant, fastened, target, tag ≤ 26}`, `left_at`, `left_tag_at`, `right_at`, `right_tag_at` |
| `suitwerk_takeaway` (zu `key_takeaway`) | drei Karten mit Mini-Sakko im jeweiligen Zustand; `mode: closing` = der Fehler wird am Sakko behoben (Zugfalten weg, Ring am richtigen Detail), Aussage und Zeile „Suitwerk · Blick fürs Detail" | `items[{title ≤ 26, sub ≤ 40, variant, fastened, at}]`; closing: `from_fastened`, `to_fastened`, `target`, `statement` ≤ 40, `chip` ≤ 40 |

Längenüberschreitungen landen als `readability_text_limits` (fail) im Prüfbericht. Alle Zeitfelder (`*_at`, `at`) nehmen Sekunden ab Beatbeginn oder einen Wortanker `"w:Wort"` bzw. `"w:Wort#2"`; ein Anker, der im Beat nicht gesprochen wird, bricht den Lauf mit Meldung ab.

## Regeln

- Kein Logo-Intro, keine Endkarte; Abschluss in der Handlung (`suitwerk_takeaway` mit `mode: closing`).
- Ein Objekt als roter Faden: das Sakko, dazu die Statusleiste (`layout.status_bar`, Bezeichnung „Sakko, …", ein Zustand je Beat; `amber` erscheint in Bernstein, `red` im Ziegelrot, `green` im Salbeigrün für den erreichten Zustand; `green` setzt das Markenmodul über `LAYER`, der gemeinsame Renderer bleibt unverändert).
- Bildmitte gefüllt: Sakko 440–560 px breit in der Zone y 290–1100, rechts bleibt x ab 930 frei; Untertitel in Sinngruppen (`caption_mode: phrases`, höchstens 4 Wörter), unten bei y ≈ 1380.
- Keine Markennamen als Empfehlung, keine Affiliate-Links, keine Produktversprechen, kein Body-Shaming. Hersteller- und Händlerseiten nur als Quelle für Fakten.
- Stilregeln sind Konventionen: „gilt als", „üblicherweise", Ausnahmen nennen. Herkunftslegenden (z. B. Edward VII.) nur als Legende oder gar nicht.
- Jede Aussage mit Quelle (URL, Abrufdatum) im Plan; Unbelegtes in `unverified`, nicht ins Video. Quellen stehen in `post.json` und `Veröffentlichung.md` und seit Fassung V2 als Quellenleiste im Bild (siehe Erklärschicht).
- Anrede „du". Gesprochener Abschluss: „… Mehr Blick fürs Detail: Folge Suitwerk." (Vorschlag)
- Länge 65–90 s, Ziel 70–80 s; Stimme Gemini `Orus` (`gemini-2.5-flash-preview-tts`).
- Messwerte dieser Stimme vom 30.10.2026, inklusive Satzpausen:

  | Fassung | Wörter | Sprache | Wörter je Sekunde | Video |
  |---|---|---|---|---|
  | V2 | 151 | 53,4 s | 2,83 | 56,4 s, zu kurz |
  | V3 | 202 | 74,6 s | 2,71 | 77,6 s |

  Faustregel: Für 70–80 s Video braucht es 185–210 Wörter, das Video ist etwa 3 s länger als die Sprache.
- `speaking_rate` in `audio_style.yaml` wirkt bei Gemini nicht. Der Wert 1,33 stellt nur die Ersatzstimme des Trockenlaufs (`--tts mock`) auf das Gemini-Tempo ein, damit die Längenprüfung schon vor der Vertonung stimmt. Das Tempo lässt sich bei Gemini nur über `style_instruction` beeinflussen.
- Die Statusleiste nimmt keine Wortanker. Nach der Vertonung ihre `offset` aus `captions.json` setzen und mit `--reuse-voice` ohne neue Kosten neu rendern.

## Erklärschicht

Seit 30.10.2026 gilt die gemeinsame Vorlage `02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`. Der Renderer setzt sie als Erklärschicht um (`src\fn\render\explainer.py`). Suitwerk schaltet sie in `brands\menswear\brand.yaml` ein, im Block `explainer`.

| Feld | Suitwerk |
|---|---|
| Stimmhinweis oben rechts | „SYNTHETISCHE STIMME“ / „SYNTHETIC VOICE“ |
| Einstiegszeile 0–3,5 s | „Synthetische Stimme · Quellen am Bildschirm · Stilregeln sind Konvention“ (EN „… · Style rules are convention“) |
| `source_y` | 1120: Die Szenen enden bei y 1100, die Quelle reicht bis etwa 1240, die Untertitel beginnen bei etwa 1310, die Statusleiste bei 1440. Rechts bleibt x ab 930 frei. |
| Fakt | Quadrat in Gold `#D4B483`, der aktiven Farbe der Sakkolinie |
| Auslegung | violette Raute `#A58BE0` |
| Unsicher | bernsteinfarbener Halbkreis `#E8A33D` |
| Lücke | roter gestrichelter Kreis `#C9776B` |
| Beispielwert | grauer Rahmen `#9AA0A8` |
| Erreicht | Grün `#8DBE96`, nur in den Suitwerk-Szenen (Ring am Schluss), nicht im Renderer |

Marker je Aussage:
- **Fakt mit Quelle**: wenn eine Schneider- oder Stilquelle die Regel oder ihren Grund beschreibt, z. B. „gilt als Fehler“, „zieht über der Hüfte“, die Faustregel und die Ausnahmen. Dass es eine Konvention ist, sagt der Sprechtext („gilt als“, „Faustregel“, „meist“).
- **Auslegung**: unsere Zusammenfassung oder Empfehlung, z. B. die Karten „Kurz gesagt“. Dann steht nur der Marker, keine Quellenleiste.
- **Unsicher**: wenn Quellen sich widersprechen, z. B. ob der obere von drei Knöpfen zu ist.
- **Lücke**: wenn ein Teil unbelegt bleibt.
- **Keiner**: Hook und Abschluss ohne Aussage. Der Abschluss hat auch keinen Kopf (`head: false`).
- **Beispielwert-Chip**: nur bei erfundenen Zahlen, im Testvideo keiner.

Plan je Beat (`beats[].overlay`):
- `marker` mit `marker_at` als Wortanker. Der Kicker kommt automatisch, z. B. „2 · DAS PROBLEM“; der Szenentitel bleibt der Kopftitel.
- `transition`:
  - Kreisübergang (`iris`) aus einem Detail des Sakkos in die nächste Szene, z. B. aus dem Ring am unteren Knopf in die Anprobe;
  - Überblendung (`blende`, 0,7 s) zwischen ruhigen Vergleichen;
  - sonst harter Schnitt.
- `vignette: true` bei der Nahaufnahme (Anprobe).
- `sources[].label`: kurz („King & Allen, Journal“, „Gentleman's Gazette“, „The Art of Manliness“), damit die Leiste höchstens zwei Zeilen hat.

Suitwerk-Szenen für die Erklärschicht (`brands\menswear\scenes.py`):
- Alle Zeiten nehmen Wortanker. Jede Bildaktion hängt an einem gesprochenen Wort.
- `hold_end: true` auf der Szene vor einem Übergang: Sie bleibt stehen, bis die nächste Szene sie überdeckt.
- `backdrop: true` auf der Szene nach einem Übergang: Ein Stoffgrund deckt die alte Szene ab und geht nach dem Übergang weg.
- Eigene Marker gibt es in den Szenen nicht. Die Farben der Etiketten folgen der festen Bedeutung: immer = Gold, nach Geschmack = Bernstein, nie = Rot.

Storyboard je Video in `05 Produktion\<Ordner>\01 Skript\Storyboard.md`, Spalten: Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild.

## Qualitätsrunde Q1 (30./31.10.2026)

Grundlage: `02 Marke\Qualitätsrunde 2026-10-31.md` (Scutoria-Niveau, Ziel Note 1,7). Umgesetzt nur in den Markendateien (`brands\menswear\scenes.py`, `tools\garment.py`, Plan); gemeinsamer Code unverändert.

| Pflicht | Suitwerk Q1 |
|---|---|
| Hintergrund mit Tiefe | Atelier aus Code (`LAYER`): Lichtkegel von oben (weich), warmer Lichtfleck, Stoffstruktur mit Körperlinien und feinem Rauschen, Schnittmusterpapier mit Raster, Vorderteil und Ärmel als Schnittteile mit Nahtzugabe und Fadenlauf, Kreidezeichen, Maßband unten; langsame Parallaxe über das ganze Video, dunkler Rand. `backdrop` der Szenen ist eine Kopie dieses Grunds zur selben Zeit, damit Übergänge nahtlos sind. |
| Hauptmotiv groß | Sakko 590–640 px (vorher 440–560), Licht von oben links (Verlauf im Tuch) und Schlagschatten. Hook: Sakko plus Detail-Lupe (Radius 172 px, 2,4-fach) auf dem unteren Knopf, zusammen etwa 90 % der Inhaltsbreite. Vergleich: zwei Sakkos zu 470 px. Karten 218 px hoch mit Nummer. |
| Leitobjekt und Statusleiste | Sakko in jeder Szene; Statusleiste wechselt am Wort (Sekunden aus der Gemini-Stimme), Schluss in Grün. |
| Bewegung an Wörtern | 61 Bildereignisse in 77,6 s; je Szene Push-in 3–4 % (Anprobe: Zoom). Neue Ereignisse: Lupe, Schnittlinie (`garment.front_edge`), Ringpulse an Knöpfen, Pfeile für Taille, Hüfte und Zug, gestrichelte Soll-Linie, englische Merkwörter an den Etiketten, Stufentitel „Zwei Knöpfe“/„Drei Knöpfe“, Kartenwechsel mit Zustandswechsel am kleinen Sakko. |
| Typografie | Szenentitel 68 px, Frage 72 px, Aussage 74 px, Etiketten 38 px, kleinste Beschriftung 28 px; Playfair Display und Inter. |
| Erklärschicht ohne Überdeckung | `overlap_check.mjs` ohne Befund; Befundkarte der Anprobe oben im Bild, damit sie die Zugpfeile nicht verdeckt. |

Neue Plan-Felder (alle mit Wortankern): Hook `loupe_at`, `nie_at`, `cut_at`, `jacket_x`; Anprobe `all_at`, `error_at`, `pull_at`, `tense_at`, `ghost_at`; Vergleich je Seite `shapes[{kind: waist|hips|pull|cut, at}]`, `pulses[{target, at, tone}]`, `strain`, `tag2` (Bernstein, ≤ 34 Zeichen) mit `tag2_at`; Leiter je Stufe `title`, `focus_at`, je Etikett `en` und `en_at`; Karten je Eintrag `ring`, `ring_at`, `then_fastened`, `then_at`; Abschluss `ring_at`.

Prüfbericht: Hinweis `visual_cuts_rhythm` (Median 1,0 s statt 1,2–8,0 s) ist eine Warnung, kein Fehler; die Ereignisse liegen dicht, weil jede Szene mehrere Wortanker hat.

## Ablauf je Video

1. Plan `data\direction\menswear-<datum>-<n>-de.json` aus dem Beispielplan ableiten (Thema aus dem Kalender, Quellen gegenlesen, fünf Hook-Kandidaten), mit `overlay` je Beat, `label` je Quelle und Wortankern; Storyboard in `01 Skript\Storyboard.md`.
2. Trockenlauf ohne Kosten (Lint, Layout, Textlimits, Regie-Prüfungen):
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version dry --tts mock --no-render`
   Standbilder zur Sichtprüfung: im Ordner `storage\direction\<id>-dry\project` `npx hyperframes snapshot . --at 3,17,31 -o <absoluter Pfad>`.
3. Sperrdatei `data\render.lock` prüfen und anlegen, freien Speicher prüfen (mindestens 30 GB), dann eine Vertonung und Render:
   `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<id>.json --version V1 --tts gemini --mirror suitwerk-regie\<datum>`
   Korrekturen ohne neue Kosten: `--reuse-voice storage\direction\voice_<id>_V1_gemini.wav`. Sperrdatei danach entfernen.
   Bei Gemini-Fehler 429 nicht ausweichen, sondern warten; Vertonung offen vermerken. Keine Windows-Stimme. (Regel von Stefan, 30.10.2026; bis dahin nur Trockenlauf mit `--tts mock --no-render`.)
4. Produktionsordner: `.venv\Scripts\python.exe brands\menswear\tools\export_suitwerk.py data\direction\<id>.json --version <Fassung> --short "<Kurztitel>"`, nur mit Gemini-Stimme.
5. Zeile in `04 Redaktionsplan\Redaktionsplan.csv`; nichts veröffentlichen.

## Testvideo (30.10.2026)

| | |
|---|---|
| Thema | Der untere Sakkoknopf bleibt offen. Mit Absicht. (Kalender Tag 1, 05.11.2026 12:00) |
| Hook | H1 Frage: „Warum hat ein Sakko einen Knopf, den man nie schließt?" (Bildschirm „Ein Knopf, den man nie schließt?"); vier weitere Kandidaten im Plan |
| Ablauf | Hook (Sakko zeichnet sich) → Anprobe (unterer Knopf geht zu, Zugfalten) → Vergleich offen/zu → Regel-Leiter für 2 und 3 Knöpfe → Ausnahmen Einknopf/Zweireiher → drei Karten → Abschluss: der Knopf wird wieder geöffnet |
| Quellen | King & Allen (Maßschneiderei London), Gentleman's Gazette (Sven Raphael Schneider), The Art of Manliness; abgerufen 30.10.2026 |
| Stand | Fassung Q1 (Qualitätsrunde, 30.10.2026 23:27): 77,6 s, Gemini `Orus` aus V3 wiederverwendet (202 Wörter, 74,6 s Sprache), Prüfbericht VALIDATED, Überschneidungs-Prüfung ohne Befund, eigene Note 2,0. Export: `05 Produktion\Suitwerk\2026-11\2026-11-05 Unterer Sakkoknopf\04 Export\2026-11-05 Unterer Sakkoknopf – 9x16.mp4`. Vorstufen V2 (zu kurz) und V3 (77,6 s, VALIDATED, nicht exportiert). Die frühere Exportdatei mit Windows-Stimme (V1, 80,8 s) liegt in `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-30 Layout-Umstellung`. |
| Standbilder | Kontaktbogen Q1: `05 Produktion\_Demos\suitwerk-regie\2026-11-05-q1\kontakt.jpg`; ältere Trockenlauf-Standbilder in `05 Produktion\_Demos\suitwerk-regie\2026-11-05-v2dry-standbilder\` |
| Dateien | `05 Produktion\Suitwerk\2026-11\2026-11-05 Unterer Sakkoknopf\`, Fassungen `05 Produktion\_Demos\suitwerk-regie\` |

## Offen (für Stefan oder die Hauptsitzung)

- Ton `green` in der Statusleiste: seit Q1 im Markenmodul gelöst (CSS über `LAYER`); kein Wunsch an den Renderer mehr. Offen bleibt der Wunsch, `offset` der Statusleiste als Wortanker anzugeben (jetzt Sekunden aus `captions.json`).
- Freigabe der Optik, des Logo-Vorschlags und des Abschlusssatzes; dann `brand_version` 1.0.
- Musik: weiterhin keine lizenzierte Quelle (`audio_style.yaml` `music.file` leer).
- Englische Fassung: gleiche Vorlage, eigene Vertonung (Freigabe nötig).
