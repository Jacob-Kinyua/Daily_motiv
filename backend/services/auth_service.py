import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.user import User
from backend.database.models.authcode import AuthCode
from backend.services.generate_email import send_email


def generate_verification_code():
    return f"{secrets.randbelow(1_000_000):06d}"


def request_login_code(session: Session, email: str):

    user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return None

    code = generate_verification_code()

    auth_code = AuthCode(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        used=False,
    )

    session.add(auth_code)
    session.commit()

    send_email(
        user.email,
        "Your verification code",
        f"""
Your verification code is:

{code}

This code will expire in 10 minutes.

If you did not request this code, you can ignore this email.
"""
    )

    return user, code

def verify_login_code(
    session: Session,
    email: str,
    code: str
):
    user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        print("USER NOT FOUND")
        return None

    print("USER FOUND:", user.id)

    auth_code = session.execute(
        select(AuthCode).where(
            AuthCode.user_id == user.id,
            AuthCode.code == code,
            AuthCode.used == False
        )
    ).scalar_one_or_none()

    if auth_code is None:
        print("AUTH CODE NOT FOUND")
        return None

    print("CODE FROM USER:", repr(code))
    print("CODE FROM DB:", repr(auth_code.code))
    print("USED:", auth_code.used)
    print("EXPIRES:", auth_code.expires_at)
    print("EXPIRES TZ:", auth_code.expires_at.tzinfo)

    now = datetime.now(timezone.utc)

    expires_at = auth_code.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        return None

    auth_code.used = True

    session.commit()

    print("LOGIN CODE VERIFIED SUCCESSFULLY")

    return user