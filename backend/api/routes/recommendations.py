from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_session
from backend.schemas.recommendation import RecommendationResponse
from backend.services.recommendation_service import generate_recommendation

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/{user_id}")
def create_recommendation(
    user_id: int,
    session: Session = Depends(get_session)
):
    return generate_recommendation(
        session,
        user_id
    )