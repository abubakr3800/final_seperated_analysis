@echo off
echo Processing Reports with Enhanced Layout Extractor
echo ================================================
echo.

REM Check if input folder exists
if not exist "..\input_pdfs" (
    echo Creating input_pdfs folder...
    mkdir "..\input_pdfs"
    echo.
    echo Please add your PDF files to the input_pdfs folder and run this script again.
    echo.
    pause
    exit /b
)

REM Run the processing script
py process_reports_enhanced.py

echo.
echo Processing completed!
echo.
pause
