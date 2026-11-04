# Prüfung des Masterplans durch Perplexity

Quelle: von Stefan am 29.10.2026 eingefügt. Perplexity hat den ChatGPT-Masterplan (siehe `2026-10-29 Masterplan (ChatGPT).md`) gegengeprüft. Wortlaut unverändert; Claude hat die Aussagen am 29.10.2026 eigenständig geprüft, siehe `Faktencheck 2026-10-29.md`.

---

Ich habe den Plan geprüft. Die technische Grundarchitektur ist stimmig, aber einige zentrale Zahlen, Plattformannahmen und die Produktionsmenge sind zu optimistisch bzw. müssen korrigiert werden.

## Was korrekt ist

- TikTok Direct Post: Nicht auditierte API-Clients dürfen nur privat posten; öffentliche Videos erfordern ein Audit. Es gilt ein Nutzer-Cap von bis zu 5 aktiven Publishern pro 24 Stunden und ein Posting-Cap von typischerweise etwa 15 Posts pro Nutzerkonto und Tag.
- YouTube Data API: videos.insert hat ein eigenes Standardkontingent von 100 Uploads pro Tag und Projekt; jeder Aufruf kostet 1 Einheit. Mehr Kontingent erfordert eine Compliance-Audit-Anfrage.
- Upload-Post: Die im Plan genannten Jahrespreise sind korrekt: Basic 16 USD/Monat bei Jahreszahlung mit 5 Profilen, Professional 33 USD/Monat mit 25 Profilen, Advanced 118 USD/Monat mit 75 Profilen. Monatliche Abrechnung kostet 24 bzw. 50 bzw. 147 USD.
- Ayrshare: Premium beginnt bei 149 USD/Monat, Launch bei 299 USD/Monat. Der Launch-Plan umfasst bis zu 10 Social Profiles.

## Wichtige Korrekturen

| Punkt im Plan | Prüfergebnis | Konsequenz |
|---|---|---|
| „TikTok: typischerweise ca. 15 Posts/Nutzer/Tag" | Korrekt, aber das Limit wird plattformseitig gesetzt und ist nutzerabhängig. | Plane nicht mit garantierten 3 API-Uploads/Tag/Konto; halte Puffer und Fallback bereit. |
| „YouTube: 100 Uploads/Tag" | Korrekt als Projekt-Default. | Bei 7 Kanälen × 2 Sprachen = 14 YouTube-Uploads/Tag technisch unkritisch; entscheidend sind App-Prüfung, OAuth und Kanal-spezifische Limits. |
| „Instagram-Reels-Limit nicht ermittelbar" | Richtig vorsichtig formuliert. | Nicht mit einer festen Zahl planen; über die Meta-/Instagram-API-Limits und Tests je Konto verifizieren. |
| „Upload-Post Professional als erster Testkandidat" | Plausibel: 25 Profile, unbegrenzte Uploads, API und TikTok-Support. | Aber: Upload-Post selbst nennt harte Plattform-Caps, u. a. 15 TikTok- und 30 YouTube-Posts pro verbundenem Konto/24 h. |
| „Ayrshare Premium 149 USD für kleines Netzwerk" | Preis korrekt, aber Premium umfasst nur 1 Social Profile. | Für mehrere Nischenkanäle wäre Launch mit 10 Profilen die realistische Ayrshare-Stufe, nicht Premium. |

## Größtes Risiko: Produktionsmenge

Bei 7 Kanälen, 3 Videos pro Tag und separaten DE-/EN-Fassungen ergeben sich:

- 42 Videos pro Tag
- 126 Uploads pro Tag über TikTok, Instagram und YouTube
- rund 3.780 Uploads pro Monat

Das ist nicht primär ein KI-Kostenproblem, sondern ein Veröffentlichungs- und Qualitätsproblem: TikTok begrenzt API-Posts pro Konto typischerweise auf etwa 15/Tag, und nicht auditierte Clients dürfen zunächst gar nicht öffentlich posten. Zudem erhöhen 42 täglich neue Videos das Risiko von Oberflächeninhalt, Duplikaten, Faktenfehlern und Richtlinienverstößen erheblich.

Empfehlung: Starte mit 2 Kanälen, 1 Video pro Tag und zunächst einer Sprache. Skaliere erst nach 4–6 Wochen, wenn Retention, Watchtime, Follows, Fehlerquote und Monetarisierungssignale messbar sind.

## Nischenrisiken

- KI & Sicherheit, Claude-Workflows: Gute Eignung für automatisierte Erklärvideos; Hauptproblem ist Aktualität und Faktenprüfung.
- Beauty: Hohes Werbepotenzial, aber hohe Haftungspflicht bei Wirkversprechen, Produktempfehlungen und Affiliate-Kennzeichnung.
- Brainrot: Technisch einfach, aber wahrscheinlich die schwächste Werbe- und Monetarisierungsnische; zudem hohes Risiko generischer, austauschbarer Inhalte.
- Motivation/Selbsthilfe: Leicht produzierbar, aber extrem gesättigt; ohne eigenständige Daten, Geschichten oder Methoden schwer differenzierbar.
- Militär/Sicherheit: Auch bei „nur öffentlich zugänglichen Inhalten" besonders sensibel. Keine Taktiken, Waffennutzung, Anleitungen oder militärische Einsatzsimulationen; auf historische Technik, Dokumentation und Analyse beschränken.
- Mode/Anzüge: Gut für Affiliate und Produktinhalte, aber visuelle Qualität und Konsistenz sind entscheidend.

## Monetarisierung aus Österreich

Der Plan macht richtig, dass TikTok Creator Rewards in Österreich nicht als verfügbar angenommen wird. Verlass dich daher zunächst nicht auf Creator-Fonds:

- YouTube Partner Program, sofern Kanäle die jeweiligen Zulassungsvoraussetzungen erfüllen
- Affiliate-Links, insbesondere Beauty, Technik, Mode und KI-Tools
- Direktwerbung/Sponsoring pro Nische
- Eigene digitale Produkte, etwa Prompt-Bibliotheken, Notion-/Workflow-Vorlagen oder Newsletter
- Lizenzierung eigener Formate an Marken

Wichtig: Affiliate- und Werbeinhalte müssen in jedem Video und in der Beschreibung klar gekennzeichnet sein; KI-Inhalte zusätzlich nach den Regeln der jeweiligen Plattform.

## Konkrete Planänderungen

1. Nicht 7 Kanäle gleichzeitig. Starte mit 2: am ehesten „Claude-Workflows/Prompts" und „KI & Sicherheit".
2. Erst DE, dann EN. Zweisprachigkeit verdoppelt Produktion, ohne zunächst zu beweisen, dass eine Sprache funktioniert.
3. Kein Blind-Upload. Behalte die menschliche Freigabe mindestens für die ersten 100 Videos und für alle sensiblen Themen.
4. TikTok erst nach Audit planen. Ohne Audit sind API-Posts privat; für den Start ist manuelles Hochladen oder ein geprüfter Drittanbieter-Workflow realistischer.
5. Publisher austauschbar halten. Teste Upload-Post wegen Preis/Profilen, aber baue die Schnittstelle so, dass Ayrshare oder direkte APIs später ersetzbar sind.
6. Musik, Bilder, Stimmen dokumentieren. Kein „Chart-Song automatisch hinzufügen"; jede Audio-, Bild- und Videoquelle braucht Lizenznachweis.
7. Qualität vor Volumen. 1 starkes Video pro Kanal/Tag ist nachhaltiger als 3 generische Videos; die Plattformen belohnen Watchtime und Wiedererkennung, nicht bloße Uploadfrequenz.

Fazit: Der Plan ist technisch gut durchdacht und die wichtigsten API-Zahlen sind weitgehend richtig. Die entscheidende Schwäche ist die angenommene Skalierung: 7 Kanäle × 3 Videos × 2 Sprachen × 3 Plattformen ist zum Start zu aggressiv und kollidiert mit TikTok-Limits, Qualitätssicherung und realistischer Monetarisierung.
