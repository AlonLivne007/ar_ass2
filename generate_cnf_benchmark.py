import os
import random

# פונקציה ליצירת פסוקית עם 3 ליטרלים ייחודיים
def generate_clause(num_vars):
    clause = set()
    while len(clause) < 3:
        literal = random.randint(1, num_vars)  # בחר משתנה
        literal *= random.choice([-1, 1])  # שלילה או לא
        clause.add(literal)
    return tuple(sorted(clause))  # המרת ליטרלים לפסוקית ייחודית

# פונקציה ליצירת קובץ CNF
def create_cnf_file(file_path, num_vars, num_clauses):
    clauses = set()
    while len(clauses) < num_clauses:
        clause = generate_clause(num_vars)
        clauses.add(clause)

    with open(file_path, "w") as f:
        # כתיבת כותרת הקובץ לפי פורמט DIMACS
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

# הגדרות
OUTPUT_DIR = "benchmark"
NUM_FILES = 100
NUM_VARS = 50
PHASE_TRANSITION_RATIO = 4.3  # יחס ההעברה לפי מה שראינו בתרגול
NUM_CLAUSES = int(NUM_VARS * PHASE_TRANSITION_RATIO)

# יצירת התיקייה אם לא קיימת
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# יצירת 100 קבצים
for i in range(1, NUM_FILES + 1):
    file_name = f"formula_{i}.cnf"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    create_cnf_file(file_path, NUM_VARS, NUM_CLAUSES)
    print(f"נוצר קובץ: {file_path}")

print("סיום יצירת הקבצים!")
