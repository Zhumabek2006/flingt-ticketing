@echo off
echo Starting Flight Ticketing Backend Server...
cd /d "%~dp0"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
pause
