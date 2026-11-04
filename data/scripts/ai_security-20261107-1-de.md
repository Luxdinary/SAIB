---
topic_id: ai_security-20261107-1
brand_id: ai_security
language: de
title: Passkeys – das Login, das man nicht phishen kann
description: Was ein Passkey ist, warum er Phishing widersteht und womit kleine Betriebe anfangen sollten.
hashtags: [passkeys, phishing, kleinunternehmen, itsicherheit, login]
risk_level: medium
sources:
  - id: S1
    url: https://fidoalliance.org/passkeys/
    title: FIDO Passkeys - Passwordless Authentication (FIDO Alliance)
    checked_at: 2026-10-30
  - id: S2
    url: https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services
    title: Multi-factor authentication for your corporate online services (UK National Cyber Security Centre)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Das stärkste Passwort deiner Firma hilft nichts, wenn ein Mitarbeiter es auf der falschen Seite eintippt.
> visual: headline="Das Passwort auf der falschen Seite" kind="hook"

## Scene 2 (card)
Deshalb gibt es Passkeys. Ein Passkey ist laut FIDO Alliance ein Anmeldenachweis auf Basis der FIDO-Standards. Er liegt auf deinem Gerät und wird so entsperrt, wie du das Gerät entsperrst: Fingerabdruck, Gesicht oder PIN. [S1]
> visual: headline="Was ein Passkey ist" body="Ein Nachweis nach FIDO-Standard, gespeichert auf dem Gerät, entsperrt wie das Gerät" kind="card"

## Scene 3 (card)
Der Unterschied zum Passwort: Passkeys sind laut FIDO Alliance immer stark und phishing-resistent, weil es kein geteiltes Geheimnis gibt, das man eintippen oder abgreifen könnte. Eine gefälschte Login-Seite bekommt nichts. [S1]
> visual: headline="Kein geteiltes Geheimnis" body="Nichts zum Eintippen, nichts zum Abgreifen" kind="card"

## Scene 4 (fact)
Das erklärte Ziel: Der Passkey ersetzt das Passwort als ersten Faktor beim Anmelden. Die FIDO Alliance nennt das den Weg zur passwortlosen Anmeldung. [S1]
> visual: headline="Ersatz für das Passwort" number="1" body="Passkey statt Passwort als erster Faktor" kind="fact"

## Scene 5 (card)
Wo noch kein Passkey geht, bleibt die Mehrfaktor-Anmeldung Pflicht. Das britische NCSC hat dazu eine eigene Anleitung für Firmen-Onlinedienste und empfiehlt Verfahren, die besser gegen Phishing schützen. [S2]
> visual: headline="Sonst: Mehrfaktor, phishing-fest" body="NCSC-Leitfaden für Firmen-Onlinedienste" kind="card"

## Scene 6 (payoff)
Heute: Prüfe, ob E-Mail, Bank und Cloud-Speicher deiner Firma Passkeys anbieten, und schalte sie dort zuerst ein. Mehr Schutz für kleine Betriebe: folgen.
> visual: headline="Heute: E-Mail, Bank, Cloud" kind="payoff"
