from datetime import date, datetime
import json

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


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty list of tasks
        return []
    except json.JSONDecodeError as error:
        # If the file contains invalid JSON
        raise ValueError("tasks.json contains invalid JSON.") from error
    # Check the validity of the tasks
    validate_tasks(tasks)
    return tasks


def save_tasks(tasks_list):
    with open("tasks.json", "w") as file:
        json.dump(tasks_list, file, indent=4)


def today():
    return date.today().strftime(DATE_FORMAT)


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


def add_task(tasks_list, title, description, due_date):
    title = title.strip()
    # Title is required and must not exceed the maximum length
    if not title:
        print("A task title is required.")
        return
    if len(title) > MAX_TITLE_LENGTH:
        print(f"Task titles cannot exceed {MAX_TITLE_LENGTH} characters.")
        return
    # Description is optional but must not exceed the maximum length
    description = description.strip()
    if len(description) > MAX_DESCRIPTION_LENGTH:
        print(f"Descriptions cannot exceed {MAX_DESCRIPTION_LENGTH} characters.")
        return

    due_date = parse_due_date(due_date)
    if due_date is None:
        return

    task = {
        "id": max((task["id"] for task in tasks_list), default=0) + 1,
        "title": title,
        "description": description,
        "status": "pending",
        "due_date": due_date,
        "created_at": today(),
        "updated_at": today(),
        "completed_at": None
    }
    tasks_list.append(task)
    print("Task added.")


def find_task(tasks_list, task_id):
    return next((task for task in tasks_list if task["id"] == task_id), None)


def edit_task(tasks_list, task_id, new_title, new_description, new_due_date):
    task = find_task(tasks_list, task_id)
    if task is None:
        print("Task not found.")
        return

    new_title = new_title.strip()
    new_description = new_description.strip()
    new_due_date = new_due_date.strip()

    if new_title:
        if len(new_title) > MAX_TITLE_LENGTH:
            print(f"Task titles cannot exceed {MAX_TITLE_LENGTH} characters.")
            return
        task["title"] = new_title
    if new_description.lower() == "none":
        task["description"] = ""
    elif new_description:
        if len(new_description) > MAX_DESCRIPTION_LENGTH:
            print(f"Descriptions cannot exceed {MAX_DESCRIPTION_LENGTH} characters.")
            return
        task["description"] = new_description

    if new_due_date.lower() == "none":
        task["due_date"] = ""
    elif new_due_date:
        due_date = parse_due_date(new_due_date)
        if due_date is None:
            return
        task["due_date"] = due_date

    task["updated_at"] = today()
    print("Task updated.")

def view_tasks(tasks_list):
    if not tasks_list:
        print("No tasks found.")
        return
    detail_view = input("View task details? (y/n): ").strip().lower() == "y"
    for task in tasks_list:
        if detail_view:
            print(
                f"ID: {task['id']}, Title: {task['title']}, "
                f"Description: {task['description']}, Status: {task['status']}, "
                f"Due Date: {task['due_date']}, Created At: {task['created_at']}, "
                f"Updated At: {task['updated_at']}, Completed At: {task['completed_at']}"
            )
        else:
            print(f"{task['id']}. {task['title']} ({task['status']})")

def complete_task(tasks_list, task_id):
    task = find_task(tasks_list, task_id)
    if task is None:
        print("Task not found.")
    elif task["status"] == "completed":
        print("Task is already completed.")
    else:
        task["status"] = "completed"
        task["completed_at"] = today()
        task["updated_at"] = today()
        print("Task completed.")

def delete_task(tasks_list, task_id):
    task = find_task(tasks_list, task_id)
    if task is None:
        print("Task not found.")
        return

    confirmation = input("Are you sure you want to permanently delete this task? (y/n): ")
    if confirmation.strip().lower() == "y":
        tasks_list.remove(task)
        print("Task deleted.")
    else:
        print("Deletion cancelled.")


def read_task_id(prompt):
    try:
        task_id = int(input(prompt))
    except ValueError:
        print("Please enter a valid numeric task ID.")
        return None
    if task_id <= 0:
        print("Task ID must be a positive integer.")
        return None
    return task_id

def display_menu():
    print()
    print("*"*33)
    print("*\tTask Manager Menu:\t*")
    print("*\t1. Add Task\t\t*")
    print("*\t2. View Tasks\t\t*")
    print("*\t3. Complete Task\t*")
    print("*\t4. Delete Task\t\t*")
    print("*\t5. Edit Task\t\t*")
    print("*\t6. Exit\t\t\t*")
    print("*"*33)

# MAIN PROGRAM
if __name__ == "__main__":
    while True:
        try :
            tasks = load_tasks()
        except ValueError as error:
            print(f"Error loading tasks: {error}")
            break
        
        display_menu()

        choice = input("What would you like to do? : ")

        if choice == "1":
            title = input("Enter task title (required): ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter task due date (optional, format: YYYY-MM-DD): ")
            add_task(tasks, title, description, due_date)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks)
            task_id = read_task_id("Enter the ID of the task to complete: ")
            if task_id is not None:
                complete_task(tasks,task_id)
        elif choice == "4":
            view_tasks(tasks)
            task_id = read_task_id("Enter the ID of the task to delete: ")
            if task_id is not None:
                delete_task(tasks,task_id)
        elif choice == "5":
            view_tasks(tasks)
            task_id = read_task_id("Enter the ID of the task to edit: ")
            if task_id is not None:
                new_title = input("New title (Enter to keep): ")
                new_description = input("New description (Enter to keep, or 'none' to clear): ")
                new_due_date = input("New due date (Enter to keep, or 'none' to clear): ")
                edit_task(tasks, task_id, new_title, new_description, new_due_date)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

        save_tasks(tasks)