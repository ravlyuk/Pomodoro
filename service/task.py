from dataclasses import dataclass
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from schema.task import TasksRetrieveSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TasksRetrieveSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)  # type: ignore
            return tasks_schema
