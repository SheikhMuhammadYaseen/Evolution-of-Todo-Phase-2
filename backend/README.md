# Todo Backend (FastAPI)

Phase II backend for the Evolution of Todo project.

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL database account

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Generate with `openssl rand -hex 32`
   - `ALLOWED_ORIGINS`: `http://localhost:3000`

4. **Initialize database**:
   ```bash
   python -m src.init_db
   ```

5. **Start server**:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── models/         # SQLModel entities
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic
│   ├── routers/        # API endpoints
│   ├── middleware/     # JWT, CORS, error handling
│   ├── utils/          # Security helpers
│   ├── config.py       # Environment configuration
│   ├── database.py     # Database connection
│   ├── init_db.py      # Database initialization
│   └── main.py         # FastAPI app entry point
└── requirements.txt
```

## Testing

Manual acceptance testing per `specs/002-phase2-fullstack-web/quickstart.md`.

Automated tests deferred to Phase III.
