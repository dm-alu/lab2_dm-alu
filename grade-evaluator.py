import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """Validate the data, compute GPA, decide pass/fail, and find resubmissions."""
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: no assignment records found.")
        return

    # a) Grade validation: every score must be within 0-100
    invalid = [a for a in data if not 0 <= a['score'] <= 100]
    if invalid:
        for a in invalid:
            print(f"Invalid score for '{a['assignment']}': {a['score']} (must be 0-100)")
        return

    # b) Weight validation: total=100, Summative=40, Formative=60
    total_weight = sum(a['weight'] for a in data)
    formative = [a for a in data if a['group'].strip().lower() == 'formative']
    summative = [a for a in data if a['group'].strip().lower() == 'summative']
    f_weight = sum(a['weight'] for a in formative)
    s_weight = sum(a['weight'] for a in summative)

    errors = []
    if abs(total_weight - 100) > 1e-9:
        errors.append(f"Total weight is {total_weight:g}, expected 100")
    if abs(s_weight - 40) > 1e-9:
        errors.append(f"Summative weight is {s_weight:g}, expected 40")
    if abs(f_weight - 60) > 1e-9:
        errors.append(f"Formative weight is {f_weight:g}, expected 60")
    if errors:
        for e in errors:
            print(f"Weight validation error: {e}")
        return

    # c) Weighted totals and GPA
    f_earned = sum(a['score'] * a['weight'] / 100 for a in formative)
    s_earned = sum(a['score'] * a['weight'] / 100 for a in summative)
    total_grade = f_earned + s_earned
    gpa = (total_grade / 100) * 5.0

    f_pct = f_earned / f_weight * 100
    s_pct = s_earned / s_weight * 100

    print(f"Formative: {f_earned:.2f}/{f_weight:g} ({f_pct:.2f}%)")
    print(f"Summative: {s_earned:.2f}/{s_weight:g} ({s_pct:.2f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")

    # d) Pass/Fail: >= 50% in BOTH categories
    passed = f_pct >= 50 and s_pct >= 50
    print(f"\nFinal Status: {'PASSED' if passed else 'FAILED'}")

    # e) Resubmission: failed formatives (< 50) with the highest weight
    failed_formatives = [a for a in formative if a['score'] < 50]
    if failed_formatives:
        max_w = max(a['weight'] for a in failed_formatives)
        resubmit = [a for a in failed_formatives if a['weight'] == max_w]
        print("\nEligible for resubmission:")
        for a in resubmit:
            print(f"  - {a['assignment']} (score {a['score']:g}, weight {a['weight']:g})")
    else:
        print("\nNo failed formative assignments; no resubmission needed.")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
