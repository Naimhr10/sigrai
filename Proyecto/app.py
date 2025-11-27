from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# ============================================================
# CARGAR VARIABLES DE ENTORNO
# ============================================================

load_dotenv()   # Carga el archivo .env automáticamente

API_TOKEN = os.getenv("HF_TOKEN")  # Lee token desde .env

# Validación opcional
if not API_TOKEN:
    print("⚠️ ADVERTENCIA: No se encontró HF_TOKEN en el archivo .env")
    print("Asegúrate de tener un archivo .env con: HF_TOKEN=tu_token")
else:
    print("✔ Token cargado correctamente desde .env")


# ============================================================
# CONFIGURACIÓN FLASK
# ============================================================

app = Flask(__name__)
CORS(app)

# ============================================================
# CONFIGURACIÓN DE IA MÉDICA (TEXTO)
# ============================================================

API_URL = "https://router.huggingface.co/hf-inference/BioMistral/BioMistral-7B"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.form.get("mensaje", "")

    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400

    payload = {
        "inputs": user_message,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        respuesta = response.json()

        if isinstance(respuesta, list) and "generated_text" in respuesta[0]:
            return jsonify({"respuesta": respuesta[0]["generated_text"]})

        if "generated_text" in respuesta:
            return jsonify({"respuesta": respuesta["generated_text"]})

        return jsonify({"respuesta": str(respuesta)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ANÁLISIS DE IMÁGENES
# ============================================================

IMG_API_URL = "https://router.huggingface.co/hf-inference/microsoft/resnet50-xray"


@app.route("/analizar", methods=["POST"])
def analizar():
    archivo = request.files.get("imagen")

    if not archivo:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    image_bytes = archivo.read()

    try:
        response = requests.post(
            IMG_API_URL,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            data=image_bytes
        )
        resultado = response.json()
        return jsonify({"resultado": resultado})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# INICIO DEL SERVIDOR
# ============================================================

if __name__ == "__main__":
    print("\n🔥 Servidor Flask corriendo en:")
    print("👉 http://127.0.0.1:5000")
    print("\n✔ IA médica conectada correctamente\n")
    app.run(port=5000, debug=True)
