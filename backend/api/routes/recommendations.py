from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_session
from backend.database.models.user import User
from backend.services.security import get_current_user
from backend.schemas.recommendation import RecommendationCreatedResponse, PastRecommendationResponse

from backend.services.recommendation_service import (
    generate_and_send_recommendation,
    get_user_recommendations
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# Generate a recommendation and send it to the user's email
@router.post(
    "/me",
    response_model=RecommendationCreatedResponse
)
def create_recommendation(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return generate_and_send_recommendation(
        session,
        current_user.id
    )


# Fetch the current user's past recommendations
@router.get(
    "/me",
    response_model=list[PastRecommendationResponse]
)
def get_my_recommendations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_recommendations(
        session,
        current_user.id
    )