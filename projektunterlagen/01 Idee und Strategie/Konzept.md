# Konzept: Automatisiertes KI-Kurzvideo-Netzwerk

Stand: 30.10.2026, 00:30 (Wien). Fassung 2: Stefans Antworten auf den Fragenkatalog (29.10.2026) eingearbeitet. Fassung 1 vom 29.10.2026 beruhte auf den drei Berichten (ChatGPT, Grok, Perplexity), dem Bauplan des Kollegen und dem eigenen Faktencheck.

## Idee in einem Satz

Ein Netzwerk aus getrennten Nischenmarken, deren 60–90-Sekunden-Erklärvideos Claude Code am Laptop weitgehend automatisch plant, schreibt, vertont, rendert und über einen Upload-Dienst auf TikTok, Instagram Reels und YouTube Shorts veröffentlicht, zweisprachig (Deutsch und Englisch), von Österreich aus regelkonform und mit KI-Kennzeichnung.

## Ziel (Vollausbau) und Start

| | Vollausbau (Architektur) | Start (Phase 2) |
|---|---|---|
| Marken | 9, alle in Phase 1 fertig konfiguriert und gestaltet | Veröffentlichung mit 2: Promptwerk und Scutoria |
| Plattformen je Marke | TikTok, Instagram, YouTube, ein Konto je Marke | alle drei |
| Sprachen | DE und EN auf demselben Konto, DE zuerst, EN parallel | beide von Anfang an |
| Slots je Marke und Tag | 3: 12:00, 14:00, 18:00 (Wien) | 3 |
| Länge | 65–90 s, 9:16, 1080 × 1920 | gleich |
| Themenplanung | 30 Tage voraus | 30 Tage voraus |
| Freigabe | automatisch nach bestandener Prüfung; Risiko „hoch" manuell | Empfehlung: erste 20 je Marke von Hand (Kalibrierung), dann automatisch |
| Puffer | 7–14 Tage geprüfte Videos | 7 Tage |
| Kommentare | Claude antwortet (ab Phase 3, eigene Regeln) | nein |

Annahme zu den Slots (Stefan bestätigen): 3 Themen je Marke und Tag, jedes in DE und EN gerendert; je Slot wird eine Sprachfassung gepostet, so dass je Konto 3 Posts/Tag bleiben. Vollausbau rechnerisch: 9 Marken × 3 Slots = 27 Posts/Tag je Plattform, 81 Uploads/Tag, 54 gerenderte Videos/Tag (DE + EN). TikTok-Cap 15/Konto bleibt unterschritten; YouTube 100/Tag/Projekt entfällt über Upload-Post. Der Betrieb wächst in Stufen (siehe `Ablaufplan.md`), weil die Plattformen massenproduzierte Template-Inhalte von der Monetarisierung ausschließen.

## Marken und Nischen (Arbeitsnamen von ChatGPT, Verfügbarkeit ungeprüft)

Namen am 30.10.2026 von Stefan festgelegt nach der Namensrecherche (`02 Marke\Namensrecherche 2026-10-29.md`); die ChatGPT-Vorschläge PromptPilot, VelvetGlow und TorqueLab waren durch eingetragene Marken ausgeschlossen. Marken-IDs im Code sind namensunabhängig. Markenregister mit Handles: `02 Marke\Marken.md`.

| Nr. | Marke | ID | Nische | Start | Begründung |
|---|---|---|---|---|---|
| 1 | Promptwerk | `claude_workflows` | Claude-Workflows und Prompts | Phase 2 | Stefans Fachwissen, gute Quellen, niedriges Risiko, eigene Produkte möglich |
| 2 | Scutoria | `ai_security` | KI und Sicherheit für kleine Betriebe | Phase 2 | Stefans bestehendes Business, Impressum und Adresse vorhanden, B2B-Werbepartner |
| 3 | Revlore | `engines` | Motorentechnik | Phase 4 | Vorbild Kollege, technische Animation, Werbepartner; Handles nur als Variante frei |
| 4 | Gigastruct | `megaconstruction` | Megakonstruktionen | Phase 4 | Vorbild Kollege, stark visuell |
| 5 | Suitwerk | `menswear` | Anzüge und Herrenstil | Phase 4 | Affiliate, visuell standardisierbar; Reserve Lapelore |
| 6 | Gritwerk | `motivation` | Motivation | Phase 5 | gesättigt, braucht eigene Methode |
| 7 | Frontlore | `military_history` | Militärtechnik und Geschichte | Phase 5 | hohes Prüf- und Werberisiko, Art. 50, § 46 BDG; Reserve Armorlore |
| 8 | Dewlane | `beauty` | Beauty | Phase 5 | Wirkversprechen, ohne Produkte angreifbar |
| 9 | Tintora (bis 02.11.2026 Zonkfruit) | `brainrot` | informative Kinder-Anime-Serie „Juna und die Insel der verlorenen Farben“ | Phase 5 | Rebranding 02.11.2026 (`Neuausrichtung 2026-11-02.md` Abschnitt 9); KI-Bild- und Videoerzeugung mit Budget; YouTube „speziell für Kinder“ ohne personalisierte Werbung |

## Zielgruppe

Je Marke eine eigene; wird in `02 Marke` und je Kanalprofil festgelegt. Gemeinsam: Zuschauer von Kurzvideo-Feeds, die in 60–90 Sekunden eine Sache verstehen wollen; Englisch international, Deutsch DACH.

## Nutzen und Alleinstellung

Fachwissen in Sicherheit und KI (statt generischer Fakten), konsistente Markenoptik je Kanal (Designsystem, Style-Lock), jede Aussage mit Quelle, keine Masse ohne redaktionellen Blickwinkel. Genau das ist nach YouTube („original, authentic insights") und TikTok („specialized content that demonstrates your expertise") das Kriterium für Monetarisierung.

## System (Zielbild)

```
Themenkalender (30 Tage, Quellen, Risiko)
  → Claude Code: Recherche, Skript DE/EN, Faktenprüfung, Szenenplan, Bildprompts
  → TTS (Gemini Flash TTS, Alternative ElevenLabs)      [Cloud, Cent-Beträge]
  → Bilder/Clips (KI-Bilder; KI-Clips erst ab Phase 3)   [Cloud]
  → faster-whisper (Wortzeiten, CUDA)                    [lokal, RTX 5080]
  → HyperFrames (HTML/Three.js → MP4) + FFmpeg NVENC     [lokal]
  → Qualitäts- und Compliance-Prüfung (Länge, Audio, Untertitel, Quellen, Lizenzen, KI-Label)
  → Warteschlange entwurf → freigegeben → geplant → gepostet
  → Handy-Zentrale (Claude-Artefakt mit Datenbank): Themenwahl, Vorschau, Freigabe
  → Upload-Post (REST + MCP): TikTok, Instagram, YouTube, KI-Label je Plattform, Zeitplanung serverseitig
  → Statistik (Upload-Post Analytics) → Themenvorschläge für morgen
```

Feste Entscheidungen:
- **Rechner:** Windows-11-Laptop Recoil III 16 (Core Ultra 9 275HX, RTX 5080 16 GB, 32 GB RAM). Alles Nötige ist installiert: Git, Node 24, Python 3.13, FFmpeg mit NVENC, Claude Code 2.1, VS Code. Mac mini ist Reserve.
- **Steuerung:** Windows-Aufgabenplanung startet die deterministischen Schritte (Render, Upload, Statistik) ohne Claude-Tokens; Claude Code nur für Recherche, Skript, Prüfung und Vorschläge. Claude Desktop Scheduled Tasks als zweite Option für die Claude-Schritte.
- **Publisher:** Upload-Post, weil es der einzige geprüfte Weg zu öffentlichen TikTok-API-Posts ist (eine eigene App wird laut TikTok für interne Upload-Werkzeuge nicht auditiert), weil es die KI-Labels aller drei Plattformen per Parameter setzt, serverseitig plant (Laptop darf dann aus sein) und einen MCP-Server für Claude Code hat. Schnittstelle austauschbar halten.
- **Musik:** nur lizenziert, mit Nachweis. Kein automatischer Chartsong (Abweichung vom Bauplan des Kollegen).
- **Kennzeichnung:** jedes Video als KI-Inhalt gekennzeichnet (Stefans Vorgabe); bei realistischen Szenen realer Ereignisse zusätzlich Offenlegung am Videoanfang (AI Act Art. 50).
- **Freigabe (Stefan, 29.10.2026): automatisch.** Ein Video geht hinaus, wenn technische Prüfung, Quellen- und Lizenzmanifest, KI-Label und Richtlinienprüfung bestanden sind; Themen mit Risiko „hoch" (Gesundheit, Produktversprechen, Militär, Aktuelles mit Personen) warten auf Stefan. Claudes Empfehlung: die ersten 20 Videos je Marke von Hand freigeben, um Prüfregeln und Stil zu kalibrieren. Stefan kann jedes geplante Video bis zur Slot-Zeit in der Handy-Zentrale stoppen.
- **Ablage:** Code und Produktion in `C:\Automation\faceless-network` (außerhalb OneDrive); fertige Videos, Skripte, Berichte gespiegelt nach `OneDrive\Business\05 Produktion`. Schlüssel nur in `.env` bzw. Windows-Anmeldeinformationsverwaltung, nie in OneDrive oder Git. C: ohne externen Datenträger; Warnung unter 30 GB frei.
- **Claude-Konto:** Stefans bestehendes Max-Konto; später eventuell Mac mini M1 als Zweitgerät. Verbrauch wird gemessen; API-Key als Ausweichweg bei Limitdruck.
- **Konten:** Google Workspace als Zentrale („1+8“, Stefan, 02.11.2026): `admin@scutoria.com` bündelt alle neun Marken, Scutoria als Hauptmarke. Je Marke ein kostenloser Alias (`<marke>@scutoria.com`, Liste in `02 Marke\Marken.md`) für TikTok (Personal Account) und Instagram (Creator); YouTube-Kanäle als Markenkonten (Brand Accounts) unter admin@. Impressum mit Name und Scutoria-Anschrift. Gewerbe (Werbeagentur) und Steuerberatung: offen, vor dem ersten bezahlten Werbepartner zwingend.
- **Stimme:** Gemini Flash TTS (Paid Tier). **Clips:** Phase 1–2 Animation und KI-Bilder, KI-Clips ab Phase 3 für die ersten 5 Sekunden. **Budget:** 50 €/Monat für Dienste; wird je Phase neu vorgelegt (Professional-Plan von Upload-Post ab 6 Marken liegt bei ca. 46 €).
- **Nischenregeln (Stefan, 29.10.2026):** Militär nur historisch, keine Taktik, nichts Dienstliches, keine Uniform. Beauty ohne eigene Produkte, Ziel Werbepartner für Beauty-Produkte, keine Wirkversprechen. Brainrot mit eigener Figur (Charakter-Sheet, Style-Lock). Claude-Workflows mit echten Bildschirmaufnahmen aus einem Demo-Projekt. Kommentare beantwortet Claude ab Phase 3 nach eigenen Regeln.

## Einnahmen (von Österreich aus, Stand Faktencheck)

| Weg | Status | Voraussetzung |
|---|---|---|
| Kooperationen und Sponsoring je Nische | Hauptziel (Stefans Idee der getrennten Kanäle) | Gewerbe Werbeagentur, Kennzeichnung, Impressum |
| Affiliate (KI-Tools, Herrenmode, Technik) | ab Phase 3 | Handelsgewerbe laut WKO, Kennzeichnung |
| Eigene digitale Produkte (Prompt-Pakete, Vorlagen; Verknüpfung mit Scutoria prüfen) | ab Phase 3 | Shop, Steuer |
| Instagram-Geschenke | in Österreich verfügbar | professionelles Konto, 500 Follower |
| YouTube-Partnerprogramm | fern | 1.000 Abonnenten + 10 Mio. Shorts-Views/90 Tage; ab 01.02.2027 für Neue 20 Mio. und keine Shorts-Erlöse unter 10 Mio. Views |
| TikTok Creator Rewards | nicht verfügbar | Länderfreigabe für Österreich; System so gebaut, dass es sofort passt (über 1 Minute, Personal Account, Original) |

Stärkstes Gegenargument gegen das ganze Vorhaben: Die beiden großen Plattformvergütungen sind für einen neuen Kanal aus Österreich entweder gesperrt (TikTok) oder sehr weit weg (YouTube ab 2027 noch weiter). Einnahmen entstehen nur, wenn die Kanäle für Werbepartner interessant werden, und das verlangt Qualität und Nische statt Menge. Antwort darauf: genau deshalb zwei Fachkanäle zuerst, Menge erst nach Nachweis.

## Ressourcen

- Zeit Stefan: ca. 15 Minuten täglich (Themenwahl, Freigaben), plus wöchentlich eine Stunde Auswertung (Annahme, Frage 5).
- Fixkosten Phase 2: Upload-Post Basic 24 USD monatlich, TTS unter 5 USD, Claude Max bestehend. Phase 4: Upload-Post Professional 50 USD (25 Profile) bzw. Advanced 147 USD bei 42 Profilen; KI-Clips 0,40–1,10 USD je Clip.
- Speicher: C: hat 61 GB frei; vor Phase 2 klären (Frage 14).
- Laptop muss zu den Produktionszeiten wach und am Netz sein; Veröffentlichung läuft serverseitig bei Upload-Post.

## Risiken (je mit stärkstem Gegenargument)

1. **Inauthentic content:** Template-Massenware wird nicht monetarisiert oder gedrosselt. Gegenargument: Erklärkanäle mit Quellen und Perspektive sind ausdrücklich die Ausnahme; Qualität vor Menge löst das.
2. **Kontosperren durch Automatisierung:** Mehrere Konten, API-Posting, gleiche Muster. Gegenargument: autorisierte APIs über auditierten Dienst, Limits weit unterschritten (3 statt 15), keine Kontoautomatisierung, Konten gestaffelt anlegen.
3. **Rechtliches in Österreich:** Gewerbe, Impressum, Werbekennzeichnung, AI Act, § 46 BDG beim Militärkanal. Gegenargument: alles bekannt und mit WKO-Mustern lösbar; Militärkanal zuletzt.
4. **Claude-Nutzungslimits:** Produktion und Stefans eigene Arbeit teilen sich das Max-Kontingent. Gegenargument: bei 2 Videos/Tag unkritisch; ab Phase 4 API-Key mit Kostenlimit.
5. **Zeit im Einsatz:** Netz und Laptop nicht immer verfügbar. Gegenargument: 7-Tage-Puffer freigegebener Videos, Upload-Post plant serverseitig.

## Offene Fragen

Alle 25 Fragen sind beantwortet (`Fragenkatalog.md`), Namen festgelegt (30.10.2026). Offen bleiben: Bestätigung der Slot-Annahme (3 Posts je Konto und Tag, Sprachen wechseln) · Handle-Varianten und Domains .at/.io sichern (Stefan) · Gewerbe und Steuerberatung (Phase 0) · Scutoria als Videomarke mit der Scutoria-`CLAUDE.md` abstimmen.
