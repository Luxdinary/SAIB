# Suitwerk-Pläne schreiben (Woche 1 ab 09.11.2026)

Muster: `brands\menswear\plans\a01_weste.py` (fertig, geprüft). Je Thema ein Generator `brands\menswear\plans\<key>_<kurz>.py`, der mit `_common.py` den deutschen und den englischen Plan nach `data\direction\<topic_id>-de.json` / `-en.json` schreibt. Qualitätsmaßstab ist das freigegebene Testvideo Q1 (`data\direction\menswear-20261105-1-de.json`).

## Inhalt

- Thema, Ansatz, Quellen und Skript-Hinweise: `data\calendars\menswear_2026-11.research.json` (Eintrag mit deinem `key`; `source_urls`, `source_evidence`, `notes`). **Nur Aussagen, die dort belegt sind.** Keine Zahlen, keine Gründe, keine Herkunftsgeschichten ohne Beleg. Stilregeln als Konvention formulieren („gilt als“, „üblicherweise“, „laut …“), Quellen im Sprechtext nennen ist erwünscht („Debrett's schreibt …“, „der Londoner Maßschneider …“).
- Keine Markenempfehlung, keine Rangliste, keine Produktversprechen, kein Body-Shaming. Hersteller nur als Quelle.
- Anrede „du“ / „you“. Ruhig, kundig, kurze Sätze.
- Englisch ist sprachlich angepasst, nicht wörtlich übersetzt; gleiche Szenen, eigene Wortanker.
- `sources[]` mit `id`, `url`, `title` (Kurzbeleg), `checked_at` "2026-11-01", `label` kurz (höchstens etwa 30 Zeichen, die Quellenleiste hat zwei Zeilen).

## Länge

- Deutsch 185–200 Wörter (Gemini Orus: 202 Wörter = 77,6 s Video). Englisch 195–215 Wörter (Stimme Algenib, erste Messung läuft; Wert wird nachgetragen).
- Sieben Beats in der Story-Reihenfolge `hook, problem, explanation, demonstration, insight, benefit, close` (einzelne Funktionen dürfen fehlen, die Reihenfolge nicht). Kein Beat länger als etwa 40 Wörter (16 s). Beats `problem`, `explanation`, `demonstration`, `insight` brauchen `source_ids`.
- Abschluss immer `closing_beat(...)` mit dem Satz „… Mehr Blick fürs Detail: Folge Suitwerk.“ / „… For more eye for detail: follow Suitwerk.“

## Szenentypen und Daten (siehe Kopf von `brands\menswear\scenes.py`)

| Typ | wofür | wichtige Felder |
|---|---|---|
| `suitwerk_hook` | Beat 1: große Frage, Objekt zeichnet sich, Lupe auf ein Detail | `question` ≤ 56 Zeichen, `object`, `target` (Punktname), `badge` "?", `question_at`, `badge_at`, `loupe_at`, `nie_at` (Zeitpunkt des „?“), `hold_end: true` |
| `suitwerk_fitting` | Nahaufnahme: Nadel, Zoom, Zustand wechselt von `from` zu `to` | `headline` ≤ 44, `from`, `to` (Objekte), `target`, `zoom` 1.3–1.6, `label` ≤ 30, `pointer_at`, `zoom_at`, `flip_at`, `label_at`; freiwillig `all_at` (Knöpfe pulsieren), `error_at` (roter Ring), `tense_at` (Zugfalten zucken), `ghost_at` (Soll-Linie, nur Sakko), `pull_at` (rote Pfeile, nur Sakko) |
| `suitwerk_ladder` | Objekt links, Etiketten rechts an Punkten | `headline`, `stages[{object, at, title ≤ 18, focus_at, tags[{spot, text ≤ 18, sub, tone always/sometimes/never, at, en, en_at}]}]`; höchstens 3 Etiketten je Stufe, 2 Stufen |
| `suitwerk_compare` | zwei Objekte nebeneinander | `headline`, `left/right{title ≤ 18, object, target, tag ≤ 26, tag2 ≤ 34 (Bernstein), tag2_at, pulses[{target, at, tone}], shapes (nur Sakko)}`, `left_at`, `left_tag_at`, `right_at`, `right_tag_at` |
| `suitwerk_takeaway` | drei Karten mit Mini-Objekt | `headline`, `items[{title ≤ 26, sub ≤ 40, object, at, then (Objekt-Änderung), then_at, ring, ring_at}]` |
| Abschluss | `closing_beat(lang, spoken, frm, to, target, statement ≤ 40, fix_at=, ring_at=, statement_at=, chip_at=)` | Objekt wechselt von falsch zu richtig, grüner Ring |

Farben der Etiketten: `always` Gold (Fakt, Normalfall), `sometimes` Bernstein (offen, nach Geschmack, je nach Quelle), `never` Rot (Fehler, nie). Bernstein-`tag2` nur für Offenes.

## Objekte (`brands\menswear\tools\objects.py`)

| `kind` | Optionen | Punktnamen für `target`, `spot`, Ringe |
|---|---|---|
| `jacket` | `variant` sb1/sb2/sb3/db6, `fastened`, `strain`, `lapel` notch/peak/shawl, `dinner` (Smoking), `neck` tie/bow/none/open, `pockets` flap/jetted/patch, `ticket`, `flower`, `lapel_hole`, `cuff` (sichtbare Manschette in Einheiten, z. B. 12), `chest_pocket` | `button:N`, `lapel`, `lapel_r`, `notch`, `collar`, `pocket`, `ticket`, `chest`, `hem`, `shoulder`, `quarters`, `break`, `sleeve`, `cuff`, `waist`, `lapel_hole`, `neck` |
| `jacket_back` | `vents` none/centre/side | `vent`, `vent_l`, `vent_r`, `seam`, `collar`, `hem`, `shoulder` |
| `waistcoat` | `fastened` (Knöpfe 0–5), `strain` | `button:N`, `button:open`, `hem`, `point`, `pocket`, `v`, `neck`, `waistband` |
| `tailcoat` | (White Tie) | `bow`, `waistcoat`, `tails`, `lapel`, `collar`, `front`, `trousers`, `shirt`, `button` |
| `torso` | `hold` belt/braces/none, `tie_tip` (y, 585 = am Bund), `neck` tie/none | `knot`, `collar`, `belt`, `buckle`, `waistband`, `brace`, `tie_tip`, `placket` |
| `legs` | `break` none/slight/full, `turnup`, `seated`, `sock` long/short, `sock_show`, `shoe` oxford/derby | `hem`, `break`, `shoe`, `sock`, `heel`, `crease`, `lacing` |
| `knot` | `knot` four_in_hand/half_windsor/windsor | `knot`, `dimple`, `collar`, `collar_r`, `blade` |
| `swatch` | `weave` plain/twill/herringbone/flannel/tweed/fresco/worsted/woollen/pinstripe/chalkstripe, `colour`, `layers` (1–4) | `center`, `corner`, `edge`, `weave`, `measure` |
| `fibres` | `microns` (Liste) | `fibre:0`, `fibre:1`, `scale` |
| `yarn` | `spin` worsted/woollen | `center`, `fibre`, `end` |

Ohne `object` gilt das Sakko aus `variant`/`fastened` (Q1). Neue Zeichnungen nicht selbst anlegen; fehlt etwas, das vorhandene Objekt sinnvoll nutzen und im Bericht nennen.

## Zeiten und Wortanker

- Jede Bildaktion hängt an einem gesprochenen Wort: `"w:Wort"` = erstes Wort im Beat, das (klein, ohne Satzzeichen) mit „wort“ beginnt; `"w:Wort#2"` das zweite. Vorsicht bei Präfixen: `w:hin` trifft auch „Hinsetzen“, `w:unter` auch „untersten“. Ein Anker, der im Beat nicht vorkommt, bricht den Lauf ab.
- Reihenfolge innerhalb einer Szene beachten: in der Anprobe `pointer_at` < `zoom_at` < `flip_at`; Etiketten in der Sprechreihenfolge.
- Übergänge: Szene vor einem Übergang `hold_end: true`, Szene danach `backdrop: true` und `overlay.transition` (`iris` mit x/y eines Objektpunkts, oder `blende` 0,7 s). Nie zweimal derselbe Szenentyp direkt hintereinander.
- `overlay.marker`: `fakt` mit `marker_at` in belegten Szenen, `auslegung` in „Kurz gesagt“, `unsicher` wenn Quellen sich widersprechen, kein Marker in Hook und Abschluss; Anprobe mit `vignette: true`.
- Statusleiste: `status_file` kurz (z. B. „Weste, einreihig“), je Beat ein Zustand ≤ 22 Zeichen; Töne `amber` (offen), `red` (Fehler), `muted`, `green` (nur Schluss).
- Hook-Kandidaten: genau 5, Typen `question`, `misconception`, `surprising_fact`, `concrete_risk`, `demonstration`; `spoken` = `on_screen` ≤ 64 Zeichen; die drei mittleren brauchen `source_ids`. H1 ist der gewählte.

## Prüfen (Pflicht, je Sprache)

1. `.venv\Scripts\python.exe brands\menswear\plans\<datei>.py`
2. `.venv\Scripts\python.exe scripts\render_direction.py data\direction\<topic_id>-<de|en>.json --version dry --tts mock --no-render --mirror suitwerk-regie/w1-dry` → muss mit `dry run: ok` enden. Warnung `visual_cuts_rhythm` ist erlaubt, `identical_consecutive_scenes` nicht.
3. Standbilder (nur Deutsch reicht): im Ordner `storage\direction\<topic_id>-de-dry\project` `npx hyperframes snapshot . --at <8–10 Zeitpunkte> -o <absoluter Pfad im Scratchpad>`; `contact-sheet-*.jpg` ansehen: Objekt groß und erkennbar, nichts überdeckt, Texte lesbar, rechts ab x 930 kein Text.
4. `node scripts\overlap_check.mjs storage\direction\<topic_id>-de-dry\project` → `"overlaps":[]`.

Nicht vertonen, nicht rendern, nichts exportieren: Das macht die Render-Warteschlange der Suitwerk-Sitzung. Gemeinsamen Code (`src\fn`, `scripts`) und `brands\menswear\scenes.py` / `tools\*` nicht ändern; Wünsche im Bericht nennen.
