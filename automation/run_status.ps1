# Daily status: states, queue, costs, free space -> logs\status_<date>.txt
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"
$py = Join-Path $root ".venv\Scripts\python.exe"
$out = Join-Path $root ("logs\status_" + (Get-Date -Format "yyyy-MM-dd") + ".txt")
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
"== $(Get-Date -Format s) ==" | Out-File -Encoding utf8 $out
& $py -m fn.cli status *>> $out
"-- costs --" | Out-File -Append -Encoding utf8 $out
& $py -m fn.cli costs *>> $out
