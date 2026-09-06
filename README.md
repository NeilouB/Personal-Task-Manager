# Personal Task Manager
The Personal Task Manager is a small task management tool that provides different features, available through a CLI menu.

Users can add, complete, edit, delete, and view tasks, with all data persisted in a local JSON file.

It is written in Python.

## Project status

This is a personal project for learning, currently in development. The core task-management features are implemented, including task creation, editing, completion, deletion, and JSON-based persistence.

## Installation
Clone the repository
```powershell
git clone https://github.com/NeilouB/Personal-Task-Manager.git
cd Personal-Task-Manager
```

Create a virtual environment and activate it
```powershell
cd project
python -m venv venv
venv\Scripts\Activate.ps1
```

Install dependencies (pytest)
```powershell
pip install pytest
```

Run the application
```powershell
python cli.py
```


## Usage
1. Adding a task:
```
*****************************
*       Task Manager Menu:  *
*       1. Add Task         *
*       2. View Tasks       *
*       3. Complete Task    *
*       4. Delete Task      *
*       5. Edit Task        *
*       6. Exit             *
*****************************
What would you like to do? :1 
Enter task title (required):Buy groceries
Enter task description (optional): Milk, Mustard, Eggs
Enter task due date (optional, format: YYYY-MM-DD): 
Task added.
```

2. Viewing tasks (without details):
```
What would you like to do? : 2
View task details? (y/n): n
1. Buy groceries (pending)
```

3. Viewing tasks (with details):
```
What would you like to do? : 2
View task details? (y/n): y
ID: 1, Title: Buy groceries, Description: Milk, Mustard, Eggs, Status: pending, Due Date: , Created At: 2026-09-05, Updated At: 2026-09-05, Completed At: None
```

4. Completing a task:
```
What would you like to do? : 3
View task details? (y/n): n
1. Buy groceries (pending)
Enter the ID of the task to complete: 1
Task completed.
```

5. Editing a task:
```
What would you like to do? : 5
View task details? (y/n): n
1. Buy groceries (completed)
Enter the ID of the task to edit: 1
New title (Enter to keep): 
New description (Enter to keep, or 'none' to clear): none
New due date (Enter to keep, or 'none' to clear):   
Task updated.
```

6. Deleting a task:
```
What would you like to do? : 4
View task details? (y/n): n
1. Buy groceries (completed)
Enter the ID of the task to delete: 1
Are you sure you want to permanently delete this task? (y/n): Y
Task deleted.
```


## Available commands
Task Manager Menu:
1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Edit Task
6. Exit


## Validation rules
- Titles are required and limited to 200 characters.
- Descriptions are limited to 2,000 characters.
- Dates must use "YYYY-MM-DD".
- Due dates are optional.
- Task IDs must be positive integers.
- Enter "none" while editing to clear the description or due date.


## Running tests
Run tests:
```powershell
pytest -v
```

## Future improvements
- Add task priority
- Use a database
- Add tasks categories
- Add reminders
- Add a web interface

## Reflection on AI-Assisted Development
### 1. Where AI saved the most time:
I used GitHub Copilot along with Claude for this project. It was useful for drafting requirements and identifying edge cases in a few hours rather than some days. 
It also helped me speed up the writing my tests phase, since manually writing every single test case would have taken much longer. 
Beyond that, it also helped me catch bugs I might have missed and gave useful suggestions for improving my code's structure and quality.

### 2. Where AI output was incomplete or incorrect:
While writing tests for parse_due_date, I initially had to rethink the logic of one of my tests to get it working correctly. It highlighted the importance of not assuming how a function behaves internally, but instead verifying its actual behavior empirically.

### 3. What I understand better now: 
This was my first time writing tests in Python, and working through this project (with Copilot and Claude) taught me that a function needs to be tested against all the cases it could realistically receive, not just the perfect cases I initially had in mind.