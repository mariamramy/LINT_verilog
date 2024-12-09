import re
from .unintialized_reg_detection import generating_reg_list

def calculating_case_index(module_lists):
    cases_index = []
    for i in module_lists:
        for j in i:
            cmp = re.search("^case",j)
            if cmp or re.search("^casez",j) or re.search("^casex",j):
                cases_index.append(module_lists.index(i))
    return cases_index

def check_full_case(module_lists):
    from Lintify import line_num_list , statement_lists
    cases_index = calculating_case_index(module_lists)
    reg_list = generating_reg_list(module_lists,cases_index)
    size_list_for_case = []
    mask = 0
    for i in cases_index:
        for j in module_lists[i]:
            for t in reg_list:
                if t[0] == i and t[1] in j:
                    tmp = j.split("=")
                    if len(tmp) > 1:
                        #print(tmp)
                        pre_defined_reg = tmp[0]

                    
            if j.startswith('case') or j.startswith('casez') or j.startswith('casex'):
                #print(module_lists[i][module_lists[i].index(j)+1:])
                line_after_case = module_lists[i][module_lists[i].index(j)+1:module_lists[i].index(j)+2]
                
                # convert from list to string
                line_after_case = ''.join(line_after_case)
                # remove all characters before :
                line_after_case = line_after_case[line_after_case.find(':')+1:]
                #print(line_after_case)
                try:
                    if pre_defined_reg in line_after_case:
                        break
                except:
                    pass
                if "synopsys" in j:
                    break
                bound = j.find('e')
                reg_name = j[bound+1:]
                reg_name = reg_name.replace(' ', '')
                reg_name = reg_name.replace('(', '')
                reg_name = reg_name.replace(')', '')
                reg_name = reg_name.replace(':', '')
                reg_name = reg_name
                #print(reg_name)
                # take size of reg_name
                for k in reg_list:
                    if k[1] == reg_name and k[0] == i:
                        size = k[2]
                        size_list_for_case.append(size)
                        break
                case_i = module_lists[i].index(j)
                
                rows_count = 0
                
                for line in module_lists[i][case_i+1:]:
                    if line.startswith('endcase'):
                        break
                    if line.startswith('default'):
                        mask = 1
                        break
                    if ":" in line:
                        rows_count += 1
                #print("rows_count", rows_count)
                if mask == 0:
                    if pow(2, size) != rows_count:
                        print("\nNon-Full Case:")
                        for x in line_num_list:
                            if x[0] == i and x[2] == j:
                                line_num = x[1] + 1
                        print("Line Number:", line_num)
                        statement_lists.append("\nNon-Full Case")
                        statement_lists.append("Line Number : " + str(line_num))
                        print("Module", i + 1, ":", module_lists[i][0])
                        statement_lists.append("Module " + str(i + 1) + " : " + module_lists[i][0])
                        print(f"Size of reg \"{reg_name}\":", size) 
                        statement_lists.append(f"Size of reg \"{reg_name}\" : " + str(size))
                        print("Number of variations:", rows_count)
                        statement_lists.append("Number of variations : " + str(rows_count))
                        print("Expected number of variations:", pow(2, size))
                        statement_lists.append("Expected number of variations : " + str(pow(2, size)))
                        print("Number of variations is not equal to expected number of variations")
                        statement_lists.append("Number of variations is not equal to expected number of variations")
                        print("=====================================")
                        statement_lists.append("=====================================")
                        print()
                        break
                    else:
                        break
            
# ----------------------------------------------------Parallel Cases------------------------------------------>

def extract_text_before_colon(input_text):
    # Find the index of the colon
    colon_index = input_text.find(':')

    if colon_index != -1:
        # Extract the text before the colon
        text_before_colon = input_text[:colon_index].strip()
        return text_before_colon
    else:
        return "None"
    
def can_be_number(input_text):
    try:
        input_text = input_text.replace(' ', '')
        if input_text[2] == 'b':
            input_text = input_text.split('b')[1]
            #print(input_text)
        elif input_text[2] == 'd':
            input_text = input_text.split('d')[1]
        elif input_text[2] == 'h':
            input_text = input_text.split('h')[1]
            input_text = int(input_text, 16)
        int(input_text)
        return True
    except :
        return False

def is_parallel_sequence(lst):
    lst0 = [element.replace('?', '0') for element in lst]
    lst0 = [element.replace('x', '0') for element in lst0]
    lst1 = [element.replace('?', '1') for element in lst]
    lst1 = [element.replace('x', '1') for element in lst1]

    set0 = set(lst0)
    set1 = set(lst1)
    if len(set0) < len(lst0) or len(set1) < len(lst1):
        return False
    else:
        return True


def check_parallel_case(module_lists):
    from Lintify import line_num_list , statement_lists
    parallel_case = calculating_case_index(module_lists)
    mask2 = 0
    for i in parallel_case:
        mask = 0
        case_values = []
        for j in module_lists[i]:
            
            k_counter = 0
            parallel_case_counter = 0
            if j.startswith('case') or j.startswith('casez') or j.startswith('casex'):
            # iterate over lines after case
                #print(j)
                case_number = j
                if "synopsys" in j:
                    tmp = j.split(" ")
                    if "parallel_case" in tmp:
                        mask2 = 1
                        break
    
        
                for k in module_lists[i][module_lists[i].index(j)+1:]:
                    #print(k)
                    k_counter += 1
                    num = extract_text_before_colon(k)
                    if num != "None" and num != "default":
                        case_values.append(num)
                    if can_be_number(num):
                        parallel_case_counter += 1
                        #print("yes")
                    # mask = 1

                    if k.startswith('endcase'):
                        break
        
        for t in case_values:
            if can_be_number(t):
                mask = 1
            else:
                mask = 0
                break
        
        if mask == 0 and mask2 == 0 :
            if is_parallel_sequence(case_values) == False:
                print("Non-Parallel Case:")
                statement_lists.append("\nNon-Parallel Case:")
                print("Module", i + 1, ":", module_lists[i][0])
                statement_lists.append("Module " + str(i + 1) + " : " + module_lists[i][0])
                for x in line_num_list:
                    if x[0] == i and x[2] == case_number:
                        line_num = x[1] + 1
                print("Line Number:", line_num)
                statement_lists.append("Line Number : " + str(line_num))
                print("=====================================")
                statement_lists.append("=====================================")
                print()

        if mask2 == 1:
            mask2 = 0            