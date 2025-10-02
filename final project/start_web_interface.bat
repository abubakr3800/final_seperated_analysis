@echo off
echo Starting Web Interface Server...
echo ============================================

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Start the web server
echo Starting Web Interface on http://localhost:3000...
echo Press Ctrl+C to stop the server
echo ============================================
py web_server.py
