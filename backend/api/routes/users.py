from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate
from backend.services.user_service import create_user, delete_user, get_user_by_id
from backend.database.session import get_session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{user_id}")
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    return get_user_by_id(
        session,
        user_id
    )


# saves user profile
@router.post("/")
def save_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    return create_user(
        session,
        user_data
    )

@router.delete("/{user_id}")
def delete_user_route(
    user_id: int,
    session: Session = Depends(get_session)
):
    return delete_user(
        session,
        user_id
    )