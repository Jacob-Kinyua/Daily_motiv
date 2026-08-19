from pydantic import BaseModel
from enum import Enum

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

class TagScore(BaseModel):
    tag: str
    score: int
    reason: str

class ScoreResponse(BaseModel):
    tag_scores: list[TagScore]


class UserResponse(BaseModel):
    subject: str
    body: str


    


