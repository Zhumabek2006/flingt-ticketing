@echo off
echo Starting Flight Ticketing Project...
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo.
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "python start_frontend_server.py"
echo.
echo Project is now running!
echo - Backend: http://localhost:8000
echo - Frontend: index.html (opened in browser)
echo - API Docs: http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause >nul
