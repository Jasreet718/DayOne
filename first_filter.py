# Jasreet — Week 3: Operation First Filter

# ---- Numbers I can change ----
CURRENT_YEAR = 2026        # the year we count from
STALE_YEARS = 5            # 5 years or older = stale

# ---- Counters. These go BEFORE the loop so they don't reset ----
total_records = 0          # how many records total
open_count = 0             # how many are OPEN
stale_count = 0            # how many OPEN ones are old
juvenile_count = 0         # how many OPEN ones are under 18
oldest_year = CURRENT_YEAR # start high so any real year is smaller
oldest_name = ""           # the name for that year

print("FLAGGED OPEN CASES")
print()

# ---- Open the file and read one line at a time ----
with open("data/wk03_data_raw_cases_50.txt") as case_file:
    for line in case_file:             # this runs once per line

        # ---- Skip bad lines so nothing crashes ----
        line = line.strip()            # take off spaces and the newline
        if line == "":                 # nothing on this line
            continue                   # skip it, go to the next line

        fields = line.split("|")       # cut the line at every |
        if len(fields) < 7:            # missing pieces
            continue                   # skip it, go to the next line

        # ---- Pull out each piece and clean it ----
        name = fields[0].strip().title()          # piece 0 = name
        sex = fields[1].strip().upper()           # piece 1 = sex
        age = int(fields[2].strip())              # "39" the text -> 39 the number
        date = fields[3].strip()                  # "2014-06-11"
        year = int(date[0:4])                     # first 4 letters = 2014
        addr = fields[4].strip().title()          # piece 4 = address
        beat = fields[5].strip().title()          # piece 5 = beat
        status = fields[6].strip().upper()        # make it CAPS so it matches "OPEN"

        years_unsolved = CURRENT_YEAR - year      # how old the case is

        # ---- Count things INSIDE the loop ----
        total_records = total_records + 1         # count every record

        if status == "OPEN":                      # only open cases below here
            open_count = open_count + 1

            if age < 18:                          # under 18
                juvenile_count = juvenile_count + 1

            # Python picks the FIRST one that is true, then stops.
            if years_unsolved >= STALE_YEARS:     # 5 years or more
                flag = "*** STALE ***"
                stale_count = stale_count + 1
            elif years_unsolved >= 2:             # 2 to 4 years
                flag = "aging"
            else:                                 # under 2 years
                flag = "recent"

            if year < oldest_year:                # older than the one I saved?
                oldest_year = year                # save the new year
                oldest_name = name                # and the new name

            print(f"{name:<24}{years_unsolved:>4} yrs   {flag}")

# ---- Print the totals AFTER the loop. No indent = runs once ----
print()
print("CASE REPORT")
print(f"{'Total records:':<22}{total_records}")
print(f"{'Open cases:':<22}{open_count}")
print(f"{'Stale (>= 5 yrs):':<22}{stale_count}")
print(f"{'Juveniles (open):':<22}{juvenile_count}")
print(f"{'Oldest open case:':<22}{oldest_name} ({oldest_year})")
