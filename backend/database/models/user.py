
"""
Columns:
    name
    occupation
    goals
    interests
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON

from backend.database.base import Base

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    occupation: Mapped[str] = mapped_column(String(100))

    career_stage: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    goals: Mapped[list[str]] = mapped_column(JSON)

    interests: Mapped[list[str]] = mapped_column(JSON)

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    auth_codes = relationship(
        "AuthCode",
        back_populates="user",
        cascade="all, delete-orphan"
    )
