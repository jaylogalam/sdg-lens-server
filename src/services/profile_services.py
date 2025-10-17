from supabase import Client

class ProfileServices:
    @staticmethod
    def get_profile_data(db: Client, user_id: str):
        response = db.table("profiles").select("*").eq("id", user_id).limit(1).execute()
        results = getattr(response, "data", None)

        if not results or len(results) == 0:
            raise ValueError("No data")
        
        return results