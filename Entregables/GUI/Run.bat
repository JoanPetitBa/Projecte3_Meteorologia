@echo off
rem Obtener la carpeta donde está ubicado el archivo .bat
cd /d "%~dp0"

rem Ejecutar el script Python
start python app.py

rem Abrir el navegador automáticamente en la dirección del servidor de Flask
start http://127.0.0.1:5000

