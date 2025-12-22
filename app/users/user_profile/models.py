from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.infrastructure.database import Base


class UserProfileModel(Base):
    __tablename__ = "UserProfiles"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    google_access_token: Mapped[str | None]
    email: Mapped[str | None]
    name: Mapped[str | None]
