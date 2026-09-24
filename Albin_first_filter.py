# first_filter.py
# Sweeps all 50 case records, flags stale open cases, and reports counts.

# Step 1: load the data
with open("data/wk03_data_raw_cases_50.txt", "r") as f:  # open() gives a file handle; "r" = read mode; "with" auto-closes it when we're done
    records = f.readlines()  # reads the whole file in one go and returns a list, one string per line (each still has a trailing \n on it)

# Step 2: accumulators, set up before the loop so they don't reset each pass
total = 0                # starts at 0, goes up by 1 every time we successfully process a record
open_count = 0            # starts at 0, goes up by 1 every time we see a record with status OPEN
stale_count = 0           # starts at 0, goes up by 1 every time an OPEN record is also 5+ years old
juvenile_open_count = 0   # starts at 0, goes up by 1 every time an OPEN record has age under 18
oldest_year = 2026        # start artificially high (later than any real case) so the very first open case we check is guaranteed to beat it
oldest_name = ""          # will hold whatever name goes with oldest_year, updated together with it below

# Step 3: loop over every record
for line in records:  # "for line in records" runs everything indented below once per item in the list, naming the current one "line" each time
    line = line.strip()  # strip() removes leading/trailing spaces and the invisible \n newline character left over from readlines()
    if line == "":        # after stripping, an empty string means this was a blank line in the file
        continue          # jumps straight to the next record in the loop, skipping every line below for this pass

    fields = line.split("|")  # split() breaks the string apart everywhere it sees "|", giving back a list of 7 text pieces

    name = fields[0].strip().title()   # index 0 is the name; strip() cleans stray spaces, .title() turns "TRAMMELL, MONICA" into "Trammell, Monica"
    age = int(fields[2].strip())        # index 2 is age, stored as text like " 39 "; strip() cleans it, int() converts the text into a real number
    date = fields[3].strip()            # index 3 is the date, e.g. "2014-06-11"; cleaned with strip() but kept as text for now
    year = int(date[0:4])               # date[0:4] slices out just the first 4 characters of the date string (the year), then int() makes it a number
    status = fields[6].strip().upper()  # index 6 is status; strip() cleans spaces, .upper() standardizes it to "OPEN"/"CLOSED" since comparisons are case-sensitive

    total = total + 1  # this line was real (not blank), so it counts toward our total no matter what its status turns out to be

    if status == "CLOSED":  # this check happens before we do any of the OPEN-only work below
        continue             # if it's closed, skip straight to the next record; everything below only applies to open cases

    years_unsolved = 2026 - year  # simple subtraction: how many years between the case's year and our reference year, 2026

    # if/elif/else is checked top to bottom and stops at the first True branch, so the most serious condition has to go first
    if years_unsolved >= 5:      # 5 or more years unsolved is the most serious bucket
        flag = "*** STALE ***"
    elif years_unsolved >= 2:    # only reached if the line above was False; catches 2-4 years
        flag = "aging"
    else:                         # only reached if both checks above were False; catches 0-1 years
        flag = "recent"

    open_count = open_count + 1  # we only get to this line if status wasn't CLOSED, so this record is definitely OPEN

    if years_unsolved >= 5:            # separate check from the flag above, just so we can update our stale counter
        stale_count = stale_count + 1   # this OPEN case is also 5+ years old, so it counts as stale

    if age < 18:                              # checking if this specific case involves someone under 18
        juvenile_open_count = juvenile_open_count + 1  # if so, add 1 to our juvenile-open counter

    if year < oldest_year:   # compare this case's year against the oldest year we've recorded so far
        oldest_year = year    # if this one is older (smaller year number), it becomes the new record-holder
        oldest_name = name    # and we save this case's name to go along with that year

    print(f"{flag} {name} - OPEN since {year} ({years_unsolved} years)")  # prints one line per open case, showing its flag, name, year, and age of the case

# Step 4: report, runs once after the loop is fully done (this code is not indented, so it's outside the for loop and only runs one time)
print()
print("Total records:", total)                                    # every record we processed, blank lines never made it this far
print("Open cases:", open_count)                                  # how many of those records had status OPEN
print("Stale (>= 5 yrs):", stale_count)                            # how many OPEN cases were also 5+ years old
print("Oldest open case:", oldest_name, f"({oldest_year})")        # the single oldest OPEN case out of all 50 records
