# Factor writeup — Squad (Jotish)

## Hypothesis (as locked at standup)
We hypothesize that DFW unemployment is associated with Dallas homicide clearance, in the negative direction.

## Data
Clearance: reports/dallas_series.csv (FBI UCR via MAP), Dallas PD, rebuilt by `python -m src.series`.
Factor: unemployment rate, DFW-Arlington MSA, annual average, FRED series `LAUMT481910000000003A`
(https://fred.stlouisfed.org/series/LAUMT481910000000003A), fetched by `src/factor.py` on 2026-11-11.
Years 1990–2025, 36 rows after merge (FRED coverage starts 1990).

## Result
clearance ~ unemployment: coef = 1.973, p = 0.100, R² = 0.078 (n = 36)
Lag-1 variant: coef = 2.390, p = 0.048, R² = 0.113 (n = 35)
Clearance is in percentage points; unemployment in percentage points.

## Two named confounders
1. **Crime waves / case mix.** Recessions and violent-crime surges can coincide, and a shift toward
   stranger or gang shootings lowers clearance with no change in police effort.
2. **Police staffing and budgets.** Recessions cut city budgets and hiring, which can reduce
   investigative capacity independently of unemployment itself. (Reverse causation is also possible:
   low clearance may feed back into budget decisions.)

## Verdict
Over 1990–2025, DFW unemployment is not detectably associated with Dallas homicide clearance
(p = 0.100, R² = 0.078). With about 36 yearly observations, two
regressions and trending series, we do not claim causation: shared trends and the
confounders above could produce this pattern on their own.

Direction check: we predicted a NEGATIVE association. The primary estimate is
positive, the opposite of our prediction
(coef = 1.973). The lag-1 variant (p = 0.048) is the
secondary check and is not a replacement for the pre-registered result; we ran only these two
models, so its p-value is not a rescued finding.
