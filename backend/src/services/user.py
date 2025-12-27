"""
User service for account management operations.
"""
from sqlmodel import Session, select
from src.models.user import User
from src.utils.security import hash_password, verify_password
from typing import Optional


class UserService:
    """Business logic for user operations."""

    @staticmethod
    def create_user(email: str, password: str, db: Session) -> User:
        """
        Create a new user account with hashed password.

        Args:
            email: User's email address
            password: Plain text password
            db: Database session

        Returns:
            Created User instance

        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing_user = db.exec(
            select(User).where(User.email == email)
        ).first()

        if existing_user:
            raise ValueError("Email already registered")

        # Hash password and create user
        hashed_password = hash_password(password)
        user = User(email=email, password_hash=hashed_password)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_email(email: str, db: Session) -> Optional[User]:
        """
        Retrieve user by email address.

        Args:
            email: User's email address
            db: Database session

        Returns:
            User instance if found, None otherwise
        """
        return db.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def verify_credentials(email: str, password: str, db: Session) -> Optional[User]:
        """
        Verify user credentials for authentication.

        Args:
            email: User's email address
            password: Plain text password
            db: Database session

        Returns:
            User instance if credentials valid, None otherwise
        """
        user = UserService.get_user_by_email(email, db)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
