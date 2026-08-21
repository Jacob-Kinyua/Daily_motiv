from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate, UserResponse, UserUpdate

from backend.services.user_service import (
    create_user,
    delete_user,
    update_user
)

from backend.database.session import get_session
from backend.database.models.user import User
from backend.services.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Get currently authenticated user
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# Create a new user
# This remains PUBLIC
@router.post("/", response_model=UserResponse)
def save_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    return create_user(
        session,
        user_data
    )


# Update currently authenticated user
@router.put("/me", response_model=UserResponse)
def change_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return update_user(
        session,
        current_user.id,
        user_data
    )


# Delete currently authenticated user
@router.delete("/me")
def unsubscribe_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return delete_user(
        session,
        current_user.id
    )