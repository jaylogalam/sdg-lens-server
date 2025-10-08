# Server entry file
from fastapi import FastAPI, Response

app = FastAPI()

# Routers
from routers import text_router
app.include_router(text_router)

# Root function
@app.get("/")
def read_root():
    return Response("Server is running")