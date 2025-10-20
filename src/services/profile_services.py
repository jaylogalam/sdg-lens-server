from supabase import Client

class ProfileServices:
    @staticmethod
    def get_profile_data(db: Client, user_id: str):
        print("Getting user data...")
        response = db.table("profiles").select("*").eq("id", user_id).limit(1).execute()
        print(response)
        results = getattr(response, "data", None)

        if not results or len(results) == 0:
            raise ValueError("No data")
        
        return results

    @staticmethod
    def get_profile_data_admin(db: Client, user_id: str):
        user = db.table("profiles").select("role").eq("id", user_id).limit(1).execute()
        role = user.data[0]['role'] # type: ignore

        if not role or role != 'admin':
            raise ValueError("Requires admin")

        response = db.table("profiles").select("*").execute()

        return response