@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (echo Python 3.10 ou 3.11 est requis. & pause & exit /b 1)
if not exist .venv (py -3.11 -m venv .venv 2>nul || py -3.10 -m venv .venv)
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-local.txt
python -c "import torch" >nul 2>nul
if errorlevel 1 (
 echo.
 echo PyTorch n'est pas installe dans cet environnement.
 echo Ouvre une deuxieme fenetre CMD puis execute :
 echo cd /d "%~dp0"
 echo .venv\Scripts\activate
 echo Installe la version adaptee a ton PC depuis https://pytorch.org/get-started/locally/
 echo Puis relance start_windows.bat.
 pause
 exit /b 1
)
python local_engine.py
pause
