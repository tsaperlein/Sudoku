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
                
class X_Sudoku(Sudoku):
    def __init__(self, m, n):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Killer_Sudoku
        self.add_x_sudoku_constraints()
        
    def add_x_sudoku_constraints(self):
        # The values of each diagonal must be different (from 0 to 9)
        for k in crange(1, self.N):
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, i, k)]
                                              for i in crange(1, self.N)]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, self.N - i + 1, k)]
                                              for i in crange(1, self.N)]) == 1)
    
class Hyper_Sudoku(Sudoku):
    def __init__(self, m, n):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Killer_Sudoku
        self.add_hyper_sudoku_constraints()
        
    def add_hyper_sudoku_constraints(self):
        for k in crange(1, self.N):
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i in crange(2, 4)
                                              for j in crange(2, 4)]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i in crange(2, 4)
                                              for j in crange(6, 8)]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i in crange(6, 8)
                                              for j in crange(2, 4)]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i in crange(6, 8)
                                              for j in crange(6, 8)]) == 1)
            
class Four_Pyramids_Sudoku(Sudoku):
    def __init__(self, m, n):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Killer_Sudoku
        self.add_four_pyramids_sudoku_constraints()
        
    def add_four_pyramids_sudoku_constraints(self):
        for k in crange(1, self.N):
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i, j in [(2,1), (3,1), (3,2), (4,1), (4,2), (4,3), (5,1), (5,2), (6,1)]]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i, j in [(1,4), (1,5), (2,5), (1,6), (2,6), (3,6), (1,7), (2,7), (1,8)]]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i, j in [(9,2), (9,3), (8,3), (9,4), (8,4), (7,4), (9,5), (8,5), (9,6)]]) == 1)
            self.sudoku_model += (pulp.lpSum([self.x[var_name(i, j, k)]
                                              for i, j in [(8,9), (7,9), (7,8), (6,9), (6,8), (6,7), (5,9), (5,8), (4,9)]]) == 1)
            
class Sandwich_Sudoku(Sudoku):
    def __init__(self, m, n, constraints):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Killer_Sudoku
        self.constraints = constraints
        self.add_sandwich_sudoku_constraints()
        
    def add_sandwich_sudoku_constraints(self):
        """The constraints are in the format:
        ['0', '0', '5', '0', '0', '7', '17', '13', '2']
        ['2', '11', '16', '20', '35', '6', '4', '2', '4']
        
        The first list is for the rows and the second for the columns.
        
        Each number in the list is the sum of the numbers that are between the cell with the number 1 and the cell with the number 9.
        """ 
        