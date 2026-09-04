# Personal Task Manager Plan

## User Stories and Acceptance Criteria

### 1. Create a task

**As a user,** I want to create a task so that I can record something I need to do.

**Acceptance criteria:**

- The user can enter a task title.
- The user can optionally add a description.
- A task cannot be saved without a title.
- The new task appears in the task list after saving.

### 2. View tasks

**As a user,** I want to view my tasks so that I know what needs to be done.

**Acceptance criteria:**

- Tasks display their title, status, and due date.
- An appropriate empty state appears when no tasks exist.

### 3. Edit a task

**As a user,** I want to edit a task so that I can keep its details accurate.

**Acceptance criteria:**

- The user can update editable task fields.
- Changes are saved after submission.
- The user can cancel without changing the task.

### 4. Complete a task

**As a user,** I want to mark a task as complete so that I can track my progress.

**Acceptance criteria:**

- The user can mark an active task as complete.
- Completed tasks are visually distinguishable.
- The user can reopen a completed task.

### 5. Delete a task

**As a user,** I want to delete a task so that I can remove tasks I no longer need.

**Acceptance criteria:**

- The user can delete a task.
- The system asks for confirmation before deletion.
- A deleted task is permanently removed and no longer appears in the task list.
- Cancelling confirmation preserves the task.

### 6. Save tasks between sessions

**As a user,** I want my tasks to be saved between sessions so that they are still available when I return.

**Acceptance criteria:**

- Tasks persist after closing and reopening the application.
- Task titles, descriptions, statuses, and due dates are preserved.
- Completed task states remain consistent between sessions, and permanently deleted tasks are not restored.
- Saved tasks are restored automatically when the user starts a new session.

## Task Model

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | Positive integer | Yes | Unique, immutable task identifier |
| `title` | String, maximum 200 characters | Yes | Short task name; must not be blank |
| `description` | String, maximum 2,000 characters | No | Additional details; empty when not provided |
| `status` | Enum | Yes | `pending`, or `completed` |
| `due_date` | `YYYY-MM-DD` string | No | Optional deadline; empty when not provided |
| `created_at` | `YYYY-MM-DD` string | Yes | Creation date |
| `updated_at` | `YYYY-MM-DD` string | Yes | Last modification date |
| `completed_at` | `YYYY-MM-DD` string or `null` | No | Set when completed; cleared if reopened |

### Model Rules

- `id` must be unique and immutable.
- New IDs must be one greater than the highest existing ID; IDs are not reused after deletion.
- `title` must contain at least one non-whitespace character.
- `title` must not exceed 200 characters after trimming whitespace.
- `description` must not exceed 2,000 characters.
- New tasks default to `pending`.
- Dates must use the `YYYY-MM-DD` format and represent valid calendar dates.
- `due_date` is optional and is stored as an empty string when omitted.
- Only completed tasks may have a `completed_at` value.
- Completed tasks must have a `completed_at` date.
- A task may be reopened, changing its status from `completed`.
- Deleted tasks are permanently removed from storage.
- `updated_at` changes whenever task data changes.
- All task fields must persist between application sessions.
- Saved task data must be a JSON list of valid task objects with unique positive IDs.

## Edge Cases

### Creation and validation

- Empty or whitespace-only title.
- Title exceeding the maximum length.
- Description exceeding its maximum length.
- Invalid date, including impossible dates such as `2026-02-30`.
- Incorrect date format.
- Duplicate task titles.
- Missing or invalid task identifier.
- Zero, negative, non-numeric, or duplicate task IDs.
- Invalid task status.
- Missing or unexpected fields in saved task data.
- Saving while required data is incomplete.
- User cancels task creation.

### Editing

- Editing a task that was deleted or no longer exists.
- Saving unchanged data.
- Cancelling after making changes.
- Concurrent edits from multiple sessions.
- Failure while saving changes.

### Status and completion

- Completing an already completed task.
- Reopening an already pending or in-progress task.
- Completing a task with no due date.
- Invalid status values.
- Incorrect or missing `completed_at` timestamp.
- Changing a completed task’s details.

### Dates and time

- Due date set to today.
- Invalid date format.
- Time-zone changes between sessions.
- Daylight-saving-time transitions, if times are supported.
- Clearing an existing due date.

### Deletion

- Deleting a nonexistent task.
- Attempting to delete a task that was already deleted.
- Cancelling the deletion confirmation.
- Application closing during deletion.
- Confirming that deletion is permanent and tasks cannot be restored.

### Persistence

- No saved task data on first launch.
- Corrupted or partially written storage.
- Storage unavailable or full.
- Duplicate tasks after reopening the application.
- Data written immediately after every change versus unsaved changes on exit.
- Application crash while saving.
- Migration when the task model changes in a future version.
- Tasks created in one session not appearing in the next session.