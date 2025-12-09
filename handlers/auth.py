from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response

from dependency import get_auth_service
from exceptions import UserNotCorrectPasswordException, UserNotFoundException
from schema import UserLoginSchema
from schema.user import UserCreateSchema
from service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginSchema:
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
