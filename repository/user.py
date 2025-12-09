from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import UserProfileModel


@dataclass
class UserRepository:
    db_session: Session  # Replace 'any' with the actual Session type

    def create_user(
        self, username: str, password: str, access_token: str
    ) -> UserProfileModel | None:
        query = (
            insert(UserProfileModel)
            .values(username=username, password=password, access_token=access_token)
            .returning(UserProfileModel.id)
        )

        with self.db_session as session:
            user_id: int = session.execute(query).scalar_one()
            session.commit()
            session.flush()

            return self.get_user(user_id)

    def get_user(self, user_id: int) -> UserProfileModel | None:
        query = select(UserProfileModel).where(UserProfileModel.id == user_id)

        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfileModel | None:
        query = select(UserProfileModel).where(UserProfileModel.username == username)

        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()
