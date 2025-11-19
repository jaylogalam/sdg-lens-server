from db.supabase import db_admin

db = db_admin()

class AuthUtils:
    @staticmethod
    def check_username_exists(username: str) -> bool:
        print(f"Checking if {username} exists...")
        results = db.table("profiles").select("id").eq("username", username).limit(1).execute()
        data = getattr(results, "data", None)
        return bool(data and len(data) > 0)

    @staticmethod
    def check_email_exists(email: str) -> bool:
        print(f"Checking if {email} exists...")
        results = db.table("profiles").select("id").eq("email", email).limit(1).execute()
        data = getattr(results, "data", None)
        return bool(data and len(data) > 0)

    