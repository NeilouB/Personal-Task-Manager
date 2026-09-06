import pytest
from validation import parse_due_date, validate_data, validate_date, validate_tasks

def make_task(**overrides):
    task = {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk and bread",
        "status": "pending",
        "due_date": "",
        "created_at": "2025-06-01",
        "updated_at": "2025-06-01",
        "completed_at": None,
    }
    task.update(overrides)
    return task

# Test cases for the validate_date function
def test_validate_date_valid():
    assert validate_date("2025-06-15", "Due date") is None

def test_validate_date_valid_not_required():
    assert validate_date("", "Due date", allow_empty=True) is None

def test_validate_date_required() :
    with pytest.raises(ValueError) :
        validate_date("", "Due date", allow_empty=False)

def test_validate_date_invalid_format() :
    with pytest.raises(ValueError) :
        validate_date("15-06-2025", "Due date")

def test_validate_date_invalid_type() :
    with pytest.raises(ValueError) :
        validate_date(42, "Due date")

# Test cases for the parse_due_date function
def test_parse_due_date_valid():
    assert parse_due_date("2021-06-05") == "2021-06-05"

def test_parse_due_date_empty():
    assert parse_due_date("") == ""

def test_parse_due_date_invalid(capsys):
    assert parse_due_date("invalid-date") is None
    assert "Due date must be a date in YYYY-MM-DD format." in capsys.readouterr().out

# Test cases for the validate_tasks function
def test_validate_tasks_accepts_valid_pending_task():
    assert validate_tasks([make_task()]) is None

def test_validate_tasks_accepts_valid_completed_task():
    task = make_task(status="completed", completed_at="2025-06-02")
    assert validate_tasks([task]) is None

@pytest.mark.parametrize(
    "tasks, message",
    [
        ("not a list", "Task data must be a JSON list."),
        ([1], "Each task must be a JSON object."),
        ([{"id": 1}], "Each task must contain the expected fields."),
        ([make_task(id=0)], "Task IDs must be positive integers."),
        ([make_task(id=True)], "Task IDs must be positive integers."),
        ([make_task(), make_task()], "Task IDs must be unique."),
        ([make_task(title=" ")], "Task titles must not be empty."),
        ([make_task(title="x" * 201)], "Task titles cannot exceed 200 characters."),
        ([make_task(description="x" * 2001)], "Descriptions cannot exceed 2000 characters."),
        ([make_task(status="in progress")], "Task status is invalid."),
        ([make_task(created_at="01-06-2025")], "Created date must be a date in YYYY-MM-DD format."),
        ([make_task(status="completed")], "Completed tasks must have a completed date."),
        ([make_task(completed_at="2025-06-02")], "Only completed tasks may have a completed date."),
    ],
)

def test_validate_tasks_rejects_invalid_tasks(tasks, message):
    with pytest.raises(ValueError, match=message):
        validate_tasks(tasks)

# Test cases for the validate_data function
def test_validate_data_accepts_valid_data():
    data = {"next_id": 2, "tasks": [make_task()]}
    assert validate_data(data) is None


@pytest.mark.parametrize(
    "data, message",
    [
        ("not an object", "Task data must be a JSON object."),
        ({"next_id": 0, "tasks": []}, "next_id must be a positive integer."),
        ({"next_id": True, "tasks": []}, "next_id must be a positive integer."),
        ({"next_id": 1}, "Task data must contain a tasks list."),
        ({"next_id": 1, "tasks": [make_task()]}, "next_id must be greater than every task ID."),
    ],
)

def test_validate_data_rejects_invalid_data(data, message):
    with pytest.raises(ValueError, match=message):
        validate_data(data)