

"""
    Columns:
        name
        reason
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base


class RoleModel(Base):

    __tablename__ = "role_models"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    fun_fact: Mapped[str] = mapped_column(String(200))

    # One RoleModel → many Lessons
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="role_model",
        cascade="all, delete-orphan"
    )

    # One RoleModel → one Book
    book: Mapped["Book"] = relationship(
        back_populates="role_model",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # One RoleModel → many Recommendations
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="role_model"
    )

    # One RoleModel → many RoleModelTagScores
    tag_scores: Mapped[list["RoleModelTagScore"]] = relationship(
        back_populates="role_model",
        cascade="all, delete-orphan"
    )