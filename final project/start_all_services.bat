@echo off
echo ================================================
echo    Lighting Compliance Checker System
echo ================================================
echo.
echo Starting all services with organized structure...
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python and ensure 'py' command is available
    pause
    exit /b 1
)

echo ✅ Python found: 
py --version

echo.
echo 📦 Installing/updating requirements...
py -m pip install -r requirements.txt

echo.
echo 🛑 Stopping any running services...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Starting services in order...
echo.

echo 1️⃣ Starting Report API (port 5000)...
start "Report API" cmd /k "cd /d %~dp0..\report_export && py api\api_server.py"
timeout /t 5 /nobreak >nul

echo 2️⃣ Starting Compliance API (port 8000)...
start "Compliance API" cmd /k "cd /d %~dp0 && py src\api_server.py"
timeout /t 5 /nobreak >nul

echo 3️⃣ Starting Web Interface (port 3000)...
start "Web Interface" cmd /k "cd /d %~dp0 && py web_server.py"

echo.
echo ================================================
echo ✅ All services started successfully!
echo.
echo 🌐 Access Points:
echo    📱 Web Interface: http://localhost:3000 (or 3001)
echo    📖 API Documentation: http://localhost:8000/docs
echo    🔧 Report API: http://localhost:5000
echo.
echo 📁 Project Structure:
echo    📂 src/           - Core application code
echo    📂 scripts/       - Utility scripts  
echo    📂 tests/         - Test files
echo    📂 docs/          - Documentation
echo    📂 temp/          - Temporary files
echo.
echo 💡 Tips:
echo    - Upload PDF reports through the web interface
echo    - Check console windows for debug information
echo    - Use Ctrl+C in service windows to stop individual services
echo.
echo Press any key to exit this window...
pause >nul
