# Todo Frontend (Next.js)

Phase II frontend for the Evolution of Todo project.

## Prerequisites

- Node.js 20 or higher
- Backend server running on http://localhost:8000

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local` and set:
   - `NEXT_PUBLIC_API_URL`: `http://localhost:8000`
   - `BETTER_AUTH_SECRET`: Same secret as backend
   - `BETTER_AUTH_URL`: `http://localhost:3000/api/auth`

3. **Start development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at http://localhost:3000

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── signup/              # Signup page
│   ├── signin/              # Signin page
│   ├── dashboard/           # Protected dashboard
│   └── api/auth/            # Better Auth routes
├── components/
│   ├── TaskList.tsx         # Task list display
│   ├── TaskItem.tsx         # Single task component
│   ├── TaskForm.tsx         # Add/edit task form
│   ├── Header.tsx           # Navigation header
│   └── EmptyState.tsx       # Empty state message
├── lib/
│   ├── auth.ts              # Better Auth configuration
│   ├── api-client.ts        # API fetch wrapper
│   └── types.ts             # TypeScript interfaces
└── package.json
```

## Testing

Manual acceptance testing per `specs/002-phase2-fullstack-web/quickstart.md`.

Automated tests deferred to Phase III.
