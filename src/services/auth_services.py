from supabase import Client

class AuthServices:
    class User:
        
        @staticmethod
        def get_user(db: Client):
            user = db.auth.get_user()
            return user.user if user else None
            
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
            if response.user is None:
                raise ValueError("Failed to create user")

            # Initialize user profile
            user = response.user
            
            db.table("profiles").insert({
                "id": user.id,
                "username": username,
                "email": email
            }).execute()

    class Login:
        @staticmethod
        def with_password(db: Client, email: str, password: str):
            if not AuthServices.Utils.check_email_exists(db, email):
                raise ValueError("Email does not exist")
            
            auth_response = db.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if auth_response.user is None:
                raise ValueError("Incorrect password")

            return auth_response

    class Logout:
        @staticmethod
        def __call__(db: Client) -> None:
            db.auth.sign_out()

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
        