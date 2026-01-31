@echo off
REM Startup script for Windows development

echo Starting Mapey Application...
echo.

REM Start backend
echo Starting Backend API...
cd backend
call venv\Scripts\activate.bat
start "Mapey Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting Frontend...
cd ..\frontend
start "Mapey Frontend" cmd /k "npm run dev"

echo.
echo Backend running at http://localhost:8000
echo Frontend running at http://localhost:3000
echo.
echo Close the command windows to stop the services.
