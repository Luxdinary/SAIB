# Themen- und Kalenderplan Promptwerk (09.11.–06.12.2026)

**Freigegeben von Stefan am 01.11.2026.** Themen im Status `planned` gehen in die Produktion; Themen im Status `idea` erst nach Quellenprüfung; Risiko „high“ vor jeder Veröffentlichung einzeln an Stefan.

Stand: 01.11.2026 (Wien). Marke Promptwerk, Marken-ID `claude_workflows`. **Entwurf, nicht freigegeben.**
Kalenderdatei: `C:\Automation\faceless-network\data\calendars\claude_workflows_2026-11.json` (168 Zeilen,
`fn.cli calendar check` ohne Befund am 01.11.2026). Grundlage: `Planungsrahmen Themen- und Kalenderplan.md`.

- 28 Tage, 84 Themen, 168 Posts. Je Tag 3 Themen als DE/EN-Paar; Deutsch 12:00, 14:00, 18:00, Englisch 15:00, 20:00, 23:00 (Wien).
- Status: alle 84 Themen `planned` (je Thema mindestens zwei Primärquellen geöffnet am 01.11.2026), 0 Themen `idea`.
- Risiko: 76 Themen niedrig, 8 mittel (Sicherheitsthemen: Berechtigungen, Sandbox, MCP-Vertrauen), 0 hoch.
- Quellen: nur offizielle Doku von Anthropic: Claude-Code-Doku (`code.claude.com/docs`, inklusive Changelog) und
  Claude-Plattform-Doku (`platform.claude.com/docs`). Geöffnet als Markdown-Fassung der Seiten (`<URL>.md`).
- Bezugsversion: Claude Code 2.1.316 (Changelog vom 31.10.2026). Modelle laut Doku: Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1.
  Die Skripte nennen die Version, die beim Schreiben aktuell ist; „getestet“ nur, wenn es wirklich lief (Markenregel).
- Oberflächen erscheinen als Animation, keine Bildschirmaufnahmen (Stefan, 30.10.2026).

## Themenreihen

Jede Reihe hat feste Plätze in der Woche (Thema 1 = DE 12:00 / EN 15:00, Thema 2 = 14:00 / 20:00, Thema 3 = 18:00 / 23:00).

| Reihe (DE / EN) | Format | Ziel | Plätze je Woche | Themen gesamt |
|---|---|---|---|---|
| Grundlagen / How it works | explainer | Ein Baustein von Claude oder Claude Code, genau so erklärt, wie ihn die Doku beschreibt | Mo 2, Di 1, Do 1, Fr 2, So 1 | 20 |
| In drei Schritten / In three steps | howto | Ein Ablauf zum Nachmachen, in drei Schritten, mit dem Beispiel aus der Doku | Mo 3, Di 2, Mi 3, Fr 1, Sa 3 | 20 |
| Mythos-Check / Myth check | myth | Eine verbreitete Annahme, die die Doku widerlegt oder einschränkt | Mo 1, Mi 1, Do 3, Sa 2 | 16 |
| Entweder-oder / This or that | comparison | Zwei Funktionen nebeneinander: wann welche passt | Di 3, Do 2, Sa 1, So 3 | 16 |
| Werkzeugkiste / Toolbox | listicle | 3 bis 6 Befehle, Kürzel oder Einstellungen in einer Liste | Mi 2, Fr 3, So 2 | 12 |

Beispiele je Reihe: Grundlagen „Auto Memory – Claude schreibt sich selbst Notizen“; In drei Schritten „Deinen ersten
Skill anlegen“; Mythos-Check „Mythos: Mehr Kontext ist immer besser“; Entweder-oder „CLAUDE.md oder Skill?“;
Werkzeugkiste „4 Tastenkürzel, die Zeit sparen“.

## Aus dem alten Entwurf übernommen

Der Entwurf vom 30.10.2026 (Themen für 05.–07.11.) liegt in `C:\Users\Stefa\Documents\_zum_loeschen\2026-11-01 Kalender alt`.
Alle drei Themen sind übernommen und in die erste Woche gelegt: CLAUDE.md (09.11., Thema 2), Hooks (09.11., Thema 3),
Deny-Regeln (10.11., Thema 2). Das Hooks-Testvideo (`05 Produktion\Promptwerk\2026-11\2026-11-06 Claude-Code-Hooks`) trägt noch die alte
Topic-ID `claude_workflows-20261106-2-de`; im neuen Kalender heißt das Thema `claude_workflows-20261109-3-de`.

## Kalender

| Datum | Uhrzeit DE/EN | Reihe | Titel DE | Titel EN | Format | Risiko | Quellen | Status |
|---|---|---|---|---|---|---|---|---|
| Mo 09.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Je länger die CLAUDE.md, desto besser | Myth: the longer your CLAUDE.md, the better | myth | niedrig | 2 | planned |
| Mo 09.11. | 14:00 / 20:00 | Grundlagen | CLAUDE.md – die Datei, die Claude Code zuerst liest | CLAUDE.md – the file Claude Code reads first | explainer | niedrig | 2 | planned |
| Mo 09.11. | 18:00 / 23:00 | In drei Schritten | Hooks – Regeln, die Claude Code nicht umgehen kann | Hooks – rules Claude Code can't talk its way around | howto | niedrig | 2 | planned |
| Di 10.11. | 12:00 / 15:00 | Grundlagen | Wie Claude Code eine Aufgabe abarbeitet | How Claude Code works through a task | explainer | niedrig | 2 | planned |
| Di 10.11. | 14:00 / 20:00 | In drei Schritten | Deny-Regeln – so sperrst du Claude Code von der .env aus | Deny rules – lock Claude Code out of your .env | howto | mittel | 2 | planned |
| Di 10.11. | 18:00 / 23:00 | Entweder-oder | CLAUDE.md oder Skill? | CLAUDE.md or a skill? | comparison | niedrig | 2 | planned |
| Mi 11.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Mehr Kontext ist immer besser | Myth: more context is always better | myth | niedrig | 2 | planned |
| Mi 11.11. | 14:00 / 20:00 | Werkzeugkiste | 5 Befehle für die erste Sitzung | 5 commands for your first session | listicle | niedrig | 2 | planned |
| Mi 11.11. | 18:00 / 23:00 | In drei Schritten | Deinen ersten Skill anlegen | Create your first skill | howto | niedrig | 2 | planned |
| Do 12.11. | 12:00 / 15:00 | Grundlagen | Was beim Kompaktieren verloren geht | What compaction keeps and what it drops | explainer | niedrig | 2 | planned |
| Do 12.11. | 14:00 / 20:00 | Entweder-oder | /compact oder /clear? | /compact or /clear? | comparison | niedrig | 2 | planned |
| Do 12.11. | 18:00 / 23:00 | Mythos-Check | Mythos: Checkpoints ersetzen Git | Myth: checkpoints replace git | myth | niedrig | 2 | planned |
| Fr 13.11. | 12:00 / 15:00 | In drei Schritten | Einen MCP-Server in drei Schritten verbinden | Connect an MCP server in three steps | howto | niedrig | 2 | planned |
| Fr 13.11. | 14:00 / 20:00 | Grundlagen | Auto Memory – Claude schreibt sich selbst Notizen | Auto memory – Claude takes its own notes | explainer | niedrig | 2 | planned |
| Fr 13.11. | 18:00 / 23:00 | Werkzeugkiste | 4 Tastenkürzel, die Zeit sparen | 4 shortcuts that save time | listicle | niedrig | 2 | planned |
| Sa 14.11. | 12:00 / 15:00 | Entweder-oder | Skill oder Subagent? | Skill or subagent? | comparison | niedrig | 2 | planned |
| Sa 14.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Viele Skills verstopfen den Kontext | Myth: lots of skills clog your context | myth | niedrig | 2 | planned |
| Sa 14.11. | 18:00 / 23:00 | In drei Schritten | Code nach jeder Änderung automatisch formatieren | Auto-format code after every edit | howto | niedrig | 2 | planned |
| So 15.11. | 12:00 / 15:00 | Grundlagen | Subagenten – ein eigenes Kontextfenster pro Aufgabe | Subagents – a separate context window per task | explainer | niedrig | 2 | planned |
| So 15.11. | 14:00 / 20:00 | Werkzeugkiste | Die Werkzeuge von Claude Code | The tools inside Claude Code | listicle | niedrig | 2 | planned |
| So 15.11. | 18:00 / 23:00 | Entweder-oder | Berechtigungsregel oder Hook? | Permission rule or hook? | comparison | mittel | 2 | planned |
| Mo 16.11. | 12:00 / 15:00 | Mythos-Check | Mythos: WICHTIG in Großbuchstaben wirkt besser | Myth: IMPORTANT in caps works better | myth | niedrig | 2 | planned |
| Mo 16.11. | 14:00 / 20:00 | Grundlagen | Skills – Wissen, das erst bei Bedarf geladen wird | Skills – knowledge that loads only when needed | explainer | niedrig | 2 | planned |
| Mo 16.11. | 18:00 / 23:00 | In drei Schritten | Benachrichtigung, wenn Claude auf dich wartet | Get notified when Claude needs you | howto | niedrig | 2 | planned |
| Di 17.11. | 12:00 / 15:00 | Grundlagen | Checkpoints – zurück zum Stand vor der Änderung | Checkpoints – rewind to before the edit | explainer | niedrig | 2 | planned |
| Di 17.11. | 14:00 / 20:00 | In drei Schritten | Einen eigenen Subagenten bauen | Build your own subagent | howto | niedrig | 2 | planned |
| Di 17.11. | 18:00 / 23:00 | Entweder-oder | Opus, Sonnet oder Haiku? | Opus, Sonnet or Haiku? | comparison | niedrig | 2 | planned |
| Mi 18.11. | 12:00 / 15:00 | Mythos-Check | Mythos: /clear löscht Claudes Gedächtnis | Myth: /clear wipes Claude's memory | myth | niedrig | 2 | planned |
| Mi 18.11. | 14:00 / 20:00 | Werkzeugkiste | 4 Hook-Ereignisse, die du kennen solltest | 4 hook events worth knowing | listicle | niedrig | 2 | planned |
| Mi 18.11. | 18:00 / 23:00 | In drei Schritten | Regeln nur für bestimmte Ordner: .claude/rules/ | Rules for specific folders: .claude/rules/ | howto | niedrig | 2 | planned |
| Do 19.11. | 12:00 / 15:00 | Grundlagen | Fast Mode – schneller, aber nicht für jedes Modell | Fast mode – faster, but not on every model | explainer | niedrig | 2 | planned |
| Do 19.11. | 14:00 / 20:00 | Entweder-oder | Output Style oder --append-system-prompt? | Output style or --append-system-prompt? | comparison | niedrig | 2 | planned |
| Do 19.11. | 18:00 / 23:00 | Mythos-Check | Mythos: bypassPermissions ist auf dem eigenen Rechner harmlos | Myth: bypassPermissions is fine on your own machine | myth | mittel | 2 | planned |
| Fr 20.11. | 12:00 / 15:00 | In drei Schritten | CLAUDE.md aufteilen mit @-Importen | Split your CLAUDE.md with @ imports | howto | niedrig | 2 | planned |
| Fr 20.11. | 14:00 / 20:00 | Grundlagen | MCP-Server: lokal, Projekt oder Benutzer | MCP servers: local, project or user scope | explainer | niedrig | 2 | planned |
| Fr 20.11. | 18:00 / 23:00 | Werkzeugkiste | 4 Schalter für Claude Code in Skripten | 4 flags for Claude Code in scripts | listicle | niedrig | 2 | planned |
| Sa 21.11. | 12:00 / 15:00 | Entweder-oder | MCP oder Skill? | MCP or skill? | comparison | niedrig | 2 | planned |
| Sa 21.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Subagenten sind gratis | Myth: subagents are free | myth | niedrig | 2 | planned |
| Sa 21.11. | 18:00 / 23:00 | In drei Schritten | Statuszeile mit Kontextanzeige | A status line that shows your context | howto | niedrig | 2 | planned |
| So 22.11. | 12:00 / 15:00 | Grundlagen | Planmodus – erst lesen, dann ändern | Plan mode – read first, edit later | explainer | niedrig | 2 | planned |
| So 22.11. | 14:00 / 20:00 | Werkzeugkiste | 5 Wege, Tokens zu sparen | 5 ways to spend fewer tokens | listicle | niedrig | 2 | planned |
| So 22.11. | 18:00 / 23:00 | Entweder-oder | Projekt, lokal oder Benutzer: welche settings.json gilt? | Project, local or user: which settings.json wins? | comparison | niedrig | 2 | planned |
| Mo 23.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Eine geänderte CLAUDE.md wirkt sofort | Myth: CLAUDE.md edits apply instantly | myth | niedrig | 2 | planned |
| Mo 23.11. | 14:00 / 20:00 | Grundlagen | Was Claude Code in großen Projekten nicht liest | What Claude Code skips in large repos | explainer | niedrig | 2 | planned |
| Mo 23.11. | 18:00 / 23:00 | In drei Schritten | Geprüftes JSON aus Claude Code holen | Get validated JSON out of Claude Code | howto | niedrig | 2 | planned |
| Di 24.11. | 12:00 / 15:00 | Grundlagen | Claude Code ohne Chatfenster: der Modus -p | Claude Code without a chat: the -p mode | explainer | niedrig | 2 | planned |
| Di 24.11. | 14:00 / 20:00 | In drei Schritten | @claude im GitHub-Issue | @claude in a GitHub issue | howto | niedrig | 2 | planned |
| Di 24.11. | 18:00 / 23:00 | Entweder-oder | Standardmodus oder dontAsk? | Default mode or dontAsk? | comparison | mittel | 2 | planned |
| Mi 25.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Claude Code ist nur für Code | Myth: Claude Code is only for code | myth | niedrig | 2 | planned |
| Mi 25.11. | 14:00 / 20:00 | Werkzeugkiste | Mitgelieferte Skills in Claude Code | Skills that ship with Claude Code | listicle | niedrig | 2 | planned |
| Mi 25.11. | 18:00 / 23:00 | In drei Schritten | Zwei Aufgaben gleichzeitig mit --worktree | Two tasks at once with --worktree | howto | niedrig | 2 | planned |
| Do 26.11. | 12:00 / 15:00 | Grundlagen | Prompt-Caching in Claude Code | Prompt caching in Claude Code | explainer | niedrig | 2 | planned |
| Do 26.11. | 14:00 / 20:00 | Entweder-oder | --continue oder --resume? | --continue or --resume? | comparison | niedrig | 2 | planned |
| Do 26.11. | 18:00 / 23:00 | Mythos-Check | Mythos: Eine Read-Sperre blockiert jeden Zugriff | Myth: a Read deny rule blocks every access | myth | mittel | 2 | planned |
| Fr 27.11. | 12:00 / 15:00 | In drei Schritten | Bash-Befehle in die Sandbox schicken | Run bash commands in the sandbox | howto | mittel | 2 | planned |
| Fr 27.11. | 14:00 / 20:00 | Grundlagen | Effort – wie viel Claude nachdenkt | Effort – how hard Claude thinks | explainer | niedrig | 2 | planned |
| Fr 27.11. | 18:00 / 23:00 | Werkzeugkiste | Die eingebauten Subagenten | The built-in subagents | listicle | niedrig | 2 | planned |
| Sa 28.11. | 12:00 / 15:00 | Entweder-oder | Thinking oder Effort? | Thinking or effort? | comparison | niedrig | 2 | planned |
| Sa 28.11. | 14:00 / 20:00 | Mythos-Check | Mythos: ultrathink ist ein Zauberwort | Myth: ultrathink is a magic word | myth | niedrig | 2 | planned |
| Sa 28.11. | 18:00 / 23:00 | In drei Schritten | Tests erzwingen mit einem Stop-Hook | Enforce your tests with a Stop hook | howto | niedrig | 2 | planned |
| So 29.11. | 12:00 / 15:00 | Grundlagen | Claude liest PDFs mit Diagrammen und Tabellen | Claude reads PDFs, charts and tables included | explainer | niedrig | 2 | planned |
| So 29.11. | 14:00 / 20:00 | Werkzeugkiste | 4 Prompt-Techniken aus der Anthropic-Doku | 4 prompting techniques from Anthropic's docs | listicle | niedrig | 2 | planned |
| So 29.11. | 18:00 / 23:00 | Entweder-oder | Subagent oder Agent-Team? | Subagent or agent team? | comparison | niedrig | 2 | planned |
| Mo 30.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Jeder MCP-Server ist geprüft | Myth: every MCP server is vetted | myth | mittel | 2 | planned |
| Mo 30.11. | 14:00 / 20:00 | Grundlagen | Plugins – Skills, Agenten und Hooks als Paket | Plugins – skills, agents and hooks in one package | explainer | niedrig | 2 | planned |
| Mo 30.11. | 18:00 / 23:00 | In drei Schritten | Ein Plugin aus dem Marketplace installieren | Install a plugin from a marketplace | howto | niedrig | 2 | planned |
| Di 01.12. | 12:00 / 15:00 | Grundlagen | Git-Worktrees – parallele Sitzungen ohne Konflikte | Git worktrees – parallel sessions without collisions | explainer | niedrig | 2 | planned |
| Di 01.12. | 14:00 / 20:00 | In drei Schritten | Eigene Tastenkürzel für Claude Code | Custom keyboard shortcuts for Claude Code | howto | niedrig | 2 | planned |
| Di 01.12. | 18:00 / 23:00 | Entweder-oder | Zeitgesteuert: Cloud, Desktop oder /loop? | Scheduled: cloud, desktop or /loop? | comparison | niedrig | 3 | planned |
| Mi 02.12. | 12:00 / 15:00 | Mythos-Check | Mythos: Auto Mode heißt alles erlauben | Myth: auto mode means allow everything | myth | mittel | 2 | planned |
| Mi 02.12. | 14:00 / 20:00 | Werkzeugkiste | Wenn Claude Code deine Einstellung ignoriert | When Claude Code ignores your settings | listicle | niedrig | 2 | planned |
| Mi 02.12. | 18:00 / 23:00 | In drei Schritten | Screenshots direkt an Claude Code geben | Hand screenshots straight to Claude Code | howto | niedrig | 2 | planned |
| Do 03.12. | 12:00 / 15:00 | Grundlagen | Welche Claude-Code-Version habe ich – und was ist neu? | Which Claude Code version am I on – and what's new? | explainer | niedrig | 2 | planned |
| Do 03.12. | 14:00 / 20:00 | Entweder-oder | Structured Outputs oder JSON per Prompt? | Structured outputs or JSON by prompt? | comparison | niedrig | 2 | planned |
| Do 03.12. | 18:00 / 23:00 | Mythos-Check | Mythos: Claude weiß schon, was du meinst | Myth: Claude knows what you mean | myth | niedrig | 2 | planned |
| Fr 04.12. | 12:00 / 15:00 | In drei Schritten | Wichtiges nach dem Kompaktieren wieder einspielen | Re-inject key context after compaction | howto | niedrig | 2 | planned |
| Fr 04.12. | 14:00 / 20:00 | Grundlagen | Claude Code mit Chrome | Claude Code with Chrome | explainer | niedrig | 2 | planned |
| Fr 04.12. | 18:00 / 23:00 | Werkzeugkiste | Die eingebauten Output Styles | The built-in output styles | listicle | niedrig | 2 | planned |
| Sa 05.12. | 12:00 / 15:00 | Entweder-oder | Terminal, Desktop oder VS Code? | Terminal, desktop or VS Code? | comparison | niedrig | 2 | planned |
| Sa 05.12. | 14:00 / 20:00 | Mythos-Check | Mythos: Prompt-Caching muss man selbst einschalten | Myth: you have to switch on prompt caching | myth | niedrig | 2 | planned |
| Sa 05.12. | 18:00 / 23:00 | In drei Schritten | Bessere Antworten mit Beispielen im Prompt | Better answers with examples in your prompt | howto | niedrig | 2 | planned |
| So 06.12. | 12:00 / 15:00 | Grundlagen | Remote Control – die lokale Sitzung am Handy weiterführen | Remote Control – continue a local session on your phone | explainer | niedrig | 2 | planned |
| So 06.12. | 14:00 / 20:00 | Werkzeugkiste | 3 Umgebungsvariablen für Claude Code | 3 environment variables for Claude Code | listicle | niedrig | 2 | planned |
| So 06.12. | 18:00 / 23:00 | Entweder-oder | Lokal oder in der Cloud? | Local or in the cloud? | comparison | niedrig | 2 | planned |

## Quellen je Thema (abgerufen 01.11.2026)

Schlüssel wie in der Spalte `notes` der Kalenderdatei.

- **09.11. Thema 1 (M1) Mythos: Je länger die CLAUDE.md, desto besser:** https://code.claude.com/docs/en/best-practices, https://code.claude.com/docs/en/memory.
- **09.11. Thema 2 (G1) CLAUDE.md – die Datei, die Claude Code zuerst liest:** https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/commands. Hinweis: aus altem Kalender (05.11.) übernommen.
- **09.11. Thema 3 (H1) Hooks – Regeln, die Claude Code nicht umgehen kann:** https://code.claude.com/docs/en/hooks-guide, https://code.claude.com/docs/en/memory. Hinweis: Testvideo vorhanden: 05 Produktion\Promptwerk\2026-11\2026-11-06 Claude-Code-Hooks (alte ID claude_workflows-20261106-2-de); Produktion liegt bei der Sitzung Qualitätsrunde.
- **10.11. Thema 1 (G4) Wie Claude Code eine Aufgabe abarbeitet:** https://code.claude.com/docs/en/how-claude-code-works, https://code.claude.com/docs/en/overview.
- **10.11. Thema 2 (H2) Deny-Regeln – so sperrst du Claude Code von der .env aus:** https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/cli-reference. Hinweis: aus altem Kalender (07.11.) übernommen; Grenze laut Doku nennen: Deny greift nicht bei Skripten, die Dateien indirekt lesen.
- **10.11. Thema 3 (V1) CLAUDE.md oder Skill?:** https://code.claude.com/docs/en/features-overview, https://code.claude.com/docs/en/costs.
- **11.11. Thema 1 (M2) Mythos: Mehr Kontext ist immer besser:** https://platform.claude.com/docs/en/build-with-claude/context-windows, https://code.claude.com/docs/en/context-window.
- **11.11. Thema 2 (W1) 5 Befehle für die erste Sitzung:** https://code.claude.com/docs/en/commands, https://code.claude.com/docs/en/memory.
- **11.11. Thema 3 (H5) Deinen ersten Skill anlegen:** https://code.claude.com/docs/en/skills, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.
- **12.11. Thema 1 (G3) Was beim Kompaktieren verloren geht:** https://code.claude.com/docs/en/context-window, https://code.claude.com/docs/en/how-claude-code-works.
- **12.11. Thema 2 (V5) /compact oder /clear?:** https://code.claude.com/docs/en/commands, https://code.claude.com/docs/en/context-window.
- **12.11. Thema 3 (M3) Mythos: Checkpoints ersetzen Git:** https://code.claude.com/docs/en/checkpointing, https://code.claude.com/docs/en/best-practices.
- **13.11. Thema 1 (H7) Einen MCP-Server in drei Schritten verbinden:** https://code.claude.com/docs/en/mcp-quickstart, https://code.claude.com/docs/en/mcp.
- **13.11. Thema 2 (G2) Auto Memory – Claude schreibt sich selbst Notizen:** https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/commands.
- **13.11. Thema 3 (W2) 4 Tastenkürzel, die Zeit sparen:** https://code.claude.com/docs/en/interactive-mode, https://code.claude.com/docs/en/keybindings. Hinweis: Windows-Varianten der Kürzel laut interactive-mode.
- **14.11. Thema 1 (V2) Skill oder Subagent?:** https://code.claude.com/docs/en/features-overview, https://code.claude.com/docs/en/sub-agents.
- **14.11. Thema 2 (M6) Mythos: Viele Skills verstopfen den Kontext:** https://code.claude.com/docs/en/skills, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.
- **14.11. Thema 3 (H3) Code nach jeder Änderung automatisch formatieren:** https://code.claude.com/docs/en/hooks-guide, https://code.claude.com/docs/en/hooks.
- **15.11. Thema 1 (G6) Subagenten – ein eigenes Kontextfenster pro Aufgabe:** https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/features-overview.
- **15.11. Thema 2 (W12) Die Werkzeuge von Claude Code:** https://code.claude.com/docs/en/tools-reference, https://code.claude.com/docs/en/how-claude-code-works.
- **15.11. Thema 3 (V3) Berechtigungsregel oder Hook?:** https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/hooks-guide. Hinweis: Sicherheitsthema; Vorrang laut permissions › Precedence among rules, hooks, and mods.
- **16.11. Thema 1 (M9) Mythos: WICHTIG in Großbuchstaben wirkt besser:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://code.claude.com/docs/en/best-practices.
- **16.11. Thema 2 (G7) Skills – Wissen, das erst bei Bedarf geladen wird:** https://code.claude.com/docs/en/skills, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.
- **16.11. Thema 3 (H4) Benachrichtigung, wenn Claude auf dich wartet:** https://code.claude.com/docs/en/hooks-guide, https://code.claude.com/docs/en/terminal-config.
- **17.11. Thema 1 (G5) Checkpoints – zurück zum Stand vor der Änderung:** https://code.claude.com/docs/en/checkpointing, https://code.claude.com/docs/en/interactive-mode.
- **17.11. Thema 2 (H6) Einen eigenen Subagenten bauen:** https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/commands. Hinweis: /agents druckt laut Doku nur einen Hinweis, legt nichts an.
- **17.11. Thema 3 (V6) Opus, Sonnet oder Haiku?:** https://platform.claude.com/docs/en/about-claude/models/choosing-a-model, https://code.claude.com/docs/en/model-config. Hinweis: Modellnamen Stand 01.11.2026: Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1.
- **18.11. Thema 1 (M15) Mythos: /clear löscht Claudes Gedächtnis:** https://code.claude.com/docs/en/commands, https://code.claude.com/docs/en/memory.
- **18.11. Thema 2 (W3) 4 Hook-Ereignisse, die du kennen solltest:** https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/hooks-guide.
- **18.11. Thema 3 (H12) Regeln nur für bestimmte Ordner: .claude/rules/:** https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/best-practices.
- **19.11. Thema 1 (G17) Fast Mode – schneller, aber nicht für jedes Modell:** https://code.claude.com/docs/en/fast-mode, https://code.claude.com/docs/en/changelog. Hinweis: Abkündigung: Entfernung für Opus 4.8 am 30.11.2026 laut Changelog 2.1.316; Datum vor Skript neu prüfen.
- **19.11. Thema 2 (V9) Output Style oder --append-system-prompt?:** https://code.claude.com/docs/en/output-styles, https://code.claude.com/docs/en/cli-reference.
- **19.11. Thema 3 (M4) Mythos: bypassPermissions ist auf dem eigenen Rechner harmlos:** https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/security. Hinweis: Sicherheitsthema.
- **20.11. Thema 1 (H13) CLAUDE.md aufteilen mit @-Importen:** https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/claude-directory.
- **20.11. Thema 2 (G8) MCP-Server: lokal, Projekt oder Benutzer:** https://code.claude.com/docs/en/mcp, https://code.claude.com/docs/en/features-overview.
- **20.11. Thema 3 (W4) 4 Schalter für Claude Code in Skripten:** https://code.claude.com/docs/en/cli-reference, https://code.claude.com/docs/en/headless.
- **21.11. Thema 1 (V10) MCP oder Skill?:** https://code.claude.com/docs/en/features-overview, https://code.claude.com/docs/en/best-practices.
- **21.11. Thema 2 (M5) Mythos: Subagenten sind gratis:** https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/best-practices.
- **21.11. Thema 3 (H8) Statuszeile mit Kontextanzeige:** https://code.claude.com/docs/en/statusline, https://code.claude.com/docs/en/context-window.
- **22.11. Thema 1 (G11) Planmodus – erst lesen, dann ändern:** https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/common-workflows.
- **22.11. Thema 2 (W5) 5 Wege, Tokens zu sparen:** https://code.claude.com/docs/en/costs, https://code.claude.com/docs/en/best-practices.
- **22.11. Thema 3 (V11) Projekt, lokal oder Benutzer: welche settings.json gilt?:** https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/permissions.
- **23.11. Thema 1 (M13) Mythos: Eine geänderte CLAUDE.md wirkt sofort:** https://code.claude.com/docs/en/prompt-caching, https://code.claude.com/docs/en/memory.
- **23.11. Thema 2 (G14) Was Claude Code in großen Projekten nicht liest:** https://code.claude.com/docs/en/large-codebases, https://code.claude.com/docs/en/permissions.
- **23.11. Thema 3 (H10) Geprüftes JSON aus Claude Code holen:** https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/cli-reference.
- **24.11. Thema 1 (G13) Claude Code ohne Chatfenster: der Modus -p:** https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/cli-reference.
- **24.11. Thema 2 (H9) @claude im GitHub-Issue:** https://code.claude.com/docs/en/github-actions, https://code.claude.com/docs/en/headless.
- **24.11. Thema 3 (V4) Standardmodus oder dontAsk?:** https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/headless. Hinweis: Sicherheitsthema.
- **25.11. Thema 1 (M8) Mythos: Claude Code ist nur für Code:** https://code.claude.com/docs/en/common-workflows, https://code.claude.com/docs/en/overview.
- **25.11. Thema 2 (W6) Mitgelieferte Skills in Claude Code:** https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/troubleshooting.
- **25.11. Thema 3 (H11) Zwei Aufgaben gleichzeitig mit --worktree:** https://code.claude.com/docs/en/worktrees, https://code.claude.com/docs/en/common-workflows.
- **26.11. Thema 1 (G9) Prompt-Caching in Claude Code:** https://code.claude.com/docs/en/prompt-caching, https://platform.claude.com/docs/en/build-with-claude/prompt-caching.
- **26.11. Thema 2 (V13) --continue oder --resume?:** https://code.claude.com/docs/en/sessions, https://code.claude.com/docs/en/cli-reference.
- **26.11. Thema 3 (M10) Mythos: Eine Read-Sperre blockiert jeden Zugriff:** https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/sandboxing. Hinweis: Sicherheitsthema; Sandbox als Ergänzung laut permissions › How permissions interact with sandboxing.
- **27.11. Thema 1 (H14) Bash-Befehle in die Sandbox schicken:** https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/security. Hinweis: Sicherheitshinweis: Grenzen der Sandbox laut Doku nennen.
- **27.11. Thema 2 (G10) Effort – wie viel Claude nachdenkt:** https://code.claude.com/docs/en/model-config, https://platform.claude.com/docs/en/build-with-claude/effort. Hinweis: Standardwerte je Modell vor dem Skript erneut prüfen (choosing-a-model).
- **27.11. Thema 3 (W7) Die eingebauten Subagenten:** https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/how-claude-code-works. Hinweis: Liste der eingebauten Subagenten vor Skript vollständig aus cc/sub-agents übernehmen.
- **28.11. Thema 1 (V14) Thinking oder Effort?:** https://platform.claude.com/docs/en/build-with-claude/effort, https://platform.claude.com/docs/en/build-with-claude/extended-thinking. Hinweis: Detail aus pl thinking#thinking-and-effort vor Skript lesen.
- **28.11. Thema 2 (M7) Mythos: ultrathink ist ein Zauberwort:** https://code.claude.com/docs/en/model-config, https://code.claude.com/docs/en/changelog. Hinweis: Changelog 2.1.316 (31.10.2026): CLAUDE_CODE_DISABLE_ULTRATHINK.
- **28.11. Thema 3 (H15) Tests erzwingen mit einem Stop-Hook:** https://code.claude.com/docs/en/best-practices, https://code.claude.com/docs/en/hooks-guide. Hinweis: Blockgrenze für Stop-Hooks (hooks-guide: block cap) erwähnen.
- **29.11. Thema 1 (G12) Claude liest PDFs mit Diagrammen und Tabellen:** https://platform.claude.com/docs/en/build-with-claude/pdf-support, https://platform.claude.com/docs/en/build-with-claude/vision. Hinweis: Plattform-Doku (API); für claude.ai vor dem Skript Gültigkeit prüfen.
- **29.11. Thema 2 (W9) 4 Prompt-Techniken aus der Anthropic-Doku:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.
- **29.11. Thema 3 (V12) Subagent oder Agent-Team?:** https://code.claude.com/docs/en/agent-teams, https://code.claude.com/docs/en/sub-agents. Hinweis: Agent-Teams experimentell (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS).
- **30.11. Thema 1 (M11) Mythos: Jeder MCP-Server ist geprüft:** https://code.claude.com/docs/en/mcp, https://code.claude.com/docs/en/security. Hinweis: Sicherheitsthema.
- **30.11. Thema 2 (G15) Plugins – Skills, Agenten und Hooks als Paket:** https://code.claude.com/docs/en/plugins/overview, https://code.claude.com/docs/en/plugins/install.
- **30.11. Thema 3 (H16) Ein Plugin aus dem Marketplace installieren:** https://code.claude.com/docs/en/plugins/install, https://code.claude.com/docs/en/plugins/overview.
- **01.12. Thema 1 (G16) Git-Worktrees – parallele Sitzungen ohne Konflikte:** https://code.claude.com/docs/en/worktrees, https://code.claude.com/docs/en/common-workflows.
- **01.12. Thema 2 (H17) Eigene Tastenkürzel für Claude Code:** https://code.claude.com/docs/en/keybindings, https://code.claude.com/docs/en/interactive-mode.
- **01.12. Thema 3 (V15) Zeitgesteuert: Cloud, Desktop oder /loop?:** https://code.claude.com/docs/en/routines, https://code.claude.com/docs/en/desktop-scheduled-tasks, https://code.claude.com/docs/en/scheduled-tasks. Hinweis: Cloud-Aufgaben (früher Routines) laut Doku Research Preview.
- **02.12. Thema 1 (M12) Mythos: Auto Mode heißt alles erlauben:** https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/auto-mode-config. Hinweis: Sicherheitsthema.
- **02.12. Thema 2 (W10) Wenn Claude Code deine Einstellung ignoriert:** https://code.claude.com/docs/en/debug-your-config, https://code.claude.com/docs/en/troubleshooting.
- **02.12. Thema 3 (H18) Screenshots direkt an Claude Code geben:** https://code.claude.com/docs/en/common-workflows, https://code.claude.com/docs/en/interactive-mode.
- **03.12. Thema 1 (G18) Welche Claude-Code-Version habe ich – und was ist neu?:** https://code.claude.com/docs/en/changelog, https://code.claude.com/docs/en/whats-new/index. Hinweis: Stand Changelog 31.10.2026: Version 2.1.316; vor dem Skript aktuelle Version neu ablesen.
- **03.12. Thema 2 (V16) Structured Outputs oder JSON per Prompt?:** https://platform.claude.com/docs/en/build-with-claude/structured-outputs, https://code.claude.com/docs/en/headless.
- **03.12. Thema 3 (M14) Mythos: Claude weiß schon, was du meinst:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://code.claude.com/docs/en/best-practices.
- **04.12. Thema 1 (H19) Wichtiges nach dem Kompaktieren wieder einspielen:** https://code.claude.com/docs/en/hooks-guide, https://code.claude.com/docs/en/context-window.
- **04.12. Thema 2 (G20) Claude Code mit Chrome:** https://code.claude.com/docs/en/chrome, https://code.claude.com/docs/en/overview. Hinweis: Voraussetzungen (Erweiterung, Pläne) vor dem Skript aus cc/chrome übernehmen.
- **04.12. Thema 3 (W11) Die eingebauten Output Styles:** https://code.claude.com/docs/en/output-styles, https://code.claude.com/docs/en/commands.
- **05.12. Thema 1 (V7) Terminal, Desktop oder VS Code?:** https://code.claude.com/docs/en/platforms, https://code.claude.com/docs/en/desktop.
- **05.12. Thema 2 (M16) Mythos: Prompt-Caching muss man selbst einschalten:** https://code.claude.com/docs/en/prompt-caching, https://code.claude.com/docs/en/costs. Hinweis: Formulierung /usage vor Skript in cc/costs prüfen (Session-Block).
- **05.12. Thema 3 (H20) Bessere Antworten mit Beispielen im Prompt:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.
- **06.12. Thema 1 (G19) Remote Control – die lokale Sitzung am Handy weiterführen:** https://code.claude.com/docs/en/remote-control, https://code.claude.com/docs/en/platforms. Hinweis: Trusted Devices ist laut Doku Beta; nicht als Kernaussage verwenden.
- **06.12. Thema 2 (W8) 3 Umgebungsvariablen für Claude Code:** https://code.claude.com/docs/en/env-vars, https://code.claude.com/docs/en/memory.
- **06.12. Thema 3 (V8) Lokal oder in der Cloud?:** https://code.claude.com/docs/en/claude-code-on-the-web, https://code.claude.com/docs/en/platforms. Hinweis: 'weiterläuft' vor Skript in cc/claude-code-on-the-web bestätigen.

## Offene Punkte für Stefan

1. Freigabe des Plans. Bis dahin bleibt alles Entwurf; nichts ist produziert oder veröffentlicht.
2. Englische Uhrzeiten (15:00, 20:00, 23:00 Wien) sind eine Annahme aus dem Planungsrahmen.
3. Hooks-Testvideo: Die alte Topic-ID im Produktionsordner und im Regieplan passt nicht mehr zum neuen Kalender.
   Die Sitzung „Promptwerk: Qualitätsrunde Video“ entscheidet, ob sie umbenennt; ihre Dateien wurden nicht angefasst.
4. Einige Funktionen sind laut Doku Vorschau oder experimentell (Agent-Teams, Cloud-Aufgaben, Fast Mode auf Opus 5 und 4.8,
   Trusted Devices bei Remote Control). Die betroffenen Themen sagen das; vor dem Skript den Stand erneut prüfen.
5. Fast Mode für Opus 4.8 wird laut Changelog am 30.11.2026 entfernt; das Thema liegt deshalb davor (19.11.). Vor dem Skript erneut prüfen.
6. Nicht in Claude Code geprüft: Kein Thema wurde praktisch nachgestellt (die CLI-Anmeldung war am 30.10.2026 abgelaufen).
   Alle Aussagen stützen sich auf die Doku; ein Skript darf nur „laut Doku“ sagen, nicht „getestet“.
