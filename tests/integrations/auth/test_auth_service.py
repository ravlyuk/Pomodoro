import pytest
from sqlalchemy import insert, select
from app.users.auth.service import AuthService
from app.users.user_profile.models import UserProfileModel
from tests.fixtures.users.user_model import (
    EXISTS_GOOGLE_USER_EMAIL,
    EXISTS_GOOGLE_USER_ID,
)


@pytest.mark.asyncio
async def test_google_auth__login_not_exist_user(auth_service, get_db_session):
    code = "fake_code"

    async with get_db_session as session:
        users = (await session.execute(select(UserProfileModel))).scalars().all()
        session.expire_all()

    user = await auth_service.google_auth(code)

    assert len(users) == 0
    assert user is not None
    async with get_db_session as session:
        login_user = (
            (
                await session.execute(
                    select(UserProfileModel).where(UserProfileModel.id == user.user_id)
                )
            )
            .scalars()
            .first()
        )
        session.expire_all()

    assert login_user is not None


@pytest.mark.asyncio
async def test_google_auth__login_exist_user(auth_service, get_db_session):
    query = insert(UserProfileModel).values(
        id=EXISTS_GOOGLE_USER_ID, email=EXISTS_GOOGLE_USER_EMAIL
    )
    code = "fake_code"

    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
        user_data = await auth_service.google_auth(code)
        login_user = (
            await session.execute(
                select(UserProfileModel).where(UserProfileModel.id == user_data.user_id)
            )
        ).scalar_one_or_none()

    assert login_user.email == EXISTS_GOOGLE_USER_EMAIL
    assert user_data.user_id == EXISTS_GOOGLE_USER_ID


@pytest.mark.asyncio
async def test_base_login__success(auth_service, get_db_session):
    username = "test_username"
    password = "test_password"

    query = insert(UserProfileModel).values(username=username, password=password)
    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
        await session.flush()
        login_user = (
            await session.execute(
                select(UserProfileModel).where(UserProfileModel.username == username)
            )
        ).scalar_one_or_none()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id
