import re

def checkArithmeticOverflow(module_lists):
    from Lintify import statement_lists , line_num_list
    # extracting the variables from the module
    variable_list = [[] for _ in range(len(module_lists))]
    
    for module_index, module in enumerate(module_lists, start=1):
        #print("Module Number:", module_index)
        for variable_declaration in module:
            # check if the variable is input, output, wire, or reg
            if variable_declaration.startswith(('input ', 'output ', 'wire ', 'reg ')):
                # Extract variable name and size
                parts = variable_declaration.split()
                parts[-1] =  parts[-1].rstrip(';')
                # Variable names are strings after '[number:number]' or after 'reg', 'wire', 'input', 'output'
                variable_names = [part.strip(',') for part in parts[1:] if part not in ('reg', 'wire', 'input', 'output')]
                for i in variable_names:
                    if '[' in i and ']' in i:
                        variable_names.remove(i)
                   

                index = 0
                for i in variable_names:
                    if '=' in i:
                        variable_names.pop(index)
                        variable_names.pop(index)
                    index += 1

                variable_size = 1  # Default size is 1
                
                # Check if [number-1:0] pattern is present
                if '[' in variable_declaration and ']' in variable_declaration:
                    size_part = variable_declaration.split('[')[1].split(']')[0]

                        # Extract the size correctly
                    if ':' in size_part:
                        sizes = size_part.split(':')
                        variable_size = abs(int(sizes[0]) - int(sizes[1])) + 1
                    else:
                        variable_size = int(size_part) + 1
                # Store the variable names and size
                variable_list[module_index - 1].extend([[name, variable_size] for name in variable_names if name])

        #print("Variable List:", variable_list[module_index - 1])
        

        # extracting the operations from the module
        operation_list = []
        for operation in module:
            if '=' in operation:
                if '+' in operation or '-' in operation or '*' in operation or '/' in operation:
                    # Extract the operation
                    parts = operation.split('=')
                    parts[-1] = parts[-1].rstrip(';')
                    parts = [part.split(' ') for part in parts]
                    # Remove empty strings
                    for part in parts:
                        while '' in part:
                            part.remove('')

                    print("Parts:", parts)

                    left_side_size = 0
                    right_side_size = 0
                    for variable in variable_list[module_index - 1]:
                        if variable[0] in parts[0]:
                            left_side_size = variable[1]
                            break
                    for variable in variable_list[module_index - 1]:
                        if variable[0] in parts[1]:
                            right_side_size = max(variable[1], right_side_size)
                    
                    binary_size = re.findall(r'\b(\d+\'b[01]+)\b', operation)
                    for i in binary_size:
                        size = i.split('\'')[0]
                        size = int(size)
                        if size > right_side_size:
                            right_side_size = size

                    
                

                    if left_side_size <= right_side_size:
                        print("\nPossible Arithmetic Overflow in module", module_index, ":", module[0])
                        statement_lists.append("\nPossible Arithmetic Overflow in module " + str(module_index) + " : " + module[0])
                        for x in line_num_list:
                            if x[0] == module_index-1 and x[2] == operation:
                                line_num = x[1] + 1
                        print("Line Number:", line_num)
                        statement_lists.append("Line Number : " + str(line_num))
                        print("Line: ", operation)
                        statement_lists.append("Line: " + operation)
                        print("Left side size:", left_side_size)
                        statement_lists.append("Left side size: " + str(left_side_size))
                        print("Right side size:", right_side_size)
                        statement_lists.append("Right side size: " + str(right_side_size))

                        

                        
                    operation_list.append(parts)


        if len(operation_list) == 0:
            pass
        else:
            print("Operation List:", operation_list)
            statement_lists.append("Operation List: " + str(operation_list))
            print("=====================")
            statement_lists.append("=====================")
