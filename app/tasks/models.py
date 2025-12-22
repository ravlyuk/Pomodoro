from typing import Any
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.infrastructure.database import Base


class TasksModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfiles.id"), nullable=False)


class CategoriesModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    type: Mapped[str]
    name: Mapped[str]
