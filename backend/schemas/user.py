from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    occupation: str
    goals: list[str]
    interests: list[str]
    hobbies: list[str]
    career_stage: str