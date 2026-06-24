@echo off
setlocal
set arg1=%1

if "%arg1%"=="" (
    echo Usage: mb_all [FolderPath or DslPath] [extra powershell args]
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0scripts\build_dsl_folder.ps1" -Path "%arg1%" %2 %3 %4 %5 %6 %7 %8 %9
endlocal
