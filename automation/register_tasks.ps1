# Registers the Windows scheduled tasks. Run as the user who owns the Claude login. Use -WhatIf first.
[CmdletBinding(SupportsShouldProcess = $true)]
param()
$root = Split-Path -Parent $PSScriptRoot
$ps = "powershell.exe"
$common = "-NoProfile -ExecutionPolicy Bypass -File"

$tasks = @(
    @{ Name = "FN Render Queue";     Script = "run_render.ps1";  Trigger = (New-ScheduledTaskTrigger -Daily -At 09:00) },
    @{ Name = "FN Costs and Status"; Script = "run_status.ps1";  Trigger = (New-ScheduledTaskTrigger -Daily -At 19:00) },
    @{ Name = "FN Publish Sync";     Script = "run_publish.ps1"; Trigger = (New-ScheduledTaskTrigger -Once -At 08:05 -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Hours 15)) }
    # Tagesläufer (docs\daily-runner.md): template only, not registered by default (Stefan, 03.11.2026). To register it,
    # remove the leading "#" of the next line. The model stage is `claude -p` in Stefan's subscription (no API key, `claude auth status` must
    # show the login); the voices need GEMINI_API_KEY in .env. About 2 topics x 8 brands x DE/EN: several hours of rendering; start it
    # before the render queue of the day.
    # ,@{ Name = "FN Daily Runner";     Script = "run_daily.ps1";   Trigger = (New-ScheduledTaskTrigger -Daily -At 06:30); Hours = 10 }
    # Month planner (docs\daily-runner.md section 6): template only. Rule: the 24th of every month at 19:30 Vienna time. A monthly trigger needs
    # more than New-ScheduledTaskTrigger offers in Windows PowerShell 5.1, so the task fires daily at 18:00 laptop time (before 19:30 Vienna in
    # summer and in winter) and run_month_plan.ps1 acts only on the 24th (Vienna date), waits until 19:30 Vienna time and then plans the next month.
    # ,@{ Name = "FN Month Plan";       Script = "run_month_plan.ps1"; Trigger = (New-ScheduledTaskTrigger -Daily -At 18:00); Hours = 3 }
)
foreach ($t in $tasks) {
    $action = New-ScheduledTaskAction -Execute $ps -Argument "$common `"$(Join-Path $root ('automation\' + $t.Script))`"" -WorkingDirectory $root
    $limit = 3
    if ($t.Hours) { $limit = $t.Hours }
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours $limit) -MultipleInstances IgnoreNew
    if ($PSCmdlet.ShouldProcess($t.Name, "Register-ScheduledTask")) {
        Register-ScheduledTask -TaskName $t.Name -Action $action -Trigger $t.Trigger -Settings $settings -Force | Out-Null
        Write-Host "registered $($t.Name)"
    }
}
Write-Host "Not registered on purpose: FN Topic Proposals (Claude step). Enable by hand after reviewing automation\run_claude_calendar.ps1."
