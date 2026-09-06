from cli import view_tasks
from tasks import add_task, complete_task, delete_task

def empty_data():
    return {"next_id": 1, "tasks": []}

def test_add_task_appends_task_and_increments_next_id(capsys):
    data = empty_data()

    add_task(data, "  Buy groceries  ", "  Milk and bread  ", "2025-06-15")

    task = data["tasks"][0]
    assert data["next_id"] == 2
    assert task["id"] == 1
    assert task["title"] == "Buy groceries"
    assert task["description"] == "Milk and bread"
    assert task["due_date"] == "2025-06-15"
    assert task["status"] == "pending"
    assert task["completed_at"] is None
    assert "Task added." in capsys.readouterr().out

def test_add_task_rejects_empty_title():
    data = empty_data()

    add_task(data, "   ", "", "")

    assert data == empty_data()


def test_view_tasks_prints_summary(capsys):
    tasks = [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "",
            "status": "pending",
            "due_date": "",
            "created_at": "2025-06-01",
            "updated_at": "2025-06-01",
            "completed_at": None,
        }
    ]

    view_tasks(tasks, "n")

    assert capsys.readouterr().out.strip() == "1. Buy groceries (pending)"


def test_view_tasks_prints_empty_message(capsys):
    view_tasks([], "n")

    assert capsys.readouterr().out.strip() == "No tasks found."


def test_complete_task_marks_task_completed(capsys):
    data = empty_data()
    add_task(data, "Buy groceries", "", "")

    complete_task(data["tasks"], 1)

    task = data["tasks"][0]
    assert task["status"] == "completed"
    assert task["completed_at"] == task["updated_at"]
    assert "Task completed." in capsys.readouterr().out


def test_complete_task_does_not_change_already_completed_task(capsys):
    data = empty_data()
    add_task(data, "Buy groceries", "", "")
    complete_task(data["tasks"], 1)
    task_before_second_attempt = data["tasks"][0].copy()
    capsys.readouterr()

    complete_task(data["tasks"], 1)

    assert data["tasks"][0] == task_before_second_attempt
    assert capsys.readouterr().out.strip() == "Task is already completed."


def test_delete_task_removes_task(capsys):
    data = empty_data()
    add_task(data, "Buy groceries", "", "")

    delete_task(data["tasks"], 1)

    assert data["tasks"] == []
    assert "Task deleted." in capsys.readouterr().out
