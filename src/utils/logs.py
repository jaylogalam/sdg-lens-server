from enum import StrEnum
from db.supabase import db_admin

db = db_admin()

class Type(StrEnum):
    log = "LOG"
    error = "ERROR"

def create_log(
    type: Type,
    description: str,
    user_id: str,
    status_code: str,
    data: dict[str, str]
):
    new_log: dict[str, str | dict[str, str | dict[str, str]]] = {
        "type": type,
        "description": description,
        "details": {
            "user_id": user_id,
            "status_code": status_code,
            "data": data
        }
    }
    
    db.table("logs").insert(new_log).execute()
    return