

"""
    Columns:
        tag_id
        role_model_id
        score
        reason
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

class RoleModelTagScore(Base):

    __tablename__ = "role_model_tag_scores"

    role_model_id: Mapped[int] = mapped_column(
        ForeignKey("role_models.id"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        primary_key=True
    )

    score: Mapped[int] = mapped_column()

    reason: Mapped[str] = mapped_column(String(300))

    role_model: Mapped["RoleModel"] = relationship(
        back_populates="tag_scores"
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="role_model_scores"
    )