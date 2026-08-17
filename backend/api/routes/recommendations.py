from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_session
from backend.schemas.recommendation import RecommendationResponse
from backend.services.recommendation_service import generate_and_send_recommendation, get_user_recommendations
from pydantic import BaseModel
from datetime import datetime


class RecommendationResponse(BaseModel):
    id: int
    role_model_id: int
    reason: str
    recommended_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# generate a recommendation and send it to the users email
@router.post("/{user_id}")
def create_recommendation(
    user_id: int,
    session: Session = Depends(get_session)
):
    return generate_and_send_recommendation(
        session,
        user_id
    )

# fetch all users past recommendations
@router.get(
    "/{user_id}",
    response_model=list[RecommendationResponse]
)
def get_my_recommendations(
    user_id: int,
    session: Session = Depends(get_session)
):
    return get_user_recommendations(
        session,
        user_id
    )