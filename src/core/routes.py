from fastapi import FastAPI
from features.convert import convert_router

def register_routes(app: FastAPI) -> None:
    app.include_router(convert_router)