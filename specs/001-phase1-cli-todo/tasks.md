# Tasks: Phase I CLI Todo Application

**Input**: Design documents from `/specs/001-phase1-cli-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md

**Tests**: No automated tests for Phase I (manual acceptance testing per quickstart.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- All code in single file: `src/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create basic project structure for single-file Python application

- [ ] T001 Create src/ directory in repository root
- [ ] T002 Create empty src/main.py file with Python shebang and module docstring

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Initialize global state (tasks list and next_id counter) in src/main.py
- [ ] T004 Implement validate_integer() function for string-to-int conversion with error handling in src/main.py
- [ ] T005 [P] Implement validate_title() function to check non-empty after strip() in src/main.py
- [ ] T006 [P] Implement validate_menu_choice() function to ensure input is 1-6 in src/main.py
- [ ] T007 [P] Implement display_menu() function to show numbered menu options 1-6 in src/main.py
- [ ] T008 [P] Implement display_message() function to print confirmation/error messages in src/main.py
- [ ] T009 Implement find_task_by_id() helper function for task lookup in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks with title and optional description

**Independent Test**: Launch application, select "Add Task", enter title and description, verify task appears in list with auto-assigned ID and incomplete status

**Spec Reference**: spec.md User Story 1, FR-004 through FR-007, data-model.md add_task()

### Implementation for User Story 1

- [ ] T010 [US1] Implement add_task() function to create task dict, append to list, return incremented next_id in src/main.py
- [ ] T011 [US1] Implement handle_add() function to prompt for title/description, validate title, call add_task(), display confirmation in src/main.py

**Checkpoint**: Users can add tasks with validation. Test acceptance scenarios from spec.md User Story 1.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to see all tasks in a formatted list

**Independent Test**: Add several tasks, select "View Task List", verify all tasks displayed with IDs, titles, descriptions, and statuses

**Spec Reference**: spec.md User Story 2, FR-009 and FR-010, plan.md Display Format

### Implementation for User Story 2

- [ ] T012 [US2] Implement format_task_row() helper function to format single task as table row in src/main.py
- [ ] T013 [US2] Implement display_tasks() function to print ASCII table with headers or "No tasks found" message in src/main.py
- [ ] T014 [US2] Implement handle_view() function to call display_tasks() with tasks list in src/main.py

**Checkpoint**: Users can view task list. MVP complete (US1 + US2). Test acceptance scenarios from spec.md User Story 2.

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Add a task, mark it complete, verify status changes to "complete", mark incomplete again, verify status reverts

**Spec Reference**: spec.md User Story 3, FR-011 through FR-013, data-model.md toggle_status()

### Implementation for User Story 3

- [ ] T015 [US3] Implement toggle_status() function to find task by ID, flip status boolean, return new status in src/main.py
- [ ] T016 [US3] Implement handle_toggle() function to prompt for ID, validate, call toggle_status(), display confirmation in src/main.py

**Checkpoint**: Users can toggle task status. Test acceptance scenarios from spec.md User Story 3.

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P3)

**Goal**: Enable users to modify task title and/or description

**Independent Test**: Add a task, select "Update Task", enter task ID, provide new title/description, verify changes appear in list

**Spec Reference**: spec.md User Story 4, FR-014 and FR-015, data-model.md update_task()

### Implementation for User Story 4

- [ ] T017 [US4] Implement update_task() function to find task by ID, update title/description, return success boolean in src/main.py
- [ ] T018 [US4] Implement handle_update() function to prompt for ID and new values, validate, call update_task(), display confirmation in src/main.py

**Checkpoint**: Users can update tasks. Test acceptance scenarios from spec.md User Story 4.

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Enable users to remove tasks from the list

**Independent Test**: Add several tasks, select "Delete Task", enter task ID, verify task is removed while others remain

**Spec Reference**: spec.md User Story 5, FR-016, data-model.md delete_task()

### Implementation for User Story 5

- [ ] T019 [US5] Implement delete_task() function to find task by ID, remove from list, return success boolean in src/main.py
- [ ] T020 [US5] Implement handle_delete() function to prompt for ID, validate, call delete_task(), display confirmation in src/main.py

**Checkpoint**: Users can delete tasks. All user stories implemented. Test acceptance scenarios from spec.md User Story 5.

---

## Phase 8: Main Application Loop & Exit Flow

**Purpose**: Integrate all handlers into main application loop with menu dispatch and exit handling

**Spec Reference**: FR-001, FR-002, FR-003, FR-018, FR-019, FR-020, plan.md Control Flow Diagram

- [ ] T021 Implement main() function with infinite loop: initialize state, display menu, get choice, dispatch to handler in src/main.py
- [ ] T022 Add menu dispatch logic (if-elif-else) mapping choices 1-6 to handlers (handle_add, handle_view, handle_update, handle_delete, handle_toggle, exit) in src/main.py
- [ ] T023 Add KeyboardInterrupt (Ctrl+C) exception handling in main() to exit gracefully with "Exiting..." message in src/main.py
- [ ] T024 Add if __name__ == "__main__": block to call main() function in src/main.py

**Checkpoint**: Complete application with all features integrated. Test all edge cases from spec.md.

---

## Phase 9: Polish & Validation

**Purpose**: Final validation and edge case handling

- [ ] T025 Test all edge cases from spec.md (non-numeric input, out-of-range menu choice, empty title, invalid IDs, special characters)
- [ ] T026 Verify all error messages match spec.md requirements (exact wording for "Invalid input", "Task ID X not found", "Title cannot be empty")
- [ ] T027 Run through all acceptance scenarios from spec.md for each user story
- [ ] T028 Verify quickstart.md usage examples work as documented
- [ ] T029 Add startup message "Welcome to TODO Manager" and exit message "All data will be lost on exit" in src/main.py

**Checkpoint**: Phase I complete and ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - Can run parallel to US1 if using separate dev branches
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) and US1 (needs tasks to toggle)
- **User Story 4 (Phase 6)**: Depends on Foundational (Phase 2) and US1 (needs tasks to update)
- **User Story 5 (Phase 7)**: Depends on Foundational (Phase 2) and US1 (needs tasks to delete)
- **Main Loop (Phase 8)**: Depends on all user story handlers (Phases 3-7)
- **Polish (Phase 9)**: Depends on Main Loop (Phase 8)

### Task Dependencies Within Phases

**Phase 2 (Foundational)**:
- T003 must complete first (initializes global state)
- T004-T009 can run in parallel (marked [P]) after T003

**Phase 3 (User Story 1)**:
- T010 must complete before T011 (handle_add calls add_task)

**Phase 4 (User Story 2)**:
- T012 and T013 have no dependencies, can run parallel
- T014 depends on T013 (handle_view calls display_tasks)

**Phase 5 (User Story 3)**:
- T015 must complete before T016 (handle_toggle calls toggle_status)

**Phase 6 (User Story 4)**:
- T017 must complete before T018 (handle_update calls update_task)

**Phase 7 (User Story 5)**:
- T019 must complete before T020 (handle_delete calls delete_task)

**Phase 8 (Main Loop)**:
- T021-T024 must run sequentially (build main loop progressively)

**Phase 9 (Polish)**:
- T025-T029 can run in any order, but T029 should be last (final touches)

### Parallel Opportunities

**Within Foundational Phase (after T003)**:
```bash
# Can implement these functions in parallel (different sections of file):
Task T004: validate_integer()
Task T005: validate_title()
Task T006: validate_menu_choice()
Task T007: display_menu()
Task T008: display_message()
Task T009: find_task_by_id()
```

**Note**: Since all code is in one file (src/main.py), true parallel development requires separate branches or careful coordination to avoid merge conflicts.

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T009) - CRITICAL
3. Complete Phase 3: User Story 1 (T010-T011)
4. Complete Phase 4: User Story 2 (T012-T014)
5. Implement minimal main() loop with just options 1, 2, and 6 (Exit)
6. **STOP and VALIDATE**: Test US1 and US2 independently
7. Demo MVP (add tasks and view them)

### Incremental Delivery (Full Phase I)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently (add tasks)
3. Add User Story 2 → Test independently (view tasks) → **MVP Demo**
4. Add User Story 3 → Test independently (toggle status)
5. Add User Story 4 → Test independently (update tasks)
6. Add User Story 5 → Test independently (delete tasks)
7. Integrate all into main loop → Complete Phase 8
8. Final polish and validation → Complete Phase 9

### Single Developer Strategy

For one person working on Phase I:

1. Complete Setup (5 minutes)
2. Complete Foundational functions (30-45 minutes)
3. Implement US1 (Add Task) - 20 minutes
4. Implement US2 (View Tasks) - 30 minutes
5. **Test MVP** (add and view tasks)
6. Implement US3 (Toggle) - 15 minutes
7. Implement US4 (Update) - 20 minutes
8. Implement US5 (Delete) - 15 minutes
9. Integrate main loop - 30 minutes
10. Polish and test all scenarios - 30 minutes

**Total Estimated Time**: 3-4 hours for complete Phase I implementation

---

## Acceptance Testing Checklist

After implementation, verify each acceptance scenario from spec.md:

### User Story 1 - Add Task
- [ ] Add task with title and description → Success with ID assigned
- [ ] Add task with title only (no description) → Success with ID assigned
- [ ] Attempt to add task with empty title → Error "Title cannot be empty"

### User Story 2 - View Tasks
- [ ] View list with 3 tasks → All 3 displayed with correct data
- [ ] View empty list → "No tasks found. Your todo list is empty."
- [ ] View tasks with varying title/description lengths → Readable format

### User Story 3 - Toggle Status
- [ ] Toggle incomplete task (ID 1) → "Task 1 marked as complete"
- [ ] Toggle complete task (ID 2) → "Task 2 marked as incomplete"
- [ ] Toggle with invalid ID (999) → "Task ID 999 not found"

### User Story 4 - Update Task
- [ ] Update task title → "Task 1 updated successfully"
- [ ] Update description only → Title preserved, description changed
- [ ] Update with invalid ID → "Task ID not found"
- [ ] Update with empty title → "Title cannot be empty", no changes saved

### User Story 5 - Delete Task
- [ ] Delete task from middle of list (ID 2) → Task removed, others remain
- [ ] Delete last remaining task → List becomes empty
- [ ] Delete with invalid ID → "Task ID not found"

### Edge Cases
- [ ] Non-numeric menu input → "Invalid input. Please enter a number."
- [ ] Out-of-range menu choice (99) → "Invalid choice. Please select a number from 1 to 6."
- [ ] Special characters in title/description → Accepted and stored
- [ ] Very long title (1000+ chars) → Accepted and stored
- [ ] Exit via option 6 → Clean exit
- [ ] Exit via Ctrl+C → "Exiting..." message, clean exit

### Success Criteria from spec.md
- [ ] SC-001: Add task in <10 seconds
- [ ] SC-002: View list in <1 second
- [ ] SC-003: All 5 operations work without errors
- [ ] SC-004: 100% input validation with clear messages
- [ ] SC-005: Self-explanatory menu (no external docs needed)
- [ ] SC-006: 100% of tasks appear correctly in list
- [ ] SC-007: Status toggles correctly
- [ ] SC-008: Clean exit without errors

---

## Notes

- All tasks modify single file: `src/main.py`
- Total lines of code: ~300-400 (per plan.md estimate)
- No external dependencies, no imports needed (Python standard library)
- IDs are never reused (per data-model.md)
- All data lost on exit (per FR-020)
- Manual acceptance testing only (no automated tests for Phase I)
- Error messages must match exact wording from spec.md
- Task functions should match signatures from data-model.md
- Display format should match ASCII table example from plan.md

---

## Task Completion Tracking

**Total Tasks**: 29
- Setup: 2 tasks (T001-T002)
- Foundational: 7 tasks (T003-T009)
- User Story 1: 2 tasks (T010-T011)
- User Story 2: 3 tasks (T012-T014)
- User Story 3: 2 tasks (T015-T016)
- User Story 4: 2 tasks (T017-T018)
- User Story 5: 2 tasks (T019-T020)
- Main Loop: 4 tasks (T021-T024)
- Polish: 5 tasks (T025-T029)

**MVP Tasks** (US1 + US2): 14 tasks (T001-T014 + minimal main loop)

**Full Phase I**: 29 tasks

---

## Reference Documentation

- **Specification**: `specs/001-phase1-cli-todo/spec.md` (user stories, acceptance scenarios)
- **Implementation Plan**: `specs/001-phase1-cli-todo/plan.md` (architecture, functions, control flow)
- **Data Model**: `specs/001-phase1-cli-todo/data-model.md` (task entity, CRUD operations)
- **Quickstart Guide**: `specs/001-phase1-cli-todo/quickstart.md` (usage examples, testing checklist)
- **Constitution**: `.specify/memory/constitution.md` (Phase I boundaries, no persistence, no external deps)
