import json
from pathlib import Path
from report.time_utils import today_timezone

LOG_DIR = Path("data/logs")


def _get_today_log_path():
    today = today_timezone()
    return LOG_DIR / f"{today}.json", today


def load_entries():
    log_path, today = _get_today_log_path()
    if not log_path.exists():
        return {"date": today, "entries": []}

    try:
        with log_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"date": today, "entries": []}

    if not isinstance(data, dict):
        return {"date": today, "entries": []}
    if "entries" not in data or not isinstance(data["entries"], list):
        data["entries"] = []
    if "date" not in data:
        data["date"] = today
    return data


def add_entry(entry):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path, today = _get_today_log_path()

    data = load_entries()
    data["date"] = today
    data["entries"].append(entry.to_dict())

    with log_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
