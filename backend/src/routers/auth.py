"""
Authentication API routes for signup, signin, and logout.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_db
from src.schemas.user import UserCreate, UserResponse
from src.services.user import UserService
from src.utils.security import create_access_token

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    Args:
        user_data: Email and password
        db: Database session

    Returns:
        Created user data (without password)

    Raises:
        HTTPException: 400 if email already registered
    """
    try:
        user = UserService.create_user(user_data.email, user_data.password, db)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/signin")
def signin(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate user and issue JWT token.

    Args:
        user_data: Email and password
        db: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = UserService.verify_credentials(user_data.email, user_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }


@router.post("/logout")
def logout():
    """
    Logout endpoint (client-side token removal).

    In JWT-based auth, logout is primarily handled client-side by
    removing the token. This endpoint exists for API consistency.

    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}
