from datetime import date
import json

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

def save_tasks(tasks_list):
    with open("tasks.json", "w") as file:
        json.dump(tasks_list, file, indent=4)


tasks = load_tasks()
tasks.append({"id": 1, "title": "Sample Task", "description": "This is a sample task.", "status": "pending","created_at": date.today().strftime("%d/%m/%Y")})
save_tasks(tasks)