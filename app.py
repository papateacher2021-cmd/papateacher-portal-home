from flask import Flask, request, jsonify, render_template_string
# import tensorflow as tf
import numpy as np
import json
import os

app = Flask(__name__)

# Cargar el modelo
def cargar_modelo():
    try:
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        modelo = tf.keras.models.model_from_json(json.dumps(config_data))
        modelo.load_weights('model.weights.h5')
        return modelo
    except Exception as e:
        print(f"Error: {e}")
        return None

modelo = cargar_modelo()

# Diseño HTML integrado (CSS incluido para que se vea moderno)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Hub IA - Pancho B</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h1 { color: #2c3e50; margin-bottom: 1rem; }
        input { width: 80%; padding: 10px; margin: 10px 0; border: 2px solid #ddd; border-radius: 8px; font-size: 1rem; }
        button { background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 1rem; transition: background 0.3s; }
        button:hover { background-color: #2980b9; }
        #resultado { margin-top: 20px; font-weight: bold; color: #27ae60; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🤖 Hub IA Pancho B</h1>
        <p>Introduce el valor para la predicción:</p>
        <input type="number" id="inputValue" placeholder="Ej: 10.5" step="any">
        <br>
        <button onclick="realizarPrediccion()">Predecir Ahora</button>
        <div id="resultado"></div>
    </div>

    <script>
        async function realizarPrediccion() {
            const val = document.getElementById('inputValue').value;
            const resDiv = document.getElementById('resultado');
            if(!val) return alert("Escribe un número");
            
            resDiv.innerText = "Calculando...";
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({data: [parseFloat(val)]})
                });
                const result = await response.json();
                resDiv.innerText = "Resultado: " + result.resultado[0][0].toFixed(4);
            } catch (error) {
                resDiv.innerText = "Error al conectar con la IA";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if modelo is None: return jsonify({'error': 'Modelo no cargado'}), 500
    try:
        datos = request.json['data']
        input_array = np.array(datos).astype('float32').reshape(1, -1)
        prediccion = modelo.predict(input_array)
        return jsonify({'resultado': prediccion.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
