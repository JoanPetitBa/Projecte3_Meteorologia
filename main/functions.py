import joblib,os
from datetime import datetime
import numpy as np

def get_season(month: int) -> int:
    """
    Determina la estación del año basada en el mes.
    Devuelve un identificador numérico para la estación.
    """
    if month in [12, 1, 2]:
        return 1  # Invierno
    elif month in [3, 4, 5]:
        return 2  # Primavera
    elif month in [6, 7, 8]:
        return 3  # Verano
    elif month in [9, 10, 11]:
        return 4  # Otoño
    return 0

def get_weather(date: str, precipitation: float, wind: float, humidity: int) -> tuple[bool, str]:
    """
    Predice el identificador del clima basado en las características y el modelo.
    """

    weather_dict = {
        1:'storm',
        2:'rain',
        3:'cloudy',
        4:'fog',
        5:'sun',
    }

    try:
        # CONVERTIR LA FECHA EN TIPO 'datetime'
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day

    except ValueError:
        return False, "Formato de fecha inválido. Debe ser 'YYYY-MM-DD'."

    # OBTENER LA ESTACION DE LA FECHA ENTRADA
    estacion_id = get_season(month)

    # CARGAR EL MODELO DE XGBOOSTING
    model_path = fr".\main\Modelos\XGB_weather_id.pkl"
    try:
        loaded_model = joblib.load(model_path)
    except FileNotFoundError:
        return False, f"No se pudo encontrar el modelo en la ruta {model_path}. PATH ACTUAL: {os.getcwd()}"

    # FORMAR UNA ARRAY PARA PASAR LOS VALORES PARA LA PREDICCIÓN
    features = np.array([[year, month, day, precipitation, wind, humidity, estacion_id]])

    # PREDECIR EL CLIMA
    try:
        
        weather_id = loaded_model.predict(features)

        weather_id += 1

        weather_str = weather_dict[int(weather_id)]

    except Exception as e:
        return False, f"Error al realizar la predicción: {str(e)}"

    return True, weather_str
