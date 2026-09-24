# Jasreet — Week 4: Operation Evidence Lockers

# ---- Step 1: normalize every line into a list ----
normalized = []

with open("data/wk04_data_raw_cases_dupes.txt") as case_file:
    for line in case_file:
        clean = line.strip().upper()   # same spacing, same caps
        if clean == "":                # blank line at the end of the file
            continue                   # skip it
        normalized.append(clean)       # add to the end of the list

# ---- Step 2: dedupe with a set (AFTER normalizing) ----
unique = set(normalized)               # a set keeps one of each

# ---- Step 3: collect ages, count open cases per beat ----
ages = []                              # list: every age
per_beat = {}                          # dict: beat -> count

for rec in unique:
    fields = rec.split("|")
    age = int(fields[2].strip())       # "25" the text -> 25 the number
    beat = fields[5].strip()
    status = fields[6].strip()

    ages.append(age)

    if status == "OPEN":
        if beat in per_beat:           # seen this beat before?
            per_beat[beat] += 1        # yes -> add 1
        else:
            per_beat[beat] = 1         # no -> start it at 1

# ---- Step 4: the report ----
print("DEDUPE REPORT")
print(f"{'Lines in file:':<20}{len(normalized)}")
print(f"{'Unique records:':<20}{len(unique)}")
print(f"{'Duplicates removed:':<20}{len(normalized) - len(unique)}")
print()

print("VICTIM AGE PROFILE")
print(f"Youngest {min(ages)} / Oldest {max(ages)} / Average {sum(ages) / len(ages):.1f}")
print()

print("OPEN CASES BY BEAT (most burdened first)")
for beat in sorted(per_beat, key=per_beat.get, reverse=True):
    count = per_beat[beat]
    bar = "#" * count                  # "#" times 4 makes "####"
    print(f"{beat:<10}{count:>3}  {bar}")
