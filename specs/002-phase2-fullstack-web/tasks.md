# Tasks: Phase II Full-Stack Web Todo Application

**Input**: Design documents from `/specs/002-phase2-fullstack-web/`
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅), quickstart.md (✅)

**Tests**: Automated tests are DEFERRED to Phase III per constitution. Phase II uses manual acceptance testing documented in quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Monorepo structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Monorepo initialization and basic structure

- [x] T001 Create monorepo directory structure: backend/, frontend/, specs/ (already exists), history/ (already exists)
- [x] T002 Create backend/.gitignore (ignore venv/, __pycache__/, .env, *.pyc)
- [x] T003 [P] Create frontend/.gitignore (ignore node_modules/, .next/, .env.local, dist/)
- [x] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS placeholders
- [x] T005 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET placeholders
- [x] T006 Create backend/requirements.txt with fastapi, uvicorn[standard], sqlmodel, psycopg2-binary, pyjwt, bcrypt, python-multipart, pydantic-settings
- [x] T007 [P] Create frontend/package.json with next@16, react@19, react-dom@19, better-auth, typescript, tailwindcss, @types/node, @types/react
- [x] T008 [P] Create backend/README.md with setup and run instructions from quickstart.md
- [x] T009 [P] Create frontend/README.md with setup and run instructions from quickstart.md

**Checkpoint**: ✅ Repository structure ready for backend and frontend development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T010 Create backend/src/__init__.py (empty marker file)
- [x] T011 Create backend/src/config.py (Pydantic Settings: DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS from env)
- [x] T012 Create backend/src/database.py (SQLModel engine, get_db session dependency)
- [x] T013 Create backend/src/init_db.py (script to run SQLModel.metadata.create_all on app startup)
- [x] T014 Create backend/src/models/__init__.py (export User, Task models)
- [x] T015 Create backend/src/schemas/__init__.py (export Pydantic schemas)
- [x] T016 Create backend/src/services/__init__.py (export services)
- [x] T017 Create backend/src/routers/__init__.py (export routers)
- [x] T018 Create backend/src/middleware/__init__.py (export middleware)
- [x] T019 Create backend/src/utils/__init__.py (export utility functions)
- [x] T020 Create backend/src/utils/security.py (bcrypt hash/verify password, JWT encode/decode helpers)
- [x] T021 Create backend/src/middleware/cors.py (CORS configuration with ALLOWED_ORIGINS, allow_credentials=True)
- [x] T022 Create backend/src/middleware/errors.py (global HTTPException → JSON error response handler)
- [x] T023 Create backend/src/main.py FastAPI app skeleton (lifespan event for init_db, register CORS and error middleware, include routers)

### Frontend Foundation

- [x] T024 Initialize Next.js project: npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir
- [x] T025 Create frontend/lib/types.ts (TypeScript interfaces: User, Task, TaskCreate, TaskUpdate, ApiResponse, ApiError)
- [x] T026 Create frontend/tailwind.config.js (configure Tailwind CSS, extend theme if needed)
- [x] T027 Create frontend/app/globals.css (Tailwind imports: @tailwind base, components, utilities)
- [x] T028 Create frontend/app/layout.tsx (root layout with <html>, <body>, global styles, Better Auth provider setup placeholder)
- [x] T029 Create frontend/lib/auth.ts (Better Auth configuration: JWT plugin, httpOnly cookie, BETTER_AUTH_SECRET)
- [x] T030 Create frontend/lib/api-client.ts (fetch wrapper that extracts JWT from cookie, attaches to Authorization header, handles errors)
- [x] T031 Create frontend/app/api/auth/[...better-auth]/route.ts (Better Auth catch-all API route for signup/signin/logout)

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, sign in, sign out, and access protected routes with JWT authentication

**Independent Test**: Visit signup page → create account → sign in → redirected to dashboard → logout → redirected to signin (manual testing per quickstart.md)

**Why MVP**: Authentication is the foundation for all other user stories. Without it, multi-user task isolation cannot be enforced.

### Backend: User Model & Authentication

- [x] T032 [P] [US1] Create backend/src/models/user.py (User SQLModel: id UUID PK, email unique indexed, password_hash, created_at)
- [x] T033 [US1] Create backend/src/schemas/user.py (UserCreate with email + password, UserResponse with id + email + created_at, exclude password_hash)
- [x] T034 [US1] Create backend/src/services/auth.py (AuthService: sign_jwt, verify_jwt, decode_jwt with BETTER_AUTH_SECRET)
- [x] T035 [US1] Create backend/src/services/user.py (UserService: create_user with bcrypt hashing, get_user_by_email, validate credentials)
- [x] T036 [US1] Create backend/src/middleware/jwt.py (JWT verification middleware: get_current_user dependency extracts user_id from JWT)
- [x] T037 [US1] Create backend/src/routers/auth.py (POST /api/auth/signup → UserService.create_user; POST /api/auth/signin → validate + AuthService.sign_jwt; POST /api/auth/logout → clear session)
- [x] T038 [US1] Register auth router in backend/src/main.py (app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"]))
- [x] T039 [US1] Update backend/src/init_db.py to create User table on startup

### Frontend: Authentication Pages

- [x] T040 [P] [US1] Create frontend/app/signup/page.tsx (signup form with email + password, Better Auth client signup, redirect to signin on success)
- [x] T041 [P] [US1] Create frontend/app/signin/page.tsx (signin form with email + password, Better Auth client signin, redirect to dashboard on success, display errors)
- [x] T042 [P] [US1] Create frontend/components/Header.tsx (navigation header with logout button, calls Better Auth logout, redirects to signin)
- [x] T043 [US1] Update frontend/app/layout.tsx (integrate Better Auth provider, configure JWT plugin with BETTER_AUTH_SECRET)
- [x] T044 [US1] Create frontend/app/page.tsx (landing page: if authenticated → redirect to /dashboard, else redirect to /signin)
- [x] T045 [US1] Create frontend/app/dashboard/layout.tsx (protected layout: middleware checks auth, redirects unauthenticated to /signin)

**Checkpoint**: ✅ User Story 1 is fully functional - users can sign up, sign in, sign out, and access protected routes

---

## Phase 4: User Story 2 - Add Task (Web Interface) (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create tasks with title and optional description via web form

**Independent Test**: Sign in → click "Add Task" → fill title and description → submit → task appears in list with incomplete status (manual testing per quickstart.md)

**Why MVP**: Task creation is the core value proposition. Without this, the application has no purpose beyond authentication.

### Backend: Task Model & Service

- [x] T046 [P] [US2] Create backend/src/models/task.py (Task SQLModel: id int PK autoincrement, user_id UUID FK to User, title max 500, description max 10000 nullable, status bool default False, created_at, updated_at)
- [x] T047 [US2] Create backend/src/schemas/task.py (TaskCreate with title + description optional, TaskResponse with all fields, TaskUpdate with title + description)
- [x] T048 [US2] Create backend/src/services/task.py (TaskService: create_task with user_id from JWT, validates title non-empty, sets status=False, timestamps auto)
- [x] T049 [US2] Create backend/src/routers/tasks.py (POST /api/tasks → TaskService.create_task, requires JWT via get_current_user dependency, returns 201 Created)
- [x] T050 [US2] Register tasks router in backend/src/main.py (app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)]))
- [x] T051 [US2] Update backend/src/init_db.py to create Task table on startup

### Frontend: Add Task Form

- [x] T052 [P] [US2] Create frontend/components/TaskForm.tsx (Client Component: form with title input, description textarea, submit button, calls POST /api/tasks via api-client, displays success/error)
- [x] T053 [US2] Create frontend/app/dashboard/page.tsx (Server Component: placeholder for task list, include TaskForm component for adding tasks)

**Checkpoint**: ✅ User Stories 1 AND 2 work - users can sign up, sign in, and create tasks

---

## Phase 5: User Story 3 - View Task List (Web Interface) (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can view all their tasks in a web interface with titles, descriptions, and completion status

**Independent Test**: Sign in with account that has tasks → dashboard loads → all tasks displayed with correct data (manual testing per quickstart.md)

**Why MVP**: Viewing tasks is equally critical as creating them. This completes the minimum viable product.

### Backend: List Tasks Endpoint

- [x] T054 [US3] Add list_tasks method to backend/src/services/task.py (TaskService: get all tasks filtered by user_id, ordered by created_at DESC)
- [x] T055 [US3] Add GET /api/tasks endpoint to backend/src/routers/tasks.py (returns TaskService.list_tasks for current user, requires JWT)

### Frontend: Task List Display

- [x] T056 [P] [US3] Create frontend/components/TaskItem.tsx (Client Component: displays single task with title, description, status indicator, edit/delete buttons placeholder)
- [x] T057 [P] [US3] Create frontend/components/TaskList.tsx (Client Component: maps tasks array to TaskItem components, handles empty state)
- [x] T058 [P] [US3] Create frontend/components/EmptyState.tsx (displays "No tasks yet. Create your first task to get started!" message)
- [x] T059 [US3] Update frontend/app/dashboard/page.tsx (Server Component: fetch tasks via GET /api/tasks using api-client, pass to TaskList, display EmptyState if no tasks)

**Checkpoint**: ✅ **MVP COMPLETE!** User Stories 1, 2, AND 3 are functional - users can sign up, sign in, create tasks, and view their task list

---

## Phase 6: User Story 4 - Mark Task Complete or Incomplete (Priority: P2)

**Goal**: Authenticated users can toggle task completion status by clicking a checkbox

**Independent Test**: Sign in → view task list → click checkbox on incomplete task → status changes to complete with visual indicator → click again → reverts to incomplete (manual testing per quickstart.md)

### Backend: Toggle Status Endpoint

- [ ] T060 [US4] Add toggle_status method to backend/src/services/task.py (TaskService: get task by id and user_id, toggle status boolean, update updated_at, return updated task)
- [ ] T061 [US4] Add PATCH /api/tasks/{id}/complete endpoint to backend/src/routers/tasks.py (calls TaskService.toggle_status, returns 200 OK with updated task, 404 if not found or wrong user)

### Frontend: Toggle Task Status

- [ ] T062 [US4] Update frontend/components/TaskItem.tsx (add checkbox input, onChange calls PATCH /api/tasks/{id}/complete, applies strikethrough/checkmark styling when complete, calls router.refresh to re-fetch)

**Checkpoint**: User Story 4 complete - users can toggle task status

---

## Phase 7: User Story 5 - Update Existing Task (Priority: P3)

**Goal**: Authenticated users can edit task title and/or description via inline form or modal

**Independent Test**: Sign in → click "Edit" on a task → modify title or description → save → changes appear immediately (manual testing per quickstart.md)

### Backend: Update Task Endpoint

- [ ] T063 [US5] Add update_task method to backend/src/services/task.py (TaskService: get task by id and user_id, validate title non-empty, update fields, update updated_at, return updated task)
- [ ] T064 [US5] Add PUT /api/tasks/{id} endpoint to backend/src/routers/tasks.py (calls TaskService.update_task with TaskUpdate schema, returns 200 OK, 400 if validation fails, 404 if not found)

### Frontend: Edit Task Form

- [ ] T065 [US5] Update frontend/components/TaskForm.tsx (add editMode prop, if editMode populate initial values, call PUT /api/tasks/{id} instead of POST, emit onSave callback)
- [ ] T066 [US5] Update frontend/components/TaskItem.tsx (add "Edit" button, onClick shows TaskForm in edit mode with current task data, onSave refreshes list)

**Checkpoint**: User Story 5 complete - users can edit tasks

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Authenticated users can permanently delete tasks via delete button with optional confirmation

**Independent Test**: Sign in → click "Delete" on a task → confirm deletion → task removed from list (manual testing per quickstart.md)

### Backend: Delete Task Endpoint

- [ ] T067 [US6] Add delete_task method to backend/src/services/task.py (TaskService: get task by id and user_id, delete from database, return success)
- [ ] T068 [US6] Add DELETE /api/tasks/{id} endpoint to backend/src/routers/tasks.py (calls TaskService.delete_task, returns 204 No Content, 404 if not found)

### Frontend: Delete Task Button

- [ ] T069 [US6] Update frontend/components/TaskItem.tsx (add "Delete" button, onClick calls DELETE /api/tasks/{id}, optionally confirm with window.confirm, calls router.refresh to re-fetch)

**Checkpoint**: User Story 6 complete - users can delete tasks. All 6 user stories from spec.md are now implemented!

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories or finalize the Phase II application

### Backend Polish

- [ ] T070 [P] Create backend/tests/README.md ("Automated tests deferred to Phase III per constitution")
- [ ] T071 [P] Add structured logging to backend/src/services/task.py (log task creation, updates, deletions with user_id)
- [ ] T072 [P] Add structured logging to backend/src/services/user.py (log user creation, login attempts)
- [ ] T073 [P] Add GET /api/tasks/{id} endpoint to backend/src/routers/tasks.py (get single task for viewing, requires JWT and user_id match)

### Frontend Polish

- [ ] T074 [P] Create frontend/tests/README.md ("Automated tests deferred to Phase III per constitution")
- [ ] T075 [P] Add loading states to frontend/components/TaskForm.tsx (disable submit button while saving, show spinner)
- [ ] T076 [P] Add loading states to frontend/components/TaskItem.tsx (disable buttons while toggling/deleting, show spinner)
- [ ] T077 [P] Add error toasts/notifications to frontend/lib/api-client.ts (display user-friendly error messages from API)
- [ ] T078 [P] Add responsive design testing (verify 320px-1920px viewports per SC-005)

### Documentation & Validation

- [ ] T079 Update project root README.md (overview, links to Phase I and Phase II docs, architecture diagram)
- [ ] T080 Validate quickstart.md instructions (follow setup steps, verify all commands work)
- [ ] T081 Run manual acceptance testing per quickstart.md (all 6 user stories, edge cases)
- [ ] T082 Test user isolation (create two users, verify tasks don't leak between accounts)
- [ ] T083 Test JWT expiry handling (wait for token to expire, verify 401 and redirect to signin)
- [ ] T084 Test database connection failure (stop Neon DB, verify graceful error handling)
- [ ] T085 Generate Neon database connection string and add to backend/.env (if not done already)
- [ ] T086 Generate BETTER_AUTH_SECRET and add to both backend/.env and frontend/.env.local (if not done already)

**Final Checkpoint**: Phase II application is complete and validated - ready for demo and Phase III planning

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User Stories 1, 2, 3 (P1) are the MVP - must complete these first
  - User Stories 4, 5, 6 (P2, P3, P3) can be added incrementally after MVP
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (US1 - Auth)**: Can start after Foundational (Phase 2) - BLOCKS all other stories (auth required)
- **User Story 2 (US2 - Add Task)**: Depends on US1 completion (requires authentication) - Independent otherwise
- **User Story 3 (US3 - View Tasks)**: Depends on US1 completion (requires authentication) - Independent otherwise, but builds on US2's task model
- **User Story 4 (US4 - Toggle Status)**: Depends on US1 + US3 (requires auth + task list to display) - Independent otherwise
- **User Story 5 (US5 - Update Task)**: Depends on US1 + US3 (requires auth + task list to display) - Independent otherwise
- **User Story 6 (US6 - Delete Task)**: Depends on US1 + US3 (requires auth + task list to display) - Independent otherwise

### Within Each User Story

- Backend models before backend services
- Backend services before backend routers
- Backend routers registered in main.py
- Frontend lib/types before frontend components
- Frontend components before pages
- Pages integrate components

### Critical Path (Sequential)

1. Setup (Phase 1) → 2. Foundational (Phase 2) → 3. US1 (Auth) → 4. US2 (Add Task) + US3 (View Tasks) → 5. US4, US5, US6 (in any order) → 6. Polish

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T002-T009 can all run in parallel (different files)

**Within Foundational (Phase 2)**:
- T010-T023 (backend) can run in parallel with T024-T031 (frontend)
- Within backend: T014-T022 can run in parallel (different module files)
- Within frontend: T025-T031 can run in parallel (different files)

**Within User Stories**:
- Backend and frontend tasks for the SAME story can run in parallel (different codebases)
- Example US1: T032-T039 (backend) can run in parallel with T040-T045 (frontend)
- Models within a story marked [P] can run in parallel

**Across User Stories** (after US1 completes):
- US2, US3 can start in parallel (different endpoints/pages)
- US4, US5, US6 can all run in parallel (different endpoints/components)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Backend tasks for US1 (can parallelize these):
Task T032 [P]: "Create backend/src/models/user.py"
Task T033: "Create backend/src/schemas/user.py" (waits for T032)
Task T034 [P]: "Create backend/src/services/auth.py"
Task T035: "Create backend/src/services/user.py" (waits for T032)

# Frontend tasks for US1 (can parallelize these):
Task T040 [P]: "Create frontend/app/signup/page.tsx"
Task T041 [P]: "Create frontend/app/signin/page.tsx"
Task T042 [P]: "Create frontend/components/Header.tsx"

# Backend and frontend can run in parallel!
```

---

## Parallel Example: After US1 Completes (MVP Extension)

```bash
# All three can start in parallel (different endpoints/pages):
US2 Team: T046-T053 (Add Task)
US3 Team: T054-T059 (View Task List)

# Once US3 completes, these can all start in parallel:
US4 Team: T060-T062 (Toggle Status)
US5 Team: T063-T066 (Update Task)
US6 Team: T067-T069 (Delete Task)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 3 Only)

1. Complete Phase 1: Setup → T001-T009
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories) → T010-T031
3. Complete Phase 3: User Story 1 (Authentication) → T032-T045
4. Complete Phase 4: User Story 2 (Add Task) → T046-T053
5. Complete Phase 5: User Story 3 (View Task List) → T054-T059
6. **STOP and VALIDATE**: Test authentication, task creation, and task viewing independently per quickstart.md
7. **MVP COMPLETE** - Application is deployable and demonstrates core value

### Incremental Delivery

1. Setup + Foundational → Foundation ready (T001-T031)
2. Add User Story 1 → Test independently → Authentication works (T032-T045)
3. Add User Story 2 → Test independently → Users can add tasks (T046-T053)
4. Add User Story 3 → Test independently → Users can view tasks → **MVP DEMO!** (T054-T059)
5. Add User Story 4 → Test independently → Users can toggle status (T060-T062)
6. Add User Story 5 → Test independently → Users can edit tasks (T063-T066)
7. Add User Story 6 → Test independently → Users can delete tasks (T067-T069)
8. Add Polish → Final validation → **Phase II COMPLETE** (T070-T086)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **Week 1**: Team completes Setup + Foundational together (T001-T031)
2. **Week 2**: Once Foundational is done:
   - Developer A: User Story 1 backend (T032-T039)
   - Developer B: User Story 1 frontend (T040-T045)
   - Integrate and test US1 together
3. **Week 3**: Split again:
   - Developer A: User Story 2 backend + User Story 3 backend (T046-T055)
   - Developer B: User Story 2 frontend + User Story 3 frontend (T052-T059)
   - **MVP DEMO at end of week 3**
4. **Week 4**: Parallel feature development:
   - Developer A: User Story 4 + User Story 5 (T060-T066)
   - Developer B: User Story 6 + Polish (T067-T086)
5. Stories complete and integrate independently

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story**: Independently completable and testable per quickstart.md
- **Automated tests**: Deferred to Phase III per constitution (manual testing in Phase II)
- **Environment setup**: T085-T086 must be done before running the application (generate secrets)
- **Commit strategy**: Commit after each task or logical group (e.g., all US1 backend tasks)
- **Stop at any checkpoint**: Validate story independently before proceeding
- **Phase II boundaries**: No agents, no MCP, no advanced features (priorities, due dates, etc.)
- **Security**: Every task endpoint MUST filter by user_id from JWT (enforced in services)

---

**Total Task Count**: 86 tasks
**MVP Task Count**: 59 tasks (T001-T059: Setup + Foundational + US1 + US2 + US3)
**Estimated MVP Timeline**: 2-3 weeks for single developer, 1-2 weeks for pair
**Phase II Completion**: 3-4 weeks total including all user stories and polish
