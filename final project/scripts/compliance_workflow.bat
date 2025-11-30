@echo off
REM Compliance Workflow Batch File
REM Usage: compliance_workflow.bat <pdf_file> [output_file]

if "%1"=="" (
    echo Usage: compliance_workflow.bat ^<pdf_file^> [output_file]
    echo.
    echo Example:
    echo   compliance_workflow.bat report.pdf
    echo   compliance_workflow.bat report.pdf my_compliance.json
    exit /b 1
)

set PDF_FILE=%1
set OUTPUT_FILE=%2

if "%OUTPUT_FILE%"=="" (
    py scripts\compliance_workflow.py "%PDF_FILE%"
) else (
    py scripts\compliance_workflow.py "%PDF_FILE%" --output "%OUTPUT_FILE%"
)

pause

