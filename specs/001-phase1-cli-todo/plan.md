# Implementation Plan: Phase I CLI Todo Application

**Branch**: `001-phase1-cli-todo` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-cli-todo/spec.md`

## Summary

Phase I delivers a pure in-memory Python console todo application with menu-driven CRUD operations. Users can add, view, update, delete, and toggle completion status of tasks. All data is stored in memory (list of dictionaries) and lost on exit. No persistence, authentication, or external dependencies. The application provides a numbered menu (1-6), validates all inputs, and displays clear error/confirmation messages.

## Technical Context

**Language/Version**: Python 3.11 or higher (no external dependencies required)
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory list of dictionaries (no file or database persistence)
**Testing**: Manual acceptance testing per user stories (no automated test framework for Phase I)
**Target Platform**: Cross-platform console/terminal (Windows, macOS, Linux)
**Project Type**: Single standalone script
**Performance Goals**: Add task <10s, view list <1s (easily achievable with in-memory storage)
**Constraints**: No persistence, no external dependencies, single-user, console-only
**Scale/Scope**: Single Python file (~300-400 lines), suitable for dozens to hundreds of tasks in a session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Boundary Compliance

| Requirement | Status | Verification |
|-------------|--------|--------------|
| CLI-only (no web/API) | ✅ PASS | Console interface with input()/print() only |
| In-memory storage (no database) | ✅ PASS | Python list of dictionaries, no file I/O |
| No persistence | ✅ PASS | Data lost on exit, no save/load operations |
| No authentication | ✅ PASS | Single-user, no login/auth logic |
| No external dependencies | ✅ PASS | Python standard library only |
| No advanced features | ✅ PASS | Basic CRUD only, no priorities/filters/due dates |
| Python backend | ✅ PASS | Python 3.11+ as specified in constitution |

### Cloud-Native Principles (Phase I Interpretation)

| Principle | Status | Phase I Application |
|-----------|--------|---------------------|
| Modularity | ✅ PASS | Separate functions for display, validation, CRUD operations |
| Statelessness | ⚠️ DEFERRED | Phase I is inherently stateful (in-memory session); externalization starts Phase IV |
| Separation of Concerns | ✅ PASS | Display logic, business logic, and data operations separated into distinct functions |
| Cloud Readiness | ⚠️ DEFERRED | Containerization and observability deferred to Phase V; Phase I establishes clean foundation |

**Overall Constitution Compliance**: ✅ PASS - All Phase I boundaries respected, no violations

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-cli-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (minimal for Phase I - no research needed)
├── data-model.md        # Phase 1 output (Task entity structure)
├── quickstart.md        # Phase 1 output (how to run the application)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
└── main.py              # Single-file application containing all logic

# NO tests/ directory for Phase I
# Testing via manual acceptance scenarios per spec
```

**Structure Decision**: Single-file architecture chosen for Phase I simplicity. The application is self-contained in `src/main.py` with approximately 300-400 lines of code. This aligns with Phase I constraints (no external dependencies, no complexity) while establishing a clear foundation that can be refactored into modules in Phase II when API layer is introduced.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All constitution requirements satisfied.*

---

## Phase 0: Research & Technical Decisions

### Research Summary

**Decision: Single-file Python script with standard library only**

**Rationale**:
- Phase I explicitly prohibits external dependencies
- Task count will be modest (dozens to hundreds per session)
- In-memory list of dictionaries provides O(n) search, acceptable for Phase I scale
- No performance optimization needed for console application with <1000 tasks
- Single file simplifies deployment (just run `python main.py`)

**Alternatives Considered**:
1. **Multi-file modular structure**: Rejected - premature for Phase I; refactor in Phase II when adding API layer
2. **External libraries (click, rich, prompt_toolkit)**: Rejected - violates Phase I "no external dependencies" constraint
3. **Classes vs functions**: Decision - use functions for simplicity; introduce classes in Phase II for API serialization

**No further research required** - Phase I scope is fully specified and uses only Python standard library.

---

## Phase 1: Data Model & Architecture

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Summary**:

**Task Entity** (in-memory dictionary representation):
```python
{
    "id": int,          # Auto-incremented, starts at 1, never reused
    "title": str,       # Non-empty string (validated)
    "description": str, # Optional string (can be empty)
    "status": bool      # True = complete, False = incomplete (default)
}
```

**Global State**:
- `tasks`: List of task dictionaries (in-memory storage)
- `next_id`: Integer counter for ID assignment (increments on each add, never decrements)

### Architecture Design

#### Module Responsibility Breakdown

**Display Layer** (Console I/O):
- `display_menu()` - Show numbered menu options 1-6
- `display_tasks(tasks)` - Format and print task list
- `display_message(message)` - Print confirmation/error messages
- `get_input(prompt)` - Wrapper for input() with prompt

**Validation Layer**:
- `validate_menu_choice(choice)` - Ensure input is 1-6
- `validate_task_id(task_id, tasks)` - Check ID exists
- `validate_title(title)` - Ensure non-empty after strip()
- `validate_integer(value)` - Convert string to int, handle ValueError

**Business Logic Layer** (CRUD Operations):
- `add_task(tasks, next_id, title, description)` - Create new task, return updated next_id
- `view_tasks(tasks)` - Return task list (delegate formatting to display layer)
- `update_task(tasks, task_id, new_title, new_description)` - Modify existing task
- `delete_task(tasks, task_id)` - Remove task from list
- `toggle_status(tasks, task_id)` - Flip boolean status

**Control Flow**:
- `main()` - Main loop: display menu → get choice → dispatch to handler → repeat until exit
- `handle_add()` - Prompt for title/description, validate, call add_task()
- `handle_view()` - Call view_tasks(), format with display_tasks()
- `handle_update()` - Prompt for ID and new values, validate, call update_task()
- `handle_delete()` - Prompt for ID, validate, call delete_task()
- `handle_toggle()` - Prompt for ID, validate, call toggle_status()

#### Control Flow Diagram

```text
┌─────────────────────────────────────────────┐
│              START (main)                   │
│  Initialize: tasks = [], next_id = 1       │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Display Menu (1-6)  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Get User Choice     │
        │   (input validation)  │
        └───────────┬───────────┘
                    │
        ┌───────────┴────────────┬──────────┬───────────┬──────────┬──────────┐
        │                        │          │           │          │          │
        ▼                        ▼          ▼           ▼          ▼          ▼
    [1] Add Task          [2] View     [3] Update  [4] Delete [5] Toggle [6] Exit
        │                      │           │           │          │          │
        ▼                      ▼           ▼           ▼          ▼          ▼
  ┌─────────────┐     ┌────────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐   EXIT
  │Prompt title │     │Display all │ │Prompt ID│ │Prompt ID│ │Prompt│    ↓
  │& desc       │     │tasks       │ │& new    │ │Validate │ │ID    │   End
  │Validate     │     │            │ │values   │ │Delete   │ │Toggle│
  │Add to list  │     │            │ │Validate │ │         │ │status│
  │Confirm      │     │            │ │Update   │ │Confirm  │ │      │
  └──────┬──────┘     └──────┬─────┘ └────┬────┘ └────┬────┘ └──┬───┘
         │                   │            │           │         │
         └───────────────────┴────────────┴───────────┴─────────┘
                             │
                             ▼
                    Return to Menu (loop)
```

#### Error Handling Strategy

**Input Validation**:
- Wrap `input()` calls in try-except for KeyboardInterrupt (Ctrl+C)
- Validate menu choice: catch non-numeric, out-of-range → display error, re-prompt
- Validate task ID: catch non-numeric, non-existent ID → display error, return to menu
- Validate title: strip whitespace, check non-empty → display error, re-prompt

**Error Message Format**:
- Invalid input: `"Invalid input. Please enter a number."`
- Invalid choice: `"Invalid choice. Please select a number from 1 to 6."`
- Task not found: `"Task ID {id} not found."`
- Empty title: `"Title cannot be empty."`

**Graceful Exit**:
- Menu option 6: Clean exit (no data saved, as per Phase I spec)
- Ctrl+C: Catch KeyboardInterrupt, display "Exiting...", exit cleanly

### Contracts

*No API contracts for Phase I* - Console application with no external interfaces. Phase II will introduce REST API contracts when FastAPI is added.

**Console Interface Contract** (informal):

**Menu Options**:
```
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit
```

**Input/Output Examples**:

```
Add Task:
  Input: title (string), description (string, optional)
  Output: "Task {id} added successfully."

View Task List:
  Input: none
  Output: Formatted list or "No tasks found. Your todo list is empty."

Update Task:
  Input: task_id (int), new_title (string), new_description (string)
  Output: "Task {id} updated successfully."

Delete Task:
  Input: task_id (int)
  Output: "Task {id} deleted successfully."

Toggle Status:
  Input: task_id (int)
  Output: "Task {id} marked as complete." or "Task {id} marked as incomplete."

Exit:
  Input: menu choice 6
  Output: Application terminates
```

### Quickstart Guide

See [quickstart.md](./quickstart.md) for step-by-step usage instructions.

---

## Implementation Notes

### ID Assignment Approach

**Strategy**: Monotonically increasing counter starting at 1.

```python
next_id = 1  # Global counter
tasks = []   # Global task list

def add_task(tasks, next_id, title, description):
    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip(),
        "status": False
    }
    tasks.append(task)
    return next_id + 1  # Increment for next task
```

**Important**: IDs are never reused, even after deletion. If task ID 5 is deleted, the next added task gets ID 6, not 5. This prevents confusion and maintains audit trail within a session.

### Task Lookup

**Strategy**: Linear search through list.

```python
def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None  # Not found
```

**Performance**: O(n) search is acceptable for Phase I scale (dozens to hundreds of tasks per session). Phase II may introduce dictionary-based lookup (O(1)) if needed.

### Display Format

**Task List Display**:
```
==================== TODO LIST ====================
ID | Title                | Description           | Status
---+----------------------+-----------------------+-----------
1  | Buy groceries        | Milk, eggs, bread     | Incomplete
2  | Call dentist         |                       | Complete
3  | Submit report        | Quarterly analysis    | Incomplete
===================================================
```

### Input Prompts

**Clear, explicit prompts**:
- "Enter task title: "
- "Enter task description (press Enter to skip): "
- "Enter task ID: "
- "Enter new title (press Enter to keep current): "

### Phase I Simplification Decisions

**Decisions made to keep Phase I simple**:

1. **No configuration**: Hardcoded prompts and messages (no i18n, no customization)
2. **No logging**: Print statements only for user-facing output (no debug logs, no file logging)
3. **No tests directory**: Manual acceptance testing per spec scenarios (automated tests deferred to Phase II)
4. **No error logging**: Display errors to console, don't persist
5. **No undo/history**: Each operation is final within the session
6. **No data validation beyond empty check**: Accept all printable characters in title/description
7. **No pagination**: Display all tasks in one output (acceptable for expected scale)

---

## Post-Design Constitution Check

### Re-evaluation After Architecture Design

| Requirement | Status | Verification |
|-------------|--------|--------------|
| Phase I boundaries (CLI, in-memory, no persistence) | ✅ PASS | Architecture uses only Python standard library, list storage, console I/O |
| No external dependencies | ✅ PASS | Confirmed - no imports beyond Python standard library |
| Modularity (functions for separation of concerns) | ✅ PASS | Display, validation, CRUD, and control flow separated into distinct functions |
| No features beyond specification | ✅ PASS | Architecture implements exactly what spec requires, no additions |

**Final Verdict**: ✅ Architecture fully compliant with Constitution and Phase I boundaries

---

## Next Steps

1. **Review this plan** - Human approval required before proceeding
2. **Run `/sp.tasks`** - Generate dependency-ordered task list from this plan
3. **Run `/sp.implement`** - Execute tasks and generate code
4. **Manual acceptance testing** - Verify each user story acceptance scenario from spec.md

## Architectural Decisions for ADR Consideration

Applying the three-part ADR test:

**Decision: Single-file Python script vs modular structure**
- **Impact**: Long-term? No - Phase II will refactor when adding API layer
- **Alternatives**: Multiple files considered but rejected for Phase I simplicity
- **Scope**: Cross-cutting? No - local to Phase I implementation

**Verdict**: No ADR needed - decision is Phase I-specific and will be revisited in Phase II

**Decision: List of dictionaries vs custom class for Task**
- **Impact**: Long-term? No - Phase II will introduce proper data models for API serialization
- **Alternatives**: Class-based approach considered but rejected for Phase I simplicity
- **Scope**: Cross-cutting? No - local to Phase I implementation

**Verdict**: No ADR needed - decision is Phase I-specific and will be revisited in Phase II

*No architecturally significant decisions requiring ADR at Phase I level. Phase II API architecture will require ADRs for API design, authentication approach, and database schema.*
