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
 echo PyTorch absent : installation de la version CPU de secours...
 echo Pour activer ensuite un GPU NVIDIA, installe la version CUDA depuis https://pytorch.org/get-started/locally/
 python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
 if errorlevel 1 (
  echo Echec de l'installation automatique de PyTorch.
  pause
  exit /b 1
 )
)
python -m py_compile local_engine.py
if errorlevel 1 (
 echo.
 echo Erreur de syntaxe Python dans local_engine.py. Copie le message ci-dessus.
 pause
 exit /b 1
)
python local_engine.py
pause
