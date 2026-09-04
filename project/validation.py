from datetime import date, datetime

# Constants
DATE_FORMAT = "%Y-%m-%d"
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
VALID_STATUSES = {"pending", "completed"}
TASK_FIELDS = {
    "id",
    "title",
    "description",
    "status",
    "due_date",
    "created_at",
    "updated_at",
    "completed_at",
}


def validate_date(value, field_name, allow_empty=True):
    if allow_empty and value in ("", None):
        return
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a date in YYYY-MM-DD format.")
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError as error:
        raise ValueError(f"{field_name} must be a date in YYYY-MM-DD format.") from error


def parse_due_date(value):
    value = value.strip()
    if not value:
        return ""
    try:
        validate_date(value, "Due date", allow_empty=False)
    except ValueError as error:
        print(error)
        return None
    return value


# Check the structure of the tasks
def validate_tasks(tasks):
    if not isinstance(tasks, list):
        raise ValueError("Task data must be a JSON list.")

    ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Each task must be a JSON object.")
        if set(task) != TASK_FIELDS:
            raise ValueError("Each task must contain the expected fields.")
        if not isinstance(task["id"], int) or isinstance(task["id"], bool) or task["id"] <= 0:
            raise ValueError("Task IDs must be positive integers.")
        if task["id"] in ids:
            raise ValueError("Task IDs must be unique.")
        ids.add(task["id"])
        if not isinstance(task["title"], str) or not task["title"].strip():
            raise ValueError("Task titles must not be empty.")
        if len(task["title"].strip()) > MAX_TITLE_LENGTH:
            raise ValueError(f"Task titles cannot exceed {MAX_TITLE_LENGTH} characters.")
        if not isinstance(task["description"], str) or len(task["description"]) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Descriptions cannot exceed {MAX_DESCRIPTION_LENGTH} characters.")
        if task["status"] not in VALID_STATUSES:
            raise ValueError("Task status is invalid.")
        validate_date(task["due_date"], "Due date")
        validate_date(task["created_at"], "Created date", allow_empty=False)
        validate_date(task["updated_at"], "Updated date", allow_empty=False)
        validate_date(task["completed_at"], "Completed date")
        if task["status"] == "completed" and not task["completed_at"]:
            raise ValueError("Completed tasks must have a completed date.")
        if task["status"] != "completed" and task["completed_at"]:
            raise ValueError("Only completed tasks may have a completed date.")


def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("Task data must be a JSON object.")

    if not isinstance(data.get("next_id"), int) or isinstance(data.get("next_id"), bool) or data["next_id"] <= 0:
        raise ValueError("next_id must be a positive integer.")

    if "tasks" not in data:
        raise ValueError("Task data must contain a tasks list.")

    validate_tasks(data["tasks"])

    highest_id = max((task["id"] for task in data["tasks"]), default=0)
    if data.get("next_id") <= highest_id:
        raise ValueError("next_id must be greater than every task ID.")