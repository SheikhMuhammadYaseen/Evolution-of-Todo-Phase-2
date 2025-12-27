---
id: 002
title: Phase 2 Implementation Plan
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-phase2-fullstack-web
branch: 002-phase2-fullstack-web
user: architect
command: /sp.plan
labels: ["plan", "phase2", "fullstack", "architecture", "monorepo", "fastapi", "nextjs", "better-auth", "neon-db"]
links:
  spec: specs/002-phase2-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-phase2-fullstack-web/plan.md
 - specs/002-phase2-fullstack-web/research.md
 - specs/002-phase2-fullstack-web/data-model.md
 - specs/002-phase2-fullstack-web/quickstart.md
 - specs/002-phase2-fullstack-web/contracts/api-spec.yaml
tests:
 - Manual acceptance testing strategy documented in quickstart.md
 - Automated tests deferred to Phase III
---

## Prompt

Create the Phase 2 technical plan

Plan MUST cover:
1. Monorepo structure
   - /frontend (Next.js app)
   - /backend (FastAPI app)
   - /specs folder with organized specifications

2. Backend architecture
   - FastAPI main app
   - SQLModel models (Task with user_id foreign key)
   - Dependency injection for database session
   - JWT verification middleware
   - Routers scoped to the authenticated user
   - user_id is extracted from JWT claims on the backend (not passed in URL)
   - Service layer for business logic

3. Frontend architecture
   - Next.js App Router
   - Better Auth integration with JWT plugin
   - API client that attaches JWT to every request
   - Pages: login, signup, dashboard with task list and forms

4. Authentication flow
   - Shared BETTER_AUTH_SECRET
   - JWT issuance on login
   - Token attachment in Authorization: Bearer header
   - Backend extraction and user validation

5. Database
   - Neon Serverless PostgreSQL connection
   - Initial schema managed via SQLModel metadata
   - No versioned or incremental migrations required in Phase 2

6. Evolution from Phase 1
   - Conceptual reuse of CRUD logic
   - Replacement of in-memory storage with database

Constraints:
- No agents or MCP
- No extra features beyond basic CRUD + auth

## Response snapshot

Created comprehensive Phase 2 implementation plan with full architecture and design decisions.

**Key Sections Completed**:

### 1. Technical Context
- **Languages**: Python 3.11 (backend), TypeScript 5.x (frontend)
- **Dependencies**: FastAPI, SQLModel, PyJWT, psycopg2-binary, uvicorn (backend); Next.js 16+, React 19, Better Auth, Tailwind CSS (frontend)
- **Database**: Neon Serverless PostgreSQL
- **Testing**: Manual acceptance testing (automated tests deferred to Phase III)
- **Performance Goals**: <1s API responses, <5s dashboard load, <3min registration to first task
- **Scale**: 1-100 users, up to 1,000 tasks per user, ~50 MB database

### 2. Constitution Check
- ✅ **Phase Boundary Compliance**: All Phase II requirements met, no Phase III+ features
- ✅ **Technology Stack Compliance**: Python, FastAPI, SQLModel, Neon DB, Next.js, Better Auth all approved
- ✅ **Cloud-Native Compliance**: Stateless design, modular architecture, environment-based config
- ✅ **Agent Rules Compliance**: No unsolicited features, specification adherence strict
- **Verdict**: GATE PASSED - No constitution violations

### 3. Project Structure
- **Monorepo Layout**: `/backend` (FastAPI), `/frontend` (Next.js), `/specs` (documentation)
- **Backend Structure**:
  - `src/models/` - SQLModel entities (User, Task)
  - `src/schemas/` - Pydantic request/response schemas
  - `src/services/` - Business logic (auth, user, task services)
  - `src/routers/` - API endpoints (auth, tasks routes)
  - `src/middleware/` - JWT verification, CORS, error handling
  - `src/utils/` - Security helpers (bcrypt, JWT utilities)
- **Frontend Structure**:
  - `app/` - Next.js App Router pages (signup, signin, dashboard)
  - `components/` - React components (TaskList, TaskItem, TaskForm)
  - `lib/` - Better Auth config, API client, TypeScript types
  - `styles/` - Tailwind CSS global styles

### 4. Phase 0: Research (research.md)
**10 Key Decisions**:
1. Monorepo structure (vs. separate repos or single /src)
2. Service layer backend (vs. repository pattern or DDD)
3. httpOnly cookies for JWT (vs. localStorage/sessionStorage) - XSS protection
4. API design: `/api/tasks` with user_id from JWT (vs. `/api/{user_id}/tasks` in URL) - security
5. SQLModel metadata schema (vs. Alembic migrations from start)
6. Server Components + fetch (vs. React Query or Redux)
7. Consistent JSON error responses with status codes
8. CORS configured on FastAPI for Next.js origin
9. Separate dev servers with environment variables (vs. Docker Compose)
10. Manual acceptance testing (vs. TDD from start)

**Rationale**: Each decision documented with alternatives considered, tradeoffs, and rejection reasons. All decisions prioritize security, simplicity, and Phase II scope boundaries.

### 5. Phase 1: Design Artifacts

**Data Model** (data-model.md):
- **User**: id (UUID PK), email (unique), password_hash, created_at
- **Task**: id (int PK), user_id (FK → User), title, description, status (boolean), created_at, updated_at
- **Relationships**: One-to-Many (User → Tasks), cascade delete
- **Indexes**: email (unique), user_id (FK), (user_id, created_at DESC) composite
- **Evolution from Phase I**: Added user_id, timestamps, PostgreSQL persistence

**API Contracts** (contracts/api-spec.yaml - OpenAPI 3.0):
- `GET /api/tasks` - List all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get single task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle status
- **Auth**: JWT in Authorization: Bearer header (all endpoints)
- **Errors**: JSON format with code, message, details

**Quickstart Guide** (quickstart.md):
- Prerequisites: Node.js 20+, Python 3.11+, Neon database
- Backend setup: venv, pip install, .env config, schema init, uvicorn server
- Frontend setup: npm install, .env.local config, dev server
- First-time usage: signup, signin, CRUD operations
- Manual acceptance testing: 6 user stories from spec.md with scenarios
- Troubleshooting: Common issues and solutions
- API testing: curl examples for all endpoints

### 6. Architecture Decisions (7 major decisions documented)

1. **Monorepo vs. Separate Repos** → Monorepo (coordination, shared docs)
2. **Service Layer vs. Repository** → Service Layer (simplicity, Phase II scope)
3. **JWT Storage** → httpOnly Cookies (XSS-safe, OWASP best practice)
4. **API Endpoint Design** → user_id from JWT (security, no URL tampering)
5. **Database Migrations** → Metadata-driven (greenfield, no evolution yet)
6. **Frontend State** → Server Components (performance, simplicity)
7. **Authentication** → Better Auth (security, time savings)

Each decision includes: rationale, tradeoffs (pros/cons), alternatives considered, rejection reasons.

### 7. Implementation Phases

- **Phase 0: Research** ✅ Completed
- **Phase 1: Design** ✅ Completed
- **Phase 2: Task Decomposition** → Next step (`/sp.tasks`)
- **Phase 3: Implementation** → Final step (`/sp.implement`)

**Task Groups Preview**:
1. Setup (US0) - Monorepo structure, environment files, dependencies
2. Backend Foundation (US0) - Models, config, middleware
3. Authentication (US1) - User service, auth router, JWT middleware
4. Task CRUD (US2-6) - Task service, task router, all endpoints
5. Frontend Foundation (US0) - Next.js setup, Better Auth, API client
6. Frontend UI (US1-6) - Auth pages, dashboard, components
7. Integration Testing (US7) - Manual acceptance testing

### 8. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth misconfiguration | High | Follow docs, test early, verify shared secret |
| CORS issues | Medium | Configure before frontend dev, test preflight |
| Database connection failures | High | Validate URL early, handle errors, log |
| JWT expiry during testing | Low | 24-hour expiry, document in guide |
| User isolation bug | Critical | Test explicitly, review every query filter |
| Task list performance | Medium | Index on (user_id, created_at), test large datasets |

**Critical Path**: Backend auth (US1) → Frontend auth (US1 frontend) | Backend CRUD (US2-6) → Frontend UI (US2-6)

### 9. Success Criteria Alignment

All 12 Success Criteria from spec.md mapped to implementation:
- SC-001 (<3 min registration): Quickstart guide documents flow
- SC-002 (<5 sec signin): Server Components optimize load
- SC-003 (100% isolation): user_id filter enforced in every query
- SC-004 (<1s API response): FastAPI performance, indexed queries
- SC-005 (320px-1920px responsive): Tailwind CSS mobile-first
- SC-006 (no docs needed): Intuitive UI design
- SC-007 (100% unauthorized rejection): JWT middleware validation
- SC-008 (data persists): PostgreSQL ensures persistence
- SC-009 (graceful errors): Consistent JSON error responses
- SC-010 (99% uptime): FastAPI + Neon DB reliability
- SC-011 (8/10 satisfaction): UX testing via acceptance scenarios
- SC-012 (zero vulnerabilities): httpOnly cookies, parameterized queries, user isolation

## Outcome

- ✅ Impact: Phase 2 implementation plan complete with full architecture, design artifacts, and 7 architecturally significant decisions documented. Ready for `/sp.tasks` (task decomposition).
- 🧪 Tests: Manual acceptance testing strategy documented in quickstart.md with 6 user stories and edge cases. Automated tests deferred to Phase III per constitution.
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, quickstart.md, api-spec.yaml) totaling ~2,500 lines of comprehensive documentation.
- 🔁 Next prompts: `/sp.tasks` to generate dependency-ordered task breakdown, then `/sp.implement` for code generation.
- 🧠 Reflection: Successfully balanced Phase II requirements with constitution boundaries. All decisions prioritize security (httpOnly cookies, user_id from JWT) and simplicity (service layer, metadata schema, Server Components). Monorepo structure enables coordinated frontend/backend evolution while maintaining clear separation of concerns. Critical design choice: API endpoints do NOT include user_id in URL - backend extracts from JWT for security. This eliminates authorization bugs from URL tampering.

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning completed without clarification needs or constitution violations.
- Graders run and results (PASS/FAIL): Constitution Check - PASS (no phase boundary violations, all technologies approved, cloud-native principles followed)
- Prompt variant (if applicable): Standard /sp.plan workflow with detailed Phase 2 requirements and explicit architectural constraints provided in user input
- Next experiment (smallest change to try): Proceed to `/sp.tasks` to decompose plan into executable tasks. Validate that task breakdown maintains Phase II boundaries and maps directly to project structure defined in plan.md. Ensure tasks are dependency-ordered (backend auth before frontend auth, backend CRUD before frontend UI).
