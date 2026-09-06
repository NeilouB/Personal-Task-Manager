from datetime import date
from validation import DATE_FORMAT, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH
from validation import parse_due_date

def today():
    return date.today().strftime(DATE_FORMAT)

def add_task(data, title, description, due_date):
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
        "id": data["next_id"],
        "title": title,
        "description": description,
        "status": "pending",
        "due_date": due_date,
        "created_at": today(),
        "updated_at": today(),
        "completed_at": None
    }
    data["tasks"].append(task)
    data["next_id"] += 1
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

    if new_description.lower() == "none":
        description = ""
    elif new_description:
        if len(new_description) > MAX_DESCRIPTION_LENGTH:
            print(f"Descriptions cannot exceed {MAX_DESCRIPTION_LENGTH} characters.")
            return
        description = new_description
    else:
        description = task["description"]

    if new_due_date.lower() == "none":
        due_date = ""
    elif new_due_date:
        due_date = parse_due_date(new_due_date)
        if due_date is None:
            return
    else:
        due_date = task["due_date"]

    if new_title:
        task["title"] = new_title
    task["description"] = description
    task["due_date"] = due_date

    task["updated_at"] = today()
    print("Task updated.")


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

    tasks_list.remove(task)
    print("Task deleted.")