from datetime import datetime as dt, timezone, timedelta

import pytest
from jose import jwt

from app.settings import Settings
from app.users.auth.clients.google import GoogleClient
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.auth.clients import google_user_info_data
from tests.fixtures.infrastructure import settings

pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url__success(
    mock_auth_service: AuthService, settings: Settings
):
    settings_google_redirect_url = settings.google_redirect_url
    mock_auth_service_google_redirect_url = mock_auth_service.get_google_redirect_url()
    assert mock_auth_service_google_redirect_url == settings_google_redirect_url


async def test_get_google_redirect_url__fail(mock_auth_service: AuthService):
    settings_google_redirect_url = "http://invalid-redirect-url.com"
    mock_auth_service_google_redirect_url = mock_auth_service.get_google_redirect_url()
    assert mock_auth_service_google_redirect_url != settings_google_redirect_url


async def test_generate_access_token__success(
    mock_auth_service: AuthService,
    settings: Settings,
):
    user_id = "1"

    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decode_access_token = jwt.decode(
        access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ENCODE_ALGORITHM],
    )

    expire_timestamp = decode_access_token.get("expire")
    assert expire_timestamp is not None, "Token should have an expiration timestamp"
    decoded_token_expire = dt.fromtimestamp(expire_timestamp, tz=timezone.utc)

    assert decoded_token_expire - dt.now(tz=timezone.utc) > timedelta(days=6, hours=23)


async def test_get_user_id_from_access_token__success(
    mock_auth_service: AuthService,
):
    user_id = "1"
    access_token = mock_auth_service.generate_access_token(user_id=user_id)

    extracted_user_id = mock_auth_service.get_user_id_from_access_token(
        access_token=access_token
    )

    assert extracted_user_id == user_id
 

async def test_google_auth__success(
    mock_auth_service: AuthService, 
    google_client: GoogleClient,
    user_repository,
):

    user = await mock_auth_service.google_auth(code="code")
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert isinstance(user, UserLoginSchema)
    assert user.user_id == decoded_user_id
