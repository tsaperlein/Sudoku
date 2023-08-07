#!/bin/bash

# Check if the sudoku-solver executable exists
if [ ! -f sudoku-solver ]; then
    echo "sudoku-solver executable not found."
    exit 1
fi

if [ ! -f tests ]; then
    echo "tests directory not found."
    exit 1
fi

echo "5x5 puzzle test"
./sudoku-solver << EOF
$(cat tests/5x5_test.in)
EOF