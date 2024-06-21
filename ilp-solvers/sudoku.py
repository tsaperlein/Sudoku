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
                

class Greater_Than_Sudoku(Sudoku):
    def __init__(self, m, n, cages):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Greater_Than_Sudoku
        self.cages = cages
        self.possible_values = {}  # Initialize possible values as a dictionary

    def assign_possible_values(self):
        """
        Assign initial possible values for each cell in the Sudoku grid.
        Each cell can initially hold any value from 1 to N.
        """
        for i in crange(1, self.N):
            for j in crange(1, self.N):
                self.possible_values[(i, j)] = set(crange(1, self.N))
                
    def erase_possible_values(self):
        """
        Adjust the possible values for each cell based on the greater-than constraints.
        This function ensures that the values in the pairs of cells defined by the cages
        satisfy the greater-than relationship.
        """
        for cage in self.cages:
            i1, j1, i2, j2 = cage
            i1, j1, i2, j2 = int(i1), int(j1), int(i2), int(j2)
            
            if self.get_cell_value(i1, j1) is not None:
                # Erase the values of the second cell that are >= the value of the first cell
                value_i1_j1 = self.get_cell_value(i1, j1)
                self.possible_values[(i2, j2)] -= set(crange(value_i1_j1, self.N))
                return True
            
            elif self.get_cell_value(i2, j2) is not None:
                # Erase the values of the first cell that are <= the value of the second cell
                value_i2_j2 = self.get_cell_value(i2, j2)
                self.possible_values[(i1, j1)] -= set(crange(1, value_i2_j2))
                return True
            
            elif self.get_cell_value(i1, j1) is not None and self.get_cell_value(i2, j2) is not None:
                # Find the lowest value of the second cell
                lowest_value_i2_j2 = min(self.possible_values[(i2, j2)])
                
                # Find the highest value of the first cell
                highest_value_i1_j1 = max(self.possible_values[(i1, j1)])
                
                # Erase the values of the first cell that are <= the lowest value of the second cell
                self.possible_values[(i1, j1)] -= set(crange(1, lowest_value_i2_j2))
                
                # Erase the values of the second cell that are >= the highest value of the first cell
                self.possible_values[(i2, j2)] -= set(crange(highest_value_i1_j1, self.N))
                return True
            
            else:    
                return False
                
                    
    def solve(self):
        self.assign_possible_values()
        self.erase_possible_values()
        
        # While there is a cell with 2 or more possible values then continue running the loop
        while any(len(self.possible_values[(i, j)]) > 1 for i in crange(1, self.N) for j in crange(1, self.N)):
            print(self.possible_values)
            if not self.erase_possible_values():
                exit(1)
            
        # If there is a cell with no possible values then the puzzle is not valid
        if any(len(self.possible_values[(i, j)]) == 0 for i in crange(1, self.N) for j in crange(1, self.N)):
            return False
            
        # Assign the values to the cells
        for i in crange(1, self.N):
            for j in crange(1, self.N):
                if len(self.possible_values[(i, j)]) == 1:
                    self.set_cell_value(i, j, list(self.possible_values[(i, j)])[0])
            
                
class X_Sudoku(Sudoku):
    def __init__(self, m, n):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in X_Sudoku
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
        self.N = self.m * self.n  # Store N as an instance variable in Hyper_Sudoku
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
        self.N = self.m * self.n  # Store N as an instance variable in Four_Pyramids_Sudoku
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
    """
    The Sandwich_Sudoku class extends the standard Sudoku puzzle by adding constraints that ensure the sum of the numbers between the digits 1 and 9 in each row and column matches specified values. The class performs this by:

    - Initializing the Sudoku grid. (Αρχικοποίηση)
    - Retrieving and verifying the positions of 1 and 9. (Βρισκειί/Επιβεβαιώνει τις θέσεις του 1 και 9)
    - Calculating the sum of digits between 1 and 9. (Βρίσκει τα αθροίσματα)
    - Ensuring these sums match the provided constraints. (Ελέγχει τους αντίστοιχους περιορισμούς)

    If any of these conditions are not met, the class raises an error, enforcing the sandwich constraints on the puzzle.
    """
    def __init__(self, m, n, constraints):
        super().__init__(m, n)  # Call the constructor of the base class
        self.N = self.m * self.n  # Store N as an instance variable in Sandwich_Sudoku
        self.constraints = constraints
        self.add_sandwich_sudoku_constraints()
        
    def add_sandwich_sudoku_constraints(self):
        for i in range(self.N):
            row_constraint = int(self.constraints[0][i])
            col_constraint = int(self.constraints[1][i])
            
            # Find the positions of 1 and 9 in each row and column
            row_1_pos = -1
            row_9_pos = -1
            col_1_pos = -1
            col_9_pos = -1
            
            for j in range(self.N):
                for k in range(1, self.N + 1):
                    if self.x[var_name(i + 1, j + 1, k)].value() == 1:
                        if k == 1:
                            row_1_pos = j + 1
                        elif k == 9:
                            row_9_pos = j + 1

                    if self.x[var_name(j + 1, i + 1, k)].value() == 1:
                        if k == 1:
                            col_1_pos = j + 1
                        elif k == 9:
                            col_9_pos = j + 1
            
            if row_1_pos == -1 or row_9_pos == -1:
                raise ValueError(f"Row {i} does not contain exactly one 1 and one 9.")
            if col_1_pos == -1 or col_9_pos == -1:
                raise ValueError(f"Column {i} does not contain exactly one 1 and one 9.")
            
            if row_1_pos < row_9_pos:
                row_sum = sum(int(self.x[var_name(i + 1, j, k)].value()) for j in range(row_1_pos + 1, row_9_pos) for k in range(2, 9))
            else:
                row_sum = sum(int(self.x[var_name(i + 1, j, k)].value()) for j in range(row_9_pos + 1, row_1_pos) for k in range(2, 9))
            
            if col_1_pos < col_9_pos:
                col_sum = sum(int(self.x[var_name(j, i + 1, k)].value()) for j in range(col_1_pos + 1, col_9_pos) for k in range(2, 9))
            else:
                col_sum = sum(int(self.x[var_name(j, i + 1, k)].value()) for j in range(col_9_pos + 1, col_1_pos) for k in range(2, 9))
            
            if row_sum != row_constraint:
                raise ValueError(f"Row {i} constraint violated: Sum between 1 and 9 is not equal to {row_constraint}")
            if col_sum != col_constraint:
                raise ValueError(f"Column {i} constraint violated: Sum between 1 and 9 is not equal to {col_constraint}")