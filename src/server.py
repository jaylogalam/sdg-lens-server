# Server entry file
from fastapi import FastAPI

app = FastAPI()

# Register router
from core import register_router
register_router(app)

# Root function
@app.get("/")
def read_root() -> str:
    return "Server is running"