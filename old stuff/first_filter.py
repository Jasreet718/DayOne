# first_filter.py — Week 3: The First Filter
# Sweeps all 50 records, flags stale open cases, and reports the counts.


# open() opens the file, and .readlines() reads it into a LIST of strings —
# one string per line of the file. So records looks like:
# ["  TRAMMELL, MONICA|m|39|...|OPEN\n", "    Pruitt, Patrice | m | ...", ...]
# with 50 items in it. Last week I typed each record out by hand as its own
# variable; this one line replaces all of that.
records = open("data/wk03_data_raw_cases_50.txt").readlines()


# ---- ACCUMULATORS ----
# These all live OUT here, before the loop. That matters: if I indented them
# under the for loop they'd get reset back to 0 on every single record, and my
# final counts would come out as 1 instead of 29.

total_records = 0     # counts every record I actually parse (open AND closed)
open_count = 0        # counts just the OPEN ones
stale_count = 0       # counts OPEN cases that are 5+ years old
juvenile_count = 0    # counts OPEN cases where the victim was under 18

# For "oldest" I start the tracker at the WORST possible value and let the real
# data beat it. Any case year (1980, 2014...) is smaller than 2026, so the very
# first open case wins immediately and then better answers replace it as I go.
# If I started at 0 instead, nothing could ever be "less than" it and the answer
# would stay stuck at 0 forever.
oldest_year = 2026        # start high so the first real case beats it
oldest_name = ""          # empty string for now, gets filled in by the loop


# ---- THE LOOP ----
# "for line in records:" means: take each string out of the list one at a time,
# call it "line", and run everything indented below once for that record.
# 50 records, but only ONE copy of the code. That's the whole point of week 3.
for line in records:

    # .strip() removes whitespace from the very start and end of the line,
    # including the invisible "\n" newline character at the end of every line
    # that came from the file.
    line = line.strip()

    # The bouncer at the door. Real files have blank lines in them. If a blank
    # line got past here, line.split("|") would give me a list with only one
    # item, and fields[2] below would crash with an IndexError.
    # "continue" means: stop working on this one, jump back up to the for loop,
    # and grab the next record.
    if line == "":
        continue          # skip blanks, keep looping

    # .split("|") chops the string into a list, cutting it everywhere it finds
    # a "|". I split on the BARE pipe (not " | ") because some records are
    # written "A|B" and others "A | B" — splitting on the bare pipe handles both,
    # and then I .strip() each piece below to clean off any leftover spaces.
    # fields ends up like:
    # ['TRAMMELL, MONICA', 'm', '39', '2014-06-11', '431 KIEST BLVD', 'beat 352', 'OPEN']
    fields = line.split("|")

    # Now I pull out the pieces I need by their position (index), counting from 0.
    # I'm only grabbing the 4 fields this report actually uses — no point cleaning
    # up the address or beat when nothing below ever looks at them.
    name = fields[0].strip().title()       # 'TRAMMELL, MONICA' -> 'Trammell, Monica'
    age = int(fields[2].strip())           # '39' is TEXT. int() makes it the number 39
                                           # so I can actually compare it with < below.
    year = int(fields[3].strip()[0:4])     # '2014-06-11' -> [0:4] slices the first 4
                                           # characters -> '2014' -> int() -> 2014
    status = fields[6].strip().upper()     # 'open  ' -> strip -> 'open' -> upper -> 'OPEN'
                                           # strip FIRST, because 'OPEN  ' == 'OPEN' is False!

    # Plain math, only possible because year is a real number and not text.
    years_unsolved = 2026 - year

    # This counter is OUTSIDE the "if status" check below, so it counts every
    # record — open or closed. That's why the total comes out 50 and not 29.
    total_records = total_records + 1

    # Everything from here down is indented under this if, so it ONLY happens
    # for cases with no arrest yet. That indentation is doing real work: it's the
    # difference between "27 stale open cases" and "45 stale cases overall".
    if status == "OPEN":

        # Reads as: take what open_count is holding, add 1, put it back.
        open_count = open_count + 1

        # age is a number, so this comparison works. If age were still the
        # string '39' this would crash.
        if age < 18:
            juvenile_count = juvenile_count + 1

        # The min-tracker from slide 7: is this case older than the oldest one
        # I've seen so far? If yes, it's the new record holder. I have to update
        # BOTH variables together, or I'd end up with the wrong name attached
        # to the right year.
        if year < oldest_year:
            oldest_year = year
            oldest_name = name

        # The flag. >= means "5 or more", so a case open exactly 5 years counts.
        if years_unsolved >= 5:
            stale_count = stale_count + 1
            print(f"{name} - {years_unsolved} years *** STALE ***")
        else:
            # else = everything left over: open, but less than 5 years old.
            print(f"{name} - {years_unsolved} years")


# ---- THE REPORT ----
# These lines are NOT indented, so they're outside the loop. They run once, at
# the very end, after all 50 records have been walked. By now the accumulators
# are holding their final totals. If I indented these into the loop by mistake,
# I'd print the whole report 50 times.
print()
print(f"Juveniles among open cases: {juvenile_count}")
print()
print(f"Total records:        {total_records}")
print(f"Open cases:           {open_count}")
print(f"Stale (>= 5 yrs):     {stale_count}")
print(f"Oldest open case:     {oldest_name} ({oldest_year})")
