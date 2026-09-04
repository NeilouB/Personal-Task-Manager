from tasks import add_task, complete_task, delete_task, edit_task
from persistence import load_tasks, save_tasks

def view_tasks(tasks_list, detail_view):
    if not tasks_list:
        print("No tasks found.")
        return
    for task in tasks_list:
        if detail_view == "y":
            print(
                f"ID: {task['id']}, Title: {task['title']}, "
                f"Description: {task['description']}, Status: {task['status']}, "
                f"Due Date: {task['due_date']}, Created At: {task['created_at']}, "
                f"Updated At: {task['updated_at']}, Completed At: {task['completed_at']}"
            )
        elif detail_view == "n":
            print(f"{task['id']}. {task['title']} ({task['status']})")
        else :
            print("Invalid input. Please enter 'y' or 'n'.")
            return


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
            data = load_tasks()
        except ValueError as error:
            print(f"Error loading tasks: {error}")
            break
        tasks = data["tasks"]
        display_menu()

        choice = input("What would you like to do? : ")

        if choice == "1":
            title = input("Enter task title (required): ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter task due date (optional, format: YYYY-MM-DD): ")
            add_task(data, title, description, due_date)
        elif choice == "2":
            detail_view = input("View task details? (y/n): ").strip().lower()
            view_tasks(tasks, detail_view)
        elif choice == "3":
            detail_view = input("View task details? (y/n): ").strip().lower()
            view_tasks(tasks, detail_view)
            if tasks:
                task_id = read_task_id("Enter the ID of the task to complete: ")
                if task_id is not None:
                    complete_task(tasks, task_id)
        elif choice == "4":
            detail_view = input("View task details? (y/n): ").strip().lower()
            view_tasks(tasks, detail_view)
            if tasks:
                task_id = read_task_id("Enter the ID of the task to delete: ")
                if task_id is not None:
                    confirmation = input("Are you sure you want to permanently delete this task? (y/n): ")
                    if confirmation.strip().lower() == "y":
                        delete_task(tasks, task_id)
                    else:
                        print("Deletion cancelled.")                   
        elif choice == "5":
            detail_view = input("View task details? (y/n): ").strip().lower()
            view_tasks(tasks, detail_view)
            if tasks:
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

        save_tasks(data)