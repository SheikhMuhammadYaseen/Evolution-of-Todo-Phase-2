"""
Database initialization script.
Run this before starting the application to create tables.
"""
from src.database import init_db
# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task

if __name__ == "__main__":
    print("Initializing database schema...")
    init_db()
    print("Database initialization complete!")
