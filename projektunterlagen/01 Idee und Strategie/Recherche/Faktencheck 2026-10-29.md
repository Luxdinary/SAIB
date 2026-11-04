# Faktencheck der drei Berichte (ChatGPT, Grok, Perplexity)

Stand: 29.10.2026, 23:30 (Wien). Alle Quellen am 29.10.2026 abgerufen, nur offizielle Primärquellen (Entwicklerdokumentation, Hilfeseiten, EU-Kommission, WKO, USP, Anbieter-Preisseiten). Geprüft von drei getrennten Prüfläufen (Plattform-APIs · Recht und Monetarisierung · Werkzeuge und Preise). Legende: bestätigt · teilweise · widerlegt · nicht ermittelbar.

## 1. Was die Berichte richtig haben

| Aussage | Ergebnis | Quelle |
|---|---|---|
| TikTok Creator Rewards: Österreich nicht dabei; Länder USA, UK, Deutschland, Japan, Südkorea, Frankreich, Mexiko, Brasilien | bestätigt (Creator Academy, zuletzt aktualisiert 18.08.2026) | tiktok.com/creator-academy/en/article/eligibility |
| Rewards-Voraussetzungen: 18+, 10.000 Follower, 100.000 Views in 30 Tagen, nur Personal Account, Videos über 1 Minute, kein Photo Mode | bestätigt | ebd.; …/monetization-creativity-program-video-eligible |
| TikTok API: nicht auditierte Clients nur SELF_ONLY, höchstens 5 Nutzer je 24 h, typisch ca. 15 Posts je Konto und Tag (kontoweit über alle Clients) | bestätigt | developers.tiktok.com/doc/content-sharing-guidelines; …/content-posting-api-reference-direct-post |
| TikTok: „A utility tool to help upload contents to the account(s) you or your team manages" ist als Anwendungsfall nicht akzeptabel | bestätigt. Folge: eine eigene Direct-Post-App für das eigene Netzwerk bekommt kein Audit und bleibt privat. Öffentliches API-Posten auf TikTok geht nur über einen auditierten Drittdienst oder von Hand. | content-sharing-guidelines, „Intended use" |
| YouTube Data API: videos.insert 100 Aufrufe/Tag/Projekt, je 1 Einheit | bestätigt; Datierung präzisiert: 04.12.2025 Kostenkorrektur 1.600 → ca. 100 Einheiten, ab 01.06.2026 eigener Topf mit 100 Aufrufen/Tag. Grok (1.600 Einheiten → 6 Uploads/Tag) ist überholt. Erhöhung nur nach Compliance-Audit. | developers.google.com/youtube/v3/determine_quota_cost (Stand 15.10.2026); …/revision_history |
| YouTube-Partnerprogramm in Österreich verfügbar; 1.000 Abonnenten + 4.000 Stunden/12 Monate oder 10 Mio. Shorts-Views/90 Tage | bestätigt; Fan-Funding-Stufe ab 500 Abonnenten + 3.000 Stunden oder 3 Mio. Shorts-Views | support.google.com/youtube/answer/7101720; …/72851; …/13429240 |
| YouTube „inauthentic content" (15.07.2025): massenproduzierte, templatebasierte, KI-generische Inhalte nicht monetarisierbar | bestätigt, Wortlaut: „AI-generated content made with generic or unoriginal templates", „image slideshows … with minimal narrative" | support.google.com/youtube/answer/1311392 |
| Upload-Post Preise: Free 0 (2 Profile), Basic 24 monatlich / 16 jährlich (5 Profile), Professional 50 / 33 (25 Profile), Advanced 147 / 118 (75 Profile), Business 438 / 350 (225); TikTok nicht im Free-Plan; Zusatzprofile als Add-on (Basic +5 für 15 $, +10 für 25 $; Professional +15 für 35 $, +25 für 55 $) | bestätigt (USD) | upload-post.com/llms-full.txt |
| Upload-Post Tagesgrenzen je verbundenem Konto: TikTok 15, Instagram 50, YouTube 30 | bestätigt, aber nicht in einer FAQ, sondern im Guide „Rate limits" | docs.upload-post.com/guides/rate-limits |
| Upload-Post API: POST /api/upload, scheduled_date (bis 365 Tage voraus), Status je request_id/job_id, Analytics je Profil und je Post, offizieller MCP-Server für Claude Code | bestätigt; KI-Labels per Parameter: TikTok is_aigc, Instagram is_ai_generated, YouTube containsSyntheticMedia; kommerziell: brand_content_toggle, brand_organic_toggle, hasPaidProductPlacement | docs.upload-post.com/api/upload-video; …/guides/mcp-server-integration; github.com/Upload-Post/upload-post-mcp (MIT) |
| Ayrshare Premium 149 $/Monat (1 Profil), Launch 299 $/Monat (10 Profile) | bestätigt | ayrshare.com/pricing |
| ElevenLabs Starter 6 $, Creator 22 $ (121 Minuten), Pro 99 $; kommerzielle Lizenz ab Starter | bestätigt | elevenlabs.io/pricing |
| HyperFrames rendert HTML/Three.js zu MP4 | bestätigt: Open Source von HeyGen, Apache-2.0, Version 0.8.217 (29.10.2026), Node ≥ 22 und FFmpeg, läuft unter Windows | github.com/heygen-com/hyperframes |
| faster-whisper mit CUDA auf Windows | bestätigt (CUDA 12, cuDNN 9; offizieller Benchmark: 13 Minuten Audio in 17–63 s auf RTX 3070 Ti) | github.com/SYSTRAN/faster-whisper |
| WKO: Werbung, Kooperationen, Affiliate → Gewerbe (Werbeagentur bzw. Ankündigungsunternehmen; Affiliate mit Provision → Handelsgewerbe), SVS-Pflicht | bestätigt (WKO 20.03.2026 und 12.03.2026) | wko.at/gruendung/online-content-creatorin |

## 2. Was in den Berichten falsch, veraltet oder zu optimistisch ist

| Aussage | Befund | Konsequenz |
|---|---|---|
| Grok: YouTube videos.insert kostet 1.600 Einheiten, rechnerisch 6 Uploads/Tag | überholt seit 04.12.2025 / 01.06.2026; es sind 100 Uploads/Tag/Projekt | 7 Kanäle × 3 Videos × 2 Sprachen = 42 YouTube-Uploads/Tag passen in ein Projekt; die Grenze ist nicht YouTube, sondern TikTok (15/Konto) und Qualität |
| Grok: Instagram 100 API-Posts/24 h; ChatGPT/Perplexity: nicht ermittelbar | Meta-Dokumentation widerspricht sich selbst: Guide sagt 100, der Endpunkt content_publishing_limit liefert quota_total 50; Reels nicht ausdrücklich geregelt | konservativ mit 50/24 h rechnen und das Limit vor jedem Upload abfragen; bei 3 Videos/Tag/Konto irrelevant |
| Bauplan Kollege / Grok: Gemini-TTS gratis ca. 10 Stimmen pro Tag und Modell | nicht ermittelbar; offizielle Rate-Limits-Seite zeigt keine Tabelle mehr, Limits nur hinter Login in AI Studio | Paid Tier einplanen; Kosten sind gering (siehe Abschnitt 4) |
| ChatGPT: Google Veo (Gemini API) als Videogenerator | widerlegt: „The Veo 3.1 Preview in the Gemini API has been shut down." Nachfolger Gemini Omni Flash, ca. 0,10 $/s 720p | KI-Clips über Runway, Kling, Higgsfield oder Gemini Omni; nicht Veo |
| ChatGPT: Ayrshare Premium 149 $ „für ein kleines Netzwerk" | Premium hat nur 1 Profil; für mehrere Kanäle Launch 299 $ | Ayrshare scheidet preislich aus |
| ChatGPT: „Claude Max unbegrenzte Hintergrundverarbeitung nicht vorausgesetzt" (richtig vorsichtig), Bauplan Kollege: eigenes zweites Claude-Konto | Anthropic: Limits gelten für „ordinary, individual usage"; 5-Stunden-Fenster und Wochenlimit, geteilt zwischen Claude und Claude Code; Cloud-Scheduled-Tasks zählen ebenso; Usage Policy verbietet Mehrfachkonten zur Umgehung von Limits | Skripterstellung über Claude Code ist bei 2–7 Videos/Tag gedeckt; bei 42 Videos/Tag ist ein API-Key (Commercial Terms) die saubere Grundlage; ein zweites Max-Konto nur, wenn es ein eigenständiger Nutzer ist, nicht zur Limit-Umgehung |
| Bauplan Kollege: TikTok bekommt automatisch einen Chartsong leise untergelegt | nicht übernehmen: Musikrechte für kommerzielle Nutzung nicht geklärt; Upload-Post-Posts laufen ohne TikToks Commercial-Music-Library | nur lizenzierte Musik mit Nachweis in `08 Recht und Verwaltung\Lizenzen` |
| Alle drei: YouTube-Partnerprogramm als sicherer Hauptweg | teilweise; neu seit 10.08.2026: ab 01.02.2027 für Neuantragsteller 8.000 Stunden/365 Tage oder 20 Mio. Shorts-Views/90 Tage; zusätzlich ab 01.02.2027 keine Shorts-Werbeerlöse mehr für Kanäle unter 10 Mio. qualifizierten Shorts-Views/90 Tage. Wer vorher aufgenommen ist, ist von der Anhebung nicht betroffen. | Werbeerlöse aus Shorts allein sind für neue Kanäle sehr weit weg. Realistische Einnahmen: Kooperationen, Affiliate, eigene Produkte, Instagram-Geschenke (ab 500 Follower, in Österreich verfügbar), TikTok Rewards nur bei Länderfreigabe. Das ist das stärkste Gegenargument gegen das Geldziel. | blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn |
| Alle drei: EU-Recht nicht erwähnt | Lücke: EU AI Act Art. 50 gilt seit 02.08.2026. Deployer müssen Deepfakes offenlegen; monetarisierte Kanäle gelten laut Kommissions-Leitlinien C(2026) 5054 (20.07.2026) als professionell, also als Deployer. Deepfake = KI-Inhalt, der realen Personen, Orten, Ereignissen ähnelt und echt wirkt; keine Deepfakes sind stilisierte, physikalisch unmögliche oder cartoonhafte Darstellungen und KI-Erzählstimmen ohne Identitätstäuschung. Code of Practice (10.06.2026) ist freiwillig. WKO (07.08.2026): „täuschend echt" rechtlich nicht eindeutig definiert. | Offenlegung am Videoanfang bei realistischen KI-Szenen realer Ereignisse (betrifft vor allem den Militär-/Geschichtskanal); Plattform-Label zusätzlich. Leitlinien liegen in `08 Recht und Verwaltung`. |
| ChatGPT: Impressum „nennt Namen und Anschrift" | bestätigt und präzisiert: § 24/25 MedienG, auf Social-Media-Profilen mit höchstens zwei Klicks erreichbar; bloßer Verweis auf die Website reicht nicht; meinungsbildende Kanäle brauchen die „große" Offenlegung (Blattlinie) | Impressum je Profil ab dem ersten Post; Formulierung mit WKO-Muster |

## 3. Was keiner der Berichte hatte und für den Betrieb entscheidend ist

1. **TikTok-Token:** Access Token 24 Stunden, Refresh Token 365 Tage, der Refresh-Token rotiert („You must use the newly-returned token"). Ohne automatische Rotation mit Speicherung bricht ein unbeaufsichtigtes System nach einem Tag ab. 6 Requests/Minute je Token. Über Upload-Post entfällt das (Upload-Post hält die Tokens).
2. **Instagram:** Medien müssen zum Veröffentlichungszeitpunkt auf einem öffentlich erreichbaren Server liegen (kein lokaler Upload); Container verfallen nach 24 h; Meta empfiehlt eigene Drosselung bei geplanten Posts. Über Upload-Post entfällt auch das.
3. **YouTube:** Quota ist projektweit, nicht je Kanal; Videos, die als „locked as private" markiert werden, haben keinen Einspruch. Die API-Referenz sagt aktuell, Uploads aus nicht verifizierten Projekten seien nicht eingeschränkt; die Hilfeseite nennt die Sperre weiterhin. Vor Produktivbetrieb mit Testprojekt verifizieren oder Upload-Post nutzen.
4. **KI-Label-Pflicht je Plattform:** TikTok (Community Guidelines, gültig seit 24.09.2026) verlangt das Label für realistisch wirkende KI-Inhalte; YouTube verlangt Offenlegung bei realistischen Inhalten (Feld containsSyntheticMedia, seit 30.10.2024 über die API); Meta verlangt den AI-Disclosure bei fotorealistischem Video oder realistisch klingendem Audio (Feld is_ai_generated). Unrealistische, offensichtlich animierte Inhalte sind bei allen drei nicht labelpflichtig; Stefan kennzeichnet trotzdem alles (seine Vorgabe).
5. **Militärkanal und Werbung:** YouTube: nicht-grafische Bildungsinhalte über Krieg voll werbefähig; Kriegsaufnahmen mit Verletzung oder Tod „in any context" nicht werbefähig; Waffenbau, -umbau, -zerlegung nicht werbefähig und teilweise verboten. TikTok: Zeigen von Schusswaffen ist FYF-ineligible und altersbeschränkt (also ohne Reichweite); Dokumentation und Bildung erlaubt. Meta: Gebrauchsanleitungen 18+, sensible Inhalte nicht in Anzeigen.
6. **Kontenlimits bei der Anlage:** Instagram höchstens 5 Konten je E-Mail-Adresse; TikTok eine E-Mail und eine Telefonnummer je Konto; YouTube verifiziert eine Telefonnummer mit höchstens 2 Kanälen pro Jahr (aus Grok-PDF, Quellen help.instagram.com, TikTok Support FAQ, support.google.com/youtube/answer/171664). Für 9 Marken × 3 Plattformen braucht es mehrere Telefonnummern oder eine zeitliche Staffelung.
7. **Claude Desktop Scheduled Tasks:** laufen nur bei offener App und wachem Rechner; verpasste Zeit wird beim Aufwachen einmal nachgeholt (bis 7 Tage); „Keep computer awake" in den Einstellungen; zugeklappter Deckel schläft trotzdem. Cloud-Scheduled-Tasks laufen auf Anthropic-Infrastruktur, ziehen aber vom Abo-Kontingent ab. (code.claude.com/docs/en/desktop-scheduled-tasks.md; …/routines.md)
8. **Kleinunternehmergrenze Umsatzsteuer:** 55.000 € brutto (seit 01.01.2025, USP Stand 01.01.2026).
9. **Instagram-Abos:** Österreich laut Instagram-Creators-Blog (20.09.2023) dabei; aktuelle Hilfeseite ohne Länderliste. Bonus-Programme nur auf Zufallseinladung. TikTok Shop in Österreich nicht verfügbar (Seller-Seite listet DE, FR, ES, IE, IT, PL, NL, BE, UK).

## 4. Kosten je fertigem 75-Sekunden-Video (Listenpreise 29.10.2026, ohne USt.)

Annahmen: Rendering (HyperFrames) und Untertitel (faster-whisper) lokal auf der RTX 5080, Strom nicht gerechnet; 75 s Sprache ≈ 190 Wörter.

| Posten | Kosten je Video | Quelle |
|---|---|---|
| TTS Gemini 2.5/3.8 Flash TTS, Paid Tier | ca. 0,02 $ | ai.google.dev/gemini-api/docs/pricing (Output 9–10 $/1 Mio. Audio-Token) |
| TTS ElevenLabs Creator (22 $/Monat, 121 Minuten) | ca. 0,23 $ bei voller Auslastung | elevenlabs.io/pricing |
| Upload-Post Professional, jährlich, auf 210 Videos/Monat umgelegt | ca. 0,16 $ | upload-post.com |
| Ein KI-Clip 8 s (Hook): Runway gen4_turbo 0,40 $ · Higgsfield Plus Kling 3.0 ca. 0,55 € · Kling API 0,74 $ · Gemini Omni Flash 0,80 $ · Runway gen4.5 0,96 $ | 0,40–1,11 $ | docs.dev.runwayml.com/guides/pricing; higgsfield.ai/pricing; kling.ai/dev/pricing |
| Claude Max, umgelegt auf 210 Videos (100–200 $/Monat) | 0,48–0,95 $ (Annahme: Limit reicht) | claude.com/pricing |

Variante A (TTS + programmatische Animation): variabel ca. 0,18 $ je Video, mit Claude-Anteil ca. 0,65–1,15 $. Variante B (zusätzlich ein 8-s-Clip): variabel 0,6–1,3 $, mit Claude-Anteil 1,05–2,25 $. Monatliche Fixkosten Phase 2 (2 Kanäle, 6 Profile): Upload-Post Basic 24 $ monatlich, TTS unter 5 $, zusammen unter 30 $ zuzüglich Claude Max.

## 5. Nicht ermittelbar (mit Grund)

- Gemini-TTS-Limits im Free Tier und Tier 1 (nur hinter Google-Login sichtbar).
- Ob Upload-Posts TikTok-App auditiert ist (nicht öffentlich dokumentiert; indirekt: bezahlte Pläne enthalten TikTok mit 15 Posts/Tag). Test: erster TikTok-Post über Upload-Post auf einem Testkonto muss öffentlich erscheinen.
- Instagram: ob Reels auf das 24-h-Limit zählen; aktuelle Länderliste für Abos; „Content Monetization" in Österreich.
- TikTok: Länderlisten für LIVE-Geschenke und TikTok One.
- Vergütung je 1.000 Views bei TikTok und YouTube (nicht veröffentlicht; Creator-Angaben in den YouTube-Videos sind Marketing).
- Tatsächliche Nachfrage je Nische (keine Marktdaten erhoben; nur qualitative Einschätzung der Berichte).
- Rendergeschwindigkeit von HyperFrames auf der RTX 5080 (kein Testlauf).
