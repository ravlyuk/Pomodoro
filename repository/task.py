from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from database import TasksModel, CategoriesModel, get_db_session
from schema.task import TasksBaseSchema, TasksRetrieveSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> list[TasksModel]:
        with self.db_session as session:
            tasks: list[TasksModel] = list(
                session.execute(select(TasksModel)).scalars().all()
            )
        return tasks

    def get_task_by_id(self, task_id: int) -> TasksModel | None:
        query = select(TasksModel).where(TasksModel.id == task_id)
        with self.db_session as session:
            task = session.execute(query).scalar_one_or_none()
        return task

    def create_task(self, task: TasksBaseSchema) -> TasksModel:
        new_task = TasksModel(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
        )
        with self.db_session as session:
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task

    def delete_task(self, task_id: int) -> None:
        query = delete(TasksModel).where(TasksModel.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[TasksModel]:
        query = (
            select(TasksModel)
            .join(CategoriesModel, TasksModel.category_id == CategoriesModel.id)
            .where(CategoriesModel.name == category_name)
        )
        with self.db_session as session:
            tasks: list[TasksModel] = list(session.execute(query).scalars().all())
        return tasks

    def update_task_name(self, task_id: int, new_name: str) -> TasksModel | None:
        query = (
            update(TasksModel)
            .where(TasksModel.id == task_id)
            .values(name=new_name)
            .returning(TasksModel)
        )
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()
