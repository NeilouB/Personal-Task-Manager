import json
from validation import validate_data

def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty list of tasks
        return {"next_id": 1, "tasks": []}
    except json.JSONDecodeError as error:
        # If the file contains invalid JSON
        raise ValueError("tasks.json contains invalid JSON.") from error
    # Check the validity of the tasks
    validate_data(data)
    return data


def save_tasks(data):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
