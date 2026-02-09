from .start import router as start_router
from .submit import router as submit_router
from .admin import router as admin_router
from .deeplink import router as deeplink_router

def get_routers():
    return [start_router, submit_router, admin_router, deeplink_router]
