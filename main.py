from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from handlers import routers

app = FastAPI()


for router in routers:
    app.include_router(router=router)
