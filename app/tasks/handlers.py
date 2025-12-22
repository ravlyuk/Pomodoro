from typing_extensions import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response

from app.exceptions import TaskNotFoundException
from app.dependency import get_request_user_id, get_task_repository, get_task_service
from app.tasks.schema import TasksRetrieveSchema, TasksCreateSchema
from app.tasks.service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return await task_service.get_tasks()


@router.post("/")
async def create_task(
    body: TasksCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
) -> TasksRetrieveSchema:
    task = await task_service.create_task(body, user_id)
    return task


@router.patch("/{task_id}")
async def path_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
) -> TasksRetrieveSchema | None:
    try:
        return await task_service.update_task_name(
            task_id=task_id, name=name, user_id=user_id
        )
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
        return "success"
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
