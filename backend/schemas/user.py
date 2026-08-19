from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    occupation: str
    goals: list[str]
    interests: list[str]
    career_stage: str