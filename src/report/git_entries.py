from pathlib import Path

from report import git_reader
from report.git_sources import load_repo_paths


def messages_to_entries(repo_path: str | Path, messages: list[str]) -> list[dict]:
    project = Path(repo_path).name
    return [
        {"project": project, "section": "done", "text": message}
        for message in messages
        if message.strip()
    ]


def load_today_git_entries() -> list[dict]:
    return load_git_entries()


def load_git_entries(from_dt: str | None = None, to_dt: str | None = None) -> list[dict]:
    entries = []
    for repo_path in load_repo_paths():
        messages = git_reader.get_commit_messages(repo_path, from_dt=from_dt, to_dt=to_dt)
        entries.extend(messages_to_entries(repo_path, messages))
    return entries
