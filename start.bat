@echo off
echo ===================================
echo Starting Interview Agent Full Stack
echo ===================================
echo.

echo Starting Backend (FastAPI)...
start cmd /k "cd backend && python run.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend (Next.js)...
start cmd /k "cd frontend && npm run dev"

echo.
echo ===================================
echo Servers starting in separate windows!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Visit http://localhost:3000 to start
echo ===================================
pause
