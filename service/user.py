from dataclasses import dataclass

from exceptions import UserAlreadyExistsException
from repository import UserRepository
from schema import UserLoginSchema
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository  # Replace 'any' with the actual UserRepository type
    auth_service: AuthService  # Replace 'any' with the actual AuthService type

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExistsException(username=username)

        user = self.user_repository.create_user(username=username, password=password)

        access_token = self.auth_service.generate_access_token(user_id=user.id)

        return UserLoginSchema(user_id=user.id, access_token=access_token)
