record5 = " BOOKER, TERRENCE | M | 41 | 2018-11-08 | 907 n. calloway drive | Beat 442 | OPEN "
# Header
print(f"{'CASE':<26}{'AGE':<8}{'YEARS UNSOLVED'}")
print()


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




