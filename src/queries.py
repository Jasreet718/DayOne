"""Three questions for data/case.db, plus the FBI-versus-city comparison.

Run: python -m src.fetch_city   (once, builds case.db)
     python -m src.queries

"Murder" here is the city feed definition: offincident contains MURDER or
equals HOMICIDE. The FBI column is the week 9 MAP/UCR count of reported murders.
"""
import sqlite3
from pathlib import Path

import pandas as pd

DB = Path("data/case.db")
SERIES = Path("reports/dallas_series.csv")

# Q1: murders per service year. The feed has one row per offense record
# (servnumid), and a few incidents carry more than one, so count both.
Q1 = """SELECT servyr AS year,
               COUNT(*) AS murder_rows,
               COUNT(DISTINCT incidentnum) AS incidents
        FROM incidents
        WHERE servyr BETWEEN 2014 AND 2026
        GROUP BY servyr ORDER BY servyr"""

# Q2: the five beats with the most murder incidents since the feed began.
Q2 = """SELECT beat, division, COUNT(DISTINCT incidentnum) AS incidents
        FROM incidents
        WHERE beat IS NOT NULL
        GROUP BY beat ORDER BY incidents DESC LIMIT 5"""

# Q3 (our squad's slice): share of murder incidents that happened at a residence
# (single family house or apartment). Why: it separates domestic and
# acquaintance killings from street violence, which clear at very different
# rates, so it is a case-mix candidate for the week 12 hypothesis.
Q3 = """SELECT COUNT(DISTINCT incidentnum) AS incidents,
               COUNT(DISTINCT CASE WHEN premise LIKE '%Residence%'
                                   THEN incidentnum END) AS at_residence,
               ROUND(100.0 * COUNT(DISTINCT CASE WHEN premise LIKE '%Residence%'
                                                 THEN incidentnum END)
                     / COUNT(DISTINCT incidentnum), 1) AS pct_residence
        FROM incidents"""


def fbi_vs_city(con: sqlite3.Connection) -> pd.DataFrame:
    """Join the week 9 FBI reported count to the city feed count by year."""
    city = pd.read_sql(Q1, con)
    fbi = pd.read_csv(SERIES)[["year", "reported"]].rename(columns={"reported": "fbi_reported"})
    both = fbi.merge(city, on="year", how="inner")
    both["city_share_pct"] = (100 * both["incidents"] / both["fbi_reported"]).round(1)
    return both


def main() -> None:
    con = sqlite3.connect(DB)
    print("SELECT COUNT(*) FROM incidents ->",
          pd.read_sql("SELECT COUNT(*) AS n FROM incidents", con).n[0], "\n")
    print("Q1. Murders per year (city feed)")
    print(pd.read_sql(Q1, con).to_string(index=False), "\n")
    print("Q2. Top 5 beats, murder incidents since June 2014")
    print(pd.read_sql(Q2, con).to_string(index=False), "\n")
    print("Q3. Squad slice: murders at a residence")
    print(pd.read_sql(Q3, con).to_string(index=False), "\n")
    if SERIES.exists():
        print("Audit. FBI reported (wk9) vs city feed incidents, overlapping years")
        print(fbi_vs_city(con).to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()
