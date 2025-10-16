from supabase import Client

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(db: Client, username: str, email: str, password: str):
            AuthServices.Utils.check_username_exists(db, username)
            AuthServices.Utils.check_email_exists(db, email)
            
            # Sign up the user
            response = db.auth.sign_up({
                "email": email,
                "password": password
            })

            # Initialize user profile
            user = response.user
            if not user:
                raise Exception("Signup failed: No user returned")

            response = db.table("profiles").insert({
                "id": user.id,
                "username": username,
                "email": email
            }).execute()

    class Login:
        ...

    class Utils:
        @staticmethod
        def check_username_exists(db: Client, username: str) -> None:
            results = db.table("profiles").select("id").eq("username", username).limit(1).execute()
            data = getattr(results, "data", None)
            if bool(data and len(data) > 0):
                raise ValueError("Username already exists")

        @staticmethod
        def check_email_exists(db: Client, email: str) -> None:
            results = db.table("profiles").select("id").eq("email", email).limit(1).execute()
            data = getattr(results, "data", None)
            if bool(data and len(data) > 0):
                raise ValueError("Email already exists")
        