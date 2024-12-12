def check_infer_latch(parsed_data):
    violations = []
    for line_num, line in parsed_data["always_blocks"]:
        if "if" in line and "else" not in line and "begin" in line:
            violations.append({
                "check": "Infer Latch",
                "line": line_num,
                "details": line.strip()
            })
    return violations
