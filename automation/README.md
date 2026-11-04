# Windows Task Scheduler templates (not registered yet)

Phase 1 ships the templates only. Registering them is a Phase 2 step that Stefan triggers by hand:

```powershell
# from an elevated PowerShell in C:\Automation\faceless-network
.\automation\register_tasks.ps1 -WhatIf      # shows what would be registered
.\automation\register_tasks.ps1              # registers the tasks below
```

| Task | Time (Europe/Vienna) | Runs | Needs Claude? |
|---|---|---|---|
| `FN Render Queue` | 09:00 daily | `run_render.ps1`: produce every script in `data/scripts/` that has no video yet | no |
| `FN Publish Sync` | hourly :05, 08-23 | `run_publish.ps1`: `fn publish --dry-run` until Phase 2 flips `--live` | no |
| `FN Costs and Status` | 19:00 daily | `run_status.ps1`: status, costs, free space -> `logs/status_<date>.txt` | no |
| `FN Topic Proposals` | 19:30 daily | `claude -p` with `prompts/calendar_planner.md` (template `run_claude_calendar.ps1`) | yes |
| `FN Month Plan` (template, commented out in `register_tasks.ps1`) | daily 18:00 laptop time, acts on the 24th at 19:30 Vienna | `run_month_plan.ps1`: plans the next month per brand (2 topics a day, DE and EN) from the Konzeptplan; proposals for open slots via `claude -p` (`docs/daily-runner.md` section 6) | yes (`claude -p`, only for proposals) |
| `FN Daily Runner` (template, commented out in `register_tasks.ps1`) | 06:30 daily | `run_daily.ps1`: Tagesläufer, 2 topics per brand as DE and EN plans written by `claude -p` (Stefan's subscription login, no API key), voice (Gemini key in `.env`), render, checks, export (`docs/daily-runner.md`) | yes (`claude -p`; the run stops cleanly when the usage limit is reached) |

Rules baked into the scripts: free-space guard (no renders under 30 GB), `.env` is read by the Python code only,
nothing is published without state `APPROVED`, mock publisher stays in dry-run until Stefan changes `run_publish.ps1`.

Laptop requirements: awake and on mains at the task times (power plan "never sleep when plugged in"); the lid may be
closed only if the power settings keep the machine awake. Claude Desktop scheduled tasks are an alternative for the
Claude step, but run only while the app is open.
