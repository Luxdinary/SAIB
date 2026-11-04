# Month planner: plans the following month for every brand (scripts\month_planner.py, docs\daily-runner.md section 6).
# Template for the Windows task "FN Month Plan" (register_tasks.ps1); Stefan registers it by hand.
# Rule of the Hauptsitzung: runs on the 24th of every month at 19:30 Vienna time. The task fires every day at 18:00 laptop time
# (earlier than 19:30 Vienna in summer and in winter); this script acts only when the Vienna date is the 24th, waits until
# 19:30 Vienna time and then plans the next month. No publishing, no deletion, no Higgsfield booking.
# Model calls only for topic proposals (claude -p, Sonnet, effort low, Stefan's subscription), only for brands with open slots.
param(
    [string]$Month = "",          # yyyy-MM to plan (default: the month after today, Vienna time)
    [switch]$Force,               # run now: ignore the day of the month and the wait
    [switch]$NoPropose,           # no topic proposals for brands with open slots
    [switch]$DryRun               # numbers only, write nothing
)
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$py = Join-Path $root ".venv\Scripts\python.exe"
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
$vienna = [TimeZoneInfo]::FindSystemTimeZoneById("W. Europe Standard Time")
$nowV = [TimeZoneInfo]::ConvertTimeFromUtc([datetime]::UtcNow, $vienna)
$log = Join-Path $root ("logs\month_plan_" + $nowV.ToString("yyyy-MM-dd") + ".log")

if (-not $Force) {
    if ($nowV.Day -ne 24) { exit 0 }                       # the daily trigger does nothing on the other days
    $targetLocal = [datetime]::new($nowV.Year, $nowV.Month, 24, 19, 30, 0, [DateTimeKind]::Unspecified)
    $target = [TimeZoneInfo]::ConvertTimeToUtc($targetLocal, $vienna)
    "$(Get-Date -Format s) waiting until 19:30 Vienna time ($($target.ToString('s'))Z UTC)" | Out-File -Append -Encoding utf8 $log
    try {
        Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
        [void][Win32.Power]::SetThreadExecutionState(2147483649)      # no idle sleep while this script runs
    } catch { }
    while ([datetime]::UtcNow -lt $target) { Start-Sleep -Seconds 30 }
}

$runnerArgs = @("scripts\month_planner.py", "--brands", "all")
if ($Month) { $runnerArgs += @("--month", $Month) }
if (-not $NoPropose) { $runnerArgs += "--propose" }
if ($DryRun) { $runnerArgs += "--dry-run" }
"$(Get-Date -Format s) start month planner: $($runnerArgs -join ' ')" | Out-File -Append -Encoding utf8 $log
# The planner writes UTF-8: decode as UTF-8 and append as UTF-8 (plain "*>> $log" would store UTF-16 and mangle umlauts).
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false) } catch { }
& $py @runnerArgs 2>&1 | ForEach-Object { "$_" } | Out-File -Append -Encoding utf8 $log
"$(Get-Date -Format s) month planner exit $LASTEXITCODE" | Out-File -Append -Encoding utf8 $log
exit $LASTEXITCODE
