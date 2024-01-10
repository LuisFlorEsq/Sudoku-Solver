# Functions to calculate the fitness value of the individual


import numpy as np

# The fitness function will be aboard from a minimization criteria

# The sudoku rules are the following:
# 1. A sudoku puzzle has only one unique solution
# 2. Rule of rows: All 1 to N numbers in each row should appear and not be repeated
# 3. Rule of columns: All 1 to N numbers in each column should appear and not be repeated
# 4. The rule of subclocks: All 1 to N numbers in each N^(1/2) X N^(1/2) subclock should appear and not should be repeated


def count_incorrectCols(sudoku_matrix, N):
    """
    Count the total number of columns that not satisfies the sudoku rule

    Args:
        sudoku_matrix (_numpy-array_): The sudoku representation as a NxN matrix
        N (_int_): The number of rows and columns of the sudoku
    """
    
    # Since the sudoku is a NxN matrix it has the same number of rows and columns
    
    rows = columns = N
    count_incorrect = 0
    
    for i in range(columns):
        
        column_values = sudoku_matrix[i, rows-1]
        unique_values, counts = np.unique(column_values, return_counts=True)
        
        if np.any(counts > 1):
            
            count_incorrect +=1
    
    # for i in columns:
        
    #     aux_array = np.array([])
        
    #     for j in rows:
            
    #         current_value = sudoku_matrix[i, j]
            
    #         # Check if the current value is in the sudoku matrix if not add it to the aux_array
            
    #         if not current_value in aux_array:
                
    #             aux_array = np.append(aux_array, current_value)
            
    #         else:
                
    #             count_incorrect += 1
                
    #             break
            
    return count_incorrect


def count_incorrectSub(sudoku_matrix, N):
    
    """
    Count the total number of sublocks that not satisfies the sudoku rule
    
    
    Args:
        sudoku_matrix (_numpy-array_): The sudoku representation as a NxN matrix
        N : (_int_): The number of rows and columns of the sudoku
    """
    
    
    rows = columns = N
    count_incorrect = 0
    
    
    # Obtain the square root of the sudoku
    
    block_size = int(np.sqrt(N))
    
    rows_block = columns_block = block_size
    
    
    # Iterate over each sublock
    
    for i in range(0, rows, rows_block):
        
        for j in range(0, columns, columns_block):
            
            # Obtain the current sublock
            
            current_sublock = sudoku_matrix[i:i+rows_block, j:j+columns_block]
            
            if not check_sublock(current_sublock):
                
                count_incorrect +=1
            
    return count_incorrect
            


def check_sublock(current_sublock):
    """
    Check if there are repeated values in the current_sublock

    Args:
        current_sublock (_numpy-array_): _The current sublock in _
    """
        
    # Decompose the sublock into a uni-dimensional list
        
    list_block = current_sublock.flatten()
    
    aux_array = np.array([])
    
    for value in list_block:
        
        if value in aux_array:
            
            return False # Duplicate found
        
        else:
            
            aux_array = np.append(aux_array, value)
            
    return True # Not duplicates found


def total_error(sudoku_matrix, N):
    
    """
    Calculate the total error in the sudoku puzzle by count the incorrect_columns, and incorrect_sublocks
    """
    
    total_error = 0
    
    # Call each method to obtain the errors
    
    cols_error = count_incorrectCols(sudoku_matrix, N)
    blocks_error = count_incorrectSub(sudoku_matrix, N)
    
    # Obtain the total error
    
    total_error = cols_error + blocks_error
    
    return total_error