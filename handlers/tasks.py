from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response

from database.models import TasksModel
from dependency import get_task_repository, get_task_service
from repository import TaskRepository
from repository.cache_task import TaskCache
from schema.task import TasksBaseSchema, TasksRetrieveSchema
from service.task import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return task_service.get_tasks()


@router.post("/", response_model=TasksRetrieveSchema)
async def create_task(
    task: TasksBaseSchema,
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
):
    created_task = task_repo.create_task(task)
    return created_task


@router.patch("/{task_id}", response_model=TasksRetrieveSchema)
async def path_task(
    task_id: int,
    name: str,
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
):
    task = task_repo.update_task_name(task_id, name)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
):
    task = task_repo.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_repo.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
