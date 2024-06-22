# Description

A Sudoku puzzle solver (written in Python 3) which models and solves the puzzle as an integer linear programming (ILP) problem using the PuLP library.

This project explores various advanced methods to solve Sudoku puzzles and its variants, including Killer Sudoku, Greater-Than Sudoku, X-Sudoku, Hyper-Sudoku, Four-Pyramids Sudoku, and Sandwich Sudoku. Additionally, the solver leverages multiple advanced techniques and backtracking when necessary.

Basic Bibliography for (ILP) Sudoku Problem -> [Link](https://diego.assencio.com/?index=25ea1e49ca59de51b4ef6885dcc3ee3b)

# License

All code from this project is licensed under the GPLv3. See the [`LICENSE`](https://github.com/tsaperlein/Sudoku/blob/main/LICENSE) file for more information.

# Required modules

The `pulp` module is used. You can install it with the following command:

    pip3 install pulp==2.1

# Usage instructions

This projects illustrates how a Sudoku puzzle can be formulated as an integer
linear programming problem. It contains two main files:

- `sudoku.py`: a self-contained module with all the functionality needed to
  define and solve a puzzle
- `sudoku-solver`: an executable script which exemplifies how `sudoku.py` can
  be used to solve a puzzle.

By default, `sudoku-solver` takes its input from `stdin` and outputs the solved
puzzle on `stdout`. To solve a Sudoku puzzle, run `./sudoku-solver` and provide
the following:

- number of rows and columns on each puzzle block in one line (e.g. `2 3`)
- for each puzzle row, a line such as `_ _ _ 4 5 _` specifying the initial
  state of the row; initially unknown values can be represented using any
  non-integer character or string (e.g. `_`, `__`, `?` or `*`)

As an example, the following input specifies a puzzle with 2×3 blocks, i.e.,
each block contains 2 rows and 3 columns, and the puzzle contains 6 rows/columns
in total:

    2 3
    _ _ _ 2 _ _
    _ _ _ 4 5 _
    _ 3 4 _ _ _
    _ _ _ 1 4 _
    _ 6 1 _ _ _
    _ _ 5 _ _ _

The output is the solution to the puzzle:

    5 4 6 2 3 1
    2 1 3 4 5 6
    1 3 4 5 6 2
    6 5 2 1 4 3
    4 6 1 3 2 5
    3 2 5 6 1 4

# Solver Variants

The solver supports several Sudoku variants. Each variant is implemented in its respective script:

## 1. Killer Sudoku

### Rules:

Killer Sudoku combines elements of Sudoku and Kakuro. The grid contains cages outlined by dashed lines, with each cage having a target sum. The digits in each cage must sum to the target sum, and no digit can repeat within a cage.

### Example:

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Killersudoku_color.svg/1280px-Killersudoku_color.svg.png" alt="Killer Sudoku Example" width="500" height="500">

## 2. Greater-Than Sudoku

### Rules:

This variant adds inequality constraints between some adjacent cells. The symbols ‘>’ or ‘<’ between two cells indicate that one must be greater or less than the other.

### Example:

<img src="https://sudoku-puzzles.net/wp-content/puzzles/greater-than-sudoku/easy/1.png" alt="Greater Than Sudoku Example" width="500" height="500">

## 3. X-Sudoku

### Rules:

In addition to the standard rules of Sudoku, the diagonals of the grid must also contain the digits 1 to 9 without repetition.

### Example:

<img src="https://d3p4ev2sxj7kns.cloudfront.net/assets/images/help/xsudoku1.png" alt="X Sudoku Example" width="500" height="500">

## 4. Hyper-Sudoku

### Rules:

This variant includes additional regions (shaded or colored) that must also contain the digits 1 to 9 without repetition, typically overlapping with the standard 3x3 boxes.

### Example:

<img src="https://escape-sudoku.com/fmc/orig/1ca9/3cfa/2b15/hyper.webp" alt="Hyper Sudoku Example" width="500" height="500">

## 5. Four Pyramids Sudoku

### Rules:

Four additional triangular regions overlap with the standard Sudoku grid. Each of these triangular regions must also contain the digits 1 to 9 without repetition.

### Example:

<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjpEINO73V5GtPu8b653DZKSkPmKdbZhzFBaip5mdo2WPIUrIVJk-HEC5YoEQcwRA7N2t16_1JR1lrQoBwhYweHGjVDK6ECfbvAjqk-7qgrmOGxJZ8RrgNvfKK_43Og_X4Z1UCGoAkozGJ7/s1600/Pyramid+Sudoku+2013+-1.png" alt="Four Pyraminds Sudoku Example" width="500" height="500">

## 6. Sandwich Sudoku

### Rules:

In this variant, clues are given outside the grid indicating the sum of the digits located between the 1 and the 9 in that row or column.

### Example:

<img src="https://i0.wp.com/masteringsudoku.com/wp-content/uploads/2022/06/example-sandwich-sudoku-puzzle.png?resize=512%2C512&ssl=1" alt="Sandwich Sudoku Example" width="500" height="500">

# Advanced Techniques

The solver employs advanced techniques such as:

- Hidden Singles
- Constraint Satisfaction Problem (CSP)
- Intersection (Pointing Pairs)
- X-Wing
- Coloring
- Y-Wing
- Nice Chains
- Medusa 3D
- Backtracking (Brute Force)

# Difficulty Evaluation

The implementation can be achieved with machine learning by feeding the program known results and predicting random data. For this exercise, however, we rely on five different factors:

- Number of empty cells (30%).
- Number of candidates in empty cells after simple elimination (25%).
- The difference between the total number of candidates and the remaining candidates (20%).
- Time required to solve the puzzle (15%).
- Whether backtracking was used and how many times (10%).
- This process results in a score that determines the puzzle's difficulty level. The level with the highest score theoretically indicates the puzzle's difficulty.

# Solving Methodology (using advanced techniques)

The solver uses a systematic approach, starting with simple elimination and progressing through advanced methods. It continuously checks the number of solved cells and remaining candidates. If logic-based methods are insufficient, it resorts to backtracking. The solver prioritizes finding Hidden Singles and applies more complex methods as needed. The process continues until the puzzle is solved or no further progress is made.

## Puzzle Solving with Advanced Methods:

From the above example, we observe the following information:

- Time taken by the computer
- If backtracking was used, how much time it took and how many attempts were made
- Which methods were used
- Solution of the problem
- Estimated difficulty level of the puzzle

# Implementation with ASP

ASP (Answer Set Programming) is a powerful example of declarative programming used to solve various combinatorial problems, including Sudoku puzzles. In this chapter, we explore how ASP can be used to solve Sudoku puzzles and provide a brief explanation of the provided ASP code.

## Introduction to the ASP Sudoku Solver

Sudoku puzzles can be effectively solved using ASP, which allows us to define constraints and rules to solve the puzzle. The provided ASP code represents a Sudoku solver using the following elements:

### Definition of Constraints:

    #const num=3.
    #const n=num\*num.

These lines define constants for the puzzle size (num) and the total number of cells (n) in the Sudoku grid.

### Encoding the Initial State of the Puzzle:

    fixed(1,2,7). fixed(1,6,6). fixed(1,8,1).
    ... (other fixed values) ...

The fixed predicates encode the initial values of certain cells in the Sudoku grid. These represent the known or given numbers in the puzzle.

### Defining Value Assignments:

    1{value(I,J,X): X=1..n}1 :- I=1..n, J=1..n.

This ASP rule defines the possible value assignments (X) to each cell (I, J) in the grid. It enforces that each cell can only have one value between 1 and n.

### Same Box Constraint:

    sameBox(I1,J1,I2,J2) :- I1=1..n, J1=1..n, I2=1..n, J2=1..n, (I1-1)/num=(I2-1)/num, (J1-1)/num=(J2-1)/num.

The sameBox predicate identifies cells that are in the same box or square in the Sudoku grid. It ensures that two cells cannot have the same value if they are in the same box.

### General Constraints:

    :- sameBox(I1,J1,I2,J2), value(I1,J1,X), value(I2,J2,X), I1!=I2, J1!=J2.
    :- value(I,J1,X), value(I,J2,X), J1!=J2.
    :- value(I1,J,X), value(I2,J,X), I1!=I2.

These rules define general constraints for Sudoku puzzles. They enforce that no cell in the same box, row, or column can have the same value (X).

### Puzzle-Specific Constraints:

    :- value(I,J,X1), fixed(I,J,X2), X1!=X2.

This rule ensures that the value assigned to a cell (I, J) does not conflict with the fixed values provided in the initial state of the puzzle.

### Printing the Solution:

    #show value/3.

This line specifies what should be displayed as the solution. It prints the values assigned to cells in the solved Sudoku grid.

### Conclusion

ASP provides an elegant and declarative approach to solving Sudoku puzzles by encoding the constraints and rules of the puzzle. The provided ASP code effectively solves Sudoku puzzles by applying these constraints and generating valid solutions. This approach demonstrates the flexibility of ASP in tackling complex combinatorial problems.

# Program Usage Instructions

To run the program, use the command:

    ./sudoku

to see its options, or you can run the command:

    ./ilp-solvers/solver-name < full-file-name

to use each puzzle solver separately. For example, to use the Killer-Sudoku solver for the test3x3_1 file from the test files for Killer-Sudoku, execute the command:

    ./ilp-solvers/killer-sudoku < tests-ks/test3x3_1.in

**Note:** The above commands only apply to zshell, as Macs use bash scripts.

Continuing with the first method (through the interface), you will first encounter the following text, which will prompt you for input:

Choose one of the two options by typing:

    ilp

or

    method

Starting with Integer Linear Programming, the following solver options appear.

For each option, it will ask for the input file name that we want to pass as input to the program (only the file name, without the folder and without the .in extension). Move back with the input:

    exit

To use advanced methods, simply type:

    method

To use the program in ASP, simply type the command:

    clingo test3x3_1.asp

in the terminal.

If there are more than one cases, all results can be printed with the command:

    clingo --models=0 <file_name>

# Conclusion

Using Integer Linear Programming (ILP) with PuLP provides a systematic and efficient approach to solving various Sudoku puzzle variants. The provided Python code demonstrates how to create ILP formulations for different Sudoku variants and leverage PuLP to find solutions that satisfy all constraints. Whether it is a standard Sudoku, Killer Sudoku, or a more complex variant, the ILP approach with PuLP offers a flexible way to tackle these challenging puzzles. Additionally, there is no restriction for the Sudoku puzzle solver, so it can solve any valid puzzle, even 25x25 puzzles, with the only drawback being the solving time.

Finally, we observe from the three implementations of the Sudoku solver that the best time-wise is with the use of ASP, but the format of the result is quite obscure for the user as they do not see the grid clearly with the values.

# Bibliography

- Bartlett A.D., Chartier T.P., Langville A.N., Rankin T. An Integer Programming Model for the Sudoku Problem, J, Online Math. Applicat., vol. 8, 2008
- Simonis H., Sudoku as a Constraint Problem
- killersudokuonline.com, Killer Sudoku Killer Sudoku Online, 29-Sep-2012. Online. Available: http://killersudokuonline.com. Accessed: 30-Sep-2012
- https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=13c88d2af1dcf28e31b6b88024dcfbde6accdad8
- https://towardsdatascience.com/solve-sudoku-using-linear-programming-python-pulp-b41b29f479f3
- https://diego.assencio.com/?index=25ea1e49ca59de51b4ef6885dcc3ee3b
- https://towardsdatascience.com/using-integer-linear-programming-to-solve-sudoku-puzzles-15e9d2a70baa
- https://m.media-amazon.com/images/I/71Ncao-sOlL._AC_UF1000,1000_QL80_.jpg
- https://www.aapelivuorinen.com/blog/2023/01/18/killer-sudoku-mip/
- http://stuckinthecube.blogspot.com/2007/05/solving-greater-than-sudoku-puzzles.html
- https://www.sudokuonline.io/tips/sudoku-x-wing
- http://educ.jmu.edu/~taalmala/POW_spring2006/POW4.html
- https://dkmgames.com/SandwichSudoku/

# Contributors & Contact Information

Alexandros Tsaparas / tsaperlein@gmail.com
