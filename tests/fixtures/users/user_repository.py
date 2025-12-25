from dataclasses import dataclass

import pytest
import pytest_asyncio

from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self, email: str) -> None: ...

    async def create_user(self, user_data: UserCreateSchema) -> UserLoginSchema:
        from tests.fixtures.users.user_model import UserProfileFactory

        return UserProfileFactory()


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()


@pytest_asyncio.fixture
async def user_repository(db_session):
    """Real UserRepository fixture with test database session."""
    return UserRepository(db_session=db_session)
