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
    from .auth_router import router as signup_router
    app.include_router(signup_router)