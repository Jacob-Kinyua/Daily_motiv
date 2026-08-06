
"""
    Columns:
        id
        title
        author
        role_model_id
"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

class Book(Base):

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200))

    author: Mapped[str] = mapped_column(String(100))

    role_model_id: Mapped[int] = mapped_column(
        ForeignKey("role_models.id"),
        unique=True
    )

    role_model: Mapped["RoleModel"] = relationship(
        back_populates="book_recommendation"
    )

