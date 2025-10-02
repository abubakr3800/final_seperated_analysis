@echo off
echo Organizing Final Project Structure...
echo =====================================

REM Create directories if they don't exist
if not exist "scripts" mkdir scripts
if not exist "tests" mkdir tests
if not exist "docs" mkdir docs
if not exist "temp" mkdir temp

echo.
echo Moving test files to tests directory...
move test_*.py tests\ 2>nul
move debug_*.py tests\ 2>nul
move simple_*.py tests\ 2>nul
move quick_test.py tests\ 2>nul
move full_analysis_test.py tests\ 2>nul

echo.
echo Moving utility scripts to scripts directory...
move process_reports_enhanced.py scripts\ 2>nul
move process_reports.bat scripts\ 2>nul
move demo.py scripts\ 2>nul
move minimal_api.py scripts\ 2>nul

echo.
echo Moving debug and result files to temp directory...
move debug_*.json temp\ 2>nul
move *_test_result.json temp\ 2>nul
move test_compliance_result.json temp\ 2>nul
move web_interface_test_result.json temp\ 2>nul

echo.
echo Moving documentation files to docs directory...
move README.md docs\ 2>nul

echo.
echo =====================================
echo ✅ Project organization complete!
echo.
echo 📁 Directory Structure:
echo    📂 src/           - Core application code
echo    📂 scripts/       - Utility scripts
echo    📂 tests/         - Test files
echo    📂 docs/          - Documentation
echo    📂 temp/          - Temporary files
echo    📂 data/          - Data files
echo.
echo 🚀 Main Files:
echo    📄 web_interface.html - Web interface
echo    📄 web_server.py      - Web server
echo    📄 *.bat              - Service management scripts
echo.
pause
