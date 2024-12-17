#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <solver> <directory> <timeout>"
    exit 1
fi

# Get arguments
SOLVER=$1       # Path to the solver executable
DIRECTORY=$2    # Directory containing .cnf files
TIMEOUT=$3      # Timeout for each solver run (in seconds)
RESULT_FILE="res"
TEMP_FILE="temp"

# Clear the results file if it exists
> "$RESULT_FILE"
> "$TEMP_FILE"

# Determine if the solver is minisat
IS_MINISAT=$(basename "$SOLVER" | grep -i "minisat" | wc -l)

# Find all .cnf files, extract their numerical order, and sort them
FILES=$(find "$DIRECTORY" -type f -name "formula_*.cnf" | sed -E 's|.*/formula_([0-9]+)\.cnf$|\1 &|' | sort -n | cut -d' ' -f2)

# Iterate over all .cnf files in the directory
for FILE in $FILES; do
    if [ -f "$FILE" ]; then
        echo "Running solver on $FILE with timeout $TIMEOUT seconds..."
        if [ "$IS_MINISAT" -eq 1 ]; then
            # Run minisat directly
            timeout "$TIMEOUT" "$SOLVER" "$FILE" >> "$TEMP_FILE"
        else
            # Run the solver with python3
            timeout "$TIMEOUT" python3 "$SOLVER" "$FILE" >> "$RESULT_FILE"
        fi
        
        # Check if the timeout was reached
        if [ $? -eq 124 ]; then
            echo "Timeout reached for $FILE"
            echo "unkown" >> "$RESULT_FILE"
        fi
    fi
done

if [ "$IS_MINISAT" -eq 1 ]; then
    grep -E "SATISFIABLE|UNSATISFIABLE" "$TEMP_FILE" | \
    sed -e 's/UNSATISFIABLE/unsat/' -e 's/SATISFIABLE/sat/'  > "$RESULT_FILE"
fi 

rm "$TEMP_FILE"

echo "All results have been written to $RESULT_FILE."
