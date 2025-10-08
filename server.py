# Server entry file
from fastapi import FastAPI
from supabase_db import db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def read_test():
    data = db.table("main").select("*").execute()
    return {"data": data.data}