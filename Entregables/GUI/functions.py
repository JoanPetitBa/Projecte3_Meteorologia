import joblib
from datetime import datetime
import tensorflow as tf
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

def get_weather(date: str, precipitation: float, wind: float, humidity: int, model: str = 'XGB') -> tuple[bool, str]:
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

    # Validación de entradas
    if precipitation < 0:
        return False, "La precipitación no puede ser negativa."
    if wind < 0:
        return False, "El viento no puede ser negativo."
    if humidity < 0 or humidity > 100:
        return False, "La humedad debe estar entre 0 y 100."
    if model.upper() not in ['RNN', 'SVM', 'XGB']:
        return False, f"Modelo '{model}' desconocido."

    try:
        # Parsear la fecha
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
    except ValueError:
        return False, "Formato de fecha inválido. Debe ser 'YYYY-MM-DD'."

    # Obtener el identificador de la estación
    estacion_id = get_season(month)

    # Cargar el modelo correspondiente
    model_path = fr".\..\Modelos\{model.upper()}_weather_id.pkl"
    try:
        if model.upper() == 'RNN':
            loaded_model = tf.keras.models.load_model(model_path)
        else:
            loaded_model = joblib.load(model_path)
    except FileNotFoundError:
        return False, f"No se pudo encontrar el modelo en la ruta {model_path}."

    # Preparar las características para la predicción
    features = np.array([[year, month, day, precipitation, wind, humidity, estacion_id]])

    # Hacer la predicción
    try:
        
        weather_id = loaded_model.predict(features)
        weather_str = weather_dict[weather_id]

    except Exception as e:
        return False, f"Error al realizar la predicción: {str(e)}"

    return True, weather_id
