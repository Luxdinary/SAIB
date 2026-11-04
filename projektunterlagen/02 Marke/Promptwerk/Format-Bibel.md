# Promptwerk – Format-Bibel „Echtlauf“

Stand: 03.11.2026 (Wien). Status: freigegeben von Stefan, 02.11.2026 (Format „Echtlauf“ und Pilot „Deny-Regeln“), erweitert durch das Testvideo „Dubletten“, freigegeben 03.11.2026. Das Testvideo bringt KI-Realbilder als Einschübe, Ton, wechselnde Szenen und Bildaufbauten je Reihe; wo diese Bibel älteren Regeln widerspricht, gilt der Stand vom 03.11. Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (jede Marke bekommt ein eigenes Format; gemeinsam bleiben nur Technik und Prüfungen). Ersetzt für neue Videos die `Vorlage Promptwerk.md` (animierte Oberflächen, Leitobjekt, Statusleiste, Erklärschicht). Die Vorlage bleibt als Nachweis liegen.

## 1. Versprechen

**Echte Aufgabe, echter Ablauf, echtes Ergebnis, mit Fehlern und Grenzen.**

Claude Code führt in jedem Video eine reale Aufgabe in einem Testordner aus. Der Testordner enthält nur Beispieldaten. Was im Terminal erscheint, ist die aufgezeichnete Ausgabe dieses Laufs, Wort für Wort und in der richtigen Reihenfolge. Wenn etwas scheitert, zeigt das Video das Scheitern. Der Zuschauer sieht nicht, was Claude Code laut Doku können soll. Er sieht, was an einem bestimmten Tag mit einer bestimmten Version passiert ist.

Ein Satz für die Kanalbeschreibung: *„Wir lassen Claude Code echte Aufgaben erledigen und zeigen den ungeschnittenen Ablauf, auch wenn es schiefgeht.“*

Im Bild steht die ganze Zeit oben: **„Echter Ablauf, aufgezeichnet am TT.MM.JJJJ“**, darunter **„Claude Code <Version> · <Modell-ID>“**. Kein Logo und kein Branding von Anthropic, kein Wort „offiziell“. Claude Code wird nur als Name des Werkzeugs genannt.

## 2. Bildsprache

| Element | Regel |
|---|---|
| Grund | Fast schwarz (#0B0C10), leichte Randabdunklung. Keine Partikel, kein Code-Scherben-Hintergrund, kein Leuchten. **Das Protokoll ist das Bild.** |
| KI-Realbilder (ab 03.11.2026) | Erlaubt als gekennzeichnete Einschübe (Szene `rec_photo`): der Arbeitsplatz rund um die Aufgabe, zum Beispiel Schreibtisch, Ausdruck, Hände oder Person von hinten. Regeln:<br>• Nie ein Bildschirminhalt, ein Terminal oder ein Ergebnis; alles am Bildschirm ist echte Aufzeichnung.<br>• Keine Gesichter, keine echten Marken oder Logos, kein lesbarer Text.<br>• Jedes Bild trägt den Stempel „KI-Bild“ / „AI image“; der Stempel „Echter Ablauf“ ist währenddessen ausgeblendet.<br>• Quelle zuerst die Bibliothek `brands\claude_workflows\assets\higgsfield\library\` (Tabelle „Realbilder“ in `Vorlage Bibliothek.md`), dann Testvideo-Material.<br>• Neues Material höchstens 2 Credits je Thema, mit eigener `LICENSE.md` neben `library\`, nie darin. |
| Kamera | Langsame Nahfahrt oder Rückfahrt nur auf KI-Bildern und auf der Antwortkarte; das Terminal selbst bewegt sich nur durch seine Zeilen. |
| Fenster | Flache Terminalfenster mit Haarlinie, Titelzeile nennt den Lauf („Lauf 2: Mit Deny-Regel“). Schrift JetBrains Mono, mindestens 30 px. |
| Farben mit fester Bedeutung | Violett = Werkzeugaufruf (`● Read: .env`), Grau = Werkzeugergebnis (`⎿ …`), Rot = Fehler oder Sperre, Weiß = Antwort von Claude, Bernstein = Hinweis (Beispieldaten, Zeitraffer, offene Läufe). Urteil: Grün oder Rot als Stempel. |
| Zeit | Links neben jeder Zeile die aufgezeichnete Sekunde („4,8 s“). Oben rechts im Fenster „Echtzeit“ oder „Zeitraffer 3ד. Wartezeiten dürfen nur gleichmäßig gerafft werden, mit Einblendung, nie geschnitten. |
| Bewegung | Im Terminal nur Ereignisse aus der Aufzeichnung: eine Zeile erscheint, das Fenster rollt weiter. Dazu das Eintippen des Befehls und der Urteilsstempel. Daneben Szenen, die echte Daten der Aufzeichnung zeigen:<br>• `rec_table`: Datei als Liste mit markierten Zeilen;<br>• `rec_diff`: Zeilenstreifen und Zähler, vorher und nachher;<br>• `rec_answer`: Antwortkarte mit wörtlichen Ausschnitten;<br>• `rec_split`: zwei Läufe nebeneinander.<br>Keine Deko-Animation. Die Bildaufbauten je Reihe stehen im Konzeptplan („Neustart ab 04.11.2026“). |
| Ton (ab 03.11.2026) | Tonebene des gemeinsamen Renderers, Palette `tech`, Stimmung `tech`, Bett 14 dB unter der Stimme (`layout.sound`), Cue-Punkte in `layout.sound_cues`. Geräusche höchstens -16 dBFS Spitze (Stefans Korrektur 03.11.). |
| Dateien | Ausgangsdatei und Ergebnisdatei werden wörtlich gezeigt, mit Zeilennummern. Das Etikett „Beispieldaten, keine echten Zugangsdaten“ ist Pflicht, sobald Werte wie Schlüssel oder Passwörter vorkommen. |
| Stempel oben | Datum, Version, Modell-ID bleiben das ganze Video sichtbar (Ebene `LAYER`, y 192–272). |
| Untertitel | Gemeinsame Technik: Phrasen mit höchstens 4 Wörtern, unten, keine Großschreibung. |
| Logo | Promptwerk-Logo klein oben links, wie bei allen Marken. |

## 3. Dramaturgie (Zielwert 70 s, erlaubt 65–90 s)

| Sekunde | Szene (Typ) | Inhalt |
|---|---|---|
| 0–6 | Auftrag (`rec_auftrag`) | Die Frage, um die es geht („Hält die Sperre?“), der echte Befehl tippt sich ins Terminal, die geplanten Läufe stehen als offene Kästchen mit „?“ darunter. Der erste Satz der Stimme sagt, was getestet wird, nicht was herauskommt. |
| 6–13 | Ausgangslage (`rec_setup`) | Testordner als Dateiliste und eine Datei wörtlich, entscheidende Zeile markiert, Etikett „Beispieldaten“. |
| 13–21 | Regel oder Werkzeug (`rec_rule`), wenn das Thema eine Einstellung hat | Die Datei so, wie sie für den Lauf geschrieben wurde, dazu ein kurzes Zitat aus der Doku mit deutscher Übersetzung. |
| 21–52 | Läufe (`rec_replay`, zwei bis drei) | Je Lauf 9–12 s: Befehl, Werkzeugaufrufe, Ergebnisse, Antwort, mit Zeitstempeln. Am Ende der Urteilsstempel aus der Ergebnisdatei und „Wiederholt: 2 von 2 gleich“. |
| 52–62 | Ergebnis (`rec_result`) | Alle Läufe untereinander mit Urteil und Wiederholungszahl, darunter die Grenze mit Quelle. Auch Läufe, die im Video nicht abgespielt wurden, stehen hier. |
| 62–70 | Protokoll (`rec_protokoll`) | Protokollkarte (Datum und Uhrzeit, Version, Modell, Anzahl Läufe und Wiederholungen, „nur Beispieldaten“), ein Schlusssatz, Abschlusssatz der Marke. |

Stimme: nüchtern, berichtend, „du“. Die Läufe werden in der Vergangenheit erzählt („Claude las die Datei und nannte den Wert“), denn sie sind passiert. Keine Ausrufe, keine Wertungen wie „krass“. Was der Lauf nicht zeigt, sagt die Stimme nicht.

## 4. Wiederkehrende Reihen

1. **Hält das?** – Eine Schutz- oder Regelfunktion aus der Doku wird absichtlich auf die Probe gestellt, bis zur Grenze. Beispiele: Deny-Regel für die `.env` (Pilot), Hook gegen Änderungen an einem Ordner, Planmodus ohne Schreibzugriff, `dontAsk` und unerlaubte Befehle. Ergebnis: wo die Funktion hält und wo nicht.
2. **Eine Aufgabe, ein Lauf** – Eine alltägliche kleine Aufgabe mit Ausgangsdatei und Ergebnisdatei. Beispiele: CSV mit doppelten Kunden bereinigen, 20 Dateinamen nach Datum umbenennen, aus drei Textnotizen eine Tabelle machen, einen Fehler in einem Beispielskript finden und den Test grün machen. Ergebnis: Vorher-nachher der Datei, Dauer, Zahl der Werkzeugaufrufe.
3. **Doku gegen Wirklichkeit** – Ersetzt den „Mythos-Check“. Eine verbreitete Behauptung („Großbuchstaben wirken besser“, „/clear löscht das Gedächtnis“) wird mit zwei Läufen geprüft, die sich nur in diesem einen Punkt unterscheiden. Ergebnis: was der Lauf zeigt, und was er nicht beweisen kann.
4. **Gleicher Auftrag, anderer Schalter** – Derselbe Prompt mit zwei Einstellungen nebeneinander: mit und ohne CLAUDE.md-Regel, Haiku gegen Sonnet, `-p` mit Text gegen JSON-Ausgabe. Ergebnis: Unterschied in Ergebnis, Dauer und Werkzeugaufrufen.

Die Themen im Kalender `claude_workflows_2026-11.json` werden diesen Reihen zugeordnet, sobald Stefan das Format freigibt. Themen, die sich nicht echt ausführen lassen (reine Begriffserklärungen wie „Was ist ein Kontextfenster“), werden zu einer Aufgabe umgebaut oder fallen weg.

## 5. Abgrenzung zu den anderen acht Marken

| Marke | Kern ihres Formats | Was Promptwerk anders macht |
|---|---|---|
| Scutoria | Fälle aus kleinen Betrieben mit Entscheidung und Folge, Erklärsprache mit Markern | Kein Fall und keine Geschichte, sondern ein Protokoll. Keine Marker-Kapseln, keine Erklärschicht. |
| Zonkfruit | Anime-Kinderserie mit Figuren | Keine Figur, keine Handlung, keine KI-Bilder. |
| Dewlane | KI-animierte Beauty-Darstellung mit erfundenen Produkten | Nichts ist erfunden oder generiert außer der Stimme. Das Bild ist eine Aufzeichnung. |
| Revlore | Technik im Schnittbild | Keine Illustration, keine Explosionszeichnung. |
| Gigastruct | Größe und Maßstab von Bauwerken | Kein Maßstab, keine Kamerafahrt. Kleine, überprüfbare Abläufe. |
| Suitwerk | Stilwissen mit Linienillustration | Keine Ästhetik als Inhalt. Mono-Schrift, Terminal. |
| Frontlore | Geschichte mit Archivkarten | Kein Rückblick: ein Lauf von diesem Tag, mit Version. |
| Gritwerk | Motivation, künftig vielleicht Selbstversuche | Am nächsten verwandt (Versuch mit Protokoll), aber technisch und wiederholbar. Keine Person, kein Gefühl. |

Merkmale, die nur Promptwerk hat: Aufnahmestempel mit Version, Zeitstempel je Zeile, Wiederholungszahl, Urteil aus einer Ergebnisdatei, gezeigte Fehler.

## 6. Prüfregeln (zusätzlich zu den gemeinsamen Prüfungen)

1. **Echtheit.** Jede Zeile im Terminalbild kommt aus `transcript.json` der Aufzeichnung. Die Szenen `rec_*` lesen die Datei beim Rendern selbst, der Plan enthält keinen abgetippten Ausgabetext. Lange Werkzeugergebnisse werden nach 3 Zeilen gekürzt, Antworten von Claude nach 7 Bildzeilen (je Szene einstellbar), jeweils mit sichtbarer Zeile „… (n weitere Zeilen)“. Wortlaut wird nie geändert, nur Pfade werden geschwärzt (Testordner wird zu `.`, Benutzerpfade zu `~`).
2. **Reproduzierbar.** Jeder Lauf wird mindestens zweimal aufgezeichnet (`--repeat 2`). Das Ergebnis muss gleich sein (`outcome.json`: `all_reproducible: true`). Schwankt ein Lauf, wird das im Video gesagt („1 von 2 gleich“) oder das Thema wird nicht veröffentlicht. Vor dem Export prüft `record_run.py --check` erneut, wenn die Aufzeichnung älter als 14 Tage ist oder eine neue Claude-Code-Version installiert ist.
3. **Alle Läufe zählen.** Nichts wird so lange wiederholt, bis es passt. Jede Wiederholung steht in `outcome.json`, und auch nicht abgespielte Läufe stehen in der Ergebnisszene.
4. **Zeit ehrlich.** Echtzeit oder gleichmäßiger Zeitraffer mit Einblendung. Reihenfolge und Zeitstempel bleiben wie aufgezeichnet.
5. **Stempel.** Datum, Claude-Code-Version und Modell-ID stehen das ganze Video über im Bild und im Manifest (`echtlauf` in `manifest.json`).
6. **Testordner.** Nur unter `C:\Automation\promptwerk-sandbox\<thema>`, nur Beispieldaten aus der Spezifikation, Werte erkennbar erfunden (zum Beispiel `demo-7f3a-NICHT-ECHT`). Nie Stefans Dateien, Konten, echte Schlüssel oder Netzwerkdienste mit Anmeldung.
7. **Abgeschottet und offen gelegt.** Läufe ohne Benutzereinstellungen, MCP-Server und eigene Befehle (`--setting-sources project,local`, `--strict-mcp-config`, `--disable-slash-commands`). Die vollständige Befehlszeile steht in `meta.json`; die Beschreibung des Posts nennt den Grundbefehl und die Unterschiede je Lauf (Instagram erlaubt 2.200 Zeichen, Prüfrunde 03.11.2026). Gegenprobe vom 02.11.2026: Mit diesen Schaltern kannte der Lauf Stefans persönliche CLAUDE.md nicht, ohne `--setting-sources project,local` schon.
8. **Nur behaupten, was gezeigt wurde.** Allgemeine Aussagen („greift nie“, „immer“) nur mit Quelle aus der Doku. In der Beschreibung steht: Das Verhalten kann sich mit Version und Modell ändern.
9. **Kennzeichnung.** Stimme und Skript sind KI-erzeugt (Label „KI-generiert“, gemeinsame Regel). Die Terminalausgabe ist eine echte Aufzeichnung und wird nicht als „Animierte Darstellung“ bezeichnet. Die feste Zeile im Post kommt aus `brand.yaml` › `production.ai_note`: „KI-generiert sind Stimme, Sprechtext und die als ‚KI-Bild‘ markierten Bilder. Das Terminal ist eine echte Aufzeichnung.“ (seit 03.11.2026).
11. **Lesbarkeit (Prüfrunde 03.11.2026).** Ein Doku-Zitat erscheint nie allein auf Englisch: Die Übersetzung folgt 0,5 s nach dem Zitat. Nebentexte mindestens 24 px, Belege mindestens 28 px (alle Szenen nutzen 30 px oder mehr). Die Szenenzone reicht bis y 1250 (`zone_h` 950, `zone_lower_right_px` 940); unter y 1100 stehen nur schmale Elemente (höchstens 832 px, links von x 940), Terminalfenster enden bei y 1100. Die Ergebnisszene setzt je Lauf zwei Ereignisse (Zeile, dann Urteil) und den Hinweis unten in die Zone. Die deutsche Stimme spricht „Claude“ englisch aus. Die Anweisung in `audio_style.yaml` allein reichte nicht (03.11.: viermal „Cloud“). Seit 03.11. entsteht die deutsche Stimme deshalb über `echtlauf\voice_tts.py --say Claude=Klohd`:<br>• Die Schreibweise gilt nur im TTS-Text; Einblendungen und Untertitel zeigen „Claude“.<br>• Gegenprobe mit Whisper; Ziel ist kein einziges „Cloud“.<br>Englische Aufträge enden mit „Reply in English.“, sonst antwortet Claude bei deutschen Beispieldaten auf Deutsch.
10. **Kosten und Kontingent.** Standardmodell Haiku. Sonnet oder Opus nur, wenn das Thema genau diesen Unterschied zeigt. Ein Lauf sollte unter 60 s bleiben.

Gemeinsam mit allen Marken (unverändert): Gemini-Stimme, Untertitel, Export, `node scripts\overlap_check.mjs` ohne Befund, KI-Kennzeichnung.

## 7. Produktion je Video

1. Spezifikation `brands\claude_workflows\echtlauf\specs\<id>.json`: Testdateien, Läufe (Prompt, Einstellungen, erlaubte Werkzeuge), Prüfwert (`probe`, ein Wert, an dem das Ergebnis erkennbar ist).
2. Aufzeichnen: `.venv\Scripts\python.exe brands\claude_workflows\echtlauf\record_run.py brands\claude_workflows\echtlauf\specs\<id>.json --repeat 2`. Ergebnis in `echtlauf\recordings\<id>\`. Voraussetzung: Die Claude-CLI im Terminal ist angemeldet (`claude auth status`). Aufgezeichnet wird mit der neuesten installierten Version: Die `claude` im PATH war am 02.11.2026 noch 2.1.142, deshalb lief der Pilot über `PW_CLAUDE_BIN` mit dem Build 2.1.309 aus dem Ordner der Desktop-App. `--rebuild` baut `transcript.json` aus den gespeicherten Rohdaten neu, ohne neuen Lauf.
3. Aufzeichnung lesen, dann erst das Skript schreiben. Die Stimme erzählt, was im Protokoll steht.
4. Plan `data\direction\<video_id>.json` mit `layout.format: "echtlauf"`, `layout.echtlauf.recording: "<id>"`, `layout.explainer: false`, Szenen `rec_*`.
5. Trockenlauf mit `--tts mock --no-render`, dann Render über die Warteschlange mit Gemini, Überschneidungsprüfung, Sichtprüfung, Export nach `05 Produktion`.
6. Englische Fassung (seit 02.11.2026): eine eigene Aufzeichnung mit englischen Prompts und Dateien (`"language": "en"` in der Spezifikation, Kennung `<id>-en`). Stempel, Fensterzeilen und Protokoll erscheinen dann englisch. Eine deutsche Aufzeichnung wird nie englisch vertont. Englisch wird schneller gesprochen: für 65–90 s rund 210–260 Wörter, deutsch rund 165–200.

Weitere Felder der Spezifikation: `files` je Lauf (zum Beispiel eine CLAUDE.md nur in Lauf 2, `null` lässt eine Datei weg), `probe_where` (`answer`, `file:<pfad>`, `files`, `tool`), `same_keys`, `extra_args` (zum Beispiel `--mcp-config`), `setup_cmds`, `drop_isolation`. Im Plan: `probe_good` (Treffer ist das gewünschte Ergebnis), `metric` in `rec_result` (zum Beispiel `input_tokens`), `state: "after"` und `max_rows` in `rec_setup`, `file` in `rec_rule`.

## 8. Offene Punkte für Stefans Freigabe

- Formatname „Echtlauf“ und der Kanalsatz in Abschnitt 1.
- Ob die vollständige Spezifikation (Testdateien und Befehle) öffentlich zum Nachmachen bereitgestellt wird, zum Beispiel als Text in der Beschreibung. Das würde das Versprechen „nachprüfbar“ stärken.
- Umgang mit Läufen, die schwanken: zeigen („1 von 2“) oder Thema verwerfen.
- Zuordnung der bestehenden 42 Pläne von Woche 1: Die bezahlten Stimmen passen nicht zu echten Läufen, weil der Sprechtext aus dem Protokoll entsteht. Sie bleiben als Vorrat, werden aber für dieses Format voraussichtlich nicht verwendet.
