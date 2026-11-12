# src/factor.py — Week 12: Operation The Factor
# Pre-registered hypothesis: higher DFW unemployment is associated with LOWER Dallas
# homicide clearance (negative direction). One primary OLS + one lag-1 variant. No more.
# Needs FRED_API_KEY in .env (free: https://fredaccount.stlouisfed.org/apikeys).
# Run from the repo root, after python -m src.series:  python -m src.factor

import os
import sys

import pandas as pd
import requests
import statsmodels.formula.api as smf
from dotenv import load_dotenv

SERIES_ID = "LAUMT481910000000003A"  # Dallas-Fort Worth-Arlington MSA unemployment, annual
FACTOR_CSV = "data/fred_unemployment.csv"
HYPOTHESIS = ("We hypothesize that DFW unemployment is associated with Dallas homicide "
              "clearance, in the negative direction.")


def fetch_factor() -> pd.DataFrame:
    """Download the factor from FRED and bank it as one row per year."""
    load_dotenv()
    key = os.environ.get("FRED_API_KEY")
    if not key:
        sys.exit("FRED_API_KEY missing. Add it to .env (free key, see top of this file).")
    r = requests.get("https://api.stlouisfed.org/fred/series/observations", params={
        "series_id": SERIES_ID, "api_key": key, "file_type": "json",
        "frequency": "a", "aggregation_method": "avg",
    }, timeout=60)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["observations"])
    df["year"] = df["date"].str[:4].astype(int)
    # FRED sends missing values as the string "." — coerce turns them into NaN.
    df["unemployment"] = pd.to_numeric(df["value"], errors="coerce")
    out = df[["year", "unemployment"]].dropna()
    out.to_csv(FACTOR_CSV, index=False)
    return out


def fmt_model(label: str, term: str, m) -> str:
    return (f"{label}: coef = {m.params[term]:.3f}, p = {m.pvalues[term]:.3f}, "
            f"R² = {m.rsquared:.3f} (n = {int(m.nobs)})")


def main() -> None:
    series = pd.read_csv("reports/dallas_series.csv")
    factor = fetch_factor()
    # Both year columns are int, so the merge matches (a str/int mix gives 0 rows).
    merged = series.merge(factor, on="year", how="inner")
    # Eyeball before modeling (slide 11, step 2).
    print(merged.shape)
    print(merged.head())

    # Clearance is a fraction (0-1); scale to percentage points so coef reads "points".
    merged["clearance"] = merged["clearance"] * 100

    m1 = smf.ols("clearance ~ unemployment", data=merged).fit()
    print(m1.summary())

    # Lag-1: last year's unemployment can't be caused by this year's clearance.
    merged["unemployment_lag1"] = merged["unemployment"].shift(1)
    lagged = merged.dropna(subset=["unemployment_lag1"])
    m2 = smf.ols("clearance ~ unemployment_lag1", data=lagged).fit()
    print(m2.summary())

    line1 = fmt_model("clearance ~ unemployment", "unemployment", m1)
    line2 = fmt_model("Lag-1 variant", "unemployment_lag1", m2)
    print(line1)
    print(line2)

    # Verdict wording is computed from the p-value, so the writeup can't overclaim.
    p = m1.pvalues["unemployment"]
    direction = "negatively" if m1.params["unemployment"] < 0 else "positively"
    verdict = (f"{direction} associated with" if p < 0.05 else "not detectably associated with")
    y0, y1 = int(merged["year"].min()), int(merged["year"].max())

    os.makedirs("reports", exist_ok=True)
    with open("reports/factor_writeup.md", "w", encoding="utf-8") as f:
        f.write(f"""# Factor writeup — Squad (Jotish)

## Hypothesis (as locked at standup)
{HYPOTHESIS}

## Data
Clearance: reports/dallas_series.csv (FBI UCR via MAP), Dallas PD, rebuilt by `python -m src.series`.
Factor: unemployment rate, DFW-Arlington MSA, annual average, FRED series `{SERIES_ID}`
(https://fred.stlouisfed.org/series/{SERIES_ID}), fetched by `src/factor.py` on {pd.Timestamp.today():%Y-%m-%d}.
Years {y0}–{y1}, {len(merged)} rows after merge (FRED coverage starts 1990).

## Result
{line1}
{line2}
Clearance is in percentage points; unemployment in percentage points.

## Two named confounders
1. **Crime waves / case mix.** Recessions and violent-crime surges can coincide, and a shift toward
   stranger or gang shootings lowers clearance with no change in police effort.
2. **Police staffing and budgets.** Recessions cut city budgets and hiring, which can reduce
   investigative capacity independently of unemployment itself. (Reverse causation is also possible:
   low clearance may feed back into budget decisions.)

## Verdict
Over {y0}–{y1}, DFW unemployment is {verdict} Dallas homicide clearance
(p = {p:.3f}, R² = {m1.rsquared:.3f}). With about {len(merged)} yearly observations, two
regressions and trending series, we do not claim causation: shared trends and the
confounders above could produce this pattern on their own.

Direction check: we predicted a NEGATIVE association. The primary estimate is
{'positive, the opposite of our prediction' if m1.params['unemployment'] > 0 else 'negative, as predicted'}
(coef = {m1.params['unemployment']:.3f}). The lag-1 variant (p = {m2.pvalues['unemployment_lag1']:.3f}) is the
secondary check and is not a replacement for the pre-registered result; we ran only these two
models, so its p-value is not a rescued finding.
""")
    print("Wrote reports/factor_writeup.md")


if __name__ == "__main__":
    main()
