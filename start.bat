@echo off
title Space Defender - Game Server
cd /d "%~dp0"

echo ===================================================
echo        LAUNCHING SPACE DEFENDER GAME SERVER
echo ===================================================
echo.

set PYTHON_EXE=python

:: Check if standard 'python' command is available
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    goto :RunServer
)

:: Check if 'py' launcher is available
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_EXE=py
    goto :RunServer
)

:: Check AppData Python 3.14 installation
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set PYTHON_EXE="%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    goto :RunServer
)

:: Check generic LocalAppData Python
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_EXE="%%i\python.exe"
        goto :RunServer
    )
)

echo [ERROR] Python was not detected on this system.
echo You can still play the game directly by double-clicking 'index.html'!
echo.
pause
exit /b 1

:RunServer
echo Starting local HTTP server at http://localhost:8000 ...
echo Opening your default browser...
echo.

start "" "http://localhost:8000"

%PYTHON_EXE% server.py
pause
