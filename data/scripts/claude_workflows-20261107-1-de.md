---
topic_id: claude_workflows-20261107-1
brand_id: claude_workflows
language: de
title: Deny-Regeln – so sperrst du Claude Code von der .env aus
description: "Permissions in Claude Code: deny schlägt allow, Read(./.env) sperrt Geheimnisse, Regeln liegen in settings.json."
hashtags: [claudecode, permissions, security, kiworkflow, developer]
risk_level: low
sources:
  - id: S1
    url: https://code.claude.com/docs/en/permissions
    title: Configure permissions (Claude Code docs)
    checked_at: 2026-10-30
  - id: S2
    url: https://code.claude.com/docs/en/cli-reference
    title: CLI reference (Claude Code docs)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Eine Zeile in den Einstellungen, und Claude sieht deine Schlüssel nie wieder. [S1]
> visual: headline="Eine Zeile sperrt die Schlüssel" kind="hook"

## Scene 2 (card)
Claude Code hat ein Berechtigungssystem mit drei Listen: allow, ask und deny. Die Regeln werden in genau dieser Reihenfolge geprüft: zuerst deny, dann ask, dann allow. Der erste Treffer entscheidet. [S1]
> visual: headline="deny, dann ask, dann allow" body="Der erste Treffer entscheidet, Spezifität ändert die Reihenfolge nicht" kind="card"

## Scene 3 (card)
Das heißt: Eine breite deny-Regel schlägt jede engere allow-Regel. Eine Ausnahme aus einer Sperre herauszuschneiden geht nicht. Genau so soll es sein. [S1]
> visual: headline="deny schlägt allow" body="Eine Sperre kennt keine Ausnahmen" kind="card"

## Scene 4 (code)
Für Geheimnisse gibt es eine Read-Regel mit Pfad. Read mit Punkt Schrägstrich Punkt env sperrt die Datei im Projekt. Dieselbe Regel blockiert auch Edit und Write auf diesen Pfad, und sie gilt für cat, head und tail in der Shell. [S1]
> visual: headline="Read(./.env) sperrt die Datei" code="{ \"permissions\": {|    \"deny\": [|      \"Read(./.env)\",|      \"Read(./secrets/**)\"|    ] } }" kind="code"

## Scene 5 (fact)
Die Regeln liegen in settings.json: im Projekt unter .claude, lokal in settings.local.json oder global im Benutzerordner. Auf Windows werden Pfade vorher in die POSIX-Form gebracht. Und: Eine .claudeignore-Datei hat keine Wirkung, ihre Einträge gehören in deny-Regeln. [S1]
> visual: headline="settings.json, drei Ebenen" number="3" body="Projekt · lokal · Benutzer; .claudeignore wirkt nicht" kind="fact"

## Scene 6 (payoff)
Für Skripte und CI gibt es das Gegenstück: Mit dem Flag allowedTools gibst du beim Aufruf mit claude -p nur die Werkzeuge frei, die der Lauf braucht. Geprüft mit Claude Code zwei Punkt eins. Folgen für den nächsten Workflow. [S2]
> visual: headline="Sperren im Projekt, freigeben pro Lauf" kind="payoff"
