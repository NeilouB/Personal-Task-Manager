from datetime import date, datetime
import json

DATE_FORMAT = "%Y-%m-%d"


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_tasks(tasks_list):
    with open("tasks.json", "w") as file:
        json.dump(tasks_list, file, indent=4)


def today():
    return date.today().strftime(DATE_FORMAT)


def parse_due_date(value):
    value = value.strip()
    if not value:
        return ""
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        print("Invalid date. Use the format YYYY-MM-DD.")
        return None
    return value


def add_task(title, description, due_date):
    title = title.strip()
    if not title:
        print("A task title is required.")
        return

    due_date = parse_due_date(due_date)
    if due_date is None:
        return

    tasks = load_tasks()
    task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": title,
        "description": description.strip(),
        "status": "pending",
        "due_date": due_date,
        "created_at": today(),
        "updated_at": today(),
        "completed_at": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")


def find_task(tasks, task_id):
    return next((task for task in tasks if task["id"] == task_id), None)


def edit_task(task_id, new_title, new_description, new_due_date):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task is None:
        print("Task not found.")
        return

    if new_title.strip():
        task["title"] = new_title.strip()
    if new_description.strip().lower() == "none":
        task["description"] = ""
    elif new_description.strip():
        task["description"] = new_description.strip()

    if new_due_date.strip().lower() == "none":
        task["due_date"] = ""
    elif new_due_date.strip():
        due_date = parse_due_date(new_due_date)
        if due_date is None:
            return
        task["due_date"] = due_date

    task["updated_at"] = today()
    save_tasks(tasks)
    print("Task updated.")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    detail_view = input("View task details? (y/n): ").strip().lower() == "y"
    for task in tasks:
        if detail_view:
            print(
                f"ID: {task['id']}, Title: {task['title']}, "
                f"Description: {task['description']}, Status: {task['status']}, "
                f"Due Date: {task['due_date']}, Created At: {task['created_at']}, "
                f"Updated At: {task['updated_at']}, Completed At: {task['completed_at']}"
            )
        else:
            print(f"{task['id']}. {task['title']} ({task['status']})")

def complete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task is None:
        print("Task not found.")
    elif task["status"] == "completed":
        print("Task is already completed.")
    else:
        task["status"] = "completed"
        task["completed_at"] = today()
        task["updated_at"] = today()
        save_tasks(tasks)
        print("Task completed.")

def delete_task(task_id):
    tasks = load_tasks()
    if find_task(tasks, task_id) is None:
        print("Task not found.")
        return

    confirmation = input("Are you sure you want to permanently delete this task? (y/n): ")
    if confirmation.strip().lower() == "y":
        tasks.remove(find_task(tasks, task_id))
        save_tasks(tasks)
        print("Task deleted.")
    else:
        print("Deletion cancelled.")


def read_task_id(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid numeric task ID.")
        return None

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
        display_menu()
        choice = input("What would you like to do? : ")

        if choice == "1":
            title = input("Enter task title (required): ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter task due date (optional, format: YYYY-MM-DD): ")
            add_task(title, description, due_date)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks()
            task_id = read_task_id("Enter the ID of the task to complete: ")
            if task_id is not None:
                complete_task(task_id)
        elif choice == "4":
            view_tasks()
            task_id = read_task_id("Enter the ID of the task to delete: ")
            if task_id is not None:
                delete_task(task_id)
        elif choice == "5":
            view_tasks()
            task_id = read_task_id("Enter the ID of the task to edit: ")
            if task_id is not None:
                new_title = input("New title (Enter to keep): ")
                new_description = input("New description (Enter to keep, or 'none' to clear): ")
                new_due_date = input("New due date (Enter to keep, or 'none' to clear): ")
                edit_task(task_id, new_title, new_description, new_due_date)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")