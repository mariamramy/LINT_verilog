
def check_multidriven_variables_always_blocks(module_lists):
    from Lintify import line_num_list , statement_lists
    modules_with_multidriven_variables = set()

    for module_index, module in enumerate(module_lists, start=1):
        # Always blocks and their contents
        always_blocks = []

        # Extract contents of always blocks
        inside_always = False
        current_always_block = []

        for line in module:
            if 'always' in line:
                inside_always = True
                current_always_block = ['always']
            elif inside_always:
                current_always_block.append(line.strip())
                if 'end' in line:
                    inside_always = False
                    always_blocks.append(current_always_block)

        # Compare always blocks to identify multidriven variables
        seen_variables = set()
        seen_variables_list = []
        for i, block1 in enumerate(always_blocks):
            for j, block2 in enumerate(always_blocks):
                if i != j:
                    # Check for 'variable ='
                    for line1 in block1[2:-1]:  # Skip 'always', 'begin', 'end'
                        for line2 in block2[2:-1]:  # Skip 'always', 'begin', 'end'
                            seen_variables_list.append(line2)
                            if '=' in line1 and '=' in line2:
                                variable_name1 = line1.split('=')[0].strip()
                                variable_name2 = line2.split('=')[0].strip()
                                if variable_name1 == variable_name2:
                                    seen_variables.add(variable_name1)

        # Print the results only if there are multidriven variables in the module
        if seen_variables and module_index not in modules_with_multidriven_variables:
            modules_with_multidriven_variables.add(module_index)
            print(f"\nModule {module_index}:", module[0])
            statement_lists.append(f"\nModule {module_index}: {module[0]}")
            for block in always_blocks:
                print("Always Block:", block)
                statement_lists.append("Always Block: " + str(block))
                for n in block:
                    for x in line_num_list:
                        for y in seen_variables_list:
                            if x[2] == n and y in n:
                                line_num = x[1] + 1
                                print("Line Number:", line_num)
                                statement_lists.append("Line Number : " + str(line_num))
                                break
                        pass
                    
            print("Multidriven Variables:", seen_variables)
            statement_lists.append("Multidriven Variables: " + str(seen_variables))
            print("=====================")
            statement_lists.append("=====================")


def check_multidriven_variables_assign_statements(module_lists):
    from Lintify import line_num_list , statement_lists
    for module_index, module in enumerate(module_lists, start=1):
        # Extracted variable names and sizes
        variables = set()
        # Assign statements and assigned variables
        assign_statements = []

        for line in module:
            # Check if the line contains an assign statement
            
            if 'assign' in line:
                parts = line.split()
                assign_index = parts.index('assign')

                # Extract the assigned variable name
                if assign_index < len(parts) - 1:
                    variable_name = parts[assign_index + 1].rstrip(';')
                    # Check if the variable is already assigned in another statement
                    if variable_name in variables:
                        assign_statements.append([line, variable_name])
                    else:
                        variables.add(variable_name)

        # Check for multidriven variables within the same module based on assign statements
        seen_variables = set()
        for statement, variable in assign_statements:
            # Check if the variable is repeated (multidriven) in the same module
            if variable in seen_variables:
                print(f"Module {module_index}: Variable '{variable}' is multidriven.")
            else:
                seen_variables.add(variable)

        # Print the results only if there are multidriven variables in the module
        if seen_variables:
            print(f"\nModule {module_index}:", module[0])
            statement_lists.append(f"\nModule {module_index}: {module[0]}")
            print("Assign Statements:", assign_statements)
            for n in assign_statements:
                for x in line_num_list:
                    if x[2] == n[0]:
                        line_num = x[1] + 1
                        print("Line Number:", line_num)
                        statement_lists.append("Line Number : " + str(line_num))
                        break
    
                        
                pass
            statement_lists.append("Assign Statements: " + str(assign_statements))
            print("Multidriven Variables:", seen_variables)
            statement_lists.append("Multidriven Variables: " + str(seen_variables))
            print("=====================")
            statement_lists.append("=====================")            



def check_multidriven_variables_always_with_assign_statements(module_lists):
    from Lintify import line_num_list , statement_lists
    modules_with_multidriven_variables = set()

    for module_index, module in enumerate(module_lists, start=1):
        # Always blocks and their contents
        always_blocks = []

        # Extract contents of always blocks
        inside_always = False
        current_always_block = []
        always_blocks_variables = []

        for line in module:
            if 'always' in line:
                inside_always = True
                current_always_block = ['always']
            elif inside_always:
                current_always_block.append(line.strip())
                # extract variable name from always block
                if '<=' in line :
                    variable_name = line.split('<=')[0].strip()
                    always_blocks_variables.append(variable_name)
                    break
                if '=' in line :
                    variable_name = line.split('=')[0].strip()
                    always_blocks_variables.append(variable_name)
                    break


        # Extracted variable names and sizes
        assign_variables = set()
        # Assign statements and assigned variables
        assign_statements = []

        for line in module:
            # Check if the line contains an assign statement
            if 'assign' in line:
                parts = line.split()
                assign_index = parts.index('assign')
                assign_statements.append([line, variable_name])


                # Extract the assigned variable name
                if assign_index < len(parts) - 1:
                    variable_name = parts[assign_index + 1].rstrip(';')
                    # Check if the variable is already assigned in another statement
                    if variable_name in assign_variables:
                        assign_statements.append([line, variable_name])
                    else:
                        assign_variables.add(variable_name)


        
        # check for multidriven variables within the same module based on always block and assign statements
        seen_variables = set()
        tmp = ""
        for variable in always_blocks_variables:
            # Check if the variable is repeated (multidriven) in the same module
            #print(assign_statements)
            if variable in assign_variables:
                seen_variables.add(variable)
                print(f"Module {module_index}: Variable '{variable}' is multidriven.")
                statement_lists.append(f"Module {module_index}: Variable '{variable}' is multidriven.")
                print("Assign Statements:", assign_statements)
                statement_lists.append("Assign Statements: " + str(assign_statements))
                for n in assign_statements:
                    for x in line_num_list:
                        if "assign" in x[2]:
                            # remove all except for variable name
                            tmp = x[2].split("=")
                            tmp = tmp[0].strip()
                            tmp = tmp.split(" ")
                            tmp = tmp[1]
                            #print(tmp)
                        if n[1] == tmp:
                            line_num = x[1] + 1
                            print("Line Number:", line_num)
                            statement_lists.append("Line Number : " + str(line_num))
                            break
                print("Multidriven Variables:", seen_variables)
                statement_lists.append("Multidriven Variables: " + str(seen_variables))
                print("=====================================")
                statement_lists.append("=====================================")
            else:
                assign_variables.add(variable)            