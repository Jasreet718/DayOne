# This is the raw record I'm working with. It's one long string with each
# piece of info separated by " | " so I can split it apart later.
record5 = " BOOKER, TERRENCE | M | 41 | 2018-11-08 | 907 n. calloway drive | Beat 442 | OPEN "

#step 1
# .strip() removes any extra spaces from the very start/end of the string.
# .split(" | ") breaks the string into a list, cutting it wherever " | " shows up.
# So fields ends up being a list like:
# ["BOOKER, TERRENCE", "M", "41", "2018-11-08", "907 n. calloway drive", "Beat 442", "OPEN"]
fields = record5.strip().split(" | ")

#step 2
# Now I'm pulling each piece out of the list by its index (position),
# starting at 0, and cleaning it up a bit.
name = fields[0].title()   # .title() makes it "Booker, Terrence" instead of all caps
sex = fields[1].upper()    # .upper() just makes sure it's a capital letter like "M"
age = int(fields[2])       # this comes in as a string like "41", so int() converts it to a real number
date = fields[3]           # keeping this one as a string, e.g. "2018-11-08"
year = int(date[0:4])      # date[0:4] slices out just the first 4 characters (the year), then int() converts it
addr = fields[4].title()   # .title() capitalizes each word in the address
status = fields[6]         # note: fields[5] would be "Beat 442", I'm skipping that and grabbing "OPEN"

# Step 3: compute
# Simple math: subtract the case's year from the "current" year (2026) I'm using
# for this assignment, to get how many years it's been unsolved.
years_unsolved = 2026 - year

# Step 4: report
# Building the final sentence using an f-string, which lets me drop variables
# directly into the text with {curly braces}. The backslash at the end of the
# first line just tells Python "this string continues on the next line" so it
# doesn't turn it into two separate f-strings.
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)  # finally, print the finished summary line
