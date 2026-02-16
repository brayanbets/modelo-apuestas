from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML = """
<h1>⚽ Modelo de Apuestas</h1>

<form method="post">
    <button type="submit">Buscar partidos</button>
</form>

{% if partidos %}
<h2>Partidos de hoy</h2>

{% for liga, lista in partidos.items() %}
<h3>{{liga}}</h3>
<ul>
{% for p in lista %}
<li>{{p}}</li>
{% endfor %}
</ul>
{% endfor %}

{% endif %}
"""

from datetime import datetime

def obtener_partidos():

    headers = {"x-apisports-key": os.environ.get("API_KEY")}
    hoy = datetime.utcnow().strftime("%Y-%m-%d")

    # ligas ofensivas (muchos goles)
    ligas_ids = [
        39,   # Premier League
        140,  # La Liga
        78,   # Bundesliga
        135,  # Serie A
        61,   # Ligue 1
        88,   # Netherlands
        179,  # Norway
        113   # Sweden
    ]

    ligas = {}

    for liga_id in ligas_ids:
        url = f"https://v3.football.api-sports.io/fixtures?league={liga_id}&date={hoy}&timezone=America/Bogota"
        r = requests.get(url, headers=headers, timeout=8)
        data = r.json()

        for f in data.get("response", []):
            liga = f["league"]["name"]
            partido = f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}"
            ligas.setdefault(liga, []).append(partido)

    if not ligas:
        ligas = {"Sin datos": ["La API gratuita solo permite ligas cuando hay jornada activa"]}

    return ligas
@app.route("/", methods=["GET","POST"])
def inicio():
    partidos = {}

    if request.method == "POST":
        try:
            partidos = obtener_partidos()
        except Exception as e:
            partidos = {"Error": [str(e)]}

    return render_template_string(HTML, partidos=partidos)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
