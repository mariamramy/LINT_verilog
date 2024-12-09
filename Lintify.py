import re
import sys
import os

from file_reader import *
from module_opr import *
from check.case_detection import *
from check.unintialized_reg_detection import *
from check.infer_latch_detection import *
from check.unreachable_blocks_detection import *
from check.unreachable_FSM_state_detection import *
from check.mulidriven_reg_detection import *
from check.arithmetic_overflow import *
from report import *

statement_lists = []
file_path = input("Please enter the file name: ")

verilog_code = file_reader(file_path)

module_counter = counting_modules(verilog_code)
module_lists_space = [[] for i in range(module_counter)]
module_lists_space = creating_module_lists(verilog_code, module_lists_space, module_counter)
line_num_list = []

line_num_list = creating_line_num_list(module_lists_space)
module_lists = [[] for i in range(module_counter)]
# append each module to a module_lists from the y
module_lists = creating_module_lists(verilog_code, module_lists, module_counter)
# remove all empty strings from the module_lists
module_lists = remove_empty_strings(module_lists)
module_lists = remove_comments(module_lists)

check_full_case(module_lists)
check_unintialized_reg(module_lists)
check_infer_latch(module_lists)

#--------------------check unreachable blocks--------------------------->
issues = analyze_verilog(module_lists)
report_issues(issues)
#--------------------check unreachable FSM states----------------------->
detect_unreachable_fsm_states(module_lists)
#----------------------------------------------------------------------->

check_multidriven_variables_always_blocks(module_lists)
check_multidriven_variables_assign_statements(module_lists)
check_multidriven_variables_always_with_assign_statements(module_lists)

checkArithmeticOverflow(module_lists)

check_parallel_case(module_lists)

report_generator(statement_lists)

