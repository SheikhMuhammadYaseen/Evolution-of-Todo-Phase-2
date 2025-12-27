# Data Model: Phase II Full-Stack Web Todo Application

**Feature**: 002-phase2-fullstack-web
**Created**: 2025-12-27
**Database**: Neon Serverless PostgreSQL (PostgreSQL 15+ compatible)
**ORM**: SQLModel (combines Pydantic and SQLAlchemy)

## Overview

Phase II introduces persistent storage for multi-user task management. The data model consists of two primary entities: **User** (representing authenticated accounts) and **Task** (representing todo items owned by users).

## Entity Definitions

### User

Represents an authenticated application user with email/password credentials.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique identifier for the user |
| `email` | String(255) | Unique, Not Null, Indexed | User's email address (used for authentication) |
| `password_hash` | String(255) | Not Null | Bcrypt-hashed password (never exposed to frontend) |
| `created_at` | DateTime | Not Null, Default: `now()` | Timestamp of account creation |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for duplicate prevention and fast lookup)

**Validation Rules** (enforced at application layer):
- `email`: Must match valid email regex pattern
- `password` (pre-hash): Minimum 8 characters (validated before hashing)

**SQLModel Definition** (simplified):
```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Security Notes**:
- Password is NEVER stored in plain text
- `password_hash` uses bcrypt with cost factor 12
- Better Auth handles password hashing automatically

---

### Task

Represents a todo item owned by a specific user.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| `user_id` | UUID | Foreign Key → User.id, Not Null, Indexed | Owner of the task (enforces user isolation) |
| `title` | String(500) | Not Null | Task name/summary (mandatory) |
| `description` | Text | Nullable | Optional detailed description of the task |
| `status` | Boolean | Not Null, Default: `false` | Completion status (false = incomplete, true = complete) |
| `created_at` | DateTime | Not Null, Default: `now()` | Timestamp when task was created |
| `updated_at` | DateTime | Not Null, Default: `now()`, Auto-update | Timestamp of last modification |

**Indexes**:
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (automatic in PostgreSQL, for query performance)
- Composite index on `(user_id, created_at DESC)` (for efficient user task list retrieval)

**Validation Rules** (enforced at application layer):
- `title`: Minimum 1 character after trimming whitespace, maximum 500 characters
- `description`: Maximum 10,000 characters (optional)

**SQLModel Definition** (simplified):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional, for ORM navigation)
    user: User = Relationship()
```

**Lifecycle**:
1. **Create**: User submits title + optional description → Task created with `status=false`, timestamps auto-set
2. **Read**: User retrieves tasks filtered by `user_id` (enforces isolation)
3. **Update**: User modifies title/description → `updated_at` auto-updated
4. **Toggle Status**: User toggles `status` boolean → `updated_at` auto-updated
5. **Delete**: User deletes task → Record permanently removed (no soft delete in Phase II)

---

## Relationships

### User ↔ Task (One-to-Many)

- **Cardinality**: One User has zero or many Tasks
- **Direction**: Task → User (foreign key from Task to User)
- **Cascade Delete**: When User is deleted, all their Tasks are also deleted (`ON DELETE CASCADE`)
- **Referential Integrity**: PostgreSQL enforces that `task.user_id` must reference an existing `user.id`

**ER Diagram**:
```
┌──────────────────┐         ┌──────────────────┐
│      User        │         │      Task        │
├──────────────────┤         ├──────────────────┤
│ id (UUID) PK     │◄───────┤ id (int) PK      │
│ email            │ 1     ∞│ user_id (FK)     │
│ password_hash    │         │ title            │
│ created_at       │         │ description      │
└──────────────────┘         │ status           │
                             │ created_at       │
                             │ updated_at       │
                             └──────────────────┘
```

---

## State Transitions

### Task Status Lifecycle

```
[Created] ──────► status = false (incomplete)
    │
    │ (User clicks toggle)
    ▼
status = true (complete)
    │
    │ (User clicks toggle again)
    ▼
status = false (incomplete)
    │
    │ (cycle repeats indefinitely)
```

**Rules**:
- Tasks are created as incomplete (`status=false`)
- Status can toggle between `true` and `false` unlimited times
- No intermediate states (Phase II has only two states: complete/incomplete)
- Status changes are idempotent (setting status to current value is allowed, no-op)

---

## Data Volume Assumptions

**Phase II Scale Targets** (from spec.md Success Criteria):
- **Users**: 1-100 concurrent users (multi-user capability demonstration)
- **Tasks per User**: Up to 1,000 tasks (per assumption in spec.md SC-004)
- **Total Tasks**: ~10,000-100,000 tasks (100 users × 1,000 tasks)
- **Database Size**: ~50 MB (tasks + users + indexes)

**Performance Requirements**:
- Task list retrieval: <1 second for up to 1,000 user tasks (SC-004)
- Task CRUD operations: <1 second (SC-004)
- Query optimization: Index on `(user_id, created_at DESC)` ensures fast filtering and sorting

---

## Schema Initialization

**Phase II Approach**: SQLModel metadata-driven (no migrations)

```python
# backend/src/database.py
from sqlmodel import SQLModel, create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon connection string
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for dev logging

def init_db():
    """Create all tables on app startup"""
    SQLModel.metadata.create_all(engine)
```

**Execution**: Called once on application startup via FastAPI lifespan event

**Migration Strategy**: Deferred to Phase III (Alembic for schema evolution)

---

## Security Considerations

### User Isolation Enforcement

**Database Level**:
- Foreign key constraint ensures tasks reference valid users
- No database-level row-level security (RLS) in Phase II; enforcement at application layer

**Application Level** (Critical):
```python
# Every task query MUST filter by user_id
def list_tasks(user_id: UUID, db: Session):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(task_id: int, user_id: UUID, db: Session):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**Rule**: NEVER query tasks without filtering by `user_id` from JWT

### Password Security

- Plain text passwords NEVER stored
- Bcrypt hashing with cost factor 12 (Better Auth default)
- Password validation before hashing (minimum 8 characters, from FR-002)
- `password_hash` field NEVER returned in API responses

### SQL Injection Prevention

- SQLModel uses parameterized queries (ORM protection)
- No raw SQL execution in Phase II
- Input validation at Pydantic model layer (type checking, length limits)

---

## Data Consistency Rules

### Referential Integrity

1. **Task → User**: Task cannot exist without valid user (foreign key enforced)
2. **Cascade Delete**: Deleting user deletes all their tasks (prevents orphaned tasks)
3. **Unique Email**: No two users can have same email (unique constraint enforced)

### Timestamps

- `created_at`: Set once on record creation, immutable
- `updated_at`: Auto-updated on every UPDATE operation (PostgreSQL trigger or ORM hook)
- Timezone: All timestamps stored in UTC

### Status Consistency

- `status` defaults to `false` on creation (from FR-019)
- Only valid values: `true` or `false` (boolean type enforces this)
- No null status allowed (NOT NULL constraint)

---

## Evolution from Phase I

### Phase I Data Model (In-Memory)

```python
# Phase I: Python dictionary in memory
task = {
    "id": 1,              # Integer
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": False       # Boolean
}
tasks = [task1, task2, ...]  # List in memory, lost on exit
```

### Phase II Data Model (Persistent + Multi-User)

```python
# Phase II: SQLModel ORM, PostgreSQL database
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")  # NEW: User isolation
    title: str = Field(max_length=500)
    description: str | None = Field(default=None)
    status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # NEW: Audit trail
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # NEW: Audit trail
```

**Changes**:
- Added `user_id` foreign key for multi-user support
- Added `created_at` and `updated_at` timestamps for audit trail
- Replaced in-memory list with PostgreSQL table
- ID generation handled by database (autoincrement) instead of manual increment
- User entity added to support authentication

**Preserved Concepts**:
- Task ID (integer primary key)
- Title (non-empty string, mandatory)
- Description (optional string)
- Status (boolean, defaults to false)

---

## Future Extensions (Out of Phase II Scope)

The following are explicitly OUT OF SCOPE for Phase II but could be added in Phase III+:

- `priority` field (Low, Medium, High)
- `due_date` field (datetime)
- `tags` relationship (many-to-many)
- `category_id` foreign key (task categorization)
- Task sharing between users
- Task history/audit log (track all changes)
- Soft delete (mark deleted, don't remove)
- Full-text search on title/description

---

## Summary

Phase II data model introduces persistent, multi-user storage while preserving the core task concepts from Phase I. The model is intentionally minimal, focusing on authentication (User entity) and user-isolated task management (Task entity with user_id foreign key). All advanced features are deferred to Phase III+ to maintain Phase II boundaries.

**Key Design Decisions**:
- UUID for User IDs (better for distributed systems in Phase IV+)
- Integer for Task IDs (simpler, human-readable, sufficient for Phase II scale)
- httpOnly cookie-based JWT (user_id extracted on backend, not in URL)
- Timestamps for basic audit trail (creation and modification times)
- No soft delete (tasks permanently removed on DELETE)
- No versioned migrations (SQLModel metadata sufficient for Phase II greenfield)

**Compliance**: This data model satisfies all Key Entities requirements from `specs/002-phase2-fullstack-web/spec.md` (User and Task entities with specified fields).
