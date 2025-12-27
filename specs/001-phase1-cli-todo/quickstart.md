# Quickstart Guide: Phase I CLI Todo Application

**Feature**: 001-phase1-cli-todo
**Date**: 2025-12-27
**Audience**: End users, testers, developers

## Prerequisites

**Required**:
- Python 3.11 or higher installed
- Terminal/console access (Windows Command Prompt, PowerShell, macOS Terminal, Linux shell)

**Not Required**:
- No external dependencies
- No database setup
- No configuration files
- No internet connection

## Installation

**Phase I has no installation** - it's a single Python script.

1. Ensure Python 3.11+ is installed:
   ```bash
   python --version
   # Should show: Python 3.11.x or higher
   ```

2. Navigate to the project directory:
   ```bash
   cd /path/to/evolution-todo/phase-1/todo
   ```

## Running the Application

**Start the application**:
```bash
python src/main.py
```

**You will see the main menu**:
```
==================== TODO MANAGER ====================
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
======================================================
Enter your choice (1-6):
```

## Basic Usage

### Add a Task

1. Select option `1` from the menu
2. Enter a task title when prompted (required)
3. Enter a description when prompted (optional, press Enter to skip)
4. See confirmation: `"Task {ID} added successfully."`

**Example**:
```
Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description (press Enter to skip): Milk, eggs, bread
Task 1 added successfully.
```

### View All Tasks

1. Select option `2` from the menu
2. See a formatted list of all tasks with IDs, titles, descriptions, and statuses

**Example**:
```
Enter your choice (1-6): 2

==================== TODO LIST ====================
ID | Title                | Description           | Status
---+----------------------+-----------------------+-----------
1  | Buy groceries        | Milk, eggs, bread     | Incomplete
2  | Call dentist         |                       | Incomplete
===================================================
```

**Empty list**:
```
Enter your choice (1-6): 2
No tasks found. Your todo list is empty.
```

### Update a Task

1. Select option `3` from the menu
2. Enter the task ID to update
3. Enter a new title (or press Enter to keep current)
4. Enter a new description (or press Enter to keep current)
5. See confirmation: `"Task {ID} updated successfully."`

**Example**:
```
Enter your choice (1-6): 3
Enter task ID: 1
Enter new title (press Enter to keep current): Buy groceries and cleaning supplies
Enter new description (press Enter to keep current):
Task 1 updated successfully.
```

### Delete a Task

1. Select option `4` from the menu
2. Enter the task ID to delete
3. See confirmation: `"Task {ID} deleted successfully."`

**Example**:
```
Enter your choice (1-6): 4
Enter task ID: 2
Task 2 deleted successfully.
```

### Mark Task Complete or Incomplete

1. Select option `5` from the menu
2. Enter the task ID to toggle
3. See confirmation: `"Task {ID} marked as complete."` or `"Task {ID} marked as incomplete."`

**Example**:
```
Enter your choice (1-6): 5
Enter task ID: 1
Task 1 marked as complete.
```

**Toggle again**:
```
Enter your choice (1-6): 5
Enter task ID: 1
Task 1 marked as incomplete.
```

### Exit the Application

1. Select option `6` from the menu
2. Application exits
3. **All data is lost** (no persistence in Phase I)

**Example**:
```
Enter your choice (1-6): 6
Exiting... All data will be lost.
```

## Error Handling

### Invalid Menu Choice

**Non-numeric input**:
```
Enter your choice (1-6): abc
Invalid input. Please enter a number.
```

**Out-of-range number**:
```
Enter your choice (1-6): 99
Invalid choice. Please select a number from 1 to 6.
```

### Empty Task Title

```
Enter task title:
Title cannot be empty. Please try again.
Enter task title: Buy groceries
Enter task description (press Enter to skip):
Task 1 added successfully.
```

### Non-Existent Task ID

**Update/Delete/Toggle with invalid ID**:
```
Enter task ID: 999
Task ID 999 not found.
```

### Keyboard Interrupt (Ctrl+C)

Pressing `Ctrl+C` exits gracefully:
```
^C
Exiting... All data will be lost.
```

## Common Workflows

### Quick Todo Session

1. Start application: `python src/main.py`
2. Add a few tasks (option 1)
3. View tasks (option 2)
4. Mark one complete (option 5)
5. View again to see status change (option 2)
6. Exit (option 6)

### Editing a Task

1. View tasks to see which ID to edit (option 2)
2. Update the task (option 3)
3. Enter the ID
4. Change title, description, or both
5. View tasks again to confirm changes (option 2)

### Cleaning Up Tasks

1. View tasks (option 2)
2. Delete unwanted tasks one by one (option 4)
3. View again to confirm deletion (option 2)

## Important Notes

### Data Persistence

**⚠️ WARNING**: All data is lost when you exit the application. Phase I does not save tasks to disk or database.

- No automatic save
- No manual save option
- Closing the terminal window loses data
- Ctrl+C loses data
- Power failure loses data

**Recommendation**: Use Phase I for temporary todo lists within a single session only.

### Task ID Behavior

**Task IDs are never reused** even after deletion:

Example:
1. Add task → ID 1
2. Add task → ID 2
3. Delete task 1
4. Add task → ID 3 (not ID 1)

This prevents confusion and maintains audit trail within the session.

### Console Display

- Best viewed in terminal with at least 80 characters width
- Long titles/descriptions may wrap or truncate depending on terminal settings
- No color coding (plain text output)

## Troubleshooting

### "python: command not found"

**Solution**: Python not installed or not in PATH. Install Python 3.11+ from python.org.

### "No module named 'main'"

**Solution**: Wrong directory. Navigate to the directory containing `src/main.py`.

### "SyntaxError" on startup

**Solution**: Python version too old. Verify Python 3.11+ with `python --version`.

### Tasks not appearing after adding

**Solution**: Select option 2 (View Task List) to display tasks. Adding a task doesn't automatically show the list.

### Can't see previous tasks after restarting

**Solution**: Expected behavior. Phase I has no persistence - all data is lost on exit.

## Testing the Application

### Manual Acceptance Testing

Follow the acceptance scenarios in [spec.md](./spec.md) to verify all functionality:

**User Story 1 - Add Task**:
- ✅ Add task with title and description
- ✅ Add task with title only (no description)
- ✅ Reject task with empty title

**User Story 2 - View Tasks**:
- ✅ View multiple tasks
- ✅ View empty list
- ✅ Verify readable format

**User Story 3 - Mark Complete/Incomplete**:
- ✅ Mark incomplete task complete
- ✅ Mark complete task incomplete
- ✅ Reject invalid task ID

**User Story 4 - Update Task**:
- ✅ Update title only
- ✅ Update description only
- ✅ Update both title and description
- ✅ Reject empty title
- ✅ Reject invalid task ID

**User Story 5 - Delete Task**:
- ✅ Delete task from middle of list
- ✅ Delete last remaining task
- ✅ Reject invalid task ID

### Edge Cases to Test

- Enter non-numeric menu choice → Error message
- Enter menu choice outside 1-6 → Error message
- Add task with special characters (émojis, symbols) → Accepted
- Add task with very long title (1000+ characters) → Accepted
- Exit via Ctrl+C → Clean exit

## Next Steps

**Phase I Complete**: If all acceptance tests pass, Phase I is ready for demo.

**Phase II Preview**: Future enhancements will include:
- REST API with FastAPI
- Data persistence
- API-based task management
- Automated tests

## Support

**For Issues**:
1. Verify Python 3.11+ installed
2. Verify correct directory (`src/main.py` exists)
3. Review error messages carefully
4. Check specification ([spec.md](./spec.md)) for expected behavior

**Phase I Limitations** (by design):
- No data persistence
- No multi-user support
- No web interface
- No external dependencies
- No advanced features (filters, search, priorities)

These are not bugs - they are Phase I boundaries per the constitution.
