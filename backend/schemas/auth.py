from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str


class VerifyCodeRequest(BaseModel):
    email: str
    code: str