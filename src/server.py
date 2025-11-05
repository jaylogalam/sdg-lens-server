# This is the main entry point of the FastAPI server.
from fastapi import FastAPI
from core.middleware import Middleware
from core.routers import Routers
from routers.auth_router import router as AuthRouter

app = FastAPI()

# Register middlewares
Middleware.register(app)

# Import and register all API routers from the 'core' module.
Routers.register(app)


# Root endpoint
@app.get("/")
def read_root() -> str:
    return "Server is running"

class Routers:
    @staticmethod
    def register(app):
        app.include_router(AuthRouter)