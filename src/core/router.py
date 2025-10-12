# Registers all route modules to the main FastAPI application.

from fastapi import FastAPI

# This function imports routers (e.g., convert_router) from the features package
# and attaches them to the given FastAPI app instance using include_router().

def register_router(app: FastAPI) -> None:
    from features import convert_router
    app.include_router(convert_router)