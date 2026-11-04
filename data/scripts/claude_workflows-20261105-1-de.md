---
topic_id: claude_workflows-20261105-1
brand_id: claude_workflows
language: de
title: CLAUDE.md – die Datei, die Claude Code zuerst liest
description: Warum jedes Projekt eine CLAUDE.md braucht, was hinein gehört und wie /init sie anlegt. Geprüft mit Claude Code 2.1.
hashtags: [claudecode, claude, promptengineering, kiworkflow, developer]
risk_level: low
sources:
  - id: S1
    url: https://code.claude.com/docs/en/memory
    title: How Claude remembers your project (Claude Code docs)
    checked_at: 2026-10-30
  - id: S2
    url: https://code.claude.com/docs/en/overview
    title: Claude Code overview (Claude Code docs)
    checked_at: 2026-10-30
---
## Scene 1 (hook)
Claude Code vergisst nach jeder Sitzung alles. Außer einer Datei. [S1]
> visual: headline="Eine Datei, die Claude nie vergisst" kind="hook"

## Scene 2 (card)
Jede Sitzung startet mit einem leeren Kontextfenster. Die CLAUDE.md im Projektordner wird beim Start automatisch geladen, in jeder Sitzung. Sie ist Kontext, keine harte Regel. Wer etwas wirklich verbieten will, nutzt einen Hook. [S1]
> visual: headline="CLAUDE.md wird bei jedem Start geladen" body="Projektordner oder .claude/CLAUDE.md, dazu ~/.claude/CLAUDE.md für dich persönlich" kind="card"

## Scene 3 (code)
Du musst sie nicht selbst schreiben. Der Befehl /init analysiert dein Projekt und erzeugt eine erste CLAUDE.md mit Build-Befehlen, Testanweisungen und Konventionen. Gibt es schon eine, schlägt er nur Verbesserungen vor. [S1]
> visual: headline="/init schreibt den ersten Entwurf" code="$ claude|> /init|CLAUDE.md angelegt: Build, Tests, Konventionen|> /context  → Memory files" kind="code"

## Scene 4 (fact)
Was hinein gehört: Build- und Testbefehle, Codestandards, Architekturentscheidungen, wiederkehrende Abläufe. Und kurz bleiben: Die Dokumentation empfiehlt unter zweihundert Zeilen, weil längere Dateien Kontext kosten und schlechter befolgt werden. [S1]
> visual: headline="Unter 200 Zeilen bleiben" number="200" body="Build, Tests, Standards, Entscheidungen, Abläufe" kind="fact"

## Scene 5 (card)
Lange Dateien teilst du auf. Mit einem At-Zeichen importierst du weitere Dateien, zum Beispiel die README oder eine Git-Anleitung. Persönliches kommt in CLAUDE.local.md und in die Gitignore. [S1]
> visual: headline="Aufteilen statt aufblähen" body="@README importiert, CLAUDE.local.md bleibt privat" kind="card"

## Scene 6 (payoff)
Der Effekt: Claude kennt beim ersten Befehl schon deine Regeln. Das ist die Grundlage jedes Workflows, den wir hier zeigen, geprüft mit Claude Code Version zwei Punkt eins. Folgen für den nächsten Workflow. [S2]
> visual: headline="Regeln vor dem ersten Befehl" kind="payoff"
