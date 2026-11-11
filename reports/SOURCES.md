# Sources

- `dallas_series.csv` — Murder Accountability Project, UCR homicide and clearance data (UCR65_25), murderdata.org, accessed 2026-11-11. "Cleared" is the FBI definition: arrest or exceptional means.
- `data/wapo_dallas.csv` — The Washington Post, Unsolved Homicide Database, github.com/washingtonpost/data-homicides, 2018. CC BY-NC-SA 4.0.

Rebuild everything with `python -m src.get_data` then `python -m src.series`.
- `data/case.db` (week 11) — City of Dallas OpenData, Police Incidents, resource `qv6i-rri7`, dallasopendata.com, fetched 2026-11-11. "Murder" = `offincident` contains MURDER or equals HOMICIDE. Rebuild with `python -m src.fetch_city` (needs `DALLAS_APP_TOKEN` in `.env`), then `python -m src.queries`.
