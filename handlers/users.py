from fastapi import APIRouter, Depends, HTTPException

from dependency import get_user_service
from exceptions import UserAlreadyExistsException
from schema.user import UserCreateSchema, UserLoginSchema
from service.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
async def create_user(
    body: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserLoginSchema:
    try:
        return user_service.create_user(username=body.username, password=body.password)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=e.detail)
