# Sudoku solver from https://onestepcode.com/

from copy import deepcopy
from typing import Callable
import numpy as np
import time

def get_subgrids(grid: np.ndarray) -> np.ndarray:
    """Divide the input grid into 9 3x3 sub-grids"""

    subgrids = []
    for box_i in range(3):
        for box_j in range(3):
            subgrid = []
            for i in range(3):
                for j in range(3):
                    subgrid.append(grid[3*box_i + i][3*box_j + j])
            subgrids.append(subgrid)
    return np.array(subgrids)


def get_candidates(grid : np.ndarray) -> list:
    """Get a list of candidates for each cell of the input grid"""

    def subgrid_index(i : int, j : int) -> int:
        return (i//3) * 3 + j // 3

    subgrids = get_subgrids(grid)
    grid_candidates = []
    for i in range(9):
        row_candidates = []
        for j in range(9):
            # Row, column and subgrid digits
            row = set(grid[i])
            col = set(grid[:, j])
            sub = set(subgrids[subgrid_index(i, j)])
            common = row | col | sub
            candidates = set(range(10)) - common
            # If the case is filled take its value as the only candidate
            if not grid[i][j]:
                row_candidates.append(list(candidates))
            else:
                row_candidates.append([grid[i][j]])
        grid_candidates.append(row_candidates)
    return grid_candidates


# Take shortest candidate list from inputs for each cell
def merge(candidates_1 : list, candidates_2 : list) -> list:
    candidates_min = []
    for i in range(9):
        row = []
        for j in range(9):
            if len(candidates_1[i][j]) < len(candidates_2[i][j]):
                row.append(candidates_1[i][j][:])
            else:
                row.append(candidates_2[i][j][:])
        candidates_min.append(row)
    return candidates_min


# Fill input grid's cells with single candidates
def fill_singles(grid : np.ndarray, candidates=None) -> np.ndarray:
    grid = grid.copy()
    if not candidates:
        candidates = get_candidates(grid)
    any_fill = True
    while any_fill:
        any_fill = False
        for i in range(9):
            for j in range(9):
                if len(candidates[i][j]) == 1 and grid[i][j] == 0:
                    grid[i][j] = candidates[i][j][0]
                    candidates = merge(get_candidates(grid), candidates)
                    any_fill = True
    return grid


# Verify the input grid has a possible solution
def is_valid_grid(grid : np.ndarray) -> bool:
    candidates = get_candidates(grid)
    for i in range(9):
        for j in range(9):
            if len(candidates[i][j]) == 0:
                return False
    return True


# Verify if the input grid is a solution
def is_solution(grid : np.ndarray) -> bool:
    if np.all(np.sum(grid, axis=1) == 45) and \
       np.all(np.sum(grid, axis=0) == 45) and \
       np.all(np.sum(get_subgrids(grid), axis=1) == 45):
        return True
    return False


# Filter input grid's list of candidates
def filter_candidates(grid : np.ndarray) -> list:
    test_grid = grid.copy()
    candidates = get_candidates(grid)
    filtered_candidates = deepcopy(candidates)
    for i in range(9):
        for j in range(9):
            # Check for empty cells
            if grid[i][j] == 0:
                for candidate in candidates[i][j]:
                    # Use test candidate
                    test_grid[i][j] = candidate
                    # Remove candidate if it produces an invalid grid
                    if not is_valid_grid(fill_singles(test_grid)):
                        filtered_candidates[i][j].remove(candidate)
                    # Revert changes
                    test_grid[i][j] = 0
    return filtered_candidates


# Fill next empty cell with least candidates with first candidate
def make_guess(grid : np.ndarray, solver : Callable, candidates=None) -> np.ndarray:
    grid = grid.copy()
    if not candidates:
        candidates = get_candidates(grid)
    # Getting the shortest number of candidates > 1:
    min_len = sorted(list(set(map(len, np.array(candidates, dtype=object).reshape(1, 81)[0]))))[1]
    for i in range(9):
        for j in range(9):
            if len(candidates[i][j]) == min_len:
                for guess in candidates[i][j]:
                    grid[i][j] = guess
                    solution = solver(grid)
                    if solution is not None:
                        return solution
                    # Discarding a wrong guess
                    grid[i][j] = 0


# Recursively find a solution filtering candidates
def filtered_solve(grid : np.ndarray) -> np.ndarray:
    candidates = filter_candidates(grid)
    grid = fill_singles(grid, candidates)
    if is_solution(grid):
        return grid
    if not is_valid_grid(grid):
        return None
    return make_guess(grid, filtered_solve, candidates)


# Recursively find a solution withouot filtering
def solve(grid : np.ndarray) -> np.ndarray:
    grid = fill_singles(grid)
    if is_solution(grid):
        return grid
    if not is_valid_grid(grid):
        return None
    return make_guess(grid, solve)


# Read input from stdin
def read_input() -> tuple:
    # Read only m*n + 1 lines
    m, n = map(int, input().split())
    
    # Read the board
    board = []
    for i in range(m*n):
        row = input().split()
        for j in range(m*n):
            if row[j] == "_" or row[j] == "0" or row[j] == "." or row[j] == "*" or row[j] == "?":
                row[j] = 0
            else:
                row[j] = int(row[j])
        board.append(row)
    
    return m, n, board

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    m, n, puzzle = read_input()
    
    # Convert the board to a numpy array
    puzzle = np.array(puzzle)
    
    # Solve the puzzles
    solution1 = solve(puzzle)
    print_board(solution1)
    
    solution2 = filtered_solve(puzzle)
    print(solution2)