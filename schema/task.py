from pydantic import BaseModel, Field, model_validator


class TasksBaseSchema(BaseModel):
    name: str
    pomodoro_count: int
    category_id: int

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_came_pomodoro_count_is_not_none(self, value: str):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count is required")
        return self


class TasksRetrieveSchema(TasksBaseSchema):
    id: int
