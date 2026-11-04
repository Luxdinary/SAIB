# Revlore – Wünsche für die Hintergrund-Bibliothek (Higgsfield)

Stand: 02.11.2026, von der Revlore-Sitzung (Format „Zeitlupe“, `Format-Bibel.md`). Nur Wünsche; erzeugt wird von der Sitzung „Bibliotheken“ nach Stefans Freigabe des Ausgabeplans. Bis dahin keine Credits.

## Wozu

Die Mechanik bleibt das gerechnete Code-Modell. Die Bibliothek gibt nur Raum und Stimmung **hinter** dem Modell, vor allem in den Szenen, die Echtzeit zeigen (Anfang `zl_hook` und Schluss `zl_realtime`). In der Zeitlupe-Mitte (Lineal, Messschrieb) bleibt der ruhige Messraum-Grund, sonst lenkt der Hintergrund von den Strichen und Kurven ab.

## Bildregeln

- Hochformat 9:16, dunkel und kontrastarm. Unter einem Schleier von etwa 0,6 Deckkraft muss das Modell klar davor stehen.
- Farbwelt passend zur Palette: Graphit, kühles Stahlgrau, ein wenig Blau (#2F9BFF). Orange nur sehr sparsam (glühender Krümmer), weil Orange im Modell für Verbrennung steht.
- Kein erkennbarer Hersteller, kein Logo, kein Kennzeichen, keine lesbare Schrift, keine Personen und keine Hände.
- Keine eigene Mechanik im Hintergrund, die falsch laufen könnte (keine sich drehenden Riemen oder Zahnräder, keine Kolben). Nur Raum, Licht, Oberflächen.
- Bewegung höchstens langsam: leichter Kameradrift, Hitzeflimmern, Staub im Licht. Schleifenfähig, 5–8 s.

## Motive (Vorschlag, je 1 Clip)

1. Prüfstand-Raum bei Nacht: Motor auf einem Prüfstand als dunkle Silhouette, Messkabel, kaltes Deckenlicht, unscharf.
2. Motorraum von oben, sehr nah und unscharf: Ansaugbrücke, Kabelbaum, matte Metallflächen, Streiflicht.
3. Werkbank mit zerlegtem Zylinderkopf, unscharf im Hintergrund, Lichtkante auf Aluminium.
4. Glühender Abgaskrümmer im Dunkeln, nur Teil des Bildes, langsames Hitzeflimmern (für Themen zu Abgas und Verbrennung).
5. Leere, dunkle Werkstatt mit Hallenlicht und Raster auf dem Boden (neutraler Ersatz für alle Themen).

## Einbau

Szenentypen `zl_hook` und `zl_realtime` bekommen ein optionales Feld `backdrop` (Clip unter dem Schleier). Das baut die Revlore-Sitzung, sobald Clips da sind; der Mechanik-Code bleibt unberührt. KI-Kennzeichnung bleibt wie bisher („KI-generiert“).
