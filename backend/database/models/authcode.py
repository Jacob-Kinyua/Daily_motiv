from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.database.models.user import User


class AuthCode(Base):

    __tablename__ = "auth_codes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(6),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    used: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    user: Mapped["User"] = relationship()