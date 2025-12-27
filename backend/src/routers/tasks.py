"""
Task API routes for CRUD operations.
All endpoints require JWT authentication and enforce user isolation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_db
from src.middleware.jwt import get_current_user
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task import TaskService
from uuid import UUID
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all tasks for the authenticated user.

    Args:
        user_id: Current user's UUID (from JWT)
        db: Database session

    Returns:
        List of tasks owned by the user
    """
    tasks = TaskService.list_tasks(user_id, db)
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        user_id: Current user's UUID (from JWT)
        db: Database session

    Returns:
        Created task

    Raises:
        HTTPException: 400 if validation fails
    """
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )

    task = TaskService.create_task(user_id, task_data, db)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single task by ID for the authenticated user.

    Args:
        task_id: Task ID
        user_id: Current user's UUID (from JWT)
        db: Database session

    Returns:
        Task data

    Raises:
        HTTPException: 404 if task not found or belongs to another user
    """
    task = TaskService.get_task(task_id, user_id, db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing task for the authenticated user.

    Args:
        task_id: Task ID
        task_data: Updated task data
        user_id: Current user's UUID (from JWT)
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 400 if validation fails, 404 if task not found
    """
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )

    task = TaskService.update_task(task_id, user_id, task_data, db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task for the authenticated user.

    Args:
        task_id: Task ID
        user_id: Current user's UUID (from JWT)
        db: Database session

    Raises:
        HTTPException: 404 if task not found or belongs to another user
    """
    success = TaskService.delete_task(task_id, user_id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_status(
    task_id: int,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle task completion status for the authenticated user.

    Args:
        task_id: Task ID
        user_id: Current user's UUID (from JWT)
        db: Database session

    Returns:
        Updated task with toggled status

    Raises:
        HTTPException: 404 if task not found or belongs to another user
    """
    task = TaskService.toggle_status(task_id, user_id, db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
