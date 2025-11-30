@echo off
echo ============================================================
echo Starting LuxSCale Service
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting API Server on port 8001...
start "LuxSCale API Server" cmd /k "py api_server.py"

echo.
echo Waiting for API server to start...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Web Server on port 3000...
start "LuxSCale Web Server" cmd /k "py -m http.server 3000"

echo.
echo ============================================================
echo Services Started!
echo ============================================================
echo.
echo API Server: http://localhost:8001
echo Web Interface: http://localhost:3000
echo.
echo Press any key to close this window (services will continue running)
pause >nul

