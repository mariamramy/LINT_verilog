import re
def check_feedback_loop(block_content, module_index, line_number):
    from Lintify import line_num_list , statement_lists , module_lists
    dependencies = {}  # Dictionary to store signal dependencies

    # Extract signal dependencies from the block content
    for line in block_content[1:]:  # Exclude the sensitivity line
       match = re.search(r'\b(\w+)\s*(<=|=)\s*(.+?)\s*;', line)
       if match:
            left_signal, operator, right_expr = match.groups()
            dependencies[left_signal] = re.findall(r'\b\w+\b', right_expr)

    # Check for feedback loops
    for signal in dependencies:
        if signal in dependencies[signal]:
            for x in line_num_list:
                if block_content[0] in x[2]:
                    line_number = x[1] + 1
            print(f"\nMay Infer Latch in module {module_index}, : {module_lists[module_index-1][0]}, line: {line_number}")
            statement_lists.append(f"\nMay Infer Latch in module {module_index}, : {module_lists[module_index-1][0]}, line: {line_number}")
            print("Reason: Combinational Feedback loop detected")
            statement_lists.append("Reason: Combinational Feedback loop detected")
            print("=====================================")
            statement_lists.append("=====================================")
            return


def check_case_without_default(block_content, module_index, line_number):
    from Lintify import line_num_list , statement_lists , module_lists
    found_case = False
    found_default = False

    for line in block_content:
        if re.search(r'^\s*case\b', line):
            if not re.search(r'//\s*synopsys\s*full_case', line):
                for x in line_num_list:
                    if line in x[2]:
                        line_number = x[1] + 1
                found_case = True

        if found_case and re.search(r'^\s*default\b', line):
                found_default = True

    if found_case and not found_default:
        print(f"\nMay Infer Latch in module {module_index},: {module_lists[module_index-1][0]}, line: {line_number}")
        statement_lists.append(f"May Infer Latch in module {module_index},: {module_lists[module_index-1][0]}, line: {line_number}")
        print("Reason: 'case' statement without 'default' detected")
        statement_lists.append("Reason: 'case' statement without 'default' detected")
        print("=====================================")
        statement_lists.append("=====================================")
        return

def check_if_without_else(block_content, module_index, line_number):
    from Lintify import line_num_list , statement_lists , module_lists
    found_if = False
    found_else = False

    for line in block_content:
            if re.search(r'\bif\b', line):
                for x in line_num_list:
                    if line in x[2]:
                        line_number = x[1] + 1
                found_if = True
            
            # Check for 'else' inside 'always' block
            if found_if and re.search(r'\belse\b', line):
                found_else = True



    # If we reach here, it means 'if' was not followed by 'else' inside 'always' block
    if found_if and not found_else:
        print(f"\nInfer Latch in module {module_index}, : {module_lists[module_index - 1][0]}, line: {line_number}")
        statement_lists.append(f"Infer Latch in module {module_index}, : {module_lists[module_index - 1][0]}, line: {line_number}")
        print("Reason: 'if' statement without 'else' detected")
        statement_lists.append("Reason: 'if' statement without 'else' detected")
        print("=====================================")
        statement_lists.append("=====================================")


# Update the check_sensitivity_list function
def check_sensitivity_list(sensitivity_line, module_index, line_number, used_signals):
    from Lintify import line_num_list , statement_lists , module_lists
    # Check if sensitivity_line is "@*" or contains clk
    if "*" in sensitivity_line or "clk" in sensitivity_line:
        return

    # Extract signals from the sensitivity line
    sensitivity_list = re.findall(r'\b([a-zA-Z_]\w*)\b', sensitivity_line)
    # Remove non-signal elements from the sensitivity list
    sensitivity_list = [signal for signal in sensitivity_list if signal not in ["*", "("]]

    # Check for missing signals
    missing_signals = set()
    for signal in used_signals:
        if signal not in sensitivity_list:
            missing_signals.add(signal)

    for x in line_num_list:
        if sensitivity_line in x[2]:
            line_number = x[1] + 1

    # Print results
    if missing_signals:
        print(f"\nMay Infer Latch in module {module_index}, : {module_lists[module_index-1][0]} , line: {line_number}")
        statement_lists.append(f"May Infer Latch in module {module_index}, : {module_lists[module_index-1][0]} , line: {line_number}")
        print(f"Reason: Signal(s) missing in the sensitivity list: {', '.join(missing_signals)}")
        statement_lists.append(f"Reason: Signal(s) missing in the sensitivity list: {', '.join(missing_signals)}")
        print("=====================================")
        statement_lists.append("=====================================")
        return






def check_infer_latch(module_lists):
    line_count = 0

    for module_index, module in enumerate(module_lists, start=1):
        always_blocks = []
        used_signals = set()
        module_declaration_line = module[0]
        match = re.search(r'\bmodule\s+\w+\s*\((.*?)\);', module_declaration_line)
        if match:
            used_signals.update(set(re.findall(r'\b(\w+)\b', match.group(1))))
        else:
            print(f"Warning: No module declaration found in line: {module_declaration_line}")
        for i, line in enumerate(module):
            if re.search(r'always\s*@', line):
                always_blocks.append(i)

            
        for always_index in always_blocks:
            sensitivity_line = module[always_index]
            sensitivity_line = sensitivity_line.replace("always", "").replace("@", "").strip()

            # Extract the block content including the line with 'always' keyword
            block_content = [sensitivity_line] + module[always_index + 1:]

            # Check for latch inference scenarios
            check_sensitivity_list(sensitivity_line, module_index, line_count + always_index + 1, used_signals)
            check_feedback_loop(block_content, module_index, line_count + always_index + 1)
            check_if_without_else(block_content, module_index, line_count + always_index + 1)
            check_case_without_default(block_content, module_index, line_count + always_index + 1)

        # Update line_count for the next module
        line_count += len(module)
