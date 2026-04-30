
function mb {
    param($ProblemId)
    if (-not $ProblemId) { Write-Host "Usage: mb <ProblemId or Path>"; return }
    if (Test-Path $ProblemId) {
        powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\scripts\watch_build.ps1" -DslPath $ProblemId -Once
    } else {
        powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\scripts\watch_build.ps1" -ProblemId $ProblemId -Once
    }
}

function mw {
    param($ProblemId)
    if (-not $ProblemId) { Write-Host "Usage: mw <ProblemId or Path>"; return }
    if (Test-Path $ProblemId) {
        powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\scripts\watch_build.ps1" -DslPath $ProblemId
    } else {
        powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\scripts\watch_build.ps1" -ProblemId $ProblemId
    }
}

Write-Host "ModuMath CLI helpers (mb, mw) have been registered." -ForegroundColor Green
Write-Host "You can now use 'mb' to build once, or 'mw' to watch for changes." -ForegroundColor Gray
