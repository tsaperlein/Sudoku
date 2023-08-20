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
    
class Killer_Sudoku(Sudoku):
    def __init__(self, m, n, cages):
        super().__init__(m, n)  # Call the constructor of the base class
        self.cages = cages
        self.N = self.m * self.n  # Store N as an instance variable in Killer_Sudoku
        self.add_killer_constraints()

    def add_killer_constraints(self):
        for cage in self.cages:
            cage_cells = cage[0]
            cage_sum = cage[1]

            if len(cage_cells) == 1:
                i, j = cage_cells[0]
                self.sudoku_model += (pulp.lpSum([k * self.x[var_name(i, j, k)]
                                                 for k in crange(1, self.N)]) == cage_sum)
                continue

            self.sudoku_model += (pulp.lpSum([k * self.x[var_name(i, j, k)]
                                             for i, j in cage_cells
                                             for k in crange(1, self.N)]) == cage_sum)

            for i, j in cage_cells:
                self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                                  for k in crange(1, self.N)]) == 1)               