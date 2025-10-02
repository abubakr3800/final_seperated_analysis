@echo off
echo ================================================
echo    Cleaning Up Project Files
echo ================================================
echo.

echo 🧹 Cleaning temporary files...
if exist "temp\*.json" (
    del /q "temp\*.json"
    echo ✅ Removed temporary JSON files
)

if exist "temp\*.log" (
    del /q "temp\*.log"
    echo ✅ Removed log files
)

echo.
echo 🗂️ Cleaning Python cache...
if exist "src\__pycache__" (
    rmdir /s /q "src\__pycache__"
    echo ✅ Removed src cache
)

if exist "tests\__pycache__" (
    rmdir /s /q "tests\__pycache__"
    echo ✅ Removed tests cache
)

if exist "scripts\__pycache__" (
    rmdir /s /q "scripts\__pycache__"
    echo ✅ Removed scripts cache
)

echo.
echo 🔄 Stopping all Python services...
taskkill /f /im python.exe >nul 2>&1
echo ✅ All Python processes stopped

echo.
echo ================================================
echo ✅ Cleanup complete!
echo.
echo 📁 Cleaned directories:
echo    📂 temp/          - Temporary files
echo    📂 */__pycache__  - Python cache files
echo.
echo 🚀 Ready to start fresh with:
echo    start_all_services.bat
echo.
pause
