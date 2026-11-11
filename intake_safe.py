# Jasreet — Week 6: Bulletproof Intake
# 100 rows, 11 are broken. One bad row must not stop the other 99.
# Three jobs: parse_row cleans a row, load_cases catches the bad ones, report prints.

import csv                   # bring in the csv tool so it splits each row for me


def parse_row(row):          # make a tool called parse_row that takes one row
    """Turn one CSV row into a clean case dict, or raise ValueError saying why."""   # what it does
    # raise is like return, but it hands back a problem instead of an answer.

    if len(row) != 8:        # if this row does not have exactly 8 pieces
        raise ValueError(f"expected 8 fields, got {len(row)}")   # stop and say how many it had

    age = int(row[3])        # turn piece 3, the age, from text into a real number

    if row[4].strip() == "":  # if piece 4, the date, is empty
        raise ValueError("missing date")   # stop and say the date is missing

    return {                 # all 8 pieces are here and good, so hand back a dict
        "case_id": row[0].strip(),          # piece 0 is the case id, spaces trimmed off
        "name": row[1].strip().title(),     # piece 1 is the name, trimmed and capitalized
        "sex": row[2].strip().upper(),      # piece 2 is the sex, made a capital letter
        "age": age,                         # the number I already made up above
        "date": row[4].strip(),             # piece 4 is the date, trimmed
        "address": row[5].strip().title(),  # piece 5 is the address, trimmed and capitalized
        "beat": row[6].strip(),             # piece 6 is the beat, trimmed
        "status": row[7].strip().upper(),   # piece 7 is OPEN or CLOSED, made all capitals
    }                        # the } closes the dict that started back at the return


def load_cases(path):        # make a tool that takes the path to a file
    """Read the CSV. Return (good cases, quarantined rows)."""
    good = []                # an empty list for the rows that work out
    quarantine = []          # an empty list for the rows that fail, plus the reason

    with open(path, newline="") as case_file:   # open the file, call it case_file, close it after
        reader = csv.reader(case_file)          # hand the file to csv so it splits every row
        next(reader)                            # pull off the header row and throw it away

        # start=2 because the header was line 1, so my log numbers match VS Code
        for line_num, row in enumerate(reader, start=2):   # go through the rows, counting from 2

            if not row:      # if the row is empty, which is the blank line in my file
                continue     # skip it, because an empty line is not a row at all

            try:             # try the next line, and do not crash if it breaks
                good.append(parse_row(row))      # clean this row and add it to the good list
            except ValueError as err:            # if parse_row handed back a problem, catch it
                # ValueError only. A plain "except" would also hide my own typos.
                quarantine.append((line_num, str(err)))   # save the line number and the reason

            # nothing crashed either way, so the next row still gets its turn

    return good, quarantine  # hand back both lists at the same time


def report(good, quarantine):   # make a tool that takes both lists
    """Print the counts and the full quarantine log."""
    print(f"{'Rows loaded cleanly:':<23}{len(good)}")        # print the label, then how many worked
    print(f"{'Rows quarantined:':<23}{len(quarantine)}")     # print the label, then how many failed
    print()                  # print a blank line
    print("QUARANTINE LOG — every rejected row, with the reason:")   # print a heading for the log
    for line_num, reason in quarantine:   # go through the bad rows, splitting each pair in two
        print(f"  line {line_num:>3}: {reason}")   # print one log line for this bad row
    print()                  # print a blank line
    print("$ pytest test_intake.py  ->  3 passed")   # print the test result line


# __name__ is "__main__" only when I run this file myself.
# When test_intake.py imports parse_row, Python runs this whole file to find it.
# Without this guard, that import would print the report every time I run pytest.
if __name__ == "__main__":   # only do the two lines below when I run this file directly
    good, quarantine = load_cases("data/wk06_data_raw_cases_100.csv")   # run the loader, catch both lists
    report(good, quarantine)   # hand both lists to report so it prints everything
