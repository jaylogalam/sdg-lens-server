# services/analyze_services.py
from supabase import Client
from utils.history import add_to_history

class AnalyzeServices:
    @staticmethod
    def analyze_text(db: Client, text: str, uid: str) -> dict:
        # ... your existing code unchanged ...
        add_to_history(db, uid, text, results)
        return results

    @staticmethod
    def get_history(db: Client, user_id: str):
        res = (
            db.table("history")
            .select("*")
            .eq("user_id", user_id)           # ✅ only this user's history
            .order("created_at", desc=True)   # ✅ newest first (if you have created_at)
            .execute()
        )

        return res.data or []                # ✅ JSON-serializable list
