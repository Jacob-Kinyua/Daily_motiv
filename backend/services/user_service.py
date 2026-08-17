from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.user import User

def create_user(session, user_profile):
    user = User(
        name = user_profile.name,
        email = user_profile.email,
        occupation = user_profile.occupation,
        career_stage = user_profile.career_stage,
        goals = user_profile.goals,
        interests = user_profile.interests
    )

    session.add(user)
    session.commit()

    return user 


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)

    return session.scalars(statement).first()

def update_user(session: Session, user_id: int, **updates) -> User | None:

    user = session.get(User, user_id)

    if user is None:
        return None

    for field, value in updates.items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)

    return user

def delete_user(session: Session, user_id: int) -> bool:

    user = session.get(User, user_id)

    if user is None:
        return False

    session.delete(user)
    session.commit()

    return True