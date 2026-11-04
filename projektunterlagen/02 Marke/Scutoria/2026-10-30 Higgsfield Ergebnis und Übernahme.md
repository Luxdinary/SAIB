# Scutoria – Higgsfield: Ergebnis und Übernahme in die Produktion

Von Claude, 30.10.2026, 16:05 (Wien). Bezug: Prompt-Blatt Fassung 2 (Scutoria-Palette), Briefing `_Higgsfield-Briefings (Codex, 2026-10-30)\01-Scutoria.md`, zweite Kritik vom 30.10.2026. Guthaben vorher 278 Credits, nachher 182. Nichts veröffentlicht, nichts committet, nichts gelöscht.

## Was erzeugt wurde

| # | Datei | Zweck | Modell | Credits | Abnahme |
|---|---|---|---|---|---|
| 1 | `bg_hook_dataroom.mp4` | Hintergrund Hook (matter Tisch oben, blaue Haarlinie) | Nano Banana Pro 2k + Kling 3.0 Omni Frames pro, 8 s, Start = Endbild | 12 | Loop nahtlos (Differenz 0,33), Mitte 7 %, unten 6 % |
| 2 | `hero_document_to_chat.mp4` | Hero Hook: Blatt gleitet zum oberen Drittel und stoppt | Nano Banana Pro + Kling Omni Frames pro, 8 s, nur Startbild | 12 | kein Text, Blatt zieht durch die Mitte (gewollt); Nutzung 4,2 s |
| 3 | `bg_flow_lanes.mp4` | Hintergrund Data Flow (Segmente wandern an den Rändern) | wie 1 | 12 | nahtlos (0,17), überall 7 % |
| 4 | `bg_ui_desk.mp4` | Hintergrund UI-Demo (unscharfer Laptop, blasser Bildschirm) | wie 1 | 12 | nahtlos (0,34), oben 19 %, Mitte 9 %; kein Logo erkennbar |
| 5 | `bg_compare_split.mp4` | Hintergrund Vergleich (Haarlinie in Bildmitte) | wie 1 | 12 | nahtlos (0,26), Mitte 11 % |
| 6 | `bg_negate_pulse.mp4` | Hintergrund Verneinung (roter Rahmen) | wie 1 | 12 | nahtlos (0,35); Rahmen-Fade kaum sichtbar, praktisch Standbild |
| 7 | `bg_takeaway_calm.mp4` | Hintergrund Takeaway und Close (Band oben) | wie 1 | 12 | nahtlos (0,56), unten 4 % |
| 11 | `bg_outro_orbit.mp4` | Outro (Kreis mit Lücke dreht sich einmal) | wie 1 | 12 | nahtlos (0,26), überall 7 % |

Gestrichen: 8 `hero_shield_assemble` (Regel „kein Schild"), 10 `transition_cyan_sweep` (der Director hat keine Übergangsebene; ein Sweep bleibt Codegrafik), 9 `hero_server_corridor` (nicht erzeugt, Budget gespart). Ein Standbild (Clip 3) schlug beim ersten Versuch fehl, wurde erstattet und wiederholt; ein Videoauftrag (Clip 11) wurde vom Server zunächst mit einer Vorlagenempfehlung beantwortet und ohne Vorlage erneut eingereicht.

Technik: Kling liefert 1076 × 1928; lokal mit FFmpeg auf 1080 × 1920 skaliert (H.264, crf 16), Loops dreimal aneinandergehängt (24 s), damit auch der längste Beat (17,3 s) ohne Einfrieren abgedeckt ist. Rohdateien liegen als `_raw_*.mp4` daneben. Seeds gibt die Schnittstelle nicht aus (NOT_VERIFIED). Ablage: `C:\Automation\faceless-network\brands\ai_security\assets\higgsfield\` (Clips, Standbilder, `LICENSE.md`, `manifest.json`, `index.html`), Spiegel `05 Produktion\_Demos\scutoria-regie\higgsfield-assets\` mit Bildstreifen je Clip unter `preview\`.

Lizenz: Higgsfield Starter; Nutzungsbedingungen Abschnitt 4.4: „Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use of Outputs." Rechte an exportierten Ausgaben bleiben nach Kündigung. Je Clip eine Zeile in `LICENSE.md`; die Prüfung `license_manifest` des Renderers liest sie.

## Fassung B

Render aus `data\direction\ai_security-20261105-1-de.B.json` (Kopie des A-Plans; nur vier Layoutwerte für den neuen Check `platform_overlay` ergänzt, Übergangs-Eintrag entfernt) mit der vorhandenen Gemini-Stimme `voice_A_gemini.wav`, Asset-Schicht an, Scrim 0,55. Ergebnis in `05 Produktion\_Demos\scutoria-regie\fassung-b\` (video.mp4 75,5 s, cover.jpg, Standbilder 5/30/60 s, Overlay-Prüfbilder, report.json, manifest.json) und als Abschnitt „Fassung B" in `scutoria-regie\index.html` neben A und A2.

Render 30.10.2026, 16:07 (Wien): Status **HUMAN_REVIEW**, einziger offener Befund `schematic_ui` (UI-Demo ohne echte Bildschirmaufnahme, wie in A und A2). Alle harten Prüfungen bestanden, darunter `license_manifest` (sechs Clips mit Lizenzzeile), `platform_overlay`, `duration_range` (75,5 s), `visual_cuts_static` (9,8 s). Kein `asset_placeholders`-Befund, also keine Platzhalter mehr. Renderzeit 206 s, Vertonung wiederverwendet, variable Kosten 0 USD. Verwendet werden sechs Clips; `bg_negate_pulse.mp4` und `bg_outro_orbit.mp4` bleiben in dieser Fassung ungenutzt, weil der Plan je Szenentyp einen Clip zuordnet (beide Vergleichsbeats nutzen `bg_compare_split`) und das Outro keinen Clip vorsieht.

## Je Szene: in Code nachbaubar, festes Asset nötig oder Higgsfield je Thema

| Szene (Beat) | Clip | Einordnung | Begründung |
|---|---|---|---|
| Hook, `cinematic_hook` (b1) | `bg_hook_dataroom` + `hero_document_to_chat` | **festes Asset** (einmalig je Marke) für das Blatt; Hintergrund **in Code nachbaubar** | Der Tisch-Hintergrund ist eine flache Fläche mit Haarlinie: als CSS-Verlauf plus Linien in 30 Minuten nachbaubar. Das gleitende Papierblatt mit Schatten ist als Video überzeugender als die bisherige Dokumentkarte; es ist themenneutral (leeres Blatt) und für alle Scutoria-Videos verwendbar. Themenabhängige Hero-Motive (z. B. Serverkorridor) wären **Higgsfield je Thema**. |
| Problem, `data_flow` (b2) | `bg_flow_lanes` | **in Code nachbaubar** | Zwei Haarlinien mit wandernden Segmenten sind eine GSAP-Animation von zwei Divs; der Clip bringt gegenüber Code keinen Mehrwert. |
| Erklärung, `comparison` versus (b3) | `bg_compare_split` | **in Code nachbaubar** | Zwei Flächen und eine Linie in der Mitte; trivial als CSS. |
| Demonstration, `ui_demo` (b4) | `bg_ui_desk` | **festes Asset** | Unscharfer fotografischer Schreibtisch ist in Code nicht herstellbar; ein Clip je Marke reicht, themenneutral. Alternative: echte Bildschirmaufnahme von Stefan (ohnehin für `schematic_ui` nötig). |
| Erkenntnis, `comparison` negate (b5) | `bg_negate_pulse` | **in Code nachbaubar** | Roter Rahmen mit Ein-/Ausblendung ist eine CSS-Animation; der Clip zeigt die Bewegung kaum. |
| Nutzen, `key_takeaway` (b6) | `bg_takeaway_calm` | **in Code nachbaubar** | Band oben mit Haarlinie; CSS. |
| Abschluss, `key_takeaway` closing (b7) und Outro | `bg_takeaway_calm`, `bg_outro_orbit` | **in Code nachbaubar** | Kreisumriss mit Lücke, der sich dreht: SVG-Animation. |

Fazit: Von acht Clips sind sechs flache Grafiken, die der Renderer selbst zeichnen kann, sobald die Phase-1-Palette (`brand.yaml`) auf die Scutoria-Tokens umgestellt ist. Zwei Clips lohnen sich als feste Assets je Marke: das gleitende Papierblatt (Hero) und der unscharfe Schreibtisch (UI-Demo). Higgsfield je Thema wäre nur für themenspezifische Hero-Motive nötig; das Konzept (Kundenliste als wiederkehrendes Objekt) kommt für Scutoria ohne aus.

## Entscheidung Stefan (30.10.2026, 16:27 Wien)

**Basis für Scutoria ist Fassung B.** B nutzt Skript und Szenenplan von Fassung A (Hook „Darfst du vertrauliche Firmendaten einfach in Claude eingeben?"); die Inhaltsüberarbeitung aus A3.1 (Kundenliste als roter Faden, Statusleiste, Hook „Deine Kundenliste im KI-Chat. Wer darf sie verwenden?") ist darin nicht enthalten. Nächster Schritt: A3.1-Plan mit der Asset-Schicht von B rendern (Vertonung wiederverwenden, keine Credits). Eingetragen in der Übersicht Business.

## Was Stefan noch entscheiden muss

1. **Renderer-Palette:** erledigt durch die A2-Sitzung (`brand.yaml` seit 15:33 Wien auf Scutoria-Tokens: Grund #0b1120, Flächen #121b2f/#19243b, Text #e9eef8). Fassung B wurde bereits damit gerendert; Clips und Codegrafik passen zusammen. Zu prüfen bleibt `visual_style.md` (Motiv „shield-lines").
2. **Sechs Hintergründe in Code** nachbauen (keine laufenden Kosten) oder als Clips behalten.
3. **Clip 9 (Serverkorridor)** für Cloud-Themen erzeugen (12 Credits) oder weglassen.
4. **Echte Bildschirmaufnahme** für die UI-Demo (Befund `schematic_ui` bleibt sonst HUMAN_REVIEW).

## Verbrauch

Credits: 96 (8 Standbilder je 2, 8 Videos je 10; eine Erstattung von 2 für ein fehlgeschlagenes Standbild). Guthaben: 278 → 182 (Stand 30.10.2026, 16:00 Wien). Keine weiteren Kosten (TTS wiederverwendet, Render lokal).
