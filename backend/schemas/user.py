from pydantic import BaseModel, EmailStr, ConfigDict


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