@echo off
cd /d "%~dp0"   # Cambia al directorio donde está el archivo .bat (y app.py)
start python app.py  # Ejecuta el archivo app.py con Python
timeout /t 5  # Espera 5 segundos para permitir que Flask se inicie
start http://127.0.0.1:5000/  # Abre la URL de Flask en el navegador
