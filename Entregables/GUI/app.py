from flask import Flask, render_template, request
from datetime import datetime, timedelta
from functions  import get_weather
import random

app = Flask(__name__)

BODY_BG = {'sun':'linear-gradient(180deg, rgba(255,222,89,1) 0%, rgba(255,255,255,1) 100%)',
               'rain':'linear-gradient(180deg, rgba(0,131,181,1) 0%, rgba(213,213,213,1) 100%)',
               'fog':'linear-gradient(180deg, rgba(171,171,171,1) 0%, rgba(255,255,255,1) 100%)',
               'cloud':'linear-gradient(180deg, rgba(50,50,50,1) 0%, rgba(255,255,255,1) 100%)',
               'storm':'linear-gradient(180deg, rgba(0,83,181,1) 0%, rgba(213,213,213,1) 100%)'
}

MAIN_BG = {
    'sun': '#FFE57F',
    'rain': '#A1C4E4',
    'fog': '#D6D6D6',
    'cloud': '#B0BEC5',
    'storm': '#90A4AE'
}

MSG = {
    'sun': 'Un día soleado y brillante.',
    'rain': 'Lluvias esperadas, ¡no olvides tu paraguas!',
    'fog': 'Niebla densa, ten cuidado al conducir.',
    'cloud': 'Cielo nublado, pero tranquilo.',
    'storm': 'Tormenta en camino, quédate seguro.'
}

@app.route("/", methods=["GET", "POST"])
def home():

    today = datetime.now().strftime("%Y-%m-%d")

    state,weather = get_weather(
        date = today,
        precipitation = random.uniform(0,50),
        wind = random.uniform(0,10),
        humidity = random.randint(30,100),
    )

    if state:
        return render_template(
            "index.html",
            body_bg = BODY_BG[weather],
            main_bg = MAIN_BG[weather],
            weather_icon = f"{{ url_for('static', filename='icons/{weather}.png') }}",
            date = today,
            msg = "TEST: OK"
        )
    
    else:

        return render_template(
            "index.html",
            body_bg = BODY_BG['storm'],
            main_bg = MAIN_BG['storm'],
            weather_icon = f"{{ url_for('static', filename='icons/storm.png') }}",
            date = today,
            msg = F"TEST: {weather}"
        )

@app.route("/get_data_dates", methods=['POST'])
def get_data_dates():
    
    initial_date = request.form.get('date_1')
    ending_date = request.form.get('date_2')

    if initial_date and ending_date:

        initial_date_datetime = datetime.strptime(initial_date, "%Y-%m-%d")
        ending_date_datetime = datetime.strptime(ending_date, "%Y-%m-%d")

        # COMPROVAR SI LES DATES SON TEMPORALMENT CORRECTES
        if initial_date_datetime > ending_date_datetime:
            error_msg = "La primera fecha no puede ser posterior a la segunda."
            return render_template('index.html', error_msg= error_msg)
        
        # CREAR LISTA VACIA PARA AÑADIR LAS FECHAS INTERMEDIAS
        all_dates:list[str] = []

        # ITERAR ENTRE LAS DOS FECHAS Y AÑADIR A LA LISTA 'all_dates'
        date = initial_date_datetime
        while date <= ending_date_datetime:
            all_dates.append(date.strftime("%Y-%m-%d"))
            date += timedelta(days=1)

        # LLAMAR A LA FUNCION '' PARA OBTENER TODOS LOS DATOS NECESARIOS
        

    elif initial_date and not ending_date_datetime:
        pass


    # OBTENIR DE LA BDD PER CADA DIA ENTRE AQUESTES DUES DATES: data, weather_id(icono), avg_temp, max_temp, min_temp, humidity, precipitation, pressure, wind

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)