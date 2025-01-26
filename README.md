Predicción del Clima - Proyecto 3
============================================
Este proyecto tiene como objetivo predecir con precisión el tipo de clima que se espera, basándose en los valores proporcionados por el usuario. Para ello, se realizó un análisis exhaustivo de los datos, asegurando una imputación adecuada de los valores nulos sin alterar la estructura de la información. Además, se entrenaron diversos modelos de predicción, optándose finalmente por el algoritmo XGBoost debido a su alto rendimiento y su capacidad para diferenciar claramente entre las distintas clases.

La estructura de la documentación del proyecto se basa en la metodología CRISP-DM, lo que garantiza un entendimiento claro y ordenado del proceso realizado.

# Tabla de Contenidos
1. Características principales
2. Requisitos
3. Instalación
4. Uso
5. Resultados
6. Estructura del Proyecto
7. Funciones Principales

## Características principales:

- Observación y exploración de los datos.
- Análisis y limpieza de los datos.
- Imputación de valores nulos.
- Entrenamiento de los modelos de predicción.

## Requisitos
El proyecto requiere las siguientes dependencias:

- **flask**: Para desarrollar y ejecutar aplicaciones web.
- **numpy**: Para cálculos numéricos y manipulación de matrices.
- **joblib**: Para guardar y cargar modelos entrenados y realizar tareas de paralelización.

## Instalación
**1. Clona el repositorio**
```bash
git clone https://github.com/JoanPetitBa/Projecte3_Meteorologia.git
cd Projecte3_Meteorologia/main
```
**2. Instala las dependencias**
```bash
pip install -r requirements.txt
```

# Uso
1. ONLINE
Ingresar a la pagina web [http://weatherprediction.mooo.com:8080](http://weatherprediction.mooo.com:8080)

2. OFFLINE
Para ejecutar el sistema de predicción climática, solo es necesario ejecutar el archivo Run.bat ubicado en la raíz principal del proyecto. Este archivo instalará automáticamente las dependencias necesarias (si aún no están instaladas) y ejecutará el archivo app.py, abriendo automáticamente el navegador con la página correspondiente.

```batch
@echo off

REM ========= IMPORTAR LAS IBRERIAS =========
python -m pip install -r requirements.txt || (
    echo Ocurrió un error al instalar las dependencias.
    pause
    exit /b
)

echo Dependencias instaladas correctamente.
REM ============================================

rem Obtener la carpeta donde está ubicado el archivo .bat
cd /d "%~dp0"

rem Ejecutar el script Python
start python app.py

rem Abrir el navegador automáticamente en la dirección del servidor de Flask
start http://127.0.0.1:5000

```

## Resultados
Los resultados se visualizan directamente en la misma página web, donde la interfaz se actualiza visualmente en función del clima predicho.

## Estructura del Proyecto
```plaintext
├───main
│   │   functions.py
│   │   app.py
│   │   Run.bat
│   │   requeriments.txt
│   │
│   ├───static
│   │   ├───icons
│   │   │       cloudy.png
│   │   │       fog.png
│   │   │       humidity.png
│   │   │       lupa.png
│   │   │       pressure.png
│   │   │       rain.png
│   │   │       rain_drop.png
│   │   │       storm.png
│   │   │       sun.png
│   │   │       wind.png
│   │   │
│   │   └───styles
│   │           styles.css
│   │
│   ├───templates
│   │       index.html
│   │
│   ├───__pycache__
│   │       functions.cpython-310.pyc
│   │
│   └───Modelos
│           SVM_weather_id.pkl
│           RFC_weather_id.zip
│           RNN_weather_id.h5
│           XGB_weather_id.pkl
│
└───data exploration
    │   observar_datos.ipynb
    │   models.ipynb
    │
    └───data
            cloudiness.csv
            dates.csv
            observations.csv
            seasons.csv
            weather.csv
            observations_full.csv
```
