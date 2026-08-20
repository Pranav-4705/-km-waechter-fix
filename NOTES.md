# What I checked, and what the agent got wrong

## What the agent got wrong

The agent rewrote config_loader.py and deleted the `get_setting()` function because it said it was "just a duplicate of dict.get()." It did not check whether any other file imported that function first. The very next test run crashed with `ImportError: cannot import name 'get_setting' from 'config_loader'` because fleet_report.py still called it in two places. I had to tell it to fix the import, and it then replaced the two `get_setting()` calls with `dict.get()`. The lesson: when removing a function, grep for callers first — the agent skipped that step entirely.

## What I checked before I accepted its work

I ran `pytest -v` and confirmed all 4 tests pass (the original 3 plus the new missing-reading test). I ran `python verify.py` and confirmed 10 of 11 checks pass — the only FAIL is NOTES.md, which requires my own words. I read every diff the agent produced before accepting it. Specifically I verified:

- `wear_percent` uses `/` not `//`, and `verify.py` confirms a car at 14,900 km reports 99.3%.
- `needs_service` returns `False` when `last_service_km` is absent, and `verify.py` confirms a missing-reading car is handled.
- `SERVICE_INTERVAL_KM` is still 15000 and `WARN_AT_PERCENT` is still 80 — both untouched.
- `settings.cfg` is untouched.
- The average wear in `fleet_summary` uses `/` and `verify.py` confirms 59.67, not a truncated whole number.
- `MILES_PER_KM` is now 0.621371 and `verify.py` confirms 100 km reads as 62.1 miles.

## What the data actually said

The data says `km_since_service` is the dominant predictor of breakdown (Cohen's d = 1.06, a large effect). Cars that broke down averaged 11,678 km since their last service vs 7,261 for safe cars. `avg_daily_km` (d = 0.63) and `load_factor` (d = 0.53) are moderate secondary predictors — breakdown cars are driven harder and loaded heavier. The two obvious-looking factors, total odometer mileage and age, showed essentially zero separation between the groups (d near 0). A 90,000 km car that was recently serviced is no riskier than a 10,000 km car that skipped its service. What kills these cars is not how old they are — it is how long they go without maintenance while being pushed hard.
