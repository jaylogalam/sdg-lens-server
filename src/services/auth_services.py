from supabase import Client
from fastapi.responses import JSONResponse

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(db: Client, admin: Client, username: str, email: str, password: str):
            if AuthServices.Utils.check_username_exists(admin, username):
                raise ValueError("Username already exists")
            
            if AuthServices.Utils.check_email_exists(admin, email):
                raise ValueError("Email already exists")
            
            # Sign up the user
            auth_response = db.auth.sign_up({
                "email": email,
                "password": password
            })

            # Initialize user profile
            if auth_response.user is None:
                raise ValueError("Failed to create user")

            user = auth_response.user
            
            db.table("profiles").insert({
                "id": user.id,
                "username": username,
                "email": email
            }).execute()

            # Set session
            response = AuthServices.Login.with_password(
                db=db,
                admin=admin,
                email=email,
                password=password
            )
            
            return response

    class Login:
        @staticmethod
        def with_password(db: Client, admin: Client, email: str, password: str):
            if not AuthServices.Utils.check_email_exists(admin, email):
                raise ValueError("Email does not exist")
            
            auth_response = db.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.session or not auth_response.session.access_token:
                raise ValueError("No access token returned")

            role = AuthServices.Utils.get_role(db)
            
            access_token = auth_response.session.access_token

            # Response
            response = JSONResponse({"role": role, "message": "Login successful"})

            # Set cookie with token
            response.set_cookie(
                key="access_token",
                path="/",
                value=f"Bearer {access_token}",
                httponly=True,
                secure=True,
                samesite="none"
            )
            
            return response

    class Logout:
        @staticmethod
        def logout(db: Client):
            db.auth.sign_out()
            response = JSONResponse("Logout successful")
            response.delete_cookie(
                key='access_token',
                path="/",
                httponly=True,
                secure=True,
                samesite="none"
            )
            
            return response

    class Utils:
        @staticmethod
        def check_username_exists(admin: Client, username: str) -> bool:
            print(f"Checking if {username} exists...")
            results = admin.table("profiles").select("id").eq("username", username).limit(1).execute()
            data = getattr(results, "data", None)
            return bool(data and len(data) > 0)

        @staticmethod
        def check_email_exists(admin: Client, email: str) -> bool:
            print(f"Checking if {email} exists...")
            results = admin.table("profiles").select("id").eq("email", email).limit(1).execute()
            data = getattr(results, "data", None)
            return bool(data and len(data) > 0)
        
        @staticmethod
        def get_role(db: Client):
            results = db.table("profiles").select("role").limit(1).execute()
            role = getattr(results, "data", [{"role": "anon"}])
            role = role[0]['role']
            return role
