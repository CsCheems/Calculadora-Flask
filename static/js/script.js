function parseCoefficient(term) {
    term = term.replace(/\s+/g, '');  // Quitar espacios
    let match = term.match(/^([+-]?\d*\.?\d*)[xy]?$/);
    
    if (match) {
        let coefficient = match[1];
        if (coefficient === '' || coefficient === '+') {
            return 1; 
        } else if (coefficient === '-') {
            return -1;
        } else {
            return parseFloat(coefficient); 
        }
    }
    throw new Error(`Término inválido: ${term}`);
}

async function solveEquations(event) {
    event.preventDefault();  // Evitar la recarga de la página

    try {
        // Obtener los valores del formulario
        let a1 = parseCoefficient(document.getElementById('a1').value);
        let b1 = parseCoefficient(document.getElementById('b1').value);
        let c1 = parseFloat(document.getElementById('c1').value);
        let a2 = parseCoefficient(document.getElementById('a2').value);
        let b2 = parseCoefficient(document.getElementById('b2').value);
        let c2 = parseFloat(document.getElementById('c2').value);

        let data = {
            a1: a1,
            b1: b1,
            c1: c1,
            a2: a2,
            b2: b2,
            c2: c2
        };

        let response = await fetch('/calculadora', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        let result = await response.json();

        if (result.error) {
            document.getElementById('result').innerHTML = result.error;
        } else {
            document.getElementById('result').innerHTML = `x = ${result.x}, y = ${result.y}`;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = error.message;
    }
}
