@echo off
title SkillPath AI - Startup Launcher
echo =========================================================================
echo                  SKILLPATH AI - FULL STACK LAUNCHER                      
echo         AI-Powered Personalized Learning Platform (PromptWars X RTC)     
echo =========================================================================
echo.
echo Launching Backend (FastAPI on http://127.0.0.1:8000)...
start "SkillPath AI - Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo Waiting for backend initialization...
timeout /t 3 /nobreak > nul

echo Launching Frontend (Vite on http://localhost:5173)...
start "SkillPath AI - Frontend" cmd /k "cd /d %~dp0frontend && npm.cmd run dev"

echo.
echo =========================================================================
echo Application services initiated:
echo - Frontend Web UI : http://localhost:5173
echo - Backend API     : http://127.0.0.1:8000
echo - Swagger Docs    : http://127.0.0.1:8000/docs
echo - Demo Account    : demo@skillpath.ai / password123 (or 1-Click Demo Mode)
echo =========================================================================
echo.
pause
