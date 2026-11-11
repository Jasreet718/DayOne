"""Build the clearance trend chart from reports/dallas_series.csv."""

import pandas as pd                   # pandas reads the CSV into a table
import matplotlib.pyplot as plt       # matplotlib draws the chart

s = pd.read_csv("reports/dallas_series.csv")   # my own series from week 9
s["pct"] = s.clearance * 100          # clearance is 0.47, I want 47 for the axis

fig, ax = plt.subplots(figsize=(10, 5))        # one chart, 10 by 5 inches
ax.plot(s.year, s.pct, marker="o", linewidth=1.5)   # year on the bottom, percent up the side

ax.set_ylim(0, 100)                   # 0 to 100 always, so a dip cannot be made to look bigger
ax.set_xlabel("Year")
ax.set_ylabel("Homicide clearance (%)\nSource: FBI UCR via Murder Accountability Project")
ax.set_title("Dallas Police Department homicide clearance rate, 1965-2025 (2025 partial)")
ax.grid(alpha=0.3)                    # faint grid lines so values are readable

# My #1 suspicious year. 2016 was 49.7%, 2017 jumps to 79.6%, then 2018 drops to 39.9%.
# A 40 point fall in one year looks like a counting change, not real police work.
yr = 2017
val = float(s.loc[s.year == yr, "pct"].iloc[0])
ax.annotate(f"{yr}: {val:.0f}% - reporting change?",
            xy=(yr, val), xytext=(yr - 32, val + 10),   # point at it, put the text to the left
            arrowprops=dict(arrowstyle="->"))

fig.tight_layout()                    # stop the labels getting cut off
fig.savefig("reports/clearance_trend.png", dpi=150)   # save it as an artifact, like code
print("wrote reports/clearance_trend.png")
