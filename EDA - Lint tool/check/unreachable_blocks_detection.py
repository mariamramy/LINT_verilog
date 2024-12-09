import re

def extract_initial_values(module_lists):
    initial_values = {}
    # Improved regex pattern to capture Verilog style binary values
    initial_pattern = re.compile(r'\b(\w+)\s*=\s*(\d+\'b[01]+);')
    inside_initial_block = False
    for lines in module_lists:
        for line in lines:
            if 'initial' in line:
                inside_initial_block = True
            elif 'end' in line and inside_initial_block:
                inside_initial_block = False
            elif inside_initial_block:
                match = initial_pattern.search(line)
                if match:
                    var, value = match.groups()
                    initial_values[var] = value
    return initial_values

def normalize_bit_length(value):
    # Normalizing binary values to their simplest form for comparison
    # Example: from '2'b00' to '1'b0'
    match = re.match(r"(\d+)'b([01]+)", value)
    if match:
        bits, binary = match.groups()
        return f"{int(binary, 2)}"  # Returns the integer value of the binary
    return value

def analyze_verilog(module_lists):
    from Lintify import line_num_list
    issues = {}
    current_module = None
    line_num = 0

    initial_values = extract_initial_values(module_lists)

    if_condition_pattern = re.compile(r'if\s*\(\s*(\w+)\s*==\s*(\d+\'b[01]+)\s*\)')
    for lines in module_lists:
        for line in lines:
            for x in line_num_list:
                if x[2] == line:
                    line_num = x[1] + 1
            match = re.search(r'module\s+(\w+)', line)
            if match:
                current_module = match.group(1)
                issues[current_module] = {
                    'unreachable_blocks': [],
                    'module_line_num': line_num,
                    'initial_values': initial_values.copy()
                }
                continue

            if not current_module:
                continue

            match = if_condition_pattern.search(line)
            if match:
                var, expected_value = match.groups()
                actual_value = issues[current_module]['initial_values'].get(var)

                # Normalizing the bit-length for comparison
                if actual_value and normalize_bit_length(actual_value) != normalize_bit_length(expected_value):
                    issues[current_module]['unreachable_blocks'].append((line_num, line, var, actual_value, expected_value))

    return issues

def report_issues(issues):
    from Lintify import statement_lists
    for module, module_issues in issues.items():
        if module_issues['unreachable_blocks']:
            print(f"\nModule: {module}")
            statement_lists.append(f"\nModule: {module}")
            for line_num, line, var, actual_value, expected_value in module_issues['unreachable_blocks']:
                print(f"Unreachable Block")
                statement_lists.append(f"Unreachable Block")
                print(f"line {line_num}: {line}")
                statement_lists.append(f"line {line_num}: {line}")
                print(f"Variable '{var}' is initialized to {actual_value}, but the condition checks for {expected_value}.")
                statement_lists.append(f"Variable '{var}' is initialized to {actual_value}, but the condition checks for {expected_value}.")
            print('=====================================')  
            statement_lists.append('=====================================')

