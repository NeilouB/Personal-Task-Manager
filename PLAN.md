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
- Overdue tasks are clearly identified.
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
- A deleted task no longer appears in the task list.
- Cancelling confirmation preserves the task.

### 6. Save tasks between sessions

**As a user,** I want my tasks to be saved between sessions so that they are still available when I return.

**Acceptance criteria:**

- Tasks persist after closing and reopening the application.
- Task titles, descriptions, statuses, and due dates are preserved.
- Completed and deleted task states remain consistent between sessions.
- Saved tasks are restored automatically when the user starts a new session.

## Task Model

 Field         |Type       |Required|Description                                              |
|--------------|-----------|--------|---------------------------------------------------------|
|`id`          |UUID/string|Yes     |Unique task identifier                                   |
|`title`       |String     |Yes     |Short task name; must not be blank                       |
|`description` |String     |No      |Additional details                                       |
|`status`      |Enum       |Yes     |`pending`, `in_progress`, or `completed`                 |
|`due_date`    |Date       |No      |Optional deadline                                        |
|`created_at`  |DateTime   |Yes     |Creation timestamp                                       |
|`updated_at`  |DateTime   |Yes     |Last modification timestamp                              |
|`completed_at`|DateTime   |No      |Set when completed; cleared if reopened                  |
|`deleted_at`  |DateTime   |No      |Used for soft deletion, if deletion recovery is supported|

### Model Rules

- `id` must be unique and immutable.
- `title` must contain at least one non-whitespace character.
- Titles should have a defined maximum length, such as 200 characters.
- New tasks default to `pending`.
- Only completed tasks may have a `completed_at` value.
- A task may be reopened, changing its status from `completed`.
- Deleted tasks must not appear in the normal task list.
- `updated_at` changes whenever task data changes.
- All task fields must persist between application sessions.

## Edge Cases

### Creation and validation

- Empty or whitespace-only title.
- Title exceeding the maximum length.
- Description exceeding its maximum length.
- Duplicate task titles.
- Missing or invalid task identifier.
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

- Due date in the past.
- Due date set to today.
- Invalid date format.
- Time-zone changes between sessions.
- Daylight-saving-time transitions, if times are supported.
- Clearing an existing due date.

### Deletion

- Deleting a nonexistent task.
- Deleting an already deleted task.
- Cancelling the deletion confirmation.
- Application closing during deletion.
- Whether deleted tasks can be restored or are permanently removed.

### Persistence

- No saved task data on first launch.
- Corrupted or partially written storage.
- Storage unavailable or full.
- Duplicate tasks after reopening the application.
- Data written immediately after every change versus unsaved changes on exit.
- Application crash while saving.
- Migration when the task model changes in a future version.
- Tasks created in one session not appearing in the next session.