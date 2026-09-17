#Header
print(f"{'CASE':<26}{'AGE':<8}{'YEARS UNSOLVED'}")
print()


record1 = "CARTER, DEMARCUS | m | 36 | 2018-03-22 | 412 larkmoor lane | beat 352 | OPEN"

#Step 1
fields = record1.strip().split(" | ")

#Step 2
name = fields[0].title()
sex = fields[1].upper()
age = int(fields[2])
date = fields[3]
year = int(date[0:4])
addr = fields[4].title()
status = fields[6].upper()

# Step 3
years_unsolved = 2026 - year

# Step 4
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)



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



record3 = "OKAFOR, SAMUEL J | M | 55 | 2018-07-09 | 1519 westhollow avenue | beat 341 | OPEN"

#Step 1
fields = record3.strip().split(" | ")

#Step 2
name = fields[0].title()
sex = fields[1].upper()
age = int(fields[2])
date = fields[3]
year = int(date[0:4])
addr = fields[4].title()
status = fields[6].upper()

# Step 3
years_unsolved = 2026 - year

# Step 4: report
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)



record4 = "Nguyen, Daniel | m | 17 | 2018-04-03 | 2846 QUAIL RIDGE ROAD | beat 537 | Open"


#Step 1
fields = record4.strip().split(" | ")

#Step 2
name = fields[0].title()
sex = fields[1].upper()
age = int(fields[2])
date = fields[3]
year = int(date[0:4])
addr = fields[4].title()
status = fields[6].upper()

# Step 3
years_unsolved = 2026 - year

# Step 4
summary = f"CASE: {name} ({sex}, {age})" \
f" {years_unsolved} years without an arrest"
print(summary)



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
