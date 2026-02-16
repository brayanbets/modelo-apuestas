from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

HTML = """
<h1>⚽ Modelo de Apuestas</h1>

<form method="post">
    <button type="submit">Buscar partidos con goles</button>
</form>

{% if partidos %}
<h2>Partidos recomendados (+2.5 goles)</h2>
<ul>
{% for p in partidos %}
<li>{{p}}</li>
{% endfor %}
</ul>
{% endif %}
"""

def obtener_partidos():
    url = "https://v3.football.api-sports.io/fixtures?next=20"
    headers = {"x-apisports-key": os.environ.get("API_KEY")}
    r = requests.get(url, headers=headers, timeout=20)
    data = r.json()

    partidos = []

    for f in data["response"]:
        home = f["teams"]["home"]["name"]
        away = f["teams"]["away"]["name"]
        liga = f["league"]["name"]

        partidos.append(f"{home} vs {away}  ({liga})")

    return partidos

@app.route("/", methods=["GET","POST"])
def inicio():
    partidos = None
    try:
        partidos = obtener_partidos()
    except Exception as e:
        partidos = [f"Error cargando datos: {e}"]

    return render_template_string(HTML, partidos=partidos)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
