import os
import random

# Function to create a clause with 3 unique literals
def generate_clause(num_vars):
    clause = set()
    while len(clause) < 3:
        literal = random.randint(1, num_vars)  # Choose a variable
        literal *= random.choice([-1, 1])  # Negate or not
        clause.add(literal)
    return tuple(sorted(clause))  # Convert literals to a unique clause

# Function to create a CNF file
def create_cnf_file(file_path, num_vars, num_clauses):
    clauses = set()
    while len(clauses) < num_clauses:
        clause = generate_clause(num_vars)
        clauses.add(clause)

    with open(file_path, "w") as f:
        # Write the file header in DIMACS format
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

# Settings
OUTPUT_DIR = "benchmark"
NUM_FILES = 100
NUM_VARS = 50
NUM_CLAUSES = 222  # Total clauses (fixed value)

# Create the output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Generate 100 files
for i in range(1, NUM_FILES + 1):
    file_name = f"formula_{i}.cnf"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    create_cnf_file(file_path, NUM_VARS, NUM_CLAUSES)
    print(f"File created: {file_path}")

print("Finished creating files!")
