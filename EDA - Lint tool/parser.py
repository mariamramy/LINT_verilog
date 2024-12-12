import re

class VerilogParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        """Parse the Verilog file into structured data."""
        with open(self.filename, "r") as file:
            lines = file.readlines()

        parsed_data = {
            "lines": lines,
            "signals": [],
            "fsm_states": {},
            "registers": [],
            "always_blocks": [],
            "assignments": [],
        }

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Parse signals and registers
            if re.match(r"^\s*(input|output|wire|reg)", stripped_line):
                parsed_data["signals"].append((i + 1, stripped_line))

            # Parse FSM states
            if "case" in stripped_line or "state" in stripped_line:
                parsed_data["fsm_states"][i + 1] = stripped_line

            # Parse always blocks
            if "always" in stripped_line:
                parsed_data["always_blocks"].append((i + 1, stripped_line))

            # Parse assignments
            if "=" in stripped_line and ";" in stripped_line:
                parsed_data["assignments"].append((i + 1, stripped_line))

        return parsed_data
