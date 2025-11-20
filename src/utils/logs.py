from db.supabase import db_admin
from typing import Optional, Any

db = db_admin()

def create_log(
    type: str,
    description: str,
    user_id: Any,
    endpoint: str,
    data: Optional[dict[str, Any]] = None,
    error: Optional[str] = None
):
    details: Any = {
        "user_id": user_id,
        "endpoint": endpoint,
    }

    if data:
        details['data'] = data

    if error:
        details['error'] = error

    new_log: Any = {
        "type": type,
        "description": description,
        "details": details
    }
    
    db.table("logs").insert(new_log).execute() # type: ignore
    return