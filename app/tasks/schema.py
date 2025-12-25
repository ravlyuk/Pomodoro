from pydantic import BaseModel, ConfigDict, model_validator


class TasksBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    pomodoro_count: int
    category_id: int
    user_id: int

    @model_validator(mode="after")
    def check_came_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count is required")
        return self


class TasksRetrieveSchema(TasksBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None


class TasksCreateSchema(BaseModel):
    name: str
    pomodoro_count: int
    category_id: int
