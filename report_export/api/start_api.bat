@echo off
echo ========================================
echo PDF Report Extraction API Server
echo ========================================
echo.

REM Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found! Starting API server...
echo.

REM Install Flask if not already installed
echo Checking dependencies...
py -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Flask...
    py -m pip install Flask requests
)

echo.
echo Starting API server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo API Endpoints:
echo   GET  /           - API documentation
echo   GET  /health     - Health check
echo   POST /extract    - Upload PDF and extract data
echo   GET  /files      - List processed files
echo   GET  /download/<file_id> - Download extracted JSON
echo.
echo Web Interface: http://localhost:5000
echo ========================================
echo.

REM Start the API server
py api_server.py

pause
