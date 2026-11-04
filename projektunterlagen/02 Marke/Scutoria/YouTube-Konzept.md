# Scutoria – YouTube-Konzept Langvideo (Fassung 1.0, Entwurf zur Freigabe)

Stand 02.11.2026, Sitzung „Scutoria YouTube“. Grundlage: Stefans Vorgabe vom 02.11.2026 (Langvideos 15–25 min, Reels als Ausschnitte daraus und eigene Reels 65–95 s, mindestens 10 Videos, 3 sofort, 7 in Planung), der freigegebene Ausgabeplan `01 Idee und Strategie\Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md` (Abschnitte 3 und 4), deine Originalvorlage `02 Marke\Vorlage Langvideo Scutoria (Original 2026-10-30).md`, die Format-Bibel „Was tust du?“ und das Kanalkonzept `OneDrive\scutoria\marketing\youtube\KONZEPT.md` vom 29.10.2026.

Umsetzung im Code: `C:\Automation\faceless-network\brands\ai_security\longform\` (eigener Composer der Marke, siehe Abschnitt 6).

## 1. Versprechen

Ein Langvideo beantwortet **eine** Frage, die ein kleiner Betrieb tatsächlich gestellt bekommt, so gründlich, dass man danach weiß, was man diese Woche tut. Mit Quelle und Datum am Bildschirm, offenen Punkten beim Namen, ohne Angst und ohne Verkauf als Rettung. Der Claim bleibt „Belegt. Datiert. Vorzeigbar.“

Was das Langvideo von den Reels unterscheidet: Reels zeigen **einen** Moment und **einen** Schritt. Das Langvideo zeigt den **ganzen Weg**: die Lage, die Schritte in Reihenfolge, was davon Pflicht ist und was Auslegung, zwei Entscheidungsfälle im Stil „Was tust du?“, und am Beispielbetrieb, wie das fertige Dokument aussieht.

## 2. Aufbau eines Langvideos in Minuten

Richtwert für ein Video von 20 Minuten. Bei 15 oder 25 Minuten wachsen oder schrumpfen nur die Kapitel 2 bis 4; Einstieg, Kapitel 5 bis 7 bleiben fast gleich lang.

| Zeit (20 min) | Kapitel | Inhalt | Szenentypen |
|---|---|---|---|
| 0:00–0:50 | **0 Kaltstart** | Ein Beispielfall öffnet wie im Reel: Uhrzeit, Ort, das Objekt kommt herein (Mail, Fragebogen, Chatfenster). Die Frage des Videos in einem Satz, dann was das Video liefert. Ab Sekunde 0 unten links „Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung“. | `case`, `statement` |
| 0:50–1:20 | **Überblick** | Kapitelkarte mit den 5 bis 6 Kapiteln, damit der Zuschauer springen kann (YouTube-Kapitel decken sich damit). | `chapters` |
| 1:20–4:00 | **1 Die Lage** | Wie die Lage in einem Betrieb ohne IT-Abteilung aussieht, am Beispielbetrieb; warum das zählt (erste Belege). | `paper`, `statement`, `broll` |
| 4:00–9:30 | **2 Der Weg** | Die Schritte in Reihenfolge, je Schritt: was, wer, wie lange, woran man merkt, dass es fertig ist. Der Kern des Nutzens. | `steps`, `paper`, `compare` |
| 9:30–13:00 | **3 Was gilt** | Die Rechtslage und Fachquellen, je Aussage mit Marker Fakt, Auslegung, Unsicher oder Lücke und Quellenleiste. Was offen ist, wird gesagt. | `quote`, `statement`, `compare` |
| 13:00–16:30 | **4 Was tust du?** | Zwei Entscheidungsfälle: Situation, drei Optionen mit Denkpause, Folge einer falschen Wahl an der Uhr, der richtige Schritt. Das ist die Brücke zu den Reels. | `case`, `choice`, `timeline`, `step` |
| 16:30–18:30 | **5 Der Beispielbetrieb** | Muster Elektrotechnik e.U. (erfunden, 10–49 Beschäftigte, Österreich): das fertige Dokument als Papierkarte, Abschnitt für Abschnitt. | `paper`, `steps` |
| 18:30–19:20 | **6 Was es nicht ist** | Keine Rechtsberatung, kein Audit, kein Zertifikat; die offenen Punkte des Themas. | `statement`, `compare` |
| 19:20–20:00 | **7 Verweis und Schluss** | Erst das freie Memo oder Tool, dann das Toolkit mit einem Preissatz, dann gesprochen „Hier ist Scutoria … synthetische Stimme … keine Rechtsberatung“. Danach 20 s ruhiges Endbild (Endscreen-Fläche). | `close` |

Tempo und Rhythmus:
- Sprechtempo Gemini Charon gemessen: DE 16,5 Zeichen/s, EN 15,7 Zeichen/s. 20 min DE sind etwa 18.500 Zeichen Sprechtext (etwa 2.500 Wörter), EN etwa 17.600 Zeichen (etwa 2.900 Wörter).
- Ein Bildereignis spätestens alle 10 s (Wortanker `@Wort`), ein Szenenwechsel spätestens alle 45 s, ein Zwischenschnitt (Higgsfield-Clip) etwa alle 2–3 min als Atempause.
- Kapitelwechsel mit eigener Kapitelkarte (Nummer, Titel, 3 s), YouTube-Kapitelmarke auf dieselbe Sekunde.

## 3. Bild und Layout (16:9)

Übernommen aus deiner Originalvorlage, auf den Renderer übertragen. 1920 × 1080, 30 fps, H.264, AAC.

| Ebene | Regel |
|---|---|
| Kopf oben links | Kicker in IBM Plex Mono 24 px, blau, gesperrt („2 · DER WEG“), darunter der Kapiteltitel in Manrope 800, 56 px. Steht 8 s nach jedem Kapitelwechsel, danach nur der Kicker. |
| Oben rechts | „SYNTHETISCHE STIMME“ / „SYNTHETIC VOICE“, Mono 18 px, dauerhaft. |
| Unten links | Marker als Kapsel (Form und Wort): Fakt blaues Quadrat, Auslegung violette Raute, Unsicher bernsteinfarbener Halbkreis, Lücke roter gestrichelter Kreis, Beispiel graues Quadrat. |
| Unten | Quellenleiste über die Breite, „Quelle: …“ wörtlich aus `[QUELLE]` mit Abrufdatum, Mono 22 px, solange der belegte Absatz gesprochen wird. |
| Inhalt | zwischen y 200 und y 900, Seitenrand 96 px. Ein dominantes Motiv je Szene. Papier (`#fbfbfd`) ist das einzige Helle. |
| Grund | `#0b1120`, flach, Haarlinienraster, kein Glühen, kein Verlauf. Higgsfield-Clips der Bibliothek liegen unter einem Schleier (0,62), ohne Schrift und ohne Marken. |
| Farben mit Bedeutung | Blau aktiv, Bernstein offen (gestrichelt), Rot nur Risiko und Endpunkt der Folge, Grün nur erreichter Zustand, Violett nur Auslegung. Kein Schild-Klischee, kein Countdown, kein Konfetti. |
| Untertitel | im Langvideo **nicht** eingebrannt; YouTube bekommt eine SRT-Datei je Sprache aus den Wortzeiten. In den Reels eingebrannt (Phrasen bis 4 Wörter). |
| KI-Kennzeichnung | „Synthetische Stimme“ dauerhaft oben rechts, Einstiegszeile ab Sekunde 0, gesprochen im Schluss; in der Beschreibung „KI-generiert (Stimme, Grafik, Hintergrundclips)“ und bei YouTube „Veränderte oder synthetische Inhalte“ nach `KENNZEICHNUNG.md`. |

Szenentypen der Vorlage (Daten je Szene im Plan, Zeiten als Wortanker): `chapter` (Kapitelkarte), `chapters` (Überblick), `statement` (Kernsatz mit Marker), `paper` (Dokument als Papierkarte, Zeilen erscheinen und werden markiert), `steps` (nummerierte Schritte, der aktive blau), `compare` (zwei Spalten), `quote` (kurzes Zitat aus der Quelle mit Herkunft, höchstens 25 Wörter), `case` (Uhr, Ort, Objekt), `choice` (A/B/C mit Denkbalken), `timeline` (Folge an der Uhr), `step` (der richtige Schritt, falsche durchgestrichen), `broll` (Zwischenschnitt mit einem Schlagwort), `close` (Verweis und Endbild).

## 4. Reels aus dem Langvideo

**Grundsatz: nativ im Hochformat aus denselben Szenen gerendert, nicht ausgeschnitten.** Jede Szene ist Code mit Daten; der Composer kennt zwei Layouts (16:9 und 9:16) und baut dieselbe Szene für 1080 × 1920 neu auf: Papierkarten stehen untereinander statt nebeneinander, die Zeitleiste läuft senkrecht, Schrift größer, Untertitel eingebrannt. Das Bild ist scharf und kostet keine Credits.

- Je Langvideo **4–6 Reels**, je eines aus Kapitel 1 bis 5 (Kapitel 4 liefert meist zwei, weil es zwei Fälle hat).
- Länge **65–95 s**. Ein Reel ist eine zusammenhängende Strecke von Szenen im Plan (`reels[].beats`), geschnitten an Szenengrenzen. Ton ist derselbe Abschnitt der Tonspur, keine neue Vertonung.
- Am Anfang 0,0 s kein Logo-Intro: die erste Szene muss als Hook taugen (meist `case` oder `statement`). Am Ende 3 s Schlusskarte „Ganzes Video: Scutoria auf YouTube“ und „Quellenbasiert. Keine Rechtsberatung.“
- Plattformzonen wie in der Format-Bibel: Inhalt y 290–1100, Untertitel unten bei y ~1380, nichts unter y 1620.
- Dateiname: `<Datum> <Kurztitel> – Reel <n> <Thema> 9x16.mp4`.
- Die eigenständigen Reels von 65–95 s laufen weiter im Format „Was tust du?“ (Woche 1, eigene Sitzung).

## 5. Thumbnail-Regeln

1280 × 720 PNG, aus Code gesetzt (Vorlage `longform\thumbnail.py`), Hintergrund aus Higgsfield.

1. Links bis 55 % der Breite: höchstens **fünf Wörter** in Manrope 800, 92–110 px, weiß auf `#0b1120`, ein Wort darf blau sein.
2. Rechts: **ein Motiv** (Higgsfield-Bild, Schreibtisch, Dokument, Bildschirm ohne Schrift), weich in den dunklen Grund auslaufend, kein Gesicht, keine Hände in Nahaufnahme, keine Marke, keine lesbare Schrift.
3. Oben links Videonummer in Mono („01“), unten links „Stand Nov. 2026“ in Mono 30 px (das Datum ist Teil des Versprechens).
4. Scutum-Marke klein unten rechts, nie größer als 64 px.
5. Verboten: Pfeile, Kreise um Dinge, rote Warnflächen, Schreckgesichter, Totenkopf, Kapuze, „SCHOCK“, Ausrufezeichen, Versalien-Sätze.
6. Lesbar bei 168 × 94 px (Prüfung: verkleinerte Vorschau im Kontaktbogen).
7. Je Video 3 Entwürfe (Motiv A/B/C), Stefan wählt einen; die EN-Fassung nutzt dasselbe Motiv mit englischem Text.

## 6. Technik und Ablauf

- **Plan je Video und Sprache:** `brands\ai_security\longform\plans\<NN>-<slug>.<de|en>.json` mit Quellen, Kapiteln, Szenen (Sprechtext, Szenentyp, Daten, Marker, Quelle) und den Reel-Strecken.
- **Vertonung:** Gemini (Charon), eine Anfrage je Kapitel, Kosten im Kostenprotokoll. Wortzeiten mit Whisper large-v3.
- **Render:** je Kapitel ein HyperFrames-Projekt und ein eigener Auftrag in `scripts\render_queue.py` (damit andere Marken dazwischen drankommen), danach Verkettung mit ffmpeg ohne Sperre, Lautheit −16 LUFS. Reels je eines ein Auftrag. Langvideos nachts (`longform\night_run.py`). Gemessen: Render-Faktor 1,06–1,37 der Laufzeit.
- **Prüfung:** HyperFrames-Check, `overlap_check.mjs` je Kapitel, Längen- und Textgrenzen, Quellen mit Datum.
- **Export:** `05 Produktion\Scutoria\JJJJ-MM\JJJJ-MM-TT Kurztitel\04 Export\…– YouTube 16x9.mp4` (DE und EN), Reels `… 9x16.mp4`, Thumbnail in `05 Thumbnail und Cover`, SRT in `06 Untertitel`, Kapitel und Beschreibung in `Veröffentlichung.md`.

## 7. Die 10 Videos

Grundlage: `OneDrive\scutoria\marketing\youtube\THEMEN.md` und `SKRIPTE\01–10` (freigegeben 29.10.2026, je 10–15 min). Jedes Skript wird ausgebaut; ausgebaute Skripte sind eine **neue Fassung** und brauchen deine Freigabe vor der Veröffentlichung.

| Nr. | Titel (DE) | Ziel-Länge | Stand | Begründung der Länge |
|---|---|---|---|---|
| 01 | Ihre Belegschaft nutzt schon KI. Womit die Regeln anfangen. | 17–18 min | **sofort** | sechs Schritte plus zwei Fälle (Kundenmail im Chat, Richtlinie in der Schublade) |
| 02 | Ihr Kunde schickt einen Sicherheitsfragebogen. So antworten Sie ehrlich. | 17 min | **sofort** | fünf Schritte, vier Antwortarten, Quellen, zwei Fälle (Frage 23, Vertragsklausel) |
| 04 | Was nie in ein KI-Tool darf. Fünf Datenarten und die Zweifelsregel. | 16–17 min | **sofort** | fünf Datenarten, zwei Tools, zwei Fälle (Tiefgaragen-Code, Krankmeldung) |
| 03 | Belegt. Datiert. Vorzeigbar. Ein Rundgang durch beide Toolkits. | 15 min | Planung | braucht die fertige Website (Bildschirmbilder der echten Seiten) |
| 05 | Artikel 4 der KI-Verordnung: die Einweisung und der Nachweis | 18 min | Planung | Pflicht und Auslegung, Muster-Einweisung |
| 06 | MFA, Sicherung, Updates: wonach jeder Fragebogen zuerst fragt | 22 min | Planung | drei Themen mit je Schritten und Fall |
| 07 | Müssen Sie kennzeichnen, was Ihre KI erzeugt? Artikel 50 | 18 min | Planung | eng umrissene Regel, viele Grenzfälle |
| 08 | Die erste Stunde nach einem Cybervorfall, und die 72-Stunden-Uhr | 20 min | Planung | Ablauf an der Uhr, ideal für Fälle |
| 09 | Sieben Fragen, bevor Sie ein KI-Tool freigeben | 20 min | Planung | sieben Fragen je etwa 2 min |
| 10 | Sind wir von NIS2 betroffen? Und warum Ihre Kunden trotzdem fragen | 25 min | Planung | Prüffragen, Größen, Sektoren, Lieferkette |

Längen der ersten drei: geschätzt aus dem Trockenlauf mit Sprechtempo Charon (02.11.2026), genaue Werte nach der Vertonung. Sie liegen unter den ursprünglich geschätzten 20–22 min, weil der freigegebene Wortlaut unverändert bleibt und nur Kaltstart, Überblick und das Kapitel „Was tun Sie?“ neu dazukommen; länger würde es nur durch neuen, wieder freizugebenden Text.

Die ersten drei: **01, 02, 04** wie im Ausgabeplan vorgeschlagen. 03 rückt in die Planung, weil es die echten Seiten von scutoria.com zeigt.

**Stand 02.11.2026 abends (Vorgabe Stefan über die Hauptsitzung):** bis 05.11.2026 sind 01 und 02 fertig, zuerst Deutsch, Englisch wenn der Render-Platz reicht, je Video die Reels. 04 ist fertig geplant (DE und EN) und folgt danach. Weil Higgsfield-Videos gerade nicht fertig werden, laufen beide Videos mit Standbildern aus der Bibliothek und Kamerafahrt im Code; Clips ersetzen sie später.

Geplante Veröffentlichung (Annahme, abhängig vom Live-Gang der Website, PLAN.md): 01 am Di 17.11.2026, 02 am Di 24.11.2026, 04 am Di 01.12.2026; DE und EN am selben Tag. Ordnernamen in `05 Produktion` tragen diese Daten.

## 8. Higgsfield (Block B, 550 Credits)

| Posten | Menge | Credits (geplant) |
|---|---|---|
| Probe | 2 Startbilder + 2 Clips + 1 Thumbnail-Hintergrund | höchstens 55 |
| Bibliothek 16:9 | 24 Zwischenschnitte zu 8 s mit Startbild (Büro, Werkstatt, Praxis, Dokumente, Bildschirme ohne Marken und ohne lesbare Schrift) | 24 × (10 + 2) = 288 |
| Einstellungen für 01, 02, 04 | 12 Clips zu 8 s mit Startbild | 12 × 12 = 144 |
| Thumbnail-Entwürfe | 10 Videos × 3 Hintergründe, 4K | 120 |
| Summe | | 552, Grenze ohne Rückfrage 605 (+10 %) |

Nachweis je Erzeugung (Job-Nummer, Modell, Prompt, Credits) in `brands\ai_security\assets\higgsfield\LICENSE.md`. Stil: Grund #0b1120, Akzent #4f8cff, kein Glühen, ruhige Kamera, keine Gesichter, keine Schrift. Hinweis zum Kanalkonzept vom 29.10. („keine KI-Bilder von Personen, Orten oder Szenen“): durch deine Entscheidungen vom 30.10. (Higgsfield-Clips als Hintergrund) und 02.11. (Ausgabeplan) überholt; es bleibt bei Hintergründen ohne erkennbare Personen, gekennzeichnet.

## 9. Offene Fragen an dich

1. **Anrede.** Die freigegebenen Langskripte und die Website sagen „Sie“, die Reels seit 30.10. „du“. Vorschlag: Langvideos bleiben bei „Sie“ (Inhaber, B2B, wie Website und Toolkits); die Reels aus dem Langvideo übernehmen das „Sie“, weil es dieselbe Tonspur ist. Die eigenen Reels bleiben bei „du“. Alternative: alles auf „du“, dann werden die Langskripte beim Ausbau umgeschrieben.
2. **Vorhandene Animationen.** 01 und 02 gibt es schon als handanimierte Erklärwelt (Fassung 2, je etwa 13 min, `C:\Users\Stefa\Videos\scutoria\…\animation\`). Vorschlag: Sie bleiben als Vorrat; die neuen Langvideos entstehen mit der Vorlage aus Abschnitt 6, weil sie ohne Handarbeit je Video wiederholbar ist.
3. **Freigabe der ausgebauten Skripte** vor der Vertonung oder erst am fertigen Video? Vorschlag: Vertonung und Render ohne Warten, Freigabe am fertigen Video (Neuvertonung kostet etwa 0,10 USD je Video und Sprache).
