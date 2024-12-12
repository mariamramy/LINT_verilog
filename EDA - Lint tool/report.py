def write_report(violations, filename):
    with open(filename, "w") as report:
        for violation in violations:
            report.write(
                f"{violation['check']} - Line {violation['line']}: {violation['details']}\n"
            )
