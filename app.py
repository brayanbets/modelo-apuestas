from flask import Flask, render_template_string
import requests

app = Flask(__name__)

HTML = """
<h1>⚽ Modelo de Apuestas</h1>

<form method="post">
    <button type="submit">Actualizar partidos</button>
</form>

{% if partidos %}
<h2>Partidos de hoy</h2>
<ul>
{% for p in partidos %}
<li>{{p}}</li>
{% endfor %}
</ul>
{% endif %}
"""

def obtener_partidos():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?s=Soccer"
    r = requests.get(url, timeout=10)
    data = r.json()

    partidos = []
    if data and data["events"]:
        for e in data["events"][:15]:
            partidos.append(f"{e['strHomeTeam']} vs {e['strAwayTeam']}")

    return partidos

@app.route("/", methods=["GET","POST"])
def inicio():
    partidos = None
    try:
        partidos = obtener_partidos()
    except:
        partidos = ["No se pudieron cargar partidos (normal la primera vez)"]

    return render_template_string(HTML, partidos=partidos)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
