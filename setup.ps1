
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

function mb_all {
    param(
        [string]$Path,
        [switch]$NoRecurse,
        [switch]$StopOnError,
        [switch]$ListOnly
    )
    if (-not $Path) { Write-Host "Usage: mb_all <FolderPath or DslPath> [-NoRecurse] [-StopOnError] [-ListOnly]"; return }
    $args = @("-ExecutionPolicy", "Bypass", "-File", "$PSScriptRoot\scripts\build_dsl_folder.ps1", "-Path", $Path)
    if ($NoRecurse) { $args += "-NoRecurse" }
    if ($StopOnError) { $args += "-StopOnError" }
    if ($ListOnly) { $args += "-ListOnly" }
    powershell @args
}

Write-Host "ModuMath CLI helpers (mb, mw, mb_all) have been registered." -ForegroundColor Green
Write-Host "You can now use 'mb' to build once, 'mw' to watch, or 'mb_all' to build a folder." -ForegroundColor Gray
