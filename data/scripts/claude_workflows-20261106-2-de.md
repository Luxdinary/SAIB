---
topic_id: claude_workflows-20261106-2
brand_id: claude_workflows
language: de
title: Hooks – Regeln, die Claude Code nicht umgehen kann
description: CLAUDE.md ist Kontext, Hooks sind Zwang. Wie ein PreToolUse-Hook Änderungen an der .env blockiert.
hashtags: [claudecode, hooks, automation, kiworkflow, developer]
risk_level: low
sources:
  - id: S1
    url: https://code.claude.com/docs/en/hooks-guide
    title: Automate actions with hooks (Claude Code docs)
    checked_at: 2026-10-30
  - id: S2
    url: https://code.claude.com/docs/en/memory
    title: How Claude remembers your project (Claude Code docs)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Deine CLAUDE.md sagt: Fass die .env nie an. Claude kann das trotzdem tun. [S2]
> visual: headline="Eine Regel, die Claude ignorieren kann" kind="hook"

## Scene 2 (card)
Die Dokumentation sagt es selbst: CLAUDE.md ist Kontext, keine erzwungene Konfiguration. Wer eine Aktion wirklich verbieten will, braucht einen PreToolUse-Hook. [S2]
> visual: headline="Kontext oder Zwang?" body="CLAUDE.md wird gelesen, ein Hook wird ausgeführt" kind="card"

## Scene 3 (card)
Hooks sind eigene Shell-Befehle, die Claude Code an festen Punkten im Ablauf ausführt. Das gibt deterministische Kontrolle: Bestimmte Dinge passieren immer, statt dass das Modell entscheidet, ob es sie tut. [S1]
> visual: headline="Hooks laufen immer" body="Shell-Befehle an festen Punkten: vor Werkzeugen, nach Änderungen, am Ende" kind="card"

## Scene 4 (code)
Die Ereignisse heißen zum Beispiel PreToolUse vor einem Werkzeugaufruf, PostToolUse danach, SessionStart beim Start und Stop, wenn Claude fertig ist. Nur PreToolUse kann eine Aktion blockieren. [S1]
> visual: headline="Vier Ereignisse, die du brauchst" code="PreToolUse   → kann blockieren|PostToolUse  → Formatter, Log|SessionStart → Kontext laden|Stop         → Abschlussprüfung" kind="code"

## Scene 5 (fact)
Die Konfiguration steht in settings.json, global unter .claude im Benutzerordner oder im Projekt. Ein Hook, der mit Exit-Code zwei endet, blockiert die Aktion, und Claude bekommt die Begründung als Rückmeldung. Genau so sperrt das Beispiel der Dokumentation Änderungen an der .env-Datei. [S1]
> visual: headline="Exit-Code 2 blockiert" number="2" body="settings.json im Projekt oder im Benutzerordner" kind="fact"

## Scene 6 (payoff)
Merksatz: Was in die CLAUDE.md kommt, ist eine Bitte. Was in einen Hook kommt, ist ein Gesetz. Geprüft mit Claude Code zwei Punkt eins. Folgen für den nächsten Workflow.
> visual: headline="Bitte oder Gesetz" kind="payoff"
