from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from backend.database.models.role_model import RoleModel
from backend.database.models.user import User
from backend.database.models.recommendation import Recommendation
from backend.database.models.tag import Tag
from backend.database.models.role_model_tag_score import RoleModelTagScore
from .role_model_service import get_role_model


def create_recommendation(session: Session, user_id: int, role_model_id: int, reason: str) -> Recommendation:

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


def get_user_recommendations(session: Session, user_id: int) -> list[Recommendation]:

    statement = (
        select(Recommendation)
        .where(Recommendation.user_id == user_id)
        .order_by(desc(Recommendation.recommended_at))
    )

    return list(session.scalars(statement).all())


# sums different role models score across different tags and returns 
# them from the highest rank
def rank_role_models(session: Session, user: User, role_models: list[RoleModel]):
    rankings = []

    for role_model in role_models:

        statement = (
            select(RoleModelTagScore)
            .join(Tag)
            .where(
                RoleModelTagScore.role_model_id == role_model.id,
                Tag.name.in_(user.interests)
            )
        )

        scores = session.scalars(statement).all()

        total_score = sum(score.score for score in scores)

        rankings.append({
            "role_model_id": role_model.id,
            "score": total_score
        })

    return sorted(
        rankings,
        key=lambda x: x["score"],
        reverse=True
    )

def select_role_model(ranked_role_models):
    if not ranked_role_models:
        return None

    return ranked_role_models[0]


def get_unseen_role_models(session: Session, user: User) -> list[RoleModel]:

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
    )

    return  list(session.scalars(statement).unique().all())


# returns the highest ranked role model not recomended to the user yet
def recommend_role_model(session: Session, user: User):

    candidates = get_unseen_role_models(session,user)

    ranked = rank_role_models(session,user,candidates)

    selected = select_role_model(ranked)

    if selected is None:
        return None

    return get_role_model(session,selected["role_model_id"])

