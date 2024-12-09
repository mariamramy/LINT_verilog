import re


def generating_reg_list(module_lists,any_specific_index):
    reg_list = []
    # in each list first number is case_index and second number is reg_index & size of reg is third number
    for i in any_specific_index:
        for j in module_lists[i]:
            if j.startswith('input'):
                j = j[len('input '):]
            if j.startswith('output'):
                j = j[len('output '):]
            if j.startswith('localparam'):
                j = j[len('localparam '):]
                if ']' in j or '[' in j:
                    low_bound = j.find('[')
                    high_bound = j.find(']')
                    size = j[low_bound+1:high_bound]
                    size = size.split(':')
                    size = int(size[0])-int(size[1])+1
                    j = j[high_bound+1:].replace(';', '')
                    j = j.replace(' ', '')
                    variables_names = j.split(',')
                    for var_name in variables_names:
                        reg_list.append([i, var_name, size])
                else:
                    size = 1
                    low_bound = j.find('g')
                    j = j[low_bound+1:].replace(';', '')
                    j = j.replace(' ', '')
                    variables_names = j.split(',')
                    for var_name in variables_names:
                        reg_list.append([i, var_name, size])  
                
            if j.startswith('reg'):
                # store reg name & size in a list
                if ']' in j or '[' in j:
                    low_bound = j.find('[')
                    high_bound = j.find(']')
                    size = j[low_bound+1:high_bound]
                    size = size.split(':')
                    size = int(size[0])-int(size[1])+1
                    j = j[high_bound+1:].replace(';', '')
                    j = j.replace(' ', '')
                    variables_names = j.split(',')
                    for var_name in variables_names:
                        reg_list.append([i, var_name, size])
                else:
                    size = 1
                    low_bound = j.find('g')
                    j = j[low_bound+1:].replace(';', '')
                    j = j.replace(' ', '')
                    variables_names = j.split(',')
                    for var_name in variables_names:
                        reg_list.append([i, var_name, size])  
    #print(reg_list)
    return reg_list


def word_position_relative_to_equal(word, sentence):
    search_pattern = r'\b{}\b'.format(word)

    matches = [match for match in re.finditer(search_pattern, sentence)]

    if matches:
        word_index = matches[0].start()
        equal_index = sentence.find('=')
        
        if sentence.count('=') > 1:
            return 3  # not found
        
        last_word_index = matches[-1].start() + len(matches[-1].group()) - 1
        
        if equal_index == -1:
            return 3  # not found
        
        if word_index < equal_index and last_word_index > equal_index:
            return 2  # found both before and after equal
        
        elif word_index < equal_index:
            return 0  # before equal
        
        elif last_word_index > equal_index:
            return 1  # after equal
    else:
        return 3  # not found
    

def reg_list_for_unintialized(module_lists):
    reg_names = [] # list of lists first place is reg name and second place is module index
    for i in module_lists:
        for j in i:
            if j.startswith('reg') and not('=' in j):
                mask = 1
                if "]" in j:
                    j = j[j.find(']')+1:]
                    if "," in j:
                        j = j.replace(",","")    
                j = j.replace("reg","")
                j = j.replace(";","")
                if j[0] == " ":
                    j = j[1:]
                if " " in j:
                    tmp = j.split(" ")
                    for t in tmp:
                        reg_names.append([t, module_lists.index(i)])
                else:
                    reg_names.append([j,module_lists.index(i)])
    return reg_names


def check_unintialized_reg(module_lists):
    from Lintify import line_num_list , statement_lists
    mask = 0
    reg_names = reg_list_for_unintialized(module_lists)
#print(reg_names)
#print()
    for i in reg_names:
        module = module_lists[i[1]]
        #print(i[1])
        #print(i[0])
        mask = 0
        for j in module:
            if i[0] in j and not(j.startswith('case')):
                
                if word_position_relative_to_equal(i[0],j) == 0:
                    #print("before equal")
                    #print(j)
                    mask = 1
                elif word_position_relative_to_equal(i[0],j) == 1:
                    #print("after equal")
                    #print(j)
                    print("\nModule Name:", module[0])
                    for x in line_num_list:
                        if x[0] == i[1] and x[2] == j:
                            line_num = x[1] + 1
                    print("Line Number:", line_num)
                    statement_lists.append("\nModule Name: " + module[0])
                    statement_lists.append("Line Number : " + str(line_num))
                    print("Reg name: ", f"\"{i[0]}\"")
                    statement_lists.append("Reg name: " + f"\"{i[0]}\"")
                    print("Possible Uninitialized reg")
                    statement_lists.append("Possible Uninitialized reg")
                    print("=====================================")
                    statement_lists.append("=====================================")
                    #mask = 1
                elif word_position_relative_to_equal(i[0],j) == 2:
                    #print("both before and after equal")
                    #print(j)
                    print("\nModule Name:", module[0])
                    statement_lists.append("\nModule Name: " + module[0])
                    for x in line_num_list:
                        if x[0] == i[1] and x[2] == j:
                            line_num = x[1] + 1
                    print("Line Number:", line_num)
                    statement_lists.append("Line Number : " + str(line_num))
                    print("Reg name: ", f"\"{i[0]}\"")
                    statement_lists.append("Reg name: " + f"\"{i[0]}\"")
                    print("Possible Uninitialized reg")
                    statement_lists.append("Possible Uninitialized reg")
                    print("=====================================")
                    statement_lists.append("=====================================")
                    #mask = 1
                #print("--------------------")
            if mask == 1:
                break
            if j.startswith('case') and i[0] in j:
                #print(j)
                #print("case")
                print("\nModule Name:", module[0])
                statement_lists.append("\nModule Name: " + module[0])
                for x in line_num_list:
                    if x[0] == i[1] and x[2] == j:
                        line_num = x[1] + 1
                print("Line Number:", line_num)
                statement_lists.append("Line Number : " + str(line_num))
                print("Reg name: ", f"\"{i[0]}\"")
                statement_lists.append("Reg name: " + f"\"{i[0]}\"")
                print("Possible Uninitialized reg")
                statement_lists.append("Possible Uninitialized reg")
                print("=====================================")
                statement_lists.append("=====================================")
                break
                