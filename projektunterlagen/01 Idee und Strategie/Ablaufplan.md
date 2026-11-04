# Ablaufplan: vom leeren Ordner zum laufenden Netzwerk

Stand: 29.10.2026, 23:45 (Wien). Phasen mit Abnahmekriterium; die nächste Phase beginnt erst, wenn das Kriterium erfüllt ist. Wochenangaben sind Planungsannahmen, keine Zusagen. Was Stefan selbst tun muss, ist mit **[Stefan]** markiert; alles andere baut Claude.

## Phase 0: Entscheidungen und Rahmen (diese Woche)

1. **[Stefan]** Fragenkatalog beantworten (mindestens Fragen 1–4, 9, 12, 14, 15).
2. Namen prüfen: Handles auf TikTok, Instagram, YouTube, Gmail-Verfügbarkeit, Domain, TMview/EUIPO für die ersten zwei Marken. Ergebnis in `02 Marke`.
3. **[Stefan]** Gewerbe klären: Werbeagentur (freies Gewerbe) bestehend oder neu; Impressumstext festlegen; Steuerberatung informieren (Kleinunternehmergrenze 55.000 €).
4. Speicher: Belegung von C: analysieren, Vorschlag an Stefan; Entscheidung externe SSD oder Aufräumen. Nichts wird gelöscht.
5. Laptop: Energieeinstellungen für Produktionszeiten (kein Standby am Netz), Test, ob die Windows-Aufgabenplanung bei zugeklapptem Deckel läuft.

Abnahme: Antworten liegen vor, zwei Markennamen sind frei, Impressumstext steht.

## Phase 1: Pipeline ohne Veröffentlichung (Woche 1–2)

1. Repository `C:\Automation\faceless-network` anlegen (Git, `.env.example`, `CLAUDE.md` mit den Betriebsregeln aus dem Konzept, `config/brands.yaml` mit allen 9 Marken, davon 2 `enabled`).
2. Designsystem: gemeinsames 9:16-Layout, je Marke Palette, Schriften (Lizenz prüfen), Logo-Position, Untertitelstil, Intro/Outro; HyperFrames-Vorlagen; je Marke ein 10-Sekunden-Demo mit Platzhaltern; Übersicht aller Demos an Stefan.
3. Produktionskette lokal: Skript (Claude Code) → TTS (Gemini Flash TTS Paid Tier; Hörprobe DE/EN gegen ElevenLabs) → faster-whisper CUDA → HyperFrames-Render → FFmpeg NVENC → Prüfbericht (Länge 65–90 s, Audio, Untertitel, Seitenverhältnis, schwarze Bilder, Quellen- und Lizenzmanifest, KI-Label gesetzt).
4. Themenkalender: 30 Tage für die zwei Startmarken, jede Zeile mit Quellen, Blickwinkel, Risiko, Status; Ideenspeicher gegen Wiederholungen.
5. Warteschlange und Zustände: PLANNED → RESEARCHED → SCRIPTED → RENDERED → VALIDATED → APPROVED → SCHEDULED → PUBLISHED → VERIFIED; Fehlerwarteschlange; idempotent (kein Doppelpost).
6. Kostenlogger: je Video TTS-Token, Clips, Claude-Aufrufe, Renderzeit.
7. Drei Testvideos je Marke in EN (und DE, wenn Frage 2 so beantwortet), nur lokal.

Abnahme: Ein 75-Sekunden-Video je Startmarke besteht alle Prüfungen, sieht nach Marke aus, Kosten je Video sind gemessen. Stefan sieht die Videos am Handy (per Datei) und sagt, was er ändern will.

## Phase 2: Konten, Publisher, erste echte Posts (Woche 3–4)

1. **[Stefan]** Konten anlegen, von Hand, gestaffelt: je Startmarke den Alias `<marke>@scutoria.com` in Google Workspace (Zentrale `admin@scutoria.com`, Stefan 02.11.2026), YouTube-Kanal als Markenkonto unter admin@ mit zweitem Inhaber, Instagram als Creator-Konto, TikTok Personal Account (nicht Business, wegen Rewards-Fähigkeit); Impressum, Profiltext, Logo einsetzen; admin@ mit Passkey oder Sicherheitsschlüssel und Wiederherstellungsadresse außerhalb der Domain absichern, Passwortmanager. Telefonnummern einplanen (YouTube höchstens 2 Kanäle je Nummer und Jahr).
2. **[Stefan]** Upload-Post-Konto anlegen (Basic, 24 USD monatlich; Jahreszahlung erst nach dem Test), je Marke ein Profil, die drei Plattformen per OAuth verbinden, API-Key erzeugen und Claude nur über `.env` geben.
3. Upload-Post-Adapter: Verbindungstest, Profile abrufen, Dry-Run, geplante Veröffentlichung, KI-Label je Plattform (is_aigc, is_ai_generated, containsSyntheticMedia), Status, Analytics; MCP-Server in Claude Code registrieren.
4. Handy-Zentrale: Claude-Artefakt mit Datenbank (Themenwahl abends, Vorschau, Freigabe, Ablehnung mit Grund), wie im Bauplan des Kollegen; nur Stefan hat den Link.
5. Automationen: Windows-Aufgabenplanung für Render und Upload-Abgleich; Claude-Schritte (Themenvorschläge 19:30, Skripte nach Themenwahl) als Claude Desktop Scheduled Tasks oder `claude -p` aus der Aufgabenplanung; Laufzeiten nach Frage 17.
6. Erster echter Post je Plattform auf jeder Startmarke, von Stefan freigegeben. Prüfung: TikTok-Post ist öffentlich (sonst ist der Dienst nicht auditiert, dann manueller TikTok-Upload), KI-Label sichtbar, Beschreibung und Hashtags korrekt.
7. Betrieb: 1 Video je Marke und Tag, 7-Tage-Puffer freigegebener Videos.

Abnahme: 14 Tage ohne Fehlpost, Doppelpost oder Richtlinienhinweis; Veröffentlichung läuft serverseitig zur Slot-Zeit; Statistik kommt täglich in die Zentrale.

## Phase 3: Zweite Sprache, Takt erhöhen, Auswertung (Woche 5–8)

1. Zweite Sprache: lokalisierte Fassung (nicht Rohübersetzung), eigene TTS-Stimme; Konten je Sprache anlegen (Frage 3), Upload-Post-Profile erweitern.
2. Takt auf 2 Videos je Marke, Sprache und Tag; Themenkalender rollierend (monatlicher Lauf, wöchentliche Aktualisierung, Slots für Aktuelles).
3. Auswertung: Retention, Abschlussrate, Follower, Kommentare je Format; Formate mit schlechter Haltequote streichen; Wochenbericht in `07 Auswertung`.
4. KI-Clips testen: ein 8-Sekunden-Hook-Clip je Video (Runway gen4_turbo 0,40 $ oder Higgsfield), A/B gegen reine Animation; Entscheidung nach Haltequote und Kosten.
5. Einnahmen vorbereiten: Affiliate-Programme (KI-Tools), Media-Kit je Marke (Zielgruppe, Zahlen, Preise), Kontaktadresse für Werbepartner, Gewerbe/Handelsgewerbe laut WKO.
6. Risikobasierte Freigabe: Formate, die Stefan nach 100 Videos als sicher markiert, werden automatisch freigegeben; sensible Themen bleiben manuell.

Abnahme: Kosten je Video stabil, Verwurfquote unter 20 %, erste Kennzahlen je Marke, Entscheidung über Clips und Sprachkonten.

## Phase 4: Kanäle 3–5 und Zielmenge (ab Woche 9)

1. TorqueLab, TitanWorks, TailoredCode anlegen (Konten gestaffelt, je Woche eine Marke); Designsystem ist vorhanden, je Marke nur Konfiguration und Demo.
2. Takt auf 3 Videos je Marke und Tag für die Marken, die es tragen; TikTok-Limit 15/Tag je Konto bleibt weit unterschritten.
3. Upload-Post Professional (25 Profile, 50 USD monatlich / 33 USD jährlich); bei getrennten DE/EN-Konten Advanced (75 Profile).
4. Claude-Nutzung: Verbrauch gegen 5-Stunden- und Wochenlimit messen; bei Engpass API-Key mit Kostenlimit für die Produktionsläufe (saubere Grundlage laut Anthropic für mehr als „ordinary, individual usage").
5. Dashboard: Kosten je freigegebenem Video, Erfolgsquote Uploads, Verwurfquote, Views, Haltequote, Netto-Follower, Umsatz je Marke, offene Rechtefragen, Strikes.

Abnahme: 5 Marken laufen, keine Richtlinienhinweise, Deckungsbeitrag je Marke ist sichtbar.

## Phase 5: Restliche Marken nur bei Nachweis

RiseTheory, IronArchive, VelvetGlow, GlitchMango nur, wenn Phase 4 trägt. IronArchive mit eigener Redaktionsregel (keine Taktikanleitungen, nichts Dienstliches, keine Uniform, keine grafische Gewalt, Art.-50-Offenlegung bei realistischen Szenen). VelvetGlow nur mit echten Produkten oder reinem Inhaltsstoffwissen. GlitchMango als Simulation ohne Figur.

## Was Claude nie automatisch tut

Konten anlegen · Passwörter speichern oder eingeben · Dienste bezahlen · Videos ohne Freigabestatus veröffentlichen · Musik oder Bilder ohne Lizenznachweis verwenden · Plattformlimits umgehen · VPN oder fremden Wohnsitz vortäuschen · dienstliche Inhalte verwenden · etwas löschen.

## Nächster Schritt

Stefan beantwortet den Fragenkatalog (oder sagt „Annahmen gelten"), dann beginnt Phase 1 mit dem Repository und dem Designsystem für die zwei Startmarken.
