import joblib, os
from datetime import datetime, timedelta
import pandas as pd

def get_weather(dates: list[str]) -> dict[str, set[int,float,float]]:
    """
    Devuelve weather_id, temp_max y temp_min de un csv de predicciones.

    Args:
        dates (list[str]): Lista de fechas en formato 'YYYY-MM-DD'.

    Returns:
        dict[str, str]: Un diccionaio donde el primer valor es el weather_id, 
                        el segundo la temperatura maxima de ese dia y el tercero la temperatura minima
    """

    try:
        predictions_df = pd.read_csv(r'.\..\weather_predictions.csv')
    except FileNotFoundError:
        raise FileNotFoundError("The file 'weather_predictions.csv' could not be found. Check the file path.")

    weather_ids = {}

    for date in dates:
        # filtrar por fecha
        matching_row = predictions_df.loc[predictions_df['date'] == date]

        # añadir al diccionario si hay coincidencias
        if not matching_row.empty:
            weather_ids[date] = str(matching_row['weather_id'].values[0])
        else:
            weather_ids[date] = "Not Found"

    return weather_ids


def intermediate_dates(initial_date:datetime,final_date:datetime) -> list[str]:

    dates = []

    while initial_date <= final_date:
        dates.append(initial_date.strftime('%Y-%m-%d'))
        initial_date += timedelta(days=1)

    return dates


