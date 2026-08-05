param(
    [ValidateSet("python-test", "flutter-analyze", "flutter-test", "check")]
    [string]$Task = "check"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$MobileRoot = Join-Path $RepoRoot "apps/mobile"

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
    Push-Location $MobileRoot
    try {
        flutter analyze
    }
    finally {
        Pop-Location
    }
}

function Invoke-FlutterTests {
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
