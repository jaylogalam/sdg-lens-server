"""App router
Registers all router modules to the main FastAPI application.

Routers are imported from the features package

register_router():
    This function imports routers (e.g., convert_router) from the features package
    and attaches them to the given FastAPI app instance using include_router().
"""

from fastapi import FastAPI

def register_router(app: FastAPI) -> None:
    from features import convert_router
    app.include_router(convert_router)

    from features import signup_router
    app.include_router(signup_router)