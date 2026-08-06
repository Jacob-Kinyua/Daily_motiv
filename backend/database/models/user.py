
"""
Columns:
    name
    occupation
    goals
    interests
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

from database.base import Base

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    occupation: Mapped[str] = mapped_column(String(100))

    goals: Mapped[list[str]] = mapped_column(JSON)

    interests: Mapped[list[str]] = mapped_column(JSON)

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="user"
    )
