@echo off
title SkillPath AI - Frontend Server
echo ========================================================
echo Starting SkillPath AI Frontend Server (React + Vite)...
echo ========================================================
cd /d %~dp0frontend
cmd.exe /c "npm.cmd run dev"
pause
