import subprocess
import sys

def extract_query_lines(file_path):
    grep_command = ["grep", "^ *query:", file_path]
    awk_command = ["awk", '{$1=""; print $0}']
    
    try:
        grep_process = subprocess.Popen(grep_command, stdout=subprocess.PIPE)
        awk_process = subprocess.Popen(awk_command, stdin=grep_process.stdout, stdout=subprocess.PIPE)
        grep_process.stdout.close()  # Close grep stdout to allow awk to finish
        
        output, _ = awk_process.communicate()
        return output.decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def validate_query(query, idx):
    errors = []

    # Check if there are equal number of opening and closing brackets
    if query.count('(') != query.count(')'):
        errors.append("Unbalanced parentheses")

    # Check if there are equal number of single quotes
    if query.count("'") % 2 != 0:
        errors.append("Unbalanced single quotes")

    # Check if there are equal number of double quotes
    if query.count('"') % 2 != 0:
        errors.append("Unbalanced double quotes")

    if errors:
        print(f"Query line {idx} is invalid: {query}")
        for error in errors:
            print(f"    - {error}")
        return False
    else:
        print(f"Query line {idx} is valid: {query}")
        return True

file_path = 'configmap-vmalertrules.yaml'
query_lines = extract_query_lines(file_path)
invalid_queries = []

for idx, line in enumerate(query_lines, start=1):
    if not validate_query(line, idx):
        invalid_queries.append(line)

if invalid_queries:
    sys.exit(1)
else:
    sys.exit(0)
