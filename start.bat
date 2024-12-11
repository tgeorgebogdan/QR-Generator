@echo off
:: Enhanced Batch Script for QR Code Generator

:: Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python to continue.
    pause
    exit /b
)

:: Check if pip is installed
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade >nul 2>&1
    IF ERRORLEVEL 1 (
        echo Failed to install pip. Please install it manually and try again.
        pause
        exit /b
    )
)

:: Upgrade pip to the latest version
echo Upgrading pip to the latest version...
pip install --upgrade pip >nul 2>&1
IF ERRORLEVEL 1 (
    echo Failed to upgrade pip. Please check your internet connection or install manually.
    pause
    exit /b
)

:: Install required dependencies
echo Installing required dependencies...
pip install --upgrade qrcode[pil] svgwrite >nul 2>&1
IF ERRORLEVEL 1 (
    echo Failed to install dependencies. Please check your internet connection or install manually.
    pause
    exit /b
)

:: Check for script updates on GitHub
echo Checking for the latest version of the script on GitHub...
set SCRIPT_URL=https://raw.githubusercontent.com/your-username/your-repo/main/qr.py
set SCRIPT_NAME=qr.py
curl -s -o %SCRIPT_NAME% %SCRIPT_URL% >nul 2>&1
IF ERRORLEVEL 1 (
    echo Failed to download the latest script. Using the local version if available.
    IF NOT EXIST %SCRIPT_NAME% (
        echo Local script not found. Please download qr.py manually.
        pause
        exit /b
    )
) ELSE (
    echo Successfully downloaded the latest version of the script.
)

:: Run the Python script
:restart_script
echo Starting the QR code generator script...
python %SCRIPT_NAME%
IF ERRORLEVEL 1 (
    echo Failed to execute the Python script. Please check the script for errors.
    pause
    exit /b
)

:: Ask user to restart or exit
choice /M "Do you want to restart the script?" /C YN /N
IF ERRORLEVEL 2 (
    echo Exiting the script.
    pause
    exit /b
) ELSE (
    goto restart_script
)

:: Finish
echo QR code generator finished successfully.
pause
exit /b
