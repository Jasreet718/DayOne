# intake_safe.py — Week 6: Bulletproof Intake
# Loads 100 CSV rows, quarantines the damaged ones, crashes on nothing.

# The csv module knows how to split a CSV line properly — including commas
# sitting INSIDE a quoted field, like "KIRKLAND, MONICA, JR, III".
# A plain .split(",") would tear that name into four pieces.
import csv


# Takes one row (a list of fields) and hands back a clean dictionary.
# If the row is damaged it doesn't return anything — it RAISES instead.
def parse_row(row):
    """One CSV row in, one clean case dict out. Raises ValueError if damaged."""
    # Trap 1: truncated rows. Some rows only have 6 fields, so reaching for
    # row[6] or row[7] below would blow up with an IndexError. Checking the
    # length FIRST means I control the error instead of Python surprising me.
    # "raise" throws the error on purpose, with a reason attached.
    if len(row) != 8:
        # The f-string drops the actual count into the message, so the log
        # says "got 6" rather than just "wrong length".
        raise ValueError(f"expected 8 fields, got {len(row)}")

    # Trap 2: ages like 'unknown'. int() raises ValueError all by itself here —
    # I don't have to check for it. I just let it happen and catch it upstairs.
    age = int(row[3])

    # Trap 3: empty date fields. Nothing crashes on an empty string, so this
    # one I have to notice myself and raise deliberately.
    if row[4].strip() == "":
        # My own wording this time, not Python's — nothing went wrong
        # mechanically, the field is just empty.
        raise ValueError("missing date")

    # Survived all three traps, so build the dictionary. Keys are labels,
    # values are the cleaned-up fields — same .strip()/.title()/.upper()
    # cleanup as every week before this one.
    return {
        "case_id": row[0].strip(),            # 'CC-20001', spaces trimmed
        "name": row[1].strip().title(),       # 'OKAFOR, TASHA' -> 'Okafor, Tasha'
        "sex": row[2].strip().upper(),        # 'm' -> 'M'
        "age": age,                           # already the int from above
        "date": row[4].strip(),               # '2011-10-24', kept as text
        "address": row[5].strip().title(),    # '9897 BUCKNER BLVD' -> title case
        "beat": row[6].strip(),               # '623', left as text
        "status": row[7].strip().upper(),     # 'closed  ' -> 'CLOSED'
    }


# Takes a file path, hands back TWO lists: the rows that loaded and the ones
# that didn't. Returning both is the whole point — load what's loadable,
# report what isn't.
def load_cases(path):
    """Every loadable row from the CSV, plus a log of the ones that failed."""
    # Two empty lists, set up before the loop so they don't reset each pass.
    good = []        # the clean dictionaries pile up here
    quarantine = []  # and the (line number, reason) pairs pile up here

    # "with" guarantees the file closes even if something explodes mid-read.
    # newline="" is what the csv module asks for, so it handles line endings.
    with open(path, newline="") as f:
        # Wraps the file in a reader that hands me each row as a LIST.
        reader = csv.reader(f)
        # next() pulls exactly one row — the header — and throws it away,
        # so the loop below only ever sees real data.
        header = next(reader)

        # start=2 because the header was line 1, so the first data row is
        # line 2. That makes line_num match what VS Code shows me.
        for line_num, row in enumerate(reader, start=2):
            # A blank line in the file comes through as an empty list [].
            # It isn't a damaged record, it's not a record at all, so skip it
            # entirely — don't load it, don't quarantine it.
            if row == []:
                # "continue" means: nothing more to do with this one, jump
                # back to the for and grab the next line.
                continue

            # try: attempt the risky thing.
            try:
                # If parse_row succeeds, its dictionary goes on the good pile.
                good.append(parse_row(row))
            # except: catch the SPECIFIC error. ValueError, never a bare
            # "except:" — a bare one would swallow my own typos and bugs too,
            # and the PR gets bounced for it.
            # "as err" gives me the error object so I can read its message.
            except ValueError as err:
                # Log the line number and the reason, then keep looping.
                # str(err) turns the error into its message text.
                quarantine.append((line_num, str(err)))

    # Hand both lists back to the caller as a pair.
    return good, quarantine


# Everything below only runs when I launch THIS file directly, with
# "python3 intake_safe.py". Python sets __name__ to "__main__" in that case.
# When some other file imports me instead — like test_intake.py doing
# "from intake_safe import parse_row" — __name__ is "intake_safe", this is
# False, and the report is skipped. Without this guard, importing the file
# would run the whole report as a side effect, and pytest would crash on
# FileNotFoundError whenever it was started from another folder.
if __name__ == "__main__":

    # Call the loader. Because it returns two things, I can unpack them into
    # two variables in one line.
    good, quarantine = load_cases("data/wk06_data_raw_cases_100.csv")

    # len() counts the items on each pile. The extra spaces inside the quotes
    # are what line the two numbers up under each other.
    print(f"Rows loaded cleanly:   {len(good)}")
    # Same idea for the second pile. These two must add up to 100.
    print(f"Rows quarantined:      {len(quarantine)}")
    # print() with nothing in it prints one blank line, as a separator.
    print()
    # A plain heading for the log that follows. No f needed — no values in it.
    print("QUARANTINE LOG — every rejected row, with the reason:")

    # Walk the quarantine list. Each item is a pair, so I unpack it into two
    # variables right in the for statement.
    for line_num, reason in quarantine:
        # :>3 pads the line number to 3 characters, right-aligned, so the
        # reasons line up in a column.
        print(f"  line {line_num:>3}: {reason}")

    # Slide 13 lists the pytest result as part of the week's report, so it
    # gets printed here. It's plain text, so it does not check anything —
    # run "pytest test_intake.py" to actually verify it.
    print()
    # The $ at the front is just the terminal prompt, copied from the slide so
    # the line reads like a command someone typed.
    print("$ pytest test_intake.py  ->  3 passed")


