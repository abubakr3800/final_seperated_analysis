@echo off
echo ============================================================
echo Starting Web Compliance API Server
echo ============================================================
echo.
echo Make sure the Report API is running on port 5000
echo.
echo Starting Compliance API on port 8000...
echo.

cd /d "%~dp0"
py api_server.py

pause

