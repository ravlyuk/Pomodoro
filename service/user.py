from dataclasses import dataclass
import random
import string

from exceptions import UserAlreadyExistsException
from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository  # Replace 'any' with the actual UserRepository type

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExistsException(username=username)

        access_token = self._generate_access_token()
        user = self.user_repository.create_user(
            username=username, password=password, access_token=access_token
        )
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(10)
        )
