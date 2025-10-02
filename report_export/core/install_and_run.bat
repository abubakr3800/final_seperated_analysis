@echo off
echo ========================================
echo PDF Report Extractor - Installation
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
echo Please make sure Python is installed first.
echo.

REM Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo Trying minimal requirements first...
py -m pip install -r requirements_minimal.txt

if %errorlevel% neq 0 (
    echo Minimal installation failed, trying full requirements...
    py -m pip install -r requirements.txt
)

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Step 2: Running the PDF extractor...
echo.

py pdf_report_extractor.py

if %errorlevel% neq 0 (
    echo ERROR: Failed to run the extractor
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Check the generated files:
echo - report_extracted.json
echo - pdf_extraction.log
echo ========================================
pause
