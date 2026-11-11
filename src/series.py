# src/series.py — Week 9: Operation First Cut
# Builds Dallas PD's clearance-by-year series from MAP's FBI archive, then audits it.
# Run from the repo root, after python -m src.get_data:  python -m src.series

# "as pd" is the nickname every pandas example uses: pd.read_csv, not pandas.read_csv.
import pandas as pd

# One call loads all 186,519 rows into a DataFrame — a table with named columns.
df = pd.read_csv("data/map_ucr.csv")

# First moves, always (slide 4): shape -> head -> columns before ANY analysis.
# .shape is (rows, columns) -> (186519, 9)
print(df.shape)
# .head() shows the first 5 rows, to eyeball what the values look like.
print(df.head())
# .columns lists the field names. This is where you learn it's YEAR, not Year.
print(df.columns)
# .nunique() counts the DIFFERENT values in a column — how many agencies are in here.
print(df["ORI"].nunique())
# Week 6's quarantine instinct: how many blanks in each column? (all zero here)
print(df.isna().sum())

# df["ORI"] == "TXDPD00" gives True/False for every row; df[...] keeps the True ones.
# Filter on ORI, not the name — four US agencies are called "Dallas".
dallas = df[df["ORI"] == "TXDPD00"]
# Confirm the row count before trusting it: should be 61, one per year 1965–2025.
print("Dallas PD rows:", len(dallas))

# groupby("YEAR") makes one bucket per year — week 4's per_beat dict, in one line.
# .agg says what to compute per bucket: new_name=("column", "how").
per_year = dallas.groupby("YEAR").agg(
    # MRD = murders reported that year, added up within the bucket.
    reported=("MRD", "sum"),
    # CLR = murders cleared that year (arrest OR exceptional means — the FBI definition).
    cleared=("CLR", "sum"),
)
# A new column from two old ones: pandas divides every year at once, no loop.
per_year["clearance"] = per_year["cleared"] / per_year["reported"]
# The year labels down the side are called "YEAR"; the deliverable wants "year".
per_year.index.name = "year"
# Deliverable #1's skeleton: year, reported, cleared, clearance. Never hand-edited.
per_year.to_csv("reports/dallas_series.csv")

# The three mandatory sanity checks (slide 7). Auditing now, not cleaning.

# Check 1: rates must live between 0 and 1. An empty table means none went over.
print()
print("CHECK 1 — clearance over 100%:")
print(per_year[per_year["clearance"] > 1])

# Check 2: every year that SHOULD be there, minus the years that ARE (week 4 sets).
# 1965 because that's where the archive starts; range stops before 2026.
print()
print("CHECK 2 — missing years:")
years = per_year.index
print(set(range(1965, 2026)) - set(years))

# Check 3: .diff() is this year minus last year, .abs() drops the minus sign so a
# big fall counts as much as a big rise, then sort biggest first and keep the top 5.
print()
print("CHECK 3 — biggest year-over-year jumps:")
print(per_year["clearance"].diff().abs().sort_values(ascending=False).head())

# The 5 most suspicious years. The reasons are my judgment from the checks above,
# so they're written by hand — a dict, year -> reason, like week 4's lockers.
suspicious = {
    2018: "39.9%, lowest in the whole series — a 40-point fall from 2017, the biggest jump",
    2017: "79.6%, up 30 points from 49.7% in 2016, then collapses — old cases cleared that year?",
    2007: "58.0%, down 23 points from 80.7% in 2006 — starts the 2007-2011 slide",
    1974: "68.9%, a one-year dip between two ~90% years, then straight back up — reporting blip?",
    2025: "51.8%, partial year still being reported — not comparable to full years yet",
}

print()
print("5 MOST SUSPICIOUS YEARS:")
# Looping a dict hands back its keys (the years); suspicious[year] looks up the reason.
for year in suspicious:
    print(f"{year}: {suspicious[year]}")
