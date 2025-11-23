from supabase import Client
from typing import Any

def add_to_history(db: Client, user_id: str, raw_text: str, results: Any):
    response = db.table("history").insert({
        "user_id": user_id,
        "raw_text": raw_text,
        "results": results
    }).execute()

    return response
    