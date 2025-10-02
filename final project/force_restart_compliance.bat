@echo off
echo Force restarting Compliance API...
echo =====================================

echo.
echo 1. Stopping all Python processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo 2. Starting Compliance API with updated code...
start "Compliance API" cmd /k "cd /d %~dp0 && py src\api_server.py"

echo.
echo 3. Waiting for API to start...
timeout /t 5 /nobreak >nul

echo.
echo 4. Testing the API...
curl http://localhost:8000/health

echo.
echo =====================================
echo ✅ Compliance API restarted with updated code!
echo 🌐 Go to http://localhost:3000 and upload your PDF again
echo =====================================
pause
