
$(document).ready(function () {
    $(".difficulty-btn").click(function () {
        var difficulty = $(this).data("difficulty");
        $('.dff').html(difficulty);
        board = $('.Boards').val()

        $.ajax({
            url: "Sudoku",
            type: "GET",
            data: { difficulty: difficulty, num_board: board },
            success: function(response) {
                if (response.success == 0)
                    alert(response.message)
                else{
                    var sudokuBoard = response.tablero_sudoku;
                    var table = '<table class="sudoku"><tbody>'
                    for (var row = 0; row < 9; row++){
                        table += '<tr>'
                        for (var column = 0; column < 9; column++){
                            if (sudokuBoard[row][column] == 0)
                            table += '<td class="sudoku-cell" contenteditable="true" onkeypress="return checkN(event)" oninput="limitarCaracteres(this,1);"></td>'
                            else
                                table += '<td class="sudoku-cell non-editable">' + sudokuBoard[row][column] + '</td>'
                        }
                        table += '</tr>'
                    }
                    table += '</tbody></table>'

                    $('#Res_Sudoku').html(table)
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        // $('.Boards').prop('disabled', 'disabled')
    });
});