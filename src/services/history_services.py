from supabase import Client
from datetime import datetime


class HistoryServices:
    class Create:
        @staticmethod
        def record_action(
             db: Client,
             id: str,
             action: str,
             raw_text: str,
             user_id: str;
        ):
        
            result = db.table("item_history").insert({ # type: ignore
                "id": id,
                "action": action,
                "raw_text": raw_text,
                "user_id": user_id,
                "created_at": datetime.now().isoformat()
            }).execute()

            if not getattr(result, "data", None):
                raise ValueError("Failed to log user history")

            return result.data[0]

