"""
Pydantic schemas for Task API requests and responses.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)


class TaskResponse(BaseModel):
    """Schema for task data in API responses."""
    id: int
    user_id: UUID
    title: str
    description: Optional[str]
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
