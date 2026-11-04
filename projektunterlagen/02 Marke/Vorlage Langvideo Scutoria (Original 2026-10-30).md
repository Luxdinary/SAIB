# Vorlage: ein weiteres Video parallel in der animierten Erklärwelt bauen

Stand 30. Oktober 2026, abends. Für Stefan und für einen zweiten Claude-Chat. Ziel: Ein weiteres Video (zum Beispiel Video 02) bekommt denselben Schnitt, dasselbe Layout und dieselbe Bildsprache wie Video 01, ohne dass sich die beiden Chats in die Quere kommen.

## 1. Was du tun musst

1. Im Code-Tab der Claude-App eine neue Sitzung im Ordner `C:\Users\Stefa\OneDrive\scutoria` öffnen. Nur dort gelten automatisch `CLAUDE.md`, die Markenregeln (Skill `scutoria-brand`) und die Werkzeuge.
2. Den Text aus Abschnitt 7 einfügen und die Videonummer eintragen. Mehr nicht.
3. Am Ende das Video ansehen und eine Note geben, wie bei der Probe.

## 2. Was vorhanden sein muss

| Was | Wo | Stand |
|---|---|---|
| Freigegebenes Skript EN und DE | `marketing/youtube/SKRIPTE/NN-slug.en.md` und `.de.md` | Video 01 bis 10 liegen vor |
| Tonspur je Sprache, zwei Dateien (Abschnitte 1 bis 3, 4 bis 7) | Flash: `C:\Users\Stefa\Videos\scutoria\NN-slug\stimme\`; Lite-Probe: `C:\Users\Stefa\Videos\scutoria\lite\NN-slug\stimme\` | Nur Video 01 ist vertont (Lite). Video 01 und 02 werden am 31. Oktober mit Flash vertont |
| Bausteine der Bildwelt | `marketing/youtube/ANIMATION/lib/welt.js` | seit 30. Oktober; wird mit Video 01 erweitert |
| Aufnahme Bild für Bild, Ton dazu | `marketing/youtube/ANIMATION/rendern.mjs` | fertig |
| Wortzeiten aus der Tonspur | `marketing/youtube/ANIMATION/woerter.py` (Whisper large-v3, lokal, auf dem Prozessor) | fertig |
| Muster mit Note 1 | `ANIMATION/probe-01/` (Szene, Storyboard, Gestaltungsblatt) | fertig |
| Muster für ein ganzes Video | `ANIMATION/video-01/` (Szene, ein Akt je Skriptabschnitt) | im Bau |
| Gestaltungsauftrag | `C:\Users\Stefa\Videos\scutoria\01-ai-rules-start\Produktionsprompt-Darstellung-Scutoria.de.md` | dein Auftrag vom 30. Oktober |

Ohne Tonspur kann der zweite Chat schon Storyboard und Szenen bauen, aber keine Zeiten binden. Für Video 02 gibt es zwei Wege:

- **Empfehlung: heute mit der Lite-Stimme vertonen.** Das sind vier Anfragen im kostenlosen Kontingent des Lite-Modells; heute wurden dort vier von zehn verbraucht. Der Chat speichert in den Ordner `lite\`, damit der Flash-Lauf morgen nichts überschreibt. Morgen werden nur die Wortzeiten neu ermittelt, die Szene bindet sich von selbst neu.
- **Oder bis morgen warten.** Dann kommt die Flash-Stimme aus dem geplanten Lauf am 31. Oktober, und der Chat beginnt mit Storyboard und Szenen ohne Zeiten.

## 3. Das gemeinsame Layout (fest)

**Bild:** 1920 × 1080, 30 Bilder je Sekunde, H.264 (crf 17), Ton AAC 192 kbit/s. Seitenrand links und rechts 96 px.

**Feste Einblendungen**, alle aus `welt.js`, nie von Hand nachgebaut:
- Oben links der Kopf: Kicker in IBM Plex Mono, 24 px, blau, gesperrt, zum Beispiel „2 · DIE LAGE IM KLEINEN BETRIEB“. Darunter der Titel in Manrope 800, 60 px. Funktion `kopf(ab, bis, kicker, titel)`.
- Oben rechts immer „SYNTHETISCHE STIMME“ (EN „SYNTHETIC VOICE“), Mono 18 px.
- Unten links der Marker als Kapsel: Form und Wort, nie Farbe allein. Fakt ist ein blaues Quadrat, Auslegung eine violette Raute, Unsicher ein bernsteinfarbener Halbkreis, Lücke ein roter gestrichelter Kreis. Funktion `marke(ab, bis, art, quelle)`.
- Darunter die Quellenleiste über die ganze Breite: „Quelle: …“ wörtlich aus dem `[QUELLE]` des Skripts, mit Abrufdatum, Mono 22 px, ein- oder zweizeilig. Sie steht, solange der belegte Absatz gesprochen wird. Auslegung zeigt nur den Marker.
- Im Einstieg unten links ab Sekunde 0: „Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung“.
- Inhalt der Szene zwischen y 220 und y 860, solange Kopf und Marker stehen. Bei Nahfahrten wird der Kopf zurückgenommen (`dimmen`).

**Bildwelt „Nachtarchiv“:** dunkler Raum mit ruhigen Archivregalen. Das einzige Licht ist Papier: Memo, Register, Regeln und Eingaben sind helle Blätter. Werkzeuge und Bildschirme leuchten blau. Keine Bildschirmfotos der Website; Seiten werden als vereinfachte Blätter nachgebaut, nur mit dem Ausschnitt, der gerade erklärt wird.

**Figuren ohne Gesicht.** Die Rolle erkennt man an Silhouette, Kleidung und Werkzeug. Für den erfundenen Betrieb Muster Elektrotechnik gilt eine feste Besetzung: Büro mit kurzem Haar und grauem Hemd, Büro mit Dutt und braunem Hemd, Montage mit Helm, Reflexstreifen und Telefon, dazu Inhaberin und Lehrling. Die Figuren handeln: tippen, zeigen, halten, reichen weiter.

**Farben mit fester Bedeutung:** Blau für den aktiven Vorgang und den betrieblichen Weg. Bernstein für Offenes und Unklares, dann gestrichelt. Rot nur für ein Risiko. Grün nur für einen erreichten Zustand. Violett nur für den Marker Auslegung. Kein Schutzschild, kein grünes Zertifikat, kein Countdown, kein Konfetti.

**Schrift:** nur Manrope und IBM Plex Mono, aus `site/public/fonts`. Beschriftungen im Bild mindestens 26 px, nur Schlagworte.

**Bewegung:** jede Bildaktion hängt an einem gesprochenen Wort, `cue('…')`; keine geschätzten Zeiten. Kleine Reaktionen um 0,3 s, Objektaktionen 0,6 bis 1,2 s, mit Beschleunigung und Abbremsung. Übergänge über ein Objekt: Ein Punkt öffnet sich als Kreis zur nächsten Szene (`kreis`), Rückweg mit `kreisRaus`. Sonst Überblendung (`blende`, 0,7 s) oder Kamerafahrt. Bei Nahfahrten wird der Rand abgedunkelt.

**Text und Recht:** Der Sprechtext bleibt unverändert. Beispielwerte sind erfunden und so markiert, Adressen nur mit der Endung `.example`. Nie „compliant“, „zertifiziert“, „sicher“ als Versprechen. Am Ende 20 Sekunden ruhiges Endbild.

## 4. Arbeitsablauf im zweiten Chat

Alle Befehle von `C:\Users\Stefa\OneDrive\scutoria` aus. `NN-slug` ist zum Beispiel `02-security-questionnaire`.

1. **Lesen:** `CLAUDE.md`, Skill `scutoria-brand`, den Gestaltungsauftrag, `ANIMATION/probe-01/STORYBOARD.md`, den Kopf von `ANIMATION/lib/welt.js` (alle Bausteine sind dort beschrieben) und `ANIMATION/video-01/` als Muster.
2. **Tonspur**, nur wenn keine da ist und Stefan den Lite-Weg will:
   ```
   node marketing/youtube/VORLAGEN/vertonen.mjs --skript marketing/youtube/SKRIPTE/NN-slug.en.md --voice Charon --model gemini-3.8-flash-lite-tts --out C:\Users\Stefa\Videos\scutoria\lite --env C:\Automation\faceless-network\.env
   ```
   Dasselbe mit `.de.md`. Der Schlüssel bleibt in `C:\Automation\faceless-network\.env`, wird nie ausgegeben und nie in den Scutoria-Ordner kopiert.
3. **Wortzeiten** je Sprache:
   ```
   python marketing/youtube/ANIMATION/woerter.py --sprache de --aus C:\Users\Stefa\Videos\scutoria\NN-slug\animation --js marketing/youtube/ANIMATION/video-NN/woerter-de.js <stimme>\01-03-de.wav <stimme>\04-07-de.wav
   ```
   Dauert auf dem Prozessor einige Minuten je Sprache; im Hintergrund starten.
4. **Storyboard** `ANIMATION/video-NN/STORYBOARD.md` im Format der Probe: Zeit, Gesprochen, Erklärziel, Bildhandlung, Ergebnisbild, Text im Bild; dazu Abweichungen und offene Punkte.
5. **Szene:** `video-01/szene.html` nach `video-NN/` kopieren, die Liste `TEILE` anpassen. Je Skriptabschnitt eine Datei `teil-N.js` mit einem Akt:
   ```js
   akt({ name: 'einstieg', bauen() {
     const b = buehne('buero'); this.buehnen = [b]; this.b = b;
     this.t1 = at({ de: 'Ihre Belegschaft', en: 'Your staff' });   // Wortanker, in Sprechreihenfolge
     shot(b, this.t1 - 0.4);                                         // ab wann die Bühne zu sehen ist
     kopf(this.t1, this.t1 + 8, { de: '1 · EINSTIEG', en: '1 · OPENING' }, { de: 'Titel', en: 'Title' });
   }, zeichnen(t) { kamera(this.b, [960, 540], 1); /* Bewegungen mit P(), pop(), rein(), fahrt() */ } });
   ```
   Jede Beschriftung als `{ de, en }`, damit eine Szene beide Sprachen trägt.
6. **Prüfen:** Fehlen Wortanker?
   ```
   node marketing/youtube/ANIMATION/rendern.mjs --szene marketing/youtube/ANIMATION/video-NN/szene.html --lang de --pruefen
   ```
   Dann Standbilder an den kritischen Stellen (`--standbilder 12.5,30,61.2 --ordner …`) ansehen: keine Überdeckung, Kopf, Marker und Quelle lesbar, nichts außerhalb des Rands.
7. **Rendern**, erst Deutsch, dann Englisch:
   ```
   node marketing/youtube/ANIMATION/rendern.mjs --szene marketing/youtube/ANIMATION/video-NN/szene.html --lang de --ton C:\Users\Stefa\Videos\scutoria\NN-slug\animation\ton-de.wav --aus C:\Users\Stefa\Videos\scutoria\NN-slug\animation\NN-slug.de.mp4 --parallel 6
   ```
   Für eine Probe zuerst nur einen Ausschnitt mit `--von` und `--bis`.
8. **Abgabe:** Video an Stefan schicken, nur den eigenen Ordner `ANIMATION/video-NN/` committen, Log-Eintrag in Google Drive schreiben.

## 5. Regeln, damit sich die Chats nicht stören

- Der zweite Chat ändert nur `ANIMATION/video-NN/` und Dateien unter `C:\Users\Stefa\Videos\scutoria\NN-slug\`.
- `lib/welt.js`, `rendern.mjs` und `woerter.py` werden nur gelesen. Fehlt ein Baustein, kommt er in `video-NN/bausteine.js` und wird im Bericht genannt; der Chat von Video 01 übernimmt ihn später in die Bibliothek. Die Bibliothek wird nur erweitert, nie umgebaut, damit fertige Szenen weiter laufen.
- `LIESMICH.md`, `STAND.md`, `AUFGABEN.md` und die Skripte bleiben unberührt; Ergebnisse stehen im Storyboard und im Bericht.
- Vor jedem Commit nach API-Schlüsseln suchen (Muster `AIza` mit 35 Zeichen). Commit nur mit `git add marketing/youtube/ANIMATION/video-NN`.
- Drei Tore bleiben: kein Geld, kein Recht live, nichts veröffentlichen, keine Konten. Gelöscht wird nichts; was weg soll, kommt nach `C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`.

## 6. Grenzen, die du kennen solltest

- Der Aufwand ist Handarbeit von Claude. Für ein Video von 13 Minuten sind mehrere Arbeitssitzungen zu erwarten (Schätzung, nicht gemessen).
- Zwei Chats rechnen gleichzeitig auf demselben Rechner. Whisper und das Rendern teilen sich die 24 Prozessorkerne; beides läuft dann langsamer.
- Die Bibliothek ist frisch. Wenn der zweite Chat auf einen Fehler darin stößt, meldet er ihn, statt ihn selbst zu ändern.

## 7. Text zum Einfügen in den neuen Chat

```
Baue Video NN (Skript marketing/youtube/SKRIPTE/NN-slug.de.md und .en.md) als animierte Erklärwelt im selben Schnitt, Layout und Design wie Video 01.
Lies zuerst marketing/youtube/ANIMATION/VORLAGE-PARALLEL.md und halte dich an alle Regeln dort, besonders Abschnitt 5: Du änderst nur ANIMATION/video-NN/ und nichts an lib/welt.js, rendern.mjs, woerter.py, LIESMICH.md oder den Skripten.
Tonspur: [Lite heute vertonen | auf die Flash-Stimme vom 31. Oktober warten].
Reihenfolge: Storyboard, dann ein Ausschnitt von 60 Sekunden zur Abnahme, dann das ganze Video Deutsch, dann Englisch.
Schick mir den Ausschnitt, bevor du weiterbaust. Nichts veröffentlichen, keine Konten, kein Geld.
```
