def check_unreachable_fsm_state(parsed_data):
    violations = []
    for line_num, state in parsed_data["fsm_states"].items():
        if "default:" not in state and state.count(":") == 1:
            violations.append({
                "check": "Unreachable FSM State",
                "line": line_num,
                "details": state.strip()
            })
    return violations
