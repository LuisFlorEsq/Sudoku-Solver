import numpy as np
import random

# Create two matrix, one with all the numbers of the sudoku puzzle and another with the given-numbers

class Chromosome:
    
    def __init__(self, N, index, general_matrix=None, binary_matrix=None):
        
        self.elements = N
        self.index = index
        self.fitness = None
        self.values = np.arange(1, N+1)
        
        if general_matrix is not None:
            
            self.general_matrix = general_matrix
            
        if binary_matrix is not None:
            
            self.binary_matrix = binary_matrix
        
    
    def randomInitialize(self, given_numbers_matrix, function, index):
        
        """
        Create two matrices based on the given_numbers_matrix
        """
        
        N = given_numbers_matrix.shape[1] # Number of columns
        
        
        # Binary matrix
        
        binary_matrix = np.where(given_numbers_matrix != 0, 1, 0)
        
        # General matrix
        
        new_matrix = given_numbers_matrix.copy()
        
        values = self.values # All the possible values for the sudoku puzzle
        
        # Identify the established numbers
        
        
        for i in range(N): # Iterate over each row
            
            fixed_cols = np.where(new_matrix[i] != 0)[0]
#             print("Fixed cols", fixed_cols)
            
            # Generate values for the remaining values
            
            remaining_values = np.setdiff1d(values, new_matrix[i, fixed_cols])
            shuffled_values = np.random.permutation(remaining_values)
            
            # Assign the shuffled values to the corresponding columns
            
            new_matrix[i, new_matrix[i] == 0] = shuffled_values
        
        # Assign all the values
        
        self.index= index
        self.general_matrix = new_matrix
        self.binary_matrix = binary_matrix
        self.evaluateFunction(function)
        
            
    def printChromosome(self):
        
        """
        Print the Chromosome's elements
        """
        
        print("General matrix:")
        print(self.general_matrix)
        
#         print("Binary matrix:")
#         print(self.binary_matrix)
        
        print("Fitness:", self.fitness)
        print("Index:", self.index)
        
    
    def evaluateFunction(self, function):
        
        """
        Obtain the fitness value of the individual from the sudoku_function file
        """
        
        self.fitness = function(self.general_matrix, self.elements)
        
        
    def column_search(self):
        
        """
        Perform a local search among all the columns of the individual
        """
        
        
        # Obtain a set C, which will contain the illegal columns
        
        set_C = self.obtain_illegal_columns()
        
        for index_col in set_C:
            
#             current_column = self.general_matrix[:, index_col]
            index_other_col = random.choice(set_C)
#             other_column = self.general_matrix[:, index_other_col]
            self.swap_columns(index_col, index_other_col)
        
        
    def obtain_illegal_columns(self):

        """
        Obtain a set C which contain the illegal columns of the Chromosome
        """

        set_C = []

        # Iterate over each column

        for i in range(self.elements):

            # Get unique values and their counts for the current column

            unique_values, counts = np.unique(self.general_matrix[:, i], return_counts=True)

            # Check if the current column have any repeated values in the current column

            if np.any(counts > 1):

                set_C.append(i)

        return set_C
        
        
    def swap_columns(self, index1, index2):

        """
        Try to swap row elements on each illegal column
        """

        # Obtain the columns based on the indexes
        
        column1 = self.general_matrix[:, index1].copy()
        column2 = self.general_matrix[:, index2].copy()
        
#         print("Original columns")
#         print(column1)
#         print(column2)
        
        # Obtain the repeated values in each column
        
        values_column1 = np.where(np.bincount(column1) > 1)[0]
        values_column2 = np.where(np.bincount(column2) > 1)[0]
        
#         print("Values columns")
#         print(values_column1)
#         print(values_column2)

        
        # Obtain the indexes of repeated values in each column
        
        indexes_column1 = np.where(np.isin(column1, values_column1))[0]
        indexes_column2 = np.where(np.isin(column2, values_column2))[0]
        
#         print("Indexes columns")
#         print(indexes_column1)
#         print(indexes_column2)


        # Obtain the indexes that are in both repeated_column variables

        common_index = np.intersect1d(indexes_column1, indexes_column2)
#         print("Common_index")
#         print(common_index)


        for i in common_index:

            if ~np.isin(column1[i], column2) and ~np.isin(column2[i], column1):
                
                if self.binary_matrix[i, index1] != 1 and self.binary_matrix[i, index2] != 1:
                    

                    aux_value = column1[i]

                    column1[i] = column2[i]

                    column2[i] = aux_value
                
#                     print("Exchange performed")
#                     print(column1)
#                     print(column2)

#         print("Final Columns")
#         print(column1)
#         print(column2)

        self.general_matrix[:, index1] = column1
        self.general_matrix[:, index2] = column2
        
        
    def sub_Block_search(self):

        """
        Perform a local search among all the sub_blocks of the individual
        """

        # Obtain a set S, which will contain the illegal columns

        set_S = self.obtain_illegal_sublocks()

        for index_block in set_S:

            index_other_block = random.choice(set_S)
            self.swap_sub_Block(index_block, index_other_block)


    def obtain_illegal_sublocks(self):

        """
        Obtain a set S which contain the illegal sub_block of the Chromosome
        """

        set_S = []

        # Iterate over each sublock

        rows = columns = self.elements

        block_size = int(np.sqrt(self.elements))

        for i in range(0, rows, block_size):

            for j in range(0, columns, block_size):

                # Obtain the current sublock

                current_sublock = self.general_matrix[i:i+block_size, j:j+block_size]

                # Check if the current sublock is illegal

                unique_values, counts = np.unique(current_sublock, return_counts=True)

                if np.any(counts > 1):

                    set_S.append((i, j))

        return set_S



    def swap_sub_Block(self, indexes1, indexes2):

        """
        Try to swap row elements on each illegal sub-block
        """

        # Obtain the indexes of the two sub_blocks

        rows1, cols1 = indexes1
        rows2, cols2 = indexes2

        blocks_size = int(np.sqrt(self.elements))

        # Obtain the sub_blocks

        sub_block1 = self.general_matrix[rows1:rows1 + blocks_size, cols1:cols1 + blocks_size].copy()
        sub_block2 = self.general_matrix[rows2:rows2 + blocks_size, cols2:cols2 + blocks_size].copy()
        
#         print("Original sub_blocks")
#         print(sub_block1)
#         print(sub_block2)

        # Obtain the repeated values in each sub_block

        values_sub_block1 = np.where(np.bincount(sub_block1.flatten()) > 1)[0]
        values_sub_block2 = np.where(np.bincount(sub_block2.flatten()) > 1)[0]
        
#         print("Repeated values")
#         print(values_sub_block1)
#         print(values_sub_block2)

        # Obtain the indexes of repeated values in each sub-block

        indexes_sub_block1 = np.where(np.isin(sub_block1, values_sub_block1))
        indexes_sub_block2 = np.where(np.isin(sub_block2, values_sub_block2))

#         print("Indexes")
#         print(indexes_sub_block1[0])
#         print(indexes_sub_block1[1])
#         print(indexes_sub_block2[0])
#         print(indexes_sub_block2[1])
        
        for i in range(blocks_size):
            
            # Find row indices where they are equal to i
            indexes_rows1 = np.where(indexes_sub_block1[0] == i)[0]
            indexes_rows2 = np.where(indexes_sub_block2[0] == i)[0]

            # Corresponding column indices for indexes_sub_block1
            indexes_columns1 = indexes_sub_block1[1][indexes_rows1]

            # Corresponding column indices for indexes_sub_block2
            indexes_columns2 = indexes_sub_block2[1][indexes_rows2]

#             print("Rows")
#             print(indexes_rows1)
#             print(indexes_rows2)
#             print("Cols")
#             print(indexes_columns1)
#             print(indexes_columns2)

            if len(indexes_rows1) > 0 and len(indexes_rows2) > 0:
                
                for k in range(len(indexes_columns1)):
                    # Use k directly instead of trying to index with indexes_columns2[k]
                    
                    for j in range(len(indexes_columns2)):
                        
                        value1 = sub_block1[i, indexes_columns1[k]]
                        value2 = sub_block2[i, indexes_columns2[j]]
                        
                        # Obtain the original coordinates
                        
                        original1 = (rows1 + i, cols1 + indexes_columns1[k])
                        original2 = (rows2 + i, cols2 + indexes_columns2[j])

#                         print("Values")
#                         print(value1)
#                         print(value2)

                        if value2 not in sub_block1 and value1 not in sub_block2:
                            
                            if self.binary_matrix[original1] != 1 and self.binary_matrix[original2] != 1:
                            
                                sub_block1[i, indexes_columns1[k]] = value2
                                sub_block2[i, indexes_columns2[j]] = value1

#                                 print("Exchange performed")
#                                 print(sub_block1)
#                                 print(sub_block2)
                            
#         print("Final Sub_blocks")
#         print(sub_block1)
#         print(sub_block2)

        # Update the general_matrix with the modified sub_blocks
    
        self.general_matrix[rows1:rows1 + blocks_size, cols1:cols1 + blocks_size] = sub_block1
        self.general_matrix[rows2:rows2 + blocks_size, cols2:cols2 + blocks_size] = sub_block2