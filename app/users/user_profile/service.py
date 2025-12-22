from dataclasses import dataclass

from app.exceptions import UserAlreadyExistsException
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema


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
