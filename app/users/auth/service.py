from dataclasses import dataclass
import datetime as dt

from jose import JWTError, jwt

from app.users.auth.clients.google import GoogleClient
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfileModel
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema
from app.settings import Settings
from app.exceptions import (
    TokenExpiredException,
    TokenNotCorrectException,
    UserNotFoundException,
    UserNotCorrectPasswordException,
)


@dataclass
class AuthService:
    settings: Settings
    user_repository: UserRepository  # Replace 'any' with the actual UserRepository type
    google_client: GoogleClient

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.google_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = await self.generate_access_token(user_id=user.id)
            print("user login - access_token", access_token)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name,
        )

        created_user = await self.user_repository.create_user(create_user_data)
        access_token = await self.generate_access_token(user_id=created_user.id)
        print("new user created - access_token", access_token)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException
        await self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    async def _validate_auth_user(user: UserProfileModel | None, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: str | None) -> str:
        expires_date_unix = (dt.datetime.now() + dt.timedelta(days=7)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "expire": expires_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> str | None:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM],
            )
        except JWTError:
            raise TokenNotCorrectException

        print(payload)
        if payload["expire"] < dt.datetime.now().timestamp():
            raise TokenExpiredException
        return payload.get("user_id")
