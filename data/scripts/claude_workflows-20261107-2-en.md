---
topic_id: claude_workflows-20261107-2
brand_id: claude_workflows
language: en
title: Deny rules – how to lock Claude Code out of your .env
description: "Permissions in Claude Code: deny beats allow, Read(./.env) protects secrets, rules live in settings.json."
hashtags: [claudecode, permissions, security, aiworkflow, developer]
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
One line in your settings, and Claude never sees your keys again. [S1]
> visual: headline="One line locks the keys away" kind="hook"

## Scene 2 (card)
Claude Code has a permission system with three lists: allow, ask and deny. Rules are evaluated in exactly that order: deny first, then ask, then allow. The first match decides. [S1]
> visual: headline="deny, then ask, then allow" body="The first match decides, specificity does not change the order" kind="card"

## Scene 3 (card)
That means a broad deny rule beats every narrower allow rule. You cannot carve an exception out of a deny. Which is exactly how it should be. [S1]
> visual: headline="deny beats allow" body="A block has no exceptions" kind="card"

## Scene 4 (code)
For secrets there is a Read rule with a path. Read with dot slash dot env blocks that file in the project. The same rule also blocks Edit and Write on the path, and it covers cat, head and tail in the shell. [S1]
> visual: headline="Read(./.env) blocks the file" code="{ \"permissions\": {|    \"deny\": [|      \"Read(./.env)\",|      \"Read(./secrets/**)\"|    ] } }" kind="code"

## Scene 5 (fact)
Rules live in settings.json: in the project under .claude, locally in settings.local.json, or globally in your home folder. On Windows, paths are normalized to POSIX form before matching. And a .claudeignore file has no effect, so move its entries into deny rules. [S1]
> visual: headline="settings.json, three levels" number="3" body="project · local · user; .claudeignore does nothing" kind="fact"

## Scene 6 (payoff)
For scripts and CI there is the counterpart: with the allowedTools flag you release only the tools a run needs when you call claude -p. Checked with Claude Code two point one. Follow for the next workflow. [S2]
> visual: headline="Block in the project, allow per run" kind="payoff"
