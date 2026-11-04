# Scutoria – Higgsfield: Designrichtungen, Modelle, Kosten (Freigabevorlage)

Von Claude, 30.10.2026, 13:35 (Wien); Farben am selben Tag 13:50 auf das Scutoria-Designsystem umgestellt (Hinweis der Hauptsitzung). Noch nichts erzeugt, keine Credits verbraucht. Guthaben laut Konnektor: 278 Credits, Tarif Starter.

## Werkzeuglage (geprüft)

| Zugang | Stand | Kann |
|---|---|---|
| claude.ai-Konnektor „Higgsfield AI" | verbunden | nur lesen: Guthaben, Modellkatalog, Verlauf, Arbeitsbereich wählen, Claude-Motion-Import |
| MCP-Server `higgsfield` (mcp.higgsfield.ai/mcp, für den Business-Ordner registriert) | **wartet auf Freigabe über `/mcp`** | laut Modellkatalog die Generierung (`generate_image`, `generate_video`, Vorlagen `get_presets`/`execute_preset`); erst nach Freigabe prüfbar |

„Katana"-Vorlagen: im lesbaren Katalog nicht enthalten; ob es sie gibt, zeigt erst der freigegebene Server (`get_presets`). Keine Vorlage wird als Ersatz gewählt.

Creditpreise je Modell stehen **nicht** im Katalog des Konnektors. Drittquellen (Stand April 2026, widersprüchlich): Kling 3.0 etwa 6–10 Credits je 5 s 720p, Seedance 2.0 Fast etwa 17 Credits je 5 s 720p. Verbindlich ist nur der Betrag, den der freigegebene Server vor der Ausführung nennt; vor jedem Auftrag wird er hier genannt und abgewartet.

## Zwei Designrichtungen

**Richtung 1 – Flacher Scutoria-Tisch (Empfehlung).** Grund #0b1120, matte Flächen #121b2f/#19243b, Haarlinien, Akzent Blau #4f8cff, das weiße Papierblatt als einziges Licht; kein Glow, keine Partikel, keine Lichtkegel; mittleres und unteres Drittel flach und dunkel. Entspricht dem Prompt-Blatt Fassung 2 und den Scutoria-Tokens (`OneDrive\scutoria\design\project\tokens.json`). Rein abstrakt: keine Menschen, keine realen Orte, keine Art.-50-Offenlegung „realistische Szene" nötig. Loops gut erreichbar (Standbild als Start- **und** Endbild).

**Richtung 2 – Unscharfer Arbeitsplatz.** Fotorealistischer dunkler Schreibtisch bei Nacht, Bildschirmschein, Bokeh, keine Personen (wie Clip 4 des Prompt-Blatts, aber für alle Szenentypen). Wirkt „echter", kostet aber: realistische Geräte zeigen schnell Marken oder lesbare Oberflächen, die Farbtreue zu #0B132B/#00D4FF ist schlechter, und der Stil beißt sich mit den flachen Diagrammen des Renderers. Nur Clip 4 (UI-Demonstration) profitiert davon.

Empfehlung: Richtung 1 durchgehend, Richtung 2 nur für `bg_ui_desk.mp4`.

## Modellwahl (Starter-Tarif, 9:16, stumm, mindestens 1080p)

| Schritt | Modell | Begründung |
|---|---|---|
| Standbild je Clip | Nano Banana Pro (`nano_banana_pro`, 2k, 9:16) | präzise Farbwerte und Komposition („diagrams"-Modell), günstig; Alternative Soul Location |
| Loop-Hintergründe (1, 3, 4, 5, 6, 7, 11) | Seedance 1.5 Pro (`seedance1_5`, 1080p, `generate_audio` aus, Start- = Endbild, 8 s bzw. 12 s) | einziges 1080p-Modell im Starter mit Start- **und** Endbild; gleiches Bild an beiden Enden ergibt einen echten Loop. Seedance 2.0 „std" braucht Plus, „fast" nur 720p. |
| Hero-Clips (2, 9) | Seedance 1.5 Pro oder Kling 3.0 Turbo (`kling3_0_turbo`, 1080p, Startbild) | Bewegung aus einem Startbild; Dauer 8 s (Hook im Video 4,2 s) |
| Alternative, falls günstiger | Kling 3.0 Omni Frames (`kling_o3_flf`, std, Ton aus, Start+Endbild, 3–15 s) | exakte Dauern (6/8/10 s); Preis erst nach Freigabe sichtbar |

Vorschlag zur Reihenfolge und zum Umfang (Budget höchstens 200 Credits):

1. **Qualitätsprobe:** Standbild + Clip 2 `hero_document_to_chat.mp4` (Kundenliste nähert sich dem Chatfenster, stoppt). Stefan sieht ihn, dann weiter.
2. **Kernpaket:** Clips 1, 3, 4, 5, 6, 7 (Hintergründe je Szenentyp), danach 11 (Outro).
3. **Entfällt oder in Code:** Clip 8 `hero_shield_assemble` widerspricht der Gestaltungsregel „kein Schild" (zweite Kritik) – Vorschlag: streichen. Clip 10 `transition_cyan_sweep` ist ein einfacher CSS-Verlauf – Vorschlag: im Renderer bauen, keine Credits. Clip 9 `hero_server_corridor` nur, wenn Budget bleibt.

Grobe Schätzung bei 8 Clips: 8 Standbilder plus 8 Videos; mit Drittquellen-Preisen 100–200 Credits. Exakt erst nach Freigabe.

## Palette (verbindlich seit 13:50 Wien)

Scutoria-Tokens: Grund #0b1120, Flächen #121b2f und #19243b, Akzent #4f8cff (nie Cyan #00D4FF), Amber #ffd166 nur für offene Fragen, Rot #ff6b6b nur für Sperren, Grün #2ec4b6 nur für Erfolg. Kein Neon, Glow, Glas, keine Lichtkegel; ruhige, einmalige Bewegung. Die Codegrafik des Renderers (`brands\ai_security\brand.yaml`) steht noch auf der Phase-1-Palette; Angleichung ist eine eigene Entscheidung (siehe Prompt-Blatt Fassung 2, Abschnitt „Hinweis Renderer").

## Lizenz

Higgsfield-Nutzungsbedingungen, Abschnitt 4.4: „Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use of Outputs." Rechte bleiben nach Kündigung bestehen (gleicher Abschnitt). Eintrag je Clip in `brands\ai_security\assets\higgsfield\LICENSE.md` und `manifest.json`.

## Was Stefan jetzt entscheidet

1. `/mcp` eingeben und den Server `higgsfield` anmelden.
2. Richtung 1 (Empfehlung) oder Richtung 2.
3. Clip 8 streichen, Clip 10 in Code – einverstanden?
4. Freigabe für die Qualitätsprobe (ein Standbild, ein Clip), sobald der Server den Creditbetrag nennt.

## Creditpreise laut Server (Vorabfrage `get_cost`, 30.10.2026, 14:05 Wien)

| Modell | Einstellung | Credits |
|---|---|---|
| Nano Banana Pro (`nano_banana_pro`) | Standbild 2k, 9:16 | 2 |
| Seedance 1.5 Pro (`seedance1_5`) | 1080p, 8 s, stumm | 24 |
| Seedance 1.5 Pro | 1080p, 4 s / 12 s, stumm | 12 / 36 |
| Seedance 1.5 Pro | 720p, 8 s, stumm | 9,6 |
| Kling 3.0 Turbo (`kling3_0_turbo`) | 1080p, 8 s | 16 |
| Kling 3.0 Omni Frames (`kling_o3_flf`) | std, 8 s, Ton aus, Start+Endbild | 8 |
| Kling 3.0 Omni Frames | pro, 8 s, Ton aus, Start+Endbild | 10 |
| Kling 3.0 Omni Frames | 4k, 8 s, Ton aus | 48 |
| Kling 3.0 Omni Frames | std, 6 s, Ton aus | 6 |

Vorlagen: `get_preset_instructions` listet die Katana-Vorlagen (Produktaufnahmen, Halloween-Porträts); keine passt zu abstrakten Hintergründen, es wird keine als Ersatz verwendet. Projektanlage in Higgsfield ist ausgeschaltet (`auto_create_project` false); die Generierungen laufen ohne Projektordner.

**Empfehlung (geändert gegenüber oben):** Kling 3.0 Omni Frames, Modus pro, 8 s, Ton aus, mit Nano-Banana-Pro-Standbild als Start- und Endbild (Loops) bzw. nur Startbild (Hero). Kosten je Clip 2 + 10 = 12 Credits; Kernpaket mit 8 Clips 96 Credits; Qualitätsprobe 12 Credits.
