from pathlib import Path
import subprocess

from report.time_utils import get_today_range


def get_commit_messages(repo_path: str, from_dt: str | None = None, to_dt: str | None = None) -> list[str]:
    repo = Path(repo_path).expanduser().resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"not a git repository: {repo}")
    if bool(from_dt) != bool(to_dt):
        raise ValueError("from_dt and to_dt must be provided together")

    if from_dt and to_dt:
        since = from_dt
        until = to_dt
    else:
        today_from, today_to = get_today_range()
        since = today_from.isoformat()
        until = today_to.isoformat()

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


def get_today_commit_messages(repo_path: str) -> list[str]:
    return get_commit_messages(repo_path)
