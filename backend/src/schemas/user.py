"""
Pydantic schemas for User API requests and responses.
"""
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in API responses (excludes password_hash)."""
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
