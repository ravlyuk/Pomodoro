from handlers.ping import router as ping_router
from handlers.tasks import router as tasks_router
from handlers.users import router as user_router
from handlers.auth import router as auth_router

routers = (
    tasks_router,
    ping_router,
    user_router,
    auth_router,
)
