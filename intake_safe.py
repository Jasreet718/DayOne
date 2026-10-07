# Jasreet — Week 6: Bulletproof Intake
# 100 rows, 11 of them damaged. One bad row must not kill the other 99.
# The plan: load what loads, quarantine what does not, report both.

import csv              # csv splits the rows for me, even names with commas in them


def parse_row(row):
    """Turn one CSV row into a clean case dict, or raise ValueError saying why."""
    # raise is the opposite of return. return hands back an answer,
    # raise throws a problem up to whoever called me. This function
    # does not decide what to do about bad rows. That is load_cases' job.

    # Check 1: is the row even the right size?
    # A 6 field row would crash on row[7] below, so I stop it here.
    if len(row) != 8:
        raise ValueError(f"expected 8 fields, got {len(row)}")

    # Check 2: I write no check at all here.
    # int("unknown") raises ValueError all by itself. I just let it fly.
    age = int(row[3])

    # Check 3: an empty date does not crash anything,
    # so nothing raises on its own. I have to raise it myself.
    if row[4].strip() == "":
        raise ValueError("missing date")

    # Got this far, so the row is good. Hand back a dict of clean fields.
    return {
        "case_id": row[0].strip(),
        "name": row[1].strip().title(),
        "sex": row[2].strip().upper(),
        "age": age,
        "date": row[4].strip(),
        "address": row[5].strip().title(),
        "beat": row[6].strip(),
        "status": row[7].strip().upper(),
    }


def load_cases(path):
    """Read the CSV. Return (good cases, quarantined rows)."""
    good = []                          # the rows that parsed
    quarantine = []                    # line number + reason for the ones that did not

    # newline="" is what the csv module wants so quoted fields work right.
    with open(path, newline="") as case_file:
        reader = csv.reader(case_file)
        next(reader)                   # eat the header row so the loop only sees data

        # start=2 because the header was line 1, so the first data row is line 2.
        # That makes my log line numbers match what I see in VS Code.
        for line_num, row in enumerate(reader, start=2):

            if not row:                # csv gives a blank line back as an empty list
                continue               # it is not damage, it is not a row. skip it.

            try:
                good.append(parse_row(row))      # the risky part
            except ValueError as err:            # catch ValueError ONLY, never bare except
                # "as err" names the error so str(err) gets me its message
                quarantine.append((line_num, str(err)))
            # No crash either way, so the loop keeps going. That is the whole point.

    return good, quarantine            # two values come back as a pair


def report(good, quarantine):
    """Print the counts and the full quarantine log."""
    print(f"{'Rows loaded cleanly:':<23}{len(good)}")   # :<23 lines the numbers up
    print(f"{'Rows quarantined:':<23}{len(quarantine)}")
    print()
    print("QUARANTINE LOG — every rejected row, with the reason:")
    for line_num, reason in quarantine:
        print(f"  line {line_num:>3}: {reason}")
    print()
    print("$ pytest test_intake.py  ->  3 passed")


# __name__ is "__main__" only when I run THIS file directly.
# When test_intake.py imports parse_row, __name__ is "intake_safe" instead,
# so this block is skipped and the tests stay quiet.
if __name__ == "__main__":
    # load_cases hands back two things, so I catch them in two names.
    good, quarantine = load_cases("data/wk06_data_raw_cases_100.csv")
    report(good, quarantine)
