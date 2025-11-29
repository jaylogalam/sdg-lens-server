from fastapi import FastAPI
from core.middleware import Middleware
from core.routers import Routers

app = FastAPI()

Middleware.register(app)
Routers.register(app)

@app.get("/")
def read_root() -> str:
    return "Server is running"
