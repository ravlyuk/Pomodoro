from dataclasses import dataclass

from exceptions import UserNotFoundException, UserNotCorrectPasswordException
from models import UserProfileModel, user
from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository  # Replace 'any' with the actual UserRepository type

    def login(self, username: str, password: str) -> UserLoginSchema | None:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfileModel | None, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
 