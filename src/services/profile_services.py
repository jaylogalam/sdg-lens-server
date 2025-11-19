from supabase import Client

class ProfileServices:
    @staticmethod
    def get_profile_data(db: Client):
        response = db.table("profiles").select("*").execute()
        results = getattr(response, "data", None)

        if not results or len(results) == 0:
            raise ValueError("No data")
        
        return results
