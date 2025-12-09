from typing import Any
from sqlalchemy.orm import (
    DeclarativeMeta,
    Mapped,
    mapped_column,
    declarative_base,
    DeclarativeBase,
    declared_attr,
)


class Base(DeclarativeBase):
    pass


class TasksModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]


class CategoriesModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    type: Mapped[str]
    name: Mapped[str]
