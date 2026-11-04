# Bericht für ChatGPT: Business „Video und Social Media“

Stand: 03.11.2026, 17:00 Uhr (Wien). Verfasst von der Hauptsitzung (Claude Code) für Stefan Dallinger. Alle Zahlen stammen aus den Dateien und Abfragen des Tages; was nicht belegt ist, steht als „nicht ermittelbar“.

## 0. Worum es geht und was ChatGPT beitragen soll

Stefan baut ein Netz aus neun faceless Videomarken (Kurzvideos 65 bis 90 Sekunden für TikTok, Instagram Reels und YouTube Shorts, dazu lange YouTube-Videos für eine Marke und eine Anime-Kinderserie für eine andere), das Claude Code auf einem Windows-Laptop weitgehend automatisch plant, schreibt, vertont, rendert und prüft. Veröffentlicht wird später über Upload-Post. Deutsch und Englisch auf demselben Konto je Marke. Betrieb von Österreich aus, jedes Video als KI-Inhalt gekennzeichnet, synthetische Stimme ausgewiesen.

Erbeten von ChatGPT: eine nüchterne Bewertung des Stands, der Entscheidungen der letzten 24 Stunden und des Plans für die nächsten sieben Tage; konkrete Risiken; Prioritäten. Die Fragen stehen in Abschnitt 9.

## 1. Die neun Marken

| Marke | Nische | Format (freigegeben) | Besonderheit |
|---|---|---|---|
| Scutoria | KI-Regeln und Datenschutz im kleinen Betrieb | Reels „Was tust du?“; YouTube-Langvideos 15–25 min auf der Bildwelt „Nachtarchiv“ | Hauptmarke, Scutoria ist zugleich ein bestehendes Unternehmen; Designsystem vorhanden |
| Promptwerk | Arbeiten mit Claude Code | „Echtlauf“: echte, aufgezeichnete Läufe als animierte Oberflächen | Aussprache „Claude“ in der Stimme gelöst |
| Tintora (vormals Zonkfruit) | Kinder-Anime-Serie „Juna und die Insel der verlorenen Farben“ | Reel-Abschnitte aus Folge 1, Kling-Clips, elf Figurenstimmen | YouTube „speziell für Kinder“, TikTok und Instagram ohne direkte Ansprache unter 13 |
| Dewlane | Beauty: Produkte, Anwendung, Wissen | „Nahaufnahme“ mit erfundenen Produkten ohne echte Marken | Risiko hoch, Freigabe je Video von Hand; Wirkung nur mit Quelle |
| Revlore | Technik erklärt (seit 02.11. statt Motoren) | „Zeitlupe“ | 52 neue Technik-Themen |
| Gigastruct | Großbauwerke und Bauaufgaben | „Bauaufgabe“ | keine KI-Bilder realer, benannter Bauwerke |
| Suitwerk | Herrenanzug und Stoffkunde | „Kreidestrich“, realer animierter Anzug in jedem Video | Passform-Themen erst mit besseren Quellen |
| Frontlore | Militärgeschichte, nur historisch | „Rekonstruktion“ | Risiko hoch, ohne Waffen und Hoheitszeichen im Bild |
| Gritwerk | Psychologie der Selbstdisziplin | „Laborbuch“: ein veröffentlichter Versuch je Video mit Grenzen und Replikationsstand | Mitmachteil am Schluss |

## 2. Stand in Zahlen (03.11.2026, 17:00)

**Fertige Videos im freigegebenen Format: 20.** Das sind je Marke das Testvideo in Deutsch (Neufassung mit der korrigierten Tonebene) und in Englisch, also 18, plus das erste Tintora-Reel F1-04 „Der Weg zum Echoberg“ in Deutsch und Englisch. Alle 20 haben den automatischen Prüfbericht bestanden (Pegel, Überschneidungen, kleine Schrift, Lizenzzeilen, Stille, Schwarzbilder); bei Dewlane und Frontlore steht wegen „Risiko hoch“ zusätzlich die Freigabe von Hand.

| Marke | Fertig DE | Fertig EN | Länge |
|---|---|---|---|
| Scutoria Reels „Chef-Mail“ | 1 | 1 | 75 s / 72 s |
| Promptwerk „Dubletten“ | 1 | 1 | 76 s / 76 s |
| Tintora Testreel F1-06 und Reel F1-04 | 2 | 2 | 83–89 s |
| Dewlane „Testmenge“ | 1 | 1 | 79 s / 81 s |
| Revlore „Sicherungsautomat“ | 1 | 1 | 87 s / 77 s |
| Gigastruct „Fehmarnbelt Absenken“ | 1 | 1 | 84 s / 84 s |
| Suitwerk „Köper und Leinwand“ | 1 | 1 | 83 s / 77 s |
| Frontlore „Fackeltelegraf“ | 1 | 1 | 75 s / 83 s |
| Gritwerk „Willenskraft“ | 1 | 1 | 86 s / 86 s |
| Summe | 10 | 10 | |

Dazu: Scutoria-YouTube-Video 01 „KI-Regeln“ (etwa 16 Minuten) rendert gerade; die Zwischenprobe (2:28 min) ist von Stefan freigegeben. Anschließend entstehen daraus sechs Reels und Thumbnails.

Außerdem liegen 71 ältere Exportdateien in den Produktionsordnern: die neun ersetzten Erstfassungen der Testvideos (lautere Geräusche) und die Videos aus den Produktionswellen vor der Pause vom 02.11. (45 Reels, das alte Scutoria-YouTube-Video mit sechs Reels, Piloten). Sie sind nicht freigegeben und werden nicht veröffentlicht; die Stimmen daraus bleiben als Vorrat.

Veröffentlicht: nichts. Konten: keine angelegt (Google Workspace als Zentrale steht, Aliase und Markenkonten fehlen). Upload-Post: Schlüssel fehlt, Endpunkte im Code noch nicht verifiziert.

## 3. Wie ein Video entsteht

1. **Thema** aus dem Konzeptplan je Marke (zusammen 689 Vorschläge, je Marke mindestens 50; Bildaufbauten wechseln nach festem Muster, damit die Videos nicht gleich aussehen).
2. **Regie-Skript** (Story-Engine: Hook, Beats, Szenentypen, Wortanker, Marker Fakt/Auslegung/Unsicher/Lücke mit Quellenzeile, Ton-Cues). Heute schreiben das neun Claude-Code-Sitzungen von Hand nach der Format-Bibel der Marke; ab etwa 06.11. soll das ein „Tagesläufer“ tun (siehe 5).
3. **Bildmaterial**: animierte Szenen aus dem gemeinsamen Renderer plus fotorealistische Einschübe aus der Realbild-Bibliothek der Marke (Higgsfield Nano Banana Pro, je Marke 17 bis 29 Bilder und ein Kling-Clip; Hände und Menschen von hinten erlaubt, nie Gesichter, keine echten Marken, kein lesbarer Text; jedes Bild mit Etikett „KI-generierte Darstellung“). Die Bibliotheken sind seit heute für alle sieben Reel-Marken fertig.
4. **Stimme**: nur Gemini TTS (Flash, 100 Anfragen am Tag für alle Marken zusammen; Pro als Ausweich, Tintora nur Pro). Keine Windows-Stimme, keine anderen Modelle.
5. **Tonebene** (seit heute): zwölf selbst erzeugte Geräusche (Übergänge, Klicks, Stempel, Papier) und ein prozedurales Musikbett, das beim Sprechen abgesenkt wird; keine fremde Musik, daher keine Lizenzfrage. Stefans Korrektur „Wisch-Geräusche zu laut“ ist umgesetzt: Standard -16 dBFS statt -9, einzelne Marken -18 bis -19.
6. **Render**: HyperFrames (GSAP) und FFmpeg mit NVENC auf dem Laptop, 1080x1920, eine Warteschlange, ein Render nach dem anderen; Langvideo 16:9 mit eigenem Composer.
7. **Prüfung**: Lautheit -16 LUFS, Spitzenpegel, Überschneidungen von Textelementen, Schriftgröße, Stille, Schwarzbilder, Lizenzzeilen für jedes Bild, Whisper-Transkript gegen den Text. Ergebnis VALIDATED oder HUMAN_REVIEW (Risiko hoch).
8. **Export** nach `05 Produktion\<Marke>\<Monat>\<Datum Kurztitel>` mit Prüfbericht und Veröffentlichungstext; Zeile im Redaktionsplan. Veröffentlichung später über Upload-Post, bis dahin nichts.

Aufwand je Reel heute: Render etwa 1,1- bis 1,4-fache Laufzeit plus Prüfungen, also wenige Minuten Maschinenzeit; der teure Teil ist das Schreiben durch Claude (siehe 5).

## 4. Chronik der letzten 24 Stunden

- **02.11., 22:00**: Stefans Urteil über die ersten Produktionswellen: Schulnote 4 von 5. Die Videos waren einander zu ähnlich, ohne Realitätsnähe, ohne Ton und Musik; das Scutoria-YouTube-Video schlechter als die Woche davor. Sieben Vorgaben: 50 Themen je Marke, Takt 2 Themen je Tag und Marke in DE und EN (4 Videos), realistische Darstellung und Variation, Scutoria YouTube zurück auf Vorwochen-Niveau, Codex-Kritik berücksichtigen, alles pausieren, Higgsfield nutzen. Neustart mit einem Testvideo je Marke zur Freigabe.
- **03.11., 00:00 bis 11:00**: Testvideo-Konzepte je Marke, Realbilder und Clips (Kappe 100 Credits je Marke), Tonebene im gemeinsamen Renderer gebaut, neun Testvideos gerendert und Stefan geschickt.
- **11:55**: Stefan gibt alle neun Testvideos frei, mit der Korrektur „Wisch-Geräusche zu laut“. Alle Marken rendern neu und bauen die englische Fassung; um 13:16 sind alle 18 fertig.
- **13:03**: Neue Verteilung des Higgsfield-Restguthabens (Abschnitt 5). **13:19**: Pegel bestätigt. Tintora Folge 1 auf acht Hochformat-Reels gekürzt (16:9-Folge im Dezember).
- **13:45**: Bibliotheken für alle sieben Reel-Marken fertig. **16:30**: Scutoria-YouTube-Zwischenprobe freigegeben, Render des ganzen Videos 01.
- **16:39 und 16:45**: Wegen des Claude-Kontingents (Abschnitt 5): Marken-Sitzungen auf Sonnet 5.5, Takt am 04.11. halbiert, neue Sitzung „Tagesläufer“, Betrieb über das normale Ultra-Abo (kein API-Schlüssel).

## 5. Kosten und Kontingente

**Higgsfield Ultra (3.000 Credits für November), Guthaben um 17:00: 1.108,75.** Verbraucht seit 02.11. zusammen 1.891 Credits, darunter: neun Testvideos rund 700 (Bilder und Clips, einschließlich Scutoria-YouTube-Vorbereitung 80), Bibliotheken 400, Konzeptbilder rund 130, Tintora Stufe 0 102 und Reels rund 93, Test AI Influencer Studio 2; der Rest entfiel auf die Piloten vor der Pause (Einzelposten in der Transaktionsliste bei Higgsfield, hier nicht nachgerechnet). Verteilung des Rests (von Stefan am 03.11. freigegeben): Tintora Folge 1 bis 500, Scutoria YouTube 250, Tagesproduktion 300 (33 je Marke bis 30.11., höchstens 2 Credits je Thema), Reserve 152; die Bibliotheken sind damit abgeschlossen. Preise: Nano Banana Pro 2 Credits je Bild, Kling 5 s 6,25, Kling 8 s pro 10.

**Gemini TTS**: bisher 3,74 USD für 200 bezahlte Anfragen (etwa 2 Cent je Reel mit Flash, 4 Cent mit Pro). Grenze: 100 Flash-Anfragen am Tag für alle Marken; bei 2 Themen je Marke in DE und EN sind das 32 bis 36 Anfragen für die acht Reel-Marken, Tintora braucht je Reel bis zu 12 Pro-Anfragen (eigenes Kontingent, Tageslimit nicht ermittelbar, beobachtet 50).

**Claude Ultra-Abo**: Das Wochenkontingent (Reset 09.11., 13:00 Wien) stand um 13:25 bei 63 Prozent und um 17:00 bei 74 Prozent, nach rund 28 Stunden der Woche. Ursache: dreizehn parallele Claude-Code-Sitzungen (neun Marken, Scutoria YouTube, Bibliotheken, Tonebene, Hauptsitzung), jede mit langem Verlauf, der bei jeder Antwort mitgezahlt wird. Beschlossene Gegenmaßnahmen: Marken-Sitzungen auf Sonnet 5.5; Takt am 04.11. nur 1 Thema je Marke; Meldungen gebündelt; ein „Tagesläufer“, der Regie-Skripte als kurze, eigenständige Aufträge über Claude Code headless (`claude -p`, Sonnet) erzeugt und die übrige Kette (Stimme, Render, Prüfung, Export) ohne Modell laufen lässt; danach Archivierung der Marken-Sitzungen. Ein API-Schlüssel ist nicht gewünscht. Ob der Tagesläufer das Kontingent ausreichend entlastet, ist erst nach dem ersten Lauf messbar.

**Sonstiges**: Upload-Post und Plattformkonten stehen aus (Stefan). Laptop muss für die geplanten Aufgaben wach und am Netz sein. OneDrive-Speicher wird mit Rohmaterial knapp, fertige Projekte können auf „nur online“ gestellt werden.

## 6. Regeln, die für alles gelten

Nichts wird veröffentlicht, kein Konto angelegt, kein Passwort oder Schlüssel in Dateien oder Chats; Claude löscht nichts (Unerwünschtes wandert in einen Ordner zum Löschen). Keine Gesichter in KI-Bildern, immer Kennzeichnung als KI-Darstellung, synthetische Stimme ausgewiesen (EU-Leitlinien zu Art. 50 KI-Verordnung liegen in der Ablage). Quellenpflicht: Fakten mit Quelle, Auslegung und Unsicherheit als Marker im Bild; Risiko „hoch“ (Gesundheit, Militärgeschichte) nur mit Freigabe von Stefan. Keine echten Marken oder Logos, keine KI-Bilder realer benannter Bauwerke, keine Darstellung als echter Produkttest. Musik nur selbst erzeugt oder mit Lizenznachweis. Bezahlte Dienste nur innerhalb freigegebener Kappen.

## 7. Offene Punkte und Risiken

1. **Veröffentlichung ist der Engpass, nicht die Produktion.** Ohne Konten, Impressum-Seite und Upload-Post entsteht Vorrat, aber kein Kanal. Stefan muss die Google-Workspace-Absicherung, die Markenkonten (zuerst Scutoria, Gritwerk, eine dritte), den Upload-Post-Schlüssel und einen privaten Testupload erledigen; die Upload-Post-Endpunkte im Code sind unverifiziert.
2. **Claude-Kontingent**: 74 Prozent nach gut einem Tag. Der Takt 2 + 2 mit neun Sitzungen ist auf diesem Weg nicht durchzuhalten; der Tagesläufer ist noch nicht gebaut (Ziel 06.11.), sein Verbrauch nicht ermittelbar.
3. **Qualität gegen Menge**: 36 Videos am Tag (2 Themen, 9 Marken, 2 Sprachen) sind nur mit Vorlagen und Bibliotheken machbar; ob die Variation dann noch reicht, zeigt erst die zweite Woche. Stefans Maßstab ist das Scutoria-Video mit Note 1,7 und das Vorwochen-Langvideo mit Note 1.
4. **Tintora**: Mit 500 Credits entstehen acht Reels, keine 16:9-Folge; die Serie braucht im Dezember neue Credits. Plattformregeln für Kinderinhalte (YouTube „speziell für Kinder“, TikTok und Instagram ohne Ansprache unter 13) sind einzuhalten.
5. **Risiko-hoch-Marken** (Dewlane Beauty, Frontlore Militärgeschichte) bleiben auf Handfreigabe; das kostet Stefan Zeit je Video.
6. **Rechtliches**: Impressum mit Scutoria-Adresse geplant, Gewerbe und Steuerberatung offen, Markenregister für Tintora ungeprüft, Handles nur reserviert, nicht gesichert.
7. **Technik**: ein Render nach dem anderen (RTX 5080 Laptop), Gemini-Tageslimits, Whisper-Transkript als einzige Hörprüfung, Hauptsitzung mit 614.000 Token Verlauf (wird bei Bedarf neu gestartet).

## 8. Plan für die nächsten sieben Tage

- **04.11.**: Je Marke ein Thema in DE und EN aus den Konzeptplänen (18 Videos), über die Marken-Sitzungen auf Sonnet; Scutoria-YouTube-Video 01 fertig prüfen, Stefan schickt, dann sechs Reels und Thumbnails; Tintora Reel F1-05.
- **05. bis 06.11.**: Tagesläufer: Bestandsaufnahme der Pläne, Prototyp mit Revlore und Suitwerk, dann alle Marken; Aufgabenvorlage für die Windows-Aufgabenplanung; Marken-Sitzungen danach archivieren.
- **bis 09.11.**: Stefan: Konten und Upload-Post; erster privater Testupload; Takt je nach Kontingent wieder auf 2 Themen; Puffer von 7 bis 14 Tagen je Kanal aufbauen.
- Laufend: Kostenlog, Drive-Übersicht, Prüfberichte; Scutoria YouTube Video 02; Tintora Reels 3 bis 8.

## 9. Fragen an ChatGPT

1. Ist der Takt „2 Themen je Marke und Tag, jedes in DE und EN“ für neun junge Kanäle sinnvoll, oder wäre weniger mit mehr Variation und Hook-Tests besser? Welche Startmenge je Kanal empfiehlst du für die ersten zwei Wochen?
2. Alle neun Kanäle gleichzeitig starten oder gestaffelt (zuerst Scutoria, Gritwerk, eine dritte)? Nach welchem Kriterium staffeln?
3. Wie würdest du das Claude-Kontingent weiter senken: Architektur des Tagesläufers (kurze Aufträge, Few-Shot-Beispiele, Validierung), Batching mehrerer Themen je Aufruf, Verzicht auf Sitzungen je Marke? Wo liegt das Risiko für die Qualität?
4. Ist die Verteilung der verbleibenden 1.108 Higgsfield-Credits sinnvoll (Tintora 500, Scutoria YouTube 250, Tagesproduktion 300, Reserve)? Was würdest du streichen?
5. Welche Plattformregeln und rechtlichen Punkte (Österreich/EU, KI-Kennzeichnung, Kinderinhalte, Beauty-Aussagen, Militärgeschichte) sind vor dem ersten Upload zwingend zu klären?
6. Was fehlt im Konzept, das ein erfahrener Betreiber solcher Netze als Erstes ändern würde (Hooks, Thumbnails, Posting-Zeiten, Kommentare, Analytik)?

Anhänge auf Anfrage: Format-Bibeln je Marke, Konzeptpläne, Prüfberichte, Testvideos (DE und EN), Zwischenprobe Scutoria YouTube.
