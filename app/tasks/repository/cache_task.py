from redis import asyncio as Redis

from app.tasks.schema import TasksBaseSchema, TasksRetrieveSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TasksRetrieveSchema]:
        async with self.redis as redis:
            task_json = await redis.lrange("tasks", 0, -1)
            return [
                TasksRetrieveSchema.model_validate_json(task.decode("utf-8"))
                for task in task_json
            ]

    async def set_tasks(self, tasks: list[TasksBaseSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush("tasks", *tasks_json)
