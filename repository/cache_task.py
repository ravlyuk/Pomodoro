from redis import Redis

from schema.task import TasksBaseSchema, TasksRetrieveSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TasksRetrieveSchema]:
        with self.redis as redis:
            task_json = redis.lrange("tasks", 0, -1)
            return [
                TasksRetrieveSchema.model_validate_json(task.decode("utf-8"))
                for task in task_json # type: ignore
            ]
 
    def set_tasks(self, tasks: list[TasksBaseSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)
