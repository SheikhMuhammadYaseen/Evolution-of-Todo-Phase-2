# Data Model: Phase I CLI Todo Application

**Feature**: 001-phase1-cli-todo
**Date**: 2025-12-27
**Phase**: Phase 1 (Design)

## Overview

Phase I uses simple in-memory data structures (Python lists and dictionaries) to store tasks. No database, no ORM, no persistence. All data is lost when the application exits.

## Entity: Task

**Purpose**: Represents a single todo item with an identifier, descriptive text, and completion status.

### Attributes

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| id | int | Unique, auto-incremented, never reused, starts at 1 | Auto-assigned | Unique identifier for the task |
| title | str | Non-empty after whitespace trimming, mandatory | None | Short description of the task |
| description | str | Optional, can be empty string | "" | Additional details about the task |
| status | bool | True = complete, False = incomplete | False | Completion status of the task |

### Python Dictionary Representation

```python
task = {
    "id": 1,                        # int: Auto-incremented identifier
    "title": "Buy groceries",       # str: Non-empty task title
    "description": "Milk, eggs, bread",  # str: Optional details
    "status": False                 # bool: False = incomplete, True = complete
}
```

### Validation Rules

**ID**:
- System-assigned, user cannot specify
- Sequential integers starting from 1
- Never reused even after task deletion
- Unique within a session

**Title**:
- Must not be empty after `title.strip()`
- Minimum 1 character (excluding leading/trailing whitespace)
- No maximum length (Python string can hold arbitrary length)
- All printable characters allowed

**Description**:
- Optional - can be empty string
- No validation required
- All printable characters allowed

**Status**:
- Boolean: False (incomplete) or True (complete)
- Defaults to False on task creation
- Toggled via "Mark Task Complete/Incomplete" operation

### State Transitions

```
[Task Created]
     ↓
  status = False (Incomplete)
     ↓
     ↕  (Toggle operation)
     ↓
  status = True (Complete)
     ↓
     ↕  (Toggle operation)
     ↓
  status = False (Incomplete)
     ↓
  [Task Deleted]
```

**Lifecycle**:
1. Task created → status = False, ID assigned
2. Task viewed → status displayed as "Complete" or "Incomplete"
3. Task updated → title/description modified, status unchanged
4. Task toggled → status flipped (False ↔ True)
5. Task deleted → removed from memory, ID never reused

## Global State

### Tasks Storage

```python
tasks = []  # List of task dictionaries
```

**Structure**: List (array) of dictionaries
**Operations**:
- Append: O(1) - add new task
- Iterate: O(n) - view all tasks
- Search: O(n) - find task by ID (linear search)
- Delete: O(n) - find and remove

**Why list instead of dict**:
- Simple and Pythonic
- No need for O(1) lookup at Phase I scale (dozens to hundreds of tasks)
- Easy to iterate for viewing all tasks
- Preserves insertion order (tasks displayed in creation order)

### ID Counter

```python
next_id = 1  # Next ID to assign
```

**Purpose**: Track the next available ID for task creation

**Behavior**:
- Initialized to 1 at application start
- Incremented after each task creation
- Never decremented (even if tasks deleted)
- Ensures unique IDs throughout session

## Data Operations

### Create (Add Task)

```python
def add_task(tasks, next_id, title, description):
    """
    Add a new task to the list.

    Args:
        tasks: List of task dictionaries
        next_id: Next available ID
        title: Non-empty task title (pre-validated)
        description: Optional task description

    Returns:
        int: Updated next_id (incremented by 1)
    """
    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip(),
        "status": False
    }
    tasks.append(task)
    return next_id + 1
```

### Read (View Tasks)

```python
def view_tasks(tasks):
    """
    Return list of all tasks.

    Args:
        tasks: List of task dictionaries

    Returns:
        list: All tasks (empty list if no tasks)
    """
    return tasks
```

### Update (Modify Task)

```python
def update_task(tasks, task_id, new_title, new_description):
    """
    Update an existing task's title and/or description.

    Args:
        tasks: List of task dictionaries
        task_id: ID of task to update
        new_title: New title (non-empty, pre-validated)
        new_description: New description

    Returns:
        bool: True if updated, False if task not found
    """
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title.strip()
            task["description"] = new_description.strip()
            return True
    return False
```

### Delete (Remove Task)

```python
def delete_task(tasks, task_id):
    """
    Delete a task by ID.

    Args:
        tasks: List of task dictionaries
        task_id: ID of task to delete

    Returns:
        bool: True if deleted, False if task not found
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False
```

### Toggle Status

```python
def toggle_status(tasks, task_id):
    """
    Toggle completion status of a task.

    Args:
        tasks: List of task dictionaries
        task_id: ID of task to toggle

    Returns:
        bool or None: New status if toggled, None if task not found
    """
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = not task["status"]
            return task["status"]
    return None
```

### Find Task by ID

```python
def find_task_by_id(tasks, task_id):
    """
    Locate a task by ID.

    Args:
        tasks: List of task dictionaries
        task_id: ID to search for

    Returns:
        dict or None: Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
```

## Data Constraints

**Memory Limits**: No explicit limits enforced in Phase I. Python list can grow to available memory. Expected usage: 10-1000 tasks per session (a few KB to ~100 KB memory).

**Concurrency**: Single-threaded, single-user. No locking or synchronization needed.

**Persistence**: None. All data lost on application exit (per Phase I specification).

## Phase II Migration Notes

**When Phase II introduces API layer and database persistence**:

1. Convert dict representation to Pydantic models for API serialization
2. Introduce SQLModel for ORM mapping to Neon DB (PostgreSQL)
3. Add UUID or auto-increment primary key at database level
4. Replace in-memory list with database queries
5. Add created_at, updated_at timestamps
6. Consider adding user_id foreign key for multi-user support (Phase III+)

**Current Phase I design supports easy migration**:
- Dictionary keys map directly to database columns
- Simple data types (int, str, bool) are database-friendly
- No complex nested structures to flatten
- Clear entity boundaries (no mixing of concerns)

## Example Data

**Empty state (application start)**:
```python
tasks = []
next_id = 1
```

**After adding three tasks**:
```python
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "status": False},
    {"id": 2, "title": "Call dentist", "description": "", "status": False},
    {"id": 3, "title": "Submit report", "description": "Quarterly analysis", "status": True}
]
next_id = 4
```

**After deleting task 2**:
```python
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "status": False},
    {"id": 3, "title": "Submit report", "description": "Quarterly analysis", "status": True}
]
next_id = 4  # Note: ID 2 is not reused, next task gets ID 4
```

## Data Integrity Rules

1. **ID Uniqueness**: Enforced by sequential assignment, no duplicates possible within a session
2. **ID Immutability**: Task ID never changes after creation
3. **Title Non-Empty**: Validated before calling add_task() or update_task()
4. **Status Boolean**: Type enforced by Python (no string "true"/"false")
5. **No Orphaned References**: Task deletion is immediate and complete, no dangling references

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Add Task | O(1) | O(1) | Append to list |
| View All Tasks | O(n) | O(1) | Iterate list |
| Find Task by ID | O(n) | O(1) | Linear search |
| Update Task | O(n) | O(1) | Find then modify |
| Delete Task | O(n) | O(1) | Find then remove |
| Toggle Status | O(n) | O(1) | Find then flip bool |

*n = number of tasks in list*

**Phase I Scale**: Expected n = 10-1000, all operations remain fast (<1ms for n=1000)

**Phase II Optimization**: If n > 10,000, replace list with dictionary keyed by ID for O(1) lookup

## Sign-off

**Data Model Status**: ✅ Complete
**Next Phase**: Generate quickstart.md, then proceed to /sp.tasks
