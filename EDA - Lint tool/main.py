from parser import VerilogParser
from check.arithmetic_overflow import check_arithmetic_overflow
from check.unreachable_blocks_detection import check_unreachable_blocks
from check.unreachable_FSM_state_detection import check_unreachable_fsm_state
from check.uninitialized_reg_detection import check_uninitialized_register
from check.multidriven_reg_detection import check_multi_driven_bus
from check.case_detection import check_non_full_parallel_case
from check.infer_latch_detection import check_infer_latch
from report import write_report

def main():
    # Input Verilog file
    verilog_file = "verilog_code.v"

    # Parse Verilog Code
    parser = VerilogParser(verilog_file)
    parsed_data = parser.parse()

    # Initialize results container
    violations = []

    # Perform checks
    violations.extend(check_arithmetic_overflow(parsed_data))
    violations.extend(check_unreachable_blocks(parsed_data))
    violations.extend(check_unreachable_fsm_state(parsed_data))
    violations.extend(check_uninitialized_register(parsed_data))
    violations.extend(check_multi_driven_bus(parsed_data))
    violations.extend(check_non_full_parallel_case(parsed_data))
    violations.extend(check_infer_latch(parsed_data))

    # Generate and save the report
    write_report(violations, "report.txt")
    print("\nLinting completed. Report saved to 'report.txt'.")
    for v in violations:
        print(f"{v['check']} - Line {v['line']}: {v['details']}")

if __name__ == "__main__":
    main()
