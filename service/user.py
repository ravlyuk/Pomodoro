from dataclasses import dataclass

from exceptions import UserAlreadyExistsException
from repository import UserRepository
from schema import UserLoginSchema
from schema import UserCreateSchema
from service.auth import AuthService

@dataclass
class UserService:
    user_repository: UserRepository  # Replace 'any' with the actual UserRepository type
    auth_service: AuthService  # Replace 'any' with the actual AuthService type

    async def create_user(self, username: str, password: str) -> UserLoginSchema:

        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExistsException(username=username)

        user_data_create = UserCreateSchema(username=username, password=password)
        user = await self.user_repository.create_user(user_data_create)
        access_token = self.auth_service.generate_access_token(user_id=user.id)

        return UserLoginSchema(user_id=user.id, access_token=access_token)
