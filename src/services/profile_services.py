from supabase import Client
from services.auth_services import AuthServices

class ProfileServices:
    @staticmethod
    def get_profile_data(db: Client):
        response = db.table("profiles").select("*").execute()
        results = getattr(response, "data", None)

        if not results or len(results) == 0:
            raise ValueError("No data")
        
        return results

    @staticmethod
    def edit_username(db: Client, admin: Client, name: str):
        previous = db.table("profiles").select("username").execute()
        previous = getattr(previous, "data", None)
        previous = previous[0]['username']

        if AuthServices.Utils.check_username_exists(admin, previous):
            raise ValueError("Username already exists")
        
        response = db.table("profiles").update({"username": name}).eq("username", previous).execute()
        return "Success"