# Suitwerk – Wünsche für die Bibliothek (Higgsfield)

Stand: 02.11.2026, von der Suitwerk-Sitzung (Format „Kreidestrich“, `Format-Bibel.md`). Nur Wünsche; erzeugt wird von der Sitzung „Bibliotheken“ nach Stefans Freigabe des Ausgabeplans (vorgesehen: 120 Credits). Bis dahin keine Credits.

## Wozu, und wozu nicht

- Die **Struktur** eines Stoffs (welcher Faden oben liegt, wohin der Grat läuft) bleibt Code: Sie wird aus der Bindung gerechnet (`warp_up` in `brands\menswear\kreidestrich\scenes.py`). KI-Bilder können Bindungen falsch zeichnen und dürfen deshalb nie als Beleg für eine Bindung, ein Maß oder eine Passform dienen.
- Die Bibliothek liefert **Anschauung von Material**: wie ein Stoff im Licht aussieht (Glanz, Haarigkeit, Fall), und **Stimmung am Zuschneidetisch** für den Hook und den Schluss. Im Video steht dann zusätzlich „KI-Bild“ am Bild, und die gezeichnete Vergrößerung daneben erklärt.
- Einsatz: als Hintergrund unter dem Tuch-Grund (`kw_hook`, `kw_close`) und als echt wirkendes Stoffmuster neben der Zeichnung („so sieht es aus“ / „so ist es gebaut“).

## Bildregeln

- Draufsicht oder flacher Winkel auf einen Zuschneidetisch; Hochformat 9:16 für Clips, quadratisch 1:1 für Stoffmuster.
- Farbwelt passend zur Palette: Marine, Anthrazit, Elfenbein, warmes Lampenlicht von links oben. Keine kräftigen Modefarben, außer das Thema verlangt es (Seersucker, Leinen).
- **Keine Marken, Logos, Etiketten, Webkanten mit Schrift, Knöpfe mit Prägung.** Keine lesbare Schrift. Keine Personen, keine Gesichter, keine Hände, keine Haut.
- Keine Kaufsituation (kein Laden, keine Preisschilder, keine Kleiderbügel mit Anhängern).
- Werkzeuge nur neutral: Schneiderkreide, Maßband ohne lesbare Zahlen, Zackenschere, Stecknadeln, Fadenzähler.
- Clips höchstens langsam: Lichtwechsel über das Tuch, leichter Kameradrift. Schleifenfähig, 5–8 s.

## Motive (Vorschlag, nach Priorität)

Stoffmuster, quadratisch, Makro, Streiflicht (je 1 Bild, Nano Banana Pro 2k laut Gedächtnis 2 Credits):

1. Marineblauer Kammgarn in Leinwandbindung, Zackenschnittkante.
2. Marineblauer Kammgarn-Köper, deutlich schräger Grat (Gabardine-ähnlich).
3. Grauer Flanell, leicht angeraut.
4. Brauner Tweed, grob, meliert.
5. Fischgrat in Grau.
6. Hahnentritt schwarz-weiß.
7. Glencheck grau.
8. Leinen naturfarben, mit Knitterfalten.
9. Seersucker blau-weiß gestreift, Kräuselstreifen.
10. Mohair-Mischung mit Glanz.

Kleidungsdetails, quadratisch, Makro, ohne Marke (je 1 Bild):

11. Handgenähtes Knopfloch am Revers.
12. Vier überlappende Ärmelknöpfe aus Horn.
13. Abgesteppte Revers-Kante (Handstich), sehr nah.
14. Leistentasche mit Patte am Sakko.
15. Innenansicht Sakko: Futter, halb gefüttert, ohne Etikett.

Stimmung, Hochformat-Clip (je 1 Clip, Kling 3.0 pro 8 s laut Gedächtnis 10 Credits):

16. Zuschneidetisch von oben: dunkles Tuch, Kreide, Zackenschere, Maßband, Lampenlicht wandert langsam.
17. Schneiderbüste im Halbdunkel, Sakko ohne Ärmel angesteckt, Streiflicht.

Grobe Rechnung: 15 Bilder × 2 = 30 Credits, 2 Clips × 10 = 20 Credits, zusammen etwa 50 Credits; Rest des Rahmens für Wiederholungen bei Fehlern (Schrift, Logo, falsche Hände). Preise vor dem Erzeugen mit `get_cost` prüfen.

## Prüfung nach dem Erzeugen

- Jedes Bild auf Schrift, Logos, Etiketten, Hände prüfen; mit Fund verwerfen.
- Stoffmuster gegen die gezeichnete Bindung halten: Läuft der Grat beim Köper nicht von rechts oben nach links unten oder ist die Bindung erkennbar falsch, wird das Bild nur als Stimmung genutzt, nie neben der Zeichnung als „so sieht es aus“.
- Lizenz und Prompt je Datei in `brands\menswear\assets\higgsfield\LICENSE.md` und `manifest.json` (wie bei Scutoria).

## Einbau

Szenentypen `kw_hook` und `kw_close` bekommen ein optionales Feld `backdrop` (Clip unter einem Schleier) und `kw_flip` ein optionales Feld `photo` (KI-Stoffmuster neben der Zeichnung, Stempel „KI-Bild“). Das baut die Suitwerk-Sitzung, sobald Bilder da sind; die gerechnete Bindung bleibt unberührt.
