def check_arithmetic_overflow(parsed_data):
    violations = []
    for line_num, line in parsed_data["assignments"]:
        if ("+" in line or "*" in line) and "signed" not in line:
            violations.append({
                "check": "Arithmetic Overflow",
                "line": line_num,
                "details": line.strip()
            })
    return violations
