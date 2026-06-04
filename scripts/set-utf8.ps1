Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Console I/O encoding
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

# Windows code page to UTF-8
chcp 65001 > $null

# Python UTF-8 mode
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# PowerShell default text encoding (PowerShell 7+)
$PSDefaultParameterValues["Out-File:Encoding"] = "utf8"
$PSDefaultParameterValues["Set-Content:Encoding"] = "utf8"
$PSDefaultParameterValues["Add-Content:Encoding"] = "utf8"

Write-Host "[set-utf8] UTF-8 session configuration applied." -ForegroundColor Green
Write-Host "[set-utf8] code page: $(chcp)" -ForegroundColor DarkGray
Write-Host "[set-utf8] PYTHONUTF8=$env:PYTHONUTF8, PYTHONIOENCODING=$env:PYTHONIOENCODING" -ForegroundColor DarkGray
