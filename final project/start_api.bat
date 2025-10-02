@echo off
echo Starting Lighting Compliance Checker API...
echo ============================================

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing requirements...
py -m pip install -r requirements.txt

REM Start the API server
echo Starting API server on http://localhost:8000...
echo Press Ctrl+C to stop the server
echo ============================================
py src/api_server.py
