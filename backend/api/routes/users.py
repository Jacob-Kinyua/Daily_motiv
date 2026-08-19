from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate, UserResponse
from backend.services.user_service import (
    create_user,
    delete_user,
    get_user_by_id,
    update_user
)
from backend.database.session import get_session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    return get_user_by_id(
        session,
        user_id
    )


@router.post("/", response_model=UserResponse)
def save_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    return create_user(
        session,
        user_data
    )


@router.put("/{user_id}")
def change_user_infe(
    user_id: int,
    session: Session = Depends(get_session)
):
    return update_user(
        session,
        user_id
    )


@router.delete("/{user_id}")
def unsubscribe_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    return delete_user(
        session,
        user_id
    )