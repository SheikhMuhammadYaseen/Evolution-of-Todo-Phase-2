"""
Database configuration and session management.
Uses SQLModel for ORM and session dependency injection.
"""
from sqlmodel import SQLModel, create_engine, Session
from src.config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.log_level == "DEBUG",  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using
)


def get_db():
    """
    Database session dependency for FastAPI.
    Yields a session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize database schema.
    Creates all tables defined by SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")
