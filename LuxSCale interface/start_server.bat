@echo off
echo ============================================================
echo Starting LuxSCale API Server
echo ============================================================
echo.
echo Server will start on http://localhost:8001
echo.
echo Starting API server...
echo.

cd /d "%~dp0"
py api_server.py

pause

