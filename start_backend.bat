@echo off
title SkillPath AI - Backend Server
echo ========================================================
echo Starting SkillPath AI Backend Server (FastAPI + SQLite)...
echo ========================================================
cd /d %~dp0backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
