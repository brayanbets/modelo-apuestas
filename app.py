from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<h1>⚽ Modelo de Apuestas</h1>

<form method="post">
    <button type="submit">Actualizar partidos</button>
</form>

{% if partidos %}
<h2>Partidos de ejemplo</h2>
<ul>
{% for p in partidos %}
<li>{{p[0]}} vs {{p[1]}}</li>
{% endfor %}
</ul>
{% endif %}
"""

@app.route("/", methods=["GET","POST"])
def inicio():
    partidos = [
        ("Real Madrid","Barcelona"),
        ("Liverpool","Chelsea"),
        ("Bayern","Dortmund"),
        ("PSG","Monaco")
    ]
    return render_template_string(HTML, partidos=partidos)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
