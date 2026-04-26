@echo off
REM AI Healthcare Chatbot - Quick Start Script for Windows
REM Usage: start.cmd

setlocal enabledelayedexpansion

echo.
echo 🏥 AI Healthcare Chatbot Platform
echo ====================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found
    echo Install from: https://www.python.org
    pause
    exit /b 1
)
echo ✓ Python found

REM Check Node.js
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js not found
    echo Install from: https://nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js found

REM Setup Backend
echo [3/6] Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Edit .env with your API keys
)

echo Installing Python dependencies...
pip install -q -r requirements.txt

cd ..
echo ✓ Backend ready

REM Setup Frontend
echo [4/6] Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install -q
)

cd ..
echo ✓ Frontend ready

REM Display instructions
echo.
echo ✓ Setup Complete!
echo.
echo To start the platform:
echo.
echo Terminal 1 ^(Backend^):
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python -m uvicorn app.main:app --reload
echo.
echo Terminal 2 ^(Frontend^):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo ⚠️  Don't forget to:
echo   1. Add API keys to backend\.env
echo   2. Check MongoDB connection string
echo   3. Generate encryption key ^(see SETUP_GUIDE.md^)
echo.
echo 📚 Documentation: Check SETUP_GUIDE.md for detailed instructions
echo 🚀 Deploy guide: Check DEPLOYMENT.md for production deployment
echo.
pause
