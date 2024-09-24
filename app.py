from flask import Flask, render_template, jsonify, request
from sympy import Matrix, sympify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculadora', methods=['POST'])
def calculadora():
    try:
        # Obtener los datos del frontend
        data = request.json
        a1 = sympify(data['a1'])
        b1 = sympify(data['b1'])
        c1 = sympify(data['c1'])
        a2 = sympify(data['a2'])
        b2 = sympify(data['b2'])
        c2 = sympify(data['c2'])

        # Definimos las matrices para aplicar la Regla de Cramer
        A = Matrix([[a1, b1], [a2, b2]])  # Matriz de coeficientes
        B = Matrix([c1, c2])              # Matriz de resultados

        # Calculamos el determinante de A (Delta)
        Delta = A.det()

        # Si el determinante es cero, el sistema no tiene solución única
        if Delta == 0:
            return jsonify({"error": "El sistema no tiene solución única, Delta es 0."})

        # Calculamos los determinantes de Delta_x y Delta_y
        A_x = A.copy()
        A_x[:, 0] = B  # Reemplazamos la primera columna por B (para x)

        A_y = A.copy()
        A_y[:, 1] = B  # Reemplazamos la segunda columna por B (para y)

        Delta_x = A_x.det()
        Delta_y = A_y.det()

        # Calculamos las soluciones x y y
        x = Delta_x / Delta
        y = Delta_y / Delta

        # Formato de la respuesta
        procedimiento = f"**Paso 1:** Matriz de coeficientes (A):<br>{A}<br><br>" \
                        f"**Paso 2:** Determinante de A (Delta): {Delta}<br>" \
                        f"Para calcular el determinante de una matriz \( 2 x 2 \):<br>" \
                        f"\\[ \\Delta = a_{11} \\cdot a_{22} - a_{12} \\cdot a_{21} \\]<br>" \
                        f"Aplicamos a nuestra matriz:<br>" \
                        f"\\[ \\Delta = {a1} \\cdot {b2} - {b1} \\cdot {a2} = {Delta} \\]<br><br>" \
                        f"**Paso 3:** Matriz modificada para Delta_x:<br>{A_x}<br>" \
                        f"Aplicamos a nuestra matriz:<br>" \
                        f"\\[ \\Delta_x = {c1} \\cdot {b2} - {b1} \\cdot {c2} = {Delta_x} \\]<br><br>" \
                        f"\\[ \\Delta_x = {Delta_x}\\]<br><br>" \
                        f"**Paso 4:** Matriz modificada para Delta_y:<br>{A_y}<br>" \
                        f"Aplicamos a nuestra matriz:<br>" \
                        f"\\[ \\Delta_y = {a1} \\cdot {c2} - {a2} \\cdot {c1} = {Delta_y} \\]<br><br>" \
                        f"\\[ \\Delta_y = {Delta_y}\\]<br><br>" \
                        f"**Paso 5:** Solución final:<br>x = {x}, y = {y}<br>"

        resultado = {
            "x": f"{x:.2f}",  # Formato a 2 decimales
            "y": f"{y:.2f}",  # Formato a 2 decimales
            "procedure": procedimiento
        }


    except Exception as e:
        resultado = {"error": f"Error en el cálculo: {str(e)}"}

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
