@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo KazNLP demo
python run_demo.py
if errorlevel 1 pause
