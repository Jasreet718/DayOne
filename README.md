GitHub Username: Jasreet718
Repo Link: https://github.com/Jasreet718/DayOne.git
Team Name: DayOne
Team mates: Tanveer Mangat, Albin AbrahamMathew and Jotish Chowdary Boddu

git config --global user.name "Jasreet718"
git config --global user.email "jkm220000@utdallas.edu"
## Setup from zero

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.get_data             # downloads the raw data into data/ (gitignored)
python -m src.series               # writes reports/dallas_series.csv
pytest
```

## Data sources

- Murder Accountability Project, UCR homicide and clearance data (UCR65_25), murderdata.org, accessed 2026-11-11.
- The Washington Post, Unsolved Homicide Database, github.com/washingtonpost/data-homicides, 2018. CC BY-NC-SA 4.0. Victim names are dropped on load; aggregate analysis only.
