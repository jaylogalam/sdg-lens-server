# Server entry file
from fastapi import FastAPI

app = FastAPI()

# Register routes
from core import register_routes
register_routes(app)

# Root function
@app.get("/")
def read_root():
    return "Server is running"