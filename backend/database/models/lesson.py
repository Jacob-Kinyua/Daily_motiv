

"""
    Columns:
        lesson
        tag_id
        role_model_id
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

class Lesson(Base):

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    lesson: Mapped[str] = mapped_column(String(500))

    role_model_id: Mapped[int] = mapped_column(
        ForeignKey("role_models.id")
    )

    role_model: Mapped["RoleModel"] = relationship(
        back_populates="lessons"
    )

    lesson_tags: Mapped[list["LessonTag"]] = relationship(
        back_populates="lesson"
    )