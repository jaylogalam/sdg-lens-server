# Server entry file
from fastapi import FastAPI, Response

app = FastAPI()

# Routers
from routers.text import router as text_route
app.include_router(text_route)

# Tests
from tests.route import router as test_route
app.include_router(test_route)

# Root function
@app.get("/")
def read_root():
    return Response("Server is running")