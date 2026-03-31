from pathlib import Path


GIT_REPO_PATHS = [
    Path("."),
]


def load_repo_paths() -> list[Path]:
    return [Path(repo_path).expanduser().resolve() for repo_path in GIT_REPO_PATHS]
