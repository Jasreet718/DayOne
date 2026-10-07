# Jasreet — Week 4: Evidence Lockers
# 60 lines go in, 8 are copies, 52 real cases come out and get counted.

# ---- Step 1: clean every line into a list ----
# Two lines for the same case must end up as the same text,
# or the set in Step 2 will not spot them as copies.
normalized = []                        # [] is an empty list

with open("data/wk04_data_raw_cases_dupes.txt") as case_file:
    for line in case_file:             # one line at a time, 60 turns
        clean = line.strip().upper()   # cut outside spaces, make letters big
        normalized.append(clean)       # add to the end of the list

# ---- Step 2: drop the copies with a set ----
# A set checks text exactly, so "CARTER" and "carter" look different to it.
# That is why the cleaning in Step 1 had to happen first.
unique = set(normalized)               # 60 in, 52 out

# ---- Step 3: get the ages, count open cases per beat ----
# These two go BEFORE the loop. Inside it, they would empty out every turn.
ages = []                              # list: every age
per_beat = {}                          # dict: beat -> count

for rec in unique:                     # go through the 52 records
    fields = rec.split("|")            # cut at every | . parts start at 0:
                                       # 0=name 2=age 5=beat 6=status
    age = int(fields[2].strip())       # text "25" -> number 25, so I can do math
    beat = fields[5].strip()           # like "BEAT 518"
    status = fields[6].strip()

    ages.append(age)                   # every age goes in, open or closed

    if status == "OPEN":               # only open cases get counted by beat
        # The first time I see a beat there is no number to add 1 to yet,
        # so I have to make it before I can grow it.
        if beat in per_beat:           # do I have this beat already?
            per_beat[beat] += 1        # yes -> add 1
        else:
            per_beat[beat] = 1         # no -> start it at 1

# ---- Step 4: print the report ----
# Nothing below is indented, so it runs once at the end, not once per record.
print("DEDUPE REPORT")
print(f"{'Lines in file:':<20}{len(normalized)}")   # len() counts the list
print(f"{'Unique records:':<20}{len(unique)}")
print(f"{'Duplicates removed:':<20}{len(normalized) - len(unique)}")   # 60 - 52
print()                                # empty print() = blank line

print("VICTIM AGE PROFILE")
# This is why a list was right for ages. min, max, sum and len come free.
print(f"Youngest {min(ages)} / Oldest {max(ages)} / Average {sum(ages) / len(ages):.1f}")
print()

print("OPEN CASES BY BEAT (most burdened first)")
# sorted(per_beat) gives the beat names.
# key=per_beat.get puts them in order by count instead of by name.
# reverse=True puts the biggest first.
for beat in sorted(per_beat, key=per_beat.get, reverse=True):
    count = per_beat[beat]             # the number saved under this beat
    bar = "#" * count                  # "#" * 4 is "####"
    print(f"{beat:<10}{count:>3}  {bar}")
