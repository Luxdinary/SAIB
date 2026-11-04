# Scutoria YouTube · Testvideo 01 DE neu (Konzept)

Stand 02.11.2026, nachts, Sitzung „Scutoria YouTube“. Auftrag: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md` (Abschnitt 5) und Codex-Bericht vom 01.11. Kein Render ohne Go der Hauptsitzung, keine Gemini-Anfrage (die Stimmen von 01 DE liegen vor: 8 Kapitel, Flash, Charon, zusammen 15:24 min Sprechzeit).

## 1. Alt gegen neu: Was das Video der Vorwoche hatte und dem neuen fehlt

Verglichen: `C:\Users\Stefa\Videos\scutoria\01-ai-rules-start\animation\01-ai-rules-start.animiert.fassung2.de.mp4` (31.10., 13:51 min) gegen `05 Produktion\Scutoria\2026-11\2026-11-17 KI-Regeln\…YouTube 16x9.mp4` (02.11., 16:10 min), je 24 bzw. 15 Standbilder.

| Das alte Video hatte | Das neue Video hat |
|---|---|
| **eine Welt:** Bürohaus im Schnitt mit Räumen, Stadtsilhouette, Archivregale; jede Szene spielt an einem Ort | Text- und Papierkarten auf dunklem Raster, dazwischen Fotos unter Schleier, aber keinen Ort, an dem etwas passiert |
| **Figuren, die handeln** (ohne Gesicht): Büro tippt, Monteur hält das Telefon, Person geht zur Regel, Lehrling, Inhaberin | keine Figuren |
| **Vorgänge statt Aufzählungen:** Datenwege mit wandernden Punkten, Zugang über privates und betriebliches Konto als Weg, Name wird geschwärzt und die Person bleibt erkennbar (rote Linien) | dieselben Inhalte als Liste oder Zwei-Spalten-Karte |
| **Prozesslandschaft** der sechs Schritte mit Stationen, die sich nacheinander öffnen (Kreisübergang in die Station, Rückweg) | nummerierte Liste |
| **Symbole und Institutionen** (Gebäude für DSK, BSI, WKO; Paragraf, Kalender, Ordner), Kurven, Diagramm „Maßnahmen gegen KI-Kompetenz“, Kreis „Überprüfen“ | ein Zitatkasten je Quelle |
| **Kamera:** Fahrten und Nahfahrten in die Welt, Rand abgedunkelt | Bild steht; nur Ein- und Ausblenden |
| **Übergänge:** Kreis öffnet sich über einem Objekt, Überblendung, Kamerafahrt | ein einziger Übergang (Ausblenden, Kapitelkarte) |
| **Takt:** etwa alle 2–4 s ein Bildereignis an einem Wort | oft 8–15 s lang dieselbe Karte, Zeilen tauchen nur auf |
| Ton: nur Stimme | Ton: nur Stimme |

Was das neue Video besser macht und bleibt: Kaltstart mit Fall und Uhr, Kapitelüberblick, Kapitel „Was tun Sie?“ mit zwei Fällen, Kapitelmarken und SRT, Reels im Hochformat, Thumbnails, Render je Kapitel über die Warteschlange, Überschneidungs-Prüfung.

Ton: Beide Videos haben nur die Stimme (Pausen unter −55 dB gemessen, kein Musikbett, keine Geräusche). Stefans Kritik am Ton gilt also für beide; der Ton kommt jetzt neu dazu.

## 2. Weg: die alte Bildwelt in den Composer holen

**Empfehlung:** Die Akte der Vorwoche (`ANIMATION\video-01\teil-*.js`, gebaut auf `lib\welt.js`, `lib\betrieb.js`, `lib\dokumente.js`) werden je Kapitel als **eigene Szene „welt“ im Composer** abgespielt. Das Bild entsteht dann aus denselben Akten wie in der Vorwoche, aber im neuen Rahmen: Warteschlange, Überschneidungs-Prüfung, Tonebene des gemeinsamen Renderers, Kapitel, Reels, Thumbnails.

So geht es technisch:
1. **Kopie, nicht Umzug:** `lib\*.js` und `video-01\*.js` werden nach `brands\ai_security\longform\welt\` kopiert (Stand 31.10.2026, Quelle und Datum im Kopf). Der Ordner in `scutoria` bleibt unverändert.
2. **Antrieb:** `welt.js` rechnet jedes Bild aus der Zeit (`render(t)`, reine Funktion). Der Composer legt die SVG-Bühne als Clip ins HyperFrames-Projekt und setzt eine GSAP-Zeitleiste darauf, die bei jedem Schritt `render(t)` ruft. Damit sieht HyperFrames die Welt wie jede andere Szene. Eine Probe von 20 s klärt vor dem Bau, ob das so trägt. Rückfallweg: Bild mit dem alten `rendern.mjs` aufnehmen und den Ton im Composer daruntermischen.
3. **Wortzeiten:** Die Akte suchen ihre Anker im gesprochenen Text (`at({de: …})`). Weil der freigegebene Wortlaut unverändert ist, passen die Anker; die Zeiten kommen aus den neuen Whisper-Wortzeiten je Kapitel (`storage\longform\yt01-ai-rules-start-de\voice\c*.words.json`) im Format `window.WOERTER`.
4. **Zuordnung Kapitel zu Akt:**

| Kapitel (neu) | Bild | Herkunft |
|---|---|---|
| c0 Kaltstart, Fall „DI 09:12“ | **neuer Akt** in der Welt: Kamera fährt ins Büro des Bürohauses, Figur Büro A tippt, Mail fliegt als Blatt in das Chatfenster, die Zeile mit den Kundendaten färbt sich bernstein; dazu Uhr | neu, auf `betrieb.js` |
| c0 Frage des Videos | Akt 1 der Vorwoche (Einstieg) | `teil-1.js` |
| c0 Überblick | **neuer Akt:** Prozesslandschaft von oben, die sieben Kapitel als Stationen, Kamera fährt sie ab | neu, auf `dokumente.js` (Weg) |
| c1 Die Lage | Akt 2 | `teil-2.js` |
| c2 Sechs Schritte | Akte 3a–3c (Prozesslandschaft, Stationen) | `teil-3a/3b/3c.js` |
| c3 Gesetz | Akt 4 | `teil-4.js` |
| c4 Was tun Sie? | **neue Akte:** Fall 1 im Büro (Reklamation, Fotos, privates Telefon), A/B/C als drei Wege, die sich vor der Figur gabeln, Folge als Weg mit Uhrzeiten, der falsche Weg endet rot, der richtige leuchtet blau; Fall 2 mit Fundstück in der Schublade und dem Weg der Bekanntgabe | neu |
| c5 Beispielbetrieb | Akt 5 | `teil-5.js` |
| c6 Was es nicht ist | Akt 6 | `teil-6.js` |
| c7 Memo, Toolkit, Schluss | Akt 7 + Endbild 20 s | `teil-7.js` |

5. **Kopf, Marker, Quellenleiste** kommen aus `welt.js` (HUD) wie in der Vorwoche. Die Kopfzeile oben rechts zeigt „KI-GENERIERT · SYNTHETISCHE STIMME“ statt nur „SYNTHETISCHE STIMME“, wie mit der Hauptsitzung vereinbart.
6. **Reels und Thumbnails** bleiben aus dem neuen Composer (Hochformat aus den Szenendaten), bekommen aber Ton und je Reel einen realistischen Higgsfield-Einschub. Die Bildwelt der Akte ist auf 16:9 gebaut; ein Hochformat der Welt wäre ein eigener Umbau und gehört nicht zum Test.

## 3. Mehr Animation und Variation als in der Vorwoche

Zusätzlich zu den alten Akten, gemessen am Plan, nicht geschätzt:
- **Realistische Einschübe:** je Kapitel ein Higgsfield-Bild als Zwischenschnitt (4–6 s) mit eigener Bewegung: langsame Fahrt plus Lichtlauf über das Papier. Ab Kling echte Clips. Der Schnitt in den Einschub und zurück läuft über ein Objekt (Blatt, Telefon, Ordner), damit Welt und Foto zusammenhängen.
- **Vier Übergangsarten** statt einer: Kreis über einem Objekt (alt), Kamerafahrt durch das Bürohaus (alt), Wischblende entlang eines Datenwegs (neu), harter Schnitt auf den realistischen Einschub mit Geräusch (neu).
- **Neue Akte** für Kaltstart, Überblick und die zwei Fälle (Abschnitt 2) mit Figuren, Wegen und Uhr; das waren im neuen Video die flachsten Stellen.
- **Takt-Prüfung:** längste Strecke ohne Bildereignis höchstens 6 s (Vorwoche etwa 4 s, neues Video bis 15 s); der Composer meldet Überschreitungen.

## 4. Higgsfield (Kappe 100 Credits)

Vorhanden und frei verwendbar: 36 Bibliotheksbilder und 30 Thumbnail-Hintergründe vom 02.11. (216 Credits, schon bezahlt). Neu nur, was die Bibliothek nicht hat: realistische Momente mit Menschen von hinten oder Händen, ohne Gesicht, ohne lesbare Schrift, ohne Marken.

| Nr. | Motiv (Einschub in Kapitel) | Art | Credits |
|---|---|---|---|
| 1 | Hände auf einer Laptop-Tastatur im Büro bei Nacht, Bildschirm unscharf (c0 Kaltstart) | Bild 2K | 2 |
| 2 | Monteur von hinten mit Helm, Telefon in der Hand, Baustelle in Dämmerung (c1, c4) | Bild 2K | 2 |
| 3 | Aushang an einer Werkstatt-Pinnwand, Blatt ohne lesbare Schrift, Hand drückt Pin fest (c2 „eine Seite“) | Bild 2K | 2 |
| 4 | Kleine Einweisung im Werkstattbüro, drei Personen von hinten vor einem Blatt (c2 Einweisung) | Bild 2K | 2 |
| 5 | Unterschrift unter ein Dokument, nur Hand und Stift (c2 Richtlinie) | Bild 2K | 2 |
| 6 | Kundin-Reklamation: Fotos einer Küchensteckdose auf einem Tisch ausgedruckt (c4 Fall 1) | Bild 2K | 2 |
| 7 | Schublade wird geöffnet, darin ein geheftetes Dokument, Hand im Bild (c4 Fall 2) | Bild 2K | 2 |
| 8 | Inhaberin von hinten am Schreibtisch, liest ein Blatt (c5) | Bild 2K | 2 |
| 1–6 als Clip | dieselben Motive als 8-s-Kling-Clip, erst wenn Kling läuft | Kling pro | 6 × 10 = 60 |
| Reserve | Nachbesserung bei Schrift oder Gesicht im Bild | | 24 |
| **Summe** | | | **100** |

Bilder sofort nach Go der Hauptsitzung, Clips erst nach ihrer Meldung „Kling läuft“. Jede Erzeugung mit Job, Prompt und Credits in `brands\ai_security\assets\higgsfield\LICENSE.md`.

## 5. Ton-Cues je Kapitel

Klangfarbe Scutoria: ruhig, trocken, Papier und Büro statt Science-Fiction. Kein Alarm, keine Sirene, kein Bass-Drop. Musikbett: leiser, langsamer Synth-Teppich (etwa 70–80 BPM), unter der Stimme abgesenkt, nur mit Lizenznachweis in `08 Recht und Verwaltung\Lizenzen`. Cue-Punkte stehen im Plan als Wortanker (`"@Wort"`) mit Geräuschnamen. Die Namen sind Vorschläge an die gemeinsame Tonebene.

| Kapitel | Cues |
|---|---|
| alle | `whoosh_soft` beim Kapitelwechsel und Kreisübergang; Musikbett ein, unter Sprache −18 dB, in Pausen −12 dB |
| c0 Kaltstart | `keys_typing` (2 s) beim Tippen, `paper_slide` wenn die Mail ins Chatfenster fliegt, `tick` beim Färben der Zeile |
| c0 Überblick | `swipe` je Station (7 ×, leise) |
| c1 Lage | `paper_slide` Memo, `click` je Antwort, `stamp_soft` beim Marker „Fakt“ |
| c2 Sechs Schritte | `whoosh_soft` je Station, `pin` beim Aushang, `pen_sign` bei der Unterschrift, `click` je Regelbereich |
| c3 Gesetz | `stamp_soft` je Marker, `swipe` je Institution |
| c4 Was tun Sie? | `clock_tick` unter der Uhr (leise), `pop` je Option A/B/C, Musik setzt 2,5 s aus in der Denkpause, `thud_low` (kein Alarm) am roten Endpunkt, `chime_soft` beim richtigen Schritt |
| c5 Beispielbetrieb | `drawer` beim Ordner, `paper_slide` je Paragraf |
| c6 Was es nicht ist | `swipe`, sonst nur Musik |
| c7 Schluss | Musik steigt im Endbild leicht an und läuft 20 s aus |

## 6. Was das Testvideo von den anderen Marken unterscheidet

Gezeichnete Welt eines kleinen Betriebs mit Figuren ohne Gesicht und Papier als einziges Licht, dazu Entscheidungen mit Uhr und Folge. Keine andere Marke hat eine durchgehende Welt mit Akten, keine nutzt die Marker Fakt, Auslegung, Unsicher und Lücke im Bild. Die realistischen Einschübe zeigen Büro und Werkstatt bei Nacht und keine Produkte, Bauwerke oder Stoffe.

## 7. Aufwand, Reihenfolge, Freigaben

1. Probe „welt im Composer“ (20 s aus Akt 2 mit neuen Wortzeiten), kein Render ohne Go. Vorbereitung ohne Render jetzt möglich.
2. Neue Akte (Kaltstart, Überblick, zwei Fälle): geschätzt 1–2 Arbeitssitzungen. Das ist eine Schätzung, nicht gemessen.
3. Higgsfield-Bilder (Abschnitt 4), Cue-Punkte in den Plan.
4. Nach Go und Tonebene: Render je Kapitel über die Warteschlange (Faktor beim neuen Composer 0,7–1,9; die Welt-Akte rechnen mehr, Messung mit der Probe), Reels, Export.

Offene Fragen an Stefan (über die Hauptsitzung):
- Dürfen realistische Einschübe Menschen von hinten und Hände zeigen (ohne Gesicht)? Das Kanalkonzept vom 29.10. schloss KI-Bilder von Personen aus; die Neustart-Vorgaben verlangen Realitätsnähe. Vorschlag: ja, ohne Gesicht.
- Anrede bleibt „Sie“ wie im freigegebenen Skript (Vorschlag).
- Musikquelle für das Bett (nur mit Lizenznachweis): Wahl durch Stefan oder die Hauptsitzung.
