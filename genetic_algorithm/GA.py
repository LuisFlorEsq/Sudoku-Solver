from .sudoku_function import *   # File that contains the objective functions to solve

import numpy as np
from .Population import *
from .Chromosome import *
import matplotlib.pyplot as plt
import time

seed_value = 2

np.random.seed(seed_value)
random.seed(seed_value)

def dibujar_sudoku(matriz_sudoku, matriz_binaria):
    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Dibujar el sudoku
    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        ax.axhline(i, color='black', lw=lw)
        ax.axvline(i, color='black', lw=lw)

    # Rellenar los valores del sudoku
    for i in range(9):
        for j in range(9):
            if matriz_sudoku[i, j] != 0:
                ax.text(j + 0.5, i + 0.5, str(matriz_sudoku[i, j]),
                        ha='center', va='center', fontsize=12, fontweight='bold')

    # Marcar en rojo los valores indicados por la matriz binaria
    for i in range(9):
        for j in range(9):
            if matriz_binaria[i, j] == 1:
                rect = plt.Rectangle((j, i), 1, 1, fill=None, edgecolor='red', linewidth=2)
                ax.add_patch(rect)

    # Configurar la apariencia
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)

    # Mostrar el sudoku
    plt.ion()  # Modo interactivo
    plt.show()
    plt.pause(5)
    plt.close()
    plt.ioff()  # Desactivar el modo interactivo después de su uso

def Marcar(matriz):

    # Crear una matriz para marc    ar las repeticiones con 'x'
    marcar_matriz = np.zeros_like(matriz, dtype=int)

    # Recorrer cada columna
    for col in range(matriz.shape[1]):
        # Encontrar los números que se repiten en la columna
        numeros_repetidos = [item for item in set(matriz[:, col]) if list(matriz[:, col]).count(item) > 1]
        
        # Marcar las posiciones de los números repetidos con 'x' en la matriz de marcado
        for num in numeros_repetidos:
            indices = np.where(matriz[:, col] == num)[0]
            marcar_matriz[indices, col] = 1

    # Recorrer cada cuadrante 3x3
    for fila in range(0, 9, 3):
        for col in range(0, 9, 3):
            # Encontrar los números que se repiten en el cuadrante
            numeros_repetidos = [item for item in set(matriz[fila:fila+3, col:col+3].flatten()) if list(matriz[fila:fila+3, col:col+3].flatten()).count(item) > 1]
            
            # Marcar las posiciones de los números repetidos con 'x' en la matriz de marcado
            for num in numeros_repetidos:
                indices = np.where(matriz[fila:fila+3, col:col+3].flatten() == num)[0]
                indices_fila, indices_col = np.unravel_index(indices, (3, 3))
                marcar_matriz[fila + indices_fila, col + indices_col] = 1
                
    return marcar_matriz

def Marcar(matriz):

    # Crear una matriz para marc    ar las repeticiones con 'x'
    marcar_matriz = np.zeros_like(matriz, dtype=int)

    # Recorrer cada columna
    for col in range(matriz.shape[1]):
        # Encontrar los números que se repiten en la columna
        numeros_repetidos = [item for item in set(matriz[:, col]) if list(matriz[:, col]).count(item) > 1]
        # Marcar las posiciones de los números repetidos con 'x' en la matriz de marcado
        for num in numeros_repetidos:
            indices = np.where(matriz[:, col] == num)[0]
            marcar_matriz[indices, col] = 1

    # Recorrer cada cuadrante 3x3
    for fila in range(0, 9, 3):
        for col in range(0, 9, 3):
            # Encontrar los números que se repiten en el cuadrante
            numeros_repetidos = [item for item in set(matriz[fila:fila+3, col:col+3].flatten()) if list(matriz[fila:fila+3, col:col+3].flatten()).count(item) > 1]
            # Marcar las posiciones de los números repetidos con 'x' en la matriz de marcado
            for num in numeros_repetidos:
                indices = np.where(matriz[fila:fila+3, col:col+3].flatten() == num)[0]
                indices_fila, indices_col = np.unravel_index(indices, (3, 3))
                marcar_matriz[fila + indices_fila, col + indices_col] = 1

    return marcar_matriz

def plot_metrics(worst, best, mean, generations):

    """
    This function takes three list with the worst, best and mean individuals of each generation and the number of generations

    """

    x = list(range(1, generations+1))
    plt.scatter(x, best, color='green', label='best')
    plt.plot(x, best, color='green')
    plt.scatter(x, worst, color='red', label='worst')
    plt.plot(x, worst, color='red')
    plt.scatter(x, mean, color='blue', label='mean')
    plt.plot(x, mean, color='blue')
    plt.legend()
    plt.xlabel('Generations')
    plt.ylabel('Fitness value')
    plt.title("Convergence graph")
    plt.show()
    

def genetic_Algorithm(mutation_rate_rows, mutation_rate_init, cross_rate, cross_rate_rows, tournament_size, elite_size, given_matrix, popsize, max_gens, function=total_error):

    """
    Function to test the genetic algorithm, we will update the population until the stop criteria is reached
    """

    print(given_matrix)
    # Default parameters
    n = 9
 
    # Initialize the stop variable as False and generations = 0


    generations = 0
    stop = False

    # Lits to save the metrics data

    worst = []
    mean = []
    best = []
    std = []

    
    # Initialize the population

    population = Population(popsize, n, given_matrix)
    population.initializePopulation(total_error)


#     population.printPopulation()


    # Obtain the metrics for the initial population
    print('-------------------')
    print("Initial population: ")
    print("Worst: ", population.worst())
    worst.append(population.worst())
    print("Best: ", population.best())
    best.append(population.best())
    print("Mean: ", population.meanFitness())
    mean.append(population.meanFitness())
    print("Standar Deviation: ", population.standarDeviation())
    std.append(population.standarDeviation())
    print('-------------------')


    # Update the population until the stop criteria is reached

    while generations < max_gens:

#         print("\nUpdating population:", generations)

        population.update_population(mutation_rate_rows, mutation_rate_init, cross_rate, cross_rate_rows, function, tournament_size, elite_size)
#             population.printPopulation()
#         print("\n")

        # Obtain the worst, best individual and the fitness mean of population

        worst_value = population.worst()
        best_value = population.best()
        mean_value = population.meanFitness()

        print('-------------------')
        print("Worst: ", worst_value)
        worst.append(worst_value)
        print("Best: ", best_value)
        best.append(best_value)
        print("Mean: ", mean_value)
        mean.append(mean_value)
        print('-------------------')

        generations += 1
        
        # Verify if the solution is found
        
        if population.best() == 0:
            break
    
        if generations % 10 == 0:
            chequeoM = population.population[0].general_matrix
            repetidos = Marcar(chequeoM)
            matriz_invertida = np.flipud(chequeoM)
            matriz_invertida_binaria = np.flipud(repetidos)

            dibujar_sudoku(matriz_invertida,matriz_invertida_binaria)

    # Obtain the final metrics and print it

    worst_value = population.worst()
    best_value = population.best()
    mean_value = population.meanFitness()
    deviation_value = population.standarDeviation()


    print('-------------------')
    print("Final results: ")
    print("Worst: ", worst_value)
    print("Best: ", best_value)
    print("Mean: ", mean_value)
    print("Standar Deviation: ", deviation_value)
    print('-------------------')
    
    # Print the solution and plot the metrics
    
    plot_metrics(worst, best, mean, generations+1)

    # Print the sudoku puzzle
    print("Final sudoku puzzle: ")
    return population.population[0].printChromosome()




#  # Define the parameters

# mutation_rate_rows = 0.3
# mutation_rate_init = 0.05
# cross_rate = 0.2
# cross_rate_rows = 0.1
# function = total_error
# tournament_size = 2
# elite_size = 50

# # Given matrix
# given_matrix = np.array([
# [0, 0, 9, 0, 0, 0, 1, 0, 0],
# [2, 1, 7, 0, 0, 0, 3, 6, 8],
# [0, 0, 0, 2, 0, 7, 0, 0, 0],
# [0, 6, 4, 1, 0, 3, 5, 8, 0],
# [0, 7, 0, 0, 0, 0, 0, 3, 0],
# [1, 5, 0, 4, 2, 8, 0, 7, 9],
# [0, 0, 0, 5, 8, 9, 0, 0, 0],
# [4, 8, 5, 0, 0, 0, 2, 9, 3],
# [0, 0, 6, 3, 0, 2, 8, 0, 0]
# ])


# print(genetic_Algorithm(mutation_rate_rows, mutation_rate_init, cross_rate, cross_rate_rows, function, tournament_size, elite_size, given_matrix))