from datetime import date, datetime, time
from pathlib import Path
import subprocess
from report.time_utils import today_timezone

def get_today_commit_messages(repo_path):
    repo = Path(repo_path)
    if not (repo / ".git").exists():
        raise ValueError(f"not a git repository: {repo}")  
    today = today_timezone()
    since = datetime.combine(today, time.min).strftime("%Y-%m-%d %H:%M:%S")
    until = datetime.combine(today, time.max).strftime("%Y-%m-%d %H:%M:%S")

    result = subprocess.run(
        [
            "git",
            "log",
            f"--since={since}",
            f"--until={until}",
            "--pretty=format:%s",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout.strip()
    if not output:
        return []
    return output.splitlines()
