"""Download the week 9 sources into data/. Run: python -m src.get_data"""
# src/get_data.py — Week 9: rebuilds data/ from nothing, straight from the publishers.
# The raw CSVs are gitignored, so this script IS how a teammate gets the data.

# Path is a file path as an object instead of a plain string. The / operator
# glues pieces together: DATA / "map_ucr.csv" -> data/map_ucr.csv
from pathlib import Path
# "as pd" is a nickname, so I can type pd.read_csv instead of pandas.read_csv.
import pandas as pd
# requests is the library that downloads a web page or file from a URL.
import requests

# The folder everything lands in. exist_ok=True means "if it's already there,
# fine" — without it, mkdir crashes the second time this runs.
DATA = Path("data")
DATA.mkdir(exist_ok=True)

# MAP's FBI archive, hosted on Dropbox. dl=1 at the end means "send the file
# itself", not Dropbox's preview page. The parentheses let one string span two lines.
MAP_URL = ("https://www.dropbox.com/scl/fi/4y2a6yy0pv4lxffm7sa4v/UCR65_25.csv"
           "?rlkey=jhs7ktqhb9h3dnml1wety4nhb&st=7rxppnar&dl=1")
# The Washington Post's file on GitHub. "raw" gives the bare CSV, not the web page.
WAPO_URL = ("https://raw.githubusercontent.com/washingtonpost/"
            "data-homicides/master/homicide-data.csv")


# url: str and dest: Path are labels saying what type each parameter should be.
# -> None says this function hands nothing back; it just saves a file.
def fetch(url: str, dest: Path) -> None:
    """Download url into dest, unless dest is already on disk."""
    # Already downloaded? Skip it — no point pulling 12.8 MB every run.
    if dest.exists():
        print(f"cached: {dest}")
        # A bare return leaves the function right here.
        return
    # Download it. timeout=120 gives up after 2 minutes instead of hanging forever.
    r = requests.get(url, timeout=120)
    # A 404 or 500 doesn't crash on its own — this turns it into a real error,
    # so a failed download never gets saved as if it were the data.
    r.raise_for_status()
    # .content is the raw bytes of the file; write them to disk exactly as they came.
    dest.write_bytes(r.content)
    # :, puts commas in the number -> 12,800,000 bytes.
    print(f"saved: {dest} ({dest.stat().st_size:,} bytes)")


def main() -> None:
    """Fetch both sources, then cut the Post's file down to Dallas."""
    # The FBI archive is used as-is.
    fetch(MAP_URL, DATA / "map_ucr.csv")
    # The Post's file has all 50 cities, so it gets saved first and filtered below.
    fetch(WAPO_URL, DATA / "wapo_all.csv")

    # The Post's file is Latin-1, not UTF-8; without this pandas raises UnicodeDecodeError.
    wapo = pd.read_csv(DATA / "wapo_all.csv", encoding="latin-1")
    # Keep Dallas rows only (filter on city — state == "TX" also pulls in other
    # Texas cities), and drop the victim name columns. Aggregate analysis only.
    dallas = wapo[wapo["city"] == "Dallas"].drop(
        columns=["victim_last", "victim_first"])
    # index=False stops pandas adding its own row-number column to the file.
    dallas.to_csv(DATA / "wapo_dallas.csv", index=False)
    # The handout's check: exactly 1,567 rows, or the filter is wrong.
    print(f"wapo_dallas.csv: {len(dallas)} rows (expect 1567)")


# Same guard as week 8: only download when run directly, never on import.
if __name__ == "__main__":
    main()
