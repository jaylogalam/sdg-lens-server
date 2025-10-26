from supabase import Client

class ProfileServices:
    @staticmethod
    def get_profile_data(db: Client):
        response = db.table("profiles").select("*").execute()
        results = getattr(response, "data", None)

        if not results or len(results) == 0:
            raise ValueError("No data")
        
        return results

    @staticmethod
    def get_profile_data_admin(db: Client):
        user = db.table("profiles").select("role").limit(1).execute()
        role = user.data[0]['role'] # type: ignore

        if not role or role != 'admin':
            raise ValueError("Requires admin")

        response = db.table("profiles").select("*").execute()

        return response