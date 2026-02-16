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

from datetime import datetime, timedelta

def obtener_partidos():

    headers = {"x-apisports-key": os.environ.get("API_KEY")}
    ligas = {}

    for i in range(7):  # buscar hasta 1 semana
        fecha = (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d")

        url = f"https://v3.football.api-sports.io/fixtures?date={fecha}&timezone=America/Bogota"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        for f in data.get("response", []):
            pais = f["league"]["country"]
            liga = f"{pais} - {f['league']['name']} ({fecha})"
            partido = f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}"
            ligas.setdefault(liga, []).append(partido)

        if ligas:
            break

    if not ligas:
        ligas = {"Sin datos": ["Tu plan gratuito no tiene partidos disponibles hoy"]}

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
