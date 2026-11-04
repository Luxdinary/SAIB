# Gigastruct - Visual style (engineering_epic), Vorlage 0.9

Stand 2026-10-30 (Claude, nur Claude Code). Verbindliche Beschreibung für Menschen: `C:\Users\Stefa\OneDrive\Business\02 Marke\Gigastruct\Vorlage Gigastruct.md`. Diese Datei hält die Regeln knapp für den Renderer und die Skript-Sitzungen fest.

## Look in one line

Monumental, aber nachvollziehbar: ein stilisiertes 3D-Architekturmodell des Bauwerks (mattes Weißgrau auf Stahlblau, Zeichnungskanten) ist in jedem Bild das Hauptmotiv und der rote Faden; orange markiert nur das Gemessene. Größe entsteht durch gerechnete Vergleiche, Maßketten und Bauphasen, nicht durch Drohnenbilder.

## Palette

| Rolle | Hex | Verwendung |
|---|---|---|
| bg | `#20384F` | Grund, Nebel, Hintergrund der 3D-Szene |
| accent | `#FF8A2A` | einziges Akzent: Maßchips, Zahlen, aktive Bauphase, Hervorhebungskante, Fortschritt, Highlight-Wort |
| text | `#E9EDF0` | Schrift (Kontrast auf bg 10,2:1; accent auf bg 5,1:1) |
| muted | `#8F9CA8` | Nebeninfos, Hinweis "schematisch" |
| surface | `#30465B` | Statusleiste |
| model / model_inner / edge | `#D6DDE3` / `#9FB0C0` / `#3A5874` | Modell, Schnittflächen innen, Zeichnungslinien |
| water / seabed / ground / grid | `#2E5A80` / `#1A2E40` / `#263F57` / `#3A5874` | Umgebung |
| compare | `#8FA6BC` | Vergleichsobjekte bleiben gedämpft |

## Type

Oswald 600/700 (Headlines, Zahlen, Untertitel), JetBrains Mono 700 (Kicker, Maße, Rechenwege, Statusleiste), Inter (Fließtext, selten). Alle SIL OFL 1.1, Dateien in `assets/fonts/` des Repositorys.

## Fünf Szenentypen (Gigastruct-Bedeutung)

| Typ | Bedeutung | Pflicht |
|---|---|---|
| `cinematic_hook` | Monument-Hook: Frage/Behauptung groß, Modell im Bild, Zahl mit Maßklammer, Chip | Zahl aus Quelle, kein Logo-Intro |
| `data_flow` | Bauphasen in Schritten: Phasenleiste, Modell ändert sich je Phase | Phasen am gesprochenen Wort (`at_word`) |
| `ui_demo` | Schnittmodell: Dach wird aufgeschnitten, Maßchips und Beschriftungen hängen am 3D-Punkt | "Querschnitt schematisch", wenn Innenmaße nicht belegt |
| `comparison` | Größenvergleich gerechnet: zwei Balken, Verhältnis, Rechenweg sichtbar, N Vergleichsobjekte maßstäblich | Verhältnis wird im Renderer gerechnet, Rechnung im Manifest |
| `key_takeaway` | Kennzahlen (bis 3 Kacheln) oder `mode: closing`: Abschluss in der Handlung mit Zähler | Abschluss ohne Endkarte |

## Motion

Eine durchgehende Kamerafahrt je Beat (Dive, Push oder Rückzug), Schnitt beim Beatwechsel. Bildereignisse am Wort. Kein Licht-Glow, kein Neon. Logo (isometrischer Block + GIGASTRUCT) klein oben links ab Bild 1.

## Never

Keine geschätzten Maße, keine unbelegten Kosten, kein laufendes Projekt ohne "Stand <Monat Jahr>", keine fotorealistischen Bilder oder KI-Renderings realer Bauwerke, keine Fotos von Dritten ohne Lizenz.
