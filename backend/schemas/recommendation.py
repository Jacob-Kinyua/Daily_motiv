from pydantic import BaseModel, EmailStr


class RecommendationResponse(BaseModel):
    recommendation_id: int
    role_model_id: int
    email_sent: bool

