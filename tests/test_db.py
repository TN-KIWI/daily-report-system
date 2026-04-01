import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from report import storage


def setup_temp_db(tmp_path):
    db_path = tmp_path / "test.db"
    storage.DB_PATH = db_path  # 上書き
    return db_path


def test_add_and_load_entries(tmp_path):
    setup_temp_db(tmp_path)

    class Dummy:
        def __init__(self, project, section, text):
            self.project = project
            self.section = section
            self.text = text

    # add
    storage.add_entry(Dummy("api", "done", "test1"))
    storage.add_entry(Dummy("api", "issue", "test2"))

    # load
    data = storage.load_entries()
    entries = data["entries"]

    assert len(entries) == 2
    assert entries[0]["text"] == "test1"
    assert entries[1]["text"] == "test2"

def test_created_at_exists(tmp_path):
    setup_temp_db(tmp_path)

    class Dummy:
        def __init__(self):
            self.project = "api"
            self.section = "done"
            self.text = "test"

    storage.add_entry(Dummy())

    data = storage.load_entries()
    entry = data["entries"][0]

    assert "created_at" in entry
    assert entry["created_at"] is not None


def test_load_entries_with_datetime_range(tmp_path):
    setup_temp_db(tmp_path)
    storage.init_storage()

    with storage._connect() as conn:
        conn.executemany(
            """
            INSERT INTO entries (project, section, text, created_at)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("api", "done", "before", "2026-04-01T04:59:00+09:00"),
                ("api", "done", "inside", "2026-04-01T05:00:00+09:00"),
                ("api", "done", "after", "2026-04-02T05:00:00+09:00"),
            ],
        )
        conn.commit()

    data = storage.load_entries(
        from_dt="2026-04-01T05:00:00+09:00",
        to_dt="2026-04-02T04:59:00+09:00",
    )

    entries = data["entries"]

    assert len(entries) == 1
    assert entries[0]["text"] == "inside"
