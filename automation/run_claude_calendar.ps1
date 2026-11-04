# Template for the Claude step (topic proposals). Uses Stefan's Claude Code login (Max plan); no API key.
# Not registered in Phase 1. Review the prompt in prompts\calendar_planner.md before enabling.
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$log = Join-Path $root ("logs\claude_calendar_" + (Get-Date -Format "yyyy-MM-dd") + ".log")
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
$brands = @("claude_workflows", "ai_security")
foreach ($b in $brands) {
    $prompt = "Read prompts/calendar_planner.md and fill the calendar for brand $b for the next 30 days. " +
              "Create the grid with 'python -m fn.cli calendar init $b' if it does not exist. Write nothing without a source."
    "$(Get-Date -Format s) claude -p for $b" | Out-File -Append -Encoding utf8 $log
    claude -p $prompt --allowedTools "Read,Write,Edit,Bash(python -m fn.cli *),WebFetch,WebSearch" *>> $log
}
