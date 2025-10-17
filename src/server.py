# This is the main entry point of the FastAPI server.
from fastapi import FastAPI
from core import AuthMiddleware

app = FastAPI()

app.middleware("http")(AuthMiddleware())

# Import and register all API routers from the 'core' module.
from routers import register_router
register_router(app)

# Root endpoint
@app.get("/")
def read_root() -> str:
    return "Server is running"