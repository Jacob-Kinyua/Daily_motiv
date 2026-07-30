from pydantic import BaseModel

class Person(BaseModel):
    name: str
    reason: str

class Lesson(BaseModel):
    lesson: str
    tags: list[str]

class BookRecommendation(BaseModel):
    title: str
    author: str

class ResearchResponse(BaseModel):
    fun_fact: str
    lessons: list[Lesson]
    book_recommendation: BookRecommendation