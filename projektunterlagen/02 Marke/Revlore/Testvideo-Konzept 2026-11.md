# Revlore – Testvideo-Konzept (Neustart, November 2026)

Stand 02.11.2026 nachts, Revlore-Sitzung. Auftrag: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md`, Abschnitte 4 und 5. Revlore wird Technik-Kanal (Konzeptplan, Nr. 75–126). Wartet auf Freigabe durch die Hauptsitzung beziehungsweise Stefan. Produktion erst nach „Go“.

## Thema

**Zwei Auslöser in einem Sicherungsautomaten** (Konzeptplan Nr. 75, Reihe „Ein Schalter, zwei Schriebe“, Bereich Elektrik, kein Motor). DE, Ziel 75 s.
Hook: „Bei Überlast lässt er sich Zeit, beim Kurzschluss nicht: zwei Auslöser in einem kleinen Schalter.“
Kern: Ein Leitungsschutzschalter hat einen thermischen Auslöser (Bimetall, langsam, gegen Überlast) und einen magnetischen Auslöser (Spule mit Schlaganker, sofort, gegen Kurzschluss). Das Video zeigt beide auf ihrer eigenen Zeitskala: das Bimetall im **Zeitraffer**, den Magnetauslöser in **Zeitlupe**. Am Ende die Auslösekennlinie, die beide verbindet.

Quellen (Stand 02.11.2026):
- geprüft: Schneider Electric, FAQ FA369327 (se.com): nach IEC 60898-1 kleiner Prüfstrom 1,13 × In, großer Prüfstrom 1,45 × In, vereinbarte Zeit 1 h.
- vor dem Skript zu prüfen (Herstellerkatalog als Primärquelle, z. B. ABB, Hager, Siemens): Magnetbereich B 3–5 × In, C 5–10 × In, Auslösung unter 0,1 s; Aufbau mit Bimetall, Spule, Schlaganker, Löschkammer. Bis dahin keine Millisekunden-Zahl im Text, die nicht belegt ist.
- Regel: keine Anleitung am Verteiler; Satz im Video und in der Beschreibung: „Arbeiten an der Installation gehören in die Hand einer Elektrofachkraft.“

## Ablauf und Bildkonzept (mindestens drei Szenentypen, fünf Bewegungsarten)

| Zeit | Szene | Bild | Bewegung | Band |
|---|---|---|---|---|
| 0–6 s | Hook im Flur | H1 Sicherungskasten (Foto, später Kling K2) | langsame Kamerafahrt auf die Schalterreihe, Hebel schnappt (K1) | ECHTZEIT |
| 6–14 s | Vom Foto zum Modell | H2 Schalter in Makro, H3 Seitenansicht | Röntgen-Wischblende: eine Scanlinie fährt über das Foto, dahinter erscheint das gerechnete Schnittmodell an derselben Stelle; Beschriftung Bimetall, Spule, Schlaganker, Kontakt, Löschkammer | ECHTZEIT |
| 14–34 s | Überlast | Einschub H5 Küche (2 s, Wasserkocher und Toaster an einer Leiste), dann Modell | Bimetall erwärmt sich farbig und biegt sich, Uhr läuft schnell, Messschrieb Auslenkung über Zeit, am Ende Klinke frei | ZEITRAFFER n:1 (aus der Rechnung) |
| 34–56 s | Kurzschluss | Modell, Nahzoom auf Spule und Kontakt | Strom springt, Schlaganker schlägt den Kontakt auf, Lichtbogen wandert in die Löschkammer und teilt sich an den Blechen; Uhr in ms | ZEITLUPE 1:n |
| 56–68 s | Kennlinie | Diagramm Strom gegen Zeit, beide Achsen logarithmisch | Stift zeichnet den thermischen Ast, dann die senkrechte Stufe des Magnetauslösers; Bereich B und C als Band; die zwei Szenen als Punkte | STANDBILD |
| 68–78 s | Zurück in Echtzeit | H4 Hebel unten (Kling K1 Ende), H7 Flur, Licht | Hebel unten, Rückblende in den Flur, Markenzeile | ECHTZEIT |

Neu gegenüber dem Piloten: echtes Bauteil als Anfang und Ende, Röntgenblende Foto zu Modell, Zeitraffer als zweite Zeitrichtung, Kennlinie mit Log-Achsen, kein Motor. Was gleich bleibt: Zeitband mit gerechnetem Faktor, Messschrieb mit Stift, Quellenzeile über den Untertiteln.

## Unterschied zu den anderen Marken

Revlore ist die einzige Marke mit gerechneter Zeit: das Band sagt immer, wie stark gebremst oder beschleunigt wird, und jede Bewegung im Modell kommt aus einer Rechnung. Das Foto eines echten Bauteils öffnet sich zum Schnittmodell (Röntgenblende). Andere Marken: Gigastruct zeigt Baustellen und Größen, Suitwerk Stoff und Kreide, Frontlore Rekonstruktionen, Gritwerk das Laborbuch, Dewlane Nahaufnahmen von Produkten, Scutoria das Nachtarchiv, Promptwerk Bildschirmaufnahmen, Tintora Anime. Abstand zu Gigastruct (Prüfrunde): Revlore nutzt kein Blaupausen-Raster und keine Größenvergleiche, sondern Zeitskalen, Uhr und Messschrieb.

## Higgsfield-Liste

Ablage `C:\Automation\faceless-network\brands\engines\assets\higgsfield\library\`, Nachweis in `LICENSE.md` dort. Alle Bilder 9:16, dunkel, Graphit und kühles Stahlgrau, ein Akzent #2F9BFF, keine Schrift, kein Logo, keine Marke, keine Personen, keine Hände. KI-Bilder zeigen Bauteile und Orte, nie das Innere als Beleg (das Innere zeigt das gerechnete Modell).

| Nr | Datei | Modell | Prompt (Kern) | Credits |
|---|---|---|---|---|
| H1 | rl_mcb_panel | Nano Banana Pro 2K | open residential distribution board in a dim hallway, one row of plain grey miniature circuit breakers on a DIN rail, all levers up, no labels | 2 |
| H2 | rl_mcb_macro_on | Nano Banana Pro 2K | macro, three-quarter view of a single plain grey miniature circuit breaker on a DIN rail, lever up, shallow depth of field | 2 |
| H3 | rl_mcb_side | Nano Banana Pro 2K | exact side profile of a single plain grey miniature circuit breaker on a DIN rail, centred, flat dark background (Vorlage für die Röntgenblende) | 2 |
| H4 | rl_mcb_macro_off | Nano Banana Pro 2K | same as H2, lever down (Endbild für K1) | 2 |
| H5 | rl_kitchen_load | Nano Banana Pro 2K | evening kitchen counter, an electric kettle and a toaster plugged into one power strip, no people | 2 |
| H6 | rl_bimetal_macro | Nano Banana Pro 2K | macro of a thin two-layer metal strip, brass on steel, on a dark workbench (Materialbild, nicht als Inneres eines bestimmten Schalters) | 2 |
| H7 | rl_hall_end | Nano Banana Pro 2K | dim hallway, closed distribution board door, soft lamp light | 2 |
| | Reserve für Wiederholungen (Schrift, Marken, Fehler) | | | 16 |
| K1 | rl_mcb_trip | Kling 3.0 Omni Frames pro, 8 s | Start H2, Ende H4: lever snaps down | 10 |
| K2 | rl_mcb_panel_push | Kling, 8 s | Start und Ende H1, sehr langsame Fahrt | 10 |
| K3 | rl_kitchen_steam | Kling, 8 s | Start und Ende H5, Dampf aus dem Wasserkocher | 10 |
| K4 | rl_hall_end_loop | Kling, 8 s | Start und Ende H7, Licht wird ruhig | 10 |

**Stand 02.11.2026, 22:35 Wien: H1–H7 erzeugt und abgelegt (`rl_mcb_panel`, `rl_mcb_macro_on`, `rl_mcb_side`, `rl_mcb_macro_off`, `rl_kitchen_load`, `rl_bimetal_macro`, `rl_hall_end`, je .jpg), 18 Credits (14 abgelegt, 4 verworfen: erste Fassung von H2/H4 trug „ON“/„OFF“ auf dem Hebel). H4 ist eine Bearbeitung von H2 mit gleichem Ausschnitt, damit K1 sauber vom einen ins andere Bild läuft. H1 trägt winzige unlesbare Pseudo-Aufdrucke; Kamerafahrt nicht zu nah.**

**Stand 03.11.2026 früh: Kling K1–K4 als 5-s-Clips (je 9 Credits, get_cost geprüft; 8 s hätte 14,4 gekostet) erzeugt und abgelegt (`rl_mcb_trip`, `rl_mcb_panel_push`, `rl_kitchen_steam`, `rl_hall_end_loop`); dazu abgeleitete 24-s-Hintergründe `rl_t_*.mp4` (0 Credits). Gesamt 54 von 100 Credits. Plan `C:\Automation\faceless-network\data\direction\engines-20261104-1-de.T1.json` (Sprechtext 1.218 Zeichen, mit Gemini etwa 80 s), Szenen `zt_photo`, `zt_mcb` (Röntgen, Zeitraffer, Zeitlupe), `zt_curve`; Ton-Cues in `layout.sound_cues`. Trockenlauf mit stummer Probestimme: Prüfungen bestanden, `overlap_check` ohne Befund, `small_text` leer. Quellen geprüft: Siemens SENTRON Tabelle (B 5 × In < 0,1 s, C 10 × In < 0,1 s), Hager (zwei Auslöser, Anwendungen B/C), Patent DE3625425A1 (Aufbau). K4 (Flur) wird im Testvideo nicht gebraucht.**

Summe geplant: Bilder 14 + Reserve 16 = 30 Credits; Kling 40 Credits erst nach Meldung der Hauptsitzung. Zusammen höchstens 70 von 100. Preise vor jedem Auftrag mit `get_cost` prüfen.

## Ton-Cues (Klangfarbe: präzise, mechanisch, leise; kein Kino-Bombast)

| Zeit | Cue | Klang |
|---|---|---|
| 0,0 s | Musikbett ein | minimal, Takt wie ein Uhrwerk, leise; unter der Stimme abgesenkt |
| 4,5 s | Hebel schnappt (K1 Vorschau) | trockenes „Klack“ eines Schalters |
| 6,0 s | Röntgenblende | kurzes Scan-Rauschen, hell, 0,6 s |
| 14,0 s | Einstieg Zeitraffer | schneller werdender Uhrticker, endet beim Auslösen |
| 33,5 s | Bimetall löst aus | „Klack“ |
| 34,0 s | Einstieg Zeitlupe | tiefer, gebremster Whoosh |
| 38,0 s | Lichtbogen | leises Knistern, gedämpft, keine Explosion |
| 56,0 s | Kennlinie | Stiftkratzen am Messschrieb |
| 68,0 s | zurück in Echtzeit | Whoosh nach oben, Musik kurz lauter, dann aus |

## Stimme, Code, offene Punkte

- Stimme: 1 Gemini-Flash-Anfrage für das deutsche Testvideo am 03.11. ab 09:05, erst nach Freigabe dieses Konzepts und fertigem Sprechtext; höchstens 2 weitere bei Fehlern.
- Code nur unter `brands\engines\zeitlupe\`: Schnittmodell Leitungsschutzschalter (Bimetall-Biegung, Spule, Schlaganker, Kontakt, Lichtbogen in der Löschkammer), Band mit ZEITRAFFER, Röntgenblende Foto zu Modell, Kennlinie mit Log-Achsen, Feld `backdrop` für Fotos und Clips. Die Tonebene kommt aus dem gemeinsamen Renderer; der Plan bekommt Cue-Punkte.
- Offen für Stefan: Stimmt die Richtung Technik-Kanal so (Konzeptplan Nr. 75–126)? Aussprache „Revlore“ und Abstand zu Gigastruct bleiben offene Punkte der Format-Bibel.
