

"""
    Columns:
        name
        reason
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

from database.base import Base

class RoleModel(Base):

    __tablename__ = "role_models"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    fun_fact: Mapped[str] = mapped_column(String(200))

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="role_model"
    )

    