function parseCoefficient(term) {
    // Quitar espacios
    term = term.replace(/\s+/g, '');
    // Regex que permite valores positivos y negativos, fracciones, raices y variables X e Y
    let match = term.match(/^([+-]?(?:\d+\/\d+|\d*\.?\d*|\d+)?(?:\s*\+\s*\sqrt{?\d+}?|\s*-\s*\sqrt{?\d+}?)?)[xy]?$/);

    if (match) {
        let coefficient = match[1];
        if (coefficient === '' || coefficient === '+') {
            return 1; 
        } else if (coefficient === '-') {
            return -1;
        } else {
            try{
                //Reemplazar 'sqrt' por 'Math.sqrt' y evaluar la ecuacion
                return eval(coefficient.replace(/sqrt/g, 'Math.sqrt').replace(/([=-]?\d+\/\d+)/g, '(($1))'));
            }catch(error){
                throw new Error(`Término inválido: ${term}`);
            }
        }
    }
    throw new Error(`Término inválido: ${term}`);
}

function solveEquations(event) {
    event.preventDefault();
    
    // Obtener valores de los inputs
    const a1 = document.getElementById('a1').value;
    const b1 = document.getElementById('b1').value;
    const c1 = document.getElementById('c1').value;
    const a2 = document.getElementById('a2').value;
    const b2 = document.getElementById('b2').value;
    const c2 = document.getElementById('c2').value;

    // Hacer la solicitud al backend
    fetch('/calculadora', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ a1, b1, c1, a2, b2, c2 })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar el procedimiento y los resultados
        document.getElementById('procedure').innerHTML = data.procedure;
        MathJax.typeset(); // Procesar el contenido nuevo para mostrar LaTeX
        document.getElementById('result').innerText = `x = ${data.x}, y = ${data.y}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error al resolver las ecuaciones.';
    });
}


