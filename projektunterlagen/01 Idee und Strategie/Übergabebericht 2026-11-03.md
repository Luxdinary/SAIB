# Übergabebericht: KI-Kurzvideo-Netzwerk (Business „Video und Social Media“)

Stand: 03.11.2026, 20:30 (Wien). Verfasst von Claude (Hauptsitzung in Claude Code, Desktop-App) für eine nachfolgende KI ohne Zugriff auf den bisherigen Chat. Dieser Bericht ersetzt den Übergabebericht vom 30.10.2026 (`01 Idee und Strategie\Übergabebericht 2026-10-30.md`), der für den Zeitraum 29.10. bis 30.10.2026 weiterhin gilt und hier nur zusammengefasst wird. Zeitraum dieses Berichts: 31.10.2026 bis 03.11.2026, mit Schwerpunkt auf dem 02.11. abends und dem 03.11.2026.

Alle Angaben stammen aus dem Chat der Hauptsitzung, aus den Meldungen der Nebensitzungen, aus Dateien auf Stefans Laptop und aus Abfragen der angebundenen Dienste. Wo etwas unsicher ist, steht es ausdrücklich dabei. Es stehen keine Passwörter, Schlüssel oder Tokens in diesem Bericht, nur ihre Ablageorte.

Hinweis zur Zeit: Der Laptop läuft in Beiruter Zeit (Stefan ist im Auslandseinsatz). Datei-Zeitstempel sind eine Stunde später als Wiener Zeit (Beirut UTC+2, Wien UTC+1). In diesem Bericht ist jede Uhrzeit Wiener Zeit, sofern nicht anders vermerkt. In Bash auf dem Laptop wirkt `TZ=` nicht; Wiener Zeit ist `date -u` plus eine Stunde.

---

## 1. Ziel und Zweck des Projekts

### 1.1 Was gebaut wird

Ein Netz aus neun getrennten Nischenmarken, die auf TikTok, Instagram Reels und YouTube Shorts KI-erzeugte Erklärvideos von 65 bis 90 Sekunden veröffentlichen, auf Deutsch und Englisch auf demselben Konto je Marke. Eine Marke (Scutoria) produziert zusätzlich lange YouTube-Videos von 15 bis 25 Minuten, eine andere (Tintora) eine Anime-Kinderserie. Die Produktion soll so weit wie möglich automatisch laufen: Themen aus einem Konzeptplan, Regie-Skript, Vertonung, Render, Prüfung und Export ohne Handarbeit; die Veröffentlichung später über den Dienst Upload-Post zu festen Uhrzeiten. Seit dem 03.11.2026 übernimmt ein „Tagesläufer“ (Skript im Code, Modellaufrufe über Claude Code im Abo) das Schreiben der Regie-Skripte, das bis dahin neun Claude-Code-Sitzungen von Hand erledigt haben.

### 1.2 Hintergrund

- Stefan Dallinger, Wohnsitz Österreich, Angehöriger des Österreichischen Bundesheeres, derzeit im Auslandseinsatz (Zeitzone Beirut). Bestehendes Business Scutoria (Informationssicherheit, Compliance und KI für kleine Betriebe; Website scutoria.com; eigener Ordner `C:\Users\Stefa\OneDrive\scutoria` mit eigener `CLAUDE.md`).
- Auslöser war das System eines Kollegen mit mehreren TikTok-Kanälen aus KI-Videos (HTML-Bauplan „Faceless-Maschine“ in `01 Idee und Strategie\Recherche`). Einzelheiten zu Herkunft, Faktencheck und Namensrecherche im Übergabebericht vom 30.10.2026.
- Scutoria ist zugleich eine der neun Videomarken; das Vorhaben läuft neben Scutoria.

### 1.3 Stefans Motivation (aus seinen Aussagen)

- Zusätzliches Einkommen, „so automatisiert wie möglich“; getrennte Kanäle, damit Werbepartner je Nische buchen können.
- TikTok Creator Rewards sind in Österreich nicht verfügbar; alles so bauen, dass Rewards aktivierbar sind, sobald sie verfügbar werden, ohne VPN oder fremden Wohnsitz.
- Realitätsnähe und Abwechslung sind ihm wichtiger als Menge. Seine Kritik vom 02.11.2026 (Schulnote 4 von 5) hat zu einem Neustart geführt; danach hat er alle neun Testvideos und das Scutoria-Langvideo freigegeben (03.11.2026).

---

## 2. Stefans Anforderungen, Vorgaben, Regeln und Präferenzen

### 2.1 Globale Regeln (aus `C:\Users\Stefa\.claude\CLAUDE.md`, Google Drive › Claude-Gedächtnis › `00 START.md`)

- Immer auf Deutsch antworten, keine Emojis, sachlich und präzise. „Nichts erfinden, auch nichts Kleines. Nicht Belegtes heißt ‚nicht ermittelbar‘ mit Grund.“
- Claude löscht nichts. Was weg soll, kommt nach `C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>`.
- Keine Zugangsdaten, Konto- oder Vertragsnummern in Dateien, Dateinamen, Logs oder Chats.
- Das Gedächtnis liegt in Google Drive › Claude-Gedächtnis (`00 START.md`, `Übersichten`, `Frühere Fassungen`, `Archiv`, `Claude-System`), nie lokal. Inhalte liegen in OneDrive. `OneDrive\Notizen` und `C:\Obsidian` sind aufgelöst, nie lesen oder anlegen.
- Entscheidungen trägt Claude sofort in die Übersicht in Google Drive ein (Datei `Übersicht — Business (Video und Social Media).md`, Verfahren in Abschnitt 5.7).
- Die Ordnerstruktur wird nur nach Vorschlag und Freigabe durch Stefan geändert.
- Wird eine Aktion vom System abgelehnt, nicht erzwingen, sondern Stefan melden.

### 2.2 Regeln für diesen Arbeitsordner (`C:\Users\Stefa\OneDrive\Business\CLAUDE.md`)

Nur Inhalte (Skripte, Rohmaterial, Grafiken, Pläne) liegen hier; der gültige Stand steht in der Drive-Übersicht. Ordner `00 Eingang` bis `08 Recht und Verwaltung`. Musik, Bilder und Clips nur mit geklärter Lizenz, Nachweis in `08 Recht und Verwaltung\Lizenzen`. Je Video ein Ordner `05 Produktion\<Marke>\<JJJJ-MM>\<JJJJ-MM-TT Kurztitel>` mit `01 Skript`, `02 Rohmaterial`, `03 Schnittprojekt`, `04 Export`, `Veröffentlichung.md`; Status im Redaktionsplan: Idee, Skript, Dreh, Schnitt, fertig, geplant, veröffentlicht, verworfen.

### 2.3 Stefans Vorgaben aus der Kritik vom 02.11.2026 (wörtlich, Schreibweise original)

„Schulnote 4 von 5. Das gehört überarbeitet. Ich will haben, zu jeder Mark: 1. 50 Video und Themenplan pro Mark 2. 2 Videos und englisch und das selbe die auf deutsch also gesamt 4 Videos pro Tag pro Marke 3. Realisitsche Darstellung, unterschideliche Varaitionen der animationen und Vorlagen, die Videos sind alle gleich und das soll ncith so sein. 4. scutoria video für youtube hat sich extrem verschlechtert. 5. hast du nicht die ChatGPT beurteilung berücksichtigt? … 6. Pausiere alles, starte erneut mit von jeder marke test video zur freigabe. 7. Nutzt higgsfield.“

Einzelurteile (sinngemäß, teils wörtlich): Scutoria YouTube „hast du das alte video noch und die vorlage dazu? es fehlat ja uach komplett deine musik oder geräusche die das video lebendig machen die ein swip oder wish etc.“; Dewlane „fehlen backround geräusche wie swips und wishes, sowie auch animationen wie man crems auftägt also echte bilder (jedoch mittels KI erstellt)“; Revlore „sollte eher ein technik channel werden“; Gigastruct „fehlen sounds und generell wirkt es sehr ki generiert“; Suitwerk „fehlen ebenfalls sound und es wird nie ein echter anzug gezeigt, ich will realitätsnähe haben. einen animierten realen anzug“.

### 2.4 Kurzentscheidungen Stefans vom 03.11.2026 (wörtlich, in dieser Reihenfolge)

| Uhrzeit (Wien) | Frage | Antwort Stefan |
|---|---|---|
| 05:25 | Menschen in KI-Bildern | „Ja, ohne Gesichter“ (Hände und Menschen von hinten erlaubt, nie Gesichter) |
| 05:41 | Musikbett | „Vorerst selbst erzeugt“ (prozedural im Renderer) |
| 11:55 | Freigabe der neun Testvideos | „Alle freigeben“, dann: „jedoch sind die wish geräusch ebz teils soundeffekte zu laut.“ |
| 13:03 | Verteilung des Higgsfield-Restguthabens | „Vorschlag so“ |
| 13:19 | Geräuschpegel nach der Suitwerk-Hörprobe | „Passt“ |
| 16:30 | Scutoria-YouTube-Zwischenprobe | „Ja, rendern“ |
| 16:39 | Claude-Kontingent | „Sonnet + Tagesläufer“ |
| 16:45 | Nachtrag dazu | „Änderung, wir machen es über den normalen ultra plan“ (kein API-Schlüssel) |
| 18:44 | Tagesläufer-Prototyp | „Ja, so produzieren“ |
| 19:59 | Scutoria-YouTube-Video 01 DE | „Passt“ |

Außerdem am 03.11.: „wie viele Videos haben wir jetzt gesamt, mache einen umfassenden Bericht für ChatGPT“ (erledigt, Abschnitt 5.4) und die Frage „Wann würde ein automatischer Ablauf ohne externe Tools laufen? Wie können wir dann User Limit von Claude sparen?“ (beantwortet, Grundlage der Entscheidung „Sonnet + Tagesläufer“).

### 2.5 Stehende Regeln für die Produktion (Stand 03.11.2026)

- Nur Gemini-Stimmen: Flash (`gemini-2.5-flash-preview-tts`) als Standard, Pro (`gemini-2.5-pro-preview-tts`) nur als Ausweich und immer für ganze Videos, Tintora nur Pro. Keine Windows-Stimme, kein `gemini-3.8-flash-tts` (liest Regieanweisungen mit).
- KI-Bilder und Clips: Hände und Menschen von hinten ja, keine Gesichter, immer als KI-Darstellung gekennzeichnet; keine echten Marken oder Logos, kein lesbarer Text in Bibliotheksbildern; keine KI-Bilder realer, benannter Bauwerke als Foto ausgeben.
- Jedes Video als KI-Inhalt gekennzeichnet, synthetische Stimme ausgewiesen; Quellenpflicht mit Markern Fakt, Auslegung, Unsicher, Lücke.
- Musikbett und Geräusche nur selbst erzeugt im Renderer; Lizenzmusik später nur mit Nachweis.
- Geräuschpegel: Standard für Sweeps -16 dBFS Spitze; Marken dürfen leiser (-18, -19), nie lauter.
- Higgsfield-Credits nur innerhalb freigegebener Kappen (Abschnitt 7.1); Tagesläufer bucht nie.
- Risiko „hoch“ (Dewlane, Frontlore) bleibt Freigabe von Hand durch Stefan.
- Nichts veröffentlichen, keine Konten anlegen, kein VPN, kein Commit ohne Stefans Auftrag.
- Takt: 2 Themen je Tag und Marke, jedes DE und EN (gilt seit der Freigabe; am 04.11. 1 Thema je Marke wegen des Claude-Kontingents).

### 2.6 Was Stefan ausdrücklich nicht will

- Videos, die alle gleich aussehen; „animierte Präsentation“ statt Reel; abstrakte Flächen, wo der Zuschauer ein echtes Bild erwartet.
- Zu laute Wisch-Geräusche und Effekte.
- API-Schlüssel für die Modellaufrufe des Tagesläufers („über den normalen Ultra-Plan“).
- VPN oder fremder Wohnsitz für TikTok Rewards; Unbelegtes; Löschen durch Claude.

---

## 3. Chronologischer Verlauf

### 3.1 29.10. bis 30.10.2026 (Zusammenfassung, Einzelheiten im Übergabebericht vom 30.10.)

Arbeitsumgebung und Gedächtnis angelegt, Faktencheck, Konzept, Ablaufplan, Fragenkatalog (25 Antworten Stefans), Namensrecherche (PromptPilot, VelvetGlow, TorqueLab ausgeschlossen), Repository `C:\Automation\faceless-network` mit vollständiger Kette Skript → TTS → Whisper → HyperFrames → FFmpeg NVENC → Prüfung → Export, Regie-System statt Folien, Scutoria-Fassungen A bis A3.1 auf dem echten Scutoria-Design, Higgsfield Starter gebucht (8 Clips, 96 Credits). Entscheidungen: Laptop statt Mac mini, kein VPN, Publisher Upload-Post, Gemini-Stimme, Anrede „du“ im Scutoria-Video, Länge 65–90 s.

### 3.2 31.10. bis 01.11.2026 (laut Drive-Übersicht und Dateien)

- 30./31.10.: Qualitätsrunde für alle neun Marken (`02 Marke\Qualitätsrunde 2026-10-31.md`); Scutoria-Video als Maßstab (Note 1,7), übrige Marken Note 3. Schnitt- und Layout-Vorlage aus Stefans Langvideo-Vorlage für alle Marken (`02 Marke\Schnitt und Layout Kurzvideo (alle Marken).md`). Alle acht übrigen Marken in je einer Claude-Code-Sitzung.
- 31.10.: Scutoria-YouTube-Video 01 „KI-Regeln“ erste Fassung auf der Bildwelt „Nachtarchiv“ (`C:\Users\Stefa\Videos\scutoria\01-ai-rules-start\animation\01-ai-rules-start.animiert.fassung2.de.mp4`, Stefan: Note 1).
- 01.11.: Stefan gibt die Testvideos aller neun Marken frei (`brand_version 1.0`), danach Themen- und Kalenderpläne aller neun Marken für 09.11. bis 06.12.2026 (je 84 Themen). Takt damals 6 Posts je Konto und Tag (3 DE, 3 EN). Codex-Bericht (ChatGPT) mit Konzeptkritik liegt vor (`Recherche\Codex-Bericht 2026-11-01 Konzeptkritik.md`): jede Marke braucht eigenes Versprechen, eigene Bildsprache und Dramaturgie.

### 3.3 02.11.2026

- Neuausrichtung (`01 Idee und Strategie\Neuausrichtung 2026-11-02.md`): Videos zu ähnlich, jede Marke bekommt ein eigenes Format (Format-Bibeln in `02 Marke\<Marke>\Format-Bibel.md`). Zonkfruit wird Tintora (Anime-Kinderserie „Juna und die Insel der verlorenen Farben“, Handle @tintora.tv; Marken-ID im Code bleibt `brainrot`). Welle 1 (Scutoria, Tintora) und Welle 2 (Dewlane, Revlore, Gigastruct) gestartet; Piloten freigegeben („Alle Videos freigegben“); Gritwerk „Laborbuch“ und Frontlore „Rekonstruktion“ freigegeben; Prüfrunde abgeschlossen (`02 Marke\Prüfrunde 2026-11-03.md`, Noten 1,8 bis 2,7, Tintora 3,0).
- Google Workspace `admin@scutoria.com` als Zentrale („1+8“), Aliase je Marke geplant, Markenkonten noch nicht angelegt.
- Higgsfield Ultra gebucht (3.000 Credits für November) mit Ausgabeplan (`Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md`: Tintora 1.300, Scutoria YouTube 550, Bibliotheken 660, Reserve 490). Kling-Ausfall etwa 15:30 bis 22:00 Wien, hängende Aufträge erstattet.
- Gemini: Flash-Tageslimit 100 Anfragen für das ganze Projekt um 19:30 erschöpft; Stefan gibt Pro als Ausweich frei („Ja, als Ausweich“, Tintora „Ganz Pro“). AI Influencer Studio (Higgsfield) für Tintora getestet (2 Credits): unbrauchbar.
- Alte Videos der ersten Woche (21 Ordner im alten Format) nach `Documents\_zum_loeschen\2026-11-02 Alte Videos` verschoben (Stefan: „kann man löschen“).
- 22:00: Stefans Kritik (Abschnitt 2.3): Pause aller zehn Produktionssitzungen, Neustart mit einem Testvideo je Marke. Auftrag an alle Sitzungen: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md` (Abschnitte 1 bis 9; Abschnitt 10 ist der Verlauf des 03.11.). Kappen: 100 Credits je Marke, Tintora 200, zusammen höchstens 1.000.

### 3.4 03.11.2026 (Kernstück dieses Berichts)

| Zeit | Ereignis | Begründung oder Ergebnis |
|---|---|---|
| 00:00–05:00 | Testvideo-Konzepte je Marke (`02 Marke\<Marke>\Testvideo-Konzept 2026-11.md`; Scutoria getrennt „… Reels …“ und „… YouTube …“ nach einer Dateikollision), Higgsfield-Bilder und Kling-Clips innerhalb der Kappen (etwa 132 Credits für Konzeptbilder) | Stefans Vorgabe Realitätsnähe über Higgsfield |
| 05:25 / 05:41 | „Ja, ohne Gesichter“; „Vorerst selbst erzeugt“ | Gesichter vermeiden Deepfake-Nähe und Rechtefragen; eigene Musik vermeidet Lizenzfragen |
| bis 07:30 | Eigene Sitzung „Tonebene“ baut `src\fn\render\sound.py` und `sound_synth.py`: 12 prozedurale Geräusche in `assets\sfx\` (LICENSE.md), prozedurales Musikbett mit Absenkung beim Sprechen, Cues aus Beats, Bildereignissen und Plan, Prüfungen `sfx_peak`, `sfx_stem_peak`, `music_bed_level`, `music_license`, `sound_cues`; lineares loudnorm; Doku `docs\direction-system.md` Abschnitt 6i. 07:50 Go für Render und Export | Stefans Kritik „kein Ton“ |
| 07:50–10:40 | Neun Testvideos gerendert und Stefan geschickt (Frontlore „Fackeltelegraf“, Suitwerk „Köper und Leinwand“, Scutoria „Chef-Mail“, Gritwerk „Willenskraft“, Dewlane „Testmenge“, Tintora Testreel F1-06, Revlore „Sicherungsautomat“, Gigastruct „Fehmarnbelt Absenken“, Promptwerk „Dubletten“); zusammen etwa 616 Credits, Scutoria-YouTube-Vorbereitung 80 Credits | Freigabe je Marke durch Stefan |
| 10:51 | Drive-Übersicht auf Stand gebracht; Gedächtnisnotiz zum Drive-Verfahren (`textContent` statt Base64, Größenkappe) | Abo-Regel „Entscheidungen sofort in die Übersicht“ |
| 11:55 | „Alle freigeben“ und „Wisch-Geräusche zu laut“ | Tonebene-Sitzung hatte den Standard um 11:57 von -9 auf -16 dBFS gesenkt (Stefan hatte es ihr direkt gesagt); alle Marken rendern neu und bauen die englische Fassung aus denselben Szenen |
| 11:57–13:16 | Alle neun Marken: deutsche Neufassung und englische Fassung exportiert, alle Prüfberichte bestanden, keine neuen Credits. Sechs Marken setzen -18 oder -19 dBFS, weil überlappende Cues den Geräusch-Stem sonst über -16 heben. Promptwerk behebt die Aussprache „Claude“ (Sprechtext „Klohd“, Whisper hört 4-mal „Claude“, 0-mal „Cloud“). Gigastruct entschärft zwei Clip-Schwächen durch Beschnitt | Takt 2 + 2 setzt englische Fassungen voraus |
| 12:39 | Vorfall: Bibliotheken-Sitzung überschreibt beim Neubau der Revlore-Bibliothek die `LICENSE.md` und entfernt Revlores Testvideo-Abschnitte; Revlore-Render T3 scheitert an der Lizenzprüfung. Behoben: Revlore legt `assets\higgsfield\testvideo\` mit eigener `LICENSE.md` an, Bibliotheken-Skript sichert vorher und erhält fremde Zeilen. Regel: eigenes Marken-Material nie in `library\` | Lizenzprüfung ist Pflicht vor jedem Export |
| 13:03 | Budget neu verteilt („Vorschlag so“): 1.416 Credits: Bibliotheken Rest 214, Tintora Folge 1 500, Scutoria YouTube 250, Tagesproduktion 300 (33 je Marke bis 30.11., höchstens 2 je Thema), Reserve 152 | alter Plan passte nicht mehr ins Guthaben |
| 13:19 | Pegel „Passt“; Tintoras gekürzter Plan freigegeben (acht Hochformat-Reels mit je 5 Kling-Clips, erwartet 434 Credits; 16:9-Folge im Dezember) | 500 Credits reichen nicht für die ganze Folge |
| 13:45 | Bibliotheken für alle sieben Reel-Marken fertig: je 17 bis 29 fotorealistische Nano-Banana-Bilder und ein Kling-Clip (Dewlane 46, Suitwerk 46, Gigastruct 48, Revlore 46, Frontlore 72, Gritwerk 74, Promptwerk 68 Credits), Ablage `brands\<id>\assets\higgsfield\library\` | Material für die Tagesproduktion ohne neue Credits |
| 13:25–17:00 | Stand und Bericht für ChatGPT (`01 Idee und Strategie\Bericht für ChatGPT 2026-11-03.md`); Claude-Wochenkontingent nach einem Tag bei 63 % (13:25), 74 % (17:00), 78 % und Fable 82 % (17:45) | Grund für die Umstellung |
| 16:30 | Zwischenprobe Scutoria YouTube (2:28 min) freigegeben; ganzes Video 01 DE gerendert (16:38 min Renderzeit), 18:03 exportiert | Zweiter Trockenlauf mit Ton war fertig |
| 16:39 / 16:45 | „Sonnet + Tagesläufer“, dann „über den normalen ultra plan“: neun Marken-Sitzungen auf Sonnet 5.5, Takt am 04.11. halbiert, Meldungen gebündelt, neue Sitzung „Tagesläufer“ gestartet | Kontingent sparen |
| 16:45–18:44 | Tagesläufer: Bestandsaufnahme (`docs\daily-runner.md`), `claude -p` headless geprüft, erster Modellaufruf 261 s mit 37.000 Ausgabe-Token, danach Aufwand „low“ (etwa 10.000 Ausgabe-Token je Fassung, 25 s), Prototyp Suitwerk Nr. 2 „Super 100s“ DE und EN exportiert und bestanden; Aufbauten-Entwürfe je Marke (`brands\<id>\aufbauten.yaml`), von sieben Marken-Sitzungen geprüft und korrigiert, Revlore liefert Aufbau F „Kennlinie“ mit 10 Themen und geprüften Quellen | Produktion ohne Sitzungen |
| 17:45 | Notbremse: keine Produktion durch die Marken-Sitzungen am 04.11., kein Trockenlauf aller Marken am Abend, Tagesläufer-Sitzung auf Sonnet | Kontingent 78 % |
| 18:44 | „Ja, so produzieren“: erster echter Tagesläufer-Lauf am 04.11. ab 09:05 Wien eingeplant (startet selbst), ein Thema je Marke DE und EN | Freigabe des Prototyps |
| 19:59 | „Passt“ für Video 01 DE; Scutoria-YouTube-Sitzung baut Reels, Thumbnails (Entwürfe vom 02.11. brauchbar, keine neuen Credits), englische Fassung, dann Video 02; Sitzung auf Sonnet | Freigabe |

### 3.5 Verworfen und warum (31.10. bis 03.11.)

| Verworfen | Grund |
|---|---|
| Takt 3 DE + 3 EN je Tag (01.11.) | ersetzt durch 2 Themen je Tag, DE und EN (Stefan, 02.11.) |
| Ziel 05.11. (3 Reels DE und EN je Marke, 2 Scutoria-Langvideos, 1 Tintora-Folge) | aufgehoben mit der Pause am 02.11. |
| Alte Videos im Format der ersten Woche (21 Ordner) und 45 Reels vor der Pause | nicht freigegeben, Format abgelöst; Stimmen bleiben Vorrat |
| Erstfassungen der neun Testvideos (Sweeps -9 dBFS) | zu laut; durch Neufassungen ersetzt, Dateien bleiben daneben |
| Revlore als reiner Motor-Kanal | Stefan: Technik-Kanal; 52 neue Technik-Themen |
| Tintora 16:9-Folge im November | 500 Credits reichen nur für acht Hochformat-Reels |
| Abstrakte Bibliotheks-Schleifen (Texturen, Clips V1–V4) | durch Realbilder überholt; nur auf Wunsch der Marke aus deren Anteil |
| API-Schlüssel (Anthropic) für den Tagesläufer | Stefan: über das Ultra-Abo |
| Trockenlauf aller Marken am Abend des 03.11. | Kontingent 78 % |
| Produktion durch die Marken-Sitzungen am 04.11. | Tagesläufer ist um ein Vielfaches günstiger |
| AI Influencer Studio (Higgsfield) für Tintora | lieferte 3D-Plüsch statt Anime, keine Kinderfigur |

---

## 4. Aktueller Stand im Detail (03.11.2026, 20:30)

### 4.1 Fertig

- **23 Videos im freigegebenen Format**, alle mit bestandenem Prüfbericht, keines veröffentlicht:
  - 18 Testvideos (je Marke DE-Neufassung mit leiseren Geräuschen und EN-Fassung): Frontlore „Fackeltelegraf“ (75 s / 83 s), Suitwerk „Köper und Leinwand“ (83 / 77), Scutoria Reels „Chef-Mail“ (75 / 72), Gritwerk „Willenskraft“ (86 / 86), Dewlane „Testmenge“ (79 / 81), Tintora Testreel F1-06 (83 / 83, alle Stimmen Pro), Revlore „Sicherungsautomat“ (87 / 77), Gigastruct „Fehmarnbelt Absenken“ (84 / 84), Promptwerk „Dubletten“ (76 / 76).
  - Tintora Reel F1-04 „Der Weg zum Echoberg“ DE 89 s und EN 90 s (42,75 Credits); Reel F1-05 „Dunkel wie Tinte“ DE 76 s (EN am 04.11.).
  - Scutoria-YouTube-Video 01 „KI-Regeln“ DE, Fassung 2026-11-03: 16:10 min, 1920x1080, 145 MB, Vorschau 27 MB, Untertitel, Prüfbericht, Standbilder je Kapitel, `Veröffentlichung.md`; Ordner `05 Produktion\Scutoria\2026-11\2026-11-17 KI-Regeln\`.
  - Tagesläufer-Prototyp Suitwerk Nr. 2 „Super 100s und die Zahl“ DE 78 s und EN 75 s (`05 Produktion\Suitwerk\2026-11\2026-11-03 Super 100s und die Zahl[ EN]\`).
- Tonebene im gemeinsamen Renderer (Abschnitt 5.5), Realbild-Bibliotheken für sieben Marken, Format-Bibeln und Konzeptpläne (689 Vorschläge, je Marke 60 bis 96) angepasst (Dewlane Produkte und Anwendung, Suitwerk realer Anzug, Promptwerk erlaubt gekennzeichnete KI-Realbilder, Revlore Technik), Aufbauten-Dateien je Marke geprüft.
- Tagesläufer (Abschnitt 5.6): Paket `src\fn\daily\`, `scripts\daily_runner.py`, `config\daily.yaml`, `config\aufbauten.vorlage.yaml`, Doku `docs\daily-runner.md`; Prototyp bestanden; erster echter Lauf eingeplant.
- Dokumente: `Neustart Testvideos 2026-11-02.md` (Abschnitt 10 mit allen Entscheidungen des 03.11.), `Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md` (Abschnitt „Neue Verteilung 03.11.“), `Bericht für ChatGPT 2026-11-03.md`, Drive-Übersicht Stand 19:59.

### 4.2 Teilweise erledigt

- **Scutoria YouTube:** sechs Reels aus Video 01 (9:16, dieselben Szenen) rendern; Thumbnails aus den drei Entwürfen vom 02.11. (a und c sauber, b mit Randlinie über dem Zeichen); englische Fassung von Video 01 mit den englischen Stimmen vom 31.10. noch nicht begonnen; Video 02 DE (alte Fassung vom 01.11. vorhanden, nicht auf der neuen Bildwelt) nur vorbereiten, Render erst mit Go. Umzug des Ordners `OneDrive\scutoria\marketing\youtube` nach `02 Marke\Scutoria\YouTube-Grundlagen` ausgesetzt.
- **Tintora Folge 1:** 2 von 8 Reels (F1-04 DE und EN, F1-05 DE); 93,25 von 500 Credits verbraucht; Pro-Anfragen heute 10 von 12. Alte Vertonung der ganzen Folge (46 von 118 Zeilen) liegt unbenutzt.
- **Tagesläufer:** Revlore nur mit Aufbau F „Kennlinie“ (10 Themen); Technik-Themen ohne eigenes gerechnetes Modell bleiben „braucht Modell“ (Nr. 76 bis 126 außer den zehn). Promptwerk nur mit vorhandenen Aufzeichnungen (12 Themen). Nicht gebaute Bildaufbauten (Scutoria B–D, Gritwerk B/D/E, Gigastruct B–D, Dewlane B–D nur als Trockenlauf, Frontlore D) werden durch gebaute ersetzt und vermerkt. Aufgabenvorlage `automation\run_daily.ps1` laut Auftrag vorgesehen; ob sie schon angelegt ist: nicht ermittelbar (die Abschlussmeldung dazu steht aus). Nicht registriert.
- **Alte Exporte:** 71 Dateien in den Produktionsordnern (ersetzte Erstfassungen, 45 Reels vor der Pause, altes Scutoria-Video mit sechs Reels, Piloten), nicht freigegeben.
- **Gedächtnis:** Drive-Übersicht auf Stand 19:59; Verweis auf diesen Bericht wird mit der nächsten Fassung ergänzt.

### 4.3 Noch nicht begonnen

- Konten: keine Gmail-Aliase, keine TikTok-, Instagram-, YouTube-Konten je Marke; keine Domains; kein Upload-Post-Konto, Endpunkte für Status, Profile und Analytics im Code „NOT_VERIFIED“.
- Veröffentlichung, privater Testupload, Registrierung der Windows-Aufgabenplanung (`automation\register_tasks.ps1`, Administratorrechte, durch Stefan).
- Impressum- oder Linkseite, Gewerbe und Steuerberatung, Markenregister für Tintora, Sicherung der Handles.
- Handy-Zentrale (Claude-Artefakt für Freigaben), Kommentar-Beantwortung (Phase 3), Media-Kit, Wochenbericht.
- Erster Git-Commit (kein Commit seit 29.10.; Stefan hat ihn nicht beauftragt).
- Strukturvorschlag für `05 Produktion` vom 31.10. (`01 Idee und Strategie\Vorschlag Ordnerstruktur 2026-10-31.md`): Entscheidung Stefans offen.
- Archivierung der neun Marken-Sitzungen (nur mit Stefans Ja, nachdem der Tagesläufer läuft).

---

## 5. Technisches Setup

### 5.1 Geräte und Software

Unverändert gegenüber dem 30.10.: PCSpecialist Recoil III 16, Windows 11 Pro, Core Ultra 9 275HX, RTX 5080 Laptop 16 GB VRAM, 31,5 GB RAM; Git, Node 24, Python 3.13 (venv `.venv` im Repository mit faster-whisper CUDA, google-genai 2.34.0, PyYAML), FFmpeg mit NVENC (`C:\Users\Stefa\AppData\Local\Microsoft\WinGet\Links\ffmpeg.EXE`), HyperFrames über `npx hyperframes`, Claude Code (Desktop-App). Kein `anthropic`-SDK installiert (nicht nötig). Freier Speicher auf C: am 03.11.: nicht ermittelt (Mindestwert für Renders 30 GB im Code; OneDrive-Speicher wird mit Rohmaterial knapp, fertige Projekte können auf „nur online“ gestellt werden).

### 5.2 Konten und Dienste (Zugänge nur als Ablageort)

| Dienst | Stand 03.11.2026 | Ablage des Zugangs |
|---|---|---|
| Claude (Abo Ultra laut App-Abfrage; die CLI `claude auth status` meldet „max“, Login stefan.dallinger.me@gmail.com) | alle Sitzungen und der Tagesläufer (`claude -p`) laufen darüber; Wochenfenster Reset 09.11.2026, 13:00 Wien | Konto Stefan, keine Datei |
| Google Gemini API (nur TTS) | Flash 100 Anfragen je Tag projektweit, Reset 09:00 Wien; Pro eigenes Kontingent | `C:\Automation\faceless-network\.env`, `GEMINI_API_KEY` (Git ignoriert) |
| Higgsfield Ultra | 3.000 Credits für November, Guthaben 1.108,75 um 17:00 | MCP-Server `higgsfield` je Sitzung per `/mcp` angemeldet; lesender Konnektor in der Hauptsitzung; `HIGGSFIELD_API_KEY` in `.env` vorhanden (Belegung nicht geprüft) |
| Google Workspace `admin@scutoria.com` | eingerichtet als Zentrale; Aliase und Markenkonten offen | Stefan |
| Upload-Post | nicht angelegt | `UPLOADPOST_API_KEY`, `UPLOADPOST_USER` in `.env` (leer) |
| ElevenLabs, Runway | nicht genutzt | Variablen in `.env` |
| Google Drive (Gedächtnis) | Konnektor in der Hauptsitzung | Ordner Übersichten `1C_0Au5INARUiG1dq_djKtf01o_eLKZ17`, Frühere Fassungen `1lqhMDs_wWQuy9tO6iY98xinBzbLHK-PP`; aktuelle Übersicht Datei-ID `1hxz-npWgVPAKhlHkrujKB5AGiqqhYlx7` (ändert sich mit jeder Fassung, mit `search_files` finden) |

### 5.3 Ordner in OneDrive (`C:\Users\Stefa\OneDrive\Business`), Ergänzungen seit 30.10.

```
01 Idee und Strategie\
   Übergabebericht 2026-10-30.md, Übergabebericht 2026-11-03.md (dieser Bericht)
   Neuausrichtung 2026-11-02.md, Neustart Testvideos 2026-11-02.md (Abschnitte 1–10)
   Ausgabe- und Arbeitsplan Higgsfield Ultra 2026-11.md (mit „Neue Verteilung 03.11.“)
   Bericht für ChatGPT 2026-11-03.md, Vorschlag Ordnerstruktur 2026-10-31.md
   Recherche\Codex-Bericht 2026-11-01 Konzeptkritik.md (und die Unterlagen vom 29.10.)
02 Marke\
   Marken.md, Qualitätsrunde 2026-10-31.md, Prüfrunde 2026-11-03.md
   Schnitt und Layout Kurzvideo (alle Marken).md, Vorlage Langvideo Scutoria (Original 2026-10-30).md
   <Marke>\Format-Bibel.md, Testvideo-Konzept 2026-11.md, Vorlage Bibliothek.md (Tabelle „Realbilder (03.11.2026)“)
   Scutoria\Testvideo-Konzept Reels 2026-11.md, Testvideo-Konzept YouTube 2026-11.md, YouTube-Konzept.md
   Tintora\Serie\ (Figurenbibel, Kostenschätzung Pilot.md mit Abschnitt 11, AI Influencer Studio Preisabfrage 2026-11-02.md)
03 Kanäle\<Marke>\Profilpaket.md (Handle, E-Mail, Bios DE/EN, Profilbild, Banner)
04 Redaktionsplan\
   Redaktionsplan.csv (Zeilen je Video, Status), Planungsrahmen Themen- und Kalenderplan.md
   Themen- und Kalenderplan <Marke> (09.11.–06.12.2026).md, Konzeptplan <Marke> (ab November 2026).md
05 Produktion\
   <Marke>\2026-11\<Datum Kurztitel>[ EN]\04 Export\*.mp4 (plus Prüfbericht, Veröffentlichung.md)
   Scutoria\2026-11\2026-11-17 KI-Regeln\ (Langvideo 01, Reels, Untertitel, Thumbnails)
   _Demos\ (Demos, Regie-Fassungen, tonebene\), Übersicht.md
08 Recht und Verwaltung\Lizenzen\Lizenzübersicht.md, Higgsfield Support-Anfrage 2026-11-02.md
```

### 5.4 Repository `C:\Automation\faceless-network` (Git, kein Commit), Ergänzungen seit 30.10.

| Pfad | Inhalt |
|---|---|
| `src\fn\direction\story.py`, `hooks.py`, `checks.py` | Story-Engine (Plan-Schema: Hook, Beats, Szenentypen, Wortanker, Marker, Cues), Prüfungen; offen: Beat-Feld `sound` |
| `src\fn\render\sound.py`, `sound_synth.py` | Tonebene: Paletten subtle, tech, paper, soft, none; Stimmungen calm, tech, warm, dark, bright; `DEFAULT_LEVELS` (`sfx_peak_db` -16, `event_peak_db` -20, `music_db` -10, `duck_db` 5, `sfx_max_peak_db` -6); Impuls-Offsets (click -8, tick -10, pop -5, stamp -3, thud -2, chime -4); Pegel je Marke in `brands\<id>\brand.yaml` unter `sound:` oder im Plan `layout.sound` |
| `src\fn\render\ffmpeg.py` | `encode_nvenc(..., loudnorm="linear")`: zweistufiges lineares loudnorm, Resampling 48 kHz, Begrenzer 0,79 |
| `src\fn\tts\gemini.py`, `config\voices.yaml` | Modellwahl über `GEMINI_TTS_MODEL`, `fallback_model: gemini-2.5-pro-preview-tts`, Preis 20 USD je Mio. Ausgabe-Token im Fallback |
| `src\fn\daily\`, `scripts\daily_runner.py`, `config\daily.yaml` | Tagesläufer: Themenwahl aus dem Konzeptplan (`reserved_days` jetzt leer), Prompt aus Regeln, Format-Auszug, Kurzkonzept, Szenen-Doku, Materialliste und Beispiel (etwa 21.000 Zeichen), Aufruf `claude -p --model claude-sonnet-5-5 --output-format stream-json --tools "" --no-session-persistence --setting-sources "" --effort low` aus einer Umgebung ohne die CLAUDE*- und ANTHROPIC*-Variablen der Desktop-App, Validierung gegen das Plan-Schema, Reparaturrunde mit Traceback, Trockenlauf DE vor EN, Vertonung (höchstens 4 Flash je Marke, Längenprüfung über Zeichen je Sekunde, `--pro-fallback`), Render über die Warteschlange, Export, Redaktionsplan, Kostenlog (`llm`-Einträge mit Token, „Abo, kein Einzelpreis“); `--list-topics`, `--dry-run` |
| `brands\<id>\aufbauten.yaml` (Vorlage `config\aufbauten.vorlage.yaml`) | je Bildaufbau Kürzel, Name, gebaut, Szenentypen, Beispielplan, Hinweis, Themen; Revlore zusätzlich Quellen je Thema (URL, Titel, checked_at) und Schlüssel `hinweis` mit Formeln; Promptwerk Block `aufzeichnungen` |
| `brands\<id>\assets\higgsfield\library\` | Realbild-Bibliothek: `*_real_*.jpg`, `*_clip_*.mp4`, `LICENSE.md`, `manifest.json`, `index.html`; eigenes Marken-Material daneben (zum Beispiel `testvideo\`) mit eigener `LICENSE.md` |
| `brands\<id>\<format>\scenes.py` | markeneigene Szenentypen (zum Beispiel `brands\beauty\nahaufnahme\scenes.py`, `brands\motivation\laborbuch\scenes.py`, `brands\engines\zeitlupe\` mit `still_to_clip.py`); Promptwerk `brands\claude_workflows\echtlauf\voice_tts.py --say Claude=Klohd --reuse-voice`, `record_run.py` |
| `brands\ai_security\longform\` | brand-lokaler 16:9-Composer für die Scutoria-Langvideos (Pläne in `longform\plans\`, Bibliothek `assets\higgsfield\yt\`), Render über `render_queue.py` |
| `scripts\render_queue.py`, `render_direction.py` (`--mirror`, `--no-sound`, `--no-render`), `export_production_folder.py`, `overlap_check.mjs`, `sort_production.py` | Warteschlange (ein Render gleichzeitig, Sperre `data\render.lock`, stale nach 20 min), Regie-Render, Export, Überschneidungsprüfung |
| `automation\` | `register_tasks.ps1`, `run_render.ps1`, `run_publish.ps1`, `run_status.ps1`, `run_claude_calendar.ps1`; `run_daily.ps1` vorgesehen; nicht registriert |
| `docs\direction-system.md` (Abschnitte 6e, 6f, 6g, 6h, 6i), `docs\daily-runner.md` | Regie-System, Tonebene, Tagesläufer mit Messwerten |
| `data\costs\costs.jsonl`, `data\direction\`, `storage\direction\<video_id>-<Fassung>\`, `storage\longform\` | Kostenlog (Felder `video_id`, `kind`, `units`, `usd`, `provider`, `note`, `at`), Pläne, Render-Ausgaben mit `check.json`, `sound.json`, Standbildern |

Marken-IDs im Code: `ai_security` (Scutoria), `claude_workflows` (Promptwerk), `brainrot` (Tintora), `beauty` (Dewlane), `engines` (Revlore), `megaconstruction` (Gigastruct), `menswear` (Suitwerk), `military_history` (Frontlore), `motivation` (Gritwerk).

### 5.5 Produktionskette je Reel (Stand 03.11.)

1. Thema aus dem Konzeptplan (Bildaufbauten wechseln nach festem Muster).
2. Regie-Skript nach dem Plan-Schema der Story-Engine, mit Quellen, Markern, Wortankern, Ton-Cues; bis 03.11. von Hand durch die Marken-Sitzung, ab 04.11. durch den Tagesläufer.
3. Bildmaterial: animierte Szenen des Renderers plus Realbilder und Clips aus der Bibliothek der Marke (mit Etikett „KI-Bild“ beziehungsweise „KI-generierte Darstellung“).
4. Vertonung über Gemini (ein Bündel höchstens 80 bis 90 Sekunden, Abbruch bei 2560 Ausgabe-Token).
5. Tonebene: Geräusche an Übergängen und Einblendungen, Musikbett 10 dB unter der Stimme und 5 dB Absenkung beim Sprechen; Mix auf -16 LUFS, Spitze höchstens -2 dBFS.
6. Render HyperFrames und FFmpeg NVENC, 1080x1920, 30 fps; Warteschlange.
7. Prüfbericht: Lautheit, Spitzenpegel, `overlap_check`, `small_text`, Stille, Schwarzbild, Lizenzzeilen, Whisper-Transkript gegen Text; Ergebnis VALIDATED oder HUMAN_REVIEW.
8. Export in den Produktionsordner, Redaktionsplan, `Veröffentlichung.md`.

### 5.6 Claude-Code-Sitzungen (Desktop-App, Gruppe „Business (Video und Social Media)“)

| Sitzung | ID | Modell | Stand 20:30 |
|---|---|---|---|
| Hauptsitzung (diese) | – | Fable 5.1, Verlauf 655.000 Token | koordiniert, Stefan-Kontakt |
| Scutoria · Reels „Was tust du?“ | `local_68b7d94e-bb49-4e57-b44e-1ae8cd5c1181` | Sonnet 5.5 seit 16:39 | idle, produziert nichts mehr selbst |
| Promptwerk · Reels „Echtlauf“ | `local_437cff37-639b-42c2-ba54-1f3597261f70` | Sonnet 5.5 | idle |
| Tintora · Anime-Serie Folge 1 | `local_e9861606-5ca6-490b-8fa2-b5947ade3269` | Sonnet 5.5 | baut Reels 3 bis 8 (F1-05 EN am 04.11.) |
| Dewlane · Reels „Nahaufnahme“ | `local_eb29efeb-2fb9-43ce-9c99-912d8666f340` | Sonnet 5.5 | idle |
| Revlore · Reels „Zeitlupe“ | `local_382ab4a8-a70b-4615-ba2e-531ace84f717` | Sonnet 5.5 | idle |
| Gigastruct · Reels „Bauaufgabe“ | `local_9cc935a1-4a1d-4f70-bf69-19934f329512` | Sonnet 5.5 | idle |
| Suitwerk · Reels „Kreidestrich“ | `local_d067b746-1263-4eff-ae65-5a2c2a041b75` | Sonnet 5.5 | idle |
| Frontlore · Reels „Rekonstruktion“ | `local_aaa03b00-f29e-4105-b5fb-fbbec45fc6d3` | Sonnet 5.5 | idle |
| Gritwerk · Reels „Laborbuch“ | `local_4f2542d2-e1d1-42c7-ba6f-d9d016a1c4fd` | Sonnet 5.5 | idle |
| Scutoria · YouTube-Langvideos | `local_df7e36fa-e465-4467-a475-fa6499aac741` | Sonnet 5.5 seit 19:59 | Reels aus Video 01 |
| Tagesläufer: Tagesproduktion | `local_d9202f2e-4004-4637-9f93-0eacc845c925` | Sonnet 5.5 seit 17:45 | Lauf 04.11. 09:05 eingeplant |
| Alle Marken · Higgsfield-Bibliotheken | `local_b61a244a-649a-40bb-8cc8-546cb7962585` | – | November-Arbeit abgeschlossen |
| Tonebene: Geräusche und Musikbett | `local_57377bc7-1cb0-409e-b444-894b996d5a52` | – | fertig |
| Alle Marken · Prüfrunde | `local_ceefba6f-8ade-45e6-b175-6841e8433130` | – | fertig |

Eigenheiten der App: Nach zehn Sitzungsnachrichten der Hauptsitzung seit Stefans letzter Eingabe sperrt die App weitere Nachrichten bis zu seiner nächsten Eingabe; Antworten gehen dann über Dateien (Neustart-Auftrag Abschnitt 10). Dateien über 30 MiB lassen sich nicht an Stefans Handy schicken; Vorschaukopien mit ffmpeg (libx264 crf 26, maxrate 2200k) im Scratchpad. Zwischen Sitzungen traten mehrfach ECONNREFUSED und Zeitüberschreitungen auf (Netz im Einsatz); Renders in der Warteschlange liefen weiter.

### 5.7 Verfahren für die Drive-Übersicht

Neue Datei mit demselben Titel in `Übersichten` anlegen (`create_file`, `textContent`, `contentMimeType text/markdown`, `disableConversionToGoogleType true`), alte mit `update_file` nach `Frühere Fassungen` verschieben und Titel um „ (bis JJJJ-MM-TT HH-MM)“ ergänzen. Die Markdown-Datei muss unter etwa 18.700 Byte bleiben (Lese-Kappe des Konnektors bei etwa 25.000 Base64-Zeichen); ältere Einträge werden dafür gekürzt. Lokale Gedächtnisnotizen für Claude Code liegen in `C:\Users\Stefa\.claude\projects\C--Users-Stefa-OneDrive-Business\memory\` (Index `MEMORY.md`, unter anderem `drive-uebersicht-upload.md`, `gemini-tts-quota-models.md`, `scutoria-youtube-longform.md`, `bash-backslash-escapes.md`).

### 5.8 Zeitpläne

- Tagesläufer: 04.11.2026, 09:05 Wien (10:05 Laptopzeit), von der Tagesläufer-Sitzung selbst gestartet, Dauer etwa drei Stunden für acht Marken; danach Sammelmeldung. Ab dem 05.11. sagt die Hauptsitzung den Takt an.
- Gemini Flash: Reset 09:00 Wien; Pro-Kontingent: Reset-Zeit nicht ermittelbar (Tintora rechnet mit 09:05).
- Claude-Wochenfenster: Reset 09.11.2026, 13:00 Wien.
- Windows-Aufgabenplanung: Vorlagen vorhanden, nichts registriert (FN Render Queue 09:00, FN Publish Sync stündlich :05 im Dry-Run, FN Costs and Status 19:00, FN Topic Proposals 19:30; `run_daily.ps1` vorgesehen).
- Veröffentlichung: geplante Slots je Marke 12:00, 14:00, 18:00 (DE) und 15:00, 20:00, 23:00 (EN, Annahme von Claude) Wien, noch ohne Konten.

---

## 6. Zahlen, Daten, Preise, Fakten (mit Quelle und Datum)

### 6.1 Videos (Zählung nach Dateien in `05 Produktion`, 03.11.2026, 17:00 und 20:00)

| Kategorie | Anzahl | Quelle |
|---|---|---|
| Fertig im freigegebenen Format | 23 (18 Testvideos DE/EN, Tintora F1-04 DE/EN, F1-05 DE, Scutoria YouTube 01 DE, Prototyp Suitwerk DE/EN) | Dateisystem, Sitzungsmeldungen |
| Ältere Exportdateien, nicht freigegeben | 71 (Dewlane 6, Frontlore 3, Gigastruct 8, Gritwerk 6, Promptwerk 7, Revlore 28, Scutoria 10, Suitwerk 2, Tintora 1) | `find` am 03.11., 17:00 |
| Veröffentlicht | 0 | – |

### 6.2 Higgsfield (Quelle: Konnektor-Abfragen und Sitzungsmeldungen, 03.11.)

| Fakt | Wert |
|---|---|
| Plan | Ultra, 3.000 Credits für November (gebucht 02.11.) |
| Guthaben | 1.602 (10:51), 1.416 (12:40), 1.159 (13:45), 1.108,75 (17:00) |
| Verbrauch seit 02.11. | 1.891 Credits, darunter neun Testvideos etwa 700 (einschließlich Scutoria-YouTube-Vorbereitung 80), Bibliotheken 400 (186 + 214), Konzeptbilder etwa 130, Tintora Stufe 0 102 und Reels etwa 93, AI Influencer Studio 2; Rest Piloten vor der Pause (Einzelposten nur in der Transaktionsliste bei Higgsfield, nicht nachgerechnet) |
| Preise | Nano Banana Pro 2 Credits je Bild; Kling O3 5 s mit Startbild 6,25; Kling 8 s pro 10 (Bibliotheken-Sitzung, 03.11.) |
| Verteilung des Rests (Stefan, 13:03) | Bibliotheken 214 (verbraucht), Tintora Folge 1 500 (93,25 verbraucht), Scutoria YouTube 250 (0 seit 13:03), Tagesproduktion 300 = 33 je Marke bis 30.11. (0 verbraucht), Reserve 152 |

### 6.3 Gemini TTS (Quelle: `data\costs\costs.jsonl`, 03.11., 17:00)

- Gesamt seit 30.10.: 3,74 USD für 200 bezahlte Anfragen; etwa 0,018 bis 0,019 USD je Reel-Fassung mit Flash, etwa das Doppelte mit Pro.
- Limits: Flash 100 Anfragen je Tag für alle Marken zusammen (beobachtet 02.11.); Pro: Tageslimit nicht ermittelbar (429-Meldung nannte 50); Abbruch einer Anfrage bei 2560 Ausgabe-Token (etwa 102 s), daher Bündel höchstens 80 bis 90 s.
- Promptwerk: eine Flash-Anfrage am 03.11. vormittags bekam 429 trotz frischem Kontingent; Ursache nicht ermittelbar.

### 6.4 Claude-Kontingent (Quelle: App-Abfrage `get_usage`, 03.11.)

| Uhrzeit | Weekly alle Modelle | Weekly Fable |
|---|---|---|
| 13:25 | 63 % | 54 % |
| 17:00 | 74 % | 73 % |
| 17:45 | 78 % | 82 % |

Wochenfenster seit 02.11., 13:00 Wien, Reset 09.11., 13:00 Wien; Zusatznutzung ausgeschaltet (Monatslimit 10 EUR eingestellt, 0 verbraucht). Hauptsitzung: 655.000 Token Verlauf (66 % des Fensters) um 17:45.

### 6.5 Tagesläufer-Messwerte (Quelle: Tagesläufer-Sitzung, 03.11.)

| Aufruf | Dauer | Token (Eingabe / Cache / Ausgabe) | CLI-Schätzung |
|---|---|---|---|
| Suitwerk „Stoffgewicht“, Standard-Aufwand, 36.600 Zeichen Prompt, mehrere Turns | 261 s | 8 / 70.000 / 37.000 | 1,27 USD (nur Rechenwert, im Abo kein Einzelpreis) |
| Suitwerk Nr. 2 DE, Aufwand medium | 126 s | 4 / 11.300 / 19.300 (davon etwa 3.200 sichtbares JSON) | 0,56 USD |
| Suitwerk Nr. 2 EN, medium, 2 Aufrufe | etwa 60 s | 8 / 18.500 / 9.900 | – |
| Dewlane Nr. 6 DE, Aufwand low, 2 Aufrufe | 25 + 25 s | Ausgabe zusammen 9.800 | – |
| Dewlane Nr. 6 EN, low, 2 Aufrufe | – | Ausgabe 8.800 | – |

Standard ist seit dem Abend Aufwand low. Alle Aufrufe meldeten `rate_limit allowed_warning` (Bedeutung nicht ermittelbar, vermutlich Nähe zur Kontingentgrenze). Belastung eines vollen Tagesläufer-Tages auf das Wochenkontingent: nicht ermittelbar vor dem ersten Lauf.

### 6.6 Ton und Render

- Tonebene-Demos (03.11., Tonebene-Sitzung, nachgemessen): Revlore -15,6 LUFS, Spitze -1,6 dBFS; Scutoria -15,8 LUFS, Spitze -2,0 dBFS. Testvideos nach der Korrektur: Geräusch-Stem -16,0 bis -18,4 dBFS, Musikbett 14 bis 19,5 dB unter der Stimme.
- Scutoria-Video 01 (Fassung 03.11.): -16,0 LUFS, LRA 6,3, Spitze -1,8 dBFS, 290 Geräusche, Renderzeit 16:38 min für 8 Kapitel (Faktor 0,93 bis 1,68) plus 1:50 min Kodierung; Zwischenprobe 2:28 min, Faktor 1,42 und 1,11.
- Reels: Renderzeiten einzeln nicht erhoben; die neun Neufassungen plus neun EN-Fassungen liefen zwischen 11:57 und 13:16 über eine Warteschlange.
- Dateigrößen: Reels 13 bis 51 MB (1080x1920), Langvideo 145 MB; Grenze für den Versand an das Handy 30 MiB.

### 6.7 Nicht ermittelbar (mit Grund)

- Pro-Tageslimit bei Gemini (nur 429-Meldung); Reset-Zeit des Pro-Kontingents.
- Ursache der 429-Antwort bei Promptwerk trotz freiem Flash-Kontingent.
- Token-Preis im Abo (es gibt keinen; CLI-Schätzungen sind API-Listenpreise).
- Kontingentverbrauch eines vollen Tagesläufer-Tages und Bedeutung von `rate_limit allowed_warning`.
- Einzelposten des Higgsfield-Verbrauchs vor der Pause (nur Transaktionsliste bei Higgsfield).
- Ob `automation\run_daily.ps1` bereits angelegt ist (Abschlussmeldung steht aus).
- Freier Speicher auf C: am 03.11. (nicht abgefragt).
- Ob Upload-Post einen auditierten TikTok-Client hat; Instagram-Reels im API-Tageslimit (unverändert seit 30.10.).

---

## 7. Entscheidungen

### 7.1 Getroffen (31.10. bis 03.11.2026)

| Entscheidung | Datum | Pro | Contra |
|---|---|---|---|
| Jede Marke eigenes Format (Format-Bibel), Neuausrichtung | 02.11. | gegen Gleichförmigkeit (Codex, Stefan) | mehr Pflege je Marke |
| Zonkfruit wird Tintora (Anime-Kinderserie) | 02.11. | klares Serienkonzept, Handle frei | Markenregister ungeprüft, Kinderinhalte mit Plattformregeln |
| Gemini Pro als Ausweich, Tintora ganz Pro | 02.11. | Produktion trotz Flash-Limit | doppelter Preis, eigenes Limit |
| Higgsfield Ultra 3.000 Credits, Ausgabeplan | 02.11. | Realitätsnähe, Bibliotheken | Credits reichen nicht für alles (Tintora-Folge) |
| Pause und Neustart mit Testvideo je Marke | 02.11., 22:00 | Qualität vor Menge, Stefans Note 4 | ein Tag Produktionsstillstand |
| Hände und Menschen von hinten ja, keine Gesichter | 03.11., 05:25 | Realität ohne Deepfake-Risiko | Einschränkung der Motive |
| Musikbett prozedural, keine fremde Musik | 03.11., 05:41 | keine Lizenzfrage, konsistent | weniger musikalische Vielfalt |
| Tonebene im gemeinsamen Renderer, Standard Sweeps -16 dBFS, Marken leiser erlaubt | 03.11. | einheitlich, prüfbar | Marken müssen bei überlappenden Cues anpassen |
| Alle neun Testvideos freigegeben, englische Fassung aus denselben Szenen | 03.11., 11:55 | Vorlage je Marke steht | Dewlane und Frontlore bleiben Handfreigabe |
| Neue Credit-Verteilung (214/500/250/300/152) | 03.11., 13:03 | passt ins Guthaben | Tintora-Folge erst im Dezember |
| Tintora: acht Hochformat-Reels statt 16:9-Folge | 03.11., 13:19 | passt in 500 Credits | Serie ohne Folge im November |
| Eigenes Marken-Material nie in `library\` | 03.11. | keine Lizenzkollisionen | zwei Ablageorte je Marke |
| Marken-Sitzungen auf Sonnet, Meldungen gebündelt | 03.11., 16:39 | Kontingent | mögliche Qualitätsunterschiede bei kreativer Arbeit |
| Tagesläufer über Claude Code im Abo (`claude -p`), kein API-Schlüssel | 03.11., 16:45 | keine zusätzlichen Kosten, Stefans Wunsch | Verbrauch bleibt im Wochenkontingent |
| Keine Produktion durch Marken-Sitzungen ab 04.11.; Tagesläufer freigegeben | 03.11., 17:45 und 18:44 | um ein Vielfaches günstiger als Sitzungsrunden; Prototyp bestanden | Tagesläufer-Qualität erst mit einem Video belegt |
| Revlore im Tagesläufer nur mit allgemeinen Aufbauten (Kennlinie), Technik zuerst, Motor höchstens jedes dritte Thema | 03.11. | Technik-Kanal laut Stefan, keine Modelle je Thema nötig | Themen mit eigenem Modell bleiben liegen |
| Scutoria-Video 01 (Fassung 03.11.) freigegeben; Reels, Thumbnails, EN, dann Video 02 | 03.11., 19:59 | Maßstab erreicht | Video 02 braucht Go für den Render |

### 7.2 Offen

| Frage | Pro | Contra |
|---|---|---|
| Takt ab 05.11.: 2 Themen je Marke und Tag oder weiter 1 | 2: Stefans Vorgabe, Puffer | Kontingent 78 % nach gut einem Tag; erst nach dem ersten Tagesläufer-Lauf messbar |
| Marken-Sitzungen archivieren | spart Kontingent, Tagesläufer übernimmt | Spezialwissen (Promptwerk-Aufzeichnungen, Revlore-Modelle, Gigastruct-3D) bleibt dann nur in Dateien |
| Zusatznutzung im Claude-Abo einschalten | Puffer für Engpässe | Geld; Stefan hat 10 EUR Limit gesetzt, nicht aktiviert |
| Strukturvorschlag `05 Produktion` (31.10.) | Ordnung je Marke und Monat | nicht entschieden |
| Konten gleichzeitig oder gestaffelt anlegen | gestaffelt (Scutoria, Gritwerk, eine dritte) ist der bisherige Plan | Puffer veraltet |
| Erste 20 Videos je Marke von Hand freigeben | Kalibrierung | widerspricht „automatisch“ |
| Tintora 16:9-Folge im Dezember (neue Credits) | Serie vollständig | Kosten |
| Erster Commit | Sicherung | nicht beauftragt |
| Gewerbe, Steuerberatung, Impressum | Pflicht vor Werbepartnern | offen seit 29.10. |

---

## 8. Probleme, Fehler, Risiken

| Problem oder Risiko | Stand |
|---|---|
| Gemini-Flash-Tageslimit (100 je Tag, projektweit) | Pro als Ausweich; Zuteilung je Marke; Tagesläufer höchstens 2 Flash je Marke |
| Gigastruct-Stimme brach bei 2560 Ausgabe-Token ab | Bündel höchstens 80 bis 90 s |
| Spitzenpegel über -1 dBFS nach AAC (Revlore, Gritwerk) | Begrenzer nach Resampling, lineares loudnorm, Prüfung auf kodiertem Ton |
| Wisch-Geräusche zu laut (Stefan) | Standard -16 statt -9 dBFS; Marken teils -18/-19; alle Testvideos neu gerendert |
| Überlappende Cues heben den Geräusch-Stem über die Grenze | Marken senken ihren Pegel; Cues entzerrt; Standard bleibt -16 |
| Promptwerk-Stimme sprach „Claude“ als „Cloud“ | Sprechtext „Klohd“ über `voice_tts.py --say`; Whisper bestätigt |
| Gigastruct-Clips: Element sinkt nicht sichtbar, Schlepper fahren aufs Element zu | durch Beschnitt und Reihenfolge entschärft |
| Lizenzkollision Revlore/Bibliotheken (`LICENSE.md` überschrieben) | behoben; Regel „eigenes Material nie in `library\`“; Skript sichert vorher |
| Kling-Ausfall 02.11. (Aufträge „queued“) | erstattet; Regel: nach 15 Minuten „queued“ abbrechen und melden |
| Nachrichtensperre der App nach zehn Sitzungsnachrichten | Antworten über Dateien; Meldungen gebündelt |
| Dateien über 30 MiB nicht ans Handy lieferbar | Vorschaukopien |
| Claude-Wochenkontingent 78 % nach gut einem Tag | Sonnet für alle Nebensitzungen, Tagesläufer, Produktion der Sitzungen gestoppt; Verbrauch des ersten Laufs abwarten |
| Tagesläufer: 37.000 Ausgabe-Token je Plan bei Standard-Aufwand | Aufwand low (etwa 10.000), stream-json, ein Turn |
| Themen-Dubletten zwischen Sitzungen und Tagesläufer | Sitzungen produzieren nicht mehr; `reserved_days` leer; Prototyp-Kennzeichnung |
| Tagesläufer-Qualität für Gigastruct (3D-Objekte, Wortanker) | größtes Risiko laut Tagesläufer; Attrappen-Trockenlauf bestanden, echtes Video steht aus |
| Revlore-Technik-Themen ohne gerechnete Modelle | nur Aufbau F mit 10 Themen; Rest „braucht Modell“ |
| Dewlane und Frontlore (Risiko hoch) | jedes Video Handfreigabe durch Stefan |
| Upload-Post-Endpunkte „NOT_VERIFIED“, TikTok-Audit unbekannt | vor dem ersten Upload prüfen |
| Veröffentlichung ist der Engpass (keine Konten) | Stefan (Abschnitt 9) |
| Hauptsitzung mit 655.000 Token Verlauf | bei Bedarf neu starten; dieser Bericht ist die Übergabe |
| Netzabbrüche zwischen Sitzungen (ECONNREFUSED) | Wiederholen; Renders laufen in der Warteschlange weiter |

---

## 9. Offene Aufgaben und nächste Schritte (Reihenfolge, Abhängigkeiten)

1. **04.11., ab 09:05:** Tagesläufer-Lauf (acht Marken, je 1 Thema DE und EN) läuft von selbst; Sammelmeldung prüfen: Prüfberichte, Token je Video, Flash-Anfragen, Fehler; Dewlane und Frontlore als HUMAN_REVIEW an Stefan. Dann Kontingent abfragen und den Takt ab 05.11. festlegen (1 oder 2 Themen). Keine Abhängigkeit.
2. **04.11.:** Tintora Reel F1-05 EN (Pro ab 09:05), dann Reel 3 von 8 nach Freigabe des Prüfberichts; Credits in der Kostenschätzung mitführen. Abhängig vom Pro-Kontingent.
3. **Scutoria YouTube:** sechs Reels prüfen und exportieren, Thumbnails ohne neue Credits, englische Fassung von Video 01, Video 02 DE vorbereiten (Render nur mit Go). Abhängig von nichts.
4. **Tagesläufer fertigstellen:** `automation\run_daily.ps1` und Eintrag in `register_tasks.ps1` (nur Vorlage), Doku; Revlore-Themen mit Modellbedarf an die Revlore-Sitzung oder streichen; nicht gebaute Bildaufbauten nachbauen lassen (Scutoria B–D, Gritwerk B/D/E, Gigastruct B–D, Frontlore D), sobald Kontingent da ist. Abhängig von 1.
5. **Marken-Sitzungen archivieren** (nur mit Stefans Ja), nachdem der Tagesläufer zwei Tage sauber lief; Spezialwissen vorher in `aufbauten.yaml` und Format-Bibeln sichern. Abhängig von 1 und 4.
6. **Drive-Übersicht** nach dem ersten Lauf nachziehen (Verweis auf diesen Bericht, Stand Videos, Kontingent). Abhängig von 1.
7. **Stefan: Konten** (Google-Workspace-Absicherung, Aliase, Markenkonten zuerst Scutoria, Gritwerk, eine dritte; Upload-Post Basic; Schlüssel in `.env`), dann privater Testupload, Prüfung der NOT_VERIFIED-Endpunkte, Registrierung der Aufgabenplanung. Abhängig von Stefan.
8. **Impressum- oder Linkseite, Gewerbe, Steuerberatung, Markenregister Tintora** (Stefan). Vor dem ersten Upload beziehungsweise vor Werbepartnern.
9. **Code (gemeinsam):** Beat-Feld `sound` in `story.py`, Lage der Kling-Clips im Renderer (z-index, `top:0`), Prüfung des Begrenzers in Grenzfällen. Niedrige Priorität.
10. **Puffer von 7 bis 14 Tagen je Kanal** aufbauen, sobald Konten und Takt stehen; Veröffentlichung zu den Slots; Kommentare (Phase 3). Abhängig von 7.
11. **Erster Commit**, wenn Stefan es beauftragt (vorher prüfen, dass `.env` ignoriert bleibt).

---

## 10. Offene Fragen an Stefan

1. Takt ab 05.11.: zurück auf 2 Themen je Marke und Tag, oder bei 1 bleiben, bis das Wochenkontingent am 09.11. zurückgesetzt ist?
2. Sollen die neun Marken-Sitzungen archiviert werden, sobald der Tagesläufer zwei Tage sauber läuft?
3. Zusatznutzung im Claude-Abo einschalten (derzeit aus, Limit 10 EUR eingestellt), um Engpässe abzufangen?
4. Wann legst du die Konten und Upload-Post an (Reihenfolge Scutoria, Gritwerk, dritte Marke)? Welche dritte Marke?
5. Strukturvorschlag `05 Produktion` vom 31.10.: freigeben oder ablehnen?
6. Tintora: 16:9-Folge im Dezember mit neuen Credits, oder nur Reels?
7. Dewlane und Frontlore: willst du die Tagesläufer-Videos dieser Marken täglich einzeln freigeben, oder nach den ersten fünf auf automatisch umstellen?
8. Erster Commit des Repositories?
9. Gewerbe, Steuerberatung, Impressum: Stand?

---

## 11. Begriffe und Abkürzungen

| Begriff | Bedeutung |
|---|---|
| Faceless | Kanäle ohne sichtbare Person; Stimme und Bild KI-erzeugt |
| Marke, Marken-ID | eine der neun Nischen; ID im Code (`ai_security`, `claude_workflows`, `brainrot`, `beauty`, `engines`, `megaconstruction`, `menswear`, `military_history`, `motivation`) |
| Format, Format-Bibel | das Erzählformat je Marke („Was tust du?“, „Echtlauf“, „Nahaufnahme“, „Zeitlupe“, „Bauaufgabe“, „Kreidestrich“, „Rekonstruktion“, „Laborbuch“, Tintora-Serie) und seine Regeln in `02 Marke\<Marke>\Format-Bibel.md` |
| Konzeptplan | Themenliste je Marke mit Bildaufbau und Reihenfolge (`04 Redaktionsplan\Konzeptplan <Marke> (ab November 2026).md`) |
| Bildaufbau (Aufbau A, B, …) | wiederverwendbares Szenengerüst einer Marke; Datei `brands\<id>\aufbauten.yaml` |
| Regie-System, Story-Engine, Plan | Datenmodell eines Videos: Hook, Beats, Szenentypen, Wortanker, Marker, Ton-Cues (`src\fn\direction\story.py`) |
| Beat | Abschnitt der Dramaturgie mit einer Funktion |
| Wortanker (`@Wort`) | zeitliche Verankerung einer Einblendung am gesprochenen Wort |
| Marker | Scutoria-Kennzeichen Fakt, Auslegung, Unsicher, Lücke (für alle Marken übernommen) |
| Tonebene | Geräusche und Musikbett aus `src\fn\render\sound.py` |
| Sweep, Impuls, Cue | Wisch-Geräusche (whoosh, swipe, paper, riser), kurze Klänge (click, tick, stamp, pop), Zeitpunkt eines Geräuschs |
| Stem | eine Tonspur vor dem Mix (Stimme, Geräusche, Musik) |
| LUFS, dBFS | Lautheit, Pegel relativ zur Vollaussteuerung |
| loudnorm linear | statische Lautheitsanpassung in zwei Durchgängen (FFmpeg) |
| Realbild-Bibliothek | fotorealistische KI-Bilder und Clips je Marke (`brands\<id>\assets\higgsfield\library\`) |
| Nano Banana Pro, Kling O3 | Higgsfield-Modelle für Bilder (2 Credits) und Clips (6,25 je 5 s, 10 je 8 s) |
| Credits | Higgsfield-Verrechnungseinheit |
| Flash, Pro | Gemini-TTS-Modelle (`gemini-2.5-flash-preview-tts`, `gemini-2.5-pro-preview-tts`) |
| 429 | HTTP-Antwort „zu viele Anfragen“ (Kontingent erschöpft) |
| Tagesläufer | Skript `scripts\daily_runner.py`, das Regie-Skripte über `claude -p` erzeugt und die Kette anstößt |
| `claude -p` | Claude Code im Headless-Modus (ohne Fenster), mit Stefans Abo-Login |
| effort low/medium | Denkaufwand des Modells je Aufruf (bestimmt die Ausgabe-Token) |
| Prüfbericht, VALIDATED, HUMAN_REVIEW | automatische Prüfung je Video; bestanden beziehungsweise Freigabe von Hand (Risiko hoch) |
| overlap_check, small_text | Prüfungen auf überlappende Textelemente und zu kleine Schrift |
| Render-Warteschlange | `scripts\render_queue.py`, ein Render gleichzeitig |
| Renderfaktor | Renderzeit geteilt durch Videolaufzeit |
| Zwischenprobe | Ausschnitt eines Langvideos zur Freigabe vor dem ganzen Render |
| Composer (longform) | brand-lokaler 16:9-Renderer für Scutoria-Langvideos |
| Nachtarchiv | Bildwelt der Scutoria-Langvideos (Büro, Archiv, Figuren ohne Gesichter) |
| Upload-Post | Multi-Plattform-Upload-Dienst mit API und MCP-Server |
| MCP, Konnektor | Model Context Protocol; angebundene Dienste in Claude Code |
| Haupt-, Nebensitzung | koordinierende Claude-Code-Sitzung und die von ihr gestarteten Sitzungen je Marke oder Aufgabe |
| Nachrichtensperre | App-Grenze von zehn Sitzungsnachrichten der Hauptsitzung je Nutzereingabe |
| Ultra, Max | Claude-Abo-Stufen; das Wochenkontingent gilt für alle Sitzungen zusammen |
| Fable 5.1, Sonnet 5.5 | Claude-Modelle; Fable in der Hauptsitzung, Sonnet in allen Nebensitzungen seit 03.11. |
| Art. 50 AI Act | EU-Transparenzpflicht für KI-Inhalte; Kennzeichnung in jedem Video |
| Risiko hoch | Marken mit Handfreigabe (Dewlane Beauty, Frontlore Militärgeschichte) |
| `_zum_loeschen` | Ablage für alles, was weg soll (Claude löscht nichts) |
