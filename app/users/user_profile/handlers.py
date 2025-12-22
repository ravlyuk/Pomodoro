from fastapi import APIRouter, Depends, HTTPException

from app.dependency import get_user_service
from app.exceptions import UserAlreadyExistsException
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
async def create_user(
    body: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserLoginSchema:
    try:
        return await user_service.create_user(
            username=body.username, password=body.password
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=e.detail)
