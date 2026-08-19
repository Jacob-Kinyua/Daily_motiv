from pydantic import BaseModel
from backend.data.models import Lesson, BookRecommendation, TagScore

class RoleModelResponse(BaseModel):
    name: str
    fun_fact: str
    lessons: list[Lesson]
    book_recommendation: BookRecommendation
    tag_scores: list[TagScore]