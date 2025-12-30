@echo off
echo ===============================================
echo   PNG to JPEG Converter
echo   Application Launcher
echo ===============================================
echo.
echo This batch file:
echo    - Launches the application immediately
echo    - Requires Python environment
echo    - For daily use
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10 or higher.
    echo Download Python: https://python.org
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo ✓ Dependencies check complete
echo.

REM Run tests
echo Running tests...
python test_app.py
if errorlevel 1 (
    echo ERROR: Tests failed. Please check dependencies.
    pause
    exit /b 1
)

echo.
echo Starting application...
echo.

REM Launch main application
python main.py

echo.
echo Application closed successfully.
echo.
echo Next time, just double-click this batch file!
pause