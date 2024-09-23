from flask import Flask, render_template, jsonify, request
import numpy as np

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para resolver ecuaciones
@app.route('/calculadora', methods=['POST'])
def calculadora():
    data = request.json  # Obtener los datos enviados desde el frontend
    a1 = float(data['a1'])
    b1 = float(data['b1'])
    c1 = float(data['c1'])
    a2 = float(data['a2'])
    b2 = float(data['b2'])
    c2 = float(data['c2'])

    # Definir las matrices para resolver el sistema de ecuaciones
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])

    try:
        solucion = np.linalg.solve(A, B)  # Resolver el sistema
        x, y = solucion[0], solucion[1]
        resultado = {"x": round(x, 2), "y": round(y, 2)}
    except np.linalg.LinAlgError:
        resultado = {"error": "El sistema de ecuaciones no tiene solución única"}

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
