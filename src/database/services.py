from .supabase import client as db

def read_item(table: str) -> list[dict]:
    response = db.table(table).select("*").execute()
    return response.data

def create_item(table: str, data: dict) -> None:
    response = db.table(table).insert(data).execute()

def update_item(table: str, id: str, column: str) -> None:
    ...

def delete_item(table: str, id: str) -> None:
    response = db.table(table).delete().eq("id", id).execute()