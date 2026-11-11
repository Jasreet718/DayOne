# lockers.py — Week 4: Evidence Lockers
# Dedupes the locker, profiles the victims, ranks the beats.


# open() finds the file and opens it. .readlines() reads the whole thing and
# hands back a LIST of strings — one string for each line in the file.
# So raw_lines holds 60 items, and raw_lines[0] is the first record.
raw_lines = open("data/wk04_data_raw_cases_dupes.txt").readlines()


# Step 2: normalize every line, collect into a list

# Square brackets with nothing inside make an EMPTY list.
# Right now it holds nothing. The loop below fills it up.
normalized = []

# "for line in raw_lines:" means: take one string out of raw_lines, call it
# "line", run the indented lines below, then come back and take the next one.
# It does this 60 times, once per record.
for line in raw_lines:

    # .strip() removes spaces from the front and back, including the invisible
    # "\n" newline character sitting at the end of every line from the file.
    # .upper() turns every letter into a capital, so "beat 537" becomes "BEAT 537".
    # Why bother? Because the computer compares text letter by letter. "beat" and
    # "BEAT" look the same to you, but to Python they are two different strings.
    # Forcing everything to capitals makes the real duplicates come out identical.
    clean = line.strip().upper()

    # .append() sticks one item onto the end of the list.
    # Pass 1 the list has 1 item, pass 2 it has 2... by the end it has all 60.
    normalized.append(clean)


# Step 3: dedupe

# A set is a container with one rule: it refuses to hold the same thing twice.
# Handing it a list of 60 strings gives back only the different ones — 52.
# The 8 that were exact copies get dropped automatically.
#
# This line comes AFTER the loop above on purpose. If I had deduped the raw
# lines instead, "beat 537" and "BEAT 537" would count as two separate records
# and almost nothing would be removed. Normalize first, dedupe second.
unique = set(normalized)


# Step 4: walk the UNIQUE records and collect

# A list, because I WANT the duplicates here. If three different victims are
# each 25 years old, all three ages need to count toward the average.
ages = []

# Curly braces make an empty DICTIONARY. A dictionary stores pairs: a label
# (the "key") and a value. Here the label is a beat number and the value is
# how many open cases it has, like {"537": 3, "731": 4}.
per_beat = {}

# Loop the 52 unique records — NOT the 60 normalized ones. If I looped the
# normalized list, the 8 duplicate victims would get counted twice.
for rec in unique:

    # rec is one whole record as a string, like:
    #   "NGUYEN, PATRICE|F|25|1992-09-01|1838 LAWRENCE STREET|BEAT 537|CLOSED"
    #
    # .split("|") chops it into a list wherever it finds a "|":
    #   ["NGUYEN, PATRICE", "F", "25", "1992-09-01", ..., "BEAT 537", "CLOSED"]
    # Then [2] grabs item number 2, counting from 0, which is the age.
    # .strip() cleans off leftover spaces, and int() turns the text "25" into
    # the actual number 25 so I can do math with it later.
    age = int(rec.split("|")[2].strip())

    # Same idea, item 5 is the beat, which reads "BEAT 537" after the .upper().
    # .replace("BEAT ", "") deletes the word "BEAT " and leaves just "537",
    # so the report can print "Beat 537" instead of "Beat BEAT 537".
    beat = rec.split("|")[5].strip().replace("BEAT ", "")

    # Item 6 is the status: "OPEN" or "CLOSED". It's already capitals because
    # the whole line was .upper()'d back in step 2.
    status = rec.split("|")[6].strip()

    # Drop this age in the bucket. No math yet — just collecting.
    # Gather everything first, ask questions about it later.
    ages.append(age)

    # == asks a question ("are these the same?"). A single = would ASSIGN
    # instead of ask, and Python would refuse to run the file.
    # Only open cases count toward the beat ranking.
    if status == "OPEN":

        # Here is the counting pattern, and here is why it needs two branches:
        # a dictionary label does not exist until you create it. Asking Python
        # to add 1 to a beat it has never seen crashes with a KeyError, because
        # there's no number there yet to add 1 to.
        #
        # "if beat in per_beat" asks: have I already made a locker for this beat?
        if beat in per_beat:
            # Yes — so there's already a number in there. Add one to it.
            per_beat[beat] += 1
        else:
            # No — this beat is brand new. Create its locker and put a 1 in it.
            per_beat[beat] = 1


# Step 5: the report

# len() counts how many items are in a list or a set. No loop required.
# The f in front of the quotes lets me drop a value into the text using {curly braces}.
print(f"Lines in file:      {len(normalized)}")     # 60 lines came in
print(f"Unique records:     {len(unique)}")         # 52 were actually different
print(f"Duplicates removed: {len(normalized) - len(unique)}")   # 60 - 52 = 8
print()                                             # print() alone = one blank line

# min() finds the smallest number in the list, max() the biggest, sum() adds
# them all together. Divide the sum by how many there are and you get the average.
# The :.1f part rounds it to one decimal, so it shows 39.1 instead of 39.096153846.
print(f"Youngest {min(ages)} / Oldest {max(ages)} / Average {sum(ages) / len(ages):.1f}")
print()

print("OPEN CASES PER BEAT")

# sorted(per_beat) on its own would sort the LABELS alphabetically: 214, 255, 326.
# That's useless for a ranking. The two extra settings fix that:
#   key=per_beat.get  -> "don't compare the beat names, look up each beat's
#                         COUNT and compare those numbers instead"
#   reverse=True      -> "biggest first" instead of smallest first
for beat in sorted(per_beat, key=per_beat.get, reverse=True):

    # Look up how many open cases this beat has: per_beat["731"] gives 4.
    count = per_beat[beat]

    # Multiplying a string repeats it. "#" * 4 gives "####".
    # That's a bar chart with no libraries at all.
    bar = "#" * count

    # :<6 pads the beat to 6 characters, lined up on the left.
    # :>3 pads the count to 3 characters, lined up on the right.
    # That's what keeps the columns straight down the page.
    print(f"Beat {beat:<6}{count:>3}  {bar}")
