#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import date, datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent / "src"))

from exerset import storage
from exerset.exercises import EXERCISES

# Load and dump raw history
raw = storage.load_history()
print("Raw history loaded:")
print(f"  - {len(raw.get('log', []))} entries")
print(f"  - Oldest: {raw['log'][0]['ts'] if raw['log'] else 'N/A'}")
print(f"  - Newest: {raw['log'][-1]['ts'] if raw['log'] else 'N/A'}")
print()

# Test weekly_summary for 7 days
today = date.today()
print(f"Today: {today}")
summary_7 = storage.weekly_summary(7)
print(f"\n7-day summary:")
for ex in EXERCISES:
    ex_id = ex["id"]
    done_list = summary_7.get(ex_id, [])
    print(f"  {ex_id}: {done_list}")
print()

# Test get_done_dates for each exercise
print("Done dates per exercise:")
for ex in EXERCISES:
    ex_id = ex["id"]
    dates = storage.get_done_dates(ex_id)
    print(f"  {ex_id}: {sorted(dates)}")
