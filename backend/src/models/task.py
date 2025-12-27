"""
Task model for todo items.
Each task belongs to a specific user.
"""
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique integer identifier (auto-incremented)
        user_id: Foreign key to User (enforces ownership)
        title: Task name/summary (mandatory, max 500 chars)
        description: Optional detailed description (max 10000 chars)
        status: Completion status (False=incomplete, True=complete)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
