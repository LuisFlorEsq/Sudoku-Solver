$(document).ready(function(){
    $('#Res_Sudoku').on('input', '.sudoku-cell', function(){
        try {
            var sudoku_values = [];
            $('.sudoku-cell').each(function () {
                var valor = $(this).text().trim() || 0;
                sudoku_values.push(valor);
            });

            var sudoku_data = JSON.stringify({ 'sudoku_values': [sudoku_values] });

            console.log("Sending AJAX request:", sudoku_data);  // Agregado para ver lo que se está enviando

            $.ajax({
                url: 'UpSudo',
                type: 'GET',
                data: { 'sudoku_values[]': sudoku_values },  // Ajusta esto según cómo estás pasando los valores en la solicitud GET
                success: function (response) {
                    console.log(response);
                    if (response.success === 0)
                        alert(response.message);
                },
                error: function (xhr, status, error) {
                    console.error("AJAX request failed:", status, error);
                }
            });
        } catch (error) {
            console.error("An error occurred:", error);
        }
    });
});
