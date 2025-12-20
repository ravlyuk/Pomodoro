from sqlalchemy import delete, select, update, insert
from sqlalchemy.orm import Session


from models import TasksModel, CategoriesModel
from schema import TasksCreateSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_tasks(self) -> list[TasksModel]:
        async with self.db_session as session:
            tasks: list[TasksModel] = list(
                (await session.execute(select(TasksModel)))
                .scalars().all()
            )
        return tasks

    async def get_task_by_id(self, task_id: int) -> TasksModel | None:
        query = select(TasksModel).where(TasksModel.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TasksCreateSchema, user_id: int) -> TasksModel:
        new_task = TasksModel(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id,
        )
        with self.db_session as session:
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(TasksModel).where(
            TasksModel.id == task_id, TasksModel.user_id == user_id
        )
        async with self.db_session as session:
            await session.execute(query)
            session.commit()

    async def get_tasks_by_category_name(self, category_name: str) -> list[TasksModel]:
        query = (
            select(TasksModel)
            .join(CategoriesModel, TasksModel.category_id == CategoriesModel.id)
            .where(CategoriesModel.name == category_name)
        )
        async with self.db_session as session:
            tasks: list[TasksModel] = list(session.execute(query).scalars().all())
        return tasks

    async def update_task_name(self, task_id: int, new_name: str) -> TasksModel | None:
        query = (
            update(TasksModel)
            .where(TasksModel.id == task_id)
            .values(name=new_name)
            .returning(TasksModel.id)
        )
        async with self.db_session as session:
            task_id_: int = await session.execute(query).scalar_one_or_none()
            await session.commit()
            await session.flush()
            return await self.get_task_by_id(task_id_)

    async def get_user_task(self, user_id: int, task_id: int) -> TasksModel | None:
        query = select(TasksModel).where(
            TasksModel.id == task_id, TasksModel.user_id == user_id
        )
        async with self.db_session as session:
            task = await session.execute(query).scalar_one_or_none()
        return task
