---
topic_id: claude_workflows-20261105-2
brand_id: claude_workflows
language: en
title: CLAUDE.md – the file Claude Code reads first
description: Why every project needs a CLAUDE.md, what belongs in it and how /init writes the first draft. Checked with Claude Code 2.1.
hashtags: [claudecode, claude, promptengineering, aiworkflow, developer]
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
Claude Code forgets everything after every session. Except one file. [S1]
> visual: headline="The one file Claude never forgets" kind="hook"

## Scene 2 (card)
Each session begins with a fresh context window. The CLAUDE.md in your project folder is loaded automatically at the start of every session. It is context, not an enforced rule. If you need to block an action for real, use a hook instead. [S1]
> visual: headline="CLAUDE.md loads at every start" body="Project root or .claude/CLAUDE.md, plus ~/.claude/CLAUDE.md for your personal rules" kind="card"

## Scene 3 (code)
You do not have to write it yourself. Run /init and Claude analyzes your codebase and creates a file with build commands, test instructions and the conventions it discovers. If a CLAUDE.md already exists, /init suggests improvements instead of overwriting it. [S1]
> visual: headline="/init writes the first draft" code="$ claude|> /init|CLAUDE.md created: build, tests, conventions|> /context  → Memory files" kind="code"

## Scene 4 (fact)
What belongs in it: build and test commands, coding standards, architecture decisions and common workflows. And keep it short. The docs recommend staying under two hundred lines, because longer files consume more context and reduce adherence. [S1]
> visual: headline="Stay under 200 lines" number="200" body="Build, tests, standards, decisions, workflows" kind="fact"

## Scene 5 (card)
Split long files instead. With an at sign you import other files, for example the README or a git guide. Personal preferences go into CLAUDE.local.md, which you add to your gitignore. [S1]
> visual: headline="Split, do not bloat" body="@README imports a file, CLAUDE.local.md stays private" kind="card"

## Scene 6 (payoff)
The effect: Claude already knows your rules before the first command. That is the foundation of every workflow we show here, checked with Claude Code version two point one. Follow for the next workflow. [S2]
> visual: headline="Rules before the first command" kind="payoff"
