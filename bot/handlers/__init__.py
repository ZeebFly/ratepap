from .start import router as start_router
from .submit import router as submit_router
from .admin import router as admin_router
from .admin_settings import router as admin_settings_router

def get_routers():
    return [start_router, submit_router, admin_router, admin_settings_router]
