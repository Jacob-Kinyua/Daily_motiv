from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    occupation: str
    goals: list[str]
    interests: list[str]
    career_stage: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    occupation: str
    career_stage: str
    goals: list[str]
    interests: list[str]

    model_config = ConfigDict(from_attributes=True)




class UserUpdate(BaseModel):
    name: Optional[str] = None
    occupation: Optional[str] = None
    goals: Optional[list[str]] = None
    career_stage: Optional[str] = None
    interests: Optional[list[str]] = None