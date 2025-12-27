#!/usr/bin/env python3
"""
Phase I CLI Todo Application

A simple in-memory todo list manager with menu-driven console interface.
All data is lost on program exit (no persistence).

Features:
- Add tasks with title and optional description
- View all tasks in formatted list
- Update task title and/or description
- Delete tasks
- Mark tasks as complete or incomplete
- Input validation and error handling

Phase I Constraints:
- In-memory storage only (no database, no file I/O)
- Single-user, single-session
- Console interface only (no web, no API)
- Python standard library only (no external dependencies)
"""

# Global state
tasks = []      # List of task dictionaries
next_id = 1     # Counter for auto-incrementing task IDs


# ============================================================================
# VALIDATION LAYER
# ============================================================================

def validate_integer(value):
    """
    Convert string to integer with error handling.

    Args:
        value: String input to convert

    Returns:
        int or None: Converted integer, or None if conversion fails
    """
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None


def validate_title(title):
    """
    Check if title is non-empty after stripping whitespace.

    Args:
        title: String to validate

    Returns:
        bool: True if valid (non-empty), False otherwise
    """
    return bool(title and title.strip())


def validate_menu_choice(choice):
    """
    Ensure menu choice is an integer between 1 and 6.

    Args:
        choice: User input string

    Returns:
        int or None: Valid choice (1-6), or None if invalid
    """
    choice_int = validate_integer(choice)
    if choice_int and 1 <= choice_int <= 6:
        return choice_int
    return None


# ============================================================================
# DISPLAY LAYER
# ============================================================================

def display_menu():
    """Display the main menu with numbered options 1-6."""
    print("\n" + "=" * 54)
    print(" " * 15 + "TODO MANAGER")
    print("=" * 54)
    print("1. Add Task")
    print("2. View Task List")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print("=" * 54)


def display_message(message):
    """
    Print confirmation or error message.

    Args:
        message: String message to display
    """
    print(message)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def find_task_by_id(tasks, task_id):
    """
    Locate a task by ID using linear search.

    Args:
        tasks: List of task dictionaries
        task_id: Integer ID to search for

    Returns:
        dict or None: Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# ============================================================================
# BUSINESS LOGIC LAYER - CRUD OPERATIONS
# ============================================================================

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
        "status": False  # Default to incomplete
    }
    tasks.append(task)
    return next_id + 1


def toggle_status(tasks, task_id):
    """
    Toggle completion status of a task.

    Args:
        tasks: List of task dictionaries
        task_id: ID of task to toggle

    Returns:
        bool or None: New status if toggled, None if task not found
    """
    task = find_task_by_id(tasks, task_id)
    if task:
        task["status"] = not task["status"]
        return task["status"]
    return None


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
    task = find_task_by_id(tasks, task_id)
    if task:
        task["title"] = new_title.strip()
        task["description"] = new_description.strip()
        return True
    return False


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


# ============================================================================
# HANDLER FUNCTIONS (Control Flow)
# ============================================================================

def handle_add(tasks, next_id):
    """
    Handle the 'Add Task' operation.

    Prompts user for title and description, validates title,
    calls add_task(), and displays confirmation.

    Args:
        tasks: List of task dictionaries
        next_id: Current next_id counter

    Returns:
        int: Updated next_id after adding task
    """
    print("\n--- Add New Task ---")

    # Prompt for title with validation loop
    while True:
        title = input("Enter task title: ").strip()
        if validate_title(title):
            break
        display_message("Title cannot be empty. Please try again.")

    # Prompt for description (optional)
    description = input("Enter task description (press Enter to skip): ").strip()

    # Add task and update next_id
    new_next_id = add_task(tasks, next_id, title, description)

    display_message(f"Task {next_id} added successfully.")
    return new_next_id


def format_task_row(task):
    """
    Format a single task as a table row.

    Args:
        task: Task dictionary

    Returns:
        str: Formatted row string
    """
    task_id = str(task["id"]).ljust(3)
    title = task["title"][:20].ljust(20)  # Truncate long titles
    description = task["description"][:20].ljust(20)  # Truncate long descriptions
    status = "Complete" if task["status"] else "Incomplete"

    return f"{task_id} | {title} | {description} | {status}"


def display_tasks(tasks):
    """
    Print ASCII table with task list or "No tasks found" message.

    Args:
        tasks: List of task dictionaries
    """
    print("\n" + "=" * 70)
    print(" " * 25 + "TODO LIST")
    print("=" * 70)

    if not tasks:
        print("No tasks found. Your todo list is empty.")
    else:
        # Print header
        print("ID  | Title                | Description          | Status")
        print("-" * 70)

        # Print each task
        for task in tasks:
            print(format_task_row(task))

    print("=" * 70)


def handle_view(tasks):
    """
    Handle the 'View Task List' operation.

    Calls display_tasks() to show all tasks.

    Args:
        tasks: List of task dictionaries
    """
    display_tasks(tasks)


def handle_toggle(tasks):
    """
    Handle the 'Mark Task Complete/Incomplete' operation.

    Prompts for task ID, validates, toggles status, displays confirmation.

    Args:
        tasks: List of task dictionaries
    """
    print("\n--- Mark Task Complete/Incomplete ---")

    # Prompt for task ID
    task_id_str = input("Enter task ID: ").strip()
    task_id = validate_integer(task_id_str)

    if task_id is None:
        display_message("Invalid input. Please enter a number.")
        return

    # Toggle status
    new_status = toggle_status(tasks, task_id)

    if new_status is None:
        display_message(f"Task ID {task_id} not found.")
    else:
        status_text = "complete" if new_status else "incomplete"
        display_message(f"Task {task_id} marked as {status_text}.")


def handle_update(tasks):
    """
    Handle the 'Update Task' operation.

    Prompts for task ID and new values, validates, updates task.

    Args:
        tasks: List of task dictionaries
    """
    print("\n--- Update Task ---")

    # Prompt for task ID
    task_id_str = input("Enter task ID: ").strip()
    task_id = validate_integer(task_id_str)

    if task_id is None:
        display_message("Invalid input. Please enter a number.")
        return

    # Check if task exists
    task = find_task_by_id(tasks, task_id)
    if not task:
        display_message(f"Task ID {task_id} not found.")
        return

    # Show current values
    print(f"Current title: {task['title']}")
    print(f"Current description: {task['description']}")

    # Prompt for new title (with option to keep current)
    print("\nEnter new title (press Enter to keep current):")
    new_title = input().strip()
    if not new_title:
        new_title = task['title']  # Keep current
    elif not validate_title(new_title):
        display_message("Title cannot be empty and does not save the changes.")
        return

    # Prompt for new description (with option to keep current)
    print("Enter new description (press Enter to keep current):")
    new_description = input().strip()
    if not new_description and task['description']:
        new_description = task['description']  # Keep current if not provided

    # Update task
    if update_task(tasks, task_id, new_title, new_description):
        display_message(f"Task {task_id} updated successfully.")


def handle_delete(tasks):
    """
    Handle the 'Delete Task' operation.

    Prompts for task ID, validates, deletes task, displays confirmation.

    Args:
        tasks: List of task dictionaries
    """
    print("\n--- Delete Task ---")

    # Prompt for task ID
    task_id_str = input("Enter task ID: ").strip()
    task_id = validate_integer(task_id_str)

    if task_id is None:
        display_message("Invalid input. Please enter a number.")
        return

    # Delete task
    if delete_task(tasks, task_id):
        display_message(f"Task {task_id} deleted successfully.")
    else:
        display_message(f"Task ID {task_id} not found.")


# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

def main():
    """
    Main application loop.

    Displays menu, gets user choice, dispatches to appropriate handler.
    Continues until user selects Exit or presses Ctrl+C.
    """
    global tasks, next_id

    # Display welcome message
    print("\n" + "=" * 54)
    print(" " * 12 + "Welcome to TODO Manager")
    print(" " * 5 + "Phase I: In-Memory Console Application")
    print("=" * 54)
    print("\n⚠️  WARNING: All data will be lost when you exit!")
    print("=" * 54)

    try:
        # Main loop
        while True:
            # Display menu and get choice
            display_menu()
            choice_str = input("\nEnter your choice (1-6): ").strip()

            # Validate menu choice
            choice = validate_menu_choice(choice_str)

            if choice is None:
                # Invalid input handling
                if not choice_str:
                    display_message("Invalid input. Please enter a number.")
                elif validate_integer(choice_str) is None:
                    display_message("Invalid input. Please enter a number.")
                else:
                    display_message("Invalid choice. Please select a number from 1 to 6.")
                continue

            # Dispatch to appropriate handler
            if choice == 1:
                next_id = handle_add(tasks, next_id)
            elif choice == 2:
                handle_view(tasks)
            elif choice == 3:
                handle_update(tasks)
            elif choice == 4:
                handle_delete(tasks)
            elif choice == 5:
                handle_toggle(tasks)
            elif choice == 6:
                # Exit
                print("\n" + "=" * 54)
                print("Exiting... All data will be lost.")
                print("Thank you for using TODO Manager!")
                print("=" * 54 + "\n")
                break

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n" + "=" * 54)
        print("Exiting... All data will be lost.")
        print("Thank you for using TODO Manager!")
        print("=" * 54 + "\n")


if __name__ == "__main__":
    main()
