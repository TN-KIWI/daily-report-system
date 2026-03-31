from datetime import datetime, time
from pathlib import Path
import subprocess

from report.time_utils import today_timezone


def get_today_commit_messages(repo_path: str) -> list[str]:
    repo = Path(repo_path).expanduser().resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"not a git repository: {repo}")

    today = today_timezone()
    since = datetime.combine(today, time.min).strftime("%Y-%m-%d %H:%M:%S")
    until = datetime.combine(today, time.max).strftime("%Y-%m-%d %H:%M:%S")

    result = subprocess.run(
        [
            "git",
            "-c",
            "i18n.logOutputEncoding=utf-8",
            "log",
            f"--since={since}",
            f"--until={until}",
            "--pretty=format:%s",
        ],
        cwd=repo,
        capture_output=True,
        text=False,
        check=False,
    )

    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        if not stderr:
            stderr = "unknown git error"
        raise RuntimeError(f"failed to read git log for {repo}: {stderr}")

    output = result.stdout.decode("utf-8", errors="replace").strip()
    if not output:
        return []

    return [line for line in output.splitlines() if line.strip()]
