import json
import pytest
from persistence import load_tasks, save_tasks

def test_load_tasks_returns_empty_data_when_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert load_tasks() == {"next_id": 1, "tasks": []}


def test_save_tasks_and_load_tasks_round_trip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {
        "next_id": 2,
        "tasks": [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk and bread",
                "status": "pending",
                "due_date": "2025-06-15",
                "created_at": "2025-06-01",
                "updated_at": "2025-06-01",
                "completed_at": None,
            }
        ],
    }

    save_tasks(data)

    assert json.loads((tmp_path / "tasks.json").read_text(encoding="utf-8")) == data
    assert load_tasks() == data


def test_load_tasks_rejects_invalid_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "tasks.json").write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="tasks.json contains invalid JSON"):
        load_tasks()
