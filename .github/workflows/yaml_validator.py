import subprocess

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

def validate_query(query):
    # Check if there are equal number of opening and closing brackets
    if query.count('(') != query.count(')'):
        return False
    
    # Check if there are equal number of single quotes
    if query.count("'") % 2 != 0:
        return False
    
    # Check if there are equal number of double quotes
    if query.count('"') % 2 != 0:
        return False
    
    # Add more validation checks as needed
    
    return True

file_path = '.github/workflows/configmap-vmalertrules.yaml'
query_lines = extract_query_lines(file_path)
for idx, line in enumerate(query_lines, start=1):
    if validate_query(line):
        print(f"Query line {idx} is valid: {line}")
    else:
        print(f"Query line {idx} is invalid: {line}")
