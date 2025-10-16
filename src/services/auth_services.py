from supabase import Client

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(db: Client, username: str, email: str, password: str):
            if AuthServices.Utils.check_username_exists(db, username):
                raise ValueError("Username already exists")
            
            if AuthServices.Utils.check_email_exists(db, email):
                raise ValueError("Email already exists")
            
            # Sign up the user
            response = db.auth.sign_up({
                "email": email,
                "password": password
            })

            # Initialize user profile
            user = response.user
            if not user:
                raise Exception("Signup failed: No user returned")

            db.table("profiles").insert({
                "id": user.id,
                "username": username,
                "email": email
            }).execute()

    class Login:
        @staticmethod
        def with_password(db: Client, email: str, password: str) -> None:
            if not AuthServices.Utils.check_email_exists(db, email):
                raise ValueError("Email does not exist")
            
            db.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

    class Utils:
        @staticmethod
        def check_username_exists(db: Client, username: str) -> bool:
            results = db.table("profiles").select("id").eq("username", username).limit(1).execute()
            data = getattr(results, "data", None)
            return bool(data and len(data) > 0)

        @staticmethod
        def check_email_exists(db: Client, email: str) -> bool:
            results = db.table("profiles").select("id").eq("email", email).limit(1).execute()
            data = getattr(results, "data", None)
            return bool(data and len(data) > 0)
        