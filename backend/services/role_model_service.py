from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.role_model import RoleModel
from backend.database.models.lesson import Lesson
from backend.database.models.lesson_tag import LessonTag
from backend.database.models.tag import Tag
from backend.database.models.role_model_tag_score import RoleModelTagScore
from backend.database.models.book import Book
from data.models import RoleModelResponse


def get_or_create_tag(session: Session, tag_name: str) -> Tag:

    statement = select(Tag).where(
        Tag.name == tag_name
    )

    tag = session.scalars(statement).first()

    if tag is None:
        tag = Tag(name=tag_name)
        session.add(tag)
        session.flush()

    return tag

def create_role_model(session: Session, role_model_profile: RoleModelResponse) -> RoleModel:

    role_model = RoleModel(
        name=role_model_profile.name,
        fun_fact=role_model_profile.fun_fact
    )

    session.add(role_model)
    session.flush()

    # Book
    book = Book(
        title=role_model_profile.book_recommendation.title,
        author=role_model_profile.book_recommendation.author,
        role_model_id=role_model.id
    )

    session.add(book)

    # Lessons
    for lesson_data in role_model_profile.lessons:

        lesson = Lesson(
            lesson=lesson_data.lesson,
            role_model_id=role_model.id
        )

        session.add(lesson)
        session.flush()

        for tag_name in lesson_data.tags:
            tag = get_or_create_tag(session, tag_name)

            lesson_tag = LessonTag(
                lesson_id=lesson.id,
                tag_id=tag.id
            )

            session.add(lesson_tag)

    # Tag scores
    for score_data in role_model_profile.tag_scores:

        tag = get_or_create_tag(
            session,
            score_data.tag
        )

        tag_score = RoleModelTagScore(
            role_model_id=role_model.id,
            tag_id=tag.id,
            score=score_data.score,
            reason=score_data.reason
        )

        session.add(tag_score)

    session.commit()
    session.refresh(role_model)

    return role_model

def get_role_model_names(session: Session) -> list[str]:
    statement = select(RoleModel.name)

    return list(session.scalars(statement).all())

def get_role_model(session: Session, role_model_id: int) -> RoleModel | None:

    statement = select(RoleModel).where(
        RoleModel.id == role_model_id
    )

    return session.scalars(statement).first()


def get_role_models_by_tag(session: Session, tag_name: str) -> list[RoleModel]:

    statement = (
        select(RoleModel)
        .join(RoleModelTagScore)
        .join(Tag)
        .where(Tag.name == tag_name)
    )

    return list(session.scalars(statement).all())


def delete_role_model(session: Session, role_model_id: int) -> bool:

    role_model = session.get(RoleModel, role_model_id)

    if role_model is None:
        return False

    try:
        session.delete(role_model)
        session.commit()
        return True

    except Exception:
        session.rollback()
        raise