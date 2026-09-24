param(
    [string]$BackendApiBaseUrl = "http://127.0.0.1:8000",
    [ValidateRange(1, 65535)]
    [int]$WebPort = 3000,
    [ValidateSet("edge", "chrome", "none")]
    [string]$Browser = "none"
)

$ErrorActionPreference = "Stop"

function Find-BrowserExecutable([string]$Name) {
    $candidates = switch ($Name) {
        "edge" {
            @(
                "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            )
        }
        "chrome" {
            @(
                "C:\Program Files\Google\Chrome\Application\chrome.exe",
                "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            )
        }
    }

    return $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}

$browserJob = $null
$appUrl = "http://127.0.0.1:$WebPort"

Push-Location -LiteralPath $PSScriptRoot
try {
    if ($Browser -ne "none") {
        $browserExecutable = Find-BrowserExecutable $Browser
        if (-not $browserExecutable) {
            throw "Could not find the $Browser browser executable."
        }

        $browserJob = Start-Job -ScriptBlock {
            param($Url, $Executable)

            $deadline = (Get-Date).AddMinutes(3)
            while ((Get-Date) -lt $deadline) {
                try {
                    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
                    if ($response.StatusCode -ge 200) {
                        Start-Process -FilePath $Executable -ArgumentList $Url
                        return
                    }
                }
                catch {
                    Start-Sleep -Milliseconds 500
                }
            }

            throw "Flutter web server did not become ready at $Url."
        } -ArgumentList $appUrl, $browserExecutable
    }

    Write-Host "Starting Flutter web server at $appUrl"
    if ($Browser -eq "none") {
        Write-Host "Open $appUrl in one browser tab, or refresh an existing tab."
    }
    else {
        Write-Host "The $Browser browser will be opened once after the server is ready."
    }

    & flutter run `
        -d web-server `
        --release `
        --web-hostname 127.0.0.1 `
        --web-port $WebPort `
        "--dart-define=BACKEND_API_BASE_URL=$BackendApiBaseUrl"
}
finally {
    if ($browserJob) {
        Stop-Job -Job $browserJob -ErrorAction SilentlyContinue
        Remove-Job -Job $browserJob -Force -ErrorAction SilentlyContinue
    }
    Pop-Location
}
