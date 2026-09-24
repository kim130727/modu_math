param(
    [ValidateSet("setup", "python-test", "flutter-analyze", "flutter-test", "check")]
    [string]$Task = "check"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$MobileRoot = Join-Path $RepoRoot "apps/mobile"

function Ensure-MobileJunction {
    # Keep the existing task entrypoints; compile disposable assets instead of
    # pointing Flutter at authored DSL/translation files.
    Push-Location $RepoRoot
    try {
        uv run python tools/export_problem_content.py
        if ($LASTEXITCODE -ne 0) { throw "Problem content export failed" }
    } finally { Pop-Location }
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
    "setup" {
        Ensure-MobileJunction
    }
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
