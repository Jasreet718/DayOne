"""Fetch every murder incident from Dallas OpenData into data/case.db.

Run: python -m src.fetch_city

Source: City of Dallas OpenData, Police Incidents (resource qv6i-rri7),
https://www.dallasopendata.com/resource/qv6i-rri7.json

The raw JSON is cached in data/raw_incidents.json. A rerun reads the cache
and does not call the API again. Delete the cache to force a fresh pull.
"""
import json
import os
import sqlite3
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
# Each detective puts their own token in .env (never committed).
# Without one the API still answers, but from a shared, throttled pool.
TOKEN = os.getenv("DALLAS_APP_TOKEN")

URL = "https://www.dallasopendata.com/resource/qv6i-rri7.json"
# City feed definition of "murder": offincident contains MURDER or equals HOMICIDE.
WHERE = "offincident like '%MURDER%' OR offincident = 'HOMICIDE'"
RAW = Path("data/raw_incidents.json")
DB = Path("data/case.db")
PAGE = 5000
FIRST_YEAR, LAST_YEAR = 2014, 2026   # feed starts June 1, 2014


def fetch_all() -> list[dict]:
    """Page through the API once, then cache the raw JSON."""
    if RAW.exists():
        print("using cache", RAW)
        return json.loads(RAW.read_text())
    if not TOKEN:
        print("warning: no DALLAS_APP_TOKEN in .env, using the shared throttled pool")
    rows, offset = [], 0
    while True:
        params = {
            "$where": WHERE,
            "$order": "incidentnum",   # stable order, or paging repeats rows
            "$limit": PAGE,
            "$offset": offset,
        }
        if TOKEN:
            params["$$app_token"] = TOKEN
        r = requests.get(URL, params=params, timeout=60)
        r.raise_for_status()
        page = r.json()
        rows.extend(page)
        print(f"offset {offset}: {len(page)} rows")
        if len(page) < PAGE:
            break
        offset += PAGE
    RAW.parent.mkdir(exist_ok=True)
    RAW.write_text(json.dumps(rows))
    return rows


def flatten(rows: list[dict]) -> pd.DataFrame:
    """Turn the list of dicts into a flat table SQLite can store."""
    df = pd.DataFrame(rows)
    if "geocoded_column" in df.columns:
        geo = df.pop("geocoded_column")
        df["lat"] = geo.apply(lambda g: float(g["latitude"]) if isinstance(g, dict) and "latitude" in g else None)
        df["lon"] = geo.apply(lambda g: float(g["longitude"]) if isinstance(g, dict) and "longitude" in g else None)
    df = df[[c for c in df.columns if not c.startswith(":@")]]   # drop computed regions
    # Any other nested values (dicts/lists) become JSON text so to_sql does not choke.
    for c in df.columns:
        if df[c].apply(lambda v: isinstance(v, (dict, list))).any():
            df[c] = df[c].apply(lambda v: json.dumps(v) if isinstance(v, (dict, list)) else v)
    df["servyr"] = pd.to_numeric(df["servyr"], errors="coerce")   # string in the API
    return df


def split_quarantine(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Rows with impossible service years (1011, 1429, 1967-1991...) go to quarantine, not the bin."""
    ok = df["servyr"].between(FIRST_YEAR, LAST_YEAR)
    return df[ok], df[~ok]


def main() -> None:
    df = flatten(fetch_all())
    clean, bad = split_quarantine(df)
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    clean.to_sql("incidents", con, if_exists="replace", index=False)
    bad.to_sql("quarantine", con, if_exists="replace", index=False)
    n = pd.read_sql("SELECT COUNT(*) AS n FROM incidents", con).n[0]
    q = pd.read_sql("SELECT COUNT(*) AS n FROM quarantine", con).n[0]
    con.close()
    print(f"case.db: {n} rows in incidents, {q} rows in quarantine (bad servyr)")


if __name__ == "__main__":
    main()
