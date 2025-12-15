from fastapi import Depends, HTTPException, Request, Security, security
import httpx
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from client import GoogleClient
from database import get_db_session
from cache import get_redis_connection
from exceptions import TokenExpiredException, TokenNotCorrectException
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService, AuthService
from settings import Settings


# Dependency Repositories


async def get_task_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TaskRepository:
    return TaskRepository(db_session=db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


# Dependency Services


async def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: TaskCache = Depends(get_tasks_cache_repository),
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=await get_async_client())


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(), 
        google_client=google_client,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service,
    )


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int | None:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except (TokenExpiredException, TokenNotCorrectException) as e:
        raise HTTPException(status_code=401, detail=e.detail)

    return user_id
