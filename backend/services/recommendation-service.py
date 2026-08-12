from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from backend.database.models.role_model import RoleModel
from backend.database.models.user import User
from backend.database.models.recommendation import Recommendation
from backend.database.models.tag import Tag
from backend.database.models.role_model_tag_score import RoleModelTagScore


def create_recommendation(
    session: Session,
    user_id: int,
    role_model_id: int,
    reason: str
) -> Recommendation:

    recommendation = Recommendation(
        user_id=user_id,
        role_model_id=role_model_id,
        reason=reason,
        recommended_at=datetime.now()
    )

    session.add(recommendation)
    session.commit()
    session.refresh(recommendation)

    return recommendation


def get_recommendation(
    session: Session,
    recommendation_id: int
) -> Recommendation | None:

    statement = select(Recommendation).where(
        Recommendation.id == recommendation_id
    )

    return session.scalars(statement).first()


def get_user_recommendations(
    session: Session,
    user_id: int
) -> list[Recommendation]:

    statement = (
        select(Recommendation)
        .where(Recommendation.user_id == user_id)
        .order_by(desc(Recommendation.recommended_at))
    )

    return list(session.scalars(statement).all())


# def rank_role_models(tags):
#     role_models = select(Role)


def get_unseen_role_models(
    session: Session,
    user: User,
    limit: int = 10
) -> list[RoleModel]:

    seen_role_models = (
        select(Recommendation.role_model_id)
        .where(Recommendation.user_id == user.id)
    )

    statement = (
        select(RoleModel)
        .join(RoleModelTagScore)
        .join(Tag)
        .where(
            Tag.name.in_(user.interests),
            ~RoleModel.id.in_(seen_role_models)
        )
        .limit(limit)
    )

    return list(session.scalars(statement).unique().all())