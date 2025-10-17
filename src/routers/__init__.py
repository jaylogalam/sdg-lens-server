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

def register_router(app: FastAPI) -> None:
    from .auth_router import router as auth_router
    app.include_router(auth_router)

    from .profile_router import router as profile_router
    app.include_router(profile_router)