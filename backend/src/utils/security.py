"""
Security utilities for password hashing and JWT operations.
"""
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from src.config import settings
from typing import Optional
from uuid import UUID


# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: UUID) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User's UUID

    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    to_encode = {
        "sub": str(user_id),  # Subject (user_id)
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.better_auth_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[UUID]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string

    Returns:
        User UUID if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token, settings.better_auth_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None
        return UUID(user_id_str)
    except JWTError:
        return None
