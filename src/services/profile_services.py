from supabase import Client
from models import ProfileModel

class ProfileServices:
    @staticmethod
    def get_profile(db: Client, user_id: str):
        session = db.auth.get_user()
        return session
        
        results = db.table("profiles").select("*").eq("id", user_id).limit(1).execute()
        data = getattr(results, "data", None)
        
        if not data or len(data) == 0:
            raise ValueError("Profile not found")
        
        profile_data = data[0]
        # return ProfileModel(**profile_data)