from datetime import datetime, timedelta, timezone

TIMEZONE = timezone(timedelta(hours=9))

def now():
    return datetime.now(TIMEZONE)

def today_timezone():
    return now().date().isoformat()