from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.form.get("mensaje")

    response = client.responses.create(
        model="gpt-4o-mini",
        input=mensaje
    )

    respuesta = response.output_text
    return jsonify({"respuesta": respuesta})


@app.route("/analizar", methods=["POST"])
def analizar():
    img = request.files.get("imagen")

    response = client.responses.create(
        model="gpt-4o-mini",
        input="Analiza la imagen médicamente.",
        image=[img]
    )

    resultado = response.output_text
    return jsonify({"resultado": resultado})


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


