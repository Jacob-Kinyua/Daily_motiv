from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate
from backend.services import user_service
from backend.database.session import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    return user_service.create_user(
        session,
        user_data
    )