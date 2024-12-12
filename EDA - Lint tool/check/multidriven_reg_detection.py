import re
def check_multi_driven_bus(parsed_data):
    violations = []
    signal_drivers = {}

    for line_num, line in parsed_data["assignments"]:
        match = re.search(r"(\w+)\s*=", line)
        if match:
            signal = match.group(1)
            if signal in signal_drivers:
                violations.append({
                    "check": "Multi-Driven Bus/Register",
                    "line": line_num,
                    "details": f"Signal '{signal}' driven on line {signal_drivers[signal]} and {line_num}"
                })
            signal_drivers[signal] = line_num
    return violations
