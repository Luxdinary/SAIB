# Produce every script in data\scripts that has no video folder yet. No publishing.
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"
$py = Join-Path $root ".venv\Scripts\python.exe"
$log = Join-Path $root ("logs\render_" + (Get-Date -Format "yyyy-MM-dd") + ".log")
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null

& $py -m fn.cli status *>> $log
$free = (Get-PSDrive C).Free / 1GB
if ($free -lt 30) {
    "$(Get-Date -Format s) WARNING: only $([math]::Round($free,1)) GB free on C:, no renders started" | Out-File -Append -Encoding utf8 $log
    exit 2
}
Get-ChildItem (Join-Path $root "data\scripts\*.md") | ForEach-Object {
    $vid = $_.BaseName
    $exists = @("drafts", "approved", "published", "failed") | ForEach-Object { Test-Path (Join-Path $root "storage\$_\$vid\video.mp4") }
    if ($exists -contains $true) { return }
    "$(Get-Date -Format s) produce $vid" | Out-File -Append -Encoding utf8 $log
    & $py -m fn.cli produce $_.FullName --quality looks *>> $log
}
