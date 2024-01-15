// Operations Logic
// Function necessary to load an excel file, in this case the operations file
function uploadFileOperations() {
    var machineNumb = parseInt(document.getElementById('machine_numb').value);
    if (isNaN(machineNumb) || machineNumb < 1) {
        alert('Ingrese un número válido de máquinas antes de generar la tabla.');
        return;
    }

    var input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .csv';
    input.addEventListener('change', function () {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var data = e.target.result;
                processFile(data, machineNumb, 'tableContainerO');
            };
            reader.readAsText(file);
        }
    });
    input.click();
}

// Change the data variable to an array
function processFile(data, numb, table) {
    var rows = data.split('\n');
    var dataArray = rows.map(function (row) {
        if (!row) return [];  // Si la fila es null o undefined, devolver un array vacío
        return row.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g).map(function(match) {
            return match.replace(/^"|"$/g, ''); // Elimina las comillas al inicio y al final
        });
    });

    tableGenerator(dataArray, numb);
}

// Generate a table with processed data
function tableGenerator(dataArray, num) {
    var tablaHTML = '<table><thead><tr>';
    tablaHTML += '<th>Operaciones</th>';

    for (var i = 1; i <= num; i++) {
        tablaHTML += '<th>M' + i + '</th>';
    }

    tablaHTML += '</tr></thead><tbody>';

    for (var row = 1; row < dataArray.length-1; row++) {
        tablaHTML += '<tr>';

        for (var col = 0; col <= num; col++) {
            tablaHTML += '<td>' + dataArray[row][col] + '</td>';
        }

        tablaHTML += '</tr>';
    }

    tablaHTML += '</tbody></table>';

    document.getElementById('tableContainerO').innerHTML = tablaHTML;
}