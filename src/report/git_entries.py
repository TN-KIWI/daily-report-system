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
    entries = []
    for repo_path in load_repo_paths():
        messages = git_reader.get_today_commit_messages(repo_path)
        entries.extend(messages_to_entries(repo_path, messages))
    return entries
