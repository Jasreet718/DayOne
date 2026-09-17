#Header
print(f"{'CASE':<26}{'AGE':<8}{'YEARS UNSOLVED'}")
print()


record2 = "reyes, miguel|M|32|2018-05-17| 3308 DELAFORD STREET |Beat 347|open"

#Step 1
fields = record2.strip().split("|")

#Step 2
name = fields[0].title()
sex = fields[1].upper()
age = int(fields[2])
date = fields[3]
year = int(date[0:4])
addr = fields[4].strip().title()
status = fields[6].strip().upper()

# Step 3
years_unsolved = 2026 - year

# Step 4
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)



record3 = "OKAFOR, SAMUEL J | M | 55 | 2018-07-09 | 1519 westhollow avenue | beat 341 | OPEN"  # raw pipe-delimited case record

#Step 1
fields = record3.strip().split(" | ")  # remove leading/trailing whitespace, then split into a list on " | "

#Step 2
name = fields[0].title()  # field 0: name, converted to Title Case
sex = fields[1].upper()  # field 1: sex, converted to uppercase
age = int(fields[2])  # field 2: age, converted from string to int
date = fields[3]  # field 3: date the case was opened, kept as a string
year = int(date[0:4])  # first 4 characters of the date string, converted to int
addr = fields[4].title()  # field 4: address, converted to Title Case
status = fields[6].upper()  # field 6: case status, converted to uppercase

# Step 3
years_unsolved = 2026 - year  # subtract the case's year from the current year

# Step 4: report
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"  # build the summary sentence for this record
print(summary)  # print the summary line



record4 = "Nguyen, Daniel | m | 17 | 2018-04-03 | 2846 QUAIL RIDGE ROAD | beat 537 | Open"  # raw pipe-delimited case record


#Step 1
fields = record4.strip().split(" | ")  # remove leading/trailing whitespace, then split into a list on " | "

#Step 2
name = fields[0].title()  # field 0: name, converted to Title Case
sex = fields[1].upper()  # field 1: sex, converted to uppercase
age = int(fields[2])  # field 2: age, converted from string to int
date = fields[3]  # field 3: date the case was opened, kept as a string
year = int(date[0:4])  # first 4 characters of the date string, converted to int
addr = fields[4].title()  # field 4: address, converted to Title Case
status = fields[6].upper()  # field 6: case status, converted to uppercase

# Step 3
years_unsolved = 2026 - year  # subtract the case's year from the current year

# Step 4
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"  # build the summary sentence for this record
print(summary)  # print the summary line



record5 = " BOOKER, TERRENCE | M | 41 | 2018-11-08 | 907 n. calloway drive | Beat 442 | OPEN "

#step 1
fields = record5.strip().split(" | ")
#step 2
name = fields[0].title()
sex = fields[1].upper()
age = int(fields[2])
date = fields[3]
year = int(date[0:4])
addr = fields[4].title()
status = fields[6]

# Step 3: compute
years_unsolved = 2026 - year

# Step 4: report
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)
