import json
from pathlib import Path


CONFIG_PATH = Path("config/repos.json")


def load_repo_paths() -> list[Path]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"repo config not found: {CONFIG_PATH}")

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    repos = data.get("repos", [])

    if not isinstance(repos, list):
        raise ValueError("repos must be a list")

    return [Path(repo_path).expanduser().resolve() for repo_path in repos]