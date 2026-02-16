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
<li>{{p['homeTeam']['name']}} vs {{p['awayTeam']['name']}}</li>
{% endfor %}
</ul>
{% endif %}
"""

API_KEY = "demo"   # luego pondremos la real

@app.route("/", methods=["GET","POST"])
def inicio():
    partidos = None

    try:
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": API_KEY}
        r = requests.get(url, headers=headers)
        data = r.json()
        partidos = data.get("matches", [])[:10]
    except:
        partidos = [{"homeTeam":{"name":"Error cargando datos"}, "awayTeam":{"name":"—"}}]

    return render_template_string(HTML, partidos=partidos)

if _name_ == "_main_":
    app.run()
