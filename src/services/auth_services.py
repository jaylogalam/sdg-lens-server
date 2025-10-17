from supabase import Client
from fastapi.responses import RedirectResponse

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

            if not auth_response.session or not auth_response.session.access_token:
                raise ValueError("No access token returned")
            
            access_token = auth_response.session.access_token
            response = RedirectResponse('', status_code=303)
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
            return response

    class Logout:
        @staticmethod
        def logout(db: Client):
            db.auth.sign_out()
            response = RedirectResponse('', status_code=303)
            response.delete_cookie(key='access_token')
            return "Logged out"

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
        