from dataclasses import dataclass

import httpx
import pytest
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.settings import Settings
from app.users.auth.schema import GoogleUserData


faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient
    _user_data: GoogleUserData  # inject test data

    async def get_user_info(self, code: str) -> GoogleUserData:
        # return injected data, do not call fixtures here
        return self._user_data

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake-access-token {code}"


@pytest.fixture
def google_client(google_user_info_data):
    return FakeGoogleClient(
        settings=Settings(),
        async_client=httpx.AsyncClient(),
        _user_data=google_user_info_data,
    )


@pytest.fixture
def google_user_info_data() -> GoogleUserData:
    from tests.fixtures.users.user_model import (
        EXISTS_GOOGLE_USER_EMAIL,
        EXISTS_GOOGLE_USER_ID,
    )

    return GoogleUserData(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL,
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256(),
    )
