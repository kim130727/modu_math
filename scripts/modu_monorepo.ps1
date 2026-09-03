param(
    [ValidateSet("python-test", "flutter-analyze", "flutter-test", "check")]
    [string]$Task = "check"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$MobileRoot = Join-Path $RepoRoot "apps/mobile"

function Ensure-MobileJunction {
    $target = Join-Path $RepoRoot "examples"
    $link = Join-Path $MobileRoot "examples"
    if (-not (Test-Path -LiteralPath $link)) {
        Write-Host "Creating junction: $link -> $target" -ForegroundColor Cyan
        New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    }
}

function Invoke-PythonTests {
    Push-Location $RepoRoot
    try {
        uv run pytest
    }
    finally {
        Pop-Location
    }
}

function Invoke-FlutterAnalyze {
    Ensure-MobileJunction
    Push-Location $MobileRoot
    try {
        flutter analyze
    }
    finally {
        Pop-Location
    }
}

function Invoke-FlutterTests {
    Ensure-MobileJunction
    Push-Location $MobileRoot
    try {
        flutter test
    }
    finally {
        Pop-Location
    }
}

switch ($Task) {
    "python-test" {
        Invoke-PythonTests
    }
    "flutter-analyze" {
        Invoke-FlutterAnalyze
    }
    "flutter-test" {
        Invoke-FlutterTests
    }
    "check" {
        Invoke-PythonTests
        Invoke-FlutterAnalyze
        Invoke-FlutterTests
    }
}
