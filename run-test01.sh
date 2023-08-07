#!/bin/bash

while true; do
    read -p "Enter the name of a .in file (or 'exit' to quit): " input_name

    if [ "$input_name" = "exit" ]; then
        echo "Exiting the script."
        break
    fi

    input_file="$input_name.in"

    if [ ! -f "tests/$input_file" ]; then
        echo "File $input_file not found."
    else
        # Check if the sudoku-solver executable exists
        if [ ! -f sudoku-solver ]; then
            echo "sudoku-solver executable not found."
            exit 1
        fi

        solution=$(./sudoku-solver < "tests/$input_file")

        echo -e "\n- Running $input_file"
        echo -e "Solution:"
        echo "$solution"

        output_file="${input_file%.in}.out"
        if [ ! -f "tests/$output_file" ]; then
            echo -e "\nFile $output_file not found, so it is created."
        fi

        echo "$solution" > "tests/$output_file"
        echo -e " "
    fi
done