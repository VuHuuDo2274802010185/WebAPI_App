@echo off
REM Setup script for WebAPI_App (Windows)
REM This script automates the environment setup process

echo.
echo 🚀 WebAPI_App Setup Script (Windows)
echo ==================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version 2>nul
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    exit /b 1
)
echo   Python found ✓
echo.

REM Check if uv is installed
echo ✓ Checking for uv package manager...
uv --version 2>nul
if errorlevel 1 (
    echo   uv not found. Installing uv...
    pip install uv
    if errorlevel 1 (
        echo ❌ Error: Failed to install uv
        exit /b 1
    )
    echo   uv installed successfully ✓
) else (
    echo   uv found ✓
)
echo.

REM Create virtual environment
echo ✓ Creating virtual environment...
if exist ".venv" (
    echo   Virtual environment already exists. Skipping...
) else (
    uv venv
    if errorlevel 1 (
        echo ❌ Error: Failed to create virtual environment
        exit /b 1
    )
    echo   Virtual environment created ✓
)
echo.

REM Install dependencies
echo ✓ Installing dependencies...
call .venv\Scripts\activate.bat
uv pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error: Failed to install dependencies
    exit /b 1
)
echo   Dependencies installed ✓
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ✓ Creating .env file from template...
    copy .env.example .env
    echo   .env file created ✓
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your actual API credentials!
) else (
    echo ✓ .env file already exists
)
echo.

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your Base.vn API credentials
echo 2. Activate virtual environment: .venv\Scripts\activate.bat
echo 3. Run the app: streamlit run app.py
echo.
pause
