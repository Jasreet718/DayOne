record1 = "CARTER, DEMARCUS | m | 36 | 2018-03-22 | 412 larkmoor lane | beat 352 | OPEN"
#step1: 
fields = record1.strip().split(" | ")
#step2:
name = fields[0].title() 
sex = fields[1].upper() 
age = int(fields[2]) 
date = fields[3]
year = int(date[0:4]) 
addr = fields[4].title() 

# Step 3:
years_unsolved = 2026 - year

# Step 4: 
print("CASE                         AGE    YEARS UNSOLVED")
print()
print(f"{name} ({sex})              {age}        {years_unsolved}")