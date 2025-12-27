"""
FastAPI application entry point.
Configures middleware, routes, and lifespan events.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import init_db
from src.middleware.cors import setup_cors
from src.middleware.errors import http_exception_handler
from fastapi.exceptions import HTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.
    Initializes database schema on startup.
    """
    # Startup
    print("Initializing database schema...")
    init_db()
    print("Application startup complete")

    yield

    # Shutdown
    print("Application shutdown")


# Create FastAPI application
app = FastAPI(
    title="Todo API - Phase II",
    description="Full-stack web todo application with multi-user support",
    version="2.0.0",
    lifespan=lifespan,
)

# Setup middleware
setup_cors(app)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get("/", tags=["Root"])
async def root():
    """Health check endpoint."""
    return {"message": "Todo API Phase II", "status": "running"}


@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check."""
    return {"status": "healthy", "phase": "II"}


# Import routers
from src.routers import auth, tasks

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
