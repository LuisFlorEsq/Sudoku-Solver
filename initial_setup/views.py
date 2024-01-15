from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from sudoku import Sudoku
# from django.http import HttpResponse

# Upload all possible htmls with functions
def config(request):

    return render(request, 'views/config.html')

def sudoku_start(request):

    difficulty = request.GET.get('difficulty')
    board = request.GET.get('num_board')
    
    sudoku_instance = Sudoku(difficulty=difficulty, n_board=int(board))

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
            'tablero_sudoku': sudoku_instance.board.tolist()
        }

    return JsonResponse(results)

def sudoku_Update(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        sudoku_matrix = data.get('sudoku_values')
        # Hacer de una lista de string a una lista de ints
        sudoku_matrix = [[int(value) for value in row] for row in sudoku_matrix]
        # Crear una instancia de Sudoku
        sudoku_instance = Sudoku(board=sudoku_matrix)
        
        # Validar el Sudoku
        if not sudoku_instance.size_validator():
            results = {'success': 0, 'message': 'El tamaño del sudoku no es de 9x9'}
        elif not sudoku_instance.rows_validate():
            print(sudoku_instance.rows_validate())
            results = {'success': 0, 'message': 'No puede haber el mismo número dos veces en una fila'}
        elif not sudoku_instance.column_validate():
            results = {'success': 0, 'message': 'No puede haber el mismo número dos veces en una columna'}
        elif not sudoku_instance.validate_cells():
            results = {'success': 0, 'message': 'Ese número ya está en este cuadrante'}
        else:
            ceros_count = sum(1 for row in sudoku_instance.board.tolist() for value in row if value == 0)
            if ceros_count == 0:
                results = {'success': 1, 'message': 'HAS GANADO EL SUDOKU!!!!'}
            else:
                results = {'success': 2, 'message': 'Sudoku válido'}
            ceros_count = 0

    except Exception as e:
        results = {'success': 0, 'message': f'Error: {str(e)}'}

    return JsonResponse(results)

def start_simulation(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        settings = data.get('settings_simulations')
        print(settings)

        return JsonResponse({'status': 'OK'})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)