@echo off
title Eklavya Setu - One-Click Launcher
echo ======================================================================
echo    Launching Eklavya Setu (एकलव्य सेतु) Prototype
echo    Ministry of Tribal Affairs (MoTA) • SIH26238
echo ======================================================================
echo.

cd /d "%~dp0"

:: Check if python is available in system PATH
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [NOTICE] Python was not found in system PATH.
    echo Launching autonomous frontend directly in your default browser...
    echo.
    start "" "%~dp0frontend\index.html"
    echo ======================================================================
    echo  Eklavya Setu Prototype is ACTIVE!
    echo  - 5-Scheme Dashboard, JAGO Multilingual Voice AI, DigiLocker Wallet,
    echo    Single-Avail De-duplication Guard, and Zero-Dropout Radar are LIVE!
    echo ======================================================================
    echo.
    pause
    exit /b 0
)

echo [1/2] Starting FastAPI Backend on port 8000...
start "Eklavya Setu Backend (FastAPI)" cmd /k "python -m uvicorn backend.main:app --port 8000 --reload"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo [2/2] Opening Eklavya Setu in your default browser...
start http://localhost:8000

echo.
echo ======================================================================
echo  Eklavya Setu Prototype is ACTIVE!
echo  - Frontend Web App: http://localhost:8000
echo  - Backend REST API: http://localhost:8000/docs
echo  To stop the backend, run: stop.bat
echo ======================================================================
echo.
pause
