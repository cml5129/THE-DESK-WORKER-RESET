import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path

APP_DIR = Path(os.environ.get("APPDATA", Path.home())) / "Exerset"
HISTORY_FILE = APP_DIR / "history.json"


def _ensure_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> dict:
    _ensure_dir()
    if not HISTORY_FILE.exists():
        return {"settings": {"timer_minutes": 60}, "log": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data.setdefault("settings", {"timer_minutes": 60})
        data.setdefault("log", [])
        return data
    except (json.JSONDecodeError, OSError):
        return {"settings": {"timer_minutes": 60}, "log": []}


def save_history(data: dict) -> None:
    _ensure_dir()
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def log_exercise(exercise_id: str) -> None:
    data = load_history()
    data["log"].append({
        "ts": datetime.now().isoformat(),
        "exercise_id": exercise_id,
    })
    save_history(data)


def get_done_dates(exercise_id: str) -> set:
    """Return the set of date objects on which this exercise was logged."""
    data = load_history()
    done: set[date] = set()
    for entry in data.get("log", []):
        if entry.get("exercise_id") == exercise_id:
            try:
                done.add(datetime.fromisoformat(entry["ts"]).date())
            except (KeyError, ValueError):
                pass
    return done


def weekly_summary(days: int = 7) -> dict:
    """
    Return {exercise_id: [done_on_date0, ..., done_on_dateN-1]} for the
    last `days` days, ordered oldest (index 0) to today (index -1).
    """
    from .exercises import EXERCISES  # local import avoids circular dependency

    today = date.today()
    # oldest first, today last
    date_list = [today - timedelta(days=i) for i in range(days - 1, -1, -1)]

    data = load_history()
    done_map: dict[str, set] = {}
    for entry in data.get("log", []):
        try:
            d = datetime.fromisoformat(entry["ts"]).date()
            ex_id = entry["exercise_id"]
            done_map.setdefault(ex_id, set()).add(d)
        except (KeyError, ValueError):
            pass

    result = {}
    for ex in EXERCISES:
        ex_id = ex["id"]
        result[ex_id] = [d in done_map.get(ex_id, set()) for d in date_list]
    return result
