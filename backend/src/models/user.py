"""
User model for authentication.
Stores user credentials and account information.
"""
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User entity representing an authenticated application user.

    Attributes:
        id: Unique UUID identifier
        email: Unique email address for authentication
        password_hash: Bcrypt-hashed password
        created_at: Account creation timestamp
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
