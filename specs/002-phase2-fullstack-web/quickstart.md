# Quickstart Guide: Phase II Full-Stack Web Todo Application

**Feature**: 002-phase2-fullstack-web
**Created**: 2025-12-27
**Audience**: Developers, testers, and stakeholders

## Overview

This guide provides step-by-step instructions to set up, run, and test the Phase II Full-Stack Web Todo Application locally. Phase II introduces multi-user support with authentication, persistent storage, and a responsive web interface.

**Architecture**:
- **Frontend**: Next.js 16+ (App Router) with Better Auth (JWT)
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens stored in httpOnly cookies

---

## Prerequisites

### Required Software

| Tool | Version | Installation |
|------|---------|--------------|
| **Node.js** | 20.x or higher | [nodejs.org](https://nodejs.org/) |
| **Python** | 3.11 or higher | [python.org](https://www.python.org/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |
| **PostgreSQL Client** (optional) | Latest | For direct database inspection |

### Neon Database Setup

1. Create a free account at [neon.tech](https://neon.tech/)
2. Create a new project named "todo-app-phase2"
3. Copy the connection string (format: `postgresql://user:password@ep-xxx.neon.tech/main?sslmode=require`)
4. Keep this connection string secure; you'll need it for environment variables

---

## Initial Setup

### 1. Clone Repository & Checkout Branch

```bash
git clone <repository-url>
cd todo
git checkout 002-phase2-fullstack-web
```

### 2. Generate Shared Secret

The `BETTER_AUTH_SECRET` must be identical in frontend and backend.

```bash
# Generate a secure 32-byte hex secret
openssl rand -hex 32
```

**Output example**: `a1b2c3d4e5f67890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890`

**IMPORTANT**: Copy this value; you'll use it in both `.env` files.

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected dependencies** (from `requirements.txt`):
- fastapi
- uvicorn[standard]
- sqlmodel
- psycopg2-binary (PostgreSQL driver)
- pyjwt (JWT handling)
- python-multipart (form data)
- pydantic-settings (environment variables)

### 4. Configure Environment Variables

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/main?sslmode=require

# Authentication
BETTER_AUTH_SECRET=<your-generated-secret-from-step-2>

# CORS (allow Next.js dev server)
ALLOWED_ORIGINS=http://localhost:3000

# Optional: Development settings
LOG_LEVEL=DEBUG
```

**Replace**:
- `DATABASE_URL` with your Neon connection string
- `BETTER_AUTH_SECRET` with the secret generated in step 2

### 5. Initialize Database Schema

```bash
python -m src.init_db
```

**Expected output**:
```
Creating database tables...
✓ User table created
✓ Task table created
Database initialization complete!
```

### 6. Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify backend**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in browser
- You should see the FastAPI Swagger UI with API endpoints

**Leave this terminal running** (backend server must stay active).

---

## Frontend Setup

### 1. Open New Terminal & Navigate to Frontend

```bash
cd frontend  # From repository root
```

### 2. Install Dependencies

```bash
npm install
```

**Expected dependencies** (from `package.json`):
- next (16.x)
- react (19.x)
- better-auth
- @better-auth/jwt (JWT plugin)
- TypeScript
- tailwindcss (for styling)

### 3. Configure Environment Variables

Create `frontend/.env.local`:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication (MUST match backend secret)
BETTER_AUTH_SECRET=<your-generated-secret-from-step-2>

# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3000/api/auth
```

**Replace**:
- `BETTER_AUTH_SECRET` with the SAME secret used in backend `.env`

### 4. Start Frontend Development Server

```bash
npm run dev
```

**Expected output**:
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- Ready in 2.5s
```

**Verify frontend**: Open [http://localhost:3000](http://localhost:3000) in browser
- You should see the signup/signin page

---

## First-Time Usage

### 1. Create Your First User Account

1. Open [http://localhost:3000](http://localhost:3000)
2. Click "Sign Up" (or navigate to `/signup`)
3. Enter email: `user@example.com`
4. Enter password: `SecurePass123!` (minimum 8 characters)
5. Click "Create Account"
6. You should see success message and be redirected to signin page

### 2. Sign In

1. Enter your email: `user@example.com`
2. Enter your password: `SecurePass123!`
3. Click "Sign In"
4. You should be redirected to the dashboard at `/dashboard`

### 3. Create Your First Task

1. On the dashboard, click "Add Task" button
2. Enter title: `Buy groceries`
3. Enter description: `Milk, eggs, bread` (optional)
4. Click "Create"
5. Task should appear in your task list with incomplete status (unchecked)

### 4. Manage Tasks

**View All Tasks**:
- All your tasks are displayed on the dashboard

**Mark Task Complete**:
- Click the checkbox next to the task
- Task should show checkmark and strikethrough (visual indicator)

**Mark Task Incomplete**:
- Click the checked checkbox again
- Task should return to unchecked state

**Edit Task**:
- Click "Edit" button on the task
- Modify title and/or description
- Click "Save"
- Changes should appear immediately

**Delete Task**:
- Click "Delete" button on the task
- Confirm deletion (if prompted)
- Task should disappear from the list

### 5. Test User Isolation

1. Sign out from current account
2. Create a second user account: `user2@example.com` / `AnotherPass123!`
3. Sign in as second user
4. You should see an empty task list (first user's tasks are NOT visible)
5. Create a task as second user
6. Sign out and sign back in as first user (`user@example.com`)
7. Verify you only see your original tasks (not second user's task)

**This confirms user isolation is working correctly!**

---

## Manual Acceptance Testing

Follow the scenarios from `specs/002-phase2-fullstack-web/spec.md` to validate all requirements.

### User Story 1: Registration & Authentication

**Test Scenarios**:
- [x] Sign up with valid email and password (8+ characters)
- [x] Sign in with correct credentials
- [x] Sign in with incorrect password (should show error)
- [x] Sign out (should redirect to signin page)
- [x] Access dashboard URL without authentication (should redirect to signin)

**Expected Results**: All scenarios pass per acceptance criteria in spec.md

---

### User Story 2: Add Task

**Test Scenarios**:
- [x] Add task with title and description
- [x] Add task with only title (no description)
- [x] Attempt to add task with empty title (should show validation error)
- [x] Verify another user cannot see your task

**Expected Results**: Tasks created successfully with correct data; validation works; user isolation enforced

---

### User Story 3: View Task List

**Test Scenarios**:
- [x] View task list with multiple tasks
- [x] View empty task list (should show "No tasks yet" message)
- [x] Refresh page (tasks should persist)
- [x] Sign in from different browser/device (should see same tasks)

**Expected Results**: Tasks display correctly; empty state shown when applicable; data persists across sessions

---

### User Story 4: Mark Complete/Incomplete

**Test Scenarios**:
- [x] Mark incomplete task as complete (checkbox checked, strikethrough)
- [x] Mark complete task as incomplete (checkbox unchecked, strikethrough removed)
- [x] Toggle status on one device, verify on another device (should sync)
- [x] Attempt to toggle another user's task via API manipulation (should return 403 Forbidden)

**Expected Results**: Status toggles correctly with visual feedback; changes persist; cross-user access blocked

---

### User Story 5: Update Task

**Test Scenarios**:
- [x] Update task title
- [x] Update task description only (preserve title)
- [x] Update both title and description
- [x] Attempt to save with empty title (should show validation error)
- [x] Attempt to edit another user's task via API (should return 403 Forbidden)

**Expected Results**: Updates save correctly; validation works; user isolation enforced

---

### User Story 6: Delete Task

**Test Scenarios**:
- [x] Delete a task (should remove from list)
- [x] Delete only task (should show empty state)
- [x] Attempt to delete another user's task via API (should return 403 Forbidden)
- [x] Verify deleted task cannot be recovered

**Expected Results**: Tasks delete permanently; user isolation enforced; no undo functionality

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem**: `Database connection failed`
**Solution**:
1. Verify `DATABASE_URL` in `backend/.env` is correct
2. Check Neon dashboard - ensure database is active
3. Test connection: `psql <DATABASE_URL>`

**Problem**: `CORS error` in browser console
**Solution**: Verify `ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:3000`

---

### Frontend Issues

**Problem**: `401 Unauthorized` on every API request
**Solution**:
1. Verify `BETTER_AUTH_SECRET` in `frontend/.env.local` matches `backend/.env`
2. Clear browser cookies and sign in again
3. Check browser dev tools → Application → Cookies for `auth_token`

**Problem**: "Cannot connect to backend" error
**Solution**:
1. Ensure backend server is running (`uvicorn` terminal)
2. Verify `NEXT_PUBLIC_API_URL=http://localhost:8000` in `frontend/.env.local`
3. Test backend health: `curl http://localhost:8000/health`

**Problem**: Tasks not persisting after page refresh
**Solution**:
1. Check backend terminal for database errors
2. Verify database connection (`DATABASE_URL` valid)
3. Ensure `init_db.py` ran successfully (tables created)

---

### General Issues

**Problem**: JWT token expires while using the application
**Solution**:
- Expected behavior in Phase II (token expiry set to 24 hours)
- Sign in again to get new token
- Token refresh mechanism deferred to Phase III

**Problem**: Changes on one browser/device not reflecting on another
**Solution**:
- Refresh the page on the second device (no real-time sync in Phase II)
- WebSocket-based live updates deferred to Phase III

---

## API Testing (Optional)

You can test the API directly using `curl` or Postman.

### 1. Get JWT Token

**Sign up**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'
```

**Sign in**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}' \
  -c cookies.txt  # Save cookies
```

**Extract JWT** from `cookies.txt` or response headers.

### 2. Test Task Endpoints

**List tasks**:
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Create task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'
```

**Get task**:
```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Update task**:
```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries and supplies","description":"Updated description"}'
```

**Toggle status**:
```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Delete task**:
```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

## Next Steps

After validating Phase II locally:

1. **Run full acceptance testing** using scenarios in spec.md
2. **Test edge cases**: JWT expiry, database failures, large task lists
3. **Verify security**: Attempt cross-user access, SQL injection (should be blocked)
4. **Review code quality**: Check generated code for consistency with plan.md
5. **Document findings**: Note any deviations from spec in test report

**Phase III Preview**: Advanced features (real-time updates, automated tests, password reset) will build on this foundation.

---

## Support & Resources

- **Specification**: `specs/002-phase2-fullstack-web/spec.md`
- **Implementation Plan**: `specs/002-phase2-fullstack-web/plan.md`
- **Data Model**: `specs/002-phase2-fullstack-web/data-model.md`
- **API Contracts**: `specs/002-phase2-fullstack-web/contracts/api-spec.yaml`
- **PHRs**: `history/prompts/002-phase2-fullstack-web/`

**Questions?** Review the spec and plan documents first, then consult the team.

---

**Last Updated**: 2025-12-27 | **Phase**: II | **Status**: Planning Complete, Ready for Implementation
