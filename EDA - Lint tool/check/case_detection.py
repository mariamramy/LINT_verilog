def check_non_full_parallel_case(parsed_data):
    violations = []
    for line_num, line in parsed_data["fsm_states"].items():
        if "case" in line:
            case_lines = parsed_data["fsm_states"].get("case_lines", {}).get(line_num, [])
            case_conditions = []
            has_default = False
            non_parallel_conditions = []

            for case_line in case_lines:
                if "default" in case_line:
                    has_default = True
                else:
                    condition = case_line.strip().split(":")[0]  # Extract the condition
                    if condition in case_conditions:
                        non_parallel_conditions.append(condition)
                    else:
                        case_conditions.append(condition)

            # Check for non-full case
            if not has_default:
                violations.append({
                    "check": "Non-Full Case",
                    "line": line_num,
                    "details": f"Missing default clause in `case` starting at line {line_num}."
                })

            # Check for non-parallel case
            if non_parallel_conditions:
                violations.append({
                    "check": "Non-Parallel Case",
                    "line": line_num,
                    "details": f"Overlapping conditions in `case` starting at line {line_num}: {non_parallel_conditions}."
                })

    return violations
