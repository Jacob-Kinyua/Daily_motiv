
"""
    Columns:
        name
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON

from database.base import Base

class Tag(Base):

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    lesson_tags: Mapped[list["LessonTag"]] = relationship(
        back_populates="tag"
    )