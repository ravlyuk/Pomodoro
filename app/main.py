from fastapi import FastAPI

from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router
from app.tasks.handlers import router as tasks_router


app = FastAPI()

routers = [auth_router, user_router, tasks_router]
for router in routers:
    app.include_router(router=router)
