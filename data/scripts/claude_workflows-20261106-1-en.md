---
topic_id: claude_workflows-20261106-1
brand_id: claude_workflows
language: en
title: Hooks – rules Claude Code cannot talk its way around
description: CLAUDE.md is context, hooks are enforcement. How a PreToolUse hook blocks edits to your .env file.
hashtags: [claudecode, hooks, automation, aiworkflow, developer]
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
Your CLAUDE.md says: never touch the .env file. Claude can still do it. [S2]
> visual: headline="A rule Claude can ignore" kind="hook"

## Scene 2 (card)
The docs say it themselves: CLAUDE.md is context, not enforced configuration. To block an action regardless of what Claude decides, you need a PreToolUse hook. [S2]
> visual: headline="Context or enforcement?" body="CLAUDE.md gets read, a hook gets executed" kind="card"

## Scene 3 (card)
Hooks are user-defined shell commands that Claude Code runs at specific points in its lifecycle. That gives you deterministic control: certain actions always happen instead of relying on the model to choose to run them. [S1]
> visual: headline="Hooks always run" body="Shell commands at fixed points: before tools, after edits, at the end" kind="card"

## Scene 4 (code)
The events are called things like PreToolUse before a tool call, PostToolUse after it, SessionStart when a session begins and Stop when Claude finishes responding. Only PreToolUse can block an action. [S1]
> visual: headline="Four events you need" code="PreToolUse   → can block|PostToolUse  → formatter, log|SessionStart → load context|Stop         → final check" kind="code"

## Scene 5 (fact)
The configuration lives in settings.json, globally under .claude in your home folder or inside the project. A hook that exits with code two blocks the action, and Claude receives the reason as feedback. That is exactly how the example in the docs stops edits to the .env file. [S1]
> visual: headline="Exit code 2 blocks" number="2" body="settings.json in the project or in your home folder" kind="fact"

## Scene 6 (payoff)
Remember: what goes into CLAUDE.md is a request. What goes into a hook is a law. Checked with Claude Code two point one. Follow for the next workflow.
> visual: headline="Request or law" kind="payoff"
