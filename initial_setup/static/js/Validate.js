// LENGTH VALIDATE
function limitarCaracteres(elemento, maxCaracteres) {
    if (elemento.innerText.length > maxCaracteres) {
      elemento.innerText = elemento.innerText.slice(0, maxCaracteres);
    }
  }
// ONLY LETTERS
function checkL(e) {
    tecla = (document.all) ? e.keyCode : e.which;

    //Tecla de retroceso para borrar, siempre la permite
    if (tecla == 8 || tecla == 32) {
        return true;
    }

    // Patrón de entrada, en este caso solo acepta letras
    patron = /[A-Za-z]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}

// ONLY NUMBERS
function checkN(e) {
    tecla = (document.all) ? e.keyCode : e.which;

    //Tecla de retroceso para borrar, siempre la permite
    if (tecla == 8) {
        return true;
    }

    // Patrón de entrada, en este caso solo acepta numeros
    patron = /[0-9]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}

function checkND(e) {
    tecla = (document.all) ? e.keyCode : e.which;

    //Tecla de retroceso para borrar, siempre la permite
    if (tecla == 8 || tecla == 46) {
        return true;
    }

    // Patrón de entrada, en este caso solo acepta numeros
    patron = /[0-9]/;
    tecla_final = String.fromCharCode(tecla);
    if (patron.test(tecla_final)){
        // Si es un número, permite la entrada
        return true;
    } else if (tecla_final === "." && e.target.value.indexOf(".") === -1) {
        // Si es un punto y no hay otro punto en el valor actual, permite la entrada
        return true;
    } else {
        // En todos los demás casos, bloquea la entrada
        return false;
    }
}

// ONLY NUMBERS AND LETTERS
function checkA(e) {

    tecla = (document.all) ? e.keyCode : e.which;

    //Tecla de retroceso para borrar, siempre la permite
    if (tecla == 8 || tecla == 32) {
        return true;
    }

    // Patrón de entrada, en este caso solo acepta numeros y letras
    patron = /[A-Za-z0-9]/;
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
}