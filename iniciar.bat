@echo off
title Iniciando Stelarys
echo Instalando dependencias...
pip install -r instaladores\requirements.txt

echo.
echo Iniciando la aplicación...
python main.py

pause
