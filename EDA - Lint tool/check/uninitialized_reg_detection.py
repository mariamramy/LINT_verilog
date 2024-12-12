def check_uninitialized_register(parsed_data):
    violations = []
    for line_num, line in parsed_data["signals"]:
        # Check for "reg" that is not initialized and is not part of an "output reg"
        if "reg" in line and "=" not in line and "output" not in line:
            violations.append({
                "check": "Uninitialized Register",
                "line": line_num,
                "details": line.strip()
            })
    return violations
