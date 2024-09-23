from flask import Flask, render_template, jsonify, request
import numpy as np

app = Flask(__name__)

# Esta es la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Se especifica la ruta para resolver la ecuacion
@app.route('/calculadora', methods=['POST'])
def calculadora():
    # Aqui obtenemos los datos enviados desde el front
    data = request.json  
    a1 = float(data['a1'])
    b1 = float(data['b1'])
    c1 = float(data['c1'])
    a2 = float(data['a2'])
    b2 = float(data['b2'])
    c2 = float(data['c2'])

    # Aqui se definen las matrices A: contiene los coeficientes de las variables (x, y) B: contiene las constantes
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])

    # Utilizando la funcion linalg.solve puede resolver el sistema de ecuaciones
    try:
        solucion = np.linalg.solve(A, B)
        x, y = solucion[0], solucion[1]
        resultado = {"x": round(x, 2), "y": round(y, 2)}
    except np.linalg.LinAlgError:
        resultado = {"error": "Sin solucion"}

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
