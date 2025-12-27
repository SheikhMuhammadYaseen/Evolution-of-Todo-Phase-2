# Evolution of Todo - Multi-Phase Learning Project

A progressive todo application demonstrating software architecture evolution from simple CLI to distributed cloud-native system.

## Project Overview

This project evolves through five distinct phases, each adding architectural complexity:

- **Phase I**: In-memory Python CLI application (✅ Complete)
- **Phase II**: Full-stack web application with multi-user support (✅ MVP Complete)
- **Phase III**: Advanced web features and optimizations (Planned)
- **Phase IV**: Horizontal scaling and cloud readiness (Planned)
- **Phase V**: Distributed cloud-native architecture with Kubernetes, Kafka, and Dapr (Planned)

---

## Current Phase: Phase II (Full-Stack Web Application)

### Architecture

**Monorepo Structure**:
```
/backend    # FastAPI + SQLModel + PostgreSQL
/frontend   # Next.js + TypeScript + Tailwind CSS
/specs      # Feature specifications and documentation
/src        # Phase I CLI application (preserved)
```

**Technology Stack**:
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with bcrypt password hashing

**Features**:
- ✅ User registration and authentication (email/password)
- ✅ Multi-user support with complete data isolation
- ✅ Persistent task storage (survives restarts)
- ✅ Create, view, and manage tasks via web UI
- ✅ Toggle task completion status
- ✅ Update and delete tasks
- ✅ Responsive design (mobile and desktop)

---

## Quick Start

### Prerequisites

- **Python 3.11+**: [Download](https://www.python.org/downloads/)
- **Node.js 20+**: [Download](https://nodejs.org/)
- **Neon Database**: Free account at [neon.tech](https://neon.tech/)

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo
git checkout 002-phase2-fullstack-web
```

### 2. Generate Shared Secret

The `BETTER_AUTH_SECRET` must be identical in both backend and frontend:

```bash
openssl rand -hex 32
```

**Copy this value** - you'll use it in both `.env` files.

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set:
#   DATABASE_URL=<your-neon-connection-string>
#   BETTER_AUTH_SECRET=<generated-secret-from-step-2>
#   ALLOWED_ORIGINS=http://localhost:3000

# Initialize database schema
python -m src.init_db

# Start backend server
uvicorn src.main:app --reload --port 8000
```

**Backend**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### 4. Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local and set:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
#   BETTER_AUTH_SECRET=<same-secret-as-backend>

# Start development server
npm run dev
```

**Frontend**: http://localhost:3000

### 5. First-Time Usage

1. Open http://localhost:3000 in your browser
2. Click "Sign up" to create an account
3. Enter email and password (min 8 characters)
4. Sign in with your credentials
5. Create tasks using the form on the dashboard
6. View, toggle status, and delete tasks

---

## Environment Variables

### Backend (.env)

```bash
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/main?sslmode=require
BETTER_AUTH_SECRET=<generated-with-openssl-rand-hex-32>
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=DEBUG
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-as-backend>
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` must be IDENTICAL in both files!

---

## API Endpoints

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate and get JWT token
- `POST /api/auth/logout` - Logout

### Tasks
- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get single task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Toggle completion status
- `DELETE /api/tasks/{id}` - Delete task

**Security**: User can only access their own tasks (user_id extracted from JWT).

---

## Project Structure

### Backend (`/backend`)

```
backend/
├── src/
│   ├── models/           # SQLModel entities (User, Task)
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic (user, task services)
│   ├── routers/          # API endpoints (auth, tasks)
│   ├── middleware/       # JWT verification, CORS, error handling
│   ├── utils/            # Security helpers (bcrypt, JWT)
│   ├── config.py         # Environment configuration
│   ├── database.py       # Database connection
│   ├── init_db.py        # Database initialization
│   └── main.py           # FastAPI app entry point
├── requirements.txt
├── .env.example
└── README.md
```

### Frontend (`/frontend`)

```
frontend/
├── app/
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Landing page
│   ├── signin/page.tsx       # Sign in page
│   ├── signup/page.tsx       # Sign up page
│   └── dashboard/page.tsx    # Protected dashboard
├── components/
│   ├── Header.tsx            # Navigation with logout
│   ├── TaskForm.tsx          # Add task form
│   ├── TaskList.tsx          # Task list container
│   ├── TaskItem.tsx          # Single task component
│   └── EmptyState.tsx        # Empty state message
├── lib/
│   ├── types.ts              # TypeScript interfaces
│   └── api-client.ts         # API fetch wrapper
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.js
```

---

## Testing

### Manual Acceptance Testing

Test scenarios in `specs/002-phase2-fullstack-web/quickstart.md`:

1. **Authentication**: Sign up → Sign in → Logout
2. **Add Task**: Create task with title and description
3. **View Tasks**: View task list (empty and populated states)
4. **Toggle Status**: Mark tasks complete/incomplete
5. **Update Task**: Edit task title and/or description
6. **Delete Task**: Remove tasks permanently

### User Isolation Test

1. Create first user account → Add tasks
2. Logout → Create second user account
3. Verify second user sees empty list (not first user's tasks)
4. Logout and sign back in as first user
5. Verify only original tasks are visible

---

## Troubleshooting

### Backend Issues

**`ModuleNotFoundError`**: Activate venv and run `pip install -r requirements.txt`

**Database connection failed**: Verify `DATABASE_URL` in `.env` is correct

**CORS error**: Ensure `ALLOWED_ORIGINS=http://localhost:3000` in backend `.env`

### Frontend Issues

**401 Unauthorized**: Verify `BETTER_AUTH_SECRET` matches in both `.env` files

**Tasks not persisting**: Check backend server is running and database initialized

---

## Documentation

### Phase II Documentation
- [Specification](specs/002-phase2-fullstack-web/spec.md)
- [Implementation Plan](specs/002-phase2-fullstack-web/plan.md)
- [Task Breakdown](specs/002-phase2-fullstack-web/tasks.md)
- [Data Model](specs/002-phase2-fullstack-web/data-model.md)
- [API Contracts](specs/002-phase2-fullstack-web/contracts/api-spec.yaml)
- [Quickstart Guide](specs/002-phase2-fullstack-web/quickstart.md)

### Phase I Documentation
- [Specification](specs/001-phase1-cli-todo/spec.md)
- [Quickstart](specs/001-phase1-cli-todo/quickstart.md)

---

## Phase Evolution

### Phase I → Phase II Changes

**Architecture**:
- Console → Web interface
- In-memory → PostgreSQL persistence
- Single-user → Multi-user with authentication
- Monolithic → Client-server architecture

**Preserved Concepts**:
- Task model (ID, title, description, status)
- CRUD operations
- Validation rules (non-empty titles)

**New Capabilities**:
- User accounts
- JWT-based API security
- Responsive web UI
- Cloud database
- Cross-device access

---

## Development Workflow

This project follows **Spec-Driven Development (SDD)**:

1. `/sp.specify` - Create feature specification
2. `/sp.clarify` - Resolve ambiguities
3. `/sp.plan` - Design architecture
4. `/sp.tasks` - Generate task breakdown
5. `/sp.implement` - Execute implementation

All specifications in `/specs` directory.

---

**Last Updated**: 2025-12-27
**Current Phase**: II
**Status**: MVP Complete
