# Schnitt und Layout Kurzvideo, alle Marken

Stand: 30.10.2026, 20:20 (Wien). Grundlage ist Stefans Vorlage für die Scutoria-Langvideos, Kopie in `Vorlage Langvideo Scutoria (Original 2026-10-30).md`. Diese Fassung überträgt deren Schnitt- und Layoutregeln auf die Kurzvideos von 65 bis 95 Sekunden im Hochformat, für alle neun Marken. Technisch steckt sie im gemeinsamen Renderer als „Erklärschicht“ (`C:\Automation\faceless-network\src\fn\render\explainer.py`).

## 1. Was gleich bleibt wie im Langvideo

- Jede Bildaktion hängt an einem gesprochenen Wort (Wortanker `w:Wort`), keine geschätzten Zeiten.
- Kleine Reaktionen um 0,3 s, Objektaktionen 0,6 bis 1,2 s, mit Beschleunigung und Abbremsung.
- Übergänge über ein Objekt: Ein Punkt öffnet sich als Kreis zur nächsten Szene. Sonst Überblendung (0,7 s) oder harter Schnitt.
- Bei Nahaufnahmen wird der Rand abgedunkelt und der Kopf zurückgenommen.
- Marker unten links als Kapsel: Form und Wort, nie Farbe allein.
  - Fakt: Quadrat in der Faktfarbe der Marke.
  - Auslegung: violette Raute.
  - Unsicher: bernsteinfarbener Halbkreis.
  - Lücke: roter gestrichelter Kreis.
  - Zusätzlich gibt es den Chip „Beispielwert“ für erfundene Zahlen.
- Quellenleiste unter dem Marker: „Quelle: …“ mit Abrufdatum, Monospace 24 px, höchstens zwei Zeilen. Sie steht, solange der belegte Abschnitt gesprochen wird. Bei Auslegung steht nur der Marker.
- Oben rechts steht durchgehend „SYNTHETISCHE STIMME“ (EN „SYNTHETIC VOICE“).
- Einstiegszeile von Sekunde 0 bis etwa 3,5 s, zum Beispiel „Synthetische Stimme · Quellen am Bildschirm“. Jede Marke ergänzt ihren eigenen Hinweis.
- Farben mit fester Bedeutung:
  - die Faktfarbe für den aktiven Vorgang,
  - Bernstein für Offenes und Unklares,
  - Rot nur für ein Risiko,
  - Grün nur für einen erreichten Zustand,
  - Violett nur für Auslegung.
- Jede Marke behält ihre zwei Schriften und ihre Bildwelt mit einer festen Lichtlogik.
- Sprechtext bleibt unverändert. Beispielwerte sind erfunden und markiert. Nie „sicher“, „zertifiziert“ oder „garantiert“ als Versprechen.

## 2. Was sich im Hochformat ändert

| Langvideo 16:9 | Kurzvideo 9:16 |
|---|---|
| 1920 × 1080, Rand 96 px | 1080 × 1920, Rand 108 px; rechts bleibt x ab 930 frei für die Plattform-Symbole |
| Kopf mit Kicker und Titel 60 px | Kicker-Zeile (Mono 24 px, z. B. „2 · DAS PROBLEM“) bei y 186. Der Titel der Szene ist der Kopftitel; ein eigener Kopftitel nur für Szenen ohne Titel |
| Marker und Quellenleiste ganz unten | Marker und Quellenleiste zwischen Szene und Untertitel, Standard y 1396; je Marke einstellbar (`source_y`), unter y 1600 liegt der Plattformtext |
| keine Untertitel | Untertitel bleiben, mittig in Phrasen |
| 20 s ruhiges Endbild | Endbild der Marke, 3 bis 4 s |
| Figuren ohne Gesicht | gilt weiter, wo eine Marke Figuren zeigt; Zonkfruit behält Plümo |

## 3. Wie eine Marke sie einschaltet

In `brands\<id>\brand.yaml`:

```yaml
explainer:
  enabled: true
  voice_tag: {de: "SYNTHETISCHE STIMME", en: "SYNTHETIC VOICE"}
  opening: {de: "Synthetische Stimme · Quellen am Bildschirm · <Markenhinweis>", en: "..."}
  source_y: 1396
  colors: {fakt: "<Faktfarbe>", auslegung: "#9b6bff", unsicher: "<Bernstein>", luecke: "<Rot>", beispiel: "#8a93a6"}
```

Im Plan gibt es je Szene (`beats[].overlay`) folgende Felder, alle freiwillig:

- `kicker`: Text der Kicker-Zeile.
- `marker`: `fakt`, `auslegung`, `unsicher`, `luecke` oder `none`. Der Standard ist `fakt` bei belegten Szenen.
- `source`: Text der Quellenleiste, oder `false` für keine Leiste.
- `example`: `true` zeigt den Chip „Beispielwert“.
- `transition`: Kreisübergang oder Überblendung in diese Szene.
- `vignette`: abgedunkelter Rand für eine Nahaufnahme.
- `dim_at`, `head_at`, `marker_at`: Zeitpunkte als Wortanker.

In `sources[]` steht je Quelle ein kurzes `label`, damit die Leiste höchstens zwei Zeilen hat. Der Renderer meldet zu lange Leisten, fehlende Wortanker und Fakt-Marker ohne Quelle im Prüfbericht.

## 4. Ablauf je Video

1. Plan anpassen: `overlay` je Szene, `label` je Quelle. Eigene Marker in den Szenen abschalten, die dem unteren Marker widersprechen.
2. Storyboard im Produktionsordner unter `01 Skript\Storyboard.md`. Spalten wie in der Vorlage: Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild.
3. Prüfen mit einem Trockenlauf ohne Stimme (`--tts mock --no-render`). Gerendert wird nur mit einer Google-Stimme (Gemini), vorhanden über `--reuse-voice` oder neu vertont. Die Windows-Stimme ist seit 30.10.2026 gesperrt (Stefan), auch als Entwurf. Renderer und Export verweigern sie.
4. Standbilder prüfen. Es darf nichts überdeckt sein, Kopf, Marker und Quelle müssen lesbar sein, und nichts darf rechts unter den Plattform-Symbolen liegen.
5. Produktionsordner neu füllen. Die alte Exportdatei kommt vorher nach `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-30 Layout-Umstellung`.

## 5. Stand der Umstellung

- Scutoria „KI-Kennzeichnung“ ist umgestellt (Fassung V2, Status VALIDATED, Gemini-Stimme unverändert).
- Die anderen Marken stellen Plan, Storyboard und Markeneinstellungen um. Ihre Endfassung entsteht nach der Gemini-Vertonung. Gritwerk hat die Gemini-Stimme schon.
