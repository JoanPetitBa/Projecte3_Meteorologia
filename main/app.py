from flask import Flask, render_template, request
from datetime import datetime
from functions import get_weather
import random
import time, os
from threading import Thread

app = Flask(__name__)

# DICCIONARIO PARA CAMBIAR EL FONDO EN BASE AL TIEMPO PREDICHO
BODY_BG = {'sun':'linear-gradient(180deg, rgba(255,222,89,1) 0%, rgba(255,255,255,1) 100%)',
            'rain':'linear-gradient(180deg, rgba(89,185,255,1) 0%, rgba(218,218,218,1) 100%)',
            'fog':'linear-gradient(180deg, rgba(140,140,140,1) 0%, rgba(255,255,255,1) 100%)',
            'cloudy':'linear-gradient(180deg, rgba(222,222,222,1) 0%, rgba(255,255,255,1) 100%)',
            'storm':'linear-gradient(180deg, rgba(56,96,175,1) 0%, rgba(181,181,181,1) 100%)'
}

# DICCIONARIO PARA CAMBIAR EL FONDO DEL CONTAINER EN BASE AL TIEMPO PREDICHO
MAIN_BG = {
    'sun': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,222,89,1) 100%)',
    'rain': 'linear-gradient(180deg, rgba(218,218,218,1) 0%, rgba(89,185,255,1) 100%)',
    'fog': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(140,140,140,1) 100%)',
    'cloudy': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(222,222,222,1) 100%)',
    'storm': 'linear-gradient(180deg, rgba(181,181,181,1) 0%, rgba(56,96,175,1) 100%)'
}

# DICCIONARIO DE LOS MENSAJES QUE SE MUESTRAN POR DA TIPO DE TIEMPO
MSG = {
    'sun': [
        'Hoy es un día soleado y perfecto para salir.',
        'El sol brilla con fuerza, no olvides tus gafas de sol.',
        'Un día soleado y brillante, ideal para un paseo al aire libre.'
    ],
    'rain': [
        'Lluvias esperadas, ¡lleva tu paraguas!',
        'El pronóstico indica lluvia, prepárate para mojarte.',
        'Lluvias en el horizonte, no te olvides de tu impermeable.'
    ],
    'fog': [
        'Niebla densa en las carreteras, ten precaución al conducir.',
        'El clima está cubierto por niebla espesa, con visibilidad reducida.',
        'No podras verte ni la nariz'
    ],
    'cloudy': [
        'El cielo está nublado, pero no parece haber lluvia.',
        'Un día nublado y fresco, ideal para quedarse en casa.',
        'Cielo cubierto de nubes, sin rastro de sol'
    ],
    'storm': [
        'Se acerca una tormenta, mejor resguardarse pronto.',
        'Tormenta fuerte en camino, toma precauciones.',
        'Saca los juegos de mesa, habra tormenta'
    ]
}

# VARIBLES PARA EL TIEMPO DE INACTIVIDAD, TIEMPO DE INACTIVIDAD 2 MINUTOS
last_request_time = time.time()
INACTIVITY_TIMEOUT = 120

# CODIGO PRINCIPAL DE FLASK
@app.route("/", methods=["GET", "POST"])
def home():

    global last_request_time
    today = datetime.now()

    # SI LA PETICION AL SERVIDOR ES UN POST
    if request.method == "POST":

        # ACTUALIZAR EL TIEMPO DE INACTIVIDAD
        last_request_time = time.time()
        
        # OBTENER LOS VALORES ENTRADOS POR EL USUARIO
        precipitation = float(request.form.get('precipitation')) if request.form.get('precipitation') != '' else 0.0
        wind = float(request.form.get('wind')) if request.form.get('wind') != '' else 0.0
        humidity = int(request.form.get('humidity')) if request.form.get('humidity') != '' else 0
        date = request.form.get('date')
        if date == '':
            date = today.strftime("%Y-%m-%d")

        # PREDECIR EL TIPO DE CLIMA
        state, weather = get_weather(
            date=date,
            precipitation=precipitation,
            wind=wind,
            humidity=humidity,
        )

        # RECARGAR LA PAGINA PRINCIPAL CON LA NUEVA INFORMACIÓN
        return render_template(
            "index.html",
            body_bg=BODY_BG[weather],
            main_bg=MAIN_BG[weather],
            weather_icon=f"{weather}.png",
            date=date,
            precipitation=f"{precipitation} mm",
            wind=f"{wind} m/s",
            humidity=f"{humidity}%",
            msg=random.choice(MSG[weather])
        )


    # SI LA PETICIÓN ES DE TIPO GET
    
    # ACTUALIZAR EL TIEMPO DE INACTIVIDAD
    last_request_time = time.time()

    # CARGAR LA PAGINA CON VALOR DE 'sun' PREDETERMINADO
    return render_template(
        "index.html",
        body_bg=BODY_BG['sun'],
        main_bg=MAIN_BG['sun'],
        weather_icon=f"sun.png",
        date=today.strftime("%d-%m-%Y"),
        precipitation="0.1 mm",
        wind="3.21 m/s",
        humidity="26%",
        msg=random.choice(MSG['sun'])
    )

# FUNCION PARA COMPROVAR SI NO SE HA SUPERADO EL TIEMPO DE INACTIVDAD
def monitor_inactivity():
    global last_request_time
    while True:
        time.sleep(1)
        if time.time() - last_request_time > INACTIVITY_TIMEOUT:
            print("No se han registrado nuevas entradas. Cerrando el servidor...")
            os._exit(0)
            break
    

############ MAIN ############
if __name__ == "__main__":

    # INICIAR EL MONITOREO EN UN HILO SEPARADO DE LA ACCION PRINCIPAL
    inactivity_thread = Thread(target=monitor_inactivity)

    # EL HILO SE CERRARÁ CUANDO EL SERVIDOR SE CIERRE
    inactivity_thread.daemon = True
    inactivity_thread.start()

    # INICIAR EL SERVIDOR DE FLASK
    app.run()
