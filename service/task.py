from dataclasses import dataclass

from sqlalchemy import delete
from models import TasksModel
from repository import TaskCache, TaskRepository
from schema import TasksRetrieveSchema, TasksCreateSchema
from exceptions import TaskNotFoundException


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TasksRetrieveSchema]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_schema = [TasksRetrieveSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)  # type: ignore
            return tasks_schema

    async def create_task(self, body: TasksCreateSchema, user_id: int) -> TasksRetrieveSchema:
        new_task = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task_by_id(new_task.id)
        return TasksRetrieveSchema.model_validate(task)

    async def update_task_name(
        self, task_id: int, name: str, user_id: int
    ) -> TasksRetrieveSchema | None:
        task = await self.task_repository.get_user_task(user_id, task_id)
        if task is None:
            raise TaskNotFoundException
        task = await self.task_repository.update_task_name(task_id, name)
        return TasksRetrieveSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id, task_id)
        if task is None:
            raise TaskNotFoundException
        
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)