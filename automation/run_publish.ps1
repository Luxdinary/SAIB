# Hourly publish sync. Phase 1: mock publisher, dry run only. Phase 2: Stefan changes $publisher and removes --dry-run.
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"
$py = Join-Path $root ".venv\Scripts\python.exe"
$log = Join-Path $root ("logs\publish_" + (Get-Date -Format "yyyy-MM-dd") + ".log")
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
$publisher = "mock"
"$(Get-Date -Format s) publish sync ($publisher, dry-run)" | Out-File -Append -Encoding utf8 $log
& $py -m fn.cli publish --publisher $publisher --dry-run *>> $log
