param(
    [switch]$Watch,
    [string]$RawDir = "examples/problems/260427/raw"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RawPath = (Resolve-Path (Join-Path $RepoRoot $RawDir)).Path
$WatchScript = Join-Path $RepoRoot "scripts\watch_build.ps1"

if (-not (Test-Path -LiteralPath $WatchScript)) {
    throw "watch_build.ps1 not found: $WatchScript"
}

$dslFiles = Get-ChildItem -Path $RawPath -Filter "*.dsl.py" | Sort-Object Name
if ($dslFiles.Count -eq 0) {
    throw "No .dsl.py files found in: $RawPath"
}

Write-Host "[mw_raw_all] raw dir: $RawPath" -ForegroundColor Cyan
Write-Host "[mw_raw_all] dsl count: $($dslFiles.Count)" -ForegroundColor Cyan

if ($Watch) {
    Write-Host "[mw_raw_all] Starting one watcher process per DSL..." -ForegroundColor Yellow
    foreach ($dsl in $dslFiles) {
        $args = @(
            "-ExecutionPolicy", "Bypass",
            "-File", $WatchScript,
            "-DslPath", $dsl.FullName
        )
        Start-Process -FilePath "powershell" -ArgumentList $args -WindowStyle Hidden | Out-Null
        Write-Host "  started: $($dsl.Name)"
    }
    Write-Host "[mw_raw_all] Watchers started. Stop them with Task Manager or:" -ForegroundColor Green
    Write-Host "  Get-CimInstance Win32_Process | ? { `$_.CommandLine -like '*watch_build.ps1*260427\\raw*' } | % { Stop-Process -Id `$_.ProcessId }"
    exit 0
}

# Default: build once for all files (quick SVG regeneration check)
$ok = 0
$fail = 0
foreach ($dsl in $dslFiles) {
    Write-Host "[mw_raw_all] build once: $($dsl.Name)" -ForegroundColor Gray
    & powershell -ExecutionPolicy Bypass -File $WatchScript -DslPath $dsl.FullName -Once
    if ($LASTEXITCODE -eq 0) {
        $ok += 1
    } else {
        $fail += 1
    }
}

Write-Host "[mw_raw_all] done. ok=$ok fail=$fail" -ForegroundColor Green
Write-Host "[mw_raw_all] svg files:"
Get-ChildItem -Path $RawPath -Filter "*.svg" | Sort-Object Name | Select-Object -ExpandProperty FullName
