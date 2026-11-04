---
topic_id: ai_security-20261105-1
brand_id: ai_security
language: de
title: Was ein KI-Chat über deinen Betrieb speichert
description: Ob deine Eingaben zum Training verwendet werden, hängt von einer Einstellung und vom Vertrag ab. Eine Regel für den Betrieb.
hashtags: [kisicherheit, kleinunternehmen, datenschutz, chatgpt, claude]
risk_level: medium
sources:
  - id: S1
    url: https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
    title: Is my data used for model training? (Anthropic Privacy Center)
    checked_at: 2026-10-30
  - id: S2
    url: https://privacy.claude.com/en/articles/7996875-can-you-delete-data-that-i-sent-via-api
    title: Can you delete data that I sent via API? (Anthropic Privacy Center)
    checked_at: 2026-10-30
  - id: S3
    url: https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html
    title: Generative KI-Modelle - Chancen und Risiken für Industrie und Behörden (BSI, 21.01.2025)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Dein Mitarbeiter tippt die Kundenliste in einen KI-Chat. Wo landet sie?
> visual: headline="Wo landet die Kundenliste?" kind="hook"

## Scene 2 (card)
Bei Anthropic gilt für private Konten: Chats werden zum Verbessern der Modelle genutzt, wenn du das in den Privatsphäre-Einstellungen erlaubst, wenn ein Chat zur Sicherheitsprüfung markiert wird, oder wenn du ausdrücklich zustimmst. [S1]
> visual: headline="Private Konten: eine Einstellung entscheidet" body="Training nur bei Erlaubnis, Sicherheitsprüfung oder ausdrücklicher Zustimmung" kind="card"

## Scene 3 (fact)
Anders über die Schnittstelle für Firmen: Daten aus der API werden laut Anthropic nicht zum Training genutzt, außer ein Vertrag sagt etwas anderes. Löschen auf Zuruf gibt es für zahlende API-Kunden aber nicht. [S2]
> visual: headline="Firmenzugang: kein Training, kein Löschen auf Zuruf" number="API" body="Vertrag und Datenhaltung vorher lesen" kind="fact"

## Scene 4 (card)
Das deutsche BSI hat im Januar 2025 eine Publikation zu generativen KI-Modellen veröffentlicht, die Risiken für Industrie und Behörden aufzeigt und Gegenmaßnahmen benennt. Eine Lektüre für jeden, der KI im Betrieb einführt. [S3]
> visual: headline="BSI: Risiken und Gegenmaßnahmen" body="Generative KI-Modelle, Publikation vom 21.01.2025" kind="card"

## Scene 5 (advice)
Die Regel für kleine Betriebe: Keine Kundendaten, keine Verträge, keine Passwörter in Chats mit privaten Konten. Für Firmendaten ein Firmenzugang mit Vertrag, und die Trainingseinstellung bei jedem Konto prüfen.
> visual: headline="Eine Regel, drei Punkte" body="Keine Kundendaten in Privatkonten · Firmenzugang mit Vertrag · Einstellung prüfen" kind="advice"

## Scene 6 (payoff)
Heute noch: Öffne die Privatsphäre-Einstellungen deines KI-Kontos und schau, was dort angehakt ist. Mehr Schutz für kleine Betriebe: folgen. [S1]
> visual: headline="Heute: Einstellungen prüfen" kind="payoff"
