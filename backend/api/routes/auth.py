from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from backend.services.security import create_access_token, get_current_user
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

    access_token = create_access_token(user.id)

    response = JSONResponse(
        content={
            "message": "Login successful",
            "user_id": user.id
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,      # True when using HTTPS in production
        samesite="lax",
        max_age=60 * 60
    )

    return response

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}