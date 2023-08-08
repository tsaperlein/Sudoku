#!/usr/bin/env python3

import pulp

# Returns a string in the format x_{i,j,k}.
def var_name(i, j, k):
    return "x_{%d,%d,%d}" % (i, j, k)

# Returns a range object for the closed interval [a,b].
def crange(a, b):
    return range(a, b + 1)

class Sudoku:
    
    # Initializes a solver for a Sudoku puzzle with block size m×n.
    def __init__(self, m, n):
        """
        m: The number of rows per puzzle block.
        n: The number of columns per puzzle block.
        """
        
        self.m = m
        self.n = n

        N = m * n

        # Initialize the Sudoku model
        self.sudoku_model = pulp.LpProblem("Sudoku", pulp.LpMinimize)

        # Define the names of all associated ILP problem variables
        """
        i: The row index of the cell.
        j: The column index of the cell.
        k: The value of the cell.
        """
        x_names = [var_name(i, j, k)
                   for i in crange(1, N)
                   for j in crange(1, N)
                   for k in crange(1, N)]

        # Create a dictionary with all the needed variables x_{i,j,k}
        self.x = pulp.LpVariable.dict("%s",
                                      x_names,
                                      lowBound=0,
                                      upBound=1,
                                      cat=pulp.LpInteger)
        
        # Define the objective function
        self.sudoku_model += 0
        
        """ CONSTRAINTS """
        # Add the constraints for the rows (each value k must appear exactly once)
        for i in crange(1, N):
            for k in crange(1, N):
                self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                  for j in crange(1, N)]) == 1)
                
        # Add the constraints for the columns (each value k must appear exactly once)
        for j in crange(1, N):
            for k in crange(1, N):
                self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                  for i in crange(1, N)]) == 1)
                
        # Add the constraints for the cells (each cell must contain exactly one value)
        for i in crange(1, N):
            for j in crange(1, N):
                self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                  for k in crange(1, N)]) == 1)
                
        # Each value k appears exactly once in each block (I,J)
        for I in crange(1, n):
            for J in crange(1, m):

                i_low = (I - 1) * m + 1
                j_low = (J - 1) * n + 1
                block_i_values = range(i_low, i_low + m)
                block_j_values = range(j_low, j_low + n)

                for k in crange(1, N):
                    self.sudoku_model += sum([self.x[var_name(i, j, k)]
                                              for i in block_i_values
                                              for j in block_j_values]) == 1
        
    # Sets the value of cell (i,j) to k.
    def set_cell_value(self, i, j, k):
        """
        This function will throw a RuntimeError exception if called
        after the puzzle has already been solved.
        """
        
        if self.sudoku_model.status != pulp.LpStatusNotSolved:
            raise RuntimeError("Puzzle has already been solved.")

        self.sudoku_model += self.x[var_name(i, j, k)] == 1
            
    # Returns the value of cell (i,j) or None if the puzzle has not yet been solved.    
    def get_cell_value(self, i, j):
        N = self.size()
        
        for k in crange(1, N):
            if self.x[var_name(i, j, k)].value() == 1:
                return k
        return None
    
    # Solves the puzzle and returns True if the puzzle is solvable, False otherwise.
    def solve(self):
        status = self.sudoku_model.solve()
        return status == pulp.LpStatusOptimal

    # Returns the number of rows/columns in the puzzle.
    def size(self):
        return self.m * self.n
    
class Killer_Sudoku:
        
        # Initializes a solver for a Killer Sudoku puzzle with block size m×n.
        def __init__(self, m, n, cages):
            """
            m: The number of rows per puzzle block.
            n: The number of columns per puzzle block.
            N: The number of rows/columns in the puzzle.
            cages: A list of tuples (C, s) where C is a list of tuples (i, j) 
                   representing the cells in the cage and s is the sum of the cage.
            """
            
            self.m = m
            self.n = n
            N = m * n
            self.cages = cages
    
            # Initialize the Killer Sudoku model
            self.killer_model = pulp.LpProblem("Killer Sudoku", pulp.LpMinimize)
    
            # Define the names of all associated ILP problem variables
            """
            i: The row index of the cell.
            j: The column index of the cell.
            k: The value of the cell.
            """
            x_names = [var_name(i, j, k)
                    for i in crange(1, N)
                    for j in crange(1, N)
                    for k in crange(1, N)]
    
            # Create a dictionary with all the needed variables x_{i,j,k}
            self.x = pulp.LpVariable.dict("%s",
                                        x_names,
                                        lowBound=0,
                                        upBound=1,
                                        cat=pulp.LpInteger)
            
            # Define the objective function
            self.killer_model += 0
            
            """ CONSTRAINTS """
            # Add the constraints for the cages (the sum of the values in each cell of the cage must be equal to the cage sum)
            # each cage is a list of tuples (i, j) representing the cells in the cage and s is the sum of the cage.
            for cage in self.cages:
                cage_cells = cage[0]
                cage_sum = cage[1]
                
                # If the cage has only one cell, then give the value of the cage sum to that cell
                if len(cage_cells) == 1:
                    i, j = cage_cells[0]
                    self.killer_model += (pulp.lpSum([k * self.x[var_name(i, j, k)]
                                                    for k in crange(1, N)]) == cage_sum)
                    continue
                
                # Check if the sum of the k values of the cells in the cage is equal to the cage sum
                self.killer_model += (pulp.lpSum([k * self.x[var_name(i, j, k)]
                                                    for i, j in cage_cells
                                                    for k in crange(1, N)]) == cage_sum)
                
                # If all the cells have k values and the sum of their k values is not equal to the cage sum, then replace the k values with "_" (empty cell)
                for i, j in cage_cells:
                    self.killer_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                    for k in crange(1, N)]) == 1)
            
            # Add the constraints for the rows (each value k must appear exactly once)
            for i in crange(1, N):
                for k in crange(1, N):
                    self.killer_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                    for j in crange(1, N)]) == 1)
                    
            # Add the constraints for the columns (each value k must appear exactly once)
            for j in crange(1, N):
                for k in crange(1, N):
                    self.killer_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                    for i in crange(1, N)]) == 1)
                    
            # Add the constraints for the cells (each cell must contain exactly one value)
            for i in crange(1, N):
                for j in crange(1, N):
                    self.killer_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                    for k in crange(1, N)]) == 1)
                    
            # Each value k appears exactly once in each block (I,J)
            for I in crange(1, n):
                for J in crange(1, m):

                    i_low = (I - 1) * m + 1
                    j_low = (J - 1) * n + 1
                    block_i_values = range(i_low, i_low + m)
                    block_j_values = range(j_low, j_low + n)

                    for k in crange(1, N):
                        self.killer_model += sum([self.x[var_name(i, j, k)]
                                                for i in block_i_values
                                                for j in block_j_values]) == 1
                        
        
        # Sets the value of cell (i,j) to k.            
        def set_cell_value(self, i, j, k):
            if self.killer_model.status != pulp.LpStatusNotSolved:
                raise RuntimeError("Puzzle has already been solved.")
    
            self.killer_model += self.x[var_name(i, j, k)] == 1
            
        # Returns the value of cell (i,j) or None if the puzzle has not yet been solved.
        def get_cell_value(self, i, j):
            N = self.m * self.n  # Use N instead of self.N
            for k in crange(1, N):
                if self.x[var_name(i, j, k)].value() == 1:
                    return k
            return None
    
        # Solves the puzzle and returns True if the puzzle is solvable, False otherwise.
        def solve(self):
            status = self.killer_model.solve()
            return status == pulp.LpStatusOptimal
        
        # Returns the number of rows/columns in the puzzle.
        def size(self):
            return self.m * self.n