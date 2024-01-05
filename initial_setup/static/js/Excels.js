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

    if (table === 'tableContainerT'){
        generateTableTasks0(dataArray, numb);
    } else {
        tableGenerator(dataArray, numb);
    }
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

var cellValues = [];

// Tasks Logic
document.getElementById('tasks').addEventListener('input', function () {
    var numRows = parseInt(this.value);
    updateCellValues(numRows);
    if (!isNaN(numRows) && numRows > 0) {
        // Volver a almacenar los valores actuales de las celdas
        generateTableTasks0('', numRows);
    } else {
        clearTableTasks();
    }
});

function generateTableTasks0(dataArray, numRows) {console.log('b')
    var tableHTML = '<table><thead><tr><th>Trabajos</th><th>Operaciones</th></tr></thead><tbody>';

    if(dataArray !== ''){
        for (var row = 0; row < numRows; row++) {
            tableHTML += '<tr>';
            tableHTML += '<td>J' + (row + 1) + '</td><td>' + dataArray[row + 1][1] + '</td>';    
            tableHTML += '</tr>';
        }
    }else{
        // Guardar los valores actuales de las celdas
        for (var i = 0; i < numRows; i++) {
            var cellValue = (cellValues.length > i && cellValues[i]) ? cellValues[i] : '';
            tableHTML += '<tr><td>J' + (i + 1) + '</td><td contenteditable="true" oninput="mayus(this);" onkeypress="return checkA(event)">' + cellValue + '</td></tr>';
        }
    }

    tableHTML += '</tbody></table>';
    // Actualizar el contenido de la tabla
    document.getElementById('tableContainerT').innerHTML = tableHTML;
}

function updateCellValues(numRows) {console.log('a')
    cellValues = [];
    var tableRows = document.getElementById('tableContainerT').getElementsByTagName('tr');
    
    // Recorrer las filas de la tabla y actualizar o agregar los valores de las celdas
    for (var i = 0; i < numRows; i++) {
        if(tableRows[i]){
            var cells = tableRows[i].getElementsByTagName('td')[1];
            
            // Si ya hay un valor en el array, actualizarlo; de lo contrario, agregarlo
            if (cells && cells.textContent.trim() !== ''){
                cellValues.push(cells.innerText);
            } else{
                if(!cells){
                    continue
                }
                if(cells.textContent.trim() === ''){
                    cellValues.push('');
                }
            }
        }else{
            break;
        }
    }
    console.log(cellValues)
}

function clearTableTasks() {
    document.getElementById('tableContainerT').innerHTML = '';
}

// File processing
function uploadFileTasks() {
    var TasksNumb = parseInt(document.getElementById('tasks').value);
    if (isNaN(TasksNumb) || TasksNumb < 1) {
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
                processFile(data, TasksNumb, 'tableContainerT');
            };
            reader.readAsText(file);
        }
    });
    input.click();
}