param(
    [string]$BackendApiBaseUrl = "http://127.0.0.1:8000",
    [ValidateRange(1, 65535)]
    [int]$WebPort = 3000,
    [ValidateSet("chrome", "edge")]
    [string]$Browser = "edge"
)

$ErrorActionPreference = "Stop"

Push-Location -LiteralPath $PSScriptRoot
try {
    $flutterArguments = @(
        "run",
        "-d", $Browser,
        "--web-port", $WebPort,
        "--dart-define=BACKEND_API_BASE_URL=$BackendApiBaseUrl"
    )

    if ($Browser -eq "chrome") {
        $chromeProfile = Join-Path $PSScriptRoot ".dart_tool\chrome_debug_profile"
        $flutterArguments += "--web-browser-flag=--user-data-dir=$chromeProfile"
    }

    & flutter @flutterArguments

    if ($LASTEXITCODE -ne 0) {
        throw "Flutter exited with code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
