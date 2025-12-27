"""
JWT authentication middleware.
Extracts and validates JWT tokens, provides current user dependency.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.security import decode_access_token
from uuid import UUID

# Security scheme for JWT bearer tokens
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    """
    Extract and validate JWT token, return user_id.

    This dependency is used on protected routes to ensure authentication
    and extract the current user's ID from the JWT token.

    Args:
        credentials: HTTP Authorization header with Bearer token

    Returns:
        UUID of authenticated user

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    token = credentials.credentials

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
