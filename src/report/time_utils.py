from datetime import datetime, timedelta, timezone

TIMEZONE = timezone(timedelta(hours=9))
CLI_DATETIME_FORMAT = "%Y-%m-%d %H:%M"

def now():
    return datetime.now(TIMEZONE)

def today_timezone():
    return now().date()


def parse_cli_datetime(value: str) -> datetime:
    parsed = datetime.strptime(value, CLI_DATETIME_FORMAT)
    return parsed.replace(tzinfo=TIMEZONE)


def parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def get_today_range() -> tuple[datetime, datetime]:
    today = today_timezone()
    start = datetime.combine(today, datetime.min.time(), tzinfo=TIMEZONE)
    end = datetime.combine(today, datetime.max.time(), tzinfo=TIMEZONE)
    return start, end
