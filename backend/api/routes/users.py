from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate
from backend.services.user_service import create_user, delete_user
from backend.database.session import get_session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# saves user profile
@router.post("/")
def create_user(
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