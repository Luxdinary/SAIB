# Lizenzübersicht der Video-Bausteine

Stand: 03.11.2026 (Wien), Tonebene ergänzt (Soundeffekte und Musikbett des gemeinsamen Renderers). Die Nachweise selbst liegen neben den Dateien im Code-Ordner `C:\Automation\faceless-network`. Jedes Video hat zusätzlich eine Lizenzliste in `manifest.json` (Abschnitt `licenses`), im Produktionsordner unter `03 Schnittprojekt`. Der Renderer bricht ab, wenn ein verwendeter Clip keine Lizenzzeile hat.

| Baustein | Wo | Lizenz und Nachweis |
|---|---|---|
| Schriften Inter, JetBrains Mono, Montserrat, Oswald, Playfair Display | `assets\fonts\` | SIL Open Font License 1.1 (laut `brand.yaml` der Marken) |
| Manrope (Scutoria) | `brands\ai_security\assets\fonts\manrope\` | SIL Open Font License 1.1, `LICENSE-manrope.txt` |
| Fraunces (Gritwerk), Fredoka (Zonkfruit) | `brands\motivation\assets\fonts\`, `brands\brainrot\assets\fonts\` | SIL Open Font License 1.1, `OFL.txt` je Ordner |
| GSAP (Animation) | `assets\vendor\` | GSAP Standard License, `LICENSE-gsap.txt` |
| Three.js (Gigastruct 3D) | `brands\megaconstruction\assets\vendor\` | MIT, `LICENSE-three.txt` |
| Higgsfield-Clips (Scutoria, 8 Clips) | `brands\ai_security\assets\higgsfield\` | Higgsfield Starter, Nutzungsbedingungen Abschnitt 4.4: keine Einschränkung der kommerziellen Nutzung der Ergebnisse; Job-Nummern je Clip in `LICENSE.md` |
| Zonkfruit-Serie, Stufe 0 (27 Bilder, 4 Videos, 02.11.2026) | `OneDrive\Business\02 Marke\Tintora\Serie\Stufe 0\` | Higgsfield Starter, Nutzungsbedingungen Abschnitt 4.4 wie oben; Job-Nummern je Datei in `LICENSE.md` dort; Referenz nur das eigene Plümo-Charakterblatt |
| Higgsfield-Bibliothek Frontlore (44 Bilder, 1 Clip; 02. und 03.11.2026) | `brands\military_history\assets\higgsfield\library\` | Higgsfield Ultra, Nutzungsbedingungen Abschnitt 4.4 wie oben; Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md` dort, Kontaktbogen `index.html` |
| Higgsfield-Bibliothek Gigastruct (29 Bilder, 1 Clip; 02. und 03.11.2026) | `brands\megaconstruction\assets\higgsfield\library\` | Higgsfield Ultra, Nutzungsbedingungen Abschnitt 4.4 wie oben; Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md` dort, Kontaktbogen `index.html` |
| Higgsfield-Bibliothek Gritwerk (39 Bilder, 1 Clip; 02. und 03.11.2026) | `brands\motivation\assets\higgsfield\library\` | wie oben; Job-Nummer, Modell, Credits und Prompt je Datei in `LICENSE.md` dort, Kontaktbogen `index.html` |
| Higgsfield-Bibliothek Promptwerk (29 Bilder, 1 Clip; 03.11.2026) | `brands\claude_workflows\assets\higgsfield\library\` | wie oben |
| Higgsfield-Bibliothek Dewlane (32 Bilder, 1 Clip; 02. und 03.11.2026; 6 Textur-Schleifen ausstehend) | `brands\beauty\assets\higgsfield\library\` | wie oben |
| Higgsfield-Bibliothek Suitwerk (34 Bilder, 1 Clip; 02. und 03.11.2026; 2 Stimmungs-Schleifen ausstehend) | `brands\menswear\assets\higgsfield\library\` | wie oben |
| Higgsfield-Bibliothek Revlore (23 Bilder, 1 Clip; 02. und 03.11.2026; 5 Hintergrund-Schleifen ausstehend) | `brands\engines\assets\higgsfield\library\` | wie oben |
| Hintergrundclips Dewlane | `brands\beauty\assets\clips\` | eigene Arbeit (SVG/CSS, lokal gerendert am 30.10.2026), keine Rechte Dritter, `LICENSE.md` |
| Soundeffekte Zonkfruit | `brands\brainrot\assets\sfx\` | eigene Synthese (numpy), keine Samples, `LICENSE.md` |
| Stimme | je Video `manifest.json` › `tts` | Google Gemini TTS (gemini-2.5-flash-preview-tts) über die Gemini-API, bezahlte Stufe seit 30.10.2026; Bedingungen des Anbieters. Keine Windows-Stimme (Stefan, 30.10.2026) |
| Soundeffekte gemeinsamer Renderer (12 Dateien: whoosh, whoosh2, swipe, swipe2, click, tick, stamp, paper, pop, thud, chime, riser; 03.11.2026) | `assets\sfx\` | eigene Synthese (`src\fn\render\sound_synth.py`, numpy, fester Startwert je Klang), keine Samples, keine Rechte Dritter; Funktion, Startwert und Parameter je Datei in `LICENSE.md` dort |
| Musikbett (prozedural, je Video im Renderer erzeugt; 03.11.2026) | je Video `manifest.json` › `sound.music` | eigene Synthese (`src\fn\render\sound_synth.py`, additive Akkordflächen, Stimmung und Startwert im Manifest), keine Samples, keine Rechte Dritter. Entscheidung Stefan, 03.11.2026: vorerst selbst erzeugt |
| Musik (Lizenzdateien) | `assets\music\` oder `brands\<id>\assets\music\` | keine; leer, bis eine Lizenzquelle gewählt und hier belegt ist (Haken: `brand.yaml` › `sound.music`, siehe `assets\music\README.md`) |

Offen: Lizenzmusik als Ergänzung zum prozeduralen Bett; Higgsfield-Audio (`generate_audio`) nicht freigegeben: Nutzungsbedingungen (Stand 23.10.2026, gelesen 03.11.2026) regeln Musik und Audio nicht eigens, Abschnitt 8 unterwirft Drittanbieter-Modelle deren Richtlinien, Abschnitt 13.2 legt die Rechteklärung dem Nutzer auf; welches Audiomodell dahinter steht, ist nicht ermittelbar; Prüfung der Gemini-API-Bedingungen zur kommerziellen Nutzung der Audioausgabe (nicht durchgeführt, nicht ermittelbar ohne Lesen der aktuellen Bedingungen).
