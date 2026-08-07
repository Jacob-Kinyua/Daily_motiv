
"""
    Columns:
        user_id
        role_model_id
        reason
"""

from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base


class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    role_model_id: Mapped[int] = mapped_column(
        ForeignKey("role_models.id")
    )

    reason: Mapped[str] = mapped_column(String(300))

    recommended_at: Mapped[datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(
        back_populates="recommendations"
    )

    role_model: Mapped["RoleModel"] = relationship(
        back_populates="recommendations"
    )