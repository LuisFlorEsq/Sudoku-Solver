// Operations Logic
// Function necessary to load an excel file, in this case the operations file
function uploadFileOperations() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .csv';
    input.addEventListener('change', function () {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var data = e.target.result;
                processFile(data);
            };
            reader.readAsText(file);
        }
    });
    input.click();
}

// Change the data variable to an array
function processFile(data) {
    var rows = data.split('\n');
    var dataArray = rows.map(function (row) {
        if (!row) return [];  // Si la fila es null o undefined, devolver un array vacío
        return row.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g).map(function(match) {
            return match.replace(/^"|"$/g, ''); // Elimina las comillas al inicio y al final
        });
    });

    tableGenerator(dataArray);
}

// Generate a table with processed data
function tableGenerator(dataArray) {
    var tablaHTML = '<table class="Settings" id="Settings"><thead><tr><th>Tasa_Muta_Fila</th><th>Tasa_Muta_Init</th><th>Tasa_Cruza</th><th>Tasa_Cruza_Fila</th><th>Tam_T</th><th>Elite_size</th><th>Tam_Pob</th><th>N</th>';

    tablaHTML += '</tr></thead><tbody>';

    for (var row = 1; row < dataArray.length-1; row++) {
        tablaHTML += '<tr>';

        for (var col = 0; col <= 7; col++) {
            tablaHTML += '<td contenteditable="true" onkeypress="return checkND(event)">' + dataArray[row][col] + '</td>';
        }

        tablaHTML += '</tr>';
    }

    tablaHTML += '</tbody></table>';

    document.getElementById('tableContainerO').innerHTML = tablaHTML;
    // Add button to start simulation of GA
    document.getElementById('Sudoku_Simulation').innerHTML += '<button type="button" class="BAccept Start_Sim" id="Start_Sim">Iniciar Simulación</button>'
    // Add listener to the previous generated button
    $(".Start_Sim").click(function (e) {
        var fila = $("#Settings tr:eq(1)");
        var rowValues = [];

        fila.find("td").each(function() {
            if(!$(this).text().trim()){
                Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: 'Debes llenar todos los campos'});
            }else{
                // Save settings to send
                rowValues.push($(this).text().trim());
            }
        });
        if(rowValues){
            // Safety way (Specific to Django)
            var csrftoken = getCookie('csrftoken');
            // Send settings to GA (views.py)
            $.ajax({
                url: 'Sim',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify({ 'settings_simulations': rowValues }),
                headers: { 'X-CSRFToken': csrftoken },
                error: function (xhr, status, error) {
                    console.error("AJAX request failed:", status, error);
                }
            })
        }
    });
}