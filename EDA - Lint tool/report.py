def report_generator(statement_lists):
    with open('report.txt', 'w') as f:
        for item in statement_lists:
            f.write("%s\n" % item)
    print("Report Generated Successfully")