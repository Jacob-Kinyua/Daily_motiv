from pydantic import BaseModel, EmailStr
from datetime import datetime

class RecommendationCreatedResponse(BaseModel):
    recommendation_id: int
    role_model_id: int
    email_sent: bool


class PastRecommendationResponse(BaseModel):
    id: int
    person_name: str
    person_title: str | None
    sent_at: datetime
    fun_fact: str | None
    lessons: list[str]