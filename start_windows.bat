@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (echo Python 3.10 ou 3.11 est requis. & pause & exit /b 1)
if not exist .venv (py -3.11 -m venv .venv 2>nul || py -3.10 -m venv .venv)
call .venv\Scripts\activate
python -m pip install --upgrade pip
echo.
echo IMPORTANT : installe d'abord PyTorch adapte a ton GPU depuis https://pytorch.org/get-started/locally/
echo Pour CPU seulement, installe PyTorch CPU. Puis appuie sur une touche.
pause
python -m pip install -r requirements-local.txt
python local_engine.py
pause
