from supabase import Client
from datetime import datetime
from typing import Optional, Dict, Any


class HistoryServices:
    class Create:
        @staticmethod
        def record_action(
            db: Client,
            user_id: str,
            action: str,
            item_name: str,
            details: Optional[Dict[str, Any]] = None
        ):
        
            result = db.table("item_history").insert({
                "user_id": user_id,
                "action": action,
                "item_name": item_name,
                "details": details,
                "created_at": datetime.now().isoformat()
            }).execute()

            if not getattr(result, "data", None):
                raise ValueError("Failed to log user history")

            return result.data[0]

