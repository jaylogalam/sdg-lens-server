# This is the main entry point of the FastAPI server.
from fastapi import FastAPI
from core.middleware import Middleware
from core.routers import Routers

app = FastAPI()

# Register middlewares
Middleware.register(app)

# Import and register all API routers from the 'core' module.
Routers.register(app)

# Root endpoint
@app.get("/")
def read_root() -> str:
    return "Server is running"