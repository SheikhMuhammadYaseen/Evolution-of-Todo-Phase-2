# Implementation Plan: Phase II Full-Stack Web Todo Application

**Branch**: `002-phase2-fullstack-web` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack-web/spec.md`

## Summary

Phase II evolves the Phase I in-memory CLI todo application into a modern full-stack web application with multi-user support, persistent storage, and JWT-based authentication. The implementation introduces a Next.js frontend, FastAPI backend, Neon PostgreSQL database, and Better Auth for secure user authentication.

**Primary Requirements**:
- Multi-user authentication with Better Auth (email/password + JWT)
- Persistent task storage in Neon Serverless PostgreSQL
- Responsive Next.js web interface (App Router)
- RESTful FastAPI backend with user isolation
- All 5 CRUD operations from Phase I adapted for web (add, view, update, delete, toggle status)

**Technical Approach** (from research.md):
- Monorepo structure (`/backend`, `/frontend`)
- Service layer pattern on backend (Routers → Services → SQLModel)
- JWT in httpOnly cookies (XSS-safe)
- User context extraction from JWT on backend (not passed in URL)
- SQLModel metadata-driven schema (no migrations in Phase II)
- Server Components + Client Components for optimal performance

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, PyJWT, psycopg2-binary, uvicorn
- Frontend: Next.js 16+, React 19, Better Auth (with JWT plugin), Tailwind CSS

**Storage**: Neon Serverless PostgreSQL (PostgreSQL 15+ compatible)
**Testing**: Manual acceptance testing (Phase II); automated tests deferred to Phase III
**Target Platform**:
- Backend: Linux/macOS/Windows development servers, uvicorn ASGI server
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge latest 2 versions), responsive design (320px - 1920px viewports)

**Project Type**: Web application (full-stack monorepo)
**Performance Goals**:
- API response time: <1 second for task CRUD operations with <1000 user tasks (SC-004)
- Frontend load time: Dashboard renders in <5 seconds (SC-002)
- Registration to first task: <3 minutes (SC-001)

**Constraints**:
- No real-time sync (WebSockets deferred to Phase III)
- No automated tests (deferred to Phase III)
- No password reset (deferred to Phase III)
- No advanced todo features (priorities, due dates, tags, categories)
- No agents, MCP, or AI features (Phase V)
- Phase II boundaries strictly enforced per constitution

**Scale/Scope**:
- Target: 1-100 concurrent users (multi-user demonstration)
- Task capacity: Up to 1,000 tasks per user
- Database: ~50 MB estimated (tasks + users + indexes)
- Codebase: ~3,000-5,000 lines (backend + frontend)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Boundary Compliance

**Phase II Requirements** (from constitution V):
- ✅ Full-Stack Web Application architecture
- ✅ Next.js responsive frontend with Better Auth and JWT authentication
- ✅ FastAPI backend with SQLModel ORM
- ✅ Neon DB (PostgreSQL) for multi-user persistent storage
- ✅ RESTful API contracts
- ❌ No distributed systems (deferred to Phase V)
- ❌ No orchestration (deferred to Phase V)
- ❌ No agent frameworks (deferred to Phase V)

**Prohibited Features** (Phase III+):
- ❌ No advanced web features (real-time updates, advanced state management) - Phase III
- ❌ No horizontal scaling infrastructure (load balancing, caching) - Phase IV
- ❌ No Kubernetes, Kafka, Dapr, or microservices - Phase V
- ❌ No OpenAI Agents SDK or MCP integration - Phase V

**Verdict**: ✅ **PASS** - All features belong to Phase II; no phase boundary violations

### Technology Stack Compliance

**Backend** (from constitution VI):
- ✅ Python 3.11 (approved language)
- ✅ FastAPI (approved API framework, Phase II+)
- ✅ SQLModel (approved ORM, Phase II+)
- ✅ Neon DB PostgreSQL (approved database, Phase II+)
- ✅ Better Auth with JWT (approved authentication, Phase II+)
- ❌ No OpenAI Agents SDK (Phase V+ only)
- ❌ No MCP SDK (Phase V+ only)

**Frontend** (from constitution VI):
- ✅ Next.js 16+ (approved framework, Phase II+)
- ✅ TypeScript (preferred for type safety)
- ✅ Better Auth integration with JWT tokens
- ✅ Responsive design with mobile-first approach
- ❌ No alternative frameworks (Vue, Angular, Svelte)

**Infrastructure** (Phase II):
- ✅ Development servers only (uvicorn for FastAPI, Next.js dev server)
- ❌ No Docker (deferred to Phase IV+)
- ❌ No Kubernetes (Phase V+ only)
- ❌ No Kafka (Phase V+ only)
- ❌ No Dapr (Phase V+ only)

**Verdict**: ✅ **PASS** - All technologies approved for Phase II

### Cloud-Native Architecture Compliance

**Modularity** (from constitution VII):
- ✅ Backend and frontend independently deployable
- ✅ Clear separation: presentation (Next.js), business logic (Services), data access (SQLModel)
- ✅ Well-defined interfaces: OpenAPI spec for REST API

**Statelessness** (from constitution VII, Phase II+):
- ✅ JWT-based authentication (no server-side session storage)
- ✅ User context passed explicitly via JWT in Authorization header
- ✅ Persistent state externalized to Neon PostgreSQL

**Separation of Concerns** (from constitution VII):
- ✅ Business logic isolated in Service layer (not in routers)
- ✅ Data models (SQLModel) decoupled from API representations (Pydantic schemas)
- ✅ Cross-cutting concerns: JWT middleware, CORS middleware, error handling middleware

**Cloud Readiness** (Phase II preparedness):
- ✅ Configuration via environment variables (DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS)
- ✅ Horizontal scalability consideration: stateless backend design (Phase IV readiness)
- ✅ Observability readiness: structured logging (FastAPI logs, errors logged with context)
- ⚠️  Container-friendly: Deferred to Phase IV, but design doesn't prevent containerization

**Verdict**: ✅ **PASS** - Cloud-native principles followed for Phase II scope

### Agent Operational Rules Compliance

**Agent Constraints** (from constitution):
- ✅ No unsolicited features: Implementation strictly follows spec.md requirements
- ✅ Specification adherence: All ambiguities resolved in research.md
- ✅ No speculative coding: Code generated only after task approval (`/sp.tasks`)
- ✅ Phase awareness: All dependencies validated against Phase II boundaries

**Verdict**: ✅ **PASS** - Agent operational rules will be followed during `/sp.implement`

### Overall Constitution Compliance

✅ **GATE PASSED** - No constitution violations. Safe to proceed with Phase 0 research and Phase 1 design.

**Re-check after Phase 1**: ✅ **GATE PASSED** - No violations introduced during design phase.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-fullstack-web/
├── spec.md              # Feature specification (from /sp.specify)
├── plan.md              # This file (from /sp.plan)
├── research.md          # Phase 0 research findings (from /sp.plan)
├── data-model.md        # Phase 1 data model (from /sp.plan)
├── quickstart.md        # Phase 1 usage guide (from /sp.plan)
├── contracts/
│   └── api-spec.yaml    # Phase 1 OpenAPI 3.0 spec (from /sp.plan)
├── checklists/
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Phase 2 task breakdown (from /sp.tasks - NOT yet created)
```

### Source Code (repository root)

```text
/
├── backend/                      # FastAPI backend application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry point, lifespan events
│   │   ├── config.py             # Environment variable loading (Pydantic Settings)
│   │   ├── database.py           # SQLModel engine, session dependency
│   │   ├── init_db.py            # Database schema initialization script
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User SQLModel (id, email, password_hash, created_at)
│   │   │   └── task.py           # Task SQLModel (id, user_id FK, title, description, status, timestamps)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User Pydantic schemas (UserCreate, UserResponse)
│   │   │   └── task.py           # Task Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication service (JWT signing, verification)
│   │   │   ├── user.py           # User service (create user, get by email, password hashing)
│   │   │   └── task.py           # Task service (CRUD operations with user_id filtering)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Auth routes: POST /api/auth/signup, /api/auth/signin
│   │   │   └── tasks.py          # Task routes: GET/POST/PUT/PATCH/DELETE /api/tasks/*
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py            # JWT verification middleware, get_current_user dependency
│   │   │   ├── cors.py           # CORS configuration
│   │   │   └── errors.py         # Global error handling (HTTPException → JSON errors)
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── security.py       # Password hashing (bcrypt), JWT utilities
│   ├── tests/                    # Placeholder (automated tests deferred to Phase III)
│   │   └── README.md             # "Tests deferred to Phase III"
│   ├── .env.example              # Example environment variables
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend setup instructions
│
├── frontend/                     # Next.js frontend application
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx        # Root layout (Better Auth provider, global styles)
│   │   │   ├── page.tsx          # Landing page (redirect to signin if not authenticated)
│   │   │   ├── signup/
│   │   │   │   └── page.tsx      # Signup page (Better Auth form)
│   │   │   ├── signin/
│   │   │   │   └── page.tsx      # Signin page (Better Auth form)
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx      # Dashboard (Server Component: fetch tasks, render list)
│   │   │   │   └── layout.tsx    # Protected layout (auth guard middleware)
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── [...better-auth]/route.ts  # Better Auth API routes
│   │   ├── components/
│   │   │   ├── TaskList.tsx      # Client Component: renders tasks, handles interactions
│   │   │   ├── TaskItem.tsx      # Client Component: single task with toggle/edit/delete
│   │   │   ├── TaskForm.tsx      # Client Component: add/edit task form
│   │   │   ├── Header.tsx        # Navigation header with logout button
│   │   │   └── EmptyState.tsx    # "No tasks yet" message
│   │   ├── lib/
│   │   │   ├── auth.ts           # Better Auth configuration (JWT plugin, httpOnly cookie)
│   │   │   ├── api-client.ts     # Fetch wrapper that attaches JWT to requests
│   │   │   └── types.ts          # TypeScript types (Task, User, ApiResponse)
│   │   └── styles/
│   │       └── globals.css       # Tailwind CSS imports, custom global styles
│   ├── public/                   # Static assets (favicon, images)
│   ├── tests/                    # Placeholder (automated tests deferred to Phase III)
│   │   └── README.md             # "Tests deferred to Phase III"
│   ├── .env.local.example        # Example environment variables
│   ├── next.config.js            # Next.js configuration
│   ├── package.json              # NPM dependencies
│   ├── tsconfig.json             # TypeScript configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   └── README.md                 # Frontend setup instructions
│
├── specs/                        # Feature specifications (already exists)
├── history/                      # PHRs and ADRs (already exists)
├── .specify/                     # SpecKit Plus templates and scripts (already exists)
├── .gitignore                    # Ignore node_modules, venv, .env, __pycache__
└── README.md                     # Project overview, links to Phase I and Phase II docs
```

**Structure Decision**: Web application structure (Option 2 from template) selected based on project type. The monorepo separates backend (Python/FastAPI) and frontend (TypeScript/Next.js) for clear technology boundaries and independent deployment readiness (Phase IV+).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. This table is empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Research Findings

**Status**: ✅ Completed

All technical unknowns resolved and documented in [research.md](./research.md).

**Key Decisions**:
1. **Monorepo Structure**: `/backend` and `/frontend` separation at root (vs. single `/src` or separate repos)
2. **Backend Architecture**: Service layer pattern with dependency injection (vs. repository pattern or DDD)
3. **JWT Storage**: httpOnly cookies (vs. localStorage or sessionStorage) for XSS protection
4. **API Design**: `/api/tasks` with user_id extracted from JWT (vs. `/api/{user_id}/tasks` in URL)
5. **Database Schema**: SQLModel metadata-driven (vs. Alembic migrations from start)
6. **Frontend State**: Server Components + fetch (vs. client-only with React Query or Redux)
7. **Error Handling**: Consistent JSON error responses with status codes
8. **CORS**: Configured on FastAPI for Next.js origin (vs. same-origin deployment in Phase II)
9. **Development**: Separate dev servers with environment variables (vs. Docker Compose)
10. **Testing**: Manual acceptance testing (vs. automated TDD from start)

**Rationale**: See [research.md](./research.md) for detailed analysis of each decision, alternatives considered, and rejection reasons.

## Phase 1: Design Artifacts

**Status**: ✅ Completed

### Data Model

**Status**: ✅ Completed - [data-model.md](./data-model.md)

**Entities**:
- **User**: `id` (UUID PK), `email` (unique), `password_hash`, `created_at`
- **Task**: `id` (int PK), `user_id` (FK → User), `title`, `description`, `status` (boolean), `created_at`, `updated_at`

**Relationships**: One-to-Many (User → Tasks), cascade delete

**Indexes**:
- `user.email` (unique, for fast login lookup)
- `task.user_id` (foreign key, for filtering)
- `(task.user_id, task.created_at DESC)` (composite, for efficient task list retrieval)

**Evolution from Phase I**: Added `user_id` foreign key, timestamps, persistent storage (SQLModel ORM + PostgreSQL) replacing in-memory dictionary list.

### API Contracts

**Status**: ✅ Completed - [contracts/api-spec.yaml](./contracts/api-spec.yaml)

**Endpoints** (OpenAPI 3.0 specification):
- `GET /api/tasks` → List all tasks for authenticated user
- `POST /api/tasks` → Create new task
- `GET /api/tasks/{id}` → Get single task
- `PUT /api/tasks/{id}` → Update task (title and/or description)
- `DELETE /api/tasks/{id}` → Delete task permanently
- `PATCH /api/tasks/{id}/complete` → Toggle completion status

**Authentication**: All endpoints require JWT in `Authorization: Bearer <token>` header

**Error Responses**: Consistent JSON format with `code`, `message`, `details` fields

**HTTP Status Codes**: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error

### Quickstart Guide

**Status**: ✅ Completed - [quickstart.md](./quickstart.md)

**Contents**:
- Prerequisites (Node.js 20+, Python 3.11+, Neon database)
- Backend setup (venv, pip install, environment variables, database initialization, uvicorn server)
- Frontend setup (npm install, environment variables, dev server)
- First-time usage (create account, sign in, CRUD operations)
- Manual acceptance testing scenarios (6 user stories from spec.md)
- Troubleshooting guide (common issues and solutions)
- API testing with curl examples

## Architecture Decisions

### 1. Monorepo vs. Separate Repositories

**Decision**: Monorepo with `/backend` and `/frontend` at repository root

**Rationale**:
- **Coordination**: Frontend and backend evolve together in Phase II; monorepo simplifies synchronization
- **Documentation**: Shared `/specs` folder accessible to both components
- **Phase II scope**: Only two components; monorepo tooling (Turborepo, Nx) unnecessary overhead
- **Future flexibility**: Can split into separate repos in Phase IV if microservices architecture adopted

**Trade-offs**:
- ✅ Pro: Simplified dependency management, atomic commits for cross-stack changes
- ❌ Con: Larger repository size (mitigated by .gitignore for node_modules, venv)
- ❌ Con: Requires discipline to avoid circular dependencies (enforced by directory structure)

**Alternatives Considered**:
- Separate repos: Rejected due to coordination overhead for Phase II tight coupling
- Single `/src`: Rejected due to language/tooling conflicts (Python vs. TypeScript)

---

### 2. Backend: Service Layer vs. Repository Pattern

**Decision**: Service layer pattern (Routers → Services → SQLModel)

**Rationale**:
- **Simplicity**: Phase II CRUD operations are straightforward; service layer sufficient
- **Testability**: Business logic isolated in services, can be unit tested independently
- **SQLModel clarity**: ORM queries are clean; no need for repository abstraction layer
- **Over-engineering avoidance**: Repository pattern adds indirection without Phase II benefit

**Trade-offs**:
- ✅ Pro: Fewer layers (3 vs. 4), simpler codebase, faster development
- ✅ Pro: Services can be tested with in-memory SQLite (Phase III)
- ❌ Con: Direct SQLModel usage in services; if ORM changes, services must change (low risk in Phase II)

**Alternatives Considered**:
- Repository pattern: Rejected as premature abstraction; YAGNI (You Ain't Gonna Need It)
- Direct DB access in routers: Rejected due to testability and business logic leakage

---

### 3. JWT Storage: httpOnly Cookies vs. localStorage

**Decision**: httpOnly cookies for JWT token storage

**Rationale**:
- **Security**: httpOnly cookies are inaccessible to JavaScript, preventing XSS token theft
- **Better Auth native support**: JWT plugin designed for cookie-based sessions
- **Automatic transmission**: Browser sends cookie with every request to same domain (no manual header attachment needed in many cases)
- **CSRF protection**: Next.js has built-in CSRF protection; SameSite=Strict/Lax prevents cross-origin attacks

**Trade-offs**:
- ✅ Pro: Best security practice, recommended by OWASP
- ✅ Pro: Logout is simple (server clears cookie)
- ❌ Con: Requires backend to set cookie (not purely stateless JWT); acceptable for Phase II
- ❌ Con: CORS must allow credentials (`allow_credentials=True`); configured in research.md

**Alternatives Considered**:
- localStorage: Rejected due to XSS vulnerability (malicious scripts can read token)
- sessionStorage: Rejected for same XSS reason + poor UX (session lost on tab close)
- In-memory only: Rejected due to poor UX (re-login on every page refresh)

---

### 4. API Endpoint Design: User ID in URL vs. JWT

**Decision**: Extract `user_id` from JWT on backend; do NOT include in URL path

**Endpoint Pattern**: `/api/tasks` (NOT `/api/{user_id}/tasks`)

**Rationale**:
- **Security**: User cannot manipulate URL to access other users' data
- **Simplicity**: No need to validate URL `user_id` matches JWT claim
- **RESTful best practice**: Resource paths identify the resource; authentication context is implicit
- **Backend extraction**: Middleware parses JWT, provides `user_id` via dependency injection

**Trade-offs**:
- ✅ Pro: Eliminates entire class of authorization bugs (URL parameter tampering)
- ✅ Pro: Simpler frontend code (no need to pass user_id in every API call)
- ❌ Con: Slightly less explicit in URL; acceptable for security gain

**Alternatives Considered**:
- `/api/{user_id}/tasks`: Rejected due to security risk (user can change URL parameter)
- Cookie-based sessions without JWT: Rejected as stateful (violates cloud-native principles for Phase IV+)

---

### 5. Database Migrations: Alembic vs. Metadata-Driven

**Decision**: SQLModel metadata-driven schema creation (no migrations in Phase II)

**Rationale**:
- **Greenfield project**: No existing schema to migrate from
- **Phase II simplicity**: No schema evolution needs during Phase II development
- **Fast iteration**: `metadata.create_all()` on startup is instant; no migration script maintenance
- **Sufficient for Phase II**: Alembic deferred to Phase III when schema changes become necessary

**Trade-offs**:
- ✅ Pro: Zero migration complexity in Phase II
- ✅ Pro: Faster development (no migration script generation)
- ❌ Con: No schema version tracking; acceptable for Phase II (single schema version)
- ❌ Con: Cannot roll back schema changes; acceptable for Phase II (no schema evolution)

**Alternatives Considered**:
- Alembic from start: Rejected as premature; Phase II has no migration needs
- Raw SQL scripts: Rejected due to lack of type safety and ORM integration

---

### 6. Frontend State Management: Server Components vs. Client State Libraries

**Decision**: Next.js Server Components + `fetch` for data, minimal client state

**Rationale**:
- **App Router paradigm**: Server Components are default and recommended in Next.js 14+
- **Performance**: Less JavaScript sent to client (better mobile performance)
- **Simplicity**: Phase II state is simple (task list, form inputs); no need for Redux/Zustand
- **SEO readiness**: Server-rendered content (future Phase III benefit)

**Trade-offs**:
- ✅ Pro: Reduced bundle size, faster initial load
- ✅ Pro: Simplified data fetching (no useEffect boilerplate)
- ❌ Con: Mixed Server/Client Component model requires understanding of boundaries; acceptable learning curve
- ❌ Con: No global state library; if Phase III needs complex state, refactor then

**Alternatives Considered**:
- Client-only with React Query: Rejected due to larger bundle size and unnecessary for Phase II
- Redux/Zustand from start: Rejected as over-engineering; Phase II state is trivial
- tRPC: Rejected as FastAPI backend is already established (not TypeScript end-to-end)

---

### 7. Authentication: Better Auth vs. Custom JWT Implementation

**Decision**: Better Auth library with JWT plugin

**Rationale**:
- **Security**: Better Auth handles bcrypt hashing, JWT signing, token expiry correctly
- **Time savings**: No need to implement signup/signin/logout flows from scratch
- **Cookie management**: Better Auth sets httpOnly cookies automatically
- **Industry standard**: Well-tested library, reduces risk of auth vulnerabilities

**Trade-offs**:
- ✅ Pro: Reduced implementation time, fewer auth bugs
- ✅ Pro: httpOnly cookie handling built-in
- ❌ Con: Dependency on external library; mitigated by mature, well-maintained library
- ❌ Con: Learning curve for Better Auth API; acceptable for time savings

**Alternatives Considered**:
- Custom JWT implementation: Rejected due to security risk (easy to get wrong) and time cost
- Passport.js: Rejected as Node.js library (backend is Python)
- Auth0/Clerk: Rejected as third-party service (Phase II uses self-hosted Better Auth)

---

## Implementation Phases

### Phase 0: Research (Completed ✅)

**Artifact**: [research.md](./research.md)

**Decisions Made**:
1. Monorepo structure
2. Service layer backend architecture
3. httpOnly cookie JWT storage
4. API design without user_id in URL
5. SQLModel metadata-driven schema
6. Server Components frontend
7. CORS configuration
8. Error handling patterns
9. Development environment setup
10. Manual testing approach

### Phase 1: Design (Completed ✅)

**Artifacts**:
- [data-model.md](./data-model.md) - User and Task entities, relationships, indexes
- [contracts/api-spec.yaml](./contracts/api-spec.yaml) - OpenAPI 3.0 REST API specification
- [quickstart.md](./quickstart.md) - Setup and testing guide

**Deliverables**:
- Entity definitions (User, Task) with fields, types, constraints
- API contract (6 endpoints, schemas, error responses)
- Manual testing scenarios (6 user stories, edge cases)

### Phase 2: Task Decomposition (Next Step)

**Command**: `/sp.tasks`

**Expected Output**: [tasks.md](./tasks.md) with dependency-ordered implementation tasks

**Task Groups** (preview):
1. **Setup Tasks** (US0): Initialize monorepo structure, environment files, dependencies
2. **Backend Foundation** (US0): Database models, configuration, middleware
3. **Authentication** (US1): User service, auth router, JWT middleware
4. **Task CRUD** (US2-6): Task service, task router, all CRUD endpoints
5. **Frontend Foundation** (US0): Next.js setup, Better Auth integration, API client
6. **Frontend UI** (US1-6): Auth pages, dashboard, task components
7. **Integration Testing** (US7): Manual acceptance testing per quickstart.md

### Phase 3: Implementation (Final Step)

**Command**: `/sp.implement`

**Expected Behavior**:
- Execute tasks in dependency order (US0 → US1 → US2-6 in parallel where possible)
- Generate code adhering to structure in "Project Structure" section
- Validate against spec.md acceptance criteria
- Commit work via `/sp.git.commit_pr` after logical groupings

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Better Auth JWT plugin misconfiguration** | High (authentication broken) | Medium | Follow official docs, test JWT issuance/verification early, verify shared secret matches |
| **CORS issues in development** | Medium (frontend can't call backend) | Medium | Configure CORS on FastAPI before frontend development, test preflight requests |
| **Database connection failures (Neon)** | High (app unusable) | Low | Validate DATABASE_URL early, handle connection errors gracefully, log errors for debugging |
| **JWT token expiry during testing** | Low (user must re-login) | High | Set token expiry to 24 hours for Phase II, document in quickstart.md, defer token refresh to Phase III |
| **User isolation bug (cross-user data access)** | Critical (security vulnerability) | Low | Test user isolation explicitly (second user scenario in quickstart.md), review every task query for user_id filter |
| **Task list performance degradation (>1000 tasks)** | Medium (slow load times) | Low | Index on (user_id, created_at DESC), test with large dataset, pagination deferred to Phase III if needed |

**Critical Path**: Backend authentication (US1) must be complete before frontend auth (US1 frontend tasks) can begin. Task CRUD (US2-6 backend) must be complete before frontend task UI (US2-6 frontend tasks).

## Success Criteria Alignment

This plan is designed to satisfy all 12 Success Criteria from [spec.md](./spec.md):

- **SC-001** (Registration to first task <3 min): Quickstart guide documents this flow; manual testing validates timing
- **SC-002** (Signin and view <5 sec): Server Components optimize load time; tested in acceptance scenarios
- **SC-003** (100% user isolation): `user_id` filter enforced in every task service method; tested with two users
- **SC-004** (API response <1 sec): FastAPI is performant; SQLModel queries optimized with indexes
- **SC-005** (Responsive 320px-1920px): Tailwind CSS mobile-first approach; tested on multiple viewports
- **SC-006** (No documentation needed): Intuitive UI design; user tested in manual acceptance testing
- **SC-007** (100% unauthorized access rejection): JWT middleware validates all requests; tested with missing/expired/invalid tokens
- **SC-008** (Data persists): PostgreSQL ensures persistence; tested with page refresh and multi-device signin
- **SC-009** (Graceful error handling): Consistent JSON error responses; user-friendly messages displayed in UI
- **SC-010** (99% uptime): FastAPI + Neon DB are reliable; production deployment readiness in Phase III+
- **SC-011** (8/10 satisfaction): UX testing via manual acceptance scenarios; feedback incorporated
- **SC-012** (Zero security vulnerabilities): httpOnly cookies, parameterized queries, user isolation enforced

## Next Steps

1. **Human review and approval of this plan** - Confirm architecture, structure, and decisions
2. **ADR creation** (if needed) - Architecturally significant decisions may warrant ADRs (e.g., JWT storage, API design)
3. **Run `/sp.tasks`** - Generate dependency-ordered task breakdown
4. **Human approval of tasks** - Review task list before implementation
5. **Run `/sp.implement`** - Execute tasks, generate code
6. **Manual acceptance testing** - Follow quickstart.md scenarios
7. **Commit and create PR** via `/sp.git.commit_pr`

---

**Plan Status**: ✅ Complete | **Phase**: II | **Ready for**: `/sp.tasks`
