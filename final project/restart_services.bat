@echo off
echo Restarting Lighting Compliance System...
echo ============================================

echo.
echo 1. Stopping any running services...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo 2. Starting Report API (port 5000)...
start "Report API" cmd /k "cd /d %~dp0..\report_export && py api\api_server.py"
timeout /t 5 /nobreak >nul

echo.
echo 3. Starting Compliance API (port 8000)...
start "Compliance API" cmd /k "cd /d %~dp0 && py src\api_server.py"
timeout /t 5 /nobreak >nul

echo.
echo 4. Starting Web Interface (port 3000)...
start "Web Interface" cmd /k "cd /d %~dp0 && py web_server.py"

echo.
echo ============================================
echo ✅ All services started!
echo.
echo 🌐 Access Points:
echo    📱 Web Interface: http://localhost:3000 (or 3001)
echo    📖 API Docs: http://localhost:8000/docs
echo    🔧 Report API: http://localhost:5000
echo.
echo Press any key to exit...
pause >nul
