# Masterplan: Automatisiertes KI-Kurzvideo-Netzwerk (ChatGPT)

Quelle: von Stefan am 29.10.2026 eingefügt. ChatGPT hat auf den von Grok formulierten Kurzbrief geantwortet, dann auf Stefans Nachfragen (Laptop statt Mac mini, Windows 11, Templates je Kanal, Namen und Mail-Adressen). Wortlaut inhaltlich unverändert, nur als Markdown gesetzt; interaktive Rechner und Bildreferenzen der Originalseite sind nur beschrieben. Alle Zahlen hat Claude am 29.10.2026 eigenständig geprüft, siehe `Faktencheck 2026-10-29.md`. Dort steht auch, was hier nicht stimmt.

---

## Der Kurzbrief (von Grok für ChatGPT)

Ich möchte ein vollständig automatisiertes Netzwerk aus KI-Kurzvideo-Kanälen planen und offiziell, regelkonform umsetzen.

Ausgangslage:
- Wohnsitz Österreich. Das TikTok Creator Rewards Program ist hier derzeit nicht verfügbar. Keine Umgehung per VPN oder fremdem Wohnsitz; alles so aufbauen, dass Rewards aktivierbar sind, sobald sie offiziell verfügbar werden.
- Nebenbeschäftigung ist abgeklärt. KI-Inhalte werden auf allen Plattformen gekennzeichnet.
- Hardware: Mac mini M1 (2020) mit 8 GB RAM als Steuerzentrale. Rechenintensive Video- und Sprachgenerierung läuft in der Cloud. *(später geändert: Windows-11-Laptop)*
- Tools: Claude Max mit Claude Code.

Ziel:
- 5 bis 7 Kanäle mit je eigener Nische, jeweils auf TikTok, Instagram Reels und YouTube Shorts.
- Alles zweisprachig, Deutsch und Englisch.
- Pro Kanal eine eigene Gmail-Adresse.
- 3 Videos pro Tag und Kanal, jeweils über 1 Minute lang, vollständig automatisiert.
- Themenplanung jeweils 1 Monat im Voraus.
- Getrennte Kanäle, damit Werbepartner gezielt pro Nische buchen können.

Nischen: KI und Sicherheit · Beauty und Schönheitsprodukte · Claude-Workflows und Prompts · Kleidungsstil und Anzugarten · Brainrot · Motivation und Selbsthilfe · Sicherheit und Militär (Taktiken und Techniken, nur öffentlich zugängliche Inhalte). Zum Vergleich: Baustellen und Megakonstruktionen, Motorentechnik.

Gewünscht: 1. Schritt-für-Schritt-Setup (Konten, Gmail, Claude Code mit Projektstruktur und Prompts). 2. Automatisierungspipeline (Themenkalender, Skript, Übersetzung, Sprachausgabe, Video, Schnitt, Upload, Monitoring). 3. Vergleich von Multi-Plattform-Upload-Diensten (Ayrshare, Upload-Post, Blotato) und der offiziellen Plattform-APIs mit Limits. 4. Nischenanalyse. 5. Monetarisierungswege von Österreich aus. 6. Kosten und Umsetzungsplan in Phasen.

Regeln: Nichts erfinden. Jede Zahl mit Quelle und Datum. Nicht Belegbares als „nicht ermittelbar" markieren. Bei jeder Einschätzung das stärkste Gegenargument.

---

## Teil 1: Masterplan (Planungsstand 29.10.2026)

### 1. Zusammenfassung und Machbarkeitsprüfung

Technisch umsetzbar. Wirtschaftlich und plattformrechtlich nicht sofort mit allen Kanälen in voller Produktionsmenge starten. Architektur von Anfang an für alle Nischen entwickeln, Betrieb mit wenigen Kanälen validieren.

Der Bauplan des Kollegen liefert das Grundgerüst (Claude plant und produziert, Freigabewarteschlange, API-Dienst verteilt, Dashboard), beschreibt aber ein Windows-System mit ca. 40-Sekunden-Videos; für Videolänge, Zweisprachigkeit und Durchsatz anzupassen.

Produktionsumfang (Rechenannahme 30 Tage): 7 Kanäle × 3 Videos × 2 Sprachen = 42 Videos/Tag, 1.260/Monat, 3.780 Uploads/Monat auf drei Plattformen. Eine Nische ist nicht zwangsläufig nur ein Social-Media-Konto; separate Sprachkonten verdoppeln den Aufwand. YouTube: mehrsprachige Audiospuren möglich, sofern für den Kanal verfügbar.

Nicht vorausgesetzt: Creator Rewards in Österreich; dass ein Upload-Dienst alle API-Berechtigungen besitzt; dass KI-Masseninhalte monetarisierbar sind; dass Claude Max unbegrenzte Hintergrundverarbeitung erlaubt; dass automatisches Posten auf allen Plattformen ohne Prüfung funktioniert.

Grundsatz: Produktion maximal automatisieren, Veröffentlichung nur nach überprüfbarer technischer und inhaltlicher Freigabe. Gegenargument: manuelle Freigaben begrenzen die Skalierbarkeit; Antwort: risikobasierter Freigabeprozess (technische Prüfungen automatisch, Mensch nur bei neuen Formaten, sensiblen Themen, Auffälligkeiten).

### 2. Systemarchitektur

Claude Code entwickelt und steuert; Cloud-Dienste erzeugen Medien; eine Datenbank verwaltet den Zustand; autorisierte APIs veröffentlichen.

Kette: Monatlicher Themenkalender → Claude Code (Recherche, Skript, Faktenprüfung, Übersetzung, Produktionsaufträge) → Cloud-TTS DE/EN → Cloud-Video (Bild/Animation) → FFmpeg (Schnitt, Untertitel) → Qualitäts- und Compliance-Gate (Rechte, Originalität, KI-Kennzeichnung, Freigabe) → API-Publisher (TikTok, Instagram Reels, YouTube Shorts) → Monitoring.

| Komponente | Empfehlung | Gegenargument |
|---|---|---|
| Rechner | Steuerzentrale für Scheduler, API-Aufrufe, Datenbank, leichte Medienverarbeitung | Dauerbetrieb nötig |
| Claude Code | Entwicklung, Skripterstellung, Workflow-Logik | Interaktives Abo ist kein garantierter Produktionsserver |
| Cloud-KI | Sprach- und Bild-/Videogenerierung | Kosten, Warteschlangen, wechselnde Modellqualität |
| FFmpeg | Schnitt, Audio-Mix, Formatprüfung | Komplexe Animationen brauchen zusätzliche Renderer |
| PostgreSQL oder SQLite | Zustände, Jobs, Freigaben | SQLite für mehrere verteilte Worker weniger geeignet |
| S3-kompatibler Speicher | Medienarchiv | laufende Kosten |
| Upload-API | geplante Veröffentlichung | plattformabhängige Lücken und Genehmigungen |

Anpassung des Bauplans: Das automatische Hinzufügen eines Chartsongs nicht übernehmen; Musikrechte sind nicht automatisch für kommerzielle Nutzung geklärt.

### 3. Schritt-für-Schritt-Setup

Phase A – Konten: zentrale Verwaltungsidentität mit Passwortmanager und MFA; je Marke eigene Gmail-Adresse; je Marke TikTok-, Instagram-, YouTube-Präsenzen; Instagram als professionelles Konto mit Meta-Anbindung; eindeutige Kennung je Kanal; korrekte Eigentümer-, Verifizierungs- und Monetarisierungsdaten; OAuth statt Passwörter in Skripten; gewerbliche Angaben, Kontakt, Datenschutz, Werbekennzeichnung je Profil. Nicht alle Konten gleichzeitig anlegen; keine Automatisierung der Kontoerstellung.

Phase B – Rechner einrichten (Windows-Fassung siehe Teil 2).

Phase C – Projektstruktur:

```
faceless-network/
├── CLAUDE.md
├── .env.example
├── .gitignore
├── config/        channels.yaml · platforms.yaml · policies.yaml · voices.yaml
├── prompts/       research.md · calendar.md · script.md · translate.md · factcheck.md · compliance.md
├── channels/      ai-security/ beauty/ claude-workflows/ menswear/ brainrot/ motivation/ military-tech/
├── src/           scheduler/ research/ generation/ rendering/ publishing/ analytics/ compliance/
├── data/          calendars/ scripts/ manifests/ analytics/
├── storage/       drafts/ approved/ published/
├── tests/
└── logs/
```

Beispiel CLAUDE.md (Betriebsregeln): nur rechtmäßig nutzbare Quellen; keine erfundenen Fakten, Studien, Zitate; Quellen-URL und Abrufdatum speichern; Tatsachen, Meinungen, Simulationen trennen; eigenständige redaktionelle Inhalte; synthetische Inhalte kennzeichnen; keine ungeklärten Musik- oder Bildrechte; keine Heilversprechen; keine operativen Gewalt- oder Waffenanleitungen; keine Umgehung von Plattformlimits; keine Veröffentlichung ohne APPROVED; nie Schlüssel protokollieren. Produktionsziel 9:16, 65–90 s, DE und EN, plattformangepasste Metadaten, Quellen- und Lizenzmanifest pro Video. Status: NEEDS_RESEARCH, BLOCKED, HUMAN_REVIEW, READY_FOR_REVIEW; nur autorisierte Freigaben führen zu APPROVED.

Startprompt für Claude Code: produktionsfähige, aber nicht veröffentlichende Pipeline; Konfigurationsschema; Themenkalender mit Quellenfeldern; Skriptgenerator DE/EN; Fakten- und Richtlinienprüfung; Medienmanifest; Warteschlange mit Freigabestatus; FFmpeg-Renderpipeline; Mock-Publisher; Logging, Wiederholungen, Tests; lokales Dashboard. Keine echten Uploads, keine erfundenen Endpunkte, Umgebungsvariablen, idempotent, keine Zugangsdaten im Repository.

### 4. Produktionspipeline

Kalendereintrag: topic_id, channel_id, language, angle, source_urls, source_checked_at, format, risk_level, publish_at, status. Monatlicher Planungslauf mit wöchentlicher Aktualisierung; Slots für aktuelle Themen reservieren.

Skript-Prompt: Fachredakteur für {{channel_name}}, eigenständiges vertikales Erklärvideo zu {{topic}}, Zielgruppe, Sprache, 65–90 s, sofort verständlicher Einstieg, klarer Erkenntnisgewinn, keine erfundenen Fakten, kein Umschreiben fremder Videos. Ausgabe: Arbeitstitel, Hook, Sprechertext, Szenenfolge mit Zeitmarken, Quellen, Bildanweisungen, Risikohinweise, Plattformbeschreibungen, KI-Kennzeichnung, offene Fragen. UNVERIFIED-Aussagen blockieren die Produktion. Zweite Sprachfassung lokalisiert, nicht wörtlich übersetzt.

Videotypen: Erklärvideos (KI-Stimme, Typo-Animation, Grafiken); Beauty/Mode (lizenzierte Produktbilder, eigene Diagramme); Technik (schematische Animationen); Brainrot (eigene Figuren, originale Animationen, lizenzierte Musik); Militärtechnik (historisch-technisch, keine operativen Anleitungen). Ein einzelner generativer Videodienst für alles wäre unnötig teuer.

Qualitätskontrolle vor Upload: gültige Datei mit Audio, Länge, Seitenverhältnis; Untertitel stimmen; keine schwarzen Bilder; Fakten, Bildrechte, Musiklizenzen dokumentiert; KI- und Werbekennzeichnung gesetzt; keine Duplikate; Freigabe und autorisiertes Konto. Zustände: PLANNED → RESEARCHED → SCRIPTED → RENDERED → VALIDATED → APPROVED → SCHEDULED → PUBLISHED → VERIFIED. Fehlgeschlagene Uploads in eigene Warteschlange, kein blinder Retry.

### 5. Plattform-APIs und Upload-Dienste (laut ChatGPT, Abruf 29.10.2026)

- TikTok Content Posting API: nicht auditierte Clients nur privat; höchstens 5 aktive Nutzer/24 h; Posting-Cap typischerweise ca. 15/Tag; rein interne Upload-App für eigene Konten ist kein akzeptabler Anwendungsfall.
- YouTube Data API: Standardkontingent 100 videos.insert pro Tag und Projekt (Änderungen Dezember 2025 und Juni 2026; nicht mehr mit 1.600 Punkten je Upload rechnen).
- Instagram: exakte Reels-Grenze je Konto und 24 h nicht ermittelbar.

| Dienst | API | Preis (USD, laut ChatGPT) | Einschätzung |
|---|---|---|---|
| Ayrshare | ja | Premium 149/Monat; Launch 299/Monat (bis 10 Profile) | gut dokumentiert, teuer |
| Upload-Post | ja, REST und MCP-Server | Free 0 (2 Profile); Basic 16/Monat jährlich (5); Professional 33/Monat jährlich (25); Advanced 118/Monat jährlich (75) | erster Testkandidat: Professional |
| Blotato | zu verifizieren | nicht ermittelbar | Alternative |
| Offizielle APIs | nach Berechtigung | keine Gebühr | höchste Kontrolle, höchster Prüfaufwand |

Upload-Post dokumentiert eigene Tagesgrenzen je verbundenem Konto: TikTok 15, Instagram 50, YouTube 30. Auswahlverfahren: realer Integrationstest je Anbieter (autorisiertes Konto, KI-gekennzeichnetes Video, geplanter Upload, Status, Fehler, Analytics, Prüfung in der App). Publisher-Schnittstelle austauschbar halten.

### 6. Nischenanalyse (qualitativ, keine Marktstudie)

| Nische | Nachfrage | Werbepotenzial | KI-Produktion | Richtlinienrisiko |
|---|---|---|---|---|
| KI und Sicherheit | hoch | hoch | sehr gut | mittel |
| Beauty | hoch | hoch | gut | mittel–hoch |
| Claude-Workflows | hoch | sehr hoch | sehr gut | niedrig–mittel |
| Anzüge und Stil | mittel | hoch | sehr gut | niedrig |
| Brainrot | hoch, volatil | eher gering | sehr gut | mittel–hoch |
| Motivation | hoch | mittel | sehr gut | mittel |
| Sicherheit und Militär | mittel–hoch | mittel | gut | hoch |
| Megakonstruktionen | mittel–hoch | mittel | sehr gut | niedrig–mittel |
| Motorentechnik | mittel–hoch | hoch | gut | mittel |

Priorisierung: 1. Claude-Workflows (Pilot), 2. Kleidungsstil und Anzüge, 3. KI und Sicherheit, 4. Motorentechnik, 5. Megakonstruktionen. Militär und Brainrot nur als kontrollierte Formatversuche. Je Nische das stärkste Gegenargument: Tutorials veralten; Sicherheitsbehauptungen brauchen Prüfung; ohne Produktkenntnis geringe Glaubwürdigkeit; synthetische Vorher-Nachher sind Risiko; Trendabhängigkeit; generische Zitate; Gewaltbezug und Werbetauglichkeit; technische Fehler mit realen Folgen.

### 7. Monetarisierung aus Österreich

| Modell | Österreich | Voraussetzung |
|---|---|---|
| YouTube-Partnerprogramm | verfügbar | 1.000 Abonnenten und 4.000 Wiedergabestunden/12 Monate oder 10 Mio. Shorts-Aufrufe/90 Tage |
| TikTok Creator Rewards | nicht eingeplant | Länderfreigabe |
| Markenkooperationen | möglich | Vertrag, Kennzeichnung, Steuer |
| Affiliate | möglich | Partnerprogramm |
| Eigene digitale Produkte | möglich | Recht, Steuer |
| Newsletter, Mitgliedschaften | möglich | Anbieter, Verbraucherrecht |
| Instagram-Funktionen | je Funktion prüfen | Konto, Land |

YouTube hat am 15.07.2025 die Richtlinie zu repetitiven Inhalten unter „inauthentic content" präzisiert. Strategie: nicht nur auf Plattformauszahlungen setzen; Claude-Workflows → Prompt-Pakete, Vorlagen, Softwarepartner; Anzüge → Affiliate; KI-Sicherheit → Fachsoftware, Schulungen, B2B. Österreich: WKO unterscheidet Creator-Einkünfte; Werbung, Kooperationen, Affiliate in der Regel Gewerbeanmeldung; Steuerberatung für ausländische Plattformen, Umsatzsteuer, EU-Leistungen, Sachleistungen; Werbung und Affiliate kennzeichnen; online gefundene Bilder nicht automatisch kommerziell nutzbar.

### 8. Kostenmodell

Keine belastbare Vollkostenrechnung ohne konkrete Anbieter. Szenariorechner: 630 Sprachvideos/Monat × 0,40 € + 100 € Fixkosten + Publisher = ca. 385 €/Monat (reine Annahme). Entscheidend ist der gemessene Preis je veröffentlichungsfähigem Video inkl. Fehlgenerierungen, Wiederholungen, Prüfzeit, Speicher.

### 9. Umsetzungsplan

Phase A Fundament (Wochen 1–2): Projekt, Datenmodell, Kontenstruktur, Compliance, Mock-Publisher; Abnahme: Testvideo ohne Upload. Phase B Pilot (Wochen 3–4): Claude-Workflows DE/EN; TTS, Untertitel, Render, Publisher, Status; Abnahme: wiederholbare Veröffentlichungen, nachvollziehbare Kosten. Phase C Mehrere Nischen (Wochen 5–8): Kleidungsstil, KI-Sicherheit, Monatsplanung automatisieren, Monitoring. Phase D Skalierung (ab Woche 9): weitere Nischen nur bei nachgewiesener Qualität und Wirtschaftlichkeit. Dashboard-Kennzahlen: Kosten je freigegebenem Video, Erfolgsquote Uploads, Verwurfquote, Views, Wiedergabedauer, Netto-Follower, Umsatz je Nische, offene Rechtefragen.

### 10. Offene Punkte

Creator Rewards AT; Blotato-Preise; Instagram-Limit; Kosten KI-Video; Nischennachfrage; Sponsoringumsätze; Claude-Max-Automationskapazität. Zielkonfiguration: Rechner + Claude Code + Python/Node.js + FFmpeg + Cloud-TTS/Video + Datenbank + austauschbarer Upload-Post-Publisher + Dashboard. Entscheidungen: Architektur für alle Nischen; Pilot Claude-Workflows; DE und EN produzieren, Sprachkonten erst nach Test trennen; Upload-Post testen; Claude Code als Orchestrierungswerkzeug, nicht als alleinige unbeaufsichtigte Laufzeit; Rewards nicht einplanen; Umfang erst nach Nachweis erhöhen.

---

## Teil 2: Bauplan für Windows 11 (Stefans Nachfrage)

Rechner: Windows-11-Laptop statt Mac mini. Claude Code als zentrales Werkzeug. Laptop im Schlafmodus führt lokale Aufgaben nicht aus; für Dauerbetrieb Laptop eingeschaltet lassen oder später Cloud-Worker.

Installation (winget): Git.Git, OpenJS.NodeJS.LTS, Python.Python.3.13, Gyan.FFmpeg, Microsoft.VisualStudioCode, Anthropic.ClaudeCode. Projektordner `C:\AI-Faceless-Network`, `git init`, `claude`. Anthropic unterscheidet lokale geplante Desktop-Aufgaben, Cloud-Routines und zeitlich begrenzte Wiederholungen in der CLI; Cloud-Routines laufen unabhängig vom Laptop.

Großer Projektauftrag an Claude Code: Rolle leitender Architekt; Umgebung Windows 11, `C:\AI-Faceless-Network`, Claude Max, Python/Node/FFmpeg/Git, Cloud für Medien, Windows-Aufgabenplanung; Ziel 7 Marken, 3 Plattformen, DE/EN, 3 Videos täglich je Marke als Skalierungsziel, ≥ 61 s (65–90 s), Monatskalender, getrennte Konten, Monetarisierung aus Österreich ohne Länderumgehung; Architektur: modulare Python/Node-Anwendung mit Konfiguration, SQLite, Themenplanung, Skript- und Übersetzungspipeline, TTS-Adapter, Bild-/Video-Adapter, FFmpeg, Qualitäts- und Compliance-Prüfung, Freigabewarteschlange, austauschbarer Publisher (Upload-Post zuerst), Monitoring, Web-Dashboard, Task-Scheduler, Logging, Tests. Regeln: keine echten Uploads ohne Freigabe, keine erfundenen Endpunkte, keine Zugangsdaten in Git, keine automatisierte Kontoerstellung, keine Umgehung von Limits, Kennzeichnung, keine ungeklärten Rechte, keine Duplikate, keine kostenpflichtigen Dienste ohne Zustimmung.

Kontenstruktur: Marke → Gmail → je Sprache TikTok/Instagram/YouTube. Variante gemeinsame Sprachkonten (weniger Konten) vs. getrennte (klare Zielgruppen, mehr Aufwand). Software für beide Varianten auslegen; Pilot mit wenigen echten Konten, Rest als Konfiguration (`enabled: false`). Gmail nicht massenhaft per Browserautomatisierung anlegen.

Claude Skills (`.claude/skills/`): calendar-planner, research-factcheck, script-writer, translator, voice-generator, video-producer, video-editor, compliance-check, social-publisher, analytics-review. Beginn mit den ersten drei.

Tagesplan (Vorschlag): 07:00 Tagesplanung · 07:30 Skripte · 08:00 Cloud-Produktion · 09:00 Rendering · 10:00 Qualitätskontrolle · 11:00 Freigabe · nach Freigabe Scheduling · 19:30 Monitoring.

Upload-Post: REST-API (POST /api/upload, Status, geplante Veröffentlichung, externe IDs, Parameter zur KI-Kennzeichnung), offizieller MCP-Server; Tagesgrenzen je Konto TikTok 15 / Instagram 50 / YouTube 30 (laut Upload-Post-FAQ). Adapter: Verbindungstest, Profile, Zielplattform, Freigabe, KI-Kennzeichnung, geplante Veröffentlichung, Job-ID, Status, Fehlerprotokoll, Retry ohne Doppelposts, Dry-Run; nicht Dokumentiertes als NOT_VERIFIED.

Automation unter Windows: Variante A Claude Desktop Scheduled Tasks (Anweisung im Kontext, abhängig vom Rechnerzustand); Variante B Windows-Aufgabenplanung (bevorzugt für die Produktionspipeline): Aufgabe „Faceless-Daily-Production", täglich, `powershell.exe` mit Startskript (`.venv\Scripts\python.exe .\src\run_pipeline.py --mode daily --dry-run`), nur bei Netzstrom, Wiederholungen, verpasste Starts nachholen.

Dashboard: lokales Web-Dashboard im Browser mit Kanalfilter, DE/EN-Status, Vorschauen, Freigabeprotokoll, Kosten, Links, Fehler, Statistik; Zugriff vom Handy nur mit sicherer Anmeldung, kein offener Port.

Nischenregeln: KI-Sicherheit (keine missbrauchsfähigen Details), Beauty (keine erfundenen Tests, keine Wirkversprechen), Claude-Workflows (funktionierende Beispiele), Anzüge (korrekte Darstellung, transparente Links), Brainrot (keine kopierten Charaktere), Motivation (keine psychologischen/medizinischen Versprechen), Militärtechnik (keine operativen Anleitungen).

Ausbauphasen: 1 Fundament · 2 Video-Pilot (ein Kanal, DE/EN, ohne Upload) · 3 Publisher-Pilot · 4 Mehrkanalbetrieb · 5 Vollausbau.

---

## Teil 3: Video-Templates für neun Kanäle

Gemeinsames Designsystem: 9:16, 1080 × 1920; einheitliche Logo-Position und Titelanimation; zwei Schriftfamilien (z. B. Inter für Text, Montserrat für Titel, Rechte prüfen); maximal zwei Schriftgrößen für Einblendungen; keine großen Wasserzeichen; gleicher Stil für Untertitel, Fortschrittsanzeige, Schlussbild; je Kanal feste Palette; 65–90 s; DE und EN gleiches Layout. Layout: Markenlogo oben, Zähler (01/05), visuelle Hauptszene, Untertitel in der sicheren Zone, Abschluss/Quellen/CTA unten.

| Nr. | Kanal | Stil | Palette |
|---|---|---|---|
| 01 | KI & Cybersecurity | Tech Editorial, seriös; Diagramme, Netzwerke, ruhige Kamera | #0B132B · #00D4FF · #F4F7FB |
| 02 | Beauty | Luxury Editorial, elegant; weiches Licht, Produkt-Makros | #F8F3EF · #C98F93 · #6C4B50 |
| 03 | Claude-Workflows & Prompts | Clean SaaS, didaktisch; echte Bildschirmaufnahmen, Klickpfade | #171923 · #A78BFA · #F8FAFC |
| 04 | Anzüge & Herrenstil | Quiet Luxury, zeitlos; Stofftexturen, Details | #172337 · #D4B483 · #F2EEE6 |
| 05 | Brainrot & Surreal Comedy | Surreal 3D, verspielt; eigene Figuren, schnelle Schnitte | #B7FF00 · #FF43C0 · #101010 |
| 06 | Motivation & Selbstentwicklung | Cinematic Human, emotional; Landschaften, kraftvolle Typografie | #121212 · #E5B45A · #F4F0E8 |
| 07 | Militärtechnik & Geschichte | Documentary Tech, sachlich; Karten, Querschnitte | #29352D · #A9B29F · #E6E9E5 |
| 08 | Megakonstruktionen & Baustellen | Engineering Epic, monumental; Luftaufnahmen, 3D-Schnitte | #20384F · #FF8A2A · #E9EDF0 |
| 09 | Motorentechnik | Precision Engineering, technisch; Explosionszeichnungen | #171C22 · #AEB9C5 · #2F9BFF |

Beispiel-Vorlage (Kanal 01), Datei `.claude/brand-templates/ai_security.md`:

```
ROLLE: Du bist Creative Director für einen seriösen KI- und Cybersecurity-Erklärkanal.
MARKENIDENTITÄT: Editorial Tech, hochwertig, sachlich, modern. Farben: Hintergrund #0B132B, Akzent #00D4FF, Text #F4F7FB.
Typografie: Montserrat SemiBold für Titel, Inter für Untertitel. Wiederkehrende Elemente: dezentes Datenraster, cyanfarbene Linien, nummerierte Infokarten.
BILDSPRACHE: Cinematische technische Visualisierungen, abstrakte Netzwerke, echte Softwareansichten bei Tutorials. Keine klischeehaften Hacker mit Kapuzen. Keine erfundenen Screenshots, Vorfälle oder Statistiken. 70 % erklärende Szenen, 30 % atmosphärisch.
SZENEN: 1. Hook mit nachvollziehbarer Frage. 2. Visuelle Erklärung des Problems. 3. Zwei bis vier Fakten oder Mechanismen. 4. Praktische, sichere Einordnung. 5. Fazit.
BEWEGUNG: langsame Push-ins, klare Datenanimationen, maximal dezente Glitch-Effekte.
AUDIO: ruhige, kompetente Stimme; zurückhaltende elektronische Musik.
VERBOTEN: erfundene Quellen, Angstmache, operative Missbrauchsanleitungen.
ZIEL: 65–90 Sekunden, 9:16, konsistente Serienoptik.
```

Design technisch erzwingen: Claude erzeugt Geschichte, Szenenplan, Medienprompts; Generatoren liefern Bilder und Clips ohne eingebrannte Untertitel, Logos, Titel; FFmpeg bzw. festes Render-Template fügt die Markenbestandteile hinzu; Claude prüft gegen eine kanalbezogene Design-Checkliste.

Master-Prompt für Claude Code (Template-System): Struktur `brands/<marke>/` mit brand.yaml, visual_style.md, image_prompt.md, video_prompt.md, script_prompt.md, subtitle_style.json, intro_config.json, outro_config.json, audio_style.yaml, assets/, references/, examples/. Anforderungen: 1080 × 1920, 65–90 s, feste Farben/Schriften/Koordinaten, einheitliche Logo- und Untertitelposition, wiederverwendbare Intro/Outro, Motion-Design je Marke, DE/EN ohne Identitätsänderung, Mediengenerierung getrennt vom Rendering, FFmpeg-Templates, automatische Qualitätskontrolle, Manifest je Video, keine Veröffentlichung ohne Freigabe. Reihenfolge: Struktur → Designsystem → neun Konfigurationen → je Marke 10-Sekunden-Demo mit Platzhaltern → Übersicht → Korrektur → erst dann 65–90-s-Produktion.

Timeline 75 s: 0–6 Hook · 6–18 Kontext · 18–57 Hauptteil · 57–69 Fazit · 69–75 CTA (Vorschlag, kein nachgewiesenes Optimum).

Style-Lock je Kanal: Referenzassets versionieren (Logo, Titelkarte, Untertitelbeispiel, Szenenreferenzen, feste Figuren mit Charakter-Sheets bei Brainrot; 3D-Modelle und Diagrammvorlagen bei Technik), `brand_version` 1.0.

---

## Teil 4: Markennamen und Gmail-Adressen (Vorschläge, Verfügbarkeit ungeprüft)

| Nr. | Marke | Nische | Gmail (Vorschlag) | Handle (Vorschlag) |
|---|---|---|---|---|
| 01 | NeuralShield | KI & Cybersecurity | neuralshield.media@gmail.com | @neuralshield.media |
| 02 | VelvetGlow | Beauty | velvetglow.studio@gmail.com | @velvetglow.studio |
| 03 | PromptPilot | Claude-Workflows & Prompts | promptpilot.media@gmail.com | @promptpilot.media |
| 04 | TailoredCode | Anzüge & Herrenstil | tailoredcode.media@gmail.com | @tailoredcode.media |
| 05 | GlitchMango | Brainrot & Surreal Comedy | glitchmango.studio@gmail.com | @glitchmango.studio |
| 06 | RiseTheory | Motivation & Selbstentwicklung | risetheory.media@gmail.com | @risetheory.media |
| 07 | IronArchive | Militärtechnik & Geschichte | ironarchive.media@gmail.com | @ironarchive.media |
| 08 | TitanWorks | Megakonstruktionen & Baustellen | titanworks.media@gmail.com | @titanworks.media |
| 09 | TorqueLab | Motorentechnik | torquelab.media@gmail.com | @torquelab.media |

Bei getrennten Sprachkanälen: `@<marke>.de` und `@<marke>.en`. Namen sind Arbeitsnamen, keine markenrechtlich geprüften Bezeichnungen (PromptPilot, TitanWorks, TorqueLab könnten belegt sein). Vor Festlegung Verfügbarkeit auf Gmail, TikTok, Instagram, YouTube prüfen und Markenkonflikte über TMview und EUIPO. Für geschäftliche Nutzung eigene Domain (`kontakt@<marke>.at`) professioneller als Gmail. Start: nicht neun Gmail-Konten, sondern zuerst NeuralShield, PromptPilot, TorqueLab prüfen und die ersten drei Kanäle einrichten.
