
"""
    id
    lesson_id
    tag_id
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class LessonTag(Base):

    __tablename__ = "lesson_tags"

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        primary_key=True
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="lesson_tags"
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="lesson_tags"
    )