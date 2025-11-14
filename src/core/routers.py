""" 
"""

""" App router section
Registers all router modules to the main FastAPI application.

Routers are imported from the routers package

register_router():
    This function imports routers (e.g., convert_router) from the features package
    and attaches them to the given FastAPI app instance using include_router().
"""

from fastapi import FastAPI
from routers import (
    auth_router,
    profile_router,
    analyze_router,
    admin_router
)

class Routers:
    @staticmethod
    def register(app: FastAPI) -> None:
        app.include_router(auth_router)
        app.include_router(profile_router)
        app.include_router(analyze_router)
        app.include_router(admin_router)