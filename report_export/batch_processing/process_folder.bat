@echo off
echo ========================================
echo PDF Folder Processor
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

echo Python found! Processing PDF files...
echo.

REM Get input folder (default to current directory)
if "%1"=="" (
    set INPUT_FOLDER=.
    echo Using current directory as input folder
) else (
    set INPUT_FOLDER=%1
    echo Using input folder: %INPUT_FOLDER%
)

REM Get output folder (default to "output")
if "%2"=="" (
    set OUTPUT_FOLDER=output
    echo Using output folder: %OUTPUT_FOLDER%
) else (
    set OUTPUT_FOLDER=%2
    echo Using output folder: %OUTPUT_FOLDER%
)

echo.
echo Starting batch processing...
echo.

REM Run the Python script
py process_folder.py "%INPUT_FOLDER%" "%OUTPUT_FOLDER%"

if %errorlevel% neq 0 (
    echo ERROR: Batch processing failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo BATCH PROCESSING COMPLETED SUCCESSFULLY
echo ========================================
echo Check the %OUTPUT_FOLDER% folder for results
echo.
pause
