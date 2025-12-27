"""
Task service for CRUD operations.
All operations enforce user isolation by filtering with user_id.
"""
from sqlmodel import Session, select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class TaskService:
    """Business logic for task operations with user isolation."""

    @staticmethod
    def create_task(
        user_id: UUID, task_data: TaskCreate, db: Session
    ) -> Task:
        """
        Create a new task for the authenticated user.

        Args:
            user_id: UUID of task owner (from JWT)
            task_data: Task creation data
            db: Database session

        Returns:
            Created Task instance
        """
        task = Task(
            user_id=user_id,
            title=task_data.title.strip(),
            description=task_data.description.strip() if task_data.description else None,
            status=False,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def list_tasks(user_id: UUID, db: Session) -> List[Task]:
        """
        Retrieve all tasks for the authenticated user.

        Args:
            user_id: UUID of task owner (from JWT)
            db: Database session

        Returns:
            List of Task instances, ordered by creation date (newest first)
        """
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
        )
        tasks = db.exec(statement).all()
        return list(tasks)

    @staticmethod
    def get_task(task_id: int, user_id: UUID, db: Session) -> Optional[Task]:
        """
        Retrieve a single task by ID for the authenticated user.

        Args:
            task_id: Task ID
            user_id: UUID of task owner (from JWT)
            db: Database session

        Returns:
            Task instance if found and owned by user, None otherwise
        """
        statement = select(Task).where(
            Task.id == task_id, Task.user_id == user_id
        )
        return db.exec(statement).first()

    @staticmethod
    def update_task(
        task_id: int, user_id: UUID, task_data: TaskUpdate, db: Session
    ) -> Optional[Task]:
        """
        Update an existing task for the authenticated user.

        Args:
            task_id: Task ID
            user_id: UUID of task owner (from JWT)
            task_data: Updated task data
            db: Database session

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = TaskService.get_task(task_id, user_id, db)

        if not task:
            return None

        task.title = task_data.title.strip()
        task.description = task_data.description.strip() if task_data.description else None
        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def toggle_status(task_id: int, user_id: UUID, db: Session) -> Optional[Task]:
        """
        Toggle task completion status for the authenticated user.

        Args:
            task_id: Task ID
            user_id: UUID of task owner (from JWT)
            db: Database session

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = TaskService.get_task(task_id, user_id, db)

        if not task:
            return None

        task.status = not task.status
        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def delete_task(task_id: int, user_id: UUID, db: Session) -> bool:
        """
        Delete a task for the authenticated user.

        Args:
            task_id: Task ID
            user_id: UUID of task owner (from JWT)
            db: Database session

        Returns:
            True if task was deleted, False if not found
        """
        task = TaskService.get_task(task_id, user_id, db)

        if not task:
            return False

        db.delete(task)
        db.commit()

        return True
