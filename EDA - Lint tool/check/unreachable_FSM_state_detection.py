import re

def extract_fsm_states(module_lists):
    """
    Extract FSM states from the module using `localparam`, `parameter`, or `typedef enum`.
    Returns a dictionary where keys are module names and values are lists of states.
    """
    fsm_states = {}
    state_pattern = re.compile(r'(localparam|parameter|typedef\s+enum)\s*.*\s*{(.*)};')
    current_module = None

    for lines in module_lists:
        for line in lines:
            match = re.search(r'module\s+(\w+)', line)
            if match:
                current_module = match.group(1)
                fsm_states[current_module] = []

            if current_module:
                state_match = state_pattern.search(line)
                if state_match:
                    states = state_match.group(2).split(',')
                    states = [state.strip().split('=')[0] for state in states]
                    fsm_states[current_module].extend(states)

    return fsm_states


def extract_state_transitions(module_lists):
    """
    Extract state transitions defined in case or if-else constructs.
    Returns a dictionary where keys are module names and values are transition graphs.
    """
    state_transitions = {}
    case_pattern = re.compile(r'case\s*\((\w+)\)')
    next_state_pattern = re.compile(r'next_state\s*=\s*(\w+);')

    current_module = None
    current_state_var = None

    for lines in module_lists:
        for line in lines:
            match = re.search(r'module\s+(\w+)', line)
            if match:
                current_module = match.group(1)
                state_transitions[current_module] = {}
                continue

            if current_module:
                case_match = case_pattern.search(line)
                if case_match:
                    current_state_var = case_match.group(1)

                if current_state_var:
                    next_state_match = next_state_pattern.search(line)
                    if next_state_match:
                        next_state = next_state_match.group(1)
                        if current_state_var not in state_transitions[current_module]:
                            state_transitions[current_module][current_state_var] = set()
                        state_transitions[current_module][current_state_var].add(next_state)

    return state_transitions


def find_unreachable_fsm_states(fsm_states, state_transitions):
    """
    Compare defined FSM states with reachable states and identify unreachable states.
    """
    unreachable_states = {}

    for module, states in fsm_states.items():
        if module in state_transitions:
            reachable_states = set()
            for transitions in state_transitions[module].values():
                reachable_states.update(transitions)

            unreachable = set(states) - reachable_states
            unreachable_states[module] = list(unreachable)

    return unreachable_states


def report_unreachable_states(unreachable_states):
    from Lintify import statement_lists
    """
    Report unreachable FSM states in the modules.
    """
    for module, states in unreachable_states.items():
        if states:
            print(f"\nModule: {module}")
            statement_lists.append(f"\nModule: {module}")
            print(f"Unreachable FSM States: {', '.join(states)}")
            statement_lists.append(f"Unreachable FSM States: {', '.join(states)}")
            print("=====================================")
            statement_lists.append("=====================================")


def detect_unreachable_fsm_states(module_lists):
    """
    Main function to detect unreachable FSM states.
    """
    fsm_states = extract_fsm_states(module_lists)
    state_transitions = extract_state_transitions(module_lists)
    unreachable_states = find_unreachable_fsm_states(fsm_states, state_transitions)
    report_unreachable_states(unreachable_states)
