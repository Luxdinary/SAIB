# Qualitätsrunde 31.10.2026: alle Marken auf Scutoria-Niveau

Stand: 30.10.2026, 22:15 (Wien). Auftrag von Stefan: Er hat Scutoria „KI-Kennzeichnung“ mit Note 1,7 bewertet und alle anderen Videos mit Note 3. Alle Videos werden optisch, in der Animation und grafisch überarbeitet. Die vorhandenen Gemini-Stimmen bleiben. Ziel für den Morgen des 31.10.: je Kanal ein fertiges deutsches Video.

## 1. Warum Scutoria besser wirkt (Vergleich der Kontaktbögen, 30.10.2026)

| Scutoria (1,7) | übrige Marken (3) |
|---|---|
| Hintergrund mit Tiefe: Filmmaterial, Licht und Schatten füllen das ganze Bild, darüber ein ruhiger Schleier | flacher, fast schwarzer Grund; große leere Flächen, besonders unten und an den Seiten |
| Ein Leitobjekt (Datei „Website-Chat“) und eine Statusleiste führen durch alle Szenen; der Zuschauer sieht, was sich ändert | Motiv wechselt je Szene ohne roten Faden, oder der rote Faden ist klein |
| Karten dicht, groß, sauber gesetzt; Szenentitel 2 Zeilen groß und mittig; Inhalt nutzt die Breite | Hauptmotiv zu klein (z. B. Motor nimmt ein Drittel der Breite ein), Titel klein oben links |
| Jede Szene hat mehrere Bildereignisse an gesprochenen Wörtern (Karte erscheint, Zustand kippt, Haken setzt) | wenige Bewegungen, lange Standbilder |
| Einheitliche Bildsprache aus einem echten Designsystem (Radien, Schatten, Icons, zwei Schriften) | Stil uneinheitlich oder roh |

Schwächen auch bei Scutoria, die keine Marke übernehmen darf: Marker und Quellenleiste überdecken Szeneninhalt, und die Chips „Unsicher“ an den Gabelkarten widersprechen dem Marker „Fakt“.

## 2. Pflicht für jede Marke

1. **Hintergrund mit Tiefe, nur mit Code:** Er füllt das ganze Bild, mit Licht, Textur, Verlauf und langsamer Kamerabewegung oder Parallaxe, passend zur Bildwelt der Marke. Möglich sind CSS, SVG, Canvas oder WebGL (Three.js liegt bei Gigastruct). Kein Higgsfield, keine KI-Bilder, keine fremden Clips.
2. **Hauptmotiv groß:** Das Motiv füllt 70 bis 90 % der Inhaltsbreite. Keine leere Fläche über 20 % der Bildhöhe zwischen Kopf und Untertitel.
3. **Leitobjekt und Statusleiste:** Ein markentypisches Objekt läuft durch alle Szenen und ändert seinen Zustand mit der Geschichte, nach dem Vorbild der Scutoria-Datei mit Statusleiste.
4. **Bewegung an Wörtern:** Mindestens drei Bildereignisse je Szene, jedes an einem gesprochenen Wort. Dazu Kamerafahrt oder Push-in je Szene, Kreisübergang aus einem Objekt, wo es passt.
5. **Typografie:** Szenentitel höchstens zwei Zeilen und groß. Beschriftungen mindestens 26 px. Zwei Schriften je Marke, einheitliche Radien, Schatten und Icons.
6. **Erklärschicht ohne Überdeckung:** Kicker, Marker und Quellenleiste liegen in eigenen, freien Zonen. `node scripts/overlap_check.mjs <projekt>` muss ohne Befund durchlaufen. Szenen-Chips, die dem unteren Marker widersprechen, werden abgeschaltet.
7. **Stimme bleibt:** Die vorhandene Gemini-Aufnahme wird mit `--reuse-voice` wiederverwendet. Der Sprechtext darf sich deshalb nicht ändern, sonst verweigert der Renderer. Keine neue Vertonung, keine Windows-Stimme.
8. **Prüfen vor dem Export:**
   - Trockenlauf.
   - Render als Fassung `Q1`.
   - Prüfbericht VALIDATED, bei Risiko „hoch“ HUMAN_REVIEW.
   - Überschneidungs-Prüfung ohne Befund.
   - Kontaktbogen (`ffmpeg -i video.mp4 -vf "fps=1/8,scale=270:480,tile=5x2" -frames:v 1 kontakt.jpg`) selbst ansehen und gegen Scutoria vergleichen.
   - Erst wenn das eigene Urteil mindestens Note 2 ist, exportieren.

## 3. Regeln

- Nur die eigenen Markendateien ändern: `brands\<id>\`, den eigenen Plan, die eigenen Ordner in `05 Produktion` und `02 Marke\<Marke>`. Gemeinsamer Code (`src\fn`, `scripts`) nur lesen; Wünsche an die Hauptsitzung.
- Rendern nacheinander über `data\render.lock` (älter als 20 Minuten gilt als frei). Bei Speicherschutz unter 30 GB zehn Minuten warten und erneut versuchen.
- Alte Exportdatei vor dem neuen Export nach `C:\Users\Stefa\Documents\_zum_loeschen\2026-10-31 Qualitätsrunde` verschieben. Nichts löschen, nichts veröffentlichen, keine Commits, keine Konten.
- Stefan schläft. Nicht auf ihn warten; Fragen an die Hauptsitzung, sonst begründet selbst entscheiden und im Bericht nennen.
- Am Ende Storyboard, Vorlage-Datei der Marke und Redaktionsplan aktualisieren und berichten: Länge, Prüfstatus, Befund der Überschneidungs-Prüfung, eigene Note, Pfad des Exports und des Kontaktbogens.
