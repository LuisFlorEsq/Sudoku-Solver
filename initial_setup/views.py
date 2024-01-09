from django.shortcuts import render
from django.http import JsonResponse
import json
from sudoku import Sudoku
# from django.http import HttpResponse

# Upload all possible htmls with functions
def config(request):

    return render(request, 'views/config.html')

def sudoku_start(request):

    difficulty = request.GET.get('difficulty')
    
    sudoku_instance = Sudoku(difficulty=difficulty)

    if sudoku_instance.size_validator() == False:
        results = {'success': 0, 'message': 'El tamaño del sudoku no es de 9x9'}
    if sudoku_instance.rows_validate() == False:
        results = {'success': 0, 'message': 'No puede estar el mismo número dos veces en una fila'}
    if sudoku_instance.column_validate() == False:
        results = {'success': 0, 'message': 'No puede estar el mismo número dos veces en una columna'}
    if sudoku_instance.validate_cells() == False:
        results = {'success': 0, 'message': 'Ese número ya está en este cuadrante'}
    
    if sudoku_instance.size_validator() == True and sudoku_instance.rows_validate() == True and sudoku_instance.column_validate() == True and sudoku_instance.validate_cells() == True:
        results = {
            'mensaje': 'Sudoku cargado exitosamente',
            'tablero_sudoku': sudoku_instance.board
        }

    return JsonResponse(results)

def sudoku_Update(request):
    if request.method == 'GET':
        try:
            sudoku_values = request.GET.getlist('sudoku_values[]')
            print(sudoku_values)
            # Asegúrate de que `sudoku_values` es una lista de listas
            if isinstance(sudoku_values, list) and all(isinstance(row, list) for row in sudoku_values):
                # Crear una instancia de Sudoku
                sudoku_instance = Sudoku(board=sudoku_values)
                
                # Validar el Sudoku
                if not sudoku_instance.size_validator():
                    results = {'success': 0, 'message': 'El tamaño del sudoku no es de 9x9'}
                elif not sudoku_instance.rows_validate():
                    results = {'success': 0, 'message': 'No puede haber el mismo número dos veces en una fila'}
                elif not sudoku_instance.column_validate():
                    results = {'success': 0, 'message': 'No puede haber el mismo número dos veces en una columna'}
                elif not sudoku_instance.validate_cells():
                    results = {'success': 0, 'message': 'Ese número ya está en este cuadrante'}
                else:
                    results = {'success': 1, 'message': 'Sudoku válido'}
            else:
                results = {'success': 0, 'message': 'Los datos proporcionados no son válidos'}

        except Exception as e:
            results = {'success': 0, 'message': f'Error: {str(e)}'}

        return JsonResponse(results)
    else:
        return JsonResponse({'success': 0, 'message': 'La solicitud debe ser de tipo GET'})