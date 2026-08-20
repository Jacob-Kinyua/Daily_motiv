from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_session
from backend.schemas.auth import LoginRequest, VerifyCodeRequest
from backend.services.auth_service import (
    request_login_code,
    verify_login_code
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    result = request_login_code(
        session,
        request.email
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user, code = result

    # temporarily return the code for testing
    return {
        "message": "Verification code generated",
        "user_id": user.id,
        "code": code
    }

@router.post("/verify")
def verify_code(
    request: VerifyCodeRequest,
    session: Session = Depends(get_session)
):
    user = verify_login_code(
        session,
        request.email,
        request.code
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired verification code"
        )

    return {
        "message": "Login successful",
        "user_id": user.id
    }