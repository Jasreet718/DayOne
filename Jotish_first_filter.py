# ============================================================
# first_filter.py
# Week 3 Squad Lab: The First Filter
# ============================================================

# THE MISSION:
#   1. Read every line out of data/wk03_data_raw_cases_50.txt
#   2. Parse it into fields, same idea as intake.py
#   3. Print name + years_unsolved for every record
#   4. Flag *** STALE *** for OPEN cases that are 5+ years old
#   5. Keep running totals (accumulators) as I walk the file
#   6. Print the final counts report once the loop is completely done

# This line creates a variable called STALE_YEARS and sets it to 5.
STALE_YEARS = 5

# This line sets CURRENT_YEAR to 2026. 
CURRENT_YEAR = 2026

# This line stores the file path to this week's data file in a
# variable called DATA_FILE, so the open() call below can just refer
# to this variable instead of retyping the path.
DATA_FILE = "data/wk03_data_raw_cases_50.txt"

# Will count every real (non-blank) record processed. Starts at 0
total_records = 0

# Will count how many records have status "OPEN". Starts at 0.
open_count = 0

# Will count how many records are both open and stale. Starts at 0.
stale_count = 0

# Will count open cases where the victim's age is under 18. Starts at 0.
juvenile_open_count = 0

# Sets oldest_year to CURRENT_YEAR. I'm starting it deliberately high, 
# on purpose, so that the very first open case I look at will always be 
# "older" than this starting value.
oldest_year = CURRENT_YEAR

# Will hold the name that goes with oldest_year.
oldest_name = ""

# This line prints a header row for my table of results. The
# f-string uses :<26 and :<6 and :<16 to left-align each column and
# pad it with spaces to a fixed width, so everything lines up neatly
# no matter how long each individual value is.
print(f"{'CASE':<26}{'AGE':<6}{'YEARS UNSOLVED':<16}{'FLAG'}")

# prints a blank line 
print()

# This line opens the data file for reading and names it f. Using
# "with" means Python will automatically close the file for me once
# I'm done with it, even if an error happens somewhere inside.
with open(DATA_FILE) as f:
    # This line reads every line in the file into a list of strings
    # and names that list "records,".
    records = f.readlines()

# This line starts a for loop that goes through the records list one
# line at a time. Each time through the loop, the variable "line"
# holds exactly one raw record as it was written in the file.
for line in records:
    # This line overwrites "line" with a cleaned-up version of
    # itself: .strip() removes the newline character at the end and
    # any extra spaces at the very start or end of the text.
    line = line.strip()

    # If, after stripping, the line has nothing left in it (a blank line from the file), 
    # skip everything below and jump to the next line in the list.
    if line == "":
        continue                               

    # This line splits the record into a list of pieces every place
    # it finds the "|" character, so I end up with a list like
    # ["Trammell, Monica ", " m ", " 39 ", ...] with the extra spaces
    # still attached.
    fields = line.split("|")

    # Takes piece 0 (the name), strips extra spaces, 
    # then .title() turns "TRAMMELL, MONICA" into "Trammell, Monica."
    name = fields[0].strip().title()

    # Takes piece 1 (sex code), strips spaces, .upper() forces it to a 
    # capital letter like "M" regardless of how it was originally typed.
    sex = fields[1].strip().upper()

    # This line pulls out field 2, the age, strips off any extra
    # spaces, and wraps the result in int() to convert it from text
    # like "39" into an actual number I can do math and comparisons
    # with.
    age = int(fields[2].strip())

    # This line pulls out field 3, the date, strips it, and then
    # slices out just the first four characters — the year — before
    # converting that to a number with int().
    year = int(fields[3].strip()[0:4])

    # Takes piece 5 (a location code), strips spaces. 
    # Note: parsed but not currently used anywhere later in the script.
    beat = fields[5].strip()

    # Takes piece 6 (open/closed status), strips spaces, .upper() forces 
    # it to "OPEN" or "CLOSED" regardless of original casing.
    status = fields[6].strip().upper()

    # This line calculates how many years the case has been unsolved
    # by subtracting the case's year from CURRENT_YEAR.
    years_unsolved = CURRENT_YEAR - year

    # This line adds 1 to total_records, since this is a real record
    # that made it past the blank-line check.
    total_records = total_records + 1

    # This line checks two conditions at once using "and": is the
    # status OPEN, and has it been unsolved for STALE_YEARS or more
    # years. Both conditions have to be true for this branch to run.
    if status == "OPEN" and years_unsolved >= STALE_YEARS:
        # This line sets flag to the text "*** STALE ***" so that
        # when I print this record, it's visibly marked as an old
        # open case that needs attention.
        flag = "*** STALE ***"
    else:
        # This line sets flag to an empty string for every record
        # that isn't an old open case, so closed cases and recent
        # open cases print with no flag at all.
        flag = ""

    # This line prints one row of my results table: the name, the
    # age, how many years it's been unsolved, and the flag, all lined
    # up in fixed-width columns using the same :< formatting as the
    # header.
    print(f"{name:<26}{age:<6}{years_unsolved:<16}{flag}")

    # This line checks if the case is currently OPEN. Everything
    # indented under this if-statement only updates my accumulators
    # for open cases, not closed ones.
    if status == "OPEN":
        # This line adds 1 to open_count
        open_count = open_count + 1

        # This line checks if this open case has also been unsolved
        # for STALE_YEARS or more.
        if years_unsolved >= STALE_YEARS:
            # This line adds 1 to stale_count, so by the end of the
            # loop it holds the total number of open cases that are
            # also stale.
            stale_count = stale_count + 1

        # This line checks if the age is less than 18, meaning the
        # victim was a minor.
        if age < 18:
            # This line adds 1 to juvenile_open_count, so by the end
            # of the loop it holds how many open cases involve a
            # victim under 18.
            juvenile_open_count = juvenile_open_count + 1

        # This line compares this record's year to oldest_year to see
        # if this case is older than the oldest one I've found so far
        # while looping.
        if year < oldest_year:
            # This line updates oldest_year to this record's year,
            # since it just confirmed it's the new oldest one.
            oldest_year = year

            # This line updates oldest_name to this record's name at
            # the same time, so the name and year never get out of
            # sync with each other.
            oldest_name = name

# This line prints a blank line to separate the row-by-row output
# above from the summary report below. 
print()

# This line prints the total number of records I processed.
print(f"Total records:        {total_records}")

# This line prints how many of those records had a status of OPEN.
print(f"Open cases:           {open_count}")

# This line prints how many open cases were also stale, and it uses
# the STALE_YEARS variable inside the f-string so the label always
# matches whatever threshold I actually used.
print(f"Stale (>= {STALE_YEARS} yrs):     {stale_count}")

# This line prints the name and year of the single oldest open case I
# found while looping through the whole file.
print(f"Oldest open case:     {oldest_name} ({oldest_year})")

