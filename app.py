from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML = """
<h1>📊 Modelo de Apuestas</h1>

<form method="post">
    <label for="market">Selecciona mercado:</label>
    <select name="market" id="market">
        <option value="over">Over 2.5 goles</option>
        <option value="btts">BTTS</option>
        <option value="basket">Basket Más/Menos</option>
    </select>
    <button type="submit">Actualizar partidos</button>
</form>

{% if partidos %}
<h2>Partidos del día</h2>

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

def obtener_partidos_futbol(market):
    # usa tu API actual para partidos del día
    # aquí se puede agregar cálculo Poisson o heurística simple
    headers = {"x-apisports-key": os.environ.get("API_KEY")}
    hoy = datetime.utcnow().strftime("%Y-%m-%d")
    
    url = f"https://v3.football.api-sports.io/fixtures?date={hoy}&timezone=America/Bogota"
    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    ligas = {}
    for f in data.get("response", []):
        liga = f"{f['league']['country']} - {f['league']['name']}"
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        # Aquí puedes aplicar lógica Poisson simple
        if market == "over":
            prob = "Over 2.5: 65%"  # ejemplo
        else:
            prob = "BTTS: 55%"     # ejemplo

        partido = f"{home} vs {away} | {prob}"
        ligas.setdefault(liga, []).append(partido)

    if not ligas:
        ligas = {"Sin datos": ["No hay partidos hoy"]}
    return ligas
    def obtener_partidos_basket():
    # ejemplo con API gratuita balldontlie.io
    url = "https://www.balldontlie.io/api/v1/games?per_page=10"
    r = requests.get(url, timeout=10)
    data = r.json()

    partidos = {}
    liga = "NBA"
    for g in data.get("data", []):
        home = g["home_team"]["full_name"]
        away = g["visitor_team"]["full_name"]
        puntos = g["home_team_score"] + g["visitor_team_score"]
        prob = f"Total Pts: {puntos + 5}"  # ejemplo heurístico
        partido = f"{home} vs {away} | {prob}"
        partidos.setdefault(liga, []).append(partido)

    if not partidos:
        partidos = {"Sin datos": ["No hay partidos de basket hoy"]}
    return partidos
from flask import request

@app.route("/", methods=["GET","POST"])
def inicio():
    market = "over"  # default
    partidos = {}

    if request.method == "POST":
        market = request.form.get("market", "over")
        try:
            if market == "basket":
                partidos = obtener_partidos_basket()
            else:
                partidos = obtener_partidos_futbol(market)
        except Exception as e:
            partidos = {"Error": [str(e)]}

    return render_template_string(HTML, partidos=partidos)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
