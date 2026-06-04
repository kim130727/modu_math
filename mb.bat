@echo off
setlocal
set arg1=%1

if "%arg1%"=="" (
    echo Usage: mb [ProblemId or DslPath]
    exit /b 1
)

if exist "%arg1%" (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\watch_build.ps1" -DslPath "%arg1%" -Once %2 %3 %4 %5
) else (
    powershell -ExecutionPolicy Bypass -File "%~dp0scripts\watch_build.ps1" -ProblemId "%arg1%" -Once %2 %3 %4 %5
)
endlocal
