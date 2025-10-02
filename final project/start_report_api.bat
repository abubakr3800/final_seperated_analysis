@echo off
echo Starting Report Extraction API (report_export)...
echo ================================================

REM Navigate to report_export directory
cd ..\report_export

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

REM Start the report extraction API
echo Starting Report Extraction API on http://localhost:5000...
echo Press Ctrl+C to stop the server
echo ================================================
py api/api_server.py
