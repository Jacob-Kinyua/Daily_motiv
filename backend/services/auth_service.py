import secrets
from datetime import datetime, timedelta

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from backend.database.models.user import User
from backend.database.models.authcode import AuthCode


def generate_verification_code():
    return f"{secrets.randbelow(1_000_000):06d}"

import secrets
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.user import User
from backend.database.models.authcode import AuthCode


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
        expires_at=datetime.utcnow() + timedelta(minutes=10),
        used=False,
    )

    session.add(auth_code)
    session.commit()

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
        return None

    auth_code = session.execute(
        select(AuthCode).where(
            AuthCode.user_id == user.id,
            AuthCode.code == code,
            AuthCode.used == False
        )
    ).scalar_one_or_none()

    if auth_code is None:
        return None

    if auth_code.expires_at < datetime.utcnow():
        return None

    auth_code.used = True

    session.commit()

    return user