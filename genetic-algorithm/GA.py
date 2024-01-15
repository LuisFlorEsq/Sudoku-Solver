from sudoku_function import *   # File that contains the objective functions to solve

from Population import *
from Chromosome import *
import matplotlib.pyplot as plt
import random

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

def genetic_Algorithm(mutation_rate_rows, mutation_rate_init, cross_rate, cross_rate_rows, function, tournament_size, elite_size, given_matrix):


    """
    Function to test the genetic algorithm, we will update the population until the stop criteria is reached
    """

    # Default parameters
    
    popsize = 150
    n = 9
    max_gens = 200
 
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
    
    # Print the sudoku puzzle

    print("Final sudoku puzzle: ")
    population.population[0].printChromosome()
    
    plot_metrics(worst, best, mean, generations+1)

    return 


seed_value = 2

np.random.seed(seed_value)
random.seed(seed_value)

 # Define the parameters

mutation_rate_rows = 0.3
mutation_rate_init = 0.05
cross_rate = 0.2
cross_rate_rows = 0.1
function = total_error
tournament_size = 2
elite_size = 50

# Given matrix
given_matrix = np.array([
[0, 0, 9, 0, 0, 0, 1, 0, 0],
[2, 1, 7, 0, 0, 0, 3, 6, 8],
[0, 0, 0, 2, 0, 7, 0, 0, 0],
[0, 6, 4, 1, 0, 3, 5, 8, 0],
[0, 7, 0, 0, 0, 0, 0, 3, 0],
[1, 5, 0, 4, 2, 8, 0, 7, 9],
[0, 0, 0, 5, 8, 9, 0, 0, 0],
[4, 8, 5, 0, 0, 0, 2, 9, 3],
[0, 0, 6, 3, 0, 2, 8, 0, 0]
])

genetic_Algorithm(mutation_rate_rows, mutation_rate_init, cross_rate, cross_rate_rows, function, tournament_size, elite_size, given_matrix)