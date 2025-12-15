from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import RedirectResponse

from dependency import get_auth_service
from exceptions import UserNotCorrectPasswordException, UserNotFoundException
from schema import UserLoginSchema, UserCreateSchema
from service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginSchema:
    try:
        return await  auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/google")
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get("/google")
async def google_auth(
    code: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginSchema:
    return await auth_service.google_auth(code=code)
