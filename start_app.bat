@echo off
title Fantasy11 Sports App
echo ===================================================
echo     FANTASY11 SPORTS WEB APPLICATION
echo ===================================================
echo Server starting on http://localhost:8000 ...
timeout /t 2 >nul
start "" "http://localhost:8000"
"%USERPROFILE%\.local\bin\uv.exe" run python server.py
pause
