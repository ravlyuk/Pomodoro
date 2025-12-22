from pydantic import BaseModel


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str
