---
id: 003
title: Phase 2 Task Breakdown
stage: tasks
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-phase2-fullstack-web
branch: 002-phase2-fullstack-web
user: architect
command: /sp.tasks
labels: ["tasks", "phase2", "breakdown", "user-stories", "mvp", "incremental-delivery"]
links:
  spec: specs/002-phase2-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-phase2-fullstack-web/tasks.md
tests:
 - Manual acceptance testing strategy (automated tests deferred to Phase III)
 - Test user isolation with 2 accounts
 - Test JWT expiry handling
 - Test database connection failures
---

## Prompt

Break the Phase 2 plan into atomic, sequential implementation tasks.

Each task MUST include:
- Task ID (e.g., P2-T1)
- Description
- Preconditions
- Expected output/artifacts
- Reference to spec/plan section

Tasks MUST cover:
1. Monorepo setup and UV configuration
2. Backend: FastAPI project init and dependencies
3. Database connection and SQLModel Task model
4. JWT middleware and user extraction
5. CRUD routers with user_id enforcement
6. Service layer and error handling
7. Frontend: Next.js project init with App Router
8. Better Auth setup with JWT plugin
9. Authentication pages (signin/signup)
10. Task dashboard with list and forms
11. API client with JWT attachment
12. Testing and run instructions

Rules:
- Tasks must be small and testable
- No task introduces agents or future features
- Full coverage of Phase 2 requirements

## Response snapshot

Created comprehensive task breakdown for Phase 2 with 86 atomic tasks organized by user story for independent implementation and testing.

**Task Organization**:

### Phase 1: Setup (9 tasks: T001-T009)
- Monorepo structure (backend/, frontend/)
- .gitignore files for both codebases
- .env example files with required variables
- requirements.txt (Python) and package.json (Node.js)
- README.md files with setup instructions

### Phase 2: Foundational (22 tasks: T010-T031)
**Backend Foundation** (T010-T023):
- Project structure (__init__.py files)
- config.py (Pydantic Settings for env vars)
- database.py (SQLModel engine, session dependency)
- init_db.py (schema initialization script)
- utils/security.py (bcrypt, JWT helpers)
- middleware/cors.py (CORS config)
- middleware/errors.py (global error handler)
- main.py (FastAPI app skeleton)

**Frontend Foundation** (T024-T031):
- Next.js initialization with TypeScript + Tailwind
- lib/types.ts (TypeScript interfaces)
- lib/auth.ts (Better Auth config)
- lib/api-client.ts (fetch wrapper with JWT)
- app/layout.tsx (root layout)
- app/globals.css (Tailwind imports)
- app/api/auth/[...better-auth]/route.ts (Better Auth routes)

### Phase 3: User Story 1 - Authentication (14 tasks: T032-T045) 🎯 MVP
**Backend** (T032-T039):
- models/user.py (User SQLModel)
- schemas/user.py (UserCreate, UserResponse)
- services/auth.py (JWT sign/verify/decode)
- services/user.py (create user, validate credentials)
- middleware/jwt.py (get_current_user dependency)
- routers/auth.py (signup, signin, logout endpoints)
- Register auth router in main.py
- Update init_db.py for User table

**Frontend** (T040-T045):
- app/signup/page.tsx (signup form)
- app/signin/page.tsx (signin form)
- components/Header.tsx (logout button)
- Update app/layout.tsx (Better Auth provider)
- app/page.tsx (landing page with redirect logic)
- app/dashboard/layout.tsx (protected layout)

**Why MVP**: Authentication is foundational for all other stories; enables multi-user isolation

### Phase 4: User Story 2 - Add Task (8 tasks: T046-T053) 🎯 MVP
**Backend** (T046-T051):
- models/task.py (Task SQLModel with user_id FK)
- schemas/task.py (TaskCreate, TaskResponse, TaskUpdate)
- services/task.py (create_task with user_id)
- routers/tasks.py (POST /api/tasks endpoint)
- Register tasks router in main.py
- Update init_db.py for Task table

**Frontend** (T052-T053):
- components/TaskForm.tsx (add task form)
- app/dashboard/page.tsx (dashboard with form)

**Why MVP**: Task creation is core value proposition; without this, app has no purpose beyond auth

### Phase 5: User Story 3 - View Task List (6 tasks: T054-T059) 🎯 MVP
**Backend** (T054-T055):
- Add list_tasks to services/task.py (filter by user_id, order by created_at DESC)
- Add GET /api/tasks endpoint to routers/tasks.py

**Frontend** (T056-T059):
- components/TaskItem.tsx (single task display)
- components/TaskList.tsx (map tasks to TaskItem)
- components/EmptyState.tsx ("No tasks yet" message)
- Update app/dashboard/page.tsx (fetch + display tasks)

**Why MVP**: Viewing tasks is equally critical as creating them; completes basic CRUD cycle

**MVP Complete at T059**: Users can sign up, sign in, create tasks, view tasks - core functionality delivered!

### Phase 6: User Story 4 - Toggle Status (3 tasks: T060-T062) - Priority P2
**Backend** (T060-T061):
- Add toggle_status to services/task.py
- Add PATCH /api/tasks/{id}/complete endpoint

**Frontend** (T062):
- Update components/TaskItem.tsx (checkbox with toggle handler)

### Phase 7: User Story 5 - Update Task (3 tasks: T063-T066) - Priority P3
**Backend** (T063-T064):
- Add update_task to services/task.py
- Add PUT /api/tasks/{id} endpoint

**Frontend** (T065-T066):
- Update components/TaskForm.tsx (edit mode)
- Update components/TaskItem.tsx (edit button)

### Phase 8: User Story 6 - Delete Task (3 tasks: T067-T069) - Priority P3
**Backend** (T067-T068):
- Add delete_task to services/task.py
- Add DELETE /api/tasks/{id} endpoint

**Frontend** (T069):
- Update components/TaskItem.tsx (delete button)

### Phase 9: Polish & Cross-Cutting (17 tasks: T070-T086)
**Backend Polish** (T070-T073):
- tests/README.md (note automated tests deferred)
- Structured logging (task operations, user operations)
- GET /api/tasks/{id} endpoint (view single task)

**Frontend Polish** (T074-T078):
- tests/README.md (note automated tests deferred)
- Loading states (forms, buttons, spinners)
- Error toasts/notifications
- Responsive design testing (320px-1920px)

**Documentation & Validation** (T079-T086):
- Update root README.md
- Validate quickstart.md instructions
- Run manual acceptance testing (all 6 user stories)
- Test user isolation (2 accounts)
- Test JWT expiry, database failures
- Generate Neon connection string
- Generate BETTER_AUTH_SECRET

**Key Statistics**:
- **Total Tasks**: 86
- **MVP Tasks**: 59 (T001-T059: Setup + Foundational + US1 + US2 + US3)
- **Parallel Opportunities**: 35+ tasks marked [P] (different files, no dependencies)
- **User Stories**: 6 (US1-US6 mapped to tasks)
- **Estimated MVP Timeline**: 2-3 weeks single developer, 1-2 weeks pair
- **Phase II Completion**: 3-4 weeks total

**Task Format Compliance**:
✅ All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ Task IDs sequential (T001-T086)
✅ [P] markers for parallelizable tasks (35+ tasks)
✅ [Story] labels for user story tasks (US1-US6)
✅ Exact file paths in all task descriptions

**Dependencies**:
- Setup (Phase 1) → Foundational (Phase 2) → User Story 1 → {US2 + US3 in parallel} → {US4 + US5 + US6 in parallel} → Polish
- **Critical Path**: Setup → Foundational → US1 (auth blocks all) → US2+US3 (MVP) → US4/US5/US6 (features) → Polish

**Parallel Execution Examples**:
- Phase 1: T002-T009 can all run in parallel (different files)
- Phase 2: Backend (T010-T023) parallel with Frontend (T024-T031)
- US1: Backend (T032-T039) parallel with Frontend (T040-T045)
- After US1: US2 + US3 can start in parallel
- After US3: US4 + US5 + US6 can all run in parallel

**Implementation Strategies**:
1. **MVP First**: T001-T059 (Setup + Foundational + US1 + US2 + US3) = Core authentication and task management
2. **Incremental Delivery**: Add US4, US5, US6 one at a time after MVP validation
3. **Parallel Team**: Split backend/frontend work within each user story after Foundational completes

**Independent Test Criteria per Story**:
- **US1**: Sign up → sign in → access dashboard → logout → redirected to signin
- **US2**: Sign in → add task with title → task appears in list
- **US3**: Sign in → view existing tasks → refresh page → tasks persist
- **US4**: Toggle task checkbox → status changes with visual indicator
- **US5**: Click edit → modify title/description → save → changes appear
- **US6**: Click delete → confirm → task removed from list

**Security Enforcement**:
- Every backend service method filters by user_id from JWT (no URL tampering)
- JWT in httpOnly cookies (XSS-safe)
- CORS configured for Next.js origin (localhost:3000 in dev)
- Better Auth handles password hashing (bcrypt cost factor 12)

**Phase II Boundaries Respected**:
- ❌ No agents or MCP integration
- ❌ No automated tests (deferred to Phase III per constitution)
- ❌ No advanced todo features (priorities, due dates, tags)
- ✅ Manual acceptance testing per quickstart.md
- ✅ All tasks map to Phase II requirements from spec.md

## Outcome

- ✅ Impact: Phase 2 task breakdown complete with 86 atomic, testable tasks organized by user story. MVP defined as first 59 tasks (Setup + Foundational + US1 + US2 + US3). Ready for `/sp.implement` execution.
- 🧪 Tests: Manual acceptance testing strategy with independent test criteria for each user story. Automated tests explicitly deferred to Phase III per constitution.
- 📁 Files: 1 file created (tasks.md) with 86 tasks, dependency graph, parallel execution examples, and 3 implementation strategies (MVP first, incremental delivery, parallel team).
- 🔁 Next prompts: `/sp.implement` to execute tasks in dependency order, starting with Setup (Phase 1) then Foundational (Phase 2) then MVP (US1 + US2 + US3).
- 🧠 Reflection: Successfully decomposed plan into granular tasks while maintaining user story independence. Each story can be implemented, tested, and delivered as a complete increment. MVP is clearly defined (authentication + add task + view tasks) and can be validated after T059. Tasks strictly follow format requirements (checkbox + ID + optional [P] + optional [Story] + file path). Security considerations embedded in every backend task (user_id filtering from JWT). No Phase III features leaked (automated tests, advanced features). Task count (86) is comprehensive yet manageable, with clear checkpoints after each user story for independent validation.

## Evaluation notes (flywheel)

- Failure modes observed: None. Task generation completed without clarifications or format violations.
- Graders run and results (PASS/FAIL): Format validation - PASS (all 86 tasks follow checklist format with IDs, labels, file paths)
- Prompt variant (if applicable): Standard /sp.tasks workflow with explicit coverage requirements and user story organization mandate
- Next experiment (smallest change to try): Proceed to `/sp.implement` to execute tasks. Validate that implementation follows exact file paths, respects user story independence, and enables checkpoints after each story for manual testing. Monitor if tasks are granular enough (no task should take >2 hours). If tasks too large, break down further during implementation. Verify parallel opportunities are actually utilized (backend/frontend work should proceed simultaneously within each story).
