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
    var tablaHTML = '<table class="Settings" id="Settings"><thead><tr><th>Tasa_Muta_Fila</th><th>Tasa_Muta_Init</th><th>Tasa_Cruza</th><th>Tasa_Cruza_Fila</th><th>Tam_T</th><th>Elite_size</th><th>Pop_size</th><th>Max_Gens</th>';

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
            var table = $('.dff').text()
            if (table) {

                // Safety way (Specific to Django)
                var csrftoken = getCookie('csrftoken');
                // Send settings to GA (views.py)
                // Variable to get the sudoku table from html
                var sudoku_values = [];
                $('.sudoku-cell').each(function () {
                    var valor = $(this).text().trim() || 0;
                    sudoku_values.push(valor);
                });

                // Put all data in matrix 9x9 form
                var sudoku_matrix = [];
                for (var i = 0; i < 9; i++) {
                    var row_values = sudoku_values.slice(i * 9, (i + 1) * 9);
                    sudoku_matrix.push(row_values);
                }

                $.ajax({
                    url: 'Sim',
                    type: 'POST',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({ 'settings_simulations': rowValues, 'matrix': sudoku_matrix }),
                    headers: { 'X-CSRFToken': csrftoken },
                    success: function (response) {
                        console.log(response)
                        for (var i = 0; i < 9; i++) {
                            for (var j = 0; j < 9; j++) {
                                // Asigna el valor de la lista a la celda
                                $(".sudoku tr:eq(" + i + ") td:eq(" + j + ")").text(response.result[i][j]);
                            }
                        }

                        if (response.success === 1){
                            $.ajax({
                                url: 'UpSudo',
                                type: 'POST',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify({ 'sudoku_values': response.result }),
                                headers: { 'X-CSRFToken': csrftoken },
                                success: function (response) {
                                    
                                    if (response.success === 0){
                                        setTimeout(function(){
                                            Swal.fire({
                                            icon: "error",
                                            title: "Oops...",
                                            text: response.message});
                                            currentCell.empty();
                                        }, 100);
                                    }else if (response.success === 1){
                                        Swal.fire({
                                            icon: "success",
                                            title: "GENIAL!!!!",
                                            text: response.message
                                        });
                                    }
                                },
                                error: function (xhr, status, error) {
                                    console.error("AJAX request failed:", status, error);
                                }
                            });
                            
                        }else if (response.success === 0){
                            Swal.fire({
                            icon: "error",
                            title: "Oops...",
                            text: response.message});
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("AJAX request failed:", status, error);
                    }
                })
            }else{
                Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: 'Debes seleccionar una dificultad'});
            }
           
        }
    });
}