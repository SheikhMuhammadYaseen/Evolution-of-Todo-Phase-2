# Research Document: Phase II Full-Stack Web Todo Application

**Feature**: 002-phase2-fullstack-web
**Created**: 2025-12-27
**Purpose**: Resolve technical unknowns and establish architectural patterns for Phase II implementation

## Overview

This document captures research findings and technical decisions for Phase II, which evolves the Phase I in-memory CLI application into a full-stack web application with multi-user support, persistent storage, and JWT-based authentication.

## Research Areas

### 1. Monorepo Structure for Full-Stack Application

**Decision**: Use monorepo with `/backend` and `/frontend` separation at repository root

**Rationale**:
- Clear separation of concerns between Next.js frontend and FastAPI backend
- Each component can have independent dependencies (package.json vs requirements.txt)
- Simplifies deployment - can containerize separately if needed in Phase IV
- Aligns with industry standards for full-stack TypeScript/Python projects
- `/specs` folder remains at root for project-wide documentation access

**Structure**:
```
/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── specs/            # Feature specifications
└── history/          # PHRs and ADRs
```

**Alternatives Considered**:
- Single `/src` with language-mixed code: Rejected due to tooling complexity (Python + TypeScript in same dir)
- Separate repositories: Rejected as overkill for Phase II; monorepo simplifies coordination
- `/apps/backend` and `/apps/frontend`: Rejected as unnecessary nesting for a two-component system

---

### 2. Backend Architecture Pattern

**Decision**: Service layer pattern with dependency injection

**Rationale**:
- **Routers** handle HTTP concerns (request/response, validation)
- **Services** encapsulate business logic (task CRUD operations, user validation)
- **Models** define data structures (SQLModel entities)
- **Middleware** handles cross-cutting concerns (JWT verification, error handling, CORS)
- Dependency injection via FastAPI's `Depends()` for database sessions and user context
- Testable: Services can be tested independently of HTTP layer

**Layering**:
```
API Layer (Routers) → Service Layer → Data Access Layer (SQLModel) → Database
                  ↓
              Middleware (JWT, CORS, Errors)
```

**Alternatives Considered**:
- Direct database access in routers: Rejected due to poor testability and business logic leakage
- Repository pattern: Rejected as over-engineering for Phase II; SQLModel queries are clean enough
- Domain-Driven Design (DDD): Rejected as too heavy for simple CRUD operations

---

### 3. Authentication Flow & JWT Storage

**Decision**: httpOnly cookies for JWT token storage

**Rationale**:
- **Security**: httpOnly cookies are inaccessible to JavaScript, preventing XSS attacks
- **Better Auth native support**: Better Auth's JWT plugin is designed for cookie-based sessions
- **Automatic transmission**: Browser sends cookie with every request to same domain
- **Logout support**: Server can clear cookie on logout
- **CSRF mitigation**: Next.js includes CSRF protection; SameSite=Strict/Lax prevents cross-origin attacks

**Flow**:
1. User submits email/password to Better Auth endpoint (frontend)
2. Better Auth validates credentials, generates JWT signed with BETTER_AUTH_SECRET
3. Better Auth sets httpOnly cookie with JWT
4. Next.js API routes/client components make requests to FastAPI backend
5. Frontend extracts JWT from cookie and sends in `Authorization: Bearer <token>` header
6. Backend verifies JWT signature using BETTER_AUTH_SECRET
7. Backend extracts `user_id` from JWT claims
8. Backend enforces user isolation (user can only access their own tasks)

**Alternatives Considered**:
- localStorage: Rejected due to XSS vulnerability (malicious scripts can read token)
- sessionStorage: Rejected for same XSS reason + session lost on tab close (poor UX)
- In-memory only: Rejected due to poor UX (user must re-login on every page refresh)

---

### 4. API Endpoint Design & User Isolation

**Decision**: Extract `user_id` from JWT claims on backend; do NOT pass in URL path

**Corrected API Endpoints**:
```
GET    /api/tasks              → List all tasks for authenticated user
POST   /api/tasks              → Create new task
GET    /api/tasks/{id}         → Get single task
PUT    /api/tasks/{id}         → Update task
DELETE /api/tasks/{id}         → Delete task
PATCH  /api/tasks/{id}/complete → Toggle completion status
```

**Rationale**:
- **Security**: User cannot manipulate URL to access other users' data
- **Simplicity**: No need to validate `user_id` in URL matches JWT claim
- **Standard REST pattern**: Resource paths identify the resource, auth context implicit
- **Backend extracts user_id from JWT**: `user_id = get_current_user(jwt_token)` via dependency injection
- **Service layer receives user_id**: All service methods include `user_id` parameter for filtering

**Implementation**:
```python
# Backend middleware extracts user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    payload = jwt.decode(token, BETTER_AUTH_SECRET)
    return payload["user_id"]

# Router uses dependency injection
@router.get("/api/tasks")
def list_tasks(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return task_service.list_tasks(user_id, db)

# Service layer enforces user isolation
def list_tasks(user_id: int, db: Session):
    return db.query(Task).filter(Task.user_id == user_id).all()
```

**Alternatives Considered**:
- `/api/{user_id}/tasks`: Rejected due to security risk (user can change URL parameter)
- Cookie-based sessions without JWT: Rejected as stateful (violates cloud-native principles for Phase IV+)

---

### 5. Database Schema Management

**Decision**: SQLModel metadata-driven schema creation (no migrations in Phase II)

**Rationale**:
- **Simplicity**: Phase II is greenfield; no existing schema to migrate from
- **SQLModel generates DDL**: `Base.metadata.create_all(engine)` creates tables from models
- **Sufficient for Phase II**: No data migration needs, no backward compatibility requirements
- **Alembic deferred to Phase III**: When schema evolution becomes necessary

**Schema Initialization**:
```python
# On app startup (FastAPI lifespan event)
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)  # Creates tables if not exist
```

**Models**:
- `User`: id (UUID primary key), email (unique), password_hash, created_at
- `Task`: id (integer primary key, autoincrement), user_id (foreign key to User.id), title, description, status (boolean), created_at, updated_at

**Alternatives Considered**:
- Alembic migrations from start: Rejected as premature; Phase II has no migration needs
- Raw SQL scripts: Rejected due to lack of type safety and ORM integration
- Manual CREATE TABLE: Rejected in favor of declarative SQLModel approach

---

### 6. Frontend State Management

**Decision**: React Server Components + `fetch` with JWT forwarding

**Rationale**:
- **Next.js App Router paradigm**: Server Components are the default and recommended
- **Simplified data fetching**: Server Components fetch data on server, send HTML to client
- **Reduced client-side JavaScript**: Better performance, especially on mobile
- **JWT forwarding**: Server Component reads httpOnly cookie, forwards JWT to backend API
- **Client Components for interactivity**: Forms, buttons, checkboxes use `"use client"` directive

**Pattern**:
```typescript
// app/dashboard/page.tsx (Server Component)
export default async function DashboardPage() {
  const tasks = await fetchTasks();  // Server-side fetch with JWT from cookie
  return <TaskList tasks={tasks} />;  // Renders on server
}

// components/TaskList.tsx (Client Component for interactivity)
"use client";
export function TaskList({ tasks }) {
  const handleToggle = async (id) => {
    await fetch(`/api/tasks/${id}/complete`, { method: 'PATCH' });
    router.refresh();  // Re-fetch server component
  };
  return <div>{/* Render tasks with toggle buttons */}</div>;
}
```

**State Management**:
- **Server state**: Fetched in Server Components, passed as props
- **Client state**: Minimal; only for form inputs, UI toggles, optimistic updates
- **No global state library**: Zustand/Redux deferred to Phase III if complex state management needed

**Alternatives Considered**:
- Client-side only with React Query: Rejected due to increased bundle size and server component benefits
- Redux/Zustand from start: Rejected as over-engineering; Phase II state is simple
- tRPC: Rejected as Next.js + FastAPI architecture already established

---

### 7. Error Handling Strategy

**Decision**: Consistent JSON error responses with status codes

**Backend Error Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title cannot be empty",
    "details": { "field": "title", "constraint": "non_empty" }
  }
}
```

**Frontend Error Handling**:
```typescript
try {
  const response = await fetch('/api/tasks', { method: 'POST', body: JSON.stringify(task) });
  if (!response.ok) {
    const error = await response.json();
    displayErrorToast(error.message);  // User-friendly message
    logError(error);  // Technical details to console
  }
} catch (err) {
  displayErrorToast("Network error. Please try again.");
}
```

**Error Categories**:
- **400 Bad Request**: Validation failures (empty title, invalid email format)
- **401 Unauthorized**: Missing, expired, or invalid JWT
- **403 Forbidden**: Attempting to access another user's resource
- **404 Not Found**: Task ID doesn't exist
- **500 Internal Server Error**: Database failures, unexpected errors

**Rationale**:
- User sees friendly message ("Title is required")
- Developers see technical details in console/logs
- Consistent format simplifies frontend error handling
- HTTP status codes follow REST conventions

**Alternatives Considered**:
- Plain text errors: Rejected due to lack of structure for programmatic handling
- GraphQL-style errors array: Rejected as we're using REST, not GraphQL
- Exception-based flow control: Rejected in favor of explicit error responses

---

### 8. CORS Configuration

**Decision**: Configure CORS on FastAPI backend to allow Next.js frontend origin

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server (Phase II)
    allow_credentials=True,  # Required for cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Production Adjustment** (Phase III+):
```python
# Environment-based origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
allow_origins=ALLOWED_ORIGINS,  # e.g., ["https://app.example.com"]
```

**Rationale**:
- Next.js dev server (port 3000) and FastAPI dev server (port 8000) are different origins
- Cookies require `allow_credentials=True`
- Restricting origins prevents CSRF from untrusted sites

**Alternatives Considered**:
- Same-origin deployment (Next.js proxies to FastAPI): Deferred to Phase IV deployment planning
- `allow_origins=["*"]`: Rejected due to security risk (any site can call API)

---

### 9. Development Environment Setup

**Decision**: Separate dev servers with environment variables

**Backend** (`/backend`):
```bash
# .env file
DATABASE_URL=postgresql://user:pass@neon.db/todo
BETTER_AUTH_SECRET=<shared-secret>
ALLOWED_ORIGINS=http://localhost:3000

# Run
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend** (`/frontend`):
```bash
# .env.local file
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<shared-secret>  # Same as backend

# Run
cd frontend
npm install
npm run dev  # Runs on port 3000
```

**Shared Secrets**:
- `BETTER_AUTH_SECRET` MUST be identical in frontend and backend
- Generated once: `openssl rand -hex 32`
- Stored in `.env` files (gitignored)
- Production: Injected via environment variables or secret manager

**Rationale**:
- Standard development workflow for full-stack apps
- Environment variables externalize configuration (12-factor app principle)
- Separate processes simplify debugging

**Alternatives Considered**:
- Docker Compose from start: Deferred to Phase IV (unnecessary complexity for Phase II)
- Shared monorepo scripts (Turborepo, Nx): Deferred as Phase II only has 2 apps

---

### 10. Testing Strategy (Phase II)

**Decision**: Manual acceptance testing with documented scenarios

**Rationale**:
- **Phase II focus**: Deliver working full-stack application
- **Manual testing sufficient**: Small scope (6 user stories), single developer
- **Acceptance scenarios**: Defined in spec.md provide test checklist
- **Automated testing deferred**: Phase III will add Jest (frontend), pytest (backend)

**Manual Test Execution**:
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Follow acceptance scenarios from spec.md:
   - User Story 1: Sign up, sign in, logout
   - User Story 2: Add task with title and description
   - User Story 3: View task list
   - User Story 4: Toggle task completion status
   - User Story 5: Edit task
   - User Story 6: Delete task
4. Verify user isolation: Create second user, confirm tasks don't leak

**Documentation**: `quickstart.md` will include test scenarios

**Alternatives Considered**:
- TDD from start: Rejected due to Phase II time constraints; prioritize working software
- E2E with Playwright: Deferred to Phase III when test infrastructure justified
- Contract testing: Deferred to Phase III for API stability validation

---

## Summary of Decisions

| Area | Decision | Phase |
|------|----------|-------|
| Structure | Monorepo with `/backend`, `/frontend` | Phase II |
| Backend | FastAPI + Service Layer + SQLModel | Phase II |
| Frontend | Next.js App Router + Server Components | Phase II |
| Authentication | Better Auth with httpOnly cookies | Phase II |
| JWT Storage | httpOnly cookies (XSS-safe) | Phase II |
| API Design | `/api/tasks` (user_id from JWT) | Phase II |
| Database | Neon PostgreSQL + SQLModel metadata | Phase II |
| Migrations | Deferred to Phase III (Alembic) | Phase III+ |
| State Management | Server Components (no global state lib) | Phase II |
| Testing | Manual acceptance testing | Phase II |
| Automated Tests | Deferred to Phase III (Jest, pytest) | Phase III+ |
| CORS | Configured on FastAPI for Next.js origin | Phase II |
| Error Handling | JSON errors with consistent format | Phase II |

---

## Open Questions

None. All critical technical decisions resolved for Phase II implementation.

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Better Auth Documentation](https://www.better-auth.com/)
- [Neon PostgreSQL](https://neon.tech/docs)
- Phase I spec: `specs/001-phase1-cli-todo/spec.md`
- Phase II spec: `specs/002-phase2-fullstack-web/spec.md`
- Constitution: `.specify/memory/constitution.md`
