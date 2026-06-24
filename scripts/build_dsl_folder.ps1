param(
    [Parameter(Mandatory = $true)]
    [string]$Path,
    [switch]$NoRecurse,
    [switch]$StopOnError,
    [switch]$ListOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$WatchScript = Join-Path $RepoRoot "scripts\watch_build.ps1"

if (-not (Test-Path -LiteralPath $WatchScript)) {
    throw "watch_build.ps1 not found: $WatchScript"
}

if (-not (Test-Path -LiteralPath $Path)) {
    throw "Path not found: $Path"
}

$Target = (Resolve-Path -LiteralPath $Path).Path
$Item = Get-Item -LiteralPath $Target

if ($Item.PSIsContainer) {
    $SearchOption = if ($NoRecurse) { "TopDirectoryOnly" } else { "AllDirectories" }
    $DslFiles = [System.IO.Directory]::EnumerateFiles($Target, "*.dsl.py", $SearchOption) |
        Sort-Object |
        ForEach-Object { Get-Item -LiteralPath $_ }
} elseif ($Item.Name.EndsWith(".dsl.py")) {
    $DslFiles = @($Item)
} else {
    throw "Target must be a directory or a *.dsl.py file: $Target"
}

if ($DslFiles.Count -eq 0) {
    throw "No *.dsl.py files found: $Target"
}

Write-Host "[mb_all] target: $Target" -ForegroundColor Cyan
Write-Host "[mb_all] dsl count: $($DslFiles.Count)" -ForegroundColor Cyan

if ($ListOnly) {
    foreach ($Dsl in $DslFiles) {
        Write-Host $Dsl.FullName
    }
    exit 0
}

$Ok = 0
$Fail = 0
$Failed = New-Object System.Collections.Generic.List[string]
$StartedAt = Get-Date

for ($i = 0; $i -lt $DslFiles.Count; $i += 1) {
    $Dsl = $DslFiles[$i]
    $Index = $i + 1
    Write-Host "[mb_all] [$Index/$($DslFiles.Count)] $($Dsl.Name)" -ForegroundColor Gray

    & powershell -ExecutionPolicy Bypass -File $WatchScript -DslPath $Dsl.FullName -Once
    if ($LASTEXITCODE -eq 0) {
        $Ok += 1
    } else {
        $Fail += 1
        $Failed.Add($Dsl.FullName)
        Write-Host "[mb_all] failed: $($Dsl.FullName)" -ForegroundColor Red
        if ($StopOnError) {
            break
        }
    }
}

$Elapsed = (Get-Date) - $StartedAt
Write-Host "[mb_all] done. ok=$Ok fail=$Fail elapsed=$([Math]::Round($Elapsed.TotalSeconds, 1))s" -ForegroundColor Green

if ($Failed.Count -gt 0) {
    Write-Host "[mb_all] failed files:" -ForegroundColor Red
    foreach ($FailedPath in $Failed) {
        Write-Host "  $FailedPath" -ForegroundColor Red
    }
    exit 1
}

exit 0
