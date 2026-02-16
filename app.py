from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Modelo de Apuestas activo</h1>
    <p>Tu servidor está funcionando correctamente</p>
    """

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=10000)
