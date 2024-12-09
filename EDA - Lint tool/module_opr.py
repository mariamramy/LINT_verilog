def counting_modules(verilog_code):
    module_counter = 0
    for i in verilog_code:
        if i == "endmodule":
            module_counter += 1
    return module_counter

def creating_module_lists(verilog_code, module_lists, module_counter):
    for i in verilog_code:
        module_lists[len(module_lists)-module_counter].append(i)
        if i == "endmodule":
            module_counter -= 1
    return module_lists

def remove_empty_strings(module_lists):
    for i in module_lists:
     while("" in i) : 
        i.remove("")
    return module_lists

def remove_comments(module_lists):
    i_counter = 0
    for i in module_lists:
        
        j_counter = 0
        
        for j in i:
            
            if j.startswith('//'):
                i.remove(j)
            
            elif '//' in j:
                index = j.find('//')
                tmp = j[index:].split(" ")
                if "synopsys" in tmp:
                    break
                j = j[:index]
                module_lists[i_counter][j_counter] = j
            
            j_counter += 1

        i_counter += 1
    return module_lists

def creating_line_num_list(module_lists_space):
    from Lintify import line_num_list
    tmp = 0
    for i in module_lists_space:
        for line_num,j in enumerate(i):
            x = line_num+tmp
            line_num_list.append([module_lists_space.index(i),x,j]) # module number , line number , line
        tmp = x+1
    return line_num_list 


