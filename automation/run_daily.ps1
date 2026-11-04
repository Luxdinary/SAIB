# Tagesläufer: daily production per brand with claude -p (Stefan's subscription) (scripts\daily_runner.py, docs\daily-runner.md).
# Template for the Windows task "FN Daily Runner" (register_tasks.ps1); Stefan registers it by hand.
# No publishing, no deletion, no Higgsfield booking. Keys are read from .env by the Python code only.
param(
    [string]$Brands = "all",          # comma-separated brand ids or "all" (enabled brands of config\daily.yaml)
    [int]$Topics = 0,                 # topics per brand; 0 = config default (2)
    [switch]$DryRun,                  # plans and checks only
    [string]$Provider = "",           # "" = config default (claude_cli, Stefan's subscription); "mock" = no model call, tests the task for free
    [string]$Date = "",               # production date yyyy-MM-dd (default: today)
    [int]$MaxFlash = 0,               # Flash voice requests per brand and day; 0 = config default
    [string]$StartAt = ""             # UTC time such as 2026-11-04T08:05:00Z: wait until then (compares clocks, so a sleep in between does no harm)
)
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$py = Join-Path $root ".venv\Scripts\python.exe"
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
$logDay = if ($Date) { $Date } else { Get-Date -Format "yyyy-MM-dd" }
$log = Join-Path $root ("logs\daily_" + $logDay + ".log")

# No idle sleep while this script runs (ES_CONTINUOUS + ES_SYSTEM_REQUIRED); ends with the process, changes no setting. A closed lid still sleeps.
try {
    Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
    [void][Win32.Power]::SetThreadExecutionState(2147483649)
} catch { }

if ($StartAt) {
    $target = [datetime]::Parse($StartAt, [Globalization.CultureInfo]::InvariantCulture, ([Globalization.DateTimeStyles]::AdjustToUniversal -bor [Globalization.DateTimeStyles]::AssumeUniversal))
    "$(Get-Date -Format s) waiting until $($target.ToString('s'))Z (UTC)" | Out-File -Append -Encoding utf8 $log
    while ([datetime]::UtcNow -lt $target) { Start-Sleep -Seconds 30 }
}

$free = (Get-PSDrive C).Free / 1GB
if ($free -lt 30) {
    "$(Get-Date -Format s) WARNING: only $([math]::Round($free,1)) GB free on C:, daily runner not started" | Out-File -Append -Encoding utf8 $log
    exit 2
}
if (Test-Path (Join-Path $root "data\render.pause")) {
    "$(Get-Date -Format s) data\render.pause exists: daily runner not started" | Out-File -Append -Encoding utf8 $log
    exit 3
}
$runnerArgs = @("scripts\daily_runner.py", "--brands", $Brands)
if ($Topics -gt 0) { $runnerArgs += @("--topics", "$Topics") }
if ($DryRun) { $runnerArgs += "--dry-run" }
if ($Date) { $runnerArgs += @("--date", $Date) }
if ($MaxFlash -gt 0) { $runnerArgs += @("--max-flash", "$MaxFlash") }
if ($Provider) { $runnerArgs += @("--provider", $Provider) }
if ($Provider -eq "mock") { $runnerArgs += "--no-mark" }
"$(Get-Date -Format s) start daily runner: $($runnerArgs -join ' ')" | Out-File -Append -Encoding utf8 $log
# The runner writes UTF-8. Plain "*>> $log" would store UTF-16 and mangle umlauts, so decode as UTF-8 and append as UTF-8.
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false) } catch { }
& $py @runnerArgs 2>&1 | ForEach-Object { "$_" } | Out-File -Append -Encoding utf8 $log
"$(Get-Date -Format s) daily runner exit $LASTEXITCODE" | Out-File -Append -Encoding utf8 $log
exit $LASTEXITCODE
