@echo off
title Stop Eklavya Setu Services
echo ======================================================================
echo    Stopping Eklavya Setu Services...
echo ======================================================================
echo.

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a 2>nul
)

echo Services stopped.
timeout /t 2 >nul
exit
