def check_unreachable_blocks(parsed_data):
    """
    Detects unreachable blocks in the Verilog code, such as if (0) or similar constructs.
    """
    violations = []
    for line_num, line in enumerate(parsed_data["lines"], start=1):  # Include line numbers
        if "if (0)" in line or "else if (0)" in line:  # Check for unreachable conditions
            violations.append({
                "check": "Unreachable Blocks",
                "line": line_num,
                "details": line.strip()
            })
    return violations
