header = f"{'CASE':<25}{'AGE':>6}{'YEARS UNSOLVED':>18}"
print(header)
record2= "reyes, miguel|M|32|2018-05-17| 3308 DELAFORD STREET |Beat 347|open"
#Step 1:
fields = record2.strip().split("|")
# Step 2: clean each field
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
