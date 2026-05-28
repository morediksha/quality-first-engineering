@echo off
REM Quick Start Setup Script for Jenkins Pipeline with Playwright (Windows)

setlocal enabledelayedexpansion

echo ======================================
echo Jenkins Pipeline - Quick Start Setup
echo ======================================
echo.

REM Step 1: Check Python
echo [Step 1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.7+
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Step 2: Create virtual environment
echo [Step 2] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Step 3: Activate virtual environment
echo [Step 3] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Step 4: Install dependencies
echo [Step 4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Step 5: Install Playwright browsers
echo [Step 5] Installing Playwright browsers...
playwright install chromium
echo [OK] Playwright browsers installed
echo.

REM Step 6: Verify test discovery
echo [Step 6] Verifying test discovery...
pytest tests --collect-only -q
echo [OK] Test discovery complete
echo.

REM Step 7: Check squad_urls.txt
echo [Step 7] Checking squad URLs file...
if not exist squad_urls.txt (
    echo squad_urls.txt not found. Creating template...
    (
        echo # Squad Account URLs for Testing
        echo # Add your newly created account URLs here, one per line
        echo # Example format: https://squad-dev.example.com/account/12345
    ) > squad_urls.txt
    echo [OK] Template created
    echo [WARNING] Please update squad_urls.txt with your account URLs
) else (
    echo [OK] squad_urls.txt found
)
echo.

REM Step 8: Summary
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo [INFO] Next steps:
echo 1. Update squad_urls.txt with your account URLs
echo 2. Run smoke tests locally: pytest tests\smoke -v
echo 3. Run regression tests locally: pytest tests\regression -v
echo 4. Run all tests: pytest tests -v
echo 5. Generate Allure report: allure generate allure-results -o allure-reports
echo 6. View report: allure open allure-reports
echo.
echo [INFO] To run Jenkins pipeline:
echo 1. Set up Jenkins job with Jenkinsfile
echo 2. Build with parameters (BRANCH, TESTS_PATH, SQUAD_URL_FILE)
echo.
echo [INFO] Virtual environment is active. To deactivate: deactivate
echo.
