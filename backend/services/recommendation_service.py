from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from backend.database.models.role_model import RoleModel
from backend.database.models.user import User
from backend.database.models.recommendation import Recommendation
from backend.database.models.tag import Tag
from backend.database.models.role_model_tag_score import RoleModelTagScore
from .role_model_service import get_role_model
from backend.constansts.tags import AVAILABLE_TAGS
from backend.prompts.find_person import choose_person
from backend.prompts.research_person import research_person
from backend.prompts.score_person import score_person
from backend.schemas.role_model import RoleModelResponse
from .role_model_service import get_role_model_names, create_role_model
from backend.prompts.curate_response import curate_response
from backend.services.generate_email import send_email
from backend.schemas.recommendation import RecommendationCreatedResponse, PastRecommendationResponse



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


def get_user_recommendations(
    session: Session,
    user_id: int
):
    statement = (
        select(Recommendation)
        .where(Recommendation.user_id == user_id)
        .order_by(desc(Recommendation.recommended_at))
    )

    recommendations = list(session.scalars(statement).all())

    return [
        PastRecommendationResponse(
            id=rec.id,
            person_name=rec.role_model.name,
            person_title=None,
            sent_at=rec.recommended_at,
            fun_fact=rec.role_model.fun_fact,
            lessons=[
                lesson.lesson
                for lesson in rec.role_model.lessons
            ],
        )
        for rec in recommendations
    ]


def generate_new_role_model(user, existing_people):
    person = choose_person(user, existing_people)

    person_details = research_person(
        person,
        AVAILABLE_TAGS
    )

    person_score = score_person(
        person,
        AVAILABLE_TAGS
    )

    role_model = RoleModelResponse(
        name=person.name,
        fun_fact=person_details.fun_fact,
        lessons=person_details.lessons,
        book_recommendation=person_details.book_recommendation,
        tag_scores=person_score.tag_scores
    )

    return role_model


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


# return a recommendation for a user
def generate_recommendation(session: Session, user_id: int):

    user = session.get(User, user_id)

    if user is None:
        return None

    # 1. Find unseen RoleModels relevant to the user
    candidates = get_unseen_role_models(
        session,
        user
    )

    # 2. Select an existing RoleModel if possible
    if candidates:
        ranked = rank_role_models(
            session,
            user,
            candidates
        )

        selected = select_role_model(ranked)

        if selected is None:
            return None

        role_model = get_role_model(
            session,
            selected["role_model_id"]
        )

    # 3. Otherwise generate a new RoleModel
    else:
        existing_people = get_role_model_names(session)

        role_model_profile = generate_new_role_model(
            user,
            existing_people
        )

        role_model = create_role_model(
            session,
            role_model_profile
        )

    # 4. Create the Recommendation record
    recommendation = create_recommendation(
        session,
        user_id=user.id,
        role_model_id=role_model.id,
        reason="Recommended based on your interests."
    )

    return recommendation



# send a recommendation
def generate_and_send_recommendation(
    session: Session,
    user_id: int
):

    user = session.get(User, user_id)

    if user is None:
        return None

    recommendation = generate_recommendation(
        session,
        user_id
    )

    if recommendation is None:
        return None

    role_model = get_role_model(
        session,
        recommendation.role_model_id
    )

    if role_model is None:
        return None

    response = curate_response(
        user,
        recommendation
    )

    sent = send_email(
        user.email,
        response.subject,
        response.body
    )

    return RecommendationCreatedResponse(
        recommendation_id=recommendation.id,
        role_model_id=recommendation.role_model_id,
        email_sent=sent
    )