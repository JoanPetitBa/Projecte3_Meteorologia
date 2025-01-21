from flask import Flask, render_template, request
from datetime import datetime, timedelta
from functions  import get_weather
import random

app = Flask(__name__)

BODY_BG = {'sun':'linear-gradient(180deg, rgba(255,222,89,1) 0%, rgba(255,255,255,1) 100%)',
            'rain':'linear-gradient(180deg, rgba(89,185,255,1) 0%, rgba(218,218,218,1) 100%)',
            'fog':'linear-gradient(180deg, rgba(140,140,140,1) 0%, rgba(255,255,255,1) 100%)',
            'cloudy':'linear-gradient(180deg, rgba(222,222,222,1) 0%, rgba(255,255,255,1) 100%)',
            'storm':'linear-gradient(180deg, rgba(56,96,175,1) 0%, rgba(181,181,181,1) 100%)'
}

MAIN_BG = {
    'sun': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,222,89,1) 100%)',
    'rain': 'linear-gradient(180deg, rgba(218,218,218,1) 0%, rgba(89,185,255,1) 100%)',
    'fog': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(140,140,140,1) 100%)',
    'cloudy': 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(222,222,222,1) 100%)',
    'storm': 'linear-gradient(180deg, rgba(181,181,181,1) 0%, rgba(56,96,175,1) 100%)'
}

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
        'Sca los juegos de mesa, habra tormenta'
    ]
}


@app.route("/", methods=["GET", "POST"])
def home():

    today = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        
        precipitation = float(request.form.get('precipitation')) if request.form.get('precipitation') != '' else 0.0
        wind = float(request.form.get('wind')) if request.form.get('wind') != '' else 0.0
        humidity = int(request.form.get('humidity')) if request.form.get('humidity') != '' else 0
        date = request.form.get('date')

        state,weather = get_weather(
            date = today,
            precipitation = precipitation,
            wind = wind,
            humidity = humidity,
        )

        
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

    return render_template(
        "index.html",
        body_bg = BODY_BG['sun'],
        main_bg = MAIN_BG['sun'],
        weather_icon = f"sun.png",
        date = today,
        precipitation="0.1 mm",
        wind=f"3.21 m/s",
        humidity=f"26%",
        msg = random.choice(MSG['sun'])
    )

if __name__ == "__main__":
    app.run(debug=True)